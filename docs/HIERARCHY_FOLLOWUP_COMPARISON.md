# Live before-and-after evidence

Known validation cases from the [candidate-feedback follow-up](HIERARCHY_FOLLOWUP.md).
These outputs are model observations, including hypothetical booking assumptions,
not verified commercial terms or customer advice. After includes one failed request;
no paired quality conclusion is possible for that case. AI-assisted review found
mixed results and restored the stable instructions. Candidate verdicts on this
follow-up are pending; preferences on the earlier experiment are recorded separately.

Model: `gemini-3.5-flash-lite`; temperature: 0.2.
Before version: `ce7e6789-c0ff-4a68-b940-8caf7ce8ccd7`; after: `55aa0c3c-d819-4db4-a7ab-1e345cee3d22`.
Matched request timeout: 30 seconds. Deployment timeout changes are assessed separately.
Service errors: before 0/6; after 1/6.

Knowledge changed: **False**. Reviewed knowledge was held constant.

## Actual instruction diff

```diff
--- before
+++ after
@@ -80,15 +80,19 @@
     },
     {
       "id": "tone",
-      "text": "Use concise, approachable support-chat language. Avoid introductions or implementation details. Explain capability limits plainly without listing integrations, and keep required demo labeling when discussing unverified agency policy claims."
+      "text": "Use warm, plain, concise support-chat language. Acknowledge the customer's concern naturally. Keep recommendations open to a material correction without sounding indecisive about known facts. Explain relevant limits once in everyday language without listing integrations or implementation details. Keep required demo labeling for unverified agency policy claims."
     },
     {
       "id": "choices",
-      "text": "For decision requests, first state the material constraint, then briefly compare relevant supported options, each with a benefit and drawback. After the comparison, recommend an option only when supported terms and the customer's stated priorities and limits justify it; explain the fit and main downside. Treat customer-supplied hypothetical terms as assumptions, never verified policies. If a missing fact or conflicting priority could reverse the choice, ask a focused question instead of choosing. End with a useful feasible next step when needed. Do not invent options, terms, eligibility or outcomes, and do not force comparisons into simple or capability questions."
+      "text": "For decisions, describe supported options with a benefit and drawback before recommending. Tie the suggestion to stated priorities and limits, using conditional language rather than treating the customer's choice as settled. If a missing fact or conflicting priority could change the choice, ask a focused question or give conditional branches. When useful, finish with a feasible preparation step, an offer of further explanation, or an invitation to correct a material assumption. Do not repeatedly check known priorities, ask for agreement by default, or imply an external procedure has started. Keep simple questions brief without forced options or a closing question."
     },
     {
       "id": "scope",
       "text": "When an exception needs review, explain what is uncertain and what the customer can prepare; do not promise the exception or claim a referral was sent."
+    },
+    {
+      "id": "decision_evidence",
+      "text": "When reasoning from a hypothetical, label its terms as assumptions; do not generalize them into real booking policies or invent refund, penalty or change-fee conditions. In a real planning answer, retain material reviewed timing and constraints, then explain conditional alternatives without asserting their cost, availability or terms. Missing commercial terms call for those terms to be checked; missing transaction integrations do not prevent explaining supported choices."
     }
   ]
 }
```

Human verdicts below are pending until the candidate reviews them. These outputs alone do not establish improvement.

## hierarchy-explicit-priority

Customer need: Understand alternatives and a recommendation tied to an explicit priority

Comparability: both requests produced replies.

**Before**

Booking A has the benefit of a lower initial cost, but its major drawback is that it cannot be changed if your plans shift. Booking B gives you the flexibility to change dates, with the main downside being a higher initial price. Given that your dates are uncertain and flexibility matters more to you than the lowest price, Booking B fits your priorities better, though you will pay more upfront.

**After**

