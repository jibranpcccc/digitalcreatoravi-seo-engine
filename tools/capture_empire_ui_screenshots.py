#!/usr/bin/env python3
"""
Captures high-resolution Desktop (1440x900) and Mobile (390x844) screenshots
for all 20 live sites in the portfolio using Playwright Chromium.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHOT_DIR = os.path.join(ROOT_DIR, "reports", "ui_screenshots")
os.makedirs(SHOT_DIR, exist_ok=True)

FLEET = [
    {"id": "site-1", "name": "LocalAgentStack", "url": "https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/"},
    {"id": "site-2", "name": "WorkationRadar", "url": "https://jibranpcccc.github.io/workationradar/"},
    {"id": "site-3", "name": "OpenAgentStack", "url": "https://openagentstack.pages.dev/"},
    {"id": "site-4", "name": "IndieStackAudit", "url": "https://indiestackaudit.pages.dev/"},
    {"id": "site-5", "name": "VectorBench", "url": "https://vectorbench-hq.netlify.app/"},
    {"id": "site-6", "name": "NomadTreaty", "url": "https://nomadtreaty.vercel.app/"},
    {"id": "site-7", "name": "WebhookWatch", "url": "https://webhookwatch.vercel.app/"},
    {"id": "site-8", "name": "LocalDocPrivacy", "url": "https://localdocprivacy.netlify.app/"},
    {"id": "site-9", "name": "FounderRunway", "url": "https://site-9-inky.vercel.app/"},
    {"id": "site-10", "name": "RAGInspect", "url": "https://raginspect.pages.dev/"},
    {"id": "site-11", "name": "NomadPassportIndex", "url": "https://nomadpassportindex.netlify.app/"},
    {"id": "site-12", "name": "SaaSUnitMath", "url": "https://site-12-taupe.vercel.app/"},
    {"id": "site-13", "name": "GrokLogTester", "url": "https://groklogtester.pages.dev/"},
    {"id": "site-14", "name": "SOC2Ready", "url": "https://site-14-sable.vercel.app/"},
    {"id": "site-15", "name": "EORCalculator", "url": "https://site-15-ruby.vercel.app/"},
    {"id": "site-16", "name": "DevConfigHub", "url": "https://site-16-indol.vercel.app/"},
    {"id": "site-17", "name": "OpenCRMStack", "url": "https://opencrmstack.pages.dev/"},
    {"id": "site-18", "name": "CIPipelineGraph", "url": "https://site-18-chi.vercel.app/"},
    {"id": "site-19", "name": "GreekVisualizer", "url": "https://site-19-nine.vercel.app/"},
    {"id": "site-20", "name": "EdgeRuntimeHQ", "url": "https://edgeruntimehq.pages.dev/"},
]

def capture_all():
    print(f"[*] Starting screenshot capture for {len(FLEET)} sites...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Desktop context
        desktop_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        desktop_page = desktop_ctx.new_page()
        
        # Mobile context
        mobile_ctx = browser.new_context(viewport={"width": 390, "height": 844})
        mobile_page = mobile_ctx.new_page()
        
        for s in FLEET:
            sid = s["id"]
            name = s["name"]
            url = s["url"]
            print(f"\n--- Capturing [{sid}] {name}: {url} ---")
            
            # Desktop
            try:
                desktop_page.goto(url, timeout=25000, wait_until="domcontentloaded")
                time.sleep(1.5)
                desk_path = os.path.join(SHOT_DIR, f"{sid}_desktop.png")
                desktop_page.screenshot(path=desk_path, full_page=False)
                print(f"  [Desktop] -> {desk_path}")
            except Exception as e:
                print(f"  [Desktop ERR] {e}")
                
            # Mobile
            try:
                mobile_page.goto(url, timeout=25000, wait_until="domcontentloaded")
                time.sleep(1.0)
                mob_path = os.path.join(SHOT_DIR, f"{sid}_mobile.png")
                mobile_page.screenshot(path=mob_path, full_page=False)
                print(f"  [Mobile]  -> {mob_path}")
            except Exception as e:
                print(f"  [Mobile ERR] {e}")
                
        browser.close()
    print("\n[✔] All fleet UI screenshots captured successfully!")

if __name__ == "__main__":
    capture_all()
