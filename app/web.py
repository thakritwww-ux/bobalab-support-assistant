"""Generation-only browser sessions; privileged API keys never reach the client."""

import hashlib
import hmac
import secrets
import threading
import time
from collections import deque
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlsplit

from flask import Blueprint, jsonify, render_template, request, session
from pydantic import Field

from app.errors import ServiceError
from app.schemas import ReplyRequest, StrictModel


class DemoLogin(StrictModel):
    accessCode: str = Field(min_length=1, max_length=128)


def ui_credentials(settings):
    """Domain-separated defaults avoid a new deployment secret dependency.

    Explicit UI-only values can decouple browser access from reviewer-key rotation.
    The browser receives neither the base reviewer key nor the signing secret.
    """
    if not settings.reviewer_api_key:
        return "", ""
    key = settings.reviewer_api_key.encode()
    digest = hmac.new(key, b"bobalab/demo-access/v1", hashlib.sha256).hexdigest()[:20]
    derived_code = "-".join(digest[i : i + 4] for i in range(0, 20, 4))
    code = settings.ui_demo_access_code or derived_code
    signing = (
        settings.ui_session_secret
        or hmac.new(key, b"bobalab/session-signing/v1", hashlib.sha256).hexdigest()
    )
    if code == settings.reviewer_api_key or not 8 <= len(code) <= 128 or len(signing) < 32:
        return "", ""
    return code, signing


def display_parts(reply, sources):
    """Separate only the exact citation footer emitted by AssistantService.

    This does not reinterpret, summarize or rewrite the model's advice.
    """
    known = {}
    for source in sources:
        host = urlsplit(source["url"]).hostname or ""
        if not source["url"].startswith("https://") or not (
            host.endswith(".go.th") or host.endswith(".thaiembassy.org")
        ):
            continue
        footer = f"{source['title']} (reviewed {source['reviewed_at']}): {source['url']}"
        known[footer] = {
            "title": source["title"],
            "url": source["url"],
            "reviewedAt": source["reviewed_at"],
            "scope": source["country_scope"],
        }
    body, separator, tail = reply.rpartition("\n\n")
    lines = tail.splitlines()
    if separator and body and lines and len(lines) <= 3 and all(line in known for line in lines):
        return body, [known[line] for line in lines]
    return reply, []


def register_web(app, settings, service, reserve_request, parse):
    code, signing = ui_credentials(settings)
    app.config.update(
        SECRET_KEY=signing or secrets.token_hex(32),
        SESSION_COOKIE_NAME="bobalab_demo",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=settings.ui_secure_cookie,
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_REFRESH_EACH_REQUEST=False,
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    )
    web = Blueprint("web", __name__)
    assets = Path(app.static_folder)
    asset_version = hashlib.sha256(
        (assets / "app.css").read_bytes() + (assets / "app.js").read_bytes()
    ).hexdigest()[:12]
    login_attempts, login_lock = deque(), threading.Lock()

    def authenticated():
        issued = session.get("authenticated_at")
        valid = isinstance(issued, (int, float)) and 0 <= time.time() - issued < 1800
        if not valid:
            session.pop("authenticated_at", None)
        return valid

    def state():
        csrf = session.get("csrf")
        if not isinstance(csrf, str):
            csrf = secrets.token_urlsafe(32)
            session["csrf"] = csrf
        return {"authenticated": authenticated(), "csrfToken": csrf, "available": bool(code)}

    def protect(*, require_auth=True):
        if not code:
            raise ServiceError("ui_not_configured", "Demo access is not configured.", 503)
        origin = request.headers.get("Origin")
        if origin and origin.rstrip("/") != request.host_url.rstrip("/"):
            raise ServiceError("csrf_failed", "Please reopen the demo and try again.", 403)
        if require_auth and not authenticated():
            raise ServiceError("ui_session_expired", "Open demo access again to continue.", 401)
        supplied, expected = request.headers.get("X-CSRF-Token", ""), session.get("csrf", "")
        if (
            not supplied
            or not expected
            or not hmac.compare_digest(supplied.encode(), expected.encode())
        ):
            raise ServiceError("csrf_failed", "Please reopen the demo and try again.", 403)

    @web.get("/")
    def index():
        return render_template("index.html", asset_version=asset_version)

    @web.get("/ui/session")
    def session_state():
        return jsonify(state())

    @web.post("/ui/session")
    def login():
        protect(require_auth=False)
        with login_lock:
            now = time.monotonic()
            while login_attempts and login_attempts[0] <= now - 60:
                login_attempts.popleft()
            if len(login_attempts) >= 5:
                raise ServiceError(
                    "request_limit", "Please wait a minute before trying access again.", 429
                )
            login_attempts.append(now)
        supplied = parse(DemoLogin).accessCode
        if not hmac.compare_digest(supplied.encode(), code.encode()):
            raise ServiceError("invalid_demo_code", "That demo code was not recognized.", 401)
        session.clear()
        session.permanent = True
        session["authenticated_at"] = time.time()
        return jsonify(state())

    @web.post("/ui/logout")
    def logout():
        protect(require_auth=False)
        session.clear()
        return jsonify(state())

    @web.post("/ui/chat")
    def chat():
        protect()
        reserve_request()
        context = parse(ReplyRequest)
        version = service.store.active()
        reply = service.generate(context, version)
        text, sources = display_parts(reply, version.sections.reviewed_knowledge["sources"])
        return jsonify({"aiReply": reply, "messageText": text, "sources": sources})

    app.register_blueprint(web)
