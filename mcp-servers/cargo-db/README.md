# `cargo-db` MCP Server

This is the `cargo-db` local Model Context Protocol server responsible for returning local Database metadata with "Ruthless Token Efficiency" standards.

## Requirements
- Python 3.11+
- PostgreSQL server running locally

## How to run
1. Set up the Python environment: `make setup`
2. Create your `.env` from `.env.example` and set `DATABASE_URL`.
3. Launch via MCP standard I/O: `make run`
