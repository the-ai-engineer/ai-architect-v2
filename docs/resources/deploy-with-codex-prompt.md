# Deploy With Codex Prompt

Use this prompt when you are ready to deploy the support agent to Google Cloud.

The goal is not to outsource understanding.
The goal is to use Codex as an implementation partner while you inspect the architecture, commands, secrets, and verification steps.

```text
You are helping me deploy this AI customer support agent to Google Cloud.

Goal:
Deploy the complete support system so a scheduled job discovers a test email, the API stores its source reference durably, Pub/Sub sends the event identifier to a worker, and the system replies or marks it for human review.

Repository:
<repo URL>

Architecture:
- Cloud Run Job that polls Gmail every five minutes
- Cloud Run service for the ingestion API
- Cloud SQL Postgres for source references, events, outbox records, support documents, and processing state
- Cloud Run Job that publishes pending outbox records every minute
- Pub/Sub topic and authenticated push subscription for accepted support events
- Cloud Run service for scalable support workers
- Secret Manager for API keys and OAuth credentials
- Gmail API for reading and replying to support emails
- Cloud Logging and Cloud Monitoring for observability
- Optional Cloud Run Job or local CLI for policy ingestion

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
2. Check whether `uv` is installed and run `uv sync`.
3. Check whether `gcloud` is installed and authenticated.
4. Ask me which Google Cloud project and region to use.
5. Enable required APIs.
6. Create or confirm required service accounts.
7. Create required secrets.
8. Create or connect Cloud SQL Postgres and run schema migrations.
9. Run policy ingestion with `uv run --extra db`.
10. Deploy the ingestion API, grant only required service-to-service callers access, and verify `/health`.
11. Deploy the support worker service with authenticated Pub/Sub access.
12. Create the Pub/Sub topic, authenticated push subscription, retry policy, dead-letter topic, and monitored dead-letter subscription.
13. Deploy and schedule the outbox publisher job with overlap protection.
14. Configure offline Gmail OAuth using the `gmail.modify` scope and Secret Manager.
15. Create the `AI Answered` and `Human Needed` labels.
16. Deploy and schedule the Gmail polling job with a cursor lease and first-run baseline.
17. Send or simulate a test email.
18. Verify the source reference, event, outbox publication, worker result, and Gmail action without storing the complete message body.
19. Configure the daily retention cleanup job.
20. Test duplicate delivery, retry exhaustion, uncertain send reconciliation, expired leases, and Gmail cursor recovery.
21. Check logs, operator alerts, dead letters, queue depth, and unpublished outbox records.
22. Produce a short deployment report with resource names, URLs, secrets used, and remaining manual steps.

Output:
Work step by step.
Run checks.
Stop if you hit an auth, billing, OAuth, or IAM decision that needs my approval.
```

Use this prompt after you understand the target architecture.
Codex can help with the commands, but you still need to know what good looks like and how to verify it.
