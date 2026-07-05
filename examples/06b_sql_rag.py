from __future__ import annotations

from support_agent_app.config import AppConfig
from support_agent_app.services.policy_ingestion import UPSERT_DOCUMENT_SQL, load_documents_for_ingest


def main() -> None:
    config = AppConfig.from_env()
    documents = load_documents_for_ingest(config.policy_dir)

    print("Lesson 06B: SQL RAG")
    print()
    print("In production these markdown files become rows in Postgres.")
    print(f"Policy directory: {config.policy_dir}")
    print(f"Documents parsed: {len(documents)}")
    print()
    print("Upsert shape:")
    print(UPSERT_DOCUMENT_SQL.strip())


if __name__ == "__main__":
    main()
