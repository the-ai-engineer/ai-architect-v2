from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent.model_client import FakeModelClient, OpenAITextClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 01: make a basic model call.")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Explain what a customer support AI system does in one sentence.",
    )
    parser.add_argument("--real", action="store_true", help="Use OpenAI instead of the fake client.")
    args = parser.parse_args()

    model = OpenAITextClient() if args.real else FakeModelClient()
    print(model.complete(args.prompt))


if __name__ == "__main__":
    main()
