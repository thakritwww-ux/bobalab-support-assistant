# Prompt to give the specialist design LLM

You are designing a responsive browser interface for **BOBALAB**. The website name
must stay BOBALAB. Do not invent another product name, anonymous brand or named bot.
Read the attached HANDOFF_BUNDLE.md before proposing the design. CI means visual
brand identity, not continuous integration.

The backend already exists: a Flask customer-support API with Supabase prompt
versions and Gemini generation, deployed on a free service. This task is the
interface/identity design and its implementation handoff. Do not redesign the
learning backend, switch model/provider, change prompts or claim new integrations.

The user wants concern-first support, understandable information, useful sources,
options with benefits/drawbacks, a conditional recommendation when priorities are
clear, explicit uncertainty and a practical continuation or room for correction.
Do not force a question or comparison into every answer. The assistant is an AI
assessment demo, not a human consultant or an official immigration agency.

Deliver a design-ready proposal for one customer chat experience plus an About
panel and demo-access entry. Include desktop/mobile variants, component states,
visual identity, colour/style/font specifications and the customer journey. Treat
palette/font/layout suggestions in the packet as a starting proposal; preserve the
confirmed BOBALAB name and hard functional constraints. State which parts you keep
or change and why. No official BOBALAB logo/manual was supplied: do not invent one
and label it official. A typographic BOBALAB wordmark is acceptable.

Required output:

1. Concise design direction linked to the customer's needs.
2. BOBALAB CI proposal: wordmark treatment, palette, typography and usage rules.
3. Screen map and customer journey, including failure/recovery paths.
4. Desktop and mobile layouts for access, empty chat, active chat, About and reset.
5. Variants for pending, slow, no sources, long/Thai reply, access error, input/history
   limits, network/provider failure, short-term rate limit and daily allowance.
6. Component specification with focus/hover/disabled/error states, spacing, tokens,
   responsive behavior and English/Thai font handling.
7. Interaction/accessibility notes and a testable implementation handoff.
8. Prioritized build plan with dependencies and unresolved decisions.

Hard constraints:

- Preserve the three required JSON APIs. Customer chat only needs generation;
  prompt editing belongs to a separate optional privileged workspace.
- Current generation returns an aiReply string, not structured cards or a stream.
  Do not fabricate options, recommendations, source validation or application progress.
- Preserve actual model caveats. A polished mockup is not proof of a better answer.
- Sources can be imperfectly relevant. Say "Sources mentioned", not "Verified answer".
- No uploads, payment checks, bookings, submissions, legal-team notifications or
  follow-up promises. No approval rates, visa guarantees or government affiliation.
- No saved-conversation sidebar unless persistence is separately implemented.
- Never expose provider/DB/reviewer/session keys in browser assets. An unprotected
  proxy is insufficient. The proposed same-origin session adapter is not implemented.
- Existing Flask authentication blocks non-health requests today, including a new
  homepage/static path unless specifically addressed. Do not disable the key gate.
- Keep model calls off page load/typing; one pending send at a time; preserve draft
  on failure. No automatic retry loop or paid fallback. Free hosting may be slow.
- Keep scope small and strictly free. No marketing homepage, extra account system,
  unrelated dashboard, stock-photo hero or decorative feature bloat.
- Use licensed fonts/assets; respect Thai rendering, keyboard navigation and contrast.
- The user approved the hierarchy concept and gave two preferences on earlier
  replies. Detailed CI proposals and other quality judgments are not user decisions.

Use the labeled fixtures to show layouts. Keep observed model output separate from
illustrative interface copy. Do not represent mocks as tested live functionality.
If you supply images, identify screens/states/viewports clearly. If you supply code,
keep it a clearly labeled prototype until backend integration and tests exist, and
document exactly what is mocked. No production deployment or account actions.

Return the design and handoff now; ask only questions that genuinely block progress.
Do not send messages, publish externally or alter the deployed service.
