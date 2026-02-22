.PHONY: setup run test

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python server.py

test:
	.venv/bin/pytest tests/
