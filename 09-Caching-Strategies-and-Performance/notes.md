# Module 09 — Caching Strategies & Performance Optimization

Domain focus: **Domain 1, Task Statement 3** ("Implement caching strategies to improve application performance" — write-through, read-through, lazy loading, TTL, verbatim from the exam guide) and **Domain 4, Task Statement 3 in its entirety** ("Optimize application performance" — caching, concurrency, messaging services, profiling, minimum memory/compute sizing, and caching content based on request headers). This module assumes module 08's ElastiCache and RDS fundamentals and module 03's DynamoDB fundamentals as background — here we go deep on the *patterns* you implement on top of a cache, not the cache service setup itself.

Caching is deceptively simple to describe ("keep a copy of expensive-to-fetch data somewhere faster") and genuinely hard to get right, because every caching decision trades **freshness** for **speed**. The exam tests whether you know which trade-off a given scenario calls for, and whether you can read pseudocode and identify which pattern it implements — so this module leans heavily on tracing code, not just memorizing labels.

## 1. Why caching matters, and where the layers sit

A request in a typical AWS application can be slowed down at several points: application compute, a network hop to a database, the database's own query execution, and the network hop back. Caching attacks this by inserting a fast, usually in-memory, data store somewhere in that path so repeat requests for the same data skip the expensive hop entirely. There isn't one cache in a real system — there are usually several layers stacked on top of each other:

| Layer | Example service | What it caches |
|---|---|---|
| CDN / edge | CloudFront | Full HTTP responses (HTML, images, API responses) close to the end user |
| API layer | API Gateway caching | Responses to specific API method + parameter combinations |
| Application / data | ElastiCache (Redis/Memcached) | Query results, session data, computed objects — pattern is *your* code's responsibility |
| Database-specific | DAX (DynamoDB), RDS/Aurora read replicas | Item-level or query-level results, API-compatible with the database client |

A single request might pass through two or three of these layers. The exam likes to test whether you understand that a CDN cache miss still has to traverse every layer behind it, and that a badly configured cache at any one layer can either serve stale data or (worse) leak one user's data to another — both of which show up constantly in DVA-C02 scenarios.

## 2. Lazy Loading (Cache-Aside)

This is the pattern you'll implement most often when you're the one writing the caching logic yourself (e.g., against ElastiCache). The application code is fully responsible for checking the cache, falling back to the database on a miss, and populating the cache afterward. It's called "lazy" because the cache is only ever populated *on demand*, the first time a piece of data is actually requested — nothing is pre-loaded.

**Read path (pseudocode):**
```
function getProduct(productId):
    product = cache.get(productId)          # 1. check cache first
    if product is not null:
        return product                       # 2. cache hit — done, no DB touched
    else:
        product = database.query(productId)  # 3. cache miss — read from source of truth
        cache.set(productId, product, ttl=300)  # 4. populate cache for next time
        return product
```

**Write path (pseudocode):**
```
function updateProduct(productId, newData):
    database.update(productId, newData)     # 1. write goes straight to the DB
    cache.delete(productId)                  # 2. invalidate the now-stale cache entry
```

Two things to internalize about the write path, because they're exactly what the exam probes:
- The cache is **not** updated with the new value on a write — it's simply invalidated (deleted). The very next read for that key is guaranteed to be a cache miss, which re-populates the cache with fresh data from step 3 of the read path.
- Between the write completing and the next read repopulating the cache, there is a **window where the key is either absent or, if the invalidation step is skipped/delayed, stale** — this is the core trade-off of lazy loading.

**Exam trap:** if an option's write path shows the application writing to the cache *and* the database *together, synchronously, as one operation*, that's not lazy loading — that's write-through (Section 3). Lazy loading's defining trait is that cache population only happens reactively, from the *read* path, triggered by a miss.

## 3. Write-Through

Write-through keeps the cache always in sync with the database by updating both, together, as part of every write operation.

