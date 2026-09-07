#!/usr/bin/env python3
"""
Generates valid RSS 2.0 XML feeds (public/rss.xml) for all 20 fleet websites.
Enables instant syndication, crawler discovery, and RSS aggregator backlink distribution.
"""

import os
import sqlite3
from datetime import datetime, timezone

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_rss_for_site(site, pages):
    now_rfc822 = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    items_xml = []
    for p in pages:
        title = p["title"] or site["name"]
        url = p["url"]
        item = f"""    <item>
      <title><![CDATA[{title}]]></title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{now_rfc822}</pubDate>
      <description><![CDATA[Production guide, benchmark analysis, and interactive tools for {site['niche']}.]]></description>
    </item>"""
        items_xml.append(item)
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title><![CDATA[{site['name']} - {site['niche']}]]></title>
    <link>{site['url']}</link>
    <description><![CDATA[Empirical benchmarks, interactive client-side developer utilities, and comprehensive guides for {site['niche']}.]]></description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{site['url'].rstrip('/')}/rss.xml" rel="self" type="application/rss+xml" />
{chr(10).join(items_xml)}
  </channel>
</rss>
"""
    return rss_content

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM indexed_pages ORDER BY site_id, id")
    all_pages = [dict(r) for r in cursor.fetchall()]
    conn.close()

    count = 0
    for s in sites:
        site_id = s["id"]
        site_dir = os.path.join(ROOT_DIR, "sites", site_id)
        if not os.path.exists(site_dir):
            continue
        
        public_dir = os.path.join(site_dir, "public")
        os.makedirs(public_dir, exist_ok=True)
        
        site_pages = [p for p in all_pages if p["site_id"] == site_id]
        rss_text = generate_rss_for_site(s, site_pages)
        
        rss_path = os.path.join(public_dir, "rss.xml")
        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(rss_text)
        
        # Also copy to dist if dist exists
        dist_dir = os.path.join(site_dir, "dist")
        if os.path.exists(dist_dir):
            with open(os.path.join(dist_dir, "rss.xml"), "w", encoding="utf-8") as f:
                f.write(rss_text)
                
        count += 1
        print(f"Generated RSS 2.0 feed for {s['name']} ({site_id}) with {len(site_pages)} items.")

    print(f"\nSUCCESS: Generated {count}/20 RSS feeds across the portfolio.")

if __name__ == "__main__":
    main()
