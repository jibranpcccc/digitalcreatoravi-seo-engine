#!/usr/bin/env python3
import os
import glob
import sys

sys.path.insert(0, os.path.dirname(__file__))
import deep_fleet_audit_engine as engine

def main():
    start_site = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end_site = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    for s_num in range(start_site, end_site + 1):
        s = f"site-{s_num}"
        s_path = os.path.join(engine.SITES_DIR, s)
        md_files = glob.glob(os.path.join(s_path, "src", "content", "**", "*.md"), recursive=True)
        astro_files = [ap for ap in glob.glob(os.path.join(s_path, "src", "pages", "**", "*.astro"), recursive=True) 
                       if not os.path.basename(ap).startswith("[") and os.path.basename(ap) != "404.astro"]
        all_files = md_files + astro_files
        print(f"\n=== {s} ({len(all_files)} pages) ===")
        for f in sorted(all_files):
            res = engine.analyze_file(f)
            rel = os.path.relpath(f, s_path)
            wc = res["word_count"]
            h2 = res["h2_count"]
            tbl = res["table_count"]
            cd = res["code_count"]
            sch = res["has_schema"]
            qa = res["has_qa"]
            print(f"  {rel:<62} | W:{wc:4d} | H2:{h2:2d} | Tbl:{tbl:1d} | Cd:{cd:1d} | QA:{qa} | Sch:{sch}")

if __name__ == "__main__":
    main()
