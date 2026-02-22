import json
import mcp.types as types
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

def get_tool() -> types.Tool:
    return types.Tool(
        name="get_schema",
        description="Extracts the DDL/Schema of a table in a highly optimized format (Ruthless Token Efficiency). Returns only Column Name, Data Type, Primary Key, and Foreign Key targets.",
        inputSchema={
            "type": "object",
            "properties": {
                "table_name": {"type": "string", "description": "Name of the table to extract schema for"}
            },
            "required": ["table_name"],
        },
    )

async def execute(arguments: dict, engine) -> list[types.TextContent]:
    table_name = arguments.get("table_name")
    if not table_name:
        return [types.TextContent(type="text", text=json.dumps({"error": "Missing table_name argument."}))]
    
    try:
        insp = inspect(engine)
        if not insp.has_table(table_name):
            return [types.TextContent(type="text", text=json.dumps({"error": f"Table '{table_name}' does not exist."}))]
        
        columns = insp.get_columns(table_name)
        try:
            pk_constraint = insp.get_pk_constraint(table_name)
            pks = pk_constraint.get("constrained_columns", [])
        except NotImplementedError:
            pks = []
            
        try:
            fk_constraints = insp.get_foreign_keys(table_name)
            fks = {}
            for fk in fk_constraints:
                for col, ref_col in zip(fk.get("constrained_columns", []), fk.get("referred_columns", [])):
                    fks[col] = f"{fk.get('referred_table')}.{ref_col}"
        except NotImplementedError:
            fks = {}
        
        # Ruthless Token Efficiency: Only append valid flags rather than full structures
        optimized_schema = []
        for col in columns:
            col_info = {
                "name": col["name"],
                "type": str(col["type"])
            }
            if col["name"] in pks:
                col_info["pk"] = True
            if col["name"] in fks:
                col_info["fk"] = fks[col["name"]]
            optimized_schema.append(col_info)
            
        return [types.TextContent(type="text", text=json.dumps({"table": table_name, "schema": optimized_schema}, separators=(',', ':')))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": f"Error getting schema for {table_name}: {str(e)}"}))]
