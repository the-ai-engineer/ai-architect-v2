# Final Agent Spec

## Product

The finished application is an AI customer support agent.

A customer sends an email to a support inbox.
The system reads the message, creates a ticket, looks up the right support document, drafts an answer, and either replies by email or escalates to a human.

This spec describes the target application the course builds toward.
The current runnable repo covers the early local lessons and the support document registry first.
Gmail, Pub/Sub, guardrails, evals, observability, and deployment code are added later in the course path.

The operational interface stays simple.
If the AI answers the message, the email gets an `AI Answered` Gmail label.
If the AI cannot answer safely, the email gets a `Human Needed` Gmail label and a person handles it.

The course uses email because it makes the demo real.
The same backend shape could sit behind Zendesk, Intercom, HelpScout, Slack, a chat widget, or a custom ticketing UI.

This could be built as a naive automation with n8n, Zapier, Codex automations, Claude integrations, or a few scripts.
That is a valid prototype path.

The final app is custom code because the course is teaching how to build a system you can operate:

- clear service boundaries
- custom business logic
- guardrails
- human escalation
- tests
- evals
- retries
- logs
- traces
- cost tracking
- deployment control

The course positioning should be:

```text
Automation tools are good for quick prototypes.
Custom code is better for business-critical AI systems.
```

## Why Customer Support

Customer support is one of the clearest domains for applied AI systems.

It has repeated questions, trusted policies, private business context, human review paths, and visible business value.

It also teaches the real architecture behind AI products:

- classification
- retrieval
- tool use
- async processing
- human escalation
- guardrails
- evals
- tracing
- deployment

## Final Demo

The demo should end like this:

```text
1. Send an email from a normal email account to the course support inbox.
2. Gmail sends a mailbox-change event through Pub/Sub.
3. Cloud Run receives the event.
4. The app fetches the new email and stores it as a ticket.
5. The Pydantic AI support agent looks up the right support document from Postgres.
6. OpenAI drafts a grounded answer.
7. Guardrails decide whether the answer is safe to send.
8. Gmail sends the reply and labels the thread `AI Answered`, or the app labels it `Human Needed`.
9. The run appears in logs, traces, eval reports, and cost records.
```

## Scope

The main course path handles generic support questions.

Examples:

- refund policy
- cancellation policy
- product setup
- troubleshooting
- billing guidance that does not require private account access
- account access advice that does not change account state

The main path should not depend on customer identity verification, private order lookup, refunds, or account changes.

Those are extension examples because they add authorization and security complexity.

## Architecture

```text
Gmail support inbox
  -> Pub/Sub
  -> Cloud Run webhook
  -> ticket store
  -> Pydantic AI support agent
      -> classify question
      -> inspect support document index
      -> load the right support document
      -> draft answer
      -> check answer
      -> send reply and label AI Answered
      -> or label Human Needed
  -> Gmail reply or human review inbox
  -> logs, traces, evals, and metrics
```

The course should teach the async progression in stages:

```text
local fake email workflow
-> Gmail polling
-> Gmail Pub/Sub events
-> Cloud Run service
```

Polling is useful for local development and first demos.
Event-based processing is the final production shape.
Gmail publishes mailbox changes to Pub/Sub, Pub/Sub calls the Cloud Run service, and the app fetches the changed email state from Gmail.

The main deployed app should be a Cloud Run service.
Cloud Run jobs are useful for policy ingestion, maintenance tasks, or scheduled polling, but they are not the main API surface for the support agent.

The course should include a deployment prompt for Codex.
Students can use Codex to help configure Google Cloud, but the course should still teach the architecture and verification steps.
The reusable prompt lives in `docs/resources/deploy-with-codex-prompt.md`.

## Technology Choices

Use OpenAI as the default model provider.
It is the cleanest teaching path for model calls, structured outputs, embeddings, answer generation, and evals.
The default OpenAI model is `gpt-5.6`.

Use Google Cloud as the default deployment target.
It is the best fit for Gmail, Pub/Sub, Cloud Run, Cloud SQL, Cloud Trace, Cloud Logging, and Cloud Monitoring.

Use Pydantic AI from lesson 5 onward.
Students first build an agent by hand so they understand the loop.
Then Pydantic AI becomes the production framework for the rest of the course.
The app uses OpenAI directly by default and can use Anthropic directly through the same agent interface.

