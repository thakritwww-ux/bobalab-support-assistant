# Tone, uncertainty and continuation follow-up

## Candidate input and attribution

On 28 October, Fill preferred the after reply in the explicit-priority comparison,
requesting a more flexible tone, uncertainty and an invitation to continue or correct
the recommendation. He also preferred after in the conflicting-priorities comparison
without supplying a reason. His exact feedback is in CASE_REVIEW.md. These are two
qualitative preferences on the first experiment, not scores or judgments of this
follow-up. He authorized continued operations instead of repeated routine pauses.

The assistant generalized the feedback into implementation rules and performed the
experiment. It also addressed previously observed loss of timing context, invented
booking terms and confusion between advising and executing a transaction.

## Procedure and actual change

- A fresh six-case baseline used immutable first-experiment version
  ce7e6789-c0ff-4a68-b940-8caf7ce8ccd7. The cases were already known validation
  inputs, not unseen final tests. The old capture was not silently reused.
- The hosted manual endpoint returned 200 and applied the exact intended direct,
  choices and tone replacements plus a decision_evidence rule. It saved version
  55aa0c3c-d819-4db4-a7ab-1e345cee3d22 in 65.311 seconds in this observation.
- The live edit started from restored stable version c2168b04-8ba2-4012-a8c3-83b4ed5d73ec;
  the comparison baseline was the earlier experimental version. This distinction
  is recorded rather than implying both version IDs were identical.
- Protected policy, reviewed knowledge, context and scope rules stayed unchanged.
  Model, temperature, timeout, output budget, retry policy and case inputs were
  held fixed. Exact instructions and persistence checks are in
  [the edit summary](evidence/hierarchy-followup-edit-summary.json).

The [complete comparison](HIERARCHY_FOLLOWUP_COMPARISON.md) includes the prompt diff
and all observed outputs. Before returned 6/6 replies; after returned 5/6. The
conflicting-priorities after request failed following provider 504 responses, so
that case has no paired answer-quality conclusion. The error was not replaced by
a selected successful retry. These are single samples, not reliability estimates.

## AI-assisted assessment

| Case | Observation |
|---|---|
| Explicit priority | After explicitly labels the hypothetical basis and suggests verifying terms. However, it puts the recommendation before the options again. Assumption labeling improved in this sample; intended option-first ordering regressed. |
| Conflicting priorities | After failed. No claim about answer quality is possible for this pair. |
| Missing offer details | After still gives unrelated visa information, now including a Kuala Lumpur source despite no application country being supplied. It does not resolve the lack of verified package terms. |
| Accommodation | After restores the approximate month-or-more processing estimate. It still does not give a clear supported comparison and introduces a general price tradeoff without verified booking terms. |
| Payment | Both avoid confirming receipt, but remain impersonal and refer generically to approved channels. The requested natural acknowledgement and useful continuation were not reliably demonstrated. |
| Simple explanation | Both are short and supported; neither forces options or a closing question. |

These are assistant judgments, not Fill's scores or acceptance. They do not support
an overall quality-improvement claim. Adding detailed prompt rules did not reliably
produce the intended structure or tone in these samples.

## Final decision and maintenance

The assistant restored the stable evaluated instructions as version
bd679166-d61f-4745-bb13-8998f125d8d9, with content equal to evaluated version
ed2446a9-569c-4158-aa5e-fa18de420a8a. The follow-up remains immutable in database
history and its outputs are preserved. Neither hierarchy experiment is active.

The fresh-install prompts/playbook.json was aligned with that stable evaluated
content, resolving the earlier difference between initial seed rules and deployed
manual refinements. Existing databases retain their active version because seeding
is idempotent. No protected-policy or source changes were made.

The final application retains a working generation/edit/persistence workflow.
Reliable customer-facing hierarchy and tone remain limitations. A structured
response-format experiment could be considered later, but it has not been
implemented or claimed as complete. Further tuning should preserve these failures
and distinguish validation revisions from independent evaluation.
