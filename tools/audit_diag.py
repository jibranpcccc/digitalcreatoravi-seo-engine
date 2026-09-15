import os, sys, glob, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.deep_fleet_audit_engine import analyze_file, SITES_DIR

fpath = 'sites/site-6/src/pages/estonia-e-residency-tax-optimization.astro'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---', 2)
fm_text = parts[1] if len(parts) >= 3 else ""
m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', fm_text)
print("m_desc:", m_desc.group(1) if m_desc else None)
m_dlayout = re.search(r'<Layout[^>]+description=["\']([^"\']+)["\']', content)
print("m_dlayout:", m_dlayout.group(1) if m_dlayout else None)
m_prop = re.search(r'description=["\']([^"\']+)["\']', content)
print("m_prop:", m_prop.group(1) if m_prop else None)

res = analyze_file(fpath)
print("Result desc_len:", res["desc_len"])

print("\n--- Inspecting all pages with bad titles (<30 or >65) ---")
bad_titles = []
bad_descs = []
for s in [f'site-{i}' for i in range(1, 21)]:
    s_path = os.path.join(SITES_DIR, s)
    all_files = glob.glob(os.path.join(s_path, 'src', 'content', '**', '*.md'), recursive=True) + [
        ap for ap in glob.glob(os.path.join(s_path, 'src', 'pages', '**', '*.astro'), recursive=True)
        if not os.path.basename(ap).startswith('[') and os.path.basename(ap) != '404.astro'
    ]
    for f in all_files:
        r = analyze_file(f)
        rel = os.path.relpath(f, s_path)
        if r['title_len'] < 30 or r['title_len'] > 65:
            bad_titles.append((s, rel, r['title_len'], r['title']))
        if r['desc_len'] < 50 or r['desc_len'] > 160:
            bad_descs.append((s, rel, r['desc_len']))

for s, rel, l, t in bad_titles:
    print(f"[{s}] {rel}: len={l}, title='{t}'")

print(f"\nTotal bad titles: {len(bad_titles)}")
print(f"Total bad descriptions (<50 or >160): {len(bad_descs)}")
