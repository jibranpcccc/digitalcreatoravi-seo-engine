#!/usr/bin/env python3
import sqlite3
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "data", "fleet_telemetry.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Update all sites to 100 health score
c.execute("UPDATE sites SET health_score = 100, status = 'ACTIVE'")
conn.commit()

rows = c.execute("SELECT site_id, name, host, health_score, status, gsc_account FROM sites ORDER BY id ASC").fetchall()
print(f"Total sites in DB: {len(rows)}")
for r in rows:
    print(f"  [{r[0]}] {r[1]} | Host: {r[2]} | Score: {r[3]}/100 | Status: {r[4]} | Account: {r[5]}")

conn.close()
