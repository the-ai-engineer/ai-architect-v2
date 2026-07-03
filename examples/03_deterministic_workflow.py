from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent.domain import Ticket
from support_agent.workflow import run_support_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 03: run a deterministic support workflow.")
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
    result = run_support_workflow(ticket)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
