import httpx
import json
import re
from typing import Dict, Any, Optional

async def safe_api_execute(
    url: str, 
    method: str, 
    headers: Optional[Dict[str, str]] = None, 
    json_body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> str:
    """Executes an API request and aggressively truncates the response."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json_body,
                params=params
            )
            
            res_data = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": None
            }
            
            content_type = response.headers.get("content-type", "").lower()
            
            if "application/json" in content_type:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        res_data["body"] = {
                            "type": "list",
                            "total_items": len(data),
                            "data_sample": data[:2]
                        }
                    elif isinstance(data, dict):
                        # Truncate long strings in dict
                        truncated_data = {}
                        for k, v in data.items():
                            if isinstance(v, str) and len(v) > 200:
                                truncated_data[k] = v[:200] + "... [TRUNCATED]"
                            else:
                                truncated_data[k] = v
                        res_data["body"] = truncated_data
                    else:
                        res_data["body"] = data
                except Exception:
                    res_data["body"] = response.text[:500] + "... [UNPARSABLE JSON TRUNCATED]"
            elif "text/html" in content_type:
                # Extract title and first H1
                title_match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE)
                h1_match = re.search(r"<h1>(.*?)</h1>", response.text, re.IGNORECASE)
                res_data["body"] = {
                    "type": "html",
                    "title": title_match.group(1) if title_match else "No Title",
                    "h1": h1_match.group(1) if h1_match else "No H1",
                    "preview": response.text[:200] + "..."
                }
            else:
                res_data["body"] = response.text[:500] + "... [TRUNCATED]"
                
            return json.dumps(res_data, indent=2)
            
    except Exception as e:
        return json.dumps({"error": f"Request failed: {str(e)}"})
