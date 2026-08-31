# Module 07 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Step Functions Fundamentals & ASL Basics (1–16)

1. A company is coordinating a multi-step order fulfillment process across several Lambda functions and wants a single place to see which step is currently executing, what data each step received, and why any step failed. Which AWS service is purpose-built for this kind of centrally coordinated, inspectable workflow?
A) Amazon EventBridge
B) AWS Step Functions
C) Amazon SQS
D) AWS CloudTrail

2. A developer is authoring a new state machine definition in the Amazon States Language (ASL) and needs to specify exactly which state begins execution when the workflow starts. Which top-level field in the definition identifies that first state?
A) "InitialState"
B) "EntryPoint"
C) "StartAt"
D) "FirstState"

3. A developer is writing a new Step Functions state machine and needs every non-terminal state to indicate what happens once it finishes, while terminal states need to mark themselves as the end of their branch. Which two ASL mechanisms accomplish this? (Select TWO)
A) A "Next" field naming the following state
B) An "End": true flag marking the state as the last one in its branch
C) A "GoTo" statement embedded in the state's Comment field
D) An implicit fallthrough to the next state listed alphabetically
E) A required numeric "Sequence" field on every state

4. A new team member asks a senior developer to describe, in one sentence, what a Step Functions state machine definition actually is as an artifact. Which description is most accurate?
A) A compiled binary artifact uploaded directly to Lambda
B) A declarative, JSON-based document written in the Amazon States Language describing states and the transitions between them
C) A Python script that Step Functions interprets line by line at runtime
D) A CloudFormation template exclusively, with no other authoring format available

5. A company currently chains five Lambda functions together, with each function directly invoking the next as its final action, to implement a business process. An architect proposes migrating this chain to a Step Functions state machine instead. Which justification best supports that migration?
A) Lambda functions cannot call other Lambda functions under any circumstance
B) Step Functions provides centralized execution visibility, built-in retry and error handling, and a visual workflow representation that ad hoc function chaining lacks
C) Step Functions eliminates the need for any IAM permissions on the workflow
D) Lambda functions are limited to exactly one invocation per AWS account

6. A developer starts a Step Functions state machine multiple times with different order IDs as input, and wants to understand what uniquely identifies one specific run of that state machine, including its own history and outcome. What is this concept called in Step Functions?
A) A cold start
B) An execution — one complete run of the state machine, from its start state to a terminal state, with its own unique ID and history
C) A CloudFormation stack deployment
D) A permanently running background process

7. A support engineer is troubleshooting a single failed run of an order-processing state machine and wants to see the exact JSON input and output at each state that run passed through, alongside a visual diagram highlighting the path taken. Where should the engineer look first?
A) Raw Lambda function logs only, with no Step Functions-specific view available
B) The Step Functions console's execution detail view for that specific execution
C) The EC2 instance metadata service
D) A manually configured S3 bucket storing execution snapshots

8. A developer reviewing a colleague's draft ASL definition is checking which fields are legitimate on a state. Which of the following is NOT a valid top-level field typically found on an ASL state definition?
A) "Type"
B) "Next"
C) "Resource"
D) "DockerImage"

9. A junior developer asks why ASL is described as "declarative" rather than "imperative," having only written procedural code before. Which explanation is most accurate?
A) ASL describes the desired states and transitions between them, and Step Functions determines how to execute that graph, rather than the author writing step-by-step procedural instructions
B) ASL is declarative purely because it is written in YAML instead of JSON
C) ASL is declarative because it has no branching logic of any kind
D) ASL is declarative only when used inside Express workflows

10. A security review is examining how a newly created Step Functions state machine gains permission to invoke the Lambda functions listed in its Task states. Which two statements about this relationship are accurate? (Select TWO)
A) A state machine executes under an IAM role that must grant permission to invoke the resources referenced in its Task states
B) Without adequate permissions on its execution role, a Task state's calls to Lambda or other services will fail with an access-related error
C) Step Functions state machines never require any IAM role to operate
D) The execution role's permissions are irrelevant as long as the calling human user has administrator access
E) IAM roles cannot be attached to state machines, only to Lambda functions directly

11. A retail company's checkout workflow needs to branch differently depending on whether an order's total exceeds $1,000, routing high-value orders to a manager-approval path and everything else to standard processing. Which ASL state type implements this conditional branching?
A) Task
B) Choice
C) Pass
D) Wait

12. An architect is justifying, to a skeptical stakeholder, why Step Functions was chosen over simply chaining Lambda invocations through a sequence of EventBridge rules for a process requiring strict step ordering, visual execution tracking, and centralized retry handling. Which explanation best supports that choice?
A) EventBridge is fundamentally incapable of invoking Lambda functions
B) Step Functions is specifically designed for orchestrated, stateful, ordered workflows with built-in execution tracking, while EventBridge is designed for decoupled, independent event reactions with no central coordinator
C) EventBridge is always more expensive than Step Functions regardless of workload
D) Step Functions is incapable of invoking Lambda functions as a target

13. A financial services company's compliance team requires proof of the exact sequence of steps a loan-approval process took, including timestamps and the data present at each step, for a recent audit. Which Step Functions capability most directly satisfies this requirement?
A) A Lambda function's own internal print statements
B) The state machine's execution history, viewable per-execution for a Standard workflow
C) EC2 instance metadata retrieved at runtime
D) A manually maintained spreadsheet updated by the operations team

14. A developer new to Step Functions asks a colleague to clarify the difference between "the state machine" and "an execution of the state machine," since both terms keep appearing in documentation. Which explanation is correct?
A) They are the same thing, simply referred to by two different names
B) The state machine is the reusable definition (the ASL document); an execution is one specific run of that definition, with its own input, output, and history
C) A given state machine can only ever be executed a single time, ever
D) An execution defines the states themselves, while the state machine is only the resulting output data

15. A developer wants to attach a short, human-readable explanation to a particular state purely for documentation purposes, with no effect on how the state actually executes. Which ASL field is appropriate for this?
A) "Type"
B) "Comment"
C) "Next"
D) "Resource"

16. A platform team is deciding how to author and deploy their organization's Step Functions state machines going forward, favoring approaches that fit into their existing infrastructure-as-code practices. Which two statements about how state machines are typically created and managed are accurate? (Select TWO)
A) They can be authored and deployed directly through the Step Functions console for quick, manual iteration
B) They can be defined as code and deployed through CloudFormation or AWS SAM alongside the Lambda functions they invoke
C) They must always be typed by hand directly into a production account, with no other authoring method available
D) A given AWS account can contain only a single state machine, globally, across all Regions
E) They require a dedicated, always-on EC2 instance to host the definition file

### State Types Deep Dive (17–36)

17. A data-processing workflow needs to run identical validation logic once for each line item in an order, where the exact number of line items is unknown until the workflow actually starts and varies order to order. Which ASL state type is designed for this variable-length iteration?
A) Parallel
B) Map
C) Choice
D) Wait

18. An order-processing workflow needs to simultaneously check inventory availability, verify a shipping address, and pre-authorize a customer's payment method — three distinct, unrelated operations that must all run concurrently before the workflow proceeds further. Which ASL state type fits this fixed, known set of concurrent branches?
A) Map
B) Parallel
C) Pass
D) Succeed

19. A team is still building out a workflow and one downstream Lambda function isn't implemented yet, but they want to test the rest of the branching logic now using a hardcoded stand-in value. Which ASL state type performs no real work itself and can inject static or reshaped data for exactly this purpose?
A) Task
B) Wait
C) Pass
D) Fail

20. A workflow must pause for exactly ten minutes, with no external work happening during that time, before moving on to the next processing step. Which ASL state type is designed for this pure, time-based delay?
A) Wait
B) Pass
C) Task
D) Choice

21. A workflow's business logic determines that an incoming request is invalid and that the execution should terminate immediately as a failure, recording a custom error name and human-readable cause for later review. Which ASL state type is appropriate for this explicit failure termination?
A) Succeed
B) Fail
C) Pass
D) Wait

22. A workflow branch finishes its work correctly and the author wants to mark that branch as a clean, successful termination point, distinct from simply letting the last Task state end the branch. Which ASL state type is designed for this?
A) Succeed
B) Fail
C) Wait
D) Choice

