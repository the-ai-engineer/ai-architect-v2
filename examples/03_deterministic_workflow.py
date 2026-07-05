"""
Deterministic Workflows

A workflow is a fixed sequence of steps.
The model can classify or draft, but your code owns the control flow.
"""

import os
import sys
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent_app.services.document_registry import find_support_document
from support_agent_app.services.labels import decide_gmail_label

load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    print("Set OPENAI_API_KEY to run this example.")
    raise SystemExit(0)


client = OpenAI()

# =============================================================================
# Types
# =============================================================================


class Action(str, Enum):
    ANSWER = "answer"
    HUMAN_NEEDED = "human_needed"


class Classification(BaseModel):
    action: Action
    reason: str


# =============================================================================
# Workflow
# =============================================================================


customer_email = "Can I return a backpack if I opened the box but have not used it?"

classification_response = client.responses.parse(
    model="gpt-5.5",
    instructions="Decide if the support email can be answered from public policy docs.",
    input=customer_email,
    text_format=Classification,
)

classification = classification_response.output_parsed

if classification.action == Action.HUMAN_NEEDED:
    print(decide_gmail_label(answerable=False, reason=classification.reason))
    raise SystemExit(0)

document_result = find_support_document(customer_email)

if not document_result["found"]:
    print(decide_gmail_label(answerable=False, reason=str(document_result["reason"])))
    raise SystemExit(0)

document = document_result["document"]

reply_response = client.responses.create(
    model="gpt-5.5",
    instructions="Answer the customer using only the support policy document.",
    input=f"Customer email:\n{customer_email}\n\nPolicy document:\n{document['body']}",
)

print(reply_response.output_text)
print()
print(decide_gmail_label(answerable=True, reason=f"Answered from {document['id']}"))
