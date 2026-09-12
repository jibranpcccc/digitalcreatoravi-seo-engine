#!/usr/bin/env python3
import os
import sys
import subprocess
import time

SITES_TO_BUILD = [
    'site-2', 'site-4', 'site-12', 'site-13', 'site-14', 
    'site-15', 'site-16', 'site-17', 'site-18', 'site-19', 
    'site-21', 'site-23', 'site-24', 'site-25', 'site-27', 
    'site-29', 'site-30'
]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    print(f"Starting batch rebuild for {len(SITES_TO_BUILD)} sites...\n")
    failed = []
    success = []

    start_total = time.time()
    for sid in SITES_TO_BUILD:
        sdir = os.path.join(ROOT_DIR, "sites", sid)
        print(f"[*] Building {sid}...")
        t0 = time.time()
        res = subprocess.run(
            ["npx", "astro", "build"],
            cwd=sdir,
            shell=True,
            capture_output=True,
            text=True
        )
        duration = round(time.time() - t0, 2)
        if res.returncode == 0:
            print(f"[✓] {sid} built successfully in {duration}s")
            success.append(sid)
        else:
            print(f"[✗] {sid} failed in {duration}s:")
            print(res.stderr[:400])
            failed.append(sid)

    print("\n" + "="*50)
    print(f"Rebuild finished in {round(time.time() - start_total, 2)}s.")
    print(f"Success: {len(success)}/{len(SITES_TO_BUILD)}")
    if failed:
        print(f"Failed sites: {failed}")
        sys.exit(1)
    else:
        print("All target sites rebuilt cleanly!")

if __name__ == "__main__":
    main()
