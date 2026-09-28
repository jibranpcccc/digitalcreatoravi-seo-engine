#!/usr/bin/env python3
"""
Autonomous Wayback Machine (Archive.org) Fast-Indexing & Archival Dispatcher
Submits all 20 production homepages and primary guide URLs to the Internet Archive (DA 98+)
triggering external crawler discovery and permanent archival backlinks.
"""

import os
import time
import urllib.request
import urllib.error
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def submit_to_wayback(url):
    save_url = f"https://web.archive.org/save/{url}"
    req = urllib.request.Request(save_url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, "Archived Successfully"
    except urllib.error.HTTPError as e:
        if e.code in [302, 301]:
            return 200, "Archived (Redirected to snapshot)"
        return e.code, str(e.reason)
    except Exception as e:
        return 0, str(e)

def main():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM sites WHERE CAST(SUBSTR(id, 6) AS INTEGER) BETWEEN 1 AND 20 ORDER BY CAST(SUBSTR(id, 6) AS INTEGER)")
    sites = [dict(r) for r in c.fetchall()]
    conn.close()

    print("==========================================================================")
    print("🏛️ WAYBACK MACHINE (ARCHIVE.ORG DA 98) RAPID INDEXING DISPATCHER")
    print(f"Submitting 20 Production Properties to Internet Archive...")
    print("==========================================================================\n")

    success_count = 0
    for idx, s in enumerate(sites, 1):
        target_url = s["url"].rstrip("/") + "/"
        name = s["name"]
        print(f"[{idx:2d}/20] Archiving {name} ({target_url})...", end=" ", flush=True)
        status, msg = submit_to_wayback(target_url)
        if status in [200, 302, 301]:
            print(f"-> 🟢 HTTP {status} ({msg})")
            success_count += 1
        else:
            print(f"-> 🟡 HTTP {status} ({msg})")
        time.sleep(2)  # Respect rate limits

    print("\n==========================================================================")
    print(f"✅ Archival pass complete: {success_count}/{len(sites)} sites submitted to Archive.org.")
    print("==========================================================================")

if __name__ == "__main__":
    main()
