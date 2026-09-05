"""
Automated Google Search Console Property Registration & Sitemap Submission
Uses active authenticated Firefox session via C:\\HermesWork\\seo-tools\\ff.py
"""
import sys
import time
import json
import os
import urllib.parse
import base64

sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

TARGET_URLS = [
    "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/",
    "https://jibranpcccc.github.io/workationradar/"
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
    F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]})
    time.sleep(wait)

def type_text(ws, ctx, text):
    for ch in text:
        seq = {"type": "key", "id": "kb", "actions": [{"type": "keyDown", "value": ch}, {"type": "keyUp", "value": ch}]}
        F.cmd(ws, "input.performActions", {"context": ctx, "actions": [seq]})
        time.sleep(0.06)

def add_property_to_gsc(ws, target_url):
    print(f"\n=======================================================")
    print(f"Registering Property in GSC: {target_url}")
    print(f"=======================================================")
    
    ctx = F.get_ctx(ws)
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": "https://search.google.com/search-console?hl=en", "wait": "complete"}, timeout=60)
    time.sleep(10)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, "01_gsc_home.png")
    
    # 1. Click Property Selector (top-left)
    print("Step 1: Clicking property dropdown...")
    real_click(ws, ctx, 140, 96, 4)
    shot(ws, ctx, "02_dropdown_opened.png")
    time.sleep(2)
    
    # 2. Click "+ Add property"
    print("Step 2: Locating '+ Add property'...")
    r = ev_raw(ws, ctx, """(() => {
      const els = Array.from(document.querySelectorAll('*')).filter(e => {
        const t = (e.textContent||'').trim();
        const r = e.getBoundingClientRect();
        return t.includes('Add property') && e.offsetParent && r.x > 0 && r.y > 0;
      });
      const out = els.map(el => { const r = el.getBoundingClientRect(); return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2), t: (el.textContent||'').trim().slice(0, 40)}; });
      const seen = new Set();
      return JSON.stringify(out.filter(o => { const k = o.x+','+o.y+','+o.t; if (seen.has(k)) return false; seen.add(k); return true; }));
    })()""")
    print("Add property candidates:", r)
    
    if isinstance(r, str) and r.startswith("["):
        cands = json.loads(r)
        if cands:
            t = cands[-1]
            real_click(ws, ctx, t["x"], t["y"], 4)
            print("Clicked '+ Add property'")
            time.sleep(2)
            shot(ws, ctx, "03_modal_opened.png")
            
            # 3. Check for URL prefix input or "Add a website"
            r2 = ev_raw(ws, ctx, """(() => {
              const els = Array.from(document.querySelectorAll('*')).filter(e => {
                const t = (e.textContent||'').trim();
                const r = e.getBoundingClientRect();
                return (t.includes('Add a website') || t.includes('URL prefix')) && e.offsetParent && r.x > 0 && r.y > 0;
              });
              const out = els.map(el => { const r = el.getBoundingClientRect(); return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2), t: (el.textContent||'').trim().slice(0, 40)}; });
              return JSON.stringify(out);
            })()""")
            print("Modal option elements:", r2)
            if isinstance(r2, str) and r2.startswith("["):
                cands2 = json.loads(r2)
                if cands2:
                    real_click(ws, ctx, cands2[0]["x"], cands2[0]["y"], 3)
                    print("Selected URL prefix box")
                    time.sleep(2)
            
            # 4. Find input box
            r3 = ev_raw(ws, ctx, """(() => {
              const inps = Array.from(document.querySelectorAll('input')).filter(e => e.offsetParent && e.getBoundingClientRect().width > 200);
              if (!inps.length) return 'no input';
              // pick the second or last input (URL prefix box)
              const inp = inps[inps.length - 1];
              const r = inp.getBoundingClientRect();
              return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            })()""")
            print("Input box coordinates:", r3)
            if isinstance(r3, str) and r3.startswith("{"):
                inpc = json.loads(r3)
                real_click(ws, ctx, inpc["x"], inpc["y"], 2)
                type_text(ws, ctx, target_url)
                time.sleep(2)
                shot(ws, ctx, "04_url_typed.png")
                
                # 5. Click Continue
                r4 = ev_raw(ws, ctx, """(() => {
                  const els = Array.from(document.querySelectorAll('button, [role=button], div, span')).filter(e => {
                    const t = (e.textContent||'').trim();
                    const r = e.getBoundingClientRect();
                    return t === 'Continue' && e.offsetParent && r.x > 0 && r.y > 0;
                  });
                  const out = els.map(el => { const r = el.getBoundingClientRect(); return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)}; });
                  return JSON.stringify(out);
                })()""")
                print("Continue button coordinates:", r4)
                if isinstance(r4, str) and r4.startswith("["):
                    cands4 = json.loads(r4)
                    if cands4:
                        real_click(ws, ctx, cands4[0]["x"], cands4[0]["y"], 8)
                        print("Clicked Continue (Checking verification)...")
                        time.sleep(6)
                        shot(ws, ctx, "05_verification_state.png")
                        
                        # Handle verification result
                        verif_text = ev_raw(ws, ctx, "document.body.innerText")
                        print("Verification dialog text snippet:", (verif_text or "")[:300])
                        
                        # Check if auto-verified
                        if "Ownership auto-verified" in (verif_text or "") or "Ownership verified" in (verif_text or ""):
                            print("OWNERSHIP AUTO-VERIFIED!")
                            ev_raw(ws, ctx, """(() => {
                                const b = Array.from(document.querySelectorAll('button, [role=button], a')).find(e => (e.textContent||'').toLowerCase().includes('go to property') || (e.textContent||'').trim() === 'Done');
                                if (b) b.click();
                            })()""")
                            time.sleep(4)
                        else:
                            # Check if HTML tag verification is available
                            print("Checking HTML verification details in modal...")
                            html_tag = ev_raw(ws, ctx, """(() => {
                                const els = Array.from(document.querySelectorAll('*')).filter(e => (e.textContent||'').includes('google-site-verification'));
                                return els.map(e => (e.textContent||'').trim()).join('\\n');
                            })()""")
                            print("HTML Tag info:", html_tag)
                            ev_raw(ws, ctx, """(() => {
                                const b = Array.from(document.querySelectorAll('button, [role=button], a')).find(e => (e.textContent||'').trim() === 'Done');
                                if (b) b.click();
                            })()""")
                            time.sleep(3)

    # 6. Submit Sitemap
    submit_sitemap(ws, target_url)

