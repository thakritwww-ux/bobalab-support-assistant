# Free account setup

You do the account sign-ins. The assistant can continue building and testing locally
while you complete these steps. Do not put passwords or API keys in chat.

## 1. Gemini: the model

1. Open https://aistudio.google.com/ and sign in with Google.
2. Create an API key for a free project. Do not enable paid billing.
3. Paste the key into `GEMINI_API_KEY=` in the local `.env` file.
4. Keep `GEMINI_MODEL=gemini-3.5-flash-lite` for the first connection test.
   If your account cannot access this model on the free tier, stop and report the
   account error without sharing the key. We will not silently switch to paid usage.

## 2. Supabase: persistent instructions

1. Create a free account at https://supabase.com/ and a Free project.
2. Save the database password in your password manager.
3. In the project, click **Connect**, choose **Session pooler**, and copy the URI.
4. Substitute the database password locally and paste the URI into `DATABASE_URL=`.
   URL-encode reserved characters in the password, or use a long random alphanumeric
   password. This is a database connection string, not the Supabase anon API key.
5. Leave the project on the Free plan. The assistant will apply the schema and seed
   after the connection is configured; no pasted SQL secrets are necessary.

## 3. GitHub and Render: sharing and hosting

The assessment instance is now deployed at https://bobalab-support-assistant.onrender.com.
The following instructions also support a fresh setup.

The actual deployment used **New → Web Service → Public Git Repository**, Python 3,
the public source URL, Free compute, `pip install -r requirements.txt`,
`sh scripts/start.sh`, and Advanced health path `/health`. The candidate imported
local secrets directly with Add from .env. No paid compute plan was submitted.
The Blueprint below is an alternative reproducible setup, not a claim that this
instance was created by a Blueprint.

1. Sign in to your GitHub account. From the project terminal, run `gh auth login`.
   Complete its interactive sign-in yourself. Do not paste tokens into chat.
2. Create a free account at https://dashboard.render.com/ using GitHub sign-in.
3. Do not create a paid database or service. Deployment uses `render.yaml` with
   `plan: free`, and Supabase holds persistent state.

Later, after the repository is uploaded, create a Render Blueprint from that repo.
Enter `DATABASE_URL`, `GEMINI_API_KEY`, and `REVIEWER_API_KEY` as secret environment
variables in Render. Copy the values from your local `.env`; never commit that file.
Choose a Free web service even if Render suggests an upgrade.

## Local file and readiness

Open this folder in Cursor: `/Users/fila/Documents/Bobalab`. The local `.env` is
ignored by Git. A random reviewer key can be generated with:

```sh
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Keep that value in `.env` as `REVIEWER_API_KEY`. It is a limited application access
key for reviewers, not your provider/database credential. Share the reviewer key
privately with the submission, not in the public README.

Tell the assistant **“local keys entered”** and which account steps are complete.
Never send the values. The connection check reports status without printing secrets.

## After the code is ready

```sh
python -m app.cli check-config
python -m app.cli migrate
python -m app.cli seed
python -m app.cli check-live
python -m flask --app 'app:create_app()' run --port 8000
```

Use the project's activated Python environment. Render runs migrations and an
idempotent seed before Gunicorn starts. Tests never use your production database
unless you explicitly configure a separate disposable `TEST_DATABASE_URL`.

Free-service limits: Render may sleep after 15 minutes; Supabase may pause after
inactivity; model quotas depend on the account. This demo accepts synthetic data
only. Google documents product-improvement use of free-tier inputs/outputs.
