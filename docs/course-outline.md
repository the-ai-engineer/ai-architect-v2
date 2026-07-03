# Course Outline

## Course Introduction

AI Architect is a course about building real AI systems.

The course uses one running project: an AI customer support agent that answers customer questions by email.

The point is not to teach one framework or one cloud provider.
The point is to teach the system patterns behind useful AI products.

You can build these systems in any language.
The ideas translate to Python, TypeScript, Java, Go, or whatever stack you use.

For this course, we use Python for the code samples because it is concise, widely used for AI work, and easy to read while learning the architecture.

We use Google Cloud as the deployment platform because it is what Owain uses for client projects.
Google Cloud has a good developer interface, clean project-level billing, and strong support for the Gmail API.
Keeping each client in a separate Google Cloud project also makes billing and invoicing easier when building client systems.

We use OpenAI as the default model provider.
The system should still be designed so the model provider can change later.

We use Google ADK as the agent framework once the course moves past the fundamentals.
There are many agent frameworks, and you can also build agents by hand.
Frameworks are useful abstractions, not the core idea.

## System We Build

The finished system is an asynchronous customer support agent.

```text
Customer sends email
-> Gmail receives it
-> Pub/Sub notifies our app
-> Cloud Run processes the ticket
-> ADK agent looks up the right support document from Postgres
-> OpenAI drafts a grounded answer
-> guardrails approve, block, or escalate
-> Gmail sends the reply and labels it AI Answered
-> or Gmail labels it Human Needed for a person to handle
```

Customer support is a strong teaching domain because it has repeated questions, clear policies, business context, human escalation, and measurable outcomes.

## Synchronous vs Asynchronous AI Systems

A typical chatbot is synchronous.
A user sends a message and waits for a response.

That pattern can work well, but AI calls are often slow.
When systems need to scale, synchronous request and response flows can become fragile.

For customer support, we do not need an instant response.
It is usually fine to process work in the background.

That makes customer support a good place to teach asynchronous AI systems:

```text
receive work
store it
queue it
process it
retry failures
send the result later
log what happened
```

This is one of the most important production patterns in the course.

## Lessons

| # | Lesson | Main idea | Code |
|---|---|---|---|
| 00 | Introduction to AI Systems | What we are building, why customer support, why async, why Google Cloud, why Python | No code |
| 01 | Basic Model Calls | Treat the model as a software component behind a small boundary | `examples/01_basic_model_call.py` |
| 02 | Structured Outputs | Classify a support email into typed data with Pydantic-style schemas | `examples/02_structured_outputs.py` |
| 03 | Calls, Workflows, and Agents | Compare one model call, a deterministic workflow, and an agent | `examples/03_deterministic_workflow.py` |
| 04 | Agent by Hand | Build a minimal tool-calling agent loop in Python | `examples/04_agent_by_hand.py` |
| 05 | First ADK Agent | Move the same agent idea into ADK and explain why we now use a framework | `examples/05_first_adk_agent.py` |
| 06 | Simple RAG with Files and SQL | Load support docs from files, move them into Postgres, and query known documents as context | `06a_file_rag.py`, `06b_sql_rag.py` |
| 07 | Vector Search and Hybrid RAG | Learn vector search and hybrid search, then compare them with the simpler document-registry path | `07a_vector_rag.py`, `07b_hybrid_rag.py` |
| 08 | Gmail and Async Work | Connect Gmail, Pub/Sub, tickets, and background processing | Future cloud sample |
| 09 | Human Escalation and Guardrails | Keep the agent on topic, avoid sensitive answers, and label threads as `AI Answered` or `Human Needed` | Future guardrails sample |
| 10 | Evals | Test classification, retrieval, answers, and escalation behavior | Future eval suite |
| 11 | Tracing, Logs, and Cost | Inspect model calls, tool calls, latency, failures, and spend | Future observability sample |
| 12 | Deployment | Deploy the finished support agent to Google Cloud | Future deployment guide |

## Course Progression

Lessons 01 to 04 are plain Python fundamentals.

Students learn:

- model calls
- structured outputs
- deterministic workflows
- what an agent loop actually is
- why agents are simpler than they look

Lesson 05 introduces ADK.

From that point onward, ADK is the course runtime.
We do not keep rebuilding the same system in different frameworks.

Lessons 06 onward build the real application:

- file loading as the starting point for support docs
- Postgres document lookup as the default production RAG tool
- vector search as an alternative retrieval tool
- hybrid search as an alternative for messier knowledge bases
- human escalation as an ADK tool
- Gmail reply as an ADK tool
- evals
- tracing
- deployment

## Retrieval Progression

The course should cover four retrieval patterns without dragging the course sideways.

Lesson 06 covers the pragmatic production path:

- file loading: start with trusted markdown support docs
- SQL document lookup: store those docs in Postgres with categories, summaries, keywords, and body text

The sample support docs live in `docs/policies`.
The ingest command turns those files into rows in Postgres.

Lesson 07 covers the more flexible alternatives:

- vector search: embed support docs and retrieve semantically similar chunks
- hybrid search: combine keyword search, vector search, and SQL lookup when one retrieval method is not enough

This keeps retrieval tight while still teaching good judgment.
For this customer support system, the finished app uses the simpler Postgres document registry.
Vector search and hybrid search are included so students understand the trade-off instead of treating RAG as magic.

Keep the code samples split even when the course lesson covers more than one idea:

- `06a_file_rag.py`
- `06b_sql_rag.py`
- `07a_vector_rag.py`
- `07b_hybrid_rag.py`

Each example should be small, runnable, and easy to explain in a recording.

## Model Provider Progression

Use OpenAI for the early model calls, structured outputs, and RAG examples.
It keeps the teaching path simple.

Lesson 05 introduces ADK and the idea that model providers are a configuration choice.
The app should be able to swap providers through its model setting.

Do not make students learn a new framework, a new model provider, and retrieval at the same time.
Provider choice is part of the architecture, but it should not distract from the system being built.

## Guardrails and Human Escalation

One hard part of AI systems is that customers can send any question.
The input is unbounded.

The agent should not answer everything.
It should only answer questions that are on topic, supported by trusted context, and safe to answer.

When the question is off topic, sensitive, unsupported, or risky, the system should not force an answer.
For this course, the system simply labels the Gmail thread `Human Needed`.

When the system does answer, it labels the Gmail thread `AI Answered`.

That gives us a simple operational view:

```text
AI Answered
Human Needed
```

This keeps the product small while still teaching a serious production pattern.
We can review the agent's work in Gmail, see what it answered, and see where humans need to step in.

## Teaching Principle

Build the mechanism by hand once.
Then use the framework for the real system.

The hand-built agent is there to make the concept clear.
The ADK agent is the application we carry forward.
