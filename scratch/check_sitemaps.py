import urllib.request, xml.etree.ElementTree as ET

sites = [
    ('site-1', 'https://jibranpcccc.github.io/digitalcreatoravi-seo-engine/'),
    ('site-2', 'https://jibranpcccc.github.io/workationradar/'),
    ('site-3', 'https://openagentstack.pages.dev/'),
    ('site-4', 'https://indiestackaudit.pages.dev/'),
    ('site-5', 'https://vectorbench-hq.netlify.app/'),
    ('site-6', 'https://nomadtreaty.vercel.app/'),
    ('site-7', 'https://webhookwatch.vercel.app/'),
    ('site-8', 'https://localdocprivacy.netlify.app/'),
    ('site-9', 'https://site-9-inky.vercel.app/'),
    ('site-10', 'https://raginspect.pages.dev/'),
    ('site-11', 'https://nomadpassportindex.netlify.app/'),
    ('site-12', 'https://site-12-taupe.vercel.app/'),
    ('site-13', 'https://groklogtester.pages.dev/'),
    ('site-14', 'https://site-14-sable.vercel.app/'),
    ('site-15', 'https://site-15-ruby.vercel.app/'),
    ('site-16', 'https://site-16-indol.vercel.app/'),
    ('site-17', 'https://opencrmstack.pages.dev/'),
    ('site-18', 'https://site-18-chi.vercel.app/'),
    ('site-19', 'https://site-19-nine.vercel.app/'),
    ('site-20', 'https://edgeruntimehq.pages.dev/')
]

for sid, base in sites:
    try:
        req = urllib.request.Request(base + 'sitemap.xml', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as r:
            xml = r.read().decode('utf-8')
            root = ET.fromstring(xml)
            urls = [loc.text.strip() for loc in root.findall('.//{*}loc') if loc.text]
            sub = [u for u in urls if u.rstrip('/') != base.rstrip('/')]
            print(f"{sid}: {len(urls)} URLs | Sample: {sub[0] if sub else 'NONE'}")
    except Exception as e:
        print(f"{sid}: FAILED - {e}")
