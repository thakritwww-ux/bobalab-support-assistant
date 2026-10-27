import hashlib
import json

from app.config import ROOT
from app.schemas import Sections


def seed_sections():
    return Sections(
        protected_policy=(ROOT / "prompts/policy.md").read_text(),
        reviewed_knowledge=json.loads((ROOT / "data/knowledge.json").read_text()),
        editable_playbook=json.loads((ROOT / "prompts/playbook.json").read_text()),
    )


def render_prompt(sections):
    return "\n\n".join(
        [
            "PROTECTED POLICY\n" + sections.protected_policy,
            "REVIEWED KNOWLEDGE\n" + json.dumps(sections.reviewed_knowledge, ensure_ascii=False),
            "EDITABLE PLAYBOOK\n"
            + "\n".join(f"[{r.id}] {r.text}" for r in sections.editable_playbook),
        ]
    )


def sections_hash(sections):
    return hashlib.sha256(json.dumps(sections.model_dump(), sort_keys=True).encode()).hexdigest()
