from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from support_agent_app.config import AppConfig


STOPWORDS = {
    "about",
    "after",
    "all",
    "and",
    "are",
    "can",
    "could",
    "for",
    "from",
    "has",
    "have",
    "how",
    "into",
    "not",
    "the",
    "this",
    "what",
    "when",
    "where",
    "with",
    "would",
    "you",
    "your",
}

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


def load_support_documents(database_url: str | None = None) -> list[SupportDocument]:
    config = AppConfig.from_env()
    database_url = database_url if database_url is not None else config.database_url

    if database_url:
        return load_support_documents_from_postgres(database_url)

    return load_policy_documents(config.policy_dir)


def load_support_documents_from_postgres(database_url: str) -> list[SupportDocument]:
    import psycopg

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, title, category, summary, body, keywords
                from support_documents
                where is_active
                order by id;
                """
            )
            rows = cur.fetchall()

    return [
        SupportDocument(
            id=row[0],
            title=row[1],
            category=row[2],
            summary=row[3],
            body=row[4],
            keywords=tuple(row[5]),
        )
        for row in rows
    ]


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
        for doc in load_support_documents()
    ]


def find_support_document(query: str) -> dict[str, object]:
    """Find the most relevant support document from the registry."""
    query_terms = _extract_search_terms(query)
    documents = load_support_documents()

    if not documents:
        return {
            "found": False,
            "reason": "No support documents are available.",
            "document": None,
        }

    scored = []
    for doc in documents:
        searchable = _document_search_terms(doc)
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


def _extract_search_terms(text: str) -> set[str]:
    return {
        term.strip("?.!,;:()[]{}\"'").lower()
        for term in text.split()
        if _is_search_term(term.strip("?.!,;:()[]{}\"'").lower())
    }


def _is_search_term(term: str) -> bool:
    return len(term) > 2 and term not in STOPWORDS


def _document_search_terms(document: SupportDocument) -> set[str]:
    searchable_text = " ".join(
        (
            document.category,
            document.title,
            document.summary,
            " ".join(document.keywords),
        )
    )
    return _extract_search_terms(searchable_text)
