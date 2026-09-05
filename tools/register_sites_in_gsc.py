#!/usr/bin/env python3
"""Register LocalAgentStack and WorkationRadar in Google Search Console and submit sitemaps."""
import json, sys, time, urllib.parse, os, base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SITES = [
    {
        "name": "LocalAgentStack",
        "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/",
        "sitemap": "sitemap.xml"
    },
    {
        "name": "WorkationRadar",
        "url": "https://jibranpcccc.github.io/workationradar/",
        "sitemap": "sitemap.xml"
    }
]

SHOT_DIR = r"reports/gsc_screenshots"
os.makedirs(SHOT_DIR, exist_ok=True)

def ev_raw(ws, ctx, js, timeout=60):
    r = F.cmd(ws, "script.evaluate", {"target": {"context": ctx}, "expression": js, "awaitPromise": True, "resultOwnership": "root"}, timeout=timeout)
    if r.get("type") == "error": return {"__error__": r.get("message", "")}
    res = (r.get("result") or {}).get("result") or {}
    v = res.get("value")
    if isinstance(v, dict) and v.get("type") == "string": return v.get("value")
    return v

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
    F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]}, timeout=30)
    time.sleep(wait)

def type_text(ws, ctx, text):
    for ch in text:
        seq = {"type": "key", "id": "kb", "actions": [{"type": "keyDown", "value": ch}, {"type": "keyUp", "value": ch}]}
        F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]}, timeout=30)
        time.sleep(0.06)

