# Module 06 — Messaging, Streaming & Analytics

Domain focus: mostly **Development with AWS Services (32%)** — you're expected to write code that publishes to and consumes from these services — with a meaningful slice of **Troubleshooting and Optimization (18%)**, specifically Domain 4 Task Statement 3's "optimize messaging with SQS/SNS filter policies." This module builds directly on module 04's "loosely coupled, event-driven architecture" theme: SQS, SNS, EventBridge, and Kinesis are the four services that actually *implement* that decoupling between producers and consumers. If module 04 was "why decouple," this module is "with what, exactly."

## 1. Amazon SQS — Simple Queue Service

SQS is a fully managed **message queue**. A producer sends a message to a queue; one or more consumers poll the queue, process a message, and delete it when done. The queue is the buffer between producer and consumer — neither has to know about the other, neither has to be online at the same time, and a burst of producer traffic doesn't overwhelm a slower consumer because the queue absorbs the spike. This is the concrete mechanism behind the "loosely coupled" architecture you saw conceptually in module 04: instead of a Lambda function or EC2 app calling a downstream service directly (tight coupling — if the downstream is slow or down, the caller fails too), it drops a message on a queue and moves on.

### Standard vs. FIFO queues

| | Standard Queue | FIFO Queue |
|---|---|---|
| Ordering | Best-effort, **not guaranteed** | Strict, guaranteed order within a message group |
| Delivery | **At-least-once** — a message can be delivered more than once | **Exactly-once processing** within a 5-minute deduplication window |
| Throughput | Nearly unlimited | Up to 3,000 msg/sec with batching (300/sec without), per API action |
| Naming | Any queue name | Queue name **must** end in `.fifo` |
| Deduplication | None built in — consumer must handle duplicates | Content-based dedup (SHA-256 hash of body) or explicit `MessageDeduplicationId` |
| Use case | Decoupling at scale where strict order doesn't matter (image processing, generic task queue) | Order-sensitive workloads (financial transactions, sequential commands to a single resource) |

**Exam trap:** "Standard queue = exactly-once" is a common wrong assumption baked into distractor options — Standard is **at-least-once**, meaning your consumer code must be **idempotent** (safe to process the same message twice without side effects, e.g. by checking an already-processed flag before acting). FIFO trades throughput ceiling for ordering + exactly-once — if a question says "strict order required" or "duplicate processing must never happen," the answer is FIFO; if it just says "high throughput, order doesn't matter," it's Standard.

### Visibility timeout

When a consumer polls SQS and receives a message, the message isn't deleted — it becomes **invisible** to other consumers for a configurable **visibility timeout** (default 30 seconds, max 12 hours). If the consumer finishes processing and calls `DeleteMessage` before the timeout expires, the message is gone for good. If the consumer crashes or takes too long, the timeout expires and the message becomes visible again for another consumer to pick up.

**Exam trap:** if a consumer's processing routinely takes longer than the visibility timeout, the message reappears and gets processed a **second time by a different consumer**, even though the first one is still working on it — this is the classic "why are we getting duplicate processing" root cause. The fix: either increase the visibility timeout to comfortably exceed worst-case processing time, or call `ChangeMessageVisibility` mid-processing to extend it dynamically.

### Long polling vs. short polling

- **Short polling** (default `ReceiveMessage` behavior at `WaitTimeSeconds=0`): returns immediately, even if the queue is empty, and doesn't necessarily check every server behind SQS — can return an empty response even when messages exist.
- **Long polling** (`WaitTimeSeconds` 1–20): the `ReceiveMessage` call waits up to that many seconds for a message to arrive before returning empty, and does query all servers. This **reduces the number of empty responses**, which reduces cost (you pay per request) and reduces latency to pick up a new message compared to polling short and sleeping between calls.

**Exam trap:** "reduce cost and empty responses from polling SQS" → enable long polling by setting `ReceiveMessageWaitTimeSeconds` (queue-level default) or passing `WaitTimeSeconds` per call — this is a near-guaranteed Domain 4 optimization question.

### Dead-letter queues (DLQ) and redrive policy

A DLQ is a **separate, normal SQS queue** you designate to receive messages that repeatedly fail processing. You attach a **redrive policy** to the *source* queue specifying the DLQ's ARN and a `maxReceiveCount` — after a message has been received (and its visibility timeout has expired without deletion) that many times, SQS automatically moves it to the DLQ instead of redelivering it to consumers again.

