import time

import pytest

from app import create_app
from app.config import Settings
from app.errors import ServiceError
from app.web import display_parts, ui_credentials
from tests.fakes import MemoryStore, ScriptedLLM

SETTINGS = Settings(reviewer_api_key="test-reviewer-key")


def web_client(*outputs, settings=SETTINGS):
    store, llm = MemoryStore(), ScriptedLLM(*outputs)
    app = create_app(settings, store, llm)
    return app.test_client(), store, llm


def enter(client):
    csrf = client.get("/ui/session").json["csrfToken"]
    result = client.post(
        "/ui/session",
        json={"accessCode": ui_credentials(SETTINGS)[0]},
        headers={"X-CSRF-Token": csrf},
    )
    assert result.status_code == 200
    assert result.json["csrfToken"] != csrf
    return {"X-CSRF-Token": result.json["csrfToken"]}


def test_public_shell_and_assets_do_not_require_or_reveal_keys():
    secret = "privileged-reviewer-key-kept-server-side"
    settings = Settings(reviewer_api_key=secret, gemini_api_key="provider-secret")
    client, _, llm = web_client(settings=settings)
    html = client.get("/")
    assert html.status_code == 200
    assert "BOBALAB" in html.text
    assert secret not in html.text and "provider-secret" not in html.text
    assert client.get("/static/app.css").status_code == 200
    js = client.get("/static/app.js")
    assert js.status_code == 200 and secret not in js.text
    assert "script-src 'self'" in html.headers["Content-Security-Policy"]
    assert html.headers["Cache-Control"] == "no-store"
    assert not llm.calls


def test_unconfigured_browser_does_not_break_liveness_or_shell():
    client, _, llm = web_client(settings=Settings())
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/ui/session").json["available"] is False
    assert not llm.calls


def test_browser_code_and_session_signing_are_distinct_from_reviewer_key():
    code, signing = ui_credentials(SETTINGS)
    assert code != SETTINGS.reviewer_api_key != signing and code != signing
    assert (code, signing) == ui_credentials(SETTINGS)
    assert ui_credentials(Settings(reviewer_api_key="another-key")) != (code, signing)


def test_reusing_privileged_key_as_demo_code_disables_browser_only():
    settings = Settings(reviewer_api_key="same-code", ui_demo_access_code="same-code")
    client, _, _ = web_client(settings=settings)
    assert not client.get("/ui/session").json["available"]
    assert client.get("/health").status_code == 200


@pytest.mark.parametrize("path", ["/ui/session", "/ui/chat", "/ui/logout"])
def test_mutations_without_browser_protection_do_not_call_model(path):
    client, _, llm = web_client()
    result = client.post(path, json={})
    assert result.status_code in (401, 403)
    assert not llm.calls


def test_valid_bootstrap_csrf_alone_does_not_grant_generation():
    client, _, llm = web_client()
    csrf = client.get("/ui/session").json["csrfToken"]
    result = client.post("/ui/chat", json={"clientSequence": "Hi"}, headers={"X-CSRF-Token": csrf})
    assert result.status_code == 401
    assert not llm.calls


def test_wrong_code_and_login_throttling_are_safe():
    client, _, llm = web_client()
    csrf = client.get("/ui/session").json["csrfToken"]
    for _ in range(5):
        result = client.post(
            "/ui/session", json={"accessCode": "wrong-private-code"}, headers={"X-CSRF-Token": csrf}
        )
        assert result.status_code == 401 and "wrong-private-code" not in result.text
    result = client.post(
        "/ui/session", json={"accessCode": "wrong-private-code"}, headers={"X-CSRF-Token": csrf}
    )
    assert result.status_code == 429 and result.headers["Retry-After"] == "60"
    assert not llm.calls


def test_cross_origin_request_with_valid_session_and_csrf_is_rejected():
    client, _, llm = web_client()
    headers = {**enter(client), "Origin": "https://unrelated.invalid"}
    assert (
        client.post("/ui/chat", json={"clientSequence": "Hi"}, headers=headers).status_code == 403
    )
    assert not llm.calls


def test_login_rotates_csrf_and_cookie_has_secure_attributes():
    settings = Settings(reviewer_api_key="test-reviewer-key", ui_secure_cookie=True)
    client, _, _ = web_client(settings=settings)
    csrf = client.get("/ui/session", base_url="https://localhost").json["csrfToken"]
    result = client.post(
        "/ui/session",
        base_url="https://localhost",
        json={"accessCode": ui_credentials(settings)[0]},
        headers={"X-CSRF-Token": csrf},
    )
    cookie = result.headers["Set-Cookie"]
    assert result.status_code == 200 and result.json["csrfToken"] != csrf
    assert "Secure" in cookie and "HttpOnly" in cookie and "SameSite=Strict" in cookie
    assert settings.reviewer_api_key not in cookie and ui_credentials(settings)[0] not in cookie


def test_ui_generation_uses_history_and_returns_exact_footer_metadata():
    client, store, llm = web_client({"reply": "A bounded answer.", "source_ids": ["kl-dtv"]})
    headers = enter(client)
    history = [{"role": "client", "message": "I am considering Kuala Lumpur."}]
    result = client.post(
        "/ui/chat", json={"clientSequence": "What next?", "chatHistory": history}, headers=headers
    )
    assert result.status_code == 200
    assert result.json["messageText"] == "A bounded answer."
    assert len(result.json["sources"]) == 1
    assert result.json["sources"][0]["url"] in result.json["aiReply"]
    assert llm.calls[0]["payload"]["conversation"]["chatHistory"] == history
    assert not store.events


