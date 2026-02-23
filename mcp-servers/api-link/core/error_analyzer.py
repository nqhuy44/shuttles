import httpx
import json
import os
from typing import Optional

async def analyze_api_error_local(
    status_code: int, 
    raw_error_response: str, 
    endpoint: str
) -> str:
    """Uses local Ollama to analyze API errors."""
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
    ollama_model = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:14b")
    
    prompt = f"""Analyze this API error response for the endpoint {endpoint}.
Status code: {status_code}
Response: {raw_error_response}

Return exactly two bullet points:
1. What the error is.
2. How to fix the request payload or headers.
"""

    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 4096,
            "temperature": 0.1
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(ollama_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response from local LLM.").strip()
    except Exception as e:
        return f"Local error analysis failed: {str(e)}"
