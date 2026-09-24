#!/usr/bin/env python3
"""
Autonomous Cloudflare Pages Fleet Deployment & Verification Engine
Provisions and deploys sites 6, 7, 9, 12, 14, 15, 16, 18, 19 to Cloudflare Pages
ensuring 100% HTTP 200 OK on Google Search Console HTML verification and IndexNow.
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Load credentials from .env
if os.path.exists(os.path.join(ROOT_DIR, ".env")):
    with open(os.path.join(ROOT_DIR, ".env"), "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")

HEADERS_CF = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}
HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

TARGET_SITES = [
    {"site_id": "site-6", "project_name": "nomadtreaty", "dir": "sites/site-6"},
    {"site_id": "site-7", "project_name": "webhookwatch", "dir": "sites/site-7"},
    {"site_id": "site-9", "project_name": "founderrunway", "dir": "sites/site-9"},
    {"site_id": "site-12", "project_name": "saasunitmath", "dir": "sites/site-12"},
    {"site_id": "site-14", "project_name": "soc2ready", "dir": "sites/site-14"},
    {"site_id": "site-15", "project_name": "eorcalculator", "dir": "sites/site-15"},
    {"site_id": "site-16", "project_name": "devconfighub", "dir": "sites/site-16"},
    {"site_id": "site-18", "project_name": "cipipelinegraph", "dir": "sites/site-18"},
    {"site_id": "site-19", "project_name": "greekvisualizer", "dir": "sites/site-19"},
]

def ensure_cf_project(name):
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects"
    # Check if exists
    get_req = urllib.request.Request(f"{url}/{name}", headers=HEADERS_CF)
    try:
        with urllib.request.urlopen(get_req) as resp:
            data = json.loads(resp.read().decode())
            if data.get("success"):
                print(f"  [Cloudflare] Project '{name}' already exists.")
                return True
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"  [Cloudflare] Warning checking '{name}': {e}")

    # Create project
    print(f"  [Cloudflare] Creating project '{name}'...")
    payload = json.dumps({"name": name, "production_branch": "main"}).encode()
    post_req = urllib.request.Request(url, data=payload, headers=HEADERS_CF, method="POST")
    try:
        with urllib.request.urlopen(post_req) as resp:
            data = json.loads(resp.read().decode())
            if data.get("success"):
                print(f"  [Cloudflare] Successfully created project '{name}'.")
                return True
            else:
                print(f"  [Cloudflare] Failed to create '{name}': {data}")
                return False
    except Exception as e:
        print(f"  [Cloudflare] Error creating '{name}': {e}")
        return False

def build_site(site_dir):
    full_path = os.path.join(ROOT_DIR, site_dir)
    print(f"  [Build] Building Astro static site in {site_dir}...")
    res = subprocess.run("npm run build", cwd=full_path, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  [Build] ✓ Astro build successful.")
        return True
    else:
        print(f"  [Build] ✗ Build error: {res.stderr[:300]}")
        return False

def deploy_to_cf(site_dir, project_name):
    dist_dir = os.path.join(ROOT_DIR, site_dir, "dist")
    print(f"  [Deploy] Deploying {dist_dir} to {project_name}.pages.dev...")
    cmd = f"npx wrangler pages deploy {dist_dir} --project-name={project_name} --branch=main --commit-dirty=true"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode == 0:
        print(f"  [Deploy] ✓ Successfully deployed to {project_name}.pages.dev.")
        return True
    else:
        err_msg = err.decode("utf-8", errors="replace")[:300]
        print(f"  [Deploy] ✗ Deploy error (code {p.returncode}): {err_msg}")
        return False

def verify_live(project_name):
    base = f"https://{project_name}.pages.dev"
    tests = {
        "Root": f"{base}/",
        "GSC HTML": f"{base}/google6fe267a998c19a9a.html",
        "IndexNow": f"{base}/8303260f1bf94264ac6d00aa93efde28.txt",
        "Sitemap": f"{base}/sitemap.xml",
        "Robots": f"{base}/robots.txt"
    }
    print(f"  [Verify] Probing live edge endpoints for {base}...")
    statuses = {}
    time.sleep(2)
    for name, u in tests.items():
        try:
            req = urllib.request.Request(u, headers=HEADERS_BROWSER)
            with urllib.request.urlopen(req, timeout=8) as r:
                code = r.status
                statuses[name] = code
        except Exception as e:
            statuses[name] = str(e)
        print(f"    - {name:10}: {statuses[name]}")
    return statuses

def main():
    print("=================================================================")
    print("AUTONOMOUS CLOUDFLARE PAGES FLEET PROVISIONING & DEPLOYMENT")
    print("=================================================================\n")
    
    summary = []
    for s in TARGET_SITES:
        sid = s["site_id"]
        pname = s["project_name"]
        sdir = s["dir"]
        print(f"\n>>> Processing {sid} ({pname}) <<<")
        
        # 1. Project exists
        proj_ok = ensure_cf_project(pname)
        
        # 2. Build site
        build_ok = build_site(sdir)
        
        # 3. Deploy
        deploy_ok = False
        if proj_ok and build_ok:
            deploy_ok = deploy_to_cf(sdir, pname)
            
        # 4. Verify
        statuses = verify_live(pname) if deploy_ok else {}
        summary.append({
            "site_id": sid,
            "project_name": pname,
            "deploy_ok": deploy_ok,
            "statuses": statuses
        })
        time.sleep(2)

    print("\n=================================================================")
    print("DEPLOYMENT & VERIFICATION SUMMARY REPORT")
    print("=================================================================")
    all_ok = True
    for item in summary:
        st = item["statuses"]
        gsc = st.get("GSC HTML", "N/A")
        inow = st.get("IndexNow", "N/A")
        print(f"{item['site_id']:7} | {item['project_name']:16} | Deploy: {'OK' if item['deploy_ok'] else 'FAIL'} | GSC: {gsc} | IndexNow: {inow}")
        if gsc != 200 or inow != 200:
            all_ok = False
            
    print(f"\nFinal Edge Parity Result: {'100% PERFECT PARITY ACHIEVED' if all_ok else 'SOME EDGES REQUIRE ATTENTION'}")

if __name__ == "__main__":
    main()
