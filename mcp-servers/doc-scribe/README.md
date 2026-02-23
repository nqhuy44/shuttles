# doc-scribe MCP Server

A specialized MCP server for ruthless token efficiency in documentation management.

## Features

- **Structural TOC**: Extract Table of Contents without reading the whole file.
- **Section Patching**: Update specific sections without full-file rewrites.
- **Local Summarization**: Use local Ollama (`qwen2.5-coder:14b`) to summarize long docs.
- **Inline Docstrings**: Automatically generate and insert docstrings for Python code.

## Requirements

- Python 3.11+
- GPU with at least 8GB VRAM
- Ollama running locally

## Setup

```bash
make setup
```

## Usage

Configure your MCP client to use `python server.py` (or `make run`) in this directory.

## Tools

1. `get_markdown_toc`: Returns heading structure.
2. `patch_doc_section`: Replaces content under a heading.
3. `summarize_doc_local`: Local LLM summary of a file.
4. `generate_inline_docs`: Local LLM docstring generation.
