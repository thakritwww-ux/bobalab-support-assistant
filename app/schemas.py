from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Turn(StrictModel):
    role: Literal["client", "consultant"]
    message: str = Field(min_length=1, max_length=6000)


class ReplyRequest(StrictModel):
    clientSequence: str = Field(min_length=1, max_length=6000)
    chatHistory: list[Turn] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def context_budget(self):
        if len(self.clientSequence) + sum(len(t.message) for t in self.chatHistory) > 24000:
            raise ValueError("Conversation context exceeds 24,000 characters")
        return self


class ImproveRequest(ReplyRequest):
    consultantReply: str = Field(min_length=1, max_length=6000)


class ManualRequest(StrictModel):
    instructions: str = Field(min_length=1, max_length=4000)


class Rule(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_-]{0,47}$")
    text: str = Field(min_length=1, max_length=700)


class Sections(StrictModel):
    protected_policy: str = Field(min_length=1)
    reviewed_knowledge: dict
    editable_playbook: list[Rule] = Field(min_length=1, max_length=30)


class Edit(StrictModel):
    action: Literal["add", "replace", "delete"]
    rule_id: str = Field(pattern=r"^[a-z][a-z0-9_-]{0,47}$")
    text: str = Field(default="", max_length=700)
    category: Literal["style", "support_process"]


class Rejection(StrictModel):
    category: Literal[
        "unreviewed_fact", "unavailable_action", "concealment", "privacy", "protected_policy"
    ]
    # A reason code, never model-generated customer text in persistent audit records.
    reason: Literal[
        "requires_review", "not_supported", "not_appropriate", "sensitive_content", "immutable"
    ]


class EditProposal(StrictModel):
    edits: list[Edit] = Field(default_factory=list, max_length=8)
    rejected: list[Rejection] = Field(default_factory=list, max_length=8)


class GeneratedReply(StrictModel):
    reply: str = Field(min_length=1, max_length=4000)
    source_ids: list[str] = Field(default_factory=list, max_length=3)
