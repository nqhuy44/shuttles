import httpx
import mcp.types as types
from typing import Any

import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5-coder")
NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "32768"))
TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))

def get_tool() -> types.Tool:
    return types.Tool(
        name="analyze_crash_local",
        description="[REQUIRES LOCAL GPU/Ollama] Sends a raw, messy stack trace to the local Ollama LLM to pinpoint the root cause.",
        inputSchema={
            "type": "object",
            "properties": {
                "raw_stack_trace": {"type": "string"}
            },
            "required": ["raw_stack_trace"]
        }
    )

async def execute(arguments: dict[str, Any]) -> str:
    raw_stack_trace = arguments.get("raw_stack_trace", "")
    
    if not raw_stack_trace.strip():
        return "Error: Empty stack trace provided."
        
    prompt = f"Analyze this stack trace. Return exactly two sentences: \\n1. The exact file, line number, and error type. \\n2. The likely root cause. \\n\\nStack trace:\\n{raw_stack_trace}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": NUM_CTX,
                        "temperature": TEMPERATURE
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
    except httpx.TimeoutException:
        return "Error: Local AI analysis timed out."
    except Exception as e:
        return f"Error during local analysis: {str(e)}"
