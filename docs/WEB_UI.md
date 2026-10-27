# BOBALAB browser interface

Implemented 28 October 2026 following Fill's instruction to design/build the website.
Live target: https://bobalab-support-assistant.onrender.com . Deployment verification
is recorded below when completed; local verification alone is not evidence of deployment.

## Design and journey

BOBALAB is the visible name. Deep green, warm neutral surfaces, a quiet desktop
sidebar and a compact mobile header support one readable conversation column.
The wordmark is a typographic demo treatment, not an official agency logo.
Self-hosted IBM Plex Sans and Thai Looped provide English/Thai text; Lucide icons
and full notices are included. No font CDN, tracking or separate frontend host.

Open site → enter private demo code → choose a starter or type a question → read
reply and any cited source → continue, copy reply, start fresh or lock access.
Starters fill the draft without sending or spending a model call. Only one send
runs at a time. Enter sends; Shift+Enter adds a line. About explains limits.

The UI shows the model's actual wording as inert text. It does not insert a
fabricated decision hierarchy, options or citations. Exact known source footers
can display as source links with scope/review dates; copy and subsequent history
retain the complete original aiReply. Unknown footers remain as text.

## Access and integration

The three assessment API contracts and X-API-Key protection are unchanged.
The browser never receives that key. Same-origin routes:

- GET /: public HTML; assets and /health are public.
- GET /ui/session: availability/authentication/CSRF bootstrap; no model call.
- POST /ui/session: accessCode plus X-CSRF-Token; grants generation-only access.
- POST /ui/chat: original clientSequence/chatHistory shape, session and CSRF required;
  returns aiReply plus messageText and source metadata for display.
- POST /ui/logout: clears current browser grant, with CSRF protection.

Cookies are signed, HttpOnly, SameSite=Strict, with an absolute 30-minute grant.
They contain a timestamp/CSRF token, not conversations or privileged credentials.
Render enables Secure cookies and recognition of its forwarded HTTPS scheme. Its [documented RENDER variable](https://render.com/docs/environment-variables) identifies that environment.
Logout clears this browser's cookie; it does not revoke a copied cookie elsewhere.
This is a limited shared-code demo, without individual user accounts.

By default, two different HMAC-SHA256 domains derive a demo code (80 bits) and a
signing secret from the server-only reviewer key. They cannot be used to authorize
the three API endpoints. Reviewer-key rotation also changes these defaults.
Optional UI_DEMO_ACCESS_CODE (8–128 characters, never the reviewer key) and
UI_SESSION_SECRET (32+ characters) decouple rotation. Leave blank for defaults.
For other HTTPS hosting set UI_SECURE_COOKIE=true; Render handles this automatically.

Run `python -m app.cli write-web-access` in the configured project. It writes
work/WEB_DEMO_ACCESS.txt with mode 0600, prints only its path, and never writes a
provider/database/reviewer key. Share the limited demo code privately with reviewers.
Never include the private file in GitHub, screenshots or public design exports.

Login attempts are globally limited to five/minute per process. UI sends share the
API's ten requests/minute throttle and durable daily model-attempt budget (100).
The supported deployment uses one Gunicorn worker; this is not a distributed
per-user throttle. Failed/in-flight requests may still consume provider allowance.

## Privacy, recovery and scope

Successful thread history lives in this tab's memory and is sent with each follow-up.
No localStorage, saved-thread database, file upload, analytics or automatic learning
from chat. Refresh closes the local history. Server/provider handling still applies:
messages are sent to Gemini; use synthetic information only.

Input/context limits are checked before sending, with server validation retained.
Errors retain the unsent draft and provide an explicit retry. Expired access permits
re-entry without clearing the current tab's memory. Reset/lock confirmation warns
that cancelling the browser wait cannot undo a server call. Late replies from a
cleared conversation are discarded. No fake streaming or completed operational acts.
No payment checks, document inspection, team messages, booking or application submission.

## Verification

- 89 pytest cases passed with temporary PostgreSQL, including shared throttling,
  sessions/CSRF/origin, expiry, separate privileges, source metadata and proxy HTTPS.
- Chrome browser interactions: 15 checks, seven simulated generation requests;
  no JavaScript errors. Tested draft preservation, retry, history, unsafe HTML,
  reset, stale responses, Thai layout and re-entry.
- Axe WCAG 2A/2AA/2.1AA/2.2AA audits: no automated violations in desktop access,
  mobile active chat and mobile About. This is limited automated coverage, not
  certification or a substitute for assistive-technology/device testing.
- Desktop/mobile screenshots inspected; Thai fonts loaded and no horizontal overflow
  at 390px. Fixture replies were marked illustrative, not live quality evidence.
- No model instruction or reviewed fact was changed by this UI implementation.

Two actual local browser generations passed against Gemini/Supabase with synthetic
input. The follow-up correctly recalled Indonesian nationality and Kuala Lumpur.
The first answer introduced irrelevant agency-workflow information, and recall added
an unnecessary citation. These limitations are preserved in
[evidence/web-local-live.json](evidence/web-local-live.json). Local HTTP correctly
uses a non-Secure cookie; deployed HTTPS must verify Secure separately.
Deployment evidence is recorded after the hosted smoke check.
