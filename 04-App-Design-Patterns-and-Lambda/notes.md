# Module 04 — Application Design Patterns & AWS Lambda

Domain focus: this module is **Domain 1 — Development with AWS Services (32%)**, and specifically it covers **both** Task Statement 1.1 ("Write code for applications hosted on AWS" — architectural patterns, resilience, idempotency) and Task Statement 1.2 ("Write code that interacts with AWS services using APIs, SDKs, and AWS CLI" as applied to Lambda specifically). Because it's two full task statements compressed into one day of a 10-day sprint, this is the densest module so far — take it slowly, and expect it to run longer than Module 01. Everything here assumes you're comfortable with IAM (Module 00), EC2 fundamentals (Module 01), S3 (Module 02), and DynamoDB (Module 03), since the patterns below constantly reference all four.

---

## PART A — Architectural Patterns & Resilience (Domain 1.1)

### 1. Core architectural patterns

**Monolithic vs. microservices**

| | Monolithic | Microservices |
|---|---|---|
| Deployment unit | One large application, deployed as a single unit | Many small, independently deployable services |
| Scaling | Scale the whole app together, even if only one piece is hot | Scale each service independently based on its own load |
| Failure blast radius | A bug or crash in one module can take down the whole app | A failure in one service is contained (if designed with resilience patterns) |
| Technology choice | Usually one language/runtime for the whole app | Each service can use a different language/runtime/datastore |
| Operational complexity | Simpler to deploy and reason about at small scale | More moving parts — service discovery, network calls, distributed tracing |
| Typical AWS shape | A single EC2 fleet or one large Elastic Beanstalk app | Many Lambda functions, ECS services, or small EC2 fleets behind API Gateway/ALB, often communicating via SQS/SNS/EventBridge |

The exam doesn't ask you to *design* a microservices architecture (that's Solutions Architect territory), but it does expect you to recognize which pattern a scenario is describing and to know the AWS services that naturally implement each piece.

**Event-driven architecture.** Components communicate by producing and consuming **events** — a fact that something happened ("OrderPlaced", "ObjectUploaded") — rather than by calling each other directly. A producer publishes an event and doesn't know or care who (if anyone) consumes it. This is the dominant pattern for serverless AWS applications.

*Concrete example:* a user uploads a profile photo to S3. S3 emits an `s3:ObjectCreated:Put` event. A Lambda function subscribed to that event fires automatically, resizes the image, and writes a thumbnail back to a different S3 prefix. The web application that handled the original upload never calls the resizing code directly — it doesn't even know a resizer exists. That decoupling is the whole point: you can add a second consumer (say, a virus scanner) later without touching the upload code at all.

**Choreography vs. orchestration** — two ways to coordinate a multi-step business process, and a favorite exam distinction:

| | Choreography | Orchestration |
|---|---|---|
| Control | Decentralized — each service reacts to events and decides what to do next on its own | Centralized — one component (an orchestrator) tells each service what to do and when |
| Typical AWS implementation | Amazon EventBridge (or SNS) — services publish events, other services subscribe independently | AWS Step Functions — a state machine explicitly defines the sequence, branching, and error handling |
| Coupling | Very loose — services don't know about each other, only about events | Slightly tighter — the orchestrator knows about all participating services |
| Visibility into overall workflow state | Harder — no single place shows "where is order #123 in its lifecycle" | Easy — the state machine execution history shows exactly where a workflow is and why it failed |
| Best for | Simple, independent reactions to a single event; systems where teams truly want to be decoupled | Complex, multi-step business processes with branching, retries, human-approval steps, and required auditability |

*Concrete example:* an order-processing pipeline. Choreographed with EventBridge: "OrderPlaced" event fires, and separately, a payment service, an inventory service, and a notification service each independently listen for that event and react. Nobody centrally tracks whether all three succeeded. Orchestrated with Step Functions: a state machine explicitly calls "Charge Payment" → on success calls "Reserve Inventory" → on success calls "Send Confirmation," with defined retry and catch logic at every step, and a visual execution graph showing exactly which step failed if something breaks. (Step Functions gets full treatment in Module 07 — this module just needs you to recognize the choreography/orchestration distinction and match it to the right AWS service.)

**Fan-out.** A single event triggers multiple independent consumers in parallel. *Concrete example:* an SNS topic named `order-events` has three SQS queues subscribed to it — one feeding a fulfillment service, one feeding an analytics pipeline, one feeding a fraud-detection service. When an order event is published once to the topic, SNS delivers a copy to all three queues automatically. Each consumer processes at its own pace, and adding a fourth consumer later requires zero changes to the publisher. This SNS-fan-out-to-SQS combination is one of the most exam-tested integration patterns in the entire DVA-C02 syllabus (full depth in Module 06) — remember it here as the canonical "fan-out" example.

