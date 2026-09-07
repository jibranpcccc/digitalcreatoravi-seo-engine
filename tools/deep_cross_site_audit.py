import sqlite3
from collections import defaultdict
import re

conn = sqlite3.connect("data/fleet_telemetry.db")
c = conn.cursor()

c.execute("SELECT site_id, site_name, target_keyword, title FROM pending_posts")
posts = c.fetchall()

c.execute("SELECT site_id, query, page_url FROM search_queries")
queries = c.fetchall()

c.execute("SELECT site_id, title, url FROM indexed_pages")
pages = c.fetchall()

print(f"Loaded: {len(posts)} posts, {len(queries)} queries, {len(pages)} indexed pages.")

# Build a mapping of (site_id, text, origin)
items = []
for r in posts:
    items.append({"site": r[0], "name": r[1], "text": r[2], "title": r[3], "src": "post"})
for r in queries:
    items.append({"site": r[0], "name": r[0], "text": r[1], "title": r[2], "src": "query"})

stopwords = {"vs", "for", "in", "and", "or", "the", "a", "an", "to", "of", "with", "by", "on", "at", "2026", "guide", "tutorial", "calculator", "formula", "benchmark"}

def clean_tokens(s):
    words = re.findall(r"\b[a-z0-9\.\-]+\b", s.lower())
    return set(w for w in words if w not in stopwords and len(w) > 2)

# Check overlaps
flagged = []
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        it1 = items[i]
        it2 = items[j]
        if it1["site"] == it2["site"]:
            continue
        t1 = clean_tokens(it1["text"])
        t2 = clean_tokens(it2["text"])
        shared = t1.intersection(t2)
        union = t1.union(t2)
        if not union:
            continue
        sim = len(shared) / len(union)
        
        # Flag if 2+ key topic nouns are identical across different sites
        if len(shared) >= 3 or sim >= 0.45:
            flagged.append({
                "sim": round(sim, 3),
                "shared": list(shared),
                "site1": it1["site"],
                "text1": it1["text"],
                "site2": it2["site"],
                "text2": it2["text"],
            })

flagged.sort(key=lambda x: (x["sim"], len(x["shared"])), reverse=True)

print(f"\nPotential Cross-Site Overlaps Found: {len(flagged)}")
seen = set()
for f in flagged:
    pair_key = tuple(sorted([f["site1"] + ":" + f["text1"], f["site2"] + ":" + f["text2"]]))
    if pair_key in seen:
        continue
    seen.add(pair_key)
    print(f"\nSimilarity: {f['sim']*100:.1f}% | Shared Key Nouns: {f['shared']}")
    print(f"  [{f['site1']}] '{f['text1']}'")
    print(f"  [{f['site2']}] '{f['text2']}'")

conn.close()
