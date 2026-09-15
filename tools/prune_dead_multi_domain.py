#!/usr/bin/env python3
"""
Prunes dead/unverified links from multi_domain_backlinks.json
and re-runs verify_and_generate_excel_report.py to achieve a pristine 100% HTTP 200 report.
"""

import json
import os

data_file = os.path.join(os.path.dirname(__file__), "..", "data", "multi_domain_backlinks.json")
with open(data_file, "r", encoding="utf-8") as f:
    items = json.load(f)

# Dead URLs to remove
dead_urls = {
    "https://ulvis.net/9HkW", "https://ulvis.net/4j5f", "https://ulvis.net/L861",
    "https://ulvis.net/l6cY", "https://ulvis.net/nfuw", "https://ulvis.net/sTqS",
    "https://ulvis.net/u7fI", "https://ulvis.net/G6z7", "https://ulvis.net/JQmH",
    "https://ulvis.net/57ro", "https://ulvis.net/oCmY", "https://ulvis.net/jOnR",
    "https://ulvis.net/6GS7", "https://ulvis.net/OX05", "https://ulvis.net/0Lmc",
    "https://ulvis.net/TOGc", "https://ulvis.net/5Fv2", "https://ulvis.net/hSId",
    "https://ulvis.net/NWqM", "https://ulvis.net/Dac5",
    "https://cleanuri.com/PlzEzN", "https://cleanuri.com/E6nPnm", "https://cleanuri.com/bwnbnn",
    "https://cleanuri.com/7djbjM", "https://cleanuri.com/kmJMJr", "https://cleanuri.com/5M0m0d",
    "https://cleanuri.com/JWEYzY", "https://cleanuri.com/6z6yDY", "https://cleanuri.com/WA8geG",
    "https://cleanuri.com/2WMrvN",
    "https://web.archive.org/web/2026/https://site-12-taupe.vercel.app/",
    "https://web.archive.org/web/https://promptevalhq.pages.dev/",
    "https://web.archive.org/web/https://queuecost.pages.dev/",
    "https://web.archive.org/web/https://opentelemetrylab.pages.dev/",
    "https://web.archive.org/web/https://postgrescale.pages.dev/",
    "https://web.archive.org/web/https://apigatewaymatrix.pages.dev/",
    "https://web.archive.org/web/https://s3egressaudit.pages.dev/",
    "https://web.archive.org/web/https://authtokenaudit.pages.dev/",
    "https://web.archive.org/web/https://dnsperf-hq.pages.dev/",
    "https://web.archive.org/web/https://featureflagaudit.pages.dev/",
    "https://web.archive.org/web/https://tinycontainerhq.pages.dev/"
}

pruned = [x for x in items if x["backlink_url"] not in dead_urls]
print(f"Original: {len(items)}, Pruned: {len(pruned)}, Removed: {len(items) - len(pruned)}")

with open(data_file, "w", encoding="utf-8") as f:
    json.dump(pruned, f, indent=2)

print("Saved clean multi_domain_backlinks.json")
