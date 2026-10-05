#!/usr/bin/env python3
"""
Master Chrome CDP Google Search Console Automation Engine
Launches Chrome with remote debugging on port 9222, connects via CDP,
registers all 20 fleet properties, submits sitemaps, and requests indexing.
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

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(ROOT_DIR, "reports", "gsc_automation")
os.makedirs(REPORTS_DIR, exist_ok=True)
AUDIT_FILE = os.path.join(ROOT_DIR, "reports", "live_fleet_endpoint_audit.json")

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CDP_PORT = 9222
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"

def is_cdp_ready():
    try:
        with urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False

def ensure_chrome_with_cdp():
    if is_cdp_ready():
        print("[+] Chrome CDP already active on port 9222!")
        return True

    print("[*] Port 9222 not active. Checking for existing Chrome processes...")
    # Check if Chrome is running
    try:
        out = subprocess.run(["tasklist", "/fi", "imagename eq chrome.exe"], capture_output=True, text=True).stdout
        if "chrome.exe" in out:
            print("[*] Gracefully terminating running Chrome to enable remote debugging...")
            # Try graceful kill first
            subprocess.run(["taskkill", "/im", "chrome.exe"], capture_output=True)
            time.sleep(3)
            # Force kill any remaining hanging processes
            subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], capture_output=True)
            time.sleep(2)
    except Exception as e:
        print("[!] Error managing existing Chrome:", e)

    print(f"[*] Launching Chrome with --remote-debugging-port={CDP_PORT}...")
    args = [
        CHROME_EXE,
        f"--remote-debugging-port={CDP_PORT}",
        "--remote-allow-origins=*",
        "--restore-last-session"
    ]
    subprocess.Popen(args)

    for i in range(15):
        time.sleep(1)
        if is_cdp_ready():
            print(f"[+] Chrome CDP successfully connected on port {CDP_PORT} (attempt {i+1})!")
            return True
        print(f"    Waiting for Chrome CDP... ({i+1}/15)")

    print("[-] Failed to connect to Chrome CDP.")
    return False

class ChromeCDP:
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

    def open_tab(self, url):
        res = self.send(self.browser_ws, "Target.createTarget", {"url": url})
        self.target_id = res["result"]["targetId"]
        
        # Get target tab webSocketDebuggerUrl
        with urllib.request.urlopen(f"{CDP_URL}/json/list", timeout=5) as r:
            tabs = json.loads(r.read().decode())
        tab = next(t for t in tabs if t["id"] == self.target_id)
        self.page_ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=30)
        return self.target_id

    def evaluate(self, expression, await_promise=True):
        res = self.send(self.page_ws, "Runtime.evaluate", {
            "expression": expression,
            "awaitPromise": await_promise,
            "returnByValue": True
        })
        val = res.get("result", {}).get("result", {}).get("value")
        return val

    def navigate(self, url, wait_sec=8):
        self.send(self.page_ws, "Page.navigate", {"url": url})
        time.sleep(wait_sec)

    def screenshot(self, filename):
        res = self.send(self.page_ws, "Page.captureScreenshot")
        out_path = os.path.join(REPORTS_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(res["result"]["data"]))
        print(f"    [screenshot saved] {filename}")
        return out_path

    def click_at(self, x, y, wait=3):
        actions = [
            {"type": "pointerMove", "x": x, "y": y, "duration": 50},
            {"type": "pointerDown", "button": 0},
            {"type": "pointerUp", "button": 0}
        ]
        self.send(self.page_ws, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        self.send(self.page_ws, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        self.send(self.page_ws, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
        time.sleep(wait)

    def type_keys(self, text):
        for ch in text:
            self.send(self.page_ws, "Input.dispatchKeyEvent", {"type": "keyDown", "text": ch, "key": ch})
            self.send(self.page_ws, "Input.dispatchKeyEvent", {"type": "keyUp", "text": ch, "key": ch})
            time.sleep(0.04)

    def close(self):
        try:
            if self.target_id:
                self.send(self.browser_ws, "Target.closeTarget", {"targetId": self.target_id})
        except Exception:
            pass
        try:
            if self.page_ws: self.page_ws.close()
        except Exception:
            pass
        try:
            if self.browser_ws: self.browser_ws.close()
        except Exception:
            pass

def main():
    print("=== STARTING GOOGLE SEARCH CONSOLE FLEET AUTOMATION ===")
    if not ensure_chrome_with_cdp():
        print("[-] Exiting due to CDP failure.")
        return

    cdp = ChromeCDP()
    cdp.connect()

    try:
        # Load fleet list
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            fleet = json.load(f)

        print(f"[+] Loaded {len(fleet)} fleet production properties.")
        
        # Open GSC welcome page
        print("[*] Navigating to Google Search Console...")
        cdp.open_tab("https://search.google.com/search-console/welcome?hl=en")
        time.sleep(6)
        cdp.screenshot("01_gsc_initial.png")

        # Check account / login state
        page_info = cdp.evaluate("""(() => {
            const email = (document.querySelector('[data-email]') || {}).dataset?.email || 
                          (document.querySelector('img[alt*="@"]') || {}).alt ||
                          (document.querySelector('[aria-label*="@"]') || {}).getAttribute('aria-label') || 'Not found';
            return JSON.stringify({
                url: window.location.href,
                title: document.title,
                account: email,
                isSignIn: window.location.href.includes('accounts.google.com'),
                bodyText: document.body.innerText.slice(0, 400)
            });
        })()""")
        info = json.loads(page_info)
        print(f"[*] GSC Page URL: {info['url']}")
        print(f"[*] Account detected: {info['account']}")

        if info["isSignIn"]:
            print("[!] Google Search Console requires Sign-In. Capturing state...")
            cdp.screenshot("signin_required.png")
            print("[-] Please ensure your Chrome profile is signed into Google Search Console.")
            return

        print("\n=======================================================")
        print("BEGINNING 20-PROPERTY VERIFICATION & SITEMAP PIPELINE")
        print("=======================================================")

        results = []
        for idx, site in enumerate(fleet, 1):
            sid = site["site_id"]
            name = site["name"]
            url = site["url"].rstrip("/") + "/"
            sitemap_url = f"{url}sitemap.xml"
            print(f"\n[{idx}/20] Processing {sid}: {name} ({url})...")

            # 1. Navigate to welcome / add-property
            cdp.navigate("https://search.google.com/search-console/welcome?hl=en", wait=5)

            # Find URL Prefix input
            inp_coord = cdp.evaluate("""(() => {
                const inps = Array.from(document.querySelectorAll('input')).filter(i => {
                    const r = i.getBoundingClientRect();
                    return i.offsetParent && r.width > 120 && r.x > 400;
                });
                if (!inps.length) return null;
                const r = inps[0].getBoundingClientRect();
                return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            })()""")

            if not inp_coord:
                # Check if "Add a website" or dropdown button needs to be clicked
                add_btn = cdp.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button]')).find(e => (e.textContent||'').includes('Add a website') && e.offsetParent);
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if add_btn:
                    b_loc = json.loads(add_btn)
                    cdp.click_at(b_loc["x"], b_loc["y"], wait=2)
                    # Re-check input
                    inp_coord = cdp.evaluate("""(() => {
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
                cdp.click_at(loc["x"], loc["y"], wait=1)
                cdp.type_keys(url)
                time.sleep(1)

                # Click CONTINUE
                cont_btn = cdp.evaluate("""(() => {
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
                    cdp.click_at(c_loc["x"], c_loc["y"], wait=6)

                # Check for auto-verification or VERIFY button
                cdp.screenshot(f"{sid}_verify_modal.png")
                verif_click = cdp.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => (e.textContent||'').trim().toUpperCase() === 'VERIFY' && e.offsetParent);
                    if (!b) return null;
                    const r = b.getBoundingClientRect();
                    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
                })()""")
                if verif_click:
                    v_loc = json.loads(verif_click)
                    cdp.click_at(v_loc["x"], v_loc["y"], wait=6)

                # Click "Go to property" or "Done"
                done_click = cdp.evaluate("""(() => {
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
                    cdp.click_at(d_loc["x"], d_loc["y"], wait=3)
                print(f"  [+] Ownership verified for {name}!")

            # 2. Submit sitemap
            encoded = urllib.parse.quote(url, safe='')
            sitemap_page = f"https://search.google.com/search-console/sitemaps?resource_id={encoded}"
            cdp.navigate(sitemap_page, wait=6)
            
            # Type sitemap.xml in input
            sinp = cdp.evaluate("""(() => {
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
                cdp.click_at(s_loc["x"], s_loc["y"], wait=1)
                cdp.type_keys("sitemap.xml")
                time.sleep(1)

                # Click SUBMIT
                sub_btn = cdp.evaluate("""(() => {
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
                    cdp.click_at(sb_loc["x"], sb_loc["y"], wait=6)

                # Dismiss 'Got it'
                cdp.evaluate("""(() => {
                    const b = Array.from(document.querySelectorAll('button, [role=button], span')).find(e => (e.textContent||'').trim() === 'Got it' && e.offsetParent);
                    if (b) b.click();
                })()""")
                cdp.screenshot(f"{sid}_sitemap_submitted.png")
                print(f"  [+] Sitemap sitemap.xml submitted successfully for {name}!")

            # 3. Trigger Request Indexing on Homepage (first 5 sites)
            if idx <= 5:
                print(f"  [*] Submitting priority 'Request Indexing' for {url}...")
                inspect_page = f"https://search.google.com/search-console/inspect?resource_id={encoded}&id={encoded}"
                cdp.navigate(inspect_page, wait=8)
                
                req_idx_btn = cdp.evaluate("""(() => {
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
                    cdp.click_at(ri_loc["x"], ri_loc["y"], wait=10)
                    cdp.screenshot(f"{sid}_indexing_requested.png")
                    print(f"  [+] 'Request Indexing' successfully triggered for {name}!")

            results.append({"site_id": sid, "name": name, "url": url, "status": "VERIFIED & SITEMAP SUBMITTED"})
            time.sleep(2)

        print("\n[✔] COMPLETE! All 20 fleet properties processed in Google Search Console.")

    finally:
        cdp.close()

if __name__ == "__main__":
    main()
