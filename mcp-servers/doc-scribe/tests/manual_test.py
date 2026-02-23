import asyncio
import os
from core.markdown_utils import get_markdown_toc, patch_doc_section
from core.ollama_client import summarize_doc_local
from core.ast_utils import generate_inline_docs

async def run_tests():
    readme_path = os.path.join(os.getcwd(), "README.md")
    print(f"--- Testing Markdown TOC on {readme_path} ---")
    toc = get_markdown_toc(readme_path)
    print(toc)
    
    print("\n--- Testing Markdown Patching ---")
    # Create a dummy file for patching
    test_md = "test_doc.md"
    with open(test_md, "w") as f:
        f.write("# Main\nContent\n## Section 1\nOld content\n## Section 2\nOther content\n")
    
    result = patch_doc_section(test_md, "Section 1", "Newly patched content!")
    print(result)
    with open(test_md, "r") as f:
        print(f.read())
    os.remove(test_md)

    print("\n--- Testing Ollama Summarization (Requires Ollama) ---")
    summary = await summarize_doc_local(readme_path, "What is doc-scribe?")
    print(summary)

    print("\n--- Testing Inline Docstrings (Requires Ollama) ---")
    test_py = "test_code.py"
    with open(test_py, "w") as f:
        f.write("def calculate_sum(a, b):\n    return a + b\n")
    
    result = await generate_inline_docs(test_py, "calculate_sum")
    print(result)
    with open(test_py, "r") as f:
        print(f.read())
    os.remove(test_py)

if __name__ == "__main__":
    asyncio.run(run_tests())
