#!/usr/bin/env python3
"""
Deploys 20 dedicated tool landing pages to jibranpcccc.github.io/tools/
Each page provides an authoritative DA 96 single-page feature linking directly to the live edge app.
"""

import os
import json
import base64
import sqlite3
import subprocess
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM indexed_pages ORDER BY site_id, id")
    all_pages = [dict(r) for r in cursor.fetchall()]
    conn.close()

    print("=== DEPLOYING 20 DEDICATED LANDING PAGES TO JIBRANPCCCC.GITHUB.IO (DA 96) ===")
    
    deployed_urls = []

    for s in sites:
        site_id = s["id"]
        name = s["name"]
        url = s["url"].rstrip("/")
        niche = s["niche"]
        slug = f"{site_id}-{name.lower()}"
        file_path = f"tools/{slug}.html"
        subpages = [p for p in all_pages if p["site_id"] == site_id]

        subpages_html = ""
        for p in subpages:
            p_title = p["title"] or "Core Analysis"
            p_url = p["url"]
            subpages_html += f'<li><a href="{p_url}" class="text-indigo-400 hover:underline">{p_title}</a></li>\n'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{name} - {niche} Official Directory Listing</title>
    <meta name="description" content="Verified profile and official web application launchpad for {name}, providing zero-latency client-side tools for {niche}.">
    <link rel="canonical" href="{url}/">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans p-6 sm:p-12">
    <div class="max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">
        <div class="flex items-center justify-between border-b border-slate-800 pb-6 mb-6">
            <div>
                <span class="text-xs font-mono text-indigo-400 uppercase tracking-widest">{site_id} • Verified Utility</span>
                <h1 class="text-3xl font-extrabold text-white mt-1">{name}</h1>
                <p class="text-slate-400 text-sm mt-1">{niche}</p>
            </div>
            <a href="{url}/" target="_blank" class="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 font-bold text-white shadow-lg shadow-indigo-500/20 transition">
                Launch Live App &rarr;
            </a>
        </div>

        <div class="prose prose-invert max-w-none text-slate-300 text-sm leading-relaxed mb-8">
            <h2 class="text-lg font-bold text-white mb-2">Overview & Capabilities</h2>
            <p>{name} is an open-source, edge-deployed web utility calibrated for {niche}. Engineered for zero server dependencies, instant client-side execution, and total user privacy.</p>
            
            <h2 class="text-lg font-bold text-white mt-6 mb-2">Key Deep-Dive Guides & Modules</h2>
            <ul class="space-y-2 list-disc list-inside text-indigo-400">
                {subpages_html}
            </ul>
        </div>

        <div class="border-t border-slate-800 pt-6 flex items-center justify-between text-xs text-slate-500">
            <span>Official Canonical App: <a href="{url}/" class="text-indigo-400">{url}/</a></span>
            <a href="https://jibranpcccc.github.io/tools.html" class="text-slate-400 hover:text-white">&larr; Back to Tools Directory</a>
        </div>
    </div>
</body>
</html>"""

        b64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
        payload = {
            "message": f"feat: add dedicated profile page for {name} ({site_id})",
            "content": b64,
            "branch": "main"
        }

        # Check sha if exists
        check_res = subprocess.run(["gh", "api", f"/repos/jibranpcccc/jibranpcccc.github.io/contents/{file_path}"], capture_output=True, text=True)
        if check_res.returncode == 0:
            payload["sha"] = json.loads(check_res.stdout).get("sha")

        put_cmd = ["gh", "api", "--method", "PUT", f"/repos/jibranpcccc/jibranpcccc.github.io/contents/{file_path}", "--input", "-"]
        res = subprocess.run(put_cmd, input=json.dumps(payload), text=True, capture_output=True)
        if res.returncode == 0:
            live_page_url = f"https://jibranpcccc.github.io/{file_path}"
            print(f"[+] Deployed: {live_page_url} -> Links to: {url}")
            deployed_urls.append({"site_id": site_id, "url": live_page_url, "target": url})
        else:
            print(f"[-] Error deploying {file_path}: {res.stderr}")
        time.sleep(0.5)

    print(f"\nSUCCESS: Deployed {len(deployed_urls)}/20 dedicated landing pages on jibranpcccc.github.io (DA 96).")

if __name__ == "__main__":
    main()
