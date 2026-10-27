# BOBALAB submission handoff

Candidate: Thakrit Wongwiwatseree (Fill)

- Repository: https://github.com/thakritwww-ux/bobalab-support-assistant
- Hosted API: https://bobalab-support-assistant.onrender.com
- Public liveness: https://bobalab-support-assistant.onrender.com/health
- Setup, architecture, response formats and three cURL examples: [README](../README.md)
- Requirement coverage and limits: [map](REQUIREMENTS_MAP.md)

## Reviewer access

The three model routes require the limited application key in `X-API-Key`.
The candidate must arrange a private handoff of `REVIEWER_API_KEY`; it is not
included in the public repository or this document. Provider/database credentials
are never needed by reviewers. This handoff has not yet been completed.

The README commands use the real hosted URL and a placeholder for the privately
provided key. Its exact three JSON payloads were tested using actual curl on
28 October: all three required routes returned 200. The automatic probe reported
rejected; the manual probe saved a rule. Editing HTTP success is separate from
persistence and answer quality. The evaluated instructions were restored afterward.

## Contribution summary

Fill defined concern-first support, practical options with tradeoffs and useful
next steps, uncertainty about exceptions, reviewed-source boundaries and strictly
free API/documentation scope. He proposed an answer hierarchy and selected a
combination of option descriptions with conditional recommendations. He reviewed
two real hierarchy pairs, preferring after; on the first he requested a less
adamant tone, uncertainty and a helpful continuation or invitation to correct the
recommendation. His payment-response drafts and capability-related revision are
also recorded. No independent candidate source-code edits or numerical scores
are claimed.

The assistant generated the implementation, tests, prompt wording and documentation,
executed automated/live checks, reviewed sources and made the rollback decisions.
Candidate decisions, actual feedback and assistant assessments are distinguished in
[CONTRIBUTION.md](../CONTRIBUTION.md), [CASE_REVIEW.md](CASE_REVIEW.md) and
[AI_USAGE.md](../AI_USAGE.md). The project was opened/configured in Cursor; no
separate Cursor AI coding session is claimed.

## Improvement evidence

| Evidence | What it shows |
|---|---|
| [Automatic comparison](BEFORE_AFTER.md) | Actual example-driven prompt edits, rejections, no-op, mixed replies and rollback; no clear overall quality gain |
| [Manual example](MANUAL_IMPROVEMENT.md) | Real manual update with a matched before/after example |
| [Style refinement](STYLE_REFINEMENT.md) | Removal of unrelated information in one payment sample; incomplete accommodation tradeoffs |
| [First hierarchy experiment](HIERARCHY_COMPARISON.md) | Original reply, exact prompt diff and resulting reply; two candidate preferences recorded |
| [Feedback follow-up](HIERARCHY_FOLLOWUP.md) | Uncertainty/tone revision, a failed after request, mixed results and restoration |
| [Four final conversations](FINAL_COMPARISON.md) | Cases excluded from automatic learning, with inputs/settings held fixed; developers had already seen the dataset |
| [Final regressions](SUBMISSION_REGRESSIONS.md) | All twelve known requests returned replies; actual outputs and semantic limitations preserved |

Learning changes stored instructions, not model weights. Successful saving does
not prove a reply improved. The final stable prompt is in
[prompt-snapshot.json](evidence/prompt-snapshot.json); initial seeding now uses
the matching playbook. The source collection was held fixed in behavioral comparisons.

## Verification and remaining limits

All 63 tests passed with disposable real PostgreSQL and scripted model outputs.
Live calls and actual hosted curl checks are separate evidence in
[VERIFICATION.md](VERIFICATION.md) and
[submission-http-summary.json](evidence/submission-http-summary.json).

Free services have quotas and can sleep; a first resumed health probe took
52.409 seconds, without independent confirmation of the server's sleep state.
Long-term availability has not been measured. Tone, citation relevance, assumption
handling and hierarchy adherence remain imperfect. One hosted generation added
unsupported booking-risk inferences; successful HTTP status does not validate
every claim. No real payment, booking, attachment inspection, team-notification
or application-submission integration exists. Use synthetic data only.

Remaining personal checks include candidate source review, any additional output
assessments and final package/access review. Only two candidate preferences are
recorded; no others are inferred. The private reviewer access handoff remains open.

## Email details

A browser interface was subsequently requested. The requirements and specialist
handoff are in [docs/design](design/README.md). UI implementation and browser access
remain unfinished; the design packet must not be submitted as a functioning UI.

Recipient: bobalabth@gmail.com

Subject: BOBALAB Technical Assessment — Thakrit Wongwiwatseree

Deadline: 28 October 2026 at 23:59 Bangkok time (ICT / UTC+7).
Include the repository and hosted URLs, the three README cURL examples, documentation,
before/after evidence, contribution summary and AI usage log. Arrange reviewer access
privately. No email has been sent; sending requires the candidate's explicit instruction.
