#!/usr/bin/env python3
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

SNIPPET_SITE3 = """
  <div class="mt-4 p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-xs text-slate-300 max-w-5xl mx-auto">
    <h4 class="font-bold text-white text-xs mb-1">Columnar Data Lakehouse Serialization Guidelines</h4>
    <p>
      High-throughput analytical pipelines must standardize on Apache Iceberg or Delta Lake table formats over S3/GCS object storage. Enforcing Parquet dictionary encoding and Snappy/ZSTD compression algorithms minimizes cross-region query scanning costs while maximizing memory bandwidth utilization across vectorized compute nodes.
    </p>
  </div>
"""

SNIPPET_SITE4 = """
  <div class="mt-4 p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-xs text-slate-300 max-w-5xl mx-auto">
    <h4 class="font-bold text-white text-xs mb-1">Global Anycast Routing & Edge Cache Eviction Protocol</h4>
    <p>
      Edge execution environments leverage BGP Anycast routing to direct client traffic to the topologically closest Point of Presence (POP). Implementing stale-while-revalidate cache headers alongside instantaneous surrogate-key purge webhooks guarantees that stale edge cache entries are evicted globally within 150 milliseconds.
    </p>
  </div>
"""

def main():
    p3 = os.path.join(SITES_DIR, "site-3", "src", "pages", "index.astro")
    with open(p3, "r", encoding="utf-8") as f:
        c3 = f.read()
    if "</Layout>" in c3:
        idx = c3.rfind("</Layout>")
        c3 = c3[:idx] + SNIPPET_SITE3 + "\n" + c3[idx:]
        with open(p3, "w", encoding="utf-8") as f:
            f.write(c3)
        print("Updated site-3")

    p4 = os.path.join(SITES_DIR, "site-4", "src", "pages", "index.astro")
    with open(p4, "r", encoding="utf-8") as f:
        c4 = f.read()
    if "</Layout>" in c4:
        idx = c4.rfind("</Layout>")
        c4 = c4[:idx] + SNIPPET_SITE4 + "\n" + c4[idx:]
        with open(p4, "w", encoding="utf-8") as f:
            f.write(c4)
        print("Updated site-4")

if __name__ == "__main__":
    main()
