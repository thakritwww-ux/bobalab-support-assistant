# Live before-and-after evidence

This is the candidate-led hierarchy experiment described in
[ANSWER_HIERARCHY.md](ANSWER_HIERARCHY.md). These are known synthetic validation
cases, including hypothetical booking assumptions; model statements are not
verified booking terms or customer advice. All outputs are retained. AI-assisted
review found mixed results and the prior evaluated instructions were restored.
The experimental version remains in history; two candidate preferences are recorded
below, and the remaining verdicts are pending.

Model: `gemini-3.5-flash-lite`; temperature: 0.2.
Before version: `03f85a3f-263a-4385-9034-190a7b6636e9`; after: `ce7e6789-c0ff-4a68-b940-8caf7ce8ccd7`.
Matched request timeout: 30 seconds. Deployment timeout changes are assessed separately.
Service errors: before 0/6; after 0/6.

Knowledge changed: **False**. Reviewed knowledge was held constant.

## Actual instruction diff

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

## hierarchy-explicit-priority

Customer need: Understand alternatives and a recommendation tied to an explicit priority

Comparability: both requests produced replies.

**Before**

Given your priorities where flexibility matters more than the lowest initial price, Booking B fits your needs better because it allows date changes, whereas Booking A is non-changeable. The benefit of Booking B is that you can adjust your travel plans if your dates are uncertain, though the drawback is that it costs more upfront. For Booking A, the benefit is saving money initially, but the major drawback is losing your investment if your schedule changes. A manageable next step is to review your travel timeline to see how likely a date change might be before deciding on the booking type.

**After**

Booking A has the benefit of a lower initial price, but its main drawback is that it cannot be changed. Booking B has the benefit of allowing date changes when your plans are uncertain, but its main drawback is that it costs more. Based on your stated priority that flexibility matters more to you than the lowest initial price, Booking B fits your priorities better because it accommodates uncertain dates, though you will pay more for that flexibility.

**Candidate verdict, 28 October 2026:** Fill prefers after, with changes: a more
flexible and less adamant tone, explicit uncertainty, and a closing invitation to
continue with an appropriate next step or correct the recommendation. Exact wording
and implementation are not yet approved. See [the verbatim review](CASE_REVIEW.md).
No numerical score or whole-playbook acceptance was supplied.

## hierarchy-conflicting-priorities

Customer need: Understand a tradeoff without having a priority invented

Comparability: both requests produced replies.

**Before**

Choosing between Option A and Option B involves balancing upfront savings against flexibility. Option A keeps your initial cost lower, but you risk losing that money if your plans shift. Option B gives you the freedom to change dates, but requires a higher initial payment. Since both priorities matter to you, a practical next step is to consider how likely a date change actually is—if your schedule is mostly fixed, Option A saves money, but if flexibility is essential, Option B protects you from change fees.

**After**

Keeping initial costs low conflicts directly with needing flexible dates, as lower-cost bookings typically lock you in without changes, while flexible bookings require a higher upfront price. Option A keeps your initial payment low, but the drawback is that you cannot change your dates if plans shift. Option B allows date changes, but the drawback is a higher initial cost. Because your dates might change but you also want to minimize upfront expenses, could you clarify whether a date change is more critical to your plans, or is staying within a strict budget your primary priority?

**Candidate verdict, 28 October 2026:** after. Exact preference: "after option".
No reasoning, requested change or numerical score was supplied for this pair.
The assistant's concern about unsupported generalization remains recorded separately.

## hierarchy-unverified-options

Customer need: Know what must be verified before a meaningful recommendation exists

Comparability: both requests produced replies.

**Before**

We do not offer accommodation booking packages or sell travel itineraries in this demo. For the Destination Thailand Visa, applicants typically prepare financial evidence such as 500,000 THB along with passport, photograph, current-location evidence, and purpose-of-visit evidence, though exact requirements depend on the chosen embassy or consulate mission.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

I cannot recommend or sell accommodation booking packages in this demo, as there are no payment or booking integrations available. Please review the official agency terms and itemized quotes directly through our approved channels before making any financial commitments.

**Candidate verdict and reasoning:** pending.

## hierarchy-accommodation

Customer need: See a realistic planning path without a guaranteed duration or invented booking terms

Comparability: both requests produced replies.

**Before**

For a DTV application through Kuala Lumpur, official guidance indicates processing may take approximately one month or more, assessed case by case, and advises applying at least 30 working days before intended travel. Because processing times are estimates and subject to change, a practical approach is to check current mission requirements and secure flexible or refundable lodging to help manage costs while avoiding rigid commitments. You can prepare by reviewing the official embassy checklist and gathering your required documents.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

Processing times are assessed on a case-by-case basis, and the Royal Thai Embassy in Kuala Lumpur advises applying at least 30 working days before intended travel. Because processing estimates can vary and timelines are not guaranteed, you may want to review official guidance directly for Kuala Lumpur before locking in non-refundable accommodation.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv

**Candidate verdict and reasoning:** pending.

## hierarchy-payment-regression

Customer need: Obtain a useful payment-verification route without an unnecessary options comparison

Comparability: both requests produced replies.

**Before**

We do not have payment or account integration in this demo to verify transfers. For actual applications, you would complete payments through the agency's approved channel rather than this chat.

**After**

I cannot check accounts, confirm payments, or verify transactions in this demo chat. Please check your payment status through your own bank or the agency's approved channel once you are ready.

**Candidate verdict and reasoning:** pending.

## hierarchy-simple-regression

Customer need: Get a short, supported explanation without a forced decision template

Comparability: both requests produced replies.

**Before**

The Destination Thailand Visa (DTV) is generally intended for remote workers, freelancers, individuals participating in specified Thai cultural or other activities, and qualifying family members. It offers a five-year multiple-entry validity, allowing stays of up to 180 days per entry, with the possibility of one extension of up to 180 days through Immigration.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

The Destination Thailand Visa is generally for individuals engaging in remote work or freelancing, specified Thai cultural or other activities, and qualifying family members. It offers a five-year multiple-entry validity, allowing stays of up to 180 days per entry with one possible extension of up to 180 days through Immigration.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**Candidate verdict and reasoning:** pending.
