# Course Code Map

This repo has two kinds of code.

First, it has small teaching samples for the early lessons.
These are intentionally simple and runnable on a local machine.

Second, it will have the finished support agent.
That app uses ADK, RAG, Gmail, Google Cloud, evals, tracing, and deployment.

## Lesson Plan

| Lesson | Code shape | Outcome |
|---|---|---|
| 01 Basic model call | `examples/01_basic_model_call.py` | Call a model through a tiny boundary |
| 02 Structured outputs | `examples/02_structured_outputs.py` | Turn a support email into a typed classification |
| 03 Deterministic workflows | `examples/03_deterministic_workflow.py` | Run classify, retrieve, draft, or escalate as a fixed workflow |
| 04 Agent by hand | `examples/04_agent_by_hand.py` | Build the agent loop without a framework |
| 05 First ADK agent | Future ADK sample | Move from hand-built loop to framework runtime |
| 06 RAG in isolation | Future RAG module | Chunk support docs, embed them, and search with Postgres |
| 07 Gmail and async work | Future cloud module | Connect Gmail, Pub/Sub, and Cloud Run |
| 08 Build the email agent | Future app | Wire ADK, RAG, Gmail, guardrails, and review together |
| 09 Evals | Future eval suite | Test classification, retrieval, escalation, and answer quality |
| 10 Tracing and logs | Future observability module | Inspect model calls, tool calls, traces, and costs |
| 11 Deployment | Future deployment guide | Deploy the finished system to Google Cloud |

## Teaching Rule

Do not teach a concept and then force students to reimplement it in a different framework.

The hand-built agent is a microscope.
It shows what an agent is.

After that, ADK is the course runtime.
All later lessons should build forward from the ADK version.