```
Producer → [Source Queue] → Consumer picks up message
                 ↑                    │ (processing fails, no delete called)
                 │                    ▼
          receiveCount++ ◄──── visibility timeout expires, message reappears
                 │
                 │  receiveCount reaches maxReceiveCount (e.g. 5)
                 ▼
           [Dead-Letter Queue]  ← message stops being redelivered to consumers
                 │
                 ▼
     Engineer inspects DLQ, fixes root cause, then
     "redrives" (moves) the message back to the source queue for reprocessing
```

DLQs exist so a single malformed/"poison pill" message can't block or endlessly loop the rest of the queue — after N failed attempts it's quarantined for manual inspection rather than retried forever. The **redrive** action (via console, CLI `start-message-move-task`, or SDK) explicitly moves messages back from a DLQ to the source queue (or a new queue) once the underlying issue is fixed.

**Exam trap:** a DLQ is **not** automatically created — you create a normal queue and wire it in as the redrive target. Also, the DLQ's `maxReceiveCount` lives on the **source** queue's redrive policy, not on the DLQ itself. Lambda functions triggered by SQS have their own separate DLQ/failure-destination concept (an "on-failure destination," which can be SQS, SNS, or EventBridge) for function-level invocation failures — don't conflate the two when a question is specifically about a Lambda event source mapping.

### Delay queues and message timers

- **Delay queue**: every message sent to the queue is invisible to consumers for a set delay (0–15 min, queue-level `DelaySeconds` default).
- **Per-message delay timer**: an individual message can override the queue default via `DelaySeconds` on `SendMessage` (not supported on FIFO queues, which use a fixed queue-level delay only).

Use case: staggering work, or implementing a simple "process this later" pattern without a separate scheduler.

### Message attributes

Metadata key-value pairs attached to a message, separate from the message body, up to 10 per message (structured, typed as String/Number/Binary). Used for routing/filtering decisions and for passing metadata a consumer needs without parsing the body — and, critically, this is the same mechanism SNS filter policies match against when SQS is subscribed to an SNS topic (see §2).

### SQS as buffer/decoupling — tying back to module 04

Recall module 04's Lambda material: Lambda has **event source mappings** for SQS, where Lambda's poller reads batches off the queue and invokes your function — this is how "SQS → Lambda" actually works under the hood (Lambda does the long-polling for you). SQS is the textbook answer whenever a scenario says a fast producer (e.g., a web tier accepting file upload requests) needs to **not be blocked** by a slower downstream processor (e.g., a video transcoding job), or whenever multiple producers need to safely write into one processing pipeline without direct coupling or a thundering-herd problem hitting the consumer.

## 2. Amazon SNS — Simple Notification Service

SNS is a fully managed **pub/sub (publish/subscribe)** messaging service built around **topics**. A publisher sends one message to a topic; SNS **fans that single message out** to every subscriber of the topic, in parallel, without the publisher knowing or caring who (or how many) subscribers exist.

### Subscription types
- **Amazon SQS** — most common for durable, poll-based fanout (see below)
- **AWS Lambda** — SNS invokes the function directly, push-based
- **HTTP/HTTPS** — SNS POSTs the message to an endpoint you control
- **Email / Email-JSON** — human-readable notification
- **SMS** — text message to a phone number
- **Mobile push** — to platforms like FCM/APNs via platform application endpoints
- **Amazon Data Firehose** — stream fanout directly into a Firehose delivery stream

### The SNS + SQS fanout pattern

This is one of the single most-tested architectural patterns on the exam. Instead of one queue with one type of consumer, you put an **SQS queue between the topic and each consumer group**, so every subscriber gets its own durable, independently-scaling, independently-failing buffer:

```
                              ┌──► SQS Queue A ──► Order-Fulfillment Lambda
Publisher ──► SNS Topic  ─────┼──► SQS Queue B ──► Analytics/Data-Warehouse ingestion
 (one publish call)           └──► SQS Queue C ──► Email/notification service
```

Why not just publish straight to three SQS queues yourself? Because SNS handles the fanout — one `Publish` call reaches every subscribed queue simultaneously, new consumers can subscribe later without touching the publisher's code, and each SQS queue gives its consumer the durability, retry, visibility-timeout, and DLQ behavior of a normal queue (which raw SNS delivery to Lambda/HTTP alone doesn't give you — an HTTP subscriber that's down could simply lose messages without a queue buffering them). This is the standard way to combine SNS's fanout strength with SQS's durability/buffering strength.

