# debug-probe MCP Server

A specialized MCP server for capturing execution context, analyzing logs, and troubleshooting crashes. Part of the `shuttles` monorepo.

## Features

- **Execution Capture**: Run commands and capture stdout/stderr for investigation.
- **Log Tailing**: Tail files with specific filters to find relevant debug information.
- **Crash Analysis**: Offload crash log analysis to a local LLM (`qwen2.5-coder:14b`) to find root causes without burning cloud tokens.

## Requirements

- Python 3.11+
- Ollama running locally (for crash analysis)

## Setup

```bash
make setup
```

## Tools

1. `run_and_capture`: Executes a shell command and returns the output.
2. `tail_filtered_logs`: Tails a log file and filters for specific keywords.
3. `analyze_crash_local`: Sends crash logs to a local Ollama instance for automated root cause analysis.

## Usage

Configure your MCP client to point to this directory and use `make run` or `python server.py`.
