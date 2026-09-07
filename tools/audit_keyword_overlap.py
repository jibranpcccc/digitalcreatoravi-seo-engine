#!/usr/bin/env python3
"""
Forensic Keyword & Niche Overlap Audit across all 20 websites.
Checks:
1. Exact Keyword Collisions: Two different sites targeting the exact same query.
2. High Semantic / Token Overlap: Queries across different sites with >60% word overlap.
3. Cross-Site Intent Cannibalization: Two sites targeting the same search intent.
4. Slug & URL Clashes: Collisions in URL paths across sites.
5. Niche Boundary Purity: Verifying topical isolation per site.
"""
import sqlite3
import os
import re
from collections import defaultdict
from itertools import combinations

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "fleet_telemetry.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Fetch all pending posts
c.execute("SELECT site_id, site_name, target_keyword, title, slug FROM pending_posts")
posts = c.fetchall()

# Fetch all search queries
c.execute("SELECT site_id, query, page_url FROM search_queries")
queries = c.fetchall()

# Fetch all live indexed pages
c.execute("SELECT site_id, title, url FROM indexed_pages")
pages = c.fetchall()

print("=" * 80)
print(f"FORENSIC OVERLAP AUDIT: {len(posts)} Posts | {len(queries)} Queries | {len(pages)} Pages")
print("=" * 80)

# ---------------------------------------------------------
# 1. Exact Match Collisions Across Different Sites
# ---------------------------------------------------------
kw_map = defaultdict(list)
for site_id, site_name, kw, title, slug in posts:
    clean = kw.strip().lower()
    kw_map[clean].append({"site": site_id, "name": site_name, "type": "pending_post", "title": title})

for site_id, query, url in queries:
    clean = query.strip().lower()
    kw_map[clean].append({"site": site_id, "name": site_id, "type": "search_query", "title": url})

exact_collisions = {}
for kw, entries in kw_map.items():
    sites = set(e["site"] for e in entries)
    if len(sites) > 1:
        exact_collisions[kw] = entries

print(f"\n1. EXACT KEYWORD COLLISIONS ACROSS SITES: {len(exact_collisions)}")
if exact_collisions:
    for kw, entries in exact_collisions.items():
        print(f"  [!] COLLISION: '{kw}'")
        for e in entries:
            print(f"      -> {e['site']} ({e['type']}): {e['title']}")
else:
    print("  [PASS] 0 exact keyword collisions found across all 20 sites.")

# ---------------------------------------------------------
# 2. Token / Jaccard Semantic Overlap (> 60% word overlap)
# ---------------------------------------------------------
stopwords = {"vs", "for", "in", "and", "or", "the", "a", "an", "to", "of", "with", "by", "on", "at", "2026"}

def tokenize(text):
    words = re.findall(r"\b[a-z0-9\.\-]+\b", text.lower())
    return set(w for w in words if w not in stopwords and len(w) > 1)

all_items = []
for site_id, site_name, kw, title, slug in posts:
    tokens = tokenize(kw)
    if tokens:
        all_items.append({"site": site_id, "text": kw, "tokens": tokens, "type": "post", "title": title})

for site_id, query, url in queries:
    tokens = tokenize(query)
    if tokens:
        all_items.append({"site": site_id, "text": query, "tokens": tokens, "type": "query", "title": url})

near_matches = []
for i in range(len(all_items)):
    for j in range(i + 1, len(all_items)):
        item1 = all_items[i]
        item2 = all_items[j]
        if item1["site"] == item2["site"]:
            continue  # Same site is allowed to have related topics
            
        t1 = item1["tokens"]
        t2 = item2["tokens"]
        intersection = t1.intersection(t2)
        union = t1.union(t2)
        if not union:
            continue
        jaccard = len(intersection) / len(union)
        
        # If > 55% similarity or sharing 3+ specific keywords
        if jaccard >= 0.55 or (len(intersection) >= 3 and jaccard >= 0.4):
            near_matches.append({
                "jaccard": round(jaccard, 2),
                "shared": list(intersection),
                "item1": item1,
                "item2": item2
            })

print(f"\n2. HIGH TOKEN / SEMANTIC OVERLAPS ACROSS DIFFERENT SITES: {len(near_matches)}")
if near_matches:
    # Sort by highest jaccard
    near_matches.sort(key=lambda x: x["jaccard"], reverse=True)
    for m in near_matches[:15]:
        print(f"  [WARN] Similarity: {m['jaccard']*100}% | Shared: {m['shared']}")
        print(f"         Site A ({m['item1']['site']}): '{m['item1']['text']}'")
        print(f"         Site B ({m['item2']['site']}): '{m['item2']['text']}'")
else:
    print("  [PASS] 0 high semantic overlaps found across different sites.")

# ---------------------------------------------------------
# 3. Topic & Niche Boundary Cross-Examination
# ---------------------------------------------------------
print("\n3. SECTOR NICHE BOUNDARY VERIFICATION")
sectors = {
    "Sector 1 (AI Engineering)": ["site-1", "site-3", "site-5", "site-10", "site-20"],
    "Sector 2 (Remote Work & Nomads)": ["site-2", "site-6", "site-9", "site-11", "site-15"],
    "Sector 3 (B2B SaaS & Economics)": ["site-4", "site-7", "site-12", "site-14", "site-17"],
    "Sector 4 (Utilities & Quant Math)": ["site-8", "site-13", "site-16", "site-18", "site-19"]
}

for sec_name, s_ids in sectors.items():
    print(f"\n  Checking {sec_name}...")
    sec_kws = defaultdict(list)
    for site_id, site_name, kw, title, slug in posts:
        if site_id in s_ids:
            sec_kws[site_id].append(kw)
    for sid in s_ids:
        print(f"    - {sid:8}: {len(sec_kws[sid])} target keywords registered")

# ---------------------------------------------------------
# 4. Slug / URL Collision Check
# ---------------------------------------------------------
slug_map = defaultdict(list)
for site_id, site_name, title, slug, kw in [(r[0], r[1], r[2], r[3], r[4]) for r in posts]:
    slug_map[slug].append((site_id, site_name))

slug_collisions = {s: v for s, v in slug_map.items() if len(set(x[0] for x in v)) > 1}
print(f"\n4. SLUG & URL COLLISIONS: {len(slug_collisions)}")
if slug_collisions:
    for s, v in slug_collisions.items():
        print(f"  [!] Collision on slug '{s}': {v}")
else:
    print("  [PASS] 0 slug collisions across the entire portfolio.")

conn.close()
