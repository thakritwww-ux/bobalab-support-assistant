To: bobalabth@gmail.com
Subject: BOBALAB Technical Assessment — Thakrit Wongwiwatseree

Hi JJ,

Please find my completed BOBALAB technical assessment below. The project includes
the three required API workflows and an optional browser chat interface.

1. Repository and deployed application

GitHub repository: https://github.com/thakritwww-ux/bobalab-support-assistant
Website and server: https://bobalab-support-assistant.onrender.com
Submission index: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/SUBMISSION.md

The assistant generates replies from customer messages and history, retrieves its
active prompt from Supabase, and supports automatic and manual prompt updates.
Self-learning here means updating stored instructions, not training model weights.
The browser also offers opt-in conversation history on the same device.

2. README and setup documentation

https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/README.md

The README covers dependencies, local setup, environment configuration, system
structure, database prompt storage, improvement behavior, rollback and limits.
The repository includes placeholder-only .env.example and final application prompts.

3. Example cURL commands for all three endpoints

The commands contain an application-access placeholder, not an actual credential.
The access handoff must be arranged separately; provider/database credentials are
never needed by reviewers.

Set the service URL and separately supplied application access:

```sh
export BASE_URL='https://bobalab-support-assistant.onrender.com'
export REVIEWER_API_KEY='replace-with-the-privately-provided-reviewer-key'
```

Generate a reply:

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/generate-reply" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"How long should I book accommodation? I need to keep costs down.","chatHistory":[{"role":"client","message":"I am planning a DTV application in Kuala Lumpur."}]}'
```

Improve from a consultant example:

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"What do you mean by proof of funds?","chatHistory":[],"consultantReply":"That means evidence of money available to support your stay. I should explain an unfamiliar term in plain language before moving on."}'
```

Improve manually:

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai-manually" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"instructions":"Add this formatting rule verbatim if it is not already present: Use short bullet lists for multi-step preparation instructions, preserving essential qualifications and a clear next step."}'
```

Expected response fields:

- POST /generate-reply: aiReply, a string.
- POST /improve-ai: predictedReply and updatedPrompt, both strings, plus version/status metadata.
- POST /improve-ai-manually: updatedPrompt, a string, plus version/status metadata.

Learning status can be applied, no_change or rejected. The improvement requests
can change the shared playbook; a successful save does not guarantee a better reply.
Full request/response examples: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/submission/CURL_EXAMPLES.md

4. Before-and-after improvement examples

https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/submission/BEFORE_AFTER_HIGHLIGHTS.md

The examples include original replies, exact prompt changes, resulting replies and
assessments. One hierarchy trial moved from recommending first to describing the
options and tradeoffs before making a recommendation. I preferred that order but
asked for a less adamant tone, more uncertainty and room to correct assumptions.
Other results were mixed, so unsuccessful experimental rules were restored and
retained in the evidence. No general quality gain is claimed.

The later structured-answer design is documented separately from prompt learning:
https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/STRUCTURED_ANSWER_RESULTS.md

5. Personal contribution summary

https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/submission/CONTRIBUTION_SUMMARY.md

My contribution was defining concern-first support, practical options and tradeoffs,
conditional recommendations and honest uncertainty. I selected which behavior the
assistant could learn automatically and kept factual changes subject to separate
review. I proposed the answer hierarchy, reviewed two comparison pairs, supplied
and revised payment-response wording, requested customer-facing saved conversations,
and questioned whether excessive formatting made simple answers harder to read.

AI generated the implementation and ran the checks. My decisions and feedback are
distinguished from the assistant's code, exact prompts and preliminary assessments.
No independent coding or numerical evaluation scores are claimed on my behalf.

6. AI usage, prompts and verification

AI usage log: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/AI_USAGE.md
Active prompt snapshot: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/evidence/prompt-snapshot.json
Editor prompt: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/prompts/editor.md
Current answer-layout instruction: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/answer-format-instruction.txt
Verification record: https://github.com/thakritwww-ux/bobalab-support-assistant/blob/main/docs/VERIFICATION.md

The log covers Codex/ChatGPT assistance and Gemini, key prompts and follow-ups,
relevant AI responses, decisions, rejected suggestions and tests. The project was
opened/configured in Cursor; no separate Cursor AI coding session is claimed.
Recorded checks include 117 backend tests, 13 structured-answer browser checks and
successful real hosted calls to all three required endpoints. A clean public
checkout passed the backend suite using the existing development environment.

Known limitations include repetitive/formal wording, uneven citation relevance,
unverified booking-term generalizations, limited source coverage and free-tier
interruptions. There are no payment confirmation, attachment inspection, booking
or team-notification integrations. Further personal source/output review and the
proposed final brevity refinement remain unfinished and are disclosed.

Reviewer access

Both the repository and website are publicly reachable. Chat generation requires
a limited demo code, and the API requires a separate application-access key.
No API keys, credentials or unrelated private information are included in this
email, public repository or submission packet.

[BEFORE SENDING: replace this line with the agreed separate private access-handoff
instructions so reviewers can obtain both limited access values. Do not paste
credentials into this email or attach .env/private access files.]

The optional BOBALAB-Submission-Packet.zip attachment contains the source,
documentation and evidence together. All materials are also linked above.

Thank you for reviewing my work.

Thakrit Wongwiwatseree (Fill)
