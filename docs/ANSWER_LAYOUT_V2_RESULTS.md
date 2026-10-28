# Second answer-layout trial: actual results

Historical experiment. The subsequent deployed section-based design is documented in
[STRUCTURED_ANSWERS.md](STRUCTURED_ANSWERS.md); this report preserves its original trial state.

Decision: **rolled back** after failing the prospective acceptance criteria.

The baseline below is reused from the earlier readability experiment. Its prompt-content hash exactly equals the restored five-rule prompt used before this trial. It is not a fresh baseline sample. Same request bodies, reviewed knowledge, model and temperature were retained. One sample per case cannot isolate stochastic variation.

The user explicitly approved this exact rule and six-attempt test. Four provider attempts were used. The manual endpoint applied one style rule and left all previous rules, policy and knowledge intact. No candidate scores are inferred.

Before version: 34d6cf6a-bfe6-4fff-b76b-53718b5caa1a. Experimental version: bac43f02-4c25-4df4-8736-8b53058a7b47. Restored version: 2c866996-5fb2-4c32-b5b0-63223ec3fefb.

## Exact proposed rule

```text
Start with a short direct answer using only information needed for the immediate question. Put distinct points on separate lines: preparation under **What to check** with bullets; procedures under **Next steps** with numbered steps; comparisons as bullets showing each option's benefit, drawback and uncertain terms. Use a compact table only when every cell is supported. Put uncertainty beside its point and finish with one relevant action. Do not add facts or agency onboarding to fill a section. For a simple concern, use brief plain sentences without headings. Formatting must not add certainty, promises, requirements or capabilities.
```

## Actual replies

### options

Customer message: I am Indonesian and considering a DTV application from Kuala Lumpur. My dates might change and my budget is tight. How should I compare flexible and fixed accommodation bookings?

History: `[]`

Before (reused):

```text
When comparing flexible and fixed accommodation bookings for your DTV application through Kuala Lumpur, flexible bookings allow you to adjust your dates if travel plans shift, but they often come with a higher nightly rate. Fixed bookings are generally more budget-friendly, but they lock you into rigid dates and carry cancellation penalties if your timeline changes. As a next step, you may want to weigh your travel flexibility against your accommodation budget before preparing your application documents.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
```

After:

```text
For a Destination Thailand Visa application at the Royal Thai Embassy in Kuala Lumpur, choosing between flexible and fixed accommodation bookings involves specific trade-offs regarding cost and itinerary changes.

* Flexible bookings
  * Benefit: Easier to adjust dates if your travel plans change unexpectedly.
  * Drawback: Usually more expensive upfront.
  * Uncertainty: Embassy acceptance of specific booking types and refund terms can vary by case.
* Fixed bookings
  * Benefit: Generally more budget-friendly.
  * Drawback: Harder or more costly to modify if your dates shift.
  * Uncertainty: Strict cancellation policies may apply if your schedule changes.

Next steps:
1. Check the specific purpose-of-visit and accommodation evidence requirements directly on the Royal Thai Embassy Kuala Lumpur website.
2. Prepare your documentation carefully before submitting through an authorized channel.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
```

Assistant assessment: Compared choices using bullets and uncertainty labels. Booking terms and embassy accommodation acceptance remain unverified; the reply added application-preparation background rather than limiting the next step to the booking decision.

### steps

Customer message: Before I spend money on an application, what should I check first? Please keep the next steps easy to follow.

History: `[{"role": "client", "message": "I am considering applying from Kuala Lumpur."}]`

Before (reused):

```text
Before paying any fees, you should verify the embassy's current requirements, ensure you have financial evidence of at least 500,000 THB, and check that your passport and purpose-of-visit documentation are fully prepared. Please note that processing through Kuala Lumpur typically takes about a month or more on a case-by-case basis, and the government visa application fee is non-refundable. For your next step, review the official Royal Thai Embassy Kuala Lumpur guidance to confirm your documents match their specific checklist.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
```

After:

```text
When applying through Kuala Lumpur, you should check the official embassy guidelines regarding preparation, processing estimates, and fee non-refundability before making any financial commitments. Processing may take approximately one month or more and is assessed case by case. **What to check** * Passport, photographs, and current-location evidence * Financial evidence of at least 500,000 THB and purpose-of-visit evidence * Embassy-specific document guidelines and non-refundable fee policies **Next steps** 1. Review the official Royal Thai Embassy Kuala Lumpur DTV guidance page. 2. Prepare your documents at least 30 working days before your intended travel. Please note that processing times and additional document requests can vary.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
```

Assistant assessment: Markdown headings, bullet markers and numbered items appeared inline in one paragraph, so it did not produce valid segmented layout. It also changed an instruction to apply before travel into preparing documents before travel.

### simple

Customer message: I sent a payment. Can you confirm you received it?

History: `[]`

Before (reused):

```text
I cannot check accounts, verify payments, or confirm receipts in this demo chat, as there are no payment or account integrations. Please check with your financial institution or the approved channel you used for your transaction.
```

After:

```text
I cannot check accounts, receive payments, or confirm transactions in this demo chat, as there are no payment or account integrations. Please check your payment status through your own bank or the official payment channel you used. If you are preparing for a visa application, ensure you follow the approved agency or official submission channels.
```

Assistant assessment: Preserved inability to confirm payment but appended unrelated visa/agency-channel guidance. This failed the prospective no-onboarding criterion.

## Consequence

No answer-layout rule from this trial remains active. The original factual and behavior safeguards remain, but generated replies can still ignore requested structure or add irrelevant guidance. Frontend paragraph spacing, safe Markdown rendering and saved-thread navigation remain in place. A future schema-based approach could make layout validation explicit, but it has not been implemented or evaluated here.
