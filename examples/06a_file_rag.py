from __future__ import annotations

import argparse

from support_agent_app.services.document_registry import find_support_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 06A: simple file RAG.")
    parser.add_argument("question", nargs="?", default="Can I return an opened item?")
    args = parser.parse_args()

    result = find_support_document(args.question)
    if not result["found"]:
        print("No matching policy document found.")
        return

    document = result["document"]
    print(f"Question: {args.question}")
    print(f"Document: {document['title']}")
    print()
    print(document["body"][:800])


if __name__ == "__main__":
    main()
