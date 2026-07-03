from __future__ import annotations

import unittest

from support_agent.agent_by_hand import run_agent_by_hand
from support_agent.domain import Classification, Ticket, TicketAction, TicketCategory
from support_agent.model_client import FakeModelClient
from support_agent.workflow import run_support_workflow


class LessonExamplesTest(unittest.TestCase):
    def test_structured_output_classifies_refund_question(self) -> None:
        raw = FakeModelClient().classify_ticket("Can I get a refund?")
        classification = Classification.from_dict(raw)

        self.assertEqual(classification.category, TicketCategory.REFUND_POLICY)
        self.assertEqual(classification.action, TicketAction.DRAFT_REPLY)
        self.assertGreater(classification.confidence, 0.8)

    def test_workflow_drafts_reply_when_docs_are_found(self) -> None:
        ticket = Ticket(
            sender="customer@example.com",
            subject="Refund question",
            body="Can you explain your refund policy?",
        )

        result = run_support_workflow(ticket)

        self.assertFalse(result.escalated)
        self.assertIsNotNone(result.draft)
        self.assertEqual(result.draft.citations, ["refund-policy"])

    def test_workflow_escalates_account_access(self) -> None:
        ticket = Ticket(
            sender="customer@example.com",
            subject="Login help",
            body="I cannot log in to my account.",
        )

        result = run_support_workflow(ticket)

        self.assertTrue(result.escalated)
        self.assertIsNone(result.draft)

    def test_agent_by_hand_uses_search_then_draft(self) -> None:
        ticket = Ticket(
            sender="customer@example.com",
            subject="Refund question",
            body="Can you explain your refund policy?",
        )

        result = run_agent_by_hand(ticket)

        self.assertFalse(result.escalated)
        self.assertEqual(result.steps[0].tool_call.name, "search_support_docs")
        self.assertEqual(result.steps[1].tool_call.name, "draft_support_reply")


if __name__ == "__main__":
    unittest.main()

