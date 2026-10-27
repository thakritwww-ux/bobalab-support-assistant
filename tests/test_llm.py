from types import SimpleNamespace

import httpx
import pytest

from app.config import Settings
from app.errors import ServiceError
from app.llm import GeminiLLM
from app.schemas import GeneratedReply
from tests.fakes import MemoryStore


class SDK:
    def __init__(self, *outputs):
        self.outputs, self.calls = list(outputs), []
        self.models = self

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        result = self.outputs.pop(0)
        if isinstance(result, Exception):
            raise result
        return SimpleNamespace(text=result)


def test_malformed_json_gets_one_bounded_retry():
    sdk = SDK("{", '{"reply":"Hello","source_ids":[]}')
    store = MemoryStore()
    llm = GeminiLLM(
        Settings(gemini_api_key="synthetic-test-key"), store, client=sdk, sleep=lambda _: None
    )
    result = llm.complete(system="policy", payload={"synthetic": True}, schema=GeneratedReply)
    assert result.reply == "Hello"
    assert len(sdk.calls) == store.calls == 2


def test_timeouts_fail_without_model_reply():
    sdk = SDK(httpx.ReadTimeout("private data"), httpx.ReadTimeout("private data"))
    llm = GeminiLLM(
        Settings(gemini_api_key="synthetic-test-key"),
        MemoryStore(),
        client=sdk,
        sleep=lambda _: None,
    )
    with pytest.raises(ServiceError) as error:
        llm.complete(system="policy", payload={}, schema=GeneratedReply)
    assert error.value.code == "model_timeout"
    assert "private" not in str(error.value)
    assert len(sdk.calls) == 2


def test_daily_budget_includes_failed_attempts():
    store = MemoryStore()
    sdk = SDK("{")
    llm = GeminiLLM(
        Settings(gemini_api_key="synthetic-test-key", daily_calls=1),
        store,
        client=sdk,
        sleep=lambda _: None,
    )
    with pytest.raises(ServiceError) as error:
        llm.complete(system="policy", payload={}, schema=GeneratedReply)
    assert error.value.code == "daily_call_limit"
    assert len(sdk.calls) == store.calls == 1
