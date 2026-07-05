"""
Agent By Hand

An agent is a loop, not a single model call.

The loop is:

1. Send the current messages to the model.
2. Let the model choose the next action.
3. If it chose a tool, run the tool.
4. Add the tool result back into the messages.
5. Stop when the model returns a final answer or asks for human help.
"""

import os
from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from support_agent_app.services.document_registry import find_support_document, list_support_documents
from support_agent_app.services.labels import decide_gmail_label

load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    print("Set OPENAI_API_KEY to run this example.")
    raise SystemExit(0)


client = OpenAI()

# =============================================================================
# Agent Data Types
# =============================================================================


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    role: MessageRole
    content: str


class Email(BaseModel):
    sender: str
    subject: str
    body: str


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


class ToolResult(BaseModel):
    tool: ToolName
    content: str


# =============================================================================
# Agent
# =============================================================================


class Agent:
    def __init__(self, model: str = "gpt-5.5", max_iterations: int = 6) -> None:
        self.model = model
        self.max_iterations = max_iterations

    def run(self, email: Email) -> str:
        messages = [Message(role=MessageRole.USER, content=self.format_email(email))]

        for iteration in range(self.max_iterations):
            step = self.choose_next_step(messages)
            print(f"\nIteration {iteration + 1}")
            print(step)

            if step.tool == ToolName.ANSWER:
                return step.answer or "I do not have enough information to answer."

            if step.tool == ToolName.HUMAN_NEEDED:
                result = self.run_tool(step, email)
                return result.content

            result = self.run_tool(step, email)
            messages.append(
                Message(
                    role=MessageRole.ASSISTANT,
                    content=f"Tool call: {step.tool.value}. Reason: {step.reason}",
                )
            )
            messages.append(
                Message(
                    role=MessageRole.TOOL,
                    content=f"Tool result from {result.tool.value}:\n{result.content}",
                )
            )

        return str(
            decide_gmail_label(
                answerable=False,
                reason="The agent reached the max iteration limit.",
            )
        )

    def choose_next_step(self, messages: list[Message]) -> NextStep:
        response = client.responses.parse(
            model=self.model,
            instructions=(
                "You are a customer support agent.\n"
                "Choose exactly one next action.\n"
                "Use list_support_documents before choosing a policy document.\n"
                "Use find_support_document before answering.\n"
                "Only answer from tool results.\n"
                "If the question is unsafe, unsupported, or needs private account data, "
                "choose human_needed."
            ),
            input=self.format_messages(messages),
            text_format=NextStep,
        )
        return response.output_parsed

    def run_tool(self, step: NextStep, email: Email) -> ToolResult:
        if step.tool == ToolName.LIST_DOCUMENTS:
            return ToolResult(tool=step.tool, content=str(list_support_documents()))

        if step.tool == ToolName.FIND_DOCUMENT:
            query = step.query or email.body
            return ToolResult(tool=step.tool, content=str(find_support_document(query)))

        if step.tool == ToolName.HUMAN_NEEDED:
            label = decide_gmail_label(answerable=False, reason=step.reason)
            return ToolResult(tool=step.tool, content=str(label))

        return ToolResult(tool=step.tool, content=step.answer or "")

    def format_messages(self, messages: list[Message]) -> str:
        return "\n\n".join(f"{message.role.value.upper()}:\n{message.content}" for message in messages)

    def format_email(self, email: Email) -> str:
        return f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"


email = Email(
    sender="customer@example.com",
    subject="Return question",
    body="Can I return a backpack if I opened the box but have not used it?",
)
answer = Agent().run(email)

print("\nFinal:")
print(answer)
