.PHONY: setup run clean

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python3 server.py

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
