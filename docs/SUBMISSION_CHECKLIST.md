# Final submission checks

This is a working checklist, not a claim that deployment or evidence exists.

## Working service

- [x] Three required API flows implemented and locally tested.
- [x] Database prompt versions, persistence and concurrent update handling tested.
- [x] Actual Gemini generation and Supabase connection verified.
- [x] Source published: https://github.com/thakritwww-ux/bobalab-support-assistant (public).
- [ ] Free Render URL reachable, including after a cold start.
- [ ] Run `python -m scripts.live_smoke https://YOUR-REAL-SERVICE.onrender.com --allow-edits`.
- [ ] Confirm all three hosted responses have the required fields.
- [x] Demonstrate actual automatic and manual edits on real replies; measured usefulness remains for candidate assessment.
- [x] Record real rejection/no-op behavior and its limitations without counting it as quality improvement.

## Evidence and ownership

- [ ] Candidate verifies the source collection and country limits.
- [x] Before/after comparisons hold inputs, model/settings and reviewed knowledge fixed.
- [x] Include original replies, instruction changes and resulting replies; candidate verdicts pending.
- [x] Record unrelated final cases and AI-assisted regression/inconclusive observations.
- [ ] Candidate scores replies and explains at least three actual judgments.
- [ ] Update CONTRIBUTION.md with actual edits/reviews; retain honest AI attribution.
- [ ] Update AI_USAGE.md with meaningful follow-ups and verification, without secrets.

## Package

- [x] README, dependency locks, final prompts, .env.example and three cURL examples prepared.
- [ ] Replace README's pending status with the actual GitHub and hosted URLs.
- [x] Replace pending BEFORE_AFTER.md with real evidence.
- [ ] Add candidate verdicts to real evidence.
- [ ] Review selected evidence before explicitly publishing it; local captures are ignored.
- [ ] Verify no .env, real identity documents, provider keys or database secrets are tracked.
- [x] Fresh-copy local setup checked: 58 tests passed.
- [ ] Hosted instructions checked against the final deployed revision.
- [ ] Make the reviewer key available privately, separate from public documentation.

Email: bobalabth@gmail.com. Subject: **BOBALAB Technical Assessment — Thakrit Wongwiwatseree**.
Deadline: **28 October 2026, 23:59 Bangkok time**. Include both actual URLs, cURL
examples, reviewer access, documentation, evidence, contribution summary and AI log.
The assistant must not send the email without the candidate's explicit instruction.
