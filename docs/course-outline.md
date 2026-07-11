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

We use Pydantic AI as the agent framework once the course moves past the fundamentals.
There are many agent frameworks, and you can also build agents by hand.
Frameworks are useful abstractions, not the core idea.
Pydantic AI supports OpenAI and Anthropic directly, so students can change the model provider without rebuilding the agent loop.

## System We Build

The finished system is an asynchronous customer support agent.

```text
Customer sends email
-> Gmail receives it
-> a scheduled Cloud Run Job discovers it
-> the ingestion API stores it in Postgres
-> Pub/Sub sends it to a Cloud Run worker
-> Pydantic AI agent looks up the right support document from Postgres
-> OpenAI drafts a grounded answer
-> guardrails approve, block, or escalate
-> application code sends and labels the reply as AI Answered
-> or applies Human Needed for a person to handle
```

Customer support is a strong teaching domain because it has repeated questions, clear policies, business context, human escalation, and measurable outcomes.

## Why Not a Simpler Automation Tool

You could build a naive version of this system with n8n, Zapier, Codex automations, Claude integrations, or a small script.
For a personal workflow, that might be enough.

That is not what this course is trying to teach.

The course is about building AI systems you can trust inside a real business.
Once an AI system starts replying to customers, using business data, or making decisions on your behalf, you need more than a quick automation.

Custom code gives you control over the parts that matter as the system gets more complex:

- logs
- traces
- tests
- evals
- retries
- failure handling
- guardrails
- human review
- custom business logic
- deployment and monitoring

The useful distinction is:

```text
simple automation = good for prototypes and personal workflows
custom system = better when the workflow becomes business-critical
```

The course should not dismiss automation tools.
They are useful.
The point is that they are not always the right abstraction when you need robust monitoring, explicit guardrails, custom code, and a system you can operate over time.

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

There are two ways to discover new email work:

- polling: check Gmail every few minutes and process new messages
- event-based: let Gmail notify the app through Pub/Sub when the mailbox changes

Polling and event-based delivery are input mechanisms, not complete system architectures.
The course uses scheduled polling because email does not need an instant response.
Each discovered message is then submitted to the asynchronous support workflow so it can be processed and retried independently.

The course first submits a canonical support request directly, then connects a scheduled Gmail poller as the real event producer.
See [Architecture Patterns for AI Systems](ai-system-architecture-patterns/design.md) for the complete design.

## Lessons

| # | Lesson | Main idea | Code |
|---|---|---|---|
| 00 | Introduction to AI Systems | What we are building, why customer support, why async, why Google Cloud, why Python | No code |
| 01 | Basic Model Calls | Treat the model as a software component behind a small boundary | `examples/01_basic_model_call.py` |
| 02 | Structured Outputs | Classify a support email into typed data with Pydantic-style schemas | `examples/02_structured_outputs.py` |
| 03 | Calls, Workflows, and Agents | Compare one model call, a deterministic workflow, and an agent | `examples/03_deterministic_workflow.py` |
| 04 | Agent by Hand | Build a minimal tool-calling agent loop in Python | `examples/04_agent_by_hand.py` |
| 05 | First Framework Agent | Move the same agent idea into Pydantic AI and explain why we now use a framework | `examples/05_first_framework_agent.py` |
| 06 | Simple RAG with Files and SQL | Load support docs from files, move them into Postgres, and query known documents as context | `06a_file_rag.py`, `06b_sql_rag.py` |
| 07 | Vector Search and Hybrid RAG | Learn vector search and hybrid search, then compare them with the simpler document-registry path | `07a_vector_rag.py`, `07b_hybrid_rag.py` |
| 08 | Gmail and Async Work | Connect Gmail, Pub/Sub, tickets, and background processing | Future cloud sample |
| 09 | Human Escalation and Guardrails | Keep the agent on topic, avoid sensitive answers, and label threads as `AI Answered` or `Human Needed` | Future guardrails sample |
| 10 | Evals | Build a spreadsheet-style eval set, run sample emails through the system, and review pass/fail results | Future eval suite |
| 11 | Tracing, Logs, and Cost | Inspect model calls, tool calls, latency, failures, and spend | Future observability sample |
| 12 | Deployment | Deploy the finished support agent to Google Cloud and use Codex to help configure the cloud resources | `docs/resources/deploy-with-codex-prompt.md` |

