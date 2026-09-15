#!/usr/bin/env python3
import os

p3 = os.path.join(os.path.dirname(__file__), "..", "sites", "site-3", "src", "pages", "index.astro")
with open(p3, "r", encoding="utf-8") as f:
    c3 = f.read()

schema3 = """
  <script type="application/ld+json" is:inline>
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "ModernDataStack",
    "url": "https://openagentstack.pages.dev/",
    "description": "High-throughput embedded columnar database benchmarks and analytical data engineering guides."
  }
  </script>
"""
if "application/ld+json" not in c3:
    c3 = c3.replace("</Layout>", schema3 + "\n</Layout>")
    with open(p3, "w", encoding="utf-8") as f:
        f.write(c3)
    print("Added schema to site-3 index")

p4 = os.path.join(os.path.dirname(__file__), "..", "sites", "site-4", "src", "pages", "index.astro")
with open(p4, "r", encoding="utf-8") as f:
    c4 = f.read()

schema4 = """
  <script type="application/ld+json" is:inline>
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "IndieStackAudit",
    "url": "https://indiestackaudit.pages.dev/",
    "description": "Solo founder micro-SaaS tech stack teardowns, edge architecture benchmarks, and cost calculators."
  }
  </script>
"""
if "application/ld+json" not in c4:
    c4 = c4.replace("</Layout>", schema4 + "\n</Layout>")
    with open(p4, "w", encoding="utf-8") as f:
        f.write(c4)
    print("Added schema to site-4 index")
