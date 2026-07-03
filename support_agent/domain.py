from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TicketCategory(str, Enum):
    GENERAL_SUPPORT = "general_support"
    REFUND_POLICY = "refund_policy"
    ACCOUNT_ACCESS = "account_access"
    HUMAN_REVIEW = "human_review"


class TicketAction(str, Enum):
    DRAFT_REPLY = "draft_reply"
    HUMAN_REVIEW = "human_review"


@dataclass(frozen=True)
class Ticket:
    sender: str
    subject: str
    body: str


@dataclass(frozen=True)
class Classification:
    category: TicketCategory
    action: TicketAction
    confidence: float
    reason: str

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Classification":
        category = TicketCategory(str(data["category"]))
        action = TicketAction(str(data["action"]))
        confidence = float(data["confidence"])
        reason = str(data["reason"])

        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

        return cls(
            category=category,
            action=action,
            confidence=confidence,
            reason=reason,
        )


@dataclass(frozen=True)
class SupportDoc:
    doc_id: str
    title: str
    body: str


@dataclass(frozen=True)
class DraftReply:
    body: str
    citations: list[str]


@dataclass(frozen=True)
class WorkflowResult:
    classification: Classification
    docs: list[SupportDoc]
    draft: DraftReply | None
    escalated: bool
    reason: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentStep:
    thought: str
    tool_call: ToolCall | None
    observation: str | None = None


@dataclass(frozen=True)
class AgentResult:
    final_answer: str
    steps: list[AgentStep]
    escalated: bool

