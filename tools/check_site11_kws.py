import sqlite3

conn = sqlite3.connect("data/fleet_telemetry.db")
c = conn.cursor()

print("--- POSTS WITH GREECE ---")
for r in c.execute("SELECT site_id, target_keyword, title FROM pending_posts WHERE target_keyword LIKE '%greece%'"):
    print(r)

print("--- QUERIES WITH GREECE ---")
for r in c.execute("SELECT site_id, query, page_url FROM search_queries WHERE query LIKE '%greece%'"):
    print(r)

print("--- POSTS IN SITE 11 ---")
for r in c.execute("SELECT id, target_keyword, title FROM pending_posts WHERE site_id = 'site-11'"):
    print(r)

print("--- QUERIES IN SITE 11 ---")
for r in c.execute("SELECT id, query FROM search_queries WHERE site_id = 'site-11'"):
    print(r)
