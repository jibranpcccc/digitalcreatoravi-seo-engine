#!/usr/bin/env python3
"""Capture Desktop and Mobile UI screenshots for all 4 live websites."""
import sys
import os
import time
import base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SHOT_DIR = r"reports/ui_screenshots"
os.makedirs(SHOT_DIR, exist_ok=True)

SITES = [
    {
        "id": "site1",
        "name": "LocalAgentStack",
        "home": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/",
        "article": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/"
    },
    {
        "id": "site2",
        "name": "WorkationRadar",
        "home": "https://jibranpcccc.github.io/workationradar/",
        "article": "https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/"
    },
    {
        "id": "site3",
        "name": "OpenAgentStack",
        "home": "https://openagentstack.pages.dev/",
        "article": "https://openagentstack.pages.dev/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/"
    },
    {
        "id": "site4",
        "name": "IndieStackAudit",
        "home": "https://indiestackaudit.pages.dev/",
        "article": "https://indiestackaudit.pages.dev/stacks/nextjs-vs-astro-for-micro-saas-speed-cost-seo/"
    }
]

def shot(ws, ctx, filename):
    r = F.cmd(ws, "browsingContext.captureScreenshot", {"context": ctx}, timeout=30)
    out_file = os.path.join(SHOT_DIR, filename)
    with open(out_file, "wb") as f:
        f.write(base64.b64decode(r["result"]["data"]))
    print(f"  [saved] {out_file}")
    return out_file

def main():
    print("Connecting to Firefox...")
    ws = F.connect()
    ctx = F.get_ctx(ws)
    
    for s in SITES:
        print(f"\n--- Testing UI for {s['name']} ---")
        
        # 1. Desktop Viewport (1440 x 900)
        F.cmd(ws, "browsingContext.setViewport", {"context": ctx, "viewport": {"width": 1440, "height": 900}})
        
        print(f"  Loading Homepage: {s['home']}")
        F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": s["home"], "wait": "complete"}, timeout=30)
        time.sleep(3)
        shot(ws, ctx, f"{s['id']}_desktop_home.png")
        
        print(f"  Loading Article: {s['article']}")
        F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": s["article"], "wait": "complete"}, timeout=30)
        time.sleep(3)
        shot(ws, ctx, f"{s['id']}_desktop_article.png")
        
        # 2. Mobile Viewport (390 x 844)
        F.cmd(ws, "browsingContext.setViewport", {"context": ctx, "viewport": {"width": 390, "height": 844}})
        print(f"  Loading Mobile Article: {s['article']}")
        F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": s["article"], "wait": "complete"}, timeout=30)
        time.sleep(3)
        shot(ws, ctx, f"{s['id']}_mobile_article.png")
        
    try:
        F.cmd(ws, "session.end", {}, timeout=5)
    except:
        pass
    ws.close()
    print("\nAll UI screenshots captured successfully!")

if __name__ == "__main__":
    main()
