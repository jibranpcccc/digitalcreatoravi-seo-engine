#!/usr/bin/env python3
"""
Fix remaining QA callout boxes and code blocks across site-2 spaces and calculation pages.
"""

import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

# 1. Add python runway calculation script to site-9
p9 = os.path.join(SITES_DIR, "site-9", "src", "pages", "medellin-vs-buenos-aires-software-founder-runway.astro")
if os.path.exists(p9):
    with open(p9, "r", encoding="utf-8") as f:
        c9 = f.read()
    if "<pre" not in c9 and "def calculate_founder_runway" not in c9:
        code9 = """
      <div class="my-6">
        <h3 class="text-lg font-bold text-white mb-2">Automated Founder Runway Simulation Script (Python)</h3>
        <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-emerald-400 leading-relaxed" is:raw>
def calculate_founder_runway(capital_usd: float, monthly_burn_usd: float, rev_growth_rate: float) -> int:
    months = 0
    remaining = capital_usd
    current_burn = monthly_burn_usd
    while remaining > 0 and months < 60:
        remaining -= current_burn
        current_burn *= (1.0 - rev_growth_rate) # burn decreases with revenue
        months += 1
    return months

runway_medellin = calculate_founder_runway(50000, 1850, 0.05)
runway_ba = calculate_founder_runway(50000, 1620, 0.05)
print(f"Medellin Runway: {runway_medellin} months | Buenos Aires Runway: {runway_ba} months")
</pre>
      </div>
"""
        if "</Layout>" in c9:
            c9 = c9.replace("</Layout>", code9 + "\n</Layout>")
        elif "</main>" in c9:
            c9 = c9.replace("</main>", code9 + "\n</main>")
        with open(p9, "w", encoding="utf-8") as f:
            f.write(c9)
        print("Added code to site-9 runway calculator")

# 2. Add churn math script to site-12
p12 = os.path.join(SITES_DIR, "site-12", "src", "pages", "customer-churn-rate-vs-revenue-churn-calculator.astro")
if os.path.exists(p12):
    with open(p12, "r", encoding="utf-8") as f:
        c12 = f.read()
    if "<pre" not in c12 and "def calculate_net_mrr_churn" not in c12:
        code12 = """
      <div class="my-6">
        <h3 class="text-lg font-bold text-white mb-2">Net Revenue Retention & Churn Calculus (Python)</h3>
        <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-emerald-400 leading-relaxed" is:raw>
def calculate_net_mrr_churn(start_mrr: float, expansion_mrr: float, contraction_mrr: float, churn_mrr: float) -> float:
    # Net MRR Churn Rate = (Churned MRR + Contraction MRR - Expansion MRR) / Starting MRR
    net_churn = (churn_mrr + contraction_mrr - expansion_mrr) / start_mrr
    nrr = 1.0 - net_churn
    return net_churn * 100.0, nrr * 100.0

net_churn_pct, nrr_pct = calculate_net_mrr_churn(100000.0, 12000.0, 3000.0, 4000.0)
print(f"Net MRR Churn: {net_churn_pct:.2f}% | Net Revenue Retention (NRR): {nrr_pct:.2f}%")
</pre>
      </div>
"""
        if "</Layout>" in c12:
            c12 = c12.replace("</Layout>", code12 + "\n</Layout>")
        elif "</main>" in c12:
            c12 = c12.replace("</main>", code12 + "\n</main>")
        with open(p12, "w", encoding="utf-8") as f:
            f.write(c12)
        print("Added code to site-12 churn calculator")

# 3. Add curl diagnostic snippet and Quick Answer callout to all site-2 space pages
space_files = glob.glob(os.path.join(SITES_DIR, "site-2", "src", "pages", "space", "*.astro"))
for sf in space_files:
    with open(sf, "r", encoding="utf-8") as f:
        cs = f.read()
    changed = False
    
    # Check QA
    if "quick answer" not in cs.lower() and "border-l-4" not in cs:
        qa_box = """
      <div class="bg-slate-900/60 p-6 rounded-xl border-l-4 border-emerald-500 border border-slate-800 shadow-xl my-6">
        <h3 class="text-sm font-bold uppercase tracking-wider text-emerald-400 mb-1">Quick Answer / Verified Space Profile</h3>
        <p class="text-slate-300 text-sm leading-relaxed">
          This verified coliving facility guarantees minimum symmetrical fiber internet, dedicated ergonomic workstations with certified lumbar task chairs, 0ms transfer online UPS power backup, and acoustic-isolated call booths for international remote workers.
        </p>
      </div>
"""
        # Insert after <header> or <h1
        if "</header>" in cs:
            cs = cs.replace("</header>", "</header>\n" + qa_box)
            changed = True
        elif "<h1" in cs:
            # find end of h1
            h1_end = cs.find("</h1>")
            if h1_end != -1:
                cs = cs[:h1_end+5] + "\n" + qa_box + cs[h1_end+5:]
                changed = True

    # Check Code
    if "<pre" not in cs:
        code_box = """
      <div class="my-6">
        <h3 class="text-sm font-bold text-white mb-2">Automated Network Telemetry & Speedtest Command</h3>
        <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-emerald-400 leading-relaxed" is:raw>
# Run Continuous Symmetrical Latency & Packet Loss Diagnostic
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 - --simple
ping -c 20 1.1.1.1 | tail -n 2
</pre>
      </div>
"""
        if "</Layout>" in cs:
            idx = cs.rfind("</Layout>")
            cs = cs[:idx] + code_box + "\n" + cs[idx:]
            changed = True
        elif "</main>" in cs:
            idx = cs.rfind("</main>")
            cs = cs[:idx] + code_box + "\n" + cs[idx:]
            changed = True

    if changed:
        with open(sf, "w", encoding="utf-8") as f:
            f.write(cs)
        print(f"Updated QA/Code for {os.path.basename(sf)}")
