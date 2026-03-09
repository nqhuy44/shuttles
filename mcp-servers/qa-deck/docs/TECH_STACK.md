# Tech Stack: QA-Deck

## Core
- **Language**: Python 3.11+
- **SDK**: `mcp` (Model Context Protocol)
- **Protocol**: `stdio_server`

## Dependencies
- `httpx`: For asynchronous communication with local Ollama.
- `lxml`: For high-performance XML parsing of coverage reports.
- `subprocess`: For executing test frameworks.
- `re`: For parsing test outputs.

## Local Infrastructure
- **Ollama**: Required for local LLM offloading.
- **Model**: `qwen2.5-coder:14b` (Targeted for technical diagnosis).
