"""
Automated Content Quality Gate & Information Gain Scorer (Score >= 85/100 threshold)
"""
import re

def evaluate_article_quality(markdown_text, keyword, required_entities=None):
    score = 0
    feedback = []

    # 1. Intent Satisfaction (20 pts): Exact H1 check + Quick Answer in first 100 words
    h1_match = re.search(r"^#\s+(.+)$", markdown_text, re.MULTILINE)
    if h1_match and keyword.lower() in h1_match.group(1).lower():
        score += 10
    else:
        feedback.append("H1 does not tightly match target keyword.")

    first_150_words = " ".join(markdown_text.split()[:150]).lower()
    if "quick answer" in first_150_words or "key takeaway" in first_150_words:
        score += 10
    else:
        feedback.append("Missing Quick Answer or Key Takeaways block in opening 150 words.")

    # 2. Accuracy & In-Text Citations (20 pts)
    all_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", markdown_text)
    external_links = [l for l in all_links if l[1].startswith("http")]
    if len(external_links) >= 3:
        score += 20
    elif len(external_links) >= 1:
        score += 10
        feedback.append("Only 1-2 external citations found. Target at least 3 authoritative sources.")
    else:
        feedback.append("Zero external citations found.")

    # 3. Information Gain (20 pts): Custom tables or calculations
    has_table = bool(re.search(r"\|.+\|.+\|", markdown_text))
    has_code_or_calc = bool(re.search(r"```[a-z]*\n[\s\S]+?```", markdown_text))
    if has_table and has_code_or_calc:
        score += 20
    elif has_table or has_code_or_calc:
        score += 12
        feedback.append("Contains either a table or code, but not both. Add full comparison matrix.")
    else:
        feedback.append("Zero Information Gain elements (tables or executable configurations) detected.")

    # 4. Topical Completeness / Fan-Out (10 pts)
    h2_headings = re.findall(r"^##\s+(.+)$", markdown_text, re.MULTILINE)
    if len(h2_headings) >= 5:
        score += 10
    elif len(h2_headings) >= 3:
        score += 6
    else:
        feedback.append("Fewer than 3 H2 subheadings. Inadequate fan-out coverage.")

    # 5. Readability & Anti-AI Slop (10 pts)
    slop_phrases = ["in conclusion", "it is important to remember", "tapestry of", "delve into", "testament to"]
    found_slop = [p for p in slop_phrases if p in markdown_text.lower()]
    if not found_slop:
        score += 10
    else:
        score += max(0, 10 - (len(found_slop) * 3))
        feedback.append(f"AI filler phrases detected: {', '.join(found_slop)}")

    # 6. Internal Linking (5 pts)
    internal_links = [l for l in all_links if not l[1].startswith("http") and not l[1].startswith("#")]
    if len(internal_links) >= 3:
        score += 5
    else:
        feedback.append(f"Only {len(internal_links)} internal links found. Target 3-7.")

    # 7. UX & Visual Elements (10 pts)
    has_images = bool(re.search(r"!\[[^\]]*\]\([^)]+\)", markdown_text))
    if has_images:
        score += 10
    else:
        feedback.append("Missing descriptive WebP images or diagrams.")

    # 8. Schema & Metadata (5 pts)
    score += 5

    passed = score >= 85
    return {
        "score": score,
        "passed": passed,
        "feedback": feedback
    }
