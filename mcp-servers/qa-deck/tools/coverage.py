import mcp.types as types
import json
from lxml import etree
from typing import Any
import os

def get_tool() -> types.Tool:
    return types.Tool(
        name="get_coverage_gaps",
        description="Checks test coverage for a specific file and returns uncovered line numbers.",
        inputSchema={
            "type": "object",
            "properties": {
                "coverage_file_path": {"type": "string", "description": "Path to coverage.xml"},
                "target_file": {"type": "string", "description": "The file to check coverage for (relative path or filename)"}
            },
            "required": ["coverage_file_path", "target_file"]
        }
    )

async def execute(arguments: dict[str, Any]) -> str:
    coverage_path = arguments.get("coverage_file_path", "")
    target_file = arguments.get("target_file", "")

    if not os.path.exists(coverage_path):
        return f"Error: Coverage file not found at {coverage_path}"

    try:
        tree = etree.parse(coverage_path)
        root = tree.getroot()
        
        # In Cobertura XML format
        uncovered_lines = []
        
        # Try to find the class element focusing on the target_file
        # Check by filename first
        classes = root.xpath(f"//class[contains(@filename, '{target_file}')]")
        
        if not classes:
            return f"Error: No coverage data found for file '{target_file}' in {coverage_path}"

        for cls in classes:
            lines = cls.xpath(".//line[@hits='0']")
            for line in lines:
                uncovered_lines.append(int(line.get("number")))

        return json.dumps({"uncovered_lines": sorted(list(set(uncovered_lines)))})

    except Exception as e:
        return f"Error parsing coverage file: {str(e)}"
