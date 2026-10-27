"""Apply a small set of development-only consultant examples to the live editor."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from app.cli import configured_service
from app.dataset import development_examples
from app.errors import ServiceError
from app.prompts import render_prompt
from app.schemas import ImproveRequest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=8, choices=range(1, 13))
    parser.add_argument("--output", type=Path, default=Path("docs/evidence/replay.local.json"))
    args = parser.parse_args()
    settings, store, service = configured_service()
    records = []
    try:
        for pair in development_examples(args.limit):
            before = store.active()
            result = service.improve(
                ImproveRequest(
                    clientSequence=pair["clientSequence"],
                    chatHistory=pair["chatHistory"],
                    consultantReply=pair["learningReference"],
                )
            )
            records.append(
                {
                    "pair_id": pair["id"],
                    "split": pair["split"],
                    "base_version": before.id,
                    "before_prompt": render_prompt(before.sections),
                    "consultantReply": pair["learningReference"],
                    "clientSequence": pair["clientSequence"],
                    "chatHistory": pair["chatHistory"],
                    **result,
                }
            )
            print(
                json.dumps(
                    {
                        "pair": pair["id"],
                        "status": result["learningStatus"],
                        "versionId": result["versionId"],
                    }
                )
            )
    except ServiceError as exc:
        print(json.dumps({"error": exc.code, "message": exc.message}))
        return_code = 1
    else:
        return_code = 0
    finally:
        # Preserve completed real results if quota runs out mid-batch.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(
                {
                    "evidence_type": "live_model_outputs",
                    "model": settings.model,
                    "captured_at": datetime.now(UTC).isoformat(),
                    "records": records,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    raise SystemExit(return_code)


if __name__ == "__main__":
    main()
