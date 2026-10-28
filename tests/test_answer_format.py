"""Structured answer fixtures are synthetic, not live before/after model evidence."""

import pytest
from pydantic import ValidationError

from app import create_app
from app.answer_format import FORMAT_HASH, render_answer
from app.config import Settings
from app.errors import ServiceError
from app.llm import GeminiLLM
from app.schemas import ReplyRequest, SectionedReply
from app.service import AssistantService
from tests.fakes import MemoryStore, ScriptedLLM
from tests.test_llm import SDK


def fixture():
    return {
        "reply": {
            "direct_answer": "Compare the terms before deciding.",
            "sections": [
                {
                    "kind": "bullets",
                    "items": [
                        {"text": "Check the current guidance.", "caveat": "The scope is limited."}
                    ],
                },
                {
                    "kind": "steps",
                    "items": [{"text": "Read the terms."}, {"text": "Compare your priorities."}],
                },
                {
                    "kind": "comparison",
                    "options": [
                        {
                            "label": "Option A",
                            "benefit": "Allows changes if the terms permit.",
                            "drawback": None,
                            "uncertainty": "Check the actual conditions.",
                        },
                        {
                            "label": "Option B",
                            "benefit": None,
                            "drawback": "Changes may be restricted.",
                            "uncertainty": "Terms have not been provided.",
                        },
                    ],
                },
            ],
        },
        "source_ids": ["kl-dtv"],
    }


def test_server_builds_valid_layout_and_preserves_every_caveat():
    answer = SectionedReply.model_validate(fixture()).reply
    body = render_answer(answer)
    assert "### What to check\n\n- Check" in body
    assert "1. Read the terms.\n2. Compare" in body
    assert "| Option A |" in body
    assert "Not specified" in body
    assert "The scope is limited." in body and "Terms have not been provided." in body


@pytest.mark.parametrize(
    "section",
    [
        {"kind": "bullets", "items": []},
        {"kind": "steps", "text": "Hidden unused text", "items": [{"text": "Do this."}]},
        {"kind": "comparison", "options": [{"label": "Only one", "uncertainty": "Unknown"}]},
        {"kind": "paragraph", "text": None},
        {"kind": "comparison", "options": [{"label": "A"}, {"label": "B"}]},
        {"kind": "chart", "text": "Invented chart"},
    ],
)
def test_malformed_sections_cannot_be_silently_displayed(section):
    output = {"reply": {"direct_answer": "Answer.", "sections": [section]}, "source_ids": []}
    with pytest.raises(ValidationError):
        SectionedReply.model_validate(output)


@pytest.mark.parametrize(
    "text",
    ["**Heading** * first * second", "A\nB", "1. Step one 2. Step two", "# Heading", "- Bullet"],
)
def test_inline_layout_cannot_hide_in_a_plain_atom(text):
    with pytest.raises(ValidationError):
        SectionedReply.model_validate({"reply": {"direct_answer": text}, "source_ids": []})


def test_simple_answer_needs_no_filler_sections_or_next_step():
    result = SectionedReply.model_validate(
        {"reply": {"direct_answer": "I cannot verify it here."}, "source_ids": []}
    )
    assert render_answer(result.reply) == "I cannot verify it here."
    assert result.reply.sections == [] and result.reply.next_step is None


def test_thai_default_labels_and_unprovided_terms_are_explicit():
    output = fixture()
    output["reply"]["direct_answer"] = "เปรียบเทียบเงื่อนไขก่อนตัดสินใจ"
    body = render_answer(SectionedReply.model_validate(output).reply)
    assert "สิ่งที่ควรตรวจสอบ" in body and "ยังไม่ระบุ" in body


def test_literal_cell_pipes_cannot_create_extra_canonical_columns():
    output = fixture()
    output["reply"]["sections"][2]["options"][0]["label"] = "A | B"
    body = render_answer(SectionedReply.model_validate(output).reply)
    assert "A \\| B" in body


@pytest.mark.parametrize("field", ["https://invented.invalid", "[APP_LINK]"])
def test_link_and_placeholder_checks_cover_all_original_structured_fields(field):
    output = fixture()
    output["reply"]["sections"][2]["options"][0]["uncertainty"] = field
    service = AssistantService(MemoryStore(), ScriptedLLM(output), "sections")
    with pytest.raises(ServiceError):
        service.generate(ReplyRequest(clientSequence="Synthetic test"))


