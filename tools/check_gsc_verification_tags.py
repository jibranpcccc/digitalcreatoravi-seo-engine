import urllib.request
import re
import json

with open('reports/live_fleet_endpoint_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"{'Site':<8} | {'Brand':<18} | {'Google Verification Meta'}")
print('-' * 70)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
for item in data:
    url = item['url']
    sid = item['site_id']
    name = item['name']
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.findall(r'<meta[^>]+name=["\']google-site-verification["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
            if not m:
                m = re.findall(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']google-site-verification["\']', html, re.I)
            v = m[0] if m else 'NONE (or HTML file/DNS)'
    except Exception as e:
        v = f'ERR({e})'
    print(f"{sid:<8} | {name:<18} | {v}")
