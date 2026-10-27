# UI UX Pro Max raw reference — not the adopted design system

This is local search/generation output retained for provenance. Its automatic
performance/accessibility labels are not measured evidence. Its landing structure,
streaming suggestions, palette and typography have not been adopted. Read
UI_UX_PRO_MAX_USAGE.md and the reviewed master before using it.

Query: customer support chatbot conversational interface minimal calm accessible multilingual Thai English

---

## Design System: BOBALAB

### Pattern
- **Name:** FAQ/Documentation Landing
- **Conversion Focus:** Reduce support tickets. Track search analytics. Show related articles. Contact escalation path.
- **CTA Placement:** Search bar prominent + Contact CTA for unresolved questions
- **Color Strategy:** Clean, high readability. Minimal color. Category icons in brand color. Success green for resolved.
- **Sections:** 1. Hero with search bar, 2. Popular categories, 3. FAQ accordion, 4. Contact/support CTA

### Style
- **Name:** AI-Native UI
- **Keywords:** Chatbot, conversational, voice, assistant, agentic, ambient, minimal chrome, streaming text, AI interactions
- **Best For:** AI products, chatbots, voice assistants, copilots, AI-powered tools, conversational interfaces
- **Performance:** ⚡ Excellent | **Accessibility:** ✓ WCAG AA

### Colors
| Role | Hex |
|------|-----|
| Primary | #7C3AED |
| Secondary | #A78BFA |
| CTA | #06B6D4 |
| Background | #FAF5FF |
| Text | #1E1B4B |

*Notes: AI purple + cyan interactions*

### Typography
- **Heading:** Noto Sans Thai
- **Body:** Noto Sans Thai
- **Mood:** thai, modern, readable, clean, multilingual, accessible
- **Best For:** Thai sites, Southeast Asia, tourism, Thai restaurants
- **Google Fonts:** https://fonts.google.com/share?selection.family=Noto+Sans+Thai:wght@300;400;500;700
- **CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;700&display=swap');
```

### Key Effects
Typing indicators (3-dot pulse), streaming text animations, pulse animations, context cards, smooth reveals

### Avoid (Anti-patterns)
- Heavy chrome
- Slow response feedback

### Pre-Delivery Checklist
- [ ] No emojis as icons (use SVG: Heroicons/Lucide)
- [ ] cursor-pointer on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
