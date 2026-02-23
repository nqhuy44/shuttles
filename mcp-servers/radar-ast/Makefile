.PHONY: setup run clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python server.py

clean:
	rm -rf venv __pycache__ .pytest_cache
