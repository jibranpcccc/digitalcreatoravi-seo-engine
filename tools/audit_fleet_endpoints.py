import urllib.request
import time
import json

SITES = [
    ('site-1', 'LocalAgentStack', 'https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/'),
    ('site-2', 'WorkationRadar', 'https://jibranpcccc.github.io/workationradar/'),
    ('site-3', 'OpenAgentStack', 'https://openagentstack.pages.dev/'),
    ('site-4', 'IndieStackAudit', 'https://indiestackaudit.pages.dev/'),
    ('site-5', 'VectorBench', 'https://vectorbench-hq.netlify.app/'),
    ('site-6', 'NomadTreaty', 'https://nomadtreaty.vercel.app/'),
    ('site-7', 'WebhookWatch', 'https://webhookwatch.vercel.app/'),
    ('site-8', 'LocalDocPrivacy', 'https://localdocprivacy.netlify.app/'),
    ('site-9', 'FounderRunway', 'https://site-9-inky.vercel.app/'),
    ('site-10', 'RAGInspect', 'https://raginspect.pages.dev/'),
    ('site-11', 'NomadPassportIndex', 'https://nomadpassportindex.netlify.app/'),
    ('site-12', 'SaaSUnitMath', 'https://site-12-taupe.vercel.app/'),
    ('site-13', 'GrokLogTester', 'https://groklogtester.pages.dev/'),
    ('site-14', 'SOC2Ready', 'https://site-14-sable.vercel.app/'),
    ('site-15', 'EORCalculator', 'https://site-15-ruby.vercel.app/'),
    ('site-16', 'DevConfigHub', 'https://site-16-indol.vercel.app/'),
    ('site-17', 'OpenCRMStack', 'https://opencrmstack.pages.dev/'),
    ('site-18', 'CIPipelineGraph', 'https://site-18-chi.vercel.app/'),
    ('site-19', 'GreekVisualizer', 'https://site-19-nine.vercel.app/'),
    ('site-20', 'EdgeRuntimeHQ', 'https://edgeruntimehq.pages.dev/')
]

INDEXNOW_KEY = '8303260f1bf94264ac6d00aa93efde28'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'}

print(f"{'Site':<8} | {'Brand':<18} | {'HTTP':<5} | {'TTFB':<7} | {'Sitemap':<7} | {'Robots':<6} | {'IndexNow Key':<12}")
print('-' * 75)

results = []

for sid, name, base_url in SITES:
    base = base_url.rstrip('/')
    
    # 1. Root
    t0 = time.time()
    try:
        req = urllib.request.Request(base_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            http_code = resp.status
            ttfb = int((time.time() - t0) * 1000)
    except Exception as e:
        http_code = 'ERR'
        ttfb = '-'
        
    # 2. Sitemap
    try:
        req = urllib.request.Request(f"{base}/sitemap.xml", headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            sm_code = resp.status
    except Exception:
        sm_code = 'ERR'
        
    # 3. Robots
    try:
        req = urllib.request.Request(f"{base}/robots.txt", headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            rb_code = resp.status
    except Exception:
        rb_code = 'ERR'
        
    # 4. IndexNow Key
    try:
        req = urllib.request.Request(f"{base}/{INDEXNOW_KEY}.txt", headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read().decode('utf-8', errors='ignore').strip()
            in_status = 'VERIFIED' if INDEXNOW_KEY in body else f'VAL({body[:8]})'
    except Exception:
        in_status = 'MISSING'
        
    ttfb_str = f"{ttfb}ms" if isinstance(ttfb, int) else ttfb
    print(f"{sid:<8} | {name:<18} | {http_code:<5} | {ttfb_str:<7} | {sm_code:<7} | {rb_code:<6} | {in_status:<12}")
    results.append({
        'site_id': sid, 'name': name, 'url': base_url,
        'http': http_code, 'ttfb': ttfb, 'sitemap': sm_code,
        'robots': rb_code, 'indexnow': in_status
    })

with open('reports/live_fleet_endpoint_audit.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print("\nSaved detailed audit to reports/live_fleet_endpoint_audit.json")