### 2. Idempotency

An operation is **idempotent** if performing it multiple times produces the same result as performing it once. This matters enormously in distributed, retry-heavy AWS architectures because **at-least-once delivery is the norm, not the exception** — SQS, SNS, EventBridge, and Lambda's own async-invoke retry logic can all deliver the same event more than once. If a Lambda function that charges a customer's credit card isn't idempotent, a network blip that causes a harmless retry could charge the customer twice.

**The idempotency key pattern.** The caller (or the event itself) carries a unique identifier — an idempotency key — for the logical operation, not the physical request. Before performing the side effect, the function checks whether that key has already been processed; if so, it returns the previous result instead of repeating the work.

```python
import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table("IdempotencyKeys")

def process_payment(order_id, amount):
    try:
        # Conditional write: only succeeds if this order_id hasn't been seen before.
        table.put_item(
            Item={"order_id": order_id, "status": "PROCESSING"},
            ConditionExpression="attribute_not_exists(order_id)"
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Already processed (or in progress) — return the prior outcome, don't repeat the charge.
            existing = table.get_item(Key={"order_id": order_id})["Item"]
            return existing["result"]
        raise

    result = charge_credit_card(order_id, amount)   # the actual side effect
    table.update_item(
        Key={"order_id": order_id},
        UpdateExpression="SET #s = :s, #r = :r",
        ExpressionAttributeNames={"#s": "status", "#r": "result"},
        ExpressionAttributeValues={":s": "DONE", ":r": result}
    )
    return result
```

DynamoDB's `ConditionExpression` with `attribute_not_exists` is the standard AWS-native way to implement this: the conditional write is atomic, so even if two retries race each other, only one wins the write and proceeds to actually charge the card. This is a pattern you should be able to recognize and reason about even if the exam question doesn't show you code — "the operation must not be performed twice even if the request is retried" is the tell for an idempotency-key answer.

**Exam trap:** don't confuse idempotency with simple retry logic. A retry mechanism *causes* the need for idempotency; it doesn't provide it. "We added retries with backoff" is not a complete answer to "how do we prevent duplicate charges" — you still need the dedup/idempotency-key layer on top.

### 3. Stateful vs. stateless application design

A **stateless** component keeps no client- or session-specific data in its own memory or local disk between requests — any state it needs is either passed in with the request or fetched from an external store (DynamoDB, ElastiCache, RDS). A **stateful** component retains data locally between requests (e.g., a web server holding session data in local memory).

This distinction is central to nearly every scalable AWS pattern:
- **Lambda functions are inherently stateless** by design — you cannot rely on anything written to memory or `/tmp` persisting reliably across invocations (more on why in section 9).
- **Auto Scaling groups behind a load balancer** need stateless application instances, because any request can land on any instance, and unhealthy instances get replaced without warning (this is exactly the "session lost on instance replacement" scenario from Module 01).
- The fix for needing session/user state without sacrificing statelessness is externalizing it: store sessions in **ElastiCache** or **DynamoDB**, store uploaded files in **S3** rather than local disk, and treat every compute unit as disposable.

**Exam trap:** "the application must scale horizontally and tolerate the loss of any individual instance" is a strong signal that any answer involving local, in-memory, or local-disk state is wrong — look for the option that externalizes state to a managed store.

### 4. Tightly coupled vs. loosely coupled components

**Tight coupling**: Component A calls Component B directly and synchronously, and A's success depends on B being available and responsive right now. If B is slow, overloaded, or down, that failure propagates immediately back to A (and potentially cascades further upstream).

**Loose coupling**: Component A hands off work through an intermediary — typically a queue (SQS), topic (SNS), or event bus (EventBridge) — and doesn't wait for or depend on B's availability. B consumes the work whenever it's ready.

