# Candidate-led answer hierarchy experiment

## Decision and attribution

During discussion on 27 October 2026, Fill chose a combination of describing the
options and making a conditional recommendation. The assistant proposed the
specific conditions and answer patterns; Fill agreed to proceed with the focused
refinement and comparison. This is a product decision, not a claim of personally
writing the implementation or independently producing the assistant's proposals.

The intended behavior is to describe relevant supported alternatives with their
benefits and drawbacks, then explain which fits the customer's stated priorities
and constraints. Missing evidence or conflicting priorities should lead to a
focused clarification or conditional explanation rather than an invented decision.

## Proposed patterns

| Immediate need | Information order |
|---|---|
| Simple explanation | Direct answer, then an essential qualification if needed |
| Practical decision | Main constraint, option tradeoffs, justified conditional recommendation, useful next step |
| Unavailable action | Acknowledge request, relevant capability limit, feasible way to proceed |
| Uncertainty | What is supported, what cannot be established, material clarification or review |

Patterns are conditional and can overlap. They do not require every reply to have
headings, options or a closing question. A material uncertainty may need to appear
before a direct answer. Sources must support relevant claims. No new facts,
capabilities or eligibility decisions are authorized by this experiment.

## Protocol fixed before generation

- Six developer-authored/selected cases in eval/hierarchy_cases.json: explicit
  preference, conflicting priorities, unavailable offer details, accommodation,
  payment and a simple definition. Three reuse known inputs; none is a blind test.
- Hypothetical booking terms test reasoning from stated assumptions, not verified
  booking products or agency policies. They do not establish real-world availability.
- Capture before replies from the currently restored active version, then refine
  only existing organization rules through the real manual improvement endpoint.
- Hold requests, reviewed knowledge, protected policy, model, temperature, timeout,
  output budget and retry policy fixed. Retain failures rather than replacing them.
- Compare option coverage, the link from recommendation to stated priorities,
  unsupported assumptions, useful next action and unnecessary content. Separately
  inspect factual support, capability honesty and simple-answer regressions.
- This evaluates manual instruction improvement, not automatic learning or model
  weight training. A saved edit is not a quality gain. Candidate output verdicts
  remain pending and the earlier requested pair review is deferred at Fill's request.

## Status

The real hosted manual endpoint returned 200 with `learningStatus: applied` and
saved version `ce7e6789-c0ff-4a68-b940-8caf7ce8ccd7`. It replaced exactly `direct`
and `choices` with the intended text; the other rules, protected policy and reviewed
knowledge were unchanged. The hosted edit took 62.555 seconds in this observation.
The exact instruction and persistence checks are in
[hierarchy-edit-summary.json](evidence/hierarchy-edit-summary.json).

All six before requests and all six after requests returned replies. See the
[complete comparison](HIERARCHY_COMPARISON.md) for original replies, actual prompt
diff and resulting replies. This is one sample per case at matched settings, not a
statistical estimate of reliability. No failures were removed or replaced.

## AI-assisted assessment, not candidate verdicts

| Case | Observed result |
|---|---|
| Explicit preference | After describes both options before recommending B and explains the fit and cost drawback. Before already recommended B and described tradeoffs, but placed the recommendation first. This is a narrow improvement in alignment with the chosen order, not a newly acquired ability to compare. Neither answer explicitly labels the assumed terms as hypothetical. |
| Conflicting priorities | After asks which priority matters more instead of selecting a preference. However, it generalizes the hypothetical terms into a claim about cheaper bookings typically being inflexible. Before also added unsupported loss/change-fee assumptions. Neither is fully satisfactory. |
| Unverified packages | After removes the unrelated visa checklist. However, it links inability to recommend to missing booking integrations. The relevant distinction is missing verified offer terms; an assistant can compare supported terms without making a booking. No official agency booking channel was established by this test. |
| Accommodation | After still fails to compare practical alternatives and omits the approximate one-month-or-more estimate that appeared before. It retains scoped advance-application guidance and uncertainty, but that does not answer the booking-duration concern. This is a material usefulness concern. |
| Payment | Both avoid confirming payment. After still lacks acknowledgement and adds the unnecessary phrase "once you are ready" although the customer already reported a transfer. A bank's outgoing-transfer status alone does not establish agency receipt. |
| Simple overview | Both remain short and supported, without forcing an options template or closing question. This sample shows no obvious template-related verbosity regression. |

These observations are assistant judgments. On 28 October, Fill preferred after
for explicit priority (with requested tone/uncertainty/continuation changes) and
conflicting priorities (without a supplied reason). See CASE_REVIEW.md for his
actual wording. The remaining outputs and numerical scores are unreviewed.

## Activation decision

The experiment demonstrates a successful manual instruction change and a narrow
ordering improvement. It does **not** establish overall quality improvement or
reliable execution of the hierarchy. Given the missing accommodation guidance and
remaining assumption errors, the assistant restored the previous evaluated
instructions after the comparison. The experimental version remains immutable and
can be inspected or evaluated by version ID; its text was not promoted into the
fresh-install seed playbook.

The restored version ID is recorded in the edit summary and current
[prompt snapshot](evidence/prompt-snapshot.json). The rollback restores behavior,
not the source collection or protected policy. No new model call is needed to roll
back. Existing automatic-learning evidence remains separate from this experiment.

The next design question is whether more explicit evidence/assumption handling and
a distinct real-world planning example would address the observed failures. That
would be a further validation-driven revision, not an independent unseen test.
No additional hierarchy revision or structural response-format feature has been
implemented. Candidate review should precede any claim that this design improved
the customer experience.
