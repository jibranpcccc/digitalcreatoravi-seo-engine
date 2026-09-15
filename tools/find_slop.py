#!/usr/bin/env python3
import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES_DIR = os.path.join(ROOT_DIR, "sites")

SLOP_WORDS = [
    "in conclusion", "it is important to remember", "tapestry of",
    "delve into", "testament to", "revolutionize", "game-changer",
    "furthermore, it is worth noting", "plethora of", "unleash",
    "in this article", "beacon of hope", "navigate the landscape"
]

for s in [f"site-{i}" for i in range(1, 21)]:
    s_path = os.path.join(SITES_DIR, s)
    for f in glob.glob(os.path.join(s_path, "src", "**", "*.*"), recursive=True):
        if not (f.endswith(".md") or f.endswith(".astro")):
            continue
        with open(f, "r", encoding="utf-8", errors="ignore") as fl:
            c = fl.read()
        matches = [w for w in SLOP_WORDS if w in c.lower()]
        if matches:
            print(f"{s}: {os.path.relpath(f, s_path)} -> {matches}")
