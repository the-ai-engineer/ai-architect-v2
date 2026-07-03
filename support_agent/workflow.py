from __future__ import annotations

from support_agent.domain import Classification, DraftReply, Ticket, TicketAction, WorkflowResult
from support_agent.knowledge import search_support_docs
from support_agent.model_client import FakeModelClient


def draft_reply(ticket: Ticket, docs: list) -> DraftReply:
    citations = [doc.doc_id for doc in docs]
    context = docs[0].body if docs else ""

    body = (
        f"Hi,\n\nThanks for getting in touch. {context}\n\n"
        "If this does not answer your question, I will pass this to the team.\n\n"
        "Best,\nSupport"
    )
    return DraftReply(body=body, citations=citations)


def run_support_workflow(
    ticket: Ticket,
    model: FakeModelClient | None = None,
) -> WorkflowResult:
    model = model or FakeModelClient()
    classification = Classification.from_dict(model.classify_ticket(ticket.body))

    if classification.action == TicketAction.HUMAN_REVIEW:
        return WorkflowResult(
            classification=classification,
            docs=[],
            draft=None,
            escalated=True,
            reason=classification.reason,
        )

    docs = search_support_docs(ticket.body)
    if not docs:
        return WorkflowResult(
            classification=classification,
            docs=[],
            draft=None,
            escalated=True,
            reason="No relevant support docs were found.",
        )

    return WorkflowResult(
        classification=classification,
        docs=docs,
        draft=draft_reply(ticket, docs),
        escalated=False,
        reason="Drafted a grounded support reply.",
    )

