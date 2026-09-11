#!/usr/bin/env python3
"""
XML-RPC Fast Indexing Broadcaster for All 266 Master Backlinks
Broadcasts XML-RPC ping signals across Blo.gs and Twingly networks
for all 266 verified live backlinks in reports/MASTER_LIVE_BACKLINKS_REPORT.csv.
"""

import os
import csv
import time
import socket
import xmlrpc.client
import json

socket.setdefaulttimeout(12.0)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(ROOT_DIR, "reports", "MASTER_LIVE_BACKLINKS_REPORT.csv")

BLOGS_ENDPOINT = "http://ping.blo.gs/"
TWINGLY_ENDPOINT = "http://rpc.twingly.com/"

def ping_blogs(title, url):
    try:
        server = xmlrpc.client.ServerProxy(BLOGS_ENDPOINT)
        res = server.weblogUpdates.ping(title, url)
        return True, res.get("message", "Succeeded")
    except Exception as e:
        return False, str(e)

def ping_twingly(title, url):
    try:
        server = xmlrpc.client.ServerProxy(TWINGLY_ENDPOINT)
        res = server.weblogUpdates.ping(title, url)
        return True, res.get("message", "Thanks for the ping.")
    except Exception as e:
        return False, str(e)

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_backlinks = list(reader)

    print("==========================================================================")
    print(f"BROADCASTING XML-RPC PINGS ACROSS {len(all_backlinks)} LIVE BACKLINKS")
    print("==========================================================================\n")

    telemetry = []

    # Filter to high-priority hubs: Repos, Releases, Issues, Gists, Pages, CDNs
    high_priority_tiers = [
        "GitHub Repository (DA 96)",
        "GitHub Release v1.0 (DA 96)",
        "GitHub Release v1.1 (DA 96)",
        "GitHub Issue #1 (DA 96)",
        "GitHub Issue #2 RFC (DA 96)",
        "GitHub Gist Wave 1 (DA 96)",
        "GitHub Gist Wave 2 (DA 96)",
        "GitHub Pages Profile (DA 96)",
        "GitHub Pages Benchmark Hub (DA 96)",
        "GitHub Raw CDN Docs (DA 96)",
        "GitHub Raw CDN Benchmarks (DA 96)",
        "GitHub Profile (DA 96)",
        "GitHub Pages (DA 96)",
        "GitHub Pages Root (DA 96)"
    ]
    targets = [b for b in all_backlinks if any(t in b.get("Platform Tier", "") for t in ["GitHub", "Raw CDN", "Google Colab"])]

    print(f"Selected {len(targets)} authority backlink targets for immediate broadcast...")

    for idx, item in enumerate(targets, 1):
        brand = item["Brand Name"]
        backlink_url = item["Live Backlink URL"]
        tier = item["Platform Tier"]
        title = f"{brand} - {tier}"

        print(f"[{idx:3d}/{len(targets)}] Pinging: {backlink_url} ({brand})")

        blogs_ok, blogs_msg = ping_blogs(title, backlink_url)
        twingly_ok, twingly_msg = ping_twingly(title, backlink_url)

        telemetry.append({
            "brand": brand,
            "url": backlink_url,
            "tier": tier,
            "blogs": {"success": blogs_ok, "msg": blogs_msg},
            "twingly": {"success": twingly_ok, "msg": twingly_msg}
        })

        time.sleep(0.2)

    out_json = os.path.join(ROOT_DIR, "data", "backlinks_xmlrpc_telemetry.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    print("\n==========================================================================")
    print(f"Finished broadcasting XML-RPC pings for {len(targets)} authority backlink hubs!")
    print(f"Telemetry saved to: {out_json}")
    print("==========================================================================")

if __name__ == "__main__":
    main()
