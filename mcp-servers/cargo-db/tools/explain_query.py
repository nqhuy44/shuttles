import json
import mcp.types as types
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def get_tool() -> types.Tool:
    return types.Tool(
        name="explain_query",
        description="Evaluates a SQL query and returns the execution plan to check performance and syntax without running the actual query.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The SQL query to EXPLAIN"}
            },
            "required": ["query"],
        },
    )

async def execute(arguments: dict, engine) -> list[types.TextContent]:
    query = arguments.get("query")
    if not query:
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing query argument."}))]
    
    try:
        dialect = engine.dialect.name
        
        with engine.connect() as conn:
            try:
                # Map correctly to SQL Dialects
                if dialect == "sqlite":
                    explain_query = text(f"EXPLAIN QUERY PLAN {query}")
                    result = conn.execute(explain_query)
                    rows = [dict(row._mapping) for row in result]
                elif dialect == "mssql":
                    # MS SQL standard for fetching query plan without execution
                    conn.execute(text("SET SHOWPLAN_ALL ON"))
                    # Note: The query itself doesn't execute rows, but returns the plan
                    result = conn.execute(text(query))
                    rows = [dict(row._mapping) for row in result]
                    conn.execute(text("SET SHOWPLAN_ALL OFF"))
                else:
                    # Standard default for PostgreSQL, MySQL
                    explain_query = text(f"EXPLAIN {query}")
                    result = conn.execute(explain_query)
                    rows = [dict(row._mapping) for row in result]
                    
                return [types.TextContent(type="text", text=json.dumps({"plan": rows}, default=str, separators=(',', ':')))]
            except SQLAlchemyError as e:
                return [types.TextContent(type="text", text=json.dumps({"error": f"Error executing EXPLAIN: {str(e)}"}))]
            
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Database interaction error: {str(e)}"}))]
