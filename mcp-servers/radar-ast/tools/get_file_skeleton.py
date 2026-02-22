import os
import json
import mcp.types as types
from core.helpers import validate_path, extract_python_skeleton, extract_regex_skeleton

def get_tool() -> types.Tool:
    return types.Tool(
        name="get_file_skeleton",
        description="Parses a code file and returns ONLY its skeleton (classes, functions, arguments, docstrings). NO implementation bodies.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file to parse."}
            },
            "required": ["file_path"],
        },
    )

async def execute(arguments: dict) -> list[types.TextContent]:
    raw_path = arguments.get("file_path")
    
    if not raw_path:
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing 'file_path' argument."}))]
        
    try:
        validated_path = validate_path(raw_path)
    except ValueError as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}))]
        
    if not os.path.isfile(validated_path):
        return [types.TextContent(type="text", text=json.dumps({"error": f"File not found: {validated_path}"}))]
        
    try:
        with open(validated_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        ext = os.path.splitext(validated_path)[1].lower()
        
        if ext in ['.py']:
            skeleton = extract_python_skeleton(content)
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            skeleton = extract_regex_skeleton(content)
        else:
            return [types.TextContent(type="text", text=json.dumps({"error": f"Unsupported file extension {ext} for skeleton parser."}))]
            
        output_format = f"### File: {os.path.basename(validated_path)}\n```\n{skeleton}\n```"
        return [types.TextContent(type="text", text=output_format)]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error parsing skeleton: {str(e)}"}))]