def test_unsupported_source_id_still_fails():
    output = fixture()
    output["source_ids"] = ["unreviewed"]
    with pytest.raises(ServiceError) as error:
        AssistantService(MemoryStore(), ScriptedLLM(output), "sections").generate(
            ReplyRequest(clientSequence="Test")
        )
    assert error.value.code == "unsupported_citation"


def test_generation_contract_is_still_only_aiReply_and_prompt_store_is_unchanged():
    store, llm = MemoryStore(), ScriptedLLM(fixture())
    before = store.active()
    client = create_app(
        Settings(reviewer_api_key="test-key", reply_format="sections"), store, llm
    ).test_client()
    result = client.post(
        "/generate-reply",
        headers={"X-API-Key": "test-key"},
        json={"clientSequence": "Compare options"},
    )
    assert result.status_code == 200 and set(result.json) == {"aiReply"}
    assert "### Options" in result.json["aiReply"]
    assert store.active().id == before.id and not store.events
    assert llm.calls[0]["schema"] is SectionedReply


def test_browser_metadata_and_aiReply_come_from_the_same_generation():
    store, llm = MemoryStore(), ScriptedLLM(fixture())
    app = create_app(
        Settings(
            reviewer_api_key="test-key", ui_demo_access_code="fixture-code", reply_format="sections"
        ),
        store,
        llm,
    )
    c = app.test_client()
    csrf = c.get("/ui/session").json["csrfToken"]
    session = c.post(
        "/ui/session", json={"accessCode": "fixture-code"}, headers={"X-CSRF-Token": csrf}
    ).json
    result = c.post(
        "/ui/chat",
        json={"clientSequence": "Compare"},
        headers={"X-CSRF-Token": session["csrfToken"]},
    )
    assert result.status_code == 200
    assert result.json["replyFormat"] == "sections-v1" and result.json["formatHash"] == FORMAT_HASH
    assert result.json["answer"]["sections"][2]["options"][0]["drawback"] is None
    assert result.json["promptVersion"] == store.active().id
    assert len(llm.calls) == 1


def test_automatic_and_manual_edit_contracts_keep_existing_boundaries():
    store = MemoryStore()
    llm = ScriptedLLM(fixture(), {"edits": [], "rejected": []}, {"edits": [], "rejected": []})
    client = create_app(
        Settings(reviewer_api_key="test-key", reply_format="sections"), store, llm
    ).test_client()
    headers = {"X-API-Key": "test-key"}
    automatic = client.post(
        "/improve-ai",
        headers=headers,
        json={"clientSequence": "Compare", "consultantReply": "Explain the choices."},
    )
    assert automatic.status_code == 200
    assert {"predictedReply", "updatedPrompt"} <= automatic.json.keys()
    assert "### Options" in automatic.json["predictedReply"]
    manual = client.post(
        "/improve-ai-manually", headers=headers, json={"instructions": "Keep it clear."}
    )
    assert manual.status_code == 200 and "updatedPrompt" in manual.json
    assert all(call["schema"] is not SectionedReply for call in llm.calls[1:])


def test_invalid_model_sections_receive_only_one_retry():
    import json

    invalid = {"reply": {"direct_answer": "**Heading** * clumped list"}, "source_ids": []}
    valid = {"reply": {"direct_answer": "A clear answer."}, "source_ids": []}
    store = MemoryStore()
    sdk = SDK(json.dumps(invalid), json.dumps(valid))
    llm = GeminiLLM(Settings(gemini_api_key="test-only"), store, client=sdk, sleep=lambda _: None)
    assert (
        llm.complete(system="policy", payload={}, schema=SectionedReply).reply.direct_answer
        == "A clear answer."
    )
    assert store.calls == len(sdk.calls) == 2


def test_structured_mode_does_not_accept_a_legacy_string_as_silent_fallback():
    with pytest.raises(ValidationError):
        SectionedReply.model_validate({"reply": "Legacy string", "source_ids": []})


def test_oversized_content_rejected_before_display():
    output = fixture()
    output["reply"]["sections"] = [
        {"kind": "bullets", "items": [{"text": "x" * 350} for _ in range(6)]} for _ in range(4)
    ]
    with pytest.raises(ValidationError):
        SectionedReply.model_validate(output)
