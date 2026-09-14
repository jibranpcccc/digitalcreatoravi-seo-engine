import re

files = [
    ('Site 13 (GrokLogTester)', r'sites/site-13/src/pages/kubernetes-ingress-nginx-log-parser-fluentbit.astro'),
    ('Site 14 (SOC2Ready)', r'sites/site-14/src/pages/pentest-requirements-for-soc-2-type-2-audit.astro'),
    ('Site 15 (EORCalculator)', r'sites/site-15/src/pages/b2b-contract-vs-eor-permanent-establishment-risk.astro'),
    ('Site 16 (DevConfigHub)', r'sites/site-16/src/pages/devcontainer-feature-pgvector-ollama-local-rag.astro')
]

print("=" * 70)
print("POD D: 4-SITE EXPANSION & OPTIMIZATION AUDIT REPORT")
print("=" * 70)

all_passed = True

for name, path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter and body
    fm_match = re.search(r'^---(.*?)---', content, re.DOTALL)
    fm = fm_match.group(1) if fm_match else ''
    body = content[len(fm_match.group(0)):] if fm_match else content
    
    clean_prose = re.sub(r'<[^>]+>', ' ', body)
    clean_prose = re.sub(r'\{[^\}]+\}', ' ', clean_prose)
    prose_words = len(clean_prose.split())
    total_words = len(content.split())
    
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', content, re.DOTALL)
    h2s = re.findall(r'<h2\b[^>]*>(.*?)</h2>', content, re.DOTALL)
    
    qa_match = re.search(r'Quick Answer:[^<]*</span>\s*</div>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
    qa_text = qa_match.group(1).strip() if qa_match else 'NOT FOUND'
    qa_words = len(qa_text.split())
    
    has_schema = 'schemaJson' in content
    has_table = '<table' in content
    has_code = '<pre' in content
    
    prose_pass = prose_words >= 1500
    h2_pass = len(h2s) >= 6
    h1_pass = len(h1s) == 1
    qa_pass = 45 <= qa_words <= 60
    
    site_pass = prose_pass and h2_pass and h1_pass and qa_pass and has_schema and has_table and has_code
    if not site_pass:
        all_passed = False
        
    print(f"\n[{'PASS' if site_pass else 'FAIL'}] {name}")
    print(f"  File: {path}")
    print(f"  Prose Word Count: {prose_words} (Target: >1500) -> {'PASS' if prose_pass else 'FAIL'}")
    print(f"  Total Word Count: {total_words}")
    print(f"  H1 Count: {len(h1s)} -> {'PASS' if h1_pass else 'FAIL'}")
    if h1s:
        clean_h1 = re.sub(r'<[^>]+>', '', h1s[0]).strip()
        print(f"  H1 Title: {clean_h1}")
    print(f"  H2 Count: {len(h2s)} (Target: >=6) -> {'PASS' if h2_pass else 'FAIL'}")
    for i, h2 in enumerate(h2s, 1):
        clean_h2 = re.sub(r'<[^>]+>', '', h2).strip()
        print(f"    - H2 #{i}: {clean_h2}")
    print(f"  Quick Answer Word Count: {qa_words} words (Target: 45-60) -> {'PASS' if qa_pass else 'FAIL'}")
    print(f"  Quick Answer Preview: {qa_text[:80]}...")
    print(f"  JSON-LD Schema Included: {has_schema}")
    print(f"  Production Tables: {has_table}")
    print(f"  Production Code Blocks: {has_code}")

print("\n" + "=" * 70)
print(f"OVERALL STATUS: {'ALL CRITERIA PASSED 100%' if all_passed else 'SOME CRITERIA FAILED'}")
print("=" * 70)
