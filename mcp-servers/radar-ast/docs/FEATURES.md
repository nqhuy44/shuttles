# Features

## Codebase Exploration
Provides safe and extremely token-efficient views of local code via MCP.

### 1. `get_dir_tree`
- Generates a file tree map.
- **Aggressively ignores**: `.git`, `node_modules`, `venv`, `__pycache__`, builds, caches.

### 2. `get_file_skeleton`
- Extracts semantic structural boundaries of a file (classes, methods, functions, docstrings).
- Replaces source code bodies with `...`.
- Highly reduces Token limits used by standard IDE file reading.

### 3. `read_specific_lines`
- After using `get_file_skeleton`, an AI agent can pinpoint EXACT lines of code to investigate deeper using this tool.

### 4. `summarize_logic_local`
- Offloads understanding of deep complex logic directly to a local RTX 3060 processing unit running Ollama.
- Outputs 3 concise bullet points instead of forcing Cloud LLMs to read hundreds of lines.
