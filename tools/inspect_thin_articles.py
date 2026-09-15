#!/usr/bin/env python3
import os
import glob
import sys

sys.path.insert(0, os.path.dirname(__file__))
import deep_fleet_audit_engine as engine

def main():
    thin_articles = []
    for s_num in range(5, 21):
        s = f"site-{s_num}"
        s_path = os.path.join(engine.SITES_DIR, s)
        pages = [p for p in glob.glob(os.path.join(s_path, "src", "pages", "*.astro"))
                 if not os.path.basename(p).startswith("[") and os.path.basename(p) != "404.astro" and os.path.basename(p) != "index.astro"]
        for p in pages:
            res = engine.analyze_file(p)
            if res["word_count"] < 1500:
                thin_articles.append({
                    "site": s,
                    "file": p,
                    "slug": os.path.basename(p).replace(".astro", ""),
                    "title": res["title"],
                    "words": res["word_count"],
                    "h2_count": res["h2_count"],
                    "table_count": res["table_count"],
                    "code_count": res["code_count"]
                })

    print(f"Total thin articles on Sites 5-20: {len(thin_articles)}")
    for a in thin_articles:
        print(f"[{a['site']}] {a['slug']:<50} | Words: {a['words']:4d} | H2s: {a['h2_count']}")

if __name__ == "__main__":
    main()
