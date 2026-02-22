import asyncio
import json
import sys
import os
from dotenv import load_dotenv
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Load environment variables from .env
load_dotenv()

async def main():
    # 1. Define how to execute our server
    # Define absolute paths based on this file's directory (cargo-db/tests/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    python_exec = os.path.join(base_dir, "venv", "bin", "python")
    server_script = os.path.join(base_dir, "server.py")
    
    # We use our virtualenv's python to run server.py
    # Pass along existing environment variables to catch DATABASE_URL
    server_params = StdioServerParameters(
        command=python_exec,
        args=[server_script],
        env=os.environ.copy()
    )

    print("🚀 Start MCP Client...")
    
    # 2. Connect to the stdio server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection protocol
            await session.initialize()
            print("✅ Connected MCP Server: cargo-db")

            # --- Test 1: List Tools ---
            print("\n--- 🛠️  Test list Tools ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # --- Test 2: Call `get_tables` ---
            print("\n--- 📊 Test Tool: get_tables ---")
            try:
                result = await session.call_tool("get_tables", {})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w get_tables: {e}")

            # --- Test 3: Call `explain_query` ---
            print("\n--- 🔍 Test Tool: explain_query ---")
            try:
                # We do a basic SELECT 1 to ensure it explains correctly
                result = await session.call_tool("explain_query", {"query": "SELECT 1;"})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error when calling explain_query: {e}")

            # --- Test 4: Call `read_formatted` ---
            print("\n--- 📝 Test Tool: read_formatted ---")
            try:
                result = await session.call_tool("read_formatted", {"query": "SELECT 1 as num, 'test' as str;"})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w read_formatted: {e}")

            # --- Test 5: Call `find_join_path` ---
            print("\n--- 🔗 Test Tool: find_join_path ---")
            try:
                # Assuming table 'users' and 'roles' don't exist yet, it will return an error correctly
                result = await session.call_tool("find_join_path", {"tables": ["users", "roles"]})
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error w find_join_path: {e}")

if __name__ == "__main__":
    asyncio.run(main())
