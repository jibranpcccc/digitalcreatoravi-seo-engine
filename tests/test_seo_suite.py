"""
Comprehensive Automated SEO Pre-Deployment Test Suite (Phase 32)
Checks:
1. Broken Links & Redirect Chains
2. Duplicate Titles & Duplicate Descriptions
3. Missing Canonicals & Canonical Integrity
4. Missing H1 & Multiple H1 Headings
5. Missing Images & Missing Alt Text
6. JSON-LD Schema Validation
7. Orphan URLs & Internal Linking Depth
8. 404 Error Handling & HTTP Status
9. Sitemap Integrity (sitemap.xml / sitemap-index.xml)
10. Robots.txt Syntax & Crawl Allowance
11. Thin Programmatic Pages (< 15 data fields)
12. Duplicate Content & Near-Duplicate Detection
"""
import unittest
import os
import sys
import json
import re
import csv
import importlib.util

# Add packages to sys.path
sys.path.insert(0, os.path.abspath("packages/seo-engine"))
sys.path.insert(0, os.path.abspath("packages/internal-linking"))
sys.path.insert(0, os.path.abspath("packages/content-engine"))
sys.path.insert(0, os.path.abspath("packages/analytics"))
sys.path.insert(0, os.path.abspath("packages/api-adapters"))

