import httpx
import json
from typing import Optional, Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.generate_url = f"{self.base_url}/api/generate"

    async def generate(self, model: str, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Sends a generation request to the local Ollama instance.
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options or {}
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(self.generate_url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
        except httpx.ConnectError:
            return "Error: Ollama is not running. Please start Ollama or check its URL."
        except httpx.HTTPStatusError as e:
            return f"Error: Ollama returned an HTTP error: {e.response.status_code}."
        except Exception as e:
            return f"Error: An unexpected error occurred while calling Ollama: {str(e)}"

async def summarize_doc_local(file_path: str, focus_query: Optional[str] = None) -> str:
    """
    Reads a file and uses local Ollama to summarize it.
    """
    from pathlib import Path
    path = Path(file_path)
    if not path.exists():
        return f"Error: File {file_path} not found."
    
    text = path.read_text(encoding="utf-8")
    
    # Trim text if it's too long for the context window (Ollama default is often 2048 or 4096)
    # The prompt specifies num_ctx: 8192
    if len(text) > 25000: # Rough approximation for ~8k tokens
        text = text[:25000] + "\n... [content truncated] ..."

    focus_clause = f"based on this focus: {focus_query}" if focus_query else "concisely"
    prompt = f"Read this doc and answer/summarize {focus_clause}. Keep it under 5 bullet points.\n\nDoc:\n{text}"
    
    client = OllamaClient()
    return await client.generate(
        model="qwen2.5-coder:14b",
        prompt=prompt,
        options={"num_ctx": 8192, "temperature": 0.1}
    )
