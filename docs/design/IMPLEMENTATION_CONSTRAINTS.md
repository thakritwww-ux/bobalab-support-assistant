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
