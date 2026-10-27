import hmac
import logging
import threading
import time
from collections import deque

from flask import Flask, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from app.config import Settings
from app.errors import ServiceError
from app.llm import GeminiLLM
from app.schemas import ImproveRequest, ManualRequest, ReplyRequest
from app.service import AssistantService
from app.store import PostgresStore


def create_app(settings=None, store=None, llm=None):
    settings = settings or Settings.from_env()
    store = store or PostgresStore(settings.database_url)
    llm = llm or GeminiLLM(settings, store)
    service = AssistantService(store, llm)
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=64 * 1024)
    app.extensions["assistant"] = service
    recent_requests, lock = deque(), threading.Lock()
    # Provider libraries can log response details at debug; keep production quiet.
    for name in ("httpx", "httpcore", "google.genai"):
        logging.getLogger(name).setLevel(logging.WARNING)

    @app.before_request
    def authenticate():
        if request.path == "/health" and request.method == "GET":
            return None
        if not settings.reviewer_api_key:
            raise ServiceError("not_configured", "The reviewer access key is not configured.")
        supplied = request.headers.get("X-API-Key", "").encode()
        if not hmac.compare_digest(supplied, settings.reviewer_api_key.encode()):
            raise ServiceError("unauthorized", "Provide the reviewer key in X-API-Key.", 401)
        with lock:
            now = time.monotonic()
            while recent_requests and recent_requests[0] <= now - 60:
                recent_requests.popleft()
            if len(recent_requests) >= settings.requests_per_minute:
                raise ServiceError("request_limit", "Too many requests. Please wait a minute.", 429)
            recent_requests.append(now)

    @app.after_request
    def response_headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        if response.status_code == 429:
            response.headers["Retry-After"] = "60"
        return response

    def parse(schema):
        if not request.is_json:
            raise ServiceError("invalid_request", "Send application/json.", 415)
        try:
            return schema.model_validate(request.get_json())
        except ValidationError:
            # Pydantic's default error includes the original input. Don't echo PII.
            raise ServiceError(
                "invalid_request",
                "Invalid request fields or input limits exceeded. See the documented schema.",
                400,
            ) from None

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "service": "bobalab-support-api",
                "readiness": "Check authenticated generation; health reports process liveness only.",
            }
        )

    @app.post("/generate-reply")
    def generate():
        return jsonify({"aiReply": service.generate(parse(ReplyRequest))})

    @app.post("/improve-ai")
    def improve():
        return jsonify(service.improve(parse(ImproveRequest)))

    @app.post("/improve-ai-manually")
    def manual():
        return jsonify(service.manual(parse(ManualRequest)))

    @app.errorhandler(ServiceError)
    def service_error(exc):
        return jsonify({"error": {"code": exc.code, "message": exc.message}}), exc.status

    @app.errorhandler(HTTPException)
    def http_error(exc):
        return jsonify({"error": {"code": "http_error", "message": exc.name}}), exc.code

    @app.errorhandler(Exception)
    def internal_error(exc):
        # Log class only; exception messages can contain credentials or customer data.
        app.logger.error("Unexpected failure: %s", type(exc).__name__)
        return jsonify(
            {
                "error": {
                    "code": "internal_error",
                    "message": "The service could not complete the request.",
                }
            }
        ), 500

    return app