*Why this matters (the exam's favorite framing):* imagine an order API that, on each request, directly calls an inventory service synchronously. If the inventory service is temporarily overwhelmed, order submissions start failing or timing out — a slowdown in one service directly breaks another. Now insert an SQS queue between them: the order API drops a message on the queue and returns success immediately; the inventory service consumes messages at whatever pace it can sustain. A spike in orders no longer takes down the inventory service, and a temporary outage in the inventory service doesn't lose any orders — they simply queue up and get processed once it recovers. This is loose coupling in action, and it's why **"decouple the components"** on the exam almost always means "put a queue or topic between them."

| | Tight coupling | Loose coupling |
|---|---|---|
| Failure propagation | Failures cascade between components | Failures are isolated/absorbed by the intermediary |
| Scaling | Components must scale together | Each component scales independently |
| Availability requirement | Both components must be up simultaneously | Producer and consumer can be available at different times |
| Typical AWS glue | Direct synchronous SDK/HTTP calls | SQS, SNS, EventBridge, Kinesis |

### 5. Fault-tolerant design patterns

**Retries with exponential backoff and jitter.** A naive retry ("just try again immediately") makes things worse under load — a fleet of clients all retrying at the same instant creates a synchronized "thundering herd" that can re-overwhelm a struggling service. The standard fix is to wait progressively longer between retries (**exponential backoff**) and to randomize that wait time (**jitter**) so retries from many clients spread out instead of arriving in a synchronized burst.

```
# Exponential backoff with full jitter (pseudocode)
base_delay = 100       # ms
max_delay  = 20000     # ms
max_retries = 5

for attempt in range(max_retries):
    try:
        response = call_downstream_service()
        return response
    except TransientError:
        if attempt == max_retries - 1:
            raise   # give up, let caller / DLQ handle it
        capped = min(max_delay, base_delay * (2 ** attempt))
        sleep_time = random_between(0, capped)   # "full jitter"
        sleep(sleep_time)
```

This is exactly the algorithm the AWS SDKs implement by default under the hood for throttled/transient API calls — you rarely have to hand-roll it for AWS API calls, but you must recognize it and be able to reason about it for your own application-to-application retries. **Exam trap:** an option describing retries with a *fixed* delay, or no delay at all, is never the "best practice" answer when exponential backoff with jitter is also on offer.

**Dead-letter queues (DLQs).** When a message repeatedly fails processing (a "poison pill"), you don't want it retried forever, blocking the queue behind it. A DLQ is a separate queue that a failed message is redirected to after a configured number of failed processing attempts (`maxReceiveCount` on an SQS redrive policy), so it can be inspected/reprocessed later without stalling the main queue. Lambda has its own DLQ concept too, discussed in section 12 alongside the newer, more-favored **Lambda Destinations** feature.

**Other fault-tolerance building blocks worth recognizing** (though a deep architectural treatment is out of scope for this exam): **circuit breakers** (stop calling a downstream service for a cooldown period after it starts failing repeatedly, rather than continuing to hammer it), **timeouts** (never wait indefinitely for a dependency — always bound how long you'll wait), and **bulkheads** (isolate resource pools per dependency so one slow dependency can't exhaust the thread/connection pool needed by others).

### 6. Synchronous vs. asynchronous invocation patterns

This distinction determines who is responsible for retries and error handling, and it's foundational to how Lambda behaves (Part B leans on this heavily).

| Invocation type | Caller waits for a result? | Example AWS triggers | Who retries on failure |
|---|---|---|---|
| **Synchronous** | Yes — caller blocks until the function returns a response | API Gateway, Application Load Balancer, direct SDK `Invoke` with `RequestResponse` | The **caller** must implement retry logic; AWS does not automatically retry a sync invocation |
| **Asynchronous** | No — caller hands off the event and moves on immediately | S3, SNS, EventBridge, CloudWatch Events | **Lambda itself** automatically retries (by default, twice more) before routing to a DLQ/destination |
| **Poll-based (event source mapping)** | No — a separate polling process pulls work | SQS, Kinesis Data Streams, DynamoDB Streams | The **poller (Lambda service)** retries per the source's own semantics (visibility timeout re-delivery for SQS, iterator retry for streams) |

Notice this is a three-way split, not just sync-vs-async — the exam frequently tests whether you know which bucket a given trigger falls into, because the failure-handling story is different for each (full detail in section 12).

### 7. Unit testing during development & interacting with AWS via SDKs

**AWS SAM CLI local testing.** The AWS Serverless Application Model (SAM, covered in depth in Module 13) ships a CLI that lets you test Lambda functions **locally**, without deploying, by running them inside a Docker container that emulates the real Lambda execution environment:

```bash
# Invoke a function once with a sample event, entirely locally
sam local invoke MyFunction --event events/sample-event.json

# Run a full local API Gateway + Lambda stack for iterative testing
sam local start-api

# Step through with a debugger attached
sam local invoke MyFunction --event events/sample-event.json -d 5858
```

This is the exam-favored answer whenever a scenario says a developer wants to test Lambda function logic **before deploying**, or wants a **fast local development/debug loop** without paying for or waiting on real cloud invocations. Beyond `sam local`, ordinary unit testing still applies: mock the AWS SDK client (e.g., with `unittest.mock` in Python or `aws-sdk-client-mock` in Node) so tests don't make real network calls, and assert on your function's business logic in isolation.

**Interacting with AWS services from code.** Every AWS SDK — **boto3** for Python, the **AWS SDK for JavaScript (v3)**, the Java SDK, etc. — wraps the same underlying REST APIs and follows the same credential-resolution chain covered in Module 00 (env vars → shared config → attached role). A pattern worth internalizing now because it reappears in the performance-tuning section later: **initialize SDK clients outside your handler function**, at module/global scope, so the client (and its underlying connection pool) is reused across warm Lambda invocations instead of being rebuilt on every single call.

```python
import boto3

# Created once per execution environment, reused across warm invocations
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Orders")

def handler(event, context):
    table.put_item(Item={"order_id": event["orderId"]})
    return {"statusCode": 200}
```

```javascript
// Node.js — AWS SDK for JavaScript v3, same "init outside handler" pattern
const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const client = new DynamoDBClient({});   // created once, reused across warm invocations

exports.handler = async (event) => {
  // use `client` here
  return { statusCode: 200 };
};
```

### 8. A brief word on data streaming

Some architectures need to process continuous, high-throughput streams of data (clickstream events, IoT telemetry, log data) rather than discrete request/response calls or queued messages. **Amazon Kinesis Data Streams** is the core AWS service for this, and Lambda can consume directly from a Kinesis stream via an event source mapping (poll-based, same family as SQS and DynamoDB Streams — see section 10). The deep dive on Kinesis, shards, partition keys, and Kinesis Data Firehose/Analytics is Module 06's job; for this module, just know that streaming sources are poll-based Lambda triggers with ordered, shard-level processing, and that a Lambda function processing a Kinesis stream receives a **batch** of records per invocation, not one record at a time.

---

## PART B — AWS Lambda Deep Dive (Domain 1.2)

### 9. Lambda execution model & statelessness

A Lambda function runs inside an **execution environment** — an isolated, ephemeral runtime sandbox that AWS creates on your behalf. Its lifecycle has three phases:

1. **Init phase** — AWS provisions the execution environment: downloads your code/layers, starts the runtime, and runs any code outside your handler (like the `boto3.resource()` call above). This is what causes a **cold start**.
2. **Invoke phase** — your handler function runs against the actual event. If the execution environment is reused for a subsequent invocation (a **warm start**), the init phase is skipped entirely, which is why AWS strongly encourages initializing SDK clients and other reusable objects outside the handler.
3. **Shutdown phase** — after a period of inactivity, AWS may freeze and eventually terminate the execution environment. You cannot control exactly when this happens.

**Why Lambda is stateless by design:** because you have no guarantee that the *same* execution environment will handle your next invocation — under concurrent load, AWS spins up many parallel execution environments, and any of them (or a brand-new one) could handle the next event. Anything you write to `/tmp` (up to 10,240 MB, configurable) or hold in memory *might* survive to the next invocation if the same warm environment happens to be reused, but you must **never design around that assumption** — treat `/tmp` and in-memory state purely as an optional performance cache (e.g., caching a downloaded reference file), never as a reliable data store.

A basic Python handler, showing the `event` and `context` objects every handler receives:

```python
def handler(event, context):
    # `event` — the trigger-specific payload (API Gateway request, S3 notification, SQS batch, etc.)
    order_id = event.get("orderId")

    # `context` — runtime info about this specific invocation
    print(f"Request ID: {context.aws_request_id}")
    print(f"Time remaining (ms): {context.get_remaining_time_in_millis()}")
    print(f"Function memory limit (MB): {context.memory_limit_in_mb}")

    return {
        "statusCode": 200,
        "body": f"Processed order {order_id}"
    }
```

`context.get_remaining_time_in_millis()` is worth memorizing — it's the standard way for long-running handler logic to check how much time is left before the configured timeout fires, so it can checkpoint work or exit gracefully rather than being killed mid-operation.

### 10. Event source mapping: poll-based vs. push-based triggers

Lambda functions are invoked in one of two structurally different ways, and this distinction underlies almost every "how does Lambda scale/retry/order this" question on the exam.

| | Push-based (direct invoke) | Poll-based (event source mapping) |
|---|---|---|
| How it works | The event source calls the Lambda `Invoke` API directly (sync or async) | AWS Lambda **itself polls** the source on your behalf and batches records into an invocation |
| Example sources | S3, SNS, API Gateway, ALB, EventBridge, direct SDK invoke | SQS, Kinesis Data Streams, DynamoDB Streams, Amazon MQ, Kafka (MSK) |
| Concurrency model | Roughly one concurrent execution per concurrent triggering event | Bounded by the source's structure — e.g., one concurrent execution per Kinesis/DynamoDB Streams **shard**, or scales with SQS queue depth up to a configurable maximum |
| Who owns polling infrastructure | The event source itself pushes | The **Lambda service** manages a poller fleet that reads from the source and invokes your function with a batch |
| Ordering | Not guaranteed (S3, SNS deliver independently) | Guaranteed **within a shard/partition** for Kinesis/DynamoDB Streams; SQS standard queues are unordered, SQS FIFO queues preserve order per message group |

**Exam trap:** SQS is *not* a push source, even though it feels similar to SNS — Lambda's **event source mapping** polls SQS continuously and invokes your function with a batch of messages once available; you never "subscribe" a Lambda function to SQS the way you subscribe one to SNS or S3 event notifications. This distinction drives different retry/error-handling behavior (section 12) and different concurrency scaling behavior (section 14).

### 11. Configuring Lambda functions

This is the single most detail-dense part of the whole exam's Lambda coverage — expect several questions probing individual configuration knobs.

- **Environment variables** — key-value pairs injected into the execution environment, used for config (table names, feature flags, endpoints) without hardcoding or redeploying code. Can be encrypted with a KMS key for sensitive values (though Secrets Manager/Parameter Store, covered in Module 14, is preferred for actual secrets since it adds rotation).
- **Memory allocation** — configurable from 128 MB up to 10,240 MB. This is the single most important performance/cost knob on Lambda, because **CPU power, network bandwidth, and disk I/O all scale proportionally with the memory setting** — you cannot configure CPU independently. A CPU-bound function that's slow at 128 MB can often get *dramatically* faster (and sometimes even cheaper overall, because it finishes faster) simply by raising memory, since billed cost is memory × duration.
- **Timeout** — configurable from 1 second up to a hard ceiling of **15 minutes (900 seconds)**. This ceiling is exactly why "a job needs to run longer than 15 minutes" is the exam's standard tell to reach for ECS/Fargate, AWS Batch, or Step Functions instead of a single Lambda invocation.
- **Runtime** — the managed language runtime (Python, Node.js, Java, .NET, Go, Ruby) or a **custom runtime** via the Lambda Runtime API (packaged as a container image or a custom bootstrap), useful for languages AWS doesn't natively support.
- **Handler** — the entry-point function AWS invokes (`module.function_name`, e.g. `app.handler` in Python or `index.handler` in Node.js).
- **Lambda layers** — a way to package shared code/dependencies (libraries, common utility modules) **separately** from your function's deployment package, so multiple functions can reference the same layer without duplicating it in every deployment artifact. A function can use up to 5 layers, and layers count toward the unzipped deployment size limit (250 MB total).
- **Lambda extensions** — a way to integrate monitoring, security, and governance tools *into* the execution environment's lifecycle (they can hook into init/invoke/shutdown), run as a separate process alongside your function code, packaged as a layer. Common use: shipping logs/traces to a third-party observability tool without modifying your function code at all.
- **Triggers** — the event sources wired to invoke the function (S3, SQS, API Gateway, EventBridge rule, etc.) — configured either on the Lambda side (event source mappings) or on the source-service side (S3 event notifications, SNS subscriptions).
- **Reserved concurrency** — sets both a **ceiling** and (implicitly, by reserving it) a **guarantee** of concurrent executions available to a specific function, carved out of the account's total concurrency pool; also usable to *throttle* a noisy function down to protect a downstream dependency, or set to 0 to fully disable a function without deleting it.
- **Provisioned concurrency** — pre-initializes a specified number of execution environments so they're **already warm** and ready to serve requests instantly, eliminating cold starts for that portion of traffic. Costs more (you pay for the provisioned capacity whether it's invoked or not) and is typically paired with Application Auto Scaling to scale the provisioned amount on a schedule or target metric.
- **Lambda Destinations** — an alternative (and generally preferred, newer) way to route the *outcome* of an async invocation, discussed fully in section 12.

