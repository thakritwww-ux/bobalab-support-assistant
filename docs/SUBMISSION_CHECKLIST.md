# Final submission checks

This checklist distinguishes completed verification from remaining candidate review.

## Working service

- [x] Three required API flows implemented and locally tested.
- [x] Database prompt versions, persistence and concurrent update handling tested.
- [x] Actual Gemini generation and Supabase connection verified.
- [x] Source published: https://github.com/thakritwww-ux/bobalab-support-assistant (public).
- [x] Free Render URL reachable: https://bobalab-support-assistant.onrender.com.
- [ ] Confirm actual idle cold-start state; first resumed health probe took 52.409 seconds, but Render sleep state was not observed.
- [x] Run hosted live_smoke against the real URL.
- [x] Confirm all three hosted responses have the required fields.
- [x] Demonstrate actual automatic and manual edits on real replies; measured usefulness remains for candidate assessment.
- [x] Record real rejection/no-op behavior and its limitations without counting it as quality improvement.

## Evidence and ownership

- [ ] Candidate verifies the source collection and country limits.
- [x] Before/after comparisons hold inputs, model/settings and reviewed knowledge fixed.
- [x] Include original replies, instruction changes and resulting replies; candidate verdicts pending.
- [x] Record unrelated final cases and AI-assisted regression/inconclusive observations.
- [x] Record the two supplied candidate preferences and first-case requested changes without inventing reasons or numerical scores.
- [ ] Additional candidate case/source review; further judgments have not been supplied.
- [x] Update CONTRIBUTION.md with actual decisions/reviews and honest AI attribution; add later edits only if they occur.
- [x] Preserve Fill's product decisions, answer-hierarchy proposal, hybrid recommendation choice and payment-response revisions in CONTRIBUTION.md.
- [x] Carry those recorded contributions into the final README/submission summary and AI disclosure, distinguishing assistant implementation and assessment from Fill's decisions and later personal review.
- [x] Confirm that experiment authorization is not represented as acceptance of outputs; automated tests and AI review do not substitute for candidate assessment.
- [x] Update AI_USAGE.md with meaningful follow-ups and verification, without secrets; add any later candidate reviews.

## Package

- [x] README, dependency locks, final prompts, .env.example and three cURL examples prepared.
- [x] Replace README's pending status with the actual GitHub and hosted URLs.
- [x] Replace pending BEFORE_AFTER.md with real evidence.
- [x] Add the two supplied candidate preferences to real evidence; remaining cases explicitly unreviewed.
- [x] Assistant reviewed selected synthetic evidence for publication; raw local captures are ignored. Candidate quality verdicts remain pending.
- [x] Publishable-file scan found none of the configured Gemini, database or reviewer secrets; .env and personal handoff PDF are ignored. No real identity documents are included.
- [x] Fresh anonymous clone of published revision 9b7a751 checked: 63 tests passed with temporary PostgreSQL.
- [x] Hosted endpoint contracts originally checked at runtime code revision 9b7a751; subsequent documentation, evaluation and seed updates preserve API code.
- [x] On 28 October, actual cURL requests using all three README payloads returned 200; access/validation controls returned 401/400. Automatic edit was rejected; manual edit saved, then stable content was restored.
- [x] Stable seed aligned with evaluated database instructions; 63 tests pass after alignment. Twelve known live regression requests returned replies; semantic limitations are documented separately.
- [ ] Make the reviewer key available privately, separate from public documentation.

Email: bobalabth@gmail.com. Subject: **BOBALAB Technical Assessment — Thakrit Wongwiwatseree**.
Deadline: **28 October 2026, 23:59 Bangkok time**. Include both actual URLs, cURL
examples, reviewer access, documentation, evidence, contribution summary and AI log.
The assistant must not send the email without the candidate's explicit instruction.


## Optional browser release

- [x] Responsive BOBALAB chat implemented, preserving required API contracts.
- [x] Limited browser code/session/CSRF access; privileged key stays server-side.
- [x] 89 automated tests and 15 simulated browser interaction checks passed.
- [x] Font/icon source, hashes and license notices included.
- [ ] Deployed browser and real-model smoke check recorded in WEB_UI.md.
- [ ] Candidate inspects final interface; no visual acceptance inferred.
