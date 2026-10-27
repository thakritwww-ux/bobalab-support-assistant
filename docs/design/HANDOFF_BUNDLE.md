# BOBALAB — self-contained specialist design packet

Prepared 28 October 2026. Name is fixed: **BOBALAB**. CI means visual brand identity.
This is a design handoff, not a working web UI. Confirmed user choices and proposed
visual/technical decisions are labeled. No credentials or runtime environment values
are included. Do not share .env or unrelated private handoffs with a design LLM.

Use DESIGNER_PROMPT.md as the instruction, or tell the specialist to design from
this packet and return the screen/state, identity, component and integration outputs
listed below. Existing API behavior must be preserved.

---

<!-- Source: DESIGN_HANDOFF.md -->

# BOBALAB — interface and visual identity brief

Status: ready for specialist design; not an implemented UI. Prepared 28 October
2026 from the current code and the candidate's recorded decisions.

## 1. Identity and purpose

**Website name and primary wordmark: BOBALAB.** Preserve this exact name. Do not
invent an alternative brand, unrelated assistant persona or named chatbot.
An explanatory subtitle such as "Visa support demo" is allowed; it is not a new
product name. Browser title proposal: "BOBALAB | Visa support demo".

Build a usable browser entry point to the working Thai DTV support API for this
take-home assessment. Help a person understand their immediate concern, available
information, uncertainty and next step. The interface should make it easy to read
and continue a conversation without suggesting real visa processing is occurring.

This is an assessment demonstration using synthetic enquiries, limited reviewed
sources and sample agency information. It is not an official embassy service or
a confirmed operating immigration agency. Human, approachable writing must not
misrepresent the assistant as a human consultant.

## 2. Decisions and authority

| Status | Decision |
|---|---|
| User-confirmed | Name BOBALAB; CI means visual brand identity |
| User-confirmed | Add a browser interface; prepare requirements for a specialist LLM |
| User-confirmed | Concern-first support; clear sources, practical options and tradeoffs |
| User-confirmed | Describe options, then offer a recommendation conditional on known priorities |
| User-confirmed | Less adamant tone; uncertainty; useful continuation or invitation to correct |
| User-confirmed | Strictly free services; accept limits and slow starts |
| Existing constraint | Automatic learning edits behavior, not facts/model weights; all three APIs remain |
| Proposed | One customer chat screen and About panel; access-code gate; English UI with English/Thai chat support |
| Proposed | Calm warm-neutral/green palette; IBM Plex typography; responsive flat conversation layout |
| Not provided | Official logo files, official brand colours or a BOBALAB brand manual |

The earlier API-only choice is historical; this request expands the scope. The
designer must distinguish proposed visual choices from user-approved decisions.

## 3. Users and immediate needs

Primary user: a person trying a synthetic visa enquiry, often uncertain about
preparation, timing, costs or what the assistant can actually do. They may write
in English or Thai, use a phone, and be unfamiliar with technical language.

Secondary user: an assessor testing the service and reading the evidence. Keep
their documentation/evidence access separate from the customer's conversation.
Do not put system prompts, training controls, raw JSON or internal model metrics
in the customer flow. A read-only documentation link can serve assessors.

## 4. Minimum browser release

### Required customer-facing features

- Responsive chat with readable English/Thai input/output and current-thread context.
- Clear demo access entry, using a future server-side browser session rather than
  exposing the privileged reviewer API key. See the technical appendix.
- Empty state with a short invitation and a few optional starter questions.
- Text composer, explicit Send, multiline support and visible pending state.
- One request at a time, preserving the draft on error and preventing duplicate sends.
- Faithful display of the actual aiReply, including line breaks and uncertainty.
- Safe, clickable source links when the reply contains them. No "verified answer" badge.
- Clear recovery for access expiry, input limits, unavailable service and quotas.
- New conversation/reset with confirmation when it would discard the current thread.
- About panel describing scope, AI/demo status, source limits and data handling.
- Copy reply action with success/failure feedback, if it fits the core layout.

### Outside the minimum release

- Document uploads/inspection, payment checks, bookings or application submissions.
- Live-agent transfer, staff notifications or promised follow-up.
- Accounts, saved conversation lists, cross-device history, analytics or persistent chat storage.
- Voice, live translation, file export, marketing funnels or a full content website.
- Live search, visa eligibility calculators, approval scores or application trackers.
- Public automatic/manual prompt-edit controls or rollback buttons.
- Simulated token streaming: the existing API returns one complete JSON response.

Optional later: a protected reviewer workspace that calls the two improvement
endpoints and shows prediction, actual change, status and versions. It needs a
separate authorization design and is not needed for the customer chat release.

## 5. Customer journey

| Stage | Customer need | UI behavior | Real system boundary |
|---|---|---|---|
| Arrive | Understand what this is | BOBALAB name, short scope/demo note, access entry | No operational agency or embassy identity implied |
| Enter | Try without a long onboarding form | Demo access code; then question or starter | Browser session is proposed, not implemented |
| Ask | Explain the immediate concern | Composer; retain known details in current thread | Client sends history with each request |
| Wait | Know the request is in progress | Honest pending state and slow-service message | No known progress percentage or guaranteed ETA |
| Read | Understand the answer and its limits | Clear text, relevant sources, readable spacing | Model behavior is imperfect; UI must not invent missing content |
| Decide | Compare useful paths | Show actual comparisons and conditional reasoning when present | No fabricated recommendation cards or eligibility conclusion |
| Clarify | Correct a constraint or ask more | Continue in the same thread | Keep exact request/response ordering |
| Act or leave | Know a feasible next step | Preparation/checking guidance as actually given; reset or close | No booking, submission or team contact takes place |

```mermaid
flowchart TD
    A[BOBALAB demo entry] --> B[Enter demo access code]
    B --> C[Ask a question or choose a starter]
    C --> D[Send one message with current history]
    D --> E[Waiting state]
    E -->|Reply received| F[Read answer and sources]
    E -->|Error or quota| G[Keep draft and show recovery]
    G -->|Explicit retry when appropriate| D
    F --> H{Need more information?}
    H -->|Clarify or correct| C
    H -->|Enough for now| I[Leave or start a new conversation]
```

