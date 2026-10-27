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
- Source was pushed to the public main branch of
  https://github.com/thakritwww-ux/bobalab-support-assistant and repository visibility
  and branch presence were verified through GitHub.

Reproduce the full database suite with a disposable `TEST_DATABASE_URL` or the
local runner described in README. Plain pytest skips database tests when no
disposable test database is configured; this is not a cloud Supabase test.

## Not yet verified

- Render deployment, cold-start behavior and hosted cURL tests.
- Candidate verdicts and any general answer-quality improvement claim.
- Candidate source review and actual code modifications in Cursor.
- Final submission package and externally hosted endpoint access.

No claim of measured model improvement or deployment readiness is made from the
local test count. Real source support, naturalness, country scope and privacy need
behavioral assessment; structural tests alone cannot establish them.