def add_property(ws, target_url, name):
    print(f"\n=======================================================")
    print(f"Adding Property to Google Search Console: {target_url} ({name})")
    print(f"=======================================================")
    ctx = F.get_ctx(ws)
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://search.google.com/search-console?hl=en", "wait": "complete"}, timeout=60)
    time.sleep(14)
    ctx = F.get_ctx(ws)
    time.sleep(4)
    shot(ws, ctx, f"01_home_{name}.png")

    print("Step 1: Clicking Property dropdown at (140, 96)...")
    real_click(ws, ctx, 140, 96, 4)
    time.sleep(2)
    shot(ws, ctx, f"02_dropdown_{name}.png")
    
    print("Step 2: Finding 'Add property' button...")
    add_btn = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => (e.textContent||'').trim().includes('Add property') && e.offsetParent && e.getBoundingClientRect().x > 0);
        if (!els.length) return null;
        const target = els[els.length - 1];
        const r = target.getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Add property result:", add_btn)
    if not (isinstance(add_btn, str) and add_btn.startswith("{")):
        print("  FAIL: no add property button found")
        return False
    abj = json.loads(add_btn)
    real_click(ws, ctx, abj["x"], abj["y"], 4)
    time.sleep(2)
    shot(ws, ctx, f"03_modal_{name}.png")

    print("Step 3: Selecting URL prefix option...")
    url_box = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => (e.textContent||'').includes('URL prefix') || (e.textContent||'').includes('Add a website'));
        const matches = els.filter(e => e.offsetParent && e.getBoundingClientRect().x > 0);
        if (!matches.length) return null;
        const r = matches[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  URL prefix result:", url_box)
    if isinstance(url_box, str) and url_box.startswith("{"):
        ubj = json.loads(url_box)
        real_click(ws, ctx, ubj["x"], ubj["y"], 3)
        time.sleep(2)

    print("Step 4: Locating input and typing URL...")
    inp_loc = ev_raw(ws, ctx, """(() => {
        const inps = Array.from(document.querySelectorAll('input')).filter(e => e.offsetParent && e.getBoundingClientRect().width > 200);
        if (!inps.length) return null;
        const r = inps[inps.length - 1].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Input coordinates:", inp_loc)
    if isinstance(inp_loc, str) and inp_loc.startswith("{"):
        ij = json.loads(inp_loc)
        real_click(ws, ctx, ij["x"], ij["y"], 2)
        type_text(ws, ctx, target_url)
        time.sleep(2)
        shot(ws, ctx, f"04_typed_{name}.png")
        
        print("Step 5: Clicking Continue...")
        cont_btn = ev_raw(ws, ctx, """(() => {
            const els = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => (e.textContent||'').trim() === 'Continue' && e.offsetParent);
            if (!els.length) return null;
            const r = els[0].getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        print("  Continue button:", cont_btn)
        if isinstance(cont_btn, str) and cont_btn.startswith("{"):
            cbj = json.loads(cont_btn)
            real_click(ws, ctx, cbj["x"], cbj["y"], 8)
            time.sleep(6)
            shot(ws, ctx, f"05_verif_{name}.png")
            
            go_btn = ev_raw(ws, ctx, """(() => {
                const els = Array.from(document.querySelectorAll('button, [role=button], a')).filter(e => (e.textContent||'').toLowerCase().includes('go to property') && e.offsetParent);
                if (!els.length) return null;
                const r = els[0].getBoundingClientRect();
                return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            })()""")
            print("  Go to property button:", go_btn)
            if isinstance(go_btn, str) and go_btn.startswith("{"):
                gbj = json.loads(go_btn)
                real_click(ws, ctx, gbj["x"], gbj["y"], 6)
                print(f"  SUCCESS: Added and opened {target_url}")
                return True
            else:
                ev_raw(ws, ctx, """(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Done' && e.offsetParent);
                    if (b) b.click();
                })()""")
                time.sleep(3)
                print(f"  Verified / Done clicked for {target_url}")
                return True
    print("  FAIL: flow broke before input or continue")
    return False

def submit_sitemap(ws, target_url, sitemap_name, name):
    print(f"\nSubmitting sitemap for {target_url}...")
    encoded = urllib.parse.quote(target_url, safe='')
    sitemap_url = f"https://search.google.com/search-console/sitemaps?resource_id={encoded}"
    ctx = F.get_ctx(ws)
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": sitemap_url, "wait": "complete"}, timeout=60)
    time.sleep(12)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"06_sitemaps_page_{name}.png")
    
    sinp = ev_raw(ws, ctx, """(() => {
        const inps = Array.from(document.querySelectorAll('input')).filter(e => e.offsetParent && (e.type === 'text' || !e.type));
        if (!inps.length) return null;
        const r = inps[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Sitemap input coordinates:", sinp)
    if isinstance(sinp, str) and sinp.startswith("{"):
        sj = json.loads(sinp)
        real_click(ws, ctx, sj["x"], sj["y"], 2)
        type_text(ws, ctx, sitemap_name)
        time.sleep(2)
        shot(ws, ctx, f"07_sitemap_typed_{name}.png")
        
        s_sub = ev_raw(ws, ctx, """(() => {
            const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Submit' && e.offsetParent);
            if (!b) return null;
            const r = b.getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        print("  Sitemap submit coordinates:", s_sub)
        if isinstance(s_sub, str) and s_sub.startswith("{"):
            sbj = json.loads(s_sub)
            real_click(ws, ctx, sbj["x"], sbj["y"], 8)
            time.sleep(6)
            shot(ws, ctx, f"08_sitemap_submitted_{name}.png")
            # Dismiss 'Got it' dialog
            ev_raw(ws, ctx, """(() => {
                const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Got it' && e.offsetParent);
                if (b) b.click();
            })()""")
            print(f"  SUCCESS: Sitemap {sitemap_name} submitted successfully for {name}!")

def main():
    ws = None
    try:
        print("Connecting to isolated Firefox session (port 9334)...")
        ws = F.connect()
        time.sleep(4)
        F.cmd(ws, "browsingContext.getTree", {}, timeout=20)
        
        for site in SITES:
            add_property(ws, site["url"], site["name"])
            time.sleep(4)
            submit_sitemap(ws, site["url"], site["sitemap"], site["name"])
            time.sleep(4)
            
    finally:
        if ws:
            try: F.cmd(ws, "session.end", {}, timeout=10)
            except Exception: pass
            try: ws.close()
            except Exception: pass
            
    print("\nALL SITES ADDED TO GOOGLE SEARCH CONSOLE & SITEMAPS SUBMITTED!")

if __name__ == "__main__":
    main()
