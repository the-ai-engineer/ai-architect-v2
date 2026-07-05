"""
Deterministic Workflows

A workflow is a fixed sequence of steps.
The model can classify or draft, but your code owns the control flow.
"""

import os
from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

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


class Email(BaseModel):
    sender: str
    subject: str
    body: str


class Action(str, Enum):
    ANSWER = "answer"
    HUMAN_NEEDED = "human_needed"


class Classification(BaseModel):
    action: Action
    reason: str


def classify(email: Email) -> Classification:
    response = client.responses.parse(
        model="gpt-5.5",
        instructions="Decide if the support email can be answered from public policy docs.",
        input=f"Subject: {email.subject}\n\n{email.body}",
        text_format=Classification,
    )
    return response.output_parsed


def draft_reply(email: Email, policy: str) -> str:
    response = client.responses.create(
        model="gpt-5.5",
        instructions="Answer the customer using only the support policy document.",
        input=f"Customer email:\n{email.body}\n\nPolicy document:\n{policy}",
    )
    return response.output_text


# =============================================================================
# Workflow
# =============================================================================


email = Email(
    sender="customer@example.com",
    subject="Return question",
    body="Can I return a backpack if I opened the box but have not used it?",
)

classification = classify(email)

if classification.action == Action.HUMAN_NEEDED:
    print(decide_gmail_label(answerable=False, reason=classification.reason))
    raise SystemExit(0)

document_result = find_support_document(email.body)

if not document_result["found"]:
    print(decide_gmail_label(answerable=False, reason=str(document_result["reason"])))
    raise SystemExit(0)

document = document_result["document"]
reply = draft_reply(email, str(document["body"]))

print(reply)
print()
print(decide_gmail_label(answerable=True, reason=f"Answered from {document['id']}"))
