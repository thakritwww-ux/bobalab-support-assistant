# Reviewed sources and authority

Review date: 27 October 2026, Bangkok. Initial review was AI-assisted; candidate
verification is pending. Full machine-readable extracts and limits are in
`data/knowledge.json`. No runtime web search is performed.

| Source | Scope and review result |
|---|---|
| [MFA July 2024 measures, page 4](https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf) | Historical general DTV overview: categories, five-year validity, entries, financial evidence and preparation. Not a current country checklist or exchange-rate source. Other pages' old visa-exemption rules are excluded. |
| [Kuala Lumpur DTV page](https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv) | Page updated 7 September 2026. Processing is described as approximately a month or more, case by case. Additional evidence can be requested. This is not Indonesia, Laos or Singapore guidance. Image-based checklists have not been transcribed. |
| [Government residence reporting guide](https://thailand.go.th/public/guide-book-detail/001_01_084) | General over-90-day reporting and available methods. Old checklist details and unsupported fine leniency are excluded. Current local procedure needs confirmation. |

Agency pricing, review-before-payment, and guarantees are not government policy.
Dataset-derived business information is explicitly labeled synthetic demonstration
information. The Laos total remains unresolved, not silently corrected to the
arithmetic sum. A government fee being non-refundable does not establish whether a
private agency might reimburse it under a separate agreement.

## Maintenance

1. Read the actual official page, not just a search snippet.
2. Check the mission, applicant circumstances, update date and supporting document.
3. Edit the scoped extract, limitations and review date in `data/knowledge.json`.
4. Have the candidate review the change and record it in the contribution log.
5. Run `python -m app.cli review-knowledge data/knowledge.json --reviewed`.
6. Re-run relevant behavioral cases. Record source correction separately from
   automatic behavioral improvement.

Sources are verified URL identities and reviewed extracts, not a guarantee of ongoing
legal accuracy. If official sources conflict or coverage is missing, explain that
uncertainty and suggest qualified review. Do not invent a new source or generalize
a mission-specific rule to another country.

## Submission-session recheck — 28 October 2026, Bangkok time

The assistant reopened all three official sources. The Kuala Lumpur page still
states the scoped advance-application guidance and approximate month-or-more
processing estimate; the historical MFA overview and government reporting guide
still support the bounded extracts recorded above. This is an AI-assisted recheck,
not candidate verification or confirmation that old material is a complete current
legal checklist. Image-based embassy checklists remain untranscribed. The knowledge
snapshot was held unchanged during the hierarchy follow-up experiment so source
maintenance is not counted as behavioral improvement.
