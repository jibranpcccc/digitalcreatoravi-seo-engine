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

    target_tiers = [
        "GitHub Repository (DA 96)",
        "GitHub Pages Profile (DA 96)",
        "GitHub Profile (DA 96)",
        "GitHub Pages (DA 96)",
        "GitHub Pages Root (DA 96)"
    ]
    targets = [b for b in all_backlinks if b["Platform Tier"] in target_tiers]

    print("==========================================================================")
    print(f"BROADCASTING XML-RPC PINGS FOR {len(targets)} HIGH-DA BACKLINK HUBS")
    print("==========================================================================\n")

    telemetry = []

    for idx, item in enumerate(targets, 1):
        brand = item["Brand Name"]
        backlink_url = item["Live Backlink URL"]
        tier = item["Platform Tier"]
        title = f"{brand} - {tier}"

        print(f"[{idx:2d}/{len(targets)}] Pinging: {backlink_url} ({brand})")

        blogs_ok, blogs_msg = ping_blogs(title, backlink_url)
        print(f"       -> Blo.gs  : {'OK' if blogs_ok else 'ERR'} - {blogs_msg}")

        twingly_ok, twingly_msg = ping_twingly(title, backlink_url)
        print(f"       -> Twingly : {'OK' if twingly_ok else 'ERR'} - {twingly_msg}")

        telemetry.append({
            "brand": brand,
            "url": backlink_url,
            "tier": tier,
            "blogs": {"success": blogs_ok, "msg": blogs_msg},
            "twingly": {"success": twingly_ok, "msg": twingly_msg}
        })

        time.sleep(0.5)

    out_json = os.path.join(ROOT_DIR, "data", "backlinks_xmlrpc_telemetry.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    print("\n==========================================================================")
    print(f"Finished broadcasting XML-RPC pings for {len(targets)} backlink hubs!")
    print(f"Telemetry saved to: {out_json}")
    print("==========================================================================")

if __name__ == "__main__":
    main()
