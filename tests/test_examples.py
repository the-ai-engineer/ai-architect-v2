from __future__ import annotations

import unittest

from support_agent.agent_by_hand import run_agent_by_hand
from support_agent.domain import Classification, Ticket, TicketAction, TicketCategory
from support_agent.model_client import FakeModelClient
from support_agent.workflow import run_support_workflow
from support_agent_app.services.document_registry import (
    find_support_document,
    list_support_documents,
    load_policy_documents,
)
from support_agent_app.services.labels import decide_gmail_label
from support_agent_app.services.support_processor import process_support_email


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

    def test_document_registry_finds_returns_policy(self) -> None:
        result = find_support_document("What is your returns policy?")

        self.assertTrue(result["found"])
        self.assertEqual(result["document"]["id"], "refund-policy")

    def test_document_registry_returns_index(self) -> None:
        index = list_support_documents()

        self.assertGreaterEqual(len(index), 6)
        self.assertIn("summary", index[0])

    def test_policy_documents_load_from_markdown(self) -> None:
        documents = load_policy_documents()
        ids = {document.id for document in documents}

        self.assertIn("refund-policy", ids)
        self.assertIn("shipping-policy", ids)
        self.assertIn("privacy-policy", ids)
        self.assertIn("opening-hours", ids)

    def test_gmail_label_decision(self) -> None:
        self.assertEqual(
            decide_gmail_label(answerable=True, reason="Answered from returns policy")["label"],
            "AI Answered",
        )
        self.assertEqual(
            decide_gmail_label(answerable=False, reason="Private account question")["label"],
            "Human Needed",
        )

    def test_app_process_support_email_returns_label(self) -> None:
        result = process_support_email("Can I return an opened item?")

        self.assertEqual(result.label, "AI Answered")
        self.assertEqual(result.document_id, "refund-policy")


if __name__ == "__main__":
    unittest.main()
