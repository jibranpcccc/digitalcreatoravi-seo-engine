# The Extracted SEO Operating System: Reverse-Engineered Playbook

This playbook reconstructs the complete end-to-end SEO operating system derived from Digital Creator Avi's 6 months of public methodologies, synthesized into actionable execution protocols.

---

## Architecture of the Operating System

```
┌────────────────────────────────────────────────────────┐
│             CLAUDE CODE / AGY ORCHESTRATOR             │
│   (Keyword Mining, SERP Intelligence, Topical Map)     │
└───────────┬────────────────────────────────┬───────────┘
            │                                │
            ▼                                ▼
┌───────────────────────────┐    ┌───────────────────────┐
│     RESEARCH ENGINE       │    │  TECHNICAL PLATFORM   │
│ - Google Trends News      │    │ - Static HTML (Astro) │
│ - Perplexity Live Web     │    │ - Netlify Edge CDN    │
│ - PAA Fan-Out Extraction  │    │ - llms.txt & ai.json  │
│ - Competitor Gap Analysis │    │ - Valid Schema.org    │
└───────────┬───────────────┘    └───────────┬───────────┘
            │                                │
            ▼                                │
┌───────────────────────────┐                │
│    CONTENT DRAFTING       │                │
│ - BYOK API (Sonnet / GLM) │                │
│ - Quick Answer Block      │                │
│ - Key Takeaways           │                │
│ - Custom HTML Tables      │                │
│ - Fal.ai WebP Diagrams    │                │
│ - In-Text Citations       │                │
└───────────┬───────────────┘                │
            │                                │
            ▼                                │
┌───────────────────────────┐                │
│   QUALITY GATE & LINKING  │                │
│ - Quality Score >= 85/100 │                │
│ - Sitemap Semantic Ingest │                │
│ - 3-7 Internal Links      │                │
└───────────┬───────────────┘                │
            │                                │
            ▼                                ▼
┌────────────────────────────────────────────────────────┐
│            AUTOMATED PUBLISHING & DISPATCH             │
│        (Git Push / Webhook to Static Edge Site)        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│            INDEXING PUSH & GEO FEEDBACK LOOP           │
│   - Google Indexing API & Bing Push                    │
│   - Weekly Content Decay Audit (Striking Distance)     │
│   - GSC Generative AI Citation Tracking                │
│   - Automated Content Refresh Engine                   │
└────────────────────────────────────────────────────────┘
```

---

## Module 1: Market & Keyword Research Protocol
1. **Low-Competition Long-Tail Queries**:
   - Target queries with search volume between 100 and 1,500/month where top SERP results are stale (2+ years old), forum posts (Reddit/Quora), or generalist directory pages.
2. **Breakout / Trending News Engine**:
   - Scan Google Trends and Google News within the niche on a 24-hour lookback. Identify emerging terminology or regulatory updates before KD (Keyword Difficulty) rises.
3. **Fan-Out Query Expansion**:
   - For every seed keyword, identify 10–15 tangential sub-questions that searchers ask next. Group these into a single comprehensive guide rather than splintering into thin individual posts.
4. **Exact Match & Topical Domain Alignment**:
   - Favor descriptive, entity-rich domain names that reinforce niche topical authority.

---

## Module 2: Technical Platform & Site Architecture
1. **Zero-Bloat Static HTML**:
   - Build using modern static site generators (Astro or Next.js SSG).
   - Ensure Core Web Vitals targets: LCP < 0.8s, CLS = 0.00, INP < 50ms, PageSpeed 95+.
2. **AI Crawler Transparency Layer**:
   - `llms.txt`: Curated markdown file at the root listing all core pillar pages, categories, and direct summaries.
   - `ai.json`: Machine-readable declaration of site entity, author, licensing, and contact points.
   - `robots.txt`: Unrestrictive crawling access for Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot.
3. **Structured Data Injection**:
   - `LocalBusiness` / `MedicalBusiness` / `Organization` with exact NAP.
   - `Service` schema on specific service offerings.
   - `BlogPosting` with author, publisher, datePublished, and dateModified.
   - `FAQPage` schema corresponding to on-page accordion elements.
   - `BreadcrumbList` for category depth.

---

## Module 3: Grounded Content Creation Protocol
1. **Grounding Phase**:
   - Fetch live factual search results via Perplexity Sonar API or search scraper. Extract 3–5 verified data points, dates, and authoritative source URLs.
2. **Drafting Phase**:
   - Enforce the 9-part passage-level GEO anatomy:
     - Part 1: H1 Intent Match Title.
     - Part 2: Quick Answer (40–60 words, direct factual response).
     - Part 3: Last Reviewed / Updated Date.
     - Part 4: Key Takeaways (3–5 bullet points).
     - Part 5: Custom HTML element (table or comparison box).
     - Part 6: Fan-out H2/H3 subheadings answering related queries.
     - Part 7: WebP custom image/diagram with descriptive alt text.
     - Part 8: In-text citations linking to official primary sources.
     - Part 9: FAQ section.
3. **Quality Gate Filter**:
   - Score draft across: Intent Satisfaction (20), Accuracy (20), Information Gain (20), Topical Completeness (10), Readability (10), Internal Linking (5), UX Formatting (5), Visuals (5), Schema (5).
   - Require score >= 85/100. If lower, run automated revision pass.

---

## Module 4: Automated Internal Linking Engine
1. **Sitemap Ingestion**:
   - Regularly crawl `sitemap.xml` to maintain a live directory of published URLs and their primary entity keywords.
2. **Bidirectional Link Injection**:
   - When a new page is published, parse the existing database to identify the 3–7 most contextually relevant parent and sibling articles.
   - Inject natural contextual links from old articles pointing TO the new article, and from the new article pointing back TO the existing pillars.
3. **Anchor Text Diversity**:
   - Enforce 60% partial-match / natural descriptive anchors, 20% branded / navigational, and 20% topical entity phrases. Avoid repetitive exact-match anchors.

---

## Module 5: Indexing & Launch Strategy
1. **Phased Publishing Batches**:
   - Launch Day: Deploy core architecture + initial 20–30 high-authority pillar articles.
   - Weeks 1–4: Publish at a steady velocity of 5–8 articles/week to build crawl frequency without triggering spam filters.
2. **Multi-Engine API Push**:
   - Automatically submit every newly published URL to Google Indexing API and Bing Webmaster API upon deployment.
   - Verify indexation status weekly via GSC URL Inspection API.

---

## Module 6: Content Decay & Weekly SEO Loop
1. **Striking Distance Identification**:
   - Identify queries ranking in positions 4–20 with high impressions but low CTR.
2. **Automated Content Refresh Engine**:
   - Re-scrape ranking URL.
   - Add new 2026 data points, updated pricing, or fresh statistics.
   - Deepen thin sections and add 2–3 new fan-out questions.
   - Update `dateModified` timestamp.
   - Re-submit for immediate re-indexing.
3. **E-E-A-T & Entity Defense**:
   - Embed real expert bios, real credentials, and YouTube video assets to insulate the site against algorithmic Core Updates.
