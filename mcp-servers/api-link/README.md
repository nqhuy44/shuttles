# api-link MCP Server

A token-efficient bridge for exploring external APIs and OpenAPI specifications.

## Philosophies
- **Structural First**: Extracts high-level maps of endpoints before diving into schemas.
- **Aggressive Truncation**: Truncates large JSON arrays and HTML pages to minimize context burn.
- **Local Diagnosis**: Offloads complex API error analysis to local hardware.

## Requirements
- Python 3.11+
- `httpx`
- `pyyaml`
- Ollama (for error analysis)

## Setup
```bash
make setup
```

## Tools
1. `get_openapi_map`: Get a concise list of endpoints and methods from a spec.
2. `get_endpoint_schema`: Get request/response schemas for a specific path.
3. `safe_api_execute`: Run real HTTP requests with safety truncation.
4. `analyze_api_error_local`: Local AI analysis of 4xx/5xx errors.
