import ast
import re
from pathlib import Path
from typing import Optional, Tuple

def extract_function_source(file_path: str, function_name: str) -> Optional[str]:
    """
    Extracts the source code of a specific function from a Python file using AST.
    """
    path = Path(file_path)
    if not path.exists():
        return None
    
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == function_name:
            # We need to get the actual source lines. ast nodes have lineno and end_lineno in Python 3.8+
            lines = source.splitlines()
            start = node.lineno - 1
            end = node.end_lineno
            return "\n".join(lines[start:end])
            
    return None

async def generate_inline_docs(file_path: str, function_name: str) -> str:
    """
    Generates docstrings for functions/classes automatically using local LLM and inserts them.
    """
    source_code = extract_function_source(file_path, function_name)
    if not source_code:
        return f"Error: Function/Class '{function_name}' not found in {file_path}."
    
    from .ollama_client import OllamaClient
    client = OllamaClient()
    
    prompt = f"Write a professional Python docstring (Google style) for this function. Return ONLY the docstring text itself. Do NOT include the function signature, triple quotes, or markdown code blocks. Function:\n{source_code}"
    
    docstring = await client.generate(
        model="qwen2.5-coder:14b",
        prompt=prompt
    )
    
    if docstring.startswith("Error:"):
        return docstring

    # Clean up docstring: remove triple backticks code blocks if the LLM wrapped it
    docstring = re.sub(r'```(?:python)?\n?(.*?)\n?```', r'\1', docstring, flags=re.DOTALL).strip()
    
    # Remove any repetition of the function/class header if the LLM included it
    docstring = re.sub(r'^(def|class)\s+\w+.*?:\s*', '', docstring, flags=re.DOTALL | re.IGNORECASE).strip()

    # Remove leading/trailing triple quotes if they exist, we will add them back correctly
    docstring = docstring.strip('\"\' ')
    
    # Construct final docstring
    docstring = f'"""\n{docstring}\n"""'

    # Insertion logic
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == function_name:
            # Find the line after the definition ends
            # The definition ends at node.lineno (for basic def) but can span multiple lines if there are decorators or long params.
            # However, ast.FunctionDef.lineno in Python 3.8+ usually points to the 'def' line.
            # We want to insert it after the ':' of the def statement.
            
            # Simple approach: find the line with the 'def' or 'class' and find the first colon
            # More robust: use the line index of the first statement in the body if it exists, 
            # otherwise just below the lineno.
            
            # Let's find the correct insertion line index.
            # node.body[0] is the first statement in the function.
            # If it's already a docstring (Expr(Constant(str))), we replace it.
            
            first_stmt = node.body[0] if node.body else None
            is_existing_doc = False
            if first_stmt and isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant) and isinstance(first_stmt.value.value, str):
                is_existing_doc = True
            
            # indentation
            # We need to match the indentation of the body.
            if node.body:
                # Find indentation of the first body line
                body_line = lines[node.body[0].lineno - 1]
                match = re.match(r"^(\s+)", body_line)
                indent = match.group(1) if match else "    "
            else:
                # Fallback indentation
                def_line = lines[node.lineno - 1]
                match = re.match(r"^(\s*)", def_line)
                indent = match.group(1) + "    "
            
            indented_docstring = "\n".join([f"{indent}{l}" for l in docstring.splitlines()])
            
            if is_existing_doc:
                # Replace existing docstring
                # first_stmt.lineno and first_stmt.end_lineno
                start_doc = first_stmt.lineno - 1
                end_doc = first_stmt.end_lineno
                new_lines = lines[:start_doc] + [indented_docstring] + lines[end_doc:]
            else:
                # Insert below the def statement. 
                # The def statement might be multi-line. node.body[0].lineno - 1 is where the body starts.
                # We insert just before that.
                insert_idx = node.body[0].lineno - 1
                new_lines = lines[:insert_idx] + [indented_docstring] + lines[insert_idx:]
            
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            return f"Successfully generated and inserted docstring for '{function_name}'."
            
    return f"Error: Could not find insertion point for '{function_name}'."
