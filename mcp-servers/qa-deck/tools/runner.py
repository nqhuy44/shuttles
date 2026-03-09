import subprocess
import shlex
import json
import re
import mcp.types as types
from typing import Any

ALLOWED_COMMANDS = {"pytest", "python3", "python"}

def get_tool() -> types.Tool:
    return types.Tool(
        name="run_test_compact",
        description="Runs a test file or suite and aggressively filters the output. Returns only a concise summary and failures.",
        inputSchema={
            "type": "object",
            "properties": {
                "test_command": {"type": "string", "description": "e.g., 'pytest tests/test_core.py'"},
                "working_dir": {"type": "string", "description": "The directory to run tests in"}
            },
            "required": ["test_command", "working_dir"]
        }
    )

async def execute(arguments: dict[str, Any]) -> str:
    test_command = arguments.get("test_command", "")
    working_dir = arguments.get("working_dir", ".")

    try:
        parts = shlex.split(test_command)
        if not parts:
            return "Error: Empty test command."
        
        base_cmd = parts[0]
        if base_cmd not in ALLOWED_COMMANDS:
            return f"Error: Command '{base_cmd}' is not allowed for security reasons."

        # Force pytest to output in a way we can parse easily, or just use quiet mode
        if base_cmd == "pytest" and "-q" not in parts:
            parts.insert(1, "-q")
            parts.insert(2, "--tb=short") # Short tracebacks

        result = subprocess.run(
            parts,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=30 # Tests might take longer
        )

        output = result.stdout + result.stderr
        
        # Simple extraction logic for pytest failures
        # Pytest -q output usually looks like:
        # F.
        # ================================= FAILURES =================================
        # ___________________________ test_failure ___________________________
        # tests/test_core.py:10: AssertionError
        # E       assert False
        
        summary = {
            "total": 0,
            "passed": output.count("."),
            "failed": output.count("F"),
            "errors": output.count("E"),
            "skipped": output.count("s")
        }
        summary["total"] = summary["passed"] + summary["failed"] + summary["errors"] + summary["skipped"]

        failures = []
        if summary["failed"] > 0 or summary["errors"] > 0:
            # Extract failure messages using a regex or simple split
            # This is a basic implementation, can be refined
            failure_sections = re.split(r'={10,}\sFAILURES\s={10,}', output)
            if len(failure_sections) > 1:
                details = failure_sections[1].split('short test summary info')[0]
                failures.append(details.strip())
            else:
                # If structure is different, just return the last few lines of output
                failures.append("Could not parse failure details automatically. Raw output snippet follows:")
                failures.append("\n".join(output.splitlines()[-20:]))

        return json.dumps({
            "summary": summary,
            "failures": failures
        }, indent=2)

    except subprocess.TimeoutExpired:
        return "Error: Test command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing tests: {str(e)}"
