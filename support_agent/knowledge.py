from __future__ import annotations

from support_agent.domain import SupportDoc


SUPPORT_DOCS = [
    SupportDoc(
        doc_id="refund-policy",
        title="Refund Policy",
        body=(
            "Customers can request a refund within 14 days of purchase. "
            "Refund questions that require account changes should be reviewed by a human."
        ),
    ),
    SupportDoc(
        doc_id="setup-guide",
        title="Setup Guide",
        body=(
            "Customers can set up the product by creating an account, choosing a workspace, "
            "and inviting their team members."
        ),
    ),
    SupportDoc(
        doc_id="account-access",
        title="Account Access",
        body=(
            "For login issues, ask the customer to use the password reset flow. "
            "Do not change account access without human approval."
        ),
    ),
]

STOP_WORDS = {
    "a",
    "an",
    "and",
    "before",
    "can",
    "i",
    "is",
    "me",
    "my",
    "the",
    "to",
    "up",
    "you",
    "your",
}


def search_support_docs(query: str, limit: int = 2) -> list[SupportDoc]:
    query_terms = {
        term.strip("?.!,")
        for term in query.lower().split()
        if term.strip("?.!,") and term.strip("?.!,") not in STOP_WORDS
    }
    scored: list[tuple[int, SupportDoc]] = []

    for doc in SUPPORT_DOCS:
        haystack = f"{doc.title} {doc.body}".lower()
        score = sum(1 for term in query_terms if term.strip("?.!,") in haystack)
        scored.append((score, doc))

    matches = [doc for score, doc in sorted(scored, key=lambda row: row[0], reverse=True) if score > 0]
    return matches[:limit]


def format_docs(docs: list[SupportDoc]) -> str:
    if not docs:
        return "No support docs found."

    return "\n\n".join(f"[{doc.doc_id}] {doc.title}\n{doc.body}" for doc in docs)
