# BOBALAB — demo access entry refinements

Status: design proposal; browser authentication is not implemented.

- Use the BOBALAB wordmark and "Visa support demo" subtitle, a short scope note,
  a labeled demo-code input, Show/hide control and "Open demo" action.
- The demo code must be separate from provider, database and privileged reviewer
  credentials. Never ask the user to paste those into the browser.
- Use native form controls; show an associated inline error when a code is rejected.
- Access-expiry recovery should preserve the unsent draft in memory while the tab
  stays open. Do not promise saved conversations or cross-device continuation.
- Keep the form compact and mobile friendly; no intake questionnaire, identity
  upload, account creation, sales funnel or fake official-agency branding.
- The future backend must rate-limit access attempts, create a suitable session,
  enforce generation-only permissions and preserve existing API-key protection.

This page file only refines presentation. It is not a configured access code,
implemented route or permission to bypass the API authentication gate.
