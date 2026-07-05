from __future__ import annotations

from typing import Any

from support_agent_app.config import AppConfig
from support_agent_app.services.document_registry import find_support_document, list_support_documents
from support_agent_app.services.labels import decide_gmail_label


SUPPORT_AGENT_INSTRUCTION = """
You are a customer support agent for a small business.

Your job is to answer common support questions using trusted support documents.

Rules:
- Use list_support_documents to inspect the document index.
- Use find_support_document before answering a customer question.
- Only answer from the support document returned by the tool.
- If no document is found, do not answer.
- If the question is off topic, sensitive, account-specific, or asks for private data, do not answer.
- Use decide_gmail_label with answerable=false when a human should handle the message.
- Use decide_gmail_label with answerable=true only when you have answered from trusted context.
- Keep replies short, clear, and polite.
"""


def build_support_agent(config: AppConfig | None = None) -> Any:
    """Build the ADK support agent."""
    from google.adk import Agent
    from google.adk.models.lite_llm import LiteLlm

    config = config or AppConfig.from_env()
    return Agent(
        name="support_agent",
        model=LiteLlm(model=config.model_name),
        description="Answers safe customer support questions from a Postgres-backed document registry.",
        instruction=SUPPORT_AGENT_INSTRUCTION,
        tools=[
            list_support_documents,
            find_support_document,
            decide_gmail_label,
        ],
    )


root_agent = build_support_agent()
