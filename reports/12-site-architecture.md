# Full Technical Website Architecture Specification

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
