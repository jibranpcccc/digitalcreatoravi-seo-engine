#!/usr/bin/env python3
"""
Free Backlink & Sitemap Indexing Dispatcher
Submits all 20 production sites, backlink hubs, and sitemaps to free search engine
indexing endpoints, XML-RPC ping services, and the IndexNow protocol.
"""

import os
import sys
import json
import sqlite3
import urllib.request
import urllib.parse
import xmlrpc.client
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")
INDEXNOW_KEY = "8303260f1bf94264ac6d00aa93efde28"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ping_google_sitemap(sitemap_url):
    encoded_url = urllib.parse.quote(sitemap_url, safe="")
    ping_url = f"https://www.google.com/ping?sitemap={encoded_url}"
    req = urllib.request.Request(ping_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return res.status
    except Exception as e:
        return str(e)

def ping_bing_sitemap(sitemap_url):
    encoded_url = urllib.parse.quote(sitemap_url, safe="")
    ping_url = f"https://www.bing.com/ping?sitemap={encoded_url}"
    req = urllib.request.Request(ping_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return res.status
    except Exception as e:
        return str(e)

def ping_pingomatic(title, url, rss_url):
    try:
        server = xmlrpc.client.ServerProxy("http://rpc.pingomatic.com/")
        res = server.weblogUpdates.extendedPing(title, url, rss_url, rss_url)
        return res
    except Exception as e:
        return str(e)

def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id")
    sites = [dict(r) for r in cursor.fetchall()]
    conn.close()

    print("=== FREE SEARCH ENGINE INDEXING & CRAWL DISPATCH PASS ===")
    print(f"Submitting sitemaps and hubs for {len(sites)} sites to Google, Bing, and Ping-O-Matic...\n")

    # 1. Master GitHub Pages Sitemap
    master_sitemap = "https://jibranpcccc.github.io/sitemap-tools.xml"
    print(f"[+] Pinging Master Sitemap: {master_sitemap}")
    g_res = ping_google_sitemap(master_sitemap)
    b_res = ping_bing_sitemap(master_sitemap)
    print(f"    -> Google: {g_res} | Bing: {b_res}")

    # 2. Ping-O-Matic for Master Tools Directory
    print("[+] Pinging Ping-O-Matic for Master Directory Hub...")
    pom_res = ping_pingomatic("Open Web Utilities & Empirical Benchmarks", "https://jibranpcccc.github.io/tools.html", "https://jibranpcccc.github.io/api/v1/tools.json")
    print(f"    -> Ping-O-Matic Response: {pom_res}")

    # 3. Individual Sites Sitemaps
    for idx, s in enumerate(sites, 1):
        sitemap_url = s["sitemap_url"]
        url = s["url"]
        rss_url = f"{url.rstrip('/')}/rss.xml"
        name = s["name"]

        print(f"[{idx:2d}/{len(sites)}] Pinging Indexers for {name}...")
        g_status = ping_google_sitemap(sitemap_url)
        b_status = ping_bing_sitemap(sitemap_url)
        print(f"       Google Sitemap Ping: {g_status}")
        print(f"       Bing Sitemap Ping  : {b_status}")
        time.sleep(0.5)

    print("\n=== ALL FREE INDEXING SUBMISSIONS COMPLETED ===")

if __name__ == "__main__":
    main()
