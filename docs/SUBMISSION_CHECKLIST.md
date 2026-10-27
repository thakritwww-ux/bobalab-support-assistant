# Final submission checks

This checklist distinguishes completed verification from remaining candidate review.

## Working service

- [x] Three required API flows implemented and locally tested.
- [x] Database prompt versions, persistence and concurrent update handling tested.
- [x] Actual Gemini generation and Supabase connection verified.
- [x] Source published: https://github.com/thakritwww-ux/bobalab-support-assistant (public).
- [x] Free Render URL reachable: https://bobalab-support-assistant.onrender.com.
- [ ] Idle cold-start behavior observed; currently documented as unmeasured.
- [x] Run hosted live_smoke against the real URL.
- [x] Confirm all three hosted responses have the required fields.
- [x] Demonstrate actual automatic and manual edits on real replies; measured usefulness remains for candidate assessment.
- [x] Record real rejection/no-op behavior and its limitations without counting it as quality improvement.

## Evidence and ownership

- [ ] Candidate verifies the source collection and country limits.
- [x] Before/after comparisons hold inputs, model/settings and reviewed knowledge fixed.
- [x] Include original replies, instruction changes and resulting replies; candidate verdicts pending.
- [x] Record unrelated final cases and AI-assisted regression/inconclusive observations.
- [ ] Candidate scores replies and explains at least three actual judgments.
- [ ] Update CONTRIBUTION.md with actual edits/reviews; retain honest AI attribution.
- [x] Update AI_USAGE.md with meaningful follow-ups and verification, without secrets; add any later candidate reviews.

## Package

- [x] README, dependency locks, final prompts, .env.example and three cURL examples prepared.
- [x] Replace README's pending status with the actual GitHub and hosted URLs.
- [x] Replace pending BEFORE_AFTER.md with real evidence.
- [ ] Add candidate verdicts to real evidence.
- [x] Assistant reviewed selected synthetic evidence for publication; raw local captures are ignored. Candidate quality verdicts remain pending.
- [x] Publishable-file scan found none of the configured Gemini, database or reviewer secrets; .env and personal handoff PDF are ignored. No real identity documents are included.
- [x] Fresh anonymous clone of published revision 9b7a751 checked: 63 tests passed with temporary PostgreSQL.
- [x] Hosted endpoint contracts checked against runtime code revision 9b7a751; documentation-only updates follow.
- [ ] Make the reviewer key available privately, separate from public documentation.

Email: bobalabth@gmail.com. Subject: **BOBALAB Technical Assessment — Thakrit Wongwiwatseree**.
Deadline: **28 October 2026, 23:59 Bangkok time**. Include both actual URLs, cURL
examples, reviewer access, documentation, evidence, contribution summary and AI log.
The assistant must not send the email without the candidate's explicit instruction.
