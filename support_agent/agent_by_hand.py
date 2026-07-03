from __future__ import annotations

from support_agent.domain import AgentResult, AgentStep, Ticket, ToolCall
from support_agent.knowledge import format_docs, search_support_docs
from support_agent.workflow import draft_reply


def run_agent_by_hand(ticket: Ticket) -> AgentResult:
    steps: list[AgentStep] = []

    search_call = ToolCall(name="search_support_docs", arguments={"query": ticket.body})
    docs = search_support_docs(ticket.body)
    steps.append(
        AgentStep(
            thought="I need trusted support context before answering.",
            tool_call=search_call,
            observation=format_docs(docs),
        )
    )

    if not docs:
        review_call = ToolCall(
            name="create_human_review",
            arguments={"reason": "No relevant docs found."},
        )
        steps.append(
            AgentStep(
                thought="I cannot answer safely without evidence.",
                tool_call=review_call,
                observation="Human review created.",
            )
        )
        return AgentResult(
            final_answer="I escalated this ticket because no relevant support docs were found.",
            steps=steps,
            escalated=True,
        )

    reply = draft_reply(ticket, docs)
    draft_call = ToolCall(
        name="draft_support_reply",
        arguments={"citations": ", ".join(reply.citations)},
    )
    steps.append(
        AgentStep(
            thought="I found enough context to draft a support reply.",
            tool_call=draft_call,
            observation=reply.body,
        )
    )

    return AgentResult(
        final_answer=reply.body,
        steps=steps,
        escalated=False,
    )