### Message filtering with subscription filter policies

Without filtering, every subscriber to a topic gets **every** message published to it — wasteful if a subscriber only cares about a subset. A **filter policy** is a JSON document attached to a specific *subscription* (not the topic) that tells SNS to only deliver messages whose **message attributes** match the policy.

```json
{
  "event_type": ["order_shipped", "order_cancelled"],
  "region": [{"anything-but": "test-region"}],
  "order_value": [{"numeric": [">=", 100]}]
}
```

If a publisher sends a message with attribute `event_type = "order_created"`, this subscription simply never receives it — SNS filters it out before delivery, at no cost/traffic to the subscriber's queue or function. This is exactly why the exam (Domain 4.3, "optimize messaging") cares about filter policies: **without filtering, every consumer receives and must discard irrelevant messages itself, burning Lambda invocations / SQS polling cycles / processing cost on messages it immediately throws away. Filtering moves that waste out of the consumer and into SNS, which discards non-matching messages for free before delivery** — this is a direct cost and traffic optimization, not just a convenience feature.

**Exam trap:** filter policies match against **message attributes**, not the message body, by default (message-body filtering exists too but is the less-tested, newer variant — know that attribute-based filtering is the classic mechanism). Also, the filter policy lives on the **subscription**, so the same topic can have three subscribers each getting a different filtered slice of the same published stream.

## 3. Amazon EventBridge

EventBridge is AWS's managed **event bus** service — think of it as SNS's more structured, more feature-rich sibling, purpose-built for routing **structured JSON events** (not arbitrary messages) based on their **content**, with native integrations across dozens of AWS services and SaaS partners.

### Event buses
- **Default event bus** — every account has one automatically; receives events from ~200+ AWS services natively (e.g., an EC2 state-change event, a CodePipeline stage change) with zero setup.
- **Custom event bus** — you create one for your own application's custom events, isolating them from the noisy default bus.
- **Partner event bus** — receives events directly from an integrated SaaS partner (e.g., Zendesk, Datadog) without you writing a webhook receiver.

### Rules and event patterns
A **rule** attached to a bus defines an **event pattern** (JSON that matches against incoming event structure/content) and one or more **targets** (Lambda, SQS, SNS, Step Functions, Kinesis, another event bus, and 20+ other target types) to invoke when an event matches.

```json
{
  "source": ["myapp.orders"],
  "detail-type": ["OrderStateChange"],
  "detail": {
    "state": ["CANCELLED"],
    "amount": [{"numeric": [">", 500]}]
  }
}
```

### Scheduled rules
A rule can trigger on a **schedule** instead of (or as well as) an event pattern, using either:
- **`rate()` expression** — e.g. `rate(5 minutes)`, `rate(1 day)`
- **`cron()` expression** — e.g. `cron(0 12 * * ? *)` = every day at 12:00 UTC, for exact calendar-based timing

This is the modern replacement for "run a Lambda function every night at 2 AM" — an EventBridge scheduled rule targeting that Lambda function, no separate cron server needed. (AWS also now offers **EventBridge Scheduler** as a dedicated, higher-scale scheduling capability, but rule-based scheduling on the default bus remains the classic, most commonly tested pattern.)

### Archive & replay
EventBridge can **archive** events matching a pattern on a bus (with a retention period you set, or indefinite) and later **replay** them back onto a bus within a specified time window — useful for reprocessing after a downstream bug is fixed, or for testing, without needing the original producer to resend anything.

### EventBridge Pipes (brief)
**Pipes** connect a specific point-to-point source (e.g., an SQS queue, a DynamoDB stream, a Kinesis stream) directly to a specific target, with optional filtering and an optional enrichment step (a Lambda/Step Functions/API Destination call to transform the payload) in between — without needing a full rule/bus setup. Think of it as a simpler, more directly wired alternative to "source → EventBridge bus → rule → target" when you have exactly one source and one target and want built-in filtering/transformation without extra glue code.

### EventBridge vs. SNS vs. SQS — the decision framework

