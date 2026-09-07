#!/usr/bin/env python3
"""
Tags all 20 standalone repositories with high-intent technical topics.
Makes repositories discoverable on GitHub Explore and Topic pages (DA 96).
"""

import subprocess
import time

TOPICS = [
    ("local-agent-hardware-stack", "llm,deepseek-r1,vram-calculator,local-ai,ai-engineering"),
    ("workation-coliving-radar", "digital-nomad,coliving,remote-work,wifi-speed,coworking"),
    ("open-agent-protocol-hub", "model-context-protocol,mcp,autonomous-agents,fastmcp,llm-agents"),
    ("indie-saas-stack-audit", "micro-saas,indie-hacker,serverless,web-performance,cloud-costs"),
    ("vector-database-benchmarks", "vector-database,qdrant,pinecone,pgvector,rag-benchmark"),
    ("nomad-tax-treaty-calculator", "tax-treaty,digital-nomad,183-day-rule,geo-arbitrage,expat-taxes"),
    ("webhook-signature-audit", "webhook,hmac-sha256,security,developer-tools,api-integration"),
    ("local-pdf-privacy-redactor", "wasm,pdf-redactor,privacy-first,client-side,local-first"),
    ("founder-runway-calculator", "founder-runway,burn-rate,bootstrapped,geo-arbitrage,startup-calculator"),
    ("rag-semantic-chunking-bench", "rag,semantic-chunking,mteb,embeddings,vector-search"),
    ("nomad-passport-visa-index", "digital-nomad-visa,visa-index,remote-work,residency-tracker,consular"),
    ("saas-unit-economics-calculator", "saas-metrics,ltv-cac,churn-rate,rule-of-40,unit-economics"),
    ("nginx-grok-log-tester", "nginx,grok-patterns,log-parser,regex-tester,observability"),
    ("soc2-readiness-checklist", "soc2,compliance,security-controls,type-2,audit-readiness"),
    ("global-eor-payroll-calculator", "eor-calculator,employer-of-record,global-payroll,remote-hiring,fx-spread"),
    ("devcontainer-docker-generator", "devcontainer,docker-compose,nix-flakes,developer-environment,reproducible-builds"),
    ("open-crm-migration-tco", "open-source-crm,twenty-crm,erpnext,salesforce-alternative,crm-migration"),
    ("github-actions-dag-validator", "github-actions,ci-cd,workflow-lint,dag-graph,pipeline-visualizer"),
    ("options-greeks-visualizer", "options-greeks,black-scholes,impermanent-loss,uniswap-v3,quantitative-finance"),
    ("webgpu-edge-inference-bench", "webgpu,onnx-runtime-web,edge-ai,in-browser-inference,llm-benchmarks")
]

def main():
    print("=== TAGGING ALL 20 GITHUB REPOSITORIES WITH TECHNICAL TOPICS ===")
    for repo, topics in TOPICS:
        cmd = ["gh", "repo", "edit", f"jibranpcccc/{repo}", "--add-topic", topics]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[+] {repo}: Tagged with {topics}")
        else:
            print(f"[-] {repo} error: {res.stderr}")
        time.sleep(0.3)
    print("\nALL 20 REPOSITORIES SUCCESSFULLY TAGGED.")

if __name__ == "__main__":
    main()
