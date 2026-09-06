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
