from __future__ import annotations

from pathlib import Path
import unittest

from support_agent_app.services.document_registry import (
    find_support_document,
    list_support_documents,
    load_policy_documents,
)
from support_agent_app.services.labels import decide_gmail_label
from support_agent_app.services.support_processor import process_support_email


class LessonExamplesTest(unittest.TestCase):
    def test_legacy_support_agent_package_was_removed(self) -> None:
        self.assertFalse(Path("support_agent").exists())

    def test_standalone_examples_do_not_import_shared_packages(self) -> None:
        for path in sorted(Path("examples").glob("*.py")):
            source = path.read_text(encoding="utf-8")

            self.assertNotIn("from support_agent", source, msg=str(path))
            self.assertNotIn("import support_agent", source, msg=str(path))
            self.assertNotIn("from support_agent_app", source, msg=str(path))
            self.assertNotIn("import support_agent_app", source, msg=str(path))

    def test_vector_examples_use_postgres(self) -> None:
        for path in [Path("examples/07a_vector_rag.py"), Path("examples/07b_hybrid_rag.py")]:
            source = path.read_text(encoding="utf-8")

            self.assertIn("psycopg.connect", source, msg=str(path))
            self.assertIn("create extension if not exists vector", source, msg=str(path))
            self.assertIn("create table if not exists documents", source, msg=str(path))
            self.assertIn("<=>", source, msg=str(path))
            self.assertNotIn("lesson_", source, msg=str(path))
            self.assertNotIn("from collections import Counter", source, msg=str(path))
            self.assertNotIn("cosine_similarity", source, msg=str(path))

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
