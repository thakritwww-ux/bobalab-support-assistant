import json

import pytest

from scripts.evaluate import comparison


def record(model="test-model", knowledge_hash="same"):
    # Unit-test fixture only; never an observed model output or submission evidence.
    return {
        "evidence_type": "live_model_outputs",
        "model": model,
        "temperature": 0.2,
        "versionId": "test-version",
        "knowledge_hash": knowledge_hash,
        "sections": {},
        "results": [
            {
                "id": "fixture",
                "request": {"clientSequence": "A synthetic test"},
                "customer_need": "Fixture only",
                "reply": "Simulated output for a unit test",
            }
        ],
    }


def write_pair(tmp_path, before, after):
    a, b = tmp_path / "before.json", tmp_path / "after.json"
    a.write_text(json.dumps(before))
    b.write_text(json.dumps(after))
    return a, b


def test_model_changes_cannot_be_reported_as_controlled_prompt_comparison(tmp_path):
    a, b = write_pair(tmp_path, record(), record(model="different-test-model"))
    with pytest.raises(ValueError):
        comparison(a, b, tmp_path / "report.md")


def test_changed_knowledge_is_flagged_as_a_confound(tmp_path):
    a, b = write_pair(tmp_path, record(), record(knowledge_hash="different"))
    report = tmp_path / "report.md"
    comparison(a, b, report)
    assert "Source correction is a confound" in report.read_text()
    assert "Candidate verdict and reasoning:** pending" in report.read_text()


def test_simulated_evidence_type_is_rejected(tmp_path):
    fake = {**record(), "evidence_type": "simulated"}
    a, b = write_pair(tmp_path, fake, fake)
    with pytest.raises(ValueError):
        comparison(a, b, tmp_path / "report.md")


def test_timeout_change_cannot_be_mistaken_for_learning(tmp_path):
    before = {**record(), "model_timeout_seconds": 20}
    after = {**record(), "model_timeout_seconds": 30}
    a, b = write_pair(tmp_path, before, after)
    with pytest.raises(ValueError, match="timeout"):
        comparison(a, b, tmp_path / "report.md")


def test_service_failure_is_not_a_paired_quality_improvement(tmp_path):
    before = record()
    before["results"][0].pop("reply")
    before["results"][0]["error"] = "model_unavailable"
    a, b = write_pair(tmp_path, before, record())
    report = tmp_path / "report.md"
    comparison(a, b, report)
    assert "no paired answer-quality conclusion" in report.read_text()
