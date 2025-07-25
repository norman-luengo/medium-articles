# ---- Stage 1: Build dependencies ----
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --only=mlflow_article --no-root
    
# ---- Stage 2: Runtime image ----
FROM python:3.13-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages and binaries from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["uvicorn", "agentic_mlflow_article.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
