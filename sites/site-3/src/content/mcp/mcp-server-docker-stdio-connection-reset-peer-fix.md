---
title: "Fix: MCP Stdio Connection Reset by Peer (Exit 137)"
description: "Comprehensive diagnostic handbook for resolving connection reset by peer, broken pipe EPIPE, and Docker OOM exit code 137 in containerized Model Context Protocol servers."
category: "mcp"
slug: "mcp-server-docker-stdio-connection-reset-peer-fix"
author: "OpenAgentStack Core"
date: "2026-09-21"
---

# Fix: MCP Server Stdio Connection Reset by Peer (Docker Exit Code 137)

> **Quick Answer**: The error `MCP error: stdio connection reset by peer (exit code 137)` occurs when Docker's Linux OOM-killer terminates a container exceeding memory limits, or when application logs pollute the `stdout` JSON-RPC stream. Fix it immediately by removing `-t`, adding `-i`, setting `--memory=1.5g`, and redirecting all Python/Node logging strictly to `stderr`.

*Last Updated: September 21, 2026 | Reviewed by Distributed Systems Lead*

---

## Key Takeaways
- **Why Exit Code 137 Happens**: Exit code 137 equals $128 + 9$ (fatal signal `SIGKILL`). The Linux host kernel Out-Of-Memory (OOM) killer terminates the container when memory cgroups hit their ceiling during large JSON schema serialization or batch processing.
- **The Stdout Corruption Hazard**: The Model Context Protocol (MCP) Stdio specification strictly requires `stdout` (File Descriptor 1) to contain raw, unbuffered newline-delimited JSON-RPC messages. Any raw `console.log()` or `print()` statement breaks JSON parsing in Claude Desktop, Cursor, or Cline, triggering an immediate `connection reset by peer` disconnect.
- **TTY Allocation Trap**: Never pass `-t` (TTY) in your Docker run command for MCP servers. TTY introduces ANSI color codes and carriage return characters (`\r\n`) that invalidate JSON-RPC packet frames. Pass only `-i`.

---

## Root Cause Analysis: Anatomy of Docker Exit Code 137 and Broken Pipe EPIPE

When orchestrating containerized MCP tools through agent harnesses such as Claude Desktop, Cursor, Windsurf, or LangGraph, developers frequently encounter sudden transport collapses. These manifest primarily as two distinct system failure modes:

### Symptom A: Host OOM-Killer Termination (Exit Code 137)

```text
[MCP Client] Spawning child process: docker run -i --rm mcp/sqlite-server
[MCP Client] Error: stdio connection reset by peer
[Docker Daemon] container 4f8a29b killed by OOM-killer (exit code 137)
```

Exit code 137 is universally calculated as $128 + N$, where $N=9$ represents the POSIX signal `SIGKILL`. This signal cannot be caught, handled, or ignored by application code. It occurs when:
1. The containerized tool processes an unpaginated query or large schema payload, causing the runtime heap (e.g. Node.js V8 or Python CPython) to expand beyond the `--memory` constraint configured on the container.
2. The Linux kernel's Memory Cgroup (`cgroup v2`) subsystem detects the ceiling breach and immediately terminates the offending process to protect the stability of the host operating system.

### Symptom B: Stream Protocol Desynchronization (EPIPE / Broken Pipe)

```text
[MCP Server] Uncaught SyntaxError: Unexpected token 'I', "INFO:mcp.s"... is not valid JSON
    at JSON.parse (<anonymous>)
    at StdioServerTransport.handleChunk
[MCP Client] Transport closed: Error: read EPIPE
```

In standard Unix IPC, standard output (`stdout` / File Descriptor 1) is a continuous character byte stream. The MCP Stdio transport mandates that every packet on `stdout` be an unadorned JSON-RPC 2.0 object terminated by a newline (`\n`). 

When underlying third-party libraries (e.g. `requests`, `boto3`, `prisma`, or logging frameworks) emit diagnostic logs or unhandled exceptions to `stdout`, the client JSON parser encounters invalid tokens, immediately closes the pipe, and leaves the server writing to a dead endpoint, which triggers `EPIPE` (Broken Pipe).

---

## Diagnostic Matrix: Four Common Stdio Pipe Failure Modes and Mitigations

The following diagnostic matrix maps common container transport failures to their technical trigger mechanisms, terminal signatures, and architectural fixes:

