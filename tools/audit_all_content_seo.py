import os
import re
import glob

keywords = {
    'ollama-vs-vllm-benchmark': 'ollama vs vllm',
    'vram-requirements-calculator-70b': 'vram requirements calculator',
    'deepseek-r1-local-setup-ollama': 'deepseek r1',
    'mac-studio-m4-max-llm-benchmarks': 'mac studio m4 max',
    'custom-mcp-server-python-tutorial': 'custom mcp server',
    '2x-rtx-3090-vs-1x-rtx-4090-ai-inference': '2x rtx 3090 vs 1x rtx 4090',
    'q4_k_m-vs-q8_0-coding-accuracy-test': 'q4_k_m vs q8_0',
    'local-rag-stack-chromadb-ollama': 'local rag stack',
    'claude-code-scheduled-tasks-cron': 'claude code',
    'vllm-multi-gpu-tensor-parallel-docker': 'vllm multi-gpu'
}

slop_phrases = [
    "in conclusion", "it is important to remember", "tapestry of",
    "delve into", "testament to", "revolutionize", "game-changer",
    "furthermore, it is worth noting"
]

print("=" * 80)
print("DEEP CONTENT SEO & YOUTUBE STRATEGY AUDIT (LOCALAGENTSTACK)")
print("=" * 80)

total_articles = 0
passed_articles = 0
all_scores = []