23. A developer configuring a Task state's "Resource" field wants to know the range of valid values it can reference. Which of the following correctly describes this field's flexibility?
A) It can only ever reference a Lambda function ARN, with no other options
B) It can reference a Lambda function ARN, an AWS SDK service integration ARN (such as "arn:aws:states:::dynamodb:putItem"), or an Activity ARN, among other supported resource types
C) It can only reference an S3 bucket ARN
D) It can only reference an EC2 instance ID

24. Two developers disagree about when to use Map versus Parallel in a new workflow. Which two statements correctly distinguish the two state types? (Select TWO)
A) Map iterates dynamically over the elements of an input array, running the same sub-workflow once per element
B) Parallel executes a fixed, explicitly authored set of different branches concurrently
C) Map and Parallel are functionally identical and fully interchangeable in every scenario
D) Parallel automatically adjusts its number of branches based on the input array's length at runtime
E) Map requires manually authoring one branch in advance for every possible array element

25. A Choice state routes execution to "HighValueApproval" when an order's total is greater than or equal to 1,000, and otherwise should route to "StandardProcessing." Which ASL construct handles this "otherwise" case when none of the explicit Choice rules match?
A) A second Choice state chained immediately afterward
B) The "Default" field on the Choice state
C) A Catch block attached to the Choice state
D) A Wait state configured with a zero-second duration

26. A developer reviewing a colleague's Choice state condition rules is checking which comparison operators are legitimate ASL constructs. Which of the following would NOT typically appear as a Choice state comparison operator?
A) NumericGreaterThan
B) StringEquals
C) BooleanEquals
D) SqlWhereClause

27. A Parallel state's three branches all complete successfully during an execution. Which two statements correctly describe the resulting output of that Parallel state? (Select TWO)
A) The results of all branches are combined into a single array, one element per branch, which becomes the Parallel state's output subject to ResultPath
B) The order of elements in the output array corresponds to the order the branches were defined in the state definition, not necessarily the order in which they finished
C) Only the last branch to finish contributes to the output, with earlier branches' results discarded
D) The Parallel state produces no output at all unless a Catch block happens to be triggered
E) All branches must return byte-for-byte identical output, or the array cannot be constructed

28. One branch of a Parallel state fails after exhausting its own retries, and the Parallel state itself has no Catch block configured. What is the typical outcome for the overall Parallel state?
A) The other branches continue running independently and the failure is silently ignored
B) The Parallel state as a whole fails, since an uncaught failure in any branch propagates to the parent state
C) Only the failed branch is retried indefinitely by default
D) The Parallel state automatically converts itself into a Map state

29. A developer is categorizing ASL state types by whether they primarily control workflow structure versus perform I/O with external resources. Which two state types are best described as controlling flow rather than performing external I/O? (Select TWO)
A) Choice
B) Pass
C) Task
D) Map
E) None of the state types control flow without also performing I/O

30. A team wants to temporarily stand in for a not-yet-built Lambda function with a fixed sample response, purely so the rest of the workflow's branching logic can be tested before that function is finished. Which ASL state type is best suited to this stub?
A) A Pass state with a static "Result" field standing in for the eventual Task output
B) A Wait state configured with an unbounded duration
C) A Fail state
D) A Map state configured to iterate zero times

31. A developer is reviewing a Task state and notices an "End": true field instead of a "Next" field. What does this field indicate?
A) It specifies how long the task is allowed to run before timing out
B) It marks the state as the final state in its branch, meaning no "Next" transition follows it
C) It disables all retries configured on that state
D) It is a required field on every single state in a state machine, including non-terminal ones

32. A Choice state has three explicit condition rules but no "Default" field configured. During an execution, the incoming data matches none of the three rules. What happens next?
A) The workflow silently proceeds to whichever state happens to be listed first alphabetically
B) The execution fails with a runtime error, since a Choice state without a matching rule and no Default has no valid path forward
C) The workflow pauses indefinitely, awaiting manual operator intervention
D) The Choice state automatically defaults to a Succeed state

33. A data engineering team is evaluating Map state capabilities for a workload that may eventually need to process hundreds of thousands of individual files. Which two statements about Map state iteration are accurate? (Select TWO)
A) Iterations can run with a configurable maximum concurrency to control how many run at the same time
B) Distributed Map is designed to support very large-scale fan-out, such as processing every object under an S3 prefix, as separately trackable child executions
C) A Map state can only ever process exactly one item at a time, with no concurrency option available
D) Map states cannot contain a Task state anywhere within their iterator or item processor
E) Map states are only available inside Express workflows, never Standard workflows

34. A workflow needs to send a notification and then immediately and cleanly end that branch, with no further processing required afterward. Which combination of ASL state types most directly and idiomatically achieves "notify, then cleanly terminate"?
A) A Task state that sends the notification, followed by a Succeed state
B) A Wait state followed immediately by a Fail state
C) A Choice state configured with no branches
D) A Parallel state containing a single empty branch

35. A developer asks whether adding a "Comment" field to several states in a state machine could accidentally change how the workflow behaves at runtime. What is the correct answer?
A) Yes, "Comment" can alter transition logic depending on its content
B) No, "Comment" is a purely descriptive, human-readable annotation with no effect on execution
C) Yes, but only on Task states specifically
D) "Comment" actually defines the retry interval for the state it's attached to

36. An image-processing pipeline handles a batch of uploaded photos where the exact number of photos varies from batch to batch, and each photo needs the identical resize-and-tag sub-workflow applied independently. Rather than hardcoding a fixed number of parallel branches, which single ASL state type most directly matches this requirement?
A) Parallel
B) Map
C) Choice
D) Pass

### Standard vs. Express Workflows (37–54)

37. An insurance company's claims-processing workflow can legitimately take anywhere from a few minutes to several weeks, pending document collection and manual review, and the company insists no claim can ever be processed more than once. Which Step Functions workflow type should they choose?
A) Express, because of its low cost per execution
B) Standard, because of its exactly-once execution semantics and its support for durations far beyond a few minutes
C) Express, because it supports unlimited execution duration
D) Neither workflow type supports durations beyond one hour

38. A mobile backend runs a short, few-second data-transformation workflow for every one of millions of daily API requests, and can tolerate that transformation step running more than once on rare occasions because it was written to be idempotent. Which workflow type is the better fit, primarily due to its pricing model and execution semantics?
A) Standard, because of its one-year duration limit
B) Express, because it is priced per execution and duration and is designed for high-volume, short-duration, at-least-once processing
C) Standard, because it guarantees at-least-once semantics
D) Neither workflow type is appropriate for high request volumes

39. A developer is documenting workflow-type limits for a team wiki and needs the correct maximum execution duration for a Standard Step Functions workflow. Which of the following is accurate?
A) 5 minutes
B) 15 minutes
C) Up to 1 year
D) Unlimited, with no maximum at all

40. The same developer needs the correct maximum execution duration for an Express Step Functions workflow, to compare against the Standard limit already documented. Which of the following is accurate?
A) Up to 5 minutes
B) Up to 1 hour
C) Up to 1 year
D) Unlimited

41. A finance team building a fund-transfer workflow is adamant that each transfer step must execute exactly once, with no possibility of a step silently re-running and causing a duplicate transfer. Which Step Functions workflow type provides this guarantee natively?
A) Express
B) Standard
C) Both workflow types provide identical guarantees here
D) Neither workflow type provides this guarantee

42. A finance team wants to understand how their Standard workflow's monthly Step Functions bill is actually calculated, since usage keeps growing. How is a Standard workflow primarily priced?
A) Per gigabyte of data processed by each state
B) Per state transition
C) Strictly per second of total wall-clock duration, regardless of how many states executed
D) A flat monthly subscription fee per state machine, regardless of usage

43. The same finance team is separately evaluating an Express workflow being proposed for a different, high-volume workload, and wants to understand its pricing basis before approving it. How is an Express workflow primarily priced?
A) Per state transition, identical to Standard
B) Based on the number of executions, their duration, and memory consumption
C) A flat annual fee regardless of usage
D) Per Lambda cold start only

44. An operations engineer is comparing observability differences between Standard and Express workflows before recommending one for a new, highly regulated workload. Which two statements about their execution history and observability are accurate? (Select TWO)
A) Standard workflows retain a full, per-execution history browsable directly in the Step Functions console
B) Express workflows typically rely on CloudWatch Logs, which must be enabled, for execution data rather than the same native per-execution console history as Standard
C) Express workflows always provide identical per-execution console history to Standard workflows by default
D) Standard workflows have no execution history available at all
E) CloudWatch Logs are unavailable for every Step Functions workflow type

