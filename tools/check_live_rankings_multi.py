import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

TEST_QUERIES = [
    "site:jibranpcccc.github.io",
    "site:openagentstack.pages.dev",
    "site:indiestackaudit.pages.dev",
    "site:raginspect.pages.dev",
    "\"LocalAgentStack\"",
    "\"WorkationRadar\"",
    "\"OpenAgentStack\"",
    "\"IndieStackAudit\"",
    "DeepSeek-R1 32B vs 70B Coding Accuracy",
    "Da Nang Vietnam Remote Worker Living Cost Fiber Speed",
    "Model Context Protocol Stdio vs SSE Latency Benchmark",
    "SQLite vs PostgreSQL Micro-SaaS Under $10k MRR",
    "Syslog RFC 5424 Grok Pattern Validator",
    "HubSpot Marketing Contacts Price Cliff"
]

def check_bing_query(q):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract organic result links
            links = re.findall(r'<li class=\"b_algo\"[^>]*>.*?<h2[^>]*><a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a></h2>', html, flags=re.DOTALL)
            results = []
            for link, title in links:
                clean_t = re.sub(r'<[^>]+>', '', title).strip()
                results.append({"title": clean_t, "url": link})
            
            # Check if any fleet domain or github appears
            fleet_matches = []
            for item in results:
                u = item["url"].lower()
                if "jibranpcccc" in u or "pages.dev" in u or "vercel.app" in u or "netlify.app" in u or "workationradar" in u:
                    fleet_matches.append(item)
                    
            return {
                "query": q,
                "total_organic_found": len(results),
                "fleet_matches": fleet_matches,
                "first_result": results[0] if results else None
            }
    except Exception as e:
        return {"query": q, "error": str(e)}

if __name__ == "__main__":
    print("Running Live Bing SERP Rank Audit...")
    for q in TEST_QUERIES:
        res = check_bing_query(q)
        if "error" in res:
            print(f"[-] {q}: ERROR ({res['error']})")
        elif res["fleet_matches"]:
            print(f"[+] {q}: FOUND {len(res['fleet_matches'])} FLEET RANKINGS!")
            for m in res["fleet_matches"]:
                print(f"     -> {m['title']} | {m['url']}")
        else:
            first = res['first_result']['title'] if res['first_result'] else 'None'
            print(f"[-] {q}: No fleet rankings yet (Top organic: '{first}')")
