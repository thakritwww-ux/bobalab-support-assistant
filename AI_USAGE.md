# AI usage and prompt documentation

## Tools and responsibilities

This project uses OpenAI's Codex assistant in this conversation for planning,
implementation and verification, and Google's Gemini API as the runtime LLM. The
assistant read the assignment/data/handoffs, proposed alternatives, generated code,
and ran local checks. The project was opened in Cursor and the candidate entered
local configuration. Independent candidate source-code edits and a Cursor AI coding
session have not been reported; later use must be recorded only after it occurs.
Do not claim a separate Cursor AI model generated this code unless that happened.

The runtime model is `gemini-3.5-flash-lite`; real generation and editor calls were
verified. This does not establish continuous free quota or reliable availability.
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

Fill subsequently asked why further personal checking was still necessary. The
assistant clarified that automated tests verify application mechanics, its output
review is preliminary, and Fill's own assessment remains pending. Authorization to
run the experiment was not acceptance of the results. Fill explicitly requested
that his contributions and this distinction be retained for the final deliverables;
CONTRIBUTION.md and the submission checklist now make that requirement explicit.

## Candidate review and continued operations — 28 October 2026

Fill preferred the hierarchy after reply for the explicit-priority example, requesting
a less adamant tone, uncertainty and a useful invitation to continue or correct the
recommendation. He later preferred after for conflicting priorities without giving
a reason. Both are recorded as qualitative preferences, not numerical scores or
approval of every claim. He then instructed the assistant to keep operations moving.

The assistant designed a follow-up that makes hypothetical assumptions explicit,
keeps recommendations conditional and offers feasible continuation without forcing
agreement questions. It also addresses the earlier loss of useful planning context
and confusion between giving advice and executing a booking. Exact implementation
wording and remaining output assessments are assistant-authored. The fresh baseline,
manual edit, resulting replies and failures are retained separately from the initial
experiment; no improvement is claimed in advance.

The hosted follow-up saved the intended edits, but one after request failed and
the remaining outputs showed mixed behavior. The assistant restored the stable
evaluated instructions and aligned the fresh-install seed with that deployed
content. docs/HIERARCHY_FOLLOWUP.md explains why; the original failure was not
replaced by a selected successful retry.

Final checks used actual curl with the README request bodies. The limited reviewer
key was read locally into a private temporary curl config and never printed or put
in process arguments; the temporary directory was removed. Health/generation and
both edit routes returned 200; missing access and malformed input returned 401/400.
The automatic probe was rejected, while the manual formatting rule saved. Stable
instructions were restored after edit probes. Twelve known live regression cases
returned replies, with relevance/tone/source-labeling weaknesses preserved. All 63
automated tests passed after final seed alignment. These checks and judgments are
assistant work, not candidate-performed verification.

## Running the application

When Fill asked how to run the chatbot, the assistant added scripts/chat.py as a
lightweight terminal API client. It reads the saved reviewer key locally, sends
questions and in-memory history to the existing hosted generation endpoint, and
supports reset/quit. It does not edit shared instructions or add a web frontend.
The client code and verification are assistant work; no candidate authorship is
claimed. README includes the direct launch command.
Two synthetic messages were sent through the live client; both returned replies,
and the follow-up correctly recalled Indonesia from the preceding message. The
process exited normally and the reviewer key was absent from captured output.
An unnecessary source citation appeared on the recall answer, consistent with the
documented relevance limitation. This is a client wiring check, not a general
quality or reliability score.

## Browser-design handoff preparation

Fill requested UI, CI, style, fonts, features, customer journey and a requirement
list to hand to a specialist design LLM. He clarified CI as visual brand identity
and required retaining the website's established name. The assistant kept BOBALAB,
prepared docs/design/, and identified confirmed decisions versus proposed branding.

The packet includes low-fidelity screen layouts, prioritized acceptance criteria,
actual API schemas, planned browser-session integration, error/state handling and
labeled existing model-output fixtures. Official IBM font/license and W3C/Flask
guidance were consulted. Selected proposed colour contrasts were calculated; no
implemented accessibility compliance is claimed. No font binaries, official logo,
browser UI or authentication adapter were created. No runtime Gemini call or other
designer-LLM contact was made for this materials task. The design brief and visual
proposals are assistant work, while the UI request and name constraint are Fill's.

Fill then supplied ui-ux-pro-max locally and authorized publication/use. The assistant
tested its design-system, UX, web and stack searches without runtime Gemini calls,
and exercised persistence into an isolated work folder. Generic FAQ/analytics/contact
escalation and simulated streaming suggestions were not adopted. The raw cyan CTA
with white normal-size text failed the selected contrast target; the reviewed
proposal retains the prior provisional green palette and IBM Plex pairing.

The user-provided files are preserved without an upgrade; their exact upstream
version is unverified. Upstream MIT attribution is included in THIRD_PARTY_NOTICES.md
and third_party/ui-ux-pro-max.LICENSE, with a supplied-file hash manifest. The
reviewed master, raw reference and rationale are included in the design packet.
This is guidance/reconciliation, not a deployed UI or measured answer improvement.


