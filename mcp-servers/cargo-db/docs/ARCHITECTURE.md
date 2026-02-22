# Architecture

## Server Architecture
`cargo-db` is a specialized Model Context Protocol (MCP) server designed for the `shuttles` monorepo. It operates locally and connects securely to databases to analyze schema and query execution plans without offloading full databases to the cloud.

### Core Patterns
- **Database Agnosticism**: Implemented via SQLAlchemy, abstracting dialect differences between PostgreSQL, MySQL, SQLite, and SQL Server.
- **Token-Optimized Payload**: By design, the server adheres to the "Ruthless Token Efficiency" architecture pattern. It aggressively strips down responses (e.g., removing unneeded constraints or debug lines) to generate minimal JSON outputs suitable for Large Language Models.
- **Stateless Execution**: Connects per tool call based on `DATABASE_URL`, or initializes lazy engines. Errors are caught gracefully, and outputs are formatted for MCP standard `TextContent`.
