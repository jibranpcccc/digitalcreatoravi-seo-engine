#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import deep_fleet_audit_engine as engine

stubs = [
    'sites/site-5/src/pages/milvus-vs-qdrant-billion-scale-benchmark.astro',
    'sites/site-8/src/pages/client-side-pdf-compression-wasm-guide.astro',
    'sites/site-9/src/pages/lisbon-d8-visa-minimum-income-bootstrappers.astro',
    'sites/site-11/src/pages/greece-digital-nomad-visa-income-requirements.astro',
    'sites/site-12/src/pages/net-revenue-retention-nrr-benchmark-bootstrapped-saas.astro',
    'sites/site-14/src/pages/soc-2-continuous-monitoring-tools-open-source.astro',
    'sites/site-15/src/pages/oyster-vs-deel-pricing-contractor-management-fees.astro',
    'sites/site-16/src/pages/docker-compose-gpu-passthrough-nvidia-container-toolkit.astro',
    'sites/site-18/src/pages/github-actions-concurrency-cancel-in-progress-pattern.astro',
    'sites/site-19/src/pages/delta-neutral-liquidity-provision-uniswap-v3.astro'
]

print(f"{'File':<58} | {'Words':<6} | {'H2s':<4} | {'Tables':<6} | {'Schema':<6}")
print("-" * 88)
for p in stubs:
    full_path = os.path.join(engine.ROOT_DIR, p)
    res = engine.analyze_file(full_path)
    bname = os.path.basename(p)
    print(f"{bname:<58} | {res['word_count']:6d} | {res['h2_count']:4d} | {res['table_count']:6d} | {res['has_schema']}")
