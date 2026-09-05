import urllib.request
import re

urls = [
    'https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/robots.txt',
    'https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/sitemap.xml',
    'https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/llms.txt',
    'https://jibranpcccc.github.io/workationradar/robots.txt',
    'https://jibranpcccc.github.io/workationradar/sitemap.xml',
    'https://jibranpcccc.github.io/workationradar/llms.txt'
]

print("=== CHECKING ROBOTS, SITEMAPS & LLMS.TXT ===")
for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            print(f"[HTTP {resp.status}] {u} ({len(content)} bytes)")
    except Exception as e:
        print(f"[FAIL] {u}: {e}")

print("\n=== CHECKING OG:IMAGE & TWITTER:IMAGE META TAGS ===")
page_urls = [
    'https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/',
    'https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/'
]
for p in page_urls:
    req = urllib.request.Request(p, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        tw_img = re.search(r'<meta name="twitter:image" content="([^"]+)"', html)
        print(f"Page: {p}")
        print(f"  og:image:      {og_img.group(1) if og_img else 'MISSING'}")
        print(f"  twitter:image: {tw_img.group(1) if tw_img else 'MISSING'}")
