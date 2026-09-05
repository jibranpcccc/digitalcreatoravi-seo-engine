#!/usr/bin/env python3
"""Autonomous Site 3 (OpenAgentStack) Builder & Cloudflare Deployer."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont

SITE_DIR = "sites/site-3"
PUBLIC_DIR = f"{SITE_DIR}/public"
SRC_DIR = f"{SITE_DIR}/src"

W, H = 1200, 675

def get_fonts():
    try:
        f_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 46)
        f_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
        f_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
        f_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 34)
        f_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    except Exception:
        f_title = f_sub = f_badge = f_val = f_lbl = ImageFont.load_default()
    return f_title, f_sub, f_badge, f_val, f_lbl

def generate_cover(slug, title, category, accent=(16, 185, 129)):
    out_path = f"{PUBLIC_DIR}/images/covers/{slug}.webp"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    f_title, f_sub, f_badge, f_val, f_lbl = get_fonts()
    img = Image.new("RGB", (W, H), color=(6, 15, 12))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(16, 16), (W-16, H-16)], radius=16, outline=(20, 45, 35), width=2)
    draw.rounded_rectangle([(16, 16), (W-16, 24)], radius=8, fill=accent)
    draw.rounded_rectangle([(60, 60), (320, 92)], radius=8, fill=(10, 30, 22), outline=accent, width=1)
    draw.text((75, 68), category.upper(), font=f_badge, fill=accent)
    
    words = title.split()
    lines, curr = [], []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 38:
            lines.append(" ".join(curr[:-1]))
            curr = [w]
    if curr: lines.append(" ".join(curr))
    
    y = 120
    for l in lines[:2]:
        draw.text((60, y), l, font=f_title, fill=(255, 255, 255))
        y += 55
    draw.text((60, y + 10), "Open-Source Autonomous AI Agent Benchmarks & MCP Architecture (2026)", font=f_sub, fill=(148, 163, 184))
    
    draw.rounded_rectangle([(60, 480), (W-60, 610)], radius=12, fill=(10, 25, 20), outline=(20, 45, 35), width=1)
    draw.text((90, 510), "BENCHMARK METRIC", font=f_lbl, fill=(148, 163, 184))
    draw.text((90, 535), "Tool Execution Acc", font=f_val, fill=(52, 211, 153))
    draw.text((500, 510), "LATENCY IMPACT", font=f_lbl, fill=(148, 163, 184))
    draw.text((500, 535), "Sub-50ms Edge TTFB", font=f_val, fill=(96, 165, 250))
    draw.text((900, 510), "COMPLIANCE", font=f_lbl, fill=(148, 163, 184))
    draw.text((900, 535), "100/100 Content SEO", font=f_val, fill=(245, 158, 11))
    img.save(out_path, "WEBP", quality=92)

def generate_diagram(slug, title):
    out_path = f"{PUBLIC_DIR}/images/benchmarks/{slug}-benchmark.webp"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    f_title, f_sub, f_badge, f_val, f_lbl = get_fonts()
    img = Image.new("RGB", (W, H), color=(4, 12, 10))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(16, 16), (W-16, H-16)], radius=16, outline=(20, 45, 35), width=2)
    draw.text((60, 50), "EMPIRICAL AGENTIC ORCHESTRATION PIPELINE", font=f_badge, fill=(16, 185, 129))
    draw.text((60, 80), title[:50] + "...", font=f_title, fill=(255, 255, 255))
    
    draw.rounded_rectangle([(60, 200), (580, 580)], radius=14, fill=(10, 25, 20), outline=(16, 185, 129), width=2)
    draw.text((90, 230), "EXECUTION PROFILE", font=f_lbl, fill=(148, 163, 184))
    draw.text((90, 265), "Tool Call Precision", font=f_val, fill=(52, 211, 153))
    draw.text((90, 330), "• Native Schema Validation\n• Zero-Shot Json Output\n• Guardrailed Re-planning Loop", font=f_sub, fill=(203, 213, 225))
    
    draw.rounded_rectangle([(620, 200), (W-60, 580)], radius=14, fill=(10, 25, 20), outline=(59, 130, 246), width=2)
    draw.text((650, 230), "RESOURCE FOOTPRINT", font=f_lbl, fill=(148, 163, 184))
    draw.text((650, 265), "Local Memory Ceiling", font=f_val, fill=(96, 165, 250))
    draw.text((650, 330), "• Under 4GB RAM Footprint\n• Async Fiber Concurrency\n• 100% Offline Capable", font=f_sub, fill=(203, 213, 225))
    img.save(out_path, "WEBP", quality=90)

print("Writing package.json...")
pkg = {
    "name": "site-3-openagentstack",
    "type": "module",
    "version": "1.0.0",
    "scripts": {
        "dev": "astro dev",
        "build": "astro build",
        "preview": "astro preview"
    },
    "dependencies": {
        "astro": "^4.0.0",
        "@astrojs/tailwind": "^5.0.0",
        "tailwindcss": "^3.4.0"
    }
}
with open(f"{SITE_DIR}/package.json", "w") as f:
    json.dump(pkg, f, indent=2)

print("Writing astro.config.mjs...")
astro_cfg = """import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://openagentstack.pages.dev',
  base: '/',
  build: {
    format: 'directory'
  }
});
"""
with open(f"{SITE_DIR}/astro.config.mjs", "w") as f:
    f.write(astro_cfg)

print("Writing tailwind.config.mjs...")
tw_cfg = """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        agent: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669',
          900: '#064e3b',
          950: '#022c22'
        }
      }
    },
  },
  plugins: [],
};
"""
with open(f"{SITE_DIR}/tailwind.config.mjs", "w") as f:
    f.write(tw_cfg)

print("Site 3 core configuration written.")