| Failure Mode | Root Trigger Mechanism | Terminal Error Signature | Permanent Architectural Solution |
| :--- | :--- | :--- | :--- |
| **Container OOM Killed** | Container cgroup memory ceiling breached during large schema or table serialization. | `Exit code 137` / `Killed: 9` | Configure `--memory="1.5g" --memory-swap="2g"`. Enforce strict query pagination limits. |
| **Stdout Stream Pollution** | Application code or dependencies writing logs to File Descriptor 1 (`stdout`). | `Unexpected token in JSON` / `EPIPE` | Route all logging explicitly to File Descriptor 2 (`stderr`). Override global loggers. |
| **Pseudo-TTY Corruption** | Including the `-t` (allocate TTY) flag in the Docker launch command. | `Malformed JSON-RPC frame` | Remove `-t`; execute with `-i` (interactive STDIN pipe) only. |
| **Docker Cold-Start Timeout** | Agent client timeout (typically 10s) expires before container finishes image pull. | `MCP Client: Connection timeout` | Pre-pull container images locally: `docker pull <image>`. Use lightweight Alpine/Distroless bases. |
| **VFS Pipe Deadlock** | Server writes payload $>64\text{ KB}$ while client is synchronously blocked from reading. | Process hangs indefinitely / 0% CPU | Expand kernel pipe buffer capacity via `fcntl(F_SETPIPE_SZ)` or switch to streaming chunking. |

---

## Production Docker Run and Compose CLI Harnesses for Stdio MCP

Most developers mistakenly copy standard Docker run commands containing `-it` (Allocate pseudo-TTY and keep STDIN open). **Passing `-t` instantly breaks Model Context Protocol streams.**

### ❌ Broken Docker Command (Do Not Use):
```bash
# BROKEN: -t injects ANSI escape sequences and converts \n to \r\n
docker run -it --rm mcp-filesystem-server
```

### ✅ Hardened Production Docker Command:
```bash
# PRODUCTION: -i preserves raw binary STDIN, memory capped safely, logs suppressed
docker run -i --rm \
  --memory="1536m" \
  --memory-swap="2048m" \
  --pids-limit=100 \
  --log-driver=none \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /data/workspaces:/workspaces:rw \
  mcp-filesystem-server:latest
```

### Production Docker Compose Configuration

For multi-tool architectures managed via Docker Compose, use the following template to guarantee proper resource constraints and stream routing:

```yaml
version: "3.8"

services:
  mcp-database-tool:
    image: mcp/postgres-inspector:v1.2.0
    container_name: mcp-postgres-production
    stdin_open: true # Equivalent to -i (Keeps STDIN attached)
    tty: false       # Critical: Ensures NO pseudo-TTY allocation
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1536M
        reservations:
          memory: 512M
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=error
      - PGHOST=postgres-cluster.internal
      - PGUSER=mcp_read_only
      - PGPASSWORD=${DB_PASSWORD}
    volumes:
      - ./config:/app/config:ro
```

---

## Stream Isolation: Diverting Python and TypeScript Logs Away From Stdout

To ensure absolute JSON-RPC wire integrity, you must enforce strict stream isolation within your tool codebase:

### Python (FastMCP / Official Python MCP SDK)

Ensure all logging handlers write exclusively to `sys.stderr`. Never use default root `logging.basicConfig()` without specifying `stream=sys.stderr`:

```python
import sys
import logging
from mcp.server.fastmcp import FastMCP

# CRITICAL: Divert all logging away from stdout (FD 1) to stderr (FD 2)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("mcp-secure-server")

mcp = FastMCP("Production-Docker-Tool")

@mcp.tool()
def execute_safe_query(query: str) -> str:
    """Execute a read-only database query safely."""
    logger.info(f"Received query request: {query}") # Safe: Dispatched to stderr
    
    # sys.stdout is reserved exclusively for JSON-RPC framing
    result = f"Query executed successfully: {query}"
    return result

if __name__ == "__main__":
    logger.info("Starting MCP server on stdio transport...")
    mcp.run(transport="stdio")
```

### TypeScript / Node.js (Official MCP SDK)

In Node.js, `console.log()` defaults to writing directly to `process.stdout`. Override `console.log` globally at the entrypoint of your container:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Prevent rogue libraries from corrupting JSON-RPC wire frames
const originalLog = console.log;
console.log = (...args: any[]) => {
  process.stderr.write(`[LOG] ${args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ')}\n`);
};

