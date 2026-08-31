# Module 07 — Step Functions & Orchestration

Domain focus: primarily **Development with AWS Services (32%)** — Step Functions is the exam's flagship answer whenever a scenario needs to coordinate multiple AWS services in a defined sequence, with visibility, retries, and error handling built in rather than hand-rolled. It also carries the exam's explicit **orchestration vs. choreography** architectural-pattern distinction (Domain 1.1), and touches Deployment (Domain 3) lightly through CloudFormation/SAM-managed state machines, which gets full depth in module 13. By day 4 of the sprint you already know Lambda (module 04) and SQS/SNS/EventBridge (module 06) — Step Functions is the piece that ties those primitives into a single, coordinated, debuggable workflow.

## 1. What Step Functions actually is

AWS Step Functions is a fully managed **orchestration service**: you define a **state machine** — a sequence of steps ("states") with explicit transitions, branching logic, parallelism, and error handling — and Step Functions executes it, tracking exactly which state is active, what data is flowing through it, and what happened at every step. Contrast this with wiring services together yourself with Lambda functions calling other Lambda functions, or chaining SQS queues and EventBridge rules: that approach works, but the "what's the current state of this business process, and what failed" question becomes something you have to reconstruct from scattered logs. Step Functions makes the workflow itself a first-class, inspectable resource.

A state machine is defined in the **Amazon States Language (ASL)** — a JSON-based, declarative language. You are not writing imperative code that says "call this, then call that"; you're describing a graph of states and how execution should move between them, including what happens on success, on specific errors, and on timeout. The state machine definition is itself deployable infrastructure (often via CloudFormation or SAM — see module 13), which is exactly why the exam frames Step Functions as a Deployment-domain topic too, not just a Development-domain one.

**Why this matters for the exam:** whenever a scenario describes multiple steps that must happen *in order*, with conditional branching, needing to survive partial failures, needing a human approval step, or needing built-in retry/backoff without you writing that logic yourself — Step Functions is very often the correct answer, ahead of "chain Lambda functions together" or "use SQS to pass messages between services."

## 2. Core building block: states and the ASL

Every state machine has a `StartAt` field naming the first state, and a `States` object mapping state names to their definitions. Each state has a `Type`, and (except for terminal states) a `Next` field pointing to the following state, or an `End: true` flag marking it as the last state in that branch.

### The state types you must know

