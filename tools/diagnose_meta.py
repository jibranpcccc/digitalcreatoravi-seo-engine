#!/usr/bin/env python3
import os
import glob
from deep_fleet_audit_engine import analyze_file, SITES_DIR

bad_t = []
bad_d = []

for s in [f"site-{i}" for i in range(1, 21)]:
    s_path = os.path.join(SITES_DIR, s)
    md_files = glob.glob(os.path.join(s_path, "src", "content", "**", "*.md"), recursive=True)
    astro_files = [ap for ap in glob.glob(os.path.join(s_path, "src", "pages", "**", "*.astro"), recursive=True)
                   if not os.path.basename(ap).startswith("[") and os.path.basename(ap) != "404.astro"]
    for f in md_files + astro_files:
        r = analyze_file(f)
        rel = os.path.relpath(f, s_path)
        if r["title_len"] < 25 or r["title_len"] > 70:
            bad_t.append((s, rel, r["title_len"], r["title"]))
        if r["desc_len"] < 50 or r["desc_len"] > 165:
            bad_d.append((s, rel, r["desc_len"], f))

print(f"Bad titles count: {len(bad_t)}")
for item in bad_t[:10]:
    print("  Title:", item)

print(f"\nBad descs count: {len(bad_d)}")
for item in bad_d[:10]:
    print("  Desc len:", item[0], item[1], item[2])
