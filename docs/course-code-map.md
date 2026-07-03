# Course Code Map

This repo has two kinds of code.

First, it has small teaching samples for the early lessons.
These are intentionally simple and runnable on a local machine.

Second, it will have the finished support agent.
That app uses ADK, RAG, Gmail, Google Cloud, evals, tracing, and deployment.

The course ideas are language agnostic.
The examples use Python because it keeps the teaching code small and readable.

## Lesson Plan

| Lesson | Code shape | Outcome |
|---|---|---|
| 00 Introduction to AI systems | No code | Explain the project, customer support domain, async systems, Python examples, Google Cloud, OpenAI, and ADK |
| 01 Basic model call | `examples/01_basic_model_call.py` | Call a model through a tiny boundary |
| 02 Structured outputs | `examples/02_structured_outputs.py` | Turn a support email into a typed classification |
| 03 Calls, workflows, and agents | `examples/03_deterministic_workflow.py` | Compare one model call, a fixed workflow, and an agent |
| 04 Agent by hand | `examples/04_agent_by_hand.py` | Build the agent loop without a framework |
| 05 First ADK agent | `examples/05_first_adk_agent.py` | Move from hand-built loop to an ADK agent with document lookup tools |
| 06A File RAG | `examples/06a_file_rag.py` | Load trusted markdown files and pass the right document as context |
| 06B SQL RAG | `examples/06b_sql_rag.py` and `support_agent_app/ingest_policies.py` | Turn policy markdown into Postgres rows |
| 07A Vector RAG | `examples/07a_vector_rag.py` | Show the vector-search retrieval shape with a tiny local embedding |
| 07B Hybrid RAG | `examples/07b_hybrid_rag.py` | Combine keyword and vector-style signals |
| 08 Gmail and async work | Future cloud module | Connect Gmail, Pub/Sub, tickets, and background processing |
| 09 Human escalation and guardrails | Future guardrails module | Label safe replies as `AI Answered` and risky messages as `Human Needed` |
| 10 Evals | Future eval suite | Test classification, retrieval, escalation, and answer quality |
| 11 Tracing, logs, and cost | Future observability module | Inspect model calls, tool calls, traces, latency, and spend |
| 12 Deployment | Future deployment guide | Deploy the finished system to Google Cloud |

## Teaching Rule

Do not teach a concept and then force students to reimplement it in a different framework.

The hand-built agent is a microscope.
It shows what an agent is.

After that, ADK is the course runtime.
All later lessons should build forward from the ADK version.

## Async Teaching Thread

The finished system is asynchronous.

A synchronous chatbot is useful, but support email does not need instant replies.
That gives us room to teach production patterns:

- receive work
- store work
- queue work
- process it in the background
- retry failures
- send the result later
- trace and evaluate what happened

## Retrieval Teaching Thread

Retrieval is not only vector search.

The course covers four forms:

- file RAG for small trusted documents
- SQL document lookup for known support policies
- vector search for semantic document retrieval
- hybrid search for combining retrieval methods

Lessons 06 and 07 should carry this thread without making retrieval the whole course.

The finished customer support app uses SQL document lookup as the default.
That is the pragmatic production choice for a small business with a known set of support policies.

The editable policy files live in `docs/policies`.
The ingest command in `support_agent_app` loads those markdown files into Postgres.

## Gmail Label Teaching Thread

The support system does not need a custom dashboard at first.

Use Gmail labels as the review surface:

- `AI Answered` for messages the agent answered
- `Human Needed` for messages the agent skipped or escalated

This makes guardrails visible.
Students can inspect the inbox and see exactly what work the agent did.

## Application Structure

The deployable app lives in `support_agent_app`.

- `api.py` is the Cloud Run HTTP surface.
- `config.py` reads environment variables.
- `agents/` contains ADK agent definitions.
- `services/` contains app logic that can be tested without cloud services.
- `integrations/` contains external system boundaries like Postgres and Gmail.

The examples stay in `examples`.
They should stay small even when the deployable app becomes more complete.
