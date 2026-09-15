import os
import glob
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

# Load properties for site-2
props_map = {}
pfile = os.path.join(SITES_DIR, "site-2", "src", "data", "properties.json")
if os.path.exists(pfile):
    with open(pfile, "r", encoding="utf-8") as f:
        props = json.load(f)
        for p in props:
            props_map[p["slug"]] = p

def extract_meta(fpath):
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
    m = re.search(r'^\s*title:\s*["\']([^"\']+)["\']', fm_text, re.MULTILINE)
    if m:
        title = m.group(1)
    if not title:
        m = re.search(r'const\s+(?:pageTitle|title|spacePageTitle)\s*=\s*["\']([^"\']+)["\']', content)
        if m:
            title = m.group(1)
    if not title:
        m = re.search(r'<Layout[^>]*\btitle="([^"]+)"', content)
        if m:
            title = m.group(1)
    if not title:
        m = re.search(r'<Layout[^>]*\btitle=\'([^\']+)\'', content)
        if m:
            title = m.group(1)
    if not title:
        # Check spacePageTitle or prop in site-2
        m_slug = re.search(r"slug === ['\"]([^'\"]+)['\"]", content)
        if m_slug and m_slug.group(1) in props_map:
            p = props_map[m_slug.group(1)]
            baseSpaceTitle = f"{p['name']} Review: Speeds & Workspace (2026)"
            title = f"{p['name']}: Speed & Ergonomics Guide 2026" if len(baseSpaceTitle) > 60 else baseSpaceTitle
        elif "spacePageTitle" in content and "slug" in content:
            bname = os.path.splitext(os.path.basename(fpath))[0]
            if bname in props_map:
                p = props_map[bname]
                baseSpaceTitle = f"{p['name']} Review: Speeds & Workspace (2026)"
                title = f"{p['name']}: Speed & Ergonomics Guide 2026" if len(baseSpaceTitle) > 60 else baseSpaceTitle

    if not title:
        m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if m:
            title = m.group(1).strip()

    # Description extraction
    desc = ""
    m = re.search(r'^\s*description:\s*["\']([^"\']+)["\']', fm_text, re.MULTILINE)
    if m:
        desc = m.group(1)
    if not desc:
        m = re.search(r'const\s+(?:pageDesc|description|pageDescription|desc)\s*=\s*["\']([^"\']+)["\']', content)
        if m:
            desc = m.group(1)
    if not desc:
        m = re.search(r'<Layout[^>]*\bdescription="([^"]+)"', content)
        if m:
            desc = m.group(1)
    if not desc:
        m = re.search(r'<Layout[^>]*\bdescription=\'([^\']+)\'', content)
        if m:
            desc = m.group(1)
    if not desc:
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if m:
            desc = m.group(1)
    if not desc:
        bname = os.path.splitext(os.path.basename(fpath))[0]
        if bname in props_map:
            p = props_map[bname]
            desc = f"Independent verification of {p['name']} in {p['city']}, {p['country']}. Tested {p['download_mbps']} Mbps fiber speed, {p['chair_model']} chairs, and power backup status."
        elif "prop.slug" in content:
            m_slug = re.search(r"slug === ['\"]([^'\"]+)['\"]", content)
            if m_slug and m_slug.group(1) in props_map:
                p = props_map[m_slug.group(1)]
                desc = f"Independent verification of {p['name']} in {p['city']}, {p['country']}. Tested {p['download_mbps']} Mbps fiber speed, {p['chair_model']} chairs, and power backup status."

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
        site_root = fpath.split('src')[0]
        layout_path = os.path.join(site_root, 'src', 'layouts', 'Layout.astro')
        cat_slug_path = os.path.join(site_root, 'src', 'pages', '[category]', '[slug].astro')
        for check_p in [layout_path, cat_slug_path]:
            if os.path.exists(check_p):
                with open(check_p, 'r', encoding='utf-8', errors='ignore') as clf:
                    if 'application/ld+json' in clf.read():
                        has_schema = True
                        break

    return {
        "file": fpath,
        "title": title,
        "title_len": len(title),
        "desc": desc,
        "desc_len": len(desc),
        "word_count": words,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "has_qa": has_qa,
        "table_count": table_count,
        "code_count": code_count,
        "has_schema": has_schema,
    }

def run():
    pages = []
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
            pages.append(meta)

    print(f"Total analyzed pages: {len(pages)}")

    # Check title issues: ideal length is 30-65 chars
    bad_titles = [p for p in pages if p["title_len"] < 30 or p["title_len"] > 65]
    print(f"\nTitles outside 30-65 chars: {len(bad_titles)}")
    for p in bad_titles:
        print(f"  [{p['site']}] {p['rel']} (len {p['title_len']}): '{p['title']}'")

    short_descs = [p for p in pages if p["desc_len"] < 50]
    long_descs = [p for p in pages if p["desc_len"] > 160]
    print(f"\nShort descriptions (<50 chars): {len(short_descs)}")
    for p in short_descs:
        print(f"  [{p['site']}] {p['rel']} (len {p['desc_len']}): '{p['desc']}'")
    print(f"\nLong descriptions (>160 chars): {len(long_descs)}")

    # Check thin pages (<1500)
    thin = [p for p in pages if p["word_count"] < 1500]
    print(f"\nThin pages (<1500 words): {len(thin)}")
    for p in thin:
        print(f"  [{p['site']}] {p['rel']}: {p['word_count']} words")

    # Check low H2 (<6)
    low_h2 = [p for p in pages if p["h2_count"] < 6]
    print(f"\nLow H2 (<6): {len(low_h2)}")
    for p in low_h2:
        print(f"  [{p['site']}] {p['rel']}: {p['h2_count']} H2s")

    # Check missing schema
    no_schema = [p for p in pages if not p["has_schema"]]
    print(f"\nMissing schema: {len(no_schema)}")

    # Check missing QA
    no_qa = [p for p in pages if not p["has_qa"]]
    print(f"\nMissing QA: {len(no_qa)}")

    # Check missing tables
    no_tables = [p for p in pages if p["table_count"] < 1]
    print(f"\nMissing tables: {len(no_tables)}")

    # Check missing code
    no_code = [p for p in pages if p["code_count"] < 1]
    print(f"\nMissing code: {len(no_code)}")

if __name__ == "__main__":
    run()
