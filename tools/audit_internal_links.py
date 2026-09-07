import os
import glob
import re

sites_dir = 'sites'
results = []

for site in sorted(os.listdir(sites_dir)):
    site_path = os.path.join(sites_dir, site)
    if not os.path.isdir(site_path):
        continue
    files = glob.glob(os.path.join(site_path, 'src', '**', '*.astro'), recursive=True)
    links = []
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # match href="/...", href='...', href={`${base}/...`}
            found1 = re.findall(r'href=[\'"](/[a-zA-Z0-9_\-#/]+)[\'"]', content)
            found2 = re.findall(r'href=\{`\$\{base\}(/[a-zA-Z0-9_\-#/]*)`\}', content)
            all_found = found1 + found2
            for link in all_found:
                if link != '/' and not link.startswith('//'):
                    links.append((os.path.basename(fpath), link))
    results.append((site, len(files), len(links), len(set(l[1] for l in links))))

print(f"{'Site':<10} | {'Files':<6} | {'Total Links':<12} | {'Unique Internal Links':<20}")
print("-" * 55)
for s, f_cnt, l_cnt, u_cnt in results:
    print(f"{s:<10} | {f_cnt:<6} | {l_cnt:<12} | {u_cnt:<20}")
