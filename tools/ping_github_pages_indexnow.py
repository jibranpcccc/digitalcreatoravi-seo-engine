#!/usr/bin/env python3
"""
Submits all 20 GitHub Pages tool profiles and central hubs to IndexNow (Bing & Yandex).
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

    payload = {
        "host": "jibranpcccc.github.io",
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://jibranpcccc.github.io/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }

    print(f"=== SUBMITTING {len(url_list)} GITHUB PAGES PROFILES TO INDEXNOW ===")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            print(f"[+] IndexNow Response: {res.status} ({res.reason})")
            print(f"[+] Successfully dispatched {len(url_list)} GitHub Pages backlink URLs to Bing & Yandex!")
    except urllib.error.HTTPError as e:
        print(f"[-] IndexNow HTTP Error: {e.code} - {e.reason}")
    except Exception as e:
        print(f"[-] IndexNow Error: {e}")

if __name__ == "__main__":
    main()
