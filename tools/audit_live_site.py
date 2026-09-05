import urllib.request
import re

url = "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")

imgs = re.findall(r'<img[^>]+>', html)
print("=== LIVE IMAGE AUDIT ===")
for img in imgs:
    print("IMAGE TAG:", img)

schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
print("\n=== LIVE SCHEMA AUDIT ===")
print(f"Schema blocks found: {len(schemas)}")
for s in schemas:
    print(s[:200] + "...")

quotes = re.findall(r'<blockquote>([\s\S]*?)</blockquote>', html)
print(f"\n=== LIVE QUICK ANSWER AUDIT ===")
print(f"Quick Answer blocks: {len(quotes)}")
if quotes:
    print(quotes[0][:150].strip() + "...")

tables = re.findall(r'<table[^>]*>([\s\S]*?)</table>', html)
print(f"\n=== LIVE TABLE AUDIT ===")
print(f"HTML comparison tables: {len(tables)}")

h2s = re.findall(r'<h2[^>]*>([\s\S]*?)</h2>', html)
print(f"\n=== LIVE H2 HEADINGS AUDIT ===")
print(f"H2 count: {len(h2s)}")
for h in h2s:
    print(" - ", h.strip())

ext_links = re.findall(r'href="(https?://[^"]+)"', html)
print(f"\n=== LIVE EXTERNAL CITATIONS ===")
print(f"Citations count: {len(ext_links)}")
for l in ext_links[:5]:
    print(" - ", l)
