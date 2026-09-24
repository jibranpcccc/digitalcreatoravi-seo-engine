from precise_audit import extract_meta, SITES_DIR
import glob

pages = glob.glob(f"{SITES_DIR}/site-*/src/pages/**/*.astro", recursive=True) + glob.glob(f"{SITES_DIR}/site-*/src/content/**/*.md", recursive=True)
for p in pages:
    if "index.astro" in p or "[slug]" in p or "[category]" in p:
        continue
    meta = extract_meta(p)
    if meta["code_count"] < 1:
        print("Missing code:", p)
    if meta["word_count"] < 1500:
        print(f"Thin ({meta['word_count']} words):", p)
