"""
Structured Outputs

Classify support emails with Pydantic models and the OpenAI Responses API.
Structured outputs turn model responses into typed data your application can trust.
"""

import os
from enum import Enum

try:
    from dotenv import load_dotenv
    from openai import OpenAI
    from pydantic import BaseModel
except ImportError:
    print("Install dependencies with `pip install -e .` to run this example.")
    raise SystemExit(0)

load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    print("Set OPENAI_API_KEY to run this example.")
    raise SystemExit(0)


client = OpenAI()

# =============================================================================
# Support Email Classification
# =============================================================================


class Category(str, Enum):
    REFUND = "refund"
    SHIPPING = "shipping"
    ACCOUNT = "account"
    PRIVACY = "privacy"
    OTHER = "other"


class Action(str, Enum):
    ANSWER = "answer"
    HUMAN_NEEDED = "human_needed"


class SupportClassification(BaseModel):
    category: Category
    action: Action
    confidence: float
    reason: str


email_text = "Hi, can I return a backpack if I opened the box but have not used it?"

response = client.responses.parse(
    model="gpt-5.5",
    instructions="Classify the customer support email.",
    input=email_text,
    text_format=SupportClassification,
)

classification = response.output_parsed
print(classification)

# =============================================================================
# Extract A Customer Request
# =============================================================================


class CustomerRequest(BaseModel):
    summary: str
    customer_question: str
    needs_private_data: bool


email_text = "Can you tell me whether order NS-1029 has shipped yet?"

response = client.responses.parse(
    model="gpt-5.5",
    instructions="Extract the customer request from the email.",
    input=email_text,
    text_format=CustomerRequest,
)

request = response.output_parsed
print()
print(request)
