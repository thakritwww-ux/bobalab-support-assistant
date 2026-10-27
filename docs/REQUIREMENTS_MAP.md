# Requirement-to-evidence map

Checked against the public assessment README and the candidate-provided invitation
on 28 October 2026, Bangkok time. This map describes evidence and gaps rather than
declaring every candidate-review task complete.

| Requirement | Implementation or evidence |
|---|---|
| Source and dependencies | Public repository; pinned requirements.txt and requirements-dev.txt |
| Hosted service | https://bobalab-support-assistant.onrender.com; health is liveness, model routes require reviewer access |
| Reply from current messages and history | POST /generate-reply; validated clientSequence/chatHistory; immutable active prompt captured per request |
| Database prompt storage and retrieval | Supabase Postgres prompt_versions and active pointer; history and rollback CLI |
| Automatic improvement from consultant examples | POST /improve-ai; prediction and editor share a captured version; eight actual development examples produced two applied edits, five rejections and one no-op |
| Manual improvement | POST /improve-ai-manually; real persisted changes and no-op/rejection cases; hierarchy experiments include exact instructions and resulting outputs |
| Before/after evidence and assessment | BEFORE_AFTER.md, MANUAL_IMPROVEMENT.md, STYLE_REFINEMENT.md, FINAL_COMPARISON.md and HIERARCHY_COMPARISON.md; successful persistence is distinguished from answer-quality improvement |
| Three cURL examples and response formats | README.md; never include the reviewer key's actual value in public examples |
| Setup and architecture | README.md, SETUP.md, schema, prompt files and source collection |
| Personal decisions and AI disclosure | CONTRIBUTION.md, CASE_REVIEW.md and AI_USAGE.md; two actual candidate preferences recorded, remaining judgments attributed honestly |
| Secret handling | Ignored .env; placeholder-only .env.example; configured-secret scan and server-only database tables |
| Optional browser UI | Responsive BOBALAB chat with generation-only session access; WEB_UI.md |
| Tests | 89 tests with disposable real PostgreSQL and simulated LLM outputs; live-model/hosted evidence is recorded separately |

## Scope and honest limits

- Learning updates stored instructions, not model weights. Reviewed facts are
  maintained separately from automatically editable support behavior.
- Tone and hierarchy compliance are imperfect; before/after evidence includes
  omissions, unsupported assumptions, failed requests and rollback decisions.
- The project was opened and configured in Cursor; source generation and automated
  verification were performed by the assistant in this environment. No independent
  candidate code modifications or Cursor AI coding sessions are claimed.
- Official-source checking is AI-assisted. Candidate source verification and review
  of unassessed outputs remain outstanding; numerical scores are not fabricated.
- A browser chat is included. Actual payment, booking, document inspection, notification and application-submission integrations are absent.
- Free hosting can sleep and provider quotas can interrupt requests. Long-term
  availability and independent reviewer access have not been established by tests.

## Submission handoff

Supply the public repository, hosted URL, README/cURL instructions, comparison
evidence, contribution summary and AI usage log. Arrange the limited reviewer
access key privately, keeping provider/database credentials out of all deliverables.
Deadline: 28 October 2026 at 23:59 Bangkok time. Sending the email to
bobalabth@gmail.com requires the candidate's explicit instruction.