45. A company runs a Standard workflow that processes a batch job lasting roughly 40 minutes per execution, with occasional bursts of thousands of concurrent executions during month-end close. As volume continues to grow, which factor should most directly guide whether Standard remains the right choice?
A) Standard workflows cannot run for more than 5 minutes, so this scenario is already invalid on its face
B) Standard's per-state-transition pricing and throughput characteristics should be weighed against cost and scale needs, but the 40-minute duration alone stays comfortably within Standard's 1-year limit
C) Standard workflows automatically convert themselves to Express once execution count exceeds a fixed threshold
D) Standard workflows cannot process more than one execution at a time, account-wide

46. A team assumes Express workflows can be used for a long-running approval process that may pause for several days awaiting a human decision delivered via a task-token callback. What is the primary reason this assumption is incorrect?
A) Express workflows cannot contain Task states at all
B) Express workflows have a maximum duration of 5 minutes, far too short for a multi-day pause, making Standard the correct choice for this scenario
C) Express workflows cannot invoke Lambda functions
D) Express workflows do not support the Choice state

47. An operations engineer needs detailed, per-execution visual debugging in the Step Functions console as a primary, non-negotiable operational requirement for a new workflow. Which workflow type is generally the better fit for this requirement?
A) Express, since it is always the cheaper option
B) Standard, since its full per-execution history is natively browsable in the console
C) Both workflow types are identical in this respect
D) Neither workflow type offers any console-based execution visibility

48. A streaming IoT platform ingests sensor readings and runs a short enrichment-and-store workflow per reading, at a rate of hundreds of thousands of readings per minute. Which workflow type is built to handle this specific throughput and duration profile cost-effectively?
A) Standard, because exactly-once guarantees are required at this scale
B) Express, because it is designed for high-volume, short-duration event processing
C) Standard, because Express cannot invoke Lambda functions
D) Neither workflow type can handle more than a few hundred executions per day

49. A solutions architect is preparing a one-slide summary contrasting Standard and Express workflows for a team presentation. Which two statements are generally accurate summary points? (Select TWO)
A) Standard provides exactly-once execution semantics, while Express provides at-least-once semantics
B) Express workflows are generally better suited to high-volume, short-duration workloads than Standard
C) Standard workflows are limited to a maximum of 5 minutes per execution
D) Express workflows guarantee exactly-once semantics identical to Standard
E) Standard workflows cannot be inspected in the console under any circumstance

50. A payment-processing team chose Express workflows for cost reasons but later discovered rare duplicate charges occurring under specific failure conditions. What is the most likely underlying cause, given what is known about Express's execution semantics?
A) Express workflows execute Lambda functions using outdated runtime versions
B) Express workflows provide at-least-once execution semantics, meaning a step can run more than once under certain failure conditions, which is unsafe for a non-idempotent payment-charging step
C) Express workflows do not support Retry configuration at all
D) Express workflows are unable to invoke external payment gateway APIs

51. An architect is deciding between Standard and Express for a new workflow and lists several of its requirements. Which requirement, if present, would most strongly argue AGAINST choosing Express?
A) High execution volume
B) Short per-execution duration, well under 5 minutes
C) A hard requirement that no step ever execute more than once
D) Tolerance for idempotent re-execution of a given step

52. A company migrates an existing Standard workflow to Express purely to reduce cost, without first reviewing whether any of its Task states perform non-idempotent operations. What risk does this migration introduce?
A) No risk at all; Standard and Express are functionally identical in every respect
B) The shift to at-least-once semantics could cause non-idempotent operations, such as charging a payment or sending a duplicate notification, to execute more than once under failure conditions
C) Express workflows cannot invoke the same Lambda functions the Standard workflow originally used
D) Express workflows require the entire state machine to be rewritten in a different programming language

53. A team building a decision matrix for choosing between Standard and Express asks which two differences are most directly relevant to that specific choice. Which two should be on the matrix? (Select TWO)
A) Execution semantics — exactly-once versus at-least-once
B) Maximum supported execution duration
C) The programming language used to write the invoked Lambda functions
D) The AWS Region in which IAM happens to be enabled
E) The color scheme of the Step Functions console

54. A workflow currently runs as Express and needs to guarantee that one specific, non-idempotent billing step never executes more than once, even under rare failure conditions, while otherwise keeping the workflow's structure unchanged. What is the most direct fix?
A) Add more Retry attempts to the existing Express workflow
B) Migrate the state machine to a Standard workflow, which provides exactly-once execution semantics
C) Increase the billing Lambda function's memory allocation
D) Replace the billing step with a Wait state

### Error Handling: Retry & Catch (55–70)

55. A Task state occasionally fails due to a transient network timeout when calling a downstream service, but usually succeeds if the call is retried a few seconds later. Which ASL construct automatically retries the state under these conditions without failing the execution outright?
A) Catch
B) Retry
C) Wait
D) Choice

56. A developer configuring a Retry block wants to cap how many times a state will be retried before the error is treated as unhandled and passed to any Catch block, or failed if none exists. Which field controls this cap?
A) "BackoffRate"
B) "IntervalSeconds"
C) "MaxAttempts"
D) "ErrorEquals"

57. A developer is fine-tuning the timing behavior of a Retry block for a flaky downstream API call. Which two fields together govern how long the state waits before and between retry attempts? (Select TWO)
A) "IntervalSeconds" sets the wait before the first retry attempt
B) "BackoffRate" is a multiplier applied to the interval after each subsequent retry, increasing the wait time
C) "ErrorEquals" controls the wait duration directly
D) "MaxAttempts" determines how long each individual wait lasts
E) "BackoffRate" always resets to 1 automatically after the second retry, regardless of configuration

58. A Retry rule on a payment Task state includes "JitterStrategy": "FULL" alongside its backoff configuration. What problem is this setting primarily designed to mitigate?
A) It prevents the state from ever failing under any circumstance
B) It randomizes the exact wait time within the backoff window, avoiding many failed executions retrying at the exact same moment against the downstream dependency
C) It disables retries entirely once jitter is enabled
D) It guarantees a fixed, perfectly non-random retry interval

59. A Task state's error is not retried, or exhausts all of its configured retry attempts. The workflow author wants execution to move to a specific fallback state in that situation. Which ASL construct achieves this?
A) Retry
B) Catch
C) Parameters
D) InputPath

60. A Task state's Catch block specifies "ErrorEquals": ["States.ALL"]. A developer reviewing the definition asks what this configuration actually matches. What is the correct answer?
A) It matches only Lambda-specific error types
B) It matches any error the state could produce, acting as a catch-all fallback
C) It disables all error handling for that state entirely
D) It only matches errors that occur during the very first attempt

61. A developer configures both a Retry block and a Catch block on the same Task state. Which two statements about how they interact are accurate? (Select TWO)
A) A state can have both a Retry block, to handle transient errors by retrying, and a Catch block, to handle the case where retries are exhausted or the error isn't retried
B) Retry and Catch are mutually exclusive; a state can only ever have one or the other, never both
C) If a Retry successfully resolves an error within its configured attempts, the Catch block is not triggered for that error
D) Catch blocks always execute before any Retry attempts, regardless of configuration
E) Configuring a Retry block automatically disables all Catch blocks defined on the same state

62. A payment-gateway Task state's Retry rule specifically targets a custom error named "PaymentGateway.ThrottlingException," waiting longer between each successive attempt. Which broader concept, first introduced in this course's discussion of resilient Lambda/SDK service calls, does this Retry configuration directly build on?
A) EC2 instance metadata retrieval
B) Exponential backoff and jitter for handling throttled or transient API calls
C) VPC subnet routing tables
D) S3 bucket versioning

63. A developer wants a caught error's details, such as its name and cause, to be inserted into the state's data so a downstream notification state can describe exactly what went wrong. Which Catch block field controls where those details are placed?
A) "ErrorEquals"
B) "Next"
C) "ResultPath"
D) "IntervalSeconds"

64. A Task state has neither a Retry block nor a Catch block configured, and its underlying Lambda function throws an unhandled exception during execution. What is the most likely outcome for the overall execution?
A) The execution automatically retries the state forever
B) The state fails, and since there is no Catch block to route to a fallback, the execution as a whole fails
C) The state silently succeeds with an empty result
D) The workflow pauses indefinitely, waiting for a manual restart

