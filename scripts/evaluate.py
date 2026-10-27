"""Live synthetic evaluation and comparison; never silently substitutes a fake LLM."""

import argparse
import difflib
import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from app.cli import configured_service
from app.config import ROOT
from app.errors import ServiceError
from app.prompts import sections_hash
from app.schemas import ReplyRequest


def capture(output):
    settings, store, service = configured_service()
    version = store.active()
    cases = json.loads((ROOT / "eval/cases.json").read_text())
    results = []
    for case in cases:
        started = time.monotonic()
        try:
            reply = service.generate(ReplyRequest.model_validate(case["request"]), version)
            result = {"reply": reply}
        except ServiceError as exc:
            result = {"error": exc.code}
        results.append(
            {
                **case,
                **result,
                "seconds": round(time.monotonic() - started, 3),
                "human_scores": {
                    k: None
                    for k in (
                        "factual_support",
                        "context",
                        "comprehension",
                        "usefulness",
                        "tone",
                        "capability_honesty",
                    )
                },
                "human_notes": "",
            }
        )
    record = {
        "evidence_type": "live_model_outputs",
        "captured_at": datetime.now(UTC).isoformat(),
        "model": settings.model,
        "temperature": 0.2,
        "versionId": version.id,
        "prompt_hash": sections_hash(version.sections),
        "knowledge_hash": hashlib.sha256(
            json.dumps(version.sections.reviewed_knowledge, sort_keys=True).encode()
        ).hexdigest(),
        "sections": version.sections.model_dump(),
        "results": results,
        "disclosure": "Synthetic cases known to developers. Human review pending unless scores and notes are filled. No aggregate quality claim is computed automatically.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    print(
        json.dumps(
            {
                "output": str(output),
                "cases": len(results),
                "errors": sum("error" in r for r in results),
            }
        )
    )


def comparison(before_path, after_path, output):
    before, after = (json.loads(p.read_text()) for p in (before_path, after_path))
    if (
        before.get("evidence_type") != "live_model_outputs"
        or after.get("evidence_type") != "live_model_outputs"
    ):
        raise ValueError("Comparison requires live model records, not simulated tests")
    if (before["model"], before["temperature"]) != (after["model"], after["temperature"]):
        raise ValueError("Model/settings changed: not a controlled prompt comparison")
    if [r["request"] for r in before["results"]] != [r["request"] for r in after["results"]]:
        raise ValueError("Comparison inputs differ")
    knowledge_changed = before["knowledge_hash"] != after["knowledge_hash"]
    diff = "\n".join(
        difflib.unified_diff(
            json.dumps(before["sections"], indent=2, ensure_ascii=False).splitlines(),
            json.dumps(after["sections"], indent=2, ensure_ascii=False).splitlines(),
            fromfile="before",
            tofile="after",
            lineterm="",
        )
    )
    lines = [
        "# Live before-and-after evidence",
        "",
        f"Model: `{before['model']}`; temperature: {before['temperature']}.",
        f"Before version: `{before['versionId']}`; after: `{after['versionId']}`.",
        "",
        "Knowledge changed: **"
        + str(knowledge_changed)
        + "**. "
        + (
            "Source correction is a confound; do not attribute these results solely to behavioral learning."
            if knowledge_changed
            else "Reviewed knowledge was held constant."
        ),
        "",
        "## Actual instruction diff",
        "",
        "```diff",
        diff or "No instruction change.",
        "```",
        "",
        "Human verdicts below are pending until the candidate reviews them. These outputs alone do not establish improvement.",
        "",
    ]
    for old, new in zip(before["results"], after["results"], strict=True):
        lines.extend(
            [
                f"## {old['id']}",
                "",
                "Customer need: " + old["customer_need"],
                "",
                "**Before**",
                "",
                old.get("reply", "Service error: " + old.get("error", "unknown")),
                "",
                "**After**",
                "",
                new.get("reply", "Service error: " + new.get("error", "unknown")),
                "",
                "**Candidate verdict and reasoning:** pending.",
                "",
            ]
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines))
    print(f"Comparison written: {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("capture")
    snap.add_argument("--output", type=Path, required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    compare.add_argument("--output", type=Path, default=Path("docs/BEFORE_AFTER.md"))
    args = parser.parse_args()
    try:
        if args.command == "capture":
            capture(args.output)
        else:
            comparison(args.before, args.after, args.output)
    except ServiceError as exc:
        parser.exit(1, f"{exc.code}: {exc.message}\n")
    except (ValueError, KeyError, OSError):
        parser.exit(1, "Invalid evidence files or mismatched comparison settings.\n")


if __name__ == "__main__":
    main()
