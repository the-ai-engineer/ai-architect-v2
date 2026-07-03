from __future__ import annotations

import argparse
from pathlib import Path

from support_agent_app.config import AppConfig
from support_agent_app.services.document_registry import SupportDocument
from support_agent_app.services.policy_ingestion import ingest_documents, load_documents_for_ingest


def main() -> None:
    config = AppConfig.from_env()
    parser = argparse.ArgumentParser(description="Ingest support policy markdown into Postgres.")
    parser.add_argument(
        "policy_dir",
        nargs="?",
        default=str(config.policy_dir),
        help="Directory containing policy markdown files.",
    )
    parser.add_argument(
        "--database-url",
        default=config.database_url,
        help="Postgres connection string. Defaults to DATABASE_URL.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse files and print what would be ingested without writing to Postgres.",
    )
    args = parser.parse_args()

    documents = load_documents_for_ingest(Path(args.policy_dir))

    if args.dry_run or not args.database_url:
        print_dry_run(documents)
        if not args.database_url:
            print()
            print("Set DATABASE_URL to ingest these documents into Postgres.")
        return

    ingest_documents(args.database_url, documents)
    print(f"Ingested {len(documents)} support documents.")


def print_dry_run(documents: list[SupportDocument]) -> None:
    print(f"Parsed {len(documents)} support documents:")
    for doc in documents:
        print(f"- {doc.id} [{doc.category}]: {doc.title}")


if __name__ == "__main__":
    main()

