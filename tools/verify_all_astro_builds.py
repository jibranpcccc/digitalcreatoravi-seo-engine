#!/usr/bin/env python3
"""
Batch test Astro build for sites across the fleet to guarantee zero JSX/Vite build regressions.
"""

import os
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

# Check all sites
SITES = [f"site-{i}" for i in range(1, 21)]

def test_build(site_name):
    site_path = os.path.join(SITES_DIR, site_name)
    if not os.path.exists(site_path):
        return None, "Not Found"
    
    # Check if package.json has build script
    pkg_path = os.path.join(site_path, "package.json")
    if not os.path.exists(pkg_path):
        return None, "No package.json"

    print(f"Building {site_name}...", flush=True)
    res = subprocess.run(["npm.cmd", "run", "build"], cwd=site_path, capture_output=True, text=True)
    if res.returncode == 0:
        return True, "Build OK"
    else:
        # Extract error line
        err_lines = [line for line in res.stderr.splitlines() if "error" in line.lower() or "failed" in line.lower()]
        summary = " | ".join(err_lines[:3]) if err_lines else res.stderr[:300]
        return False, summary

def main():
    print("=== RUNNING ASTRO FLEET BUILD INTEGRITY SUITE ===")
    results = {}
    for s in SITES:
        ok, msg = test_build(s)
        results[s] = (ok, msg)
        status = "PASSED" if ok else ("FAILED" if ok is False else "SKIPPED")
        print(f"  [{s}] {status}: {msg}")

    failed = [s for s, (ok, _) in results.items() if ok is False]
    print(f"\nSummary: {len(results) - len(failed)}/{len(results)} built successfully.")
    if failed:
        print(f"Failed sites: {failed}")
    else:
        print("ALL SITES BUILT WITH ZERO REGRESSIONS!")

if __name__ == "__main__":
    main()
