import urllib.request
import urllib.parse
import ssl
import re
import json
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def inspect_site(url):
    print("=" * 60)
    print(f"DEEP TECHNICAL DIAGNOSTIC: {url}")
    print("=" * 60)
    
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            ttfb = int((time.time() - t0) * 1000)
            status = r.status
            html = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[!] Critical Connection Error: {e}")
        return

    print(f"[*] Response: HTTP {status} (TTFB: {ttfb}ms)")
    
    # 1. Social Tags
    og_title = re.search(r'<meta[^>]+property=[\'"]og:title[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', html, re.I)
    og_desc = re.search(r'<meta[^>]+property=[\'"]og:description[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', html, re.I)
    og_img = re.search(r'<meta[^>]+property=[\'"]og:image[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', html, re.I)
    tw_card = re.search(r'<meta[^>]+name=[\'"]twitter:card[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', html, re.I)
    
    print("\n--- SOCIAL SHARE PREVIEW DIAGNOSTIC ---")
    print(f"  OG Title: {og_title.group(1) if og_title else 'MISSING'}")
    print(f"  OG Description: {og_desc.group(1)[:80] + '...' if og_desc else 'MISSING'}")
    print(f"  OG Image: {og_img.group(1) if og_img else 'MISSING'}")
    print(f"  Twitter Card: {tw_card.group(1) if tw_card else 'MISSING'}")

    # 2. Schema JSON-LD
    schema_blocks = re.findall(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', html, re.I | re.DOTALL)
    print(f"\n--- SCHEMA.ORG STRUCTURED DATA DIAGNOSTIC ({len(schema_blocks)} blocks) ---")
    if not schema_blocks:
        print("  [!] ZERO Schema blocks detected. Site has zero structured data for Google Rich Results.")
    for idx, b in enumerate(schema_blocks):
        try:
            d = json.loads(b.strip())
            print(f"  Block #{idx+1} JSON Valid: True | @type: {d.get('@type', 'No @type attribute')}")
            print(f"    Raw preview: {json.dumps(d)[:180]}...")
        except Exception as e:
            print(f"  Block #{idx+1} JSON SYNTAX ERROR: {e}")

    # 3. Canonical & Viewport
    canonical = re.search(r'<link[^>]+rel=[\'"]canonical[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I)
    print(f"\n--- CRAWLABILITY & INDEXING ---")
    print(f"  Canonical URL: {canonical.group(1) if canonical else 'MISSING'}")

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://embedful.io"
    inspect_site(url)
