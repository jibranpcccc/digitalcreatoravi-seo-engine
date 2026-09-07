#!/usr/bin/env python3
"""
Fixes keyword overlaps in data/fleet_telemetry.db:
1. Sharpens Site 11 (NomadPassportIndex) to focus 100% on Income Thresholds & Bank Proof,
   completely separating it from Site 6 (NomadTreaty) which focuses 100% on Taxes & Treaties.
2. Updates Post 31 in pending_posts:
   'greece nomad visa tax break' -> 'greece digital nomad visa income requirements'
   Title: 'Greece Digital Nomad Visa: €3,500 Monthly Income Proof & Bank Requirements'
   Slug: 'greece-digital-nomad-visa-income-requirements'
3. Updates Post 82 in pending_posts:
   'croatia digital nomad visa tax free income limit' -> 'croatia digital nomad visa bank statement requirements'
   Title: 'Croatia Digital Nomad Visa: €2,540 Monthly Salary & Bank Balance Proof'
   Slug: 'croatia-digital-nomad-visa-bank-statement-requirements'
4. Updates Query 23 in search_queries:
   'japan digital nomad visa tax exemption' -> 'japan digital nomad visa 10m yen income proof'
5. Updates Query 63 in search_queries:
   'croatia digital nomad visa tax free income limit' -> 'croatia digital nomad visa bank statement requirements'
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "fleet_telemetry.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Update Post 31 on Site 11
c.execute("""
    UPDATE pending_posts
    SET target_keyword = 'greece digital nomad visa income requirements',
        title = 'Greece Digital Nomad Visa: €3,500 Monthly Income Proof & Bank Requirements',
        slug = 'greece-digital-nomad-visa-income-requirements',
        pillar_silo = 'European Income Thresholds',
        search_volume = 3200,
        keyword_difficulty = 8
    WHERE site_id = 'site-11' AND target_keyword = 'greece nomad visa tax break'
""")
print(f"Updated Post 31: {c.rowcount} rows affected.")

# 2. Update Post 82 on Site 11
c.execute("""
    UPDATE pending_posts
    SET target_keyword = 'croatia digital nomad visa bank statement requirements',
        title = 'Croatia Digital Nomad Visa: €2,540 Monthly Salary & Bank Balance Proof',
        slug = 'croatia-digital-nomad-visa-bank-statement-requirements',
        pillar_silo = 'Balkan Visa Requirements',
        search_volume = 1900,
        keyword_difficulty = 7
    WHERE site_id = 'site-11' AND target_keyword = 'croatia digital nomad visa tax free income limit'
""")
print(f"Updated Post 82: {c.rowcount} rows affected.")

# 3. Update Query 23 on Site 11
c.execute("""
    UPDATE search_queries
    SET query = 'japan digital nomad visa 10m yen income proof'
    WHERE site_id = 'site-11' AND query = 'japan digital nomad visa tax exemption'
""")
print(f"Updated Query 23: {c.rowcount} rows affected.")

# 4. Update Query 63 on Site 11
c.execute("""
    UPDATE search_queries
    SET query = 'croatia digital nomad visa bank statement requirements'
    WHERE site_id = 'site-11' AND query = 'croatia digital nomad visa tax free income limit'
""")
print(f"Updated Query 63: {c.rowcount} rows affected.")

conn.commit()
conn.close()
print("Overlap remediation committed successfully.")
