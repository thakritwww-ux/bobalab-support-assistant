import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    database_url: str = ""
    gemini_api_key: str = ""
    reviewer_api_key: str = ""
    model: str = "gemini-3.5-flash-lite"
    daily_calls: int = 100
    requests_per_minute: int = 10
    timeout_seconds: int = 30
    ui_demo_access_code: str = ""
    ui_session_secret: str = ""
    ui_secure_cookie: bool = False

    def configuration_problems(self):
        problems = []
        for name, value in (
            ("GEMINI_API_KEY", self.gemini_api_key),
            ("DATABASE_URL", self.database_url),
            ("REVIEWER_API_KEY", self.reviewer_api_key),
        ):
            if not value.strip():
                problems.append(f"{name} is empty")
        if "[your-password]" in self.database_url.casefold():
            problems.append("DATABASE_URL still contains the database-password placeholder")
        return problems

    @classmethod
    def from_env(cls):
        load_dotenv(ROOT / ".env", override=False)
        return cls(
            database_url=os.getenv("DATABASE_URL", ""),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            reviewer_api_key=os.getenv("REVIEWER_API_KEY", ""),
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            daily_calls=max(1, int(os.getenv("DAILY_MODEL_CALL_LIMIT", "100"))),
            requests_per_minute=max(1, int(os.getenv("REQUESTS_PER_MINUTE", "10"))),
            timeout_seconds=max(1, min(30, int(os.getenv("MODEL_TIMEOUT_SECONDS", "30")))),
            ui_demo_access_code=os.getenv("UI_DEMO_ACCESS_CODE", ""),
            ui_session_secret=os.getenv("UI_SESSION_SECRET", ""),
            ui_secure_cookie=os.getenv("RENDER", "").lower() == "true"
            or os.getenv("UI_SECURE_COOKIE", "").lower() == "true",
        )
