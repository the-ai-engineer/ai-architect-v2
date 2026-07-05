"""
Vector RAG

This shows the shape of vector search without needing an embedding API key.
The fake embed function turns text into token counts so the example stays local.
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
            )
        )

    return documents


def extract_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()

    return fallback


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