**Pseudocode:**
```
function updateProduct(productId, newData):
    database.update(productId, newData)     # 1. write to the source of truth
    cache.set(productId, newData)            # 2. immediately update the cache too
```

Reads become trivially simple — `cache.get(productId)` — because if the key was ever written, the cache already has the current value; there's no "check cache, fall back to DB" branching needed on the happy path (though a cold key that was never written still misses and needs a fallback, often lazy-loaded on first read).

**Trade-offs:**
- **Pro:** the cache is never stale for data that's been written — strong freshness guarantee compared to lazy loading's post-write gap.
- **Con:** every write now has higher latency, because it has to complete two operations (DB + cache) instead of one, and if the cache write fails after the DB write succeeds, you now have to handle that partial-failure case.
- **Con:** the cache fills up with data that was written but may never actually be read again — write-through caches everything that gets written, not just what's popular, which can waste cache memory on cold data.

**Exam trap:** a scenario that says "the application must never serve stale data immediately after a write, and can tolerate slightly higher write latency" is describing write-through, not lazy loading — lazy loading always has a stale/missing window after a write.

## 4. Read-Through

Read-through looks similar to lazy loading from the outside (a miss triggers a DB read and cache population), but the key difference is **where that logic lives**. In lazy loading, your application code contains the "if miss, query DB, then populate cache" branch. In read-through, the caching layer itself sits transparently in front of the database and handles the miss internally — your application code just calls the cache, and the cache client/library/service does the rest.

**Pseudocode — what your application code actually calls:**
```
function getProduct(productId):
    return cache.get(productId)     # that's it — no manual miss-handling in app code
```

**Pseudocode — what happens inside the caching layer, transparently:**
```
function cache.get(key):
    if key exists in the cache store:
        return cached value                    # cache hit
    else:
        value = database.query(key)            # cache miss — the CACHE does this, not your app
        store(key, value)
        return value
```

