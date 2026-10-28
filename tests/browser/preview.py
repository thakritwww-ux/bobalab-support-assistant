"""Local browser-test server. Uses synthetic fixtures and never the live model."""

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
        return schema.model_validate({"reply": reply, "source_ids": ["mfa-dtv-overview"]})


if __name__ == "__main__":
    app = create_app(
        Settings(
            reviewer_api_key="preview-reviewer-only",
            ui_demo_access_code="preview-demo-code",
            requests_per_minute=100,
        ),
        MemoryStore(),
        FixtureLLM(),
    )
    app.run(host="127.0.0.1", port=8002, debug=False)
