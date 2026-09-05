"""
Automated Sitemap Ingestion & Contextual Semantic Anchor Injection Engine
"""
import re

class InternalLinkEngine:
    def __init__(self, sitemap_urls=None):
        self.sitemap_urls = sitemap_urls or []

    def load_from_dict(self, url_keyword_map):
        self.url_map = url_keyword_map

    def inject_internal_links(self, markdown_content, current_url):
        modified_content = markdown_content
        injected_count = 0

        for target_url, anchor_phrases in self.url_map.items():
            if target_url == current_url or injected_count >= 5:
                continue
            for phrase in anchor_phrases:
                pattern = re.compile(rf"\b({re.escape(phrase)})\b", re.IGNORECASE)
                if pattern.search(modified_content) and f"]({target_url})" not in modified_content:
                    modified_content = pattern.sub(rf"[\1]({target_url})", modified_content, count=1)
                    injected_count += 1
                    break
        return modified_content, injected_count
