from __future__ import annotations

from dataclasses import dataclass

from support_agent_app.services.document_registry import find_support_document
from support_agent_app.services.labels import decide_gmail_label


@dataclass(frozen=True)
class ProcessedSupportEmail:
    label: str
    reason: str
    document_id: str | None


def process_support_email(question: str) -> ProcessedSupportEmail:
    result = find_support_document(question)
    if not result["found"]:
        label = decide_gmail_label(answerable=False, reason=str(result["reason"]))
        return ProcessedSupportEmail(label=label["label"], reason=label["reason"], document_id=None)

    document = result["document"]
    label = decide_gmail_label(answerable=True, reason=f"Answered from {document['id']}")
    return ProcessedSupportEmail(
        label=label["label"],
        reason=label["reason"],
        document_id=str(document["id"]),
    )

