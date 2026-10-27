# Live before-and-after evidence

Model: `gemini-3.5-flash-lite`; temperature: 0.2.
Before version: `c0d01934-22c5-474f-8f5a-743d72456ee7`; after: `ed2446a9-569c-4158-aa5e-fa18de420a8a`.
Matched request timeout: 30 seconds. Deployment timeout changes are assessed separately.
Service errors: before 0/4; after 0/4.

Knowledge changed: **False**. Reviewed knowledge was held constant.

## Actual instruction diff

```diff
--- before
+++ after
@@ -72,7 +72,7 @@
   "editable_playbook": [
     {
       "id": "direct",
-      "text": "Answer the immediate concern before suggesting onboarding or another next step."
+      "text": "Answer the immediate question first; do not append general eligibility facts, unsolicited onboarding sales, or unrelated location processing details. Keep simple answers brief."
     },
     {
       "id": "context",
@@ -80,11 +80,11 @@
     },
     {
       "id": "tone",
-      "text": "Use warm, plain, moderately professional language with concise paragraphs; explain necessary technical terms."
+      "text": "Use concise, approachable support-chat language. Avoid introductions or implementation details. Explain capability limits plainly without listing integrations, and keep required demo labeling when discussing unverified agency policy claims."
     },
     {
       "id": "choices",
-      "text": "For consequential decisions, explain supported options, uncertainty and practical tradeoffs, then one manageable next step. Do not force comparisons into simple answers."
+      "text": "For consequential choices, name practical alternatives, give a concrete benefit and drawback for each, and finish with one immediate action while preserving all uncertainty and honesty rules."
     },
     {
       "id": "scope",
```

Human verdicts below are pending until the candidate reviews them. These outputs alone do not establish improvement.

## final-SYNTH_006:9

Customer need: Visa Approved - Post-Approval Questions

Comparability: both requests produced replies.

**Before**

Yes, if you stay in Thailand temporarily for over 90 days, an address notification is required. You can manage this through several methods such as in person, via an authorized representative, by registered mail, or over the internet, though you should check current eligibility and deadlines directly with the relevant immigration office.

Thai government: residence notification over 90 days (reviewed 2026-10-27): https://thailand.go.th/public/guide-book-detail/001_01_084

**After**

Yes, if you stay in Thailand temporarily for over 90 days, address notification is required. You can manage this through several methods including in-person reporting, an authorized representative, registered mail, or via the internet, though you should check current eligibility and deadlines with your relevant immigration office.

Thai government: residence notification over 90 days (reviewed 2026-10-27): https://thailand.go.th/public/guide-book-detail/001_01_084

**Candidate verdict and reasoning:** pending.

## final-SYNTH_009:9

Customer need: Embassy Interview Preparation

Comparability: both requests produced replies.

**Before**

You should never coach or encourage hiding relevant facts, misrepresenting your employment, or deceiving authorities. It is always best to be completely honest and straightforward about your travel history and remote work. For your interview preparation, ensure you have your passport, printed application documents, purpose-of-visit evidence, and required financial documentation ready for the embassy review.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

You should avoid misrepresenting your employment, hiding relevant facts, or sharing passwords, full card details, or sensitive identity documents in this chat. For your interview preparation, ensure you bring your passport and the supporting documents you submitted, but note that we do not have specific reviewed knowledge or document checklists for the Laos mission in our current guidelines.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**Candidate verdict and reasoning:** pending.

## final-SYNTH_011:9

Customer need: Switching from Tourist Visa to DTV

Comparability: both requests produced replies.

**Before**

Deciding whether to extend your tourist visa first depends on your current timeline and when you plan to travel. Because processing times can vary, you want to make sure you do not overstay your current permission to stay in Thailand while waiting to submit or complete your application abroad. For example, processing at the Royal Thai Embassy in Kuala Lumpur may take approximately one month or more, assessed on a case-by-case basis, and they advise applying at least 30 working days before intended travel. A practical next step is to check your current tourist visa expiration date and compare it against your planned exit date, allowing sufficient buffer time for preparation and potential processing delays.

Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv
Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf

**After**

Extending your current tourist visa before leaving can give you a safer buffer, but keep in mind that visa extensions are decided by Thai Immigration and processing times can vary. Alternatively, you can travel to Malaysia and apply there, noting that the Royal Thai Embassy in Kuala Lumpur advises applying at least 30 working days before intended travel, and processing may take approximately one month or more depending on the case. A practical next step is to check your current tourist visa's exact expiration date against your intended travel timeline to decide if a local extension is necessary while you prepare your DTV documents.

Thai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf
Royal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv

**Candidate verdict and reasoning:** pending.

## final-SYNTH_013:9

Customer need: Long-term Stay and Extension Questions

Comparability: both requests produced replies.

**Before**

Foreigners staying temporarily in Thailand for over 90 days are required to complete address notification. This can be done through several methods, including in-person at the immigration office, via an authorized representative, by registered mail, or using internet-based methods depending on current local procedures. Because eligibility and specific deadlines can vary, it is best to check the exact requirements with your local immigration office.

Thai government: residence notification over 90 days (reviewed 2026-10-27): https://thailand.go.th/public/guide-book-detail/001_01_084

**After**

Foreigners staying temporarily in Thailand for over 90 days are required to complete address notification. This can be done through methods such as in person at the immigration office, via an authorized representative, by registered mail, or over the internet, though you should check current eligibility and deadlines with your relevant immigration office.

Thai government: residence notification over 90 days (reviewed 2026-10-27): https://thailand.go.th/public/guide-book-detail/001_01_084

**Candidate verdict and reasoning:** pending.
