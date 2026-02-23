import asyncio
import os
import json
from core.token_extractor import extract_design_tokens
from core.component_scanner import scan_ui_components
from core.dom_parser import extract_dom_skeleton
from core.route_mapper import map_frontend_routes

async def run_tests():
    print("--- Testing Design Token Extraction ---")
    test_css = "variables.css"
    with open(test_css, "w") as f:
        f.write(":root {\n  --color-primary: #007bff;\n  --spacing-md: 1rem;\n  --font-sans: 'Inter';\n}\n")
    print(extract_design_tokens(test_css))
    os.remove(test_css)

    print("\n--- Testing UI Component Scanning ---")
    os.makedirs("test_components", exist_ok=True)
    with open("test_components/Button.tsx", "w") as f:
        f.write("interface ButtonProps { variant: 'solid' | 'ghost'; isLoading?: boolean; }\nexport const Button = ({ variant, isLoading }: ButtonProps) => <button>{isLoading ? '...' : 'Click'}</button>;")
    print(scan_ui_components("test_components"))
    
    # Cleanup components
    for f in os.listdir("test_components"):
        os.remove(os.path.join("test_components", f))
    os.rmdir("test_components")

    print("\n--- Testing DOM Skeleton Extraction ---")
    test_jsx = "App.jsx"
    with open(test_jsx, "w") as f:
        f.write("<div id='app-root' className='bg-gray-100'>\n  <header className='flex justify-between'>\n    <h1 id='title'>Hello World</h1>\n    <nav>\n      <ul>\n        <li>Home</li>\n      </ul>\n    </nav>\n  </header>\n  <main>\n    <p>Content goes here</p>\n  </main>\n</div>")
    print(extract_dom_skeleton(test_jsx))
    os.remove(test_jsx)

    print("\n--- Testing Frontend Route Mapping ---")
    os.makedirs("test_app/users/[id]", exist_ok=True)
    with open("test_app/page.tsx", "w") as f: f.write("export default function Page() {}")
    with open("test_app/users/[id]/page.tsx", "w") as f: f.write("export default function UserPage() {}")
    print(map_frontend_routes("test_app"))
    
    # Cleanup app
    import shutil
    shutil.rmtree("test_app")

if __name__ == "__main__":
    asyncio.run(run_tests())
