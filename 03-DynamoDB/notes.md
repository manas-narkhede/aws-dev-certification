# Module 03 — DynamoDB

Domain focus: almost entirely **Development with AWS Services (32%)**, mapping directly onto Domain 1 Task Statement 3 ("Use data stores in application development"). DynamoDB is one of the single most heavily tested services on DVA-C02 — beyond the questions that ask about it directly, it shows up constantly as the backing store in Lambda/API Gateway scenario questions in later modules. Get this module genuinely solid; it pays off repeatedly.

## 1. Relational vs. non-relational — why DynamoDB exists

A relational database (module 08: RDS, Aurora) stores data in fixed-schema tables with rows and columns, enforces relationships via foreign keys, and guarantees full **ACID** transactions (Atomicity, Consistency, Isolation, Durability) across arbitrary joins. That power costs you: schema changes are disruptive, joins get expensive as data grows, and scaling *write* throughput horizontally across many nodes is hard — the classic answer is "buy a bigger box" (vertical scaling) or add read replicas (which only helps reads).

DynamoDB is a fully managed, serverless **NoSQL key-value and document database**. It trades relational features (no joins, no arbitrary ad-hoc queries, limited transaction scope) for near-unlimited horizontal scalability, single-digit-millisecond latency at any scale, and zero server management — AWS handles partitioning, replication, and patching entirely. The schema is flexible: only the primary key attributes are declared up front; every item can otherwise carry a different set of attributes.

**The exam's mental model:** if a scenario needs complex joins, multi-table ad-hoc queries, or strict relational integrity across many entities → RDS/Aurora. If a scenario needs massive, predictable-pattern read/write throughput, low and consistent latency at any scale, and you already know your access patterns up front → DynamoDB. "Access patterns known in advance" is the tell — with DynamoDB you design the table *around how you'll query it*, not around normalized entity relationships.

## 2. Core building blocks: tables, items, attributes

- **Table** — a collection of items (roughly: a "table" in the loose sense, not a relational one).
- **Item** — a single record (like a row), uniquely identified by its primary key. Maximum item size is **400 KB**, including attribute names and values.
- **Attribute** — a name-value pair on an item (like a column), but items in the same table don't need matching attributes beyond the required primary key fields — this is the "schema-less" part.

Supported data types: scalars (`String`, `Number`, `Binary`, `Boolean`, `Null`), document types (`List`, `Map` — nested JSON-like structures), and set types (`String Set`, `Number Set`, `Binary Set` — unordered, unique values).

```json
{
  "orderId": {"S": "ORD-4471"},
  "customerId": {"S": "CUST-9981"},
  "status": {"S": "SHIPPED"},
  "items": {"L": [{"M": {"sku": {"S": "A100"}, "qty": {"N": "2"}}}]},
  "totalCents": {"N": "5499"}
}
```
That's the raw, wire-level attribute-value JSON format the DynamoDB API actually speaks. Application code almost never builds this by hand — see §15 on serialization.

## 3. Primary keys: simple vs. composite

Every table needs exactly one primary key, chosen at creation and immutable afterward:

- **Simple primary key** — just a **partition key**. Every item's partition key value must be unique in the table (it behaves like a traditional unique ID column).
- **Composite primary key** — a **partition key + sort key**. The *combination* must be unique, but many items can share the same partition key, differentiated by their sort key. This is the far more common real-world design — e.g., partition key `customerId`, sort key `orderDate`, letting you store every order for a customer under one partition key and retrieve them ordered by date.

Internally, DynamoDB runs the partition key value through an internal hash function to decide which physical storage partition the item lives on. Items sharing a partition key are always co-located and sorted by sort key on that partition — which is exactly what makes range queries against a composite key fast (§6, Query).

## 4. High-cardinality partition keys and avoiding hot partitions

This is one of the most frequently tested DynamoDB concepts on DVA-C02, and it's the one beginners most often get backwards.

