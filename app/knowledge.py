from datetime import date
from urllib.parse import urlsplit


def validate_knowledge(knowledge):
    sources = knowledge["sources"]
    if not sources or len(sources) > 12:
        raise ValueError("Knowledge must include between one and twelve reviewed sources")
    ids = set()
    for source in sources:
        if source["id"] in ids:
            raise ValueError("Source IDs must be unique")
        ids.add(source["id"])
        host = urlsplit(source["url"]).hostname or ""
        if not source["url"].startswith("https://") or not (
            host.endswith(".go.th") or host.endswith(".thaiembassy.org")
        ):
            raise ValueError("Sources must be HTTPS official Thai government or embassy URLs")
        date.fromisoformat(source["reviewed_at"])
        if not source["country_scope"] or not source["facts"] or not source["limitations"]:
            raise ValueError("Source scope, facts and limitations are required")
    # Keep compiled prompt and provider request sizes bounded.
    import json

    if len(json.dumps(knowledge, ensure_ascii=False)) > 24000:
        raise ValueError("Reviewed knowledge exceeds 24,000 characters")
