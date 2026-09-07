#!/usr/bin/env python3
import os
import glob

sites_dir = "sites"
updated = 0

for site in sorted(os.listdir(sites_dir)):
    site_path = os.path.join(sites_dir, site)
    if not os.path.isdir(site_path):
        continue
    layout_path = os.path.join(site_path, "src", "layouts", "Layout.astro")
    if os.path.exists(layout_path):
        with open(layout_path, "r", encoding="utf-8") as f:
            content = f.read()
        if 'application/rss+xml' not in content:
            # Inject right before </head>
            rss_link = '    <link rel="alternate" type="application/rss+xml" title="RSS 2.0 Feed" href="/rss.xml" />\n  </head>'
            content = content.replace('</head>', rss_link, 1)
            with open(layout_path, "w", encoding="utf-8") as f:
                f.write(content)
            updated += 1
            print(f"Injected RSS alternate link into {site} Layout.astro")

print(f"\nSUCCESS: Injected RSS links into {updated} layouts.")
