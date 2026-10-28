# Verification record

Verified locally on 27 October 2026, Bangkok time.

## Completed

- Python 3.12.14 environment and pinned runtime/development requirements installed.
- **63 tests passed** against a temporary PostgreSQL 16.2 server, with scripted
  model outputs. The server was stopped and temporary database data removed.
- Actual database tests cover persistence across connections, idempotent startup,
  one-winner concurrent edits, rollback of the entire transaction after a failed
  event insert, no-op event logging, immutable history, and the shared call budget.
- All three endpoint flows were exercised with real PostgreSQL and a simulated
  LLM. Automatic/manual edits persist; subsequent reads observe the active version.
- Other tests cover auth, request/body limits, citation and placeholder rejection,
  edit boundaries, bounded retries/timeouts, data extraction and review metadata.
- `ruff check app scripts tests` and `ruff format --check app scripts tests` pass.
- Parser returns 128 traceable examples and preserves the documented edge cases.
- A clean source copy, without .env, installed its pinned dependencies into a fresh
  environment and passed the complete 58-test suite against temporary PostgreSQL.
- Real loopback HTTP requests against Gunicorn returned 200 for health, 401 for a
  missing reviewer key, 400 for invalid input, and an explicit 503 when the database
  was not configured. These are local checks, not hosted or live-model evidence.
- The local Git repository excludes .env, environments, temporary data and the
  personal handoff PDF. Exact configured secrets were not present in tracked files.
- The project folder was opened in Cursor; candidate review has not yet occurred.
- Subsequent setup checks now reject an unreplaced database-password placeholder
  before attempting a connection. Two additional tests cover that behavior.
- Gemini model metadata was accessible through the configured SDK client. This is
  not a generation or free-quota verification.
- Subsequent live checks verified Supabase migration/seeding and actual Gemini
  generation. All three local HTTP endpoints returned 200 using real dependencies;
  the manual endpoint persisted an edit. Selected results are in
  `docs/evidence/local-http-summary.json`.
- Eight real development examples produced two applied edits, five rejections and
  one no-op. The paired canary run had eight cases with replies on both sides;
  service failures and lack of clear overall quality gain are retained in evidence.
- A separate four-conversation comparison excluded from automatic learning returned
  four replies on each side at matched settings. Candidate scores remain pending.
- A fresh anonymous clone of published code revision `9b7a751`, without .env,
  installed its pinned dependencies into a new environment and passed all 63 tests
  against temporary PostgreSQL.
- Render Free deployment succeeded at https://bobalab-support-assistant.onrender.com.
  Public health and all three authenticated hosted API routes returned 200.
  Hosted edit outcomes must still be read separately from HTTP status; selected
  evidence is in `docs/evidence/hosted-http-summary.json`.
- A specific harmless formatting rule was successfully saved through the hosted
  manual endpoint. The following reply did not follow the requested bullet format;
  this limitation and earlier rejected/unavailable probes are explicitly recorded.
- Source was pushed to the public main branch of
  https://github.com/thakritwww-ux/bobalab-support-assistant and repository visibility
  and branch presence were verified through GitHub.
- A later candidate-led answer hierarchy experiment exercised the real hosted
  manual endpoint, which saved exactly the intended direct/choices replacements.
  All six before and six after generations returned replies at matched settings;
  protected policy and reviewed knowledge were unchanged. AI-assisted assessment
  found mixed behavior, so the prior evaluated instructions were restored. See
  docs/ANSWER_HIERARCHY.md for the limitations and actual comparison.
- After adding the hierarchy evaluation suite, all 63 tests passed again against
  disposable PostgreSQL; the temporary server was stopped by the test runner.

Reproduce the full database suite with a disposable `TEST_DATABASE_URL` or the
local runner described in README. Plain pytest skips database tests when no
disposable test database is configured; this is not a cloud Supabase test.

## Not yet verified

- Render idle cold-start behavior and long-term availability.
- Remaining candidate verdicts and any general answer-quality improvement claim.
- Candidate source review and actual code modifications in Cursor.
- Final submission package and independent reviewer access using the privately supplied key.

## Final local/hosted checks — 28 October 2026, Bangkok

- Aligned the fresh-install playbook with the restored evaluated database content;
  no policy, source or runtime API code changes were made. Existing DB seeding stays
  idempotent. After this alignment, all 63 tests passed with disposable PostgreSQL;
  lint and formatting passed, and the temporary test server was stopped.
