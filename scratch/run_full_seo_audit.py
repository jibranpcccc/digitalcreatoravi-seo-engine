import urllib.request
import urllib.parse
import re
import json
import time

FLEET = [
    {"id": "site-1", "name": "LocalAgentStack", "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/", "sample": "hardware/rtx-5090-vs-4090-local-llm-benchmark/"},
    {"id": "site-2", "name": "WorkationRadar", "url": "https://jibranpcccc.github.io/workationradar/", "sample": "space/roma-norte-creator-haven-cdmx/"},
    {"id": "site-3", "name": "OpenAgentStack", "url": "https://openagentstack.pages.dev/", "sample": "mcp/mcp-server-docker-kubernetes-guide/"},
    {"id": "site-4", "name": "IndieStackAudit", "url": "https://indiestackaudit.pages.dev/", "sample": "billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026/"},
    {"id": "site-5", "name": "VectorBench", "url": "https://vectorbench-hq.netlify.app/", "sample": "qdrant-vs-pinecone-benchmark-2026/"},
    {"id": "site-6", "name": "NomadTreaty", "url": "https://nomadtreaty.vercel.app/", "sample": "spain-digital-nomad-visa-beckham-law-guide/"},
    {"id": "site-7", "name": "WebhookWatch", "url": "https://webhookwatch.vercel.app/", "sample": "stripe-webhook-signature-verification-fastapi/"},
    {"id": "site-8", "name": "LocalDocPrivacy", "url": "https://localdocprivacy.netlify.app/", "sample": "redact-pdf-locally-browser-wasm-guide/"},
    {"id": "site-9", "name": "FounderRunway", "url": "https://site-9-inky.vercel.app/", "sample": "chiang-mai-vs-bali-runway-calculator/"},
    {"id": "site-10", "name": "RAGInspect", "url": "https://raginspect.pages.dev/", "sample": "late-chunking-vs-sentence-window-retrieval-benchmark/"},
    {"id": "site-11", "name": "NomadPassportIndex", "url": "https://nomadpassportindex.netlify.app/", "sample": "malaysia-de-rantau-digital-nomad-pass-tech-freelancers/"},
    {"id": "site-12", "name": "SaaSUnitMath", "url": "https://site-12-taupe.vercel.app/", "sample": "saas-ltv-cac-payback-period-calculator/"},
    {"id": "site-13", "name": "GrokLogTester", "url": "https://groklogtester.pages.dev/", "sample": "caddy-server-json-access-log-grok-patterns/"},
    {"id": "site-14", "name": "SOC2Ready", "url": "https://site-14-sable.vercel.app/", "sample": "soc-2-type-1-vs-type-2-compliance-timeline-cost/"},
    {"id": "site-15", "name": "EORCalculator", "url": "https://site-15-ruby.vercel.app/", "sample": "deel-vs-remote-com-pricing-hidden-fees-breakdown/"},
    {"id": "site-16", "name": "DevConfigHub", "url": "https://site-16-indol.vercel.app/", "sample": "devcontainer-json-vs-docker-compose-local-development/"},
    {"id": "site-17", "name": "OpenCRMStack", "url": "https://opencrmstack.pages.dev/", "sample": "twenty-crm-self-hosted-docker-deployment-guide/"},
    {"id": "site-18", "name": "CIPipelineGraph", "url": "https://site-18-chi.vercel.app/", "sample": "github-actions-vs-gitlab-ci-syntax-execution-cost-comparison/"},
    {"id": "site-19", "name": "GreekVisualizer", "url": "https://site-19-nine.vercel.app/", "sample": "uniswap-v3-concentrated-liquidity-impermanent-loss-calculator/"},
    {"id": "site-20", "name": "EdgeRuntimeHQ", "url": "https://edgeruntimehq.pages.dev/", "sample": "transformers-js-v3-webgpu-browser-inference-tutorial/"},
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AntigravityForensicSEO/2.2"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            ttfb = round((time.time() - t0) * 1000, 1)
            return resp.status, data, ttfb
    except Exception as e:
        return 0, str(e), 0

def clean_words(html):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL | re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    return len(re.sub(r'\s+', ' ', t).strip().split())

def audit_target(url):
    status, html, ttfb = fetch(url)
    if status != 200:
        return {"status": status, "error": html[:80]}
    
    # Technical
    viewport = 'name="viewport"' in html.lower()
    c_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', html, re.I)
    canonical = c_m.group(1).strip() if c_m else ""
    canonical_self = canonical.rstrip('/') == url.rstrip('/')
    
    # SERP
    t_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = t_m.group(1).strip() if t_m else ""
    d_m = re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]*)"', html, re.I)
    desc = d_m.group(1).strip() if d_m else ""
    has_og = 'property="og:title"' in html and 'property="og:image"' in html
    
    # Semantic
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.DOTALL)
    h2s = re.findall(r'<h2[^>]*>', html, re.I)
    words = clean_words(html)
    
    # Schema
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', html, re.I | re.DOTALL)
    valid_schema = False
    types = []
    if schemas:
        try:
            for s in schemas:
                data = json.loads(s.strip())
                valid_schema = True
                if "@graph" in data:
                    for item in data["@graph"]:
                        types.append(item.get("@type", "Unknown"))
                else:
                    types.append(data.get("@type", "Unknown"))
        except:
            pass
            
    # GEO & Information Gain
    has_qa = "quick answer" in html.lower() or "quick-answer" in html.lower() or "answer-box" in html.lower()
    has_table = "<table" in html.lower()
    has_code = "<pre" in html.lower() or "<code" in html.lower()
    
    return {
        "status": status,
        "ttfb_ms": ttfb,
        "viewport": viewport,
        "canonical": canonical,
        "canonical_ok": canonical_self,
        "title": title,
        "title_len": len(title),
        "desc": desc,
        "desc_len": len(desc),
        "has_og": has_og,
        "h1_count": len(h1s),
        "h2_count": len(h2s),
        "word_count": words,
        "schema_ok": valid_schema,
        "schema_types": list(set(types)),
        "has_qa": has_qa,
        "has_table": has_table,
        "has_code": has_code
    }

