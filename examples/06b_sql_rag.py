"""
SQL RAG

Turn markdown support policies into rows that can be stored in Postgres.
This file only prints the insert shape.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


POLICY_DIR = Path("docs/policies")


UPSERT_DOCUMENT_SQL = """
insert into support_documents (
    id,
    title,
    summary,
    body,
    updated_at
)
values (%s, %s, %s, %s, now())
on conflict (id) do update set
    title = excluded.title,
    summary = excluded.summary,
    body = excluded.body,
    updated_at = now();
"""


class SupportDocument(BaseModel):
    id: str
    title: str
    summary: str
    body: str


def main() -> None:
    documents = load_policy_documents()

    print("Lesson 06B: SQL RAG")
    print()
    print("In production these markdown files become rows in Postgres.")
    print(f"Policy directory: {POLICY_DIR}")
    print(f"Documents parsed: {len(documents)}")
    print()
    print("Example row:")
    print(
        {
            "id": documents[0].id,
            "title": documents[0].title,
            "summary": documents[0].summary,
            "body": documents[0].body[:120] + "...",
        }
    )
    print()
    print("Upsert shape:")
    print(UPSERT_DOCUMENT_SQL.strip())


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
                summary=extract_summary(body),
                body=body,
            )
        )

    return documents


def extract_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()

    return fallback


def extract_summary(markdown: str) -> str:
    paragraph = []

    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("Last updated:"):
            if paragraph:
                break
            continue

        paragraph.append(stripped)

    return " ".join(paragraph)


if __name__ == "__main__":
    main()
