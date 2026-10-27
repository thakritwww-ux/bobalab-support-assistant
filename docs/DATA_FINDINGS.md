# What the dataset does and does not support

Source: [BOBALAB assignment](https://github.com/MoriJinzz/Bobalab-Assesment), revision
`67dff7ad5fe38c54725df44e0e8d86943b424f16`. `data/conversations.json` is an unchanged
copy provided for this assessment. Upstream supplies no license file; this project
does not invent a license or claim authorship of the supplied data.

- 15 synthetic conversations, 262 messages: 132 inbound and 130 outbound.
- 128 customer-run / consultant-run pairs, with preceding history only.
- 241 adjacent gaps are 60 seconds, four are 20 seconds, one is 40 seconds,
  and one is 3,040 seconds. These do not measure real support response performance.
- Every conversation ends outbound. There are no observed dropout labels.
  Costs, waiting, interviews and location constraints are friction cues, not
  validated conversion or ghosting predictors.

## Parsing

Preserve source order. Group consecutive directions. SYNTH_012 begins outbound,
which belongs in history. SYNTH_008 has a payment/attachment inbound run.
SYNTH_015 has three attachment placeholders followed by text, and consecutive
outbound messages 19–20. Message 20 is delayed and claims completed document review.
Keep it in the original reference/history, but exclude it from the immediate
learning reference and flag it. The delay threshold is a heuristic; the event's
content also warrants the capability warning.

Attachments have no accessible contents. Placeholders are not actual app links,
bank details, contact information or proof of a system action.

## Noisy references

- SYNTH_003/010/014: 5,000 service + 10,000 government is described as 18,000 total.
- SYNTH_004/009: advice about hiding relevant client relationships must not become
  a learned support rule. Ordinary focused interview preparation is not automatically
  dishonest; assess the actual advice.
- Multiple examples claim account lookup, payment confirmation, document inspection
  and submissions. The proposed demo has none of those integrations.
- Different countries' processing times are not inherently contradictory. A
  country-matched official source can nevertheless conflict with an old sample.
- Tone is warm, moderately professional support. Customers are brief; consultants
  use explanations, lists and next steps. Do not equate more casual wording with
  better assistance.

The candidate chose sources, practical options, pros/cons and a visible path forward
after discussing the accommodation example. This decision is evaluated separately
from developer-discovered data errors. Neither analysis nor code is itself evidence
that the deployed model improved.
