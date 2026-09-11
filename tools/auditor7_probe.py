import urllib.request
import time
import sqlite3
import os
import csv
import json

sites = [
    ("Site 13 (GrokLogTester)", "https://groklogtester.pages.dev/"),
    ("Site 14 (SOC2Ready)", "https://site-14-sable.vercel.app/")
]

print("=" * 70)
print("1. PROBING LIVE URLS, ROBOTS.TXT, AND SITEMAP.XML")
print("=" * 70)

for name, base_url in sites:
    print(f"\n>>> Probing {name}: {base_url}")
    for endpoint in ["", "robots.txt", "sitemap.xml"]:
        url = base_url + endpoint
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Auditor7-SEO/1.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                ttfb = (time.time() - t0) * 1000
                status = resp.status
                headers = dict(resp.getheaders())
                body = resp.read()
                print(f"  URL: {url}")
                print(f"    Status: HTTP {status} OK | TTFB: {ttfb:.2f}ms | Size: {len(body)} bytes | Server: {headers.get('server', 'Unknown')}")
                if endpoint == "robots.txt":
                    print(f"    Content Preview:\n{body.decode('utf-8', errors='ignore')[:300].strip()}")
                elif endpoint == "sitemap.xml":
                    text = body.decode('utf-8', errors='ignore')
                    urls = [line.strip() for line in text.splitlines() if "<loc>" in line]
                    print(f"    Sitemap URLs ({len(urls)} found):")
                    for u in urls[:6]:
                        print(f"      - {u.replace('<loc>', '').replace('</loc>', '')}")
                    if len(urls) > 6:
                        print(f"      ... and {len(urls)-6} more")
        except urllib.error.HTTPError as e:
            ttfb = (time.time() - t0) * 1000
            print(f"  URL: {url} -> HTTP Error {e.code}: {e.reason} | TTFB: {ttfb:.2f}ms")
        except Exception as e:
            ttfb = (time.time() - t0) * 1000
            print(f"  URL: {url} -> Exception: {e} | TTFB: {ttfb:.2f}ms")

print("\n" + "=" * 70)
print("2. FLEET TELEMETRY DATABASE (data/fleet_telemetry.db)")
print("=" * 70)

db_path = "data/fleet_telemetry.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("\n--- Site 13 & 14 in search_queries ---")
cur.execute("SELECT id, site_id, query, page_url, impressions, clicks, ctr, position, last_updated FROM search_queries WHERE site_id IN ('site-13', 'site-14') ORDER BY site_id, id")
queries = cur.fetchall()
print(f"Total search_queries tracked for site-13 & site-14: {len(queries)}")
for q in queries:
    print(f"  [{q[1]}] ID: {q[0]} | Query: '{q[2]}' | Page: {q[3]} | Impr: {q[4]} | Clicks: {q[5]} | CTR: {q[6]} | Pos: {q[7]} | Updated: {q[8]}")

target_queries = [
    "HAProxy grok regex extractor",
    "SOC 2 CC6.3 access reviews",
    "Vanta vs Drata",
    "haproxy",
    "grok",
    "soc 2",
    "cc6.3",
    "vanta",
    "drata"
]
print("\n--- Cross-check target query keywords across all search_queries ---")
for term in target_queries:
    cur.execute("SELECT site_id, query, page_url, impressions, clicks, ctr, position, last_updated FROM search_queries WHERE query LIKE ?", (f"%{term}%",))
    matches = cur.fetchall()
    print(f"Keyword/Query '{term}': {len(matches)} matches")
    for m in matches:
        print(f"    Site: {m[0]} | Query: '{m[1]}' | Impr: {m[3]} | Clicks: {m[4]} | CTR: {m[5]} | Pos: {m[6]} | Updated: {m[7]}")

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
for t in tables:
    if t not in ['search_queries', 'fleet_alerts', 'synced_event_ids']:
        try:
            cur.execute(f"SELECT * FROM {t} WHERE site_id IN ('site-13', 'site-14')")
            rows = cur.fetchall()
            if rows:
                print(f"\n--- Found {len(rows)} rows in table '{t}' for site-13 / site-14 ---")
                for r in rows[:5]:
                    print(" ", r)
        except Exception as e:
            pass

conn.close()

print("\n" + "=" * 70)
print("3. MASTER BACKLINKS REPORT (reports/MASTER_LIVE_BACKLINKS_REPORT.csv)")
print("=" * 70)

csv_path = "reports/MASTER_LIVE_BACKLINKS_REPORT.csv"
site13_bl = []
site14_bl = []
with open(csv_path, mode="r", encoding="utf-8-sig", errors="ignore") as f:
    reader = csv.DictReader(f)
    for row in reader:
        s_id = row.get("Site ID", "").strip()
        if s_id == "site-13":
            site13_bl.append(row)
        elif s_id == "site-14":
            site14_bl.append(row)

def summarize_backlinks(site_label, bl_list):
    print(f"\n>>> {site_label} (Total: {len(bl_list)} backlinks)")
    platforms = {}
    statuses = {}
    verified_count = 0
    for r in bl_list:
        p = r.get("Platform Tier", "Unknown")
        platforms[p] = platforms.get(p, 0) + 1
        s = r.get("HTTP Status", "Unknown")
        statuses[s] = statuses.get(s, 0) + 1
        if r.get("Live Verified") == "YES":
            verified_count += 1
    print(f"  Platform Breakdown: {platforms}")
    print(f"  HTTP Status Breakdown: {statuses} | Verified YES: {verified_count}/{len(bl_list)}")
    for idx, r in enumerate(bl_list, 1):
        print(f"  {idx}. [{r.get('Platform Tier')}] DA: {r.get('Domain Authority (DA)')} | Status: {r.get('HTTP Status')} ({r.get('Latency (ms)')}ms) | Verified: {r.get('Live Verified')}")
        print(f"     Live URL: {r.get('Live Backlink URL')}")
        print(f"     Target:   {r.get('Target Destination URL')}")
        print(f"     Anchor/Context:  {r.get('Link Placement / Anchor Context')}")

summarize_backlinks("Site 13 (GrokLogTester)", site13_bl)
summarize_backlinks("Site 14 (SOC2Ready)", site14_bl)
