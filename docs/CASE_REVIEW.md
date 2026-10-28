# Candidate case review

**Status: two qualitative candidate preferences recorded; numerical scores and remaining cases pending.** This sheet makes Fill's
judgment visible; AI-generated judgments must not be presented as his assessment.

Use the requests and expected behaviors in `eval/cases.json`. For each actual reply,
score the following from 0 (fails), 1 (partial), to 2 (meets the need). These are
ordinal review judgments, not objective probabilities or benchmark accuracy.

| Dimension | What to inspect |
|---|---|
| Factual support | Claims fit reviewed evidence, date and country; no invented rules. |
| Context | Uses known details and addresses the current question. |
| Comprehension | Plain language; necessary terms explained; not unnecessarily long. |
| Usefulness | Resolves the concern and shows a relevant next step; options when needed. |
| Tone | Warm, direct and appropriate for the situation. |
| Capability honesty | No invented account, payment, document or notification action. |

Hard failures—concealment coaching, fabricated operational confirmation, unsupported
approval guarantees or invented sources—must be explicitly recorded even if the
answer otherwise sounds good. Do not hide a failure inside an average score.

## Fill's first decision story

- **Observed:** the accommodation answer recommends two weeks while citing business days.
- **Candidate's own guidance:** “giving sources and leading them on to the steps that
  they can do, the options they can do and the pros and cons for each help them
  visualize the path ahead”.
- **Chosen product rule:** support consequential decisions with scoped information,
  uncertainty, realistic options, tradeoffs and the immediate next step.
- **Still to test:** whether this helps on real outputs without making simple
  answers unnecessarily long or carrying the wrong country's guidance across cases.

## Review worksheet

For at least three cases, including accommodation and an unrelated simple question:

1. What does this customer need right now?
2. Which reply would you prefer, before or after, and why?
3. Which claim or action would you reject?
4. Did the prompt edit address the actual cause?
5. Did another case get worse? What would you change next?

Keep the original scores and notes if you revise your assessment. Name AI-assisted
observations honestly. Never claim universal improvement from this small synthetic set.

## Second decision story: payment confirmation

Fill's initial proposed reply promised contacting the transaction team and following
up. After the capability boundary was explained, his revision stated that the bot
cannot confirm payment and proposed preparing documents for review. The assistant
explained that payment evidence is relevant to this concern and that an unverified
visa-document checklist should not be added. These exchanges are not final personal
scores or evidence that a team was contacted.

## Candidate review — hierarchy-explicit-priority, 28 October 2026

**Preference:** after, with requested changes. This is not acceptance of the
experimental playbook as a whole. No numerical score was supplied.

**Candidate's own words:**

> I prefer the after option however, I would like to add to the option. In my opinion i think it should have more of a flexible tone and shouldn't end with jsut the assumption. Maybe this should account for uncertainty and not sound too adamant with the reply. As well as end with the suggestion for whether or not they want to continue with the procedure or whether they dont agree with the bots statement.

**Requested changes, summarized:** make the recommendation less adamant, account
for uncertainty, and invite a useful next step or correction from the customer.
The candidate asked for the assistant's opinion; he has not yet approved exact
replacement wording or an implementation of this follow-up.

**Assistant interpretation for discussion:** keep the recommendation tied to its
assumptions and stated priorities; invite a material correction or offer a feasible
next step. Do not make agreement-seeking questions mandatory, repeat known
priorities, or imply that the API can book, submit or start an external procedure.
This interpretation is assistant-authored and is not a new candidate decision.

## Candidate review — hierarchy-conflicting-priorities, 28 October 2026

**Preference:** after. The candidate's exact preference was "after option".
No explanation, requested edit or numerical score was supplied for this pair;
none is inferred. This preference does not verify all factual assumptions in the
reply or accept the whole playbook. The assistant's previously recorded concerns
about generalizing hypothetical booking terms remain visible.

The candidate also said "from now on keep continue with the operations", authorizing
continued implementation, verification and preparation without repeatedly stopping
for routine decisions. Further candidate judgments must still come from him.


## Candidate inspection of current website reply — 28 October 2026

Fill supplied a screenshot of an actual financial-exception reply and asked whether
its formatting looked professional, and whether compact text would serve a chatbot
better. The image showed a direct answer, repeated qualifications, preparation
bullets and a Next step heading. He requested an honest assessment; no numerical
score, acceptance of a replacement answer or final visual approval was supplied.

The assistant assessed the reply as overstructured for a short concern and suggested
fewer repeated caveats, lighter headings and conditional use of sections. That
assessment/rewrite is assistant work. Fill then asked whether to submit or revise,
and requested preparation of the required submission materials. No UI or prompt
revision was performed under that packaging request.
