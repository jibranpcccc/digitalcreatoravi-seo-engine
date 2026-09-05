#!/usr/bin/env python3
"""Sign into Bing Webmaster Tools via Google and check properties / import status."""
import sys, time, json, os, base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SHOT_DIR = r"reports/bing_screenshots"
os.makedirs(SHOT_DIR, exist_ok=True)

def shot(ws, ctx, name):
    r = F.cmd(ws, "browsingContext.captureScreenshot", {"context": ctx}, timeout=30)
    out_file = os.path.join(SHOT_DIR, name)
    with open(out_file, "wb") as f:
        f.write(base64.b64decode(r["result"]["data"]))
    print(f"  [screenshot] {out_file}")

def ev_raw(ws, ctx, js, timeout=60):
    r = F.cmd(ws, "script.evaluate", {"target": {"context": ctx}, "expression": js, "awaitPromise": True, "resultOwnership": "root"}, timeout=timeout)
    if r.get("type") == "error": return {"__error__": r.get("message", "")}
    res = (r.get("result") or {}).get("result") or {}
    v = res.get("value")
    if isinstance(v, dict) and v.get("type") == "string": return v.get("value")
    return v

def real_click(ws, ctx, x, y, wait=3):
    seq = {"type": "pointer", "id": "mouse", "parameters": {"pointerType": "mouse"}, "actions": [{"type": "pointerMove", "x": x, "y": y, "duration": 80}, {"type": "pointerDown", "button": 0}, {"type": "pointerUp", "button": 0}]}
    F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]}, timeout=30)
    time.sleep(wait)

def main():
    print("Connecting to Firefox...")
    ws = F.connect()
    ctx = F.get_ctx(ws)
    
    print("Navigating to Bing Webmaster...")
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://www.bing.com/webmasters/", "wait": "complete"}, timeout=30)
    time.sleep(5)
    ctx = F.get_ctx(ws)
    
    print("Clicking Sign In...")
    real_click(ws, ctx, 1077, 71, 4)
    shot(ws, ctx, "01_signin_modal.png")
    
    print("Clicking Google sign-in option at (640, 512)...")
    real_click(ws, ctx, 640, 512, 6)
    
    # Refresh context in case a popup or redirect happened
    time.sleep(6)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "02_after_google_click.png")
    
    # Check if Google account picker appeared or if we are redirected to Bing portal
    url_and_text = ev_raw(ws, ctx, "JSON.stringify({url: window.location.href, title: document.title, body: document.body.innerText.slice(0, 1000)})")
    print("Current state:", url_and_text)
    
    # If Google account picker: click the account if visible
    pick_acc = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => (e.textContent||'').includes('jibranpccc@gmail.com') && e.offsetParent);
        if (!els.length) return null;
        const r = els[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    if isinstance(pick_acc, str) and pick_acc.startswith("{"):
        print("Clicking Google account picker...")
        pj = json.loads(pick_acc)
        real_click(ws, ctx, pj["x"], pj["y"], 6)
        ctx = F.get_ctx(ws)
        shot(ws, ctx, "03_after_account_pick.png")
        
    try: F.cmd(ws, "session.end", {}, timeout=5)
    except: pass
    ws.close()

if __name__ == "__main__":
    main()
