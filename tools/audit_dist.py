import os
import re

dist_path = "sites/site-1/dist/inference/ollama-vs-vllm-benchmark/index.html"
with open(dist_path, "r", encoding="utf-8") as f:
    html = f.read()

imgs = re.findall(r'<img[^>]+>', html)
print("=== DIST IMAGE TAGS ===")
for img in imgs:
    print(" ", img)

links = re.findall(r'href="(/digitalcreatoravi-seo-engine[^"]*)"', html)
print("\n=== DIST BASE-PREFIXED LINKS ===")
print(f"Total base-prefixed links: {len(links)}")
for l in links:
    print(" ", l)

schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
print(f"\n=== DIST SCHEMA TAGS ===")
print(f"Total schemas: {len(schemas)}")
