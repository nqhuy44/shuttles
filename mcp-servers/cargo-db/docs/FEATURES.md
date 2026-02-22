# Features

## Database Introspection
Exposes capabilities for LLM assistants to explore available databases efficiently via MCP.

### 1. `list_tables`
- **Description**: Lightweight tool fetching all table names inside the target database safely.

### 2. `get_optimized_schema(table_name)`
- **Description**: Implements Ruthless Token Efficiency. Evaluates the given `table_name` to retrieve its precise layout minimizing token size.
- **Output Data**: Returns only column names, primitive types, PK signals, and mapped FK relations. Drops indexing info, defaults, and constraints.

### 3. `explain_query(query)`
- **Description**: Wraps a provided SQL string inside dialect-specific execution planners (`EXPLAIN`, `EXPLAIN QUERY PLAN`, or `SHOWPLAN_ALL`).
- **Safety**: Validates syntax and optimization boundaries before executing DML payloads in reality.
