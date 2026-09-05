#!/usr/bin/env python3
"""Portfolio Audit across all 4 live niche websites."""
import urllib.request
import re

sites = [
    {
        "id": "Site 1",
        "name": "LocalAgentStack",
        "niche": "Local AI Hardware & Inference",
        "host": "GitHub Pages",
        "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/",
        "sitemap": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/sitemap.xml",
        "sample": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/"
    },
    {
        "id": "Site 2",
        "name": "WorkationRadar",
        "niche": "Digital Nomad & Coliving Spaces",
        "host": "GitHub Pages",
        "url": "https://jibranpcccc.github.io/workationradar/",
        "sitemap": "https://jibranpcccc.github.io/workationradar/sitemap.xml",
        "sample": "https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/"
    },
    {
        "id": "Site 3",
        "name": "OpenAgentStack",
        "niche": "Autonomous Agents & MCP Protocols",
        "host": "Cloudflare Pages",
        "url": "https://openagentstack.pages.dev/",
        "sitemap": "https://openagentstack.pages.dev/sitemap.xml",
        "sample": "https://openagentstack.pages.dev/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/"
    },
    {
        "id": "Site 4",
        "name": "IndieStackAudit",
        "niche": "Micro-SaaS Tech Stacks & MoR Billing",
        "host": "Cloudflare Pages",
        "url": "https://indiestackaudit.pages.dev/",
        "sitemap": "https://indiestackaudit.pages.dev/sitemap.xml",
        "sample": "https://indiestackaudit.pages.dev/stacks/nextjs-vs-astro-for-micro-saas-speed-cost-seo/"
    }
]

print("=" * 80)
print("PORTFOLIO AUDIT REPORT: 4 NICHES / 4 SITES")
print("=" * 80)

for s in sites:
    print(f"\n--- [{s['id']}] {s['name']} | Niche: {s['niche']} ({s['host']}) ---")
    for label, target in [("Homepage", s["url"]), ("Sitemap", s["sitemap"]), ("Sample Guide", s["sample"])]:
        try:
            req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                code = r.status
                body = r.read().decode("utf-8", errors="ignore")
                t_match = re.search(r"<title>(.*?)</title>", body, re.IGNORECASE)
                title = t_match.group(1).strip() if t_match else "N/A"
                print(f"  [HTTP {code}] {label:15}: {len(body):,} bytes | {title[:55]}...")
        except Exception as e:
            print(f"  [ERROR] {label:15}: {e}")

print("\n" + "=" * 80)
