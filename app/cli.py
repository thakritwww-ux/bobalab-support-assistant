import argparse
import json
import os
import sys
from pathlib import Path
from uuid import UUID

from app.config import ROOT, Settings
from app.dataset import build_pairs
from app.errors import ServiceError
from app.knowledge import validate_knowledge
from app.llm import GeminiLLM
from app.prompts import seed_sections
from app.schemas import ReplyRequest
from app.service import AssistantService
from app.store import PostgresStore
from app.web import ui_credentials


def configured_service():
    settings = Settings.from_env()
    store = PostgresStore(settings.database_url)
    return (
        settings,
        store,
        AssistantService(store, GeminiLLM(settings, store), settings.reply_format),
    )


def main():
    parser = argparse.ArgumentParser(description="BOBALAB server and prompt maintenance")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check-config", "migrate", "seed", "check-live", "history", "write-web-access"):
        sub.add_parser(name)
    build = sub.add_parser("build-pairs")
    build.add_argument("--output", default="work/pairs.json")
    rollback = sub.add_parser("rollback")
    rollback.add_argument("version_id", type=UUID)
    knowledge = sub.add_parser("review-knowledge")
    knowledge.add_argument("path", type=Path)
    knowledge.add_argument(
        "--reviewed",
        required=True,
        action="store_true",
        help="Confirm source, scope, review date and candidate assessment before activation",
    )
    args = parser.parse_args()
    settings, store, service = configured_service()
    try:
        if args.command == "check-config":
            state = {
                "GEMINI_API_KEY": bool(settings.gemini_api_key),
                "DATABASE_URL": bool(settings.database_url),
                "REVIEWER_API_KEY": bool(settings.reviewer_api_key),
            }
            problems = settings.configuration_problems()
            print(json.dumps({"configured": state, "model": settings.model, "problems": problems}))
            return 0 if not problems else 1
        if args.command == "build-pairs":
            pairs = build_pairs()
            destination = Path(args.output)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(pairs, ensure_ascii=False, indent=2))
            print(json.dumps({"pairs": len(pairs), "output": str(destination)}))
        elif args.command == "migrate":
            store.migrate()
            print("Database schema ready.")
        elif args.command == "seed":
            sections = seed_sections()
            validate_knowledge(sections.reviewed_knowledge)
            print("Seed created." if store.seed(sections) else "Existing active prompt preserved.")
        elif args.command == "history":
            print(json.dumps(store.history(), default=str, indent=2))
        elif args.command == "write-web-access":
            code, _ = ui_credentials(settings)
            if not code:
                raise ServiceError(
                    "ui_not_configured", "Configure valid browser access settings first."
                )
            path = ROOT / "work" / "WEB_DEMO_ACCESS.txt"
            path.parent.mkdir(exist_ok=True)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w") as file:
                file.write(
                    "BOBALAB private browser demo access\n\n"
                    "Website: https://bobalab-support-assistant.onrender.com\n"
                    f"Demo access code: {code}\n\n"
                    "Generation-only browser access; not the reviewer API key.\n"
                    "Keep this file private. It contains no provider/database credentials.\n"
                    "Sessions expire after 30 minutes.\n"
                )
            path.chmod(0o600)
            print(f"Private browser access instructions saved to {path}")
        elif args.command == "rollback":
            print(json.dumps({"versionId": service.rollback(str(args.version_id)).id}))
        elif args.command == "review-knowledge":
            print(json.dumps({"versionId": service.update_knowledge(args.path).id}))
        elif args.command == "check-live":
            version = store.active()
            service.generate(
                ReplyRequest(clientSequence="Hi, what can this demo help me with?"), version
            )
            print(
                json.dumps(
                    {
                        "database": "ok",
                        "model": "ok",
                        "versionId": version.id,
                        "modelId": settings.model,
                        "note": "One synthetic generation call was made; this does not prove every behavior or editor path.",
                    }
                )
            )
        return 0
    except ServiceError as exc:
        print(json.dumps({"error": exc.code, "message": exc.message}), file=sys.stderr)
        return 1
    except (ValueError, KeyError, OSError):
        print(
            "Invalid local input. Check the file, UUID and knowledge schema; no changes confirmed.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