65. A workflow author is designing what a Catch block's target ("Next") state should actually do once a failure is caught. Which two of the following are legitimate, commonly used purposes for that target state? (Select TWO)
A) A dedicated cleanup or rollback state that compensates for work already completed
B) A notification state, such as one invoking a Lambda function or an SNS integration, that alerts an operations team of the failure
C) A field that must always point back to the exact same state that just failed, with no alternative permitted
D) Only a Succeed state, since Fail states can never be reached from a Catch block
E) Only a Wait state, since Catch blocks cannot lead to Task states

66. A Parallel state has one branch that fails after exhausting its own internal retries, and the Parallel state's own Catch block is configured to route to a "RollbackOrder" state. What happens next in the execution?
A) Only the failed branch is rolled back while the other branches continue running independently forever
B) The Parallel state's failure is caught, and execution transitions to "RollbackOrder" as defined
C) The entire state machine definition is permanently deleted
D) The failure is ignored, and the workflow proceeds as if the Parallel state had succeeded

67. A developer asks a colleague to summarize, in one sentence, how Retry and Catch differ in purpose within ASL. Which summary is most accurate?
A) Retry and Catch serve the exact same purpose and are fully interchangeable
B) Retry attempts to recover from a transient failure by trying the same state again with backoff, while Catch defines what to do once a failure is treated as unrecoverable, whether immediately or after retries are exhausted
C) Retry is only usable on Parallel states, and Catch is only usable on Task states
D) Catch always executes before any retry attempt is made, regardless of configuration

68. A state's Retry array contains a rule targeting "States.Timeout" with three max attempts, and a separate rule targeting "CustomApp.ValidationError" with zero max attempts, effectively acting as a non-retry for that error. Why might a team deliberately configure a rule this way for validation errors?
A) To ensure a genuinely non-transient error, like a validation failure that will never succeed no matter how many times it's retried, fails fast and moves directly to any Catch handling, rather than wasting time and cost retrying something that cannot succeed
B) Because ASL requires every distinct error type to appear somewhere in the Retry array
C) Because a MaxAttempts value of 0 causes an infinite retry loop
D) Because Retry rules must always be listed in alphabetical order by error name

69. A state definition includes multiple Catch entries, each targeting a different category of error. Which two statements correctly describe how multiple Catch entries on the same state behave? (Select TWO)
A) Different Catch entries can target different sets of errors and route to different fallback states
B) Catch entries are evaluated in order, with the first matching entry's "Next" being used
C) Only exactly one Catch entry is ever permitted per state
D) Catch entries cannot use "States.ALL" as a catch-all fallback
E) A state's Catch entries must all point to the identical fallback state

70. A workflow author wants a Task state to retry almost immediately on its first retry attempt, with essentially no delay, but to back off exponentially on subsequent attempts. Which combination of Retry fields controls this behavior?
A) "MaxAttempts" alone, since no other timing fields exist in ASL
B) "IntervalSeconds," set very low for the first wait, combined with "BackoffRate" to control the growth of subsequent waits
C) "ErrorEquals" only, since it directly controls timing
D) There is no supported way to control the initial retry delay in ASL

### Integration Patterns (71–88)

71. A workflow's Task state needs to run custom business logic — validating an order against several rules — as part of a processing step. Which integration pattern does invoking a Lambda function from that Task state represent?
A) An activity worker integration
B) A Lambda invocation integration, one of the most common Task state patterns
C) A wait-for-callback integration
D) A direct EC2 integration

72. A team wants a Task state to write directly to a DynamoDB table without writing or maintaining a "glue" Lambda function whose only job is calling PutItem on their behalf. Which integration approach satisfies this requirement?
A) A direct AWS SDK service integration, letting the Task state call the DynamoDB API directly via a resource such as "arn:aws:states:::dynamodb:putItem"
B) An activity worker running on a dedicated EC2 instance
C) A Wait state configured to poll DynamoDB on an interval
D) This is not possible; a Lambda function is always required as an intermediary

73. A video-encoding job is performed by custom software running on a fleet of on-premises servers, entirely outside AWS. The team wants that fleet to poll Step Functions for available work and report success or failure back once each job completes. Which integration pattern fits this requirement?
A) A direct AWS SDK service integration
B) An activity worker, using the Activity Task API to poll for and report on work happening outside AWS-managed compute
C) A Map state
D) A Choice state

74. A workflow needs to pause at a specific step until a human manager clicks "Approve" in an emailed link, which could happen anytime within the next several days. Which integration pattern is designed for this kind of arbitrary-duration, human-driven pause?
A) A Wait state configured for a multi-day fixed duration
B) The ".waitForTaskToken" callback pattern, where the state pauses until an external process calls SendTaskSuccess or SendTaskFailure with the task's token
C) A Retry block configured with a very high MaxAttempts value
D) A Map state iterating over the set of possible manager responses

75. An external approval system needs to resume a Task state that is currently paused under the ".waitForTaskToken" pattern, signaling that the work completed successfully and providing the result. Which API call does it use?
A) SendTaskSuccess, passing the task token and the result data
B) StartExecution
C) DescribeStateMachine
D) PutTargets

76. A long-running external job periodically wants to signal to a paused ".waitForTaskToken" task that it's still actively being worked on, without yet completing it, so the task isn't mistakenly treated as abandoned. Which API call accomplishes this?
A) SendTaskHeartbeat
B) SendTaskFailure
C) StopExecution
D) GetExecutionHistory

77. A developer is deciding whether a specific Task state should use a direct AWS SDK service integration instead of invoking a Lambda function. Which two reasons legitimately support choosing the direct integration for that step? (Select TWO)
A) The step is a straightforward API call, such as putting an item in DynamoDB or publishing to SNS, with no custom transformation logic required, so a Lambda function would only add unneeded latency, cost, and code to maintain
B) Direct SDK integrations support calling a very large number of AWS service APIs without an intermediary function
C) Direct SDK integrations are the only mechanism by which Step Functions can ever call any AWS service
D) Lambda functions cannot be invoked from Step Functions under any configuration
E) Direct SDK integrations eliminate the need for an IAM execution role entirely

78. A workflow's document-review step must pause for an unknown, potentially long duration until a third-party vendor's system finishes an asynchronous job and calls back with the result. The vendor's own system is able to call an AWS API directly once its work is done. Which task-token API would the vendor's callback call to signal success?
A) SendTaskSuccess, passing the previously issued task token and the job's result
B) CreateStateMachine
C) UpdateStateMachine
D) ListExecutions

79. A team is evaluating whether the activity-worker integration pattern still has a place in a mostly Lambda-based, modern architecture. Which two statements about activity workers are accurate? (Select TWO)
A) Activity workers poll Step Functions for available work using the Activity Task API, rather than being invoked directly by Step Functions
B) Activity workers are useful when the actual processing must happen outside AWS-managed compute, such as on physical devices or long-running custom on-premises processes
C) Activity workers are the newest, most recommended integration pattern for typical Lambda-based workflows
D) Activity workers are structurally incapable of reporting a failure back to Step Functions
E) Activity workers require no polling mechanism of any kind

80. A platform team notes that direct AWS SDK service integrations can eliminate many "glue" Lambda functions, but a reviewer points out this doesn't remove every other consideration. Which two statements about direct SDK service integrations are accurate? (Select TWO)
A) They can reduce the number of "glue" Lambda functions needed purely to call another AWS service's API
B) They still require the state machine's execution role to hold the specific IAM permissions needed for the called API action
C) They eliminate the need for any IAM role whatsoever on the state machine
D) They can only be used from within a Map state's iterator
E) They are structurally incompatible with Retry and Catch blocks

81. A scenario describes a workflow needing to call over a dozen different AWS services' APIs directly, with minimal custom logic required at each individual step. Which Step Functions capability most directly reduces the number of "glue" Lambda functions otherwise needed for this kind of workflow?
A) The Wait state
B) Direct AWS SDK service integrations, which let Task states call many AWS service APIs natively
C) The Choice state
D) The Fail state

