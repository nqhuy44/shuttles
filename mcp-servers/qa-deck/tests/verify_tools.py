import asyncio
import json
import os
import sys

# Add the parent directory to sys.path to import tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tools.runner
import tools.coverage
import tools.diagnoser

async def test_runner():
    print("Testing runner.py...")
    # This might fail if pytest is not in path or no tests exist, but we check the logic
    # Create a dummy test file
    os.makedirs("tests", exist_ok=True)
    with open("tests/test_dummy.py", "w") as f:
        f.write("def test_pass(): assert True\ndef test_fail(): assert False\n")
    
    args = {"test_command": "pytest tests/test_dummy.py", "working_dir": "."}
    res = await tools.runner.execute(args)
    print(f"Runner Result: {res}")
    os.remove("tests/test_dummy.py")

async def test_coverage():
    print("\nTesting coverage.py...")
    # Create a dummy coverage.xml
    with open("coverage.xml", "w") as f:
        f.write('<?xml version="1.0" ?><coverage version="7.0"><packages><package name="p"><classes>'
                '<class filename="core.py" name="core"><lines>'
                '<line hits="1" number="1"/><line hits="0" number="2"/><line hits="0" number="5"/>'
                '</lines></class></classes></package></packages></coverage>')
    
    args = {"coverage_file_path": "coverage.xml", "target_file": "core.py"}
    res = await tools.coverage.execute(args)
    print(f"Coverage Result: {res}")
    os.remove("coverage.xml")

async def main():
    await test_runner()
    await test_coverage()
    # Note: diagnose_failure_local requires Ollama, so we skip it in auto-test
    # unless we mock httpx.

if __name__ == "__main__":
    asyncio.run(main())
