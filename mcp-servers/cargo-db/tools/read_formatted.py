import json
import mcp.types as types
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def _validate_select_only(query: str) -> bool:
    """
    Validates that a given SQL query starts with SELECT (case-insensitive)
    to prevent accidental state mutations.
    """
    stripped_query = query.strip().upper()
    return stripped_query.startswith("SELECT")

def get_tool() -> types.Tool:
    return types.Tool(
        name="read_formatted",
        description="Executes a SELECT query and returns the results in a Token Optimized Output Notation (TOON) format (Array of Arrays). Only allowed for SELECT statements. Max 50 rows.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The exact SELECT query to run"}
            },
            "required": ["query"],
        },
    )

async def execute(arguments: dict, engine) -> list[types.TextContent]:
    query = arguments.get("query")
    if not query:
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing query argument."}))]
        
    if not _validate_select_only(query):
        return [types.TextContent(type="text", text=json.dumps({"error": "Invalid query. Only SELECT queries are permitted for safety."}))]
        
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            
            # Fetch up to 50 rows directly
            rows = result.fetchmany(50)
            
            if not rows:
                return [types.TextContent(type="text", text=json.dumps({"data": []}))]
            
            # TOON Format: Array of Arrays
            # First array is headers
            headers = list(result.keys())
            toon_data = [headers]
            
            # Subsequent arrays are row values
            for row in rows:
                toon_data.append(list(row))
                
            return [types.TextContent(type="text", text=json.dumps({"data": toon_data}, default=str, separators=(',', ':')))]
            
    except SQLAlchemyError as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error executing query: {str(e)}"}))]
