from __future__ import annotations

import argparse
import math
from collections import Counter

from support_agent_app.services.document_registry import load_policy_documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 07A: vector-search shape without an API key.")
    parser.add_argument("question", nargs="?", default="How long does shipping take to Canada?")
    args = parser.parse_args()

    documents = load_policy_documents()
    query_vector = embed(args.question)
    ranked = sorted(
        ((cosine_similarity(query_vector, embed(document.body)), document) for document in documents),
        key=lambda row: row[0],
        reverse=True,
    )

    print(f"Question: {args.question}")
    print()
    for score, document in ranked[:3]:
        print(f"{score:.3f} {document.id}: {document.title}")


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
