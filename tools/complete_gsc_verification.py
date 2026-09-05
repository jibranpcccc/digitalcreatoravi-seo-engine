#!/usr/bin/env python3
"""Complete Google Search Console Verification and Sitemap Submission for both sites."""
import sys, time, json, os, base64, urllib.parse

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

SHOT_DIR = r"reports/gsc_screenshots"
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

def type_text(ws, ctx, text):
    for ch in text:
        seq = {"type": "key", "id": "kb", "actions": [{"type": "keyDown", "value": ch}, {"type": "keyUp", "value": ch}]}
        F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]}, timeout=30)
        time.sleep(0.03)

def verify_and_add_site(ws, target_url, short_name):
    print(f"\n=======================================================")
    print(f"STARTING GSC REGISTRATION & VERIFICATION: {short_name}")
    print(f"URL: {target_url}")
    print(f"=======================================================")
    
    ctx = F.get_ctx(ws)
    print("Navigating to GSC welcome screen...")
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://search.google.com/search-console/welcome?hl=en", "wait": "complete"}, timeout=60)
    time.sleep(8)
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
    time.sleep(2)
    
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
    loc = json.loads(url_input)
    real_click(ws, ctx, loc["x"], loc["y"], 1)
    type_text(ws, ctx, target_url)
    time.sleep(2)
    
    print("Clicking CONTINUE...")
    cont_info = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => {
            const t = (e.textContent || '').trim();
            const r = e.getBoundingClientRect();
            return t.toUpperCase() === 'CONTINUE' && r.x > 500 && r.width > 20 && r.height > 10 && e.offsetParent;
        });
        return JSON.stringify(els.map(e => ({
            tag: e.tagName,
            text: e.textContent.trim(),
            rect: e.getBoundingClientRect()
        })));
    })()""")
    candidates = json.loads(cont_info) if isinstance(cont_info, str) and cont_info.startswith("[") else []
    if candidates:
        r = candidates[-1]["rect"]
        cx = round(r["x"] + r["width"]/2)
        cy = round(r["y"] + r["height"]/2)
        real_click(ws, ctx, cx, cy, 8)
        time.sleep(5)
    
    shot(ws, ctx, f"30_verification_modal_{short_name}.png")
    
    # Check if already auto-verified or if VERIFY button exists
    print("Looking for VERIFY button in modal...")
    verif_btn = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('button, [role=button], span, div')).filter(e => {
            const t = (e.textContent || '').trim();
            const r = e.getBoundingClientRect();
            return t.toUpperCase() === 'VERIFY' && r.width > 30 && r.height > 15 && e.offsetParent;
        });
        if (!els.length) return null;
        const r = els[els.length - 1].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  VERIFY button:", verif_btn)
    if isinstance(verif_btn, str) and verif_btn.startswith("{"):
        vb = json.loads(verif_btn)
        print(f"Clicking VERIFY at ({vb['x']}, {vb['y']})...")
        real_click(ws, ctx, vb["x"], vb["y"], 10)
        time.sleep(6)
        shot(ws, ctx, f"31_after_verify_{short_name}.png")
    
    # Dismiss or Go to property
    go_btn = ev_raw(ws, ctx, """(() => {
        const els = Array.from(document.querySelectorAll('button, [role=button], a, span')).filter(e => {
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
        real_click(ws, ctx, gb["x"], gb["y"], 5)
        time.sleep(3)
        shot(ws, ctx, f"32_property_dashboard_{short_name}.png")
    
    # Now submit sitemap
    print(f"\nSubmitting sitemap.xml for {target_url}...")
    encoded = urllib.parse.quote(target_url, safe='')
    sitemap_url = f"https://search.google.com/search-console/sitemaps?resource_id={encoded}"
    ctx = F.get_ctx(ws)
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": sitemap_url, "wait": "complete"}, timeout=60)
    time.sleep(10)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"33_sitemap_page_{short_name}.png")
    
    # Find sitemap input
    sinp = ev_raw(ws, ctx, """(() => {
        // Look for the input in the 'Add a new sitemap' form
        const inps = Array.from(document.querySelectorAll('input')).filter(i => {
            const r = i.getBoundingClientRect();
            return i.offsetParent && r.width > 80 && r.y < 350;
        });
        if (!inps.length) return null;
        const target = inps[inps.length - 1];
        const r = target.getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("  Sitemap input coord:", sinp)
    if isinstance(sinp, str) and sinp.startswith("{"):
        sj = json.loads(sinp)
        real_click(ws, ctx, sj["x"], sj["y"], 1)
        type_text(ws, ctx, "sitemap.xml")
        time.sleep(2)
        shot(ws, ctx, f"34_sitemap_typed_{short_name}.png")
        
        # Click submit
        s_sub = ev_raw(ws, ctx, """(() => {
            const btns = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
                const t = (e.textContent || '').trim();
                const r = e.getBoundingClientRect();
                return t.toUpperCase() === 'SUBMIT' && r.width > 30 && r.y < 350 && e.offsetParent;
            });
            if (!btns.length) return null;
            const r = btns[btns.length - 1].getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        print("  Sitemap submit coord:", s_sub)
        if isinstance(s_sub, str) and s_sub.startswith("{"):
            sbj = json.loads(s_sub)
            real_click(ws, ctx, sbj["x"], sbj["y"], 8)
            time.sleep(6)
            shot(ws, ctx, f"35_sitemap_submitted_{short_name}.png")
            
            # Dismiss 'Got it' dialog
            ev_raw(ws, ctx, """(() => {
                const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => (e.textContent||'').trim() === 'Got it' && e.offsetParent);
                if (b) b.click();
            })()""")
            time.sleep(3)
            shot(ws, ctx, f"36_sitemap_final_{short_name}.png")
            print(f"SUCCESS: {short_name} verified and sitemap submitted!")
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
            verify_and_add_site(ws, s["url"], s["name"])
            time.sleep(5)
    finally:
        try: F.cmd(ws, "session.end", {}, timeout=5)
        except: pass
        ws.close()

if __name__ == "__main__":
    main()
