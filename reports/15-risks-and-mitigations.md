# Comprehensive Risk Matrix & Mitigation Strategies

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
