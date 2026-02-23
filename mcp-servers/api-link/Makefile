.PHONY: setup run test

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) server.py

test:
	PYTHONPATH=. $(PYTHON) tests/manual_test.py
