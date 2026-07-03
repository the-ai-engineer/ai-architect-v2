FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY support_agent ./support_agent
COPY support_agent_app ./support_agent_app
COPY docs ./docs
COPY sql ./sql

RUN pip install --no-cache-dir ".[app]"

CMD ["uvicorn", "support_agent_app.api:app", "--host", "0.0.0.0", "--port", "8080"]

