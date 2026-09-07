#!/usr/bin/env python3
import json
import base64
import subprocess

# Fetch index.html
res = subprocess.run(["gh", "api", "/repos/jibranpcccc/jibranpcccc.github.io/contents/index.html"], capture_output=True, text=True)
if res.returncode != 0:
    print("Error fetching index.html:", res.stderr)
    exit(1)

data = json.loads(res.stdout)
sha = data["sha"]
content = base64.b64decode(data["content"]).decode("utf-8")

# Add link in nav if not present
if 'tools.html' not in content:
    target_nav = '<li><a href="https://jibranpcccc.github.io/">Hub Directory</a></li>'
    replacement_nav = '<li><a href="https://jibranpcccc.github.io/">Hub Directory</a></li>\n                <li><a href="https://jibranpcccc.github.io/tools.html" style="color:#38bdf8;font-weight:bold;">⚡ Web Utilities & Calculators (20)</a></li>'
    content = content.replace(target_nav, replacement_nav)

    # Add featured card in grid
    target_grid = '<div class="grid">'
    featured_card = '''<div class="grid">
            <a class="hub-card" href="https://jibranpcccc.github.io/tools.html" style="border: 2px solid #38bdf8; background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(15,23,42,0.6));">
                <div>
                    <h2>⚡ Open Web Utilities & Empirical Benchmarks (20 Live Apps)</h2>
                    <p>Client-side developer calculators, local AI inference benchmarks, quantitative financial models, and edge web utilities.</p>
                </div>
            </a>'''
    content = content.replace(target_grid, featured_card, 1)

    new_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": "feat: link tools.html in main nav and featured directory card",
        "content": new_b64,
        "sha": sha,
        "branch": "main"
    }

    put_res = subprocess.run(["gh", "api", "--method", "PUT", "/repos/jibranpcccc/jibranpcccc.github.io/contents/index.html", "--input", "-"], input=json.dumps(payload), text=True, capture_output=True)
    if put_res.returncode == 0:
        print("SUCCESS: index.html updated with direct link to tools.html")
    else:
        print("Error updating index.html:", put_res.stderr)
else:
    print("tools.html already linked in index.html")
