from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from support_agent_app.config import AppConfig


KEYWORDS_BY_CATEGORY = {
    "account": ("account", "login", "password", "access", "guest", "delete", "security"),
    "opening-hours": ("hours", "opening", "support", "available", "weekend", "holiday", "timezone"),
    "privacy": ("privacy", "data", "delete", "marketing", "card", "personal", "security"),
    "refund": ("refund", "return", "returns", "exchange", "money", "credit", "final sale"),
    "shipping": ("shipping", "delivery", "tracking", "package", "address", "courier", "dispatch"),
    "warranty": ("warranty", "fault", "faulty", "repair", "replacement", "defect", "damage"),
}


@dataclass(frozen=True)
class SupportDocument:
    id: str
    title: str
    category: str
    summary: str
    body: str
    keywords: tuple[str, ...]


def load_policy_documents(policy_dir: Path | None = None) -> list[SupportDocument]:
    policy_dir = policy_dir or AppConfig.from_env().policy_dir
    documents = []

    for path in sorted(policy_dir.glob("*.md")):
        if path.name == "README.md":
            continue

        documents.append(parse_policy_document(path))

    return documents


def parse_policy_document(path: Path) -> SupportDocument:
    body = path.read_text(encoding="utf-8").strip()
    lines = body.splitlines()
    title = next((line.removeprefix("# ").strip() for line in lines if line.startswith("# ")), path.stem)
    category = path.stem.removesuffix("-policy")
    summary = _first_body_paragraph(lines)
    keywords = KEYWORDS_BY_CATEGORY.get(category, tuple(category.split("-")))

    return SupportDocument(
        id=path.stem,
        title=title,
        category=category,
        summary=summary,
        body=body,
        keywords=keywords,
    )


def _first_body_paragraph(lines: list[str]) -> str:
    paragraph = []
    started = False

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("Last updated:"):
            if started:
                break
            continue

        started = True
        paragraph.append(stripped)

    return " ".join(paragraph)


def list_support_documents() -> list[dict[str, str]]:
    """Return the document index the agent can inspect before choosing a document."""
    return [
        {
            "id": doc.id,
            "title": doc.title,
            "category": doc.category,
            "summary": doc.summary,
            "keywords": ", ".join(doc.keywords),
        }
        for doc in load_policy_documents()
    ]


def find_support_document(query: str) -> dict[str, object]:
    """Find the most relevant support document from the registry."""
    query_terms = {
        term.strip("?.!,").lower()
        for term in query.split()
        if len(term.strip("?.!,")) > 2
    }

    scored = []
    for doc in load_policy_documents():
        searchable = {
            doc.category,
            *doc.keywords,
            *doc.title.lower().split(),
            *doc.summary.lower().split(),
        }
        score = len(query_terms.intersection(searchable))
        scored.append((score, doc))

    score, best = max(scored, key=lambda row: row[0])
    if score == 0:
        return {
            "found": False,
            "reason": "No matching support document was found.",
            "document": None,
        }

    return {
        "found": True,
        "reason": f"Matched document '{best.title}' with score {score}.",
        "document": {
            "id": best.id,
            "title": best.title,
            "category": best.category,
            "summary": best.summary,
            "body": best.body,
        },
    }

