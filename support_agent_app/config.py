from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AppConfig:
    model_name: str
    policy_dir: Path
    database_url: str | None

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            model_name=os.getenv("AI_ARCHITECT_MODEL", "openai/gpt-5.5"),
            policy_dir=Path(os.getenv("POLICY_DIR", str(REPO_ROOT / "docs" / "policies"))),
            database_url=os.getenv("DATABASE_URL"),
        )
