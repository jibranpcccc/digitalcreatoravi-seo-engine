import os, sys

def enrich_file(path, extra_sections):
    if not os.path.exists(path):
        print(f"Not found: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if already enriched
    if "## Extended Architecture & In-Depth Technical Breakdown" in content:
        print(f"Already enriched: {path}")
        return
        
    enriched = content.strip() + "\n\n" + extra_sections.strip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(enriched)
    words = len(enriched.split())
    print(f"Enriched {path} -> {words} words")

# Enrich Site 4 articles
s4_p1 = r"sites/site-4/src/content/stacks/nextjs-vs-astro-for-micro-saas-speed-cost-seo.md"
s4_e1 = """
## Extended Architecture & In-Depth Technical Breakdown

### Real-World Vercel Compute Billing Traps
When bootstrapped teams deploy Next.js App Router applications to Vercel, the combination of server actions, dynamic server rendering, and middleware executions triggers continuous serverless compute usage. On Vercel's Pro plan, each project includes a modest baseline of compute units. However, when Googlebot, Bingbot, and AI search scrapers index a programmatic directory with 1,000+ dynamic routes, edge serverless executions spike dramatically. Many founders discover surprise $50 to $200 monthly invoices strictly from search engine indexing activity.

With Astro's static site generation (SSG), HTML and CSS are compiled ahead of time. When deployed to Cloudflare Pages or GitHub Pages, search engine bots fetch static files directly from edge CDN storage. There is zero serverless compute invoked, meaning monthly hosting bills remain mathematically zero regardless of crawl frequency.

### Core Web Vitals Optimization Matrix
Google's ranking algorithm penalizes web pages that suffer from poor Interaction to Next Paint (INP) and Cumulative Layout Shift (CLS). Next.js applications ship React's client runtime (~84 KB gzipped), which must be parsed and executed by the browser before user interactions register. On mid-range Android devices, this hydration cost degrades mobile PageSpeed scores.

Astro eliminates this entirely through its Islands Architecture. Pure content sections compile to zero JavaScript, while interactive widgets (such as an embedded calculator or checkout form) hydrate independently using `client:visible` or `client:idle` directives.

### Step-by-Step Production Setup for 2026
1. **Frontend Hosting**: Deploy Astro to Cloudflare Pages with automated GitHub integration.
2. **Dynamic Endpoints**: Utilize Cloudflare Pages Functions (`/functions/api/*`) for lightweight serverless API logic.
3. **Database Layer**: Connect to Turso (libSQL) or Neon Postgres using connection pooling over HTTP.
4. **Content Architecture**: Store documentation, teardowns, and comparison matrices as Markdown or MDX files within `src/content/` for compile-time validation.

## Frequently Asked Questions

### Can Astro support authenticated user dashboards?
Yes. Astro supports hybrid and server-side rendering modes via official adapters for Cloudflare, Node.js, and Vercel. You can handle secure HTTP-only session cookies and render personalized user profiles while keeping marketing pages 100% static.

### How does Astro compare to Next.js for internationalization (i18n)?
Astro includes native routing-based i18n support out of the box, allowing developers to configure prefix-based language routes without external dependencies or middleware redirects.
"""

s4_p2 = r"sites/site-4/src/content/billing/stripe-vs-lemonsqueezy-vs-polar-saas-fee-calculator-2026.md"
s4_e2 = """
## Extended Architecture & In-Depth Technical Breakdown

### The True Cost of Self-Managed Sales Tax
While Stripe Direct advertises a lower nominal transaction fee (2.9% + 30¢), operating as your own merchant of record imposes severe hidden accounting overhead. In the European Union, the VAT MOSS regulation mandates that digital software sales collect and remit value-added tax according to the buyer's home country. In the United States, over 30 states have established economic nexus thresholds for remote digital sellers.

If you process $10,000 monthly with Stripe Direct, you must either manually register with tax authorities worldwide or subscribe to automated sales tax compliance software such as Stripe Tax (+0.5% per transaction) or TaxJar ($99/month base). When factoring in annual CPA filing fees for international tax returns, the effective cost of running Stripe Direct rises from 2.9% to over 4.8%.

### Why Modern Developers Prefer Polar
Polar operates as a full Merchant of Record tailored specifically for software developers, indie hackers, and open-source creators. Key advantages include:
1. **Developer-First SDKs**: Strongly typed TypeScript, Python, and Go libraries with automated webhook validation.
2. **License Key Generation**: Built-in digital license issuance, activation tracking, and seat validation.
3. **Transparent Payouts**: Direct deposits via Stripe Connect without the 10% rolling fraud reserves frequently imposed by older platforms.
4. **Discord & GitHub Sync**: Native integration for granting private repository access and Discord community roles upon checkout.

### Production Webhook Verification Code
To ensure secure order fulfillment, verify Polar webhook signatures using HMAC SHA-256:

```typescript
import { Webhook } from 'standardwebhooks';

export async function handlePolarWebhook(rawBody: string, headers: Headers) {
  const webhookSecret = process.env.POLAR_WEBHOOK_SECRET!;
  const wh = new Webhook(webhookSecret);
  
  const payload = wh.verify(rawBody, {
    'webhook-id': headers.get('webhook-id')!,
    'webhook-timestamp': headers.get('webhook-timestamp')!,
    'webhook-signature': headers.get('webhook-signature')!,
  });
  
  return payload;
}
```

## Frequently Asked Questions

### Can Polar handle recurring subscription upgrades and prorations?
Yes. Polar automatically handles billing cycle alignment, tiered subscription upgrades, credit card retries (dunning), and customer billing portal links.

### How are chargebacks handled by a Merchant of Record?
Because the MoR is the merchant of record on the customer's credit card statement, their dedicated fraud prevention team investigates dispute claims and submits evidence directly to the payment networks.
"""

s4_p3 = r"sites/site-4/src/content/stacks/self-hosted-supabase-vs-managed-neon-postgres-cost-math.md"
s4_e3 = """
## Extended Architecture & In-Depth Technical Breakdown

### Architectural Comparison: Monolith vs Decoupled Compute
Self-hosted Supabase packages a complete database platform inside Docker containers: PostgreSQL, GoTrue authentication, PostgREST RESTful APIs, Realtime WebSocket listeners, and Storage backends. This monolithic design requires sufficient RAM (minimum 2GB to 4GB) to avoid Linux out-of-memory (OOM) killer terminations.

In contrast, Neon separates compute from storage at the engine level. Neon's storage engine stores write-ahead logs (WAL) across distributed object stores. Compute nodes are ephemeral, stateless Linux microVMs that can scale up, down, or pause entirely in seconds.

### When Self-Hosting Makes Economic Sense
1. **High Data Ingestion Workloads**: If your application ingests millions of time-series records, log events, or vector embeddings monthly, managed cloud database storage tiers ($1.50 to $2.50 per GB) become expensive. A $12/month Hetzner cloud server includes 80GB of high-speed NVMe storage.
2. **Heavy WebSocket Concurrency**: If your SaaS features collaborative real-time editing or live dashboards, Supabase Realtime running on a dedicated VPS can handle thousands of simultaneous persistent WebSocket connections without per-message surcharges.

### Automated Backup Pipeline for Self-Hosted Supabase
To ensure zero data loss on a self-hosted VPS, implement an automated daily backup script that streams compressed encrypted snapshots to Cloudflare R2 or Amazon S3:

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/supabase"
mkdir -p "$BACKUP_DIR"

docker exec supabase-db pg_dump -U postgres -F c -b -v -f "$BACKUP_DIR/db_$TIMESTAMP.dump" postgres
aws --endpoint-url https://<account_id>.r2.cloudflarestorage.com s3 cp "$BACKUP_DIR/db_$TIMESTAMP.dump" s3://backups/
rm -f "$BACKUP_DIR/db_$TIMESTAMP.dump"
```

## Frequently Asked Questions

### Does Neon support the pgvector extension for AI embeddings?
Yes. Neon natively supports `pgvector` alongside standard indexing algorithms (HNSW and IVFFlat), allowing developers to store and query vector embeddings for RAG pipelines without provisioning separate vector databases.

### How does connection pooling work in serverless environments?
Neon provides an integrated PgBouncer connection pooling layer reachable via a pooled connection string (port 5432 or 6543), preventing serverless edge functions from exceeding PostgreSQL's maximum connection limits.
"""

s4_p4 = r"sites/site-4/src/content/stacks/zero-cost-saas-stack-cloudflare-pages-turso-resend.md"
s4_e4 = """
## Extended Architecture & In-Depth Technical Breakdown

### The Power of Edge-Distributed SQLite
Traditional client-server database architectures require database requests to traverse international fiber networks to reach a centralized database instance (typically in US-East or EU-Central). For users in Australia or Southeast Asia, this introduces 200ms+ of physical latency per query.

Turso addresses this by building on **libSQL**, an open-source extension of SQLite. Developers can configure read replicas at Cloudflare edge points of presence across the world. When a user requests data, the nearest edge replica serves the query in sub-5ms, while write transactions are safely committed to the primary region.

### Production Drizzle ORM Schema
Connecting Turso to your TypeScript application with Drizzle ORM ensures compile-time type safety:

```typescript
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  role: text('role').default('user'),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
});

export const auditLogs = sqliteTable('audit_logs', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => users.id),
  action: text('action').notNull(),
  ipAddress: text('ip_address'),
  timestamp: integer('timestamp', { mode: 'timestamp' }).notNull(),
});
```

### Free Tier Durability & Risk Management
To ensure your zero-cost stack remains completely free during viral traffic spikes:
1. **Cloudflare Cache Rules**: Configure 60-second public edge caching on all public directory endpoints to deflect 95% of incoming database reads.
2. **Rate Limiting**: Implement basic Cloudflare IP rate limiting rules to block automated scraping bots from exhausting libSQL read quotas.
3. **Asset Storage**: Store user avatars and uploaded documents in Cloudflare R2, which offers 10GB of free storage with zero egress bandwidth fees.

## Frequently Asked Questions

### What happens when Turso exceeds the 9GB free storage limit?
Turso notifies the team via email when storage approaches 80% capacity. Upgrading to the Pro tier costs $29/month and expands storage to 100GB with priority support.

### Can Resend send marketing campaigns as well as transactional receipts?
Yes. Resend supports automated contact lists, broadcast newsletters, and transactional messages using the same API keys and verified sending domains.
"""

s4_p5 = r"sites/site-4/src/content/billing/open-source-auth-comparison-clerk-lucia-better-auth.md"
s4_e5 = """
## Extended Architecture & In-Depth Technical Breakdown

### The Vendor Lock-In Problem in Commercial Auth
Third-party hosted authentication services store your user records, password hashes, and MFA secrets on their proprietary cloud infrastructure. While this accelerates initial time-to-market, it creates substantial platform lock-in. If a vendor changes pricing terms or sunsets features, extracting your user base is challenging because password hashes cannot be easily transferred across differing hashing algorithms.

Open-source authentication frameworks like **Better-Auth** store 100% of user data inside your own relational database tables. You maintain full schema control, allowing custom columns (such as `stripe_customer_id`, `organization_id`, or `api_quota`) to live in the same row as user credentials.

### WebAuthn & Passkey Authentication Flow
Better-Auth provides native support for WebAuthn passkeys, enabling biometric authentication (Touch ID, Face ID, Windows Hello) directly within the browser:

```typescript
import { authClient } from './auth-client';

// Register biometric passkey
export async function registerBiometricPasskey() {
  const result = await authClient.passkey.addPasskey({
    name: 'MacBook Pro Touch ID'
  });
  return result;
}

// Sign in with passkey
export async function signInWithPasskey() {
  const session = await authClient.signIn.passkey();
  return session;
}
```

This delivers a seamless, passwordless login experience that eliminates phishing risks while reducing customer support tickets related to forgotten passwords.

### Multi-Tenancy Architecture for B2B Startups
Better-Auth includes a first-class Organizations plugin designed specifically for multi-tenant SaaS products. It provides:
- Team creation and member invitations via signed email tokens.
- Role-based access control (Owner, Admin, Member, Guest).
- Context-aware session switching between personal and workspace accounts.

## Frequently Asked Questions

### How does Better-Auth prevent brute force login attempts?
Better-Auth includes automated rate limiting on password submission endpoints, progressive delay backoffs, and optional CAPTCHA verification via Cloudflare Turnstile.

### Does Better-Auth require a Node.js server, or can it run on Edge Workers?
Better-Auth is runtime agnostic. It runs smoothly on Node.js, Bun, Deno, and serverless edge environments such as Cloudflare Workers and Vercel Edge Runtime.
"""

for p, extra in [
    (s4_p1, s4_e1),
    (s4_p2, s4_e2),
    (s4_p3, s4_e3),
    (s4_p4, s4_e4),
    (s4_p5, s4_e5),
]:
    enrich_file(p, extra)

print("Enrichment complete for Site 4.")
