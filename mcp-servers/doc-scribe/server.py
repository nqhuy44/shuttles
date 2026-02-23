import asyncio
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Any, Dict, List, Optional

from core.markdown_utils import get_markdown_toc, patch_doc_section
from core.ollama_client import summarize_doc_local
from core.ast_utils import generate_inline_docs

server = Server("doc-scribe")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available documentation tools."""
    return [
        Tool(
            name="get_markdown_toc",
            description="Returns the Table of Contents of a Markdown file to understand its structure.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the markdown file."}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="patch_doc_section",
            description="Replaces the content of a specific section in a Markdown file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the markdown file."},
                    "heading_name": {"type": "string", "description": "Exact match of the heading (e.g., 'Installation')."},
                    "new_content": {"type": "string", "description": "New markdown content for this section."}
                },
                "required": ["file_path", "heading_name", "new_content"]
            }
        ),
        Tool(
            name="summarize_doc_local",
            description="Offloads heavy reading of long documentation to local LLM for a gist/summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the documentation file."},
                    "focus_query": {"type": "string", "description": "Optional focus for the summary (e.g., 'How to deploy?')."}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="generate_inline_docs",
            description="Generates Google-style docstrings for functions or classes using local LLM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the Python file."},
                    "function_name": {"type": "string", "description": "Name of the function or class."}
                },
                "required": ["file_path", "function_name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool execution requests."""
    try:
        if name == "get_markdown_toc":
            result = get_markdown_toc(arguments["file_path"])
        elif name == "patch_doc_section":
            result = patch_doc_section(
                arguments["file_path"],
                arguments["heading_name"],
                arguments["new_content"]
            )
        elif name == "summarize_doc_local":
            result = await summarize_doc_local(
                arguments["file_path"],
                arguments.get("focus_query")
            )
        elif name == "generate_inline_docs":
            result = await generate_inline_docs(
                arguments["file_path"],
                arguments["function_name"]
            )
        else:
            result = f"Error: Tool '{name}' not found."
            
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
