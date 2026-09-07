import os
import re

sites = ['site-9', 'site-10', 'site-11', 'site-12', 'site-13']
root = r"C:\Users\jibra\Desktop\1\digitalcreatoravi"

print("=" * 80)
print("🔍 WAVE 1 STATIC HTML SEO AUDIT (SITES 9 TO 13)")
print("=" * 80)

total_checked = 0
passed_checked = 0

for s in sites:
    dist_dir = os.path.join(root, "sites", s, "dist")
    print(f"\n[+] Auditing {s} ({dist_dir})...")
    
    # Check robots and sitemap
    has_robots = os.path.exists(os.path.join(dist_dir, "robots.txt"))
    has_sitemap = os.path.exists(os.path.join(dist_dir, "sitemap.xml"))
    has_key = os.path.exists(os.path.join(dist_dir, "8303260f1bf94264ac6d00aa93efde28.txt"))
    print(f"    - Discovery Assets: robots.txt={has_robots}, sitemap.xml={has_sitemap}, IndexNowKey={has_key}")
    
    for r, dirs, fnames in os.walk(dist_dir):
        for f in fnames:
            if f.endswith(".html"):
                total_checked += 1
                fpath = os.path.join(r, f)
                rel = os.path.relpath(fpath, dist_dir)
                
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                    html = fp.read()
                    
                h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
                h1_ok = len(h1s) == 1
                has_qa = "quick answer" in html.lower()
                has_schema = '<script type="application/ld+json">' in html
                has_canon = '<link rel="canonical"' in html
                has_beacon = 'webhookwatch.vercel.app/api/track' in html or 'sendBeacon' in html or 'api/track' in html
                
                status = "PASS 100/100" if (h1_ok and has_qa and has_schema and has_canon) else "FAIL"
                if status == "PASS 100/100":
                    passed_checked += 1
                    
                print(f"    ✔ {rel:50} | H1={len(h1s)} | QA={has_qa} | Schema={has_schema} | Canon={has_canon} | Status={status}")

print("\n" + "=" * 80)
print(f"AUDIT SUMMARY: {passed_checked} / {total_checked} Pages Passed 100/100 SEO Health Checks")
print("=" * 80)
