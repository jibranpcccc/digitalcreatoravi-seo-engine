#!/usr/bin/env python3
"""Autonomous Google Search Console Property Registration & Sitemap Submission via Firefox."""
import sys, time, json, os, base64, urllib.parse

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
        print(f"  [screenshot] {out_file}")
        return True
    except Exception as e:
        print("  [shot error]", e)
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

def type_text(ws, ctx, text):
    for ch in text:
        seq = {"type": "key", "id": "kb", "actions": [{"type": "keyDown", "value": ch}, {"type": "keyUp", "value": ch}]}
        F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]}, timeout=30)
        time.sleep(0.04)

def register_property(ws, target_url, short_name):
    print(f"\n=======================================================")
    print(f"Registering Property: {target_url} ({short_name})")
    print(f"=======================================================")
    ctx = F.get_ctx(ws)
    
    print("Navigating to welcome page...")
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://search.google.com/search-console/welcome?hl=en", "wait": "complete"}, timeout=60)
    time.sleep(10)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"10_welcome_{short_name}.png")
    
    print("Clicking 'Add a website' button...")
    add_web = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('button, [role=button]')).filter(e => {
            const t = (e.textContent || '').trim();
            return (t.includes('Add a website') || t.includes('website')) && e.offsetParent;
        });
        if (!els.length) return null;
        const b = els[0];
        const r = b.getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Add website coord:", add_web)
    if isinstance(add_web, str) and add_web.startswith("{"):
        loc = json.loads(add_web)
        real_click(ws, ctx, loc["x"], loc["y"], 4)
    else:
        print("  Add website button not found or modal might already be open.")
        
    shot(ws, ctx, f"11_modal_{short_name}.png")
    
    print("Locating URL Prefix input box...")
    url_input = ev_raw(ws, ctx, """(() => {
        const inps = Array.from(document.querySelectorAll('input')).filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 150 && r.x > 500 && i.offsetParent;
        });
        if (!inps.length) return null;
        const target = inps[0];
        const r = target.getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  URL Prefix input:", url_input)
    if not (isinstance(url_input, str) and url_input.startswith("{")):
        print("  ERROR: URL prefix input not found!")
        return False
        
    uinp = json.loads(url_input)
    real_click(ws, ctx, uinp["x"], uinp["y"], 2)
    print(f"Typing URL: {target_url}...")
    type_text(ws, ctx, target_url)
    time.sleep(2)
    shot(ws, ctx, f"12_typed_{short_name}.png")
    
    print("Finding URL Prefix CONTINUE button...")
    cont_btn = ev_raw(ws, ctx, """(() => {
        const btns = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
            const t = (e.textContent || '').trim();
            const r = e.getBoundingClientRect();
            return t === 'CONTINUE' && r.x > 500 && e.offsetParent;
        });
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Continue button:", cont_btn)
    if not (isinstance(cont_btn, str) and cont_btn.startswith("{")):
        print("  ERROR: Continue button not found!")
        return False
        
    cb = json.loads(cont_btn)
    real_click(ws, ctx, cb["x"], cb["y"], 8)
    time.sleep(6)
    shot(ws, ctx, f"13_verif_result_{short_name}.png")
    
    # Check verification status
    status_text = ev_raw(ws, ctx, "document.body.innerText.slice(0, 2000)")
    print("  Status summary:", (status_text or "")[:300].replace("\n", " "))
    
    # Check if Ownership auto-verified or Go to Property button exists
    go_btn = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('button, [role=button], a')).filter(e => {
            const t = (e.textContent || '').toLowerCase().trim();
            return (t.includes('go to property') || t === 'done') && e.offsetParent;
        });
        if (!els.length) return null;
        const r = els[0].getBoundingClientRect();
        return JSON.stringify({text: els[0].textContent.trim(), x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Go to property / Done button:", go_btn)
    if isinstance(go_btn, str) and go_btn.startswith("{"):
        gb = json.loads(go_btn)
        print(f"  Clicking '{gb['text']}'...")
        real_click(ws, ctx, gb["x"], gb["y"], 5)
        shot(ws, ctx, f"14_property_opened_{short_name}.png")
        return True
    else:
        print("  Needs manual or code verification inspection...")
        return "needs_inspect"

def submit_sitemap_for_site(ws, target_url, short_name):
    print(f"\nSubmitting Sitemap for {target_url}...")
    encoded = urllib.parse.quote(target_url, safe='')
    sitemap_url = f"https://search.google.com/search-console/sitemaps?resource_id={encoded}"
    ctx = F.get_ctx(ws)
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": sitemap_url, "wait": "complete"}, timeout=60)
    time.sleep(12)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"20_sitemap_page_{short_name}.png")
    
    print("Locating sitemap text field...")
    sinp = ev_raw(ws, ctx, """(() => {
        const inps = Array.from(document.querySelectorAll('input')).filter(e => e.offsetParent && (e.type === 'text' || !e.type));
        if (!inps.length) return null;
        const r = inps[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Sitemap input:", sinp)
    if isinstance(sinp, str) and sinp.startswith("{"):
        sj = json.loads(sinp)
        real_click(ws, ctx, sj["x"], sj["y"], 2)
        type_text(ws, ctx, "sitemap.xml")
        time.sleep(2)
        shot(ws, ctx, f"21_sitemap_typed_{short_name}.png")
        
        s_sub = ev_raw(ws, ctx, """(() => {
            const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Submit' && e.offsetParent);
            if (!b) return null;
            const r = b.getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        print("  Sitemap submit button:", s_sub)
        if isinstance(s_sub, str) and s_sub.startswith("{"):
            sbj = json.loads(s_sub)
            real_click(ws, ctx, sbj["x"], sbj["y"], 8)
            time.sleep(6)
            shot(ws, ctx, f"22_sitemap_submitted_{short_name}.png")
            
            # Dismiss 'Got it' modal if present
            ev_raw(ws, ctx, """(() => {
                const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Got it' && e.offsetParent);
                if (b) b.click();
            })()""")
            time.sleep(3)
            print(f"  SUCCESS: sitemap.xml submitted for {short_name}!")
            return True
    return False

def main():
    sites = [
        {"url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/", "name": "LocalAgentStack"},
        {"url": "https://jibranpcccc.github.io/workationradar/", "name": "WorkationRadar"}
    ]
    print("Connecting to Firefox...")
    ws = F.connect()
    try:
        for s in sites:
            res = register_property(ws, s["url"], s["name"])
            print(f"Registration result for {s['name']}: {res}")
            time.sleep(4)
            submit_sitemap_for_site(ws, s["url"], s["name"])
            time.sleep(4)
    finally:
        try:
            F.cmd(ws, "session.end", {}, timeout=5)
        except: pass
        ws.close()

if __name__ == "__main__":
    main()