**SAM template snippet** showing several of these knobs together:

```yaml
Resources:
  ProcessOrderFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      Runtime: python3.12
      MemorySize: 512
      Timeout: 30
      ReservedConcurrentExecutions: 20
      Environment:
        Variables:
          TABLE_NAME: !Ref OrdersTable
          LOG_LEVEL: INFO
      Layers:
        - !Ref SharedUtilsLayer
      Events:
        OrderQueue:
          Type: SQS
          Properties:
            Queue: !GetAtt OrdersQueue.Arn
            BatchSize: 10
      DeadLetterQueue:
        Type: SQS
        TargetArn: !GetAtt OrdersDLQ.Arn
```

### 12. Handling the event lifecycle and errors

Because invocation type (section 6) determines who's responsible for retries, error handling in Lambda splits into three distinct stories:

**Synchronous invocations** (API Gateway, ALB, direct SDK call): if your function throws an error, Lambda returns that error directly to the caller — **no automatic retry**. The caller (your API client, or the code that called `Invoke`) is responsible for deciding whether and how to retry, ideally with backoff and jitter as covered in section 5.

**Asynchronous invocations** (S3, SNS, EventBridge): Lambda automatically retries a failed invocation **up to two more times** (three total attempts by default), with a delay between attempts. If all attempts fail, the event is either dropped, sent to a configured **Lambda Destination** (on-failure), or sent to a configured **dead-letter queue** — you can configure both destinations and DLQs, but AWS documentation now steers new designs toward Destinations since they carry richer metadata (invocation record, error details, request/response context) and support routing to more targets.

