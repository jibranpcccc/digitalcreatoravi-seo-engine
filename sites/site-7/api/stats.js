import fs from 'fs';

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
