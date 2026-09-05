# Topical Authority Architecture & Faceted Database Map: Site 2 (WorkationRadar)

This document establishes the programmatic taxonomy, faceted filtering architecture, and internal linking structure for **Site 2**.

---

## 1. Programmatic Taxonomy & URL Architecture

```
WorkationRadar (Root)
│
├── 1.0 /destinations/ (Global Hub Index)
│   ├── 1.1 /destinations/europe/ (Regional Pillar)
│   │   ├── 1.1.1 /destinations/portugal/madeira/ (City Hub Pillar)
│   │   │   ├── Property 1: /property/madeira/digital-nomad-village-ponta-do-sol/
│   │   │   ├── Property 2: /property/madeira/funchal-cowork-coliving/
│   │   │   └── Filter: /coliving/madeira/fiber-wifi-100mbps/
│   │   └── 1.1.2 /destinations/bulgaria/bansko/ (City Hub Pillar)
│   │       ├── Property 1: /property/bansko/coworking-bansko-coliving/
│   │       └── Filter: /coliving/bansko/under-1000-month/
│   │
│   ├── 1.2 /destinations/asia/ (Regional Pillar)
│   │   ├── 1.2.1 /destinations/indonesia/bali-canggu/ (City Hub Pillar)
│   │   └── 1.2.2 /destinations/thailand/chiang-mai/ (City Hub Pillar)
│   │
│   └── 1.3 /destinations/americas/ (Regional Pillar)
│       ├── 1.3.1 /destinations/colombia/medellin/ (City Hub Pillar)
│       └── 1.3.2 /destinations/mexico/mexico-city/ (City Hub Pillar)
│
├── 2.0 /amenities/ (Faceted Feature Hubs)
│   ├── 2.1 /amenities/verified-fiber-wifi/
│   ├── 2.2 /amenities/ergonomic-standing-desks/
│   ├── 2.3 /amenities/soundproof-phone-booths/
│   └── 2.4 /amenities/backup-generator-power/
│
└── 3.0 /nomad-visas/ (Regulatory Reference Hub)
    ├── 3.1 /nomad-visas/portugal-d8-visa-guide/
    └── 3.2 /nomad-visas/spain-digital-nomad-visa-guide/
```

---

## 2. Programmatic Facet Quality Gate & Anti-Doorway Safeguards
To comply with Google's Scaled Content Abuse policies, faceted filter URLs (e.g. `/coliving/madeira/fiber-wifi-100mbps/`) are generated and indexed **ONLY IF**:
1. The filter matches at least 3 distinct, independently verified properties.
2. The page includes unique aggregated statistics (average download speed, standard deviation, median monthly rent for that amenity).
3. The page contains original editorial introductory and neighborhood context.
4. If a facet combination has fewer than 3 properties, it automatically receives a `NOINDEX, FOLLOW` meta tag.

---

## 3. Structured Data Integration
- Every City Hub outputs `ItemList` schema containing references to all listed spaces.
- Every individual Property Profile outputs `LodgingBusiness` + `Place` schema containing:
  - Exact geo-coordinates (`latitude`, `longitude`).
  - `amenityFeature` array specifying verified WiFi speeds, desk types, and call booths.
  - Transparent price ranges (`priceRange`).
  - Aggregate rating based on verified remote worker reviews.
