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
