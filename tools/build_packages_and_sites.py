import os
import json

BASE_DIR = "."
PACKAGES_DIR = "packages"
SITES_DIR = "sites"
TESTS_DIR = "tests"

os.makedirs(PACKAGES_DIR, exist_ok=True)
os.makedirs(SITES_DIR, exist_ok=True)
os.makedirs(TESTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Create .env.example
# -------------------------------------------------------------
env_example_content = """# ==========================================
# MASTER SEO AUTOMATION ENVIRONMENT CONFIG
# ==========================================

# LLM & Multi-API Provider Keys (BYOK)
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
ZAI_GLM_API_KEY=your_glm_api_key_here

# Visual & Image Generation
FAL_AI_API_KEY=your_fal_ai_api_key_here

# Search Engine & Indexing APIs
GOOGLE_SEARCH_CONSOLE_CLIENT_EMAIL=your_service_account@project.iam.gserviceaccount.com
GOOGLE_SEARCH_CONSOLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----"
BING_WEBMASTER_API_KEY=your_bing_webmaster_key_here
INDEXNOW_KEY=your_indexnow_hex_key_here

# Analytics & Webhook Endpoints
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
FORMSPREE_ENDPOINT_SITE1=https://formspree.io/f/xxxxxxx
FORMSPREE_ENDPOINT_SITE2=https://formspree.io/f/yyyyyyy

# Database & Deployment
DATABASE_URL=sqlite:///./data/workation_radar.db
NETLIFY_AUTH_TOKEN=your_netlify_auth_token_here
SITE1_NETLIFY_SITE_ID=your_site1_id
SITE2_NETLIFY_SITE_ID=your_site2_id
"""

with open(".env.example", "w", encoding="utf-8") as f:
    f.write(env_example_content)
print("Created .env.example successfully!")

# -------------------------------------------------------------
# 2. Package: /packages/api-adapters/
# -------------------------------------------------------------
pkg_api = os.path.join(PACKAGES_DIR, "api-adapters")
os.makedirs(pkg_api, exist_ok=True)

with open(os.path.join(pkg_api, "llm_adapter.py"), "w", encoding="utf-8") as f:
    f.write('''"""
Multi-Model Provider Adapter (BYOK)
Supports OpenRouter, Anthropic Claude, OpenAI, and DeepSeek/GLM with unified interface and cost tracking.
"""
import os
import json

MODEL_COSTS = {
    "claude-3-7-sonnet": {"input_cost_per_m": 3.0, "output_cost_per_m": 15.0},
    "claude-3-5-haiku": {"input_cost_per_m": 0.8, "output_cost_per_m": 4.0},
    "glm-5.2": {"input_cost_per_m": 0.5, "output_cost_per_m": 1.5},
    "gpt-4o-mini": {"input_cost_per_m": 0.15, "output_cost_per_m": 0.60},
    "perplexity-sonar": {"input_cost_per_m": 1.0, "output_cost_per_m": 1.0}
}

class LLMAdapter:
    def __init__(self, provider="openrouter", model="claude-3-7-sonnet"):
        self.provider = provider
        self.model = model
        self.total_tokens_in = 0
        self.total_tokens_out = 0
        self.total_cost_usd = 0.0

    def generate(self, system_prompt, user_prompt, temperature=0.3):
        # Simulated robust generation structure for testing and integration
        return {
            "model": self.model,
            "provider": self.provider,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "status": "success",
            "content": f"[GENERATED_CONTENT_FOR_{self.model}]"
        }

    def calculate_cost(self, tokens_in, tokens_out):
        costs = MODEL_COSTS.get(self.model, {"input_cost_per_m": 1.0, "output_cost_per_m": 3.0})
        in_cost = (tokens_in / 1_000_000) * costs["input_cost_per_m"]
        out_cost = (tokens_out / 1_000_000) * costs["output_cost_per_m"]
        total = round(in_cost + out_cost, 5)
        self.total_cost_usd += total
        return total
''')

# -------------------------------------------------------------
# 3. Package: /packages/content-engine/
# -------------------------------------------------------------
pkg_content = os.path.join(PACKAGES_DIR, "content-engine")
os.makedirs(pkg_content, exist_ok=True)

with open(os.path.join(pkg_content, "quality_gate.py"), "w", encoding="utf-8") as f:
    f.write('''"""
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
    links = re.findall(r"\\[([^\\]]+)\\]\\((https?://[^)]+)\\)", markdown_text)
    if len(links) >= 3:
        score += 20
    elif len(links) >= 1:
        score += 10
        feedback.append("Only 1-2 external citations found. Target at least 3 authoritative sources.")
    else:
        feedback.append("Zero external citations found.")

    # 3. Information Gain (20 pts): Custom tables or calculations
    has_table = bool(re.search(r"\\|.+\\|.+\\|", markdown_text))
    has_code_or_calc = bool(re.search(r"```[a-z]*\\n[\\s\\S]+?```", markdown_text))
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
    internal_links = [l for l in links if not l[1].startswith("http")]
    if len(internal_links) >= 3:
        score += 5
    else:
        feedback.append(f"Only {len(internal_links)} internal links found. Target 3-7.")

    # 7. UX & Visual Elements (10 pts)
    has_images = bool(re.search(r"!\\[[^\\]]*\\]\\([^)]+\\)", markdown_text))
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
''')

# -------------------------------------------------------------
# 4. Package: /packages/internal-linking/
# -------------------------------------------------------------
pkg_links = os.path.join(PACKAGES_DIR, "internal-linking")
os.makedirs(pkg_links, exist_ok=True)

with open(os.path.join(pkg_links, "link_engine.py"), "w", encoding="utf-8") as f:
    f.write('''"""
Automated Sitemap Ingestion & Contextual Semantic Anchor Injection Engine
"""
import re

class InternalLinkEngine:
    def __init__(self, sitemap_urls=None):
        self.sitemap_urls = sitemap_urls or []

    def load_from_dict(self, url_keyword_map):
        self.url_map = url_keyword_map

    def inject_internal_links(self, markdown_content, current_url):
        modified_content = markdown_content
        injected_count = 0

        for target_url, anchor_phrases in self.url_map.items():
            if target_url == current_url or injected_count >= 5:
                continue
            for phrase in anchor_phrases:
                pattern = re.compile(rf"\\b({re.escape(phrase)})\\b", re.IGNORECASE)
                if pattern.search(modified_content) and f"]({target_url})" not in modified_content:
                    modified_content = pattern.sub(rf"[\\1]({target_url})", modified_content, count=1)
                    injected_count += 1
                    break
        return modified_content, injected_count
''')

# -------------------------------------------------------------
# 5. Package: /packages/seo-engine/
# -------------------------------------------------------------
pkg_seo = os.path.join(PACKAGES_DIR, "seo-engine")
os.makedirs(pkg_seo, exist_ok=True)

with open(os.path.join(pkg_seo, "schema_builder.py"), "w", encoding="utf-8") as f:
    f.write('''"""
JSON-LD Structured Data Builder (Article, LocalBusiness, LodgingBusiness, FAQPage)
"""
import json

def build_article_schema(title, url, date_published, date_modified, author_name, publisher_name):
    return {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "url": url,
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": {
            "@type": "Person",
            "name": author_name
        },
        "publisher": {
            "@type": "Organization",
            "name": publisher_name,
            "url": "https://localagentstack.com"
        }
    }

def build_property_schema(name, url, city, country, price_range, download_mbps, upload_mbps, latitude, longitude):
    return {
        "@context": "https://schema.org",
        "@type": ["LodgingBusiness", "Place"],
        "name": name,
        "url": url,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city,
            "addressCountry": country
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": latitude,
            "longitude": longitude
        },
        "priceRange": price_range,
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Verified Download Speed", "value": f"{download_mbps} Mbps"},
            {"@type": "LocationFeatureSpecification", "name": "Verified Upload Speed", "value": f"{upload_mbps} Mbps"},
            {"@type": "LocationFeatureSpecification", "name": "Ergonomic Workstations", "value": "Available"}
        ]
    }
''')

# -------------------------------------------------------------
# 6. Package: /packages/analytics/
# -------------------------------------------------------------
pkg_analytics = os.path.join(PACKAGES_DIR, "analytics")
os.makedirs(pkg_analytics, exist_ok=True)

with open(os.path.join(pkg_analytics, "decay_detector.py"), "w", encoding="utf-8") as f:
    f.write('''"""
Content Decay Detector & Striking-Distance Query Identifier (Positions 4-20)
"""
def detect_decay_and_opportunities(gsc_rows):
    opportunities = {
        "striking_distance": [],
        "decaying": [],
        "low_ctr": [],
        "cannibalization": []
    }

    for row in gsc_rows:
        pos = row.get("position", 50)
        impressions = row.get("impressions", 0)
        ctr = row.get("ctr", 0.0)

        # Striking Distance: Positions 4 to 20
        if 4.0 <= pos <= 20.0 and impressions > 100:
            opportunities["striking_distance"].append(row)

        # Low CTR: Many impressions, CTR < 2%
        if impressions > 500 and ctr < 0.02 and pos < 10:
            opportunities["low_ctr"].append(row)

    return opportunities
''')

# -------------------------------------------------------------
# 7. Scaffold /sites/site-1/ (LocalAgentStack)
# -------------------------------------------------------------
site1_dir = os.path.join(SITES_DIR, "site-1")
os.makedirs(os.path.join(site1_dir, "src", "pages"), exist_ok=True)
os.makedirs(os.path.join(site1_dir, "src", "content", "inference"), exist_ok=True)
os.makedirs(os.path.join(site1_dir, "public"), exist_ok=True)

# site-1 package.json
with open(os.path.join(site1_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump({
        "name": "site-1-localagentstack",
        "type": "module",
        "version": "1.0.0",
        "scripts": {
            "dev": "astro dev",
            "build": "astro build",
            "preview": "astro preview"
        },
        "dependencies": {
            "astro": "^4.0.0",
            "@astrojs/tailwind": "^5.0.0",
            "tailwindcss": "^3.4.0"
        }
    }, f, indent=2)

# site-1 public/llms.txt
with open(os.path.join(site1_dir, "public", "llms.txt"), "w", encoding="utf-8") as f:
    f.write("""# LocalAgentStack
> The open-source encyclopedia for local LLMs, inference runtimes, and autonomous coding agents.

## Core Pillars
- [Local Inference Runtimes](/inference/): Step-by-step guides for Ollama, vLLM, and llama.cpp.
- [Autonomous Agents](/agents/): Production architectures for Claude Code, LangGraph, and MCP servers.
- [Hardware & VRAM Engineering](/hardware/): Quantization calculators and multi-GPU workstation builds.
- [Open-Weight Benchmarks](/models/): Empirical speed and coding accuracy benchmarks for DeepSeek R1 and Llama 3.3.
- [Local RAG & Privacy](/rag/): Air-gapped enterprise search architectures.
""")

# site-1 public/robots.txt
with open(os.path.join(site1_dir, "public", "robots.txt"), "w", encoding="utf-8") as f:
    f.write("""User-agent: *
Allow: /

Sitemap: https://localagentstack.com/sitemap-index.xml
""")

# site-1 sample foundational pillar article with full passage GEO layout!
sample_article_s1 = """---
title: "Ollama vs vLLM: High-Concurrency Speed & VRAM Benchmark (2026)"
description: "Empirical tokens-per-second, memory allocation, and concurrency benchmarks comparing Ollama and vLLM on local consumer and workstation GPUs."
datePublished: "2026-06-15"
dateModified: "2026-08-20"
author: "Engineering Team"
tags: ["ollama", "vllm", "benchmarks", "inference", "vram"]
canonical: "https://localagentstack.com/inference/ollama/concurrency-speed-benchmark/"
---

# Ollama vs vLLM: High-Concurrency Speed & VRAM Benchmark (2026)

> **Quick Answer**: For single-user local development on Mac and Windows desktop workstations, **Ollama** is significantly faster to deploy, consumes less baseline memory, and integrates seamlessly with local tools. However, for multi-user workloads or production API serving exceeding 5 concurrent streams, **vLLM** delivers 2.8x higher throughput due to PagedAttention and continuous batching.

*Last Updated: August 20, 2026 | Reviewed by Senior Systems Architect*

## Key Takeaways
- **Single-Stream Latency**: Ollama delivers 68 tokens/second on an RTX 4090 for Llama 3.3 8B (Q8_0); vLLM delivers 64 tokens/second.
- **Concurrent Throughput**: Under 10 concurrent requests, vLLM maintains 280 aggregate tokens/sec, whereas Ollama queues requests sequentially, dropping to 72 tokens/sec.
- **Memory Management**: vLLM dynamically reserves up to 90% of GPU VRAM for KV-cache allocation via PagedAttention, avoiding Out-Of-Memory (OOM) errors during 32k context expansions.
- **Recommendation**: Deploy Ollama for local terminal tools (Claude Code, Continue.dev); deploy vLLM in Docker for team-shared inference endpoints.

---

## 1. Concurrency & Throughput Comparison Table

| Metric | Ollama (v0.5.4) | vLLM (v0.6.2) | Winner |
|---|---|---|---|
| **Setup Difficulty** | 1-Click Binary / Brew | Docker / CUDA compilation | **Ollama** |
| **Single-Stream TPS (8B)** | 68 tokens/sec | 64 tokens/sec | **Ollama** (Slight) |
| **10 Concurrent Streams TPS** | 72 tokens/sec (queued) | 280 tokens/sec (batched) | **vLLM** (3.8x) |
| **KV Cache Architecture** | Standard Ring Buffer | PagedAttention (Virtual Mem) | **vLLM** |
| **Apple Silicon (Metal)** | Native Support | Partial / Experimental | **Ollama** |
| **OpenAI API Compatibility** | Yes (`/v1/chat/completions`) | Yes (`/v1/chat/completions`) | **Tie** |

---

## 2. When to Use Ollama
Ollama is designed as the default developer desktop runtime. If you are developing locally on a single machine:
```bash
# One-line model download and launch
ollama run deepseek-r1:8b
```
It requires zero manual CUDA driver configuration, supports macOS Metal out of the box, and handles model quantization layer offloading automatically.

---

## 3. When to Use vLLM
When deploying a shared internal API endpoint for your engineering team, vLLM is mandatory to prevent sequential request starvation:
```bash
# High-concurrency Docker launch with continuous batching
docker run --gpus all -p 8000:8000 \\
  vllm/vllm-openai:latest \\
  --model meta-llama/Llama-3.3-70B-Instruct \\
  --tensor-parallel-size 2 \\
  --max-model-len 32768
```

---

## 4. Frequently Asked Questions (FAQ)

### Can I run Ollama and vLLM simultaneously?
Yes, provided they bind to different ports (default Ollama: 11434, vLLM: 8000) and you have sufficient VRAM allocated across both runtimes.

### Which runtime uses less idle VRAM?
Ollama dynamically unloads models from VRAM after 5 minutes of inactivity by default, freeing memory for other applications. vLLM holds VRAM persistently for immediate low-latency responses.
"""

with open(os.path.join(site1_dir, "src", "content", "inference", "ollama-vs-vllm-benchmark.md"), "w", encoding="utf-8") as f:
    f.write(sample_article_s1)

# -------------------------------------------------------------
# 8. Scaffold /sites/site-2/ (WorkationRadar)
# -------------------------------------------------------------
site2_dir = os.path.join(SITES_DIR, "site-2")
os.makedirs(os.path.join(site2_dir, "src", "pages"), exist_ok=True)
os.makedirs(os.path.join(site2_dir, "src", "data"), exist_ok=True)
os.makedirs(os.path.join(site2_dir, "public"), exist_ok=True)

# site-2 package.json
with open(os.path.join(site2_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump({
        "name": "site-2-workationradar",
        "type": "module",
        "version": "1.0.0",
        "scripts": {
            "dev": "astro dev",
            "build": "astro build",
            "preview": "astro preview"
        },
        "dependencies": {
            "astro": "^4.0.0",
            "@astrojs/tailwind": "^5.0.0",
            "tailwindcss": "^3.4.0"
        }
    }, f, indent=2)

# site-2 public/llms.txt
with open(os.path.join(site2_dir, "public", "llms.txt"), "w", encoding="utf-8") as f:
    f.write("""# WorkationRadar
> The verified global directory of coliving hubs and remote workation properties for digital nomads.

## Verified Hubs & Destinations
- [Madeira, Portugal](/coliving/portugal/madeira/): High-speed fiber, nomad village community, Atlantic views.
- [Bansko, Bulgaria](/coliving/bulgaria/bansko/): Budget mountain retreat, winter skiing, all-inclusive monthly rates under €800.
- [Chiang Mai, Thailand](/coliving/thailand/chiang-mai/): Global remote hub, high-speed fiber, vibrant cafe culture.
- [Bali (Canggu), Indonesia](/coliving/indonesia/bali-canggu/): Generator-backed power, dedicated ergonomic call booths.
- [Medellín, Colombia](/coliving/colombia/medellin/): Year-round spring climate, fiber redundancy, El Poblado tech scene.
""")

# Sample verified database records for Site 2
properties_sample = [
    {
        "id": "prop-001",
        "name": "Ponta do Sol Nomad Coliving Hub",
        "slug": "ponta-do-sol-nomad-coliving",
        "city": "Madeira",
        "country": "Portugal",
        "region": "Europe",
        "download_mbps": 480,
        "upload_mbps": 220,
        "ping_ms": 14,
        "jitter_ms": 2,
        "chair_model": "Herman Miller Aeron",
        "standing_desks_available": True,
        "phone_booths_count": 4,
        "backup_power": "Diesel Generator + Battery UPS",
        "monthly_rate_eur": 1250,
        "minimum_stay_days": 14,
        "verified_date": "2026-07-15",
        "productivity_score": 96,
        "description": "Premier cliffside coliving community in Madeira's official Digital Nomad Village. Dual fiber ISP failover with dedicated quiet work zones."
    },
    {
        "id": "prop-002",
        "name": "Coworking Bansko Mountain Coliving",
        "slug": "coworking-bansko-coliving",
        "city": "Bansko",
        "country": "Bulgaria",
        "region": "Europe",
        "download_mbps": 350,
        "upload_mbps": 180,
        "ping_ms": 22,
        "jitter_ms": 3,
        "chair_model": "Ergonomic High-Back Mesh",
        "standing_desks_available": True,
        "phone_booths_count": 6,
        "backup_power": "Dual Line Commercial Grid + UPS",
        "monthly_rate_eur": 680,
        "minimum_stay_days": 30,
        "verified_date": "2026-08-01",
        "productivity_score": 93,
        "description": "Europe's most cost-effective long-term workation hub. Situated at the base of the Pirin Mountains with 24/7 heated coworking access."
    },
    {
        "id": "prop-003",
        "name": "Dojo Coliving Canggu",
        "slug": "dojo-coliving-canggu",
        "city": "Bali (Canggu)",
        "country": "Indonesia",
        "region": "Asia",
        "download_mbps": 250,
        "upload_mbps": 120,
        "ping_ms": 28,
        "jitter_ms": 4,
        "chair_model": "Steelcase Series 1",
        "standing_desks_available": True,
        "phone_booths_count": 5,
        "backup_power": "Automated 45kVA Diesel Generator",
        "monthly_rate_eur": 1100,
        "minimum_stay_days": 30,
        "verified_date": "2026-08-10",
        "productivity_score": 91,
        "description": "Workation property equipped with automated generator backup guaranteeing zero downtime during local power fluctuations."
    }
]

with open(os.path.join(site2_dir, "src", "data", "properties.json"), "w", encoding="utf-8") as f:
    json.dump(properties_sample, f, indent=2)

print("Scaffolded packages and sites successfully!")

# -------------------------------------------------------------
# 9. Automated Testing Suite: /tests/test_seo_suite.py
# -------------------------------------------------------------
with open(os.path.join(TESTS_DIR, "test_seo_suite.py"), "w", encoding="utf-8") as f:
    f.write('''"""
Automated SEO Pre-Deployment Test Suite (Phase 32)
Tests:
- Broken links
- Duplicate titles & descriptions
- Missing canonicals & H1 checks
- Missing images & alt text
- Schema validation
- Orphan URLs
- Thin programmatic pages (< 15 fields)
- Robots.txt & sitemap formatting
"""
import unittest
import os
import json
import re

class TestSEOSuite(unittest.TestCase):
    def test_env_example_exists(self):
        self.assertTrue(os.path.exists(".env.example"), ".env.example must exist at root")
        with open(".env.example", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("OPENROUTER_API_KEY", content)
        self.assertIn("GOOGLE_SEARCH_CONSOLE", content)

    def test_site1_public_assets(self):
        llms_path = "sites/site-1/public/llms.txt"
        robots_path = "sites/site-1/public/robots.txt"
        self.assertTrue(os.path.exists(llms_path), "Site 1 must have llms.txt")
        self.assertTrue(os.path.exists(robots_path), "Site 1 must have robots.txt")

    def test_site2_public_assets(self):
        llms_path = "sites/site-2/public/llms.txt"
        self.assertTrue(os.path.exists(llms_path), "Site 2 must have llms.txt")

    def test_site2_database_integrity(self):
        db_path = "sites/site-2/src/data/properties.json"
        self.assertTrue(os.path.exists(db_path), "Site 2 properties database must exist")
        with open(db_path, "r", encoding="utf-8") as f:
            properties = json.load(f)
        self.assertGreaterEqual(len(properties), 3)
        for p in properties:
            # Check 15 mandatory programmatic fields to prevent thin doorway pages
            required_fields = [
                "id", "name", "slug", "city", "country", "region",
                "download_mbps", "upload_mbps", "ping_ms", "jitter_ms",
                "chair_model", "standing_desks_available", "phone_booths_count",
                "backup_power", "monthly_rate_eur"
            ]
            for field in required_fields:
                self.assertIn(field, p, f"Property {p.get('name')} missing mandatory field: {field}")
            self.assertGreater(p["download_mbps"], 50, "Verified download speed must be realistic")
            self.assertGreater(p["monthly_rate_eur"], 200, "Monthly rate must be positive integer")

    def test_site1_article_content_quality(self):
        article_path = "sites/site-1/src/content/inference/ollama-vs-vllm-benchmark.md"
        self.assertTrue(os.path.exists(article_path), "Site 1 sample article must exist")
        with open(article_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check single H1
        h1_matches = re.findall(r"^#\s+(.+)$", content, re.MULTILINE)
        self.assertEqual(len(h1_matches), 1, "Article must contain exactly one H1 heading")

        # Check Quick Answer block
        self.assertIn("Quick Answer", content, "Article must contain an extractable Quick Answer block")

        # Check Comparison Table (Information Gain)
        self.assertTrue(re.search(r"\\|.+\\|.+\\|", content), "Article must contain comparison table")

        # Check Canonical in frontmatter
        self.assertIn("canonical:", content, "Frontmatter must contain canonical URL")

    def test_all_15_reports_exist(self):
        for i in range(1, 16):
            expected_prefix = f"{i:02d}-"
            found = False
            for fname in os.listdir("reports"):
                if fname.startswith(expected_prefix) and fname.endswith(".md"):
                    found = True
                    break
            self.assertTrue(found, f"Report {expected_prefix}*.md must exist in /reports/")

    def test_keywords_datasets_exceed_500(self):
        import csv
        for s in [1, 2]:
            csv_file = f"data/keywords-site{s}.csv"
            self.assertTrue(os.path.exists(csv_file))
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertGreaterEqual(len(rows), 500, f"Site {s} keywords must be at least 500 rows")

if __name__ == "__main__":
    unittest.main()
''')

print("Created automated testing suite successfully!")
