from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent.domain import Classification
from support_agent.model_client import FakeModelClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 02: parse a structured classification.")
    parser.add_argument(
        "email",
        nargs="?",
        default="Can you explain your refund policy before I sign up?",
    )
    args = parser.parse_args()

    raw = FakeModelClient().classify_ticket(args.email)
    classification = Classification.from_dict(raw)
    print(json.dumps(asdict(classification), indent=2))


if __name__ == "__main__":
    main()
