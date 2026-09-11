#!/usr/bin/env python3
"""
Submits all GitHub Pages tool profiles, benchmark landing pages, and central hubs
to Microsoft Bing and Central IndexNow (Yandex, Seznam, Naver).
"""

import os
import sys
import json
import sqlite3
import urllib.request

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")
INDEXNOW_KEY = "8303260f1bf94264ac6d00aa93efde28"

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, name FROM sites ORDER BY id")
    sites = [dict(r) for r in c.fetchall()]
    conn.close()

    url_list = [
        "https://jibranpcccc.github.io/tools.html",
        "https://jibranpcccc.github.io/api/v1/tools.json",
        "https://jibranpcccc.github.io/sitemap-tools.xml"
    ]

    for s in sites:
        slug = f"{s['id']}-{s['name'].lower()}"
        url_list.append(f"https://jibranpcccc.github.io/tools/{slug}.html")
        url_list.append(f"https://jibranpcccc.github.io/benchmarks/{slug}.html")

    payload = {
        "host": "jibranpcccc.github.io",
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://jibranpcccc.github.io/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }

    print(f"=== SUBMITTING {len(url_list)} GITHUB PAGES AUTHORITY URLS TO INDEXNOW ===")
    
    # 1. Bing IndexNow
    try:
        req_bing = urllib.request.Request(
            "https://www.bing.com/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_bing, timeout=15) as res:
            print(f"[+] Microsoft Bing IndexNow: HTTP {res.status} ({res.reason})")
    except Exception as e:
        print(f"[-] Bing IndexNow Notice: {e}")

    # 2. Central IndexNow (Yandex, Seznam, Naver)
    try:
        req_central = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_central, timeout=15) as res:
            print(f"[+] Central IndexNow: HTTP {res.status} ({res.reason})")
            print(f"[+] Successfully dispatched {len(url_list)} GitHub Pages URLs to Bing, Yandex & Global IndexNow!")
    except Exception as e:
        print(f"[-] Central IndexNow Notice: {e}")

if __name__ == "__main__":
    main()
