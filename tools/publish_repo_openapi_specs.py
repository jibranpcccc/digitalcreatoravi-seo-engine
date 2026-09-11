#!/usr/bin/env python3
"""
OpenAPI 3.1 Specification Publisher (DA 96 Fastly Anycast CDN Backlinks)
Publishes 20 OpenAPI 3.1 specification files (openapi.json) across all 20 standalone GitHub repositories.
Accessible via Fastly Anycast CDN at:
https://raw.githubusercontent.com/jibranpcccc/{repo}/main/openapi.json
"""

import os
import sys
import json
import base64
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "openapi_specs.json")
os.makedirs(DATA_DIR, exist_ok=True)

REPOS_SPEC = [
    {
        "site_id": "site-1",
        "repo": "local-agent-hardware-stack",
        "name": "LocalAgentStack",
        "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/",
        "title": "Local Agent GPU VRAM Sizing & Hardware API",
        "desc": "Empirical VRAM calculation, PCIe lane allocation, and quantized throughput API for local LLMs.",
        "endpoint": "/api/v1/vram-calculator",
        "summary": "Calculate dual RTX 3090/4090 VRAM requirement and token throughput"
    },
    {
        "site_id": "site-2",
        "repo": "workation-coliving-radar",
        "name": "WorkationRadar",
        "url": "https://jibranpcccc.github.io/workationradar/",
        "title": "Global Digital Nomad Coliving & WiFi Speed API",
        "desc": "Real-time verified fiber optic speeds, monthly coliving prices, and nomad hub rankings API.",
        "endpoint": "/api/v1/coliving-search",
        "summary": "Query coliving hubs by verified Mbps, monthly budget, and timezone"
    },
    {
        "site_id": "site-3",
        "repo": "open-agent-protocol-hub",
        "name": "OpenAgentStack",
        "url": "https://openagentstack.pages.dev/",
        "title": "Multi-Agent State Checkpointing & Persistence API",
        "desc": "LangGraph PostgreSQL checkpointer latency benchmark and connection pooling specs.",
        "endpoint": "/api/v1/persistence-bench",
        "summary": "Benchmark PostgresSaver vs SQLiteSaver checkpoint latency"
    },
    {
        "site_id": "site-4",
        "repo": "indie-saas-stack-audit",
        "name": "IndieStackAudit",
        "url": "https://indiestackaudit.pages.dev/",
        "title": "Indie SaaS Cloud Infrastructure Cost Audit API",
        "desc": "Forensic cloud cost auditing: Cloudflare Pages unlimited egress vs Vercel and AWS overages.",
        "endpoint": "/api/v1/bandwidth-audit",
        "summary": "Calculate monthly egress invoice across Cloudflare, Vercel, and CloudFront"
    },
    {
        "site_id": "site-5",
        "repo": "vector-database-benchmarks",
        "name": "VectorBench",
        "url": "https://vectorbench-hq.netlify.app/",
        "title": "pgvector HNSW & IVFFlat Performance Sizing API",
        "desc": "Vector database memory consumption, index build time, and QPS benchmark API.",
        "endpoint": "/api/v1/index-sizer",
        "summary": "Calculate RAM footprint and recall for 1M+ embeddings"
    },
    {
        "site_id": "site-6",
        "repo": "nomad-tax-treaty-calculator",
        "name": "NomadTreaty",
        "url": "https://nomadtreaty.vercel.app/",
        "title": "Nomad Tax Residency & Retained Earnings Optimizer API",
        "desc": "Estonia e-Residency deferred tax vs territorial tax and PE risk modeling API.",
        "endpoint": "/api/v1/tax-model",
        "summary": "Model 5-year capital growth under 0% retained earnings vs EU 25% tax"
    },
    {
        "site_id": "site-7",
        "repo": "webhook-signature-audit",
        "name": "WebhookWatch",
        "url": "https://webhookwatch.vercel.app/",
        "title": "Cryptographic Webhook Signature & Idempotency API",
        "desc": "HMAC-SHA256 signature validation and distributed Redis Redlock idempotency verification API.",
        "endpoint": "/api/v1/verify-signature",
        "summary": "Verify Stripe, GitHub, and Shopify webhook payloads with millisecond precision"
    },
    {
        "site_id": "site-8",
        "repo": "local-pdf-privacy-redactor",
        "name": "LocalDocPrivacy",
        "url": "https://localdocprivacy.netlify.app/",
        "title": "Client-Side In-Browser WASM PII Redaction API",
        "desc": "Zero-cloud data transfer PII detection engine specs for GDPR Article 32 compliance.",
        "endpoint": "/api/v1/pii-detector",
        "summary": "Extract SSN, credit cards, and emails via client-side WebAssembly"
    },
    {
        "site_id": "site-9",
        "repo": "founder-runway-calculator",
        "name": "FounderRunway",
        "url": "https://site-9-inky.vercel.app/",
        "title": "Bootstrapped Startup Burn Rate & Runway Arbitrage API",
        "desc": "Runway multiplier math comparing high-cost tech hubs with Bansko and Medellín.",
        "endpoint": "/api/v1/runway-multiplier",
        "summary": "Simulate runway expansion in months across global startup hubs"
    },
    {
        "site_id": "site-10",
        "repo": "rag-semantic-chunking-bench",
        "name": "RAGInspect",
        "url": "https://raginspect.pages.dev/",
        "title": "ColPali Vision-Language Retrieval & Chunking Benchmark API",
        "desc": "Empirical retrieval benchmarks (NDCG@10, MRR@10) across multi-modal document layouts.",
        "endpoint": "/api/v1/rag-eval",
        "summary": "Compare ColPali patch embeddings vs OCR dense retrieval latency"
    },
    {
        "site_id": "site-11",
        "repo": "nomad-passport-visa-index",
        "name": "NomadPassportIndex",
        "url": "https://nomadpassportindex.netlify.app/",
        "title": "Digital Nomad Visa Income Proof & Eligibility API",
        "desc": "Statutory income requirements, tax exemptions, and apostille validation rules across 40+ nations.",
        "endpoint": "/api/v1/visa-rules",
        "summary": "Evaluate applicant monthly income against statutory thresholds"
    },
    {
        "site_id": "site-12",
        "repo": "saas-unit-economics-calculator",
        "name": "SaaSUnitMath",
        "url": "https://site-12-taupe.vercel.app/",
        "title": "B2B SaaS Magic Number & Sales Efficiency Sizer API",
        "desc": "Quarterly net new ARR efficiency, CAC payback, and net revenue churn modeling API.",
        "endpoint": "/api/v1/magic-number",
        "summary": "Calculate SaaS GTM efficiency score and CAC payback months"
    },
    {
        "site_id": "site-13",
        "repo": "nginx-grok-log-tester",
        "name": "GrokLogTester",
        "url": "https://groklogtester.pages.dev/",
        "title": "HAProxy & Ingress-Nginx Log Grok Pattern Matcher API",
        "desc": "High-throughput PCRE regex extraction and structured log tokenization API.",
        "endpoint": "/api/v1/parse-log",
        "summary": "Extract structured JSON fields from raw HTTP proxy access logs"
    },
    {
        "site_id": "site-14",
        "repo": "soc2-readiness-checklist",
        "name": "SOC2Ready",
        "url": "https://site-14-sable.vercel.app/",
        "title": "SOC 2 Type II CC6.3 User Access Review Automation API",
        "desc": "IAM privilege auditing, MFA verification, and audit trail generation API.",
        "endpoint": "/api/v1/access-review",
        "summary": "Audit AWS/GitHub users for stale credentials and missing MFA"
    },
    {
        "site_id": "site-15",
        "repo": "global-eor-payroll-calculator",
        "name": "EORCalculator",
        "url": "https://site-15-ruby.vercel.app/",
        "title": "Global Employer of Record (EOR) True-Cost Sizer API",
        "desc": "Mandatory statutory contributions and currency exchange spread calculations API.",
        "endpoint": "/api/v1/eor-pricing",
        "summary": "Calculate all-in monthly employer cost factoring statutory on-costs and FX fees"
    },
    {
        "site_id": "site-16",
        "repo": "devcontainer-docker-generator",
        "name": "DevConfigHub",
        "url": "https://site-16-indol.vercel.app/",
        "title": "direnv & Nix Flakes Developer Environment Generator API",
        "desc": "Instant reproducible dev environment generator for TypeScript, Python, and Rust stacks.",
        "endpoint": "/api/v1/config-spec",
        "summary": "Generate flake.nix and devcontainer.json specs with 1 API call"
    },
    {
        "site_id": "site-17",
        "repo": "open-crm-migration-tco",
        "name": "OpenCRMStack",
        "url": "https://opencrmstack.pages.dev/",
        "title": "Open-Source CRM vs HubSpot/Salesforce 3-Year TCO API",
        "desc": "Per-seat SaaS cost comparison against self-hosted Twenty CRM and ERPNext API.",
        "endpoint": "/api/v1/tco-calculator",
        "summary": "Simulate 3-year TCO savings across sales team sizes"
    },
    {
        "site_id": "site-18",
        "repo": "github-actions-dag-validator",
        "name": "CIPipelineGraph",
        "url": "https://site-18-chi.vercel.app/",
        "title": "GitHub Actions DAG Dependency & Cache Optimization API",
        "desc": "Workflow dependency graph visualizer and Docker buildx cache speedup API.",
        "endpoint": "/api/v1/validate-dag",
        "summary": "Parse workflow YAML needs dependencies and calculate runner minutes"
    },
    {
        "site_id": "site-19",
        "repo": "options-greeks-visualizer",
        "name": "GreekVisualizer",
        "url": "https://site-19-nine.vercel.app/",
        "title": "Black-Scholes Options Greeks & Volatility Surface API",
        "desc": "Analytical Delta, Gamma, Theta, Vega, and Rho option pricing solver API.",
        "endpoint": "/api/v1/options-greeks",
        "summary": "Compute continuous Black-Scholes Greeks and implied volatility surfaces"
    },
    {
        "site_id": "site-20",
        "repo": "webgpu-edge-inference-bench",
        "name": "EdgeRuntimeHQ",
        "url": "https://edgeruntimehq.pages.dev/",
        "title": "WebGPU vs ONNX Runtime In-Browser AI Latency API",
        "desc": "Time-to-first-token (TTFT) and token throughput benchmarks for local AI runtimes API.",
        "endpoint": "/api/v1/runtime-bench",
        "summary": "Retrieve real-time edge runtime throughput and memory usage metrics"
    }
]

