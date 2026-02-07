.PHONY: run test lint format migrate

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check app tests

format:
	ruff check --fix app tests

migrate:
	alembic upgrade head
