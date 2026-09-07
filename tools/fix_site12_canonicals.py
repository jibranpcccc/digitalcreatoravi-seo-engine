#!/usr/bin/env python3
import os

pages_dir = r"c:\Users\jibra\Desktop\1\digitalcreatoravi\sites\site-12\src\pages"
for fname in os.listdir(pages_dir):
    if fname.endswith(".astro"):
        fpath = os.path.join(pages_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content.replace("https://jibranpcccc.github.io/saasunitmath", "https://site-12-taupe.vercel.app")
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {fname}")