for fpath in glob.glob('sites/site-1/src/content/**/*.md', recursive=True):
    total_articles += 1
    slug = os.path.basename(fpath).replace('.md', '')
    kw = keywords.get(slug, slug)
    text = open(fpath, 'r', encoding='utf-8').read()

    score = 0
    breakdown = []

    # 1. H1 & Keyword Presence (10 pts)
    # Strip code blocks first so bash comments (# ...) are not mistaken for H1
    text_no_code = re.sub(r'```[\s\S]*?```', '', text)
    h1s = re.findall(r"^#\s+(.+)$", text_no_code, re.MULTILINE)
    if len(h1s) == 1 and kw.lower() in h1s[0].lower():
        score += 10
        breakdown.append(("Target Keyword in Single Semantic H1", 10, 10))
    elif len(h1s) == 1:
        score += 7
        breakdown.append(("Single H1 present (partial keyword match)", 7, 10))
    else:
        breakdown.append((f"H1 Error ({len(h1s)} H1s found)", 0, 10))

    # 2. Meta Title & Description in Frontmatter (10 pts)
    title_m = re.search(r'title:\s*"([^"]+)"', text)
    desc_m = re.search(r'description:\s*"([^"]+)"', text)
    if title_m and desc_m and kw.lower() in title_m.group(1).lower() and len(desc_m.group(1)) >= 50:
        score += 10
        breakdown.append(("Meta Title & Description Optimized", 10, 10))
    else:
        score += 5
        breakdown.append(("Meta Title/Description Partial", 5, 10))

    # 3. Quick Answer in opening 150 words (10 pts)
    first_150_words = " ".join(text.split()[:150]).lower()
    if "quick answer" in first_150_words or "quick answer:" in first_150_words:
        score += 10
        breakdown.append(("Direct Featured Snippet Quick Answer Box", 10, 10))
    else:
        breakdown.append(("Missing Quick Answer in opening 150 words", 0, 10))

    # 4. Key Takeaways List (10 pts)
    if "key takeaways" in text.lower():
        score += 10
        breakdown.append(("LLM Citation Key Takeaways Bulleted Box", 10, 10))
    else:
        breakdown.append(("Missing Key Takeaways Box", 0, 10))

    # 5. Authoritative Outbound Links (10 pts)
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    ext_links = [l for l in links if l[1].startswith("http")]
    if len(ext_links) >= 3:
        score += 10
        breakdown.append((f"Authoritative Outbound Citations ({len(ext_links)} links)", 10, 10))
    elif len(ext_links) >= 1:
        score += 6
        breakdown.append((f"Outbound Citations ({len(ext_links)} links)", 6, 10))
    else:
        breakdown.append(("Zero Outbound Citations", 0, 10))

    # 6. Empirical Information Gain: Tables & Code (10 pts)
    has_table = bool(re.search(r"\|.+\|.+\|", text))
    has_code = bool(re.search(r"```[a-z]*\n[\s\S]+?```", text))
    if has_table and has_code:
        score += 10
        breakdown.append(("Empirical Data Table + Executable Code Blocks", 10, 10))
    elif has_table or has_code:
        score += 5
        breakdown.append(("Table or Code present (not both)", 5, 10))
    else:
        breakdown.append(("Missing Tables/Code", 0, 10))

    # 7. Topical Breadth & Fan-Out (10 pts)
    h2s = re.findall(r"^##\s+(.+)$", text, re.MULTILINE)
    if len(h2s) >= 5:
        score += 10
        breakdown.append((f"Topical Fan-Out / PAA Sections ({len(h2s)} H2s)", 10, 10))
    elif len(h2s) >= 3:
        score += 7
        breakdown.append((f"Topical Coverage ({len(h2s)} H2s)", 7, 10))
    else:
        breakdown.append((f"Thin Topical Coverage ({len(h2s)} H2s)", 0, 10))

    # 8. Visual Assets: Cover + WebP Diagram (10 pts)
    has_cover = bool(re.search(r'coverImage:\s*"([^"]+)"', text))
    has_diagram = bool(re.search(r'!\[([^\]]*)\]\(([^)]+\.webp)\)', text))
    if has_cover and has_diagram:
        score += 10
        breakdown.append(("Dual Visual Assets (1200x675 Cover + In-Body WebP Diagram)", 10, 10))
    elif has_cover or has_diagram:
        score += 5
        breakdown.append(("Partial Visual Assets", 5, 10))
    else:
        breakdown.append(("Missing Visual Assets", 0, 10))

    # 9. Internal Silo Links (10 pts)
    int_links = [l for l in links if not l[1].startswith("http") and not l[1].startswith("#")]
    if len(int_links) >= 3:
        score += 10
        breakdown.append((f"Internal Silo Links ({len(int_links)} internal anchors)", 10, 10))
    elif len(int_links) >= 1:
        score += 6
        breakdown.append((f"Partial Internal Links ({len(int_links)} links)", 6, 10))
    else:
        breakdown.append(("Zero Internal Links", 0, 10))

    # 10. Anti-AI Slop & Clean Writing (10 pts)
    found_slop = [p for p in slop_phrases if p in text.lower()]
    if not found_slop:
        score += 10
        breakdown.append(("Anti-AI Slop: 100% Clean Technical Phrasing", 10, 10))
    else:
        penalty = min(10, len(found_slop) * 3)
        score += (10 - penalty)
        breakdown.append((f"AI Clichés detected: {', '.join(found_slop)}", 10 - penalty, 10))

    all_scores.append(score)
    if score >= 85:
        passed_articles += 1

    status = "EXCELLENT (100/100)" if score == 100 else ("PASS" if score >= 85 else "FAIL")
    print(f"\nARTICLE: {slug}")
    print(f"Target Keyword: '{kw}'")
    print(f"Total SEO Score: {score} / 100  [{status}]")
    print("-" * 60)
    for desc, pts, max_pts in breakdown:
        chk = "✓" if pts == max_pts else ("~" if pts > 0 else "✗")
        print(f"  [{chk}] {desc:<50} {pts:>2}/{max_pts} pts")

print("\n" + "=" * 80)
avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
print(f"AUDIT SUMMARY: {passed_articles}/{total_articles} Articles Passed Quality Gate (Score >= 85)")
print(f"AVERAGE SEO HEALTH SCORE: {avg_score:.1f} / 100")
print("=" * 80)