| | SQS | SNS | EventBridge |
|---|---|---|---|
| Model | Point-to-point queue (pull) | Pub/sub topic (push fanout) | Event bus with content-based routing (push) |
| Consumers | One logical consumer group polls/drains the queue | Multiple subscribers, every one gets every message (unless filtered) | Multiple rules match on structured event content, route to different targets |
| Filtering | None built-in (consumer filters itself) | Subscription filter policies (attribute-based) | Rich event pattern matching directly on the JSON event body |
| Source variety | Your own producers only | Your own publishers only | 200+ AWS services natively, SaaS partners, plus your own custom events |
| Durability model | Messages persist in the queue until consumed/expired | No built-in durability for HTTP/Lambda subscribers unless backed by SQS | Not a durable buffer by itself — rules fire and route; use archive/replay or a downstream SQS target for durability |
| Best for | Decoupling a producer from a slower consumer; buffering/backpressure; work queues | Simple fanout to multiple heterogeneous subscriber types (email/SMS/Lambda/SQS) from your own app | Routing many different structured event types, from many different sources (including other AWS services), to many different targets based on content, especially SaaS/AWS-service integration and scheduling |

**Rule of thumb the exam wants**: if the scenario is "one producer, need a durable buffer so a slow consumer doesn't block it" → **SQS**. If it's "one event needs to reach several different subscriber types simultaneously" → **SNS** (often **SNS+SQS fanout** if durability matters per-subscriber). If it's "route events based on their content/type from many different sources (including native AWS service events or SaaS), or on a schedule" → **EventBridge**.

## 4. Amazon Kinesis family — streaming data

Kinesis handles **continuous, high-throughput streaming data** — this is a fundamentally different shape of problem from SQS's "discrete task queue." The classic exam signal: **need multiple independent consumers to read the *same* data, need to replay/re-read historical data, or need real-time analytics on a continuous stream** → Kinesis. **Need a simple decoupled task queue, one logical consumer group, no replay needed** → SQS.

### Kinesis Data Streams
- **Shards** — the base throughput unit of a stream. Each shard supports up to 1 MB/sec or 1,000 records/sec **write**, and up to 2 MB/sec **read** (in classic/shared-fan-out mode). You provision (or use On-Demand auto-scaling) the number of shards a stream needs for its expected volume.
- **Partition key** — chosen by the producer per record; records with the same partition key are routed to (and stay ordered within) the same shard. Choosing a good partition key (high cardinality, evenly distributed) avoids a "hot shard" that gets overloaded while others sit idle.
- **Producers** — the Kinesis Producer Library (KPL), AWS SDK `PutRecord`/`PutRecords`, or the Kinesis Agent (for tailing log files).
- **Consumers** — the Kinesis Client Library (KCL), which handles shard discovery, checkpointing (tracking how far a consumer has read), and load balancing across multiple consumer instances automatically; or a Lambda function via an event source mapping (like SQS, but Lambda reads shard iterators).
- **Retention** — default 24 hours, extendable up to 365 days — this is what enables **replay**: a new consumer, or a consumer recovering from a bug, can re-read data from any point still within the retention window, something SQS fundamentally cannot do once a message is deleted.
- **Multiple consumers**: unlike an SQS message (consumed once, then gone), the same record in a Kinesis stream can be read independently by several different consumer applications (e.g., one doing real-time fraud detection, another archiving to S3, another feeding a dashboard) — each consumer tracks its own position.

### Kinesis Data Firehose
A **fully managed delivery service** — it is not itself something you "consume from"; it automatically buffers incoming records (by size or time interval) and delivers them near-real-time to a fixed set of destinations: **S3, Redshift, OpenSearch Service**, and various HTTP/partner endpoints (Splunk, Datadog, etc.). It supports **inline data transformation via a Lambda function** you attach (e.g., converting JSON to Parquet, enriching a record, filtering bad records) before delivery. Firehose has **no shard management** — you don't provision throughput, it scales automatically — which is exactly the tradeoff: less operational control, but "least operational overhead" for the common case of "get streaming data into S3/Redshift/OpenSearch reliably."

### Kinesis Data Analytics (brief)
Runs **SQL or Apache Flink (managed)** queries directly against a Kinesis Data Stream or Firehose delivery stream in real time — e.g., computing a rolling 5-minute average or detecting anomalies as data flows through, without standing up a separate stream-processing cluster. Developer-level awareness only for DVA-C02: know it exists as the "SQL-on-a-live-stream" piece of the family, not deep implementation detail.

### Kinesis Data Streams vs. Firehose vs. Data Analytics

