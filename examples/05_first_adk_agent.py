from __future__ import annotations

from support_agent_app.services.document_registry import find_support_document, list_support_documents


def main() -> None:
    print("Support document index:")
    for doc in list_support_documents():
        print(f"- {doc['id']}: {doc['summary']}")

    print()
    print("Example tool lookup:")
    result = find_support_document("What is your returns policy?")
    print(result)

    print()
    print("ADK agent file:")
    print("support_agent_app/agents/support_agent.py")
    print()
    print("Run with ADK after installing optional dependencies:")
    print("pip install -e '.[adk]'")
    print("adk run support_agent_app")
    print()
    print("Load these docs into Postgres:")
    print("python3 -m support_agent_app.ingest_policies --dry-run")
    print("DATABASE_URL='postgresql://...' python3 -m support_agent_app.ingest_policies")


if __name__ == "__main__":
    main()