**Lambda Destinations** let you route the outcome of an async (or event-source-mapping streams) invocation **without writing any error-handling code yourself** — you declare a target for success and/or a target for failure, and Lambda handles the routing:

| Destination target | Typical use |
|---|---|
| SQS queue | Failed events queued for later reprocessing |
| SNS topic | Fan out a notification about success/failure to multiple subscribers |
| EventBridge event bus | Trigger further downstream workflow based on outcome |
| Another Lambda function | Chain a follow-up function directly on success or failure |

**Poll-based invocations (event source mapping — SQS, Kinesis, DynamoDB Streams)**: retry behavior is governed by the **source's own semantics**, not Lambda's async retry counter.
- **SQS**: a message that fails processing becomes visible again after the queue's visibility timeout expires and is redelivered; after `maxReceiveCount` failed attempts (configured on the queue's redrive policy), it moves to the queue's configured **DLQ**.
- **Kinesis / DynamoDB Streams**: because these are ordered, per-shard streams, a stuck/poison record can **block the entire shard** from making progress until it's resolved. Lambda supports `MaximumRetryAttempts`, `MaximumRecordAgeInSeconds`, and **bisect-on-error** (splitting a failing batch into smaller batches to isolate the bad record) to limit how much a poison record can stall a shard, plus an **on-failure destination** to route the problem batch out of the way.

