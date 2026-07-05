"""
First ADK Agent

This file keeps the tools local so the lesson is easy to follow.
The deployable app later moves the same ideas into support_agent_app.
"""

from __future__ import annotations

from pydantic import BaseModel


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
        summary="Return opened, unused items within 30 days.",
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
        summary="Standard shipping and tracking guidance.",
        body=(
            "Standard shipping usually takes 3 to 5 business days in the UK "
            "and 7 to 14 business days for international orders."
        ),
        keywords=["shipping", "delivery", "tracking", "package"],
    ),
]


def list_support_documents() -> list[dict[str, str]]:
    return [
        {
            "id": document.id,
            "title": document.title,
            "summary": document.summary,
        }
        for document in SUPPORT_DOCUMENTS
    ]


def find_support_document(query: str) -> dict[str, str | bool]:
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


def main() -> None:
    print("Support document index:")
    for doc in list_support_documents():
        print(f"- {doc['id']}: {doc['summary']}")

    print()
    print("Example tool lookup:")
    result = find_support_document("What is your returns policy?")
    print(result)

    print()
    print("ADK version:")
    print("Use these same two functions as ADK tools in the next app module.")
    print("The idea is the same: define tools, give them to the agent, then let the agent call them.")


if __name__ == "__main__":
    main()
