import sqlite3

conn = sqlite3.connect('data/fleet_telemetry.db')
c = conn.cursor()
p_count = c.execute('SELECT count(*) FROM indexed_pages').fetchone()[0]
q_count = c.execute('SELECT count(*) FROM search_queries').fetchone()[0]
posts_count = c.execute('SELECT count(*) FROM pending_posts').fetchone()[0]
print(f'Indexed Pages in DB: {p_count}')
print(f'Tracked Queries in DB: {q_count}')
print(f'Posts in DB: {posts_count}')

print('\nSample Tracked Queries:')
for r in c.execute('SELECT site_id, query, impressions, clicks, position FROM search_queries LIMIT 10').fetchall():
    print(f'  [{r[0]}] "{r[1]}" - Pos: {r[4]}, Imp: {r[2]}, Clicks: {r[3]}')
