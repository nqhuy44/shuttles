import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any

def scan_ui_components(directory_path: str) -> str:
    """
    Scans a directory for UI components and extracts their names and props.
    """
    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        return json.dumps({"error": f"Directory {directory_path} not found or is not a directory."})
    
    registry = []
    
    # Supported extensions
    extensions = {'.tsx', '.jsx', '.vue', '.svelte'}
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in extensions:
                content = file_path.read_text(encoding="utf-8")
                
                # 1. Component Name (filename usually, or export default/const ...)
                component_name = file_path.stem
                if component_name == "index":
                    component_name = file_path.parent.name
                
                # 2. Extract Props (Simplified Regex approach)
                # Matches: interface Props { ... } or type Props = { ... } or defineProps({ ... })
                props = []
                
                # TS Interface/Type
                match_ts = re.search(r"(?:interface|type)\s+(?:Props|.*?Props)\s*=?\s*\{(.*?)\}", content, re.DOTALL)
                if match_ts:
                    prop_defs = re.findall(r"([a-zA-Z0-9_-]+)\s*(\??)\s*:", match_ts.group(1))
                    props.extend([p[0] for p in prop_defs])
                
                # Vue defineProps
                match_vue = re.search(r"defineProps\s*\(\s*\{(.*?)\}\s*\)", content, re.DOTALL)
                if match_vue:
                    prop_defs = re.findall(r"([a-zA-Z0-9_-]+)\s*:", match_vue.group(1))
                    props.extend([p[0] for p in prop_defs])

                # React Func Param Destructuring: const MyComp = ({ prop1, prop2 }) =>
                match_react = re.search(r"const\s+" + re.escape(component_name) + r"\s*=\s*\(\s*\{(.*?)\}\s*\)", content, re.DOTALL)
                if match_react:
                    prop_defs = re.findall(r"([a-zA-Z0-9_-]+)(?:\s*[:,]|\s*[=}]|$)", match_react.group(1))
                    props.extend([p[0] for p in prop_defs if p[0] not in {'key', 'children'}])

                registry.append({
                    "name": component_name,
                    "file": str(file_path.relative_to(directory_path)),
                    "props": sorted(list(set(props)))
                })

    return json.dumps(registry, indent=2)
