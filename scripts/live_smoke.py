"""Exercise deployed endpoints with synthetic data, without printing credentials."""

import argparse
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from app.config import Settings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url")
    parser.add_argument(
        "--allow-edits",
        action="store_true",
        required=True,
        help="Acknowledge that testing improvement endpoints can change the active prompt",
    )
    parser.add_argument("--output", type=Path, default=Path("docs/evidence/live-smoke.local.json"))
    args = parser.parse_args()
    settings = Settings.from_env()
    base = args.base_url.rstrip("/")
    parsed = urlparse(base)
    if parsed.scheme != "https" and not (
        parsed.scheme == "http" and parsed.hostname in ("localhost", "127.0.0.1")
    ):
        parser.error("Use HTTPS for remote services, or HTTP only on localhost")
    if not settings.reviewer_api_key:
        parser.error("REVIEWER_API_KEY is not configured")
    examples = [
        ("/health", None, {"status"}),
        (
            "/generate-reply",
            {
                "clientSequence": "What should I consider about accommodation while a Kuala Lumpur DTV application is pending?",
                "chatHistory": [],
            },
            {"aiReply"},
        ),
        (
            "/improve-ai",
            {
                "clientSequence": "What do you mean by proof of funds?",
                "chatHistory": [],
                "consultantReply": "Explain unfamiliar terms in everyday language before continuing.",
            },
            {"predictedReply", "updatedPrompt"},
        ),
        (
            "/improve-ai-manually",
            {"instructions": "Finish multi-step explanations with the immediate next action."},
            {"updatedPrompt"},
        ),
    ]
    results = []
    for path, payload, expected in examples:
        request = Request(
            base + path,
            data=json.dumps(payload).encode() if payload else None,
            headers={"Content-Type": "application/json", "X-API-Key": settings.reviewer_api_key},
        )
        started = time.monotonic()
        try:
            with urlopen(request, timeout=150) as response:
                body = json.load(response)
                passed = response.status == 200 and expected <= body.keys()
                result = {"path": path, "passed": passed, "status": response.status, "body": body}
        except HTTPError as exc:
            result = {"path": path, "passed": False, "status": exc.code}
        except (URLError, TimeoutError, ValueError):
            result = {"path": path, "passed": False, "status": "connection_or_json_error"}
        result["seconds"] = round(time.monotonic() - started, 3)
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if k != "body"}))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {"evidence_type": "live_http_smoke", "base_url": base, "results": results},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