82. A workflow uses ".waitForTaskToken" for a document-review step, but no timeout or heartbeat expectation is configured for that pause, and the reviewer never responds. What is the practical operational risk here?
A) The execution could remain paused indefinitely, up to the workflow type's maximum duration, so teams typically configure a timeout or heartbeat expectation to avoid an execution silently stalling forever
B) The execution automatically fails after exactly 60 seconds regardless of configuration
C) Step Functions automatically approves the pending request after 24 hours with no configuration needed
D) The task token becomes reusable for a completely different, unrelated execution

83. A Task state simply needs to publish a message to an SNS topic, with no custom transformation logic required at all. Which integration approach introduces the most unnecessary operational overhead for this specific, simple use case?
A) A direct AWS SDK service integration calling SNS's Publish API directly from the Task state
B) Standing up and maintaining a dedicated activity-worker process solely to poll for and forward this one simple publish call
C) Scoping the direct integration's IAM execution role narrowly to just the sns:Publish action
D) Using the Task state's native Parameters field to shape the message before publishing via the direct integration

84. An architect reviews how task tokens function within the ".waitForTaskToken" pattern before rolling it out. Which two statements about task tokens are accurate? (Select TWO)
A) The task token uniquely identifies the specific paused task within a specific execution, so a callback using that token resumes the correct execution
B) SendTaskFailure lets an external system explicitly fail the paused task, which triggers that state's Catch block if one is configured
C) Task tokens are shared globally across every execution of a given state machine, with no per-execution distinction
D) Task tokens are usable only with activity workers, never with Task states integrated directly
E) A task token expires the instant it is issued and can never be used afterward

85. A workflow's Task state directly integrates with AWS Batch to submit a job, and the team wants that Task state to remain paused until the submitted job actually finishes, rather than proceeding the moment the submission API call returns. What best describes this capability?
A) This is not possible; direct integrations always behave as fire-and-forget submissions with no way to wait for completion
B) Certain direct SDK integrations support a "run a job and wait for it to complete" pattern, distinct from simply calling the API and immediately moving on, letting the Task state pause until the downstream job's actual completion
C) This requires standing up an activity worker in every case
D) This requires converting the Task state into a Map state

86. A developer is deciding whether a given workflow step should invoke a Lambda function or use a direct AWS SDK service integration instead. Which factor most accurately points toward choosing the Lambda function?
A) The step requires custom business logic, data transformation, or calling a non-AWS third-party API that a direct service integration alone cannot perform
B) Lambda functions are always cheaper than direct integrations in every possible case
C) Direct integrations cannot be used from within a Parallel state
D) Lambda is the only integration pattern Step Functions supports at all

87. A workflow's approval step uses the callback pattern, and the external system calls SendTaskFailure instead of SendTaskSuccess after determining the request should be rejected. What happens next in the state machine?
A) The workflow ignores the failure signal and proceeds as though the step had succeeded
B) The state is treated as failed, triggering that state's Retry (if configured) and then Catch (if configured), the same as any other Task state failure
C) The entire AWS account's Step Functions service becomes disabled
D) SendTaskFailure has no defined effect anywhere in ASL

88. A developer is summarizing the four Task state integration approaches covered in this module for a study guide. Which two statements correctly capture how these patterns relate to one another? (Select TWO)
A) Lambda invocation, direct AWS SDK service integrations, activity workers, and the waitForTaskToken callback pattern together cover synchronous custom logic, direct API calls, external polling workers, and asynchronous human or long-running callbacks, respectively
B) All four integration patterns require a Lambda function to be present somewhere in the call chain
C) Direct SDK integrations and Lambda invocations are functionally the exact same underlying mechanism, just named differently
D) The waitForTaskToken pattern is usable only for Lambda-invoked Task states
E) These four patterns give Step Functions the flexibility to fit synchronous, asynchronous, custom, and external-worker-based work into the same state machine model

### Map State & Input/Output Processing (89–104)

89. A developer configuring a Map state needs to specify the exact path, within the incoming input data, to the array the Map state should iterate over. Which field is used for this?
A) "ItemsPath"
B) "InputPath"
C) "MaxConcurrency"
D) "Iterator" alone, with no separate field needed

90. A team wants to limit how many Map state iterations run at the same time, to avoid overwhelming a downstream dependency with concurrent calls. Which field controls this?
A) "ItemsPath"
B) "MaxConcurrency"
C) "ResultPath"
D) "BackoffRate"

91. A company needs to process every object under an S3 prefix, potentially hundreds of thousands of objects, with each object's processing tracked as its own separately observable child execution rather than running inline within a single, large parent execution. Which Map state mode is designed for this scale?
A) Inline (classic) Map
B) Distributed Map
C) Parallel
D) Choice

92. A developer omits the "ResultPath" field entirely from a Task state's definition. What is the default behavior in that case?
A) It defaults to "$", meaning the task's result replaces the entirety of the state's data, discarding whatever else was present in the input
B) It defaults to automatically preserving all prior data with no further configuration needed
C) It defaults to storing the result only in CloudWatch Logs, never in the state's own data
D) Omitting "ResultPath" causes an immediate validation error at deployment time

93. A later state in a workflow reports that it can no longer access a field that was clearly present several steps earlier in the execution's original input. Which ASL misconfiguration is the most likely culprit?
A) A missing or incorrectly scoped "ResultPath" on an earlier Task state, causing its result to overwrite the entire state data instead of merging in as a new field
B) A Choice state evaluated one of its conditions incorrectly
C) The Lambda function invoked by an earlier state had too little memory allocated
D) The state machine's IAM execution role is missing a specific permission

94. A workflow author wants a state to receive only a specific sub-portion of the incoming state data, filtered out before any Parameters transformation or the actual task execution takes place. Which ASL field is used for this?
A) "OutputPath"
B) "InputPath"
C) "ResultPath"
D) "ResultSelector"

95. A workflow author wants to control what portion of a state's combined data, after "ResultPath" has already merged in the task's result, gets passed along to the next state as its input. Which ASL field accomplishes this?
A) "InputPath"
B) "Parameters"
C) "OutputPath"
D) "ItemsPath"

96. A Task state's "Parameters" field includes the entry "orderId.$": "$.orderId". A developer new to ASL asks what the ".$" suffix on that key actually indicates. What is the correct answer?
A) It marks the field as required by an attached IAM policy
B) It indicates the value should be dynamically resolved from the current state's InputPath-filtered input using the given JSONPath, rather than treated as a literal string
C) It disables that particular field entirely
D) It is a syntax error and would cause the definition to fail validation

97. A developer is explaining how InputPath and Parameters work together on a single Task state. Which two statements accurately describe their respective roles? (Select TWO)
A) InputPath filters which portion of the incoming state data the state considers as its starting input
B) Parameters can reshape, add static values to, or pull dynamic values (via ".$") from that InputPath-filtered input to construct the exact payload sent to the state's resource
C) InputPath and Parameters both apply only strictly after the task has already executed
D) Parameters can only ever contain static, hardcoded values, never data pulled dynamically from the input
E) InputPath is usable only inside Map states, never within ordinary Task states

98. A team wants a Task state's result merged into the existing state data under a new key called "paymentResult," preserving every other field already present, such as "orderId" and "customer." Which ResultPath configuration achieves this?
A) "ResultPath": "$"
B) "ResultPath": "$.paymentResult"
C) Omitting "ResultPath" entirely
D) "OutputPath": "$.paymentResult"

99. A developer is trying to understand the correct sequence in which InputPath, Parameters, the task's execution, ResultPath, and OutputPath are applied to a single Task state's data. Which ordering is correct, from first to last?
A) OutputPath, ResultPath, task execution, Parameters, InputPath
B) InputPath filters the input, Parameters shapes the payload sent to the resource, the task executes, ResultPath merges the result into the state data, and OutputPath filters what's passed to the next state
C) Parameters, InputPath, ResultPath, task execution, OutputPath
D) They are all applied simultaneously, with no defined order between them

100. A Map state's "ItemsPath" points to "$.orderItems," but the incoming state data for a particular execution has no "orderItems" field at all, because it was omitted or misnamed upstream. What is the most likely outcome?
A) The Map state silently skips all iteration and proceeds to the next state as though it had succeeded
B) The Map state fails with a runtime error, since it cannot locate the array it was told to iterate over
C) The Map state treats the entire input as a single-element array automatically
D) The Map state pauses indefinitely, waiting for the missing field to eventually appear