Based on your hypothetical planning example where flexibility is your top priority, booking B would be the better fit. Option A offers a lower initial price, but its drawback is that it cannot be changed, which conflicts with your uncertain dates. Option B costs more, but its benefit is that it allows date changes, giving you the flexibility you need. Since your dates are uncertain, this trade-off makes booking B align closer with your stated preferences, though you may want to verify the exact terms before finalizing any decision.

**Candidate verdict and reasoning:** pending.

## hierarchy-conflicting-priorities

Customer need: Understand a tradeoff without having a priority invented

Comparability: a request failed; no paired answer-quality conclusion is possible.

**Before**

Keeping initial costs low conflicts directly with needing flexible dates. Option A offers a lower upfront price but locks you in completely, so any change means losing your money if plans shift. Option B costs more initially, but it protects you against unexpected date changes without losing the booking. Because you mentioned both priorities as equally important and they oppose each other, I cannot recommend one over the other without knowing which risk you prefer to take. To help decide, consider whether the cost of a potential change fee later is higher or lower than the savings of booking Option A today.

**After**

Service error: model_unavailable

**Candidate verdict and reasoning:** pending.

## hierarchy-unverified-options

Customer need: Know what must be verified before a meaningful recommendation exists

Comparability: both requests produced replies.

**Before**

We do not offer accommodation booking packages, payments, or booking integrations in this demo. For the Destination Thailand Visa, general preparation typically includes evidence of your purpose of visit, passport, photograph, current-location evidence, and financial evidence of at least 500,000 THB, though specific requirements depend on the chosen Royal Thai Embassy or Consulate-General.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

We do not offer accommodation booking packages, manage travel bookings, or process payments in this demo. For your Destination Thailand Visa preparation, the Royal Thai Embassy in Kuala Lumpur advises applying at least 30 working days before intended travel, and processing times can take approximately one month or more depending on the case. Government visa application fees are non-refundable.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv

**Candidate verdict and reasoning:** pending.

## hierarchy-accommodation

Customer need: See a realistic planning path without a guaranteed duration or invented booking terms

Comparability: both requests produced replies.

**Before**

Processing times are assessed on a case-by-case basis, and the Royal Thai Embassy in Kuala Lumpur advises applying at least 30 working days before intended travel as an estimate rather than a guaranteed completion date. Because timelines can vary and additional documents may be requested, you may want to check current processing guidance directly through official channels before finalizing accommodation bookings.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv

**After**

When applying through Kuala Lumpur, processing may take approximately one month or more, assessed on a case-by-case basis, and the embassy advises applying at least 30 working days before intended travel. Because processing times are estimates and can vary, balancing accommodation costs with potential scheduling changes involves considering flexible booking options or fully refundable rates, though these sometimes carry a higher upfront price compared to non-refundable stays. You might want to check the Royal Thai Embassy Kuala Lumpur guidelines directly to help time your booking.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv

**Candidate verdict and reasoning:** pending.

## hierarchy-payment-regression

Customer need: Obtain a useful payment-verification route without an unnecessary options comparison

Comparability: both requests produced replies.

**Before**

I cannot check accounts or confirm payments in this demo chat. Please prepare your documentation for the agency's approved channel.

**After**

I cannot check accounts or confirm payments in this demo, as there are no payment integrations. Please check with your bank or refer to the agency's approved channel for payment verification.

**Candidate verdict and reasoning:** pending.

## hierarchy-simple-regression

Customer need: Get a short, supported explanation without a forced decision template

Comparability: both requests produced replies.

**Before**

The Destination Thailand Visa is generally for remote workers, freelancers, participants in specified Thai cultural or other activities, and qualifying family members. It offers a five-year multiple-entry validity with stays of up to 180 days per entry, which can be extended once for another 180 days through Immigration.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

The Destination Thailand Visa (DTV) is generally intended for remote workers, freelancers, individuals participating in specified Thai cultural or other activities, and qualifying family members. It offers a five-year multiple-entry validity, allowing stays of up to 180 days per entry, with the option for one extension of up to 180 days through Immigration.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**Candidate verdict and reasoning:** pending.
