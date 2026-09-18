import sqlite3

conn = sqlite3.connect('data/fleet_telemetry.db')
c = conn.cursor()

print("--- Site 2 Indexed Pages ---")
for r in c.execute("SELECT url, title FROM indexed_pages WHERE site_id = 'site-2'").fetchall():
    print(r)

print("\n--- Posts 62 to 100 ---")
for r in c.execute("SELECT id, site_id, title, slug, scheduled_date FROM pending_posts WHERE id >= 62 AND id <= 100 ORDER BY id").fetchall():
    print(r)