## Course Progression

Lessons 01 to 04 are plain Python fundamentals.

Students learn:

- model calls
- structured outputs
- deterministic workflows
- what an agent loop actually is
- why agents are simpler than they look

Lesson 05 introduces Pydantic AI.
Run the lesson 05 example with `uv run python examples/05_first_framework_agent.py`.

From that point onward, Pydantic AI is the course runtime.
We do not keep rebuilding the same system in different frameworks.

Lessons 06 onward build the real application:

- file loading as the starting point for support docs
- Postgres document lookup as the default production RAG tool
- vector search as an alternative retrieval tool
- hybrid search as an alternative for messier knowledge bases
- a typed Pydantic AI reply or escalation decision
- deterministic Gmail reply and label actions
- evals
- tracing
- deployment

The architecture progression should be explicit:

```text
local examples
-> local fake email workflow
-> direct support events through the API
-> Postgres acceptance and an outbox
-> Pub/Sub and scalable workers
-> scheduled Gmail polling as a real input channel
-> Cloud Run Jobs for polling and outbox publishing, plus API and worker services
-> Cloud Run job or local CLI for one-off work like policy ingestion
```

The deployed app uses one codebase in four roles: scheduled poller, ingestion API, scheduled outbox publisher, and support worker.
Pub/Sub invokes authenticated private workers using OIDC, Cloud Run probes handle service health, and any admin surface requires separate authentication.
Cloud Run jobs are also useful for policy ingestion and maintenance work.

The deployment lesson should also teach how to use Codex as a deployment partner.
Students should understand the architecture first, then use the prompt in `docs/resources/deploy-with-codex-prompt.md` to help configure Google Cloud step by step.

The point is not to memorise every `gcloud` command.
The point is to understand enough of the system to supervise Codex, catch mistakes, and verify that the deployed app actually works.

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
The current default OpenAI model in the repo is `gpt-5.6`.

Lesson 05 introduces Pydantic AI and the idea that model providers are a configuration choice.
The app should be able to swap providers through its model setting.
The sample uses Pydantic AI's direct OpenAI provider by default.
Changing `AI_ARCHITECT_MODEL` to an `anthropic:` model uses Anthropic directly while keeping the same instructions and business tools.

This is one reason to adopt a framework after building the loop by hand.
The hand-built example exposes the provider's request, response, tool-call, and retry details.
The framework normalises those details behind one agent interface, so changing models usually means changing configuration instead of rewriting orchestration code.

Provider portability is not perfect.
Native tools, model settings, token limits, structured output support, and response behaviour still differ between providers.
The lesson should teach frameworks as a useful boundary, not as proof that every model is interchangeable.

Do not make students learn a new framework, a new model provider, and retrieval at the same time.
Provider choice is part of the architecture, but it should not distract from the system being built.

## Testing and Evals

Evals should start with sample support emails, not complex infrastructure.

The course should include a simple eval file that looks like a spreadsheet:

```text
id
email_subject
email_body
expected_category
expected_label
expected_document_id
expected_should_reply
expected_key_points
actual_category
actual_label
actual_document_id
actual_reply
classification_pass
retrieval_pass
answer_pass
overall_pass
notes
```

Students can run the evals by passing sample emails into the same support workflow used by the app.
The output should be another CSV that compares expected results with actual results.

Manual review is part of the lesson.
Students should inspect the answers and mark pass or fail for the parts that require judgment:

- did the system classify the email correctly?
- did it choose the right support document?
- did it answer using only trusted policy context?
- did it include the required policy points?
- did it escalate when it should?
- would you be comfortable sending this reply to a customer?

Automated checks should handle the obvious parts:

- expected label matches actual label
- expected document matches actual document
- escalation cases do not generate a customer reply
- answers do not include banned phrases
- answers include required key points where possible

LLM-as-judge can come later, but it should not be the first eval pattern.
Start with visible sample data and human review because it is easier to understand and closer to real QA.

The core lesson is:

```text
Do not eval the model in the abstract.
Eval the business workflow.
```

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
The Pydantic AI agent is the application we carry forward.
