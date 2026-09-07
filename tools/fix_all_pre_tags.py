import os
import re

target_dir = os.path.join("sites", "site-13", "src", "pages")
for root, dirs, files in os.walk(target_dir):
    for fname in files:
        if fname.endswith(".astro"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as fp:
                txt = fp.read()
            
            # Split frontmatter and template
            parts = txt.split("---")
            if len(parts) >= 3:
                fm = parts[1]
                body = "---".join(parts[2:])
                
                # In frontmatter, restore clean string literals
                fm = fm.replace("{ \x27%{", "%{").replace("}\x27 }", "}")
                
                # In body, add is:raw to all <pre ...> that do not already have is:raw
                def add_is_raw(m):
                    tag = m.group(0)
                    if "is:raw" not in tag:
                        return tag.replace("<pre", "<pre is:raw")
                    return tag
                    
                body = re.sub(r"<pre[^>]*>", add_is_raw, body)
                
                new_txt = "---" + fm + "---" + body
                with open(fpath, "w", encoding="utf-8") as fp:
                    fp.write(new_txt)
                print("Added is:raw to pre tags in", fpath)
