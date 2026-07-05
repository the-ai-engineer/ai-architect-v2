from __future__ import annotations

from support_agent.domain import Classification, TicketAction, TicketCategory


class FakeModelClient:
    """Deterministic stand-in for examples and tests."""

    def complete(self, prompt: str) -> str:
        if "refund" in prompt.lower():
            return "I can help explain the refund policy from the support docs."

        return "I can help answer this support question from the knowledge base."

    def classify_ticket(self, body: str) -> dict[str, object]:
        text = body.lower()

        if any(term in text for term in ["refund", "cancel", "money back"]):
            classification = Classification(
                category=TicketCategory.REFUND_POLICY,
                action=TicketAction.DRAFT_REPLY,
                confidence=0.91,
                reason="The customer is asking about refund policy.",
            )
            return _classification_dict(classification)

        if any(term in text for term in ["password", "login", "account"]):
            classification = Classification(
                category=TicketCategory.ACCOUNT_ACCESS,
                action=TicketAction.HUMAN_REVIEW,
                confidence=0.78,
                reason="Account access questions need careful handling.",
            )
            return _classification_dict(classification)

        classification = Classification(
            category=TicketCategory.GENERAL_SUPPORT,
            action=TicketAction.DRAFT_REPLY,
            confidence=0.86,
            reason="The customer is asking a general support question.",
        )
        return _classification_dict(classification)


class OpenAITextClient:
    """Small OpenAI wrapper used only when students opt into a real API call."""

    def __init__(self, model: str = "gpt-5.5") -> None:
        self.model = model

    def complete(self, prompt: str) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Install dependencies with `pip install -e .`."
            ) from exc

        client = OpenAI()
        response = client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text


def _classification_dict(classification: Classification) -> dict[str, object]:
    return {
        "category": classification.category.value,
        "action": classification.action.value,
        "confidence": classification.confidence,
        "reason": classification.reason,
    }
