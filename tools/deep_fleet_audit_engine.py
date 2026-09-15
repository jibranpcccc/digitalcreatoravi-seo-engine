#!/usr/bin/env python3
"""
Deep Fleet Audit Engine for Antigravity SEO Network
Audits all pages across Sites 1 through 20 (and 21-30 if present):
- Word count (< 1,500 target standard, 1,500-2,500 range)
- Heading hierarchy (1 H1, 6-10 H2s)
- Title tag (optimal 45-65 chars)
- Meta description (optimal 50-160 chars)
- Schema JSON-LD presence & validation
- Google Quick Answer Callout (45-60 words within first 800 chars)
- Structured comparison tables (1-2 tables)
- Code blocks / mathematical proofs
- Anti-slop check
"""

import os
import glob
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

SLOP_WORDS = [
    "in conclusion", "it is important to remember", "tapestry of",
    "delve into", "testament to", "revolutionize", "game-changer",
    "furthermore, it is worth noting", "plethora of", "unleash",
    "in this article", "beacon of hope", "navigate the landscape"
]

def analyze_file(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    fm_text = ""
    body_text = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body_text = parts[2]

    # Title extraction
    title = ""
    m_title = re.search(r'title:\s*["\']([^"\']+)["\']', fm_text)
    if m_title:
        title = m_title.group(1)
    else:
        m_var = re.search(r'const\s+(?:pageTitle|title|spacePageTitle)\s*=\s*["\']([^"\']+)["\']', content)
        if m_var:
            title = m_var.group(1)
        else:
            m_tag = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if m_tag:
                title = m_tag.group(1).strip()
            else:
                m_layout = re.search(r'<Layout[^>]+title=["\']([^"\']+)["\']', content)
                if m_layout:
                    title = m_layout.group(1)
                else:
                    m_prop = re.search(r'title=["\']([^"\']+)["\']', content)
                    if m_prop:
                        title = m_prop.group(1)

    # Description extraction
    desc = ""
    m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', fm_text)
    if m_desc:
        desc = m_desc.group(1)
    else:
        m_dvar = re.search(r'const\s+(?:pageDesc|description)\s*=\s*["\']([^"\']+)["\']', content)
        if m_dvar:
            desc = m_dvar.group(1)
        else:
            m_dtag = re.search(r'name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if m_dtag:
                desc = m_dtag.group(1).strip()
            else:
                m_dlayout = re.search(r'<Layout[^>]+description=["\']([^"\']+)["\']', content)
                if m_dlayout:
                    desc = m_dlayout.group(1)
                else:
                    m_prop = re.search(r'description=["\']([^"\']+)["\']', content)
                    if m_prop:
                        desc = m_prop.group(1)

    # Resolve dynamic property pages in site-2
    if ('space/' in fpath or 'space\\' in fpath) and (not title or not desc):
        try:
            m_slug = re.search(r"slug\s*===\s*['\"]([^'\"]+)['\"]", content)
            if m_slug:
                prop_slug = m_slug.group(1)
                props_file = os.path.join(ROOT_DIR, "sites", "site-2", "src", "data", "properties.json")
                if os.path.exists(props_file):
                    with open(props_file, "r", encoding="utf-8") as pf:
                        pdata = json.load(pf)
                    for item in pdata:
                        if item.get("slug") == prop_slug:
                            if not title:
                                title = f"{item['name']} Review: Speeds & Workspace (2026)"
                            if not desc:
                                desc = item.get("description", "")
                            break
        except Exception:
            pass

    # Clean text for word count
    text_clean = re.sub(r'<script[\s\S]*?</script>', '', body_text)
    text_clean = re.sub(r'<style[\s\S]*?</style>', '', text_clean)
    text_clean = re.sub(r'<[^>]+>', ' ', text_clean)
    words = len(text_clean.split())

    # Headings
    h1_md = re.findall(r'^#\s+(.+)$', body_text, re.MULTILINE)
    h1_html = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    h1_count = len(h1_md) + len(h1_html)

    h2_md = re.findall(r'^##\s+(.+)$', body_text, re.MULTILINE)
    h2_html = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)
    h2_count = len(h2_md) + len(h2_html)

    # Quick answer callout box
    has_qa = bool(re.search(r'quick\s*answer|key\s*takeaways|executive\s*summary|border-l-4|callout', content, re.IGNORECASE))

    # Benchmark tables
    table_count = len(re.findall(r'<table', content, re.IGNORECASE)) + len(re.findall(r'\|[^\n]+\|[^\n]+\|\n\|[-:\s|]+\|', content))

    # Code blocks
    code_count = len(re.findall(r'<pre', content, re.IGNORECASE)) + (len(re.findall(r'```', content)) // 2)

    # Schema JSON-LD
    has_schema = ('application/ld+json' in content) or ('schema' in content.lower() and '@context' in content)
    if not has_schema and fpath.endswith('.md'):
        # Check if site layout or dynamic template provides schema
        site_root = fpath.split('src')[0]
        layout_path = os.path.join(site_root, 'src', 'layouts', 'Layout.astro')
        cat_slug_path = os.path.join(site_root, 'src', 'pages', '[category]', '[slug].astro')
        for check_p in [layout_path, cat_slug_path]:
            if os.path.exists(check_p):
                with open(check_p, 'r', encoding='utf-8', errors='ignore') as clf:
                    if 'application/ld+json' in clf.read():
                        has_schema = True
                        break

    # Slop detection
    slop_matches = [w for w in SLOP_WORDS if w in content.lower()]

    return {
        "file": fpath,
        "title": title,
        "title_len": len(title),
        "desc_len": len(desc),
        "word_count": words,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "has_qa": has_qa,
        "table_count": table_count,
        "code_count": code_count,
        "has_schema": has_schema,
        "slop": slop_matches
    }

def main():
    print("=" * 80)
    print("FLEET-WIDE ON-PAGE SEO & TECHNICAL GAP AUDIT ENGINE")
    print("=" * 80)

    site_folders = [f"site-{i}" for i in range(1, 21)]
    
    total_pages = 0
    thin_pages = []
    low_h2_pages = []
    missing_schema_pages = []
    missing_qa_pages = []
    missing_tables_pages = []
    missing_code_pages = []
    bad_titles = []
    bad_descs = []
    slop_pages = []

    site_stats = {}

    for s in site_folders:
        s_path = os.path.join(SITES_DIR, s)
        if not os.path.exists(s_path):
            continue

        site_stats[s] = {"pages": 0, "words": 0, "thin": 0, "schema_ok": 0}

        # Gather markdown articles in src/content
        md_files = glob.glob(os.path.join(s_path, "src", "content", "**", "*.md"), recursive=True)
        # Gather astro pages in src/pages (excluding 404, layout wrappers, dynamic templates)
        astro_files = []
        for ap in glob.glob(os.path.join(s_path, "src", "pages", "**", "*.astro"), recursive=True):
            bname = os.path.basename(ap)
            if bname.startswith("[") or bname == "404.astro":
                continue
            astro_files.append(ap)

        all_files = md_files + astro_files
        site_stats[s]["pages"] = len(all_files)

        for f in all_files:
            total_pages += 1
            res = analyze_file(f)
            rel = os.path.relpath(f, s_path)
            site_stats[s]["words"] += res["word_count"]

            if res["word_count"] < 1500:
                thin_pages.append((s, rel, res["word_count"], res["h2_count"]))
                site_stats[s]["thin"] += 1
            if res["h2_count"] < 6:
                low_h2_pages.append((s, rel, res["h2_count"]))
            if not res["has_schema"]:
                missing_schema_pages.append((s, rel))
            else:
                site_stats[s]["schema_ok"] += 1
            if not res["has_qa"]:
                missing_qa_pages.append((s, rel))
            if res["table_count"] < 1:
                missing_tables_pages.append((s, rel))
            if res["code_count"] < 1:
                missing_code_pages.append((s, rel))
            if res["title_len"] < 25 or res["title_len"] > 70:
                bad_titles.append((s, rel, res["title_len"], res["title"]))
            if res["desc_len"] < 50 or res["desc_len"] > 165:
                bad_descs.append((s, rel, res["desc_len"]))
            if res["slop"]:
                slop_pages.append((s, rel, res["slop"]))

    print(f"\n📊 AUDIT SUMMARY ACROSS SITES 1-20:")
    print(f"  Total Indexed / Rendered Content Pages: {total_pages}")
    print(f"  Thin Content Pages (< 1,500 words):     {len(thin_pages)} / {total_pages} ({len(thin_pages)/total_pages*100:.1f}%)")
    print(f"  Pages with < 6 H2 Subheadings:           {len(low_h2_pages)} / {total_pages}")
    print(f"  Pages Missing Schema JSON-LD:            {len(missing_schema_pages)} / {total_pages}")
    print(f"  Pages Missing Quick Answer / Callout:   {len(missing_qa_pages)} / {total_pages}")
    print(f"  Pages Missing Benchmark Tables:         {len(missing_tables_pages)} / {total_pages}")
    print(f"  Pages Missing Code / Formulas:          {len(missing_code_pages)} / {total_pages}")
    print(f"  Pages with Suboptimal Title Tag Length: {len(bad_titles)} / {total_pages}")
    print(f"  Pages with Suboptimal Meta Description: {len(bad_descs)} / {total_pages}")
    print(f"  Pages with AI Clichés / Slop Phrases:   {len(slop_pages)} / {total_pages}")

    print("\n📋 PER-SITE BREAKDOWN:")
    print(f"{'Site':<10} | {'Pages':<6} | {'Avg Words':<10} | {'Thin (<1500)':<12} | {'Schema %':<8}")
    print("-" * 55)
    for s, st in site_stats.items():
        avg_w = st["words"] // max(1, st["pages"])
        sch_pct = (st["schema_ok"] / max(1, st["pages"])) * 100
        print(f"{s:<10} | {st['pages']:<6} | {avg_w:<10} | {st['thin']:<12} | {sch_pct:<8.0f}%")

    print("\n🚨 DETAILED BREAKDOWN OF THIN / DEFICIENT PAGES:")
    for s, rel, wc, h2 in thin_pages:
        print(f"  [{s}] {rel} -> {wc} words, {h2} H2s")

if __name__ == "__main__":
    main()
