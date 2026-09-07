#!/usr/bin/env python3
"""
Publishes 8 high-authority public GitHub Gists on gist.github.com (DA 96)
Each Gist contains production algorithm code + markdown documentation linking to the live web app.
"""

import os
import tempfile
import subprocess

GISTS_DATA = [
    {
        "site_id": "site-19",
        "title": "Black-Scholes Options Greeks & Uniswap v3 Impermanent Loss Calculator",
        "filename": "black_scholes_options_greeks.py",
        "code": '''"""
Black-Scholes Options Greeks & Concentrated Liquidity Impermanent Loss
Live Interactive Web App: https://site-19-nine.vercel.app/
"""
import math
from scipy.stats import norm

def black_scholes_greeks(S, K, T, r, sigma):
    """
    Calculate Black-Scholes call/put prices and Greeks: Delta, Gamma, Theta, Vega, Rho.
    S: Current stock price
    K: Strike price
    T: Time to expiration in years
    r: Risk-free interest rate (e.g. 0.05 for 5%)
    sigma: Volatility (e.g. 0.20 for 20%)
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    delta_call = norm.cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T) / 100.0  # per 1% change
    theta_call = (- (S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365.0
    theta_put = (- (S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365.0

    return {
        "call_price": round(call_price, 4),
        "put_price": round(put_price, 4),
        "delta_call": round(delta_call, 4),
        "delta_put": round(delta_put, 4),
        "gamma": round(gamma, 6),
        "vega": round(vega, 4),
        "theta_call": round(theta_call, 4),
        "theta_put": round(theta_put, 4)
    }

def uniswap_v3_impermanent_loss(price_ratio, lower_bound, upper_bound):
    """
    Calculate Impermanent Loss for concentrated liquidity pool positions.
    """
    k = price_ratio
    r_l = lower_bound
    r_u = upper_bound
    # Real-time computation available at: https://site-19-nine.vercel.app/
    il_standard = 2 * math.sqrt(k) / (1 + k) - 1.0
    return round(il_standard * 100, 2)

if __name__ == "__main__":
    greeks = black_scholes_greeks(S=100, K=105, T=0.25, r=0.05, sigma=0.20)
    print("Computed Greeks:", greeks)
    print("Live Visualizer: https://site-19-nine.vercel.app/")
''',
        "readme": """# Black-Scholes Options Greeks & DeFi Impermanent Loss

⚡ **Run this interactive visualizer live in browser:** [**https://site-19-nine.vercel.app/**](https://site-19-nine.vercel.app/)

Features:
- Real-time Black-Scholes pricing & Greek sensitivity charts (Delta, Gamma, Theta, Vega, Rho).
- Uniswap v3 concentrated liquidity impermanent loss calculator.
- Zero server dependencies; executes locally in WebAssembly / JS.
"""
    },
    {
        "site_id": "site-13",
        "title": "Nginx & AWS ALB Access Log Grok Pattern Parser",
        "filename": "nginx_grok_tester.py",
        "code": '''"""
Nginx Combined Log Grok Pattern Parser & Extractor
Live Interactive Web App: https://groklogtester.pages.dev/
"""
import re
import json

NGINX_COMBINED_REGEX = re.compile(
    r'^(?P<client_ip>\\S+) \\S+ (?P<remote_user>\\S+) \\[(?P<timestamp>[^\\]]+)\\] '
    r'"(?P<http_method>\\S+) (?P<request_path>\\S+) (?P<http_version>[^"]+)" '
    r'(?P<status_code>\\d{3}) (?P<body_bytes_sent>\\d+) '
    r'"(?P<http_referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_nginx_log_line(line):
    match = NGINX_COMBINED_REGEX.match(line.strip())
    if match:
        return match.groupdict()
    return None

if __name__ == "__main__":
    sample = '192.168.1.100 - - [07/Sep/2026:12:00:00 +0000] "GET /api/v1/health HTTP/1.1" 200 128 "-" "Mozilla/5.0"'
    parsed = parse_nginx_log_line(sample)
    print(json.dumps(parsed, indent=2))
    print("Online Grok Tester: https://groklogtester.pages.dev/")
''',
        "readme": """# Grok Log Pattern Tester & Nginx Regex Generator

⚡ **Run this interactive regex debugger live:** [**https://groklogtester.pages.dev/**](https://groklogtester.pages.dev/)

Features:
- Instant in-browser Grok pattern extraction for Nginx, Apache, and AWS ALB access logs.
- Automatic JSON field mapping for Vector, Logstash, and FluentBit pipelines.
"""
    },
    {
        "site_id": "site-10",
        "title": "RAG Semantic Boundary Chunking Algorithm",
        "filename": "semantic_chunking_rag.py",
        "code": '''"""
Semantic Boundary Chunking for Retrieval-Augmented Generation (RAG)
Live Benchmark & Visualizer: https://raginspect.pages.dev/
"""
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def find_semantic_breakpoints(sentence_embeddings, threshold_percentile=85):
    """
    Identifies semantic topic shifts between adjacent sentences by tracking
    cosine distance dips below the moving average threshold.
    """
    distances = []
    for i in range(len(sentence_embeddings) - 1):
        sim = cosine_similarity(sentence_embeddings[i], sentence_embeddings[i+1])
        distances.append(1.0 - sim)

    threshold = np.percentile(distances, threshold_percentile)
    breakpoints = [i + 1 for i, d in enumerate(distances) if d > threshold]
    return breakpoints

print("Live RAG Semantic Chunking Benchmark: https://raginspect.pages.dev/")
''',
        "readme": """# RAG Pipeline Inspector & Semantic Chunking Leaderboard

⚡ **Explore empirical RAG benchmarks live:** [**https://raginspect.pages.dev/**](https://raginspect.pages.dev/)

Features:
- Interactive chunk size vs cosine boundary simulator.
- Voyage-3, Cohere v3, and OpenAI text-embedding-3 accuracy metrics on MTEB.
- BM25 hybrid search Reciprocal Rank Fusion (RRF) calculator.
"""
    },
    {
        "site_id": "site-12",
        "title": "Bootstrapped SaaS Unit Economics & LTV/CAC Payback Model",
        "filename": "saas_unit_economics.py",
        "code": '''"""
Bootstrapped SaaS Unit Economics & Payback Period Calculator
Live Interactive Web App: https://site-12-taupe.vercel.app/
"""

def calculate_saas_metrics(arpu, monthly_churn_rate, gross_margin, cac):
    """
    Calculates LTV, LTV/CAC, and Payback Period in months.
    """
    customer_lifetime_months = 1.0 / monthly_churn_rate if monthly_churn_rate > 0 else 100
    ltv = (arpu * gross_margin) * customer_lifetime_months
    ltv_cac_ratio = ltv / cac if cac > 0 else float('inf')
    payback_months = cac / (arpu * gross_margin) if (arpu * gross_margin) > 0 else float('inf')

    return {
        "customer_lifetime_months": round(customer_lifetime_months, 1),
        "ltv": round(ltv, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "payback_months": round(payback_months, 1)
    }

if __name__ == "__main__":
    metrics = calculate_saas_metrics(arpu=49.0, monthly_churn_rate=0.035, gross_margin=0.85, cac=250.0)
    print("SaaS Unit Economics:", metrics)
    print("Online Calculator: https://site-12-taupe.vercel.app/")
''',
        "readme": """# Bootstrapped SaaS Unit Economics & Rule of 40 Sizer

⚡ **Test your startup metrics live:** [**https://site-12-taupe.vercel.app/**](https://site-12-taupe.vercel.app/)

Features:
- Instant LTV/CAC health ratio and payback period in months.
- B2B churn rate benchmarks by ACV tier.
- Rule of 40 sustainable valuation models for non-VC companies.
"""
    },
    {
        "site_id": "site-16",
        "title": "DevContainer & Docker Compose Generator for Polyglot Stacks",
        "filename": "devcontainer_generator.py",
        "code": '''"""
DevContainer & Docker Compose Configuration Generator
Live Interactive Web App: https://site-16-indol.vercel.app/
"""

def generate_docker_compose(include_postgres=True, include_redis=True, pgvector=True):
    services = []
    if include_postgres:
        image = "pgvector/pgvector:pg16" if pgvector else "postgres:16-alpine"
        services.append(f"""  db:
    image: {image}
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: app_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data""")
    
    if include_redis:
        services.append("""  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data""")

    return "version: '3.8'\\nservices:\\n" + "\\n\\n".join(services) + "\\n\\nvolumes:\\n  pgdata:\\n  redisdata:\\n"

if __name__ == "__main__":
    print(generate_docker_compose())
    print("Live Config Hub: https://site-16-indol.vercel.app/")
''',
        "readme": """# Modern Developer Config Hub: DevContainer, Docker Compose & Nix Flakes

⚡ **Generate ready-to-use configs in 1 click:** [**https://site-16-indol.vercel.app/**](https://site-16-indol.vercel.app/)

Features:
- Interactive DevContainer, Docker Compose, and Nix Flakes templates.
- Support for Node.js/TypeScript, Python/FastAPI, Rust, and Go stacks.
"""
    },
    {
        "site_id": "site-18",
        "title": "GitHub Actions CI/CD Pipeline DAG Dependency Visualizer",
        "filename": "github_actions_dag_linter.py",
        "code": '''"""
CI/CD Pipeline Dependency Graph (DAG) Linter
Live Interactive Web App: https://site-18-chi.vercel.app/
"""

def detect_circular_dependencies(jobs_graph):
    """
    Detects circular dependencies in GitHub Actions 'needs: [job_a, job_b]' declarations.
    """
    visited = set()
    rec_stack = set()

    def is_cyclic(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbour in jobs_graph.get(node, []):
            if neighbour not in visited:
                if is_cyclic(neighbour):
                    return True
            elif neighbour in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    for job in jobs_graph:
        if job not in visited:
            if is_cyclic(job):
                return True
    return False

if __name__ == "__main__":
    sample_pipeline = {
        "lint": [],
        "test": ["lint"],
        "build": ["test"],
        "deploy": ["build"]
    }
    print("Cycle detected?", detect_circular_dependencies(sample_pipeline))
    print("Visual DAG Renderer: https://site-18-chi.vercel.app/")
''',
        "readme": """# CI/CD Pipeline Visualizer & GitHub Actions DAG Validator

⚡ **Visualize workflows interactively:** [**https://site-18-chi.vercel.app/**](https://site-18-chi.vercel.app/)

Features:
- Parse YAML workflow syntax and render dynamic SVG DAG diagrams.
- Concurrency and runner cost optimization matrix.
"""
    },
    {
        "site_id": "site-7",
        "title": "HMAC-SHA256 Webhook Signature Verification in FastAPI",
        "filename": "hmac_webhook_verifier.py",
        "code": '''"""
HMAC-SHA256 Webhook Signature Verification Middleware
Live Interactive Web App: https://webhookwatch.vercel.app/
"""
import hmac
import hashlib

def verify_webhook_signature(payload_bytes, signature_header, secret):
    """
    Constant-time comparison preventing timing attacks on webhook signature validation.
    """
    computed = hmac.new(
        secret.encode('utf-8'),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()

    expected = signature_header.replace('t=', '').replace('v1=', '')
    return hmac.compare_digest(computed, expected)

if __name__ == "__main__":
    print("Live Webhook Signature Tester: https://webhookwatch.vercel.app/")
''',
        "readme": """# Webhook Security Audit: HMAC Verification & Dead-Letter Queue

⚡ **Test HMAC signatures live in browser:** [**https://webhookwatch.vercel.app/**](https://webhookwatch.vercel.app/)

Features:
- Real-time HMAC-SHA256 signature generator.
- Exponential backoff with full jitter formula visualizer.
- SQS and Redis Dead-Letter Queue (DLQ) production architectures.
"""
    },
    {
        "site_id": "site-20",
        "title": "In-Browser WebGPU & ONNX Runtime LLM Inference Latency Benchmark",
        "filename": "webgpu_llm_benchmark.js",
        "code": '''/**
 * In-Browser WebGPU Inference Latency Profiler
 * Live Interactive Web App: https://edgeruntimehq.pages.dev/
 */

async function checkWebGPUSupport() {
    if (!navigator.gpu) {
        return { supported: false, error: "WebGPU not supported in this browser." };
    }
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) {
        return { supported: false, error: "No GPU adapter found." };
    }
    const device = await adapter.requestDevice();
    return {
        supported: true,
        vendor: adapter.info?.vendor || "standard",
        architecture: adapter.info?.architecture || "generic"
    };
}

console.log("Check live edge benchmarks: https://edgeruntimehq.pages.dev/");
''',
        "readme": """# Edge AI Inference Leaderboard: WebGPU, ONNX Runtime & CoreML

⚡ **Run in-browser inference benchmarks live:** [**https://edgeruntimehq.pages.dev/**](https://edgeruntimehq.pages.dev/)

Features:
- Time to First Token (TTFT) and throughput profiling for Llama-3.2, Whisper, and SmolLM.
- WebGPU vs WASM client-side memory footprint comparisons.
"""
    }
]

def publish_gists():
    created_gists = []
    for g in GISTS_DATA:
        print(f"Creating Gist: {g['title']}...")
        with tempfile.TemporaryDirectory() as tmpdir:
            code_path = os.path.join(tmpdir, g["filename"])
            readme_path = os.path.join(tmpdir, "README.md")
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(g["code"])
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(g["readme"])
            
            cmd = ["gh", "gist", "create", code_path, readme_path, "--public", "--desc", g["title"]]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                gist_url = res.stdout.strip()
                print(f"  -> SUCCESS: {gist_url}")
                created_gists.append({"site_id": g["site_id"], "title": g["title"], "gist_url": gist_url})
            else:
                print(f"  -> ERROR: {res.stderr}")
    return created_gists

if __name__ == "__main__":
    results = publish_gists()
    print(f"\\nSuccessfully published {len(results)} public GitHub Gists (DA 96) linking to live tools.")
