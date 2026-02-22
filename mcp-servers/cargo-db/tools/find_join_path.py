import json
import mcp.types as types
from sqlalchemy import inspect
from collections import deque

def _bfs_find_path(tables: list[str], engine) -> str:
    """
    Finds the shortest JOIN path connecting a list of tables using BFS on foreign keys.
    Returns the explicitly formatted JOIN string.
    """
    if not tables or len(tables) < 2:
        return "At least two tables are required to find a join path."
        
    insp = inspect(engine)
    
    # 1. Build adjacency list of all tables
    # Node -> List[(TargetNode, SourceCol, TargetCol)]
    graph = {}
    all_tables = insp.get_table_names()
    for t in all_tables:
        graph[t] = []
        try:
            fks = insp.get_foreign_keys(t)
            for fk in fks:
                ref_table = fk.get("referred_table")
                if not ref_table: continue
                # Add directed edges both ways for undirected traversal
                for s_col, t_col in zip(fk.get("constrained_columns", []), fk.get("referred_columns", [])):
                    graph[t].append((ref_table, s_col, t_col))
                    
                    if ref_table not in graph:
                        graph[ref_table] = []
                    graph[ref_table].append((t, t_col, s_col))
        except NotImplementedError:
            continue
            
    # 2. Find path between tables consecutively
    full_join_clauses = []
    current_table = tables[0]
    
    visited_tables = {current_table}
    
    for next_table in tables[1:]:
        if current_table not in graph or next_table not in graph:
            return f"Table '{current_table}' or '{next_table}' not found in schema graph."
            
        queue = deque([(current_table, [])]) # (node, path_of_edges)
        visited_in_search = set([current_table])
        found_path = None
        
        while queue:
            curr, path = queue.popleft()
            if curr == next_table:
                found_path = path
                break
                
            for neighbor, s_col, t_col in graph.get(curr, []):
                if neighbor not in visited_in_search:
                    visited_in_search.add(neighbor)
                    queue.append((neighbor, path + [(curr, neighbor, s_col, t_col)]))
                    
        if not found_path:
            return f"No relationship path found between '{current_table}' and '{next_table}'."
            
        # Append logic without duplicating tables
        for p_source, p_target, p_s_col, p_t_col in found_path:
            if p_target not in visited_tables:
                if not full_join_clauses:
                    full_join_clauses.append(f"{p_source} JOIN {p_target} ON {p_source}.{p_s_col} = {p_target}.{p_t_col}")
                else:
                    full_join_clauses.append(f"JOIN {p_target} ON {p_source}.{p_s_col} = {p_target}.{p_t_col}")
                visited_tables.add(p_target)
                
        current_table = next_table
        
    return " ".join(full_join_clauses)

def get_tool() -> types.Tool:
    return types.Tool(
        name="find_join_path",
        description="Inspects schema paths to find the exact JOIN statement connecting multiple tables.",
        inputSchema={
            "type": "object",
            "properties": {
                "tables": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "List of table names to connect, e.g. ['users', 'permissions']"
                }
            },
            "required": ["tables"],
        },
    )

async def execute(arguments: dict, engine) -> list[types.TextContent]:
    tables = arguments.get("tables", [])
    if not tables or not isinstance(tables, list):
        return [types.TextContent(type="text", text=json.dumps({"error": "Argument 'tables' must be a list of strings."}))]
        
    try:
        join_clause = _bfs_find_path(tables, engine)
        return [types.TextContent(type="text", text=json.dumps({"join_path": join_clause}, separators=(',', ':')))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error generating join path: {str(e)}"}))]
