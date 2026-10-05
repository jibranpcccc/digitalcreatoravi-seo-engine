import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl
import re
import json
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_show_hn():
    url = "https://news.ycombinator.com/showrss"
    items = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            root = ET.fromstring(r.read())
            for el in root.findall(".//item"):
                title = el.find("title").text
                link = el.find("link").text
                # Filter out pure github repos if possible, keep SaaS/tools
                items.append({"title": title, "url": link})
    except Exception as e:
        print(f"Error fetching Show HN: {e}")
    return items

def analyze_prospect(site_url, title):
    try:
        req = urllib.request.Request(site_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
            
            # Find twitter/x handle
            handles = re.findall(r'https?://(?:www\.)?(?:twitter\.com|x\.com)/([a-zA-Z0-9_]{3,20})', html, re.I)
            excluded = {"share", "intent", "search", "home", "privacy", "terms", "about"}
            valid_handles = [h for h in handles if h.lower() not in excluded]
            handle = valid_handles[0] if valid_handles else None
            
            # Check schema
            schema_blocks = re.findall(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', html, re.I | re.DOTALL)
            has_schema = len(schema_blocks) > 0
            
            # Check OG image
            og_image = re.search(r'<meta[^>]+property=[\'"]og:image[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', html, re.I)
            has_og = og_image is not None
            
            return {
                "url": site_url,
                "title": title,
                "handle": handle,
                "has_schema": has_schema,
                "schema_count": len(schema_blocks),
                "has_og": has_og,
                "needs_fix": (not has_schema) or (not has_og)
            }
    except Exception as e:
        return None

def main():
    print("=" * 60)
    print("AUTONOMOUS CLIENT DISCOVERY & TECHNICAL AUDIT ENGINE")
    print("=" * 60)
    print("[*] Ingesting live newly launched SaaS products from Show HN...")
    
    items = fetch_show_hn()
    print(f"[*] Found {len(items)} live submissions. Scanning for SaaS domains...")
    
    qualified = []
    
    for item in items:
        link = item["url"]
        # Skip github or news.ycombinator.com internal links
        if "github.com" in link or "ycombinator.com" in link:
            continue
            
        print(f" -> Probing: {link}")
        audit = analyze_prospect(link, item["title"])
        if audit and audit["needs_fix"] and audit["handle"]:
            qualified.append(audit)
            print(f"    [!] MATCH! Founder Handle: @{audit['handle']} | Schema: {audit['has_schema']} | OG: {audit['has_og']}")
            if len(qualified) >= 5:
                break
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"QUALIFIED CLIENT OUTREACH QUEUE ({len(qualified)} READY)")
    print("=" * 60)
    
    for idx, q in enumerate(qualified):
        clean_name = q['title'].replace("Show HN: ", "").split("–")[0].split("-")[0].strip()
        print(f"\n--- [LEAD #{idx+1}] {clean_name} ({q['url']}) ---")
        print(f"Founder Twitter: https://x.com/{q['handle']} (@{q['handle']})")
        print(f"Technical Defect: {'ZERO Schema.org markup' if not q['has_schema'] else 'Missing OpenGraph social card'}")
        print("\nPre-Written High-Converting DM:")
        print(f"\"Hey @{q['handle']}, saw your Show HN launch for {clean_name}! Really cool product.")
        if not q['has_schema']:
            print(f"Took a quick look at {q['url']} — noticed the site has zero Schema.org structured data (no SoftwareApplication or Offer tags), so Google won't generate Rich Results or pricing snippets for you.")
        else:
            print(f"Took a quick look at {q['url']} — noticed your OpenGraph social card image is missing, so link previews on X and LinkedIn render as empty cards.")
        print("Put together a quick visual diff showing the missing tags. Mind if I share it here?\"")

if __name__ == "__main__":
    main()
