#!/usr/bin/env python3
"""
Updates sitemap-tools.xml on jibranpcccc/jibranpcccc.github.io
to include all 20 dedicated benchmark landing pages alongside existing tools.
"""

import os
import sys
import json
import base64
import subprocess

REPOS_CONFIG = [
    {"site_id": "site-1", "slug": "localagentstack"},
    {"site_id": "site-2", "slug": "workationradar"},
    {"site_id": "site-3", "slug": "openagentstack"},
    {"site_id": "site-4", "slug": "indiestackaudit"},
    {"site_id": "site-5", "slug": "vectorbench"},
    {"site_id": "site-6", "slug": "nomadtreaty"},
    {"site_id": "site-7", "slug": "webhookwatch"},
    {"site_id": "site-8", "slug": "localdocprivacy"},
    {"site_id": "site-9", "slug": "founderrunway"},
    {"site_id": "site-10", "slug": "raginspect"},
    {"site_id": "site-11", "slug": "nomadpassportindex"},
    {"site_id": "site-12", "slug": "saasunitmath"},
    {"site_id": "site-13", "slug": "groklogtester"},
    {"site_id": "site-14", "slug": "soc2ready"},
    {"site_id": "site-15", "slug": "eorcalculator"},
    {"site_id": "site-16", "slug": "devconfighub"},
    {"site_id": "site-17", "slug": "opencrmstack"},
    {"site_id": "site-18", "slug": "cipipelinegraph"},
    {"site_id": "site-19", "slug": "greekvisualizer"},
    {"site_id": "site-20", "slug": "edgeruntimehq"}
]

def update_sitemap():
    repo_full = "jibranpcccc/jibranpcccc.github.io"
    path = "sitemap-tools.xml"
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url><loc>https://jibranpcccc.github.io/tools.html</loc><changefreq>daily</changefreq><priority>1.0</priority></url>',
        '  <url><loc>https://jibranpcccc.github.io/api/v1/tools.json</loc><changefreq>daily</changefreq><priority>0.9</priority></url>'
    ]
    
    # 20 Tools pages
    for item in REPOS_CONFIG:
        url = f"https://jibranpcccc.github.io/tools/{item['site_id']}-{item['slug']}.html"
        xml_lines.append(f"  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
        
    # 20 Benchmark pages
    for item in REPOS_CONFIG:
        url = f"https://jibranpcccc.github.io/benchmarks/{item['site_id']}-{item['slug']}.html"
        xml_lines.append(f"  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.85</priority></url>")
        
    xml_lines.append('</urlset>')
    sitemap_xml = "\n".join(xml_lines)
    
    content_b64 = base64.b64encode(sitemap_xml.encode("utf-8")).decode("ascii")
    
    # Fetch SHA
    res = subprocess.run(["gh", "api", f"repos/{repo_full}/contents/{path}"], capture_output=True, text=True)
    sha = None
    if res.returncode == 0:
        data = json.loads(res.stdout)
        sha = data.get("sha")
        
    payload = {
        "message": "Update sitemap-tools.xml with 20 new benchmark landing pages",
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
        print(" -> SUCCESS: Updated sitemap-tools.xml with 42 URLs!")
    else:
        print(f" -> ERROR: {res.stderr}")

if __name__ == "__main__":
    update_sitemap()