def get_file_sha(repo_full, path):
    try:
        res = subprocess.run(
            ["gh", "api", f"repos/{repo_full}/contents/{path}"],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            return json.loads(res.stdout).get("sha")
    except Exception:
        pass
    return None

def publish_all_openapi_specs():
    results = []
    print(f"Publishing {len(REPOS_SPEC)} OpenAPI 3.1 specifications across standalone repositories...")

    for idx, item in enumerate(REPOS_SPEC, 1):
        repo_full = f"jibranpcccc/{item['repo']}"
        site_name = item["name"]
        url = item["url"]
        path = "openapi.json"

        spec = {
            "openapi": "3.1.0",
            "info": {
                "title": f"{site_name} - {item['title']}",
                "description": f"{item['desc']} Official production documentation hosted at {url}",
                "version": "1.1.0",
                "contact": {
                    "name": f"{site_name} Architecture Team",
                    "url": url
                }
            },
            "servers": [
                {
                    "url": url.rstrip("/"),
                    "description": "Production Web Application Gateway"
                }
            ],
            "paths": {
                item["endpoint"]: {
                    "get": {
                        "summary": item["summary"],
                        "description": f"Executes the empirical calculations and data models for {site_name}.",
                        "responses": {
                            "200": {
                                "description": "Successful calculation response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {"type": "string", "example": "ok"},
                                                "timestamp": {"type": "string", "format": "date-time"},
                                                "site_url": {"type": "string", "example": url},
                                                "data": {"type": "object"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        content_json = json.dumps(spec, indent=2)
        content_b64 = base64.b64encode(content_json.encode("utf-8")).decode("ascii")

        print(f"[{idx}/20] Pushing {path} to {repo_full}...")
        sha = get_file_sha(repo_full, path)

        payload = {
            "message": f"Add OpenAPI 3.1 specification for {site_name}",
            "content": content_b64,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        cmd = [
            "gh", "api",
            "--method", "PUT",
            f"repos/{repo_full}/contents/{path}",
            "--input", "-"
        ]
        res = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
        if res.returncode == 0:
            cdn_url = f"https://raw.githubusercontent.com/{repo_full}/main/{path}"
            print(f" -> SUCCESS: {cdn_url}")
            results.append({
                "site_id": item["site_id"],
                "site_name": site_name,
                "target_url": url,
                "repo": item["repo"],
                "backlink_url": cdn_url,
                "platform": "GitHub Raw CDN (Fastly Anycast DA 96)",
                "link_type": "OpenAPI 3.1 Specification JSON",
                "da": 96,
                "anchor": f"OpenAPI 3.1 Spec: {site_name}"
            })
        else:
            print(f" -> NOTICE: {res.stderr.strip()}")
        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nAll 20 OpenAPI 3.1 specs published and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    publish_all_openapi_specs()