DynamoDB divides a table's total provisioned (or on-demand) throughput across its physical partitions based on the **distribution of partition key values actually being read/written**. If your access pattern hammers a small number of partition key values — or worse, uses a **low-cardinality** attribute (one with only a handful of distinct values, like `status` with values `PENDING`/`SHIPPED`/`DELIVERED`) as the partition key — all that traffic lands on one or a few physical partitions. Those partitions throttle (`ProvisionedThroughputExceededException`) even though the table's *aggregate* provisioned capacity looks more than sufficient on a dashboard. This is the **hot partition** problem.

**The fix is a high-cardinality partition key** — an attribute with many distinct values, spreading reads and writes evenly across the underlying partitions. A well-designed table uses something like `userId`, `deviceId`, or `orderId` as the partition key (many distinct values, roughly even access frequency) rather than a coarse categorical attribute.

When you genuinely need to query *by* a low-cardinality attribute (like "give me all orders with status = SHIPPED"), the right tool is a **Global Secondary Index** on that attribute (§5) — not making it your base table's partition key.

**Write sharding** is the escape hatch when even a naturally high-cardinality key still has a single "hot" value you can't avoid (e.g., one celebrity user's `userId` gets disproportionate traffic). The pattern: append a random or calculated suffix to the partition key at write time (`userId#1`, `userId#2`, ... `userId#9`), spreading that one logical entity's items across several physical partitions; on read, fan out across all the suffix values and merge results in application code.

**Exam trap:** a question describing throttling on a table with "plenty" of provisioned capacity, where the workload skews heavily toward a small set of key values, is almost always testing hot-partition recognition — the fix is a better-chosen (higher-cardinality) partition key or write sharding, **not** simply raising provisioned throughput further.

## 5. Secondary indexes: GSI vs. LSI

Base-table queries only work efficiently against the primary key. To query efficiently by other attributes, you add a secondary index.

| | Local Secondary Index (LSI) | Global Secondary Index (GSI) |
|---|---|---|
| Partition key | Same as base table | Can be a different attribute |
| Sort key | Different attribute than base table's sort key | Can be any attribute (or none) |
| When created | Only at table creation time — cannot add/remove later | Anytime, including after the table exists |
| Throughput | Shares the base table's provisioned RCU/WCU | Has its own provisioned RCU/WCU (or scales independently under on-demand) |
| Consistency | Supports both eventually and **strongly** consistent reads | **Eventually consistent reads only** |
| Limit per table | Max 5 | Max 20 (default quota, raisable) |
| Size constraint | All items for one partition key value (base table + all LSIs combined) capped at 10 GB | No such per-partition-key cap |

**Mental shortcut:** LSI = "same partition key, different sort order, locked in at creation." GSI = "essentially a separate, differently-keyed index table that DynamoDB maintains asynchronously for you" — far more flexible, and the one you reach for by default. Because a GSI is propagated asynchronously from the base table, it can only ever be eventually consistent — there's a small replication lag between a base-table write and that write showing up in the GSI.

