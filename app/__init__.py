import hmac
import logging
import os
import threading
import time
from collections import deque

from flask import Flask, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Settings
from app.errors import ServiceError
from app.llm import GeminiLLM
from app.schemas import ImproveRequest, ManualRequest, ReplyRequest
from app.service import AssistantService
from app.store import PostgresStore
from app.web import register_web


def create_app(settings=None, store=None, llm=None):
    settings = settings or Settings.from_env()
    store = store or PostgresStore(settings.database_url)
    llm = llm or GeminiLLM(settings, store)
    service = AssistantService(store, llm, settings.reply_format)
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=64 * 1024)
    app.extensions["assistant"] = service
    if os.getenv("RENDER", "").lower() == "true":
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=0, x_proto=1, x_host=0, x_port=0, x_prefix=0)
    recent_requests, lock = deque(), threading.Lock()
    # Provider libraries can log response details at debug; keep production quiet.
    for name in ("httpx", "httpcore", "google.genai"):
        logging.getLogger(name).setLevel(logging.WARNING)

    def reserve_request():
        with lock:
            now = time.monotonic()
            while recent_requests and recent_requests[0] <= now - 60:
                recent_requests.popleft()
            if len(recent_requests) >= settings.requests_per_minute:
                raise ServiceError("request_limit", "Too many requests. Please wait a minute.", 429)
            recent_requests.append(now)

    @app.before_request
    def authenticate():
        if request.path == "/health" and request.method == "GET":
            return None
        if request.endpoint == "static" and request.method in ("GET", "HEAD"):
            return None
        if request.endpoint in {
            "web.index",
            "web.session_state",
            "web.login",
            "web.logout",
            "web.chat",
        }:
            return None  # Browser POST handlers enforce their own session + CSRF checks.
        if not settings.reviewer_api_key:
            raise ServiceError("not_configured", "The reviewer access key is not configured.")
        supplied = request.headers.get("X-API-Key", "").encode()
        if not hmac.compare_digest(supplied, settings.reviewer_api_key.encode()):
            raise ServiceError("unauthorized", "Provide the reviewer key in X-API-Key.", 401)
        reserve_request()

    @app.after_request
    def response_headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; "
            "base-uri 'self'; form-action 'self'; object-src 'none'"
        )
        if request.endpoint == "static":
            response.headers["Cache-Control"] = "public, max-age=3600"
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

    register_web(app, settings, service, reserve_request, parse)
    return app
