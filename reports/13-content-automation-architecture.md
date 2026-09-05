# Autonomous Content Engine & Multi-API Architecture

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
