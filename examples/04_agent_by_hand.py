"""
Agent By Hand

An agent is a loop where the model can choose tools.
This example keeps the loop tiny so the mechanism is easy to see.
"""

import os
import sys
from enum import Enum
from pathlib import Path

try:
    from dotenv import load_dotenv
    from openai import OpenAI
    from pydantic import BaseModel
except ImportError:
    print("Install dependencies with `pip install -e .` to run this example.")
    raise SystemExit(0)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent_app.services.document_registry import find_support_document, list_support_documents
from support_agent_app.services.labels import decide_gmail_label

load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    print("Set OPENAI_API_KEY to run this example.")
    raise SystemExit(0)


client = OpenAI()

# =============================================================================
# Tool Choice Schema
# =============================================================================


class ToolName(str, Enum):
    LIST_DOCUMENTS = "list_support_documents"
    FIND_DOCUMENT = "find_support_document"
    ANSWER = "answer"
    HUMAN_NEEDED = "human_needed"


class NextStep(BaseModel):
    tool: ToolName
    query: str | None = None
    answer: str | None = None
    reason: str


# =============================================================================
# Tools
# =============================================================================


def run_tool(step: NextStep, question: str) -> str:
    if step.tool == ToolName.LIST_DOCUMENTS:
        return str(list_support_documents())

    if step.tool == ToolName.FIND_DOCUMENT:
        return str(find_support_document(step.query or question))

    if step.tool == ToolName.HUMAN_NEEDED:
        return str(decide_gmail_label(answerable=False, reason=step.reason))

    return step.answer or ""


# =============================================================================
# Agent Loop
# =============================================================================


question = "Can I return a backpack if I opened the box but have not used it?"
observations: list[str] = []

for _ in range(4):
    response = client.responses.parse(
        model="gpt-5-mini",
        instructions=(
            "You are a support agent. Choose the next tool. "
            "Use documents before answering. If the question is unsafe, choose human_needed."
        ),
        input=f"Customer question:\n{question}\n\nObservations:\n{observations}",
        text_format=NextStep,
    )

    step = response.output_parsed
    print(step)

    if step.tool in {ToolName.ANSWER, ToolName.HUMAN_NEEDED}:
        print(run_tool(step, question))
        break

    observations.append(run_tool(step, question))
