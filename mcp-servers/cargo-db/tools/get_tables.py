import json
import mcp.types as types
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

def get_tool() -> types.Tool:
    return types.Tool(
        name="get_tables",
        description="Returns a list of all tables in the database.",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    )

async def execute(arguments: dict, engine) -> list[types.TextContent]:
    try:
        insp = inspect(engine)
        tables = insp.get_table_names()
        return [types.TextContent(type="text", text=json.dumps({"tables": tables}, separators=(',', ':')))]
    except SQLAlchemyError as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error listing tables: {str(e)}"}))]
