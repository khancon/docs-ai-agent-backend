include .env
export LLM_MODEL="llama3.2:1b"

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
	ollama pull deepseek-llm
	# ollama serve
	ollama run deepseek-llm

uvicorn-serve:
	uvicorn main:app --reload

docker-build:
	docker-compose up --build

clean-docker-build:
	docker-compose down -v
	rm -rf chroma_db  # make sure your local folder is clean
	docker-compose up --build

clean-docker-rebuild:
	docker-compose down -v
	docker-compose build
	docker-compose up

chat:
	curl -X POST http://localhost:8000/chat \
	     -H "Content-Type: application/json" \
	     -d '{"query": "What is a CustomResourceDefinition?", "model_name": ${LLM_MODEL}}'

pull-model:
	curl -X POST http://localhost:8000/models/pull \
		-H "Content-Type: application/json" \
		-d '{"model_name": ${LLM_MODEL}}'

delete-model:
	curl -X DELETE http://localhost:8000/models/${LLM_MODEL}

list-models:
	curl -X GET http://localhost:8000/models


