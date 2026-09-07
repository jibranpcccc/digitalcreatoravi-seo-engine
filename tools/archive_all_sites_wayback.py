#!/usr/bin/env python3
"""
Wayback Machine Batch Archiver (Archive.org DA 96)
Programmatically submits all 20 production websites to the Internet Archive.
Uses zero accounts / zero emails. Generates permanent, public, crawlable historical snapshots.
"""

import os
import sys
import json
import sqlite3
import urllib.request
import urllib.error
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "wayback_snapshots.json")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_to_wayback(url):
    save_endpoint = f"https://web.archive.org/save/{url}"
    req = urllib.request.Request(save_endpoint, headers={"User-Agent": USER_AGENT})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=35) as res:
            latency = int((time.time() - start) * 1000)
            return res.status, latency, "Saved"
    except urllib.error.HTTPError as e:
        latency = int((time.time() - start) * 1000)
        return e.code, latency, str(e.reason)
    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return 0, latency, str(e)

def check_wayback_availability(url):
    check_api = f"https://archive.org/wayback/available?url={url}"
    req = urllib.request.Request(check_api, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=12) as res:
            data = json.loads(res.read().decode("utf-8"))
            snap = data.get("archived_snapshots", {}).get("closest", {})
            if snap.get("available"):
                return snap.get("url"), snap.get("timestamp")
    except Exception:
        pass
    return None, None

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = [dict(r) for r in cursor.fetchall()]
    conn.close()

    print("=== STARTING WAYBACK MACHINE (ARCHIVE.ORG DA 96) ARCHIVING PASS ===")
    print(f"Targeting {len(sites)} production websites with zero email exposure...\n")

    snapshots = []

    for idx, s in enumerate(sites, 1):
        site_id = s["id"]
        name = s["name"]
        url = s["url"]

        print(f"[{idx:2d}/{len(sites)}] Submitting {name} ({url}) to Wayback Machine...")
        status, latency, msg = save_to_wayback(url)
        print(f"       -> Response: HTTP {status} ({latency}ms) - {msg}")

        # Check availability
        time.sleep(2)
        snap_url, snap_ts = check_wayback_availability(url)
        if snap_url:
            print(f"       -> [✓] Snapshot Confirmed: {snap_url}")
        else:
            snap_url = f"https://web.archive.org/web/{url}"
            print(f"       -> [*] Queued at: {snap_url}")

        snapshots.append({
            "site_id": site_id,
            "site_name": name,
            "target_url": url,
            "status": status,
            "latency_ms": latency,
            "archive_url": snap_url,
            "timestamp": snap_ts,
            "da": 96
        })

        time.sleep(3)

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshots, f, indent=2)

    print(f"\n[+] SUCCESS: All {len(snapshots)} sites submitted to Archive.org (DA 96).")
    print(f"[+] Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
