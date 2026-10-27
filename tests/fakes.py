import threading
from uuid import uuid4

from app.errors import Conflict, ServiceError
from app.prompts import sections_hash, seed_sections
from app.store import Version


class MemoryStore:
    """Test double only. The deployed app always uses PostgreSQL."""

    def __init__(self):
        self.current = Version(str(uuid4()), seed_sections())
        self.versions = {self.current.id: self.current}
        self.events, self.calls = [], 0
        self.lock = threading.Lock()

    def active(self):
        return self.current

    def get(self, version_id):
        return self.versions[version_id]

    def commit(self, base, sections, source, outcome, operations, rejected):
        with self.lock:
            if base.id != self.current.id:
                raise Conflict()
            if sections_hash(base.sections) != sections_hash(sections):
                self.current = Version(str(uuid4()), sections.model_copy(deep=True), source)
                self.versions[self.current.id] = self.current
            self.events.append({"operations": operations, "rejected": rejected, "outcome": outcome})
            return self.current

    def reserve_call(self, limit):
        if self.calls >= limit:
            raise ServiceError("daily_call_limit", "Daily budget exhausted.", 429)
        self.calls += 1


class ScriptedLLM:
    """Deliberately simulated outputs, never valid before/after model evidence."""

    def __init__(self, *outputs):
        self.outputs, self.calls = list(outputs), []

    def complete(self, **kwargs):
        self.calls.append(kwargs)
        output = self.outputs.pop(0)
        if isinstance(output, Exception):
            raise output
        return kwargs["schema"].model_validate(output)