| State Type | Purpose |
|---|---|
| **Task** | Does actual work — invokes a Lambda function, calls another AWS service directly via an SDK integration, or coordinates an activity worker. This is where business logic executes. |
| **Choice** | Branching logic — evaluates conditions against the current state's input data and routes execution to different next states based on the result (like an if/else or switch statement). |
| **Parallel** | Executes multiple fixed branches of states concurrently within the same execution, waiting for all branches to complete before moving on. Good for a known, fixed number of independent sub-workflows. |
| **Map** | Iterates over an array in the input, running the same set of states once per array element — either concurrently (up to a configurable concurrency) or sequentially. Good for a variable-length collection (unlike Parallel's fixed branches). |
| **Wait** | Pauses execution for a specified duration or until a specified timestamp before continuing — no compute is consumed while waiting. |
| **Pass** | Passes its input to its output, optionally transforming or injecting data, without doing any real work. Useful for reshaping data, mocking a step during development, or injecting static values. |
| **Succeed** | Stops the execution successfully — a clean terminal "this branch/workflow finished" marker. |
| **Fail** | Stops the execution and marks it as failed, with a custom `Error` and `Cause` you define — used for explicit business-logic failures (e.g., "validation failed"), distinct from an unhandled runtime exception. |

**Exam trap:** Map is for iterating over a *variable-length array* (e.g., "process every item in this order," where the number of items isn't known until runtime). Parallel is for a *fixed, known number* of different branches doing different things (e.g., "check inventory AND charge payment AND reserve shipping, simultaneously"). Confusing these two is a common distractor pattern — if the scenario says "for each file in the batch" or "for every record in the array," that's Map; if it says "do these three specific, different things at the same time," that's Parallel.

## 3. Standard vs. Express workflows

Step Functions offers two workflow types, chosen when you create the state machine, and this comparison is one of the most heavily tested facts in this module.

| Aspect | **Standard Workflows** | **Express Workflows** |
|---|---|---|
| Execution semantics | **Exactly-once** — each step runs once, cleanly | **At-least-once** — a step could run more than once under failure conditions, so steps should be idempotent |
| Max duration | Up to **1 year** | Up to **5 minutes** |
| Execution history | Full, detailed execution history retained and viewable per-execution in the console (list of every state transition, input/output at each step) | No per-execution history in the console by default; you enable **CloudWatch Logs** for execution data instead |
| Pricing model | Priced **per state transition** | Priced **per execution** (based on number of invocations, duration, and memory consumed) |
| Best fit | Long-running, auditable, often human-involved workflows: order processing, approval chains, ETL orchestration | High-volume, high-throughput, short-duration event processing: IoT telemetry ingestion, streaming data transformation, mobile-backend request processing |
| Throughput character | Lower-throughput, transition-priced — cost scales with how many discrete steps a single execution takes | Built for very high execution volume — cost scales with executions and duration, not step count |

**Exam trap:** "Exactly-once" vs. "at-least-once" is the semantic detail the exam loves to test with a scenario like "a payment must never be double-charged, and the workflow runs for up to 20 minutes" → **Standard** (exactly-once, well within the 1-year cap). Compare to "a company ingests millions of IoT sensor events per day, each needing a short transformation workflow lasting a few seconds" → **Express** (high volume, short duration, at-least-once is acceptable because the transformation Lambda is idempotent). If a scenario needs exactly-once guarantees, Express is disqualified outright regardless of how well it fits everything else.

## 4. Error handling: Retry and Catch

This is where Step Functions earns its keep versus hand-rolled orchestration — retry-with-backoff and structured error handling are declarative, built into the state definition, not code you write yourself.

### Retry
A `Retry` array on a Task, Parallel, or Map state lists one or more retry rules, each matching specific errors and defining backoff behavior:

```json
"Retry": [
  {
    "ErrorEquals": ["States.Timeout", "Lambda.ServiceException"],
    "IntervalSeconds": 2,
    "MaxAttempts": 3,
    "BackoffRate": 2.0
  }
]
```

- `ErrorEquals` — the specific error name(s) this rule handles (AWS-predefined names like `States.Timeout`, `States.TaskFailed`, `Lambda.ServiceException`, or custom error strings your Lambda function throws), or `States.ALL` to catch anything.
- `IntervalSeconds` — how long to wait before the first retry.
- `MaxAttempts` — how many retry attempts to make (not counting the original attempt) before giving up and treating it as a failure the state's `Catch` block (if any) can handle.
- `BackoffRate` — a multiplier applied to the interval after each retry (e.g., `2.0` doubles the wait each time: 2s, 4s, 8s...).
- Newer state machines also support a `JitterStrategy` (`FULL` or `NONE`) to randomize the exact wait within the backoff window, avoiding the "thundering herd" problem where many failed executions retry at the exact same moment.

This is **the exact same exponential-backoff-and-jitter concept from module 04's Lambda/SDK retry discussion** — Step Functions just gives you a declarative way to configure it at the workflow level instead of writing retry loops in application code.

### Catch
A `Catch` array defines what to do when a state fails outright (either the underlying error isn't retried, or all retries are exhausted):

```json
"Catch": [
  {
    "ErrorEquals": ["States.ALL"],
    "ResultPath": "$.error",
    "Next": "NotifyFailure"
  }
]
```

- `ErrorEquals` — which errors this catch handles (you can have multiple `Catch` entries targeting different errors to different fallback states).
- `Next` — which state to transition to on catching the error (a cleanup step, a notification, a compensating "rollback" action).
- `ResultPath` — where to inject the error details into the state's data, so downstream states can inspect what went wrong.

**Exam trap:** `Retry` handles *transient* failures by trying again; `Catch` handles the case where retrying either isn't appropriate or has been exhausted, by routing to a different state (often a cleanup/compensation/notification path) rather than failing the entire execution outright. A state can have both: retry a few times, and only if all retries fail, catch and route to a fallback.

## 5. Integration patterns

Step Functions Task states can integrate with the outside world in a few distinct ways:

1. **Lambda invocation** — the most common pattern; a Task state invokes a Lambda function (either via the legacy `Resource: "arn:aws:lambda:...:function:Name"` shorthand or the recommended `Resource: "arn:aws:states:::lambda:invoke"` with explicit `Parameters`).
2. **Direct AWS SDK service integrations** — Step Functions can call over 200 AWS services' APIs *directly* from a Task state, with no Lambda function in between — e.g., putting an item into DynamoDB, publishing to SNS, sending to SQS, starting an ECS task, or calling Batch. This reduces cost, latency, and the amount of glue code you'd otherwise write in a "do-nothing" Lambda function whose only job is calling another AWS API.
3. **Activity workers** — a legacy-but-still-valid pattern where a worker process (running anywhere — EC2, on-premises, a container) polls Step Functions for work using the Activity Task API, does the work itself, and reports success/failure back. Useful when the work must happen outside AWS-managed compute (e.g., on a physical device or a long-running custom process not well suited to Lambda).
4. **Wait for callback with a task token (`.waitForTaskToken`)** — the pattern for **human-in-the-loop** or **long-running external work** that doesn't fit neatly into a synchronous call. The Task state pauses and waits (up to that workflow's max duration) until *something else* calls back to Step Functions with a **task token** via `SendTaskSuccess`, `SendTaskFailure`, or `SendTaskHeartbeat`. Common uses: an approval step where a manager clicks a link in an email (the link's backend calls `SendTaskSuccess` with the token), or a long-running third-party job (e.g., a video encoding service) that calls back only when it's genuinely done, rather than Step Functions polling it.

**Exam trap:** "A workflow must pause until a human approves a request, potentially hours or days later" → this is the textbook signal for the **`.waitForTaskToken`** integration pattern, not a `Wait` state (which only pauses for a *known* duration/timestamp, not an arbitrary external event) and not a tight polling loop.

## 6. The Map state for parallel iteration

The Map state runs the same sub-workflow once per element of an input array. Two execution modes:

- **Inline Map** (the "classic" Map state) — runs iterations within the state machine's own execution, with a configurable `MaxConcurrency` to control how many iterations run at once (0 means "as much concurrency as possible").
- **Distributed Map** — a newer mode designed for very large-scale fan-out (tens of thousands to millions of items, e.g. every object in an S3 bucket), where each iteration runs as its own separate, trackable child execution rather than inline, giving much higher scale and per-item observability at the cost of some added complexity.

A basic Map state:

```json
"ProcessEachLineItem": {
  "Type": "Map",
  "ItemsPath": "$.orderItems",
  "MaxConcurrency": 5,
  "Iterator": {
    "StartAt": "ValidateLineItem",
    "States": {
      "ValidateLineItem": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ValidateLineItem",
        "End": true
      }
    }
  },
  "ResultPath": "$.validatedItems",
  "Next": "ShipOrder"
}
```

**Exam trap:** if a scenario says the number of items to process is only known at runtime (a variable-length array from the input, or every object under an S3 prefix), that's Map — often Distributed Map at real scale. If it says a fixed, small number of *different, named* operations must happen concurrently, that's Parallel.

## 7. Input/output processing: InputPath, Parameters, ResultPath, OutputPath

This is the part of ASL that trips up almost everyone at first, because four different fields all touch "the data," but at different points in a state's execution:

1. **`InputPath`** — filters what part of the *incoming* state data the state actually receives, before it does anything. Default `$` (the whole input).
2. **`Parameters`** — reshapes or constructs the exact payload sent to the state's task/resource, which can mix static values, values pulled from the (already-InputPath-filtered) input via a `.$` suffixed key (e.g., `"orderId.$": "$.orderId"`), and intrinsic functions (e.g., `States.Format`).
3. **`ResultPath`** — determines *where in the original state data* the task's result gets placed. Default `$` means the result *replaces* the entire input. Setting it to something like `$.taskResult` instead *merges* the result into the input as a new field, preserving everything else that was already there — critical when a later state still needs the earlier data.
4. **`OutputPath`** — filters what part of the (post-`ResultPath`) combined data gets passed on to the *next* state as its input. Default `$` (everything).

Worked example — a Task state receiving `{"orderId": "5521", "customer": {"id": "c-9"}}`:

- With no `ResultPath` set (default `$`), if `ValidateOrder` returns `{"isValid": true}`, the *entire* state data becomes `{"isValid": true}` — the original `orderId` and `customer` are gone, which breaks any later state that needed them.
- With `"ResultPath": "$.validation"`, the state data becomes `{"orderId": "5521", "customer": {"id": "c-9"}, "validation": {"isValid": true}}` — nothing is lost, and the next state's Choice logic can test `$.validation.isValid`.

**Exam trap:** a scenario describing "a later state in the workflow lost access to data it needed from an earlier step" is almost always pointing at a missing or wrong `ResultPath` — the default behavior replaces the entire input with the task's result, silently discarding everything else, unless you explicitly merge with a `ResultPath`.

## 8. A complete worked ASL example

The following state machine validates an order, branches on validity, then fans out into a `Parallel` state to reserve inventory and charge payment simultaneously — with a `Retry` on the payment call (transient gateway errors) and a `Catch` that routes any failure to a rollback/notification path:

```json
{
  "Comment": "Order processing: validate, branch, then parallel inventory + payment with retry/catch",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "ValidateOrder",
        "Payload.$": "$"
      },
      "ResultPath": "$.validation",
      "Retry": [
        {
          "ErrorEquals": ["Lambda.ServiceException", "States.Timeout"],
          "IntervalSeconds": 2,
          "MaxAttempts": 3,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "NotifyFailure"
        }
      ],
      "Next": "IsOrderValid"
    },
    "IsOrderValid": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.validation.Payload.isValid",
          "BooleanEquals": true,
          "Next": "ReserveAndCharge"
        }
      ],
      "Default": "NotifyFailure"
    },
    "ReserveAndCharge": {
      "Type": "Parallel",
      "ResultPath": "$.parallelResults",
      "Branches": [
        {
          "StartAt": "ReserveInventory",
          "States": {
            "ReserveInventory": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": { "FunctionName": "ReserveInventory", "Payload.$": "$" },
              "End": true
            }
          }
        },
        {
          "StartAt": "ChargePayment",
          "States": {
            "ChargePayment": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": { "FunctionName": "ChargePayment", "Payload.$": "$" },
              "Retry": [
                {
                  "ErrorEquals": ["States.Timeout", "PaymentGateway.ThrottlingException"],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 5,
                  "BackoffRate": 2.0,
                  "JitterStrategy": "FULL"
                }
              ],
              "End": true
            }
          }
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "RollbackOrder"
        }
      ],
      "Next": "ShipOrder"
    },
    "ShipOrder": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": { "FunctionName": "ShipOrder", "Payload.$": "$" },
      "End": true
    },
    "RollbackOrder": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": { "FunctionName": "RollbackOrder", "Payload.$": "$" },
      "Next": "NotifyFailure"
    },
    "NotifyFailure": {
      "Type": "Fail",
      "Error": "OrderProcessingFailed",
      "Cause": "Order validation or processing could not complete successfully"
    }
  }
}
```

Notice every concept from this module in one place: a `Task` with `Retry` and `Catch`, a `Choice` branching on the result, a `Parallel` fan-out with its own per-branch `Retry` and shared `Catch`, and explicit `ResultPath`/`Parameters` usage keeping the data intact as it flows through.

## 9. Orchestration vs. choreography — the design-pattern decision

This is an explicit architectural-pattern distinction the exam tests directly (Domain 1, Task Statement 1 — architectural patterns), and it's the natural companion to module 04's broader pattern catalogue and module 06's event-driven services.

| Aspect | **Orchestration** (Step Functions) | **Choreography** (EventBridge) |
|---|---|---|
| Control model | A **central coordinator** (the state machine) explicitly defines the sequence, branching, and error handling for every step | **No central controller** — each service independently reacts to events it cares about, publishing further events as needed |
| Visibility | One place to see the whole workflow's status, execution history, and current state | Distributed by nature — understanding the full flow means tracing across many independently-deployed consumers and their logs |
| Coupling | Services are decoupled from *each other*, but the workflow definition is coupled to *knowing about every step* | Services are decoupled from each other *and* from any central definition — a publisher doesn't know or care who's listening |
| Adding a new step | Requires editing the central state machine definition | A new consumer simply subscribes to an existing event — no change needed to the publisher or any other consumer |
| Failure handling | Centralized `Retry`/`Catch` at the state-machine level, with a single execution to inspect | Each consumer handles its own retries/failures independently (e.g., its own SQS dead-letter queue) |
| Best fit | Complex, ordered, stateful business processes: order fulfillment, approval chains, multi-step data pipelines, anything needing an audit trail of "what happened, in what order" | Simple, independent reactions to domain events where strict ordering isn't required: "when an order ships, notify billing AND update analytics AND alert the warehouse," each independently, with no single process needing to track them all |

**Exam trap:** a scenario describing a workflow that must be strictly sequential, needs conditional branching, needs a visual audit trail of exactly what happened and in what order, or needs a human approval step — that's **orchestration → Step Functions**. A scenario describing multiple *independent* services each reacting to the same business event without needing to know about each other, and where the order between them genuinely doesn't matter — that's **choreography → EventBridge**. If the scenario explicitly needs centralized error handling and a single place to see workflow status, that phrase alone should pull you toward Step Functions even if EventBridge could technically also route the events.

## 10. Visual debugging via the console

Every Standard Workflow execution can be inspected in the Step Functions console as a **visual graph** of the state machine, with the actual path taken through it highlighted, and the exact input/output JSON at every single state available for inspection. This turns "why did this workflow fail" from a log-archaeology exercise into clicking the red (failed) state and reading its error and input directly. Express Workflows rely on CloudWatch Logs for this instead, since they don't retain the same kind of per-execution history by default — another reason Express is a worse fit when deep, ongoing auditability matters more than raw throughput.

## 11. Deployment: a brief forward-look to module 13

State machines are just another resource you can define as code. In CloudFormation, `AWS::StepFunctions::StateMachine` takes the ASL definition (inline or referencing an S3 object); AWS SAM has a dedicated `AWS::Serverless::StateMachine` resource type with a friendlier authoring experience for ASL alongside your Lambda functions in the same template. Step Functions also supports **versions and aliases** for a state machine (conceptually similar to Lambda versions/aliases), letting you publish an immutable version of a definition and shift execution traffic between versions gradually. Full CI/CD and IaC treatment of this lives in module 13 — for now, just know that "how do I deploy and version a Step Functions workflow safely" is a CloudFormation/SAM answer, not a manual console-editing one.

## 12. Use cases worth memorizing

- **Order processing** — validate, reserve inventory, charge payment, ship, with compensating rollback logic on failure (the worked example above).
- **Data pipelines / ETL** — coordinate a sequence of Glue jobs, Lambda transformations, and Athena queries, using Map to fan out over many files or partitions.
- **Approval workflows** — human-in-the-loop processes (expense approval, document review, content moderation escalation) using the `.waitForTaskToken` pattern, potentially pausing for hours or days.

## 13. Worked real-world scenarios

**Scenario A — the double-charged customer.** A retail company originally chained their order-processing steps with a sequence of Lambda functions, each invoking the next directly. During a regional network blip, a payment-charging Lambda function was invoked twice for the same order because an upstream retry mechanism (build outside Step Functions) didn't know the first invocation had actually succeeded just before the connection dropped — the customer was billed twice. Migrating this workflow to a Step Functions **Standard** workflow (exactly-once execution semantics) around the same Lambda functions, with explicit `Retry`/`Catch` blocks replacing the ad hoc retry code, eliminates this class of bug: Step Functions itself guarantees each state executes exactly once per execution, and any transient failure is handled by a declared, auditable `Retry` policy rather than an unreliable, hand-rolled loop. **Lesson:** "must never double-charge" is a strong signal for Standard workflows' exactly-once guarantee, not just "use Step Functions" generically — Express would have been the wrong choice here.

**Scenario B — the expense report that waited three days.** A company's expense-approval process needs a manager to review and approve or reject a submitted report, sometimes not for a day or two given normal scheduling. The team's first attempt used a `Wait` state with a fixed retry-poll loop, checking every few minutes whether an external "approvals" DynamoDB table had been updated — burning needless state transitions and adding complexity for no benefit. Switching the approval step to a Task state using the **`.waitForTaskToken`** integration pattern lets the execution pause indefinitely (well within Standard's 1-year cap) with zero polling cost; the state resumes the instant the manager clicks "Approve" in an email link, whose backend Lambda function calls `SendTaskSuccess` with the token, carrying the manager's decision as the task's result. **Lesson:** an arbitrary-duration wait for an external human or system decision is the callback-token pattern, not a polling loop or a `Wait` state (which only handles a *known* duration or timestamp).

**Scenario C — the thumbnail pipeline that needed both speed and scale.** A photo-sharing company processes millions of newly uploaded images per day, generating three thumbnail sizes for each, and wants the lowest possible per-image cost and highest possible throughput, tolerating the rare double-processed image (their thumbnail-generation Lambda function is idempotent — regenerating the same thumbnail twice is harmless). This is an **Express** workflow, not Standard: the work per image completes in a few seconds (well under Express's 5-minute cap), volume is enormous (favoring per-execution, not per-state-transition, pricing), and at-least-once semantics are acceptable given the idempotent processing step. Within that Express workflow, a **Map** state (potentially Distributed Map if fed a batch manifest rather than one image per execution) fans out the three thumbnail-size generations concurrently per image. **Lesson:** high-volume + short-duration + tolerable-duplicate-processing is the Express signal; the same requirements phrased as "must never process twice" and "can run for tens of minutes" would flip the answer to Standard.

## Key exam traps

- **Standard = exactly-once, up to 1 year, priced per state transition, full console execution history.** **Express = at-least-once, up to 5 minutes, priced per execution, relies on CloudWatch Logs.** "Must never double-process" always eliminates Express.
- **Map** iterates a variable-length array (unknown count until runtime); **Parallel** runs a fixed, known number of different branches concurrently. Don't swap them.
- **`Retry`** handles transient errors by trying again with backoff (optionally with jitter, same backoff-and-jitter concept from module 04); **`Catch`** handles a state failing outright (after retries are exhausted, or for non-retried errors) by routing to a fallback/cleanup state.
- **`.waitForTaskToken`** is the pattern for human-in-the-loop approval or long-running external work of arbitrary/unknown duration — not a `Wait` state (fixed duration/timestamp only) and not a polling loop.
- **`ResultPath`** defaults to replacing the entire state's data with the task's result — a classic "later state lost data it needed" bug is almost always a missing or wrong `ResultPath`.
- **Orchestration (Step Functions)** = central coordinator, explicit sequence, single place to see workflow status — best for complex, ordered, auditable processes. **Choreography (EventBridge)** = no central controller, independent reactions to events — best for simple, decoupled, order-independent reactions. A requirement for centralized visibility/error-handling across steps pulls the answer toward Step Functions even when EventBridge could technically route the same events.
- Direct AWS SDK service integrations from a Task state can eliminate "glue" Lambda functions whose only job is calling another AWS API — the exam favors this over an unnecessary Lambda function in the middle when the scenario doesn't need custom logic, just a service call.
- State machines are deployed as code (CloudFormation `AWS::StepFunctions::StateMachine` or SAM `AWS::Serverless::StateMachine`), and support versions/aliases for safer rollout — full depth in module 13.
