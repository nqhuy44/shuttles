# Features

The `debug-probe` MCP server provides the following automated debugging tools:

## 1. `run_and_capture`
Safely executes a specific script or test command and strictly captures the error output if it fails.
-   **Security**: Prevents dangerous commands (e.g., `rm -rf`) by utilizing an allowed list of base commands (`python`, `pytest`, `node`, `npm`, `go`).
-   **Timeouts**: Enforces a strict 10-second timeout to prevent infinite loops.
-   **Token Efficiency**: Returns "Success" if the command passes, and *only* returns `stderr` or the bottom-most stack trace if it fails.

## 2. `tail_filtered_logs`
Reads the tail of a log file but aggressively filters out non-critical noise to save tokens.
-   **Log Tail**: Skips to the last N lines (default 50) of a specified log file.
-   **Noise Filtering**: Uses regex to strip out lines containing `INFO`, `DEBUG`, or `TRACE`. Keeps lines with `ERROR`, `FATAL`, `WARN`, and stack traces.

## 3. `analyze_crash_local`
Sends a raw, messy stack trace to the local Ollama LLM to pinpoint the root cause, returning a highly compressed summary to the Cloud AI.
-   **Local Offloading**: Makes a POST request to `http://localhost:11434/api/generate` to keep heavy processing local.
-   **Compressed Output**: Instructs the local model to return exactly two sentences: 1) the file, line, and error type; 2) the likely root cause.
