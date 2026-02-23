---
name: Shuttles MCP Strategy
description: Strategic guidelines for utilizing the Shuttles MCP ecosystem (radar-ast, debug-probe, doc-scribe, cargo-db). Focuses on token conservation, local hardware usage, and precise technical execution.
---

# Shuttles MCP Strategy Guide

This skill directs the AI on how to interact with the Shuttles MCP ecosystem efficiently.

## Core Directives

### 1. The "Structural First" Rule
**Never** read a file completely if it is larger than 100 lines. Use structural tools first:
- **Markdown**: Use `doc-scribe.get_markdown_toc` to find relevant sections.
- **Python/Code**: Use `radar-ast.get_file_skeleton` to map out class and function definitions.
- **Directories**: Use `radar-ast.get_dir_tree` (max depth 2-3) to understand context.

## Specialized Server Skills
For detailed instructions on each server, refer to their dedicated skills:
- [Radar AST (Code Structure)](file:///home/nqhuy/nqhuy/shuttles/.agent/skills/mcp-radar-ast/SKILL.md)
- [Doc Scribe (Documentation)](file:///home/nqhuy/nqhuy/shuttles/.agent/skills/mcp-doc-scribe/SKILL.md)
- [Debug Probe (Diagnostics)](file:///home/nqhuy/nqhuy/shuttles/.agent/skills/mcp-debug-probe/SKILL.md)
- [Cargo DB (Data)](file:///home/nqhuy/nqhuy/shuttles/.agent/skills/mcp-cargo-db/SKILL.md)
- [View Port (Frontend)](file:///home/nqhuy/nqhuy/shuttles/.agent/skills/mcp-view-port/SKILL.md)

### 2. The "Token-Offload" Mandate
Whenever a task requires a summary, explanation, or docstring generation, **always** prefer the `*_local` tools. This uses the local RTX 3060 to save Cloud AI input/output tokens.
- `radar-ast.summarize_logic_local`
- `doc-scribe.summarize_doc_local`
- `doc-scribe.generate_inline_docs`
- `debug-probe.analyze_crash_local`

### 3. The "Patch-Only" Protocol
For large configuration or documentation files, **never** perform a full-file rewrite.
- Use `doc-scribe.patch_doc_section` to target specific headings.
- If a Code Patch tool exists (e.g., in radar-ast), use it for specific line replacement.

## Tool Selection Matrix

| Objective | Server | Primary Tool | Avoid |
| :--- | :--- | :--- | :--- |
| Exploring Project | `radar-ast` | `get_dir_tree` | `list_dir` (recursive) |
| Reading Large File | `radar-ast` | `get_file_skeleton` | `view_file` (full) |
| Updating Docs | `doc-scribe` | `patch_doc_section` | `write_to_file` (rewrite) |
| Running Tests | `debug-probe` | `run_and_capture` | Manual terminal commands |
| DB Research | `cargo-db` | `get_schema` / `find_join_path` | Manual SQL exploration |

## When NOT to use MCP Tools
- **Small Files**: If `ls` shows the file is small, `view_file` is faster.
- **Known Paths**: Don't use `get_dir_tree` if you already have the file link in your workspace or history.
- **Static Documentation**: If `docs/ARCHITECTURE.md` exists, read it before querying `radar-ast`.
