#!/usr/bin/env python3
import os

p = os.path.join(os.path.dirname(__file__), "..", "sites", "site-3", "src", "pages", "index.astro")
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

add = """
  <div class="mt-4 p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-xs text-slate-300 max-w-5xl mx-auto">
    <h4 class="font-bold text-white text-xs mb-1">Data Cataloging & Granular Access Controls</h4>
    <p>
      Enterprise analytical lakehouses must enforce column-level encryption and role-based access control (RBAC). Implementing automated data lineage tracking ensures regulatory compliance under GDPR and SOC2 while providing auditing visibility into query consumption patterns.
    </p>
  </div>
"""

if "</Layout>" in c:
    idx = c.rfind("</Layout>")
    c = c[:idx] + add + "\n" + c[idx:]
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)
    print("Pushed site-3 over 1500!")
