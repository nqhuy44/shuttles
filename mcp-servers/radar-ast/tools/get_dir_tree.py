import os
import json
import mcp.types as types
from core.helpers import validate_path

NOISE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', '.next', 'dist', 'build', 'env', '.venv', '.nx', '.idea', '.vscode'}
NOISE_FILES = {'.DS_Store'}

def _build_tree(startpath: str, max_depth: int) -> str:
    tree_str = []
    startpath = os.path.abspath(startpath)
    
    for root, dirs, files in os.walk(startpath):
        # Calculate current depth
        level = root.replace(startpath, '').count(os.sep)
        
        # Prune search early if over depth
        if level > max_depth:
            del dirs[:] 
            continue
            
        # Prune noise directories in place so os.walk doesn't visit them
        dirs[:] = [d for d in dirs if d not in NOISE_DIRS and not d.endswith('.egg-info')]
        
        indent = ' ' * 4 * (level)
        tree_str.append(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 4 * (level + 1)
        for f in sorted(files):
            if f in NOISE_FILES or f.endswith('.pyc') or f.endswith('.pyo'):
                continue
            tree_str.append(f"{subindent}{f}")
            
    return '\n'.join(tree_str)

def get_tool() -> types.Tool:
    return types.Tool(
        name="get_dir_tree",
        description="Returns a token-optimized tree structure of a given directory. Automatically ignores noise folders like node_modules and venv.",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The directory to scan, relative to workspace or absolute."},
                "max_depth": {"type": "integer", "description": "How deep to scan the tree. Default 3", "default": 3}
            },
            "required": ["path"],
        },
    )

async def execute(arguments: dict) -> list[types.TextContent]:
    raw_path = arguments.get("path")
    max_depth = arguments.get("max_depth", 3)
    
    if not raw_path:
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing 'path' argument."}))]
        
    try:
        validated_path = validate_path(raw_path)
    except ValueError as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}))]
        
    if not os.path.isdir(validated_path):
        return [types.TextContent(type="text", text=json.dumps({"error": f"Path is not a valid directory: {validated_path}"}))]
        
    tree_output = _build_tree(validated_path, max_depth)
    return [types.TextContent(type="text", text=tree_output)]
