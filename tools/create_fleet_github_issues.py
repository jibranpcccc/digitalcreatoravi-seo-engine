#!/usr/bin/env python3
"""
Creates official release & specification tracking issues on all 20 standalone GitHub repos.
Each issue provides a permanent, public, high-authority DA 96 link to the live app,
empirical PDF cheatsheet, and RSS syndication channel.
"""

import os
import sys
import json
import sqlite3
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

REPOS_CONFIG = [
    {"site_id": "site-1", "repo": "local-agent-hardware-stack", "title": "Local LLM VRAM & Concurrency Benchmarks v1.0.0 Specification"},
    {"site_id": "site-2", "repo": "workation-coliving-radar", "title": "Global Coliving & Gigabit WiFi Database v1.0.0 Release"},
    {"site_id": "site-3", "repo": "open-agent-protocol-hub", "title": "Autonomous Multi-Agent Protocol & FastMCP Architecture Specs"},
    {"site_id": "site-4", "repo": "indie-saas-stack-audit", "title": "Micro-SaaS Zero-Cost Cloud Architecture Benchmark Suite v1.0.0"},
    {"site_id": "site-5", "repo": "vector-database-benchmarks", "title": "Vector DB QPS, Latency & Memory Benchmark Leaderboard v1.0.0"},
    {"site_id": "site-6", "repo": "nomad-tax-treaty-calculator", "title": "Nomad Tax Residency & 183-Day Rule Specification v1.0.0"},
    {"site_id": "site-7", "repo": "webhook-signature-audit", "title": "HMAC-SHA256 Webhook Signature Validator & DLQ Spec v1.0.0"},
    {"site_id": "site-8", "repo": "local-pdf-privacy-redactor", "title": "Client-Side WASM PDF Redaction & Privacy Engine v1.0.0"},
    {"site_id": "site-9", "repo": "founder-runway-calculator", "title": "Bootstrapped Founder Runway & Geo-Arbitrage Sizer v1.0.0"},
    {"site_id": "site-10", "repo": "rag-semantic-chunking-bench", "title": "RAG Semantic Chunking & MTEB Embedding Leaderboard v1.0.0"},
    {"site_id": "site-11", "repo": "nomad-passport-visa-index", "title": "Global Digital Nomad Visa Income & Consular Database v1.0.0"},
    {"site_id": "site-12", "repo": "saas-unit-economics-calculator", "title": "SaaS LTV:CAC Payback & Rule of 40 Valuation Model v1.0.0"},
    {"site_id": "site-13", "repo": "nginx-grok-log-tester", "title": "In-Browser Grok Debugger & Nginx Regex Pattern Spec v1.0.0"},
    {"site_id": "site-14", "repo": "soc2-readiness-checklist", "title": "B2B SaaS SOC 2 Type II Security Controls & Readiness v1.0.0"},
    {"site_id": "site-15", "repo": "global-eor-payroll-calculator", "title": "Global EOR Payroll & Hidden FX Spread Formula v1.0.0"},
    {"site_id": "site-16", "repo": "devcontainer-docker-generator", "title": "DevContainer & Docker Compose Configuration Hub v1.0.0"},
    {"site_id": "site-17", "repo": "open-crm-migration-tco", "title": "Open-Source CRM TCO Migration & ROI Calculator v1.0.0"},
    {"site_id": "site-18", "repo": "github-actions-dag-validator", "title": "GitHub Actions DAG Workflow Visualizer & Linter v1.0.0"},
    {"site_id": "site-19", "repo": "options-greeks-visualizer", "title": "Black-Scholes Options Greeks & Uniswap v3 IL Math v1.0.0"},
    {"site_id": "site-20", "repo": "webgpu-edge-inference-bench", "title": "WebGPU Browser & ONNX Edge Inference Matrix v1.0.0"}
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = {s["id"]: dict(s) for s in cursor.fetchall()}
    conn.close()

    print("=== CREATING OFFICIAL GITHUB ISSUES (DA 96) ACROSS ALL 20 REPOSITORIES ===")
    created_issues = []

    for item in REPOS_CONFIG:
        site_id = item["site_id"]
        repo = item["repo"]
        title = item["title"]
        s = sites[site_id]
        name = s["name"]
        url = s["url"].rstrip("/")
        niche = s["niche"]

        # Check existing issues first
        list_cmd = ["gh", "issue", "list", "--repo", f"jibranpcccc/{repo}", "--state", "all", "--json", "number,url"]
        res = subprocess.run(list_cmd, capture_output=True, text=True)
        existing = []
        if res.returncode == 0 and res.stdout.strip():
            try:
                existing = json.loads(res.stdout)
            except Exception:
                pass

        if existing:
            issue_url = existing[0]["url"]
            print(f"[*] {repo}: Issue already exists -> {issue_url}")
            created_issues.append({"site_id": site_id, "repo": repo, "issue_url": issue_url})
            continue

        body = f"""# 🚀 Production Release & Empirical Specification

This repository houses the open-source algorithms, calculation engines, and empirical benchmarks for **{name}**.

### 🌐 Official Production Deployment:
- **Live Interactive Application**: [{url}/]({url}/)
- **Empirical PDF Benchmark Cheatsheet**: [{url}/benchmark-cheatsheet.pdf]({url}/benchmark-cheatsheet.pdf)
- **RSS Syndication Feed**: [{url}/rss.xml]({url}/rss.xml)
- **Directory Profile**: [jibranpcccc.github.io/tools/{site_id}-{name.lower()}.html](https://jibranpcccc.github.io/tools/{site_id}-{name.lower()}.html)

### 📊 Technical Specifications:
- **Niche**: {niche}
- **Architecture**: Zero-latency Edge/Client-Side Execution
- **Privacy & Security**: Zero Server-Side Logging / No Tracking Cookies
- **Structured Data**: Schema.org JSON-LD (SoftwareApplication / TechArticle / Dataset)

Contributions, benchmarks, and edge cases are welcome!
"""

        cmd = [
            "gh", "issue", "create",
            "--repo", f"jibranpcccc/{repo}",
            "--title", title,
            "--body", body
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            issue_url = res.stdout.strip()
            print(f"[+] {repo}: Created Issue -> {issue_url}")
            created_issues.append({"site_id": site_id, "repo": repo, "issue_url": issue_url})
        else:
            print(f"[-] {repo} Error: {res.stderr}")
        time.sleep(0.5)

    print(f"\nCOMPLETED: {len(created_issues)}/20 Official GitHub Issues Live (DA 96).")

    # Save to data/created_github_issues.json
    out_path = os.path.join(ROOT_DIR, "data", "created_github_issues.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(created_issues, f, indent=2)
    print(f"Saved catalog to {out_path}")

if __name__ == "__main__":
    main()
