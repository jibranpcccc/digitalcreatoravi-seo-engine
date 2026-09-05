#!/usr/bin/env python3
"""Finish Bing Webmaster Tools GSC Import by confirming Google OAuth consent."""
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
    
    # Check if on Bing home or need to click Import
    body_text = ev_raw(ws, ctx, "document.body.innerText.slice(0, 1000)")
    if "Import your sites from GSC" in (body_text or ""):
        print("Clicking Import button...")
        real_click(ws, ctx, 358, 584, 4)
        time.sleep(2)
        ctx = F.get_ctx(ws)
        
        # Click Continue on modal
        cont = ev_raw(ws, ctx, """(() => {
            const btns = Array.from(document.querySelectorAll('button, [role=button]')).filter(e => (e.textContent||'').trim().toLowerCase() === 'continue' && e.offsetParent);
            if (!btns.length) return null;
            const r = btns[0].getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        if isinstance(cont, str) and cont.startswith("{"):
            cj = json.loads(cont)
            real_click(ws, ctx, cj["x"], cj["y"], 5)
        else:
            real_click(ws, ctx, 1214, 919, 5)
            
        time.sleep(4)
        ctx = F.get_ctx(ws)
        
        # If on account chooser: click jibranpccc
        acc = ev_raw(ws, ctx, """(() => {
            const els = Array.from(document.querySelectorAll('*')).filter(e => (e.textContent||'').includes('jibranpccc@gmail.com') && e.offsetParent);
            if (!els.length) return null;
            const r = els[0].getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        if isinstance(acc, str) and acc.startswith("{"):
            aj = json.loads(acc)
            real_click(ws, ctx, aj["x"], aj["y"], 6)
            time.sleep(4)
            ctx = F.get_ctx(ws)

    # Now on Google Consent page: click Continue at (742, 812)
    print("Clicking Consent Continue button...")
    shot(ws, ctx, "20_before_consent_click.png")
    
    # Try finding Continue button via DOM or coordinates
    c_btn = ev_raw(ws, ctx, """(() => {
        const btns = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
            const t = (e.textContent||'').trim().toLowerCase();
            return t === 'continue' && e.offsetParent;
        });
        if (!btns.length) return null;
        const r = btns[btns.length - 1].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("Continue button location:", c_btn)
    if isinstance(c_btn, str) and c_btn.startswith("{"):
        cb = json.loads(c_btn)
        real_click(ws, ctx, cb["x"], cb["y"], 10)
    else:
        real_click(ws, ctx, 742, 812, 10)
        
    time.sleep(10)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "21_after_consent_redirect.png")
    
    # Check if Bing is showing the sites selection table
    body2 = ev_raw(ws, ctx, "document.body.innerText.slice(0, 1500)")
    print("Bing redirect text:\n", (body2 or "")[:500])
    
    # Look for Import button on Bing sites list
    imp_final = ev_raw(ws, ctx, """(() => {
        const btns = Array.from(document.querySelectorAll('button, [role=button]')).filter(e => {
            const t = (e.textContent||'').trim().toLowerCase();
            return (t === 'import' || t.includes('import')) && e.offsetParent;
        });
        if (!btns.length) return null;
        const r = btns[btns.length - 1].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("Final import button:", imp_final)
    if isinstance(imp_final, str) and imp_final.startswith("{"):
        fb = json.loads(imp_final)
        print("Clicking Final Import button...")
        real_click(ws, ctx, fb["x"], fb["y"], 12)
        time.sleep(6)
        ctx = F.get_ctx(ws)
        shot(ws, ctx, "22_bing_import_done.png")
        print("SUCCESS: Bing import finished!")
        
    try: F.cmd(ws, "session.end", {}, timeout=5)
    except: pass
    ws.close()

if __name__ == "__main__":
    main()