**Exam trap:** a question describing a scenario where "one bad message is blocking all other messages in a stream from being processed" is testing Kinesis/DynamoDB Streams' ordered, per-shard processing model plus bisect-on-error — this exact stuck-shard scenario doesn't happen with SQS, because SQS delivers messages independently, not in a strict blocking order.

### 13. Accessing private VPC resources from Lambda

By default, a Lambda function runs in an AWS-managed environment with a route straight to the public internet and to other public AWS service endpoints — it has **no path to resources inside your VPC** (a private RDS instance, an internal ElastiCache cluster, an EC2-hosted internal API). To reach those, you must explicitly **attach the Lambda function to your VPC** by specifying subnets and security groups, at which point AWS provisions **elastic network interfaces (ENIs)** in those subnets that the function uses to route traffic.

Two consequences the exam tests directly:

1. **Cold-start implications.** Historically, ENI creation/attachment was slow and could add meaningful cold-start latency to VPC-attached functions. AWS's **Hyperplane ENI** improvement (rolled out in 2019) made ENIs shared and pre-provisioned across functions in the same subnet/security-group combination, dramatically reducing this penalty — but the exam still expects you to know that **VPC attachment is not free of cold-start considerations**, and that this was historically the single biggest reason developers avoided attaching Lambda to a VPC unless they actually needed private resource access.
2. **Losing default internet access.** Once attached to *private* subnets, a Lambda function loses its default internet route and can only reach what those subnets can reach. If the function still needs to call a public API or a public AWS service endpoint (and you're not using a VPC endpoint for that service), the subnet needs a route to a **NAT Gateway** in a public subnet — exactly the same NAT pattern used for any other private-subnet resource that needs outbound-only internet access.

**Exam trap:** "our VPC-attached Lambda function can reach our private RDS instance but times out calling a public third-party API" → the fix is a NAT Gateway (or NAT instance) reachable from the function's subnet route table, **not** re-attaching the function to a public subnet (Lambda functions in a VPC should always use private subnets; a "public" subnet route doesn't grant the function a public IP the way it would for EC2).

### 14. Scalability

Lambda's headline value proposition is scaling concurrency automatically, but the exam wants specific numbers and mechanics, not just "it scales."

