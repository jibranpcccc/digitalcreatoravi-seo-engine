import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

domains = [
    'jibranpcccc.github.io',
    'openagentstack.pages.dev',
    'indiestackaudit.pages.dev',
    'vectorbench.pages.dev',
    'nomadtreaty.pages.dev',
    'raginspect.pages.dev',
    'edgeruntimehq.pages.dev',
    'nomadpassportindex.netlify.app'
]

print("=== CHECKING BING SEARCH FOR FLEET DOMAINS ===")
for d in domains:
    url = f"https://www.bing.com/search?q={urllib.parse.quote('site:' + d)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            if "There are no results for" in html or "No results found" in html or "class=\"b_no\"" in html:
                status = "0 indexed (No results)"
            else:
                # Check if there are organic search result cards (b_algo)
                results_count = len(re.findall(r'<li class="b_algo"', html))
                status = f"{results_count} pages indexed!" if results_count > 0 else "0 indexed (No b_algo cards)"
            print(f"Bing site:{d:<32} -> {status}")
    except Exception as e:
        print(f"Bing site:{d:<32} -> Error ({e})")
