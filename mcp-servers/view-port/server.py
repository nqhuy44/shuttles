import asyncio
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List

from core.token_extractor import extract_design_tokens
from core.component_scanner import scan_ui_components
from core.dom_parser import extract_dom_skeleton
from core.route_mapper import map_frontend_routes

server = Server("view-port")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available frontend introspection tools."""
    return [
        Tool(
            name="extract_design_tokens",
            description="Parses config files (tailwind, CSS vars) to extract design tokens (colors, spacing, fonts).",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the configuration file (e.g., tailwind.config.js)."}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="scan_ui_components",
            description="Scans a directory to build a registry of available UI components and their accepted Props.",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string", "description": "Path to the components directory (e.g., src/components)."}
                },
                "required": ["directory_path"]
            }
        ),
        Tool(
            name="extract_dom_skeleton",
            description="Strips inner text and noise from HTML/JSX, returning only structural Tags, IDs, and Classes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the HTML or JSX file."}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="map_frontend_routes",
            description="Scans a routing directory to return a list of valid URL paths in the application.",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string", "description": "Path to the routing directory (e.g., app/ or src/routes/)."}
                },
                "required": ["directory_path"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool execution requests."""
    try:
        if name == "extract_design_tokens":
            result = extract_design_tokens(arguments["file_path"])
        elif name == "scan_ui_components":
            result = scan_ui_components(arguments["directory_path"])
        elif name == "extract_dom_skeleton":
            result = extract_dom_skeleton(arguments["file_path"])
        elif name == "map_frontend_routes":
            result = map_frontend_routes(arguments["directory_path"])
        else:
            result = f"Error: Tool '{name}' not found."
            
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
