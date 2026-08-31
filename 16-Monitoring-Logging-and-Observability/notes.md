# Module 16 — Monitoring, Logging & Observability

Domain focus: this module covers **Domain 4 — Troubleshooting and Optimization (18%)** essentially in full. Task Statement 1 ("Root cause and resolve failures/errors") and Task Statement 2 ("Instrument code for observability") are covered here end to end; Task Statement 3 ("Optimize the application to best use AWS services and features") had its caching/concurrency half covered in Module 09 — this module closes the loop with a short recap tying performance troubleshooting back to the observability tools you'll learn here. Everything in this module assumes Lambda (Module 04), API Gateway (Module 05), DynamoDB (Module 03), and CI/CD tooling (Module 10, 13) as background — the point of this module is learning to **see** what those services are actually doing in production and **prove** why something broke.

## 1. Logging vs. Monitoring vs. Observability — the conceptual foundation

These three words get used loosely in casual conversation but the exam (and real engineering practice) treats them as distinct, layered concepts:

- **Logging** — discrete, timestamped records of individual events ("at 14:22:05, request abc123 failed with a CardDeclinedException"). Logs answer "what happened, exactly, on this one occasion." CloudWatch Logs is AWS's log storage/query service.
- **Monitoring** — aggregated, numeric measurements collected over time, watched against thresholds ("average latency over the last 5 minutes exceeded 800ms"). Monitoring answers "is the system currently healthy, according to metrics I decided in advance to track." CloudWatch metrics and alarms are AWS's monitoring layer.
- **Observability** — the property of a system that lets you ask **arbitrary new questions** you didn't anticipate in advance, using the instrumentation (logs, metrics, and traces) you already have, without shipping new code. It's not a single AWS service — it's an outcome you get from combining structured logs, custom metrics, and distributed traces (X-Ray) well enough that when a totally new kind of failure shows up, you can still root-cause it from existing data.

**Why this distinction matters for the exam:** a question describing "we need to know that error rates crossed a threshold and page someone" is a monitoring/alarm question. A question describing "we need to reconstruct exactly what happened to one specific failing request as it moved through five microservices" is a tracing/observability question, and CloudWatch alarms alone can't answer it — you need X-Ray (or structured logs correlated by a request ID). A question describing "who deleted this S3 bucket" is neither — it's an audit question, which is CloudTrail's job, not CloudWatch's or X-Ray's. Keeping these three buckets separate is the single highest-leverage mental model for this whole domain.

## 2. Amazon CloudWatch fundamentals

CloudWatch is AWS's native metrics, logs, alarms, and dashboards service — the default monitoring backbone for nearly every AWS service.

- **Namespace** — a container that isolates a set of metrics, preventing collisions between applications/services (e.g. `AWS/Lambda`, `AWS/DynamoDB`, or a custom namespace like `OrderService` for your own application metrics). AWS-published namespaces always start with `AWS/`.
- **Metric** — a time-ordered set of data points published to a namespace (e.g. `Invocations`, `Duration`, `Errors`, `Throttles` for Lambda; `ConsumedReadCapacityUnits` for DynamoDB).
- **Dimension** — a name/value pair that further identifies a metric within a namespace, letting you slice the same metric name by, say, `FunctionName` or `TableName`. A metric is uniquely identified by the combination of namespace + metric name + the full set of dimension values. Up to 30 dimensions per metric.
- **Standard resolution vs. high-resolution metrics** — standard-resolution metrics have a minimum granularity of **one minute**; high-resolution metrics can be published (and alarmed on) down to **one second**. High-resolution costs more (more data points ingested/stored) and is used when you need to detect and react to very short-lived spikes that a 1-minute average would smooth over and hide.
- **Metric retention** — CloudWatch automatically retains data at decreasing granularity over time: 1-second data for 3 hours, 1-minute data for 15 days, 5-minute data for 63 days, 1-hour data for 15 months. You don't manage this manually; older, coarser rollups are always available even after fine-grained data ages out.

