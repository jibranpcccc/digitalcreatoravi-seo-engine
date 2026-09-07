#!/usr/bin/env python3
"""
Deploys api/v1/tools.json and sitemap-tools.xml to jibranpcccc.github.io (DA 96).
Provides search engines, AI crawlers, and API clients with a high-density,
machine-readable directory linking to all 20 web tools, repos, issues, and assets.
"""

import os
import sys
import json
import base64
import sqlite3
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def push_github_file(repo, file_path, content_bytes, commit_msg):
    b64 = base64.b64encode(content_bytes).decode("utf-8")
    payload = {
        "message": commit_msg,
        "content": b64,
        "branch": "main"
    }

    # Check sha if exists
    check_res = subprocess.run(["gh", "api", f"/repos/{repo}/contents/{file_path}"], capture_output=True, text=True)
    if check_res.returncode == 0:
        payload["sha"] = json.loads(check_res.stdout).get("sha")

    put_cmd = ["gh", "api", "--method", "PUT", f"/repos/{repo}/contents/{file_path}", "--input", "-"]
    res = subprocess.run(put_cmd, input=json.dumps(payload), text=True, capture_output=True)
    if res.returncode == 0:
        print(f"[+] Pushed https://jibranpcccc.github.io/{file_path}")
        return True
    else:
        print(f"[-] Error pushing {file_path}: {res.stderr}")
        return False

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # Load created issues
    issues_file = os.path.join(ROOT_DIR, "data", "created_github_issues.json")
    issues_map = {}
    if os.path.exists(issues_file):
        with open(issues_file, "r", encoding="utf-8") as f:
            issues = json.load(f)
            issues_map = {i["site_id"]: i["issue_url"] for i in issues}

    REPOS_MAP = {
        "site-1": "local-agent-hardware-stack",
        "site-2": "workation-coliving-radar",
        "site-3": "open-agent-protocol-hub",
        "site-4": "indie-saas-stack-audit",
        "site-5": "vector-database-benchmarks",
        "site-6": "nomad-tax-treaty-calculator",
        "site-7": "webhook-signature-audit",
        "site-8": "local-pdf-privacy-redactor",
        "site-9": "founder-runway-calculator",
        "site-10": "rag-semantic-chunking-bench",
        "site-11": "nomad-passport-visa-index",
        "site-12": "saas-unit-economics-calculator",
        "site-13": "nginx-grok-log-tester",
        "site-14": "soc2-readiness-checklist",
        "site-15": "global-eor-payroll-calculator",
        "site-16": "devcontainer-docker-generator",
        "site-17": "open-crm-migration-tco",
        "site-18": "github-actions-dag-validator",
        "site-19": "options-greeks-visualizer",
        "site-20": "webgpu-edge-inference-bench"
    }

    tools_data = []
    for s in sites:
        site_id = s["id"]
        repo_name = REPOS_MAP.get(site_id, "")
        tools_data.append({
            "id": site_id,
            "name": s["name"],
            "url": s["url"],
            "niche": s["niche"],
            "github_repo": f"https://github.com/jibranpcccc/{repo_name}" if repo_name else None,
            "github_issue": issues_map.get(site_id),
            "directory_profile": f"https://jibranpcccc.github.io/tools/{site_id}-{s['name'].lower()}.html",
            "pdf_cheatsheet": f"{s['url'].rstrip('/')}/benchmark-cheatsheet.pdf",
            "rss_feed": f"{s['url'].rstrip('/')}/rss.xml",
            "open_source": True,
            "license": "MIT"
        })

    api_json = {
        "title": "Open Engineering Tools & Empirical Benchmarks Registry",
        "version": "1.0.0",
        "publisher": "Jibran Ayub",
        "profile": "https://github.com/jibranpcccc",
        "total_tools": len(tools_data),
        "tools": tools_data
    }

    print("=== DEPLOYING API/V1/TOOLS.JSON TO JIBRANPCCCC.GITHUB.IO ===")
    push_github_file(
        "jibranpcccc/jibranpcccc.github.io",
        "api/v1/tools.json",
        json.dumps(api_json, indent=2).encode("utf-8"),
        "feat(api): publish machine-readable tools registry (v1.0.0)"
    )

    # Sitemap XML for tools
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap_lines.append('  <url><loc>https://jibranpcccc.github.io/tools.html</loc><changefreq>daily</changefreq><priority>1.0</priority></url>')
    sitemap_lines.append('  <url><loc>https://jibranpcccc.github.io/api/v1/tools.json</loc><changefreq>daily</changefreq><priority>0.9</priority></url>')
    for s in sites:
        site_id = s["id"]
        slug = f"{site_id}-{s['name'].lower()}"
        sitemap_lines.append(f'  <url><loc>https://jibranpcccc.github.io/tools/{slug}.html</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    sitemap_lines.append('</urlset>')
    sitemap_xml = "\n".join(sitemap_lines)

    print("=== DEPLOYING SITEMAP-TOOLS.XML TO JIBRANPCCCC.GITHUB.IO ===")
    push_github_file(
        "jibranpcccc/jibranpcccc.github.io",
        "sitemap-tools.xml",
        sitemap_xml.encode("utf-8"),
        "feat(seo): publish sitemap-tools.xml indexing all 20 tool profiles"
    )

if __name__ == "__main__":
    main()
