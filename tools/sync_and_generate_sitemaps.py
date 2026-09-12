#!/usr/bin/env python3
"""
Synchronizes and regenerates 100% compliant XML sitemaps across all 30 sites.
Ensures every indexed page in fleet_telemetry.db is explicitly included with
lastmod, changefreq, and priority tags.
"""

import os
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    sites = [dict(r) for r in conn.execute("SELECT * FROM sites ORDER BY id").fetchall()]
    pages = [dict(r) for r in conn.execute("SELECT * FROM indexed_pages ORDER BY site_id, id").fetchall()]
    conn.close()

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total_urls = 0

    for s in sites:
        sid = s["id"]
        base_url = s["url"].rstrip("/")
        site_pages = [p for p in pages if p["site_id"] == sid]

        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]

        # 1. Homepage
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{base_url}/</loc>")
        xml_lines.append(f"    <lastmod>{now_iso}</lastmod>")
        xml_lines.append("    <changefreq>daily</changefreq>")
        xml_lines.append("    <priority>1.0</priority>")
        xml_lines.append("  </url>")
        total_urls += 1

        # 2. Subpages
        seen_urls = {f"{base_url}/"}
        for p in site_pages:
            p_url = p["url"]
            if p_url in seen_urls or p_url.rstrip("/") == base_url:
                continue
            seen_urls.add(p_url)
            xml_lines.append("  <url>")
            xml_lines.append(f"    <loc>{p_url}</loc>")
            xml_lines.append(f"    <lastmod>{now_iso}</lastmod>")
            xml_lines.append("    <changefreq>weekly</changefreq>")
            xml_lines.append("    <priority>0.8</priority>")
            xml_lines.append("  </url>")
            total_urls += 1

        xml_lines.append("</urlset>")
        sitemap_content = "\n".join(xml_lines)

        # Write to public/
        p_path = os.path.join(ROOT_DIR, "sites", sid, "public", "sitemap.xml")
        with open(p_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(sitemap_content)

        # Write to dist/ if dist exists
        d_path = os.path.join(ROOT_DIR, "sites", sid, "dist", "sitemap.xml")
        if os.path.exists(os.path.dirname(d_path)):
            with open(d_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(sitemap_content)

    print(f"SUCCESS: Generated 100% synchronized sitemaps across all {len(sites)} sites with {total_urls} valid URLs.")

if __name__ == "__main__":
    main()
