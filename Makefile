.PHONY: build run web test lint typecheck format

build:
	docker build -t project_app .

run:
	docker compose up --build app

test:
	PYTHONPATH=src uv run --group dev pytest -v --cov=src --cov-report=term-missing

lint:
	PYTHONPATH=src uv run --group dev ruff check src

typecheck:
	PYTHONPATH=src uv run --group dev mypy src

format:
	PYTHONPATH=src uv run --group dev black src
