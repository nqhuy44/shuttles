import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any

def extract_design_tokens(file_path: str) -> str:
    """
    Extracts design tokens (colors, spacing, fonts) from tailwind.config or CSS variables.
    """
    path = Path(file_path)
    if not path.exists():
        return json.dumps({"error": f"File {file_path} not found."})
    
    content = path.read_text(encoding="utf-8")
    
    tokens = {
        "colors": [],
        "spacing": [],
        "fonts": []
    }
    
    # 1. Try to find tailwind-style colors: 'primary': '#...' or primary: '#...'
    # This is a simplified regex, but good enough for token discovery.
    color_matches = re.findall(r"['\"]?([a-zA-Z0-9-]+)['\"]?\s*:\s*['\"](#[a-fA-F0-9]{3,8}|rgba?\(.*?\)|hsla?\(.*?\))['\"]", content)
    if color_matches:
        tokens["colors"] = list(set([m[0] for m in color_matches]))
    
    # 2. Try to find CSS variables: --color-primary: ...
    css_var_matches = re.findall(r"--([a-zA-Z0-9-]+)\s*:", content)
    if css_var_matches:
        for var in css_var_matches:
            if "color" in var or "bg" in var or "text" in var:
                tokens["colors"].append(var)
            elif "spacing" in var or "gap" in var or "p-" in var or "m-" in var:
                tokens["spacing"].append(var)
            elif "font" in var:
                tokens["fonts"].append(var)

    # 3. Handle spacing if explicitly defined in tailwind config
    spacing_matches = re.findall(r"spacing\s*:\s*\{(.*?)\}", content, re.DOTALL)
    if spacing_matches:
        keys = re.findall(r"['\"]?([a-zA-Z0-9.-]+)['\"]?\s*:", spacing_matches[0])
        tokens["spacing"].extend(keys)

    # De-duplicate
    tokens["colors"] = sorted(list(set(tokens["colors"])))
    tokens["spacing"] = sorted(list(set(tokens["spacing"])))
    tokens["fonts"] = sorted(list(set(tokens["fonts"])))

    return json.dumps(tokens, indent=2)
