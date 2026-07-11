"""
First ADK Agent

Move the same document lookup tools from the hand-built agent into ADK.
ADK expects a root_agent object that the CLI or web UI can load.
"""

from __future__ import annotations

from pydantic import BaseModel

try:
    from google.adk.agents.llm_agent import Agent
    from google.adk.models.lite_llm import LiteLlm
except ImportError:  # pragma: no cover - exercised by running without the adk extra.
    Agent = None
    LiteLlm = None


MODEL_NAME = "openai/gpt-5.6"


class SupportDocument(BaseModel):
    id: str
    title: str
    summary: str
    body: str
    keywords: list[str]


SUPPORT_DOCUMENTS = [
    SupportDocument(
        id="refund-policy",
        title="Refund Policy",
        summary="Opened, unused items can usually be returned within 30 days.",
        body=(
            "Customers can return most items within 30 days of delivery. "
            "Opened items can be returned if they are complete, undamaged, "
            "and have only been inspected in a normal way."
        ),
        keywords=["refund", "return", "opened", "exchange"],
    ),
    SupportDocument(
        id="shipping-policy",
        title="Shipping Policy",
        summary="Standard shipping times and tracking guidance.",
        body=(
            "Standard shipping usually takes 3 to 5 business days in the UK "
            "and 7 to 14 business days for international orders."
        ),
        keywords=["shipping", "delivery", "tracking", "package"],
    ),
]


def list_support_documents() -> list[dict[str, str]]:
    """Return the policy index the agent should inspect before answering."""
    return [
        {
            "id": document.id,
            "title": document.title,
            "summary": document.summary,
        }
        for document in SUPPORT_DOCUMENTS
    ]


def find_support_document(query: str) -> dict[str, str | bool]:
    """Return the best matching policy document for a support question."""
    normalized_query = query.lower()

    for document in SUPPORT_DOCUMENTS:
        if any(keyword in normalized_query for keyword in document.keywords):
            return {
                "found": True,
                "id": document.id,
                "title": document.title,
                "body": document.body,
            }

    return {"found": False, "reason": "No matching support document was found."}


def build_root_agent():
    if Agent is None or LiteLlm is None:
        return None

    return Agent(
        model=LiteLlm(model=MODEL_NAME),
        name="support_agent",
        description="Answers simple support questions from approved policy documents.",
        instruction=(
            "You are a customer support agent.\n"
            "Use list_support_documents before choosing a policy.\n"
            "Use find_support_document before answering.\n"
            "Answer only from the returned policy document.\n"
            "If no policy matches, say a human should handle the message."
        ),
        tools=[list_support_documents, find_support_document],
    )


root_agent = build_root_agent()


def main() -> None:
    if root_agent is None:
        print("Install ADK to run this lesson:")
        print("uv run --extra adk python examples/05_first_adk_agent.py")
        return

    print(f"ADK agent: {root_agent.name}")
    print(f"Model: {MODEL_NAME}")
    print("Tools:")
    for tool in root_agent.tools:
        print(f"- {tool.__name__}")
    print()
    print("The deployable app uses this same root_agent pattern in support_agent_app/agent.py.")


if __name__ == "__main__":
    main()
