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

Run the first examples:

```bash
python3 examples/01_basic_model_call.py
python3 examples/02_structured_outputs.py
python3 examples/03_deterministic_workflow.py
python3 examples/04_agent_by_hand.py
python3 examples/05_first_adk_agent.py
python3 examples/06a_file_rag.py
python3 examples/06b_sql_rag.py
python3 examples/07a_vector_rag.py
python3 examples/07b_hybrid_rag.py
```

Load the sample support policies:

```bash
python3 -m support_agent_app.ingest_policies --dry-run
DATABASE_URL="postgresql://..." python3 -m support_agent_app.ingest_policies
```

Run the deployable app locally after installing the app dependencies:

```bash
pip install -e '.[app]'
uvicorn support_agent_app.api:app --reload --port 8080
```

Build the Cloud Run container:

```bash
docker build -t ai-architect-support-agent .
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Teaching Stack

- Python for the examples.
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
- `sql/`: Postgres schema.

## Repo Status

This repo is being built lesson by lesson.
The early examples are intentionally small.
The production app will appear as the course moves from fundamentals into ADK and Google Cloud.
