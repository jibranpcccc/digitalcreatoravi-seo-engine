---
title: "Self-Hosted Supabase vs Managed Neon Postgres: Real Cost Math"
description: "Cold starts, connection pooling limits, compute pricing, and operational maintenance comparison of self-hosted Supabase vs Neon Serverless Postgres."
category: "stacks"
slug: "self-hosted-supabase-vs-managed-neon-postgres-cost-math"
author: "IndieStackAudit Research"
date: "2026-09-05"
---
> **Quick Answer**: **Managed Neon Serverless Postgres** is the superior database choice for micro-SaaS projects generating under \$5,000 MRR due to its generous free tier (0.5GB compute, scale-to-zero, and branching), eliminating server maintenance. **Self-hosted Supabase** on a \$10/month Hetzner VPS becomes cost-effective once your database requires multi-gigabyte storage, real-time WebSocket subscriptions, and high-frequency background worker jobs.

## Key Takeaways
* **Scale to Zero**: Neon automatically pauses compute during inactivity, saving resources for early-stage products with intermittent traffic.
* **Storage Pricing**: Neon charges \$1.50/GB/month after free limits, whereas a self-hosted VPS provides 40GB+ NVMe SSD storage for a flat \$6/month.
* **Connection Pooling**: Neon provides built-in PgBouncer pooling that prevents serverless function exhaustion.

## Cost Breakdown by Workload

| Workload Profile | Managed Neon Serverless | Self-Hosted Supabase (Docker) | Managed Supabase Pro |
| :--- | :--- | :--- | :--- |
| **MVP (< 1k users)** | **\$0.00 / month** | \$5.00 / month (VPS) | \$25.00 / month |
| **Early Growth (10k users)** | \$19.00 / month | \$12.00 / month (VPS) | \$25.00 / month |
| **High Traffic (> 100k users)** | \$85.00 / month | **\$28.00 / month (VPS)** | \$95.00 / month |
| **Database Branching** | Instant (Copy-on-write) | Manual dump/restore | Add-on fee |
