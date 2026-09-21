import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_bing(q):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<h2[^>]*><a[^>]+href="([^"]+)"[^>]*>(.*?)</a></h2>', html)
            print(f"=== Bing Results for \"{q}\" ({len(matches)} matches) ===")
            if not matches:
                if "There are no results for" in html or "No results found" in html:
                    print("  No indexed results found yet.")
                else:
                    print("  Page returned, but no standard h2 link matched.")
            for link, title in matches[:6]:
                clean_t = re.sub(r'<[^>]+>', '', title)
                print(f"  * {clean_t} -> {link}")
    except Exception as e:
        print(f"Error searching \"{q}\": {e}")

if __name__ == "__main__":
    check_bing("site:openagentstack.pages.dev")
    check_bing("site:jibranpcccc.github.io/digitalcreatoravi-seo-engine")
    check_bing("site:raginspect.pages.dev")
    check_bing("site:groklogtester.pages.dev")
    check_bing("site:site-14-sable.vercel.app")
    check_bing("site:nomadpassportindex.netlify.app")
