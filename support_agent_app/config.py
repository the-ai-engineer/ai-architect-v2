from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
APP_ENV_PATH = APP_DIR / ".env"


@dataclass(frozen=True)
class AppConfig:
    model_name: str
    policy_dir: Path
    database_url: str | None

    @classmethod
    def from_env(cls) -> "AppConfig":
        load_dotenv(APP_ENV_PATH)
        return cls(
            model_name=_normalize_model_name(
                os.getenv("AI_ARCHITECT_MODEL", "openai:gpt-5.6")
            ),
            policy_dir=_resolve_policy_dir(os.getenv("POLICY_DIR")),
            database_url=os.getenv("DATABASE_URL"),
        )


def _resolve_policy_dir(policy_dir: str | None) -> Path:
    if not policy_dir:
        return REPO_ROOT / "docs" / "policies"

    path = Path(policy_dir)
    if path.is_absolute():
        return path

    return REPO_ROOT / path


def _normalize_model_name(model_name: str) -> str:
    if model_name.startswith(("openai/", "anthropic/")):
        provider, model = model_name.split("/", maxsplit=1)
        return f"{provider}:{model}"
    return model_name
