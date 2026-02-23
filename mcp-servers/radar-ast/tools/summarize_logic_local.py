import os
import json
import mcp.types as types
from core.helpers import validate_path, call_ollama_local

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5-coder")
NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "32768"))
TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))

def get_tool() -> types.Tool:
    return types.Tool(
        name="summarize_logic_local",
        description="[REQUIRES LOCAL GPU/Ollama] Uses the local Ollama model to summarize the implementation details of a specific function or file, preventing the Cloud AI from having to read raw code.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file to summarize."},
                "function_name": {"type": "string", "description": "Optional: Name of specific function/class to focus on."}
            },
            "required": ["file_path"],
        },
    )

async def execute(arguments: dict) -> list[types.TextContent]:
    raw_path = arguments.get("file_path")
    func_name = arguments.get("function_name", "the entire file")
    
    if not raw_path:
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing 'file_path'."}))]
        
    try:
        validated_path = validate_path(raw_path)
    except ValueError as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}))]
        
    if not os.path.isfile(validated_path):
        return [types.TextContent(type="text", text=json.dumps({"error": f"File not found: {validated_path}"}))]
        
    try:
        with open(validated_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
            
        prompt = f"Summarize the core logic of {func_name} in 3 concise bullet points. Focus on inputs, outputs, and side effects. Code:\n\n{code_content}"
        
        summary = call_ollama_local(prompt)
        
        output_format = f"### Local LLM Summary for {os.path.basename(validated_path)} ({func_name})\n\n{summary}"
        return [types.TextContent(type="text", text=output_format)]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error during summarization: {str(e)}"}))]
