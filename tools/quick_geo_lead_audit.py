import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

targets = [
    {"name": "GoodSocials", "url": "https://goodsocials.co", "founder": "Pavel Kucherbaev", "x": "https://x.com/kucherbaev"},
    {"name": "Keiki", "url": "https://keiki.ai", "founder": "Nizar Abi Zaher", "x": "https://x.com/nizzyabi"},
    {"name": "Tadata", "url": "https://tadata.com", "founder": "Tori Seidenstein", "x": "https://x.com/toriseidenstein"},
]

results = []

for item in targets:
    t = item["url"]
    report = {
        "name": item["name"],
        "url": t,
        "founder": item["founder"],
        "x": item["x"],
        "schema_ok": False,
        "llms_ok": False,
        "robots_ok": False,
        "details": []
    }
    
    # 1. Homepage & Schema
    try:
        req = urllib.request.Request(t, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
            matches = re.findall(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
            if matches:
                report["schema_ok"] = True
                report["details"].append(f"Found {len(matches)} schema block(s)")
            else:
                report["schema_ok"] = False
                report["details"].append("ZERO JSON-LD schema blocks found")
    except Exception as e:
        report["details"].append(f"Homepage error: {e}")

    # 2. llms.txt
    try:
        req = urllib.request.Request(t + "/llms.txt", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
            if r.status == 200:
                report["llms_ok"] = True
                report["details"].append("llms.txt is PRESENT")
    except Exception as e:
        report["llms_ok"] = False
        report["details"].append("llms.txt is MISSING (404)")

    # 3. robots.txt
    try:
        req = urllib.request.Request(t + "/robots.txt", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
            content = r.read().decode("utf-8", errors="ignore")
            mentions_ai = any(bot in content for bot in ["GPTBot", "PerplexityBot", "ClaudeBot"])
            report["robots_ok"] = mentions_ai
            report["details"].append(f"Explicit AI bot rules: {mentions_ai}")
    except Exception as e:
        report["details"].append("robots.txt missing/error")

    results.append(report)

print("=== FINAL GEO AUDIT RESULTS ===")
for r in results:
    score = 100
    if not r["schema_ok"]: score -= 40
    if not r["llms_ok"]: score -= 35
    if not r["robots_ok"]: score -= 15
    print(f"[{r['name']}] ({r['url']}) | Founder: {r['founder']} ({r['x']})")
    print(f"  GEO Score: {score}/100")
    print(f"  Issues: {', '.join(r['details'])}")
    print("-" * 50)
