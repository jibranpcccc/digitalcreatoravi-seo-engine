#!/usr/bin/env python3
import os
import glob
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

for s in [f"site-{i}" for i in range(1, 21)]:
    s_path = os.path.join(SITES_DIR, s)
    for f in glob.glob(os.path.join(s_path, "src", "**", "*.*"), recursive=True):
        if not (f.endswith(".md") or f.endswith(".astro")):
            continue
        bname = os.path.basename(f)
        if bname.startswith("[") or bname == "404.astro":
            continue
        with open(f, "r", encoding="utf-8", errors="ignore") as fl:
            c = fl.read()
        has_qa = bool(re.search(r'quick\s*answer|key\s*takeaways|executive\s*summary|border-l-4|callout', c, re.IGNORECASE))
        has_code = len(re.findall(r'<pre', c, re.IGNORECASE)) + (len(re.findall(r'```', c)) // 2) >= 1
        if not has_qa:
            print(f"Missing QA: {s} -> {os.path.relpath(f, s_path)}")
        if not has_code:
            print(f"Missing Code: {s} -> {os.path.relpath(f, s_path)}")
