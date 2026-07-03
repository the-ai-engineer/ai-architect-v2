from __future__ import annotations

import argparse

from support_agent_app.services.support_processor import process_support_email


def main() -> None:
    parser = argparse.ArgumentParser(description="Process one support question locally.")
    parser.add_argument("question", nargs="?", default="Can I return an opened item?")
    args = parser.parse_args()

    result = process_support_email(args.question)
    print(result)


if __name__ == "__main__":
    main()
