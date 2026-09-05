import urllib.request

covers = [
    "ollama-vs-vllm-benchmark.webp",
    "vram-requirements-calculator-70b.webp",
    "deepseek-r1-local-setup-ollama.webp",
    "mac-studio-m4-max-llm-benchmarks.webp",
    "custom-mcp-server-python-tutorial.webp"
]

benchmarks = [
    "ollama-vs-vllm-concurrency-benchmarks.webp",
    "vram-requirements-calculator-70b.webp",
    "deepseek-r1-local-setup-ollama.webp",
    "mac-studio-m4-max-llm-benchmarks.webp",
    "custom-mcp-server-python-tutorial.webp"
]

base = "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/images/"

print("=" * 70)
print("AUDITING ALL 10 PRODUCTION ASSETS ON GITHUB PAGES EDGE CDN")
print("=" * 70)

print("\n1. FEATURED HERO COVERS (1200x675):")
for img in covers:
    url = base + "covers/" + img
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        size = res.headers.get("Content-Length")
        ctype = res.headers.get("Content-Type")
        print(f"  [HTTP {res.status} OK] {img:<45} {size:>6} bytes | {ctype}")

print("\n2. IN-ARTICLE TECHNICAL BENCHMARK DIAGRAMS (1200x675):")
for img in benchmarks:
    url = base + "benchmarks/" + img
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        size = res.headers.get("Content-Length")
        ctype = res.headers.get("Content-Type")
        print(f"  [HTTP {res.status} OK] {img:<45} {size:>6} bytes | {ctype}")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE: 10/10 PRODUCTION IMAGES SERVING 200 OK")
print("=" * 70)