No application-progress bar should be inferred from this journey. It describes
information use, not tracked operational milestones or customer conversion.

## 6. Information hierarchy

| Kind of enquiry | Intended content order |
|---|---|
| Simple definition | Answer, then an essential qualification if needed |
| Practical choice | Main constraint, relevant option tradeoffs, conditional recommendation, useful next step |
| Missing material information | What can be said, what is uncertain, focused clarification |
| Unavailable action | Acknowledge, relevant capability limit, feasible route to verification |

Recommendations should explain the connection to the customer's stated priorities
and leave room for a material correction. Do not repeat known priorities merely to
ask for agreement. A closing question is useful only when it supports continuation.

These are product intentions, not guaranteed structured backend fields. Earlier
hierarchy prompt experiments were rolled back after mixed results. The UI must
not silently rewrite, reorder, strengthen or add to model advice to make it look
as though learning succeeded. Essential uncertainty stays visible, not behind
a collapsed disclosure. New rendering behavior requires separate verification.

## 7. Screen inventory and low-fidelity layouts

### S1 — Demo access

BOBALAB wordmark, "Visa support demo", concise explanation, labeled access-code
field, Show/hide code control and "Open demo" action. Provide a useful invalid-code
message and the route to the code the reviewer was privately given. Do not ask for
Gemini, database or privileged reviewer keys. No new account or identity documents.

### S2 — Empty chat / desktop

```text
┌────────────────────────────────────────────────────────────────────┐
│ BOBALAB   Visa support demo                   About   New chat     │
├────────────────────────────────────────────────────────────────────┤
│ AI demo · Use made-up examples. Don't send personal documents.      │
│                                                                    │
│             What would you like to understand?                     │
│             Ask about preparation, timing or a concern.            │
│                                                                    │
│       [What is the DTV generally for?] [Planning my next step]      │
│                                                                    │
│        ┌───────────────────────────────────────────────────┐       │
│        │ Ask your question…                               │       │
│        │                                            Send  │       │
│        └───────────────────────────────────────────────────┘       │
│            AI can make mistakes. Check relevant sources.           │
└────────────────────────────────────────────────────────────────────┘
```

Starters prefill the composer; they do not spend a model call before Send. Proposed
starters should be neutral enquiries, not promises such as "Check my payment".

### S3 — Active chat / desktop

```text
┌────────────────────────────────────────────────────────────────────┐
│ BOBALAB   Visa support demo                   About   New chat     │
├────────────────────────────────────────────────────────────────────┤
│ Demo notice remains discoverable without dominating every reply.   │
│                                                                    │
│                  Customer question in a restrained tinted bubble   │
│                                                                    │
│ BOBALAB assistant                                                  │
│ Actual answer, readable paragraphs and any options it supplied.     │
│ Important uncertainty remains in the conversation.                 │
│ Sources mentioned: readable title/link when provided                │
│ [Copy reply]                                                       │
│                                                                    │
│        ┌───────────────────────────────────────────────────┐       │
│        │ Follow up or clarify…                            │       │
│        │                                            Send  │       │
│        └───────────────────────────────────────────────────┘       │
└────────────────────────────────────────────────────────────────────┘
```

Use a centered, restrained reading column, approximately 680–760 px on a large
screen, with breathing room. Prefer flat assistant text and subtle user bubbles
over cards inside cards. A sidebar is optional; do not invent saved chat history.

### S4 — Mobile

```text
┌───────────────────────────────┐
│ BOBALAB              About ⋯  │
│ Visa support demo             │
├───────────────────────────────┤
│ Compact demo/privacy note     │
│                               │
│          Customer question    │
│                               │
│ BOBALAB assistant             │
│ Readable answer and caveats   │
│ Sources mentioned            │
│                               │
├───────────────────────────────┤
│ Follow up…                    │
│                         Send  │
└───────────────────────────────┘
```

Composer stays usable with the mobile keyboard and safe area. Avoid narrow split
panes and horizontally scrolling option tables. Confirm reset on a populated
thread. Keep essential uncertainty visible when the keyboard is open.

### S5 — About / source information panel

Explain AI/demo status, limited reviewed sources, no operational integrations and
synthetic-data use. Distinguish model-provider handling from the app's proposed
in-memory chat behavior. A source being an official URL does not verify every
claim or imply endorsement. Offer documentation/evidence links in a secondary area.

### Required variants for S2–S4

Empty; draft; sending; slow response; received; no cited sources; long response;
Thai/mixed-language response; retryable error; access expired; rate limited;
daily allowance exhausted; input/history limit; reset confirmation; narrow viewport.

## 8. Visual brand identity proposal

Brand character: clear, attentive, calm and capable. The interface should make a
complicated question feel manageable. It should look like a support product rather
than a visa advertisement or a technical lab dashboard.

- Name: BOBALAB, consistently capitalized.
- Wordmark proposal: clean typographic BOBALAB; text-only is acceptable initially.
- Any new symbol must remain subordinate to the name. No unrelated mascot/name.
- Do not fabricate an official lab logo or copy government seals, passport stamps,
  approval emblems, national insignia or another service's identity.
- No claims of government affiliation, legal-team availability or success rates.
- Avoid stock travel photos, large promotional heroes and decorative elements that
  displace the conversation. Illustrations are optional, not required assets.

Proposed palette; exact machine-readable values are in design-tokens.json:

| Role | Proposed value | Intended use |
|---|---|---|
| Background | #F7F6F2 | Warm, quiet app canvas |
| Surface | #FFFFFF | Composer/panel backgrounds |
| Main text | #182B29 | Headings and conversation |
| Secondary text | #51645F | Supporting labels, readable metadata |
| Primary | #1D5D4F | Send/action/focus; not a claim of answer verification |
| Gentle tint | #DDECE6 | User message background |
| Decorative border | #D7E1DC | Nonessential separators only |
| Control border | #6B7F76 | Essential input/control boundaries |
| Error text | #A32935 | Errors with text/icon, not colour alone |
| Notice text | #795300 | Caution/uncertainty notices with written explanation |

