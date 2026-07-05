# AGENTS.md

This repo contains teaching code for the AI Engineer course AI Architect v2.

The code is designed for lessons, recordings, and student exercises.
Prefer clarity over cleverness.
Examples should be easy to read on screen and easy to run locally.

Keep the code practical, small, and aligned with the private course material in `/Users/owainlewis/Code/github/ai-engineer/ai-architect-course`.

## Course Direction

The finished application is an AI customer support system.

A customer sends an email to a support inbox.
The system turns it into a ticket, looks up a known support document from Postgres, drafts an answer with OpenAI, and escalates to a human when it cannot answer safely.

Use OpenAI as the default teaching model.
Use Google Cloud as the default deployment target.
Use ADK after the hand-built agent lesson.

## Code Style

- Use Python.
- Keep lesson examples runnable from the command line.
- Prefer simple interfaces over framework magic.
- Do not introduce cloud dependencies into early lessons.
- Do not use em dashes in prose.
- Keep markdown sentences on separate physical lines when files get long.

## Structure

- `examples/01_basic_model_call.py` to `examples/04_agent_by_hand.py` are small teaching samples.
- `examples/05_first_adk_agent.py` introduces the ADK-shaped support agent.
- `examples/06a_file_rag.py`, `06b_sql_rag.py`, `07a_vector_rag.py`, and `07b_hybrid_rag.py` are separate retrieval examples.
- `support_agent/` contains shared teaching code for lessons 01-04.
- `support_agent_app/` contains the deployable application.
- `sql/` contains the production-shaped Postgres schema.
- `docs/policies/` contains editable sample support policies.
- `docs/final-agent-spec.md` is the source of truth for the finished app.
- `docs/course-code-map.md` maps lessons to code.

## Verification

Run this before reporting code changes:

```bash
uv run python -m unittest discover -s tests
uv run python examples/01_basic_model_call.py
uv run python examples/02_structured_outputs.py
uv run python examples/03_deterministic_workflow.py
uv run python examples/04_agent_by_hand.py
uv run python examples/05_first_adk_agent.py
uv run python examples/06a_file_rag.py
uv run python examples/06b_sql_rag.py
uv run python examples/07a_vector_rag.py
uv run python examples/07b_hybrid_rag.py
uv run python -m support_agent_app.ingest_policies --dry-run
uv run python -m support_agent_app.main
```
