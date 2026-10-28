# Selected before-and-after evidence

These are excerpts of actual recorded outputs, not newly generated examples.
Synthetic inputs were used. Prompt-learning evidence and the later code-controlled
presentation change are separate experiments. Exact requests/settings and all
cases, including errors and regressions, remain in the linked source reports.

## 1. Automatic improvement: stored changes with inconclusive quality

Source: [full automatic trial](../BEFORE_AFTER.md),
[batch outcomes and rollback](../LIVE_RESULTS.md).
Model gemini-3.5-flash-lite, temperature 0.2; matched 20-second timeout and unchanged
reviewed knowledge. The eight-example learning batch applied two edits, rejected
five lessons and made one no-op. Those classifications are editor outputs, not
independent correctness labels. The automatic run changed these stored rules:


```diff
--- before
+++ after
@@ -76,7 +76,7 @@
     },
     {
       "id": "context",
-      "text": "Use known customer details from preceding history; ask only for missing information that changes the answer."
+      "text": "Use known customer details from preceding history; ask only for missing and material information, such as application location when relevant to requirements."
     },
     {
       "id": "tone",
@@ -88,7 +88,7 @@
     },
     {
       "id": "scope",
-      "text": "When an exception needs review, explain what is uncertain and what the customer can prepare; do not promise the exception or claim a referral was sent."
+      "text": "When additional documents are requested by an embassy, explain that processing may be delayed and refer to official guidelines, avoiding unverified integrations while suggesting appropriate preparation."
     }
   ]
 }
```

Human verdicts below are pending until the candidate reviews them. These outputs alone do not establish improvement.

### Actual known-context pair


Customer need: Preparation without repeating qualification questions

Comparability: both requests produced replies.

**Before**

To get started on your Destination Thailand Visa preparation, you will generally need to gather your passport, a photograph, current-location evidence, financial proof showing at least 500,000 THB, and documents supporting your remote-work purpose. Because you are considering applying in Indonesia, please keep in mind that specific application procedures, checklists, and timelines can vary by location. As we do not have specific reviewed guidelines for Indonesia in our current database, it is best to check the exact requirements directly with the specific Thai embassy or consulate where you plan to submit your application.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

To get started on your Destination Thailand Visa preparation, general guidelines suggest gathering your passport, a photograph, current-location evidence, financial evidence of at least 500,000 THB, and purpose-of-visit documentation for remote work. Because application requirements can vary by location, please note that we do not currently have reviewed country-specific application guidance for Indonesia in our sources. It is best to check the specific requirements of the official Thai mission where you plan to apply. A manageable next step is to review the specific guidelines provided by the embassy or consulate you will be using.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**Candidate verdict and reasoning:** pending.


**Assistant assessment:** both replies use known context and flag missing country
coverage. No clear improvement is established by this pair. The broader run showed
that the scope replacement narrowed the original exception-handling coverage;
several outputs added unrelated details. Stable behavior was restored. This
shows working persistence and a deliberate rejection of an unconvincing result.

## 2. Manual hierarchy: a narrow ordering change reviewed by the candidate

Source: [complete hierarchy comparison](../HIERARCHY_COMPARISON.md).
The model/settings, requests and reviewed facts were held fixed. These are known
validation cases with hypothetical booking terms. The manual endpoint changed:


```diff
--- before
+++ after
@@ -72,7 +72,7 @@
   "editable_playbook": [
     {
       "id": "direct",
-      "text": "Answer the immediate question first; do not append general eligibility facts, unsolicited onboarding sales, or unrelated location processing details. Keep simple answers brief."
+      "text": "Answer the immediate concern first; do not append general eligibility facts, unsolicited onboarding sales, or unrelated location processing details. For a simple explanation, give a plain direct answer with essential qualifications only. For an unavailable action, acknowledge the request, state the relevant limit and suggest a feasible verification or review step without claiming it was performed. Do not force headings, comparisons, recommendations or a closing question when they add no value."
     },
     {
       "id": "context",
@@ -84,7 +84,7 @@
     },
     {
       "id": "choices",
-      "text": "For consequential choices, name practical alternatives, give a concrete benefit and drawback for each, and finish with one immediate action while preserving all uncertainty and honesty rules."
+      "text": "For decision requests, first state the material constraint, then briefly compare relevant supported options, each with a benefit and drawback. After the comparison, recommend an option only when supported terms and the customer's stated priorities and limits justify it; explain the fit and main downside. Treat customer-supplied hypothetical terms as assumptions, never verified policies. If a missing fact or conflicting priority could reverse the choice, ask a focused question instead of choosing. End with a useful feasible next step when needed. Do not invent options, terms, eligibility or outcomes, and do not force comparisons into simple or capability questions."
     },
     {
       "id": "scope",
```

Human verdicts are recorded only when supplied; the remaining cases are pending.
These outputs alone do not establish improvement.

### Actual explicit-priority pair


Customer need: Understand alternatives and a recommendation tied to an explicit priority

Comparability: both requests produced replies.

**Before**

Given your priorities where flexibility matters more than the lowest initial price, Booking B fits your needs better because it allows date changes, whereas Booking A is non-changeable. The benefit of Booking B is that you can adjust your travel plans if your dates are uncertain, though the drawback is that it costs more upfront. For Booking A, the benefit is saving money initially, but the major drawback is losing your investment if your schedule changes. A manageable next step is to review your travel timeline to see how likely a date change might be before deciding on the booking type.

**After**

Booking A has the benefit of a lower initial price, but its main drawback is that it cannot be changed. Booking B has the benefit of allowing date changes when your plans are uncertain, but its main drawback is that it costs more. Based on your stated priority that flexibility matters more to you than the lowest initial price, Booking B fits your priorities better because it accommodates uncertain dates, though you will pay more for that flexibility.

**Candidate verdict, 28 October 2026:** Fill prefers after, with changes: a more
flexible and less adamant tone, explicit uncertainty, and a closing invitation to
continue with an appropriate next step or correct the recommendation. Exact wording
and implementation are not yet approved. See [the verbatim review](../CASE_REVIEW.md).
No numerical score or whole-playbook acceptance was supplied.


**Assistant assessment:** the after answer describes both options before the
recommendation, matching Fill's chosen order. Both already compare options;
this is a narrow ordering improvement, not a newly acquired general capability.
Neither clearly labels the booking assumptions. Other cases regressed, so the
experimental playbook was restored. Fill's preference is specific to this pair.

## 3. Current presentation: typed sections, separate from learning

The application now validates section fields and renders native lists/tables.
[The latest results](../STRUCTURED_ANSWER_RESULTS.md) include the actual reused
baseline, exact final schema/instruction, resulting responses and all earlier
rejected iterations in [JSON](../evidence/structured-answers.json). Model and stored
prompt content match the baseline; the schema and code-owned instruction changed.
This is a generation-design comparison rather than isolated prompt learning.

The release controls presentation more reliably. It still has repeated caveats,
weak citation relevance, generalized booking terms and a preparation example that
omits a useful fee warning. The candidate subsequently questioned the visual
professionalism using an actual screenshot; no final visual acceptance is claimed.

## Interpretation

Successful saved edits, isolated useful changes, rejection, no-ops and rollbacks
are all demonstrated. No statistical or general answer-quality improvement is
claimed. Candidate scores and remaining source/output review are unfinished.