Selected contrast pairs are computed separately. Any palette revision must be
rechecked; the calculation is not a complete accessibility certification.

## 9. Fonts and typography proposal

Use **IBM Plex Sans** for Latin UI and **IBM Plex Sans Thai Looped** for Thai.
Proposed weights: 400 body, 500 labels, 600 headings/actions. This pairing keeps
the family coherent while allowing Thai text to be checked for legibility.

Official availability: [IBM Plex repository](https://github.com/IBM/plex) and
[IBM typeface reference](https://www.ibm.com/design/language/typography/typeface/).
The upstream [font license](https://github.com/IBM/plex/blob/master/LICENSE.txt)
is Open Font License 1.1. Preserve its license/notices with redistributed font
files. The packet names the fonts; it does not bundle font files or a final logo.

Implementation proposal: self-host only the required WOFF2 faces, use font-display
swap, and keep a system fallback. No paid fonts or mandatory third-party font call.
English stack: IBM Plex Sans, IBM Plex Sans Thai Looped, system-ui, sans-serif.
For Thai-language content, place the Thai Looped family first and test mixed text.

| Element | Proposed size / line height |
|---|---|
| Initial invitation | 28–32 px / 1.2; smaller on mobile |
| App headings | 24 px / 1.3 |
| Conversation | 17 px / 1.6; Thai may need 1.75 after rendering checks |
| Form labels/buttons | 16 px / 1.4 |
| Secondary metadata | 14 px / 1.5 |

Use zero added letter spacing for Thai. Test combining marks, wrapping and real
English/Thai fixtures. No clipping or tiny source captions. Numeric sizes and font
choices are proposals; actual browser and native-language review are still required.

## 10. Style and components

- 4/8 px spacing rhythm; 16 px minimum mobile side padding; generous paragraph spacing.
- Restrained rounded corners: about 8 px controls, 12 px messages/panels.
- Minimal shadows; visible borders where needed; no gradient-heavy dashboard shell.
- Clear text labels, visible keyboard focus and disabled/sending states.
- Primary actions about 44 px high as a product usability target, distinct from
  WCAG's smaller minimum target criterion and its exceptions.
- Motion is functional and short; respect reduced-motion preferences. No simulated
  streaming, fake progress percentages or large theatrical animations.

Required components: app header/wordmark, demo notice, access form, starter chip,
message, source link, composer, Send, pending status, error notice, quota notice,
copy action, reset confirmation and About panel. Show hover/focus/disabled/error
variants wherever applicable. Colour alone must not communicate meaning.

## 11. Copy and voice

Proposed interface copy, not model-test evidence:

| Situation | Copy direction |
|---|---|
| Empty | "What would you like to understand?" |
| Composer | "Ask your question…" / "Follow up or clarify…" |
| Pending | "Preparing a reply…" |
| Slow | "This may take a little longer on free hosting." |
| Retryable failure | "The assistant couldn't reply. Your message is still here." |
| Daily limit | "The demo has reached its daily allowance. Please try another Bangkok day." |
| Source area | "Sources mentioned"; not "Fact-checked answer" |
| Reset | "Start a new conversation? This clears the chat in this tab." |

Keep public copy plain; do not expose prompt-version IDs, exception names or raw
provider errors. Acknowledge limits without listing internal integrations. Make
the AI identity and synthetic nature clear in the interface without labeling
official visa information as fictional agency policy in every reply.

## 12. Accessibility and delivery

Design toward WCAG 2.2 AA; do not claim compliance before implementation testing.
Ordinary text should meet at least 4.5:1 contrast; large text at least 3:1, with
the standard's exceptions. See [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
Pointer target minimums and exceptions are described in [W3C target guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html);
our proposed primary controls target 44 px. Status changes should be exposed to
assistive technology without moving focus unnecessarily, per [W3C status guidance](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).

Provide keyboard-only flows, labeled controls, readable focus, reduced motion,
zoom/reflow checks and no loss of content on narrow mobile screens. Test the
mobile keyboard, source-link wrapping and Thai combining marks. English interface
copy plus English/Thai chat support is the proposed MVP; full UI translation is
optional and must not be implied by a nonfunctional language switch.

The specialist should return: a visual concept with rationale; desktop/mobile
screens and all key states; CI/style/token sheet; font/asset manifest; component
specifications; customer-journey map; interaction and accessibility notes; and a
clear handoff identifying required backend work. Visual mockups are not evidence
that backend capabilities exist or that answer quality improved.


---

<!-- Source: IMPLEMENTATION_CONSTRAINTS.md -->

# BOBALAB — implementation constraints for the designer/builder

This document describes current facts and proposed work separately. It is not
permission to expose secrets or a claim that browser routes already exist.

## 1. Existing service

- Repository: https://github.com/thakritwww-ux/bobalab-support-assistant
- API origin: https://bobalab-support-assistant.onrender.com
- Flask/Python, Gemini SDK, Supabase Postgres, Render Free.
- A terminal client exists at scripts/chat.py. No browser frontend exists yet.
- All non-health requests currently pass through the X-API-Key gate in
  app/__init__.py. Adding a template at GET / or static assets alone will still
  hit that gate unless carefully scoped browser-route handling is implemented.
- The runtime has one Gunicorn worker/four threads, process-local request throttling
  and a durable 100-model-attempt Bangkok-day budget. Retries consume attempts.
- The three existing assessment contracts and their authentication must remain usable.

## 2. Existing API contract

All requests/outputs are JSON. Model routes require the private reviewer key in
X-API-Key. History runs oldest to newest and excludes the current clientSequence.
Map browser user messages to role client and successful assistant messages to role
consultant. Do not send role assistant or duplicate the pending question in history.

| Existing route | Request | Required response |
|---|---|---|
| POST /generate-reply | clientSequence string, chatHistory array | aiReply string |
| POST /improve-ai | Same plus consultantReply string | predictedReply string, updatedPrompt string |
| POST /improve-ai-manually | instructions string | updatedPrompt string |
| GET /health | No key/body | status, service, readiness; liveness only |

Editing responses additionally expose learningStatus (applied/no_change/rejected),
versionId, appliedEdits and rejectedLearnings. A 200 edit is not necessarily a saved
change. There is no public history, rollback, usage, streaming or structured-decision
endpoint. History/rollback currently use the maintenance CLI.

Exact schema snapshots and limits are in api-contract.json, generated from current
Pydantic models. Principal limits: 6,000 characters per message; 100 history entries;
24,000 conversation characters total; 4,000 manual-instruction characters; request
body at most 64 KiB. The UTF-8 serialized byte limit can be reached before the
character limit, especially with Thai. Server validation remains authoritative.

## 3. Actual reply structure

generate-reply returns one aiReply string. Sources are appended as text with a
title, review date and approved URL. It does not return option cards, recommendation
objects, confidence scores, eligibility results or separate source arrays.

For the first release, preserve the actual text and paragraphs. Render as text,
with safe links for approved source URLs. Do not parse arbitrary sentences into
"verified" cards, fabricate a recommended option, omit caveats or invent missing
comparison content. Source URL identity is checked by the backend; relevance can
still be wrong. Use "Sources mentioned" rather than a factual-verification claim.

Rich source/option components would require a separately specified and tested
adapter contract. They must not add another model call or change the required API
response shapes silently. Do not implement them merely because a mockup shows cards.

## 4. Proposed browser integration — not implemented

Recommended minimal path: serve responsive HTML/CSS/JS from the existing Flask app
and add a same-origin, authenticated browser adapter. This avoids requiring another
paid service or separate frontend host. A specialist may propose a different free
stack, but must justify extra hosting, build complexity and authentication work.

Proposed route names, which do not exist yet:

| Route | Intended access and behavior |
|---|---|
| GET / and static assets | Public shell/access UI; no privileged data |
| POST /ui/session | Rate-limited demo-code verification and browser session creation |
| POST /ui/chat | Authenticated browser session; validate context and call the generation service once |
| POST /ui/logout | Clear browser session; protected against cross-site submission |

The shell can show access entry or chat according to session state. Keep the original
three API routes behind X-API-Key. Do not make cookie login an alternative credential
for automatic/manual improvement routes: that would grant chat users prompt-edit power.
Do not remove the key gate globally to make the website load.

New browser access code/session-secret configuration would be required; placeholders
such as UI_DEMO_ACCESS_CODE and UI_SESSION_SECRET are **planned names only**. They
are not configured and no values belong in this packet. A short-lived cookie session
should contain only minimal authorization state, never provider/reviewer keys or
conversation transcripts. Add secure/HttpOnly/SameSite cookie settings, cross-site
request protection, logout and login/usage controls before publishing the adapter.

The server can reuse AssistantService.generate directly after browser authentication,
input validation and request throttling. Preserve the durable model allowance. Do
not proxy arbitrary URLs or accept client-selected credentials. An unprotected proxy
with a hidden key is still an unprotected model-spending endpoint.

No Gemini, database, privileged reviewer or session-signing key belongs in browser
JavaScript, public-prefixed environment variables, localStorage, screenshots or a
specialist-LLM prompt. The demo access code is distinct from those keys. For technical
implementation, consult [Flask security guidance](https://flask.palletsprojects.com/en/stable/web-security/).
This describes required work; this packet does not implement authentication.

## 5. Conversation state and pending requests

- Default to memory in the open tab only. Do not save chats to localStorage,
  sessionStorage, a database or analytics without a separate approved feature.
- Append a user turn and assistant turn to the request history only after a
  successful response. Keep failed/pending message state separate for retry UI.
- Allow one in-flight send per chat. Enter sends, Shift+Enter creates a new line;
  respect composition events so IME input is not submitted prematurely.
- A starter fills the draft and still requires Send. Do not call the model on page
  load, while typing, for source display, or merely to demonstrate loading states.
- Preserve drafts after errors. Avoid silent automatic retries; every attempt may
  consume the shared allowance. Retry is an explicit action.
- Use a client request identity so reset/logout or a stale response cannot insert
  an old answer into a new conversation. Reset is not a server-side generation cancel.
- No token stream exists. Show an indeterminate pending state, then the complete
  response. Do not offer "Stop generating" unless actual cancellation is implemented.
- A refresh/reset clears the local thread, not the provider's records. Do not claim
  provider erasure. Explain that messages are sent to the model provider; its data
  handling is separate from the app's proposed local conversation state.

## 6. Loading and errors

Use the current 150-second client ceiling as a starting implementation constraint,
not an advertised wait time. The observed first resumed health probe was 52.409
seconds without proof of actual Render sleep state. Model requests have also failed.
No fake percentage, known completion time or "legal team is reviewing" animation.

| Situation | Customer recovery |
|---|---|
| Draft/empty | Send disabled for empty input; clear instructions and labels |
| Pending | Disable duplicate send; announce preparing reply without moving focus |
| Slow response | Patient free-hosting message; retain the draft and conversation |
| 400/413 | Explain message/history limit; shorten or start a new conversation |
| Browser session expiry | Preserve the draft in memory, ask to reopen demo access |
| API 401/config issue inside adapter | Owner configuration issue; never ask customer for provider/reviewer keys |
| 429 request_limit | Respect a valid Retry-After delay; no automatic retry loop |
| 429 daily_call_limit | Explain shared daily allowance; next Bangkok day, not a promised 60-second reset |
| 502 invalid/unsupported output | No fabricated fallback; show inability to prepare a reply and explicit retry |
| 503 provider/database unavailable | Preserve draft, explain temporary unavailability; no claim that payment/application failed |
| Network timeout | Explain no reply arrived; do not assert the server stopped processing |

Existing error envelope: {"error":{"code":"…","message":"…"}}. Display safe
customer copy; retain status/code for controlled diagnostics without logging user
content or keys. Health only shows process liveness, not model/database readiness.
There is no usage-count API: do not invent "messages remaining" metrics.

## 7. Safe display and privacy

Treat both model and customer text as untrusted. Use escaped text nodes or a narrowly
sanitized renderer; never raw innerHTML. Permit only approved HTTPS source URLs in
assistant source linkification; label destinations and use safe external-link behavior.
Do not execute links/code embedded in a customer message. Source inspection never
requires exposing system prompts or API credentials to the browser.

No uploads, payment details, identity-document collection or staff notification
controls. No analytics or raw-message logging in the initial release. Demo copy must
not say "nothing is stored anywhere" because the model provider receives messages.

## 8. Verification and release gates

Existing 63 tests are backend evidence; they are not browser tests or evidence of
WCAG compliance. A future implementation must add meaningful checks for session
isolation, protected edit routes, CSRF, escaped model text, safe source links, history
ordering, stale-response/reset handling, retries and duplicate sends. Also test real
desktop/mobile layouts, keyboard flow, Thai text and slow/failure states.

Keep fixtures clearly labeled and distinguish simulated UI tests from real provider
calls. Use the stable evaluated prompt for UI integration. No new training batch,
model swap or source edit is required to design the interface. Compare semantic
answer quality separately from visual polish. Run the three original cURLs again
after integration to ensure existing reviewer access and persistence still work.

No production deployment, new account, paid service, browser-auth configuration or
email sending is part of this materials task. The next builder must implement and
verify the proposed routes before the interface can be called operational.


---

<!-- Source: REQUIREMENTS_CHECKLIST.md -->

# BOBALAB interface requirements and acceptance list

P0 means required for the proposed first browser release. P1 is optional afterward.
These requirements are prepared; **implementation checks below have not run**.
CI here means visual identity. No automated CI pipeline is being requested or added.

| ID | Priority | Requirement | Acceptance evidence for the next builder |
|---|---|---|---|
| ID-01 | P0 | Name remains BOBALAB | Name/wordmark/title consistent on all screens; no renamed assistant/product |
| ID-02 | P0 | Truthful identity | AI/demo status visible; no government seal, fake agency identity or human-consultant impersonation |
| ID-03 | P0 | Proposed vs official CI separated | Brand rationale states that official BOBALAB assets were not provided |
| UI-01 | P0 | Responsive conversation layout | Desktop 1440/1280, tablet 768 and mobile 390/360 layouts; no clipped composer/content |
| UI-02 | P0 | Empty state and starters | Clear invitation; starter prefills draft; no unsolicited model request |
| UI-03 | P0 | Message/composer semantics | Labeled textarea, usable Send, multiline/composition handling and empty-input prevention |
| UI-04 | P0 | Current-thread context | Second message receives ordered prior client/consultant history; current question included once |
| UI-05 | P0 | One request at a time | Double-click/Enter cannot produce duplicate generation; stale responses do not enter reset threads |
| UI-06 | P0 | Complete state set | Empty/draft/pending/slow/reply/error/access/quota/limit/reset layouts supplied and implemented |
| UI-07 | P0 | Faithful actual output | Full reply and material caveats retained; no invented option/recommendation/source cards |
| UI-08 | P0 | Sources when present | Approved links clickable and readable; no verification badge or unsupported freshness claim |
| UI-09 | P0 | No fake capabilities | No uploads, payment confirmation, booking, submission, case tracking or team-contact controls |
| UI-10 | P0 | New conversation | Confirm destructive reset; clear local thread/draft; explain limits of deletion |
| UI-11 | P0 | Scope/data handling | About panel accurately explains demo, limited sources, local thread and external provider handling |
| UI-12 | P0 | Usable English/Thai text | Combining marks, mixed text, long URLs and line breaks display without clipping |
| UX-01 | P0 | Customer concern before funnel | No forced nationality/intake form or sales step before a general question |
| UX-02 | P0 | Conditional decision support | UI accommodates option tradeoffs and corrections but does not manufacture missing model content |
| UX-03 | P0 | Honest loading | No token streaming/progress percentage/guaranteed ETA without actual backend support |
| UX-04 | P0 | Recovery preserves work | Draft retained; explicit retry; request/daily quotas distinguished; no paid fallback |
| UX-05 | P0 | Clear source scope | No implication that an official source validates every claim or every application country |
| SEC-01 | P0 | Server-only credentials | No provider, DB, reviewer or signing keys in assets/storage/screenshots/network responses |
| SEC-02 | P0 | Gated browser adapter | Session/demo access implemented and rate limited; no unprotected spending proxy |
| SEC-03 | P0 | Original API auth preserved | Existing three API routes still require X-API-Key; browser chat session cannot edit prompts |
| SEC-04 | P0 | Exact public-route boundaries | Public shell/static/session entry work without disabling authentication globally |
| SEC-05 | P0 | Browser security | Session/logout, secure cookie settings and cross-site submission controls tested |
| SEC-06 | P0 | Safe rendering | Malicious HTML is text; no executable links; approved source URLs only for source treatment |
| DATA-01 | P0 | Request bounds | Message/context and serialized byte limits respected; no silent context truncation |
| DATA-02 | P0 | No transcript persistence by default | No localStorage/sessionStorage/database/analytics chat writes; no raw-body diagnostics |
| A11Y-01 | P0 | Measured contrast | Text pairs checked for intended size; essential boundaries/focus remain perceivable |
| A11Y-02 | P0 | Keyboard/screen reader | Focus order, labels, pending/error announcements and reset dialog tested |
| A11Y-03 | P0 | Reflow and interaction | Zoom/reflow, mobile keyboard, touch targets and reduced-motion preference tested |
| FONT-01 | P0 | License/asset manifest | Actual self-hosted fonts identified with version/weights and upstream license included |
| QA-01 | P0 | Tests remain honest | Backend tests, browser tests, fixture simulations and live calls reported separately |
| QA-02 | P0 | Original contracts retained | Three original cURLs and active DB prompt behavior rechecked after UI integration |
| QA-03 | P0 | Budget and scope | Free services; no provider change/new deployment/account without justified authorization |
| DEL-01 | P0 | Design handoff complete | CI sheet, components, desktop/mobile screens, states, journey and constraints delivered |
| DEL-02 | P0 | Contribution attribution | User choices distinguished from specialist proposals/implementation; no unmeasured benefit claims |
| OPT-01 | P1 | Full UI localization | Real English/Thai interface translations reviewed; no fake language switch |
| OPT-02 | P1 | Read-only evidence view | Clearly labeled before/after examples and provenance; no cherry-picked improvement claim |
| OPT-03 | P1 | Reviewer editing workspace | Separate privileged auth; statuses/version/conflict handling; no customer exposure |

## Design delivery acceptance

- [ ] Specialist produces the BOBALAB visual proposal and explains its choices.
- [ ] All P0 screens/states/components and mobile variants are specified.
- [ ] Proposed branding is identified as a proposal, with no invented official assets.
- [ ] Layout does not assume unsupported backend fields/capabilities.
- [ ] Font source/license, tokens and accessibility checks are handed off.
- [ ] Remaining questions/dependencies are explicit; no fake implemented status.

## Implementation release acceptance — a later stage

- [ ] Browser adapter/session/access configuration implemented and tested.
- [ ] Chat, context, errors, sources and reset verified with fixtures and real calls.
- [ ] Security and accessibility checks above completed, with observed results.
- [ ] Three existing API contracts and database edit behavior still work.
- [ ] README, hosted URL, contribution notes and AI log reflect actual UI work.

Prepared materials do not satisfy these implementation boxes. No web application
has been built as part of this handoff task.


---

## Appendix — design-tokens.json

```json
{
  "project": "BOBALAB",
  "status": "assistant-proposed starting point, not user-approved final CI",
  "prepared_on": "2026-10-28",
  "official_brand_assets_provided": false,
  "colors": {
    "background": "#F7F6F2",
    "surface": "#FFFFFF",
    "text": "#182B29",
    "textSecondary": "#51645F",
    "primary": "#1D5D4F",
    "primaryHover": "#16483D",
    "onPrimary": "#FFFFFF",
    "userTint": "#DDECE6",
    "borderDecorative": "#D7E1DC",
    "borderControl": "#6B7F76",
    "focus": "#1D5D4F",
    "error": "#A32935",
    "errorSurface": "#FCEEF0",
    "warning": "#795300",
    "warningSurface": "#FFF4D8",
    "info": "#254F78",
    "infoSurface": "#ECF3FA"
  },
  "typography": {
    "latinFamily": "IBM Plex Sans",
    "thaiFamily": "IBM Plex Sans Thai Looped",
    "fallback": [
      "system-ui",
      "sans-serif"
    ],
    "weights": [
      400,
      500,
      600
    ],
    "bodyPx": 17,
    "bodyLineHeight": 1.6,
    "thaiBodyLineHeight": 1.75,
    "metadataPx": 14,
    "headingPx": 24,
    "invitationPx": 32,
    "thaiAddedLetterSpacing": 0,
    "fontDisplay": "swap"
  },
  "spacingPx": [
    4,
    8,
    12,
    16,
    24,
    32,
    48,
    64
  ],
  "radiusPx": {
    "control": 8,
    "message": 12,
    "panel": 12
  },
  "layout": {
    "readingColumnMaxPx": 760,
    "mobileMinSidePaddingPx": 16,
    "designViewportsPx": [
      360,
      390,
      768,
      1280,
      1440
    ],
    "primaryControlHeightTargetPx": 44
  },
  "motion": {
    "shortTransitionMs": 160,
    "respectReducedMotion": true,
    "simulateTokenStreaming": false
  },
  "notes": [
    "Decorative border is not suitable as the only essential control boundary.",
    "Do not use green to claim a model answer is verified.",
    "Numbers are design proposals; test actual rendered states."
  ]
}
```

---

## Appendix — font-manifest.json

```json
{
  "status": "proposed; names/license checked upstream, font files not downloaded or bundled",
  "families": [
    {
      "name": "IBM Plex Sans",
      "use": "Latin interface and messages",
      "weights": [
        400,
        500,
        600
      ]
    },
    {
      "name": "IBM Plex Sans Thai Looped",
      "use": "Thai messages and future Thai interface copy",
      "weights": [
        400,
        500,
        600
      ]
    }
  ],
  "source": "https://github.com/IBM/plex",
  "typeface_reference": "https://www.ibm.com/design/language/typography/typeface/",
  "license": "OFL-1.1",
  "license_url": "https://github.com/IBM/plex/blob/master/LICENSE.txt",
  "implementation_requirements": [
    "Use actual upstream WOFF2 faces and record the chosen version/files.",
    "Retain license and copyright notices with redistributed font assets.",
    "Self-host required normal faces only; no paid font dependency.",
    "Use font-display swap and system fallbacks.",
    "Test English/Thai mixed text, combining marks and wrapping in actual browsers."
  ],
  "approved_final_brand": false
}
```

---

## Appendix — api-contract.json

```json
{
  "snapshot_on": "2026-10-28",
  "origin": "https://bobalab-support-assistant.onrender.com",
  "auth": {
    "existing_model_routes": "X-API-Key: private reviewer key",
    "public_existing_route": "GET /health",
    "browser_session_adapter": "proposed, not implemented",
    "expose_privileged_key_to_browser": false
  },
  "requests": {
    "generate-reply": {
      "$defs": {
        "Turn": {
          "additionalProperties": false,
          "properties": {
            "role": {
              "enum": [
                "client",
                "consultant"
              ],
              "title": "Role",
              "type": "string"
            },
            "message": {
              "maxLength": 6000,
              "minLength": 1,
              "title": "Message",
              "type": "string"
            }
          },
          "required": [
            "role",
            "message"
          ],
          "title": "Turn",
          "type": "object"
        }
      },
      "additionalProperties": false,
      "properties": {
        "clientSequence": {
          "maxLength": 6000,
          "minLength": 1,
          "title": "Clientsequence",
          "type": "string"
        },
        "chatHistory": {
          "items": {
            "$ref": "#/$defs/Turn"
          },
          "maxItems": 100,
          "title": "Chathistory",
          "type": "array"
        }
      },
      "required": [
        "clientSequence"
      ],
      "title": "ReplyRequest",
      "type": "object"
    },
    "improve-ai": {
      "$defs": {
        "Turn": {
          "additionalProperties": false,
          "properties": {
            "role": {
              "enum": [
                "client",
                "consultant"
              ],
              "title": "Role",
              "type": "string"
            },
            "message": {
              "maxLength": 6000,
              "minLength": 1,
              "title": "Message",
              "type": "string"
            }
          },
          "required": [
            "role",
            "message"
          ],
          "title": "Turn",
          "type": "object"
        }
      },
      "additionalProperties": false,
      "properties": {
        "clientSequence": {
          "maxLength": 6000,
          "minLength": 1,
          "title": "Clientsequence",
          "type": "string"
        },
        "chatHistory": {
          "items": {
            "$ref": "#/$defs/Turn"
          },
          "maxItems": 100,
          "title": "Chathistory",
          "type": "array"
        },
        "consultantReply": {
          "maxLength": 6000,
          "minLength": 1,
          "title": "Consultantreply",
          "type": "string"
        }
      },
      "required": [
        "clientSequence",
        "consultantReply"
      ],
      "title": "ImproveRequest",
      "type": "object"
    },
    "improve-ai-manually": {
      "additionalProperties": false,
      "properties": {
        "instructions": {
          "maxLength": 4000,
          "minLength": 1,
          "title": "Instructions",
          "type": "string"
        }
      },
      "required": [
        "instructions"
      ],
      "title": "ManualRequest",
      "type": "object"
    }
  },
  "responses": {
    "generate-reply": {
      "required": [
        "aiReply"
      ],
      "properties": {
        "aiReply": {
          "type": "string"
        }
      },
      "structured_sources_or_options": false,
      "streaming": false
    },
    "improve-ai": {
      "required": [
        "predictedReply",
        "updatedPrompt"
      ],
      "additional_observed": [
        "learningStatus",
        "versionId",
        "appliedEdits",
        "rejectedLearnings"
      ]
    },
    "improve-ai-manually": {
      "required": [
        "updatedPrompt"
      ],
      "additional_observed": [
        "learningStatus",
        "versionId",
        "appliedEdits",
        "rejectedLearnings"
      ]
    },
    "error": {
      "error": {
        "code": "string",
        "message": "string"
      }
    }
  },
  "limits": {
    "requestBytes": 65536,
    "messageCharacters": 6000,
    "historyEntries": 100,
    "conversationCharacters": 24000,
    "manualInstructionCharacters": 4000,
    "defaultModelAttemptsPerBangkokDay": 100,
    "defaultRequestsPerMinutePerProcess": 10,
    "clientTimeoutSecondsSuggested": 150
  },
  "notes": [
    "History roles are client and consultant, oldest to newest; current clientSequence is separate.",
    "chatHistory defaults to an empty array in the current schema; the browser should send it explicitly.",
    "Provider retries consume attempted-model-call allowance; this is not a customer-message counter.",
    "A 200 edit may be applied, no_change or rejected.",
    "GET /health is liveness only, not dependency readiness."
  ]
}
```

---

## Appendix — fixtures.json

```json
{
  "purpose": "Design and future simulated browser tests; no new model calls made for this packet",
  "all_customer_examples_synthetic": true,
  "observed_outputs_are_not_verified_advice": true,
  "fixtures": [
    {
      "id": "empty",
      "kind": "illustrative_interface_copy_not_implemented",
      "state": "empty",
      "heading": "What would you like to understand?",
      "placeholder": "Ask your question…"
    },
    {
      "id": "waiting",
      "kind": "illustrative_interface_copy_not_implemented",
      "state": "pending",
      "text": "Preparing a reply…",
      "fake_progress_or_streaming": false
    },
    {
      "id": "slow",
      "kind": "illustrative_interface_copy_not_implemented",
      "state": "slow",
      "text": "This may take a little longer on free hosting."
    },
    {
      "id": "received-with-sources",
      "kind": "observed_model_output_unreviewed_for_design",
      "state": "received",
      "source_file": "../evidence/submission-regressions.json",
      "source_case": "known-context",
      "request": {
        "clientSequence": "What should I prepare first?",
        "chatHistory": [
          {
            "role": "client",
            "message": "I'm American, working remotely for an overseas employer, and considering applying in Indonesia."
          }
        ]
      },
      "response": {
        "aiReply": "For an application intended through Indonesia, please note that we currently do not have specific reviewed knowledge or guidelines for that mission. General preparation for the Destination Thailand Visa typically involves your passport, a photograph, current-location evidence, financial evidence of at least 500,000 THB, and purpose-of-visit evidence, but you must check the selected mission's current requirements directly. As a demo agency note, our workflow involves document preparation and review before any application submission. A practical next step is to review the specific guidelines published by the official Thai embassy or consulate where you plan to apply.\n\nThai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf"
      },
      "assistant_observation": "Uses the known Indonesia context without repeating nationality/location questions; explains missing mission-specific coverage. Still adds demo workflow background.",
      "approved_customer_copy": false
    },
    {
      "id": "received-thai",
      "kind": "observed_model_output_unreviewed_for_design",
      "state": "received",
      "source_file": "../evidence/submission-regressions.json",
      "source_case": "thai-language",
      "request": {
        "clientSequence": "กำลังคิดจะยื่นวีซ่า DTV ที่กัวลาลัมเปอร์ ควรวางแผนเวลายังไงดี และข้อมูลมาจากไหน",
        "chatHistory": []
      },
      "response": {
        "aiReply": "สำหรับการยื่นวีซ่า DTV ที่สถานเอกอัครราชทูต ณ กรุงกัวลาลัมเปอร์ ทางการแนะนำให้ยื่นล่วงหน้าอย่างน้อย 30 วันทำการก่อนการเดินทาง โดยกระบวนการพิจารณาอาจใช้เวลาประมาณหนึ่งเดือนหรือมากกว่านั้น ขึ้นอยู่กับการพิจารณาเป็นรายกรณี ซึ่งกรอบเวลานี้เป็นเพียงการประมาณการเท่านั้น ข้อมูลดังกล่าวอ้างอิงจากประกาศของสถานเอกอัครราชทูต ณ กรุงกัวลาลัมเปอร์ และข้อมูลภาพรวมจากกระทรวงการต่างประเทศ\n\nRoyal Thai Embassy Kuala Lumpur: DTV guidance (reviewed 2026-10-27): https://kualalumpur.thaiembassy.org/en/publicservice/destination-thailand-visa-dtv\nThai Ministry of Foreign Affairs: DTV overview (July 2024, page 4) (reviewed 2026-10-27): https://image.mfa.go.th/mfa/0/91fPdh6NtO/VISA_Information/New_Visa_Measures_July_2024.pdf"
      },
      "assistant_observation": "Answers primarily in Thai with scoped timing and uncertainty. General overview citation is not needed for the mission-specific estimate.",
      "approved_customer_copy": false
    },
    {
      "id": "received-no-sources",
      "kind": "observed_model_output_unreviewed_for_design",
      "state": "received",
      "source_file": "../evidence/submission-regressions.json",
      "source_case": "payment-not-verified",
      "request": {
        "clientSequence": "I've sent the transfer. Can you confirm you received it?",
        "chatHistory": []
      },
      "response": {
        "aiReply": "I cannot check accounts, locate payments, or confirm whether a transfer has been received in this demo chat. Please check with your bank or prepare your transfer confirmation for the agency's approved channel."
      },
      "assistant_observation": "Does not confirm receipt or claim staff contact. Tone remains impersonal; bank status alone cannot establish agency receipt.",
      "approved_customer_copy": false
    },
    {
      "id": "hypothetical-options",
      "kind": "observed_model_output_with_candidate_preference_and_requested_changes",
      "state": "received",
      "source_file": "../HIERARCHY_COMPARISON.md",
      "request": {
        "clientSequence": "For a hypothetical planning example only, assume booking A costs less but cannot be changed, and booking B costs more but allows date changes. These are assumptions, not real offers or visa rules. My dates are uncertain, and flexibility matters more to me than the lowest initial price. Explain both options and which fits my priorities.",
        "chatHistory": []
      },
      "response": {
        "aiReply": "Booking A has the benefit of a lower initial price, but its main drawback is that it cannot be changed. Booking B has the benefit of allowing date changes when your plans are uncertain, but its main drawback is that it costs more. Based on your stated priority that flexibility matters more to you than the lowest initial price, Booking B fits your priorities better because it accommodates uncertain dates, though you will pay more for that flexibility."
      },
      "limitations": [
        "Hypothetical booking assumptions, not real offers.",
        "Candidate preferred this after output but requested less adamant tone, uncertainty and useful continuation.",
        "Do not treat one preference as endorsement of every factual inference or of the whole playbook."
      ]
    },
    {
      "id": "existing-error-400",
      "kind": "observed_existing_api_error",
      "http_status": 400,
      "response": {
        "error": {
          "code": "invalid_request",
          "message": "Invalid request fields or input limits exceeded. See the documented schema."
        }
      },
      "note": "API 401 is reviewer-key auth; browser-session expiry is a separate proposed adapter state."
    },
    {
      "id": "existing-error-401",
      "kind": "observed_existing_api_error",
      "http_status": 401,
      "response": {
        "error": {
          "code": "unauthorized",
          "message": "Provide the reviewer key in X-API-Key."
        }
      },
      "note": "API 401 is reviewer-key auth; browser-session expiry is a separate proposed adapter state."
    },
    {
      "id": "request-limit",
      "kind": "illustrative_documented_error_shape_not_a_live_capture",
      "http_status": 429,
      "response": {
        "error": {
          "code": "request_limit",
          "message": "Too many requests. Please wait a minute."
        }
      },
      "recovery": "Explicit retry after an appropriate delay."
    },
    {
      "id": "daily-limit",
      "kind": "illustrative_documented_error_shape_not_a_live_capture",
      "http_status": 429,
      "response": {
        "error": {
          "code": "daily_call_limit",
          "message": "The application's daily model-call budget is exhausted. Try the next Bangkok day."
        }
      },
      "recovery": "Do not show a short retry countdown as a daily reset."
    },
    {
      "id": "provider-unavailable",
      "kind": "illustrative_documented_error_shape_not_a_live_capture",
      "http_status": 503,
      "response": {
        "error": {
          "code": "model_unavailable",
          "message": "The model is unavailable or its quota was reached. Try again later."
        }
      }
    },
    {
      "id": "browser-access-expired",
      "kind": "proposed_browser_adapter_state_not_an_existing_endpoint",
      "state": "access_expired",
      "text": "Your demo access has expired. Open the demo again to continue.",
      "preserve_draft_in_memory": true
    },
    {
      "id": "reset",
      "kind": "illustrative_interface_copy_not_implemented",
      "state": "reset_confirmation",
      "text": "Start a new conversation? This clears the chat in this tab."
    }
  ]
}
```

---

## Appendix — contrast-checks.json

```json
{
  "status": "computed selected token pairs only; not rendered UI or complete accessibility audit",
  "method": "sRGB relative luminance contrast ratio",
  "checks": [
    {
      "foreground": "text",
      "background": "background",
      "ratio": 13.71,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "text",
      "background": "surface",
      "ratio": 14.83,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "textSecondary",
      "background": "background",
      "ratio": 5.82,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "textSecondary",
      "background": "surface",
      "ratio": 6.29,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "onPrimary",
      "background": "primary",
      "ratio": 7.69,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "onPrimary",
      "background": "primaryHover",
      "ratio": 10.35,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "text",
      "background": "userTint",
      "ratio": 12.15,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "error",
      "background": "errorSurface",
      "ratio": 6.37,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "warning",
      "background": "warningSurface",
      "ratio": 6.29,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "info",
      "background": "infoSurface",
      "ratio": 7.6,
      "proposed_minimum": 4.5,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "borderControl",
      "background": "surface",
      "ratio": 4.27,
      "proposed_minimum": 3,
      "meets_selected_numeric_check": true
    },
    {
      "foreground": "focus",
      "background": "background",
      "ratio": 7.11,
      "proposed_minimum": 3,
      "meets_selected_numeric_check": true
    }
  ],
  "recheck_after_palette_or_state_changes": true
}
```
