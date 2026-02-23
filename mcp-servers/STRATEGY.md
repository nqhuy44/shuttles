# MCP Ecosystem Strategy & Tool Review

This document provides definitive guidelines for AI agents and developers on how to use the MCP tools in the `shuttles` monorepo.

## 1. `radar-ast` (Structural Analysis)

| Tool | When to Use | When NOT to Use |
| :--- | :--- | :--- |
| `get_dir_tree` | To understand the project's folder layout and find specific modules. | When you already know the exact file path. It consumes tokens unnecessarily for large trees. |
| `get_file_skeleton` | **Always** your first step for a new file. Use it to see class/method signatures and determine relevance. | For small files (< 50 lines). Just read the whole file instead. |
| `read_specific_lines` | After identifying relevant logic via the skeleton. Minimizes input context. | When you need to understand the full context or cross-method references in a file. |
| `summarize_logic_local` | For files with high complexity (e.g., > 300 lines of implementation) to get a gist. | For utility files or simple getters/setters. |

---

## 2. `doc-scribe` (Documentation Excellence)

| Tool | When to Use | When NOT to Use |
| :--- | :--- | :--- |
| `get_markdown_toc` | For large `.md` files to navigate to a specific section. | For quick READMEs. |
| `patch_doc_section` | **Mandatory** for updating specific sections. Prevents "full-file rewrite" hallucinations and saves output tokens. | When restructuring the entire document or merging multiple sections. |
| `summarize_doc_local` | When you need to extract specific info (naming conventions, deploy steps) from massive docs. | When the doc is short enough to fit in the current context comfortably. |
| `generate_inline_docs` | When adding Google-style docstrings to Python functions/classes to maintain repo standards. | For internal helpers or temporary scripts where overhead isn't justified. |

---

## 3. `debug-probe` (Diagnostics & Runtime)

| Tool | When to Use | When NOT to Use |
| :--- | :--- | :--- |
| `run_and_capture` | To verify if changes fixed a build error or to run targeted unit tests. | For long-running background processes or interactive CLI tools. |
| `tail_filtered_logs` | To monitor live logs for specific patterns (e.g., "SQL", "ERROR"). | For reading historic logs; use standard file reading if log rotation hasn't occurred. |
| `analyze_crash_local` | When a task fails with a complex stack trace and you need an intelligent starting point. | For simple syntax errors or obvious configuration issues. |

---

## 4. `cargo-db` (Data Introspection)

| Tool | When to Use | When NOT to Use |
| :--- | :--- | :--- |
| `get_tables` | To get an overview of the current database state. | If you already have the schema/ERD in `docs/`. |
| `get_schema` | To see table columns, types, and constraints. | Before checking `docs/DATABASE.md` (which is often more descriptive). |
| `explain_query` | Before committing new complex SQL queries to ensure performance safety. | For simple `SELECT *` or ID-based lookups. |
| `find_join_path` | When joining disparate tables to find the most efficient FK relationship. | When the relationship is documented in the code's ORM model. |

---

## General Efficiency Rules

1.  **Look Before You Leap**: Always use TOC/Skeleton tools before Reading.
2.  **Edit Only What You Must**: Use `patch` tools whenever possible.
3.  **Localize Heavy Lifting**: Offload summarization and explanation to Ollama (`_local` suffix).
4.  **No Double Dipping**: If the info is in `docs/`, use standard file tools. Use MCP tools for live/dynamic introspection.
