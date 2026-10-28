from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator


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


# The presentation contract is independent of automatically editable support rules.
# Plain atoms cannot hide multiple Markdown sections inside a single field.


def plain_atom(value):
    import re

    if re.search(
        r"[\r\n\u2028\u2029]|\*\*|__|(?:^|\s)#{1,6}\s|(?:^|\s)[*•]\s|(?:^|\s)\d+[.)]\s|^-\s", value
    ):
        raise ValueError("Use plain single-line text; put lists and headings in section fields")
    return value


LabelText = Annotated[str, Field(min_length=1, max_length=80), AfterValidator(plain_atom)]
PointText = Annotated[str, Field(min_length=1, max_length=350), AfterValidator(plain_atom)]
ParagraphText = Annotated[str, Field(min_length=1, max_length=800), AfterValidator(plain_atom)]
OpeningText = Annotated[str, Field(min_length=1, max_length=500), AfterValidator(plain_atom)]


def explicit_presentation_fields(schema):
    # Required nullable fields avoid optional-property branching in constrained decoding.
    # Python defaults still make local callers and stored fixtures convenient to validate.
    schema["required"] = list(schema.get("properties", {}))


class PresentationModel(StrictModel):
    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, json_schema_extra=explicit_presentation_fields
    )


class AnswerPoint(PresentationModel):
    text: PointText
    caveat: PointText | None = Field(
        default=None, description="Only relevant uncertainty; otherwise null"
    )


class AnswerOption(PresentationModel):
    label: LabelText
    benefit: PointText | None = Field(
        default=None, description="Supported benefit, or null if unknown"
    )
    drawback: PointText | None = Field(
        default=None, description="Supported drawback, or null if unknown"
    )
    uncertainty: PointText | None = Field(
        default=None, description="What must be verified; never fill unknown terms with promises"
    )

    @model_validator(mode="after")
    def meaningful_option(self):
        if not any((self.benefit, self.drawback, self.uncertainty)):
            raise ValueError("An option needs a supported point or explicit uncertainty")
        return self


class AnswerSection(PresentationModel):
    kind: Literal["paragraph", "bullets", "steps", "comparison"]
    heading: LabelText | None = Field(
        default=None, description="Short heading in the customer's language, or null"
    )
    text: ParagraphText | None = None
    items: list[AnswerPoint] = Field(default_factory=list, max_length=6)
    options: list[AnswerOption] = Field(default_factory=list, max_length=4)
    caveat: PointText | None = None

    @model_validator(mode="after")
    def content_matches_kind(self):
        if self.kind == "paragraph":
            valid = self.text is not None and not self.items and not self.options
        elif self.kind in ("bullets", "steps"):
            valid = self.text is None and bool(self.items) and not self.options
        else:
            valid = self.text is None and not self.items and len(self.options) >= 2
        if not valid:
            raise ValueError("Section content must match its kind; no empty or unused fields")
        return self


class AnswerContent(PresentationModel):
    direct_answer: OpeningText = Field(description="Short immediate answer; plain text only")
    caveat: PointText | None = None
    sections: list[AnswerSection] = Field(
        default_factory=list,
        max_length=4,
        description="Only useful detail; use an empty list for a simple concern",
    )
    next_step: PointText | None = Field(
        default=None,
        description="One relevant action or necessary question; null if already covered",
    )


class SectionedReply(PresentationModel):
    reply: AnswerContent
    source_ids: list[str] = Field(default_factory=list, max_length=3)

    @model_validator(mode="after")
    def total_content_budget(self):
        def count(value):
            if isinstance(value, str):
                return len(value)
            if isinstance(value, dict):
                return sum(count(v) for k, v in value.items() if k != "kind")
            if isinstance(value, list):
                return sum(map(count, value))
            return 0

        if count(self.reply.model_dump()) > 3500:
            raise ValueError("Structured answer text exceeds the response budget")
        return self
