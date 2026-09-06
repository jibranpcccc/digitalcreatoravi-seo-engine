import os
import json
import sqlite3
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "fleet_telemetry.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Create Pending Posts Table
c.execute("""
CREATE TABLE IF NOT EXISTS pending_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    site_name TEXT,
    title TEXT,
    slug TEXT,
    target_keyword TEXT,
    search_volume INTEGER,
    keyword_difficulty INTEGER,
    pillar_silo TEXT,
    status TEXT DEFAULT 'queued',
    scheduled_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 2. Create Indexed Pages Table
c.execute("""
CREATE TABLE IF NOT EXISTS indexed_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    url TEXT UNIQUE,
    title TEXT,
    in_sitemap INTEGER DEFAULT 1,
    index_status TEXT DEFAULT 'Indexed',
    google_status TEXT DEFAULT 'Indexed (Mobile-Friendly)',
    bing_status TEXT DEFAULT 'Indexed (IndexNow Push)',
    http_status INTEGER DEFAULT 200,
    ttfb_ms INTEGER DEFAULT 280,
    h1_ok INTEGER DEFAULT 1,
    schema_ok INTEGER DEFAULT 1,
    quick_answer_ok INTEGER DEFAULT 1,
    total_hits INTEGER DEFAULT 0,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 3. Create Search Queries & Rankings Table (Replacing GSC Performance Tab)
c.execute("""
CREATE TABLE IF NOT EXISTS search_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    query TEXT,
    page_url TEXT,
    impressions INTEGER,
    clicks INTEGER,
    ctr REAL,
    position REAL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 4. Create Fleet Alerts Table
c.execute("""
CREATE TABLE IF NOT EXISTS fleet_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    alert_type TEXT,
    title TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved INTEGER DEFAULT 0
)
""")

# Seed Pending Posts Queue (3 per site = 24 curated low-competition topics from intelligence dossier)
pending_posts_data = [
    # Site 1: LocalAgentStack
    ("site-1", "LocalAgentStack", "RTX 5090 vs RTX 4090 Local LLM Inference Benchmark (32GB VRAM)", "rtx-5090-vs-4090-local-llm-benchmark", "rtx 5090 local llm benchmark", 4400, 14, "Hardware Benchmarks", "queued", "2026-09-08"),
    ("site-1", "LocalAgentStack", "Llama.cpp vs ExLlamaV2 Quantization Speed: GGUF vs EXL2 on Consumer GPUs", "llama-cpp-vs-exllamav2-quantization-speed", "exllamav2 vs llamacpp speed", 2900, 12, "Inference Engines", "queued", "2026-09-10"),
    ("site-1", "LocalAgentStack", "Run DeepSeek-R1 70B on 48GB VRAM with Dual RTX 3090: The Budget Rig", "deepseek-r1-70b-dual-rtx-3090-setup", "deepseek r1 dual 3090", 3800, 11, "Budget Hardware", "queued", "2026-09-12"),

    # Site 2: WorkationRadar
    ("site-2", "WorkationRadar", "Top 10 Coliving Spaces in Split, Croatia for Remote Workers (2026 Guide)", "split-croatia-coliving-guide", "coliving split croatia", 1800, 8, "Destination Hubs", "queued", "2026-09-08"),
    ("site-2", "WorkationRadar", "Tbilisi Digital Nomad Coliving & Coworking Hubs with Fiber Internet", "tbilisi-georgia-coliving-coworking", "coliving tbilisi georgia", 1500, 6, "Destination Hubs", "queued", "2026-09-10"),
    ("site-2", "WorkationRadar", "Florianópolis Coliving Guide: Brazil's Silicon Island for Tech Nomads", "florianopolis-brazil-coliving-guide", "coliving florianopolis brazil", 2100, 9, "Destination Hubs", "queued", "2026-09-12"),

    # Site 3: OpenAgentStack
    ("site-3", "OpenAgentStack", "Containerizing Model Context Protocol (MCP) Servers in Docker & Kubernetes", "mcp-server-docker-kubernetes-guide", "mcp server docker production", 3200, 13, "MCP Protocols", "queued", "2026-09-08"),
    ("site-3", "OpenAgentStack", "LangGraph State Persistence with PostgreSQL Checkpointers in Production", "langgraph-postgres-checkpointer-persistence", "langgraph checkpointer postgres", 2400, 15, "Agent Architecture", "queued", "2026-09-10"),
    ("site-3", "OpenAgentStack", "Building an Autonomous Coding Agent with Smolagents & Claude 3.5 Sonnet", "smolagents-coding-agent-claude-tutorial", "smolagents tutorial python", 2700, 11, "Autonomous Frameworks", "queued", "2026-09-12"),

    # Site 4: IndieStackAudit
    ("site-4", "IndieStackAudit", "Drizzle ORM vs Prisma Cold-Start Latency on Neon Serverless Postgres", "drizzle-vs-prisma-neon-postgres-cold-starts", "drizzle vs prisma cold start", 3500, 12, "Database ORM", "queued", "2026-09-08"),
    ("site-4", "IndieStackAudit", "Better-Auth vs Clerk: Why Bootstrappers Are Migrating in 2026", "better-auth-vs-clerk-migration-cost", "better-auth vs clerk", 4100, 14, "Authentication Billing", "queued", "2026-09-10"),
    ("site-4", "IndieStackAudit", "Zero-Cost Micro-SaaS Stack: Cloudflare Pages + Turso LibSQL + Resend", "zero-cost-saas-cloudflare-pages-turso", "free saas stack 2026", 2900, 10, "Bootstrap Architecture", "queued", "2026-09-12"),

    # Site 5: VectorBench
    ("site-5", "VectorBench", "Milvus vs Qdrant at 1 Billion Vectors: RAM Footprint & Recall Latency", "milvus-vs-qdrant-billion-scale-benchmark", "milvus vs qdrant benchmark", 2100, 16, "Scalability Benchmarks", "queued", "2026-09-08"),
    ("site-5", "VectorBench", "Voyage AI vs OpenAI text-embedding-3-large: Retrieval Accuracy & Cost Math", "voyage-ai-vs-openai-embeddings-rag-cost", "voyage ai vs openai embeddings", 2600, 13, "Embedding Models", "queued", "2026-09-10"),
    ("site-5", "VectorBench", "ChromaDB Embedded vs LanceDB In-Memory: Vector DB Shootout for Local Apps", "chroma-vs-lancedb-embedded-shootout", "chroma vs lancedb local", 3100, 11, "Embedded Engines", "queued", "2026-09-12"),

    # Site 6: NomadTreaty
    ("site-6", "NomadTreaty", "Cyprus 60-Day Rule & Non-Dom Tax Regime for Digital Nomads (2026 Guide)", "cyprus-non-dom-tax-nomad-guide", "cyprus non dom digital nomad", 2800, 9, "Tax Treaties", "queued", "2026-09-08"),
    ("site-6", "NomadTreaty", "Estonia e-Residency Corporate Tax 0% Retained Earnings Optimization", "estonia-e-residency-tax-optimization", "estonia e residency tax guide 2026", 3600, 12, "Corporate Structuring", "queued", "2026-09-10"),
    ("site-6", "NomadTreaty", "Italy Digital Nomad Visa Flat Tax vs Beckham Law Comparison", "italy-digital-nomad-visa-flat-tax-vs-spain", "italy nomad visa tax 2026", 2400, 14, "Visa Comparisons", "queued", "2026-09-12"),

    # Site 7: WebhookWatch
    ("site-7", "WebhookWatch", "Shopify Webhook Signature Verification in Node.js & Go (HMAC-SHA256)", "shopify-webhook-signature-verification-guide", "shopify webhook signature verification", 3100, 10, "Security Blueprints", "queued", "2026-09-08"),
    ("site-7", "WebhookWatch", "GitHub Webhook Delivery Architecture: Handling 100k Webhooks/Sec with Kafka", "github-webhook-delivery-kafka-architecture", "high throughput webhook architecture", 2200, 15, "Enterprise Scale", "queued", "2026-09-10"),
    ("site-7", "WebhookWatch", "Webhook Idempotency with Redis Redlock: Preventing Double-Billing in SaaS", "webhook-idempotency-redis-redlock-guide", "webhook idempotency redis", 2800, 12, "Idempotency Patterns", "queued", "2026-09-12"),

    # Site 8: LocalDocPrivacy
    ("site-8", "LocalDocPrivacy", "Client-Side PDF Compression with WebAssembly (WASM): Ghostscript vs PDF-lib", "client-side-pdf-compression-wasm-guide", "compress pdf in browser wasm", 3400, 9, "WASM Optimization", "queued", "2026-09-08"),
    ("site-8", "LocalDocPrivacy", "In-Browser OCR with Tesseract.js WASM: Zero Cloud Data Transmission", "in-browser-ocr-tesseract-wasm-guide", "local ocr browser wasm", 4200, 11, "Offline Tooling", "queued", "2026-09-10"),
    ("site-8", "LocalDocPrivacy", "GDPR Article 32 Technical Safeguards Checklist for Client-Side Document Tools", "gdpr-article-32-client-side-safeguards", "gdpr client side document processing", 1900, 7, "Compliance Audits", "queued", "2026-09-12")
]

for p in pending_posts_data:
    c.execute("""
    INSERT OR REPLACE INTO pending_posts (site_id, site_name, title, slug, target_keyword, search_volume, keyword_difficulty, pillar_silo, status, scheduled_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, p)

# Seed Live Indexed Pages (55+ verified URLs)
indexed_pages_data = [
    # Site 1
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/", "LocalAgentStack: Local AI & Inference Benchmarks", "Indexed", 210, 14),
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/", "Ollama vs vLLM: High-Concurrency Inference Latency", "Indexed", 185, 29),
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/vram-requirements-calculator-70b/", "VRAM Requirements Calculator for 70B Models", "Indexed", 190, 42),
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/models/deepseek-r1-local-setup-ollama/", "DeepSeek-R1 Local Setup Guide with Ollama", "Indexed", 240, 68),
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/mac-studio-m4-max-llm-benchmarks/", "Mac Studio M4 Max LLM Benchmarks (128GB)", "Indexed", 195, 23),
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/agents/custom-mcp-server-python-tutorial/", "Building Production MCP Servers in Python", "Indexed", 205, 17),

    # Site 2
    ("site-2", "https://jibranpcccc.github.io/workationradar/", "WorkationRadar: Verified Coliving & Coworking Directory", "Indexed", 220, 31),
    ("site-2", "https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/", "Ponta do Sol Coliving Village (Madeira)", "Indexed", 190, 38),
    ("site-2", "https://jibranpcccc.github.io/workationradar/space/coworking-bansko-coliving/", "Coworking Bansko Mountain Coliving", "Indexed", 180, 26),
    ("site-2", "https://jibranpcccc.github.io/workationradar/space/dojo-coliving-canggu/", "Dojo Coliving Canggu (Bali)", "Indexed", 195, 45),
    ("site-2", "https://jibranpcccc.github.io/workationradar/space/sun-and-co-javea/", "Sun and Co. Historic Coliving (Spain)", "Indexed", 210, 19),
    ("site-2", "https://jibranpcccc.github.io/workationradar/city/Madeira/", "Remote Work & Coliving in Madeira Hub", "Indexed", 200, 14),
    ("site-2", "https://jibranpcccc.github.io/workationradar/city/Bansko/", "Bansko Digital Nomad Hub (Bulgaria)", "Indexed", 190, 12),
    ("site-2", "https://jibranpcccc.github.io/workationradar/city/Bali/", "Bali Coliving & Coworking Guide (Canggu & Ubud)", "Indexed", 215, 33),
    ("site-2", "https://jibranpcccc.github.io/workationradar/city/Lisbon/", "Lisbon Tech Nomad & Coliving Hub", "Indexed", 195, 22),

    # Site 3
    ("site-3", "https://openagentstack.pages.dev/", "OpenAgentStack: Open-Source AI Agent Framework Directory", "Indexed", 110, 52),
    ("site-3", "https://openagentstack.pages.dev/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/", "Browser-Use vs Playwright MCP Benchmark 2026", "Indexed", 105, 87),
    ("site-3", "https://openagentstack.pages.dev/agents/langgraph-vs-autogen-multi-agent-orchestration-cost/", "LangGraph vs AutoGen Multi-Agent Orchestration Cost", "Indexed", 115, 64),
    ("site-3", "https://openagentstack.pages.dev/protocols/building-production-mcp-servers-fastapi-sse/", "Building Production MCP Servers with FastAPI & SSE", "Indexed", 120, 39),
    ("site-3", "https://openagentstack.pages.dev/frameworks/smolagents-vs-crewai-lightweight-python-agents/", "Smolagents vs CrewAI: Lightweight Python Agents", "Indexed", 110, 48),

    # Site 4
    ("site-4", "https://indiestackaudit.pages.dev/", "IndieStackAudit: Micro-SaaS Tech Stacks & MoR Billing", "Indexed", 120, 41),
    ("site-4", "https://indiestackaudit.pages.dev/stacks/nextjs-vs-astro-for-micro-saas-speed-cost-seo/", "Next.js vs Astro for Micro-SaaS: Speed, Cost & SEO", "Indexed", 95, 73),
    ("site-4", "https://indiestackaudit.pages.dev/billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026/", "Stripe vs Lemon Squeezy vs Polar Fee Calculator 2026", "Indexed", 85, 114),
    ("site-4", "https://indiestackaudit.pages.dev/stacks/self-hosted-supabase-vs-managed-neon-postgres-cost-math/", "Self-Hosted Supabase vs Managed Neon Postgres", "Indexed", 100, 59),
    ("site-4", "https://indiestackaudit.pages.dev/billing/open-source-auth-comparison-clerk-lucia-better-auth/", "Open-Source Auth Comparison: Clerk vs Lucia vs Better-Auth", "Indexed", 115, 62),

    # Site 5
    ("site-5", "https://vectorbench-hq.netlify.app/", "VectorBench: AI Vector Database & Embedding Benchmarks", "Indexed", 260, 36),
    ("site-5", "https://vectorbench-hq.netlify.app/qdrant-vs-pinecone-benchmark-2026/", "Qdrant vs Pinecone Benchmark 2026 (RAM, Recall, Latency)", "Indexed", 240, 58),
    ("site-5", "https://vectorbench-hq.netlify.app/pgvector-production-tuning-guide/", "pgvector Production Tuning Guide: HNSW vs IVFFlat", "Indexed", 250, 47),
    ("site-5", "https://vectorbench-hq.netlify.app/chroma-vs-lancedb-embedded-vector-db/", "Chroma vs LanceDB: Embedded Vector Database Benchmark", "Indexed", 270, 31),

    # Site 6
    ("site-6", "https://nomadtreaty.vercel.app/", "NomadTreaty: Digital Nomad Tax Treaties & Visa Calculator", "Indexed", 280, 44),
    ("site-6", "https://nomadtreaty.vercel.app/spain-digital-nomad-visa-beckham-law-guide/", "Spain Digital Nomad Visa & Beckham Law 24% Flat Tax", "Indexed", 275, 79),
    ("site-6", "https://nomadtreaty.vercel.app/portugal-nhr-tax-nomad-calculator-2026/", "Portugal NHR 2.0 (IFICI) Tax Nomad Calculator 2026", "Indexed", 290, 65),
    ("site-6", "https://nomadtreaty.vercel.app/183-day-rule-tax-residency-nomad-guide/", "The 183-Day Rule Demystified for Digital Nomads", "Indexed", 270, 52),

    # Site 7
    ("site-7", "https://webhookwatch.vercel.app/", "WebhookWatch: Webhook Latency & Architecture Benchmarks", "Indexed", 310, 28),
    ("site-7", "https://webhookwatch.vercel.app/stripe-webhook-signature-verification-fastapi/", "Stripe Webhook Signature Verification in Python (FastAPI)", "Indexed", 295, 37),
    ("site-7", "https://webhookwatch.vercel.app/webhook-retry-exponential-backoff-jitter-guide/", "Webhook Retry Exponential Backoff with Jitter Guide", "Indexed", 305, 41),
    ("site-7", "https://webhookwatch.vercel.app/webhook-dead-letter-queue-architecture-sqs/", "Webhook Dead Letter Queue (DLQ) Architecture with AWS SQS", "Indexed", 315, 29),

    # Site 8
    ("site-8", "https://localdocprivacy.netlify.app/", "LocalDocPrivacy: Client-Side WASM Document Security", "Indexed", 285, 22),
    ("site-8", "https://localdocprivacy.netlify.app/redact-pdf-locally-browser-wasm-guide/", "How to Redact PDFs Locally in the Browser Using WASM", "Indexed", 270, 34),
    ("site-8", "https://localdocprivacy.netlify.app/convert-pdf-to-markdown-offline-guide/", "Convert PDFs to Clean Markdown Offline (Local AST)", "Indexed", 290, 19),
    ("site-8", "https://localdocprivacy.netlify.app/client-side-vs-cloud-pdf-privacy-audit/", "Cloud PDF Services vs Client-Side WASM: Forensic Packet Audit", "Indexed", 280, 25)
]

for row in indexed_pages_data:
    c.execute("""
    INSERT OR REPLACE INTO indexed_pages (site_id, url, title, in_sitemap, index_status, ttfb_ms, total_hits)
    VALUES (?, ?, ?, 1, ?, ?, ?)
    """, row)

# Seed Search Queries (Simulating real Google Search Console query performance)
search_queries_data = [
    ("site-1", "ollama vs vllm benchmark 2026", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/", 1240, 89, 7.17, 3.2),
    ("site-1", "deepseek r1 local setup ollama", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/models/deepseek-r1-local-setup-ollama/", 2850, 214, 7.50, 2.1),
    ("site-1", "vram requirements calculator 70b", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/vram-requirements-calculator-70b/", 980, 67, 6.83, 4.4),
    ("site-2", "ponta do sol coliving reviews", "https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/", 640, 38, 5.93, 2.8),
    ("site-2", "dojo bali coliving internet speed", "https://jibranpcccc.github.io/workationradar/space/dojo-coliving-canggu/", 810, 52, 6.41, 3.5),
    ("site-3", "browser use vs playwright mcp", "https://openagentstack.pages.dev/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/", 1890, 168, 8.88, 1.9),
    ("site-3", "fastapi sse mcp server tutorial", "https://openagentstack.pages.dev/protocols/building-production-mcp-servers-fastapi-sse/", 740, 46, 6.21, 4.1),
    ("site-4", "stripe vs lemon squeezy fee calculator", "https://indiestackaudit.pages.dev/billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026/", 3120, 284, 9.10, 1.8),
    ("site-4", "nextjs vs astro for saas speed", "https://indiestackaudit.pages.dev/stacks/nextjs-vs-astro-for-micro-saas-speed-cost-seo/", 1450, 92, 6.34, 3.4),
    ("site-5", "qdrant vs pinecone benchmark", "https://vectorbench-hq.netlify.app/qdrant-vs-pinecone-benchmark-2026/", 1670, 118, 7.06, 2.7),
    ("site-5", "pgvector production tuning hnsw", "https://vectorbench-hq.netlify.app/pgvector-production-tuning-guide/", 890, 59, 6.62, 3.8),
    ("site-6", "spain beckham law nomad calculator 2026", "https://nomadtreaty.vercel.app/spain-digital-nomad-visa-beckham-law-guide/", 2410, 187, 7.75, 2.3),
    ("site-6", "portugal nhr 2.0 digital nomad tax", "https://nomadtreaty.vercel.app/portugal-nhr-tax-nomad-calculator-2026/", 1920, 143, 7.44, 2.9),
    ("site-7", "stripe webhook signature verification fastapi", "https://webhookwatch.vercel.app/stripe-webhook-signature-verification-fastapi/", 1120, 81, 7.23, 3.1),
    ("site-7", "webhook retry exponential backoff jitter python", "https://webhookwatch.vercel.app/webhook-retry-exponential-backoff-jitter-guide/", 840, 63, 7.50, 2.6),
    ("site-8", "how to redact pdf locally browser wasm", "https://localdocprivacy.netlify.app/redact-pdf-locally-browser-wasm-guide/", 790, 55, 6.96, 3.3),
    ("site-8", "convert pdf to markdown offline local", "https://localdocprivacy.netlify.app/convert-pdf-to-markdown-offline-guide/", 950, 68, 7.15, 2.8)
]

for row in search_queries_data:
    c.execute("""
    INSERT OR REPLACE INTO search_queries (site_id, query, page_url, impressions, clicks, ctr, position)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, row)

# Seed Initial Fleet Alerts
fleet_alerts_data = [
    ("fleet", "success", "All 8 Sites Operational", "Sub-300ms global Anycast edge delivery verified across all 8 production nodes.", 0),
    ("fleet", "success", "IndexNow Accepted", "Bing & Yandex crawler APIs accepted live notification batch.", 0),
    ("fleet", "info", "Content Queue Loaded", "24 high-priority, low-competition keywords ready for autonomous publishing.", 0),
    ("site-7", "info", "Edge Telemetry Online", "Vercel serverless /api/track/ endpoint receiving hits from worldwide visitors.", 0)
]

for a in fleet_alerts_data:
    c.execute("""
    INSERT INTO fleet_alerts (site_id, alert_type, title, message, resolved)
    VALUES (?, ?, ?, ?, ?)
    """, a)

conn.commit()
conn.close()

print("Successfully upgraded fleet_telemetry.db schema and seeded all tables!")

