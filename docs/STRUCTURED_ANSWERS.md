# Validated answer sections

Status: deployed on Render Free as application commit 9efb9da after local and hosted checks. This is a software presentation
contract, not another automatically editable prompt rule or model-weight training.

Fill's concern-first hierarchy guides this change: immediate answer, relevant
preparation/steps/options, uncertainty near the affected information and a useful
next step. Simple concerns need no additional sections. The exact schema, layout
instruction, implementation and test assessment are assistant-authored.

## Internal generation contract

The model's reply field becomes an object: direct_answer, optional caveat,
optional typed sections and optional next_step. Supported kinds are paragraph,
bullets, steps and comparison. Point-specific caveats and option uncertainty are
separate text fields. Unknown option benefits/drawbacks can stay null. The software
shows Not specified (or the Thai equivalent), rather than inventing cell contents.

The protected policy already delegates output shape to the supplied JSON schema.
Its text and reviewed knowledge remain unchanged. A versioned code-owned layout
instruction clarifies the new schema; it is appended to the stored prompt for this
mode and included with the schema in formatHash. DB promptVersion alone therefore
does not identify the entire effective generation setup. Both values are retained
in UI history/export. This trial compares generation designs, not isolated prompt
learning; earlier before/after evidence remains separate.

Pydantic enforces limits and field-kind relationships on the server. Newlines,
embedded Markdown section/list markers, missing items, unused hidden fields and
invalid comparisons are rejected. Invalid output gets the existing one bounded
retry; final failure returns an explicit service error. Validation checks structure,
not truth. Source-ID/URL/placeholder checks cover every original structured field.
No extra provider call is required solely to format a successful answer.

Gemini documents a JSON Schema subset and notes that some string-length constraints
are not enforced by the provider; local runtime validation remains necessary.
Sources: [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output),
[Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/).

## Compatibility

- POST /generate-reply still returns exactly aiReply as a string.
- Automatic improvement still returns predictedReply and updatedPrompt. Its
  prediction uses one captured prompt/version and the same selected generation mode.
- Manual improvement/editor permissions and immutable prompt history are unchanged.
- The server builds canonical Markdown text deterministically from validated fields,
  then appends the same reviewed source footer. Null/unsupported cells remain explicit.
- POST /ui/chat adds answer, replyFormat and formatHash, alongside existing fields.
  The browser renders section data with text nodes/native lists and tables; it does
  not depend on the model placing Markdown newlines correctly.
- Copy, subsequent API history and text export retain canonical aiReply. JSON export
  additionally retains the original typed fields. Older saved replies use the safe
  legacy renderer. No new customer-history database or account sync.
- REPLY_FORMAT=text is the legacy generation path. REPLY_FORMAT=sections selects
  the new contract. The release defaults to sections after local acceptance; hosted checks still gate final release.

## Local evidence

117 backend tests passed against disposable PostgreSQL, including generation/edit
contracts, malformed section rejection, source checks, budgets and bounded retry.
13 browser checks with clearly labeled fixtures passed: native lists/steps/tables,
uncertainty/null cells, literal pipes, exact copy/export, versioned history/reopen,
Thai labels, inert HTML, old saved threads and simple answers without filler.
Desktop/mobile axe audits had zero automated violations in those states; this is
not full accessibility certification. These are not real model-quality results.

Schema: answer-section-contract.json. Exact layout instruction:
answer-format-instruction.txt. Browser suite: tests/browser/answer-sections.cjs.
Local fixture: BROWSER_REPLY_FORMAT=sections BROWSER_PORT=8003 python -m tests.browser.preview.

## Approved live comparison and release gate

Explicitly approved before live use: at most 14 real provider attempts within the
existing free cap. Three matched synthetic cases (options, preparation and payment)
use at most six attempts. A hosted generation check uses at most two. Hosted
automatic improvement uses at most four (prediction plus editor), and manual
improvement at most two. Failed attempts count. Never raise the daily cap or use
paid fallback. UI/storage smoke checks can replay labeled recorded outputs at zero
model cost. Temporary edit probes are restored to the starting prompt afterward.

Reuse the prior baseline only with an identical stored-prompt/knowledge hash,
model and temperature; label that reuse. Record the new schema/instruction hash as
an additional changed variable. Accept only if all three generated outputs validate,
use useful structure without filler and avoid observed unsupported guarantees or
irrelevant agency onboarding. Structural success alone cannot establish general
answer-quality improvement. Preserve failures, rejections and any rollback.

Only enable/deploy sections if the live checks are acceptable. Otherwise retain
legacy production mode and the trial evidence. The user explicitly approved the fourteen-attempt live comparison and conditional
release. Six local provider attempts were used: the first three cases validated,
with one schema retry; two comparison rechecks corrected booking certainty and
separation of provider terms from government fees. Initial unsuccessful outputs are
retained. The final comparison is acceptable for the conditional hosted checks;
preparation/payment will be rechecked under the final contract through the required
endpoints. This is not an overall model-quality gain.


## Release outcome — 28 October 2026

117 backend tests and 13 section-browser checks passed. Render deployed 9efb9da
successfully (dep-dbgvqegm7kps73etgc80). The first hosted generation failed with
provider-side 503 after two attempts; the same input later succeeded in one.
All three required endpoints then returned 200. Automatic/manual probes each
persisted a temporary behavior change and were restored immediately afterward.
The final active prompt is f41fb3bf-ae36-43ef-8bdb-69c42e0c5aa8, with the unchanged
five-rule content hash e6f157fed5545314e16828a6963d9f83b601363fcb41b1112f30c26247260f84.

The complete trial used 12 of the explicitly approved 14 provider attempts:
local 6, hosted 6. No further provider calls are queued. The daily count was 74/100
afterward. The production default is sections; REPLY_FORMAT=text remains the
configuration rollback. Stored-prompt rollback restores editable rules, while
this format switch controls the code-owned schema/instruction. They are distinct.

The hosted browser smoke used the actual deployed assets/session and an explicitly
intercepted replay of recorded local model output. It verified typed tables,
uncertainty, exact copy, reload/reopen, format metadata and mobile navigation, with
zero extra model calls and no browser errors. It is not a fresh hosted UI generation.
See STRUCTURED_ANSWER_RESULTS.md and evidence/structured-answers.json for exact
before/after replies, earlier rejected iterations, failures and limitations.

This improves software control over presentation, not general factual accuracy.
The final comparison retains official citations that do not establish hotel terms.
The payment reply remains repetitive; the preparation reply omits a relevant
fee warning from its baseline and offers a specific checklist beyond the limited
extract. Candidate review of these new outputs is still pending.
