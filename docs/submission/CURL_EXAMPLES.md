# Three required cURL examples

In a second terminal, activate the environment and set these **application** values:

```sh
export BASE_URL='https://bobalab-support-assistant.onrender.com'
export REVIEWER_API_KEY='replace-with-the-privately-provided-reviewer-key'
```

For local testing use `BASE_URL='http://127.0.0.1:8000'`. Provider and
database credentials are never needed by reviewers. Keep credentials out of the repository, submission email and attachments. Arrange
the limited application-access handoff separately through an agreed private channel.

**1. Generate**

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/generate-reply" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"How long should I book accommodation? I need to keep costs down.","chatHistory":[{"role":"client","message":"I am planning a DTV application in Kuala Lumpur."}]}'
```

Response shape: `{"aiReply":"Generated customer reply, with reviewed source links when used."}`.
This is a shape illustration, not an observed live result. For this case, assess
whether the reply explains uncertainty and booking tradeoffs rather than promising
a two-week completion date.

**2. Improve from a consultant example**

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"clientSequence":"What do you mean by proof of funds?","chatHistory":[],"consultantReply":"That means evidence of money available to support your stay. I should explain an unfamiliar term in plain language before moving on."}'
```

Response contains `predictedReply`, `updatedPrompt`, `versionId`, `learningStatus`,
`appliedEdits`, and `rejectedLearnings`. The status is `applied`, `no_change`, or
`rejected`. The example does not guarantee an edit: the starting prompt may already
cover the lesson. Actual learning is documented from real outputs, not assumed.

To exercise rejection, supply a consultant reply claiming a payment is verified
because the customer says so, or coaching concealment of a relevant client. A
correct editor should reject that lesson; useful unrelated style edits may still
be accepted. Rejection by itself does not satisfy the successful-learning requirement.

**3. Improve manually**

```sh
curl --fail-with-body --max-time 150 "$BASE_URL/improve-ai-manually" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $REVIEWER_API_KEY" \
  --data '{"instructions":"Add this formatting rule verbatim if it is not already present: Use short bullet lists for multi-step preparation instructions, preserving essential qualifications and a clear next step."}'
```

Response contains `updatedPrompt` and the same version/status metadata. Generate
the same question again to assess the effect. Manual instructions cannot introduce
unreviewed facts or override capability limits.

`GET /health` is public **liveness only**. It does not assert model/database readiness.
All model-backed routes require `X-API-Key`. History is oldest to newest; join
consecutive customer messages with newlines in the string `clientSequence`.


## Illustrative response shapes

These show types, not promised model wording or evidence of a new test.

```json
{"aiReply":"Customer-facing answer, with source links when selected."}
```

```json
{"predictedReply":"Answer before the edit","updatedPrompt":"Rendered active prompt","versionId":"UUID","learningStatus":"applied","appliedEdits":[{"action":"replace","rule_id":"tone","category":"style"}],"rejectedLearnings":[]}
```

```json
{"updatedPrompt":"Rendered active prompt","versionId":"UUID","learningStatus":"no_change","appliedEdits":[],"rejectedLearnings":[]}
```

`learningStatus` may be applied, no_change or rejected. Arrays and status above are
shape illustrations; no particular edit outcome is guaranteed. An HTTP 200 edit
response does not establish an answer-quality gain. Both improvement commands can
change the shared playbook. Use synthetic inputs and compare version IDs/results.

The exact README examples passed earlier hosted cURL checks. All three routes also
passed the latest structured-generation hosted checks using the requests recorded
in [the raw trial](../evidence/structured-answers.json). Packaging made no new model
calls. Public liveness: `curl --max-time 120 "$BASE_URL/health"`.
