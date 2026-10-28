# BOBALAB design system — reviewed starting proposal

Prepared 28 October 2026 as the reviewed starting proposal. The first website now uses this direction; see docs/WEB_UI.md for actual implementation and tests. It is not official BOBALAB CI or candidate acceptance of final visuals.

## Authority and use

1. The user's BOBALAB name, scope, budget and product decisions are fixed constraints.
2. Actual backend behavior and [implementation constraints](../../docs/design/IMPLEMENTATION_CONSTRAINTS.md)
   determine which interactions are real.
3. This reviewed master and [design tokens](../../docs/design/design-tokens.json)
   are the current visual starting proposal.
4. Page files may refine local layout/interaction details. They cannot override
   naming, capabilities, source honesty, privacy or authentication requirements.

The specialist may propose visual refinements with a reason. Do not automatically
replace this file with generic search output. Record what was changed and why.

## Identity

Use **BOBALAB**, with an explanatory "Visa support demo" subtitle if useful.
Use a typographic wordmark initially. No unrelated product/bot name, fabricated
official logo, embassy seal, government affiliation or approval emblem.

## Experience and layout

Use a responsive conversational interface with minimal chrome: demo access entry,
one chat screen, an About panel and honest failure/recovery states. A central
680–760 px reading column and restrained user bubbles keep the answer easy to read.
No marketing hero, FAQ-first landing funnel, pricing section or analytics dashboard.

Show the actual answer faithfully. Accommodate conditional options and a helpful
continuation when present, without constructing missing advice or hiding caveats.
Keep sources labeled "Sources mentioned". Do not treat a trusted URL as an answer
verification badge. No operational case-progress indicator.

## Palette and fonts

Retain the existing proposed palette while specialist review is pending:

| Role | Value |
|---|---|
| Canvas / surface | #F7F6F2 / #FFFFFF |
| Main / secondary text | #182B29 / #51645F |
| Primary / primary text | #1D5D4F / #FFFFFF |
| User tint | #DDECE6 |
| Essential control border | #6B7F76 |
| Decorative separator | #D7E1DC |
| Error / notice text | #A32935 / #795300 |

IBM Plex Sans for Latin and IBM Plex Sans Thai Looped for Thai remain proposed.
Use weights 400/500/600, 17 px conversation text, comfortable line height and
readable metadata. Six normal WOFF2 faces are now self-hosted; follow the
[font manifest](../../docs/design/font-manifest.json) and retain upstream notices.

Do not silently adopt the tool's purple/cyan palette or Noto alternative. Those are
unreviewed alternatives, not the user's choices. Recheck actual state contrasts
after any visual revision. The tool's accessibility labels are not compliance tests.

## Components and interactions

- Native buttons, links and labeled inputs; avoid copying generic clickable-div examples.
- Clear keyboard focus and error text associated with the affected field.
- One pending request, disabled duplicate Send and a preserved draft on failure.
- Honest indeterminate loading; no simulated streaming or made-up completion time.
- Concise recovery action appropriate to rate, daily allowance, access or provider error.
- Reset confirmation on an existing conversation; reject stale replies after reset.
- No forced scroll to the bottom while a person is reading earlier text. Offer a
  nonintrusive jump to a newly arrived reply when appropriate.
- Functional short transitions and reduced-motion support; no distracting pulses.
- Consistent SVG icons with labels where needed; no emoji interface icons.

## Hard boundaries

No file inspection, payment confirmation, booking, application submission, legal-team
notification or real-time escalation. Fill subsequently approved optional device-local conversation history; see docs/CUSTOMER_EXPERIENCE.md. No model calls while typing
or on page load. No paid fallback. No provider, DB or reviewer key in the browser.
The generation-only browser session adapter is implemented and verified. Preserve all three current API contracts.

## Pages and verification

- [Chat page](pages/chat.md)
- [Access entry](pages/access.md)
- [Full requirement checklist](../../docs/design/REQUIREMENTS_CHECKLIST.md)
- [Tool use and review rationale](../../docs/design/UI_UX_PRO_MAX_USAGE.md)

No UI test, native-language review or full accessibility audit has been completed
by writing this master. Existing backend tests remain a separate evidence set.