101. A developer is investigating the "ResultSelector" field available on certain ASL states. Which two statements about it are accurate? (Select TWO)
A) It lets you reshape a task's raw result into a custom structure before ResultPath merges it into the state data
B) It is applied before ResultPath, transforming the resource's raw output
C) It fully replaces the need for InputPath in every state where it is used
D) It can only be used inside Choice states
E) It disables all error handling configured for that state

102. A developer configures "OutputPath": "$.validatedOrder" on a state, but the merged state data, after ResultPath has run, has no "validatedOrder" field at that path. What is the likely consequence?
A) The next state receives the full, unfiltered data regardless of the mismatch
B) This mismatch will typically cause an error, since OutputPath is attempting to filter to a path that doesn't exist in the state's data
C) The workflow automatically creates an empty "validatedOrder" field to satisfy the OutputPath reference
D) OutputPath mismatches are always silently ignored with no effect on execution

103. A developer needs to invoke a Lambda function with a custom-constructed payload built from several fields of the incoming data, then merge just that Lambda function's response into the state data under a new key, without discarding the rest of the original input. Which combination of ASL fields accomplishes this?
A) "InputPath" alone, with no other fields needed
B) "Parameters" to construct the custom payload sent to the function, and "ResultPath" set to a specific new key (not "$") to merge the response without discarding existing data
C) "OutputPath" alone, with no Parameters or ResultPath configured
D) "MaxConcurrency," since it governs how payloads are constructed

104. A workflow author intentionally wants a Task state's result to completely replace all prior state data, discarding everything from before that state, because the next state genuinely only needs the fresh result. Which configuration achieves this, and is in fact the default behavior if left unset?
A) "ResultPath": "$.newData"
B) "ResultPath": "$", or simply omitting ResultPath entirely, since "$" is the default
C) "InputPath": "$"
D) "MaxConcurrency": 0

### Orchestration vs. Choreography (105–116)

105. A company's checkout process must validate an order, reserve inventory, charge payment, and ship the order, strictly in that sequence, with a single place to see the current status and a defined rollback path if any step fails. Which architectural pattern, and corresponding AWS service, best fits this requirement?
A) Choreography, using EventBridge alone with no central coordinator
B) Orchestration, using AWS Step Functions as the central coordinator that defines the explicit sequence and error handling
C) Choreography, using S3 event notifications exclusively
D) Orchestration, using Amazon SNS as the coordinating service

106. A company wants three independent teams' services to each react to a single "OrderShipped" event — one updates an analytics dashboard, another sends a customer notification, and a third updates inventory forecasting — with no team needing to know about or coordinate with the others, and no strict ordering required. Which architectural pattern best fits, and which AWS service is the natural implementation choice?
A) Orchestration, using a single Step Functions state machine jointly owned by all three teams
B) Choreography, using Amazon EventBridge to let each team's service independently subscribe to and react to the event
C) Orchestration, requiring all three teams to embed their logic inside one shared Lambda function
D) Choreography, requiring a shared database table that all three teams poll continuously

107. An architect is asked to describe, in one sentence, the core structural difference between orchestration and choreography as architectural patterns. Which description is most accurate?
A) Orchestration relies on a central coordinator explicitly directing the sequence of steps, while choreography has no central controller, with each service independently reacting to events
B) Orchestration and choreography are simply two different names for the identical underlying pattern
C) Choreography always uses fewer distinct AWS services than orchestration
D) Orchestration cannot handle branching logic, while choreography can

108. A team debating orchestration versus choreography for a new workflow raises a concern: in a purely choreographed design, understanding the full end-to-end flow requires tracing logs and configuration across many independently deployed services. Which pattern's design more directly avoids this specific downside?
A) Choreography, since it has no single point of failure
B) Orchestration, since a central state machine definition and its execution history provide one place to see the full workflow's status and history
C) Neither pattern addresses this particular concern
D) This concern applies only to Lambda-based workflows, not to choreography generally

109. A team is listing the typical advantages of a choreography-based design over an orchestration-based one. Which two of the following are accurate advantages of choreography? (Select TWO)
A) Adding a new consumer of an existing event requires no changes to the event publisher or to any other existing consumer
B) Services remain loosely coupled, since publishers do not need to know who, if anyone, is listening
C) It automatically provides a single visual execution history for the entire business process
D) It guarantees exactly-once processing of every event by every consumer
E) It eliminates the need for any error handling within consuming services

110. A team is listing the typical advantages of an orchestration-based design over a choreography-based one for a complex, ordered business process. Which two of the following are accurate advantages of orchestration? (Select TWO)
A) Centralized, declarative Retry and Catch handling at the workflow level, rather than each service independently reinventing its own error handling
B) A single execution history showing the exact sequence and outcome of every step, aiding audits and debugging
C) Complete elimination of the need for any IAM permissions anywhere in the workflow
D) Guaranteed lower cost in every possible scenario, regardless of workload shape
E) No possibility of ever needing to invoke a Lambda function

111. A scenario states that a workflow's steps must happen in a specific, strictly enforced order, with conditional branching and a human-approval step partway through the process. Which pattern, and AWS service, does this most strongly point toward?
A) Choreography via EventBridge, since it supports Lambda as a target
B) Orchestration via Step Functions, given the need for enforced sequencing, branching, and a pausable human-approval step
C) Choreography via SNS fan-out to multiple subscribers
D) Neither pattern applies; this scenario requires a fully custom-built scheduler

112. A scenario describes several completely independent microservices that each need to be notified whenever a new customer signs up, with each microservice's reaction being entirely self-contained and order-independent. Introducing a central Step Functions state machine to coordinate these reactions would primarily introduce which drawback compared to a choreography approach?
A) Unnecessary coupling of independent, order-independent reactions to a central workflow definition that must be modified every time a new independent reactor is added, when a choreographed event-driven design would let new services simply subscribe to the existing event with zero changes elsewhere
B) Step Functions is structurally incapable of invoking more than one Lambda function
C) Step Functions has no mechanism to invoke Lambda functions in parallel
D) Choreography is structurally incapable of using IAM at all

113. A study-guide question asks how orchestration and choreography relate to the exam's Domain 1, Task Statement 1 coverage of architectural patterns. Which statement correctly ties the two concepts together?
A) Orchestration and choreography are unrelated to any exam domain and appear only informally in AWS marketing material
B) They represent two named, testable architectural patterns for coordinating multiple services, and the exam expects a candidate to match a scenario's coordination requirements — centralized and ordered versus independent and event-reactive — to the correct pattern and its representative AWS service
C) Only choreography is ever tested on the exam; orchestration is explicitly out of scope
D) The exam does not require memorizing either pattern by name

114. A company currently coordinates a five-step business process using a chain of EventBridge rules, each triggering the next Lambda function in sequence, effectively hand-rolling ordering through event routing. They increasingly struggle to answer "what state is a given execution currently in, and what happened at each step" without digging through several services' separate logs. Which change most directly solves this specific operational pain point?
A) Adding even more EventBridge rules to the existing chain
B) Migrating the process to a Step Functions Standard workflow, which centralizes the sequence and provides a single, inspectable execution history per run
C) Switching every Lambda function in the chain to a larger memory allocation
D) Adding additional SQS queues between each existing step

115. An architect is choosing between orchestration and choreography for four different candidate scenarios and must pick the strongest candidate for choreography specifically. Which scenario fits best?
A) A strict, multi-step approval chain requiring centralized retry logic and a full audit trail of exact step ordering
B) A checkout process where inventory reservation must complete successfully before payment is even attempted
C) Three independent teams' services each needing to react, without any required ordering between them, whenever a "UserRegistered" event occurs
D) A workflow needing a human-in-the-loop approval step that can pause for several days

116. A study group is compiling the conditions under which the exam expects "orchestration" (Step Functions), rather than "choreography" (EventBridge), to be the correct architectural answer. Which two conditions correctly belong on that list? (Select TWO)
A) The scenario requires a strictly ordered sequence of steps with centralized error handling and a single place to audit exactly what happened
B) The scenario requires a human-in-the-loop pause of arbitrary duration as an explicit step in a defined process
C) The scenario describes services that must remain completely unaware of one another and react independently with no defined order
D) The scenario has no requirement for step ordering, retries, or centralized visibility of any kind
E) Cost must always be minimized regardless of any other stated requirement

### Use Cases, Deployment & Integrative Scenarios (117–125)

