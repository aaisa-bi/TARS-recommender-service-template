FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock* ./

RUN pip install 'uv==0.4.30' && \
    if [ -f uv.lock ]; then uv sync --frozen --python 3.12; else uv sync --python 3.12; fi

COPY src/ ./src/

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH="/app/src"

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
