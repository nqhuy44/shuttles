import json
import yaml
import httpx
from typing import Dict, Any, List, Optional
from pathlib import Path

async def _fetch_spec(source: str) -> Dict[str, Any]:
    """Fetches OpenAPI spec from URL or local file."""
    if source.startswith(("http://", "https://")):
        async with httpx.AsyncClient() as client:
            response = await client.get(source)
            response.raise_for_status()
            content = response.text
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Source file {source} not found.")
        content = path.read_text(encoding="utf-8")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return yaml.safe_load(content)

async def get_openapi_map(source: str) -> str:
    """Returns a concise map of endpoints and methods."""
    try:
        spec = await _fetch_spec(source)
        paths = spec.get("paths", {})
        
        api_map = {}
        for path, methods in paths.items():
            api_map[path] = [m.upper() for m in methods.keys() if m.lower() in ["get", "post", "put", "delete", "patch", "options", "head"]]
            
        return json.dumps(api_map, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

async def get_endpoint_schema(source: str, path: str, method: str) -> str:
    """Retrieves request/response schemas for a specific endpoint."""
    try:
        spec = await _fetch_spec(source)
        endpoint = spec.get("paths", {}).get(path, {}).get(method.lower())
        
        if not endpoint:
            return json.dumps({"error": f"Endpoint {method.upper()} {path} not found in spec."})
            
        result = {
            "summary": endpoint.get("summary"),
            "requestBody": endpoint.get("requestBody"),
            "responses": {
                "200": endpoint.get("responses", {}).get("200"),
                "201": endpoint.get("responses", {}).get("201")
            }
        }
        
        # Note: This does NOT resolve $ref. In a full implementation, you'd want to traversal components/schemas.
        # But per requirements "Do it right at first" (filtering), we keep it localized to the endpoint.
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
