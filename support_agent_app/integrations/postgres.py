from __future__ import annotations


def require_database_url(database_url: str | None) -> str:
    if not database_url:
        raise RuntimeError("DATABASE_URL is required for Postgres operations.")

    return database_url

