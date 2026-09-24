import urllib.request
import json

with open('reports/live_fleet_endpoint_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0'}
verified_count = 0
total_count = len(data)

print(f"=== Probing IndexNow Key across all {total_count} live sites ===")
for item in data:
    u = item['url'].rstrip('/') + '/8303260f1bf94264ac6d00aa93efde28.txt'
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore').strip()
            if '8303260f1bf94264ac6d00aa93efde28' in content:
                status = 'VERIFIED (HTTP 200 OK)'
                verified_count += 1
            else:
                status = f'CONTENT_MISMATCH({content[:15]})'
    except Exception as e:
        status = f'ERR({e})'
    print(f"{item['site_id']} ({item['name']}) -> {status}")

print(f"\nFinal IndexNow Verification Score: {verified_count}/{total_count} ({(verified_count/total_count)*100:.1f}%)")
