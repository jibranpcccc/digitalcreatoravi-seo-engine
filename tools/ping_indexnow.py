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
        "key_location": "https://jibranpcccc.github.io/8303260f1bf94264ac6d00aa93efde28.txt",
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
        "key_location": "https://jibranpcccc.github.io/8303260f1bf94264ac6d00aa93efde28.txt",
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
    },
    {
        "name": "OpenAgentStack",
        "host": "openagentstack.pages.dev",
        "key_location": "https://openagentstack.pages.dev/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://openagentstack.pages.dev/",
            "https://openagentstack.pages.dev/frameworks/browser-use-vs-playwright-mcp-web-automation-benchmark/",
            "https://openagentstack.pages.dev/agents/langgraph-vs-autogen-multi-agent-orchestration-cost/",
            "https://openagentstack.pages.dev/protocols/building-production-mcp-servers-fastapi-sse/",
            "https://openagentstack.pages.dev/frameworks/smolagents-vs-crewai-lightweight-python-agents/",
            "https://openagentstack.pages.dev/protocols/mcp-authorization-oauth2-bearer-tokens-guide/"
        ]
    },
    {
        "name": "IndieStackAudit",
        "host": "indiestackaudit.pages.dev",
        "key_location": "https://indiestackaudit.pages.dev/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://indiestackaudit.pages.dev/",
            "https://indiestackaudit.pages.dev/stacks/nextjs-vs-astro-for-micro-saas-speed-cost-seo/",
            "https://indiestackaudit.pages.dev/billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026/",
            "https://indiestackaudit.pages.dev/stacks/self-hosted-supabase-vs-managed-neon-postgres-cost-math/",
            "https://indiestackaudit.pages.dev/stacks/zero-cost-saas-stack-cloudflare-pages-turso-resend/",
            "https://indiestackaudit.pages.dev/billing/open-source-auth-comparison-clerk-lucia-better-auth/"
        ]
    },
    {
        "name": "VectorBench",
        "host": "vectorbench-hq.netlify.app",
        "key_location": "https://vectorbench-hq.netlify.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://vectorbench-hq.netlify.app/",
            "https://vectorbench-hq.netlify.app/qdrant-vs-pinecone-benchmark-2026/",
            "https://vectorbench-hq.netlify.app/pgvector-production-tuning-guide/",
            "https://vectorbench-hq.netlify.app/chroma-vs-lancedb-embedded-vector-db/"
        ]
    },
    {
        "name": "NomadTreaty",
        "host": "nomadtreaty.vercel.app",
        "key_location": "https://nomadtreaty.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://nomadtreaty.vercel.app/",
            "https://nomadtreaty.vercel.app/spain-digital-nomad-visa-beckham-law-guide/",
            "https://nomadtreaty.vercel.app/portugal-nhr-tax-nomad-calculator-2026/",
            "https://nomadtreaty.vercel.app/183-day-rule-tax-residency-nomad-guide/"
        ]
    },
    {
        "name": "WebhookWatch",
        "host": "webhookwatch.vercel.app",
        "key_location": "https://webhookwatch.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://webhookwatch.vercel.app/",
            "https://webhookwatch.vercel.app/stripe-webhook-signature-verification-fastapi/",
            "https://webhookwatch.vercel.app/webhook-retry-exponential-backoff-jitter-guide/",
            "https://webhookwatch.vercel.app/webhook-dead-letter-queue-architecture-sqs/"
        ]
    },
    {
        "name": "LocalDocPrivacy",
        "host": "localdocprivacy.netlify.app",
        "key_location": "https://localdocprivacy.netlify.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://localdocprivacy.netlify.app/",
            "https://localdocprivacy.netlify.app/redact-pdf-locally-browser-wasm-guide/",
            "https://localdocprivacy.netlify.app/convert-pdf-to-markdown-offline-guide/",
            "https://localdocprivacy.netlify.app/client-side-vs-cloud-pdf-privacy-audit/"
        ]
    },
    {
        "name": "FounderRunway",
        "host": "site-9-inky.vercel.app",
        "key_location": "https://site-9-inky.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-9-inky.vercel.app/",
            "https://site-9-inky.vercel.app/chiang-mai-vs-bali-runway-calculator/",
            "https://site-9-inky.vercel.app/lisbon-nhr-tax-runway-founder-guide/",
            "https://site-9-inky.vercel.app/top-latin-america-tech-hubs-for-bootstrappers/"
        ]
    },
    {
        "name": "RAGInspect",
        "host": "raginspect.pages.dev",
        "key_location": "https://raginspect.pages.dev/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://raginspect.pages.dev/",
            "https://raginspect.pages.dev/semantic-chunking-vs-fixed-size-rag-benchmarks/",
            "https://raginspect.pages.dev/hybrid-search-bm25-vs-dense-vector-accuracy/",
            "https://raginspect.pages.dev/ragas-vs-trulens-rag-evaluation-frameworks/"
        ]
    },
    {
        "name": "NomadPassportIndex",
        "host": "nomadpassportindex.netlify.app",
        "key_location": "https://nomadpassportindex.netlify.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://nomadpassportindex.netlify.app/",
            "https://nomadpassportindex.netlify.app/spain-digital-nomad-visa-income-requirements/",
            "https://nomadpassportindex.netlify.app/japan-digital-nomad-visa-guide-tax-exemption/",
            "https://nomadpassportindex.netlify.app/easiest-digital-nomad-visas-in-europe-2026/"
        ]
    },
    {
        "name": "SaaSUnitMath",
        "host": "site-12-taupe.vercel.app",
        "key_location": "https://site-12-taupe.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-12-taupe.vercel.app/",
            "https://site-12-taupe.vercel.app/saas-ltv-cac-payback-period-calculator/",
            "https://site-12-taupe.vercel.app/b2b-saas-churn-benchmarks-by-acv-2026/",
            "https://site-12-taupe.vercel.app/rule-of-40-saas-valuation-growth-model/"
        ]
    },
    {
        "name": "GrokLogTester",
        "host": "groklogtester.pages.dev",
        "key_location": "https://groklogtester.pages.dev/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://groklogtester.pages.dev/",
            "https://groklogtester.pages.dev/nginx-access-log-grok-pattern-generator/",
            "https://groklogtester.pages.dev/aws-alb-access-log-regex-parser/",
            "https://groklogtester.pages.dev/high-throughput-log-parsing-vector-vs-fluentbit/"
        ]
    },
    {
        "name": "SOC2Ready",
        "host": "site-14-sable.vercel.app",
        "key_location": "https://site-14-sable.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-14-sable.vercel.app/",
            "https://site-14-sable.vercel.app/soc-2-type-1-vs-type-2-compliance-timeline-cost/",
            "https://site-14-sable.vercel.app/vanta-vs-drata-vs-secureframe-compliance-automation-review/",
            "https://site-14-sable.vercel.app/soc-2-compliance-for-bootstrapped-startups-under-20k/"
        ]
    },
    {
        "name": "EORCalculator",
        "host": "site-15-ruby.vercel.app",
        "key_location": "https://site-15-ruby.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-15-ruby.vercel.app/",
            "https://site-15-ruby.vercel.app/deel-vs-remote-com-pricing-hidden-fees-breakdown/",
            "https://site-15-ruby.vercel.app/contractor-vs-eor-legal-misclassification-risk-matrix/",
            "https://site-15-ruby.vercel.app/hiring-remote-engineers-in-latin-america-vs-eastern-europe-eor-cost/"
        ]
    },
    {
        "name": "DevConfigHub",
        "host": "site-16-indol.vercel.app",
        "key_location": "https://site-16-indol.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-16-indol.vercel.app/",
            "https://site-16-indol.vercel.app/devcontainer-json-vs-docker-compose-local-development/",
            "https://site-16-indol.vercel.app/nix-flakes-for-reproducible-python-rust-node-environments/",
            "https://site-16-indol.vercel.app/fastest-docker-compose-postgres-redis-local-stack/"
        ]
    },
    {
        "name": "OpenCRMStack",
        "host": "opencrmstack.pages.dev",
        "key_location": "https://opencrmstack.pages.dev/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://opencrmstack.pages.dev/",
            "https://opencrmstack.pages.dev/twenty-crm-vs-hubspot-open-source-sales-pipeline-audit/",
            "https://opencrmstack.pages.dev/self-hosted-erpnext-vs-salesforce-cost-migration-breakdown/",
            "https://opencrmstack.pages.dev/mautic-vs-hubspot-email-automation-deliverability-benchmark/"
        ]
    },
    {
        "name": "CIPipelineGraph",
        "host": "site-18-chi.vercel.app",
        "key_location": "https://site-18-chi.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-18-chi.vercel.app/",
            "https://site-18-chi.vercel.app/github-actions-vs-gitlab-ci-syntax-execution-cost-comparison/",
            "https://site-18-chi.vercel.app/matrix-build-optimization-github-actions-cache-speed/",
            "https://site-18-chi.vercel.app/act-run-github-actions-locally-debugging-guide/"
        ]
    },
    {
        "name": "GreekVisualizer",
        "host": "site-19-nine.vercel.app",
        "key_location": "https://site-19-nine.vercel.app/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://site-19-nine.vercel.app/",
            "https://site-19-nine.vercel.app/uniswap-v3-concentrated-liquidity-impermanent-loss-calculator/",
            "https://site-19-nine.vercel.app/options-gamma-scalping-theta-decay-hedging-strategies/",
            "https://site-19-nine.vercel.app/crypto-funding-rate-arbitrage-delta-neutral-yield-guide/"
        ]
    },
    {
        "name": "EdgeRuntimeHQ",
        "host": "edgeruntimehq.pages.dev",
        "key_location": "https://edgeruntimehq.pages.dev/8303260f1bf94264ac6d00aa93efde28.txt",
        "urls": [
            "https://edgeruntimehq.pages.dev/",
            "https://edgeruntimehq.pages.dev/webgpu-vs-wasm-in-browser-llm-inference-benchmarks/",
            "https://edgeruntimehq.pages.dev/onnx-runtime-vs-tensorrt-edge-server-latency/",
            "https://edgeruntimehq.pages.dev/running-whisper-speech-to-text-locally-in-browser-webgpu/"
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
