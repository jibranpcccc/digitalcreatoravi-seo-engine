# Graph Report - .  (2026-09-05)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 112 nodes · 85 edges · 32 communities (25 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `475d4977`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TestFullSEOSuite
- space/[slug].astro
- [category]/[slug].astro
- site-1/package.json
- site-2/package.json
- dependencies
- dependencies
- LLMAdapter
- InternalLinkEngine
- schema_builder.py
- fetch_channel.py
- decay_detector.py
- quality_gate.py

## God Nodes (most connected - your core abstractions)
1. `TestFullSEOSuite` - 14 edges
2. `LLMAdapter` - 4 edges
3. `InternalLinkEngine` - 4 edges
4. `scripts` - 4 edges
5. `scripts` - 4 edges
6. `../data/properties.json` - 3 edges
7. `astro` - 2 edges
8. `@astrojs/tailwind` - 2 edges
9. `tailwindcss` - 2 edges
10. `astro` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (32 total, 7 thin omitted)

### Community 1 - "space/[slug].astro"
Cohesion: 0.28
Nodes (3): ../data/properties.json, cities, schemaData

### Community 2 - "[category]/[slug].astro"
Cohesion: 0.22
Nodes (5): base, base, schemaData, articles, base

### Community 3 - "site-1/package.json"
Cohesion: 0.25
Nodes (7): name, scripts, build, dev, preview, type, version

### Community 4 - "site-2/package.json"
Cohesion: 0.25
Nodes (7): name, scripts, build, dev, preview, type, version

### Community 5 - "dependencies"
Cohesion: 0.29
Nodes (7): dependencies, astro, @astrojs/tailwind, tailwindcss, astro, @astrojs/tailwind, tailwindcss

### Community 6 - "dependencies"
Cohesion: 0.29
Nodes (7): dependencies, astro, @astrojs/tailwind, tailwindcss, astro, @astrojs/tailwind, tailwindcss

## Knowledge Gaps
- **25 isolated node(s):** `name`, `type`, `version`, `dev`, `build` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `dependencies` connect `dependencies` to `site-1/package.json`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `site-2/package.json`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `name`, `type`, `version` to the rest of the system?**
  _25 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `TestFullSEOSuite` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._