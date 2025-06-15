include .env

install-venv:
	python -m venv venv
	source venv/bin/activate && pip install --upgrade pip
	pip install -r requirements.txt
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

lint:
	flake8 src tests

test:
	pytest --cov=src --cov-report=xml --cov-report=html

coverage:
	pytest --cov=src --cov-report=xml --cov-report=html

clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov
	rm -rf src/*.egg-info src/build src/dist
	rm -rf tests/__pycache__ tests/*.pyc
	rm -rf .mypy_cache .ruff_cache
	rm -rf .vscode

format:
	ruff format src tests

mypy:
	mypy src tests

.PHONY: install lint test coverage clean format mypy


ollama-serve-and-run:
	ollama serve
	ollama run deepseek-llm

uvicorn-serve:
	uvicorn main:app --reload