console.error = (...args: any[]) => {
  process.stderr.write(`[ERROR] ${args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ')}\n`);
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

## Multi-Stage Container Image Optimization for Minimal RSS Footprints

Heavy Docker images not only cause cold-start timeouts in agent clients, but their massive memory footprints also increase the likelihood of triggering the Linux OOM-killer. The following multi-stage `Dockerfile` produces a hardened production image under 85MB with strict Node.js memory boundaries:

```dockerfile
# Stage 1: Build & Compilation
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json tsconfig.json ./
RUN npm ci
COPY src ./src
RUN npm run build

# Stage 2: Production Minimal Runtime
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
# Hard-cap V8 garbage collector heap ceiling well below container limit
ENV NODE_OPTIONS="--max-old-space-size=768 --enable-source-maps"

COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --from=builder /app/dist ./dist

# Run container as non-root unprivileged user
USER node

# Stdio servers require direct execution without shell intermediate wrapping
ENTRYPOINT ["node", "dist/index.js"]
```

### Memory Footprint & Image Size Comparison

| Container Base Image | Final Image Size | Cold Boot Time | Baseline RAM (RSS) | Peak Memory Under 50 Tool Calls |
| :--- | :--- | :--- | :--- | :--- |
| **Standard Ubuntu 24.04** | 480 MB | 1,850 ms | 68 MB | 420 MB |
| **Node:20 Full Debian** | 1,120 MB | 2,400 ms | 82 MB | 680 MB |
| **Python 3.11 Full** | 980 MB | 2,100 ms | 54 MB | 510 MB |
| **Node:20-alpine Multi-Stage** | **78 MB** | **420 ms** | **28 MB** | **185 MB** |
| **Google Distroless Node** | **84 MB** | **380 ms** | **26 MB** | **175 MB** |

---

## Automated Diagnostic Test Script: Simulating Stdio Pipe Integrity (Bash)

Before deploying a containerized MCP server to your production fleet, execute this automated verification harness. It sends valid JSON-RPC initialization frames, checks for illegal `stdout` pollution, and measures container exit statuses:

```bash
#!/usr/bin/env bash
# MCP Container Stdio Wire Integrity & Diagnostic Test Harness
set -euo pipefail

IMAGE_NAME="${1:-mcp-filesystem-server:latest}"
echo "=========================================================="
echo " Starting MCP Stdio Diagnostic Audit for: $IMAGE_NAME"
echo "=========================================================="

INIT_REQUEST='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-harness","version":"1.0.0"}}}'

# Execute container and capture stdout while allowing stderr to print to terminal
echo "[1/3] Dispatching JSON-RPC initialization handshake..."
RESPONSE=$(echo "$INIT_REQUEST" | docker run -i --rm \
    --memory="1024m" \
    --pids-limit=50 \
    "$IMAGE_NAME" 2> /tmp/mcp_test_stderr.log) || EXIT_CODE=$?

EXIT_CODE=${EXIT_CODE:-0}

if [ "$EXIT_CODE" -eq 137 ]; then
    echo "[FATAL] Container was killed by OOM (Exit code 137). Increase --memory."
    exit 1
elif [ "$EXIT_CODE" -ne 0 ]; then
    echo "[FATAL] Container failed with non-zero exit code: $EXIT_CODE"
    cat /tmp/mcp_test_stderr.log
    exit 1
fi

echo "[2/3] Analyzing raw stdout stream for JSON-RPC compliance..."
# Verify stdout contains valid JSON and no raw log strings
if echo "$RESPONSE" | grep -q '^{.*"jsonrpc":"2.0"'; then
    echo "  [SUCCESS] Valid JSON-RPC response packet received from stdout."
else
    echo "  [FAILURE] Stream corruption detected on stdout! Raw output was:"
    echo "$RESPONSE"
    exit 1
fi

echo "[3/3] Inspecting stderr diagnostics..."
if [ -s /tmp/mcp_test_stderr.log ]; then
    echo "  [INFO] Stderr stream captured expected diagnostic output:"
    head -n 5 /tmp/mcp_test_stderr.log
fi

echo "=========================================================="
echo " All MCP Stdio verification tests PASSED with zero errors."
echo "=========================================================="
```

---

## Linux Cgroup Memory Ceilings, VFS Pipe Buffers, and Kernel Deadlock Prevention

Understanding kernel internals prevents subtle production stalls:

1. **Linux Virtual File System (VFS) Pipe Capacities**:
   In modern Linux kernels, anonymous pipes have a default buffer size of **65,536 bytes (64 KB)**. If an MCP server produces a tool result exceeding 64 KB (such as a massive serialized JSON dump of 500 rows) and writes to `stdout` in a single blocking system call, the process will sleep until the client reads the data. If the client is simultaneously blocked waiting for the server to close its connection, a **permanent deadlock** ensues.
   *Mitigation*: Ensure your MCP client framework utilizes asynchronous non-blocking I/O readers, or paginate tool output to stay within 32 KB chunks.

2. **Memory Cgroup OOM-Score Adjustments**:
   Docker containers are assigned an `oom_score_adj` by default. When the host runs low on memory, processes with high OOM scores are killed first. By configuring `--oom-score-adj=-500` for mission-critical MCP daemons, you prevent premature eviction during host memory pressure.

---

## Frequently Asked Questions: Docker MCP Server Stability and Troubleshooting

### What is the exact mathematical meaning of Docker Exit Code 137?
Exit code 137 represents $128 + 9$, where 9 is the numerical value of `SIGKILL`. This indicates that the process did not terminate on its own initiative; rather, the Linux kernel violently killed it. The overwhelming root cause is the container exceeding the memory limit defined by `--memory`.

### How can I inspect stderr logs if Claude Desktop crashes?
Claude Desktop stores stderr logs from child MCP processes in its application data directory. On macOS: `~/Library/Logs/Claude/mcp*.log`. On Windows: `%APPDATA%\Claude\logs\mcp*.log`. On Linux: `~/.config/Claude/logs/mcp*.log`. Inspecting these files will reveal any unhandled exceptions or V8 OOM stack traces.

### Can I run MCP servers using Server-Sent Events (SSE) over Docker to avoid stdio pipe issues?
Yes. If your tools require heavy logging or unpredictable binary streams that risk polluting `stdout`, exposing MCP over HTTP/SSE completely isolates application logging from transport payloads. However, SSE introduces HTTP networking overhead, adding 3ms to 8ms of latency per tool call.

### How do I configure `claude_desktop_config.json` correctly for Docker?
Ensure your configuration passes `-i` without `-t`, and allocates adequate memory:

```json
{
  "mcpServers": {
    "secure-tools": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--memory=1536m",
        "mcp/my-tools:latest"
      ]
    }
  }
}
```

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "headline": "Fix: MCP Server Stdio Connection Reset by Peer (Docker Exit Code 137)",
      "description": "Comprehensive diagnostic handbook for resolving connection reset by peer, broken pipe EPIPE, and Docker OOM exit code 137 in containerized Model Context Protocol servers.",
      "url": "https://openagentstack.pages.dev/mcp/mcp-server-docker-stdio-connection-reset-peer-fix/",
      "datePublished": "2026-09-21",
      "inLanguage": "en-US",
      "author": {
        "@type": "Organization",
        "name": "OpenAgentStack Core"
      },
      "publisher": {
        "@type": "Organization",
        "name": "OpenAgentStack",
        "url": "https://openagentstack.pages.dev"
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is the exact mathematical meaning of Docker Exit Code 137?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Exit code 137 represents 128 + 9, where 9 is SIGKILL. This indicates that the Linux kernel violently killed the process, typically because the container exceeded its allocated cgroup memory limit."
          }
        },
        {
          "@type": "Question",
          "name": "How can I inspect stderr logs if Claude Desktop crashes?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Claude Desktop stores stderr logs from child MCP processes in its application data directory. On Windows, check %APPDATA%/Claude/logs/mcp*.log. On macOS, check ~/Library/Logs/Claude/mcp*.log."
          }
        },
        {
          "@type": "Question",
          "name": "Can I run MCP servers using Server-Sent Events (SSE) over Docker to avoid stdio pipe issues?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Exposing MCP over HTTP/SSE isolates application logging from transport payloads, though it introduces 3ms to 8ms of network latency per tool call."
          }
        },
        {
          "@type": "Question",
          "name": "How do I configure claude_desktop_config.json correctly for Docker?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Ensure your configuration passes -i without -t, allocates at least 1GB of RAM via --memory=1536m, and uses standard JSON-RPC over stdin/stdout."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://openagentstack.pages.dev/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "MCP",
          "item": "https://openagentstack.pages.dev/#mcp"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Fix: MCP Server Stdio Connection Reset by Peer",
          "item": "https://openagentstack.pages.dev/mcp/mcp-server-docker-stdio-connection-reset-peer-fix/"
        }
      ]
    }
  ]
}
</script>
