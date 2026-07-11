from __future__ import annotations

import os
from pathlib import Path
import unittest
from unittest.mock import patch

from pydantic_ai.models import infer_model

from support_agent_app.config import _normalize_model_name
from support_agent_app.services.document_registry import (
    find_support_document,
    list_support_documents,
    load_policy_documents,
    load_support_documents,
)
from support_agent_app.services.labels import decide_gmail_label
from support_agent_app.services.support_processor import process_support_email


class LessonExamplesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env_patcher = patch.dict(os.environ, {"DATABASE_URL": ""})
        self.env_patcher.start()
        self.addCleanup(self.env_patcher.stop)

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

    def test_first_framework_agent_uses_pydantic_ai_with_direct_providers(self) -> None:
        source = Path("examples/05_first_framework_agent.py").read_text(encoding="utf-8")

        self.assertIn("from pydantic_ai import Agent", source)
        self.assertIn('OPENAI_MODEL = "openai:gpt-5.6"', source)
        self.assertIn('CLAUDE_MODEL = "anthropic:claude-sonnet-4-6"', source)
        self.assertIn("support_agent = Agent(", source)
        self.assertIn("tools=[list_support_documents, find_support_document]", source)
        self.assertIn("defer_model_check=True", source)
        self.assertNotIn("LiteLlm", source)
        self.assertNotIn("google.adk", source)

    def test_pydantic_ai_resolves_openai_and_anthropic_models(self) -> None:
        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test", "ANTHROPIC_API_KEY": "test"},
        ):
            openai_model = infer_model("openai:gpt-5.6")
            anthropic_model = infer_model("anthropic:claude-sonnet-4-6")

        self.assertEqual(type(openai_model).__name__, "OpenAIResponsesModel")
        self.assertEqual(type(anthropic_model).__name__, "AnthropicModel")

    def test_legacy_model_name_is_normalized(self) -> None:
        self.assertEqual(_normalize_model_name("openai/gpt-5.5"), "openai:gpt-5.5")
        self.assertEqual(
            _normalize_model_name("anthropic/claude-sonnet-4-6"),
            "anthropic:claude-sonnet-4-6",
        )

    def test_sql_rag_matches_support_document_schema(self) -> None:
        source = Path("examples/06b_sql_rag.py").read_text(encoding="utf-8")

        self.assertIn("category", source)
        self.assertIn("keywords", source)
        self.assertIn("is_active = true", source)

    def test_document_registry_finds_returns_policy(self) -> None:
        result = find_support_document("What is your returns policy?")

        self.assertTrue(result["found"])
        self.assertEqual(result["document"]["id"], "refund-policy")

    def test_document_registry_uses_postgres_when_database_url_is_set(self) -> None:
        with patch(
            "support_agent_app.services.document_registry.load_support_documents_from_postgres"
        ) as load_from_postgres:
            load_from_postgres.return_value = []

            documents = load_support_documents("postgresql://localhost/ai_architect")

        self.assertEqual(documents, [])
        load_from_postgres.assert_called_once_with("postgresql://localhost/ai_architect")

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
        self.assertIsNotNone(result.draft_reply)
        self.assertIn("Refund Policy", result.draft_reply or "")

    def test_app_process_support_email_escalates_off_topic_questions(self) -> None:
        result = process_support_email("Explain quantum entanglement and black hole evaporation.")

        self.assertEqual(result.label, "Human Needed")
        self.assertIsNone(result.document_id)
        self.assertIsNone(result.draft_reply)


if __name__ == "__main__":
    unittest.main()