| | Kinesis Data Streams | Kinesis Data Firehose | Kinesis Data Analytics |
|---|---|---|---|
| What it is | Raw, low-latency streaming storage you manage shards/consumers for | Fully managed delivery pipeline to fixed destinations | Real-time SQL/Flink query engine over a stream |
| Consumers | Custom (KCL, Lambda, SDK) — you write consumer logic | None — Firehose itself delivers to the destination | Query results, which can feed another stream/Firehose |
| Latency | Near-real-time, seconds | Near-real-time, ~60 sec buffering minimum (configurable) | Real-time, continuous query |
| Replay / multiple independent readers | Yes — this is its defining strength | No — data flows through to the destination, not re-readable as a stream | N/A — it queries the source stream, doesn't store its own copy |
| Operational overhead | You manage shard count/scaling (or use On-Demand mode) | Fully managed, auto-scales, no shard management | Fully managed query runtime |
| Typical use | Custom real-time processing, multiple analytics consumers, clickstream/IoT ingestion feeding several systems | "Get this stream into S3/Redshift/OpenSearch reliably," log/clickstream archival with light transformation | Live dashboards, real-time anomaly/aggregation on a stream already in Kinesis |

### Kinesis vs. SQS — the other classic exam decision point

| Need | Answer |
|---|---|
| Strict ordered replay of the same data by multiple independent consumer applications | **Kinesis Data Streams** |
| Real-time analytics/aggregation on a continuous flow of data | **Kinesis** (Data Streams + Data Analytics, or Firehose to a destination that does the analytics) |
| Simple decoupling of a producer from one logical consumer group, work distributed once across consumers (not replayed) | **SQS** |
| Delivering streaming data continuously into S3/Redshift/OpenSearch with minimal operational effort | **Kinesis Data Firehose** |
| A task/job queue where each unit of work should be processed exactly by one worker, not broadcast/replayed | **SQS** |

## 5. Amazon Athena (light coverage)

Athena is a **serverless, interactive SQL query service** that runs standard SQL directly against data sitting in **S3** (CSV, JSON, Parquet, ORC, Avro, etc.) — no cluster to provision, no data loading step; you point Athena at an S3 location (registered as a table, typically via the AWS Glue Data Catalog) and query it with standard ANSI SQL. Billing is per-query, based on the amount of data scanned, which is why columnar formats like Parquet (which let Athena skip irrelevant columns) and partitioning (letting Athena skip irrelevant S3 prefixes) directly reduce cost. As a developer, the level of awareness needed: Athena is the answer whenever a scenario wants **ad-hoc SQL analysis over data already at rest in S3** without standing up a database or a Redshift cluster — e.g., "run occasional SQL reports over our application's S3-based access logs" or "query Firehose-delivered data that landed in S3." It is not a place you write application data to directly — it queries what's already there.

## 6. Amazon OpenSearch Service (light coverage)

OpenSearch Service is AWS's managed, distributed **search and analytics engine** (a fork of Elasticsearch), commonly used by developers for two things: **full-text/application search** (product search, autocomplete) and **log analytics/observability dashboards** (via OpenSearch Dashboards, the Kibana-derived UI). From a developer's perspective, the relevant pattern is: application/CloudWatch logs, or a Kinesis Data Firehose stream, are pushed into an OpenSearch domain, and engineers query/visualize that data near-real-time for operational insight — this is one of Firehose's four named destinations (§4) and shows up in scenarios like "centralize and search logs from many microservices in near-real-time." Deep cluster-sizing/operational detail is out of scope for DVA-C02; know **what it's for and how data typically gets there (Firehose or direct SDK/API indexing)**, not how to tune shard allocation.

## 7. Worked real-world scenarios

**Scenario A — the duplicate-charge bug.** An e-commerce backend uses a Standard SQS queue to process payment-capture jobs; a Lambda function is subscribed via an event source mapping. During a load spike, a support ticket reports a handful of customers were charged twice for the same order. Investigating, the team finds the payment-processing Lambda occasionally takes 45 seconds under load, while the queue's visibility timeout is the SQS default of 30 seconds — so a second Lambda invocation picks up the same still-unprocessed message and charges the card again before the first invocation finishes and deletes it. There are two contributing causes, both must be fixed: first, the visibility timeout should be increased comfortably above the function's worst-case processing time (or extended dynamically via `ChangeMessageVisibility` for genuinely variable-length jobs); second — and this is the deeper fix — the payment-capture logic itself should be made **idempotent** (e.g., checking an `idempotency_key`/order-charge-status before capturing) precisely because Standard SQS is at-least-once delivery by design, so duplicate delivery under other conditions (retries, DLQ redrives) will happen again regardless of timeout tuning. **Lesson:** visibility timeout mismatches are a classic root cause of "why did this get processed twice," but the exam-correct long-term fix for Standard-queue duplicates is always application-level idempotency, not just a longer timeout.

