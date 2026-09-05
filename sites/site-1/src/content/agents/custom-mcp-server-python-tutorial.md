---
title: "Custom MCP Server Python Tutorial: Build Production Model Context Protocol Tools (2026)"
description: "Step-by-step tutorial to create, test, and deploy a custom Model Context Protocol (MCP) server in Python using FastMCP, stdio transport, and SQLite tool state."
datePublished: "2026-08-18"
dateModified: "2026-09-04"
author: "Engineering Team"
tags: ["mcp", "python", "model-context-protocol", "claude-code", "agentic-ai"]
coverImage: "/images/covers/custom-mcp-server-python-tutorial.webp"
canonical: "https://localagentstack.com/agents/custom-mcp-server-python-tutorial/"
---

# Custom MCP Server Python Tutorial: FastMCP & SQLite Architecture

> **Quick Answer**: To build a custom MCP server in Python, install the official `mcp` SDK via `pip install mcp`, initialize a `FastMCP("ServerName")` instance, define tools using the `@mcp.tool()` decorator with strict type annotations, and run the server over stdio transport via `mcp.run()`. This exposes your custom Python functions directly to Claude Code, Cursor, and OpenAI desktop clients.

*Last Updated: September 4, 2026 | Reviewed by Senior Systems Architect*

## Key Takeaways
- **Standardized Protocol**: The Model Context Protocol (MCP) replaces fragmented tool-calling plugins with a single JSON-RPC 2.0 interface across LLM hosts.
- **FastMCP Framework**: FastMCP provides automated Pydantic schema generation, OpenAPI documentation, and asynchronous tool execution with minimal boilerplate.
- **Stateful Tool Integration**: Persisting local agent task state via SQLite ensures long-running agents survive context window resets.
- **Local Model Serving**: Pair your MCP servers with local reasoning runtimes using our [DeepSeek R1 Ollama Setup](/models/deepseek-r1-local-setup-ollama/) or scale throughput with [vLLM Serving](/inference/ollama-vs-vllm-benchmark/).

---

## 1. FastMCP vs Traditional REST Tool Calling Matrix

| Feature | FastMCP (Python) | Raw JSON-RPC 2.0 | Custom REST API Server |
|---|---|---|---|
| **Lines of Boilerplate** | ~15 lines | ~120 lines | ~85 lines |
| **Transport Types** | Stdio & SSE (Server-Sent Events) | Manual Socket / Stdio | HTTP/HTTPS Only |
| **Schema Generation** | Automatic from Python Typehints | Manual JSON Schema dict | Manual Pydantic / OpenAPI |
| **Desktop Client Support** | 1-Click (`claude_desktop_config.json`) | Manual JSON Config | Requires reverse proxy / ngrok |
| **Latency** | < 4ms (Local IPC Stdio) | < 4ms (Local IPC Stdio) | 25–60ms (TCP handshake) |

![Custom MCP Server Python Architecture Workflow Diagram](/images/benchmarks/custom-mcp-server-python-tutorial.webp)

---

## 2. Production FastMCP Server Code Example
Below is a complete, executable custom MCP server that provides local database querying and file auditing tools:

```python
import sqlite3
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("DatabaseInspector", dependencies=["sqlite3"])

DB_PATH = "analytics.db"

@mcp.tool()
def execute_readonly_query(sql_query: str) -> List[Dict[str, Any]]:
    """Execute a read-only SELECT query against the local SQLite database."""
    if not sql_query.strip().upper().startswith("SELECT"):
        raise ValueError("Only read-only SELECT statements are permitted.")
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

if __name__ == "__main__":
    mcp.run()
```

Configure your local client by editing `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "db-inspector": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

---

## 3. Protocol Architecture & Transports
According to the [Official Model Context Protocol Specification](https://modelcontextprotocol.io/) and the [Model Context Protocol GitHub Repository](https://github.com/modelcontextprotocol/python-sdk), MCP relies on three core primitives:
1. **Tools**: Executable functions that perform external actions (APIs, filesystem, terminal).
2. **Resources**: Read-only passive context files (logs, schemas, documents).
3. **Prompts**: Pre-engineered system prompt templates surfaced to the user.

For hosting your agent cluster on dedicated hardware, consult our [VRAM Requirements Calculator](/hardware/vram-requirements-calculator-70b/) and our [Mac Studio M4 Max Review](/hardware/mac-studio-m4-max-llm-benchmarks/).

---

## 4. Security & Isolation Best Practices
1. **Sandboxed Filesystem Access**: Restrict read/write operations to explicit workspace paths using Python's `pathlib.Path.resolve()`.
2. **SQL Parameterization**: Never format raw user strings into SQL statements; utilize parameterized bindings to prevent injection attacks.
3. **Environment Secrets**: Reference credentials from local environment variables rather than hardcoding tokens, adhering to the [Python Software Foundation Security Guidelines](https://www.python.org/dev/peps/pep-0578/).

---

## 5. Frequently Asked Questions (FAQ)

### What is the difference between stdio and SSE transports in MCP?
Stdio runs locally over standard input/output streams, making it ideal for desktop agents (Claude Code, Cursor). SSE (Server-Sent Events) runs over HTTP, allowing you to host MCP servers on remote cloud servers accessible across networks.

### Can I connect multiple MCP servers to the same client?
Yes. Desktop clients allow registering dozens of independent MCP servers simultaneously. The host client routes tool calls to the appropriate server based on tool namespace.

### Which Python versions are supported by the MCP SDK?
The official `mcp` SDK requires Python 3.10 or newer to support modern union types and structural pattern matching.
