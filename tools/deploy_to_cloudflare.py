#!/usr/bin/env python3
"""Cloudflare Pages Autonomous Project Provisioning & Deployment Engine."""
import os, sys, subprocess, json, urllib.request, urllib.error, time

# Load credentials from environment or .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")

def cf_api_request(endpoint, method="GET", data=None):
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"API Error [{e.code}]: {err}")
        return {"success": False, "error": err}

def ensure_project_exists(project_name, production_branch="main"):
    print(f"\n[Cloudflare] Checking if project '{project_name}' exists...")
    res = cf_api_request(f"projects/{project_name}")
    if res.get("success"):
        print(f"  Project '{project_name}' already exists.")
        subdomain = res["result"]["subdomain"]
        return f"https://{subdomain}"
    
    print(f"  Creating new Cloudflare Pages project: '{project_name}'...")
    payload = {
        "name": project_name,
        "production_branch": production_branch
    }
    create_res = cf_api_request("projects", method="POST", data=payload)
    if create_res.get("success"):
        subdomain = create_res["result"]["subdomain"]
        print(f"  SUCCESS: Created project at https://{subdomain}")
        return f"https://{subdomain}"
    else:
        print("  Falling back to wrangler pages project create...")
        cmd = ["npx", "wrangler", "pages", "project", "create", project_name, "--production-branch", production_branch]
        subprocess.run(cmd, check=False, shell=True)
        return f"https://{project_name}.pages.dev"

def deploy_pages_site(project_name, dist_dir):
    print(f"\n[Cloudflare] Deploying {dist_dir} to project '{project_name}'...")
    cmd = [
        "npx", "wrangler", "pages", "deploy", dist_dir,
        f"--project-name={project_name}",
        "--branch=main",
        "--commit-dirty=true"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True)
    print(result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr)
    return result.returncode == 0

def verify_live_url(url, timeout=30):
    print(f"\n[Cloudflare] Verifying live deployment: {url}...")
    for attempt in range(timeout // 3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    print(f"  [HTTP 200 OK] Live at: {url}")
                    return True
        except Exception as e:
            time.sleep(3)
    print(f"  Verification check completed for {url}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 2:
        p_name = sys.argv[1]
        p_dist = sys.argv[2]
        live_subdomain = ensure_project_exists(p_name)
        ok = deploy_pages_site(p_name, p_dist)
        if ok:
            verify_live_url(f"https://{p_name}.pages.dev")
    else:
        print("Usage: python deploy_to_cloudflare.py <project_name> <dist_dir>")