print("Executing comprehensive live audit across all 20 production fleet sites...")
fleet_results = []

for s in FLEET:
    home_url = s["url"]
    sample_url = home_url + s["sample"]
    
    home_res = audit_target(home_url)
    sample_res = audit_target(sample_url)
    
    # Check robots, sitemap, llms.txt
    r_status, _, _ = fetch(home_url + "robots.txt")
    s_status, _, _ = fetch(home_url + "sitemap.xml")
    l_status, _, _ = fetch(home_url + "llms.txt")
    
    # Scoring computation
    # 1. Technical (20 pts): HTTP 200 (4), Canonical self (4), Viewport (2), Robots (3), Sitemap (4), LLMS (3)
    tech_score = 0
    if home_res.get("status") == 200 and sample_res.get("status") == 200: tech_score += 4
    if home_res.get("canonical_ok") and sample_res.get("canonical_ok"): tech_score += 4
    elif home_res.get("canonical") and sample_res.get("canonical"): tech_score += 2 # Canonical exists
    if home_res.get("viewport") and sample_res.get("viewport"): tech_score += 2
    if r_status == 200: tech_score += 3
    if s_status == 200: tech_score += 4
    if l_status == 200: tech_score += 3
    
    # 2. SERP Clickability (15 pts): Title length (5), Meta desc (5), OG tags (5)
    serp_score = 0
    if 35 <= sample_res.get("title_len", 0) <= 65: serp_score += 5
    elif sample_res.get("title_len", 0) > 0: serp_score += 3
    if 90 <= sample_res.get("desc_len", 0) <= 175: serp_score += 5
    elif sample_res.get("desc_len", 0) > 0: serp_score += 3
    if sample_res.get("has_og"): serp_score += 5
    
    # 3. Content Quality (25 pts): 1 H1 (5), H2 depth (5), Word count (10), No thin (5)
    content_score = 0
    if sample_res.get("h1_count") == 1: content_score += 5
    if sample_res.get("h2_count", 0) >= 3: content_score += 5
    elif sample_res.get("h2_count", 0) >= 1: content_score += 3
    w = sample_res.get("word_count", 0)
    if w >= 1000: content_score += 10
    elif w >= 600: content_score += 7
    elif w >= 400: content_score += 4
    if w >= 400: content_score += 5
    
    # 4. Structured Data (15 pts): JSON-LD valid (8), recognized types (7)
    schema_score = 0
    if sample_res.get("schema_ok"): schema_score += 8
    if len(sample_res.get("schema_types", [])) > 0: schema_score += 7
    
    # 5. GEO & Information Gain (25 pts): Quick Answer (10), Table/Data (8), Code/Interactive (7)
    geo_score = 0
    if sample_res.get("has_qa"): geo_score += 10
    if sample_res.get("has_table"): geo_score += 8
    if sample_res.get("has_code"): geo_score += 7
    
    total_score = tech_score + serp_score + content_score + schema_score + geo_score
    
    fleet_results.append({
        "id": s["id"],
        "name": s["name"],
        "score": total_score,
        "tech": tech_score,
        "serp": serp_score,
        "content": content_score,
        "schema": schema_score,
        "geo": geo_score,
        "home": home_res,
        "sample": sample_res,
        "robots": r_status,
        "sitemap": s_status,
        "llms": l_status
    })
    
    print(f"[{s['id']}] {s['name']}: Score {total_score}/100 | Words: {sample_res.get('word_count')} | Canon: {sample_res.get('canonical_ok')} | H2s: {sample_res.get('h2_count')} | TTFB: {sample_res.get('ttfb_ms')}ms")

# Summary statistics
scores = [r["score"] for r in fleet_results]
avg_score = round(sum(scores) / len(scores), 1)
print(f"\n==========================================")
print(f"FLEET SEO HEALTH SCORE: {avg_score} / 100")
print(f"MIN SCORE: {min(scores)} | MAX SCORE: {max(scores)}")
print(f"==========================================")

with open("scratch/seo_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(fleet_results, f, indent=2)
print("Saved full audit results to scratch/seo_audit_results.json")
