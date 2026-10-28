"""Versioned presentation contract. It does not supply new visa or agency facts."""

import hashlib
import json
from dataclasses import dataclass

from app.schemas import AnswerContent, SectionedReply

FORMAT_VERSION = "sections-v1"
FORMAT_INSTRUCTION = """RESPONSE PRESENTATION CONTRACT: sections-v1
Follow the protected policy and reviewed facts. The supplied JSON schema makes reply
an object containing direct_answer, optional caveat, sections and optional next_step.
Each text field is plain single-line text: no Markdown, bullet characters, numbered
prefixes or embedded headings. Structure belongs in the typed fields, not text.
Answer the immediate concern briefly first. Use sections only when useful: bullets
for distinct preparation items, steps for ordered procedures, comparison for supported
options with meaningful tradeoffs, paragraph for other relevant detail. Leave unused
fields null or empty. Simple questions can have no sections and no next_step.
Put uncertainty beside its point or option. Unknown comparison terms remain null or
are explicitly qualified; never invent benefits, penalties, requirements or guarantees
to fill a cell. Do not append agency onboarding or unrelated facts to fill sections.
Use the customer's language for text/headings. Keep all human-facing text concise.
Choose source_ids through the reviewed citation mechanism; no URLs in reply fields.
The application formats these fields; valid structure is not proof of factual accuracy.
"""
FORMAT_HASH = hashlib.sha256(
    (
        FORMAT_INSTRUCTION
        + json.dumps(SectionedReply.model_json_schema(), sort_keys=True, ensure_ascii=False)
    ).encode()
).hexdigest()


@dataclass(frozen=True)
class ReplyResult:
    text: str
    answer: AnswerContent | None
    reply_format: str
    format_hash: str | None


def labels(answer):
    thai = any("\u0e00" <= c <= "\u0e7f" for c in answer.direct_answer)
    if thai:
        return {
            "paragraph": "รายละเอียด",
            "bullets": "สิ่งที่ควรตรวจสอบ",
            "steps": "ขั้นตอนถัดไป",
            "comparison": "ทางเลือก",
            "next": "ขั้นตอนถัดไป",
            "unknown": "ยังไม่ระบุ",
            "columns": ["ทางเลือก", "ข้อดี", "ข้อจำกัด", "สิ่งที่ควรตรวจสอบ"],
        }
    return {
        "paragraph": "Details",
        "bullets": "What to check",
        "steps": "Next steps",
        "comparison": "Options",
        "next": "Next step",
        "unknown": "Not specified",
        "columns": ["Option", "Benefit", "Drawback", "What to check"],
    }


def escape(text):
    # Escape syntax, not meaning. Stored/copied output cannot create extra table cells.
    return (
        text.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("*", "\\*")
        .replace("_", "\\_")
        .replace("`", "\\`")
        .replace("#", "\\#")
    )


def render_answer(answer):
    names = labels(answer)
    blocks = [escape(answer.direct_answer)]
    if answer.caveat:
        blocks.append(escape(answer.caveat))
    for section in answer.sections:
        heading = section.heading or (None if section.kind == "paragraph" else names[section.kind])
        if heading:
            blocks.append("### " + escape(heading))
        if section.kind == "paragraph":
            blocks.append(escape(section.text))
        elif section.kind in ("bullets", "steps"):
            lines = []
            for i, item in enumerate(section.items, 1):
                prefix = f"{i}. " if section.kind == "steps" else "- "
                line = prefix + escape(item.text)
                if item.caveat:
                    line += " — " + escape(item.caveat)
                lines.append(line)
            blocks.append("\n".join(lines))
        else:
            rows = ["| " + " | ".join(names["columns"]) + " |", "| --- | --- | --- | --- |"]
            for option in section.options:
                values = [option.label, option.benefit, option.drawback, option.uncertainty]
                rows.append(
                    "| "
                    + " | ".join(escape(value) if value else names["unknown"] for value in values)
                    + " |"
                )
            blocks.append("\n".join(rows))
        if section.caveat:
            blocks.append(escape(section.caveat))
    if answer.next_step:
        blocks.extend(["### " + names["next"], escape(answer.next_step)])
    return "\n\n".join(blocks)
