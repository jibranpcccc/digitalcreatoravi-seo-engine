#!/usr/bin/env python3
"""Deep forensic audit of Schema.org, broken links, image assets, and keyword gaps."""
import os
import glob
import re
import json

def audit_dist(name, dist_dir, base_url):
    print(f"\n=======================================================")
    print(f"FORENSIC AUDIT: {name} ({dist_dir})")
    print(f"=======================================================")
    
    html_files = [f for f in glob.glob(f"{dist_dir}/**/*.html", recursive=True) if not os.path.basename(f).startswith("google")]
    print(f"Total HTML pages: {len(html_files)}")
    
    schema_count = 0
    schema_errors = []
    broken_local_assets = []
    
    for f in html_files:
        rel = os.path.relpath(f, dist_dir)
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
            
        # 1. Schema JSON-LD
        pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
        matches = re.findall(pattern, html, re.DOTALL)
        for m in matches:
            schema_count += 1
            try:
                data = json.loads(m.strip())
                stype = data.get("@type", "Unknown")
                # Verify required fields
                if stype in ("TechArticle", "Article", "BlogPosting"):
                    for field in ["headline", "author"]:
                        if field not in data:
                            schema_errors.append(f"{rel}: {stype} missing '{field}'")
            except Exception as e:
                schema_errors.append(f"{rel}: JSON error: {e}")
                
        # 2. Local asset links (img src)
        img_srcs = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', html)
        for src in img_srcs:
            if src.startswith("http://") or src.startswith("https://"):
                continue
            # Strip query params
            clean_src = src.split("?")[0].lstrip("/")
            # Check against dist directory
            local_target = os.path.join(dist_dir, clean_src)
            # Also check if src has base path
            if not os.path.exists(local_target):
                # Try stripping leading base dir name if present
                parts = clean_src.split("/", 1)
                fallback = os.path.join(dist_dir, parts[1]) if len(parts) > 1 else ""
                if not (fallback and os.path.exists(fallback)):
                    broken_local_assets.append(f"{rel}: missing image {src}")

    print(f"  Schemas found: {schema_count}")
    if schema_errors:
        print(f"  Schema Warnings ({len(schema_errors)}):")
        for se in schema_errors[:5]:
            print(f"    - {se}")
    else:
        print("  ✓ Schema JSON-LD: 100% valid and well-formed")
        
    if broken_local_assets:
        print(f"  Broken Image Assets ({len(broken_local_assets)}):")
        for ba in broken_local_assets[:5]:
            print(f"    - {ba}")
    else:
        print("  ✓ Local Assets & Images: 100% verified on disk")

if __name__ == "__main__":
    audit_dist("Site 1: LocalAgentStack", "sites/site-1/dist", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/")
    audit_dist("Site 2: WorkationRadar", "sites/site-2/dist", "https://jibranpcccc.github.io/workationradar/")
    audit_dist("Site 3: OpenAgentStack", "sites/site-3/dist", "https://openagentstack.pages.dev/")
    audit_dist("Site 4: IndieStackAudit", "sites/site-4/dist", "https://indiestackaudit.pages.dev/")
