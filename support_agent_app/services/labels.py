from __future__ import annotations


def decide_gmail_label(answerable: bool, reason: str) -> dict[str, str]:
    """Return the Gmail label the app should apply after processing a ticket."""
    label = "AI Answered" if answerable else "Human Needed"
    return {"label": label, "reason": reason}

