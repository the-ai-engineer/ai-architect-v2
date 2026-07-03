from __future__ import annotations

from pathlib import Path

from support_agent_app.services.document_registry import SupportDocument, load_policy_documents


UPSERT_DOCUMENT_SQL = """
insert into support_documents (
    id,
    title,
    category,
    summary,
    body,
    keywords,
    updated_at
)
values (%s, %s, %s, %s, %s, %s, now())
on conflict (id) do update set
    title = excluded.title,
    category = excluded.category,
    summary = excluded.summary,
    body = excluded.body,
    keywords = excluded.keywords,
    is_active = true,
    updated_at = now();
"""


def load_documents_for_ingest(policy_dir: Path) -> list[SupportDocument]:
    return load_policy_documents(policy_dir)


def ingest_documents(database_url: str, documents: list[SupportDocument]) -> None:
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Install Postgres dependencies with `pip install -e '.[db]'`.") from exc

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            for doc in documents:
                cur.execute(
                    UPSERT_DOCUMENT_SQL,
                    (
                        doc.id,
                        doc.title,
                        doc.category,
                        doc.summary,
                        doc.body,
                        list(doc.keywords),
                    ),
                )