117. A study group is listing commonly cited, exam-relevant use cases for AWS Step Functions. Which two of the following belong on that list? (Select TWO)
A) Coordinating a multi-step order-processing workflow spanning inventory, payment, and shipping
B) Running a human-in-the-loop approval workflow that pauses for a manager's decision
C) Hosting a static website with globally distributed edge caching
D) Serving as a relational database engine with ACID transaction guarantees
E) Acting as a content delivery network for streaming video

118. A data engineering team needs to coordinate a sequence of AWS Glue jobs and Lambda-based transformations, fanning out over many data partitions using a Map state, with full auditability of each run for compliance purposes. Which combination of Step Functions choices best fits these requirements?
A) An Express workflow with no Map state involved
B) A Standard workflow, using Map (potentially Distributed Map at scale) to fan out over partitions, giving both durability for a multi-step pipeline and per-execution audit history
C) A Choice state used entirely in isolation with no Task states
D) A Parallel state containing exactly one branch

119. A platform team wants to define a Step Functions state machine as infrastructure as code within an existing CloudFormation template, alongside their other application resources. Which CloudFormation resource type do they use?
A) AWS::Lambda::Function
B) AWS::StepFunctions::StateMachine
C) AWS::SNS::Topic
D) AWS::EC2::Instance

120. A team using AWS SAM wants a more streamlined way to author a Step Functions state machine alongside the Lambda functions it invokes, within the same SAM template. Which SAM resource type provides this?
A) AWS::Serverless::Function exclusively, with no dedicated state machine resource available
B) AWS::Serverless::StateMachine
C) AWS::Serverless::Api
D) AWS::Serverless::LayerVersion

121. A platform team wants to roll out a new version of a Step Functions state machine definition gradually, shifting a portion of execution traffic to it before fully committing, conceptually similar to how Lambda handles versions and aliases. Which Step Functions capability supports this?
A) State machine versions and aliases, which allow publishing an immutable version of a definition and shifting execution traffic between versions gradually
B) A feature that allows a single state machine definition to run in two AWS Regions simultaneously with no additional configuration
C) A capability unrelated to deployment that only affects IAM permissions
D) A feature that eliminates the need for CloudFormation entirely

122. A DevOps team is designing how Step Functions state machines fit into their existing CI/CD pipeline. Which two statements about deploying state machines this way are accurate? (Select TWO)
A) The ASL definition can be maintained as a file in source control and deployed via CloudFormation or SAM alongside related Lambda functions
B) Versions and aliases can support safer, gradual rollout of a new state machine definition
C) State machines can only ever be created manually through the console, never via infrastructure as code
D) CI/CD pipelines are structurally incapable of deploying any Application Integration service, including Step Functions
E) Deploying a new state machine version always immediately deletes the execution history of every prior version

123. A company reviews three workflows: an approval workflow (Standard, using waitForTaskToken), an order-processing workflow (Standard, requiring exactly-once execution), and an IoT enrichment workflow (Express, high volume and short duration). Which statement correctly evaluates whether each workflow's chosen type matches its stated requirement?
A) All three should use Express for cost savings, since Standard is never worth its extra cost
B) The approval and order-processing workflows correctly use Standard, given their long/arbitrary-duration and exactly-once needs respectively, and the IoT workflow correctly uses Express, given its high volume, short duration, and tolerance for at-least-once processing
C) All three should use Standard, since Express is structurally unable to invoke Lambda functions
D) The IoT workflow should switch to Standard because Express cannot handle high request volume

124. A security review of a Step Functions-based order workflow finds three issues: an execution role granting broader permissions than any Task state actually needs, a payment Task state running on an Express workflow, and a missing ResultPath causing a downstream state to lose earlier order data. Which set of fixes correctly addresses all three findings?
A) Scope the execution role down to least privilege for the specific resources each Task state calls, migrate the payment step's guarantees to a Standard workflow given the need to avoid duplicate charges, and add an explicit ResultPath so the task's result merges into the state data rather than replacing it
B) Delete the execution role entirely, since Step Functions does not require IAM to function
C) Leave the Express workflow unchanged, since payment steps are always safe under at-least-once semantics
D) Remove ResultPath entirely from every state in the workflow to avoid the issue altogether

125. A senior developer is asked to summarize this module's core theme for a teammate studying separately, in a single sentence covering when to reach for Step Functions versus a looser event-driven approach. Which summary best captures it?
A) Step Functions should be used for absolutely every workflow, regardless of requirements, since it is strictly superior in all cases
B) Reach for Step Functions (orchestration) when a process needs an explicit, centrally coordinated, auditable sequence with built-in retry and error handling — including exactly-once guarantees, long pauses for human input, or fan-out over variable-length data — and reach for EventBridge (choreography) when independent services simply need to react to shared events with no required central coordination or ordering
C) Step Functions and EventBridge are functionally identical, and the choice between them never actually matters
D) Choreography is always the correct choice because it has no associated cost

---

## Answer Key & Explanations

