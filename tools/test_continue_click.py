#!/usr/bin/env python3
import sys, time, json, os, base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SHOT_DIR = r"reports/gsc_screenshots"

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

def type_text(ws, ctx, text):
    for ch in text:
        seq = {"type": "key", "id": "kb", "actions": [{"type": "keyDown", "value": ch}, {"type": "keyUp", "value": ch}]}
        F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]}, timeout=30)
        time.sleep(0.03)

def main():
    target_url = "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/"
    print(f"Testing URL prefix registration for: {target_url}")
    
    ws = F.connect()
    ctx = F.get_ctx(ws)
    
    print("Navigating to welcome screen...")
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://search.google.com/search-console/welcome?hl=en", "wait": "complete"}, timeout=60)
    time.sleep(10)
    ctx = F.get_ctx(ws)
    
    print("Clicking Add a website...")
    add_web = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('button, [role=button]')).filter(e => (e.textContent||'').includes('Add a website') && e.offsetParent);
        if (!els.length) return null;
        const r = els[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    if isinstance(add_web, str) and add_web.startswith("{"):
        loc = json.loads(add_web)
        real_click(ws, ctx, loc["x"], loc["y"], 3)
        
    shot(ws, ctx, "test_modal.png")
    
    print("Locating URL Prefix input...")
    url_input = ev_raw(ws, ctx, """(() => {
        const inps = Array.from(document.querySelectorAll('input')).filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 150 && r.x > 500 && i.offsetParent;
        });
        if (!inps.length) return null;
        const r = inps[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Input coord:", url_input)
    loc = json.loads(url_input)
    real_click(ws, ctx, loc["x"], loc["y"], 1)
    type_text(ws, ctx, target_url)
    time.sleep(2)
    shot(ws, ctx, "test_typed.png")
    
    print("Searching for Continue button (case-insensitive)...")
    cont_info = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => {
            const t = (e.textContent || '').trim();
            const r = e.getBoundingClientRect();
            return t.toUpperCase() === 'CONTINUE' && r.x > 500 && r.width > 20 && r.height > 10 && e.offsetParent;
        });
        return JSON.stringify(els.map(e => ({
            tag: e.tagName,
            text: e.textContent.trim(),
            rect: e.getBoundingClientRect(),
            classes: e.className
        })));
    })()""")
    print("  Found Continue candidates:", cont_info)
    
    candidates = json.loads(cont_info) if isinstance(cont_info, str) and cont_info.startswith("[") else []
    if candidates:
        target = candidates[-1] # pick deepest element
        r = target["rect"]
        cx = round(r["x"] + r["width"]/2)
        cy = round(r["y"] + r["height"]/2)
        print(f"Clicking Continue at ({cx}, {cy})...")
        real_click(ws, ctx, cx, cy, 8)
        time.sleep(6)
        shot(ws, ctx, "test_after_continue.png")
        
        body_text = ev_raw(ws, ctx, "document.body.innerText.slice(0, 3000)")
        print("\nPage text after Continue:\n", body_text[:1500])
    
    try: F.cmd(ws, "session.end", {}, timeout=5)
    except: pass
    ws.close()

if __name__ == "__main__":
    main()
