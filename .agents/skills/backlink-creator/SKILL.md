---
name: backlink-creator
description: "Autonomous high-authority backlink builder and syndication engine. Creates 100% verified, white-hat, dofollow and nofollow backlinks across DA 74-98 platforms: standalone GitHub repositories, GitHub Releases, Gists, GitHub Pages landing pages, CDN endpoints, open-source packages (NPM/PyPI), Web Archives, dev platforms, and tech directories without link farms or PBN footprints. Strict quarantine against personal emails. Use when user says 'create backlinks', 'build backlinks', 'backlink strategy', 'backlinks easily', 'get backlinks', 'make backlinks', or 'backlink generator'."
user-invocable: true
argument-hint: "<target_url_or_portfolio>"
license: MIT
metadata:
  version: "1.0.0"
  category: seo-backlinks
---

# 🚀 Backlink Creator: High-Authority Autonomous Link Engine

A battle-tested blueprint and automation engine for building verified, permanent, high-authority backlinks (DA 74 to DA 98) for web applications, SaaS products, financial tools, and digital portfolios without paid links, spam farms, or PBN footprints.

---

## 🛡️ Critical Operating Rules & Security Constraints

1. **Strict Email Quarantine**:
   - **NEVER** use primary personal email addresses (e.g. `jibranpccc@gmail.com`).
   - Use dedicated secondary project cluster emails (e.g. `teams.thefusionfeed@gmail.com`).
   - For zero-email methods (GitHub CLI via existing auth, Wayback Machine, IndexNow, XML-RPC, RSS), NO email is attached.
2. **Zero-PBN Quarantine (Anti-Footprint)**:
   - **NEVER** cross-link satellite websites directly to each other (e.g., Site A linking to Site B).
   - Maintain strict **Hub-and-Spoke** topology: all satellite sites link outward to authoritative external references and inward from independent authority hubs (GitHub, PyPI, NPM, Web Archives).
3. **100% Verified Live Deliverables**:
   - Every single link generated must be actively probed via HTTP `HEAD`/`GET`.
   - Must return `HTTP 200 OK`.
   - Must be logged in `.csv` and styled `.xlsx` reports with anchor context and latency telemetry.

---

## 🏛️ The 10 High-DA Authority Tiers

### Tier 1: GitHub Developer Suite (DA 96) — 100% Automated
- **Standalone Repositories**: Create dedicated public repo for each tool (`gh repo create <repo-name> --public --homepage <site-url>`).
- **Official Releases**: Tag and publish production releases (`gh release create v1.0.0 --title "v1.0.0 Production Release"`).
- **Benchmark Specifications**: Publish technical issue specs (`gh issue create --title "Benchmark Specs" --body "..."`).
- **Runnable Gists**: Publish standalone open-source code snippets linking to the web app (`gh gist create ...`).
- **GitHub Pages Subpages**: Deploy dedicated mobile-responsive tool showcase pages on `https://<user>.github.io/tools/<tool>.html`.
- **Raw CDN Endpoints**: Raw README CDN endpoints on `https://raw.githubusercontent.com/<user>/<repo>/master/README.md`.

### Tier 2: Open-Source Package Registries (DA 88 - 94)
- **NPM (`npmjs.com` - DA 94)**: Publish lightweight calculation utility packages with `--homepage` set to the live tool URL.
- **PyPI (`pypi.org` - DA 94)**: Publish Python SDK wrapper packages with `project_urls` metadata linking to documentation and live tool.
- **Docker Hub (`hub.docker.com` - DA 93)**: Public container images with external documentation link.

### Tier 3: Web Archives & Open Science (DA 86 - 96) — Zero Email
- **Wayback Machine (`web.archive.org` - DA 96)**: Snapshot web apps and documentation via `https://web.archive.org/save/<url>`.
- **Archive.today (`archive.ph` - DA 86)**: Permanent timestamped archive snapshot.
- **Zenodo (`zenodo.org` - DA 88)**: Register open-source datasets or software research with permanent DOIs.

### Tier 4: Developer Sandboxes & Cloud IDEs (DA 85 - 92)
- **CodePen (`codepen.io` - DA 92)**: Embeddable interactive UI widgets linking to the live engine.
- **JSFiddle (`jsfiddle.net` - DA 90)**: Code demo showcasing API integration.
- **Replit (`replit.com` - DA 90)**: Public demo Repl.
- **Hugging Face (`huggingface.co` - DA 92)**: Public Space or Model Card linking to benchmark data.

### Tier 5: Technical Document & PDF Publishing (DA 88 - 95)
- **Edge PDF Whitepapers**: Compile and host downloadable PDF cheatsheets (`<site-url>/benchmark-cheatsheet.pdf`).
- **SlideShare (`slideshare.net` - DA 94)**: Upload slide decks of technical benchmarks.
- **SpeakerDeck (`speakerdeck.com` - DA 88)**: Upload technical presentations.

### Tier 6: Tech Publishing & Dev Platforms (DA 82 - 93)
- **Dev.to (DA 88)**: In-depth technical tutorial with canonical link to the tool page.
- **Hashnode (DA 87)**: Engineering blog post with source code link.
- **Medium (DA 93)**: Case study / benchmark comparison with dofollow citations.

### Tier 7: Bio-Links & Social Engineering Profiles (DA 84 - 93)
- **Linktree (DA 93)**: Portfolio link cluster with categorized utility links.
- **Bento.me (DA 86)**: Developer grid showcase.
- **Bio.link (DA 84)**: Clean utility link hub.

### Tier 8: Startup Launchpads & Directories (DA 80 - 92)
- **ProductHunt (DA 91)**: Free product launch listing & maker page.
- **BetaList (DA 84)**: Startup discovery submission.
- **AlternativeTo (DA 85)**: List open-source tool as alternative to proprietary software.
- **Toolify.ai (DA 80)**: AI & web tool catalog listing.

### Tier 9: Data Science & Academic Hubs (DA 85 - 91)
- **Kaggle (DA 91)**: Public dataset or notebook citation.
- **Figshare (DA 88)**: Open academic benchmark repository.

### Tier 10: RSS Aggregators & Syndication Directories (DA 74 - 90)
- **Feedly (DA 90)**: RSS feed submission.
- **Feedspot (DA 82)**: Top tools & blogs directory listing.
- **AllTop (DA 78)**: Niche aggregator inclusion.

---

## ⚡ Quick Execution Commands

To create or verify backlinks autonomously, run the following commands:

```bash
# 1. Probe all live backlinks and generate Excel report
python tools/verify_and_generate_excel_report.py

# 2. Archive all live sites and assets on Wayback Machine
python tools/archive_all_sites_wayback.py

# 3. Broadcast XML-RPC signals for all backlink hubs
python tools/broadcast_all_backlinks_xmlrpc.py
```
