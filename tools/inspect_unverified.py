#!/usr/bin/env python3
import csv
import os

csv_file = os.path.join(os.path.dirname(__file__), "..", "reports", "MASTER_LIVE_BACKLINKS_REPORT.csv")
with open(csv_file, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

unverified = [r for r in rows if r['Live Verified'] != 'YES']
print(f"Total unverified: {len(unverified)}")
for r in unverified:
    print(f"[{r['Site ID']}] {r['Platform Tier']} -> {r['Live Backlink URL']} ({r['HTTP Status']})")