## Browser implementation — 28 October 2026

Key user instruction: “can you commit with the designing go ahead and design it”.
The assistant ran the provided UI UX Pro Max design-system search, used the reviewed
BOBALAB proposal, and wrote Flask templates, CSS, JavaScript, a limited browser-session
adapter and tests. No separate design LLM was contacted. The earlier design-only
paragraphs describe the preceding stage; a working first version is now built.

The implemented identity uses BOBALAB, deep green and warm neutral colours, self-hosted
IBM Plex Sans/Thai Looped and licensed Lucide icons. The assistant selected detailed
spacing, layout and assets. Fill requested the website, retained the name and selected
the skill; visual acceptance and personal code changes are not inferred.

89 automated tests passed with disposable PostgreSQL and scripted LLM responses.
Headless Chrome checked chat history, sources, Thai layout, errors/retry, access expiry,
reset and late-response handling. Three axe audits found no automated violations in
those tested states; this is not a complete accessibility certification. Fixture
screenshots are explicitly illustrative. Real-model/deployed checks are reported
separately in docs/WEB_UI.md and docs/VERIFICATION.md when completed. No prompt
learning or overall answer-quality improvement is claimed from the UI work.


The assistant committed/pushed the UI, manually deployed it through the existing
Render Free dashboard, then tested the deployed browser with two synthetic model
requests. Cookies/source display/Copy/mobile layout passed. The exact three README
cURL bodies also returned 200; both edit probes applied style rules this time.
The assistant restored the previous evaluated content afterward and refreshed the
prompt snapshot. This is deployment/contract evidence, not a new measured quality
gain. Fill has not yet personally accepted the finished visuals. No email was sent.


## Readability and customer conversation history

Fill asked for clearer segmentation like his ChatGPT examples and durable customer
history. He then said “then no, just website please continue”, declining Graphify
work. The assistant used UI UX Pro Max searches as references and implemented a
DOM-only Markdown subset plus optional IndexedDB history, rename/search/export/
delete, conflict detection and storage-failure recovery. These detailed technical
choices and browser/automated tests are assistant work, not candidate-authored code.
All stored customer threads remain on the device; raw replies/source metadata are
preserved. The app does not train or automatically learn from saved conversations.

Automatic approval review rejected an attempted live formatting experiment because
shared deployed prompt editing and real model calls required more specific approval.
It did not execute. The assistant prepared docs/READABILITY_RULE_PROPOSAL.md, checked
it with the local edit validator and requested explicit approval while continuing
authorized frontend work. No claim that fixture formatting proves model improvement.


Fill then explicitly selected “Approve the formatting rule and live tests.” The
assistant captured three actual baseline replies, called the hosted manual endpoint
and captured three after replies using seven provider attempts total. Only the one
style rule was added; previous rules/knowledge/policy were unchanged. The assistant
observed unsupported penalty-free booking certainty, no clear structure in the steps
case and an irrelevant payment-document detour, and restored the previous evaluated
content. All evidence is retained in docs/READABILITY_EXPERIMENT.md. No candidate
scores or overall model improvement are claimed. The frontend additionally spaces
long plain paragraphs at sentence boundaries without changing original text.


The website release was deployed on Render Free and checked with one actual synthetic
UI generation after rollback. The exact reply and prompt/source metadata persisted
through reload/reopen; Copy matched the original. The model still ignored a table
request and generalized booking terms. The frontend's sentence-boundary spacing
preserved the original prose. No learned default table behavior is claimed.
The browser suite also verified closing/restarting the same disposable profile;
22 local checks pass. These are assistant-run checks, not candidate acceptance.


Fill requested sidebar-first navigation and then another hierarchy refinement.
The assistant used the supplied UI UX Pro Max references, wrote the sidebar/mobile
drawer using the existing local history records, and tested actions, focus, contrast
and stale-write safeguards with fixtures. The first active-row contrast audit failed;
the background was darkened and retested. No new accounts or Graphify work.


The sidebar was deployed and verified before the proposed answer_layout follow-up.
Automatic approval review rejected that second live trial, requiring explicit
authorization of this exact new shared-prompt mutation and its six-attempt budget.
The command did not execute. The assistant prepared/docs-validated the candidate
and asked a specific approval question while completing sidebar evidence.


Fill explicitly selected “Approve this rule and six-attempt live test” for the exact
answer_layout candidate after the sidebar deployment. The assistant then ran the
bounded trial through /improve-ai-manually, retaining the same-content earlier
baseline transparently and guarding subsequent generation attempts. Final output
assessment and retention/rollback are recorded in docs/ANSWER_LAYOUT_V2.md.


The explicitly approved answer_layout trial used four provider attempts and applied
only the one new rule. The comparison used bullets, but the preparation reply put
format markers inline and changed a timing instruction's scope; the payment reply
added unrelated visa-channel guidance. The assistant restored the prior evaluated
prompt after these failures. Same-content baseline reuse is explicitly documented
rather than represented as newly captured. Exact replies and assessment are in
docs/ANSWER_LAYOUT_V2_RESULTS.md. No model-quality gain or candidate score claimed.
