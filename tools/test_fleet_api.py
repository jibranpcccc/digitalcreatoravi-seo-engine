#!/usr/bin/env python3
import urllib.request
import json

endpoints = [
    ("/api/fleet", "sites"),
    ("/api/stats", "total_hits"),
    ("/api/pending-posts", "posts"),
    ("/api/indexed-pages", "pages"),
    ("/api/search-queries", "queries"),
    ("/api/alerts", "alerts")
]

print("=== COMMAND CENTER ENDPOINTS VERIFICATION ===")
for path, key in endpoints:
    url = f"http://localhost:8088{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
            val = data.get(key)
            count = len(val) if isinstance(val, list) else val
            print(f"  [200 OK] {path:20} -> {key}: {count}")
    except Exception as e:
        print(f"  [ERR]    {path:20} -> {e}")
