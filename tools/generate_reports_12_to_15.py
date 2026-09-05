import os

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# 12-site-architecture.md
r12_content = """# Full Technical Website Architecture Specification

**Scope**: Architectural design for Site 1 (`LocalAgentStack`) and Site 2 (`WorkationRadar`).

---

## 1. Core Framework Selection: Astro + Tailwind CSS
We select **Astro** as the primary web application framework for both websites for the following verified reasons:
1. **Zero-JS by Default**: Astro renders pure static HTML at build time. Unlike Next.js which ships hydration bundles for static pages, Astro ships zero client-side JavaScript unless explicitly opted-in via client islands.
2. **Sub-Second Performance**: Delivers consistent 95–100 PageSpeed Insights performance scores, meeting Core Web Vitals (LCP < 0.8s, CLS = 0.00, INP < 50ms).
3. **Markdown & MDX Native**: Site 1's editorial content lives in version-controlled markdown/MDX with typed frontmatter schemas via Astro Content Collections.
4. **Hybrid Database Capabilities**: Site 2 leverages Astro's hybrid rendering and server endpoints to query local SQLite/PostgreSQL for programmatic database filtering and search.
5. **Edge Deployment**: Compiles to static assets effortlessly deployed to Netlify or Cloudflare Pages with global CDN caching.

---

## 2. Technical Feature Implementation Matrix

| Technical Requirement | Site 1: LocalAgentStack | Site 2: WorkationRadar |
|---|---|---|
| **Rendering Strategy** | Pure Static Site Generation (SSG) | Hybrid SSG + Edge Endpoints |
| **Data Layer** | Astro Content Collections (Markdown/MDX) | SQLite / Postgres + JSON database |
| **URL Canonicalization** | Strict self-referential canonical tags | Canonical tags with query-param normalization |
| **Sitemap Architecture** | Single `sitemap-index.xml` + `sitemap.xml` | Segmented sitemaps: `/sitemaps/cities.xml`, `/sitemaps/properties.xml` |
| **Robots.txt** | Permits Googlebot, Bingbot, GPTBot, ClaudeBot | Permits all major crawlers; rate limits heavy aggregators |
| **AI Crawler Index** | `/llms.txt` listing core tech pillars | `/llms.txt` listing top 30 global workation hubs |
| **Machine Entity Data**| `/ai.json` declaring site authorship | `/ai.json` declaring database licensing and API endpoints |
| **Structured Data** | `TechArticle`, `BreadcrumbList`, `FAQPage` | `LodgingBusiness`, `Place`, `ItemList`, `FAQPage` |
| **Image Optimization** | Automated WebP conversion via Astro Image | High-res WebP with verified Speedtest overlays |
| **Lead / Contact Form** | Formspree / Web3Forms webhook | Direct booking referral outbound links + inquiry form |
| **Search / Filtering** | Client-side Pagefind static search | Interactive client-side facet filter (speed, price, chairs) |

---

## 3. URL Structure & Taxonomy

### Site 1 (LocalAgentStack):
- Homepage: `/`
- Pillar Hub: `/[category]/` (e.g. `/inference/`, `/agents/`, `/hardware/`)
- Cluster Hub: `/[category]/[cluster]/` (e.g. `/inference/ollama/`, `/hardware/vram/`)
- Content Article: `/[category]/[cluster]/[article-slug]` (e.g. `/inference/ollama/concurrency-speed-benchmark`)
- Interactive Tools: `/tools/[tool-slug]` (e.g. `/tools/vram-calculator`)
- System Pages: `/about/`, `/editorial-standards/`, `/llms.txt`, `/robots.txt`, `/sitemap.xml`

### Site 2 (WorkationRadar):
- Homepage: `/`
- Regional Pillar: `/destinations/[region]/` (e.g. `/destinations/europe/`)
- Country Hub: `/destinations/[country]/` (e.g. `/destinations/portugal/`)
- City Hub Pillar: `/coliving/[country]/[city]/` (e.g. `/coliving/portugal/madeira/`)
- Individual Property: `/property/[city]/[property-slug]/` (e.g. `/property/madeira/nomad-village-ponta-do-sol/`)
- Curated Facet: `/coliving/[city]/[amenity-filter]/` (e.g. `/coliving/madeira/fiber-wifi-100mbps/`)
- System Pages: `/methodology/`, `/speedtest-verification/`, `/llms.txt`, `/robots.txt`

---

## 4. Edge CDN Caching & Security Headers
Both sites will deploy with security and caching configurations:
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Cache-Control: public, max-age=3600, stale-while-revalidate=86400
```
"""

with open(os.path.join(REPORTS_DIR, "12-site-architecture.md"), "w", encoding="utf-8") as f:
    f.write(r12_content)

