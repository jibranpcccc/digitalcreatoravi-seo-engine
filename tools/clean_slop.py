#!/usr/bin/env python3
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

FILES = [
    os.path.join(SITES_DIR, "site-10", "src", "pages", "hybrid-search-bm25-vs-dense-vector-accuracy.astro"),
    os.path.join(SITES_DIR, "site-11", "src", "pages", "index.astro"),
    os.path.join(SITES_DIR, "site-14", "src", "pages", "vanta-vs-drata-vs-secureframe-compliance-automation-review.astro"),
]

for fpath in FILES:
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        c_new = c.replace("revolutionize", "accelerate").replace("Revolutionize", "Accelerate")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(c_new)
        print(f"Cleaned slop in {fpath}")
