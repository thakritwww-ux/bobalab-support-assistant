# BOBALAB interface design handoff

Prepared 28 October 2026 as a design handoff. **The first browser interface is now implemented following Fill’s subsequent instruction to build it.** See [WEB_UI.md](../WEB_UI.md) for actual architecture, access and verification. The packet below preserves the original design-stage proposals; future-tense gaps describe that earlier stage.

## Give these to the specialist LLM

1. Upload **HANDOFF_BUNDLE.md**, the self-contained brief with requirements,
   visual identity, screen layouts, customer journey, integration constraints,
   acceptance checklist, proposed tokens and labeled UI fixtures.
2. Paste **DESIGNER_PROMPT.md** as the instruction.
3. If the specialist needs separate files, use the directory contents below.

| File | Purpose |
|---|---|
| [DESIGN_HANDOFF.md](DESIGN_HANDOFF.md) | Product requirements, UI, CI, style, fonts, features and journey |
| [IMPLEMENTATION_CONSTRAINTS.md](IMPLEMENTATION_CONSTRAINTS.md) | Actual API contract, current authentication gap, future browser adapter and state handling |
| [REQUIREMENTS_CHECKLIST.md](REQUIREMENTS_CHECKLIST.md) | Prioritized, testable requirements and design/implementation acceptance gates |
| [DESIGNER_PROMPT.md](DESIGNER_PROMPT.md) | Copyable specialist-LLM instruction |
| [design-tokens.json](design-tokens.json) | Proposed visual tokens; not an approved or deployed brand system |
| [font-manifest.json](font-manifest.json) | Proposed families, weights, official source/license and asset status |
| [api-contract.json](api-contract.json) | Actual request schemas, response fields and service limits |
| [fixtures.json](fixtures.json) | Labeled actual model examples and illustrative interface states |
| [contrast-checks.json](contrast-checks.json) | Computed checks on selected proposed colour pairs; not a WCAG audit |
| [UI_UX_PRO_MAX_USAGE.md](UI_UX_PRO_MAX_USAGE.md) | Skill invocation, reviewed adoption/rejection decisions and provenance |
| [Reviewed design master](../../design-system/bobalab/MASTER.md) | BOBALAB-specific starting proposal plus chat/access page refinements |
| [ui-ux-pro-max-review.json](ui-ux-pro-max-review.json) | Actual search findings and measured contrast check on the raw CTA suggestion |

The repository includes the user-provided skill at .codex/skills/ui-ux-pro-max/.
Use the usage guide rather than assuming a separate hosted LLM or menu integration.
The expanded ZIP includes the skill, its license notice and the reviewed master.

## Confirmed decisions

- Website name: **BOBALAB**. Do not invent a different product or assistant name.
- CI means **visual brand identity**, not continuous integration.
- Fill now wants a browser interface; the prior API-only scope has been expanded.
- The original task prepared materials for a specialist. Fill subsequently authorized this assistant to implement the design using the supplied skill.
- Keep the three assessment API endpoints, free-service constraint, source and
  capability boundaries, and honest contribution/evidence records.
- Customer experience: concern first; understandable choices and tradeoffs;
  conditional recommendations; uncertainty; useful continuation and room to correct
  material assumptions. Do not force every reply into a decision template.

## Proposed, not yet approved

The palette, IBM Plex font pairing, wordmark treatment, layouts and browser access
flow are assistant proposals. No official BOBALAB brand manual/logo asset was
provided. The specialist may refine the visual proposal while keeping the BOBALAB
name and functional requirements. Do not present this as the lab's official CI.

The recommended first release is one responsive chat experience plus an About
panel. A reviewer prompt-editing dashboard is optional and outside that release.
No keys, .env contents, production access codes or unrelated private handoffs are
included in this packet. Do not upload those to the specialist LLM.