- The feedback follow-up saved intended rules but had mixed results and one failed
  after request. Stable content was restored; exact evidence is in HIERARCHY_FOLLOWUP.md.
- All twelve known live regression requests returned replies. This is availability
  evidence, not twelve passing semantic judgments; relevance and source-labeling
  weaknesses are documented in SUBMISSION_REGRESSIONS.md.
- Actual curl used all three README request bodies against the public API with a
  private temporary access-key config. Required routes returned 200, missing access
  401 and invalid input 400. Automatic editing was rejected; manual editing saved a
  rule, then evaluated content was restored. Temp key/config files were removed.
- A first resumed health request took 52.409 seconds; actual idle/sleep state was not
  observed. This does not establish cold-start or long-term availability guarantees.
- Current prompt ID/content are exported in evidence/prompt-snapshot.json, with the
  earlier equivalent evaluated version recorded for traceability.
- The terminal API client was checked with two synthetic live messages and quit:
  both returned replies, the follow-up recalled the earlier application country,
  the process exited normally, and the reviewer key was not printed. No shared
  instruction editing or local server is required to use the hosted client.

No claim of measured model improvement or deployment readiness is made from the
local test count. Real source support, naturalness, country scope and privacy need
behavioral assessment; structural tests alone cannot establish them.


## Optional browser interface — 28 October 2026

After Fill authorized implementation, all **89 tests passed** with disposable
PostgreSQL and scripted LLM outputs. Chrome also passed 15 interaction checks with
seven simulated generation requests and no JavaScript errors. Three axe audits
(desktop access, mobile active chat and mobile About) reported no automated
violations. The report is [web-browser-checks.json](evidence/web-browser-checks.json).
This does not establish full accessibility compliance or better model answers.
See [WEB_UI.md](WEB_UI.md) for architecture, boundaries and deployed checks.


The browser release was deployed on the existing Render Free service (ae3dd2e).
Two real browser sends returned 200 with correct follow-up recall; Secure/HttpOnly/
SameSite=Strict cookies, source rendering and full-reply Copy passed. Five viewport
sizes showed no horizontal overflow in additional simulated checks.
All three README cURL examples returned 200 after deployment, with 401 for missing
access and 400 for malformed input. Automatic and manual probes both applied a
style rule; stable content was restored afterward as version
23f300e4-4acb-40cc-9cad-dc6b6b28927c. See
[web-release-http-summary.json](evidence/web-release-http-summary.json) and
[web-hosted-live.json](evidence/web-hosted-live.json). These observations do not
replace candidate review or prove overall answer improvement.


## Customer readability and device-local history

89 backend tests passed after adding captured prompt-version metadata to /ui/chat.
The new reproducible Chrome suite passed 22 synthetic checks covering opt-in/off/on,
refresh/reopen, thread-only context, rename/search, export/copy, headings/lists/tables,
mobile containment, inert HTML, Thai rendering, stale writes, single/all deletion,
profile isolation and unavailable-storage recovery. Two axe states had no automated
violations. The prior 15-check browser regression suite also passed with three axe
states. See [customer experience](CUSTOMER_EXPERIENCE.md) and
[report](evidence/customer-history-browser-checks.json). These tests use clearly
labeled fixtures, not real model before/after quality evidence.


The specifically approved live readability experiment used seven provider attempts:
three before replies, one manual edit and three after replies. Existing rules and
reviewed facts remained unchanged. The model produced useful headings/bullets in
one case but also unsupported booking certainty and an irrelevant payment detour;
the steps case stayed dense. The stable prompt was restored as
34d6cf6a-bfe6-4fff-b76b-53718b5caa1a. All outputs and the rollback are preserved in
[READABILITY_EXPERIMENT.md](READABILITY_EXPERIMENT.md). No overall quality gain claimed.


Final website presentation code 63dac82 deployed successfully on Render Free. A real
hosted browser send returned 200 with prompt version
34d6cf6a-bfe6-4fff-b76b-53718b5caa1a. Original reply/source metadata persisted through
refresh/reopen and matched Copy. The model did not follow the explicit table request;
the frontend displayed the prose with sentence-boundary paragraph spacing. This
limitation is preserved in customer-history-real-smoke.json. A separate disposable
persistent browser-profile test verified history survives browser close/restart.
The full customer-history browser suite now passes 22 checks.
