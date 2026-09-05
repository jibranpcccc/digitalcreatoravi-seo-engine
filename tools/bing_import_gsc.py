#!/usr/bin/env python3
"""Import verified Google Search Console properties and sitemaps into Bing Webmaster Tools."""
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
    time.sleep(6)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "08_bing_home.png")
    
    print("Finding 'Import' button on GSC card...")
    imp_btn = ev_raw(ws, ctx, """(() => {
        const btns = Array.from(document.querySelectorAll('button, [role=button]')).filter(e => {
            const t = (e.textContent||'').trim().toLowerCase();
            return t === 'import' && e.offsetParent;
        });
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("Import button coord:", imp_btn)
    
    if isinstance(imp_btn, str) and imp_btn.startswith("{"):
        ij = json.loads(imp_btn)
        real_click(ws, ctx, ij["x"], ij["y"], 5)
    else:
        # Fallback click on coordinates from screenshot
        real_click(ws, ctx, 280, 612, 5)
        
    time.sleep(3)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "09_import_modal.png")
    
    # Check for Continue button in modal
    cont_modal = ev_raw(ws, ctx, """(() => {
        const btns = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
            const t = (e.textContent||'').trim().toLowerCase();
            return (t === 'continue' || t === 'proceed') && e.offsetParent;
        });
        if (!btns.length) return null;
        const r = btns[btns.length - 1].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("Modal Continue button:", cont_modal)
    if isinstance(cont_modal, str) and cont_modal.startswith("{"):
        cj = json.loads(cont_modal)
        real_click(ws, ctx, cj["x"], cj["y"], 6)
        time.sleep(4)
        ctx = F.get_ctx(ws)
        shot(ws, ctx, "10_after_continue.png")
        
        # If Google Account Chooser appears: select jibranpccc@gmail.com
        acc_loc = ev_raw(ws, ctx, """(() => {
            const els = Array.from(document.querySelectorAll('*')).filter(e => {
                const t = (e.textContent||'').trim();
                return t === 'jibranpccc@gmail.com' && e.offsetParent;
            });
            if (!els.length) return null;
            let p = els[0];
            while (p && p.tagName !== 'LI' && p.getAttribute('role') !== 'link' && p.parentElement && p.parentElement !== document.body) {
                p = p.parentElement;
            }
            const r = (p || els[0]).getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        if isinstance(acc_loc, str) and acc_loc.startswith("{"):
            print("Selecting Google account...")
            aj = json.loads(acc_loc)
            real_click(ws, ctx, aj["x"], aj["y"], 6)
            time.sleep(3)
            ctx = F.get_ctx(ws)
            shot(ws, ctx, "11_oauth_consent.png")
            
            # Click Allow / Continue on Google permissions
            consent = ev_raw(ws, ctx, """(() => {
                const btns = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
                    const t = (e.textContent||'').trim().toLowerCase();
                    return (t === 'continue' || t === 'allow') && e.offsetParent;
                });
                if (!btns.length) return null;
                const r = btns[btns.length - 1].getBoundingClientRect();
                return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            })()""")
            if isinstance(consent, str) and consent.startswith("{"):
                print("Clicking Consent Continue...")
                cj = json.loads(consent)
                real_click(ws, ctx, cj["x"], cj["y"], 8)
                time.sleep(8)
                ctx = F.get_ctx(ws)
                shot(ws, ctx, "12_bing_import_sites_list.png")
                
                # Check for final Import button on the sites selection list
                final_imp = ev_raw(ws, ctx, """(() => {
                    const btns = Array.from(document.querySelectorAll('button, [role=button]')).filter(e => {
                        const t = (e.textContent||'').trim().toLowerCase();
                        return (t === 'import' || t.includes('import')) && e.offsetParent;
                    });
                    if (!btns.length) return null;
                    const r = btns[btns.length - 1].getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if isinstance(final_imp, str) and final_imp.startswith("{"):
                    print("Clicking Final Import button...")
                    fj = json.loads(final_imp)
                    real_click(ws, ctx, fj["x"], fj["y"], 10)
                    time.sleep(6)
                    ctx = F.get_ctx(ws)
                    shot(ws, ctx, "13_bing_import_completed.png")
                    print("SUCCESS: GSC sites imported into Bing Webmaster Tools!")

    time.sleep(5)
    info = ev_raw(ws, ctx, "JSON.stringify({url: window.location.href, title: document.title, body: document.body.innerText.slice(0, 1000)})")
    print("Current state:", info)
    
    try: F.cmd(ws, "session.end", {}, timeout=5)
    except: pass
    ws.close()

if __name__ == "__main__":
    main()
