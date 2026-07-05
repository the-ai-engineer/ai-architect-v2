from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TicketCategory(str, Enum):
    GENERAL_SUPPORT = "general_support"
    REFUND_POLICY = "refund_policy"
    ACCOUNT_ACCESS = "account_access"
    HUMAN_REVIEW = "human_review"


class TicketAction(str, Enum):
    DRAFT_REPLY = "draft_reply"
    HUMAN_REVIEW = "human_review"


class CourseModel(BaseModel):
    """Base model for small teaching data types."""

    model_config = ConfigDict(frozen=True)


class Ticket(CourseModel):
    sender: str
    subject: str
    body: str


class Classification(CourseModel):
    category: TicketCategory
    action: TicketAction
    confidence: float
    reason: str

    @field_validator("confidence")
    @classmethod
    def confidence_must_be_probability(cls, value: float) -> float:
        if not 0 <= value <= 1:
            raise ValueError("confidence must be between 0 and 1")
        return value

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Classification":
        return cls(
            category=TicketCategory(str(data["category"])),
            action=TicketAction(str(data["action"])),
            confidence=float(data["confidence"]),
            reason=str(data["reason"]),
        )


class SupportDoc(CourseModel):
    doc_id: str
    title: str
    body: str


class DraftReply(CourseModel):
    body: str
    citations: list[str]


class WorkflowResult(CourseModel):
    classification: Classification
    docs: list[SupportDoc]
    draft: DraftReply | None
    escalated: bool
    reason: str


class ToolCall(CourseModel):
    name: str
    arguments: dict[str, str] = Field(default_factory=dict)


class AgentStep(CourseModel):
    thought: str
    tool_call: ToolCall | None
    observation: str | None = None


class AgentResult(CourseModel):
    final_answer: str
    steps: list[AgentStep]
    escalated: bool
