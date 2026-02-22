# Architecture

The `debug-probe` MCP server is designed as a standalone debugging assistant within the `shuttles` monorepo. It adheres to the Model Context Protocol (MCP) using a `stdio` transport layer, suitable for local integration with language models.

## Core Components

1.  **Server Process (`server.py`)**: The entry point that initializes the standard IO streams and registers debugging tools. It routes incoming requests to the specific tool modules.
2.  **Tool Modules (`tools/`)**: Isolated modules encapsulating specific debugging capabilities.
3.  **Local LLM Integration (Ollama)**: Uses HTTP requests to communicate with a local instance of Ollama (specifically the `qwen2.5-coder` model) for complex analysis without consuming cloud API tokens.

## Design Patterns
- **Dependency Inversion**: Tools are decoupled from the server implementation, making them easy to test and extend.
- **Fail-Safe Execution**: External commands and network requests use aggressive timeouts and whitelisting to prevent blocking and security risks.
