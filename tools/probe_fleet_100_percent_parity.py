import urllib.request
import json
import time

FLEET_20 = [
    {"site_id": "site-1", "name": "LocalAgentStack", "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine"},
    {"site_id": "site-2", "name": "WorkationRadar", "url": "https://jibranpcccc.github.io/workationradar"},
    {"site_id": "site-3", "name": "OpenAgentStack", "url": "https://openagentstack.pages.dev"},
    {"site_id": "site-4", "name": "IndieStackAudit", "url": "https://indiestackaudit.pages.dev"},
    {"site_id": "site-5", "name": "VectorBench", "url": "https://vectorbench.pages.dev"},
    {"site_id": "site-6", "name": "NomadTreaty", "url": "https://nomadtreaty.pages.dev"},
    {"site_id": "site-7", "name": "WebhookWatch", "url": "https://webhookwatch.pages.dev"},
    {"site_id": "site-8", "name": "LocalDocPrivacy", "url": "https://localdocprivacy.pages.dev"},
    {"site_id": "site-9", "name": "FounderRunway", "url": "https://founderrunway.pages.dev"},
    {"site_id": "site-10", "name": "RAGInspect", "url": "https://raginspect.pages.dev"},
    {"site_id": "site-11", "name": "NomadPassportIndex", "url": "https://nomadpassportindex.pages.dev"},
    {"site_id": "site-12", "name": "SaaSUnitMath", "url": "https://saasunitmath.pages.dev"},
    {"site_id": "site-13", "name": "GrokLogTester", "url": "https://groklogtester.pages.dev"},
    {"site_id": "site-14", "name": "SOC2Ready", "url": "https://soc2ready.pages.dev"},
    {"site_id": "site-15", "name": "EORCalculator", "url": "https://eorcalculator.pages.dev"},
    {"site_id": "site-16", "name": "DevConfigHub", "url": "https://devconfighub.pages.dev"},
    {"site_id": "site-17", "name": "OpenCRMStack", "url": "https://opencrmstack.pages.dev"},
    {"site_id": "site-18", "name": "CIPipelineGraph", "url": "https://cipipelinegraph.pages.dev"},
    {"site_id": "site-19", "name": "GreekVisualizer", "url": "https://greekvisualizer.pages.dev"},
    {"site_id": "site-20", "name": "EdgeRuntimeHQ", "url": "https://edgeruntimehq.pages.dev"}
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

results = []
print("=" * 80)
print("PROBING 100% OF 20 FLEET PROPERTIES (ROOT, GSC HTML, INDEXNOW, SITEMAP, ROBOTS)")
print("=" * 80)

for site in FLEET_20:
    base = site["url"].rstrip("/")
    sid = site["site_id"]
    name = site["name"]
    
    # 1. Root
    t0 = time.time()
    try:
        req = urllib.request.Request(base + "/", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            root_code = r.status
            ttfb = int((time.time() - t0) * 1000)
    except Exception as e:
        root_code = f"ERR({e})"
        ttfb = -1

    # 2. GSC HTML
    try:
        req = urllib.request.Request(base + "/google6fe267a998c19a9a.html", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode("utf-8", errors="ignore").strip()
            gsc_code = "200 OK" if "google6fe267a998c19a9a" in body else f"MISMATCH({body[:10]})"
    except Exception as e:
        gsc_code = f"ERR({e})"

    # 3. IndexNow
    try:
        req = urllib.request.Request(base + "/8303260f1bf94264ac6d00aa93efde28.txt", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode("utf-8", errors="ignore").strip()
            inow_code = "200 OK" if "8303260f1bf94264ac6d00aa93efde28" in body else f"MISMATCH({body[:10]})"
    except Exception as e:
        inow_code = f"ERR({e})"

    # 4. Sitemap
    try:
        req = urllib.request.Request(base + "/sitemap.xml", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            sitemap_code = f"{r.status} ({len(r.read())}b)"
    except Exception as e:
        sitemap_code = f"ERR({e})"

    # 5. Robots
    try:
        req = urllib.request.Request(base + "/robots.txt", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            robots_code = f"{r.status} ({len(r.read())}b)"
    except Exception as e:
        robots_code = f"ERR({e})"

    print(f"{sid:7} | {name:18} | Root: {str(root_code):3} ({ttfb:4}ms) | GSC: {gsc_code:6} | IndexNow: {inow_code:6} | S: {sitemap_code:10} | R: {robots_code}")
    results.append({
        "site_id": sid,
        "name": name,
        "url": base,
        "root_code": root_code,
        "ttfb_ms": ttfb,
        "gsc": gsc_code,
        "indexnow": inow_code,
        "sitemap": sitemap_code,
        "robots": robots_code
    })
    time.sleep(0.5)

gsc_count = sum(1 for r in results if r["gsc"] == "200 OK")
inow_count = sum(1 for r in results if r["indexnow"] == "200 OK")
root_count = sum(1 for r in results if r["root_code"] == 200)

print("=" * 80)
print(f"FINAL AUDIT SCORECARD:")
print(f"  • Root URLs:                 {root_count}/20 ({root_count/20*100:.1f}%)")
print(f"  • Google Search Console:     {gsc_count}/20 ({gsc_count/20*100:.1f}%)")
print(f"  • Microsoft Bing / IndexNow: {inow_count}/20 ({inow_count/20*100:.1f}%)")
print("=" * 80)

# Save updated telemetry report
with open("reports/live_fleet_endpoint_audit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Updated reports/live_fleet_endpoint_audit.json successfully.")
