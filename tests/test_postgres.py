"""Real PostgreSQL tests. Each test gets a disposable isolated schema."""

import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from app.errors import Conflict, ServiceError
from app.prompts import seed_sections
from app.store import PostgresStore

pytestmark = pytest.mark.postgres


@pytest.fixture
def store():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to a disposable PostgreSQL database")
    schema = "test_" + uuid4().hex
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    config = conninfo_to_dict(url)
    config["options"] = f"-c search_path={schema}"
    # PostgresStore also accepts libpq connection strings; keep local TLS explicit.
    connection = make_conninfo(**config)
    result = PostgresStore(connection)
    result.migrate()
    result.seed(seed_sections())
    try:
        yield result
    finally:
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def changed(base, text="Prefer compact explanations before a checklist."):
    sections = base.sections.model_copy(deep=True)
    sections.editable_playbook[0].text = text
    return sections


def test_real_persistence_and_idempotent_startup(store):
    initial = store.active()
    result = store.commit(initial, changed(initial), "manual", "applied", [], [])
    other_connection = PostgresStore(store.url)
    assert other_connection.active().id == result.id
    assert result.id != initial.id
    store.migrate()
    assert store.seed(seed_sections()) is False
    assert store.active().id == result.id


def test_concurrent_updates_only_one_wins(store):
    base = store.active()

    def apply(index):
        try:
            return store.commit(
                base, changed(base, f"Unique test instruction {index}"), "auto", "applied", [], []
            ).id
        except Conflict:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(apply, [1, 2]))
    assert results.count("conflict") == 1
    assert len(store.history()) == 2


def test_failed_event_rolls_back_version_and_pointer(store):
    base = store.active()
    with pytest.raises(ServiceError):
        store.commit(base, changed(base), "auto", "invalid-outcome", [], [])
    assert store.active().id == base.id
    assert len(store.history()) == 1


def test_noop_logs_event_without_version(store):
    base = store.active()
    result = store.commit(base, base.sections, "auto", "no_change", [], [])
    assert result.id == base.id
    with store.connect() as conn:
        assert conn.execute("SELECT count(*) AS n FROM improvement_events").fetchone()["n"] == 1


def test_history_cannot_be_rewritten(store):
    with pytest.raises(ServiceError):
        with store.connect() as conn:
            conn.execute("UPDATE prompt_versions SET source='manual'")


def test_shared_daily_call_budget_is_atomic(store):
    def reserve(_):
        try:
            store.reserve_call(3)
            return True
        except ServiceError as exc:
            assert exc.code == "daily_call_limit"
            return False

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(reserve, range(5)))
    assert sum(results) == 3


def test_all_three_routes_use_real_persistent_versions(store):
    from app import create_app
    from app.config import Settings
    from tests.fakes import ScriptedLLM

    settings = Settings(reviewer_api_key="test-key", requests_per_minute=100)
    headers = {"X-API-Key": "test-key"}
    llm = ScriptedLLM(
        {"reply": {"direct_answer": "Initial simulated reply"}, "source_ids": []},
        {
            "reply": {"direct_answer": "Prediction for simulated learning"},
            "source_ids": [],
        },
        {
            "edits": [
                {
                    "action": "add",
                    "rule_id": "define_terms",
                    "text": "Explain unfamiliar abbreviations briefly.",
                    "category": "style",
                }
            ]
        },
        {
            "edits": [
                {
                    "action": "add",
                    "rule_id": "closing",
                    "text": "End a multi-step explanation with the immediate next action.",
                    "category": "support_process",
                }
            ]
        },
    )
    client = create_app(settings, store, llm).test_client()
    assert (
        client.post(
            "/generate-reply", headers=headers, json={"clientSequence": "Hello"}
        ).status_code
        == 200
    )
    response = client.post(
        "/improve-ai",
        headers=headers,
        json={
            "clientSequence": "What does that term mean?",
            "consultantReply": "A brief explanation.",
        },
    )
    assert response.json["learningStatus"] == "applied"
    manual = client.post(
        "/improve-ai-manually",
        headers=headers,
        json={"instructions": "End a multi-step explanation with the immediate next action."},
    )
    assert manual.json["learningStatus"] == "applied"
    reconnected = PostgresStore(store.url)
    assert reconnected.active().id == manual.json["versionId"]
    assert {r.id for r in reconnected.active().sections.editable_playbook} >= {
        "define_terms",
        "closing",
    }
