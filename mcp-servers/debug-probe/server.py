import asyncio
import json
from typing import Any
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

import tools.runner
import tools.logger
import tools.analyzer

app = Server("debug-probe")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Registers available tools for debugging and analysis."""
    return [
        tools.runner.get_tool(),
        tools.logger.get_tool(),
        tools.analyzer.get_tool()
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handles standard tool calls."""
    if arguments is None:
        arguments = {}

    try:
        if name == "run_and_capture":
            result = await tools.runner.execute(arguments)
        elif name == "tail_filtered_logs":
            result = await tools.logger.execute(arguments)
        elif name == "analyze_crash_local":
            result = await tools.analyzer.execute(arguments)
        else:
            return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
            
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Internal Tool Error in {name}: {str(e)}"}))]

async def main():
    options = InitializationOptions(
        server_name="debug-probe",
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
