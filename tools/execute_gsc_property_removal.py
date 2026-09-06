import sys
import time
import os
import json
import base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SHOT_DIR = r"reports/gsc_removal"
os.makedirs(SHOT_DIR, exist_ok=True)

def shot(ws, ctx, name):
    try:
        r = F.cmd(ws, "browsingContext.captureScreenshot", {"context": ctx}, timeout=30)
        out_file = os.path.join(SHOT_DIR, name)
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(r["result"]["data"]))
        print(f"  [screenshot saved] {out_file}")
        return True
    except Exception as e:
        print("  [shot failed]", e)
        return False

def real_click(ws, ctx, x, y, wait=3):
    seq = {"type": "pointer", "id": "mouse", "parameters": {"pointerType": "mouse"}, "actions": [{"type": "pointerMove", "x": x, "y": y, "duration": 80}, {"type": "pointerDown", "button": 0}, {"type": "pointerUp", "button": 0}]}
    F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]})
    time.sleep(wait)

def remove_site(ws, target_url, slug):
    print(f"\n=======================================================")
    print(f"Removing Property from jibranpccc@gmail.com: {target_url}")
    print(f"=======================================================")
    
    settings_url = f"https://search.google.com/search-console/settings?resource_id={target_url}"
    ctx = F.get_ctx(ws)
    print(f"Step 1: Navigating to settings: {settings_url}")
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": settings_url, "wait": "complete"}, timeout=60)
    time.sleep(6)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"{slug}_step1_settings.png")

    # Step 2: Click red "REMOVE PROPERTY" button at bottom right
    print("Step 2: Clicking bottom-right 'REMOVE PROPERTY' button (x=1167, y=903)...")
    real_click(ws, ctx, 1167, 903, 3)
    time.sleep(2)
    shot(ws, ctx, f"{slug}_step2_modal_open.png")

    # Step 3: Click confirmation "REMOVE PROPERTY" button in modal at exact coordinates (x=783, y=573)
    print("Step 3: Clicking modal confirm 'REMOVE PROPERTY' button at exact (x=783, y=573)...")
    real_click(ws, ctx, 783, 573, 5)
    time.sleep(6)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"{slug}_step3_removed_confirmation.png")
    print(f"SUCCESS: Property removal confirmed for {slug}!")

def main():
    ws = F.connect()
    print("Connected to Firefox!")
    
    # 1. Remove Site 1 (digitalcreatoravi-seo-engine)
    remove_site(ws, "https%3A%2F%2Fjibranpcccc.github.io%2Fdigitalcreatoravi-seo-engine%2F", "site1")
    time.sleep(4)

    # 2. Remove Site 2 (workationradar)
    remove_site(ws, "https%3A%2F%2Fjibranpcccc.github.io%2Fworkationradar%2F", "site2")
    time.sleep(4)

    try:
        F.cmd(ws, "session.end", {}, timeout=5)
    except Exception:
        pass
    ws.close()
    print("\n[✔] ALL PROPERTIES SUCCESSFULLY REMOVED FROM jibranpccc@gmail.com!")

if __name__ == "__main__":
    main()
