import json
import re

from app.schemas import Rule, Sections

# Defense in depth, not a semantic proof. The editor and behavioral evaluations
# also check whether proposed rules smuggle new facts into the playbook.
SENSITIVE = re.compile(
    r"\d|https?://|www\.|\[[A-Z_]+\]|[\w.+-]+@[\w.-]+|"
    r"\b(?:Thailand|Thai|Laos|Malaysia|Indonesia|Singapore|Vietnam|Taiwan|"
    r"Australia|Germany|Korea|Bangkok|Vientiane|Jakarta|Phuket|Chiang Mai)\b",
    re.IGNORECASE,
)
UNSAFE = re.compile(
    r"(?:ignore|override|disable|bypass).{0,35}(?:policy|guardrail|protected|safety)|"
    r"(?:hide|conceal|omit|don't mention|do not mention).{0,40}(?:client|employment|relevant|income)|"
    r"(?:confirm|verify|verified|received).{0,20}(?:payment|bank balance)|"
    r"(?:payment|bank balance).{0,20}(?:confirmed|verified|received)",
    re.IGNORECASE,
)


def words(text):
    return re.findall(r"\w+", text.casefold())


def repeats_context(text, context):
    tokens = words(text)
    context_tokens = words(json.dumps(context, ensure_ascii=False))
    context_runs = {tuple(context_tokens[i : i + 6]) for i in range(len(context_tokens) - 5)}
    return any(tuple(tokens[i : i + 6]) in context_runs for i in range(len(tokens) - 5))


def apply_edits(sections, proposal, context):
    rules = {rule.id: rule.text for rule in sections.editable_playbook}
    # A proposal is atomic: one invalid operation rejects the entire edit batch.
    for edit in proposal.edits:
        if edit.action == "add" and edit.rule_id in rules:
            return sections, "duplicate_rule"
        if edit.action in ("replace", "delete") and edit.rule_id not in rules:
            return sections, "unknown_rule"
        if edit.action == "delete":
            if edit.text:
                return sections, "unexpected_text"
            del rules[edit.rule_id]
        else:
            if not edit.text or SENSITIVE.search(edit.text) or UNSAFE.search(edit.text):
                return sections, "restricted_content"
            if repeats_context(edit.text, context):
                return sections, "context_copy"
            rules[edit.rule_id] = edit.text
    if not 1 <= len(rules) <= 30 or sum(map(len, rules.values())) > 8000:
        return sections, "playbook_limit"
    candidate = Sections(
        protected_policy=sections.protected_policy,
        reviewed_knowledge=sections.reviewed_knowledge,
        editable_playbook=[Rule(id=k, text=v) for k, v in rules.items()],
    )
    return candidate, None
