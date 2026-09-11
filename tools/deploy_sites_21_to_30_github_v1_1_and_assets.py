#!/usr/bin/env python3
"""
Deploy v1.1.0 releases, issue #2 RFCs, and benchmark assets (PDF and RSS)
to GitHub repositories for sites 21-30.
"""

import os
import sys
import json
import base64
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

REPOS_21_30 = [
    {
        "site_id": "site-21",
        "repo": "llm-eval-promptfoo-benchmark",
        "name": "PromptEvalHQ",
        "url": "https://promptevalhq.pages.dev/"
    },
    {
        "site_id": "site-22",
        "repo": "task-queue-memory-benchmark",
        "name": "QueueCost",
        "url": "https://queuecost.pages.dev/"
    },
    {
        "site_id": "site-23",
        "repo": "opentelemetry-tail-sampling-collector",
        "name": "OpenTelemetryLab",
        "url": "https://opentelemetrylab.pages.dev/"
    },
    {
        "site_id": "site-24",
        "repo": "postgres-autovacuum-index-tuner",
        "name": "PostgresScale",
        "url": "https://postgrescale.pages.dev/"
    },
    {
        "site_id": "site-25",
        "repo": "api-gateway-latency-benchmarks",
        "name": "APIGatewayMatrix",
        "url": "https://apigatewaymatrix.pages.dev/"
    },
    {
        "site_id": "site-26",
        "repo": "s3-zero-egress-cost-audit",
        "name": "S3EgressAudit",
        "url": "https://s3egressaudit.pages.dev/"
    },
    {
        "site_id": "site-27",
        "repo": "jwt-paseto-token-security-matrix",
        "name": "AuthTokenAudit",
        "url": "https://authtokenaudit.pages.dev/"
    },
    {
        "site_id": "site-28",
        "repo": "anycast-dns-latency-benchmarks",
        "name": "DNSPerfHQ",
        "url": "https://dnsperf-hq.pages.dev/"
    },
    {
        "site_id": "site-29",
        "repo": "feature-flags-openfeature-tco",
        "name": "FeatureFlagAudit",
        "url": "https://featureflagaudit.pages.dev/"
    },
    {
        "site_id": "site-30",
        "repo": "minimal-docker-base-image-cve",
        "name": "TinyContainerHQ",
        "url": "https://tinycontainerhq.pages.dev/"
    }
]

def upload_binary_file(full_repo, file_path_in_repo, local_file_path):
    if not os.path.exists(local_file_path):
        print(f"  [!] Missing local file: {local_file_path}")
        return False
    with open(local_file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    get_url = f"repos/{full_repo}/contents/{file_path_in_repo}"
    res = subprocess.run(["gh", "api", get_url], capture_output=True, text=True)
    body = {
        "message": f"docs: publish {file_path_in_repo} authoritative asset",
        "content": b64,
        "branch": "main"
    }
    if res.returncode == 0:
        existing = json.loads(res.stdout)
        body["sha"] = existing["sha"]

    put_cmd = ["gh", "api", "--method", "PUT", get_url, "--input", "-"]
    proc = subprocess.run(put_cmd, input=json.dumps(body), capture_output=True, text=True)
    if proc.returncode == 0:
        print(f"  [✓] Uploaded {file_path_in_repo}")
        return True
    else:
        print(f"  [!] Failed to upload {file_path_in_repo}: {proc.stderr[:120]}")
        return False

def deploy_extras(item):
    site_id = item["site_id"]
    repo = item["repo"]
    name = item["name"]
    homepage = item["url"]
    full_repo = f"jibranpcccc/{repo}"

    print(f"\n[*] Processing {full_repo} ({name})...")

    # 1. Upload benchmark-cheatsheet.pdf and rss.xml
    pdf_local = os.path.join(ROOT_DIR, "sites", site_id, "public", "benchmark-cheatsheet.pdf")
    upload_binary_file(full_repo, "benchmark-cheatsheet.pdf", pdf_local)

    rss_local = os.path.join(ROOT_DIR, "sites", site_id, "public", "rss.xml")
    upload_binary_file(full_repo, "rss.xml", rss_local)

    # 2. Create Release v1.1.0
    rel_cmd = [
        "gh", "release", "create", "v1.1.0",
        "--repo", full_repo,
        "--title", f"{name} v1.1.0 Advanced Benchmarks",
        "--notes", f"Production release v1.1.0 featuring advanced empirical benchmarks and models.\nOfficial Web App: {homepage}\n\nFeatures:\n- Advanced empirical calculation models\n- Comprehensive technical guides\n- MIT Licensed"
    ]
    rel_proc = subprocess.run(rel_cmd, capture_output=True, text=True)
    if rel_proc.returncode == 0:
        print(f"  [✓] Created Release v1.1.0")
    else:
        print(f"  [*] Release v1.1.0 notice: {rel_proc.stderr.strip()[:100]}")

    # 3. Create Issue RFC #2
    issue_cmd = [
        "gh", "issue", "create",
        "--repo", full_repo,
        "--title", f"RFC #2: Architecture Spec ({name})",
        "--body", f"RFC #2: Technical Architecture Specification & Benchmark Sizing Methodology for {name}.\n\nExplore live interactive tools and guides at [{homepage}]({homepage})."
    ]
    issue_proc = subprocess.run(issue_cmd, capture_output=True, text=True)
    if issue_proc.returncode == 0:
        print(f"  [✓] Created Issue RFC #2: {issue_proc.stdout.strip()}")
    else:
        print(f"  [*] Issue RFC #2 notice: {issue_proc.stderr.strip()[:100]}")

    time.sleep(1)

def main():
    print("==========================================================================")
    print("DEPLOYING GITHUB v1.1.0 RELEASES, RFC #2 ISSUES & ASSETS FOR SITES 21-30")
    print("==========================================================================\n")
    for item in REPOS_21_30:
        deploy_extras(item)
    print("\n[+] Done deploying GitHub v1.1.0 releases, RFC #2 issues & assets!")

if __name__ == "__main__":
    main()
