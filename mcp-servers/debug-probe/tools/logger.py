import os
import re
import mcp.types as types
from typing import Any

NOISE_PATTERN = re.compile(r'\b(INFO|DEBUG|TRACE)\b', re.IGNORECASE)

def get_tool() -> types.Tool:
    return types.Tool(
        name="tail_filtered_logs",
        description="Reads the tail of a log file but aggressively filters out non-critical noise to save tokens.",
        inputSchema={
            "type": "object",
            "properties": {
                "log_file_path": {"type": "string"},
                "lines": {"type": "integer"}
            },
            "required": ["log_file_path"]
        }
    )

async def execute(arguments: dict[str, Any]) -> str:
    log_file_path = arguments.get("log_file_path")
    lines = arguments.get("lines", 50)
    
    if not log_file_path:
        return "Error: log_file_path is required."
        
    try:
        if not os.path.exists(log_file_path):
            return f"Error: Log file not found at {log_file_path}"
            
        with open(log_file_path, 'r', encoding='utf-8', errors='replace') as f:
            all_lines = f.readlines()
            
        tail_lines = all_lines[-lines:]
        
        filtered_lines = []
        for line in tail_lines:
            if not NOISE_PATTERN.search(line):
                filtered_lines.append(line.rstrip())
                
        if not filtered_lines:
            return "No critical errors found in the requested tail lines."
            
        return "\\n".join(filtered_lines)
    except Exception as e:
        return f"Error reading log file: {str(e)}"
