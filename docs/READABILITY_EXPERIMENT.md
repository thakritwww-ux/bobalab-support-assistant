# Live readability experiment — retained evidence, prompt restored

Fill explicitly approved the proposed formatting rule and bounded live tests after automatic approval review requested more specific authorization. The approved experiment used seven provider attempts, within the limit of fourteen.

## What changed and what stayed fixed

The live /improve-ai-manually endpoint added readable_structure. Every previous rule, the protected policy and reviewed knowledge stayed unchanged. The model and temperature were held fixed. Three synthetic requests were generated once before and once after; this small sample does not isolate every stochastic effect.

Original version: 23f300e4-4acb-40cc-9cad-dc6b6b28927c. Experimental version: f920dd2d-c8c5-48db-9f9a-61fee0dcec38. Restored version: 34d6cf6a-bfe6-4fff-b76b-53718b5caa1a.

## Exact instruction

```text
Add a single conditional style rule named readable_structure with the following meaning, leaving every existing rule untouched: For replies with several distinct points, start with a short direct answer and use brief descriptive Markdown headings, bullets or numbered steps where useful. Use a compact Markdown comparison table only for supported options with meaningful tradeoffs. Keep uncertainty and the practical next step visible. Keep simple answers short without forced headings. Never invent data, charts, probabilities, progress indicators, requirements or actions for presentation.
```

## Assistant assessment

The options reply gained headings and bullets, but described flexible bookings as penalty-free without actual booking terms. The baseline also generalized booking conditions; neither should be treated as a verified accommodation policy. The steps reply remained a dense paragraph. The payment reply added unrequested agency-document guidance. The assistant restored the stable content rather than claiming a general quality gain. These are assistant observations, not candidate scores.

## Actual matched replies

### options

Customer input: I am Indonesian and considering a DTV application from Kuala Lumpur. My dates might change and my budget is tight. How should I compare flexible and fixed accommodation bookings?

History: `[]`

Before:

```text
When comparing flexible and fixed accommodation bookings for your DTV application through Kuala Lumpur, flexible bookings allow you to adjust your dates if travel plans shift, but they often come with a higher nightly rate. Fixed bookings are generally more budget-friendly, but they lock you into rigid dates and carry cancellation penalties if your timeline changes. As a next step, you may want to weigh your travel flexibility against your accommodation budget before preparing your application documents.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
```

After:

```text
When preparing your Destination Thailand Visa application through Kuala Lumpur, choosing between flexible and fixed accommodation bookings involves balancing cost and travel certainty. Here is a brief comparison to help you weigh your options: 

### Flexible Bookings
- **Benefit:** Allows you to change your dates without financial penalties if your travel plans shift.
- **Drawback:** Generally carries a higher nightly rate or upfront price tag.

### Fixed Bookings
- **Benefit:** Usually offers a lower, more budget-friendly rate.
- **Drawback:** Provides no leeway if your schedule changes, and you could lose your payments if plans are disrupted.

Since processing times through the Royal Thai Embassy in Kuala Lumpur can vary and are assessed case by case, official guidance recommends applying at least 30 working days before intended travel, keeping in mind that government visa application fees are non-refundable. A practical next step is to check current accommodation pricing for your estimated timeframe to see how much flexibility your budget can accommodate.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
```

### steps

Customer input: Before I spend money on an application, what should I check first? Please keep the next steps easy to follow.

History: `[{"role": "client", "message": "I am considering applying from Kuala Lumpur."}]`

Before:

```text
Before paying any fees, you should verify the embassy's current requirements, ensure you have financial evidence of at least 500,000 THB, and check that your passport and purpose-of-visit documentation are fully prepared. Please note that processing through Kuala Lumpur typically takes about a month or more on a case-by-case basis, and the government visa application fee is non-refundable. For your next step, review the official Royal Thai Embassy Kuala Lumpur guidance to confirm your documents match their specific checklist.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
```

After:

```text
Before paying any fees, you should verify the specific document checklist directly with the Royal Thai Embassy in Kuala Lumpur, as they advise applying at least 30 working days before intended travel and note that processing times can take about a month or more on a case-by-case basis. Additionally, keep in mind that government visa application fees are non-refundable. For your next step, review the official embassy guidance page to ensure your current-location, financial, and purpose-of-visit evidence meets their exact local standards.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
```

### simple

Customer input: I sent a payment. Can you confirm you received it?

History: `[]`

Before:

```text
I cannot check accounts, verify payments, or confirm receipts in this demo chat, as there are no payment or account integrations. Please check with your financial institution or the approved channel you used for your transaction.
```

After:

```text
I cannot check accounts or confirm payments in this demo chat as there is no payment integration. For our agency demo workflow, please prepare your documents for review through our approved channel, and ensure you check with your financial institution regarding your transaction status.
```

## Website behavior retained

Safe Markdown rendering and optional IndexedDB conversation history remain implemented. Long plain paragraphs can also gain spacing at sentence boundaries using the browser sentence segmenter; words/order/copy text remain unchanged. No headings, facts, charts or comparison rows are inferred from an ordinary paragraph. This presentation fallback does not depend on activating the rejected prompt candidate.

[Machine-readable evidence](evidence/readability-experiment.json) records the full sections, instruction, replies and restoration. Earlier automatic/manual improvement evidence remains separate.
