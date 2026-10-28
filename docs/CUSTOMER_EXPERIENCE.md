# Customer-facing readability and conversation history

Fill requested clearer ChatGPT-like segmentation and durable customer-visible
conversation history, supplied list/table references, and explicitly approved the
website work while declining Graphify setup. These are his product contributions.
The assistant implemented and tested the detailed design and code. No new candidate
output scores or final visual acceptance are inferred.

## Structured replies

The browser now renders a deliberately limited Markdown subset using DOM nodes:
paragraphs, headings, bullets, numbered lists, emphasis, inline code and simple
comparison tables. Long plain paragraphs gain spacing at sentence boundaries when
the browser supports segmentation, preserving every character. Model HTML never becomes executable markup. Unsupported syntax
remains text. Links continue through the reviewed-source mechanism, with country
scope and review dates. Tables scroll inside their own keyboard-focusable region
on narrow screens; the page itself remains within the viewport.

The original aiReply is preserved for copying, later chat history and export.
No extra facts, missing options, charts, progress estimates or numerical claims are
manufactured by the renderer. It cannot turn an unstructured paragraph into an
invented comparison. A proposed separate model-formatting rule is in
[READABILITY_RULE_PROPOSAL.md](READABILITY_RULE_PROPOSAL.md); its actual activation
status is recorded there. Rendering existing text is separate from changing model
instructions or demonstrating automatic learning.

## Device-local history

Open **Conversations**, then opt into **Save conversations on this device**.
Saving is off by default. Enabling it saves the open completed conversation, and
later completed customer/reply pairs save automatically. Unsent drafts and failed
requests are not persisted. Refresh keeps saved copies but starts a blank open
conversation; reopen a saved conversation explicitly to continue it.

The panel provides titles/dates, search over titles and messages, reopen, rename,
delete, clear-all and downloads as text or JSON. Copy/export retain original reply
text and cited source references. Each reply records its received time separately
from source-review dates; /ui/chat also returns the actual captured promptVersion.
The three required assessment API responses retain their existing contracts.

Records use IndexedDB in this browser profile and website origin, with a limit of
100 conversations. There is no customer-thread table on the server, account sync,
shared-prompt learning or automatic sending of archived conversations. Reopening
sends only the selected thread on a subsequent Send; existing context/size limits
still apply, with no silent truncation. New conversation and Lock clear the open
thread/draft while saved copies remain until deleted.

This is convenience storage, not encrypted personal accounts. Anyone using the
same browser profile may access saved copies; the shared demo code does not isolate
people on that device. Browser clearing, private mode or storage eviction can lose
history. Export important synthetic test records before clearing data. Provider
handling remains separate, since messages sent for a reply go to Gemini.

Turning saving off leaves existing records. Clear-all requires confirmation and
also disables saving. Deleting the active saved copy disables saving to avoid
silently recreating it. Open copies in other tabs/devices are not erased.
Transactional revision checks reject conflicting writes from stale tabs. Full or
unavailable storage leaves the current conversation usable in memory and shows an
export/recovery notice. No automatic fallback uploads customer history.

## Verification

89 backend tests passed with temporary PostgreSQL. The reproducible browser suite
in tests/browser/customer-history.cjs passed 21 checks with synthetic model fixtures:
opt-in, refresh/reopen, context isolation, rename/search, exact export/copy, structures,
mobile overflow, inert HTML, Thai lists, stale-write rejection, confirmed deletion,
profile isolation and unavailable-storage recovery. Two axe audits reported no
automated violations (desktop structured reply, mobile history). This is limited
Chrome coverage, not full accessibility certification or measured model improvement.

The simulated fixtures are deliberately labeled and do not constitute real
before/after answer-quality evidence. The original real model evidence remains
separate. The approved formatting-rule experiment was run separately and rolled back after
regressions. See [READABILITY_EXPERIMENT.md](READABILITY_EXPERIMENT.md); frontend
readability and history do not require retaining that model change.

Deployment 352a19c succeeded on Render Free. Hosted assets, real login/session,
IndexedDB reload/reopen, Copy and mobile layout passed; invalid UI input returned
400 and browser sessions could not authorize the three reviewer API routes (401).
Those initial hosted checks used a clearly labeled intercepted local reply fixture,
with zero real model calls; they are not live generation evidence.
See [hosted report](evidence/customer-history-hosted-smoke.json).
The final presentation-only paragraph-spacing update is verified after deployment.

## Reproduce browser checks locally

Python 3.12, Node.js and Google Chrome are needed for this optional development test.
There is no production Node dependency. From the repository root:

```sh
npm install --prefix work/browser-tools --ignore-scripts playwright@1.62.1 axe-core@4.14.0
.venv/bin/python -m tests.browser.preview
```

In a second terminal:

```sh
NODE_PATH="$PWD/work/browser-tools/node_modules" node tests/browser/customer-history.cjs
```

This suite targets localhost:8002, uses its clearly named fixture demo code, and
refuses remote targets. No provider key, real database or paid model access is needed.
It writes screenshots/report into ignored work/. Stop the fixture server afterward.
