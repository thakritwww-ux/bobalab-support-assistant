# Using UI UX Pro Max for BOBALAB

The candidate supplied `.codex/skills/ui-ux-pro-max/` and authorized publishing and
using it. This is a local Python/CSV design-guidance skill, not another LLM, model
API or deployment service. Python 3.12 in the existing project environment works;
its search scripts use the standard library and need no provider key.

## Call it from the repository root

```sh
.venv/bin/python -B .codex/skills/ui-ux-pro-max/scripts/search.py \
  "customer support chatbot conversational interface minimal calm accessible multilingual Thai English" \
  --design-system -p BOBALAB -f markdown
```

Use the project's setup instructions to create .venv in a fresh checkout. An
environment with a suitable Python installation can use that interpreter directly.
The script/data folder structure must remain intact. Menu auto-discovery in other
assistants has not been verified; direct script invocation has.

Generate raw references into a separate folder so they cannot overwrite the
reviewed proposal:

```sh
.venv/bin/python -B .codex/skills/ui-ux-pro-max/scripts/search.py \
  "customer support chatbot conversational interface minimal calm accessible multilingual Thai English" \
  --design-system --persist -p BOBALAB -f markdown \
  --output-dir work/ui-ux-pro-max-generated --page chat
```

That creates work/ui-ux-pro-max-generated/design-system/bobalab/MASTER.md and
pages/chat.md. The reviewed starting proposal lives separately at
[design-system/bobalab/MASTER.md](../../design-system/bobalab/MASTER.md).

Useful follow-up searches:

```sh
.venv/bin/python -B .codex/skills/ui-ux-pro-max/scripts/search.py \
  "chat focus scroll status messages keyboard" --domain web --json
.venv/bin/python -B .codex/skills/ui-ux-pro-max/scripts/search.py \
  "loading error recovery feedback" --domain ux --json
.venv/bin/python -B .codex/skills/ui-ux-pro-max/scripts/search.py \
  "responsive form keyboard focus" --stack html-tailwind --json
```

The stack search is reference guidance, not a mandate to replace the Flask service
or introduce a new frontend host. Product/user requirements override generic skill
recommendations. See [third-party notices](../../THIRD_PARTY_NOTICES.md) and
[the supplied-file manifest](ui-ux-pro-max-provenance.json).

## What the generated output changed or did not change

| Tool recommendation | Review decision |
|---|---|
| Minimal-chrome conversational UI | Use as a direction for the chat screen; no full dashboard |
| Keyboard support, visible focus, inline errors and recovery | Retain; prefer native controls over the example clickable div |
| Async loading feedback | Retain an honest pending state; no fake stream/progress |
| FAQ/search landing, analytics, contact escalation | Do not adopt; outside the requested chat and unavailable backend capabilities |
| Purple/cyan palette | Keep as an unreviewed alternative; current warm-neutral/green proposal remains |
| Noto Sans Thai | Record as an alternative; no font switch or unverified licensing claim |
| Streaming/pulse/context-card effects | Do not copy as real capabilities; no stream or structured-card API exists |
| Accessibility/performance checkmarks | Do not treat as measured compliance or performance evidence |

The raw button suggestion uses white text on cyan #06B6D4. Its measured contrast is
recorded in ui-ux-pro-max-review.json and does not meet our normal-size action-text
target. The retained palette's previously computed checks remain separate from a
future rendered UI/accessibility audit.

The reviewed master/page files are assistant-authored reconciliations of generated
guidance and the existing handoff. They are not a final user-approved visual system
or a working website. The specialist can propose changes while preserving the
BOBALAB name, API/security constraints and honest capability boundaries.
