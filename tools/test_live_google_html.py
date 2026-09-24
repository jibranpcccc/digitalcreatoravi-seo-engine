import urllib.request
import json

with open('reports/live_fleet_endpoint_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0'}
for item in data:
    base = item['url'].rstrip('/')
    url = f"{base}/google6fe267a998c19a9a.html"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            code = resp.status
            body = resp.read().decode('utf-8', errors='ignore').strip()
            ok = 'OK' if 'google6fe267a998c19a9a' in body else f'BODY({body[:15]})'
    except Exception as e:
        ok = f'ERR({e})'
    print(f"{item['site_id']}: {ok}")
