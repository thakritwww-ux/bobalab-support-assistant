# Before-and-after evidence: not collected yet

No real Gemini baseline or improvement results have been collected. This file is
an honest status record, not a completed submission deliverable. Unit tests use
scripted responses and must not be copied here as real model evidence.

After local credentials are configured:

```sh
python -m app.cli check-live
python -m scripts.evaluate capture --output docs/evidence/before.local.json
python -m scripts.replay --limit 8
python -m scripts.evaluate capture --output docs/evidence/after.local.json
python -m scripts.evaluate compare docs/evidence/before.local.json docs/evidence/after.local.json
```

The final command replaces this file with actual replies and the prompt diff.
Fill must add his verdicts, including regressions or inconclusive outcomes.
Keep the knowledge snapshot fixed when assessing behavioral learning. A factual
source correction is not proof of the automatic-learning mechanism.

Also demonstrate a useful manual edit and an appropriately rejected lesson. If
the model makes no useful automatic changes, record that honestly and investigate;
do not weaken the initial prompt or fabricate successful learning.

Local evidence files are ignored by Git so they can be reviewed before deliberate
publication. Commit only the selected sanitized results needed for the assessment.
