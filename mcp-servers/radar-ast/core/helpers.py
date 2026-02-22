import os
import ast
import re
import urllib.request
import urllib.error
import json

def get_workspace_root() -> str:
    """
    Returns the absolute path of the workspace root (e.g. shuttles/ directory)
    Assumes this file is in shuttles/mcp-servers/radar-ast/core/
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up 3 levels: core -> radar-ast -> mcp-servers -> shuttles
    return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

def validate_path(file_path: str) -> str:
    """
    Validates that a path stays within the workspace root.
    Prevents path traversal attacks (e.g. ../../../etc/passwd).
    Returns the absolute path if valid, raises ValueError if not.
    """
    workspace_root = get_workspace_root()
    
    # Resolve the requested path
    if os.path.isabs(file_path):
        resolved_path = os.path.normpath(file_path)
    else:
        # Default relative paths to workspace root
        resolved_path = os.path.normpath(os.path.join(workspace_root, file_path))
        
    if not resolved_path.startswith(workspace_root):
        raise ValueError(f"Security Error: Path '{file_path}' attempts to traverse outside the workspace root.")
        
    return resolved_path

def extract_python_skeleton(content: str) -> str:
    """
    Parses Python code using the built-in `ast` module and returns ONLY the skeleton
    (classes, methods, functions, and their signatures/docstrings).
    Implementation bodies are replaced with `...`.
    """
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return f"Syntax Error during AST parsing: {str(e)}"

    output = []
    
    class SkeletonVisitor(ast.NodeVisitor):
        def visit_ClassDef(self, node):
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
            base_str = f"({', '.join(bases)})" if bases else ""
            output.append(f"class {node.name}{base_str}:")
            
            docstring = ast.get_docstring(node)
            if docstring:
                output.append(f'    """{docstring.split(chr(10))[0]}"""')
                
            # Process children without full body
            self.generic_visit(node)
            output.append("") # newline
            
        def visit_FunctionDef(self, node):
            self._visit_function(node, is_async=False)
            
        def visit_AsyncFunctionDef(self, node):
            self._visit_function(node, is_async=True)
            
        def _visit_function(self, node, is_async: bool):
            prefix = "async def " if is_async else "def "
            
            # Very basic extraction of arguments for token efficiency
            args = [a.arg for a in node.args.args]
            arg_str = ", ".join(args)
            
            returns = ""
            if type(node.returns) == ast.Name:
                returns = f" -> {node.returns.id}"
            elif type(node.returns) == ast.Constant:
                returns = f" -> {node.returns.value}"
                
            indent = "    " if isinstance(getattr(node, 'parent', None), ast.ClassDef) else ""
            
            output.append(f"{indent}{prefix}{node.name}({arg_str}){returns}: ...")
            
            docstring = ast.get_docstring(node)
            if docstring:
                output.append(f'{indent}    """{docstring.split(chr(10))[0]}"""')

    # Quick hack to assign parents for indentation logic
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
            
    visitor = SkeletonVisitor()
    visitor.visit(tree)
    
    if not output:
        return "No classes or functions found."
        
    return "\n".join(output)

def extract_regex_skeleton(content: str) -> str:
    """
    Lightweight regex-based parser for TS/JS files to extract skeleton structures.
    Finds classes, functions, interfaces, and arrow functions.
    """
    lines = content.splitlines()
    output = []
    
    # Regex patterns
    class_pattern = re.compile(r'^\s*(export\s+)?(default\s+)?class\s+(\w+)')
    interface_pattern = re.compile(r'^\s*(export\s+)?interface\s+(\w+)')
    func_pattern = re.compile(r'^\s*(export\s+)?(default\s+)?(async\s+)?function\s+(\w+)')
    arrow_pattern = re.compile(r'^\s*(export\s+)?const\s+(\w+)\s*=\s*(async\s+)?\([^)]*\)\s*=>')
    
    for line in lines:
        if class_pattern.search(line):
            output.append(line.strip() + " { ... }")
        elif interface_pattern.search(line):
            output.append(line.strip() + " { ... }")
        elif func_pattern.search(line):
            output.append(line.strip() + " { ... }")
        elif arrow_pattern.search(line):
            output.append(line.strip() + " { ... }")
            
    if not output:
        return "No clear structures found using lightweight regex parser."
        
    return "\n".join(output)

def call_ollama_local(prompt: str) -> str:
    """
    Makes a POST request to the local Ollama instance.
    Uses OLLAMA_API_URL and OLLAMA_MODEL from environment if present.
    """
    url = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
    model = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
    num_ctx = int(os.environ.get("OLLAMA_NUM_CTX", "32768"))
    temperature = float(os.environ.get("OLLAMA_TEMPERATURE", "0.1"))
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": num_ctx,
            "temperature": temperature
        }
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "Error: No response generated from model.")
    except urllib.error.URLError as e:
        return f"Connection Error to Ollama ({url}): {str(e)}. Please ensure Ollama is running locally and the model '{model}' is pulled."
    except Exception as e:
        return f"Unexpected Error calling Ollama: {str(e)}"
