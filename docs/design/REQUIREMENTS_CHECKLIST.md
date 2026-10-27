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
