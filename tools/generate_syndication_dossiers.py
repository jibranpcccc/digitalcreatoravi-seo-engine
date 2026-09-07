#!/usr/bin/env python3
"""
Generates complete, publication-ready Syndication & Directory Submission Dossiers.
1. syndication/directory_submissions.md (AlternativeTo, ProductHunt, BetaList, SaaSHub)
2. syndication/devto_canonical_articles.md (Dev.to & Hashnode with canonical tags)
"""

import os
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")
SYNDICATION_DIR = os.path.join(ROOT_DIR, "syndication")
os.makedirs(SYNDICATION_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # 1. Directory Submissions
    dir_lines = [
        "# 🚀 Master Directory & AlternativeTo Submission Dossier",
        "",
        "Use these pre-formatted submission templates for **AlternativeTo (DA 78)**, **Product Hunt (DA 90)**, **BetaList (DA 75)**, and **SaaSHub (DA 76)**.",
        "",
        "---",
        ""
    ]

    for s in sites:
        site_id = s["id"]
        name = s["name"]
        url = s["url"]
        niche = s["niche"]
        
        dir_lines.append(f"## [{site_id}] {name}")
        dir_lines.append(f"- **Website URL:** {url}")
        dir_lines.append(f"- **Tagline:** Free, client-side interactive {niche} platform.")
        dir_lines.append(f"- **Pricing Model:** 100% Free / Open-Source (MIT)")
        dir_lines.append(f"- **Primary Category:** Developer Tools / Productivity / Finance")
        dir_lines.append(f"- **Alternative To:** Competitor solutions in {niche}")
        dir_lines.append(f"- **Short Description:** {name} is a zero-latency, local-first web utility for {niche} with sub-100ms response time and zero external server tracking.")
        dir_lines.append(f"- **Key Features:**")
        dir_lines.append(f"  - 100% client-side calculation")
        dir_lines.append(f"  - Verified Schema.org structured data")
        dir_lines.append(f"  - No signup or credit card required")
        dir_lines.append(f"  - Pre-rendered static edge performance")
        dir_lines.append("")
        dir_lines.append("---")
        dir_lines.append("")

    with open(os.path.join(SYNDICATION_DIR, "directory_submissions.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(dir_lines))

    # 2. Dev.to Canonical Articles
    devto_lines = [
        "# 📝 Dev.to & Hashnode High-DA Canonical Articles",
        "",
        "Publish these on **Dev.to (DA 85)** and **Hashnode (DA 87)**. The `canonical_url` tag guarantees 100% SEO credit transfers to your live tools.",
        "",
        "---",
        "",
        "## Article 1: Sector 1 (AI Engineering)",
        "```markdown",
        "---",
        "title: Benchmarking Production RAG: Semantic Chunking vs Fixed-Size Windows in 2026",
        "published: true",
        "tags: ai, machinelearning, python, webdev",
        "canonical_url: https://raginspect.pages.dev/semantic-chunking-vs-fixed-size-rag-benchmarks/",
        "---",
        "",
        "# Benchmarking Production RAG: Semantic Chunking vs Fixed-Size Windows",
        "",
        "When building production Retrieval-Augmented Generation (RAG) pipelines, the choice of text segmentation directly impacts retrieval accuracy...",
        "",
        "Explore the interactive visualizer live: [RAGInspect](https://raginspect.pages.dev/)",
        "```",
        "",
        "---",
        "",
        "## Article 2: Sector 3 (B2B SaaS Unit Economics)",
        "```markdown",
        "---",
        "title: Bootstrapped SaaS Math: Why VC LTV/CAC Metrics Lie to Indie Founders",
        "published: true",
        "tags: saas, startup, entrepreneurship, productivity",
        "canonical_url: https://site-12-taupe.vercel.app/saas-ltv-cac-payback-period-calculator/",
        "---",
        "",
        "# Bootstrapped SaaS Math: The Truth About Payback Periods",
        "",
        "Most venture-backed SaaS advice assumes infinite capital subsidies. For bootstrapped founders, cash flow payback period is the only metric that matters...",
        "",
        "Test your own startup metrics live: [SaaSUnitMath](https://site-12-taupe.vercel.app/)",
        "```",
        "",
        "---",
        "",
        "## Article 3: Sector 4 (Developer Utilities)",
        "```markdown",
        "---",
        "title: Debugging Nginx and AWS Access Logs with Real-Time Grok Patterns",
        "published: true",
        "tags: devops, nginx, docker, observability",
        "canonical_url: https://groklogtester.pages.dev/nginx-access-log-grok-pattern-generator/",
        "---",
        "",
        "# In-Browser Grok Log Parsing Made Simple",
        "",
        "Extracting structured JSON from unstructured Nginx access logs is often frustrating. Here is how constant-time regex patterns can debug logs instantly...",
        "",
        "Test logs live: [GrokLogTester](https://groklogtester.pages.dev/)",
        "```"
    ]

    with open(os.path.join(SYNDICATION_DIR, "devto_canonical_articles.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(devto_lines))

    print(f"SUCCESS: Generated directory and canonical syndication dossiers in {SYNDICATION_DIR}")

if __name__ == "__main__":
    main()
