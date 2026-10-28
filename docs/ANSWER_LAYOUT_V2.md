# Second answer-layout trial

Requested after the sidebar update by Fill: “sure fix the sidebar first then this.”
This is an assistant-authored refinement of his answer-hierarchy product decision.
The failed first trial remains preserved in READABILITY_EXPERIMENT.md.

Proposed single style rule, answer_layout:

> Start with a short direct answer using only information needed for the immediate question. Put distinct points on separate lines: preparation under **What to check** with bullets; procedures under **Next steps** with numbered steps; comparisons as bullets showing each option's benefit, drawback and uncertain terms. Use a compact table only when every cell is supported. Put uncertainty beside its point and finish with one relevant action. Do not add facts or agency onboarding to fill a section. For a simple concern, use brief plain sentences without headings. Formatting must not add certainty, promises, requirements or capabilities.

Before activation, the sidebar must be deployed and verified. Keep all previous
rule texts, protected policy and reviewed knowledge unchanged. Use the existing
matched options/steps/payment inputs and settings. Baseline replies may be reused
from the prior experiment because their prompt-content hash equals the restored
active prompt; explicitly label this reuse rather than claiming a fresh baseline.

Budget: at most six additional provider attempts, keeping the prior seven-attempt
trial plus its one-request UI smoke and this follow-up within the approved fourteen.
The editor can use at most two; subsequent generations are guarded by the remaining
allowance. Failed attempts count. Stop rather than increase the free daily cap.

Prospective acceptance: visible useful segmentation in the multi-point cases;
no unsupported booking guarantees or irrelevant agency onboarding; payment remains
brief with its capability limit; all prior rules/knowledge/policy remain intact.
A table is conditional, not a mandatory success metric. Preserve failures and
regressions and restore stable instructions if this candidate is unacceptable.
No automatic-learning or overall answer-quality gain can be inferred from saving it.

Status: explicitly approved, executed and rolled back. The rule is not active.
The hosted manual endpoint added exactly answer_layout; previous rules, protected
policy and reviewed knowledge stayed unchanged. Four provider attempts were used
(one edit, three generations), below the approved maximum of six. No paid fallback.

## Outcome against the acceptance criteria

- Options: useful bullets and uncertainty labels appeared. Booking assumptions and
  application-preparation background remained; no verified accommodation policy is
  established by this reply.
- Preparation: headings/list markers were placed inline in a dense paragraph, so
  the intended structure was not valid Markdown. The reply also changed the scope
  of a timing instruction from applying to preparing documents.
- Payment: the capability limit remained, but unrelated visa/agency-channel guidance
  was appended. This failed the explicit no-onboarding condition.

The assistant restored the previous stable instructions. This is an assistant
assessment of a small trial, not a candidate score or a general model-quality claim.
The sidebar and safe frontend display remain deployed. The hierarchy is still not
reliable through the tested prompt-only approach.

[Full actual matched replies](ANSWER_LAYOUT_V2_RESULTS.md) and
[machine-readable evidence](evidence/answer-layout-v2.json) preserve the instruction,
prior/experimental sections, baseline reuse, responses, attempt count and rollback.
