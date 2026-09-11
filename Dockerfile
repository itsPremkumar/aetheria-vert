# Dockerfile for Aetheria Vertical AI Platform
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
COPY tests/ tests/
COPY README.md .

RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "pytest", "tests/", "-v"]
EXPOSE 8000
