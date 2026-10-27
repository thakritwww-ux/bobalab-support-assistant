# AI usage and prompt documentation

## Tools and responsibilities

This project is being implemented with AI assistance in this conversation. The
assistant read the assignment/data/handoffs, proposed alternatives, generated code,
and ran local checks. Cursor is installed and selected for the candidate's project
review/run/edit workflow; its actual use must be recorded after it occurs.
Do not claim a separate Cursor AI model generated this code unless that happened.

The runtime model is configured as `gemini-3.5-flash-lite`. Until the free account
connection check succeeds, this is a configured choice, not a verified live result.
The final runtime prompts are `prompts/policy.md`, `prompts/editor.md`,
`prompts/playbook.json`, plus the reviewed knowledge snapshot in `data/knowledge.json`.

## Selected exchanges that shaped the project

### Assignment understanding

**User:** “go through the conversations.json and understand what youre working with”.

**Relevant assistant response:** identified 15 conversations / 262 messages, 128
reply sequences, synthetic timing, contradictory totals, unavailable operational
actions and problematic concealment advice. These are AI-suggested findings;
candidate verification is recorded separately.

### Ownership and accurate terminology

**User:** asked whether individuality and judgment about learning should be solidified
before building, and requested realism rather than hallucination.

**Relevant assistant response:** distinguished prompt optimization from reinforcement
learning/model-weight training, stated that competitors' work is unknown, and proposed
testing rather than assuming superiority.

### Candidate's product judgment

**User decisions:** concern-first support; explain uncertainty and prepare for review;
allow tone plus conditional support rules; use reviewed sources; API/documentation
without a frontend; strictly free services.

**User's own contribution:** “giving sources and leading them on to the steps that
they can do, the options they can do and the pros and cons for each help them
visualize the path ahead”.

**Relevant assistant response:** translated that into a conditional rule for
consequential decisions and an accommodation-planning evaluation case. This remains
a hypothesis until actual outputs are reviewed.

### Implementation instruction

**User:** “PLEASE IMPLEMENT THIS PLAN”, followed by the agreed implementation and
evidence plan (27 October 2026).

**Relevant assistant action:** generated the Flask service, database versioning,
shared edit validator, source collection, dataset parser, evaluation tools, tests,
and free-service setup instructions. It explicitly separated simulated local tests
from pending real-model evidence and requested account setup without asking for keys
in chat.

## Accepted, modified and rejected suggestions

- Accepted: controlled learning and explicit capability boundaries, subject to testing.
- Candidate-shaped: source-backed options and tradeoffs, with understandable next steps.
- Removed from core: frontend, live browsing, vector search, fine-tuning, paid services,
  and an unrestricted-learning benchmark.
- Simplified: one editor classifies and proposes edits; no separate screener call.
- Rejected assumption: consultant references are inherently correct or every conversation
  should silently update shared instructions.

## Verification record

### Setup follow-up

After the candidate entered local configuration, a live metadata request reached
the configured Gemini model. Actual reply generation remains untested. The database
connection retained a password placeholder, so no Supabase migration or seed
succeeded. The assistant added actionable configuration validation and tested it;
it did not fabricate successful connection results. GitHub authentication was
verified and a candidate-owned repository was created. No secrets were copied
into this record.

After the database placeholder was replaced, Supabase initialization and real Gemini
generation succeeded. The first eight development examples made two edits, five
rejections and one no-op. AI-assisted review found no clear overall quality gain and
possible scope/relevance regressions; the assistant restored the initial playbook
while preserving versions and real before/after outputs. Subsequent manual style
corrections were tested on known validation cases, explicitly separated from the
four-conversation final comparison. No personal candidate scores were invented.

During payment-response review, Fill proposed contacting the transaction team and
following up, then revised toward a capability limit and document preparation. The
assistant explained the unavailable actions and the need to keep preparation tied
to payment evidence rather than inventing a required checklist. Original input and
assistant adaptation are distinguished in CONTRIBUTION.md.

The assistant deployed the service through the candidate's signed-in Render
workspace, selected Free compute, configured the start command and public health
path, and had the candidate enter secrets directly in Render. Hosted health and
all required endpoint contracts returned 200. Further editing probes included
rejections and a 503; a specific manual rule was persisted, but its post-edit reply
did not follow the requested bullet formatting. These failures are retained.

See `docs/VERIFICATION.md` for actual local results and pending checks. Tests use
explicit fakes where stated; no test output is represented as a live Gemini reply.
Add the candidate's actual source review, code modifications, output scores and
rejected AI suggestions as they happen. Keep provider keys, database credentials,
private communications and unrelated conversation content out of this log.

## Answer hierarchy follow-up

Fill proposed a customer-facing information hierarchy and asked whether manually
defining answer layers would help. The assistant explained that existing rules
already express concern-first organization, so overlapping instructions should be
refined rather than added as a separate mechanism. It proposed conditional answer
patterns and a controlled manual-improvement experiment.

Fill's decision was: "I think a combination of describing the options and make a
conditional recommendation is the best way to do it". After further explanation,
he authorized proceeding. His review of the earlier output pairs is deferred,
not assumed completed.

The assistant authored six known synthetic validation cases, prospective criteria
and specific replacement text for the direct and choices rules. It captured fresh
before replies from the restored evaluated prompt and submitted the refinement
through the hosted manual endpoint. The exact instruction, saved prompt diff and
actual outputs are recorded in docs/ANSWER_HIERARCHY.md and
docs/HIERARCHY_COMPARISON.md. The hosted edit applied exactly the intended two
replacement rules and all six before/after pairs returned replies. AI-assisted
review found clearer option-first ordering in the explicit-preference case but
remaining unsupported assumptions and missing accommodation guidance. The assistant
restored the previously evaluated live instructions while preserving the experiment.
This is not represented as a candidate verdict or an overall quality gain. No new
visa facts, agency policies, capabilities or weight training are part of this work.
