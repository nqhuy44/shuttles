import os
import json
import mcp.types as types
from core.helpers import validate_path

def get_tool() -> types.Tool:
    return types.Tool(
        name="read_specific_lines",
        description="Reads exact lines from a file. Useful when the AI needs to see specific implementation details.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file to read."},
                "start_line": {"type": "integer", "description": "1-based starting line number."},
                "end_line": {"type": "integer", "description": "1-based ending line number."}
            },
            "required": ["file_path", "start_line", "end_line"],
        },
    )

async def execute(arguments: dict) -> list[types.TextContent]:
    raw_path = arguments.get("file_path")
    start_line = arguments.get("start_line")
    end_line = arguments.get("end_line")
    
    if not all([raw_path, start_line, end_line]):
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing 'file_path', 'start_line', or 'end_line'."}))]
        
    try:
        validated_path = validate_path(raw_path)
    except ValueError as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}))]
        
    if not os.path.isfile(validated_path):
        return [types.TextContent(type="text", text=json.dumps({"error": f"File not found: {validated_path}"}))]
        
    if start_line > end_line or start_line < 1:
        return [types.TextContent(type="text", text=json.dumps({"error": "Invalid line range."}))]
        
    try:
        with open(validated_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        total_lines = len(lines)
        actual_end = min(end_line, total_lines)
        
        if start_line > total_lines:
             return [types.TextContent(type="text", text=json.dumps({"error": f"Start line {start_line} is beyond file length ({total_lines})."}))]
             
        snippet = []
        # Convert 1-based index to 0-based for slicing
        for i in range(start_line - 1, actual_end):
             # Prefix with line number: "15: def example():"
             snippet.append(f"{i + 1}: {lines[i].rstrip('\n')}")
             
        output_format = f"### File: {os.path.basename(validated_path)} (Lines {start_line}-{actual_end})\n```\n" + '\n'.join(snippet) + "\n```"
        return [types.TextContent(type="text", text=output_format)]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error reading lines: {str(e)}"}))]
