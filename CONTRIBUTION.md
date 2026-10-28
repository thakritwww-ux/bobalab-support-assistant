# Contribution and ownership

## Candidate decisions, made during planning

Thakrit Wongwiwatseree (Fill) chose:

- Resolve a concern before suggesting a next step.
- Explain uncertain exceptions with preparation guidance, not promises.
- Learn tone plus conditional support behavior, while separating factual review.
- Use a reviewed official-source collection rather than live web browsing.
- Keep the submission API-first, understandable and strictly free.
- For consequential choices, show sources, options, pros/cons and the path forward.

The last principle came from Fill's own explanation of the accommodation case,
not a claim that he independently discovered every dataset issue or wrote the code.

## Payment-response review during live testing

Fill first suggested acknowledging the transfer and promising that the team would
be contacted and the customer called back. The assistant identified that this
promise exceeds the API's capabilities: no team notification or follow-up is sent.
Fill then retained the payment-verification limit and suggested preparing documents
for the transaction team. The assistant's proposed adaptation keeps preparation
focused on payment evidence, without inventing a required-document checklist.

This captures a real product tradeoff: useful ownership and preparation versus an
unsupported operational promise. Original candidate wording is distinct from
assistant-authored corrections and has not been represented as a supplied consultant
conversation. Candidate scores and approval of final outputs remain pending.

## Answer hierarchy decision

Fill proposed organizing customer-facing information into a clearer hierarchy.
After discussing neutral option descriptions and conditional recommendations, he
selected their combination: describe the choices, then give a recommendation tied
to the customer's stated priorities. The assistant proposed the detailed conditions
and implementation. Fill authorized a focused manual-improvement experiment.
See docs/ANSWER_HIERARCHY.md for the prospective protocol and attribution.
On 28 October, Fill reviewed the explicit-priority pair and preferred after with
requested changes: a more flexible tone, uncertainty and an invitation to continue
or correct the recommendation. The verbatim review is in docs/CASE_REVIEW.md.
Remaining output judgments and numerical scores are pending. The exact follow-up
implementation wording is assistant-authored, rather than quoted candidate text.

Fill subsequently preferred after for the conflicting-priorities pair without
supplying a reason or numerical score, and instructed the assistant to continue
operations. This authorizes continued refinement and verification; it does not
turn assistant-authored assessments of other cases into candidate judgments.

Under that authorization, the assistant tested the tone/uncertainty follow-up and
restored stable instructions after mixed results, preserving all outputs. Fill's
two preferences concern the earlier hierarchy pairs, not personal acceptance of
the follow-up or final regression outputs. See docs/HIERARCHY_FOLLOWUP.md.

## Required attribution in final deliverables

Fill explicitly requested that these decisions and contributions be retained and
mentioned in the final submission. The contribution summary, README/submission
summary and AI-usage disclosure must consistently include:

- His concern-first, understandable support approach and preference for sources,
  practical options, benefits/drawbacks and a visible next step.
- His proposal for a customer-facing answer hierarchy and his choice to combine
  option descriptions with conditional recommendations tied to stated priorities.
- His payment-response drafts and revision after discussing the assistant's actual
  capabilities, distinguishing his wording from assistant-authored corrections.
- His selected learning boundaries, reviewed-source approach, API/documentation
  scope and strictly free-service constraint.

Implementation, test execution, preliminary output assessment and the hierarchy
rollback were performed by the assistant. Fill authorized the experiment and has
supplied two qualitative preferences, including one with requested changes; he has not accepted
the whole experimental playbook or supplied numerical quality scores. Automated checks
and AI-assisted observations do not complete his review. Record his later judgments
and any actual code modifications only after they happen. Do not claim model-weight
training, general quality improvement or independently authored code on his behalf.

## Browser interface and identity handoff — 28 October 2026

