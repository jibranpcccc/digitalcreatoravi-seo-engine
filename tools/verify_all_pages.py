import glob
import os
import re

files = glob.glob("sites/site-1/dist/**/*.html", recursive=True)
print(f"Auditing {len(files)} compiled static pages in dist/:\n")

all_passed = True
for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        html = fp.read()
    rel = os.path.relpath(f, "sites/site-1/dist")
    
    imgs = re.findall(r'<img[^>]+>', html)
    schemas = re.findall(r'<script type="application/ld\+json">', html)
    h1s = re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', html)
    quotes = re.findall(r'<blockquote>', html)
    tables = re.findall(r'<table', html)
    
    # Validation rules
    is_article = rel != "index.html"
    status = "OK"
    if is_article:
        if len(imgs) < 2:
            status = "WARN: Under 2 images"
            all_passed = False
        if len(schemas) < 1:
            status = "FAIL: Missing Schema"
            all_passed = False
        if len(h1s) != 1:
            status = f"FAIL: Expected 1 H1, found {len(h1s)}"
            all_passed = False
        if len(quotes) < 1:
            status = "FAIL: Missing Quick Answer block"
            all_passed = False
        if len(tables) < 1:
            status = "FAIL: Missing Comparison Table"
            all_passed = False

    print(f"[{status}] {rel}")
    print(f"   -> Images: {len(imgs)} | Schema: {len(schemas)} | H1: {len(h1s)} | Quick Answer: {len(quotes)} | Tables: {len(tables)}")

print(f"\nOverall Audit Result: {'ALL CHECKS PASSED (1000% READY)' if all_passed else 'SOME CHECKS FAILED'}")