- **Concurrent execution scaling**: each simultaneous invocation of your function consumes one unit of **concurrency**. Lambda scales the number of execution environments up to meet demand, subject to a **burst concurrency limit** (an initial pool of 500–3,000 concurrent executions depending on Region) that can absorb a sudden spike immediately, after which concurrency continues to grow by an additional 500 executions per minute until it hits the account's concurrency ceiling.
- **Account concurrency limit**: a soft limit (1,000 by default, increasable via support request) on the total concurrent executions across **all** functions in an account/Region combined — a runaway function can starve every other function in the same account of available concurrency unless reserved concurrency is used to wall it off.
- **Throttling**: once concurrency limits are hit, further invocation attempts are throttled — synchronous callers get a `429 TooManyRequestsException` they must handle/retry; asynchronous invocations and event-source-mapping polls are automatically retried by Lambda/the poller rather than being surfaced as an immediate caller-facing error.
- **Reserved concurrency**, revisited here from the scaling angle: setting it on a function both guarantees that function a slice of the account pool (protecting it from being starved by other functions) and caps it (protecting downstream dependencies, like a relational database that can only handle a limited number of concurrent connections, from being overwhelmed by an unbounded Lambda burst).

### 15. Testing Lambda with AWS tools

Beyond `sam local` (section 7), the Lambda console lets you configure and save named **test events** (sample JSON payloads matching a given trigger shape — an S3 notification, an API Gateway request, etc.) and invoke your function against them directly from the console, viewing the return value, logs, and duration/memory-used report inline. **AWS X-Ray** (full depth in Module 16) can be enabled on a function to trace a request as it flows through Lambda and any downstream AWS service calls, which is invaluable for diagnosing where time is actually being spent across a multi-service, event-driven chain — especially useful once you move past unit testing into integration-level performance debugging.

### 16. Integrating Lambda with other AWS services

Lambda's role in almost every serverless architecture on this exam is as **the glue** — the piece of custom logic that reacts to one service's event and calls into another. A non-exhaustive but exam-relevant map: triggered by **S3** (object created/removed) to process uploads; triggered by **API Gateway** to implement a REST/HTTP API backend; triggered by **DynamoDB Streams** to react to table changes (e.g., replicate to another table, trigger a notification); triggered by **SNS** for fan-out notification handling; triggered/polling **SQS** for decoupled async work; triggered by **EventBridge** rules on a schedule or in response to AWS service events; invoked as a task inside a **Step Functions** state machine; used as a **custom authorizer** for API Gateway; used as a **CloudFormation custom resource** provider. The consistent theme: Lambda rarely stands alone on the exam — nearly every Lambda question is really testing whether you understand the *trigger* and the *downstream call* around it.

### 17. Performance tuning

- **Cold starts** — the latency penalty of the init phase (section 9) on a function's first invocation, or any invocation that lands on a freshly created execution environment. Worse for larger deployment packages, VPC-attached functions (mitigated but not eliminated by Hyperplane ENIs), and heavier runtime initializations (large dependency trees, big SDK imports, JVM/​.NET startup for Java/.NET runtimes vs. lighter Python/Node.js startup).
- **Memory/CPU tradeoff** — revisited from section 11: because CPU scales with memory, a slow, CPU-bound function is often best tuned by *increasing* memory and measuring the actual cost-per-invocation change, not by assuming more memory always costs more overall (faster execution can offset the higher per-ms rate).
- **Provisioned concurrency** — the direct fix for cold starts on latency-sensitive, spiky, or scheduled-traffic workloads (e.g., a customer-facing API with a predictable morning traffic ramp) — pre-warms execution environments ahead of demand rather than reacting to it.
- **Package size optimization** — trim deployment packages to only what's needed at runtime; move shared/heavy dependencies into **layers** so they're not duplicated across every function and (for supported runtimes) can benefit from being cached separately; prefer container images with multi-stage builds to strip build-time-only dependencies for very large functions.
- **Connection reuse** — as shown in section 7, initializing SDK clients, database connections, and other expensive-to-create objects **outside the handler**, at global scope, so warm invocations reuse them instead of re-establishing a connection on every single call.

---

## Worked real-world scenarios

**Scenario A — the double-charged customer.** An e-commerce checkout Lambda function is triggered synchronously via API Gateway, calls a payment processor's API, then writes an order record to DynamoDB. Under load, some requests time out at the API Gateway layer even though the Lambda function actually completed successfully server-side; the frontend, seeing a timeout, automatically retries the checkout request. Customers report being charged twice. The root issue isn't retries themselves — retries are the correct client behavior for a timed-out request — the issue is that **the payment-charging operation isn't idempotent**. The fix: generate an idempotency key client-side per checkout attempt (or use an existing cart/session ID), and before calling the payment processor, perform a DynamoDB conditional put keyed on that idempotency key (exactly the pattern in section 2); if the key already exists, skip straight to returning the stored result instead of charging again. **Lesson:** synchronous invocation with client-side retries is a completely normal pattern — but any side effect it triggers (charging a card, sending an email, decrementing inventory) must be made idempotent, because "the client will retry on failure" is a given, not an edge case.

