# `radar-ast` MCP Server

This is the `radar-ast` local Model Context Protocol server. It handles codebase structure awareness and token reduction parsing using AST trees and Local LLM (Ollama) offloading capabilities.

## How to run
1. Set up the Python environment: `make setup`
2. Configure `.env`: Use `.env.example` as a template for configuring the connection to your local Ollama runtime.
3. Start the server via MCP standard stdio: `make run`

## Testing locally
You can use the built-in test client to verify operations:
```bash
env PYTHONPATH=. ./venv/bin/python tests/test_client.py
```
*(Make sure to run this inside `mcp-servers/radar-ast/`)*
