import sys, time, json, os, base64
sys.path.insert(0, r"C:\HermesWork\seo-tools")
import ff as F

ws = F.connect()
ctx = F.get_ctx(ws)
target_url = "https://search.google.com/search-console/performance/search-analytics?resource_id=https%3A%2F%2Fjibranpcccc.github.io%2Fdigitalcreatoravi-seo-engine%2F&hl=en"
print(f"Navigating to GSC performance for LocalAgentStack: {target_url}")
F.cmd(ws, "browsingContext.navigate", {"context": ctx, "url": target_url, "wait": "complete"}, timeout=60)
time.sleep(10)
ctx = F.get_ctx(ws)

title = F.ev(ws, ctx, "document.title")
url = F.ev(ws, ctx, "window.location.href")
print("Title:", title)
print("URL:", url)

# Grab screenshot
r = F.cmd(ws, "browsingContext.captureScreenshot", {"context": ctx})
os.makedirs("reports/gsc_live_check", exist_ok=True)
with open("reports/gsc_live_check/gsc_perf_site1.png", "wb") as f:
    f.write(base64.b64decode(r["result"]["data"]))
print("Saved screenshot to reports/gsc_live_check/gsc_perf_site1.png")

# Extract visible text & stats
body_text = F.ev(ws, ctx, "document.body.innerText")
print("Snippet of GSC page text:")
print(body_text[:1200])

try: F.cmd(ws, "session.end", {}, timeout=5)
except: pass
ws.close()
