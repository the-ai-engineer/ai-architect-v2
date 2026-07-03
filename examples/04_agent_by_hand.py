from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent.agent_by_hand import run_agent_by_hand
from support_agent.domain import Ticket


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 04: build a tiny agent loop by hand.")
    parser.add_argument(
        "body",
        nargs="?",
        default="Can you explain your refund policy before I sign up?",
    )
    args = parser.parse_args()

    ticket = Ticket(
        sender="customer@example.com",
        subject="Support question",
        body=args.body,
    )
    result = run_agent_by_hand(ticket)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
