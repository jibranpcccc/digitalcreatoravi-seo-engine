import urllib.request

imgs = [
  "ollama-vs-vllm-concurrency-benchmarks.webp",
  "vram-requirements-calculator-70b.webp",
  "deepseek-r1-local-setup-ollama.webp",
  "mac-studio-m4-max-llm-benchmarks.webp",
  "custom-mcp-server-python-tutorial.webp"
]

base = "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/images/benchmarks/"
print("Verifying all 5 WebP benchmark diagrams on live edge CDN:\n")

for img in imgs:
    url = base + img
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        size = res.headers.get("Content-Length")
        ctype = res.headers.get("Content-Type")
        print(f"[HTTP {res.status} OK] {img} -> {size} bytes | {ctype}")

print("\n100% OF LIVE IMAGES ARE ONLINE AND SERVING PROPERLY!")
