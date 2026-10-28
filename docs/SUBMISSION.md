# BOBALAB technical assessment submission

Candidate: Thakrit Wongwiwatseree (Fill)

Role: Technology and Lab Operations

Deadline: 28 October 2026,23:59 Bangkok (ICT/UTC+7)

- **Repository:** https://github.com/thakritwww-ux/bobalab-support-assistant
- **Website and API:** https://bobalab-support-assistant.onrender.com
- **Public liveness:** https://bobalab-support-assistant.onrender.com/health
- **Original assignment:** https://github.com/MoriJinzz/Bobalab-Assesment

## Start here

This is a working Flask/Gemini/Supabase support assistant. It generates replies from
customer history, retrieves the active prompt from a database, learns bounded
behavioral edits from consultant examples, and accepts manual prompt changes.
Learning updates stored instructions, not model weights. The optional BOBALAB web
interface adds validated answer sections and opt-in same-device history.

The website uses a limited demo code; the three API routes require a separate
application-access key in X-API-Key. Access must be arranged separately through
an agreed private channel. No credentials are included here or in the packet.
This private handoff remains an owner action before sending; application
credential protection has not been disabled. Free hosting may take time to wake.

## Required materials

| Requested item | Where to find it |
|---|---|
| Source, dependencies and configuration example | Repository root; requirements.txt, requirements-dev.txt, .env.example |
| Setup, architecture and improvement workflow | [README](../README.md), [setup](SETUP.md) |
| Three cURL requests and expected formats | [cURL examples](submission/CURL_EXAMPLES.md) |
| Original response, prompt change, resulting response and assessment | [Selected actual examples](submission/BEFORE_AFTER_HIGHLIGHTS.md) |
| Brief contribution summary and limitations | [Candidate summary](submission/CONTRIBUTION_SUMMARY.md), [full attribution](../CONTRIBUTION.md) |
| AI tools, key prompts, meaningful responses and follow-ups | [AI_USAGE.md](../AI_USAGE.md) |
| Final application prompts | prompts/policy.md, prompts/editor.md, data/knowledge.json, [active snapshot](evidence/prompt-snapshot.json), [layout guide](answer-format-instruction.txt), [schema](answer-section-contract.json) |
| Requirement coverage and verification | [Coverage map](REQUIREMENTS_MAP.md), [verification](VERIFICATION.md) |

## Product decisions and contribution

Fill chose concern-first support, practical options with tradeoffs, conditional
recommendations tied to the customer's priorities, honest uncertainty and reviewed
sources. He proposed the answer hierarchy, supplied/revised payment wording,
reviewed two hierarchy pairs and later questioned the professionalism of excessive
segmentation. He selected free services and requested the optional browser and
customer-facing local history.

The assistant authored code, exact prompts, tests and preliminary assessments and
performed the recorded deployment/checks. The project was opened/configured in
Cursor; no separate Cursor AI coding session or independent candidate code edits
are claimed. Candidate feedback, experiment approval and output acceptance are
kept distinct. No invented scores or whole-system visual acceptance.

## Evidence and results

- Dataset:15 synthetic conversations,262 messages,128 reply pairs. Order, preceding
  history, outbound openers and attachment placeholders are preserved. Operational
  updates unavailable from visible messages are flagged. [Data findings](DATA_FINDINGS.md).
- Automatic learning: eight development references produced two applied edits,
  five rejections and one no-op. Some edits reduced useful coverage; stable behavior
  was restored. Saving an edit is distinct from quality improvement.
- Manual hierarchy: real stored changes and a narrow ordering improvement; two
  candidate preferences recorded. Other outputs regressed and the trial was restored.
- Structured presentation:117 backend tests and13 browser checks passed. All three
  required hosted endpoints returned 200 in the latest trial; temporary changes
  were restored.12/14 approved attempts used, including an initial provider 503.
  [Actual structured results](STRUCTURED_ANSWER_RESULTS.md).
- Public checkout 0485be9 was anonymously cloned and passed 117tests with disposable
  PostgreSQL using the existing Python environment. This is a clean-checkout test,
  not a claim of testing a new machine or fresh dependency installation.
- Public website, health and session-bootstrap checks returned 200 on28 October 2026
  at 22:44 Bangkok, with zero model calls. Health is process liveness only.
- Remaining historical reports are linked by [the evidence map](REQUIREMENTS_MAP.md).
  Unsuccessful samples and failures were retained; no broad quality gain is claimed.

## Known limitations and unfinished work

Replies can be verbose, repeat caveats, generalize private booking terms, omit useful
context or cite weakly relevant official sources. The latest screenshot prompted a
readability critique; the proposed final brevity revision is unfinished. Structure
validation is not factual validation. Source review is AI-assisted; candidate source
verification and additional output review remain incomplete. Coverage is deliberately
small and country-scoped; no runtime browsing or individualized legal determination.

No payment confirmation, attachment inspection, booking, application submission,
team notification or follow-up integration exists. Saved conversations are on the
same device/browser only. Free quotas/cold starts/provider 503s can interrupt use;
long-term availability is not established. Request throttling is process-local;
the daily model-call counter is shared in PostgreSQL.

## Submission preparation

- [Copy-ready email draft](submission/EMAIL_DRAFT.md), with three cURL examples.
- [Owner checks](submission/OWNER_CHECKS.md), including the unresolved separate
  reviewer-access handoff. The draft contains a handoff placeholder to resolve.
- Recipient: bobalabth@gmail.com
- Subject: **BOBALAB Technical Assessment — Thakrit Wongwiwatseree**

The packet and source archive contain no actual access credentials. No email has
been sent. Sending requires the candidate's explicit instruction.
