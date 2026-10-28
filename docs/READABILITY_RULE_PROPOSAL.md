# Proposed conditional reply formatting

Status: prepared for explicit approval; not applied to the live prompt.

Fill approved website readability and optional on-device history. The implemented
renderer can display existing Markdown safely without rewriting advice. To also
encourage the model to choose readable structures, the assistant proposes adding
one editable style rule while preserving all existing rules and reviewed facts:

> For replies with several distinct points, start with a short direct answer and use brief descriptive Markdown headings, bullets or numbered steps where useful. Use a compact Markdown comparison table only for supported options with meaningful tradeoffs. Keep uncertainty and the practical next step visible. Keep simple answers short without forced headings. Never invent data, charts, probabilities, progress indicators, requirements or actions for presentation.

Proposed rule ID: readable_structure. Category: style.

An attempted live before/after experiment was rejected by automatic approval review:
website approval was not considered specific authorization for a shared deployed
prompt change and real model calls. The attempt did not execute. No bypass or
indirect activation is authorized by this document.

On explicit approval, capture matched real baseline replies, call the existing
/improve-ai-manually endpoint with this instruction, verify existing rules and
protected/knowledge sections remain unchanged, and compare the same inputs/settings.
Record failures and regressions. Restore the original prompt if the change is not
acceptable. No model-quality or prompt-learning benefit has been established by the
frontend implementation or synthetic display fixtures alone.
