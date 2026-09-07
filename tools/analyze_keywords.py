import sqlite3

conn = sqlite3.connect("data/fleet_telemetry.db")
c = conn.cursor()

print("=== CURRENT TARGET KEYWORDS IN PENDING POSTS (BY SITE) ===")
c.execute("SELECT site_id, site_name, target_keyword, search_volume, keyword_difficulty, scheduled_date FROM pending_posts ORDER BY site_id, scheduled_date")
rows = c.fetchall()
for r in rows:
    print(f"[{r[0]}] {r[1]:18} | KW: {r[2]:45} | Vol: {r[3]:5} | KD: {r[4]:2} | Date: {r[5]}")

print(f"\nTotal Pending Posts: {len(rows)}")

print("\n=== CURRENT SEARCH QUERIES (BY SITE) ===")
c.execute("SELECT site_id, query, impressions, position FROM search_queries ORDER BY site_id")
qrows = c.fetchall()
for q in qrows:
    print(f"[{q[0]}] Query: {q[1]:45} | Impr: {q[2]:4} | Pos: {q[3]}")
print(f"\nTotal Tracked Queries: {len(qrows)}")
