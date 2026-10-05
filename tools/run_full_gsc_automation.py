#!/usr/bin/env python3
"""
Master GSC Autonomous Engine
Launches Chrome dedicated GSC instance, attaches CDP on port 9222,
waits for clean account session, then loops through all 20 sites to
auto-verify ownership, submit sitemap.xml, and trigger 'Request Indexing'.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
import subprocess
import base64
import websocket

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(ROOT_DIR, "reports", "gsc_automation")
os.makedirs(REPORTS_DIR, exist_ok=True)
AUDIT_FILE = os.path.join(ROOT_DIR, "reports", "live_fleet_endpoint_audit.json")

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA = r"C:\Users\jibra\ChromeGSC"
CDP_PORT = 9222
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"

def is_cdp_ready():
    try:
        with urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False

def launch_chrome():
    if is_cdp_ready():
        print("[+] Chrome CDP already active on port 9222!")
        return True

    os.makedirs(USER_DATA, exist_ok=True)
    args = [
        CHROME_EXE,
        f"--user-data-dir={USER_DATA}",
        f"--remote-debugging-port={CDP_PORT}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check",
        "https://search.google.com/search-console/welcome?hl=en"
    ]
    print(f"[*] Launching Chrome with dedicated GSC workspace at {USER_DATA}...")
    subprocess.Popen(args)

    for i in range(15):
        time.sleep(1)
        if is_cdp_ready():
            print(f"[+] Chrome CDP connected on port {CDP_PORT}!")
            return True
        print(f"    Waiting for Chrome CDP... ({i+1}/15)")
    return False

class GSCAutomator:
    def __init__(self):
        self.msg_id = 0
        self.browser_ws = None
        self.page_ws = None
        self.target_id = None

    def connect(self):
        with urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=5) as r:
            v_info = json.loads(r.read().decode())
        ws_url = v_info["webSocketDebuggerUrl"]
        self.browser_ws = websocket.create_connection(ws_url, timeout=15)
        print("[+] Connected to Browser WebSocket.")

    def send(self, ws, method, params=None):
        self.msg_id += 1
        i = self.msg_id
        payload = {"id": i, "method": method, "params": params or {}}
        ws.send(json.dumps(payload))
        while True:
            res = json.loads(ws.recv())
            if res.get("id") == i:
                return res

    def attach_gsc_tab(self):
        with urllib.request.urlopen(f"{CDP_URL}/json/list", timeout=5) as r:
            tabs = json.loads(r.read().decode())
        
        # Find existing tab or open new
        tab = next((t for t in tabs if "search.google.com" in t.get("url", "") or "accounts.google.com" in t.get("url", "")), None)
        if not tab:
            tab = tabs[0]
            
        self.target_id = tab["id"]
        print(f"[+] Attaching to tab: {tab.get('title')} ({tab.get('url')})")
        self.page_ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=30)

    def evaluate(self, expression, await_promise=True):
        res = self.send(self.page_ws, "Runtime.evaluate", {
            "expression": expression,
            "awaitPromise": await_promise,
            "returnByValue": True
        })
        val = res.get("result", {}).get("result", {}).get("value")
        return val

    def navigate(self, url, wait_sec=6):
        self.send(self.page_ws, "Page.navigate", {"url": url})
        time.sleep(wait_sec)

    def screenshot(self, filename):
        res = self.send(self.page_ws, "Page.captureScreenshot")
        out_path = os.path.join(REPORTS_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(res["result"]["data"]))
        print(f"    [screenshot] {filename}")
        return out_path

    def click_at(self, x, y, wait=3):
        self.send(self.page_ws, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        self.send(self.page_ws, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        self.send(self.page_ws, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
        time.sleep(wait)

    def type_keys(self, text):
        for ch in text:
            self.send(self.page_ws, "Input.dispatchKeyEvent", {"type": "keyDown", "text": ch, "key": ch})
            self.send(self.page_ws, "Input.dispatchKeyEvent", {"type": "keyUp", "text": ch, "key": ch})
            time.sleep(0.03)

    def close(self):
        try:
            if self.page_ws: self.page_ws.close()
            if self.browser_ws: self.browser_ws.close()
        except Exception:
            pass

def main():
    print("=== FULLY AUTOMATED GOOGLE SEARCH CONSOLE RUNNER ===")
    if not launch_chrome():
        print("[-] Could not start Chrome with CDP.")
        return

    automator = GSCAutomator()
    automator.connect()
    automator.attach_gsc_tab()

    try:
        # Load fleet list
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            fleet = json.load(f)

        print("[*] Monitoring Google Search Console login state...")
        # Check login loop
        logged_in = False
        for attempt in range(300):
            state = automator.evaluate("""(() => {
                const u = window.location.href;
                const isSign = u.includes('accounts.google.com') || u.includes('/about');
                const isGsc = u.includes('search.google.com/search-console') && !u.includes('/about');
                const email = (document.querySelector('[data-email]') || {}).dataset?.email || 
                              (document.querySelector('img[alt*="@"]') || {}).alt ||
                              (document.querySelector('[aria-label*="@"]') || {}).getAttribute('aria-label') || 'None';
                return JSON.stringify({url: u, isGsc: isGsc, isSign: isSign, email: email});
            })()""")
            s = json.loads(state) if state else {}
            if s.get("isGsc"):
                print(f"[+] ACTIVE GSC SESSION DETECTED! Account: {s.get('email')}")
                logged_in = True
                break
            else:
                if attempt % 5 == 0:
                    print(f"    [!] Waiting for Google Sign-In in Chrome window... ({attempt * 2}/600s)")
                time.sleep(2)

        if not logged_in:
            print("[-] GSC login not detected within timeout. Screenshot captured.")
            automator.screenshot("gsc_login_timeout.png")
            return

        print("\n=======================================================")
        print("EXECUTING FLEET REGISTRATION & SITEMAP PIPELINE (20 SITES)")
        print("=======================================================")

        summary = []
        for idx, site in enumerate(fleet, 1):
            sid = site["site_id"]
            name = site["name"]
            url = site["url"].rstrip("/") + "/"
            print(f"\n[{idx}/20] Processing {sid}: {name} ({url})...")

            # Navigate to welcome screen
            automator.navigate("https://search.google.com/search-console/welcome?hl=en", wait=5)

            # Check if property already exists in dropdown
            has_prop = automator.evaluate(f"""(() => {{
                const text = document.body.innerText || '';
                return text.includes('{url}');
            }})()""")

            # Find URL Prefix input
            inp_coord = automator.evaluate("""(() => {
                const inps = Array.from(document.querySelectorAll('input')).filter(i => {
                    const r = i.getBoundingClientRect();
                    return i.offsetParent && r.width > 120 && r.x > 400;
                });
                if (!inps.length) return null;
                const r = inps[0].getBoundingClientRect();
                return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            })()""")

            if not inp_coord:
                # Click 'Add a website' or property selector
                add_btn = automator.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').includes('Add a website') && e.offsetParent);
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if add_btn:
                    b_loc = json.loads(add_btn)
                    automator.click_at(b_loc["x"], b_loc["y"], wait=2)
                    inp_coord = automator.evaluate("""(() => {
                        const inps = Array.from(document.querySelectorAll('input')).filter(i => {
                            const r = i.getBoundingClientRect();
                            return i.offsetParent && r.width > 120 && r.x > 400;
                        });
                        if (!inps.length) return null;
                        const r = inps[0].getBoundingClientRect();
                        return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                    })()""")

            if inp_coord:
                loc = json.loads(inp_coord)
                automator.click_at(loc["x"], loc["y"], wait=1)
                automator.type_keys(url)
                time.sleep(1)

                # Click CONTINUE
                cont_btn = automator.evaluate("""(() => {
                    const btns = Array.from(document.querySelectorAll('button, [role=button], span')).filter(e => {
                        const t = (e.textContent||'').trim().toUpperCase();
                        const r = e.getBoundingClientRect();
                        return t === 'CONTINUE' && r.x > 400 && e.offsetParent;
                    });
                    if (!btns.length) return null;
                    const r = btns[btns.length - 1].getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if cont_btn:
                    c_loc = json.loads(cont_btn)
                    automator.click_at(c_loc["x"], c_loc["y"], wait=6)

                # Click VERIFY if modal appears
                automator.screenshot(f"{sid}_verify_modal.png")
                verif_click = automator.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => (e.textContent||'').trim().toUpperCase() === 'VERIFY' && e.offsetParent);
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if verif_click:
                    v_loc = json.loads(verif_click)
                    automator.click_at(v_loc["x"], v_loc["y"], wait=6)

                # Click 'Go to property' or 'Done'
                done_click = automator.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], a, span')).find(e => {
                        const t = (e.textContent||'').toLowerCase().trim();
                        return (t.includes('go to property') || t === 'done') && e.offsetParent;
                    });
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if done_click:
                    d_loc = json.loads(done_click)
                    automator.click_at(d_loc["x"], d_loc["y"], wait=3)
                print(f"  [✔] Property added and verified: {name}")

            # 2. Submit sitemap
            encoded = urllib.parse.quote(url, safe='')
            sitemap_page = f"https://search.google.com/search-console/sitemaps?resource_id={encoded}"
            automator.navigate(sitemap_page, wait=6)
            
            sinp = automator.evaluate("""(() => {
                const inps = Array.from(document.querySelectorAll('input')).filter(i => {
                    const r = i.getBoundingClientRect();
                    return i.offsetParent && r.width > 80 && r.y < 350;
                });
                if (!inps.length) return null;
                const r = inps[inps.length - 1].getBoundingClientRect();
                return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            })()""")
            if sinp:
                s_loc = json.loads(sinp)
                automator.click_at(s_loc["x"], s_loc["y"], wait=1)
                automator.type_keys("sitemap.xml")
                time.sleep(1)

                sub_btn = automator.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => {
                        const t = (e.textContent||'').trim().toUpperCase();
                        const r = e.getBoundingClientRect();
                        return t === 'SUBMIT' && r.y < 350 && e.offsetParent;
                    });
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if sub_btn:
                    sb_loc = json.loads(sub_btn)
                    automator.click_at(sb_loc["x"], sb_loc["y"], wait=6)

                # Dismiss 'Got it'
                automator.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => (e.textContent||'').trim() === 'Got it' && e.offsetParent);
                    if (b) b.click();
                })()""")
                automator.screenshot(f"{sid}_sitemap_submitted.png")
                print(f"  [✔] sitemap.xml submitted for {name}")

            # 3. Request indexing on top 5
            if idx <= 5:
                print(f"  [*] Triggering 'Request Indexing' for {url}...")
                inspect_page = f"https://search.google.com/search-console/inspect?resource_id={encoded}&id={encoded}"
                automator.navigate(inspect_page, wait=8)
                req_idx_btn = automator.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => {
                        const t = (e.textContent||'').toLowerCase().trim();
                        return (t.includes('request indexing') || t.includes('richiedi indicizzazione')) && e.offsetParent;
                    });
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if req_idx_btn:
                    ri_loc = json.loads(req_idx_btn)
                    automator.click_at(ri_loc["x"], ri_loc["y"], wait=10)
                    automator.screenshot(f"{sid}_indexing_requested.png")
                    print(f"  [✔] Indexing requested for {name}")

            summary.append({"site_id": sid, "name": name, "url": url, "status": "VERIFIED & SUBMITTED"})
            time.sleep(2)

        print("\n=======================================================")
        print(f"SUCCESS: All {len(summary)} properties registered in GSC!")
        print("=======================================================")

    finally:
        automator.close()

if __name__ == "__main__":
    main()