# 13-content-automation-architecture.md
r13_content = """# Autonomous Content Engine & Multi-API Architecture

This specification details the architecture of our modular content automation pipeline, designed to decouple strategic reasoning from drafting and support interchangeable LLM providers.

---

## 1. High-Level Pipeline Architecture

```
                      ┌─────────────────────────────────┐
                      │    AGY / CLAUDE ORCHESTRATOR    │
                      │  (Topical Map, Gap & PAA Mining)│
                      └────────────────┬────────────────┘
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │     RESEARCH ENGINE ADAPTER     │
                      │ (Perplexity Sonar / Search Scrape)│
                      └────────────────┬────────────────┘
                                       │ Verified Research Packet
                                       ▼
                      ┌─────────────────────────────────┐
                      │      OUTLINE & PROMPT ENGINE    │
                      │  (GEO 9-Part Passage Anatomy)   │
                      └────────────────┬────────────────┘
                                       │ Grounded Outline
                                       ▼
                      ┌─────────────────────────────────┐
                      │     WRITER ADAPTER (BYOK)       │
                      │ (Claude 3.7 / GLM 5.2 / GPT-4o) │
                      └────────────────┬────────────────┘
                                       │ Raw First Draft
                                       ▼
                      ┌─────────────────────────────────┐
                      │    CRITIC & FACT-CHECK ENGINE   │
                      │  (Verification of Claims & Code)│
                      └────────────────┬────────────────┘
                                       │ Fact-Checked Draft
                                       ▼
                      ┌─────────────────────────────────┐
                      │    INTERNAL LINKING ENGINE      │
                      │ (Sitemap Parsing & Injections)  │
                      └────────────────┬────────────────┘
                                       │ Linked Markdown
                                       ▼
                      ┌─────────────────────────────────┐
                      │      QUALITY SCORE GATE         │
                      │   Threshold Check (Score >= 85) │
                      └────────────────┬────────────────┘
                                       │ Pass
                                       ▼
                      ┌─────────────────────────────────┐
                      │    IMAGE & VISUAL GENERATOR     │
                      │ (Fal.ai Flux / SVG Benchmarks)  │
                      └────────────────┬────────────────┘
                                       │ Complete Asset
                                       ▼
                      ┌─────────────────────────────────┐
                      │      PUBLISHER ADAPTER          │
                      │ (Git Commit to Astro Content)   │
                      └────────────────┬────────────────┘
                                       │ Deployment Trigger
                                       ▼
                      ┌─────────────────────────────────┐
                      │     API INDEXING DISPATCH       │
                      │ (Google Indexing API & Bing API)│
                      └─────────────────────────────────┘
```

---

## 2. Quality Score Gate Rubric (Threshold >= 85/100)

Every generated article is evaluated algorithmically before publication:
1. **Search Intent Satisfaction (20 Points)**: Direct H1 intent match; immediate answers provided without conversational preamble.
2. **Accuracy & Citation Grounding (20 Points)**: Every factual statistic, date, and benchmark is linked to a verified source URL.
3. **Information Gain (20 Points)**: Contains at least one original comparison table, proprietary code configuration, benchmark test, or calculation formula.
4. **Topical Completeness (10 Points)**: Covers at least 10 fan-out subtopics and PAA queries.
5. **Readability & Human Tone (10 Points)**: Absence of AI clichés ("In conclusion", "delve into", "testament", "tapestry"); active voice; code snippets formatted correctly.
6. **Internal Linking (5 Points)**: Contains 3–7 contextually relevant internal links to parent and sibling articles.
7. **UX & Semantic Formatting (5 Points)**: Proper H1->H2->H3 hierarchy, bullet points, callout boxes, and highlighted code syntax.
8. **Visual Assets (5 Points)**: At least one descriptive WebP diagram or table with descriptive alt text.
9. **Structured Schema Validation (5 Points)**: Valid JSON-LD schema matching page type.

*Automated Remediation*: If an article scores below 85, the Critic Engine generates a targeted revision prompt that re-runs the specific weak section before re-scoring.

---

## 3. Cost Modeling & API Budget Control
- **Research Phase**: Perplexity Sonar API call: ~$0.005
- **Drafting Phase**: Z.AI GLM 5.2 ($0.03) or Claude 3.5/3.7 Sonnet ($0.12)
- **Critic & Fact-Check Phase**: Claude 3.5 Haiku / GPT-4o-mini: ~$0.015
- **Visuals Phase**: Fal.ai Flux Schnell / SVG generation: ~$0.02
- **Total Estimated Cost Per Complete 2,500-Word Article**: **$0.07 to $0.17**
"""

with open(os.path.join(REPORTS_DIR, "13-content-automation-architecture.md"), "w", encoding="utf-8") as f:
    f.write(r13_content)

