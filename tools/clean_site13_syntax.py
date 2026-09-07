import os
import re

target_dir = os.path.join("sites", "site-13", "src", "pages")
for root, dirs, files in os.walk(target_dir):
    for fname in files:
        if fname.endswith(".astro"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as fp:
                txt = fp.read()
            
            # Remove all the backslash single quotes: replace {\ \' with {" and \' } with "}
            txt = txt.replace(r"{ \'", '{"').replace(r"\' }", '"}')
            txt = txt.replace("{ '", '{"').replace("' }", '"}')
            
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(txt)
            print("Cleaned quotes in", fpath)
