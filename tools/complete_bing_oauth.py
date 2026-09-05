#!/usr/bin/env python3
"""Complete Bing Webmaster Tools OAuth sign-in and import from GSC."""
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
    real_click(ws, ctx, 1077, 71, 3)
    
    print("Clicking Google sign-in...")
    real_click(ws, ctx, 640, 512, 5)
    
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "03_oauth_screen.png")
    
    # Click Jibran Ayub account
    print("Selecting jibranpccc@gmail.com...")
    real_click(ws, ctx, 600, 200, 8)
    
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "04_after_account_select.png")
    
    # Check if Google Consent / Continue button appears
    cont_check = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
            const t = (e.textContent||'').trim().toLowerCase();
            return (t === 'continue' || t === 'allow') && e.offsetParent;
        });
        if (!els.length) return null;
        const r = els[els.length - 1].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("Consent Continue coord:", cont_check)
    if isinstance(cont_check, str) and cont_check.startswith("{"):
        cj = json.loads(cont_check)
        real_click(ws, ctx, cj["x"], cj["y"], 8)
        
    time.sleep(10)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "05_bing_final_dashboard.png")
    
    info = ev_raw(ws, ctx, "JSON.stringify({url: window.location.href, title: document.title, body: document.body.innerText.slice(0, 1500)})")
    print("Bing final state:\n", info)
    
    try: F.cmd(ws, "session.end", {}, timeout=5)
    except: pass
    ws.close()

if __name__ == "__main__":
    main()
