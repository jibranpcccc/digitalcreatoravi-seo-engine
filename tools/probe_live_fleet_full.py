import urllib.request
import json
import time

with open('reports/live_fleet_endpoint_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

results = []
print("=== Probing All 20 Live Edge Properties (Root, Sitemap, Robots) ===")
for item in data:
    site_id = item['site_id']
    name = item['name']
    base_url = item['url'].rstrip('/')
    
    # 1. Root
    t0 = time.time()
    try:
        req = urllib.request.Request(base_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            root_code = resp.status
            ttfb = int((time.time() - t0) * 1000)
    except Exception as e:
        root_code = f"ERR({e})"
        ttfb = -1

    # 2. Sitemap
    sitemap_url = f"{base_url}/sitemap.xml"
    try:
        req = urllib.request.Request(sitemap_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            sitemap_code = resp.status
            sitemap_len = len(resp.read())
    except Exception as e:
        sitemap_code = f"ERR({e})"
        sitemap_len = 0

    # 3. Robots
    robots_url = f"{base_url}/robots.txt"
    try:
        req = urllib.request.Request(robots_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            robots_code = resp.status
            robots_len = len(resp.read())
    except Exception as e:
        robots_code = f"ERR({e})"
        robots_len = 0

    print(f"{site_id:7} | {name:18} | Root: {str(root_code):3} ({ttfb}ms) | Sitemap: {str(sitemap_code):3} ({sitemap_len}b) | Robots: {str(robots_code):3}")
    results.append({
        "site_id": site_id,
        "name": name,
        "url": base_url,
        "root_code": root_code,
        "ttfb_ms": ttfb,
        "sitemap_code": sitemap_code,
        "sitemap_bytes": sitemap_len,
        "robots_code": robots_code
    })

all_roots_ok = all(r['root_code'] == 200 for r in results)
all_sitemaps_ok = all(r['sitemap_code'] == 200 for r in results)
all_robots_ok = all(r['robots_code'] == 200 for r in results)

print(f"\nRoot Health: {'100% OK (20/20)' if all_roots_ok else 'Issues detected'}")
print(f"Sitemap Health: {'100% OK (20/20)' if all_sitemaps_ok else 'Issues detected'}")
print(f"Robots Health: {'100% OK (20/20)' if all_robots_ok else 'Issues detected'}")