**Scenario B — the image pipeline that quietly fell behind.** A photo-sharing app processes uploads with a chain: S3 upload triggers a Lambda function that resizes the image into three sizes, writes them back to S3, and updates a DynamoDB record. During a viral traffic spike, the team notices resized images appearing minutes late, and CloudWatch shows the function's concurrent executions pinned at a low, oddly consistent ceiling well below the account's default limit. Investigation reveals another, unrelated function in the same account had been accidentally given **no reserved concurrency limit** and was itself spiking hard, consuming most of the account's shared concurrency pool and starving the image-resize function. The fix: set an explicit **reserved concurrency** on the noisy function (both capping its worst-case burst and guaranteeing the image-resize function its own protected slice of the account pool), and additionally set a modest reserved concurrency floor on the image-resize function itself so it always has guaranteed headroom regardless of what else is happening in the account. **Lesson:** Lambda's concurrency pool is shared account/Region-wide by default — a single misbehaving function can silently starve every other function unless reserved concurrency boundaries are deliberately drawn.

**Scenario C — the Lambda that couldn't reach the internet.** A scheduled Lambda function (triggered by an EventBridge rule every 15 minutes) needs to read a value from a private ElastiCache cluster and then call a public third-party pricing API to enrich the data before writing results to DynamoDB. A developer attaches the function to the VPC's private subnets to reach ElastiCache, and the ElastiCache call works fine — but every invocation now times out on the call to the public pricing API, which worked perfectly before the VPC attachment. This is the exact VPC-and-NAT trap from section 13: attaching to private subnets removed the function's default internet route, and nothing was added to replace it. The fix: add a **NAT Gateway** in a public subnet within the same VPC, and update the private subnets' route table to send `0.0.0.0/0` traffic to it — restoring outbound internet access for the public API call while keeping the function's ENIs (and therefore its access to ElastiCache) inside the private subnets where they belong. **Lesson:** VPC attachment is additive (it grants access to private resources) but also subtractive (it removes the default public internet path) — a function that needs both must have both a private route to internal resources and an explicit NAT path outward.

---

## Key exam traps from this module

- "Decouple the components" / "prevent a slow downstream service from affecting the caller" → insert SQS, SNS, or EventBridge between them; almost never means "add more compute" or "increase timeouts."
- Retries with a fixed delay, or no delay, are never the "best practice" answer when exponential backoff with jitter is available as an option.
- An operation that can be retried (which is nearly all of them, given at-least-once delivery) needs an **idempotency key** check, not just "we added retry logic," to prevent duplicate side effects.
- SQS is poll-based (Lambda's event source mapping polls it) — it is not a push trigger the way S3 or SNS are, even though it "feels" similar in architecture diagrams.
- Sync invocation errors are returned to the caller with **no automatic retry**; async invocations get **two automatic retries**; poll-based sources follow the source's own redelivery/DLQ semantics (SQS visibility timeout + redrive policy; Kinesis/DynamoDB Streams bisect-on-error).
- A stuck/poisoned record blocking an entire shard's progress is a **Kinesis/DynamoDB Streams**-specific failure mode (ordered, per-shard processing) — it doesn't happen with SQS.
- Lambda's hard timeout ceiling is **15 minutes** — anything longer needs ECS/Fargate, AWS Batch, or a Step Functions workflow breaking the job into smaller steps, not a single Lambda invocation.
- Memory is the only lever you set directly on Lambda — CPU and network throughput scale automatically **with** memory, so a slow CPU-bound function is often fixed by raising memory, not by "optimizing code" first.
- VPC-attaching a Lambda function grants access to private resources but **removes default internet access**; restoring outbound internet access requires a NAT Gateway on the route out of the private subnet.
- Cold starts are mitigated (not caused) by Hyperplane ENIs for VPC-attached functions, and are directly solved for latency-sensitive workloads by **provisioned concurrency**, not by raising memory alone.
- Reserved concurrency both protects a function's guaranteed capacity and caps its maximum burst — remember it's a double-edged setting, useful both for "protect this function" and "protect this function's downstream dependency from being overwhelmed" scenarios.
- "Least operational overhead" plus "event-driven" plus "unpredictable/bursty" together are the strongest combined signal on this exam that Lambda (not EC2, not a fixed-size container service) is the intended answer.
