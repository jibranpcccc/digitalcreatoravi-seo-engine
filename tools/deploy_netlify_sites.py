#!/usr/bin/env python3
"""
Deploys site-8 and site-11 to Netlify using their specific Netlify Site UUIDs.
"""

import os
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

NETLIFY_SITES = [
    ("site-8", "344533ec-75ca-41a7-9d5f-cab3f5ef014c", "localdocprivacy"),
    ("site-11", "feeee3df-9c28-4de6-929d-7d102ad148b4", "nomadpassportindex")
]

def main():
    for site, site_uuid, name in NETLIFY_SITES:
        site_path = os.path.join(ROOT_DIR, "sites", site)
        print(f"\n--- Deploying {site} ({name}) to Netlify (ID: {site_uuid}) ---")
        cmd = f"netlify deploy --prod --dir dist --site {site_uuid}"
        res = subprocess.run(cmd, cwd=site_path, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[+] Successfully deployed {site} to Netlify!")
        else:
            print(f"[-] Deploy error for {site}:\n{res.stderr[:300]}")
        time.sleep(1)

if __name__ == "__main__":
    main()