def submit_sitemap(ws, target_url):
    print(f"\nSubmitting sitemap for {target_url}...")
    encoded = urllib.parse.quote(target_url, safe='')
    sitemap_url = f"https://search.google.com/search-console/sitemaps?resource_id={encoded}"
    ctx = F.get_ctx(ws)
    F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": sitemap_url, "wait": "complete"}, timeout=60)
    time.sleep(10)
    ctx = F.get_ctx(ws)
    shot(ws, ctx, f"sitemap_{target_url.split('/')[-2]}_page.png")
    
    sinp = ev_raw(ws, ctx, """(() => {
        const inps = Array.from(document.querySelectorAll('input')).filter(e => e.offsetParent && (e.type === 'text' || !e.type));
        if (!inps.length) return null;
        const r = inps[0].getBoundingClientRect();
        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
    })()""")
    print("Sitemap input coords:", sinp)
    if isinstance(sinp, str) and sinp.startswith("{"):
        sj = json.loads(sinp)
        real_click(ws, ctx, sj["x"], sj["y"], 2)
        type_text(ws, ctx, "sitemap.xml")
        time.sleep(2)
        
        s_sub = ev_raw(ws, ctx, """(() => {
            const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Submit' && e.offsetParent);
            if (!b) return null;
            const r = b.getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
        })()""")
        print("Sitemap submit button coords:", s_sub)
        if isinstance(s_sub, str) and s_sub.startswith("{"):
            sbj = json.loads(s_sub)
            real_click(ws, ctx, sbj["x"], sbj["y"], 8)
            time.sleep(5)
            shot(ws, ctx, f"sitemap_{target_url.split('/')[-2]}_submitted.png")
            # Dismiss 'Got it' dialog
            ev_raw(ws, ctx, """(() => {
                const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').trim() === 'Got it' && e.offsetParent);
                if (b) b.click();
            })()""")
            print(f"SUCCESS: Sitemap submitted for {target_url}!")

def main():
    print("Connecting to authenticated Firefox instance...")
    ws = F.connect()
    time.sleep(2)
    
    for url in TARGET_URLS:
        try:
            add_property_to_gsc(ws, url)
        except Exception as e:
            print(f"Error registering {url}: {e}")
            
    try:
        F.cmd(ws, "session.end", {}, timeout=5)
    except Exception:
        pass
    ws.close()
    print("\nALL GOOGLE SEARCH CONSOLE REGISTRATIONS COMPLETE!")

if __name__ == "__main__":
    main()
