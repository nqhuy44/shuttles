import subprocess
import shlex
import mcp.types as types
from typing import Any

ALLOWED_COMMANDS = {"python", "python3", "pytest", "node", "npm", "npx", "go"}

def get_tool() -> types.Tool:
    return types.Tool(
        name="run_and_capture",
        description="Safely executes a specific script or test command and strictly captures the error output if it fails.",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "working_dir": {"type": "string"}
            },
            "required": ["command"]
        }
    )

async def execute(arguments: dict[str, Any]) -> str:
    command = arguments.get("command", "")
    working_dir = arguments.get("working_dir", ".")
    
    try:
        parts = shlex.split(command)
        if not parts:
            return "Error: Empty command string given."
        
        base_cmd = parts[0]
        if base_cmd not in ALLOWED_COMMANDS:
            return f"Error: Command '{base_cmd}' is not allowed for security reasons."
        
        result = subprocess.run(
            parts,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return "Success"
        else:
            if result.stderr.strip():
                return result.stderr.strip()
            else:
                lines = result.stdout.strip().splitlines()
                return "\\n".join(lines[-50:])
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 10 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"
