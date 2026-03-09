import mcp.types as types
import httpx
import json
import os
from typing import Any

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:14b")

def get_tool() -> types.Tool:
    return types.Tool(
        name="diagnose_failure_local",
        description="Analyzes a complex stack trace using a local LLM to find the root cause.",
        inputSchema={
            "type": "object",
            "properties": {
                "raw_stack_trace": {"type": "string"},
                "test_name": {"type": "string"}
            },
            "required": ["raw_stack_trace", "test_name"]
        }
    )

async def execute(arguments: dict[str, Any]) -> str:
    stack_trace = arguments.get("raw_stack_trace", "")
    test_name = arguments.get("test_name", "")

    prompt = f"Diagnose why the test {test_name} failed based on this stack trace. Give the root cause in 2 concise sentences. Stack trace: {stack_trace}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0 # LLM might take time
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response from local LLM.")
            else:
                return f"Error: Local LLM returned status {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error connecting to local LLM: {str(e)}"
