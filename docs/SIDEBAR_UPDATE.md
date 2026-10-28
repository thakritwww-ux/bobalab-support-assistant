# Saved-conversation sidebar

Fill asked to display saved conversations in the left sidebar like his supplied
navigation screenshot, then refine the answer hierarchy separately. The assistant
implemented the navigation and tests; detailed visual choices are not candidate code.

On desktop, the BOBALAB panel now shows New conversation, search, saved threads,
active-thread highlighting, concise dates/reply counts, rename/delete controls and
on-device storage status/settings. It replaces decorative content. Full titles
remain accessible; long visual titles are clamped. The management panel retains
full dates, export and storage controls. On narrow screens, Conversations opens a
left drawer with native dialog keyboard/focus behavior.

Both views use the same IndexedDB records. No migration, cloud sync, account feature,
model call on opening/searching or new conversation database was introduced. Existing
saved threads remain available. Private demo access and the API contracts are unchanged.

Switching protects unsaved drafts and unsaved replies after failed writes. Renaming
a stale thread does not advance its local revision if another tab has different
messages, preventing a later save from overwriting that tab's content.

The sidebar suite checks 12 navigation/storage/accessibility behaviors with local
synthetic replies. Its first audit found insufficient contrast in active-row small
text; the active background was darkened. The corrected metadata contrast is about
5.02:1, and the final desktop/mobile axe audits have no automated violations.
Existing history and backend regression results are recorded alongside deployment
verification when complete. This is not full accessibility certification.


Deployment d5344b3 is verified on the existing Render Free origin. Real assets, demo
login and IndexedDB persistence were exercised; the reply was an explicitly
intercepted local fixture, with zero model calls. Reopen from the sidebar, active
state, rename/search and the mobile left drawer/Escape passed. See
[evidence/sidebar-hosted-checks.json](evidence/sidebar-hosted-checks.json).
89 backend and the existing 22 history browser checks also passed.
