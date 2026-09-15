import os
import glob
import re

SPACE_DIR = os.path.join(os.path.dirname(__file__), "..", "sites", "site-2", "src", "pages", "space")

def fix_space_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Check if citySlug is defined
    if "const citySlug" not in content:
        # Insert citySlug definition after prop definition
        # Look for const prop = ... or const { prop } = Astro.props;
        if "const { prop } = Astro.props;" in content:
            content = content.replace(
                "const { prop } = Astro.props;",
                "const { prop } = Astro.props;\nconst citySlug = prop.city.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');"
            )
        elif "if (!prop) {" in content:
            content = content.replace(
                "if (!prop) {\n  throw new Error(",
                "const citySlug = prop.city.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');\nif (!prop) {\n  throw new Error("
            )
        elif "const prop =" in content:
            # Match line ending of const prop = ...;
            content = re.sub(
                r'(const prop\s*=\s*properties\.find\([^;]+;\n)',
                r"\1const citySlug = prop.city.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');\n",
                content
            )

    # Replace broken city links and schema items
    content = content.replace(
        '"item": `https://workationradar.com/city//`',
        '"item": `https://workationradar.com/city/${citySlug}/`'
    )
    content = content.replace(
        '"item": `https://workationradar.com/city/`',
        '"item": `https://workationradar.com/city/${citySlug}/`'
    )
    content = content.replace(
        '<a href={`/city//`}',
        '<a href={`${base}/city/${citySlug}/`}'
    )
    content = content.replace(
        '<a href={`/city/`}',
        '<a href={`${base}/city/${citySlug}/`}'
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed: {os.path.basename(filepath)}")
        return True
    else:
        print(f"No change needed: {os.path.basename(filepath)}")
        return False

def main():
    files = glob.glob(os.path.join(SPACE_DIR, "*.astro"))
    print(f"Processing {len(files)} files in {SPACE_DIR}...")
    fixed_count = 0
    for fp in sorted(files):
        if fix_space_file(fp):
            fixed_count += 1
    print(f"Completed: {fixed_count} files fixed.")

if __name__ == "__main__":
    main()
