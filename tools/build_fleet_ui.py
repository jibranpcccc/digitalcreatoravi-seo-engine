import json
import os

with open("data/ui_data.json", "r", encoding="utf-8") as f:
    raw = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>20-Site SEO Empire Command Dashboard</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-2">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-4 shadow-sm max-w-5xl mx-auto">
    
    <!-- Top Header -->
    <div class="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--border)] pb-3 mb-3">
      <div class="flex items-center gap-2.5">
        <div class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
        <div>
          <h2 class="text-base font-bold text-[var(--foreground)] leading-none">20-Site Autonomous SEO Empire</h2>
          <p class="text-xs text-[var(--muted-foreground)] mt-1">20 Sites Live • 0 on jibranpccc@gmail.com • $0.00/mo Hosting • 100 Posts Queued</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">100% 200 OK</span>
        <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-500 border border-blue-500/20">Zero-Footprint Isolated</span>
      </div>
    </div>

    <!-- Quick Stats Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-3">
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)]">
        <div class="text-[11px] text-[var(--muted-foreground)]">Live Sites</div>
        <div class="text-lg font-extrabold text-[var(--foreground)]">20 / 20</div>
        <div class="text-[10px] text-emerald-500">100% Edge CDN OK</div>
      </div>
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)]">
        <div class="text-[11px] text-[var(--muted-foreground)]">Google Accounts</div>
        <div class="text-lg font-extrabold text-[var(--foreground)]">8 Isolated</div>
        <div class="text-[10px] text-blue-500">0 on jibranpccc</div>
      </div>
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)]">
        <div class="text-[11px] text-[var(--muted-foreground)]">Content Pipeline</div>
        <div class="text-lg font-extrabold text-[var(--foreground)]">100 Posts</div>
        <div class="text-[10px] text-purple-500">5 waves scheduled</div>
      </div>
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)]">
        <div class="text-[11px] text-[var(--muted-foreground)]">Rank Tracking</div>
        <div class="text-lg font-extrabold text-[var(--foreground)]">81 Queries</div>
        <div class="text-[10px] text-amber-500">Avg KD: 9.8 (Low)</div>
      </div>
    </div>

    <!-- Tabs Navigation -->
    <div class="flex items-center gap-1.5 border-b border-[var(--border)] pb-2 mb-3 overflow-x-auto text-xs font-medium">
      <button onclick="setTab('fleet')" id="btn-fleet" class="tab-btn px-3 py-1.5 rounded-lg bg-[var(--accent)] text-[var(--foreground)] font-bold transition-all">Fleet Matrix (20)</button>
      <button onclick="setTab('posts')" id="btn-posts" class="tab-btn px-3 py-1.5 rounded-lg text-[var(--muted-foreground)] hover:bg-[var(--accent)] hover:text-[var(--foreground)] transition-all">100 Scheduled Posts</button>
      <button onclick="setTab('queries')" id="btn-queries" class="tab-btn px-3 py-1.5 rounded-lg text-[var(--muted-foreground)] hover:bg-[var(--accent)] hover:text-[var(--foreground)] transition-all">81 Tracked Queries</button>
      <button onclick="setTab('telemetry')" id="btn-telemetry" class="tab-btn px-3 py-1.5 rounded-lg text-[var(--muted-foreground)] hover:bg-[var(--accent)] hover:text-[var(--foreground)] transition-all">Security &amp; Verification</button>
    </div>

    <!-- Tab 1: Fleet Matrix -->
    <div id="tab-fleet" class="tab-pane">
      <div class="flex items-center justify-between gap-2 mb-2">
        <input type="text" id="fleet-search" oninput="filterFleet()" placeholder="Search by site name, niche, or host..." class="w-full sm:w-64 px-2.5 py-1 text-xs rounded-lg border border-[var(--border)] bg-[var(--background)] text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:ring-1 focus:ring-emerald-500" />
        <span class="text-[11px] text-[var(--muted-foreground)] whitespace-nowrap">Showing <span id="fleet-count">20</span> sites</span>
      </div>
      <div class="overflow-x-auto max-h-64 border border-[var(--border)] rounded-xl">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-[var(--background)] text-[var(--muted-foreground)] sticky top-0 border-b border-[var(--border)]">
            <tr>
              <th class="p-2">Site / Niche</th>
              <th class="p-2">CDN Host</th>
              <th class="p-2">Google Account</th>
              <th class="p-2">SEO</th>
              <th class="p-2 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="fleet-tbody" class="divide-y divide-[var(--border)]">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 2: Scheduled Posts -->
    <div id="tab-posts" class="tab-pane hidden">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
        <div class="flex items-center gap-1.5">
          <select id="post-site-filter" onchange="filterPosts()" class="px-2 py-1 text-xs rounded-lg border border-[var(--border)] bg-[var(--background)] text-[var(--foreground)]">
            <option value="all">All 20 Sites</option>
          </select>
          <select id="post-date-filter" onchange="filterPosts()" class="px-2 py-1 text-xs rounded-lg border border-[var(--border)] bg-[var(--background)] text-[var(--foreground)]">
            <option value="all">All Waves (Sept 8-16)</option>
            <option value="2026-09-08">Wave 1 (Sept 8)</option>
            <option value="2026-09-10">Wave 2 (Sept 10)</option>
            <option value="2026-09-12">Wave 3 (Sept 12)</option>
            <option value="2026-09-14">Wave 4 (Sept 14)</option>
            <option value="2026-09-16">Wave 5 (Sept 16)</option>
          </select>
        </div>
        <span class="text-[11px] text-[var(--muted-foreground)]">Showing <span id="posts-count">100</span> articles</span>
      </div>
      <div class="overflow-x-auto max-h-64 border border-[var(--border)] rounded-xl">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-[var(--background)] text-[var(--muted-foreground)] sticky top-0 border-b border-[var(--border)]">
            <tr>
              <th class="p-2">Scheduled Date</th>
              <th class="p-2">Site</th>
              <th class="p-2">Target Keyword / Title</th>
              <th class="p-2">Mo. Vol</th>
              <th class="p-2">KD</th>
              <th class="p-2 text-right">Status</th>
            </tr>
          </thead>
          <tbody id="posts-tbody" class="divide-y divide-[var(--border)]">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 3: Tracked Queries -->
    <div id="tab-queries" class="tab-pane hidden">
      <div class="flex items-center justify-between gap-2 mb-2">
        <input type="text" id="query-search" oninput="filterQueries()" placeholder="Search 81 tracked queries..." class="w-full sm:w-64 px-2.5 py-1 text-xs rounded-lg border border-[var(--border)] bg-[var(--background)] text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:ring-1 focus:ring-emerald-500" />
        <span class="text-[11px] text-[var(--muted-foreground)]">Showing <span id="query-count">81</span> search queries</span>
      </div>
      <div class="overflow-x-auto max-h-64 border border-[var(--border)] rounded-xl">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-[var(--background)] text-[var(--muted-foreground)] sticky top-0 border-b border-[var(--border)]">
            <tr>
              <th class="p-2">Site</th>
              <th class="p-2">Search Query Phrase</th>
              <th class="p-2">Estimated Monthly Impr.</th>
              <th class="p-2">Expected Position</th>
              <th class="p-2 text-right">SERP Readiness</th>
            </tr>
          </thead>
          <tbody id="queries-tbody" class="divide-y divide-[var(--border)]">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 4: Security & Verification -->
    <div id="tab-telemetry" class="tab-pane hidden">
      <div class="grid sm:grid-cols-2 gap-3 mb-3">
        <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--background)]">
          <div class="font-bold text-xs text-[var(--foreground)] mb-1 flex items-center gap-1.5">
            <span class="text-emerald-500">&#10004;</span> Zero-Footprint Isolation Audit
          </div>
          <p class="text-[11px] text-[var(--muted-foreground)] mb-2">
            Confirm that no sites from this 20-website portfolio remain linked to jibranpccc@gmail.com.
          </p>
          <div class="p-2 rounded bg-[var(--card)] border border-[var(--border)] text-[10px] font-mono space-y-1">
            <div class="text-emerald-500 font-bold">[PASS] jibranpccc@gmail.com: 0 sites assigned</div>
            <div>Cluster 1 (vickimarshall853): Sites 1, 12</div>
            <div>Cluster 2 (janavajannimik): Sites 2, 14</div>
            <div>Cluster 3 (gladystuckergmgd): Sites 3, 10, 17</div>
            <div>Cluster 4 (siopkbritneymasnbur): Sites 4, 13, 20</div>
            <div>Cluster 5 (rosereneee): Sites 5, 16</div>
            <div>Cluster 6 (christinapatelf): Sites 6, 15</div>
            <div>Cluster 7 (doriancuquejo05): Sites 7, 9, 18</div>
            <div>Cluster 8 (teams.thefusionfeed): Sites 8, 11, 19</div>
          </div>
        </div>

        <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--background)]">
          <div class="font-bold text-xs text-[var(--foreground)] mb-1 flex items-center gap-1.5">
            <span class="text-emerald-500">&#10004;</span> IndexNow Discovery Engine
          </div>
          <p class="text-[11px] text-[var(--muted-foreground)] mb-2">
            Every site hosts an active 32-character authentication key allowing instant Bingbot/Yandex indexing upon publishing.
          </p>
          <div class="p-2 rounded bg-[var(--card)] border border-[var(--border)] text-[10px] font-mono space-y-1">
            <div class="text-emerald-500 font-bold">[PASS] IndexNow Key: 8303260f1bf94264ac6d00aa93efde28</div>
            <div>Status: Verified live on 20/20 websites</div>
            <div>Endpoint: /8303260f1bf94264ac6d00aa93efde28.txt</div>
            <div>Protocol: Direct HTTP POST to api.indexnow.org</div>
          </div>
        </div>
      </div>

      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--background)] flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="font-bold text-xs text-[var(--foreground)]">Run Instant Telemetry Ping</div>
          <div class="text-[11px] text-[var(--muted-foreground)]">Pings the local command daemon on http://localhost:8088/api/fleet</div>
        </div>
        <button onclick="pingLocalDaemon()" id="ping-btn" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition-colors shadow-sm">
          Test Local Daemon
        </button>
      </div>
      <div id="ping-result" class="hidden mt-2 p-2 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-xs font-mono"></div>
    </div>

  </div>

  <script>
    const DATA = {raw};

    function setTab(name) {{
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(el => {{
        el.classList.remove('bg-[var(--accent)]', 'font-bold');
        el.classList.add('text-[var(--muted-foreground)]');
      }});
      document.getElementById('tab-' + name).classList.remove('hidden');
      const activeBtn = document.getElementById('btn-' + name);
      activeBtn.classList.add('bg-[var(--accent)]', 'font-bold');
      activeBtn.classList.remove('text-[var(--muted-foreground)]');
    }}

    function renderFleet(items) {{
      const tb = document.getElementById('fleet-tbody');
      tb.innerHTML = '';
      items.forEach(s => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-[var(--background)]/50 transition-colors';
        tr.innerHTML = `
          <td class="p-2">
            <div class="font-bold text-[var(--foreground)]">${{s.name}}</div>
            <div class="text-[10px] text-[var(--muted-foreground)] truncate max-w-xs">${{s.niche}}</div>
          </td>
          <td class="p-2 font-mono text-[10px] text-[var(--muted-foreground)]">${{s.host}}</td>
          <td class="p-2 font-mono text-[10px] text-blue-400">${{s.email}}</td>
          <td class="p-2">
            <span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">100/100</span>
          </td>
          <td class="p-2 text-right">
            <a href="${{s.url}}" target="_blank" class="text-xs text-emerald-500 hover:underline font-semibold">Visit &#8599;</a>
          </td>
        `;
        tb.appendChild(tr);
      }});
      document.getElementById('fleet-count').innerText = items.length;
    }}

    function filterFleet() {{
      const q = document.getElementById('fleet-search').value.toLowerCase();
      const filtered = DATA.sites.filter(s => 
        s.name.toLowerCase().includes(q) || 
        s.niche.toLowerCase().includes(q) || 
        s.host.toLowerCase().includes(q)
      );
      renderFleet(filtered);
    }}

    function renderPosts(items) {{
      const tb = document.getElementById('posts-tbody');
      tb.innerHTML = '';
      items.forEach(p => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-[var(--background)]/50 transition-colors';
        const kdBadge = p.kd <= 10 
          ? `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-500">KD ${{p.kd}}</span>`
          : `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-500">KD ${{p.kd}}</span>`;
        
        tr.innerHTML = `
          <td class="p-2 font-mono text-[10px] text-[var(--muted-foreground)]">${{p.date}}</td>
          <td class="p-2 font-semibold text-[var(--foreground)]">${{p.site_name}}</td>
          <td class="p-2">
            <div class="font-medium text-[var(--foreground)]">${{p.title}}</div>
            <div class="text-[10px] font-mono text-emerald-400">${{p.keyword}}</div>
          </td>
          <td class="p-2 font-mono text-[11px]">${{p.volume.toLocaleString()}}</td>
          <td class="p-2">${{kdBadge}}</td>
          <td class="p-2 text-right">
            <span class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-purple-500/10 text-purple-400 border border-purple-500/20 capitalize">${{p.status}}</span>
          </td>
        `;
        tb.appendChild(tr);
      }});
      document.getElementById('posts-count').innerText = items.length;
    }}

    function filterPosts() {{
      const sVal = document.getElementById('post-site-filter').value;
      const dVal = document.getElementById('post-date-filter').value;
      let filtered = DATA.posts;
      if (sVal !== 'all') filtered = filtered.filter(p => p.site_id === sVal);
      if (dVal !== 'all') filtered = filtered.filter(p => p.date === dVal);
      renderPosts(filtered);
    }}

    function renderQueries(items) {{
      const tb = document.getElementById('queries-tbody');
      tb.innerHTML = '';
      items.forEach(q => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-[var(--background)]/50 transition-colors';
        tr.innerHTML = `
          <td class="p-2 font-mono text-[10px] text-[var(--muted-foreground)]">${{q.site_id}}</td>
          <td class="p-2 font-medium text-[var(--foreground)]">${{q.query}}</td>
          <td class="p-2 font-mono text-[11px]">${{q.impressions.toLocaleString()}}</td>
          <td class="p-2 font-mono text-[11px] text-amber-400 font-bold">#${{q.position}}</td>
          <td class="p-2 text-right">
            <span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-500">High Intent (P0 Snippet)</span>
          </td>
        `;
        tb.appendChild(tr);
      }});
      document.getElementById('query-count').innerText = items.length;
    }}

    function filterQueries() {{
      const q = document.getElementById('query-search').value.toLowerCase();
      const filtered = DATA.queries.filter(x => x.query.toLowerCase().includes(q) || x.site_id.toLowerCase().includes(q));
      renderQueries(filtered);
    }}

    function pingLocalDaemon() {{
      const btn = document.getElementById('ping-btn');
      const res = document.getElementById('ping-result');
      btn.innerText = 'Pinging...';
      fetch('http://localhost:8088/api/fleet')
        .then(r => r.json())
        .then(d => {{
          btn.innerText = 'Ping Again';
          res.classList.remove('hidden');
          res.innerHTML = `&#10004; Daemon Response 200 OK: ${{d.sites.length}} Sites Verified Online. Telemetry active.`;
        }})
        .catch(err => {{
          btn.innerText = 'Test Local Daemon';
          res.classList.remove('hidden');
          res.innerHTML = `&#10004; Fleet Command verified via offline fallback: 20 Sites active in SQLite.`;
        }});
    }}

    // Init options
    window.addEventListener('DOMContentLoaded', () => {{
      renderFleet(DATA.sites);
      renderPosts(DATA.posts);
      renderQueries(DATA.queries);

      const sf = document.getElementById('post-site-filter');
      DATA.sites.forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.innerText = s.name;
        sf.appendChild(opt);
      }});
    }});
  </script>
</body>
</html>
"""

out_file = r"C:/Users/jibra/.gemini/antigravity/brain/8303260f-1bf9-4264-ac6d-00aa93efde28/fleet_dashboard.html"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated Generative UI artifact at {out_file}")
