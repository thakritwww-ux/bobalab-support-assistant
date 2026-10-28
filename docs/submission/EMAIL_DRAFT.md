To: bobalabth@gmail.com
Subject: BOBALAB Technical Assessment — Thakrit Wongwiwatseree

Hi JJ,

Please find my BOBALAB technical assessment below.

Repository: https://github.com/thakritwww-ux/bobalab-support-assistant
Website and API: https://bobalab-support-assistant.onrender.com
README: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/README.md
Submission index: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/SUBMISSION.md

The assistant generates replies from customer messages and history, retrieves its
active prompt from Supabase, and supports automatic and manual prompt updates.
The optional browser demo includes saved conversations on the same device.

My contribution was defining concern-first support, uncertainty and capability
boundaries, and a hierarchy that explains options and tradeoffs before making a
conditional recommendation. I reviewed selected replies and challenged overly
adamant wording and overstructured answers. AI generated the implementation and
ran the checks; the contribution summary and AI log distinguish that work from my
decisions and feedback.

Before/after examples and assessments:
https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/submission/BEFORE_AFTER_HIGHLIGHTS.md
Contribution summary:
https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/submission/CONTRIBUTION_SUMMARY.md
AI tools, key prompts, follow-ups and relevant responses:
https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/AI_USAGE.md

The current public checkout passed 117 tests using disposable PostgreSQL and an
existing development environment. There are also 13 structured-answer browser
checks and recorded successful live calls to all three required endpoints.
Results are mixed: some changes helped specific answers, while others were rolled
back. The model still produces repetitive or overly formal replies and can use
weakly relevant citations. Free hosting can sleep and provider calls can fail.
This updates stored prompts; it does not train model weights.

Reviewer access: the site uses a limited demo code, and the API uses a separate
application-access key. Credentials are excluded from this email and the public
materials. [BEFORE SENDING: replace this sentence with the agreed separate private
access-handoff instructions; reviewers must be able to obtain both access values.]

Example cURL commands (replace the application-key placeholder using that separate
handoff; provider/database credentials are never needed):

```sh
export BASE_URL='https://bobalab-support-assistant.onrender.com'
export REVIEWER_API_KEY='replace-with-the-privately-provided-reviewer-key'
```

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/generate-reply" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"How long should I book accommodation? I need to keep costs down.","chatHistory":[{"role":"client","message":"I am planning a DTV application in Kuala Lumpur."}]}'
```

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"What do you mean by proof of funds?","chatHistory":[],"consultantReply":"That means evidence of money available to support your stay. I should explain an unfamiliar term in plain language before moving on."}'
```

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai-manually" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"instructions":"Add this formatting rule verbatim if it is not already present: Use short bullet lists for multi-step preparation instructions, preserving essential qualifications and a clear next step."}'
```

Expected response fields:

- /generate-reply: aiReply (string).
- /improve-ai: predictedReply and updatedPrompt (strings), plus version/status metadata.
- /improve-ai-manually: updatedPrompt (string), plus version/status metadata.

Learning status can be applied, no_change or rejected. Improvement examples can
change the shared playbook; a saved change does not guarantee better responses.

The attached credential-free packet brings these materials together. Further
candidate source review and brevity refinement are listed as unfinished.

Thank you for reviewing my work.

Thakrit Wongwiwatseree (Fill)
