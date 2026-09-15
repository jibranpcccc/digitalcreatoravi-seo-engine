import urllib.request

test_urls = [
    ("site-1", "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/hardware/rtx-5090-vs-4090-local-llm-benchmark/"),
    ("site-6", "https://nomadtreaty.vercel.app/spain-digital-nomad-visa-beckham-law-guide/"),
    ("site-7", "https://webhookwatch.vercel.app/stripe-webhook-signature-verification-fastapi/"),
    ("site-9", "https://site-9-inky.vercel.app/chiang-mai-vs-bali-runway-calculator/"),
    ("site-12", "https://site-12-taupe.vercel.app/saas-ltv-cac-payback-period-calculator/"),
    ("site-14", "https://site-14-sable.vercel.app/soc-2-type-1-vs-type-2-compliance-timeline-cost/"),
    ("site-15", "https://site-15-ruby.vercel.app/deel-vs-remote-com-pricing-hidden-fees-breakdown/"),
    ("site-16", "https://site-16-indol.vercel.app/devcontainer-json-vs-docker-compose-local-development/"),
    ("site-18", "https://site-18-chi.vercel.app/github-actions-vs-gitlab-ci-syntax-execution-cost-comparison/"),
    ("site-19", "https://site-19-nine.vercel.app/uniswap-v3-concentrated-liquidity-impermanent-loss-calculator/")
]

for sid, url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            print(f"[+] {sid}: HTTP {r.status} - {url}")
    except Exception as e:
        print(f"[-] {sid}: {e} - {url}")