**Exam trap:** "the team needs to add a new query pattern to a table that's already been live in production for a year" → must be a GSI (LSIs can only be defined at table creation). "The requirement explicitly needs a strongly consistent read on the alternate key" → must be an LSI (GSIs can't do it).

## 6. Query vs. Scan

- **Query** — requires a partition key value (equality only) and optionally a sort key condition (`=`, `<`, `>`, `BETWEEN`, `begins_with`, etc.). Extremely efficient: DynamoDB goes straight to the relevant partition and reads a contiguous, sorted range. You can further narrow results with a `FilterExpression`, but note it's applied **after** the matching items are read and RCUs are already consumed — a filter reduces what's *returned*, not what's *read* (and billed).
- **Scan** — reads **every item in the table (or index)**, then optionally applies a filter. This is expensive at scale: it consumes read capacity for the entire table regardless of how selective the filter is, and gets slower as the table grows. `Limit`, pagination, and **parallel scan** (splitting the scan across multiple workers using `Segment`/`TotalSegments`) can make a necessary scan less painful, but none of them turn it into a cheap operation.

**Rule of thumb the exam wants:** design your table's keys and indexes so that every real access pattern can be satisfied with `Query`. `Scan` is acceptable for occasional full-table analytics/export jobs, not for a hot path in a request-serving application. A question describing "slow, expensive reads that get worse as the table grows" on a table lacking a matching index is a Scan-vs-Query diagnosis almost every time.

## 7. Capacity modes: On-Demand vs. Provisioned (+ Auto Scaling)

Throughput is measured in:
- **RCU (Read Capacity Unit)** — 1 strongly consistent read/sec of an item up to 4 KB (or 2 eventually consistent reads/sec of the same size — eventually consistent reads are half the cost).
- **WCU (Write Capacity Unit)** — 1 write/sec of an item up to 1 KB (transactional writes cost double, §10).

| | Provisioned | On-Demand |
|---|---|---|
| Setup | You specify RCU/WCU ahead of time | No capacity planning — scales instantly to traffic |
| Cost model | Pay for what's provisioned, whether used or not | Pay per request actually made |
| Best for | Steady, predictable traffic you can forecast | Spiky, unpredictable, or new/unknown workloads |
| Scaling | Manual, or automatic via **Application Auto Scaling** (define a target utilization % and min/max RCU/WCU bounds; it adjusts provisioned capacity to track the target) | Automatic and instant, no configuration |
| Overrun behavior | Throttling (`ProvisionedThroughputExceededException`) if traffic exceeds provisioned capacity and auto scaling hasn't caught up yet | Scales to absorb spikes; extreme, sudden spikes can still briefly throttle if they exceed DynamoDB's internal scale-up ability |

You can switch between the two modes, but only **once per 24 hours**. The SDK's default retry/backoff behavior helps absorb brief throttling in provisioned mode while auto scaling reacts — but it isn't a substitute for correctly-provisioned capacity or a well-distributed key design.

**Exam trap:** "unpredictable/spiky new application, team has no historical traffic data to forecast capacity" → On-Demand. "Stable, well-understood, cost-sensitive steady-state traffic" → Provisioned with Auto Scaling, generally cheaper per unit at scale.

## 8. Consistency models

DynamoDB replicates each item across multiple Availability Zones within a Region for durability. That replication isn't instantaneous, which is why you choose per-read:

| | Eventually consistent read | Strongly consistent read |
|---|---|---|
| Default? | Yes | No — must set `ConsistentRead: true` |
| Might return stale data | Yes, for a very short window (typically sub-second) after a write | No — always reflects all writes that completed before the read began |
| RCU cost | 1 RCU per 4 KB | 2 RCU per 4 KB (double) |
| Latency | Slightly lower | Slightly higher |
| Available on GSIs? | Yes | **No — GSIs only ever support eventually consistent reads** |

**Exam trap:** a scenario needing "read-your-writes" correctness immediately after a write (e.g., a user submits a form and the next screen must show the just-saved value) needs `ConsistentRead: true` on the base table — and if that read pattern happens to require a GSI, the correct fix is redesigning to query the base table (or an LSI) instead, since a GSI structurally cannot give you strong consistency.

## 9. DynamoDB Streams

A **Stream** is an ordered, time-ordered log of item-level changes (insert, modify, remove) on a table, retained for **24 hours**. Enable it with one of four `StreamViewType` settings controlling what each change record captures: `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, or `NEW_AND_OLD_IMAGES` (both before and after states — the most commonly used, since it lets consuming code diff a change).

The overwhelmingly common integration is a **Lambda event source mapping**: Lambda polls the stream and invokes your function with a batch of change records whenever new ones appear — this is DynamoDB's change-data-capture (CDC) mechanism. Typical uses:
- Replicating changes into another table, a search index (e.g. OpenSearch), or a data warehouse.
- Maintaining a derived aggregate or materialized view (e.g., incrementing a running total whenever an order item is inserted).
- Fanning changes out to other systems via SNS/EventBridge for downstream event-driven processing.
- Cross-Region replication (this is, in fact, how DynamoDB Global Tables work under the hood).

**Exam trap:** "capture every change to a table and trigger downstream processing without polling the table yourself" is a Streams + Lambda question nearly every time it appears. Don't confuse Streams (change events, 24-hour retention, item-level deltas) with TTL-triggered deletes (§13) — TTL deletions *do* appear in a stream, but the stream itself isn't the deletion mechanism.

## 10. Transactions: TransactWriteItems / TransactGetItems

DynamoDB supports ACID transactions across **up to 100 items (or 4 MB), spanning multiple tables** within the same account and Region:

- **`TransactWriteItems`** — an all-or-nothing batch of up to 100 `Put`/`Update`/`Delete`/`ConditionCheck` actions. Either every action succeeds, or none of them apply — no partial writes.
- **`TransactGetItems`** — an atomic, consistent snapshot read across multiple items/tables at once.

Transactional operations cost **double** the RCU/WCU of the equivalent non-transactional call, reflecting the extra coordination work.

Use transactions when an operation must maintain an invariant across more than one item — e.g., transferring funds (debit account A, credit account B, both-or-neither), or decrementing inventory while creating an order record atomically. `ConditionCheck` actions let you include a condition on an item *without writing to it*, useful for enforcing invariants that live on a different item than the one being written.

**Exam trap:** don't reach for `TransactWriteItems` for a single-item conditional update — that's a plain conditional `PutItem`/`UpdateItem` (§12) at half the cost. Transactions are for **multi-item, cross-table atomicity**.

## 11. DAX (DynamoDB Accelerator)

DAX is a fully managed, **in-memory cache** that sits in front of DynamoDB, purpose-built for it — not a general-purpose cache like ElastiCache (module 09 covers that comparison in depth). Key properties:

- **API-compatible** with the DynamoDB SDK — pointing existing application code at a DAX cluster instead of DynamoDB directly typically requires changing only the client/endpoint construction, not your Get/Put/Query calls.
- Delivers **microsecond** read latency (vs. single-digit-millisecond for DynamoDB itself) for cache hits.
- **Write-through**: writes go to DynamoDB through DAX, and DAX's item cache is updated as part of that write.
- Caches both individual item lookups (item cache) and the results of `Query`/`Scan` calls (query cache), each with a configurable TTL.
- Deployed as a cluster with a primary node and optional read replicas across AZs for high availability and read scaling.

**When the exam wants DAX:** a read-heavy application needing microsecond-level response times, with an acceptable tolerance for briefly-stale cached reads (it's an eventually-consistent cache layer — don't reach for DAX when a requirement demands strong read-your-writes consistency on every single read). Not a fit for write-heavy workloads (DAX doesn't meaningfully speed up writes) or as a substitute for Streams-based CDC.

## 12. Conditional writes and optimistic locking

A `ConditionExpression` on `PutItem`, `UpdateItem`, or `DeleteItem` makes the write succeed **only if** the condition evaluates true against the item's *current* state; otherwise it fails with a `ConditionalCheckFailedException` and nothing is written. This is how DynamoDB enforces invariants without needing a separate locking mechanism.

Two extremely common patterns:
- **Insert-only / prevent overwrite:** `ConditionExpression: "attribute_not_exists(orderId)"` on a `PutItem` — guarantees you never silently clobber an existing item.
- **Optimistic locking via a version attribute:** every item carries a `version` number; an update's condition expression requires `version = :expectedVersion`, and the update itself increments `version`. If two clients read the same item and both try to update it, only the first write succeeds — the second fails the condition check (its `:expectedVersion` is now stale) and the client must re-read and retry. AWS's `DynamoDBMapper` (Java SDK) has a built-in `@DynamoDBVersionAttribute` for exactly this pattern; other SDKs implement it manually with an explicit `ConditionExpression`.

DynamoDB has no native **pessimistic** locking (no "lock this row until I'm done" primitive) — optimistic locking (detect-and-retry on conflict) is the idiomatic approach, which fits its high-concurrency, horizontally-scaled design.

**Exam trap:** "prevent two concurrent requests from both successfully applying the same update, without heavy application-side locking infrastructure" → conditional writes with a version attribute, not a distributed lock service.

## 13. TTL (Time to Live)

TTL lets you designate one attribute (storing a Unix epoch timestamp) as the item's expiration marker. Once that time passes, DynamoDB automatically deletes the item in the background — typically within 48 hours of expiration — **at no additional write-capacity cost**. TTL deletions do show up in DynamoDB Streams (if enabled), distinguishable from application-driven deletes by an identity marker showing DynamoDB itself performed the deletion, which is handy if downstream processing needs to react differently to expired-and-purged data versus explicit user deletes.

Typical uses: session tokens, temporary cache-like rows, event/log records that only need to live for a defined retention window, expiring promotional codes. This is DynamoDB's main built-in answer to "manage a data lifecycle without a scheduled cleanup job."

**Exam trap:** TTL deletion isn't instantaneous — a scenario demanding items disappear from *queries* at the exact expiration second still needs an application-level filter on the expiry attribute; TTL is a background reaper for storage/cost hygiene, not a real-time query-time guarantee.

## 14. DynamoDB Local and SAM for local testing

**DynamoDB Local** is a downloadable (JAR or Docker image) implementation of the DynamoDB API that runs entirely on your machine — no AWS account calls, no cost, no network dependency. It's used for local development and automated tests so you're not hitting a real table (and its real cost/throughput limits) on every test run. AWS SAM CLI supports spinning up Lambda functions locally alongside a DynamoDB Local container for realistic offline integration testing of an event-driven, DynamoDB-backed application before deploying anything to AWS.

**Exam trap:** if a question emphasizes fast, free, offline iteration during development/CI without touching real AWS resources, DynamoDB Local (not a low-provisioned real table) is the intended answer.

## 15. CRUD and batch operations via the SDK

The core single-item operations: `GetItem`, `PutItem` (full item replace), `UpdateItem` (partial, in-place attribute update — generally preferred over `PutItem` when you only need to change a few attributes, since it avoids re-sending/overwriting the whole item), `DeleteItem`, plus `Query` and `Scan` (§6).

Batch operations trade a little flexibility for fewer round trips:
- **`BatchGetItem`** — up to 100 items / 16 MB across up to 100 tables in one call. Still consumes capacity per item as if requested individually; a partial failure returns `UnprocessedKeys` that the client must retry (with backoff).
- **`BatchWriteItem`** — up to 25 put/delete requests / 16 MB per call. No partial `UpdateItem` support in a batch (only whole-item put or delete). Partial failures return `UnprocessedItems`, again requiring retry.

**Serialization matters in practice:** application objects (a Python dict, a Java POJO, a JS object) aren't the wire-format attribute-value JSON shown in §2 — the SDK's document client / marshaller handles converting your native objects to/from that format. In Python, `boto3.resource("dynamodb")` (the higher-level resource client) does this transparently; the lower-level `boto3.client("dynamodb")` requires you to build/parse attribute-value dictionaries by hand. Java's `DynamoDBMapper` and the AWS SDK for JavaScript's `DynamoDBDocumentClient` play the same role. This "serializing/deserializing for persistence" step is exactly what those higher-level clients exist to hide.

```python
import boto3
table = boto3.resource("dynamodb").Table("Orders")

# PutItem
table.put_item(Item={"orderId": "ORD-4471", "customerId": "CUST-9981", "status": "PENDING"})

# UpdateItem with a condition (optimistic locking pattern)
table.update_item(
    Key={"orderId": "ORD-4471"},
    UpdateExpression="SET #s = :new, version = version + :inc",
    ConditionExpression="version = :expected",
    ExpressionAttributeNames={"#s": "status"},
    ExpressionAttributeValues={":new": "SHIPPED", ":expected": 3, ":inc": 1},
)

# Query — partition key required, sort key optional
resp = table.query(
    KeyConditionExpression="customerId = :c AND orderDate > :d",
    ExpressionAttributeValues={":c": "CUST-9981", ":d": "2026-01-01"},
)
```

## 16. Fine-grained access control: `dynamodb:LeadingKeys`

This ties directly back to module 00's IAM policy JSON. DynamoDB supports an IAM policy `Condition` key, `dynamodb:LeadingKeys`, that restricts a caller to only reading/writing items whose **partition key** matches a specific value — commonly a policy variable resolved from the caller's identity, such as `${cognito-identity.amazonaws.com:sub}` (the authenticated Cognito identity pool user's ID). Combined with a Cognito identity pool issuing temporary, per-user IAM credentials, this lets you enforce **row-level, per-user data isolation directly at the IAM layer** — a mobile or web client can only ever see its own rows, with no server-side authorization code required to check "does this row belong to this user."

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:Query"],
    "Resource": "arn:aws:dynamodb:us-east-1:111122223333:table/UserProfiles",
    "Condition": {
      "ForAllValues:StringEquals": {
        "dynamodb:LeadingKeys": ["${cognito-identity.amazonaws.com:sub}"]
      }
    }
  }]
}
```

**Exam trap:** a scenario asking for "each mobile app user to access only their own items, without building custom server-side authorization logic" is a `dynamodb:LeadingKeys` + Cognito identity pool question — the table's partition key must actually be (or be prefixed by) the user identifier for this to work at all, which is one more reason partition key design (§3–4) matters from day one.

## 17. Ephemeral vs. persistent storage, in DynamoDB's context

DynamoDB itself is always a **persistent** data store — every successful write is durably replicated across multiple AZs before being acknowledged. Where "ephemeral vs. persistent" bites on DynamoDB-adjacent exam questions: DAX (§11) is an in-memory, **ephemeral** cache layer sitting in front of the persistent DynamoDB table underneath it — losing/restarting a DAX node doesn't lose data, because DynamoDB remains the durable source of truth. The same pattern recurs elsewhere in this course (module 01's instance store vs. EBS, module 09's ElastiCache vs. RDS): a fast, volatile cache layer in front of a slower, durable system-of-record. Recognizing which role a given service is playing in a scenario — "cache in front of" vs. "the actual persistent store" — is a recurring exam skill, not a DynamoDB-specific one.

## 18. Worked real-world scenarios

**Scenario A — the flash-sale hot partition.** An e-commerce company's `Orders` table uses `orderStatus` (values: `PENDING`, `SHIPPED`, `DELIVERED`, `CANCELLED`) as the partition key, because early on it seemed convenient for a dashboard query that groups orders by status. During a flash sale, write throughput spikes and the table starts throwing `ProvisionedThroughputExceededException` — even though CloudWatch shows the table's aggregate provisioned WCU is nowhere near its limit. The root cause: nearly every new order lands in the `PENDING` partition, because `orderStatus` is a low-cardinality attribute with only four possible values — all that write traffic concentrates onto one physical partition regardless of how much *total* capacity is provisioned. The fix: redesign the base table around a high-cardinality key (`orderId` as partition key), and add a **GSI** with `orderStatus` as its partition key to serve the "all orders in status X" dashboard query the original design was trying to optimize for. This is the single most common hot-partition pattern the exam tests.

**Scenario B — GSI vs. LSI for a messaging app.** A chat application stores messages with `conversationId` (partition key) and `sentAt` (sort key) on the base table, supporting "get all messages in a conversation, in order" efficiently via `Query`. Product now wants a new screen: "show me all messages a specific user has ever sent, across every conversation, most recent first." That's a completely different partition key (`senderId` instead of `conversationId`), and the feature is being added to a table that's already live in production with data. An LSI is disqualified immediately — LSIs can only be defined at table creation, and this table already exists with real data. The answer is a **GSI** with `senderId` as its partition key and `sentAt` as its sort key, added to the live table without disrupting existing traffic, accepting that reads against it will be eventually consistent (acceptable here — a "message history" screen doesn't need read-your-writes strictness the way a payment confirmation would).

**Scenario C — per-user row isolation without server-side auth code.** A mobile app lets each authenticated user store personal notes. The team wants users to only ever be able to read or write their own notes, and wants to avoid hand-writing "does `note.userId == currentUser.id`" checks in every single API handler — that logic is easy to forget in a new endpoint and represents a real security risk if missed. The design: a Cognito identity pool authenticates users and vends temporary IAM credentials scoped by a role with a `dynamodb:LeadingKeys` condition tying access to `${cognito-identity.amazonaws.com:sub}`, against a `Notes` table whose partition key is the user's Cognito identity ID. The mobile app's SDK calls hit DynamoDB directly with those temporary credentials; IAM itself refuses any `Query`/`GetItem`/`PutItem` attempting to touch a partition key that isn't the caller's own identity — enforcement moves from "application code that could have a bug" to "the IAM policy engine, which cannot be bypassed by a missed `if` statement."

## Comparison: DynamoDB vs. RDS at a glance (full depth in module 08)

| | DynamoDB | RDS (relational) |
|---|---|---|
| Schema | Flexible (only key attributes fixed) | Fixed, enforced |
| Scaling | Horizontal, near-limitless, managed automatically | Vertical primarily; read replicas for read scaling |
| Query flexibility | Access patterns must be designed for up front; no joins | Arbitrary SQL joins/aggregations |
| Consistency | Tunable per-read (eventual/strong); transactions available but scoped | Full ACID by default across the whole dataset |
| Latency at scale | Consistently single-digit ms regardless of table size | Can degrade as data/joins grow without tuning |
| Ops overhead | Fully serverless (with on-demand mode) | You manage instance sizing, patching windows (unless Aurora Serverless) |

## Key exam traps from this module
- Low-cardinality partition keys cause hot partitions and throttling even when aggregate table capacity looks sufficient — fix with a high-cardinality key or write sharding, not more provisioned capacity.
- LSIs must be created at table creation and can't be added later; GSIs can be added anytime but are eventually-consistent only.
- `Query` requires a partition key and is efficient; `Scan` reads the whole table and gets more expensive as it grows — filters reduce what's returned, not what's read/billed.
- Strongly consistent reads cost 2x the RCU of eventually consistent reads and are never available on a GSI.
- On-Demand capacity mode suits unpredictable/spiky/new workloads; Provisioned (+ Auto Scaling) suits steady, forecastable ones and is generally cheaper at scale.
- `TransactWriteItems`/`TransactGetItems` are for multi-item, cross-table atomicity at double the capacity cost — not a substitute for a simple single-item conditional write.
- Conditional writes with a version attribute implement optimistic locking; DynamoDB has no native pessimistic locking.
- TTL deletion is background/eventual (up to ~48 hours after expiry), not an instant, query-time guarantee.
- DAX accelerates reads (microsecond latency, write-through, eventually-consistent cache) — it does not meaningfully speed up writes and is not a CDC mechanism.
- DynamoDB Streams + Lambda is the standard change-data-capture pattern; retention is only 24 hours.
- `dynamodb:LeadingKeys` in an IAM condition enforces per-user row-level access at the identity layer, typically paired with a Cognito identity pool — and only works if the partition key design actually matches the identity being restricted.
- DynamoDB Local is the free, offline, no-AWS-account way to develop/test against the DynamoDB API before deploying.
