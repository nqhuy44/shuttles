import re
from pathlib import Path
from typing import List, Optional

def get_markdown_toc(file_path: str) -> str:
    """
    Extracts the Table of Contents from a Markdown file.
    Ignores headings inside code blocks.
    """
    path = Path(file_path)
    if not path.exists():
        return f"Error: File {file_path} not found."
    
    content = path.read_text(encoding="utf-8")
    
    # Remove code blocks to avoid false positives
    content_no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    
    # Regex for headings: starts with #, ##, etc.
    heading_pattern = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
    headings = heading_pattern.findall(content_no_code)
    
    if not headings:
        return "No headings found in the document."
    
    toc = []
    for level_hashes, title in headings:
        level = len(level_hashes)
        indent = "  " * (level - 1)
        toc.append(f"{indent}- {title}")
    
    return "\n".join(toc)

def patch_doc_section(file_path: str, heading_name: str, new_content: str) -> str:
    """
    Replaces the content of a specific section in a Markdown file.
    Finds the requested heading and replaces text until the next heading of same or higher level.
    """
    path = Path(file_path)
    if not path.exists():
        return f"Error: File {file_path} not found."
    
    lines = path.read_text(encoding="utf-8").splitlines()
    
    # Regex for heading match (case-insensitive for more robustness but prompt says "exact match")
    # Let's stick to exact match as requested.
    heading_pattern = re.compile(r"^(#{1,6})\s+" + re.escape(heading_name) + r"$")
    
    start_idx = -1
    target_level = -1
    
    for i, line in enumerate(lines):
        match = heading_pattern.match(line)
        if match:
            start_idx = i
            target_level = len(match.group(1))
            break
            
    if start_idx == -1:
        return f"Error: Heading '{heading_name}' not found."
    
    end_idx = len(lines)
    # Find the next heading of same or higher level (<= target_level hashes)
    for i in range(start_idx + 1, len(lines)):
        match = re.match(r"^(#{1,6})\s+", lines[i])
        if match:
            current_level = len(match.group(1))
            if current_level <= target_level:
                end_idx = i
                break
    
    # Reconstruct the file
    # We keep the heading line (lines[start_idx]) and replace the rest until end_idx
    new_lines = lines[:start_idx + 1] + [new_content] + lines[end_idx:]
    
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    
    return f"Successfully patched section '{heading_name}' in {file_path}."
