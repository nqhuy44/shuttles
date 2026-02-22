import os
import sys
import json
import asyncio
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

import tools.get_dir_tree
import tools.get_file_skeleton
import tools.read_specific_lines
import tools.summarize_logic_local

app = Server("radar-ast")

REGISTERED_TOOLS = {
    "get_dir_tree": tools.get_dir_tree,
    "get_file_skeleton": tools.get_file_skeleton,
    "read_specific_lines": tools.read_specific_lines,
    "summarize_logic_local": tools.summarize_logic_local,
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
    """
    if arguments is None:
        arguments = {}

    if name in REGISTERED_TOOLS:
        module = REGISTERED_TOOLS[name]
        try:
            return await module.execute(arguments)
        except Exception as e:
            return [types.TextContent(type="text", text=json.dumps({"error": f"Internal Tool Error in {name}: {str(e)}"}))]
    else:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

async def main():
    """
    Initializes the MCP server and binds it to stdio transport.
    """
    options = InitializationOptions(
        server_name="radar-ast",
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
