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
import concurrent.futures

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

def ping_worker(item):
    brand = item["Brand Name"]
    backlink_url = item["Live Backlink URL"]
    tier = item["Platform Tier"]
    title = f"{brand} - {tier}"
    blogs_ok, blogs_msg = ping_blogs(title, backlink_url)
    twingly_ok, twingly_msg = ping_twingly(title, backlink_url)
    return {
        "brand": brand,
        "url": backlink_url,
        "tier": tier,
        "blogs": {"success": blogs_ok, "msg": blogs_msg},
        "twingly": {"success": twingly_ok, "msg": twingly_msg}
    }

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

    targets = [b for b in all_backlinks if any(t.lower() in b.get("Platform Tier", "").lower() for t in [
        "github", "raw cdn", "google colab", "rentry", "dpaste", "cl1p", "paste.rs", "tinyurl", "cleanuri", "ulvis", "jsdelivr", "statically", "wayback"
    ])]

    print(f"Selected {len(targets)} authority backlink targets for concurrent broadcast...", flush=True)

    telemetry = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(ping_worker, item) for item in targets]
        for idx, f in enumerate(concurrent.futures.as_completed(futures), 1):
            res = f.result()
            telemetry.append(res)
            if idx % 50 == 0 or idx == len(targets):
                print(f"  [{idx:3d}/{len(targets)}] Broadcasted: {res['url']} ({res['brand']})", flush=True)

    out_json = os.path.join(ROOT_DIR, "data", "backlinks_xmlrpc_telemetry.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    print("\n==========================================================================")
    print(f"Finished broadcasting XML-RPC pings for {len(targets)} authority backlink hubs!")
    print(f"Telemetry saved to: {out_json}")
    print("==========================================================================")

if __name__ == "__main__":
    main()
