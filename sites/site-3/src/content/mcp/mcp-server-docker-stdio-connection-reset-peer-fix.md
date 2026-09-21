---
title: "Fix: MCP Server Stdio Connection Reset by Peer (Docker Exit Code 137)"
description: "Comprehensive diagnostic handbook for resolving 'connection reset by peer', broken pipe EPIPE, and Docker OOM exit code 137 in containerized Model Context Protocol servers."
category: "mcp"
slug: "mcp-server-docker-stdio-connection-reset-peer-fix"
author: "OpenAgentStack Core"
date: "2026-09-21"
---

> **Quick Answer**: The error `MCP error: stdio connection reset by peer (process exited with code 137)` occurs when Docker's Linux kernel Out-Of-Memory (OOM) killer abruptly terminates a containerized Model Context Protocol (MCP) server that exceeds its memory limit, or when Node.js/Python writes logging statements directly to `stdout` instead of `stderr`, corrupting the JSON-RPC pipe. To resolve it immediately: add `-i` (interactive mode) to your Docker CLI harness, redirect non-RPC application logs strictly to `stderr`, and increase the container memory limit to at least `1GB` (`--memory="1g"`).

*Last Updated: September 21, 2026 | Reviewed by Distributed Systems Lead*

---

## Key Takeaways
- **Why Exit Code 137 Happens**: Exit code 137 equals $128 + 9$ (fatal signal `SIGKILL`). The Linux host OOM-killer violently terminates the process when Docker memory cgroups hit the container ceiling during large JSON schema serialization.
- **The Stdout Corruption Hazard**: The MCP Stdio specification strictly requires `stdout` to contain raw, unbuffered JSON-RPC messages. Any raw `console.log()` or `print()` statement breaks JSON parsing in Claude Desktop, Cursor, or Cline, causing an immediate client-side `connection reset by peer` disconnect.
- **Tty Allocation Trap**: Never pass `-t` (TTY) in your Docker run command for MCP servers. TTY introduces ANSI color codes and carriage return characters (`\r\n`) that invalidate JSON-RPC packet frames. Pass only `-i`.

---

## 1. Diagnostic Error Breakdown

When orchestrating MCP servers via Claude Desktop, Cursor, Windsurf, or custom Python agent harnesses, you will encounter two primary manifestations of this failure:

### Symptom A: Host OOM-Killer Termination (Exit Code 137)
```text
[MCP Client] Spawning child process: docker run -i --rm mcp/sqlite-server
[MCP Client] Error: stdio connection reset by peer
[Docker Daemon] container 4f8a29b killed by OOM-killer (exit code 137)
```

### Symptom B: Stream Protocol Desynchronization (EPIPE / Broken Pipe)
```text
[MCP Server] Uncaught SyntaxError: Unexpected token 'I', "INFO:mcp.s"... is not valid JSON
    at JSON.parse (<anonymous>)
    at StdioServerTransport.handleChunk
[MCP Client] Transport closed: Error: read EPIPE
```

---

## 2. Root Cause Analysis: The 3 Core Triggers

| Failure Mode | Trigger Mechanism | Terminal Indicator | Permanent Architectural Solution |
| :--- | :--- | :--- | :--- |
| **Container OOM Killed** | Container memory limit exceeded during large schema serialization. | `Exit code 137` / `Killed: 9` | Set `--memory="1.5g" --memory-swap="2g"`. |
| **Stdout Pollution** | Libraries emitting logs/debug text to File Descriptor 1 (`stdout`). | `Unexpected token 'D' in JSON` | Re-route logging to File Descriptor 2 (`stderr`). |
| **Pseudo-TTY Encoding** | Running `docker run -it` instead of `docker run -i`. | `Malformed JSON-RPC frame` | Strip `-t` flag; use clean raw stdin pipe `-i`. |
| **Docker Engine Timeout** | Cold image startup taking >10 seconds during container creation. | `MCP Client: Connection timeout` | Pre-pull images: `docker pull <image>`. |

