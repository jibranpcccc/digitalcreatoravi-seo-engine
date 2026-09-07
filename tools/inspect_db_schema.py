import sqlite3

conn = sqlite3.connect("data/fleet_telemetry.db")
for row in conn.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
    print(row[0])
    print("-" * 50)