The framework makes model changes easier because it owns the provider-specific agent loop and tool-call format.
The business tools, instructions, and application boundaries can stay the same.
Provider-native tools and model-specific settings may still require changes, so provider portability must be tested rather than assumed.

## Core Components

| Component | Responsibility |
|---|---|
| `TicketStore` | Store incoming support tickets and their status |
| `DocumentRegistry` | Store support documents, categories, summaries, and keywords in Postgres |
| `SupportAgent` | Decide which tools to call and when to escalate |
| `list_support_documents` | Show the agent the document index |
| `find_support_document` | Load the best support document for the question |
| `draft_support_reply` | Draft an answer grounded in retrieved context |
| `check_reply` | Decide whether the answer is safe enough to send |
| `send_email_reply` | Send a Gmail reply when approved |
| `apply_gmail_label` | Label the thread `AI Answered` or `Human Needed` |
| `create_human_review` | Escalate uncertain or risky tickets |
| `RunLogger` | Record events, traces, model calls, and tool calls |

## Application Layout

The deployable application lives in `support_agent_app`.

```text
support_agent_app/
  api.py
  config.py
  main.py
  agents/
  services/
  integrations/
```

Keep business logic in `services`.
Keep external APIs in `integrations`.
Keep Pydantic AI code in `agents`.
Keep small teaching examples in `examples`.

## Human Escalation

Customers can send anything to a support inbox.
That is where AI systems get more complex.

The system has unbounded input, so it must decide which questions are suitable for AI and which questions need a person.
The agent should only answer questions that are on topic and supported by trusted context.

The assistant escalates when:

- no relevant docs are found
- retrieved docs conflict
- the question is off topic
- the question requires private account data
- the question asks for a refund or account change
- the user appears to be trying to extract sensitive information
- the model confidence is low
- the draft contains unsupported claims
- a send action fails

Human escalation is part of the product.
It is not a failure case.

For the course system, escalation is deliberately simple.
When a message needs human input, the app does not reply.
It applies a `Human Needed` Gmail label so the team can review it inside the inbox.

When the AI does answer, the app applies an `AI Answered` Gmail label.
That gives us a visible audit trail of the agent's work without building a custom support dashboard.

The customer experience is simple:

```text
customer sends email
  -> AI answers it
  -> or a human answers it
```

The internal workflow is also simple:

```text
AI Answered
Human Needed
```

## Data Model

Start with these tables in the production app:

```text
tickets
ticket_messages
support_documents
draft_replies
human_reviews
gmail_labels
agent_runs
tool_calls
model_calls
events
eval_cases
eval_runs
eval_results
```

Use plain Postgres as the default production path.
Store support documents with categories, summaries, keywords, and body text.
The agent should pick from a known document index before it answers.

The editable source documents live in `docs/policies`.
Students can update the markdown files, then run:

```bash
uv run python -m support_agent_app.ingest_policies --dry-run
DATABASE_URL="postgresql://..." uv run --extra db python -m support_agent_app.ingest_policies
```

Vector search is still useful to understand, and the course teaches it.
It is not the default path for the finished support assistant because this domain has a small, known set of policy documents.

Use normal relational tables for state.
Use events for audit and debugging.

## Evals

The first eval system should be spreadsheet-shaped.

Use sample email rows with expected outcomes:

```text
id
email_subject
email_body
expected_category
expected_label
expected_document_id
expected_should_reply
expected_key_points
```

The eval runner should pass each email through the support processor and write actual outcomes:

```text
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

The system can automatically check labels, selected documents, reply presence, and simple required phrases.
Humans should manually review answer quality, groundedness, tone, and whether they would send the reply to a customer.

This keeps evals concrete.
Students can see the test cases, run the workflow, and inspect the failures.

LLM-as-judge can be introduced later as an extension, but the course should start with explicit sample data and manual review.

## Observability

The final app should show:

- structured logs for each ticket
- traces for model calls and tool calls
- cost records for model and embedding calls
- eval results for known support questions
- escalation rate
- answer rate
- retrieval quality signals

The course should keep returning to this idea:

> Generation is cheap.
> Verification is the product work.
