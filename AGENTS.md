# AGENTS.md

This repo contains the public code companion for AI Architect v2.

Keep the code practical, small, and aligned with the private course material in `/Users/owainlewis/Code/github/ai-engineer/ai-architect-course`.

## Course Direction

The finished application is an AI customer support system.

A customer sends an email to a support inbox.
The system turns it into a ticket, retrieves relevant support docs, drafts an answer with OpenAI, and escalates to a human when it cannot answer safely.

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
- `support_agent/` contains shared teaching code.
- `docs/final-agent-spec.md` is the source of truth for the finished app.
- `docs/course-code-map.md` maps lessons to code.

## Verification

Run this before reporting code changes:

```bash
python3 -m unittest discover -s tests
python3 examples/01_basic_model_call.py
python3 examples/02_structured_outputs.py
python3 examples/03_deterministic_workflow.py
python3 examples/04_agent_by_hand.py
```

