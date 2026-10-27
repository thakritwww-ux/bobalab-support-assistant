import copy

import pytest

from app.knowledge import validate_knowledge
from app.prompts import seed_sections


def test_seed_knowledge_urls_and_metadata_validate():
    validate_knowledge(seed_sections().reviewed_knowledge)


@pytest.mark.parametrize(
    "url",
    ["https://fake-embassy.invalid/info", "https://notgo.th/info", "http://image.mfa.go.th/info"],
)
def test_nonofficial_or_nonhttps_sources_rejected(url):
    knowledge = copy.deepcopy(seed_sections().reviewed_knowledge)
    knowledge["sources"][0]["url"] = url
    with pytest.raises(ValueError):
        validate_knowledge(knowledge)


def test_duplicate_sources_rejected():
    knowledge = copy.deepcopy(seed_sections().reviewed_knowledge)
    knowledge["sources"].append(knowledge["sources"][0])
    with pytest.raises(ValueError):
        validate_knowledge(knowledge)
