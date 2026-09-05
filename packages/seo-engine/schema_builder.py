"""
JSON-LD Structured Data Builder (Article, LocalBusiness, LodgingBusiness, FAQPage)
"""
import json

def build_article_schema(title, url, date_published, date_modified, author_name, publisher_name):
    return {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "url": url,
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": {
            "@type": "Person",
            "name": author_name
        },
        "publisher": {
            "@type": "Organization",
            "name": publisher_name,
            "url": "https://localagentstack.com"
        }
    }

def build_property_schema(name, url, city, country, price_range, download_mbps, upload_mbps, latitude, longitude):
    return {
        "@context": "https://schema.org",
        "@type": ["LodgingBusiness", "Place"],
        "name": name,
        "url": url,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city,
            "addressCountry": country
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": latitude,
            "longitude": longitude
        },
        "priceRange": price_range,
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Verified Download Speed", "value": f"{download_mbps} Mbps"},
            {"@type": "LocationFeatureSpecification", "name": "Verified Upload Speed", "value": f"{upload_mbps} Mbps"},
            {"@type": "LocationFeatureSpecification", "name": "Ergonomic Workstations", "value": "Available"}
        ]
    }
