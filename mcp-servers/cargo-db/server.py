import os
import sys
import json
import asyncio
from typing import Any
import importlib

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from core.db import get_engine

# Import externalized tools dynamically or statically
import tools.get_tables
import tools.get_schema
import tools.explain_query
import tools.read_formatted
import tools.find_join_path

app = Server("cargo-db")

# Register tools mapping
REGISTERED_TOOLS = {
    "get_tables": tools.get_tables,
    "get_schema": tools.get_schema,
    "explain_query": tools.explain_query,
    "read_formatted": tools.read_formatted,
    "find_join_path": tools.find_join_path,
}

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Registers the available tools from the tools folder for the MCP server.
    """
    return [module.get_tool() for module in REGISTERED_TOOLS.values()]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handles standard tool calls by dynamically delegating to the respective module in tools/.
    Implements robust error handling and token-optimized payloads.
    """
    if arguments is None:
        arguments = {}

    try:
        engine = get_engine()
    except Exception as e:
        # Return generic structural error to maintain predictability.
        return [types.TextContent(type="text", text=json.dumps({"error": f"Database Connection Error: {str(e)}"}))]

    if name in REGISTERED_TOOLS:
        module = REGISTERED_TOOLS[name]
        try:
            return await module.execute(arguments, engine)
        except Exception as e:
            return [types.TextContent(type="text", text=json.dumps({"error": f"Internal Tool Error in {name}: {str(e)}"}))]
    else:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

async def main():
    """
    Initializes the MCP server and binds it to stdio transport.
    """
    options = InitializationOptions(
        server_name="cargo-db",
        server_version="0.1.0",
        capabilities=app.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        )
    )
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, options)

if __name__ == "__main__":
    asyncio.run(main())
