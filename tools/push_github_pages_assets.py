#!/usr/bin/env python3
"""
Pushes benchmark-cheatsheet.pdf and rss.xml to jibranpcccc/workationradar
and jibranpcccc/digitalcreatoravi-seo-engine via gh api so they return 200 on GitHub Pages.
"""

import os
import json
import base64
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def upload_file(repo, file_path_repo, local_file_path):
    with open(local_file_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "message": f"feat: add {os.path.basename(file_path_repo)}",
        "content": content_b64,
        "branch": "master"
    }

    # Check sha
    check_cmd = ["gh", "api", f"/repos/{repo}/contents/{file_path_repo}?ref=master"]
    check_res = subprocess.run(check_cmd, capture_output=True, text=True)
    if check_res.returncode == 0:
        try:
            payload["sha"] = json.loads(check_res.stdout).get("sha")
        except Exception:
            pass

    put_cmd = ["gh", "api", "--method", "PUT", f"/repos/{repo}/contents/{file_path_repo}", "--input", "-"]
    res = subprocess.run(put_cmd, input=json.dumps(payload), text=True, capture_output=True)
    if res.returncode == 0:
        print(f"[+] Successfully uploaded to {repo}/{file_path_repo}")
    else:
        print(f"[-] Error uploading to {repo}/{file_path_repo}: {res.stderr}")

def main():
    # Site 2: workationradar
    site2_pdf = os.path.join(ROOT_DIR, "sites", "site-2", "public", "benchmark-cheatsheet.pdf")
    site2_rss = os.path.join(ROOT_DIR, "sites", "site-2", "public", "rss.xml")
    upload_file("jibranpcccc/workationradar", "public/benchmark-cheatsheet.pdf", site2_pdf)
    upload_file("jibranpcccc/workationradar", "public/rss.xml", site2_rss)

    # Site 1: digitalcreatoravi-seo-engine
    site1_pdf = os.path.join(ROOT_DIR, "sites", "site-1", "public", "benchmark-cheatsheet.pdf")
    site1_rss = os.path.join(ROOT_DIR, "sites", "site-1", "public", "rss.xml")
    upload_file("jibranpcccc/digitalcreatoravi-seo-engine", "sites/site-1/public/benchmark-cheatsheet.pdf", site1_pdf)
    upload_file("jibranpcccc/digitalcreatoravi-seo-engine", "sites/site-1/public/rss.xml", site1_rss)

if __name__ == "__main__":
    main()
