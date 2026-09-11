#!/usr/bin/env python3
"""
Master Antigravity CLI: Autonomous Backlinks & Multi-Protocol Indexing Suite
Single command runner for:
1. Verifying all live backlinks & generating styled Excel report
2. Broadcasting 5-protocol search engine indexing (Google, Bing, Yandex, Blo.gs, Twingly)
3. Broadcasting XML-RPC signals for all verified backlink hubs
"""

import sys
import subprocess
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_step(name, script_rel_path):
    script_full_path = os.path.join(ROOT_DIR, script_rel_path)
    print("\n" + "=" * 75)
    print(f"🚀 EXECUTING STEP: {name}")
    print(f"   Script: {script_rel_path}")
    print("=" * 75)
    res = subprocess.run([sys.executable, script_full_path], cwd=ROOT_DIR)
    if res.returncode != 0:
        print(f"⚠️ Warning: Step '{name}' exited with status code {res.returncode}")
    else:
        print(f"✅ Step '{name}' completed successfully!")
    return res.returncode

def main():
    args = sys.argv[1:]
    
    do_verify = "--verify" in args or "--all" in args or not args
    do_index_fleet = "--index-fleet" in args or "--all" in args or not args
    do_index_backlinks = "--index-backlinks" in args or "--all" in args or not args

    print("===========================================================================")
    print("⚡ ANTIGRAVITY MASTER BACKLINK & INDEXING COMMAND CENTER")
    print("===========================================================================")

    if do_verify:
        run_step("1. Live Backlink Verification & Excel Report Generation", "tools/verify_and_generate_excel_report.py")

    if do_index_fleet:
        run_step("2. Multi-Protocol Fleet Search Engine Indexing", "tools/master_search_engine_indexing_suite.py")
        run_step("2b. GitHub Pages & API v1 IndexNow Submission", "tools/ping_github_pages_indexnow.py")

    if do_index_backlinks:
        run_step("3. XML-RPC Broadcast for All Backlink Hubs", "tools/broadcast_all_backlinks_xmlrpc.py")

    print("\n===========================================================================")
    print("🎉 ALL ANTIGRAVITY BACKLINK & INDEXING TASKS COMPLETED!")
    print("===========================================================================")

if __name__ == "__main__":
    main()
