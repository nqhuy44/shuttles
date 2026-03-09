import asyncio
import json
import os
from typing import Any
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

import tools.runner
import tools.coverage
import tools.diagnoser

# Ensure environment variables are loaded if using a .env file
# (Optionally use python-dotenv here, but we'll assume they are set in the environment)

app = Server("qa-deck")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Registers available tools for QA and Testing optimization."""
    return [
        tools.runner.get_tool(),
        tools.coverage.get_tool(),
        tools.diagnoser.get_tool()
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handles tool calls for qa-deck."""
    if arguments is None:
        arguments = {}

    try:
        if name == "run_test_compact":
            result = await tools.runner.execute(arguments)
        elif name == "get_coverage_gaps":
            result = await tools.coverage.execute(arguments)
        elif name == "diagnose_failure_local":
            result = await tools.diagnoser.execute(arguments)
        else:
            return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
            
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Internal Tool Error in {name}: {str(e)}"}))]

async def main():
    options = InitializationOptions(
        server_name="qa-deck",
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
