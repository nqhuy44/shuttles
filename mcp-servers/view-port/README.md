# view-port MCP Server

A specialized MCP server for Frontend and Web UI development, focusing on structural analysis and design system introspection.

## Philosophies
- **Ruthless Token Efficiency**: Strips DOM noise and extracts only metadata to minimize cloud input context.
- **Deterministic Execution**: Uses Regex and BeautifulSoup for reliability. No LLMs or GPUs required for these tools.

## Features
- **Design Token Extraction**: Parse Tailwind/CSS variables.
- **UI Component Registry**: Scan component folders for props/names.
- **DOM Skeleton Parser**: Remove inner text and noisy attributes from JSX/HTML.
- **Route Navigator**: Map folder structures to valid URL paths.

## Requirements
- Python 3.11+

## Setup
```bash
make setup
```

## Tools
1. `extract_design_tokens`: Parses config files for colors, spacing, fonts.
2. `scan_ui_components`: Build a registry of components and props.
3. `extract_dom_skeleton`: Get stripped structural tags from JSX/HTML.
4. `map_frontend_routes`: Get a list of valid URL paths from the routing directory.
