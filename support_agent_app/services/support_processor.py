from __future__ import annotations

from dataclasses import dataclass

from support_agent_app.services.document_registry import find_support_document
from support_agent_app.services.labels import decide_gmail_label


@dataclass(frozen=True)
class ProcessedSupportEmail:
    label: str
    reason: str
    document_id: str | None
    draft_reply: str | None


@dataclass(frozen=True)
class ReplyCheck:
    approved: bool
    reason: str


def process_support_email(question: str) -> ProcessedSupportEmail:
    result = find_support_document(question)
    if not result["found"]:
        label = decide_gmail_label(answerable=False, reason=str(result["reason"]))
        return ProcessedSupportEmail(
            label=label["label"],
            reason=label["reason"],
            document_id=None,
            draft_reply=None,
        )

    document = result["document"]
    draft_reply = draft_support_reply(question, document)
    check = check_reply(draft_reply, document)
    if not check.approved:
        label = decide_gmail_label(answerable=False, reason=check.reason)
        return ProcessedSupportEmail(
            label=label["label"],
            reason=label["reason"],
            document_id=str(document["id"]),
            draft_reply=draft_reply,
        )

    label = decide_gmail_label(answerable=True, reason=check.reason)
    return ProcessedSupportEmail(
        label=label["label"],
        reason=label["reason"],
        document_id=str(document["id"]),
        draft_reply=draft_reply,
    )


def draft_support_reply(question: str, document: dict[str, object]) -> str:
    """Draft a small grounded reply for local smoke tests and early lessons."""
    title = str(document["title"])
    summary = str(document["summary"])
    return (
        "Thanks for getting in touch.\n\n"
        f"Based on our {title}, {summary}\n\n"
        "If your situation includes private account details or an order-specific change, "
        "a support teammate should review it before we take action."
    )


def check_reply(reply: str, document: dict[str, object]) -> ReplyCheck:
    title = str(document["title"])
    if title not in reply:
        return ReplyCheck(approved=False, reason="Draft did not cite the selected policy.")

    if not reply.strip():
        return ReplyCheck(approved=False, reason="Draft reply was empty.")

    return ReplyCheck(approved=True, reason=f"Drafted and checked reply from {document['id']}")
