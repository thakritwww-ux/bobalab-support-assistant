# BOBALAB — support that learns carefully

A Thai DTV customer-support API that improves its database-stored instructions
without treating consultant replies as unquestionable facts. No model weights are
trained. A responsive BOBALAB browser chat and a small terminal client exercise the same generation service.

**Repository:** [thakritwww-ux/bobalab-support-assistant](https://github.com/thakritwww-ux/bobalab-support-assistant).

**Hosted API:** https://bobalab-support-assistant.onrender.com — [public health check](https://bobalab-support-assistant.onrender.com/health).

**Status:** implemented locally with live Supabase and Gemini connections verified.
The first real learning batch applied two edits, rejected five lessons, and made one
no-op. This does not establish a quality gain. The service is deployed on Render
Free and all three hosted endpoints returned 200 in recorded live tests. Fill has
reviewed two hierarchy comparisons; further cases and numerical scores remain
unreviewed. See [live results](docs/LIVE_RESULTS.md) and the
[requirement-to-evidence map](docs/REQUIREMENTS_MAP.md).

**Browser interface:** responsive English/Thai chat, reviewed-source links, copy,
new conversation, access expiry and explicit error/retry states. See
[browser implementation and access](docs/WEB_UI.md). The user-provided
[UI UX Pro Max skill](.codex/skills/ui-ux-pro-max/SKILL.md) informed the design;
[design materials](docs/design/README.md) distinguish the original proposals from
the implemented first release. This does not change model instructions or prove
better answers.

## Try the service

### Open the website

Open https://bobalab-support-assistant.onrender.com and enter the privately supplied
**demo access code**. Render Free may take time to wake. This limited code permits
chat only; do not enter the reviewer API key, a provider key or a password.

The project owner can create the private access instructions locally:

```sh
.venv/bin/python -m app.cli write-web-access
```

Read `work/WEB_DEMO_ACCESS.txt` locally and share only its limited demo code privately.
Chat remains in the current tab's memory; refreshing clears it. Use synthetic data.
The API cURL workflow and its separate reviewer key remain available below.

### Type questions in the existing project

The hosted API is already running. In Cursor, open Terminal → New Terminal and run:

```sh
cd /Users/fila/Documents/Bobalab
.venv/bin/python -m scripts.chat
```

This lightweight API test client reads the existing local reviewer key, keeps chat
history in memory, and prints the assistant's replies. It does not save a transcript
or change the shared prompt. Type `/reset` to start fresh or `/quit` to exit. Use
synthetic questions only. For a different checkout, use its actual project path.

### Start the API locally or set up a fresh checkout

Complete [free account setup](docs/SETUP.md), then:

```sh
uv venv --python 3.12
source .venv/bin/activate
uv pip sync requirements-dev.txt
# Copy .env.example to .env only if .env does not already exist; edit it in Cursor.
python -m app.cli check-config
python -m app.cli migrate
python -m app.cli seed
python -m app.cli check-live
python -m flask --app 'app:create_app()' run --port 8000
```

`check-config` prints credential presence and setup problems without values. It
rejects an unreplaced database-password placeholder. `check-live` makes one
real synthetic generation call. Seeding is idempotent: restarting does not erase
learned instructions. Python 3.12 is required by the verified development setup.

### Three required cURL examples

In a second terminal, activate the environment and set these **application** values:

```sh
export BASE_URL='https://bobalab-support-assistant.onrender.com'
export REVIEWER_API_KEY='replace-with-the-privately-provided-reviewer-key'
```

For local testing use `BASE_URL='http://127.0.0.1:8000'`. Provider and
database credentials are never needed by reviewers. Keep the reviewer key out of
the public repository; include it privately with the submission.

**1. Generate**

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/generate-reply" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"How long should I book accommodation? I need to keep costs down.","chatHistory":[{"role":"client","message":"I am planning a DTV application in Kuala Lumpur."}]}'
```

Response shape: `{"aiReply":"Generated customer reply, with reviewed source links when used."}`.
This is a shape illustration, not an observed live result. For this case, assess
whether the reply explains uncertainty and booking tradeoffs rather than promising
a two-week completion date.

**2. Improve from a consultant example**

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"What do you mean by proof of funds?","chatHistory":[],"consultantReply":"That means evidence of money available to support your stay. I should explain an unfamiliar term in plain language before moving on."}'
```

Response contains `predictedReply`, `updatedPrompt`, `versionId`, `learningStatus`,
`appliedEdits`, and `rejectedLearnings`. The status is `applied`, `no_change`, or
`rejected`. The example does not guarantee an edit: the starting prompt may already
cover the lesson. Actual learning is documented from real outputs, not assumed.

To exercise rejection, supply a consultant reply claiming a payment is verified
because the customer says so, or coaching concealment of a relevant client. A
correct editor should reject that lesson; useful unrelated style edits may still
be accepted. Rejection by itself does not satisfy the successful-learning requirement.

**3. Improve manually**

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai-manually" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"instructions":"Add this formatting rule verbatim if it is not already present: Use short bullet lists for multi-step preparation instructions, preserving essential qualifications and a clear next step."}'
```

Response contains `updatedPrompt` and the same version/status metadata. Generate
the same question again to assess the effect. Manual instructions cannot introduce
unreviewed facts or override capability limits.

`GET /health` is public **liveness only**. It does not assert model/database readiness.
All model-backed routes require `X-API-Key`. History is oldest to newest; join
consecutive customer messages with newlines in the string `clientSequence`.

### Errors and limits

Errors use `{"error":{"code":"...","message":"..."}}`:

| HTTP | Meaning |
|---|---|
| 400 / 415 | Invalid fields, context limit, malformed JSON or wrong content type |
| 401 | Missing or incorrect reviewer key |
| 409 | Active version changed while an edit was being generated; retry |
| 413 | Body exceeds 64 KiB |
| 429 | Request rate or daily application model-call budget reached |
| 502 | Invalid structured model output, citation, or placeholder |
| 503 | Unconfigured/unavailable model or database, or model timeout |

Limits: 6,000 characters per message, 100 history entries, 24,000 total conversation
characters, 4,000 manual-instruction characters, 30 playbook rules / 8,000 rule-text
characters. Model outputs and retries are bounded. Default application allowance:
100 attempted model calls per Bangkok day; every retry counts. This is not a promise
of provider quota. Request throttling is process-local (10/minute); the deployment
uses one worker. The durable call budget is shared in Postgres across workers/restarts.
No success reply is fabricated when a dependency fails.

## Findings → design decisions

| Finding in the 15 conversations | Decision |
|---|---|
| Laos line items do not match the quoted total | Explain the conflict; confirm an itemized quote instead of inventing a payable amount. |
| Consultant claims include account/payment/document actions | The demo explicitly has no such integrations. Customer claims are not verified system state. |
| Some consultant replies coach concealment | Reject that lesson; suggest honest qualified review. |
| Replies are warm and semi-formal, not slang-heavy | Use approachable plain language with concise structure. |
| Every conversation ends outbound; timing is artificial | Discuss friction signals, not observed ghosting rates or conversion predictions. |
| The sample estimates Kuala Lumpur at 10–14 business days | Prefer the scoped official page's month-or-more estimate, with uncertainty. |
| Fill wanted sources, options, pros/cons and a path forward | For consequential choices, make practical tradeoffs visible; keep simple answers simple. |

Fill also proposed a customer-facing answer hierarchy and chose to combine option
descriptions with conditional recommendations. He reviewed two actual comparison
pairs, preferring after and requesting a less adamant tone, uncertainty and useful
continuation on the first. The assistant implemented and tested the experiments;
mixed results led to restoration of the stable instructions. His decisions and
feedback are distinguished from assistant-authored code, tests and assessments in
[CONTRIBUTION.md](CONTRIBUTION.md) and [AI_USAGE.md](AI_USAGE.md).

The assignment calls the input `conversations.py` in one place; the actual file is
`conversations.json`. See [data findings](docs/DATA_FINDINGS.md) and
[source review](docs/SOURCES.md).

## Architecture and learning workflow

```text
Request + history → validate/authenticate → read active database version
    → Gemini structured JSON → validate citations → customer reply

Consultant example → prediction using captured version → editor classification/edits
    → deterministic edit validation → atomic new version + active pointer + audit
```

The compiled prompt has **protected policy**, **reviewed knowledge**, and **editable
playbook** sections. Automatic and manual editing share one validator. The editor
only proposes add/replace/delete operations on playbook rules; it cannot replace
the whole prompt or directly edit protected sections. One invalid operation rejects
the entire edit batch. Valid partial learning can retain style edits and report
rejected factual lessons.

The editor is an LLM and may misclassify content. Structural protection and lexical
checks do not prove semantic safety; behavioral evaluation is necessary. No new
reviewed source is accepted merely because a consultant mentioned it.

Postgres stores append-only snapshots, one active pointer, sanitized events, and
the shared daily usage counter. A database trigger prevents rewriting version
history. Compare-and-swap activation prevents stale edits overwriting a newer prompt.
No database transaction remains open while waiting for Gemini. Audit events contain
operation IDs/categories, not raw customer text or model explanations.

Generation normally uses one model call, automatic improvement two, and manual
improvement one, each with at most one retry. No live browsing, fine-tuning, vector
database, agent framework, operational integration or automatic paid fallback exists.

### History, rollback and explicit knowledge review

```sh
python -m app.cli history
python -m app.cli rollback UUID_FROM_HISTORY
python -m app.cli review-knowledge data/knowledge.json --reviewed
```

Rollback creates a version restoring earlier playbook behavior while preserving
current protected policy and knowledge. A knowledge update requires local operator
access and explicit review confirmation; verify source text, country scope, date and
conflicts first. Re-running seed does not update an existing knowledge snapshot.

## Evaluation and evidence

```sh
python -m app.cli build-pairs
python -m scripts.evaluate capture --output docs/evidence/before.local.json
python -m scripts.replay --limit 8
python -m scripts.evaluate capture --output docs/evidence/after.local.json
python -m scripts.evaluate compare docs/evidence/before.local.json docs/evidence/after.local.json
```

These are real, quota-consuming calls; no fake model fallback exists. Review the
results before sharing. The replay script uses development conversations only and
preserves completed results if a later call fails. Capture pins one prompt version
for all cases. Comparison checks equal inputs, model and temperature, shows actual
prompt differences, and flags knowledge changes as a confound. It does not fabricate
scores or verdicts. Repeat a small subset if results are borderline; low temperature
does not make a model deterministic.

All 128 pairs are traceable. Eight development, three validation and four final
conversations are declared in `data/splits.json`. We already inspected all the data:
“final” means excluded from automatic updates, **not unseen by developers**.
The supplementary behavioral cases are known test fixtures, not independent unseen
data. See [candidate case sheet](docs/CASE_REVIEW.md) and [evidence status](docs/BEFORE_AFTER.md).

Real records now include the [automatic comparison](docs/BEFORE_AFTER.md),
[manual example](docs/MANUAL_IMPROVEMENT.md), [validation-driven style correction](docs/STYLE_REFINEMENT.md),
and [four-conversation final comparison](docs/FINAL_COMPARISON.md). Applied edits
did not establish a clear overall quality gain; an over-narrowed rule was rolled
back. Candidate verdicts are pending. The initial canary comparison preserves its
20-second timeout; the service default is now 30 seconds and that operational
change is not credited as learning.

A separate [answer hierarchy experiment](docs/ANSWER_HIERARCHY.md) records Fill's
choice to combine option descriptions with a recommendation tied to stated
priorities. Its six known validation cases also check conflicting priorities,
missing evidence, payment capability and simple-answer regressions. It is a manual
instruction refinement, separate from the automatic-learning evidence.
The hosted edit saved successfully and all six paired cases returned replies, but
the results were mixed. The previous evaluated instructions were restored; the
experimental hierarchy version remains available in history and its full
[before/after comparison](docs/HIERARCHY_COMPARISON.md) is retained.
The [candidate-feedback follow-up](docs/HIERARCHY_FOLLOWUP.md) also had mixed results
and one failed after request; it was restored rather than represented as a reliable
improvement. The checked-in seed playbook now matches the restored evaluated
instructions; the current database snapshot is in docs/evidence/prompt-snapshot.json.

Capture that suite using the current prompt or an immutable version from this
database's history. These calls consume the same daily free allowance:

```sh
python -m scripts.evaluate capture --suite hierarchy \
  --output docs/evidence/new-hierarchy.local.json
```

To evaluate an immutable earlier version on the final suite without changing the
active prompt, replace `UUID` with a version from history:

```sh
python -m scripts.evaluate capture --suite final --version UUID \
  --output docs/evidence/new-final.local.json
```

### Automated verification

```sh
pytest -q
ruff check app scripts tests
ruff format --check app scripts tests
```

Ordinary tests use simulated model outputs and skip PostgreSQL integration tests
unless `TEST_DATABASE_URL` names a disposable test database. Integration tests use
isolated schemas and check real persistence, concurrent updates, transactional
rollback, immutable history, and atomic usage limits. Optional local server runner:

```sh
python -m scripts.test_postgres --bin-dir /path/to/postgres/bin
```

Do not point `TEST_DATABASE_URL` at production. Local verification results and
outstanding live checks are recorded in [verification](docs/VERIFICATION.md).

## Deployment and limitations

Follow [setup](docs/SETUP.md). The Render Blueprint pins a Free web service. Prompts
live in Supabase, not Render's ephemeral filesystem. Deployment runs schema migration
and idempotent seeding before serving traffic. Render can cold-start after inactivity;
the service is not guaranteed always-on. See [Render Free](https://render.com/docs/free)
and [Supabase pricing](https://supabase.com/pricing).

The deployed service was created from the public repository with Python 3, Free
compute, `sh scripts/start.sh`, and `/health`. Tested runtime code revision:
`9b7a751`. The hosted smoke sample took 30.45 seconds for generation, 68.796 seconds
for automatic improvement and 33.158 seconds for manual improvement. These are
individual observations, not averages or uptime guarantees. Idle cold-start latency
has not been measured. A 200 response from an editing endpoint can report a no-op
or rejected edit; inspect `learningStatus` and the recorded evidence.

Use **synthetic data only**. The model provider receives request content. Google
documents product-improvement use of free-tier content. No customer conversation
store is implemented; the caller supplies history. No real payment, document upload,
account lookup, legal review, or notification is performed.

Knowledge coverage is deliberately small. Missing missions and stale/ambiguous
information require review. Source existence checks do not establish that every
sentence is supported. Privacy checks are best effort, especially for names and
non-English content. A compromised reviewer key permits edits within implemented
limits and can exhaust the daily model allowance; rotate it in local and hosted config.

## Submission

Deadline: **28 October 2026, 23:59 Bangkok time**. Submit to
`bobalabth@gmail.com` with subject **BOBALAB Technical Assessment — Thakrit Wongwiwatseree**.
Include the accessible GitHub URL, live Render URL, three cURL examples and private
reviewer key, README, real before/after evidence, [contribution summary](CONTRIBUTION.md),
and [AI usage log](AI_USAGE.md). URLs and measured results must be filled only after
they exist. Sending the email requires the candidate's instruction.
