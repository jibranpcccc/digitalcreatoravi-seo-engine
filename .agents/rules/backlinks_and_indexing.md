# Antigravity Autonomous Rules: Backlinks & Multi-Protocol Indexing

## 1. Backlink Creation Directives
- **Zero-PBN Quarantine**: Never interlink satellite sites. Every satellite site must link outward to authoritative sources, and receive inward links from independent high-DA platforms (GitHub, NPM, PyPI, Web Archives).
- **Strict Email Quarantine**: Under NO circumstances use `jibranpccc@gmail.com` for account creation or link registration. Use dedicated secondary project emails (e.g. `teams.thefusionfeed@gmail.com`) or zero-email protocols.
- **Machine Verification Guarantee**: Every link created must be verified with an active HTTP request returning `HTTP 200 OK`.
- **Master Excel & CSV Sync**: Whenever new backlinks are established, immediately update `reports/MASTER_LIVE_BACKLINKS_REPORT.csv` and regenerate `reports/MASTER_LIVE_BACKLINKS_REPORT.xlsx` with complete telemetry.

## 2. Multi-Protocol Indexing Directives
- **Deprecated Endpoints**: Never use `google.com/ping?sitemap=` (HTTP 404 retired) or `bing.com/ping?sitemap=` (HTTP 410 retired).
- **Active 5-Protocol Suite**:
  1. **Google WebSub**: `https://pubsubhubbub.appspot.com/` (HTTP 204 -> Googlebot priority crawl)
  2. **Microsoft Bing IndexNow**: `https://www.bing.com/indexnow` (HTTP 200 -> Bingbot priority queue)
  3. **Central IndexNow API**: `https://api.indexnow.org/indexnow` (HTTP 200 -> Yandex, Seznam, Naver)
  4. **Blo.gs XML-RPC**: `http://ping.blo.gs/` (HTTP 200 -> Automattic global ping stream)
  5. **Twingly XML-RPC**: `http://rpc.twingly.com/` (HTTP 200 -> European & international search crawlers)
  6. **Wayback Machine**: `https://web.archive.org/save/<url>` (Permanent archive crawl discovery)
- **Automatic Execution**: When requested to index, execute `python tools/master_search_engine_indexing_suite.py` and `python tools/broadcast_all_backlinks_xmlrpc.py`.
