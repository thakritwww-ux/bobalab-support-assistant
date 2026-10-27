"""Try the support API from a terminal; conversation history stays in memory."""

import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from pydantic import ValidationError

from app.config import Settings
from app.schemas import ReplyRequest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://bobalab-support-assistant.onrender.com")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    url = urlsplit(base)
    if (
        url.username
        or url.password
        or not (
            url.scheme == "https"
            or (url.scheme == "http" and url.hostname in ("localhost", "127.0.0.1"))
        )
    ):
        parser.error("Use HTTPS, or HTTP on localhost. Do not put credentials in the URL.")
    settings = Settings.from_env()
    if not settings.reviewer_api_key:
        parser.error("Set REVIEWER_API_KEY in your local .env file first.")
    history = []
    print("BOBALAB API chat test — use synthetic questions only.")
    print("Type /reset for a new conversation, or /quit to leave. Free hosting can be slow.")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nClosed.")
            return 0
        if question == "/quit":
            print("Closed.")
            return 0
        if question == "/reset":
            history.clear()
            print("Conversation cleared.")
            continue
        if not question:
            continue
        try:
            payload = ReplyRequest(clientSequence=question, chatHistory=history).model_dump()
        except ValidationError:
            print("Message or history is too long. Shorten the question or type /reset.")
            continue
        request = Request(
            base + "/generate-reply",
            data=json.dumps(payload, ensure_ascii=False).encode(),
            headers={"Content-Type": "application/json", "X-API-Key": settings.reviewer_api_key},
        )
        print("Waiting for the assistant…", flush=True)
        try:
            with urlopen(request, timeout=150) as response:
                body = json.load(response)
            reply = body["aiReply"]
            if not isinstance(reply, str) or not reply.strip():
                raise ValueError
        except HTTPError as exc:
            print(f"The service returned HTTP {exc.code}. Check README errors or try again later.")
            continue
        except (URLError, TimeoutError):
            print("The service could not respond in time. Try again later.")
            continue
        except (ValueError, KeyError, TypeError):
            print("The service returned an unexpected response. No reply was added to history.")
            continue
        history.extend(
            [{"role": "client", "message": question}, {"role": "consultant", "message": reply}]
        )
        print("\nAssistant: " + reply)


if __name__ == "__main__":
    raise SystemExit(main())
