from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from support_agent_app.services.support_processor import process_support_email


class SupportEmailRequest(BaseModel):
    sender: str
    subject: str
    body: str


class SupportEmailResponse(BaseModel):
    label: str
    reason: str
    document_id: str | None
    draft_reply: str | None


app = FastAPI(title="AI Architect Support Agent")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/support-email", response_model=SupportEmailResponse)
def support_email(request: SupportEmailRequest) -> SupportEmailResponse:
    result = process_support_email(request.body)
    return SupportEmailResponse(
        label=result.label,
        reason=result.reason,
        document_id=result.document_id,
        draft_reply=result.draft_reply,
    )
