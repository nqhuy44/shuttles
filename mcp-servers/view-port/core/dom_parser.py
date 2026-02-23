import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

def extract_dom_skeleton(file_path: str) -> str:
    """
    Strips inner text and noise from HTML/JSX, keeping only structural tags, IDs, and classes.
    """
    path = Path(file_path)
    if not path.exists():
        return f"Error: File {file_path} not found."
    
    content = path.read_text(encoding="utf-8")
    
    # Handle JSX: BeautifulSoup doesn't like JSX-specific syntax well (like fragments <> or curly braces {})
    # We do a pre-processing to make it look like more standard HTML for the parser if it's JSX
    if file_path.endswith(('.jsx', '.tsx')):
        # Remove JSX curly brace expressions {...} or replace them with a placeholder
        content = re.sub(r'\{.*?\}', '"jsx-expr"', content)
        # Handle fragments <></> by replacing them with <div>
        content = re.sub(r'<>\s*', '<div>', content)
        content = re.sub(r'\s*</>', '</div>', content)

    soup = BeautifulSoup(content, 'lxml')
    
    # List of attributes to keep
    KEEP_ATTRS = ['id', 'class', 'className']
    
    def process_element(element):
        if hasattr(element, 'string') and element.string:
            element.string = "" # Strip text
            
        # Filter attributes
        if hasattr(element, 'attrs'):
            new_attrs = {}
            for attr in KEEP_ATTRS:
                if attr in element.attrs:
                    val = element.attrs[attr]
                    if isinstance(val, list):
                        new_attrs[attr] = " ".join(val)
                    else:
                        new_attrs[attr] = val
            element.attrs = new_attrs
            
        for child in element.find_all(recursive=False):
            process_element(child)

    # Clean up scripts, styles, and comments first
    for s in soup(["script", "style"]):
        s.decompose()
    
    # Process from root
    if soup.body:
        process_element(soup.body)
        return soup.body.prettify()
    else:
        # For snippets
        for tag in soup.find_all(True, recursive=False):
            process_element(tag)
        return soup.prettify()