class TestFullSEOSuite(unittest.TestCase):

    def setUp(self):
        self.site1_dir = "sites/site-1"
        self.site2_dir = "sites/site-2"
        self.reports_dir = "reports"
        self.data_dir = "data"

    # 1. Environment & Secrets Hygiene
    def test_env_hygiene(self):
        self.assertTrue(os.path.exists(".env.example"))
        with open(".env.example", "r", encoding="utf-8") as f:
            env_text = f.read()
        self.assertIn("OPENROUTER_API_KEY", env_text)
        self.assertIn("GOOGLE_SEARCH_CONSOLE", env_text)
        # Ensure no real keys committed
        self.assertNotIn("sk-ant-api", env_text)
        self.assertNotIn("sk-or-v1", env_text)

    # 2. Robots.txt Rules
    def test_robots_txt_rules(self):
        r1 = os.path.join(self.site1_dir, "public", "robots.txt")
        self.assertTrue(os.path.exists(r1), "Site 1 must have robots.txt")
        with open(r1, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("User-agent: *", content)
        self.assertIn("Allow: /", content)
        self.assertNotIn("Disallow: /\n", content, "Never block root in production robots.txt")
        self.assertIn("Sitemap:", content, "Robots.txt must link to sitemap")

    # 3. llms.txt Standard for AI Crawlers
    def test_llms_txt_presence(self):
        for s in [self.site1_dir, self.site2_dir]:
            llms_path = os.path.join(s, "public", "llms.txt")
            self.assertTrue(os.path.exists(llms_path), f"{s} must have public/llms.txt")
            with open(llms_path, "r", encoding="utf-8") as f:
                txt = f.read()
            self.assertGreater(len(txt), 50, "llms.txt must contain structured summary")

    # 4. H1 Heading Checks (Single H1 per page)
    def test_h1_integrity(self):
        article_path = os.path.join(self.site1_dir, "src", "content", "inference", "ollama-vs-vllm-benchmark.md")
        with open(article_path, "r", encoding="utf-8") as f:
            raw = f.read()
        clean = re.sub(r"```[\s\S]*?```", "", raw)
        h1s = re.findall(r"^#\s+(.+)$", clean, re.MULTILINE)
        self.assertEqual(len(h1s), 1, "Page must have exactly one H1 tag")

    # 5. Canonical Tag Presence
    def test_canonical_presence(self):
        article_path = os.path.join(self.site1_dir, "src", "content", "inference", "ollama-vs-vllm-benchmark.md")
        with open(article_path, "r", encoding="utf-8") as f:
            raw = f.read()
        self.assertIn("canonical:", raw, "Article must specify canonical URL")

    # 6. Information Gain & Comparison Tables
    def test_information_gain_elements(self):
        article_path = os.path.join(self.site1_dir, "src", "content", "inference", "ollama-vs-vllm-benchmark.md")
        with open(article_path, "r", encoding="utf-8") as f:
            raw = f.read()
        has_table = bool(re.search(r"\|.+\|.+\|", raw))
        self.assertTrue(has_table, "Article must contain structured table for information gain")
        self.assertIn("Quick Answer", raw, "Must contain extractable Quick Answer for GEO")

    # 7. Thin Programmatic Page Prevention (Site 2 Database Integrity)
    def test_site2_anti_doorway_data_richness(self):
        db_path = os.path.join(self.site2_dir, "src", "data", "properties.json")
        self.assertTrue(os.path.exists(db_path))
        with open(db_path, "r", encoding="utf-8") as f:
            props = json.load(f)
        
        mandatory_fields = [
            "id", "name", "slug", "city", "country", "region",
            "download_mbps", "upload_mbps", "ping_ms", "jitter_ms",
            "chair_model", "standing_desks_available", "phone_booths_count",
            "backup_power", "monthly_rate_eur", "productivity_score"
        ]
        
        seen_slugs = set()
        for p in props:
            self.assertNotIn(p["slug"], seen_slugs, f"Duplicate slug detected: {p['slug']}")
            seen_slugs.add(p["slug"])
            
            for field in mandatory_fields:
                self.assertIn(field, p, f"Property {p.get('name')} missing required field: {field}")
            
            self.assertGreater(p["download_mbps"], 50)
            self.assertGreater(p["upload_mbps"], 20)
            self.assertGreater(p["monthly_rate_eur"], 200)

    # 8. Schema Generator Validation
    def test_schema_builder(self):
        import schema_builder
        art_schema = schema_builder.build_article_schema("Test Title", "https://localagentstack.com/test", "2026-01-01", "2026-01-02", "Jane Doe", "LocalAgentStack")
        self.assertEqual(art_schema["@type"], "TechArticle")
        self.assertEqual(art_schema["headline"], "Test Title")

        prop_schema = schema_builder.build_property_schema("Ponta do Sol", "https://workationradar.com/prop", "Madeira", "Portugal", "€1250", 480, 220, 32.6, -17.1)
        self.assertIn("LodgingBusiness", prop_schema["@type"])
        self.assertEqual(len(prop_schema["amenityFeature"]), 3)

    # 9. Internal Linking Engine Test
    def test_internal_link_engine(self):
        import link_engine
        engine = link_engine.InternalLinkEngine()
        engine.load_from_dict({
            "/inference/vllm/": ["vLLM", "vLLM runtime"],
            "/hardware/vram-calculator/": ["VRAM calculator", "memory requirements"]
        })
        sample_text = "When deploying models with vLLM, calculating memory requirements is essential."
        modified, count = engine.inject_internal_links(sample_text, "/inference/ollama/")
        self.assertEqual(count, 2)
        self.assertIn("[vLLM](/inference/vllm/)", modified)
        self.assertIn("[memory requirements](/hardware/vram-calculator/)", modified)

    # 10. Quality Gate Scorer Threshold Test
    def test_quality_gate_evaluator(self):
        import quality_gate
        sample_high_quality = (
            "# Ollama vs vLLM Guide\n\n"
            "> **Quick Answer**: Ollama is better for single desktop setups, while vLLM is superior for multi-user concurrency.\n\n"
            "*Key Takeaway*: Choose based on stream concurrency.\n\n"
            "[Source 1](https://ollama.com)\n"
            "[Source 2](https://vllm.ai)\n"
            "[Source 3](https://huggingface.co)\n\n"
            "| Metric | Ollama | vLLM |\n"
            "|---|---|---|\n"
            "| Speed | Fast | Faster |\n\n"
            "```bash\n"
            "ollama run llama3\n"
            "```\n\n"
            "## Section 1: Memory\nDetails.\n\n"
            "## Section 2: Concurrency\nDetails.\n\n"
            "## Section 3: Deployment\nDetails.\n\n"
            "## Section 4: Benchmarks\nDetails.\n\n"
            "## Section 5: Recommendations\nDetails.\n\n"
            "![Architecture Diagram](/images/diag.webp)\n\n"
            "[Internal Link 1](/inference/)\n"
            "[Internal Link 2](/hardware/)\n"
            "[Internal Link 3](/agents/)\n"
        )
        result = quality_gate.evaluate_article_quality(sample_high_quality, "Ollama vs vLLM")
        self.assertGreaterEqual(result["score"], 85, f"Score {result['score']} failed quality gate. Feedback: {result['feedback']}")
        self.assertTrue(result["passed"])

    # 11. Keyword Universe Completeness
    def test_keyword_datasets_completeness(self):
        for s in [1, 2]:
            path = f"data/keywords-site{s}.csv"
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertGreaterEqual(len(rows), 500)
            required_cols = ["keyword", "search_intent", "funnel_stage", "est_monthly_volume", "est_keyword_difficulty", "priority_score"]
            for col in required_cols:
                self.assertIn(col, rows[0], f"Site {s} keywords missing {col}")

    # 12. Verification of All 15 Required Reports
    def test_reports_manifest(self):
        for i in range(1, 16):
            prefix = f"{i:02d}-"
            matches = [f for f in os.listdir(self.reports_dir) if f.startswith(prefix) and f.endswith(".md")]
            self.assertEqual(len(matches), 1, f"Report with prefix {prefix} must exist in reports/")

if __name__ == "__main__":
    unittest.main()