**Scenario B — the noisy fanout.** A retail company's order-processing service publishes every order event (created, shipped, cancelled, refunded — about 50,000 events/day) to a single SNS topic. Three teams subscribe: fulfillment (needs only "created" events), a finance Lambda (needs only "refunded" events, about 200/day), and a data warehouse ingestion queue (needs everything). Before optimization, all three subscribers receive all 50,000 events daily and each does its own filtering in code — the finance Lambda alone burns 50,000 invocations/day to find 200 relevant events, needlessly inflating Lambda cost and SQS polling traffic. The fix: attach a **subscription filter policy** to the fulfillment queue's subscription matching `{"event_type": ["order_created"]}`, and to the finance Lambda's subscription matching `{"event_type": ["order_refunded"]}`; the data warehouse queue keeps no filter since it genuinely needs every event. SNS now discards non-matching messages before delivery, cutting the finance Lambda's invocations from 50,000/day to ~200/day with zero code changes required in the subscribers. **Lesson:** this is precisely the Domain 4.3 "optimize messaging" scenario — filter policies move waste out of consumer code and into the free filtering SNS already does at delivery time.

**Scenario C — choosing between SQS and Kinesis for clickstream data.** A media company wants to capture website clickstream events (page views, clicks) for three simultaneous purposes: real-time fraud/bot detection (needs to see every event within seconds), a nightly batch load into a data warehouse for BI reporting, and a live "concurrent viewers" dashboard. A junior engineer's first proposal is a single SQS queue with three consumer applications competing to read from it — but this breaks immediately: an SQS message is deleted once one consumer processes it, so the other two consumer applications would only ever see roughly a third of the events each, and there's no way to "replay" yesterday's events if the BI job fails and needs to rerun. The correct design uses **Kinesis Data Streams**: all three consumer applications (fraud detection via KCL or Lambda, a Kinesis Data Analytics query feeding the live dashboard, and a Kinesis Data Firehose delivery stream landing raw events into S3 for the nightly BI job to query via Athena) independently read the *same* stream at their own pace, each tracking its own position, and the stream's retention window lets the BI job re-read a full day's data if a run fails. **Lesson:** "multiple independent consumers need to see the full, potentially-replayable stream of the same data" is the signal that rules out SQS and points to Kinesis, even though both are technically "queues you can put data into."

## Key exam traps from this module

- Standard SQS = at-least-once, not exactly-once — application code must be idempotent; only FIFO gives exactly-once processing (within its dedup window) and strict ordering.
- A visibility timeout shorter than actual processing time causes duplicate delivery to a second consumer — increase it or extend it dynamically with `ChangeMessageVisibility`.
- Long polling (`WaitTimeSeconds` 1–20) reduces empty responses and cost versus short polling — a frequent Domain 4 optimization answer.
- A DLQ's `maxReceiveCount` is configured on the **source queue's** redrive policy, not on the DLQ itself; the DLQ is just a normal queue you designate.
- SNS filter policies live on the **subscription**, match **message attributes** by default, and are a cost/traffic optimization (Domain 4.3) because they discard non-matching messages before delivery, not after.
- SNS + SQS fanout gives every subscriber its own durable buffer — plain SNS delivery to HTTP/Lambda has no built-in durability if that endpoint is down.
- EventBridge is the pick when the trigger is a native AWS service event, a SaaS partner event, a scheduled `rate()`/`cron()` job, or content-based routing across many event types/sources; SNS is the pick for simple fanout from your own app to heterogeneous subscriber types.
- Kinesis vs. SQS: if multiple independent consumers must each read the **same full data set**, or historical data must be **replayable**, it's Kinesis — SQS deletes a message once consumed and cannot replay.
- Kinesis Data Streams = you manage shards/consumers/replay; Firehose = fully managed delivery to S3/Redshift/OpenSearch with no shard management, near-real-time not real-time; Data Analytics = SQL/Flink queries running live over a stream.
- A hot shard (uneven partition key distribution) throttles a Kinesis stream even when total provisioned throughput looks sufficient — partition key choice matters.
- Athena queries data already at rest in S3 via SQL, billed per data scanned — it is not a place to write live application data to, and it's not a substitute for a transactional database.
- OpenSearch Service is the developer-relevant answer for centralized log search/analytics dashboards, commonly fed via Kinesis Data Firehose.
