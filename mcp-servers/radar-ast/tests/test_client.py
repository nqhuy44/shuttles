import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

load_dotenv()

async def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    python_exec = os.path.join(base_dir, "venv", "bin", "python")
    server_script = os.path.join(base_dir, "server.py")
    
    server_params = StdioServerParameters(
        command=python_exec,
        args=[server_script],
        env=os.environ.copy()
    )

    print("🚀 Start MCP Client...")
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("✅ Connected MCP Server: radar-ast")

            print("\n--- 🛠️  Test list Tools ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # 1. Test get_dir_tree
            print("\n--- 📁 Test Tool: get_dir_tree ---")
            try:
                # Provide path relative to workspace or absolute.
                result = await session.call_tool("get_dir_tree", {"path": "mcp-servers/radar-ast/tools", "max_depth": 2})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w get_dir_tree: {e}")

            # 2. Test get_file_skeleton
            print("\n--- 🦴 Test Tool: get_file_skeleton ---")
            try:
                result = await session.call_tool("get_file_skeleton", {"file_path": "mcp-servers/radar-ast/server.py"})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w get_file_skeleton: {e}")
                
            # 3. Test read_specific_lines
            print("\n--- 📖 Test Tool: read_specific_lines ---")
            try:
                result = await session.call_tool("read_specific_lines", {"file_path": "mcp-servers/radar-ast/server.py", "start_line": 20, "end_line": 23})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w read_specific_lines: {e}")
                
            # 4. Test summarize_logic_local
            print("\n--- 🤖 Test Tool: summarize_logic_local ---")
            try:
                result = await session.call_tool("summarize_logic_local", {"file_path": "mcp-servers/radar-ast/core/helpers.py", "function_name": "validate_path"})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w summarize_logic_local: {e}")

if __name__ == "__main__":
    asyncio.run(main())