### CloudWatch Alarms
An alarm watches a single metric (or a math expression across metrics) against a threshold over an evaluation period and changes state between `OK`, `ALARM`, and `INSUFFICIENT_DATA`. Alarm state changes trigger **actions**:
- **SNS notification** — publish to a topic, fanning out to email, SMS, or a Lambda function (the most common "page someone" pattern).
- **Auto Scaling action** — trigger a scale-out/scale-in policy directly (this is exactly how target tracking and step scaling policies work under the hood, from Module 01 — they're CloudWatch alarms wired to ASG scaling policies).
- **EC2 action** — recover, stop, terminate, or reboot an instance automatically on certain alarm conditions.

**Composite alarms** combine the states of multiple underlying alarms using AND/OR logic (e.g. "only page on-call if BOTH high error rate AND high latency alarms are simultaneously in ALARM") to reduce alert noise from a single flaky metric tripping a threshold in isolation — a single upstream blip shouldn't page anyone if it doesn't correlate with an actual user-facing symptom.

## 3. CloudWatch Logs

- **Log group** — a named container for logs from one source (e.g. one Lambda function, `/aws/lambda/order-service`). Each log group has its own retention setting and, optionally, its own KMS encryption key.
- **Log stream** — within a group, a sequence of log events from a single source instance of that resource (e.g. one Lambda execution environment, one EC2 instance's agent). A busy Lambda function will have many concurrent streams as AWS spins up multiple execution environments.
- **Retention** — by default, CloudWatch Logs **never expires log data** (kept indefinitely) unless you explicitly set a retention policy (1 day up to 10 years, or "never expire"). **Exam trap:** forgetting to set retention is a real-world cost leak the exam likes to test — the fix isn't "delete logs manually," it's setting an explicit retention period on the log group.
- **Subscription filters** — a log group can stream matching log events, in near real time, to **Lambda**, **Kinesis Data Streams**, or **Kinesis Data Firehose** as they're ingested, for real-time processing (e.g. scanning every incoming log line for a specific error pattern and triggering an alert, or shipping logs to a third-party SIEM/analytics tool). This is different from Logs Insights (section 4 below), which queries logs *after* they've landed, on demand — subscription filters are push-based and continuous.
- **Metric filters** — a related but distinct feature: define a pattern to match against incoming log lines, and each match increments a CloudWatch metric (e.g. count every log line containing `"level":"ERROR"` and publish that count as a custom metric you can then alarm on). This is the classic pattern the official AWS sample question describes: CloudWatch agent ships EC2 fleet logs into a log group, a metric filter counts error occurrences, and a CloudWatch alarm fires off that derived metric.

## 4. CloudWatch Logs Insights — query language

Logs Insights is a purpose-built query language for interactively searching and aggregating CloudWatch Logs, without needing to export logs elsewhere first. Core commands, piped together like a Unix pipeline:

- `fields` — select which fields to return (`@timestamp`, `@message`, or fields parsed out of structured JSON logs automatically, e.g. `level`, `requestId`).
- `filter` — keep only log events matching a condition (`filter level = "ERROR"`, or `filter @message like /Timeout/`).
- `parse` — extract structured fields out of unstructured/plain-text log lines using a pattern (useful when logs *aren't* JSON, e.g. `parse @message "latency=* ms" as latencyMs`).
- `stats` — aggregate: `count()`, `sum()`, `avg()`, `min()`, `max()`, `pct()`, optionally grouped `by` a field or a time bucket via `bin()`.
- `sort` — order results, ascending or descending.
- `limit` — cap the number of returned rows.

**Worked example** — filter ERROR-level logs from an order-processing service and count them in 5-minute buckets, to spot when an error spike started:
```
fields @timestamp, @message
| filter level = "ERROR"
| stats count(*) as errorCount by bin(5m)
| sort errorCount desc
```
Because this service logs structured JSON (section 7 below), Logs Insights automatically discovers the `level` field without needing a `parse` step — this is a direct payoff of structured logging, and exactly why the exam pairs the two concepts. If the logs were plain text instead, you'd need something like `parse @message "level=* " as level` first before `filter level = "ERROR"` would work at all.

A second common pattern — finding the slowest requests to identify a performance regression:
```
fields @timestamp, requestId, latencyMs, @message
| filter latencyMs > 1000
| sort latencyMs desc
| limit 20
```

Logs Insights queries run against one or more chosen log groups over a selected time window, are billed per GB of log data scanned, and are the exam's go-to answer whenever a scenario says "search across logs for a pattern" or "find how often X occurred over time" without wanting to build custom log-processing infrastructure.

## 5. CloudWatch Dashboards

Dashboards are customizable, shareable visual boards combining widgets — line/stacked graphs of metrics, single-value "big number" tiles, alarm status widgets, and even embedded Logs Insights query results — into one view. They're **global** in the sense that a single dashboard can pull metrics from multiple Regions and multiple accounts (with cross-account observability configured). Dashboards don't generate alerts themselves; they're for human visualization. The exam differentiates dashboards (a viewing surface) from alarms (an automated action trigger) — a dashboard showing a metric trending badly does *nothing* on its own unless a separate alarm is also configured on that metric.

## 6. Structured logging and the case for JSON logs

**Plain-text logging** looks like:
```
2026-08-31 14:22:05 ERROR Failed to charge payment for order 48213, card declined
```
This is human-readable at a glance but painful to query reliably — Logs Insights (or any log tool) has to guess at field boundaries with regex-like `parse` patterns, which is brittle if the message format ever changes even slightly.

**Structured (JSON) logging** looks like:
```json
{"timestamp":"2026-08-31T14:22:05.183Z","level":"ERROR","service":"order-service","requestId":"6f2b9b1e-27b1-4a3e-9c2d-1a7e5f9b2c31","userId":"u-48213","orderId":"o-90218","errorType":"CardDeclinedException","latencyMs":842,"message":"Failed to charge payment"}
```
Every field is explicitly named and typed, so Logs Insights (and any downstream tool) can `filter`, `stats`, and `sort` directly on `level`, `errorType`, `userId`, or `latencyMs` with zero parsing logic. This is the concrete, practical reason "structured logging" is exam-relevant, not just a style preference: **it's what makes Logs Insights querying, metric filters, and correlation across services actually reliable at scale.** A `requestId` (or trace ID, see section 9) present in every log line from every service a request touches is what lets you reconstruct one request's full journey across a distributed system after the fact — this is the connective tissue between logging and tracing.

## 7. CloudWatch embedded metric format (EMF)

Custom metrics normally require a separate API call (`PutMetricData`, section 8) for every metric you want to record — which means extra network calls, extra latency, and extra cost if you're emitting metrics at high volume or high cardinality (e.g. one metric per customer ID). **Embedded Metric Format (EMF)** solves this: you emit a specially-structured JSON log line (to CloudWatch Logs, or via the CloudWatch Logs agent/Lambda extension) that contains both your regular log context *and* an embedded metric definition. CloudWatch automatically extracts and graphs the metrics from that log line — **no separate PutMetricData call needed** — while the full structured log line (with every dimension, even ones not used in the metric) remains queryable in Logs Insights.

```json
{
  "_aws": {
    "Timestamp": 1693495325183,
    "CloudWatchMetrics": [
      {
        "Namespace": "OrderService",
        "Dimensions": [["Service", "Environment"]],
        "Metrics": [
          {"Name": "PaymentLatency", "Unit": "Milliseconds"},
          {"Name": "PaymentFailure", "Unit": "Count"}
        ]
      }
    ]
  },
  "Service": "order-service",
  "Environment": "production",
  "PaymentProvider": "stripe",
  "requestId": "6f2b9b1e-27b1-4a3e-9c2d-1a7e5f9b2c31",
  "PaymentLatency": 842,
  "PaymentFailure": 1
}
```
The `_aws` block tells CloudWatch which top-level fields are metrics, what namespace/dimensions to file them under, and their unit — everything else in the JSON object (like `PaymentProvider` or `requestId`) stays as ordinary structured log context, queryable but not graphed as a metric. **EMF is the exam's answer whenever a scenario wants high-cardinality custom metrics (e.g. per-customer, per-order-type) emitted efficiently, directly from application code that's already logging structured JSON, without the overhead of one PutMetricData call per data point.**

## 8. Application metrics: built-in vs. custom (PutMetricData)

Every AWS service publishes a baseline set of **built-in metrics** automatically at no extra setup (Lambda's `Invocations`/`Errors`/`Duration`/`Throttles`, DynamoDB's `ConsumedReadCapacityUnits`, ALB's `HTTPCode_Target_5XX_Count`, and so on) — these cover infrastructure- and service-level health but know nothing about *your* application's business logic.

**Custom metrics** let you publish your own application-specific measurements — "number of orders placed," "cart abandonment count," "payment provider latency" — via the `PutMetricData` API, called directly from your application code:

```python
import boto3
from datetime import datetime, timezone

cloudwatch = boto3.client("cloudwatch")

cloudwatch.put_metric_data(
    Namespace="OrderService",
    MetricData=[
        {
            "MetricName": "PaymentFailure",
            "Dimensions": [
                {"Name": "Environment", "Value": "production"},
                {"Name": "PaymentProvider", "Value": "stripe"},
            ],
            "Timestamp": datetime.now(timezone.utc),
            "Value": 1,
            "Unit": "Count",
        }
    ],
)
```
This works everywhere but costs one API call (and its associated latency/cost) per data point published, and every distinct combination of dimension values counts toward metric cardinality/cost. When that per-call overhead or high-cardinality cost becomes a problem, EMF (section 7) is the better-fitting answer on the exam — same underlying goal (custom application metrics), different delivery mechanism, and the differentiator the exam tests is exactly this cost/overhead tradeoff.

## 9. AWS X-Ray — distributed tracing

CloudWatch tells you *that* something is slow or erroring in aggregate. X-Ray tells you **where, specifically, in a chain of service calls** the slowness or error actually originates — this is the core value proposition to internalize.

- **Trace** — the end-to-end record of one request as it moves through your application, potentially across many services (API Gateway → Lambda → DynamoDB → an external HTTP call, for example). A trace is identified by a **trace ID**, generated at the entry point and **propagated** forward through every downstream call (typically via an HTTP header, `X-Amzn-Trace-Id`), so every service touched by that one request contributes its data to the same trace.
- **Segment** — the data one service/resource contributes to a trace — timing, resource metadata, errors/faults, for the work that one node did.
- **Subsegment** — a more granular breakdown *within* a segment — e.g. the specific downstream call your Lambda function made to DynamoDB, or a distinct block of business logic — timed separately from the rest of the segment's work, so you can see not just "this Lambda invocation took 900ms" but "of that 900ms, 780ms was one specific downstream call."
- **Annotations vs. metadata** — both let you attach extra key-value context to a segment/subsegment, but they behave very differently:
  - **Annotations** are **indexed and searchable** — you can filter/query traces in the X-Ray console by annotation value (e.g. "show me every trace where `orderId = o-90218`" or "every trace where `paymentProvider = stripe` AND it errored"). Use annotations for values you'll want to search or group traces by.
  - **Metadata** is **not indexed** — it's still attached to and visible on the trace for context when you're looking at one specific trace in detail, but you cannot search across traces by a metadata value. Use metadata for larger, less-structured context (e.g. a full request payload) that helps a human understand one trace but that you'd never query across traces.
- **X-Ray SDK** — the language-specific library (Node.js, Python, Java, .NET, Go, Ruby) your application code uses to create segments/subsegments, add annotations/metadata, and automatically instrument common AWS SDK calls and outgoing HTTP requests.
- **X-Ray daemon** — a lightweight background process/container that listens locally (UDP, port 2000 by default) for trace data emitted by the X-Ray SDK and batches/forwards it to the X-Ray API. On Lambda, this is handled automatically when X-Ray active tracing is enabled (no daemon to manage yourself); on EC2/ECS/on-prem, you run the daemon yourself (or, on ECS, as a sidecar container).
- **Sampling rules** — tracing every single request at high volume is expensive and often unnecessary; sampling rules let you control what fraction of requests get traced (e.g. "trace 100% of the first request per second, plus 5% of everything beyond that," or different rates per service/URL path) to balance tracing cost/volume against visibility. Sampling is configured centrally in the X-Ray console/API and pulled down by the SDK, without a code deployment.

```javascript
const AWSXRay = require("aws-xray-sdk-core");
const segment = AWSXRay.getSegment();

const subsegment = segment.addNewSubsegment("chargePayment");
subsegment.addAnnotation("orderId", orderId);          // indexed — searchable across traces
subsegment.addAnnotation("paymentProvider", "stripe"); // indexed — searchable across traces
subsegment.addMetadata("requestPayload", payload);     // not indexed — context only, this trace

try {
  const result = await chargeCard(orderId, amount);
  subsegment.close();
  return result;
} catch (err) {
  subsegment.addError(err);
  subsegment.close(err);
  throw err;
}
```

### X-Ray service maps
The **service map** is X-Ray's visual call graph: every service/resource that participated in traced requests, drawn as nodes, connected by edges representing calls between them, color-coded by health (green = healthy, red/yellow = errors or high latency present). This is the fastest way to visually spot **which specific node** in a multi-service call chain is the slow or erroring one, without manually correlating logs across five different services by hand — you look at the map, see the one red node, and drill into its traces from there. This is precisely the workflow the exam tests when it describes "a company wants to visualize the call graph of a distributed application and quickly identify which microservice is causing elevated latency."

## 10. Common HTTP error codes — what they mean for debugging

The exam guide explicitly calls out interpreting HTTP status codes as a root-cause skill. The 4xx vs. 5xx split is the first thing to anchor on: **4xx = the client did something the server considers invalid; 5xx = the server (or something it depends on) failed to fulfill an otherwise-valid request.**

| Code | Meaning | What it tells you to investigate |
|---|---|---|
| 400 Bad Request | Malformed/invalid request syntax or parameters | Client-side input validation, request body/schema mismatch |
| 403 Forbidden | Authenticated (or not) but **not authorized** for this action | IAM policy, resource policy (e.g. S3 bucket policy), or API Gateway resource policy denying the caller |
| 404 Not Found | The requested resource doesn't exist (or the API deliberately hides its existence) | Wrong URL/path/resource identifier, or a resource genuinely deleted/never created |
| 429 Too Many Requests | **Throttling** — caller exceeded a rate limit | Client needs retry with exponential backoff/jitter, or a service-side quota needs raising (API Gateway throttling limits, DynamoDB provisioned throughput, Lambda concurrency limits) |
| 500 Internal Server Error | Unhandled exception/failure inside the backend itself | Application code bug, unhandled exception — check application/Lambda logs first |
| 502 Bad Gateway | An intermediary (e.g. API Gateway, ALB) got an **invalid response** from the upstream/backend | Backend returned malformed output (e.g. a Lambda proxy integration returning a response not shaped as API Gateway expects) |
| 503 Service Unavailable | The service is temporarily overloaded or unavailable | Capacity/overload issue, ongoing deployment, or a dependency outage |
| 504 Gateway Timeout | An intermediary didn't get a response from the upstream **in time** | Backend took too long — e.g. a Lambda function's execution exceeded API Gateway's fixed 29-second integration timeout, or a downstream dependency (database, external API) hung |

**Exam trap:** 403 is an *authorization* problem (identity is known, permission is denied), not an *authentication* problem — don't confuse it with "invalid credentials," which typically surfaces as 401 outside of AWS's own API conventions (AWS APIs commonly return 403 for both missing and insufficient credentials, so don't over-index on 401 appearing on this exam). And 502/504 specifically point at the **integration/response shape or timing** between two hops, not necessarily a bug deep inside the backend's business logic — that distinction (bad response shape vs. slow response vs. backend logic bug) is exactly what separates a 502 from a 504 from a 500 on the exam.

## 11. Common exceptions generated by AWS SDKs

The exam guide separately calls out recognizing SDK-level exceptions as a root-cause skill — these are the typed exceptions your application code actually catches, one layer below the raw HTTP status code:

| Exception | Root cause it signals |
|---|---|
| `ThrottlingException` | The API call rate exceeded a service's rate limit — retry with exponential backoff, or request a limit increase if this is a sustained legitimate load pattern |
| `AccessDeniedException` | The caller's IAM identity (or resource policy) does not authorize this specific action/resource — check the identity policy, resource policy, and permissions boundary/SCP, in that order |
| `ResourceNotFoundException` | The referenced resource (a DynamoDB table, a Lambda function, a Secrets Manager secret, etc.) does not exist in this account/Region, or was deleted, or the name/ARN is wrong |
| `ProvisionedThroughputExceededException` | **DynamoDB-specific** — the table (or a specific partition) exceeded its provisioned read/write capacity; points to a hot partition or under-provisioned capacity, and is resolved by switching to on-demand capacity mode, provisioning more capacity, or fixing a partition key design that's concentrating traffic (Module 03) |
| `ConditionalCheckFailedException` | **DynamoDB-specific** — a conditional write (`ConditionExpression`) failed because the item's current state didn't match what the condition expected — normal and expected behavior for optimistic locking patterns, not necessarily a bug |

**Exam trap:** `ThrottlingException` and `ProvisionedThroughputExceededException` are easy to conflate — the general one applies broadly across services (API rate limiting), while the DynamoDB-specific one is about the table's own provisioned capacity being exceeded, and the fix set is different (backoff/retry helps both, but only the DynamoDB one is fixed by changing capacity mode or partition key design).

## 12. Debugging code and troubleshooting deployment failures

**Debugging application code:** unlike a traditional server you can attach a live debugger to, Lambda functions (and most managed compute) are best debugged through a combination of: structured logging at key decision points (section 6), local invocation/testing (the SAM CLI's `sam local invoke`, from Module 13, lets you run a function locally against a sample event before ever deploying), replaying a captured failing event against the function in a test environment, and reading the X-Ray subsegment breakdown to see exactly which internal call was slow or threw. The exam favors "add structured logging / check CloudWatch Logs / use X-Ray" over "SSH in and attach a debugger" for anything serverless — there's usually no server to SSH into.

**Troubleshooting deployment failures** means reading the *deployment tool's own* output logs, not your application's runtime logs — these are different failure surfaces:
- **CodeBuild** — build logs (streamed to CloudWatch Logs by default) show compilation errors, failed test steps, or a `buildspec.yml` phase that exited non-zero — always the first place to look when a build stage fails in a pipeline (Module 10).
- **CodeDeploy** — deployment events and per-instance/per-task lifecycle hook logs show exactly which hook (`BeforeInstall`, `AfterInstall`, `ApplicationStart`, `ValidateService`, etc.) failed and why, plus whether an automatic rollback was triggered (Module 10).
- **CloudFormation** — the **stack events** tab shows each resource's creation/update/deletion status in order, and critically, the **specific reason a resource failed** (e.g. "already exists," an invalid property value, an IAM permissions failure creating a role) — this is what you read to understand why a stack rolled back, and it's the single most exam-relevant CloudFormation troubleshooting skill (Module 13).

## 13. AWS CloudTrail — distinct from CloudWatch

CloudTrail answers a fundamentally different question than CloudWatch or X-Ray: **"who (or what) called which AWS API, when, from where, and what was the result?"** It's an **audit log of API activity**, not an application performance or tracing tool.

- **Management events** — control-plane operations on AWS resources themselves (creating an S3 bucket, modifying an IAM policy, launching an EC2 instance). Logged by default, and free for the first copy of management events per Region.
- **Data events** — data-plane operations *within* a resource (an S3 `GetObject`/`PutObject` call, a Lambda function invocation, a DynamoDB item-level operation). **Not logged by default** — you opt in explicitly, and they're higher-volume and billed per event, because logging every single object read in a busy S3 bucket is a lot of events.
- **CloudTrail Lake** — a managed data lake/query feature for CloudTrail events, letting you run SQL-based queries directly across trail data (including from multiple accounts/Regions) without standing up your own ETL pipeline into Athena/S3 — useful for security investigations and compliance reporting that need ad hoc querying over a long retention window.

**Exam trap:** if a scenario asks "who deleted this DynamoDB table" or "which IAM user modified this security group," the answer is always CloudTrail (an audit/API-call question), never CloudWatch Logs or X-Ray, even though all three are technically "AWS observability services." CloudWatch and X-Ray have no concept of *identity/who-called-it* baked into their core data model the way CloudTrail does.

## 14. Amazon CodeGuru

Two distinct tools under one brand, easy to mix up on the exam:

- **CodeGuru Reviewer** — automated code review, run against a pull request (integrates with CodeCommit, GitHub, Bitbucket, Module 10), using ML models trained on best practices to flag potential bugs, resource leaks, security vulnerabilities (including detecting hardcoded secrets), and deviations from AWS best practices — a **static, pre-deployment** analysis of your source code.
- **CodeGuru Profiler** — analyzes your **running** application in production (or any environment) to identify CPU and latency hotspots — which specific lines/methods are consuming the most time or resources — visualized as a flame graph, so you can find the actual bottleneck in running code rather than guessing. This is a **runtime, post-deployment** tool, complementary to Reviewer, not a replacement for it.

**Exam trap:** "find security/quality issues before merging code" → Reviewer. "Find out why this already-running application is using excessive CPU / is slower than expected" → Profiler. They cover different points in the software lifecycle and the exam tests that distinction directly.

## 15. Implementing alerts for specific actions

Beyond generic "alarm when a metric crosses a threshold," the exam expects you to recognize a couple of specific alerting patterns:

- **Approaching a service quota** — many AWS services publish **usage metrics relative to their account-level quotas** (e.g. Lambda concurrent executions vs. your account's concurrency limit, or a CloudWatch alarm on a `ServiceQuotas`-related metric), letting you set an alarm that fires *before* you actually hit a hard limit and start seeing throttling/errors, giving you time to request a quota increase proactively rather than reactively.
- **Notification when a deployment completes** — a common **EventBridge + SNS** pattern: a deployment tool (CodePipeline, CodeDeploy) emits a state-change event to EventBridge on completion/failure; an EventBridge rule matches that specific event pattern and targets an SNS topic, which fans out to email/Slack/chat-ops integrations. This is the general-purpose pattern for "notify someone when X AWS-native event happens" whenever the trigger is a discrete state change (a deployment finishing, a Step Functions execution failing, a GuardDuty finding) rather than a metric crossing a numeric threshold — **EventBridge + SNS for discrete events, CloudWatch Alarms + SNS for metric thresholds** is the distinction the exam is testing.

## 16. CloudWatch vs. X-Ray vs. CloudTrail — what each answers (and doesn't)

| | CloudWatch (metrics/logs/alarms) | AWS X-Ray (distributed tracing) | AWS CloudTrail (API audit log) |
|---|---|---|---|
| Core question it answers | "Is the system healthy right now, in aggregate? What happened in this log line?" | "As this one request moved across services, where exactly did it slow down or fail?" | "Who/what called which AWS API, when, and what happened?" |
| Data shape | Numeric time series (metrics) + discrete log events | Per-request traces made of segments/subsegments across services | Per-API-call audit records (identity, action, resource, result) |
| Good for | Alerting on thresholds, dashboards, searching/aggregating logs | Root-causing latency/errors in multi-service call chains, visualizing a service map | Security investigation, compliance, "who changed this resource" |
| Does NOT answer | Which specific downstream call in a chain caused the slowness (no cross-service call graph) | Whether an IAM identity was authorized to do something, or account-wide resource health trends | Application performance, latency, or error rates — CloudTrail doesn't care whether the API call was "slow," only that it happened |
| Typical trigger for using it | "Set up an alarm," "search logs for a pattern," "visualize trend over time" | "Find the bottleneck in a call chain," "visualize the service map" | "Who deleted/modified this," "prove compliance with an audit" |

These three services are complementary, not competing — a real production incident is often root-caused using all three together (see Scenario A below): X-Ray shows *which* service is slow, CloudWatch Logs Insights shows *what* was happening in that service's logs at that time, and CloudTrail (if the issue turns out to be a misconfiguration) shows *who* changed the configuration and when.

## 17. Recap tie-in: Optimization (Module 09) meets Observability (this module)

Module 09 covered the "optimize" half of this domain — caching strategies (ElastiCache, DAX, CloudFront, API Gateway caching) and concurrency tuning (Lambda provisioned/reserved concurrency, connection pooling) as *fixes* for performance problems. This module is how you'd *discover* that a performance problem exists and *prove* which fix applies in the first place: a CloudWatch alarm on elevated P99 latency or a DynamoDB `ThrottlingException` rate is what tells you a caching or capacity problem exists; an X-Ray service map showing one node consistently slow is what tells you *where* to add a cache or raise concurrency, rather than guessing; and a Logs Insights query aggregating error types over time is what confirms whether a fix (e.g. adding a DAX cache in front of DynamoDB, or raising Lambda reserved concurrency) actually reduced the error/latency rate afterward. On the exam, a scenario describing degraded performance with no clear cause almost always expects you to reach for CloudWatch/X-Ray *first* to root-cause, before jumping to an optimization fix — implementing a fix (like a cache) without first confirming what's actually slow via these tools is treated as premature.

## 18. Worked real-world scenarios

**Scenario A — the slow downstream dependency, found via service map + Logs Insights.** A checkout API built on API Gateway → Lambda → DynamoDB, with a synchronous call out to a third-party payment provider, starts showing elevated P99 latency company-wide, but average latency looks fine and no alarms have fired yet (P99 vs. average masking the problem — a good example of why percentile metrics matter). An engineer opens the X-Ray service map for the checkout workflow and sees every node green except the node representing the outbound call to the payment provider, which is amber, with noticeably wider (slower) edges leading into it. Drilling into individual traces touching that node shows subsegment durations for the payment call frequently exceeding 2 seconds, versus a normal ~200ms. Cross-referencing with a CloudWatch Logs Insights query — `fields @timestamp, latencyMs, paymentProvider | filter latencyMs > 1500 | stats count(*) by paymentProvider` — confirms the slow calls are concentrated on one specific payment provider integration, not evenly spread, and correlates in time with that provider's own status-page-reported degradation. **Root cause:** an external dependency's outage, not application code — the fix is a timeout + circuit breaker around that specific call, not a code rewrite. Without X-Ray's service map narrowing the search to one specific node in the call chain, this would have meant manually correlating logs across three separate services by hand.

**Scenario B — throttling exceptions traced back to a hot partition.** A DynamoDB-backed API starts returning intermittent 500 errors under peak load. A CloudWatch alarm on the Lambda function's `Errors` metric fires, and a Logs Insights query — `fields @timestamp, errorType, @message | filter errorType = "ProvisionedThroughputExceededException" | stats count(*) by bin(1m)` — shows a sharp spike in `ProvisionedThroughputExceededException` occurrences exactly matching the alarm window, all originating from writes to the same table. Checking DynamoDB's own `ConsumedWriteCapacityUnits` metric alongside `ThrottledRequests` (both partition-level where available) confirms the table's aggregate provisioned capacity looks fine, but activity is concentrated on a narrow key range — a hot partition, likely caused by a low-cardinality partition key design (e.g. partitioning by a coarse `orderDate` instead of a higher-cardinality key), a topic covered in depth in Module 03. **Root cause:** partition key design, not insufficient overall capacity — the fix is either a better-distributed key design or switching to on-demand capacity mode as a stopgap, not blindly raising provisioned throughput on a table that already has enough *aggregate* capacity.

**Scenario C — a deployment failure root-caused via CloudFormation stack events.** A CI/CD pipeline's CloudFormation deployment stage fails, and the application's own CloudWatch Logs show nothing unusual, because the *application never actually started* — the stack failed before any application code ran. The engineer opens the CloudFormation console's **Events** tab for the failed stack and reads chronologically: most resources show `CREATE_COMPLETE`, but one resource — an IAM role the Lambda function depends on — shows `CREATE_FAILED` with the reason "Role name already exists," followed by a cascade of `ROLLBACK_IN_PROGRESS` entries for every resource created after it. **Root cause:** a naming collision with a role left over from a previous manual test deployment that used the same fixed role name, not a code or application logic issue at all. This illustrates why deployment troubleshooting is a separate skill from application debugging — the relevant log surface here was CloudFormation's own stack events, not CloudWatch Logs, X-Ray, or anything application-level.

## Key exam traps
- Logging (discrete events) ≠ monitoring (aggregated metrics/alarms) ≠ observability (answering new questions from existing instrumentation) — a question's phrasing tells you which layer is being tested.
- CloudWatch Logs never expires log data by default — always set an explicit retention policy; unmanaged log groups are a real cost trap the exam likes to probe.
- Subscription filters (push, real-time, to Lambda/Kinesis) are not the same mechanism as Logs Insights (pull, on-demand queries) — don't conflate them.
- Structured (JSON) logging is what makes Logs Insights `filter`/`stats` work without brittle `parse` patterns — this is the concrete payoff, not just a style preference.
- EMF beats a separate `PutMetricData` call whenever the scenario emphasizes high-cardinality custom metrics or avoiding extra API-call overhead from already-structured logs.
- X-Ray annotations are indexed/searchable across traces; metadata is not — pick annotations for anything you'll need to filter/query by later.
- A CloudWatch alarm tells you *that* something is wrong in aggregate; only X-Ray's service map (or per-request tracing) tells you *which specific node* in a call chain is the actual cause.
- 4xx = client-side problem (400 bad input, 403 authorization denied, 404 missing resource, 429 throttling); 5xx = server/dependency-side problem (500 unhandled exception, 502 bad upstream response shape, 503 overloaded, 504 upstream too slow) — know the difference cold.
- `ThrottlingException` (general rate limiting) vs. `ProvisionedThroughputExceededException` (DynamoDB-specific capacity/hot-partition signal) are easy to conflate but point to different fixes.
- CloudTrail is the only one of the three core observability services that knows about **identity** (who called an API) — CloudWatch and X-Ray don't answer "who did this."
- Management events are logged by CloudTrail by default; data events (e.g. S3 object-level access, Lambda invocations) are not, and must be explicitly enabled.
- CodeGuru Reviewer is pre-deployment static code analysis; CodeGuru Profiler is runtime hotspot analysis on already-running code — don't swap them.
- Deployment failures are diagnosed from the deployment tool's own logs/events (CodeBuild build logs, CodeDeploy lifecycle hook events, CloudFormation stack events) — not from application runtime logs, which may show nothing because the app never started.
- EventBridge + SNS is the pattern for alerting on a discrete state-change event (a deployment finishing, a pipeline failing); CloudWatch Alarms + SNS is the pattern for alerting on a metric crossing a numeric threshold — match the trigger type to the mechanism.
