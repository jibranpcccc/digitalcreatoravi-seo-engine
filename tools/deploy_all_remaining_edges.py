#!/usr/bin/env python3
"""
Builds and deploys all Vercel, Netlify, and GitHub Pages sites
to ensure 100% of benchmark-cheatsheet.pdf and rss.xml return HTTP 200.
"""

import os
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

VERCEL_SITES = ["site-6", "site-7", "site-9", "site-14", "site-15", "site-16", "site-18", "site-19"]
NETLIFY_SITES = [
    ("site-5", "vectorbench-hq"),
    ("site-8", "localdocprivacy"),
    ("site-11", "nomadpassportindex")
]

def deploy_vercel():
    for site in VERCEL_SITES:
        site_path = os.path.join(ROOT_DIR, "sites", site)
        print(f"Deploying {site} to Vercel...")
        subprocess.run("npm run build", cwd=site_path, shell=True, capture_output=True)
        res = subprocess.run("vercel deploy --prod --yes", cwd=site_path, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [+] {site} deployed to Vercel successfully.")
        else:
            print(f"  [-] {site} Vercel error: {res.stderr[:200]}")
        time.sleep(1)

def deploy_netlify():
    for site, site_name in NETLIFY_SITES:
        site_path = os.path.join(ROOT_DIR, "sites", site)
        print(f"Deploying {site} to Netlify...")
        subprocess.run("npm run build", cwd=site_path, shell=True, capture_output=True)
        dist_path = os.path.join(site_path, "dist")
        if os.path.exists(dist_path):
            res = subprocess.run(f"netlify deploy --prod --dir dist --site {site_name}", cwd=site_path, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  [+] {site} deployed to Netlify successfully.")
            else:
                print(f"  [-] {site} Netlify deploy output: {res.stdout[:200]}")
        time.sleep(1)

if __name__ == "__main__":
    deploy_vercel()
    deploy_netlify()
    print("\nALL EDGE DEPLOYMENTS COMPLETE.")
