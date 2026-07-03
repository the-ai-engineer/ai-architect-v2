# Final Agent Spec

## Product

The finished application is an AI customer support agent.

A customer sends an email to a support inbox.
The system reads the message, creates a ticket, searches trusted support docs, drafts an answer, and either replies by email or escalates to a human.

The course uses email because it makes the demo real.
The same backend shape could sit behind Zendesk, Intercom, HelpScout, Slack, a chat widget, or a custom ticketing UI.

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
5. The ADK support agent searches the support knowledge base.
6. OpenAI drafts a grounded answer.
7. Guardrails decide whether the answer is safe to send.
8. Gmail sends the reply or the app creates a human review item.
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
  -> ADK support agent
      -> classify question
      -> search support docs
      -> draft answer
      -> check answer
      -> send reply or escalate
  -> Gmail reply
  -> logs, traces, evals, and metrics
```

## Technology Choices

Use OpenAI as the default model provider.
It is the cleanest teaching path for model calls, structured outputs, embeddings, answer generation, and evals.

Use Google Cloud as the default deployment target.
It is the best fit for Gmail, Pub/Sub, Cloud Run, Cloud SQL, Cloud Trace, Cloud Logging, and Cloud Monitoring.

Use ADK from lesson 5 onward.
Students first build an agent by hand so they understand the loop.
Then ADK becomes the production framework for the rest of the course.

## Core Components

| Component | Responsibility |
|---|---|
| `TicketStore` | Store incoming support tickets and their status |
| `KnowledgeBase` | Store markdown docs, chunks, and embeddings |
| `SupportAgent` | Decide which tools to call and when to escalate |
| `search_support_docs` | Retrieve support docs for RAG |
| `draft_support_reply` | Draft an answer grounded in retrieved context |
| `check_reply` | Decide whether the answer is safe enough to send |
| `send_email_reply` | Send a Gmail reply when approved |
| `create_human_review` | Escalate uncertain or risky tickets |
| `RunLogger` | Record events, traces, model calls, and tool calls |

## Human Escalation

The assistant escalates when:

- no relevant docs are found
- retrieved docs conflict
- the question requires private account data
- the question asks for a refund or account change
- the model confidence is low
- the draft contains unsupported claims
- a send action fails

Human escalation is part of the product.
It is not a failure case.

## Data Model

Start with these tables in the production app:

```text
tickets
ticket_messages
support_docs
support_doc_chunks
draft_replies
human_reviews
agent_runs
tool_calls
model_calls
events
eval_cases
eval_runs
eval_results
```

Use pgvector for document chunk embeddings.

Use normal relational tables for state.
Use events for audit and debugging.

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

