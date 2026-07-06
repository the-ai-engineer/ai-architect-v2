# Course Code Map

This repo has two kinds of code.

First, it has small teaching samples for the early lessons.
These are intentionally simple and runnable on a local machine.
They should be self-contained so each lesson can be taught from one open file.

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
| 07A Vector RAG | `examples/07a_vector_rag.py` | Store embeddings in Postgres with pgvector and run vector search |
| 07B Hybrid RAG | `examples/07b_hybrid_rag.py` | Combine Postgres full-text search and pgvector similarity |
| 08 Gmail and async work | Future cloud module | Connect Gmail, Pub/Sub, tickets, and background processing |
| 09 Human escalation and guardrails | Future guardrails module | Label safe replies as `AI Answered` and risky messages as `Human Needed` |
| 10 Evals | Future eval suite | Run sample support emails through the workflow and review spreadsheet-style pass/fail results |
| 11 Tracing, logs, and cost | Future observability module | Inspect model calls, tool calls, traces, latency, and spend |
| 12 Deployment | `docs/resources/deploy-with-codex-prompt.md` | Deploy the finished system to Google Cloud with Codex as an implementation partner |

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

The course should show the progression from simple to production-shaped:

```text
local fake email workflow
-> Gmail polling
-> Gmail Pub/Sub events
-> Cloud Run service
```

Polling is easier to explain because the app checks Gmail on a schedule.
It is a good bridge for local testing and a first working demo.

Event-based processing is the final architecture.
Gmail notifies Pub/Sub, Pub/Sub calls Cloud Run, and the app processes the changed mailbox state.
This avoids constant polling and matches how production event systems are usually built.

The main support agent should be a Cloud Run service.
Use a Cloud Run job or local CLI for one-off work such as policy ingestion.

The deployment resource is `docs/resources/deploy-with-codex-prompt.md`.
Students should use it after they understand the target architecture.
This reinforces the course position: AI tools can help with setup, but the engineer still owns the architecture, verification, and debugging.

## Why Not Just n8n or Codex Automations

Students will reasonably ask why this is not just an automation workflow.

The answer is that simple automation tools are useful for prototypes, personal workflows, and low-risk internal tasks.
They are not always the right abstraction when the system touches customers, private business data, or operational decisions.

This course is teaching the production concerns that appear after the basic demo works:

- monitoring
- tracing
- evals
- tests
- retries
- failure handling
- guardrails
- human review
- custom business logic
- deployment control

A naive version can be hacked together with integrations.
A business system needs clear boundaries, explicit failure modes, and a way to inspect what happened.

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

## Eval Teaching Thread

Evals should be practical and visible.

Start with a CSV or spreadsheet of sample support emails.
Each row should include the input email, the expected classification, the expected document, the expected action, and notes on what a good answer must include.

The eval runner should pass each sample email into the support workflow and write results back out to a CSV.
Some checks can be automatic, such as matching labels or document ids.
Other checks should be manually reviewed, such as whether the final answer is clear, grounded, and safe to send.

This teaches students to evaluate the whole workflow instead of treating model quality as a vague feeling.

## Application Structure

The deployable app lives in `support_agent_app`.

- `api.py` is the Cloud Run HTTP surface.
- `config.py` reads environment variables.
- `agents/` contains ADK agent definitions.
- `services/` contains app logic that can be tested without cloud services.
- `integrations/` contains external system boundaries like Postgres and Gmail.

The examples stay in `examples`.
They should stay small even when the deployable app becomes more complete.
They should not import `support_agent_app`.
When an example needs a small tool or document type, duplicate the tiny teaching version in the file.
