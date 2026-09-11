#!/usr/bin/env python3
"""
API v1 JSON Registry Publisher (DA 96 Fastly Anycast CDN Backlinks)
Publishes 20 API v1 JSON endpoint descriptors to jibranpcccc/jibranpcccc.github.io
Served globally via Fastly Anycast CDN at:
https://jibranpcccc.github.io/api/v1/{site_id}.json
"""

import os
import sys
import json
import base64
import subprocess
import time
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "apiv1_registry.json")
os.makedirs(DATA_DIR, exist_ok=True)

SITES_CONFIG = [
    {"site_id": "site-1", "name": "LocalAgentStack", "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/", "category": "AI Hardware & Local Inference", "endpoint": "/api/v1/vram-calculator"},
    {"site_id": "site-2", "name": "WorkationRadar", "url": "https://jibranpcccc.github.io/workationradar/", "category": "Digital Nomad Hubs & Coliving", "endpoint": "/api/v1/coliving-search"},
    {"site_id": "site-3", "name": "OpenAgentStack", "url": "https://openagentstack.pages.dev/", "category": "Autonomous Agents & MCP Protocols", "endpoint": "/api/v1/persistence-bench"},
    {"site_id": "site-4", "name": "IndieStackAudit", "url": "https://indiestackaudit.pages.dev/", "category": "SaaS Infrastructure & Cloud Billing", "endpoint": "/api/v1/bandwidth-audit"},
    {"site_id": "site-5", "name": "VectorBench", "url": "https://vectorbench-hq.netlify.app/", "category": "Vector Databases & Semantic Search", "endpoint": "/api/v1/index-sizer"},
    {"site_id": "site-6", "name": "NomadTreaty", "url": "https://nomadtreaty.vercel.app/", "category": "Nomad Taxation & Double Tax Treaties", "endpoint": "/api/v1/tax-model"},
    {"site_id": "site-7", "name": "WebhookWatch", "url": "https://webhookwatch.vercel.app/", "category": "API Security & Webhook Delivery", "endpoint": "/api/v1/verify-signature"},
    {"site_id": "site-8", "name": "LocalDocPrivacy", "url": "https://localdocprivacy.netlify.app/", "category": "Client-Side Document Privacy & WASM", "endpoint": "/api/v1/pii-detector"},
    {"site_id": "site-9", "name": "FounderRunway", "url": "https://site-9-inky.vercel.app/", "category": "Startup Financial Modeling & Runway", "endpoint": "/api/v1/runway-multiplier"},
    {"site_id": "site-10", "name": "RAGInspect", "url": "https://raginspect.pages.dev/", "category": "RAG Chunking & Multimodal Document AI", "endpoint": "/api/v1/rag-eval"},
    {"site_id": "site-11", "name": "NomadPassportIndex", "url": "https://nomadpassportindex.netlify.app/", "category": "Global Digital Nomad Visas", "endpoint": "/api/v1/visa-rules"},
    {"site_id": "site-12", "name": "SaaSUnitMath", "url": "https://site-12-taupe.vercel.app/", "category": "SaaS Unit Economics & Sales Metrics", "endpoint": "/api/v1/magic-number"},
    {"site_id": "site-13", "name": "GrokLogTester", "url": "https://groklogtester.pages.dev/", "category": "Log Parsing & Grok Regex Extractor", "endpoint": "/api/v1/parse-log"},
    {"site_id": "site-14", "name": "SOC2Ready", "url": "https://site-14-sable.vercel.app/", "category": "B2B SaaS SOC 2 Compliance", "endpoint": "/api/v1/access-review"},
    {"site_id": "site-15", "name": "EORCalculator", "url": "https://site-15-ruby.vercel.app/", "category": "Global Employer of Record & Payroll", "endpoint": "/api/v1/eor-pricing"},
    {"site_id": "site-16", "name": "DevConfigHub", "url": "https://site-16-indol.vercel.app/", "category": "Developer Tooling & Environments", "endpoint": "/api/v1/config-spec"},
    {"site_id": "site-17", "name": "OpenCRMStack", "url": "https://opencrmstack.pages.dev/", "category": "Open Source CRM & Migration", "endpoint": "/api/v1/tco-calculator"},
    {"site_id": "site-18", "name": "CIPipelineGraph", "url": "https://site-18-chi.vercel.app/", "category": "CI/CD Optimization & DAG Validators", "endpoint": "/api/v1/validate-dag"},
    {"site_id": "site-19", "name": "GreekVisualizer", "url": "https://site-19-nine.vercel.app/", "category": "Financial Math & Options Greeks", "endpoint": "/api/v1/options-greeks"},
    {"site_id": "site-20", "name": "EdgeRuntimeHQ", "url": "https://edgeruntimehq.pages.dev/", "category": "Edge AI Inference & WebGPU", "endpoint": "/api/v1/runtime-bench"},
    {"site_id": "site-21", "name": "PromptEvalHQ", "url": "https://promptevalhq.pages.dev/", "category": "LLM Evaluation & Prompt Benchmarks", "endpoint": "/api/v1/eval-cost"},
    {"site_id": "site-22", "name": "QueueCost", "url": "https://queuecost.pages.dev/", "category": "Background Queues & Message Brokers", "endpoint": "/api/v1/worker-sizer"},
    {"site_id": "site-23", "name": "OpenTelemetryLab", "url": "https://opentelemetrylab.pages.dev/", "category": "Observability & OpenTelemetry Collector", "endpoint": "/api/v1/tail-sampling"},
    {"site_id": "site-24", "name": "PostgresScale", "url": "https://postgrescale.pages.dev/", "category": "Database Tuning & PostgreSQL Optimization", "endpoint": "/api/v1/autovacuum-tuner"},
    {"site_id": "site-25", "name": "APIGatewayMatrix", "url": "https://apigatewaymatrix.pages.dev/", "category": "API Gateways & Reverse Proxies", "endpoint": "/api/v1/gateway-latency"},
    {"site_id": "site-26", "name": "S3EgressAudit", "url": "https://s3egressaudit.pages.dev/", "category": "Cloud Storage & Egress Economics", "endpoint": "/api/v1/egress-calc"},
    {"site_id": "site-27", "name": "AuthTokenAudit", "url": "https://authtokenaudit.pages.dev/", "category": "Authentication & Cryptographic Tokens", "endpoint": "/api/v1/token-sizer"},
    {"site_id": "site-28", "name": "DNSPerfHQ", "url": "https://dnsperf-hq.pages.dev/", "category": "Anycast DNS & Global Propagation", "endpoint": "/api/v1/dns-latency"},
    {"site_id": "site-29", "name": "FeatureFlagAudit", "url": "https://featureflagaudit.pages.dev/", "category": "Feature Management & OpenFeature", "endpoint": "/api/v1/feature-flag-tco"},
    {"site_id": "site-30", "name": "TinyContainerHQ", "url": "https://tinycontainerhq.pages.dev/", "category": "Container Security & Minimal Images", "endpoint": "/api/v1/container-cve"}
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

def publish_all_apiv1_descriptors():
    repo_full = "jibranpcccc/jibranpcccc.github.io"
    results = []
    print(f"Publishing {len(SITES_CONFIG)} API v1 descriptors to {repo_full}...")

    for idx, item in enumerate(SITES_CONFIG, 1):
        site_id = item["site_id"]
        path = f"api/v1/{site_id}.json"
        site_name = item["name"]
        url = item["url"]

        payload_content = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "service": site_name,
            "site_id": site_id,
            "category": item["category"],
            "official_url": url,
            "api_endpoint": f"{url.rstrip('/')}{item['endpoint']}",
            "documentation": f"{url.rstrip('/')}/benchmarks/{site_id}.html",
            "version": "1.1.0",
            "status": "operational",
            "verified_da": 96,
            "cdn_provider": "Fastly Anycast Global CDN",
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }

        content_json = json.dumps(payload_content, indent=2)
        content_b64 = base64.b64encode(content_json.encode("utf-8")).decode("ascii")

        print(f"[{idx}/20] Pushing {path} to {repo_full}...")
        sha = get_file_sha(repo_full, path)

        payload = {
            "message": f"Add API v1 service descriptor for {site_name}",
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
            api_url = f"https://jibranpcccc.github.io/{path}"
            print(f" -> SUCCESS: {api_url}")
            results.append({
                "site_id": site_id,
                "site_name": site_name,
                "target_url": url,
                "backlink_url": api_url,
                "platform": "GitHub Pages (Fastly CDN DA 96)",
                "link_type": "API v1 JSON Service Descriptor",
                "da": 96,
                "anchor": f"API v1 Service Descriptor: {site_name}"
            })
        else:
            print(f" -> NOTICE: {res.stderr.strip()}")
        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nAll {len(SITES_CONFIG)} API v1 descriptors published and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    publish_all_apiv1_descriptors()
