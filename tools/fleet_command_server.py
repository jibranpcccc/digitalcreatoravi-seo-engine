#!/usr/bin/env python3
"""
Unified Fleet Master & Traffic Command Center Server
Serves the executive Webmaster + Traffic Analytics Dashboard on http://localhost:8088
Collects incoming beacon hits from all websites in real time and stores in SQLite.
"""

import os
import sys
import json
import sqlite3
import subprocess
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PORT = 8088
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DASHBOARD_DIR = os.path.join(ROOT_DIR, "dashboard")
DB_PATH = os.path.join(DATA_DIR, "fleet_telemetry.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class FleetServerHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/dashboard", "/index.html"):
            index_file = os.path.join(DASHBOARD_DIR, "index.html")
            if os.path.exists(index_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                with open(index_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Dashboard HTML not found")
            return

        if path == "/api/fleet":
            conn = get_db()
            c = conn.cursor()
            sites = [dict(row) for row in c.execute("SELECT * FROM sites ORDER BY id ASC").fetchall()]
            
            # Count hits per site
            for s in sites:
                cnt = c.execute("SELECT COUNT(*) FROM traffic_hits WHERE site_id=?", (s["id"],)).fetchone()[0]
                s["total_hits"] = cnt
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "sites": sites}).encode("utf-8"))
            return

        if path == "/api/stats":
            conn = get_db()
            c = conn.cursor()
            total_hits = c.execute("SELECT COUNT(*) FROM traffic_hits").fetchone()[0]

            # By site
            by_site = {}
            for row in c.execute("SELECT site_id, COUNT(*) as cnt FROM traffic_hits GROUP BY site_id").fetchall():
                by_site[row["site_id"]] = row["cnt"]

            # By source
            by_source = {"organic": 0, "direct": 0, "referral": 0, "social": 0}
            for row in c.execute("SELECT referrer FROM traffic_hits").fetchall():
                ref = (row["referrer"] or "").lower()
                if ref in ("direct", "", "none"):
                    by_source["direct"] += 1
                elif any(s in ref for s in ["google.", "bing.", "yahoo.", "duckduckgo."]):
                    by_source["organic"] += 1
                elif any(s in ref for s in ["t.co", "twitter.com", "x.com", "linkedin.com", "reddit.com"]):
                    by_source["social"] += 1
                else:
                    by_source["referral"] += 1

            # Recent hits
            recent_hits = [dict(row) for row in c.execute("SELECT * FROM traffic_hits ORDER BY id DESC LIMIT 50").fetchall()]
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "total_hits": total_hits,
                "by_site": by_site,
                "by_source": by_source,
                "recent_hits": recent_hits
            }).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"

        try:
            payload = json.loads(post_body)
        except Exception:
            payload = {}

        if path in ("/api/track", "/api/hit"):
            site = payload.get("site", "unknown")
            # Map hostname to site_id if needed
            site_map = {
                "jibranpcccc.github.io": "site-1",
                "openagentstack.pages.dev": "site-3",
                "indiestackaudit.pages.dev": "site-4",
                "vectorbench-hq.netlify.app": "site-5",
                "nomadtreaty.vercel.app": "site-6",
                "webhookwatch.vercel.app": "site-7",
                "localdocprivacy.netlify.app": "site-8"
            }
            site_id = site_map.get(site, site)
            page_path = payload.get("path", "/")
            full_url = payload.get("url", f"https://{site}{page_path}")
            referrer = payload.get("ref") or payload.get("referrer") or self.headers.get("Referer", "direct")
            user_agent = self.headers.get("User-Agent", "Unknown")
            device = "Mobile" if any(m in user_agent.lower() for m in ["mobile", "android", "iphone"]) else "Desktop"
            country = payload.get("country", "US")

            conn = get_db()
            c = conn.cursor()
            c.execute("""
            INSERT INTO traffic_hits (site_id, path, full_url, referrer, user_agent, device, country)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (site_id, page_path, full_url, referrer, user_agent, device, country))
            hit_id = c.lastrowid
            conn.commit()
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "hit_id": hit_id}).encode("utf-8"))
            return

        if path == "/api/simulate-hit":
            import random
            sites = ["site-1", "site-2", "site-3", "site-4", "site-5", "site-6", "site-7", "site-8"]
            refs = ["https://www.google.com/", "https://www.bing.com/", "direct", "https://news.ycombinator.com/", "https://t.co/"]
            countries = ["US", "DE", "GB", "CA", "FR", "ES", "NL", "JP"]
            
            chosen_site = random.choice(sites)
            conn = get_db()
            c = conn.cursor()
            c.execute("""
            INSERT INTO traffic_hits (site_id, path, full_url, referrer, user_agent, device, country)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (chosen_site, "/guide/", f"https://{chosen_site}/guide/", random.choice(refs), "Chrome/Desktop", "Desktop", random.choice(countries)))
            conn.commit()
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "simulated_site": chosen_site}).encode("utf-8"))
            return

        if path == "/api/ping-indexnow":
            # Run ping_indexnow.py asynchronously
            cmd = [sys.executable, os.path.join(ROOT_DIR, "tools", "ping_indexnow.py")]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "output": res.stdout}).encode("utf-8"))
            return

        if path == "/api/audit-all":
            # Run daily_seo_auditor.py asynchronously
            cmd = [sys.executable, os.path.join(ROOT_DIR, "tools", "daily_seo_auditor.py")]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "output": res.stdout}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), FleetServerHandler)
    print(f"================================================================")
    print(f"⚡ FLEET COMMAND CENTER & TELEMETRY HUB RUNNING ON:")
    print(f"👉 http://localhost:{PORT}/")
    print(f"================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Fleet Server...")
        server.server_close()

if __name__ == "__main__":
    run()

