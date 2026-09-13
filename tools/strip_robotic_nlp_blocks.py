import os, glob, re

root_dir = os.path.abspath(os.path.join(os.getcwd(), 'sites'))
all_files = [f for f in glob.glob(os.path.join(root_dir, '**', '*.*'), recursive=True) if f.endswith(('.md', '.astro')) and 'node_modules' not in f and 'dist' not in f]

cleaned = 0
for f in all_files:
    try:
        content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    orig = content
    if f.endswith('.md'):
        content = re.sub(r'\n+---\s*\n+##\s+Semantic Architecture & NLP Entity Optimization[\s\S]*?$', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'\n+##\s+Semantic Architecture & NLP Entity Optimization[\s\S]*?$', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'\|\s*\*\*[^\|]+\*\*\s*\|\s*(?:Primary|Secondary|LSI) Entity\s*\|[\s\S]*?$', '\n', content, flags=re.IGNORECASE)
    elif f.endswith('.astro'):
        content = re.sub(r'\s*<!--\s*Surfer SEO NLP Entity Optimization Matrix[\s\S]*?-->\s*<section[\s\S]*?Semantic Architecture & NLP Entity Optimization[\s\S]*?</section>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s*<section[^>]*>[\s\S]*?Semantic Architecture & NLP Entity Optimization[\s\S]*?</section>', '', content, flags=re.IGNORECASE)
    if content != orig:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content.strip() + '\n')
        cleaned += 1
        print('Cleaned:', os.path.relpath(f))

print(f'Done! Successfully cleaned {cleaned} files.')
