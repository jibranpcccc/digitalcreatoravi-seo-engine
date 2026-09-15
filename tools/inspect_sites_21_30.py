#!/usr/bin/env python3
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "data", "fleet_telemetry.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("PRAGMA table_info(sites)")
print("Columns in sites:", [row[1] for row in c.fetchall()])
c.execute("SELECT * FROM sites ORDER BY id")
for row in c.fetchall():
    if int(row[0].replace("site-", "")) >= 21:
        print(row)
