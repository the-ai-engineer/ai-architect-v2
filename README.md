# AI Architect v2

Public code companion for the AI Architect course.

The course teaches how to build production-style AI systems by building one running project: an AI customer support agent.

The final demo is simple and concrete:

```text
Send an email to a support inbox
-> create a support ticket
-> look up the right support document
-> generate an answer with OpenAI
-> reply by email or escalate to a human
-> inspect logs, traces, evals, and deployment state
```

The course starts with small Python examples.
Then it moves into ADK, RAG, Gmail, Google Cloud, evals, tracing, and deployment.

## Start Here

Read the finished application spec:

- [docs/course-outline.md](/Users/owainlewis/Code/github/ai-engineer/ai-architect-v2/docs/course-outline.md)
- [docs/final-agent-spec.md](/Users/owainlewis/Code/github/ai-engineer/ai-architect-v2/docs/final-agent-spec.md)
- [docs/course-code-map.md](/Users/owainlewis/Code/github/ai-engineer/ai-architect-v2/docs/course-code-map.md)
- [docs/resources/deploy-with-codex-prompt.md](/Users/owainlewis/Code/github/ai-engineer/ai-architect-v2/docs/resources/deploy-with-codex-prompt.md)

Run the first examples:

```bash
uv sync
uv run python examples/01_basic_model_call.py
uv run python examples/02_structured_outputs.py
uv run python examples/03_deterministic_workflow.py
uv run python examples/04_agent_by_hand.py
uv run python examples/05_first_adk_agent.py
uv run python examples/06a_file_rag.py
uv run python examples/06b_sql_rag.py
uv run python examples/07a_vector_rag.py
uv run python examples/07b_hybrid_rag.py
```

Load the sample support policies:

```bash
uv run python -m support_agent_app.ingest_policies --dry-run
DATABASE_URL="postgresql://..." uv run --extra db python -m support_agent_app.ingest_policies
```

Run the deployable app locally:

```bash
uv sync --extra app
uv run --extra app uvicorn support_agent_app.api:app --reload --port 8080
```

Build the Cloud Run container:

```bash
docker build -t ai-architect-support-agent .
```

Run tests:

```bash
uv run python -m unittest discover -s tests
```

## Teaching Stack

- Python for the examples.
- `uv` for package management and running commands.
- The ideas translate to other languages.
- OpenAI `gpt-5.5` as the default model provider.
- Google ADK 2.x for the agent framework once students understand the agent loop.
- Gmail and Pub/Sub for asynchronous email ingestion.
- Cloud Run for deployment.
- Cloud SQL Postgres for state and support documents.
- pgvector for the vector-search lesson.
- Cloud Logging, Cloud Trace, and Cloud Monitoring for observability.

## Repo Structure

- `examples/`: small runnable lesson examples.
- `support_agent/`: plain Python teaching code for lessons 01-04.
- `support_agent_app/`: deployable support agent application.
- `support_agent_app/api.py`: FastAPI HTTP surface for Cloud Run.
- `support_agent_app/services/`: document registry, Gmail labels, and policy ingestion.
- `support_agent_app/agents/`: ADK agent definitions.
- `support_agent_app/integrations/`: external system boundaries.
- `docs/policies/`: editable support policy documents.
- `docs/resources/`: reusable course prompts and support material.
- `sql/`: Postgres schema.

## Repo Status

This repo is being built lesson by lesson.
The early examples are intentionally small.
The production app will appear as the course moves from fundamentals into ADK and Google Cloud.
