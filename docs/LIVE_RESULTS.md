# Live results — in progress

27 October 2026, Bangkok time. These are real free-tier model and Supabase checks,
not scripted test replies. Candidate evaluation and hosted deployment remain pending.

## Connections and initial baseline

- Supabase schema migration and initial seeding succeeded.
- A synthetic Gemini generation succeeded using the stored active prompt.
- The first 12-case baseline produced nine replies and three `model_unavailable`
  errors. The original raw capture is preserved locally; it is not replaced by
  selectively successful retries.
- A separate Laos-pricing diagnostic using a 30-second timeout returned a reply
  in 30.214 seconds. This supports allowing more time, not a claim of guaranteed
  reliability. The service default is now 30 seconds.
- The paired after-capture explicitly uses the original 20-second timeout. Model,
  temperature, inputs and reviewed knowledge are held constant. Deployment timeout
  tuning must not be counted as a learned answer-quality gain.

## First automatic learning batch

Eight development-only references were processed: two edits applied, five lessons
rejected, and one no-op. The protected policy and reviewed knowledge were unchanged.

| Pair | Outcome | Recorded reason/change |
|---|---|---|
| SYNTH_001:1 | Rejected | Unreviewed fact |
| SYNTH_002:1 | No change | No new edit proposed |
| SYNTH_003:1 | Rejected | Unreviewed fact |
| SYNTH_004:1 | Applied | Clarification rule emphasizes missing, material application-location information |
| SYNTH_005:1 | Rejected | Unavailable operational action |
| SYNTH_008:1 | Rejected | Unavailable operational action |
| SYNTH_010:1 | Rejected | Unreviewed fact |
| SYNTH_012:2 | Applied | Scope rule changed to address embassy document requests |

These classifications are the editor's outputs, not independent correctness labels.

## Observations to assess, not claims of success

- Some baseline replies are formal and verbose despite the intended approachable tone.
- The payment reply includes an embassy citation that does not establish the bot's
  payment-checking capability. Valid source identity does not ensure relevance.
- The scope edit replaced a general uncertain-exception rule with a narrower
  document-request rule. This may lose useful coverage; assess unrelated cases.
- An applied edit proves the mechanism changes persistent instructions. It does not
  by itself prove that the result is better.

The candidate has been asked to write a more approachable payment response as a
reviewer-authored synthetic reference. No response or personal scores are fabricated.

## Paired comparison and operational decision

The after-run returned eleven replies and one availability error. Only eight cases
produced replies in both runs. A successful response after an earlier timeout is
not a paired answer-quality improvement. The original 20-second timeout was used
for both captures; the status-only diagnostic logging identified provider 504s.

AI-assisted review did not find a clear overall quality gain. In particular, the
edited scope rule was narrower and several replies added unrelated eligibility or
processing details. The initial playbook was restored through the rollback command,
preserving the learned versions and evidence. This is an assistant assessment;
candidate verdicts remain pending.

As a separate implementation correction, the editor instructions now explicitly
require preserving the original coverage of generally applicable rules. This
instruction change is not retrospectively credited to the original learning run.
Its effect still needs a real follow-up test.