1. B — Step Functions is purpose-built for centrally coordinated, inspectable multi-step workflows across services.
2. C — "StartAt" names the first state a state machine execution begins with.
3. A & B — A "Next" field names the following state, while "End": true marks a branch's terminal state.
4. B — A state machine definition is a declarative, JSON-based ASL document describing states and transitions.
5. B — Step Functions adds centralized visibility, built-in retry/error handling, and visual tracking absent from ad hoc function chaining.
6. B — An execution is one complete, uniquely identified run of a state machine from start to a terminal state.
7. B — The Step Functions console's execution detail view shows per-state input/output and a visual path for that run.
8. D — "DockerImage" is not a valid ASL state field.
9. A — ASL describes states/transitions declaratively; Step Functions determines how to execute that graph.
10. A & B — The state machine's execution role must grant the needed permissions, or Task state calls fail with access errors.
11. B — Choice states implement conditional branching based on evaluated conditions.
12. B — Step Functions centralizes ordered, stateful workflow execution and tracking; EventBridge is decoupled and reactive with no central coordinator.
13. B — A Standard workflow's per-execution history provides the exact sequence and timestamps needed for an audit trail.
14. B — The state machine is the reusable definition; an execution is one specific run of it with its own history.
15. B — "Comment" is a documentation-only field with no execution effect.
16. A & B — State machines can be authored via the console for quick iteration, or as code via CloudFormation/SAM.
17. B — Map iterates over a variable-length array, running the same logic once per element.
18. B — Parallel runs a fixed, known set of different concurrent branches.
19. C — Pass performs no real work and can inject static values, useful for stubbing incomplete steps.
20. A — Wait pauses for a specified duration or timestamp with no external work performed.
21. B — Fail explicitly terminates an execution as a failure with a custom error and cause.
22. A — Succeed marks a clean, successful termination point for a branch or execution.
23. B — A Task state's Resource field can reference a Lambda ARN, an SDK integration ARN, an Activity ARN, and more.
24. A & B — Map iterates dynamically over an array; Parallel runs a fixed, explicitly authored set of concurrent branches.
25. B — The "Default" field defines where execution goes when no explicit Choice rule matches.
26. D — "SqlWhereClause" is not a legitimate ASL Choice comparison operator.
27. A & B — Branch results combine into an array matching branch-definition order, not completion order.
28. B — An uncaught branch failure in a Parallel state propagates to fail the Parallel state as a whole.
29. A & B — Choice and Pass control workflow structure/data without performing external I/O.
30. A — A Pass state with a static Result field is the standard way to stub an unfinished step.
31. B — "End": true marks a state as the final one in its branch, replacing the need for "Next."
32. B — A Choice state with no matching rule and no Default has no valid path and fails at runtime.
33. A & B — Map iterations support configurable concurrency, and Distributed Map supports very large-scale, separately tracked fan-out.
34. A — A Task state to notify, followed by a Succeed state, cleanly notifies then terminates the branch.
35. B — "Comment" is purely descriptive and never alters runtime behavior.
36. B — Map handles a variable-length collection needing identical per-element processing, without hardcoding branches.
37. B — Standard's exactly-once semantics and up-to-1-year duration fit a claim process that must never double-process and may run long.
38. B — Express's per-execution pricing and design for high-volume, short, idempotent-tolerant work fits this profile.
39. C — Standard workflows support execution durations of up to 1 year.
40. A — Express workflows are capped at up to 5 minutes per execution.
41. B — Standard provides exactly-once execution semantics natively; Express does not.
42. B — Standard workflows are priced per state transition.
43. B — Express workflows are priced based on number of executions, duration, and memory.
44. A & B — Standard retains full per-execution console history; Express typically relies on CloudWatch Logs instead.
45. B — The 40-minute duration is well within Standard's 1-year cap; cost/throughput tradeoffs should still be evaluated separately.
46. B — Express's 5-minute cap makes it unsuitable for a pause that could last several days; Standard is required.
47. B — Standard's native per-execution console history directly satisfies a detailed visual-debugging requirement.
48. B — Express is designed specifically for high-volume, short-duration event processing like this IoT workload.
49. A & B — Standard is exactly-once and Express is at-least-once; Express suits high-volume, short-duration workloads better.
50. B — Express's at-least-once semantics allow a step to run more than once under failure, risking duplicate charges if not idempotent.
51. C — A hard exactly-once requirement disqualifies Express, which only guarantees at-least-once.
52. B — At-least-once semantics can cause non-idempotent operations to run more than once after such a migration.
53. A & B — Execution semantics and maximum duration are the two most directly relevant differentiators for this choice.
54. B — Migrating to Standard restores the exactly-once guarantee the billing step requires.
55. B — Retry automatically re-attempts a state after a transient failure, without failing the execution.
56. C — "MaxAttempts" caps how many retry attempts occur before the error is treated as unhandled.
57. A & B — "IntervalSeconds" sets the initial wait; "BackoffRate" multiplies the interval on each subsequent retry.
58. B — Jitter randomizes the exact wait within the backoff window to avoid synchronized retry storms.
59. B — Catch defines the fallback state to transition to when an error isn't retried or retries are exhausted.
60. B — "States.ALL" is a catch-all matching any error the state could produce.
61. A & C — A state can have both Retry and Catch, and a successful Retry resolution does not trigger Catch.
62. B — This is the same exponential-backoff-and-jitter concept applied to resilient Lambda/SDK service calls.
63. C — "ResultPath" on a Catch block places the caught error's details into the state's data.
64. B — With no Catch block, an unhandled failure propagates to fail the overall execution.
65. A & B — A Catch target commonly leads to a cleanup/rollback state or a notification/alerting state.
66. B — The Parallel state's Catch block catches the branch failure and routes to "RollbackOrder" as configured.
67. B — Retry recovers from transient failures via backoff; Catch defines the fallback once a failure is unrecoverable.
68. A — Setting MaxAttempts to 0 for a non-transient error lets it fail fast into Catch handling instead of wasting retries.
69. A & B — Different Catch entries can target different errors and route differently, evaluated in order with the first match applied.
70. B — A low initial IntervalSeconds combined with BackoffRate controls near-immediate first retries and exponential subsequent growth.
71. B — Invoking a Lambda function from a Task state is the Lambda invocation integration pattern.
72. A — A direct AWS SDK service integration lets the Task state call DynamoDB's API without an intermediary Lambda function.
73. B — Activity workers poll for and report on work performed outside AWS-managed compute, fitting an on-premises fleet.
74. B — The waitForTaskToken callback pattern supports an arbitrary-duration pause for human approval, unlike a fixed-duration Wait state.
75. A — SendTaskSuccess resumes a paused callback task and supplies its result.
76. A — SendTaskHeartbeat signals a paused task is still being actively worked on, preventing premature timeout.
77. A & B — Simple API calls with no custom logic favor direct integrations, which cover a large number of AWS service APIs.
78. A — SendTaskSuccess, using the previously issued task token, is how an external system signals successful completion.
79. A & B — Activity workers poll via the Activity Task API and suit processing that must occur outside AWS-managed compute.
80. A & B — Direct integrations reduce glue Lambda functions but still require correctly scoped IAM permissions on the execution role.
81. B — Direct AWS SDK service integrations let Task states call many AWS APIs natively, cutting down on glue Lambda functions.
82. A — Without a timeout or heartbeat expectation, a waitForTaskToken pause can stall indefinitely up to the workflow's max duration.
83. B — Standing up a dedicated activity worker for a single simple SNS publish call is disproportionate, unnecessary overhead.
84. A & B — Task tokens identify a specific paused task within a specific execution, and SendTaskFailure triggers that state's Catch if configured.
85. B — Certain direct integrations support "run and wait for completion" semantics rather than simple fire-and-forget submission.
86. A — Custom logic, transformation, or third-party API calls a direct integration can't perform point toward using Lambda.
87. B — SendTaskFailure is treated as a state failure, subject to that state's Retry and Catch configuration like any other failure.
88. A & E — The four patterns cover synchronous custom logic, direct API calls, external polling, and async callbacks, giving Step Functions broad integration flexibility.
89. A — "ItemsPath" specifies where in the input the array to iterate over is located.
90. B — "MaxConcurrency" caps how many Map iterations run simultaneously.
91. B — Distributed Map is designed for very large-scale fan-out with separately trackable child executions.
92. A — The default ResultPath of "$" causes the task's result to replace the entire state data.
93. A — A missing or misconfigured ResultPath is the classic cause of a later state losing access to earlier data.
94. B — "InputPath" filters the incoming data a state receives before Parameters or task execution.
95. C — "OutputPath" filters the post-ResultPath combined data before it's passed to the next state.
96. B — The ".$" suffix indicates the value should be dynamically resolved via JSONPath from the input, not treated literally.
97. A & B — InputPath filters the starting input; Parameters reshapes/constructs the payload from that filtered input.
98. B — Setting "ResultPath": "$.paymentResult" merges the result as a new field, preserving existing data.
99. B — The correct order is InputPath, Parameters, task execution, ResultPath, then OutputPath.
100. B — A Map state fails at runtime if its configured ItemsPath cannot locate an array in the input.
101. A & B — ResultSelector reshapes a task's raw output before ResultPath merges it into the state data.
102. B — An OutputPath referencing a nonexistent path in the state's data typically causes a runtime error.
103. B — Parameters constructs the custom payload, while a non-"$" ResultPath merges the response without discarding prior data.
104. B — "$" (the default) causes the task's result to fully replace the prior state data, as intended here.
105. B — Strict sequencing, centralized status, and rollback handling are hallmarks of orchestration via Step Functions.
106. B — Independent, order-independent reactions to a shared event are the classic choreography fit via EventBridge.
107. A — Orchestration uses a central coordinator directing steps; choreography has no central controller, with independent reactions.
108. B — A central state machine's execution history provides one place to see the full workflow's status, unlike distributed choreography.
109. A & B — New consumers can subscribe without publisher changes, and choreography keeps services loosely coupled.
110. A & B — Orchestration centralizes Retry/Catch handling and provides a single, auditable execution history.
111. B — Enforced sequencing, branching, and a pausable approval step are all hallmarks of orchestration via Step Functions.
112. A — Centralizing independent, order-independent reactions unnecessarily couples them to a workflow definition that must change for every new reactor.
113. B — Orchestration and choreography are testable, named architectural patterns tied to a scenario's coordination requirements.
114. B — Migrating to a Standard Step Functions workflow centralizes sequencing and gives a single inspectable execution history per run.
115. C — Independent, order-independent reactions to a shared event are the strongest choreography fit among the options.
116. A & B — Centralized error handling/auditability and an arbitrary-duration human-in-the-loop pause both point to orchestration.
117. A & B — Order-processing coordination and human-in-the-loop approval workflows are core, commonly cited Step Functions use cases.
118. B — A Standard workflow with Map (or Distributed Map at scale) provides both durability and full per-execution auditability for the pipeline.
119. B — "AWS::StepFunctions::StateMachine" is the CloudFormation resource type for a state machine.
120. B — "AWS::Serverless::StateMachine" is the SAM resource type for authoring a state machine alongside Lambda functions.
121. A — State machine versions and aliases support publishing immutable versions and shifting traffic gradually, like Lambda's model.
122. A & B — ASL can be source-controlled and deployed via CloudFormation/SAM, and versions/aliases support safer gradual rollout.
123. B — Each workflow's chosen type correctly matches its stated duration, exactly-once, or high-volume/short-duration requirement.
124. A — Scoping the role to least privilege, using Standard for the payment step's exactly-once need, and adding ResultPath together address all three findings.
125. B — Orchestration fits centrally coordinated, auditable, retry-driven processes; choreography fits independent, order-agnostic event reactions.
