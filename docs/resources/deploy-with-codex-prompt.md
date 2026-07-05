# Deploy With Codex Prompt

Use this prompt when you are ready to deploy the support agent to Google Cloud.

The goal is not to outsource understanding.
The goal is to use Codex as an implementation partner while you inspect the architecture, commands, secrets, and verification steps.

```text
You are helping me deploy this AI customer support agent to Google Cloud.

Goal:
Deploy the app as a Cloud Run service, with supporting Google Cloud resources, so I can send a test support email and see the system process it.

Repository:
<repo URL>

Architecture:
- Cloud Run service for the support agent API
- Cloud SQL Postgres for support documents and app state
- Secret Manager for API keys and OAuth credentials
- Gmail API for reading and replying to support emails
- Pub/Sub for Gmail mailbox-change notifications
- Cloud Logging and Cloud Monitoring for observability
- Optional Cloud Run job or local CLI for policy ingestion

Constraints:
- Do not use destructive commands.
- Explain each cloud resource before creating it.
- Prefer least-privilege IAM.
- Store secrets in Secret Manager, not in code or env files committed to git.
- Make the deployment reproducible with scripts or documented commands.
- After each major step, verify it worked.
- If OAuth consent or Gmail setup requires browser/manual steps, pause and give exact instructions.
- Do not skip verification.

Tasks:
1. Inspect the repo and identify the app entrypoint, Dockerfile, config, and required environment variables.
2. Check whether `gcloud` is installed and authenticated.
3. Ask me which Google Cloud project and region to use.
4. Enable required APIs.
5. Create or confirm required service accounts.
6. Create required secrets.
7. Create or connect Cloud SQL Postgres.
8. Run policy ingestion.
9. Deploy the Cloud Run service.
10. Verify `/health`.
11. Configure Gmail API access.
12. Configure Pub/Sub notification flow.
13. Send or simulate a test email.
14. Check logs and confirm the system processed the message.
15. Produce a short deployment report with resource names, URLs, secrets used, and remaining manual steps.

Output:
Work step by step.
Run checks.
Stop if you hit an auth, billing, OAuth, or IAM decision that needs my approval.
```

Use this prompt after you understand the target architecture.
Codex can help with the commands, but you still need to know what good looks like and how to verify it.