# 14-90-day-launch-plan.md
r14_content = """# 90-Day Staged Launch Plan & Content Velocity Roadmap

This document outlines the phased launch, crawl ramp-up, and velocity schedule for both websites to build topical authority safely without triggering algorithmic spam filters.

---

## 1. Timeline & Phased Milestone Breakdown

```
Days 1-14: Foundation & Infrastructure
   ├── Deploy Astro codebases to Netlify edge with custom domains
   ├── Configure Google Search Console, Bing Webmaster Tools, and Analytics
   ├── Verify robots.txt, llms.txt, and sitemap-index.xml
   └── Seed Initial Content:
       - Site 1: 25 Foundational Pillar Articles
       - Site 2: 10 City Hubs + 40 Programmatic Verified Properties

Days 15-30: Initial Crawl & Indexation Ramp-up
   ├── Submit published URLs to Google Indexing API and Bing Webmaster API
   ├── Monitor daily crawl activity in GSC Crawl Stats report
   ├── Target Velocity: 5 quality articles/week on Site 1; 15 curated properties/week on Site 2
   └── Verify zero 404 errors, zero schema validation errors, and sub-second TTFB

Days 31-60: Topical Authority Expansion & Internal Link Tightening
   ├── Expand into secondary clusters (Claude Code workflows, multi-GPU rigs, Asian nomad hubs)
   ├── Target Velocity: 6-8 articles/week on Site 1; 20 verified properties/week on Site 2
   ├── Conduct first automated internal linking recalculation across all published URLs
   └── First Impression Traction: Expect 5,000-15,000 monthly impressions in GSC

Days 61-90: Striking-Distance Optimization & Monetization Activation
   ├── Launch the Weekly Content Decay & Striking-Distance Refresh Loop (queries Pos 4-20)
   ├── Activate monetization links (RunPod/Lambda GPU bounties on Site 1; direct booking referrals on Site 2)
   ├── Publish original linkable benchmark reports (e.g. '2026 Local LLM Speed Index')
   └── Milestone Targets: 50,000+ monthly impressions, 2,000+ monthly clicks, initial affiliate revenue
```

---

## 2. Velocity Safeguards
- **Never exceed 8 articles/week on Site 1 during the first 30 days**: Rapid content dumping without domain trust signals triggers algorithmic review.
- **Strict Quality Threshold on Site 2**: Every property profile must pass the 15-field data completeness gate before receiving an `INDEX` meta tag. Incomplete listings remain `NOINDEX`.
"""

with open(os.path.join(REPORTS_DIR, "14-90-day-launch-plan.md"), "w", encoding="utf-8") as f:
    f.write(r14_content)

# 15-risks-and-mitigations.md
r15_content = """# Comprehensive Risk Matrix & Mitigation Strategies

This document identifies potential structural, algorithmic, operational, and commercial risks facing our two sites and outlines concrete preventive safeguards.

---

## 1. Master Risk Matrix

| # | Risk Event | Likelihood | Impact | Affected Site | Mitigation Strategy |
|---|---|---|---|---|---|
| 1 | **Google Scaled Content Abuse Penalty** | Low | Critical | Site 1 & Site 2 | Enforce the Quality Score Gate (>= 85/100); mandate original Information Gain (tables, calculations, tested configs); maintain conservative publishing velocity. |
| 2 | **Thin Programmatic Doorway Penalty** | Med | Critical | Site 2 | Never generate pages by simple text template substitution. Require 15+ verified data points, unique speedtest proof, and auto-noindex for low-inventory facets. |
| 3 | **Code Obsolescence & Library Churn** | High | Med | Site 1 | The Content Decay Engine scans GitHub releases and test commands against current library flags, triggering automated code block refreshes. |
| 4 | **Core Algorithm Update Volatility** | Med | High | Site 1 & Site 2 | Strict adherence to non-YMYL topics; transparent author bios; external entity citations on GitHub/YouTube/directories; high-DR link building. |
| 5 | **AI Search Hallucination in Citations** | Med | Med | Site 1 | Two-step research engine: all facts grounded via Perplexity/Search before LLM drafting; links to primary official documentation only. |
| 6 | **API Provider Outage or Model Deprecation** | Med | Low | Site 1 & Site 2 | Modular adapter layer supports dynamic hot-swapping between Anthropic, OpenRouter, OpenAI, and DeepSeek via unified interfaces. |
| 7 | **Affiliate Link Hijacking or Program Closure**| Low | Med | Site 1 & Site 2 | Centralized affiliate link redirection engine (`/go/[partner]`), allowing global link updates in a single configuration file. |
| 8 | **Google Image Search Traffic Evaporation** | Low | Low | Site 1 | Images hosted on fast CDN edge with descriptive alt tags; diversified traffic across Web Search, AI Overviews, and direct referral. |
| 9 | **Crawl Budget Exhaustion on Programmatic URLs**| Med | Med | Site 2 | Segmented XML sitemaps; strict canonicalization; `NOINDEX` on zero-search faceted combinations. |
| 10 | **Stale Pricing / Closed Property Data** | High | Med | Site 2 | Automated monthly verification script that pings property websites and updates the `last_verified` database timestamp. |
"""

with open(os.path.join(REPORTS_DIR, "15-risks-and-mitigations.md"), "w", encoding="utf-8") as f:
    f.write(r15_content)

print("Saved reports 12, 13, 14, 15 successfully!")
