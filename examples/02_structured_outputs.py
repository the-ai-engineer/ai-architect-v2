"""
Structured Outputs

Classify support emails with Pydantic models and the OpenAI Responses API.
Structured outputs turn model responses into typed data your application can trust.
"""

import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv(Path(__file__).with_name(".env"))


if not os.getenv("OPENAI_API_KEY"):
    print("Set OPENAI_API_KEY in examples/.env to run this example.")
    raise SystemExit(0)


client = OpenAI()

# =============================================================================
# Support Email Classification
# =============================================================================


class Email(BaseModel):
    sender: str
    subject: str
    body: str


class Category(str, Enum):
    REFUND = "refund"
    SHIPPING = "shipping"
    ACCOUNT = "account"
    PRIVACY = "privacy"
    OTHER = "other"


class Action(str, Enum):
    ANSWER = "answer"
    HUMAN_NEEDED = "human_needed"


class Classification(BaseModel):
    category: Category
    action: Action
    confidence: float
    reason: str


def classify(email: Email) -> Classification:
    response = client.responses.parse(
        model="gpt-5.6",
        instructions="Classify the customer support email.",
        input=f"Subject: {email.subject}\n\n{email.body}",
        text_format=Classification,
    )
    return response.output_parsed


email = Email(
    sender="customer@example.com",
    subject="Return question",
    body="Hi, can I return a backpack if I opened the box but have not used it?",
)

classification = classify(email)

print(classification)

# =============================================================================
# Extract A Customer Request
# =============================================================================


class CustomerRequest(BaseModel):
    summary: str
    customer_question: str
    needs_private_data: bool


def extract_request(email: Email) -> CustomerRequest:
    response = client.responses.parse(
        model="gpt-5.6",
        instructions="Extract the customer request from the email.",
        input=f"Subject: {email.subject}\n\n{email.body}",
        text_format=CustomerRequest,
    )
    return response.output_parsed


email = Email(
    sender="customer@example.com",
    subject="Shipping update",
    body="Can you tell me whether order NS-1029 has shipped yet?",
)

request = extract_request(email)
print()
print(request)
