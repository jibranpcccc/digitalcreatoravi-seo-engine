import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
import glob
import re
import json

SITES_DIR = os.path.join(ROOT_DIR, "sites")

from tools.precise_audit import extract_meta

def get_long_descriptions():
    results = []
    for s in [f"site-{i}" for i in range(1, 21)]:
        s_path = os.path.join(SITES_DIR, s)
        md_files = glob.glob(os.path.join(s_path, "src", "content", "**", "*.md"), recursive=True)
        astro_files = [
            ap for ap in glob.glob(os.path.join(s_path, "src", "pages", "**", "*.astro"), recursive=True)
            if not os.path.basename(ap).startswith("[") and os.path.basename(ap) != "404.astro"
        ]
        for f in md_files + astro_files:
            meta = extract_meta(f)
            meta["site"] = s
            meta["rel"] = os.path.relpath(f, s_path)
            if meta["desc_len"] > 160:
                results.append(meta)
    return results

def dump_descriptions():
    long_items = get_long_descriptions()
    print(f"Found {len(long_items)} descriptions over 160 chars.")
    out_file = os.path.join(ROOT_DIR, "data", "long_descriptions.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump([{
            "file": item["file"],
            "site": item["site"],
            "rel": item["rel"],
            "len": item["desc_len"],
            "desc": item["desc"]
        } for item in long_items], f, indent=2)
    print(f"Saved to {out_file}")

if __name__ == "__main__":
    dump_descriptions()
