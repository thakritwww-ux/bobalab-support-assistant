import pytest

from app.config import Settings
from app.errors import ServiceError
from app.store import PostgresStore


def test_empty_configuration_reports_field_names_without_values():
    problems = Settings().configuration_problems()
    assert len(problems) == 3
    assert "DATABASE_URL is empty" in problems


def test_password_placeholder_is_not_reported_as_ready():
    settings = Settings(
        database_url="postgresql://postgres.fixture:[YOUR-PASSWORD]@db.invalid/postgres",
        gemini_api_key="synthetic-test-key",
        reviewer_api_key="synthetic-reviewer-key",
    )
    assert settings.configuration_problems() == [
        "DATABASE_URL still contains the database-password placeholder"
    ]
    with pytest.raises(ServiceError) as error:
        with PostgresStore(settings.database_url).connect():
            pytest.fail("Connection must not be attempted")
    assert error.value.code == "not_configured"
    assert "db.invalid" not in str(error.value)