Fill expanded the original API-only scope by requesting a browser interface and
materials covering UI, visual identity, style, fonts, features and customer journey
for a more specialized design LLM. He clarified that CI means visual brand identity
and the website must not use an unrelated name. The established BOBALAB name is
retained throughout the packet.

The assistant authored the requirements, wireframes, proposed colours/fonts,
integration constraints, labeled fixtures and designer prompt in docs/design/.
Those visual choices are proposals, not Fill's approved CI or official BOBALAB assets.
This paragraph records the earlier handoff stage. Fill subsequently instructed the assistant to go ahead and design/build it. The first responsive Flask browser UI and generation-only session adapter are now implemented; detailed design and code are assistant-authored. Candidate acceptance of the finished visuals has not been recorded.

Fill also supplied the repository-local UI UX Pro Max skill and authorized making
it available through GitHub and using it. The assistant verified its local search
commands, preserved its source and upstream license, and reconciled its output
against the BOBALAB requirements. Providing/selecting the tool is Fill's contribution;
the detailed design reconciliation and contrast calculation are assistant work.
The assistant implemented a green/neutral design with self-hosted IBM Plex English/Thai fonts and Lucide icons, and tested browser behavior and access boundaries. Fill authorized implementation and selected the tool; no independent candidate code authorship or final CI acceptance is claimed. See docs/WEB_UI.md.

## Assistant contribution

The assistant inspected the assignment and data, suggested the controlled-learning
architecture, verified a small set of official sources, generated the implementation
and tests, and prepared setup/deployment/evidence tools and documentation.

## Candidate verification still pending

- Run and inspect the project in Cursor; record any actual edits and reasons.
- Verify the reviewed source extracts and agency-demo labeling.
- Review remaining before/after cases if desired; two qualitative preferences are
  already recorded and no numerical scores have been supplied.
- Confirm live endpoint access and the final repository/submission package.

Do not describe these pending tasks as completed. AI-produced findings must remain
distinguished from candidate decisions and personally verified observations.

## Limitations

Small synthetic dataset; limited source coverage; no real operational integrations;
free-service limits; semantic learning and citation errors remain possible. Live
model calls and hosted endpoint checks are recorded, but they do not establish
general answer-quality improvement or long-term availability.


## Customer readability and local history

Fill requested distinct answer segments, bullets/tables and useful visual structure,
using screenshots of ChatGPT's list/table presentation as references. He also asked
for durable customer-visible conversations, distinguishing them from developer
audit/prompt history. After discussing Graphify's limited demonstrated benefit here,
he declined Graphify work and explicitly instructed continuing website improvements.
The assistant implemented safe structured rendering and opt-in on-device history
with management/export controls, preserving original replies and source metadata.
Detailed code and test execution are assistant work. Local history does not imply
customer accounts, cross-device sync, model-weight training or global learning.
No acceptance of the final outputs or general quality improvement is inferred.


Fill also explicitly approved a bounded live test of the proposed formatting rule.
The assistant performed matched tests and restored the stable prompt after mixed
results/regressions. Authorization is Fill's; exact rule wording, code, test execution
and the rollback assessment are assistant work. His preference for structured
information remains implemented through the frontend without claiming that every
model answer now follows a hierarchy.


## Sidebar navigation and hierarchy follow-up

Fill supplied a screenshot of left-side conversation navigation and asked for that
layout. He then clarified that the next improvement meant the customer-answer
hierarchy, and instructed “sure fix the sidebar first then this.” The assistant
implemented desktop saved-thread navigation, mobile drawer presentation and
unsaved/stale-record safeguards. Visual details and test execution are assistant
work. The subsequent hierarchy refinement is recorded separately; no result or
quality acceptance is inferred in advance.


Fill explicitly approved the exact answer_layout rule and up to six live provider
attempts. The assistant ran the four-attempt trial, assessed the unchanged-rule and
factual boundaries, and restored stable content when structure/relevance criteria
were not met. Candidate authorization is distinct from assistant assessment; no
new personal output ratings or acceptance have been inferred.
