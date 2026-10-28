# BOBALAB — chat page refinements

Status: design proposal; use with ../MASTER.md and the confirmed product constraints.

- Header: BOBALAB, concise demo subtitle, About and New chat. A Conversations panel now provides explicitly approved optional device-local history.
- Empty state: a short invitation and optional starters that fill the composer.
- Active state: restrained user bubble, flat assistant text, relevant source links
  when provided, and a persistent usable composer.
- Keep the real reply intact. Do not split it into fictional decision/source fields.
- Use an inline pending indicator and a slow-service explanation, not fake word streaming.
- Put errors near the composer/failed message and pair them with a recovery action.
  Do not repeatedly steal focus when a background status changes.
- Keep draft/history state separate from an unresolved request. Retry is explicit;
  do not duplicate a pending message or insert stale responses after reset.
- Test 360/390 px mobile, 768 px tablet and 1280/1440 px desktop, including the
  mobile keyboard, Thai combining marks, long replies and long source URLs.
- When the reader has scrolled upward, do not yank their reading position to a new
  reply. A "New reply" jump control can appear only after a reply actually arrives.
- Recommended body 17 px, spacious line height, no tiny citation captions and comparison tables contained in focusable horizontal-scroll regions on narrow screens.

All palette/font values remain in the reviewed master/tokens. These refinements
cannot grant new backend capabilities or expose prompt-editing controls to chat users.
