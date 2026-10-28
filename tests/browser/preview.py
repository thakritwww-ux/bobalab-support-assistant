"""Local browser-test server. Uses synthetic fixtures and never the live model."""

import os

from app import create_app
from app.config import Settings
from app.errors import ServiceError
from tests.fakes import MemoryStore


class FixtureLLM:
    def complete(self, *, payload, schema, **kwargs):
        text = payload["conversation"]["clientSequence"]
        if text == "__test_error__":
            raise ServiceError("model_unavailable", "Simulated provider failure.", 503)
        if text == "__test_slow__":
            import time

            time.sleep(2)
        if text == "__test_html__":
            reply = (
                '<img src=x onerror="window.injected=true">\n<script>window.injected=true</script>'
            )
        elif text == "__test_structure__":
            reply = (
                "Illustrative interface fixture, not visa advice.\n\n"
                "## Your options\n"
                "| Option | Benefit | Tradeoff |\n| --- | --- | --- |\n"
                "| Flexible | Can accommodate changes | Check the price and terms |\n"
                "| Fixed | May fit a firm plan | Changes may cost more |\n\n"
                "## What to check\n"
                "- **Timing:** remains uncertain.\n"
                "- **Costs:** compare actual terms.\n\n"
                "### Next steps\n1. Check the current guidance.\n2. Compare your priorities."
            )
        elif any("\u0e00" <= c <= "\u0e7f" for c in text):
            reply = "ตัวอย่างสำหรับทดสอบหน้าจอเท่านั้น\n\n## ขั้นตอนถัดไป\n- ตรวจสอบข้อมูล\n- เปรียบเทียบทางเลือก"
        else:
            reply = "Illustrative interface fixture.\n\nA concise reply with uncertainty preserved."
        if schema.__name__ == "SectionedReply":
            if text == "__test_sections__":
                value = {
                    "direct_answer": "Illustrative structured fixture, not visa advice.",
                    "sections": [
                        {
                            "kind": "bullets",
                            "items": [
                                {
                                    "text": "Check the relevant guidance.",
                                    "caveat": "This collection is limited.",
                                },
                                {"text": "Keep the actual terms available."},
                            ],
                        },
                        {
                            "kind": "comparison",
                            "options": [
                                {
                                    "label": "Option A | literal pipe",
                                    "benefit": "May allow changes if terms permit.",
                                    "drawback": None,
                                    "uncertainty": "Check actual terms.",
                                },
                                {
                                    "label": "Option B",
                                    "benefit": None,
                                    "drawback": "Changes may be restricted.",
                                    "uncertainty": "Terms were not provided.",
                                },
                            ],
                        },
                        {
                            "kind": "steps",
                            "items": [
                                {"text": "Read the conditions."},
                                {"text": "Choose according to your priorities."},
                            ],
                        },
                    ],
                }
            elif any("\u0e00" <= c <= "\u0e7f" for c in text):
                value = {
                    "direct_answer": "ตัวอย่างข้อมูลสำหรับทดสอบหน้าจอเท่านั้น",
                    "sections": [
                        {
                            "kind": "steps",
                            "items": [
                                {"text": "ตรวจสอบข้อมูล", "caveat": "ข้อมูลอาจมีข้อจำกัด"},
                                {"text": "เปรียบเทียบเงื่อนไข"},
                            ],
                        }
                    ],
                }
            elif text == "__test_html__":
                value = {"direct_answer": '<img src=x onerror="window.injected=true">'}
            else:
                value = {"direct_answer": "Illustrative structured fixture.", "sections": []}
            return schema.model_validate({"reply": value, "source_ids": ["mfa-dtv-overview"]})
        return schema.model_validate({"reply": reply, "source_ids": ["mfa-dtv-overview"]})


if __name__ == "__main__":
    app = create_app(
        Settings(
            reviewer_api_key="preview-reviewer-only",
            ui_demo_access_code="preview-demo-code",
            requests_per_minute=100,
            reply_format=os.getenv("BROWSER_REPLY_FORMAT", "text"),
        ),
        MemoryStore(),
        FixtureLLM(),
    )
    app.run(host="127.0.0.1", port=int(os.getenv("BROWSER_PORT", "8002")), debug=False)
