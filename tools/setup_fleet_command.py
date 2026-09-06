import os
import json
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DASHBOARD_DIR = os.path.join(ROOT_DIR, "dashboard")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)

# 1. Initialize SQLite Database
DB_PATH = os.path.join(DATA_DIR, "fleet_telemetry.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS sites (
    id TEXT PRIMARY KEY,
    name TEXT,
    niche TEXT,
    url TEXT,
    sitemap_url TEXT,
    host TEXT,
    gsc_cluster TEXT,
    gsc_email TEXT,
    seo_score INTEGER,
    verified_gsc INTEGER DEFAULT 1,
    verified_indexnow INTEGER DEFAULT 1,
    last_audit_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS traffic_hits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    path TEXT,
    full_url TEXT,
    referrer TEXT,
    user_agent TEXT,
    device TEXT,
    country TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS webmaster_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    score INTEGER,
    verified_urls INTEGER,
    issues_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Seed Fleet Data (8 live sites)
fleet_seeds = [
    ("site-1", "LocalAgentStack", "Local AI Hardware & Inference", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/sitemap.xml", "GitHub Pages (Fastly CDN)", "Cluster 1", "jibranpccc@gmail.com", 100, 1, 1, "200 OK"),
    ("site-2", "WorkationRadar", "Digital Nomad & Coliving Spaces", "https://jibranpcccc.github.io/workationradar/", "https://jibranpcccc.github.io/workationradar/sitemap.xml", "GitHub Pages (Fastly CDN)", "Cluster 1", "jibranpccc@gmail.com", 100, 1, 1, "200 OK"),
    ("site-3", "OpenAgentStack", "Autonomous Agents & MCP Protocols", "https://openagentstack.pages.dev/", "https://openagentstack.pages.dev/sitemap.xml", "Cloudflare Pages Edge", "Cluster 1", "jibranpccc@gmail.com", 100, 1, 1, "200 OK"),
    ("site-4", "IndieStackAudit", "Micro-SaaS Tech Stacks & MoR Billing", "https://indiestackaudit.pages.dev/", "https://indiestackaudit.pages.dev/sitemap.xml", "Cloudflare Pages Edge", "Cluster 1", "jibranpccc@gmail.com", 100, 1, 1, "200 OK"),
    ("site-5", "VectorBench", "AI Vector DB & Embedding Benchmarks", "https://vectorbench-hq.netlify.app/", "https://vectorbench-hq.netlify.app/sitemap.xml", "Netlify Edge CDN", "Cluster 2", "rosereneee@gmail.com (Profile 2)", 100, 1, 1, "200 OK"),
    ("site-6", "NomadTreaty", "Digital Nomad Tax & Visas", "https://nomadtreaty.vercel.app/", "https://nomadtreaty.vercel.app/sitemap.xml", "Vercel Global Anycast", "Cluster 2", "rosereneee@gmail.com (Profile 2)", 100, 1, 1, "200 OK"),
    ("site-7", "WebhookWatch", "Webhook Architecture & Reliability", "https://webhookwatch.vercel.app/", "https://webhookwatch.vercel.app/sitemap.xml", "Vercel Global Anycast", "Cluster 3", "doriancuquejo05@gmail.com (Profile 3)", 100, 1, 1, "200 OK"),
    ("site-8", "LocalDocPrivacy", "Client-Side WASM Document Security", "https://localdocprivacy.netlify.app/", "https://localdocprivacy.netlify.app/sitemap.xml", "Netlify Edge CDN", "Cluster 4", "teams.thefusionfeed@gmail.com (Profile 4)", 100, 1, 1, "200 OK")
]

for s in fleet_seeds:
    c.execute("""
    INSERT INTO sites (id, name, niche, url, sitemap_url, host, gsc_cluster, gsc_email, seo_score, verified_gsc, verified_indexnow, last_audit_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name=excluded.name,
        niche=excluded.niche,
        url=excluded.url,
        sitemap_url=excluded.sitemap_url,
        host=excluded.host,
        gsc_cluster=excluded.gsc_cluster,
        gsc_email=excluded.gsc_email,
        seo_score=excluded.seo_score,
        last_audit_status=excluded.last_audit_status
    """, s)

# Seed realistic initial baseline hits to verify analytics visualization
initial_hits = [
    ("site-1", "/", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/", "https://www.google.com/", "Chrome/Desktop", "Desktop", "US"),
    ("site-1", "/hardware/vram-requirements-calculator-70b/", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/vram-requirements-calculator-70b/", "https://www.google.com/", "Chrome/Desktop", "Desktop", "DE"),
    ("site-2", "/space/ponta-do-sol-nomad-coliving/", "https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/", "https://www.bing.com/", "Edge/Desktop", "Desktop", "PT"),
    ("site-3", "/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/", "https://openagentstack.pages.dev/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/", "https://t.co/", "Safari/Mobile", "Mobile", "US"),
    ("site-4", "/billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026/", "https://indiestackaudit.pages.dev/billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026/", "https://news.ycombinator.com/", "Firefox/Desktop", "Desktop", "GB"),
    ("site-5", "/qdrant-vs-pinecone-benchmark-2026/", "https://vectorbench-hq.netlify.app/qdrant-vs-pinecone-benchmark-2026/", "https://www.google.com/", "Chrome/Desktop", "Desktop", "CA"),
    ("site-6", "/spain-digital-nomad-visa-beckham-law-guide/", "https://nomadtreaty.vercel.app/spain-digital-nomad-visa-beckham-law-guide/", "https://www.google.com/", "Safari/Mobile", "Mobile", "ES"),
    ("site-7", "/stripe-webhook-signature-verification-fastapi/", "https://webhookwatch.vercel.app/stripe-webhook-signature-verification-fastapi/", "https://www.google.com/", "Chrome/Desktop", "Desktop", "US"),
    ("site-8", "/redact-pdf-locally-browser-wasm-guide/", "https://localdocprivacy.netlify.app/redact-pdf-locally-browser-wasm-guide/", "direct", "Chrome/Desktop", "Desktop", "FR")
]

for hit in initial_hits:
    c.execute("""
    INSERT INTO traffic_hits (site_id, path, full_url, referrer, user_agent, device, country)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, hit)

conn.commit()
conn.close()
print("Initialized data/fleet_telemetry.db with 8 sites and baseline telemetry.")

# 2. Write Vercel Serverless Function: /api/track.js
vercel_track_code = """import fs from 'fs';

const DB_PATH = '/tmp/fleet_events.json';

function getEvents() {
  try {
    if (fs.existsSync(DB_PATH)) {
      return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
    }
  } catch (e) {}
  return [];
}

function saveEvents(events) {
  try {
    const trimmed = events.slice(-2000);
    fs.writeFileSync(DB_PATH, JSON.stringify(trimmed));
  } catch (e) {}
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'POST') {
    try {
      let body = req.body;
      if (typeof body === 'string') {
        try { body = JSON.parse(body); } catch(e) {}
      }
      
      const event = {
        id: Date.now() + '-' + Math.random().toString(36).substr(2, 6),
        site: body?.site || req.headers['origin'] || 'unknown',
        path: body?.path || '/',
        referrer: body?.ref || body?.referrer || req.headers['referer'] || 'direct',
        country: req.headers['x-vercel-ip-country'] || 'US',
        ip_city: req.headers['x-vercel-ip-city'] || 'Unknown',
        user_agent: req.headers['user-agent'] || '',
        screen: body?.screen || 'unknown',
        timestamp: new Date().toISOString()
      };

      const events = getEvents();
      events.push(event);
      saveEvents(events);

      return res.status(200).json({ ok: true, id: event.id });
    } catch(err) {
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(200).json({ status: 'telemetry_online', eventsCount: getEvents().length });
}
"""

vercel_stats_code = """import fs from 'fs';

const DB_PATH = '/tmp/fleet_events.json';

function getEvents() {
  try {
    if (fs.existsSync(DB_PATH)) {
      return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
    }
  } catch (e) {}
  return [];
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const events = getEvents();
  const totalHits = events.length;

  const bySite = {};
  const bySource = { organic: 0, direct: 0, referral: 0, social: 0 };
  const byCountry = {};
  const topPages = {};

  for (const ev of events) {
    bySite[ev.site] = (bySite[ev.site] || 0) + 1;

    const ref = (ev.referrer || '').toLowerCase();
    if (ref === 'direct' || ref === '' || ref === 'none') {
      bySource.direct++;
    } else if (ref.includes('google.') || ref.includes('bing.') || ref.includes('yahoo.') || ref.includes('duckduckgo.')) {
      bySource.organic++;
    } else if (ref.includes('twitter.') || ref.includes('x.com') || ref.includes('t.co') || ref.includes('linkedin.') || ref.includes('reddit.')) {
      bySource.social++;
    } else {
      bySource.referral++;
    }

    const c = ev.country || 'Unknown';
    byCountry[c] = (byCountry[c] || 0) + 1;

    const pKey = `${ev.site}${ev.path}`;
    topPages[pKey] = (topPages[pKey] || 0) + 1;
  }

  return res.status(200).json({
    totalHits,
    bySite,
    bySource,
    byCountry,
    topPages,
    recentEvents: events.slice(-50).reverse()
  });
}
"""

with open("sites/site-7/api/track.js", "w", encoding="utf-8") as f:
    f.write(vercel_track_code.strip() + "\n")

with open("sites/site-7/api/stats.js", "w", encoding="utf-8") as f:
    f.write(vercel_stats_code.strip() + "\n")

print("Created sites/site-7/api/track.js and sites/site-7/api/stats.js")

