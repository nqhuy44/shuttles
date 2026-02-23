import asyncio
import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent
from core.spec_parser import get_openapi_map, get_endpoint_schema
from core.safe_executor import safe_api_execute
from core.error_analyzer import analyze_api_error_local

server = Server("api-link")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available API exploration tools."""
    return [
        Tool(
            name="get_openapi_map",
            description="Fetches OpenAPI spec and returns a concise map of endpoints and methods.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "URL or local path to OpenAPI spec (JSON/YAML)"}
                },
                "required": ["source"]
            }
        ),
        Tool(
            name="get_endpoint_schema",
            description="Retrieves Request and Response schemas for a specific endpoint.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "URL or local path to OpenAPI spec"},
                    "path": {"type": "string", "description": "API path (e.g., /api/v1/users)"},
                    "method": {"type": "string", "description": "HTTP method (GET, POST, etc.)"}
                },
                "required": ["source", "path", "method"]
            }
        ),
        Tool(
            name="safe_api_execute",
            description="Executes a real HTTP request with aggressive response truncation to save tokens.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Full target URL"},
                    "method": {"type": "string", "description": "HTTP method"},
                    "headers": {"type": "object", "description": "Optional HTTP headers"},
                    "json_body": {"type": "object", "description": "Optional JSON request body"},
                    "params": {"type": "object", "description": "Optional query parameters"}
                },
                "required": ["url", "method"]
            }
        ),
        Tool(
            name="analyze_api_error_local",
            description="[REQUIRES LOCAL GPU/Ollama] Uses local hardware to analyze complex 4xx/5xx API errors and suggest fixes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status_code": {"type": "integer", "description": "HTTP status code"},
                    "raw_error_response": {"type": "string", "description": "The truncated/raw error body"},
                    "endpoint": {"type": "string", "description": "The endpoint that failed"}
                },
                "required": ["status_code", "raw_error_response", "endpoint"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests."""
    try:
        if name == "get_openapi_map":
            result = await get_openapi_map(arguments["source"])
        elif name == "get_endpoint_schema":
            result = await get_endpoint_schema(
                arguments["source"], 
                arguments["path"], 
                arguments.get("method", "GET")
            )
        elif name == "safe_api_execute":
            result = await safe_api_execute(
                url=arguments["url"],
                method=arguments["method"],
                headers=arguments.get("headers"),
                json_body=arguments.get("json_body"),
                params=arguments.get("params")
            )
        elif name == "analyze_api_error_local":
            result = await analyze_api_error_local(
                status_code=arguments["status_code"],
                raw_error_response=arguments["raw_error_response"],
                endpoint=arguments["endpoint"]
            )
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
