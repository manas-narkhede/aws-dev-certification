# Module 08 — Relational & In-Memory Databases

Domain focus: primarily **Development with AWS Services (32%)** — knowing how an application actually talks to a relational database or a cache — with a substantial slice of **Security (26%)**, since "how do you securely hand a Lambda function or an EC2 app a database password" is one of the most heavily tested patterns on DVA-C02 (it's the subject of an official AWS sample question). This module assumes modules 00–07, especially module 03's DynamoDB coverage — you'll need it for the relational-vs-NoSQL decision table near the end.

## 1. Amazon RDS: the managed relational database

RDS (Relational Database Service) is AWS's managed offering for running a standard relational (SQL) engine without you patching the OS, installing the database software, or building your own backup tooling. You still design your schema, write your queries, and tune your application — AWS manages the underlying host, storage layer, patching cadence (during a maintenance window you configure), and automated backups.

### Supported engines
RDS supports five traditional engines, each launched as a `DBInstance`:

| Engine | Notes |
|---|---|
| MySQL | Open-source, widely used, free to run (you pay AWS infra costs only) |
| PostgreSQL | Open-source, feature-rich, popular default choice for new relational workloads |
| MariaDB | MySQL-compatible fork, open-source |
| Oracle | Commercial, License Included or Bring-Your-Own-License (BYOL) pricing models |
| SQL Server | Commercial (Microsoft), also License Included or BYOL |

(Amazon Aurora is technically launched through the RDS API too, but it's architecturally different enough that AWS — and this module — treat it separately in section 2.)

**Exam trap:** if a scenario mentions per-core/per-socket licensing audits or "bring your own license," that's a purchasing/compliance detail — it doesn't change which *purchasing option* you'd reach for on EC2 (Dedicated Hosts, module 01); on RDS, License Included vs BYOL is simply a billing model choice for Oracle/SQL Server, not a security or architecture decision.

### What you configure vs. what AWS manages
You choose: engine + version, instance class (`db.t3.medium`, `db.r6g.large`, etc. — same family logic as EC2), storage type and size, VPC/subnet group, security groups, backup retention, and maintenance windows. AWS manages: underlying host provisioning, OS-level patching, automated backup execution, and (if you enable Multi-AZ) synchronous replication and failover orchestration.

### Storage
RDS storage behaves similarly to EBS conceptually: **gp3** (general purpose SSD, the modern default — IOPS/throughput provisionable independently of size) for most workloads, and **io1/io2** (Provisioned IOPS SSD) for demanding, latency-sensitive database workloads that need consistent high IOPS regardless of burst behavior. RDS also supports **Storage Auto Scaling**, which automatically increases allocated storage when free space drops below a threshold, without you manually resizing the volume or taking downtime.

### Parameter groups and option groups
Two distinct configuration mechanisms, and the exam likes to test the difference:
- **DB parameter groups**: control engine configuration parameters (e.g., `max_connections`, `slow_query_log`, character set defaults). Apply to any engine.
- **DB option groups**: enable specific *engine features* that require additional configuration, most relevant to Oracle and SQL Server (e.g., Oracle Enterprise Manager, SQL Server Transparent Data Encryption via an option). Not every engine uses option groups the same way — MySQL/PostgreSQL rarely need them; Oracle/SQL Server frequently do.

**Exam trap:** "I need to change a database engine setting like `max_connections`" → parameter group. "I need to enable a bundled engine feature like TDE" → option group. Mixing these up is a common wrong-answer bait.

### Encryption at rest
Enabled at creation time using AWS KMS. **You cannot directly enable encryption on an already-running, unencrypted RDS instance** — the standard path is: take a snapshot → copy the snapshot with encryption enabled → restore a new instance from the encrypted copy. This "snapshot, copy encrypted, restore" sequence is a frequently tested workaround pattern.

## 2. Multi-AZ vs. Read Replicas — the single most important RDS distinction on this exam

These solve **completely different problems**, and confusing them is the exam's favorite RDS trap.

| | Multi-AZ (DB instance) | Read Replicas |
|---|---|---|
| Purpose | High availability / disaster recovery | Read scaling (offload read traffic) |
| Replication | **Synchronous** to a standby in a different AZ | **Asynchronous** |
| Standby/replica readable? | No — the standby is not directly readable in a standard Multi-AZ DB instance | Yes — replicas serve read-only queries |
| Failover | Automatic; RDS flips the DNS endpoint to the standby on primary failure | Not automatic; a replica can be manually *promoted* to a standalone writable instance |
| Region scope | Same Region (different AZ) | Can be same-Region **or cross-Region** |
| Consistency | Strong (synchronous) | Eventual — replica lag exists, monitor `ReplicaLag` in CloudWatch |

**The core exam trap the scope explicitly calls out:** Multi-AZ is for *availability*, not for scaling reads. If a question says "reduce read load on the primary" or "offload reporting queries," the answer is a **Read Replica**, never "enable Multi-AZ." If a question says "survive an AZ outage with automatic failover and zero data loss," the answer is **Multi-AZ**, never "add a read replica" (a replica's asynchronous lag means it *can* lose the last few transactions, and promotion isn't automatic).

You can combine both: a Multi-AZ primary with one or more Read Replicas (replicas can themselves optionally be Multi-AZ) is a common production pattern — HA for the primary, horizontal read scaling via replicas.

## 3. Backups and snapshots

| | Automated Backups | Manual Snapshots |
|---|---|---|
| Trigger | Daily backup + continuous transaction log capture | User-initiated |
| Retention | 1–35 days (you configure); enables **point-in-time recovery (PITR)** to any second within that window | Persist until you explicitly delete them |
| Lifecycle | Deleted when the DB instance is deleted, unless you opt to retain final snapshot | Independent of instance lifecycle |
| Storage | S3 (incremental, like EBS snapshots) | S3 |

**Exam trap:** PITR restores create a **new** DB instance with a new endpoint — you don't restore "in place." This mirrors EBS snapshot restore behavior from module 01 and trips people expecting the original endpoint to just start working again.

## 4. Secure database connections: the pattern this exam tests hardest

This is directly the subject of an official AWS sample question, and it's worth internalizing the *exact* mechanism, not just the vocabulary.

### The wrong pattern (what the exam wants you to reject)
Storing a plaintext username/password in source code, in an AMI, or in unencrypted EC2 user data. All of these are static, long-lived, hard to rotate, and easy to leak (e.g., via `git log`, via the EC2 `DescribeInstanceAttribute` API for user data, or via a compromised host).

### Pattern A: IAM database authentication (token-based)
Available for RDS MySQL and PostgreSQL (and Aurora MySQL/PostgreSQL). Instead of a static password, the application authenticates using a **short-lived authentication token** generated from IAM credentials:

```
# Conceptual flow, e.g. via AWS CLI or SDK
1. The app's IAM role/user must have an IAM policy allowing rds-db:connect
   for the specific DB resource ARN and DB user.
2. The app (or a helper) calls the token-generation API:
     aws rds generate-db-auth-token \
       --hostname mydb.xxxxxxx.us-east-1.rds.amazonaws.com \
       --port 3306 \
       --username app_iam_user \
       --region us-east-1
   -> returns a signed token string, valid for 15 minutes
3. The app connects to the DB over SSL/TLS, using that token
   in place of a password.
4. Before the token expires, the app requests a new one — no
   permanent secret is ever stored anywhere.
```

Key properties: tokens are valid for **15 minutes**, connections must use SSL/TLS, and the DB user must be mapped to allow `AWSAuthenticationPlugin` (MySQL) or the `rds_iam` role (PostgreSQL). This eliminates a stored, static password entirely — auth is derived from IAM, which you already control with policies, roles, and (module 01) instance profiles.

**Exam trap:** IAM database authentication is not supported by every engine (notably not by default for SQL Server or Oracle) — know it as a MySQL/PostgreSQL/Aurora-MySQL/Aurora-PostgreSQL capability.

### Pattern B: Secrets Manager with automatic rotation
This is the pattern from the official sample question you should be able to answer cold: *"A company needs to securely store and automatically rotate database credentials for an RDS for MySQL instance."* Answer: **Secrets Manager, with rotation configured.**

```
# Conceptual application-side pattern
1. App has an IAM role permitting secretsmanager:GetSecretValue
   for the specific secret ARN (least privilege).
2. At runtime (on connect, or cached with a short TTL), the app calls:
     secret = secretsmanager.get_secret_value(SecretId="prod/orders-db")
     conn = connect(host=secret["host"], user=secret["username"],
                     password=secret["password"], dbname=secret["dbname"])
3. Secrets Manager rotates the credential on a schedule (e.g., every 30 days)
   using an AWS-provided Lambda rotation function template for RDS —
   it updates the password in the database AND the secret value,
   in a coordinated two-step process, with zero application code changes.
4. The app simply fetches the current secret value on its next connection;
   no manual credential distribution, no restart required.
```

Secrets Manager (unlike Parameter Store, module 01) has this rotation built in natively for RDS, Aurora, Redshift, and DocumentDB via ready-made Lambda rotation templates. This is *the* reason the exam prefers Secrets Manager over Parameter Store whenever automatic credential rotation is a stated requirement.

**Exam trap:** Parameter Store SecureString can *store* a secret encrypted with KMS, but it has **no native automatic rotation** — you'd have to build your own Lambda + EventBridge schedule to rotate it yourself. If the requirement explicitly says "automatically rotate," Secrets Manager is the answer unless the question is artificially constraining you away from it.

## 5. RDS Proxy — solving the "too many connections" problem

This is a frequently tested, specific scenario: **a Lambda function connecting to RDS/Aurora, invoked at high concurrency.** Each concurrent Lambda invocation can open its own new database connection. Relational databases have a hard cap on `max_connections` (often in the low thousands or less) — at high concurrency, Lambda can exhaust that limit, causing connection errors for every client, including non-Lambda ones.

**RDS Proxy** is a fully managed, highly available connection pooler that sits between your application (typically Lambda, but also usable from EC2/ECS) and your RDS or Aurora database:
- **Pools and multiplexes connections**: many application-side connections share a much smaller pool of actual database connections, absorbing bursts of concurrent Lambda invocations without overwhelming the DB.
- **Reduces failover time**: RDS Proxy can cut failover time for Aurora/RDS Multi-AZ events significantly (AWS cites up to ~66% faster) because the proxy maintains the connection pool and reroutes without every client needing to re-resolve DNS and reconnect from scratch.
- **Credential handling**: RDS Proxy integrates with Secrets Manager (or IAM authentication) for the actual DB credentials — your application authenticates to the proxy, and the proxy manages the real backend credentials, so app code doesn't need direct access to the DB password at all.
- **Requires**: the proxy and the Lambda function (or other client) need network reachability — typically the same VPC (or VPC peering/reachable networking) as the RDS/Aurora instance. Enforces TLS.
- **Supported engines**: MySQL, PostgreSQL, MariaDB, and Aurora (MySQL- and PostgreSQL-compatible).

**Exam trap:** whenever a scenario says "a Lambda function intermittently fails to connect to RDS with 'too many connections' errors under high concurrency," the answer is **RDS Proxy** — not "increase `max_connections`" (a band-aid with a hard ceiling) and not "switch to Provisioned Concurrency" (that controls Lambda cold starts, not DB connection exhaustion — a classic decoy).

## 6. Amazon Aurora

Aurora is AWS's cloud-native, MySQL-compatible and PostgreSQL-compatible relational database, built on a distributed, self-healing storage architecture that's decoupled from compute.

### Storage architecture
Aurora's storage layer automatically replicates data **six ways across three Availability Zones** and grows in increments as needed, up to very large sizes (many terabytes) — you never manually provision or resize Aurora storage the way you do for standard RDS gp3/io1 volumes. This underlying shared storage volume is also what makes Aurora Replicas fundamentally different from RDS Read Replicas (see below).

### Aurora Replicas
Because Aurora Replicas share the *same underlying storage volume* as the writer instance (rather than receiving an asynchronously-shipped copy of the data like RDS Read Replicas), replica lag is typically very low — commonly single-digit milliseconds. Aurora supports up to 15 replicas, and — critically — **Aurora Replicas can serve as automatic failover targets**: if the writer fails, Aurora promotes a replica to writer in seconds, with no data loss, because the storage was already shared. This is faster and safer than standard RDS Multi-AZ failover for equivalent engines, and it's a major reason Aurora is generally the preferred choice over "plain" RDS for the same engine when performance, scaling, or fast failover matter.

### Aurora Serverless v2
Auto-scales database capacity (measured in **Aurora Capacity Units, ACUs**) up and down **automatically and near-instantly** in response to load, without you managing fixed instance sizes. Ideal for variable, intermittent, or hard-to-predict workloads — e.g., a dev/test database that's idle most of the day, a new product with unknown traffic patterns, or a multi-tenant SaaS database per customer where usage varies wildly. Serverless v2 instances can coexist with regular provisioned Aurora instances in the same cluster (e.g., a provisioned writer plus serverless readers, or vice versa).

### Aurora Global Database
For **cross-Region** requirements — disaster recovery across Regions or serving read traffic with low latency close to a global user base. One primary Region handles writes; up to several (commonly cited: up to 5, though AWS has raised limits over time) secondary Regions receive data via dedicated storage-based replication infrastructure (not standard database engine replication), typically with **under 1 second** of replication lag. In a regional outage, a secondary Region can be promoted to take over write traffic in about a minute — far faster than rebuilding a database in a new Region from backups.

### RDS vs. Aurora
| | RDS (MySQL/PostgreSQL/etc.) | Aurora |
|---|---|---|
| Storage | You provision/manage EBS-backed storage (gp3/io1) | Auto-scaling, distributed storage (6-way replication, 3 AZs) — no manual provisioning |
| Read scaling | Read Replicas (async, higher lag, up to 5 for most engines) | Aurora Replicas (near-sync via shared storage, up to 15, low lag) |
| Failover | Multi-AZ standby, typically ~60–120 seconds | Replica promotion, typically well under 30 seconds, no data loss |
| Cross-Region | Cross-Region Read Replicas | Aurora Global Database (purpose-built, faster, sub-second lag) |
| Serverless option | No native serverless mode | Aurora Serverless v2 |
| Cost model | Generally lower baseline cost for small/simple workloads | Typically higher baseline cost, but better price-performance at scale |
| Engine compatibility | Native engine (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server) | MySQL-compatible or PostgreSQL-compatible only |

**Rule of thumb the exam rewards:** if a scenario needs Oracle or SQL Server, or the simplest/cheapest option for a small, low-traffic relational workload, RDS is fine. If the scenario emphasizes performance at scale, minimal storage management, fast failover, many read replicas, or cross-Region reads with low replication lag — and the engine is MySQL or PostgreSQL — **Aurora is the preferred answer.**

### Aurora Standard (provisioned) vs. Aurora Serverless v2
| | Aurora Provisioned | Aurora Serverless v2 |
|---|---|---|
| Capacity | Fixed instance classes you choose and resize manually | Auto-scales in fine-grained ACU increments based on load |
| Best for | Steady, predictable, well-understood workloads | Variable, intermittent, unpredictable, or spiky workloads |
| Scaling speed | Manual instance class change (brief interruption) | Seconds, automatic, no manual intervention |
| Mixing | Can run alongside Serverless v2 instances in the same cluster | Can run alongside provisioned instances in the same cluster |

## 7. Amazon ElastiCache

ElastiCache is a fully managed **in-memory data store used as a cache** (or, for Redis specifically, sometimes as a lightweight primary store for ephemeral data) sitting in front of a slower backing database to absorb read load and cut latency from milliseconds down to sub-millisecond/microsecond territory.

### Redis vs. Memcached
| | Redis | Memcached |
|---|---|---|
| Data structures | Rich: strings, lists, sets, sorted sets, hashes, streams | Simple key-value strings only |
| Persistence | Yes — RDB snapshots and/or AOF (append-only file) | No — purely in-memory, data lost on node failure/restart |
| Replication / HA | Yes — Multi-AZ with automatic failover (primary/replica) | No native replication or HA |
| Pub/Sub messaging | Yes | No |
| Transactions | Yes (MULTI/EXEC) | No |
| Threading model | Historically single-threaded per node for command execution (newer versions add I/O multithreading); scale via sharding (cluster mode) | Multi-threaded — can use multiple cores on a single node natively |
| Typical use cases | Session store, leaderboards (sorted sets), pub/sub, rate limiting, real-time analytics | Simple, high-throughput object cache with no durability/HA requirement, needing to fully use multi-core nodes |

**Exam trap:** "Needs a leaderboard with ranked scores" or "needs pub/sub messaging" or "needs replication/automatic failover for the cache tier" → **Redis**, every time — Memcached simply doesn't have these features. "Wants the simplest possible cache, doesn't care about persistence or HA, wants to fully utilize multiple cores per node" → Memcached is a legitimate, if narrower, answer.

### Cache-aside (lazy-loading) pattern
The most common caching strategy tested on this exam — the application, not the database, owns the caching logic:

```
function get_user_profile(user_id):
    cached = redis.get("user:" + user_id)
    if cached is not None:
        return cached                     # cache hit — fast path

    data = rds.query("SELECT * FROM users WHERE id = ?", user_id)  # cache miss
    redis.set("user:" + user_id, data, ttl_seconds=300)            # populate cache
    return data
```

Reads check the cache first; on a miss, fall through to the database and populate the cache for next time, typically with a TTL so stale data eventually expires. Writes usually go directly to the database, and the corresponding cache entry is either invalidated (deleted) or updated at write time so subsequent reads don't serve stale data — a design detail worth getting right if a scenario stresses data-freshness requirements.

### Cluster mode
- **Cluster mode disabled**: a single shard with one primary and up to 5 read replicas — simpler, but writes are capped by a single node's capacity.
- **Cluster mode enabled**: data is partitioned (sharded) across multiple shards, each with its own primary and optional replicas — enables horizontal scaling of both reads *and writes* beyond a single node's limits. This is the Redis-only answer to "we need to scale write throughput beyond one node."

## 8. Amazon MemoryDB for Redis — a durable primary database, not "just a cache"

This is the distinction the exam wants crystal clear: **ElastiCache (including ElastiCache for Redis) is a cache** — even Redis's optional persistence (AOF) is best-effort and not designed to make ElastiCache your system of record. **MemoryDB for Redis is different: it is Redis-API-compatible but architected as a durable, Multi-AZ primary database**, not a cache sitting in front of one.

MemoryDB achieves durability via a distributed transactional log that persists data across multiple Availability Zones, so data survives node failures without needing a separate backing database at all. It still delivers in-memory-class performance — microsecond reads, single-digit-millisecond writes — but it's positioned for use cases where you need Redis's speed and data structures **and** you need that data to be durable and authoritative, not just a disposable performance layer in front of RDS/Aurora.

| | ElastiCache (Redis/Memcached) | MemoryDB for Redis |
|---|---|---|
| Role | Cache in front of another data store | Durable primary data store in its own right |
| Durability | Best-effort at most (Redis AOF/snapshots); not a source of truth | Durable via distributed transactional log across multiple AZs |
| Typical pattern | Cache-aside in front of RDS/Aurora/DynamoDB | Used directly as the application's database for latency-critical data |
| Data loss risk on failure | Possible (cache is disposable/rebuildable) | Designed to avoid data loss — it's meant to *be* the durable copy |

**Exam trap:** if a scenario says "needs Redis-compatible performance **and** the data must not be lost, and this store **is** the application's database" (not a cache in front of something else) → **MemoryDB for Redis**. If the scenario says "cache in front of our relational/NoSQL database to reduce read load," even if it emphasizes needing Redis features like sorted sets or pub/sub → **ElastiCache for Redis**.

## 9. Relational database vs. DynamoDB — the recurring decision (ties back to module 03)

This decision recurs constantly on DVA-C02: given a scenario, is the right data store RDS/Aurora or DynamoDB?

| Signal in the scenario | Favors |
|---|---|
| Complex multi-table JOINs, ad-hoc reporting queries, existing SQL-based application/tooling | Relational (RDS/Aurora) |
| Multi-statement ACID transactions across several related tables | Relational (RDS/Aurora) — though DynamoDB does support transactions across up to 100 items/25 items per call depending on API, they're not a substitute for arbitrary relational JOIN-heavy transactional logic |
| Fixed, well-understood schema that changes rarely | Either fits, but relational tooling (migrations, ORMs) is more mature here |
| Access pattern is simple and known in advance (e.g., "get all orders for this customer ID"), extremely high scale, need for single-digit-millisecond latency at massive throughput | DynamoDB (module 03) |
| Need for a fully serverless, zero-capacity-planning data store that scales automatically with unpredictable, bursty traffic | DynamoDB |
| Flexible/evolving schema, wide variation in item attributes | DynamoDB |
| Team explicitly wants to avoid managing connections, instance sizing, or Multi-AZ/replica topology | DynamoDB |

**Rule of thumb:** if the scenario's pain point is *relationships between data* (joins, foreign keys, complex queries) — reach for RDS/Aurora. If the pain point is *scale and access-pattern simplicity* (huge throughput, known lookups by key, serverless-first architecture) — reach for DynamoDB. A scenario combining Lambda + "unpredictable, bursty traffic" + "simple key-based lookups" is DynamoDB bait even if it never says the word "NoSQL."

## 10. Worked real-world scenarios

**Scenario A — the Lambda function that "ran out of connections."** A serverless order-processing API uses Lambda functions that each open a new connection to an Aurora MySQL database on every invocation. During a flash sale, traffic spikes to thousands of concurrent invocations, and the application starts throwing `Too many connections` errors — even though the database itself isn't CPU- or memory-constrained. The team's first instinct is to raise `max_connections` in the parameter group, which buys a little headroom but doesn't scale with demand and risks destabilizing the database at extreme concurrency. The actual fix: put **RDS Proxy** in front of the Aurora cluster. Lambda connects to the proxy instead of directly to the database; the proxy pools and multiplexes a large number of application-side connections onto a much smaller, stable set of real database connections, absorbing the burst without the database ever seeing thousands of simultaneous raw connections. **Lesson:** "many concurrent Lambda invocations, one relational database, connection exhaustion errors" is the RDS Proxy scenario, not a `max_connections` tuning problem.

**Scenario B — the credential that never needed to be looked at again.** A legacy application migrating to EC2 currently has its MySQL username and password hardcoded in source code, targeting a database the company is moving to RDS for MySQL. Security review flags this immediately: the credential is static, checked into version control history, and manually rotated (rarely, and painfully) by an engineer editing a config file and redeploying. The fix mirrors the official AWS sample question almost exactly: store the credential in **Secrets Manager**, configure **automatic rotation** using the AWS-provided Lambda rotation template for RDS, and update the application to call `GetSecretValue` at connection time via an IAM role — never a hardcoded string. Now rotation happens on a schedule with zero application code changes and zero manual password handoffs, and the IAM role's permissions (scoped to that one secret ARN) are the only thing standing between the app and the credential. **Lesson:** "automatically rotate database credentials," especially phrased close to a migration scenario, is Secrets Manager, not Parameter Store (no native rotation) and not any form of static storage.

**Scenario C — the read replica that couldn't save the day.** A company runs a single-AZ RDS PostgreSQL instance and, worried about an AZ outage, adds a same-Region Read Replica for "disaster recovery." During an actual AZ-level outage that takes down the primary, the team discovers two problems: promoting the replica is a *manual* action (not automatic), and because replication is asynchronous, a handful of the most recent transactions never made it to the replica before the primary went down — a small but real amount of data loss. The correct HA design would have been **Multi-AZ**, whose standby is kept in **synchronous** lockstep with the primary and fails over **automatically** with no data loss for committed transactions. The team ultimately adopts both: Multi-AZ for automatic, zero-data-loss failover, plus a separate Read Replica (which can itself be Multi-AZ) purely for offloading reporting queries — using each feature for the job it's actually built for. **Lesson:** Read Replicas are not a substitute for Multi-AZ, and this exact confusion (replica-as-HA-strategy) is one of the most common wrong answers on RDS questions.

## Key exam traps

- Multi-AZ = **synchronous**, automatic failover, standby **not** readable, for **availability**. Read Replicas = **asynchronous**, manual promotion, readable, for **read scaling**, and can be cross-Region. Never confuse the two.
- "Automatically rotate database credentials" → **Secrets Manager** (native rotation via Lambda templates). Parameter Store SecureString can store a secret but has **no native rotation**.
- IAM database authentication issues **15-minute tokens** derived from IAM policy (`rds-db:connect`) instead of a static password — supported on MySQL/PostgreSQL (and Aurora MySQL/PostgreSQL), not every engine.
- "Lambda + RDS/Aurora + many concurrent invocations + connection errors" → **RDS Proxy**, not a `max_connections` bump and not Lambda Provisioned Concurrency (that solves cold starts, a different problem).
- Aurora Replicas share the writer's storage volume (low lag, valid failover targets); RDS Read Replicas are asynchronous copies (higher lag, not automatic failover targets).
- Aurora Serverless v2 is for **variable/intermittent** workloads; provisioned Aurora/RDS is for **steady, predictable** workloads.
- Aurora Global Database is the cross-Region answer for Aurora specifically (sub-second lag, fast regional promotion) — don't reach for a plain cross-Region read replica when the scenario is Aurora and cross-Region DR/low-latency reads are the goal.
- Redis has replication, persistence, pub/sub, and rich data structures (sorted sets for leaderboards); Memcached has none of that but is multi-threaded and simpler — match the feature the scenario actually needs.
- **ElastiCache is a cache; MemoryDB for Redis is a durable primary database.** A scenario needing Redis-compatible speed *and* durability as the system of record points to MemoryDB, not ElastiCache.
- Relational (RDS/Aurora) wins on joins, multi-table transactions, and existing SQL tooling; DynamoDB (module 03) wins on massive scale, simple known access patterns, and serverless-first, schema-flexible design.
- Encryption at rest can't be toggled on an existing unencrypted RDS instance — it's snapshot → copy encrypted → restore.
