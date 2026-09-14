# Antigravity Workspace Instruction & Memory: digitalcreatoravi

## 🚀 Autonomous Backlink & Indexing Directives

Whenever the user asks to **create backlinks**, **build backlinks**, **index links**, or **check rankings**:

### 1. Backlink Creation Protocol (`backlink-creator`)
- **Authority Sources (DA 74-98)**: GitHub Repositories, Releases, Gists, GitHub Pages profiles, Raw CDNs, NPM/PyPI utility packages, Web Archives (Wayback Machine), Dev Platforms, and Directories.
- **Strict Email Quarantine**: **NEVER** use `jibranpccc@gmail.com`. Use dedicated project cluster emails (e.g., `teams.thefusionfeed@gmail.com`) or zero-email authenticated CLI flows (`gh`, `npm`, `urllib`).
- **Zero-PBN Quarantine**: Never interlink satellite sites. Topology is strictly Hub-and-Spoke.
- **Live HTTP Verification**: Every backlink must be verified via HTTP `HEAD`/`GET` returning `HTTP 200 OK` before reporting.
- **Master Excel Sync**: Keep `reports/MASTER_LIVE_BACKLINKS_REPORT.xlsx` and `reports/MASTER_LIVE_BACKLINKS_REPORT.csv` up to date.

### 2. Multi-Protocol Fast Indexing Protocol (`search-engine-indexer`)
- **Active 5-Protocol Suite**:
  1. Google WebSub (`https://pubsubhubbub.appspot.com/` -> HTTP 204)
  2. Microsoft Bing IndexNow (`https://www.bing.com/indexnow` -> HTTP 200)
  3. Central IndexNow (`https://api.indexnow.org/indexnow` -> HTTP 200)
  4. Blo.gs XML-RPC (`http://ping.blo.gs/` -> HTTP 200)
  5. Twingly XML-RPC (`http://rpc.twingly.com/` -> HTTP 200)
- **Deprecated Endpoints**: Do not use `google.com/ping?sitemap` (404) or `bing.com/ping?sitemap` (410).

### 3. Immediate CLI Shortcuts
- Full Pipeline: `python tools/create_and_index_backlinks.py --all`
- 1-Click Windows Batch: `RUN_INDEXING_AND_BACKLINKS.bat`
- Master Fleet Indexing: `python tools/master_search_engine_indexing_suite.py`
- Backlink XML-RPC Broadcast: `python tools/broadcast_all_backlinks_xmlrpc.py`
- Live Probing & Excel Report: `python tools/verify_and_generate_excel_report.py`

---

## ✍️ Content Architecture & Anti-Fluff Protocol (`fleet-content-architect`)

Whenever creating, updating, or reviewing content across the 20-site fleet:

### 1. The Anti-"Mumble Jumble" Design & Formatting Standard
- **Zero Raw Wall of Text**: Content must NEVER be written as unformatted paragraphs. Every guide must have clear, structured breathing room.
- **Word Count & Structure**: Minimum **1,500 – 2,500 words** with **6 to 10 descriptive, keyword-rich H2 headings** (never generic headings like "Introduction" or "Overview").
- **Google Quick Answer Callout**: A 45–60 word direct, bolded answer box in the first 800 characters featuring a 4px theme-accent border (`bg-slate-900/60 p-6 rounded-xl border-l-4`).
- **Empirical Benchmark Tables**: Every article MUST include at least 1–2 structured comparison tables with dark slate headers (`#0f172a`), `#334155` borders, zebra striping, and clear numeric units (latency ms, QPS, pricing USD, RAM GB).
- **Executable Code & Mathematical Proofs**: Include syntax-highlighted, copyable code blocks (Python, TypeScript, SQL, Bash) with error-handling failure modes or formal algebraic proofs. In Astro, use `<pre is:raw>` or escape `${{` with `&#36;{{` to prevent Vite JSX AST crashes.
- **Interactive Calculators / Sizers**: Embed client-side vanilla JS interactive tools (fee sliders, runway estimators, memory calculators) for maximum dwell time and near-zero bounce rates.
- **Structured Data JSON-LD**: Embed valid Schema `@graph` containing `TechArticle` / `Article`, `FAQPage` (minimum 3 QA pairs), and `BreadcrumbList`.

---

## 🔍 Keyword Research & Content Gap Protocol (`seo-keyword-intelligence`)

Whenever researching keywords or expanding content coverage:

### 1. Keyword Research Methodology
- **Intent-Driven Clustering**:
  - **TOFU (Top-of-Funnel / Informational)**: Architecture patterns, formulas, algorithms, syntax comparisons.
  - **MOFU (Middle-of-Funnel / Commercial Investigation)**: Head-to-head benchmarks (e.g. `X vs Y`, `Best A for B 2026`).
  - **BOFU (Bottom-of-Funnel / Transactional)**: TCO calculators, migration scripts, pricing breakdowns, visa checklists.
- **Zero-Search-Volume & High-Intent Strategy**: Target specific technical queries (e.g. `devcontainer feature pgvector ollama gpu passthrough`) that keyword tools mark as 0-10 volume but have 100% developer purchase/setup intent.
- **Query Modifiers**: Programmatically cross-join base topics with modifiers: `[tool A] vs [tool B] benchmark 2026`, `[framework] cold start latency`, `[service] pricing hidden fees`, `how to calculate [metric] formula`.

### 2. Content Gap Discovery & Fill Process
- **Competitor SERP Reversal**: Identify what top-ranking pages omit (e.g., real production benchmarks, edge failure modes, concrete dollar pricing, code implementations).
- **Entity Coverage Matrix**: Ensure primary NLP entities (libraries, RFCs, laws, protocols) are present in the text with precise semantic context.
- **FAQ & People Also Ask Integration**: Directly address the top 3–5 searcher objections/questions in dedicated H2/H3 sections mapped to FAQPage schema.

