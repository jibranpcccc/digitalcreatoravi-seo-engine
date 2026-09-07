---
name: search-engine-indexer
description: "Multi-protocol fast indexing engine for websites, sitemaps, and backlinks. Broadcasts crawling signals across Google WebSub (PubSubHubbub HTTP 204), Microsoft Bing IndexNow (HTTP 200), Central IndexNow API for Yandex/Seznam (HTTP 200), Blo.gs XML-RPC network, Twingly European/global search indexer, Ping-O-Matic, and Wayback Machine. Submits both website URLs and live backlink assets for immediate crawler discovery with zero accounts required. Use when user says 'index', 'indexing', 'submit sitemap', 'ping', 'index backlinks', 'fast index', 'XML-RPC ping', 'blo.gs', 'indexnow', or 'get indexed'."
user-invocable: true
argument-hint: "<url_sitemap_or_backlink_list>"
license: MIT
metadata:
  version: "1.0.0"
  category: search-engine-indexing
---

# ⚡ Search Engine Indexer: Multi-Protocol Crawl & Indexing Engine

A high-performance indexing automation system that broadcasts newly published web pages, sitemaps, RSS feeds, and backlink URLs across 5 global indexing protocols simultaneously to trigger rapid crawler discovery and indexation.

---

## 📡 The 5 Global Indexing Protocols

| Protocol | Endpoint | Status Response | Mechanics & Crawl Behavior |
| :--- | :--- | :--- | :--- |
| **Google WebSub (PubSubHubbub)** | `https://pubsubhubbub.appspot.com/` | `HTTP 204 (No Content)` | **Googlebot Priority Crawl**: Google's official hub for RSS/Atom feed subscriptions. Schedules Googlebot to immediately fetch updated content feeds. |
| **Microsoft Bing IndexNow** | `https://www.bing.com/indexnow` | `HTTP 200 / 202` | **Bingbot Queue Dispatched**: Microsoft's dedicated fast-indexing protocol. Bypasses sitemap crawl cycles; alerts Bingbot within seconds. |
| **Central IndexNow API** | `https://api.indexnow.org/indexnow` | `HTTP 200 / 202` | **Global Engine Replication**: Replicates crawl signals across participating search engines (Yandex, Seznam.cz, Naver). |
| **Blo.gs XML-RPC** | `http://ping.blo.gs/` | `HTTP 200 ('Succeeded.')` | **Automattic / WordPress Stream**: Public ping stream polled continuously by global search engine spiders and aggregators. |
| **Twingly XML-RPC** | `http://rpc.twingly.com/` | `HTTP 200 ('Thanks for the ping.')` | **European & International Crawlers**: Real-time blog and news search indexer. |

---

## 🚫 Deprecated Protocols (Do NOT Use)

1. **Google Sitemap Ping (`google.com/ping?sitemap=...`)**:
   - **Status**: Returns `HTTP 404 (Sitemaps ping is deprecated)`.
   - **Reason**: Google officially retired this endpoint in December 2023.
   - **Replacement**: Use **Google WebSub (PubSubHubbub)** with RSS/Atom feeds, Google Search Console URL Inspection API, or IndexNow where supported.
2. **Bing Sitemap Ping (`bing.com/ping?sitemap=...`)**:
   - **Status**: Returns `HTTP 410 (Gone)`.
   - **Reason**: Bing officially replaced sitemap GET pings with **IndexNow** (`bing.com/indexnow`).

---

## 💻 Standalone Python Indexing Implementations

### 1. Google WebSub (PubSubHubbub) POST
```python
import urllib.request
import urllib.parse

def ping_google_websub(rss_url):
    data = urllib.parse.urlencode({
        "hub.mode": "publish",
        "hub.url": rss_url
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://pubsubhubbub.appspot.com/",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=12) as res:
        return res.status  # Returns 204 on success
```

### 2. Microsoft Bing IndexNow API
```python
import json
import urllib.request

def ping_bing_indexnow(host, url_list, key):
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": url_list
    }
    req = urllib.request.Request(
        "https://www.bing.com/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=12) as res:
        return res.status  # Returns 200 or 202
```

### 3. Blo.gs & Twingly XML-RPC Pings
```python
import socket
import xmlrpc.client

socket.setdefaulttimeout(12.0)

def ping_xmlrpc(title, url):
    # 1. Blo.gs
    try:
        server = xmlrpc.client.ServerProxy("http://ping.blo.gs/")
        b_res = server.weblogUpdates.ping(title, url)
    except Exception as e:
        b_res = str(e)

    # 2. Twingly
    try:
        twingly = xmlrpc.client.ServerProxy("http://rpc.twingly.com/")
        t_res = twingly.weblogUpdates.ping(title, url)
    except Exception as e:
        t_res = str(e)

    return b_res, t_res
```

---

## ⚡ 1-Click Execution Commands

```bash
# Run full 5-protocol indexing pass across all 20 production sites + master hubs
python tools/master_search_engine_indexing_suite.py

# Broadcast XML-RPC pings across Blo.gs and Twingly for all verified backlink hubs
python tools/broadcast_all_backlinks_xmlrpc.py
```
