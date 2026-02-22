# Tech Stack

This project utilizes the following technologies, adhering to the monorepo standards:

- **Python 3.11+**: The core programming language, chosen for its fast development cycle, strong typing (using `typing` module), and ecosystem of AI/ML tools.
- **MCP SDK (`mcp`)**: The official Model Context Protocol library used to expose debugging capabilities to the Cloud AI.
- **HTTPX (`httpx`)**: An async-capable HTTP client used for communicating with the local Ollama instance securely and with proper timeout mechanisms.
- **Ollama**: A local LLM runner used to offload token-heavy summarization of stack traces, preserving Cloud AI context limits.
- **qwen2.5-coder**: The specific model used by Ollama for specialized reasoning over code errors and stack traces.
