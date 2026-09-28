import sqlite3
import urllib.request

conn = sqlite3.connect('data/fleet_telemetry.db')
c = conn.cursor()

rows = c.execute("SELECT id, site_id, url FROM indexed_pages").fetchall()
print(f"Checking all {len(rows)} pages across entire DB for 404s...")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
dead = []
live = []

for rid, sid, u in rows:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            if resp.status == 200:
                live.append((rid, sid, u))
            else:
                dead.append((rid, sid, u, resp.status))
    except Exception as e:
        dead.append((rid, sid, u, str(e)))
        print(f"  [DEAD] {sid}: {u} -> {e}")

print(f"\nAudit complete: {len(live)} live, {len(dead)} dead.")

if dead:
    print(f"Pruning {len(dead)} dead URLs from database indexed_pages...")
    dead_ids = [d[0] for d in dead]
    c.executemany("DELETE FROM indexed_pages WHERE id = ?", [(did,) for did in dead_ids])
    conn.commit()
    print("Database purged of dead URLs.")

conn.close()
