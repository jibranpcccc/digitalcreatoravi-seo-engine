"""
Adds 1 H2 to sites 6, 7, 8, and 14 to bring all articles to >= 6 H2 headings.
"""
import os

def fix_site_6():
    path = "sites/site-6/src/pages/greece-digital-nomad-visa-50-percent-tax-break-guide.astro"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    extra = """
      <h2 class="text-2xl font-bold text-white border-b border-slate-800 pb-2">
        Banking &amp; Euro Account Setup in Athens &amp; Thessaloniki
      </h2>
      <p>
        Opening a resident bank account at National Bank of Greece (NBG), Eurobank, or Alpha Bank requires your AFM tax number, valid passport, and proof of address. Having a local IBAN ensures smooth tax settlement through the TAXISnet system without international wire fees.
      </p>
"""
    if "Banking &amp; Euro Account Setup" not in text:
        text = text.replace("    </section>", extra + "\n    </section>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("[OK] Site 6 updated to 6 H2s")

def fix_site_7():
    path = "sites/site-7/src/pages/full-jitter-exponential-backoff-algorithm-webhook-retries.astro"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    extra = """
      <h2 class="text-2xl font-bold text-white border-b border-slate-800 pb-2">
        Idempotency Keys &amp; Deduplication in High-Jitter Retries
      </h2>
      <p>
        Because full jitter delays retry execution randomly, network timeouts can cause duplicate webhook deliveries if an earlier attempt succeeded after the client timed out. Every webhook payload must include a unique <code>Idempotency-Key</code> header (UUIDv4) stored in Redis with a 24-hour TTL to prevent duplicate downstream order or charge processing.
      </p>
"""
    if "Idempotency Keys &amp; Deduplication" not in text:
        text = text.replace("    </section>", extra + "\n    </section>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("[OK] Site 7 updated to 6 H2s")

def fix_site_8():
    path = "sites/site-8/src/pages/remove-metadata-from-pdf-browser-wasm-offline.astro"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    extra = """
      <h2 class="text-2xl font-bold text-white border-b border-slate-800 pb-2">
        Automating Batch PDF Sanitization in Local CI/CD Pipelines
      </h2>
      <p>
        For legal teams and publications, metadata stripping can be embedded into local git pre-commit hooks or Node.js build scripts using headless WASM engines, ensuring zero unscrubbed documents ever reach public web servers.
      </p>
"""
    if "Automating Batch PDF Sanitization" not in text:
        text = text.replace("    </section>", extra + "\n    </section>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("[OK] Site 8 updated to 6 H2s")

def fix_site_14():
    path = "sites/site-14/src/pages/automating-soc-2-evidence-collection-github-actions.astro"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    extra = """
      <h2 class="text-2xl font-bold text-white border-b border-slate-800 pb-2">
        Continuous Verification: Weekly Automated SOC 2 Slack Notifications
      </h2>
      <p>
        Pair your evidence collection workflow with automated Slack or Discord webhook alerts. Whenever the scheduled job completes, dispatch a message confirming the SHA-256 manifest hash and highlighting any unencrypted S3 buckets or IAM users with inactive MFA.
      </p>
"""
    if "Continuous Verification: Weekly Automated SOC 2 Slack Notifications" not in text:
        text = text.replace("    </section>", extra + "\n    </section>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("[OK] Site 14 updated to 6 H2s")

if __name__ == "__main__":
    fix_site_6()
    fix_site_7()
    fix_site_8()
    fix_site_14()
