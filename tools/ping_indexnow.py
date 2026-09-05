"""
IndexNow Instant Submission Engine (Bing, Yandex, Seznam, Naver)
Automatically notifies search engine crawlers whenever pages are published or modified.
Zero-cost, immediate crawl dispatch.
"""
import json
import urllib.request
import sys

INDEXNOW_KEY = "8303260f1bf94264ac6d00aa93efde28"

SITES_CONFIG = [
    {
        "name": "LocalAgentStack",
        "host": "jibranpcccc.github.io",
        "key_location": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/",
            "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/inference/ollama-vs-vllm-benchmark/",
            "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/vram-requirements-calculator-70b/",
            "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/models/deepseek-r1-local-setup-ollama/",
            "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/mac-studio-m4-max-llm-benchmarks/",
            "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/agents/custom-mcp-server-python-tutorial/"
        ]
    },
    {
        "name": "WorkationRadar",
        "host": "jibranpcccc.github.io",
        "key_location": "https://jibranpcccc.github.io/workationradar/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://jibranpcccc.github.io/workationradar/",
            "https://jibranpcccc.github.io/workationradar/space/ponta-do-sol-nomad-coliving/",
            "https://jibranpcccc.github.io/workationradar/space/coworking-bansko-coliving/",
            "https://jibranpcccc.github.io/workationradar/space/dojo-coliving-canggu/",
            "https://jibranpcccc.github.io/workationradar/space/sun-and-co-javea/",
            "https://jibranpcccc.github.io/workationradar/city/Madeira/",
            "https://jibranpcccc.github.io/workationradar/city/Bansko/",
            "https://jibranpcccc.github.io/workationradar/city/Bali/",
            "https://jibranpcccc.github.io/workationradar/city/Lisbon/"
        ]
    }
]

def ping_indexnow(site):
    payload = {
        "host": site["host"],
        "key": INDEXNOW_KEY,
        "keyLocation": site["key_location"],
        "urlList": site["urls"]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"[{site['name']}] IndexNow Ping Response: {response.status} {response.reason}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[{site['name']}] IndexNow HTTP Error: {e.code} {e.reason}")
        return False
    except Exception as e:
        print(f"[{site['name']}] IndexNow Ping Exception: {e}")
        return False

def main():
    print("=== PINGING INDEXNOW API (BING & YANDEX DISPATCH) ===")
    all_ok = True
    for site in SITES_CONFIG:
        ok = ping_indexnow(site)
        if not ok:
            all_ok = False
    print("=== FINISHED INDEXNOW NOTIFICATIONS ===")

if __name__ == "__main__":
    main()
