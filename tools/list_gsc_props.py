import sys, time, json, os
sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

ws = F.connect()
ctx = F.get_ctx(ws)
print("Connected. Opening property dropdown...")

# Click search property dropdown
ev_props = F.ev(ws, ctx, """(() => {
    const btn = document.querySelector('[aria-label="Search property"], [aria-label*="property"]');
    if (btn) btn.click();
    return !!btn;
})()""")
time.sleep(3)

# Read dropdown list items
props = F.ev(ws, ctx, """(() => {
    const items = Array.from(document.querySelectorAll('[role="option"], [role="menuitem"], .b3-list-item, div[data-property-url]'));
    return items.map(e => (e.innerText || e.textContent || '').trim()).filter(Boolean);
})()""")

print("Visible properties in GSC dropdown:")
print(json.dumps(props, indent=2))

try: F.cmd(ws, "session.end", {}, timeout=5)
except: pass
ws.close()
