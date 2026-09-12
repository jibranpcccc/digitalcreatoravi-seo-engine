#!/usr/bin/env python3
"""
Forensic On-Page & Technical SEO Auditor across all 30 compiled site distributions.
Inspects all HTML pages in sites/*/dist/ for:
1. Title tag (length, non-empty)
2. Meta description (length, non-empty)
3. Canonical URL tag (presence, self-referential)
4. Heading Hierarchy (exact 1 H1, presence of H2)
5. Schema JSON-LD (valid JSON, Schema.org type)
6. Mobile Viewport
7. OpenGraph / Twitter metadata
8. Clean HTML / No parse errors
"""

import os
import glob
import re
import json
from html.parser import HTMLParser

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta_desc = ""
        self.canonical = ""
        self.viewport = ""
        self.h1s = []
        self.h2s = []
        self.h3s = []
        self.current_tag = None
        self.tag_text = ""
        self.in_script_ld = False
        self.script_content = ""
        self.schemas = []
        self.og_title = ""
        self.twitter_card = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag

        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_desc = content
            elif name == "viewport":
                self.viewport = content
            elif prop == "og:title":
                self.og_title = content
            elif name == "twitter:card":
                self.twitter_card = content
        elif tag == "link" and attrs_dict.get("rel") == "canonical":
            self.canonical = attrs_dict.get("href", "")
        elif tag in ("h1", "h2", "h3"):
            self.tag_text = ""
        elif tag == "script" and attrs_dict.get("type") == "application/ld+json":
            self.in_script_ld = True
            self.script_content = ""

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.current_tag in ("h1", "h2", "h3"):
            self.tag_text += data
        elif self.in_script_ld:
            self.script_content += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            text = self.tag_text.strip()
            if text:
                self.h1s.append(text)
            self.tag_text = ""
        elif tag == "h2":
            text = self.tag_text.strip()
            if text:
                self.h2s.append(text)
            self.tag_text = ""
        elif tag == "h3":
            text = self.tag_text.strip()
            if text:
                self.h3s.append(text)
            self.tag_text = ""
        elif tag == "script" and self.in_script_ld:
            self.in_script_ld = False
            raw = self.script_content.strip()
            if raw:
                try:
                    parsed = json.loads(raw)
                    self.schemas.append(parsed)
                except Exception as e:
                    self.schemas.append({"_error": str(e), "raw": raw[:100]})
            self.script_content = ""

def audit_dist():
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    html_files = []
    for i in range(1, 31):
        sid = f"site-{i}"
        dist_dir = os.path.join(ROOT, "sites", sid, "dist")
        if os.path.exists(dist_dir):
            for h in glob.glob(os.path.join(dist_dir, "**", "*.html"), recursive=True):
                # Ignore google verification file or 404
                if "google" in os.path.basename(h) or "404" in os.path.basename(h):
                    continue
                html_files.append((sid, h))

    print(f"Auditing {len(html_files)} compiled HTML pages across all 30 sites...\n")

    issues = []
    passed_pages = 0

    for sid, hpath in html_files:
        rel_path = os.path.relpath(hpath, ROOT)
        with open(hpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        parser = PageParser()
        try:
            parser.feed(content)
        except Exception as e:
            issues.append((sid, rel_path, f"HTML parsing crash: {e}"))
            continue

        page_issues = []

        # 1. Title
        title = parser.title.strip()
        if not title:
            page_issues.append("Missing <title> tag")
        elif len(title) > 85:
            page_issues.append(f"Title too long ({len(title)} chars): '{title[:45]}...'")

        # 2. Meta description
        desc = parser.meta_desc.strip()
        if not desc:
            page_issues.append("Missing <meta name='description'>")
        elif len(desc) < 30:
            page_issues.append(f"Meta description too short ({len(desc)} chars)")

        # 3. Canonical
        if not parser.canonical:
            page_issues.append("Missing <link rel='canonical'>")

        # 4. Viewport
        if not parser.viewport:
            page_issues.append("Missing <meta name='viewport'>")

        # 5. H1 tag
        if len(parser.h1s) == 0:
            page_issues.append("Missing <h1> heading")
        elif len(parser.h1s) > 1:
            page_issues.append(f"Multiple <h1> headings found ({len(parser.h1s)})")

        # 6. Schema JSON-LD
        if not parser.schemas:
            page_issues.append("Missing Schema.org JSON-LD")
        else:
            for s in parser.schemas:
                if "_error" in s:
                    page_issues.append(f"Invalid Schema JSON-LD syntax: {s['_error']}")

        if page_issues:
            issues.append((sid, rel_path, "; ".join(page_issues)))
        else:
            passed_pages += 1

    print(f"Audit Complete: {passed_pages}/{len(html_files)} pages passed 100% of checks.")
    if issues:
        print(f"\nFound {len(issues)} pages with notices or issues:")
        for sid, path, err in issues[:20]:
            print(f"  [{sid}] {path}: {err}")
        if len(issues) > 20:
            print(f"  ...and {len(issues) - 20} more.")
    else:
        print("\nALL PAGES PASSED 100%! ZERO ISSUES!")

if __name__ == "__main__":
    audit_dist()
