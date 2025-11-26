# AGENTS.md — Universal Project Development Guide

This document defines **how coding agents and developers should build, test, and extend** within this repository. It follows the [AGENTS.md specification](https://github.com/openai/agents.md) and is designed to provide a FASTAPI API service to deliver AI based recommendations.

---

## 🧩 1. Project Overview

* **Language:** Python 3.12+
* **Core Stack:** Docker, UV (dependency management), Hydra (configuration), Pydantic (settings), and docker based cloud integrations.
* **Purpose:** Provide a reproducible, secure, and containerized development workflow that works for any project type — data, web, ML, or analytics.
* **Deployment Targets:** Any Docker-compatible runtime.

---

## 🧱 2. Repository Structure

```bash
project_root/
├── credentials/        # service-account keys mounted locally (gitignored)
├── src/
│   ├── app/            # fast studies and assets
│   │   ├── config/     # Hydra YAML configurations
│   │   ├── utils/      # helpers for loading, transformations, etc.
│   │   ├── model/      # model logic
│   │   └── main.py     # main entry point for the FAST API logic and endpoints for this service
│   ├── connections/    # integrations and connectors (e.g., AWS, GCP, APIs, DBs)
│   └── settings.py     # environment-driven settings (pydantic base settings)
├── .env.example        # environment variable template (secrets handled by runtime)
├── .gitignore
├── Dockerfile
├── Makefile
├── pyproject.toml
└── AGENTS.md (this file)
```

> **Note:** Large datasets must never be versioned in the repository. Use cloud storage (S3) or mounted volumes for large files.

---

## ⚙️ 3. Environment Setup

### Dependency Management — UV

```bash
uv init
uv add pydantic hydra-core scikit-learn
uv add --dev pytest ruff mypy black
```

**`pyproject.toml`** example:

```toml
[tool.uv]
python = "3.12"

[tool.ruff]
line-length = 100

[tool.mypy]
strict = true

# Basic project stack
[project]
dependencies = [
    "pydantic>=2.6",
    "pydantic-settings>=2.0",
    "hydra-core>=1.3",
]
optional-dependencies.dev = [
    "pytest",
    "ruff",
    "mypy",
    "black"
]
```

### Environment Variables

* Environment variables are defined in `.env`.
* `.env` **must never be never commited to git** , always ensure it is present on the gitignore of the file.

Example `.env.example`:

```bash
ENV=local
BUCKET_NAME=aaisa-dev-bucket
APPLICATION_CREDENTIALS=/app/credentials/service-account.json
PUBLIC_ENV_VARIABLE=your-public-variable
SECRET_ENV_VARIABLE=your-secret-variable
```

### Pydantic Settings Example

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "local"
    public_env_variable: str
    secret_env_variable: SecretStr

    class Config:
        env_file = ".env"

settings = Settings()
```

### Hydra Configuration Example

Hydra YAML files should capture project-internal structure while remaining environment agnostic:

```yaml
defaults:
  - _self_

app:
  name: kyc_exploration

storage:
  list_prefix: ""
  datasets:
    pensions_root: "public/s-pensiones/db"
    statistics_root: "public/s-pensiones/statistics"
```

---

## 🐳 4. Docker Configuration

**Dockerfile**

```dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN pip install 'uv==0.4.30' && uv sync --frozen --python 3.12

COPY src/ ./src/

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> This Docker image supports any Python project with a `main.py` entry point in the `src/` directory.

**Docker Compose** is used locally to mount the `credentials/` directory into the container while keeping secrets out of the image. Add extra services (databases, brokers) only when needed.

Example (optional):

```yaml
services:
  app:
    build: .
    env_file: .env
    volumes:
      - ./src:/app/src
      - ./credentials:/app/credentials:ro
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app_db
    ports:
      - "5432:5432"
```

---

## 🧰 5. Makefile Commands

```makefile
.PHONY: build run test lint typecheck

build:
	docker build -t project_app .

run:
	docker compose run --rm app

test:
	uv run pytest -v

lint:
	uv run ruff check src

typecheck:
	uv run mypy src
```

---

## 🧪 6. Testing & Quality Standards

* Unit tests: `pytest` (optional, only if required by user)
* Linting: `ruff`
* Type checking: `mypy`
* Code formatting: `black`

Example:

```bash
make lint
make test
make typecheck
```

---

## 🔀 7. Git & CI/CD Workflow

* Branch naming: `feature/<name>` or `fix/<name>`
* Each PR must pass:

  * `ruff` lint
  * `mypy` type checks
  * `pytest` unit tests
* CI/CD pipelines (GitHub Actions + Cloud Build) are configured to:

  * Build and test the image.
  * Push to **Artifact Registry**.

---

## 📦 8. .gitignore

```gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.env.*
venv/
.DS_Store
.ipynb_checkpoints/
__cache__/
*.log
/data/
/tests/__pycache__/
.idea/
.vscode/
*.egg-info/
```

---

## 🧠 10. Coding Conventions

* Follow [PEP8](https://peps.python.org/pep-0008/)
* Enforce typing for all methods.
* Use `loguru` or `structlog` for logging.
* Configurations should always be handled through Hydra YAMLs and not hardcoded.

---

## 🧾 References

* [AGENTS.md Specification](https://github.com/openai/agents.md)
* [Hydra Documentation](https://hydra.cc/docs/intro/)
* [Pydantic Settings](https://docs.pydantic.dev/latest/)
* [UV Package Manager](https://github.com/astral-sh/uv)
* [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