def test_no_source_reply_keeps_full_text_including_untrusted_html():
    text = '<img src=x onerror="alert(1)"> is untrusted text.'
    client, _, _ = web_client({"reply": text, "source_ids": []})
    response = client.post("/ui/chat", json={"clientSequence": "Test"}, headers=enter(client))
    assert response.status_code == 200
    assert response.json == {"aiReply": text, "messageText": text, "sources": []}


def test_unrecognized_footer_is_not_removed_or_promoted_to_source():
    text = "Keep this answer.\n\nUnregistered source: https://unrelated.invalid"
    assert display_parts(text, MemoryStore().active().sections.reviewed_knowledge["sources"]) == (
        text,
        [],
    )


@pytest.mark.parametrize("path", ["/generate-reply", "/improve-ai", "/improve-ai-manually"])
def test_browser_session_cannot_authorize_privileged_api_routes(path):
    client, _, llm = web_client()
    enter(client)
    assert client.post(path, json={}).status_code == 401
    assert not llm.calls


def test_browser_access_code_is_not_a_privileged_api_key():
    client, _, llm = web_client()
    result = client.post(
        "/generate-reply",
        json={"clientSequence": "Hi"},
        headers={"X-API-Key": ui_credentials(SETTINGS)[0]},
    )
    assert result.status_code == 401 and not llm.calls


def test_cookie_does_not_relax_csrf_and_original_api_still_works():
    client, _, llm = web_client({"reply": "API reply.", "source_ids": []})
    enter(client)
    assert client.post("/ui/chat", json={"clientSequence": "Hi"}).status_code == 403
    response = client.post(
        "/generate-reply",
        json={"clientSequence": "Hi"},
        headers={"X-API-Key": SETTINGS.reviewer_api_key},
    )
    assert response.status_code == 200 and len(llm.calls) == 1


def test_browser_and_original_api_share_request_allowance():
    settings = Settings(reviewer_api_key="test-reviewer-key", requests_per_minute=1)
    client, _, llm = web_client({"reply": "API reply.", "source_ids": []}, settings=settings)
    headers = enter(client)
    assert (
        client.post(
            "/generate-reply",
            json={"clientSequence": "Hi"},
            headers={"X-API-Key": SETTINGS.reviewer_api_key},
        ).status_code
        == 200
    )
    assert (
        client.post("/ui/chat", json={"clientSequence": "Hi"}, headers=headers).status_code == 429
    )
    assert len(llm.calls) == 1


def test_expired_session_does_not_call_model():
    client, _, llm = web_client()
    headers = enter(client)
    with client.session_transaction() as data:
        data["authenticated_at"] = time.time() - 1801
    response = client.post("/ui/chat", json={"clientSequence": "Hi"}, headers=headers)
    assert response.status_code == 401 and not llm.calls


def test_logout_clears_browser_grant():
    client, _, llm = web_client()
    headers = enter(client)
    result = client.post("/ui/logout", json={}, headers=headers)
    assert result.status_code == 200 and not result.json["authenticated"]
    assert (
        client.post("/ui/chat", json={"clientSequence": "Hi"}, headers=headers).status_code == 401
    )
    assert not llm.calls


def test_invalid_browser_context_does_not_reach_model():
    client, _, llm = web_client()
    result = client.post(
        "/ui/chat",
        json={
            "clientSequence": "Hi",
            "chatHistory": [{"role": "assistant", "message": "Wrong role"}],
        },
        headers=enter(client),
    )
    assert result.status_code == 400 and not llm.calls


def test_provider_failure_is_an_error_not_a_fabricated_answer():
    client, _, _ = web_client(ServiceError("model_unavailable", "Unavailable.", 503))
    result = client.post("/ui/chat", json={"clientSequence": "Hi"}, headers=enter(client))
    assert result.status_code == 503 and result.json["error"]["code"] == "model_unavailable"


def test_operator_access_file_is_private_and_code_not_printed(tmp_path, monkeypatch, capsys):
    import app.cli

    monkeypatch.setattr(app.cli, "ROOT", tmp_path)
    monkeypatch.setattr(app.cli, "configured_service", lambda: (SETTINGS, None, None))
    monkeypatch.setattr("sys.argv", ["app.cli", "write-web-access"])
    assert app.cli.main() == 0
    path = tmp_path / "work" / "WEB_DEMO_ACCESS.txt"
    assert path.stat().st_mode & 0o777 == 0o600
    assert ui_credentials(SETTINGS)[0] in path.read_text()
    assert SETTINGS.reviewer_api_key not in path.read_text()
    assert ui_credentials(SETTINGS)[0] not in capsys.readouterr().out


def test_render_forwarded_https_origin_is_recognized(monkeypatch):
    monkeypatch.setenv("RENDER", "true")
    client, _, _ = web_client()
    headers = {"X-Forwarded-Proto": "https"}
    csrf = client.get("/ui/session", headers=headers).json["csrfToken"]
    result = client.post(
        "/ui/session",
        json={"accessCode": ui_credentials(SETTINGS)[0]},
        headers={**headers, "Origin": "https://localhost", "X-CSRF-Token": csrf},
    )
    assert result.status_code == 200
