from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from app.config import ROOT
from app.errors import Conflict, ServiceError
from app.prompts import sections_hash
from app.schemas import Sections


@dataclass(frozen=True)
class Version:
    id: str
    sections: Sections
    source: str = "seed"
    created_at: datetime | None = None


class PostgresStore:
    def __init__(self, url):
        self.url = url

    @contextmanager
    def connect(self):
        if not self.url:
            raise ServiceError("not_configured", "Database connection is not configured.")
        if "[your-password]" in self.url.casefold():
            raise ServiceError(
                "not_configured",
                "Replace the Supabase database-password placeholder in your local configuration.",
            )
        try:
            # Local disposable tests can explicitly use sslmode=disable.
            sslmode = "disable" if "sslmode=disable" in self.url else "require"
            with psycopg.connect(
                self.url, connect_timeout=5, sslmode=sslmode, row_factory=dict_row
            ) as conn:
                conn.execute("SET statement_timeout = '5000ms'")
                yield conn
        except psycopg.Error as exc:
            # Do not expose connection strings, SQL errors or passwords to clients/logs.
            raise ServiceError(
                "database_unavailable", "The database could not complete the operation."
            ) from exc

    def migrate(self):
        with self.connect() as conn:
            conn.execute((ROOT / "db/schema.sql").read_text())

    def seed(self, sections):
        with self.connect() as conn:
            conn.execute("SELECT pg_advisory_xact_lock(47291823)")
            if conn.execute("SELECT active_version FROM prompt_state WHERE singleton").fetchone():
                return False
            version_id = str(uuid4())
            self._insert(conn, version_id, None, "seed", sections)
            conn.execute(
                "INSERT INTO prompt_state(singleton, active_version) VALUES(true,%s)", (version_id,)
            )
        return True

    @staticmethod
    def _version(row):
        return Version(
            str(row["id"]),
            Sections.model_validate(row["sections"]),
            row["source"],
            row["created_at"],
        )

    def active(self):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT v.* FROM prompt_versions v JOIN prompt_state s ON s.active_version=v.id WHERE s.singleton"
            ).fetchone()
            if row is None:
                raise ServiceError(
                    "not_seeded", "Initialize the prompt database before using the API."
                )
            return self._version(row)

    def get(self, version_id):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM prompt_versions WHERE id=%s", (version_id,)
            ).fetchone()
            if row is None:
                raise ServiceError("version_not_found", "Unknown prompt version.", 404)
            return self._version(row)

    def history(self):
        with self.connect() as conn:
            return conn.execute(
                "SELECT id,parent_id,source,created_at,content_hash FROM prompt_versions ORDER BY created_at DESC LIMIT 100"
            ).fetchall()

    @staticmethod
    def _insert(conn, version_id, parent, source, sections):
        conn.execute(
            "INSERT INTO prompt_versions(id,parent_id,source,sections,content_hash) VALUES(%s,%s,%s,%s,%s)",
            (version_id, parent, source, Jsonb(sections.model_dump()), sections_hash(sections)),
        )

    def commit(self, base, sections, source, outcome, operations, rejected):
        with self.connect() as conn:
            state = conn.execute(
                "SELECT active_version FROM prompt_state WHERE singleton FOR UPDATE"
            ).fetchone()
            if not state or str(state["active_version"]) != base.id:
                raise Conflict()
            changed = sections_hash(base.sections) != sections_hash(sections)
            result_id = str(uuid4()) if changed else base.id
            if changed:
                self._insert(conn, result_id, base.id, source, sections)
                conn.execute(
                    "UPDATE prompt_state SET active_version=%s WHERE singleton", (result_id,)
                )
            conn.execute(
                "INSERT INTO improvement_events(id,base_version,result_version,source,outcome,operations,rejected) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                (
                    str(uuid4()),
                    base.id,
                    result_id,
                    source,
                    outcome,
                    Jsonb(operations),
                    Jsonb(rejected),
                ),
            )
            return Version(result_id, sections, source)

    def reserve_call(self, limit):
        with self.connect() as conn:
            row = conn.execute(
                """INSERT INTO model_usage(day,calls) VALUES ((now() AT TIME ZONE 'Asia/Bangkok')::date,1)
                ON CONFLICT(day) DO UPDATE SET calls=model_usage.calls+1
                WHERE model_usage.calls < %s RETURNING calls""",
                (limit,),
            ).fetchone()
            if not row:
                raise ServiceError(
                    "daily_call_limit",
                    "The application's daily model-call budget is exhausted. Try the next Bangkok day.",
                    429,
                )
