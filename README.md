# AI Architect v2

Public code companion for the AI Architect course.

The course teaches how to build production-style AI systems by building one running project: an AI customer support agent.

The final demo is simple and concrete:

```text
Send an email to a support inbox
-> create a support ticket
-> retrieve support docs
-> generate an answer with OpenAI
-> reply by email or escalate to a human
-> inspect logs, traces, evals, and deployment state
```

The course starts with small Python examples.
Then it moves into ADK, RAG, Gmail, Google Cloud, evals, tracing, and deployment.

## Start Here

Read the finished application spec:

- [docs/final-agent-spec.md](/Users/owainlewis/Code/github/ai-engineer/ai-architect-v2/docs/final-agent-spec.md)
- [docs/course-code-map.md](/Users/owainlewis/Code/github/ai-engineer/ai-architect-v2/docs/course-code-map.md)

Run the first examples:

```bash
python3 examples/01_basic_model_call.py
python3 examples/02_structured_outputs.py
python3 examples/03_deterministic_workflow.py
python3 examples/04_agent_by_hand.py
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Teaching Stack

- Python for the examples.
- OpenAI as the default model provider.
- Google ADK for the agent framework once students understand the agent loop.
- Gmail and Pub/Sub for asynchronous email ingestion.
- Cloud Run for deployment.
- Cloud SQL Postgres and pgvector for state and retrieval.
- Cloud Logging, Cloud Trace, and Cloud Monitoring for observability.

## Repo Status

This repo is being built lesson by lesson.
The early examples are intentionally small.
The production app will appear as the course moves from fundamentals into ADK and Google Cloud.