The real-world example the exam wants you to connect this to is **DAX (DynamoDB Accelerator)**: your application keeps calling the same DynamoDB API operations (`GetItem`, `Query`) against the DAX endpoint instead of DynamoDB directly, and DAX transparently returns a cached result on a hit or fetches from DynamoDB on a miss — you didn't write any cache-checking logic yourself. That's the practical, testable distinction: **lazy loading = you write the miss-handling code; read-through = the caching layer/service writes it for you.** Functionally, the staleness dynamics end up similar to lazy loading (a write to the underlying DB doesn't automatically update a read-through cache unless that layer also does write-through internally, as DAX does).

**Exam trap:** a question describing "the application makes the exact same call whether the data is cached or not, and the caching mechanism decides internally whether to hit the database" is read-through — if the application code visibly contains an if/else checking the cache first, that's lazy loading, even if the end behavior looks similar.

## 5. TTL-Based Expiration

Time-to-live (TTL) is not a fourth alternative to the three patterns above — it's a **complementary safety net** you attach to cache entries under any of them. Every cached item is written with an expiration time; once that time passes, the cache automatically treats the key as absent (evicts it, or refuses to serve it), forcing the next access to go back to the source of truth.

```
cache.set(productId, product, ttl=60)   # expires automatically 60 seconds after being set
```

**The core trade-off is a dial, not a binary choice:**
- **Short TTL** → data is fresher (bounded staleness window is small), but the cache hit rate drops because entries expire and get re-fetched from the database more often, increasing database load and average latency.
- **Long TTL** → higher hit rate, less database load, faster average response time, but a longer window during which the cache can silently serve stale data if the underlying record changed and nothing explicitly invalidated the entry.

TTL is especially important as a **backstop** for lazy loading and read-through: if an explicit invalidation step (`cache.delete()`) is ever missed, skipped due to a bug, or a write happens through a path that forgets to invalidate the cache, TTL guarantees the staleness can never exceed the TTL duration — it's a self-healing property that pure invalidation-on-write doesn't give you by itself.

**Exam trap:** "the application must guarantee data is never more than 30 seconds stale" is a TTL-sizing requirement (TTL ≤ 30s), not a signal to pick a specific one of the three main patterns — TTL questions are usually really asking you to reason about the hit-rate/staleness trade-off, not to name a pattern.

## 6. Cache Invalidation Strategies

There's an old, widely quoted line in software engineering: *"There are only two hard things in Computer Science: cache invalidation and naming things."* The reason invalidation is hard isn't the mechanics of deleting a key — it's coordinating **when** to do it correctly across every code path that can change the underlying data, and doing so without creating new problems (like a "thundering herd" of simultaneous cache misses hammering the database right after a popular key is invalidated, or invalidating too aggressively and destroying your hit rate).

The invalidation strategies you'll see combined on the exam:
- **Explicit delete/update on write** — the active approach used in lazy loading (`cache.delete()`) and write-through (`cache.set()` with the new value). Precise and immediate, but only as reliable as every write path remembering to do it — a write that bypasses your application code (a manual DB update, a second service writing to the same table) will *not* trigger it, leaving a silently stale cache.
- **TTL expiration** — the passive approach from Section 5. Reliable and self-healing regardless of *how* the data changed, but only bounds staleness to the TTL window rather than eliminating it.
- **Event-driven invalidation** — a variant worth recognizing: a write triggers an event (e.g., a DynamoDB Stream or an EventBridge event) that an asynchronous consumer uses to invalidate or refresh the cache, decoupling the invalidation from the write path itself. Useful when multiple services/paths can change the same underlying data and you want one central place responsible for keeping the cache honest.

In practice, production systems combine at least two of these — explicit invalidation for the common case, with a TTL as insurance against the paths that forget.

## 7. Comparing the Four Strategies

| | Lazy Loading (Cache-Aside) | Write-Through | Read-Through | TTL-Based Expiration |
|---|---|---|---|---|
| **Who writes the miss-handling logic** | Application code | N/A (writes handled explicitly; reads are simple gets) | Caching layer/service, transparently | N/A — a modifier applied to entries in any strategy |
| **Consistency behavior** | Stale/absent after a write until next read repopulates it | Always fresh immediately after a write | Similar to lazy loading unless the layer also does write-through internally (e.g., DAX) | Bounded staleness — guaranteed fresh again after TTL elapses, regardless of writes |
| **Latency on a cache miss** | Higher — DB read + cache write happen inline on the request path | N/A for reads once written; a never-written key still misses | Higher — same DB round trip, just hidden inside the cache client | Same as whichever underlying strategy it's layered on |
| **Staleness risk** | Moderate — depends on invalidation reliability and time between write and next read | Low — cache mirrors every write | Moderate — same dynamics as lazy loading unless the layer writes through | Low, and *bounded* — worst case is exactly one TTL duration |
| **Implementation complexity** | Low–moderate; all logic lives in your application | Moderate; every write path must touch two systems and handle partial failure | Low for your app code, but you depend on the caching layer supporting it (e.g., DAX) | Very low to add, but genuinely hard to *tune* correctly |
| **Cache pollution risk** | Low — only data that's actually been read gets cached | Higher — every write populates the cache, even data that's never read again | Low — same as lazy loading | N/A |

**How the exam tends to phrase the differentiator:** "data is only cached after being requested" → lazy loading. "the cache is updated as part of every write, before it's ever read" → write-through. "the application code doesn't contain cache-miss handling logic" → read-through. "the requirement is a maximum staleness window measured in seconds/minutes" → a TTL-sizing question.

## 8. Caching Content Based on Request Headers

This is a Domain 4 favorite and a genuine production security risk, not just a trivia point. Both CloudFront and API Gateway can cache full HTTP responses, and by default they compute a **cache key** — the set of request attributes used to decide whether two requests are "the same" and can share a cached response — from just the request URL (path + optionally query string). Headers are typically **excluded from the cache key by default.**

That default becomes dangerous the moment your origin returns different content for the same URL depending on a header:
- **`Accept-Language`** — if your origin returns a French response to one user and an English response to another, both for `GET /home`, and the CDN's cache key doesn't include `Accept-Language`, the CDN will cache whichever language response it saw first and serve it to *every* subsequent visitor regardless of their own language header, until that entry expires. Fix: explicitly add `Accept-Language` to the cache policy's header allowlist so it becomes part of the cache key — now French and English requests are cached separately.
- **`Authorization` (or any per-user/session-identifying header)** — this is the security-critical version of the same bug. If your origin returns *personalized* content based on the caller's identity (a dashboard, an account page) and a CDN or API Gateway cache is sitting in front of it with `Authorization` excluded from the cache key, the CDN can serve **User A's personalized response to User B**, because from the cache's point of view they both requested the identical URL. This has caused real, disclosed incidents in the industry.

**The correct fixes, and how the exam frames them:**
- Include the differentiating header (or cookie, or query string) in the **cache key** so responses that vary by that header are cached separately — appropriate when the number of distinct values is small and reasonable to cache separately (like a handful of languages).
- Mark personalized responses as **not cacheable at all** — `Cache-Control: private, no-store` (or `no-cache`) from the origin — appropriate for per-user data where caching any version of it to share across users is never correct.
- On API Gateway specifically, per-stage caching lets you define the cache key from a combination of path and query string parameters, and you must explicitly configure which parameters participate in the key; API Gateway also lets you require IAM authorization to invalidate the cache manually, preventing a malicious caller from flushing it at will.

**Exam trap:** "users are intermittently seeing another user's account data on a cached page" is *always* this bug — a personalized response was cached with a cache key that didn't vary by identity. The fix is cache-key scope or `Cache-Control: private`, never "add more cache nodes" or "increase the TTL."

## 9. CDN-Level Caching (CloudFront Cache Behaviors)

CloudFront caching is a distinct layer above application/database caching — it caches full HTTP responses at edge locations physically close to end users, which means a cache hit at the edge never even reaches your origin (EC2, ALB, S3, API Gateway), cutting both latency and origin load dramatically.

Key configuration concepts:
- **Cache behaviors** — a CloudFront distribution can define multiple path-pattern-based behaviors (e.g., `/api/*` vs `/images/*`), each with its own origin, TTL settings, and cache policy — similar in spirit to ALB's path-based routing, but for caching rules instead of backend routing.
- **TTL settings** — CloudFront lets you configure a minimum, maximum, and default TTL per cache behavior. If the origin sends `Cache-Control` or `Expires` headers, CloudFront respects them within the min/max bounds you've set; if the origin sends nothing, the default TTL applies.
- **Cache policy (the cache key)** — explicitly defines which of the following participate in the cache key: query strings (all, none, or an allowlist), headers (none by default, or an allowlist — this is where `Accept-Language` gets added per Section 8), and cookies (none, all, or an allowlist). Anything **not** included in the cache key is not used to distinguish cached responses from each other, but can still be forwarded to the origin via a separate **origin request policy** if the origin needs it for the *first* (cache-miss) request even though it shouldn't fragment the cache.
- **Invalidations** — you can explicitly invalidate (evict) cached paths in CloudFront (e.g., after a deployment), though frequent invalidations are billed and slower than just relying on short TTLs for content that changes often.

**Exam trap:** a scenario where "static assets served through CloudFront aren't updating after a deployment even though the origin was updated" is almost always a **TTL/invalidation** issue (the old response is still within its TTL at the edge) — the fix is either an explicit invalidation of that path or versioned file names (e.g., `app.a1b2c3.js`) so each deployment naturally has a unique, uncached URL, which is the AWS-preferred long-term fix over repeated manual invalidations.

## 10. DAX — DynamoDB-Specific Caching

DAX (DynamoDB Accelerator) is a fully managed, **in-memory read-through/write-through cache purpose-built for DynamoDB**, tying directly back to module 03. Its defining trait versus building your own ElastiCache-based cache-aside layer: DAX is **API-compatible** with the DynamoDB SDK — you point your existing `GetItem`/`Query`/`PutItem` calls at a DAX cluster endpoint instead of DynamoDB directly, and DAX handles the caching transparently with **little to no application code change**.

Key facts:
- Delivers **microsecond** read latency for cached responses, versus DynamoDB's typical single-digit-millisecond latency — a meaningful jump for read-heavy, latency-sensitive workloads (leaderboards, product catalogs, session lookups).
- Runs as a **cluster** — AWS recommends a minimum of three nodes across multiple AZs for high availability, with one primary and read replicas.
- Caches **both** item-level results (`GetItem`) and query/scan results, each with independently configurable TTLs.
- Writes go through DAX to DynamoDB and DAX updates its own cache accordingly (write-through behavior for the write path), but DAX's main value is accelerating **reads** — it does not make writes to DynamoDB itself faster.
- Distinct from **ElastiCache** (Redis/Memcached): ElastiCache is general-purpose — it can sit in front of *any* backend (RDS, DynamoDB, a custom API, computed results) but you must write the cache-aside or write-through logic yourself. DAX is DynamoDB-specific, drop-in, and read-through by design.

**Exam trap:** "minimal code changes" + "DynamoDB" together in a requirement is the signature phrase pointing to DAX over a hand-rolled ElastiCache layer — if the scenario instead needs to cache results from multiple different data sources or wants full control over cache key structure, that points back to ElastiCache.

## 11. Concurrency Concepts

**Lambda concurrency (recap from module 04, now applied to performance):**
- **Unreserved (account-level) concurrency** — the shared pool every function without its own reservation draws from, capped account-wide (default 1,000 concurrent executions per Region, raisable via support request).
- **Reserved concurrency** — carves out a guaranteed maximum (and, since it's reserved, also a *ceiling*) of concurrent executions for one specific function, both protecting it from being starved by other functions AND protecting the rest of the account from one runaway function consuming the whole shared pool. Setting it to 0 effectively throttles a function to zero (a documented technique for an emergency "kill switch").
- **Provisioned concurrency** — pre-initializes a set number of execution environments so they're warm and ready, eliminating cold-start latency for that many concurrent invocations, at a continuous cost (you pay for provisioned capacity whether it's invoked or not) — this is a **performance/latency** optimization, distinct from reserved concurrency's **capacity-limiting/isolation** purpose. A scenario needing predictable low p99 latency for a user-facing API points to provisioned concurrency; a scenario needing to cap or guarantee a function's blast radius points to reserved concurrency.

**Connection pool sizing:** a subtler but heavily tested consequence of Lambda's concurrency model. Each concurrent Lambda execution environment that opens its own database connection (to RDS, for example) is a *separate* connection from the database's point of view. A traffic spike that drives Lambda to hundreds or thousands of concurrent executions can open that many simultaneous DB connections and exhaust the database's `max_connections` limit almost instantly — something that never happens with a small, fixed EC2 fleet holding a stable, small connection pool. Mitigations the exam expects you to recognize:
- **Amazon RDS Proxy** — sits between Lambda and RDS/Aurora, pooling and multiplexing many Lambda-side "connections" over a much smaller number of actual database connections, which is the AWS-preferred fix for this exact problem.
- **Reserved concurrency** on the Lambda function, to put a hard ceiling on how many concurrent executions (and therefore potential connections) can exist at once.
- Initializing the DB connection **outside the handler function**, in the global/init scope, so a warm execution environment reuses its existing connection across invocations instead of opening a new one every time (this reduces connection *churn*, but doesn't by itself cap the total number of connections during a genuine concurrency spike — RDS Proxy or reserved concurrency address the ceiling itself).

## 12. Profiling Application Performance

Before you can fix a slow application, you need to identify **which resource is actually the bottleneck** — throwing more of the wrong resource at a problem (more memory at an I/O-bound app, more CPU at a network-bound app) wastes money and doesn't fix the symptom. The exam expects you to classify a described symptom into one of three buckets:

| Bottleneck type | Typical symptoms | Typical fix |
|---|---|---|
| **CPU-bound** | High CPU utilization correlating with request latency; latency scales with computational complexity of the request | More compute (larger instance/Lambda memory, which also scales proportional vCPU), algorithmic optimization, offloading heavy work to async/batch processing |
| **Memory-bound** | Out-of-memory errors, swapping (EC2), Lambda hitting its configured memory ceiling, degraded performance from excessive garbage collection | Increase allocated memory, use more memory-efficient data structures/streaming instead of loading entire datasets into memory, paginate large result sets |
| **I/O-bound** | Low CPU utilization but slow overall response; time is spent waiting on network calls, disk reads, or database queries | Caching (this entire module), connection pooling, parallelizing/async I/O calls, read replicas, moving hot data closer (CDN) |

**Tools that surface which bucket you're in:**
- **Amazon CloudWatch** metrics — `CPUUtilization`, `MemoryUtilization` (via the CloudWatch agent on EC2, or natively for containers), and for Lambda specifically: `Duration`, `Init Duration` (cold start cost), `ConcurrentExecutions`, and `Throttles`.
- **AWS X-Ray** — distributed tracing that produces a service map and a timing breakdown per request, showing exactly which downstream call (a specific DB query, a specific service hop) is consuming the bulk of the request's latency — the go-to tool when the bottleneck spans multiple services and you don't yet know which hop is slow.
- **Amazon CodeGuru Profiler** — code-level, in-production profiling that identifies the specific functions/lines consuming the most CPU time or causing the most latency, without needing a synthetic load test — useful when the bottleneck is inside your own code rather than an external dependency.

**Exam trap:** "CPU utilization is low but response times are high" always points to I/O-bound (waiting on something external), never to a CPU or memory fix — this exact phrasing shows up as a distractor-eliminator on multiple questions.

## 13. Right-Sizing Memory/Compute for Cost-Efficient Performance

It's tempting to assume "pick the smallest memory/instance size that technically works" is always the cost-optimal answer. For Lambda specifically, that assumption is often wrong, because of how Lambda prices and allocates resources: **Lambda allocates CPU power proportional to the memory setting you configure**, and you're billed for `duration × configured memory`, not duration alone. Under-provisioning memory can make a function run so much slower (because it also has less CPU) that the *total* cost (longer duration × even the smaller memory) ends up **higher** than a more generously provisioned, faster-finishing configuration.

This is the concept behind **AWS Lambda Power Tuning** (an open-source tool built as a Step Functions state machine): it invokes your function repeatedly across a range of memory settings, measures actual duration and cost at each level, and produces a cost-vs-duration curve so you can pick the genuinely optimal point — which is frequently *not* the minimum memory setting, and sometimes not even the setting with the lowest raw duration (you may deliberately trade a bit of latency for a meaningfully lower cost, or vice versa, depending on the workload's priority).

The same right-sizing mindset applies to EC2/ECS: use CloudWatch utilization metrics (and tools like Compute Optimizer) to find the smallest instance/task size that keeps utilization in a healthy range under real load, rather than guessing — oversized resources waste money, undersized resources create the CPU/memory bottlenecks described in Section 12.

**Exam trap:** "reduce Lambda memory to the minimum possible to cut costs" is a trap distractor whenever the scenario also cares about performance — the exam wants you to recognize that memory and duration are linked, and that the actually cost-optimal setting has to be *measured* (e.g., with Power Tuning), not assumed to be the floor.

## 14. Worked Real-World Scenarios

**Scenario A — the lazy-loaded product catalog with a stale-price incident.** An e-commerce team puts ElastiCache for Redis in front of their RDS product catalog using lazy loading: `getProduct` checks the cache first, falls back to RDS and populates the cache on a miss, with a 10-minute TTL. A pricing team updates a product's price directly in RDS through an internal admin tool that bypasses the main application's `updateProduct` code path entirely — so the `cache.delete()` invalidation step never runs. For up to 10 minutes (the TTL), customers see the old price, because nothing ever told the cache the data changed; the cache only self-corrects once the TTL naturally expires. **Lesson:** lazy loading's invalidation step only works if *every* write path goes through it — an out-of-band write (a manual DB edit, a second service, a migration script) will silently produce stale reads until TTL expiry, which is exactly why TTL is treated as a backstop, not an optional extra, in Section 5 and 6.

**Scenario B — DAX instead of hand-rolled caching for a viral leaderboard.** A gaming company's DynamoDB-backed leaderboard table experiences a 50x read spike during a viral event, driving up both latency and DynamoDB read costs. One engineer proposes standing up an ElastiCache cluster and writing cache-aside logic around every leaderboard read. Instead, the team adopts DAX: they point the existing DynamoDB SDK client at the DAX cluster endpoint, and because DAX is API-compatible, almost no application code changes — the same `GetItem`/`Query` calls now transparently hit an in-memory, microsecond-latency cache with automatic read-through and write-through behavior. **Lesson:** when the requirement is specifically "cache DynamoDB reads with minimal code change," DAX is the purpose-built answer over a general-purpose ElastiCache cache-aside implementation, which would need to be built and maintained by hand for no added benefit in this single-data-source scenario.

**Scenario C — the CloudFront cache-key security incident.** A SaaS company puts CloudFront in front of their API Gateway-backed dashboard API to reduce latency for a globally distributed user base. The origin returns each user's personalized dashboard data based on the caller's `Authorization` bearer token, but the CloudFront cache policy was configured with the default cache key (URL path only, no headers). Within hours, support tickets report users seeing *other* customers' dashboard data. Root cause: because `Authorization` wasn't part of the cache key, CloudFront treated every request to `GET /dashboard` as identical regardless of who made it, cached the first response it saw, and served that same cached (personalized!) response to every subsequent caller until the entry's TTL expired. **Fix:** the team marks the dashboard response `Cache-Control: private, no-store` at the origin so CloudFront never caches it at all — the correct choice here, since dashboard content is fully personalized per user and caching any single version of it to share is never valid, unlike the `Accept-Language` case where including the header in the cache key (rather than disabling caching entirely) is the right fix because there are only a handful of legitimate cacheable variants.

## Key exam traps from this module

- Lazy loading = application code contains the cache-miss branch; read-through = the caching layer/service contains it, transparently (DAX is the canonical read-through example).
- Write-through updates cache and DB together on every write (always fresh, higher write latency); lazy loading only updates the DB on a write and invalidates the cache, leaving a stale/absent window until the next read.
- TTL is a complementary safety net under any strategy, not a fourth standalone pattern — exam questions about "maximum staleness in seconds" are TTL-sizing questions, not pattern-selection questions.
- "Users see another user's cached data" is always a cache-key-doesn't-vary-by-identity bug — fix with `Cache-Control: private` or by adding the identifying header/cookie to the cache key, never by adjusting TTL or adding cache nodes.
- `Accept-Language` (and similar legitimately-multi-valued headers) belongs in the cache key (cache separately per value); `Authorization` and other per-user headers usually belong *out* of caching entirely.
- DAX = DynamoDB-specific, API-compatible, minimal code change, read-through by design. ElastiCache = general-purpose, any backend, you write the pattern yourself.
- Reserved concurrency limits/guarantees a function's concurrency ceiling (capacity isolation); provisioned concurrency pre-warms environments to kill cold starts (latency optimization) — different problems, don't swap them.
- A Lambda-to-RDS connection-exhaustion scenario under high concurrency points to RDS Proxy, not just "increase max_connections."
- "Low CPU utilization but high latency" = I/O-bound, not a CPU or memory problem.
- The cost-optimal Lambda memory setting is rarely the minimum allowed — it must be measured (e.g., via Lambda Power Tuning), because CPU scales with memory and total cost is duration × memory, not memory alone.
