"""
Hybrid RAG

Hybrid search combines keyword matching and vector-style similarity.
This example stays self-contained so it is easy to teach from one file.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path

from pydantic import BaseModel


POLICY_DIR = Path("docs/policies")


class SupportDocument(BaseModel):
    id: str
    title: str
    body: str
    keywords: list[str]


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 07B: hybrid search over support policies.")
    parser.add_argument("question", nargs="?", default="My package tracking has not updated.")
    args = parser.parse_args()

    documents = load_policy_documents()
    ranked = sorted(
        ((hybrid_score(args.question, document), document) for document in documents),
        key=lambda row: row[0],
        reverse=True,
    )

    print(f"Question: {args.question}")
    print()
    for score, document in ranked[:3]:
        print(f"{score:.3f} {document.id}: {document.title}")


def load_policy_documents() -> list[SupportDocument]:
    documents = []

    for path in sorted(POLICY_DIR.glob("*.md")):
        if path.name == "README.md":
            continue

        body = path.read_text(encoding="utf-8").strip()
        documents.append(
            SupportDocument(
                id=path.stem,
                title=extract_title(body, path.stem),
                body=body,
                keywords=extract_keywords(path.stem),
            )
        )

    return documents


def extract_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()

    return fallback


def extract_keywords(document_id: str) -> list[str]:
    keyword_map = {
        "account-policy": ["account", "login", "password", "access"],
        "opening-hours": ["hours", "support", "weekend", "holiday"],
        "privacy-policy": ["privacy", "data", "delete", "card"],
        "refund-policy": ["refund", "return", "exchange", "opened"],
        "shipping-policy": ["shipping", "delivery", "tracking", "package"],
        "warranty-policy": ["warranty", "fault", "repair", "replacement"],
    }
    return keyword_map.get(document_id, document_id.split("-"))


def hybrid_score(query: str, document: SupportDocument) -> float:
    keyword_score = count_keyword_matches(query, document)
    vector_score = cosine_similarity(embed(query), embed(document.body))
    return keyword_score + vector_score


def count_keyword_matches(query: str, document: SupportDocument) -> float:
    query_terms = {token.strip(".,!?():").lower() for token in query.split()}
    matches = query_terms.intersection(set(document.keywords))
    return float(len(matches))


def embed(text: str) -> Counter[str]:
    tokens = [token.strip(".,!?():").lower() for token in text.split()]
    return Counter(token for token in tokens if len(token) > 3)


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    terms = set(left) | set(right)
    numerator = sum(left[term] * right[term] for term in terms)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0

    return numerator / (left_norm * right_norm)


if __name__ == "__main__":
    main()
