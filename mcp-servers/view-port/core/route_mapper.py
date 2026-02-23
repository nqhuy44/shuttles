import os
import os.path
import re
import json
from pathlib import Path
from typing import List

def map_frontend_routes(directory_path: str) -> str:
    """
    Scans a routing directory to build a list of valid URL paths.
    Supports Next.js (App/Pages) and general folder-based routing.
    """
    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        return json.dumps({"error": f"Directory {directory_path} not found or is not a directory."})
    
    routes = []
    
    # Determine type of routing
    # Check for 'app' directory (Next.js App Router)
    is_app_router = "app" in path.parts or (path / "page.tsx").exists() or (path / "page.jsx").exists()

    for root, dirs, files in os.walk(directory_path):
        rel_path = os.path.relpath(root, directory_path)
        
        # Skip internal folders like _components, (groups) in Next.js
        if any(d.startswith('_') or (d.startswith('(') and d.endswith(')')) for d in rel_path.split(os.sep)):
            continue

        for file in files:
            # Next.js App Router: page.tsx/page.jsx/page.js
            if is_app_router:
                if file in ["page.tsx", "page.jsx", "page.js"]:
                    route = "/" + rel_path if rel_path != "." else "/"
                    # Cleanup rel_path formatting
                    route = route.replace("\\", "/") # Windows compat
                    # Handle dynamic routes [id] -> :id
                    route = re.sub(r'\[(.*?)\]', r':\1', route)
                    routes.append(route)
            
            # Next.js Pages Router / General: index.tsx, user.tsx, [id].tsx
            else:
                if file.endswith(('.tsx', '.jsx', '.js', '.vue')):
                    clean_name = Path(file).stem
                    route_base = "/" + rel_path if rel_path != "." else ""
                    route_base = route_base.replace("\\", "/")
                    
                    if clean_name == "index":
                        route = route_base if route_base else "/"
                    else:
                        route = f"{route_base}/{clean_name}"
                    
                    # Handle dynamic routes
                    route = re.sub(r'\[(.*?)\]', r':\1', route)
                    routes.append(route)

    return json.dumps(sorted(list(set(routes))), indent=2)