---

## 3. The Correct `docker run` Command for MCP Stdio

Most developers mistakenly copy standard Docker run commands containing `-t` (Allocate pseudo-TTY). **This instantly corrupts Model Context Protocol streams.**

### ❌ Incorrect Docker Command:
```bash
# BROKEN: -t corrupts JSON-RPC with carriage returns and ANSI escapes
docker run -it --rm mcp-filesystem-server
```

### ✅ Production-Hardened Docker Command:
```bash
# CORRECT: -i keeps STDIN open, zero TTY allocation, memory capped safely
docker run -i --rm \
  --memory="1024m" \
  --memory-swap="2048m" \
  --pids-limit=100 \
  --log-driver=none \
  -v /local/data:/data:ro \
  mcp-filesystem-server:latest
```

---

## 4. Hardening Python & TypeScript MCP Code Against Broken Pipes

### Python (FastMCP / Official SDK)
Ensure all logging handlers write exclusively to `sys.stderr`. Never use default root `logging.basicConfig()` without specifying `stream=sys.stderr`:

```python
import sys
import logging
from mcp.server.fastmcp import FastMCP

# CRITICAL: Divert all logging away from stdout (FD 1) to stderr (FD 2)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("mcp-server")

mcp = FastMCP("Reliable-Docker-Tool")

@mcp.tool()
def execute_safe_query(query: str) -> str:
    logger.info(f"Executing query: {query}") # Safe: logged to stderr
    # sys.stdout is reserved exclusively for JSON-RPC
    return f"Result for {query}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### TypeScript / Node.js
Override `console.log` or route standard application output to `process.stderr`:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Prevent rogue console.log from polluting JSON-RPC stdout channel
console.log = (...args: any[]) => {
    process.stderr.write(`[LOG] ${args.join(" ")}\n`);
};

const server = new Server(
    { name: "production-node-mcp", version: "1.0.0" },
    { capabilities: { tools: {} } }
);

const transport = new StdioServerTransport();
await server.connect(transport);
process.stderr.write("⚡ MCP Server successfully connected via Stdio\n");
```

---

## 5. Dockerfile Best Practices for Low-Memory Footprints

To prevent the kernel OOM killer (exit code 137) when running multiple MCP tools side-by-side, build multi-stage slim container images:

```dockerfile
# Build Stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production Runtime Stage (Under 90MB image footprint)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Force Node.js memory ceiling below container limit
ENV NODE_OPTIONS="--max-old-space-size=512"

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev

USER node
ENTRYPOINT ["node", "dist/index.js"]
```

---

## 6. Benchmarking Transport Performance

Notice that Stdio transport overhead is negligible compared to network sockets. Read our complete [Model Context Protocol Stdio vs SSE Latency Benchmark](/mcp/mcp-server-stdio-vs-sse-latency-benchmark/) for empirical microsecond measurements across agent tool-calling loops.

---

## 7. Frequently Asked Questions (FAQ)

### What does Exit Code 137 specifically mean in Docker?
Exit code 137 occurs when the containerized process was sent signal 9 (`SIGKILL`) by the Linux host operating system. The most frequent cause is the kernel OOM (Out Of Memory) killer terminating the container when RAM usage crosses the allocated cgroup boundary.

### Can I run MCP over Docker using HTTP SSE instead to avoid stdio pipe breaks?
Yes. If your tools suffer from frequent local pipe crashes, switching to SSE transport wraps messages in standard HTTP POST / Server-Sent Events, isolating application logs from the transport payload. However, SSE adds 4–10ms of network latency per tool call.

### How do I configure Claude Desktop config to prevent this?
Inside `claude_desktop_config.json`, always pass `-i` and avoid `-t`:
```json
{
  "mcpServers": {
    "my-tool": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--memory=1g", "my-mcp-image"]
    }
  }
}
```
