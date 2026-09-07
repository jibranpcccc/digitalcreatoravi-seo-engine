import os
import re

target_dir = os.path.join("sites", "site-13", "src", "pages")
for root, dirs, files in os.walk(target_dir):
    for fname in files:
        if fname.endswith(".astro"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as fp:
                txt = fp.read()
            
            # First clean up previous replacements
            txt = txt.replace("{\x27{\x27}", "{").replace("{\x27}\x27}", "}")
            
            # Pattern: %{...}
            # Replace with { '%{...}' }
            # But avoid already wrapped ones
            def replacer(m):
                content = m.group(0)
                return "{ '" + content + "' }"
                
            new_txt = re.sub(r'%\{[A-Za-z0-9_:\.\-]+(\[[^\]]*\])?\}', replacer, txt)
            
            # Also check for unescaped \{ and \} in LaTeX or regex
            new_txt = new_txt.replace(r"\[", "[").replace(r"\]", "]")
            
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(new_txt)
            print("Sanitized Grok syntax in", fpath)
