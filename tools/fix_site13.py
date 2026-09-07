import os

target_dir = os.path.join("sites", "site-13", "src", "pages")
for root, dirs, files in os.walk(target_dir):
    for fname in files:
        if fname.endswith(".astro"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as fp:
                txt = fp.read()
            new_txt = txt.replace("&#123;", "{\x27{\x27}").replace("&#125;", "{\x27}\x27}")
            if new_txt != txt:
                with open(fpath, "w", encoding="utf-8") as fp:
                    fp.write(new_txt)
                print("Fixed braces in", fpath)
