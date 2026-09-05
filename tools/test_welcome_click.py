#!/usr/bin/env python3
import sys, time, json, os, base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SHOT_DIR = r"reports/gsc_screenshots"
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
    
    print("Navigating to GSC welcome screen...")
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://search.google.com/search-console/welcome?hl=en", "wait": "complete"}, timeout=60)
    time.sleep(10)
    ctx = F.get_ctx(ws)
    
    shot(ws, ctx, "10_welcome_screen.png")
    
    print("Finding 'Add a website' button...")
    add_web = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => {
            const t = (e.textContent || '').trim();
            return (t.includes('Add a website') || t.includes('website')) && e.offsetParent && e.getBoundingClientRect().width > 50;
        });
        if (!els.length) return null;
        const b = els.find(e => e.tagName === 'BUTTON' || e.getAttribute('role') === 'button') || els[0];
        const r = b.getBoundingClientRect();
        return JSON.stringify({tag: b.tagName, text: b.textContent.trim(), x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  'Add a website' button location:", add_web)
    
    if isinstance(add_web, str) and add_web.startswith("{"):
        loc = json.loads(add_web)
        real_click(ws, ctx, loc["x"], loc["y"], 4)
        shot(ws, ctx, "11_after_add_website.png")
        
        info = ev_raw(ws, ctx, """(() => {
            return JSON.stringify({
                url: window.location.href,
                bodyText: document.body.innerText.slice(0, 1000),
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({
                    placeholder: i.placeholder,
                    type: i.type,
                    rect: i.getBoundingClientRect()
                }))
            });
        })()""")
        print("  Page state after click:", info)
    
    try:
        F.cmd(ws, "session.end", {}, timeout=5)
    except: pass
    ws.close()

if __name__ == "__main__":
    main()
