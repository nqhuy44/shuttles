# Architecture

## Server Architecture
`radar-ast` is a Model Context Protocol (MCP) server designed to parse codebase intelligence without burning AI tokens on massive text files. It adheres to the "Ruthless Token Efficiency" philosophy by using local AST parsers and a local Ollama model to summarize code.

## Component Breakdown

1. **`core/helpers.py`**:
   - `validate_path()`: Critical security constraint preventing Directory Traversal attacks outside the workspace directory `shuttles/`.
   - `extract_python_skeleton()`: Uses standard `ast` to parse structures without bodies.
   - `extract_regex_skeleton()`: Fallback mechanism for JS/TS code.
   - `call_ollama_local()`: Handles raw HTTP requests to the local LLM.

2. **`tools/`**:
   - Individual logical abstractions mapped into `server.py`'s `REGISTERED_TOOLS`. Keeps the monolith modular.

3. **`server.py`**:
   - Exposes MCP standard HTTP transports via stdio. Translates incoming `call_tool` objects into functional invocations securely.
