# Module 04 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Architectural Patterns & Resilience (1–22)

1. A retail application currently runs as a single monolith on a large EC2 instance. During promotional events, the checkout process crashes due to high load, taking down the entire catalog and search functionality as well. Which architectural pattern should the team adopt to prevent failures in checkout from affecting other parts of the application?
A) Deploy the monolith across multiple Availability Zones in an Auto Scaling group
B) Decompose the monolith into microservices, allowing checkout, catalog, and search to scale and fail independently
C) Increase the EC2 instance size to the largest available instance type
D) Move the monolithic database to an in-memory cache

2. A photo-sharing platform wants to resize user-uploaded images and scan them for inappropriate content. The upload service should not wait for image resizing or moderation to finish before acknowledging the upload to the user. Which architectural pattern best fits this requirement?
A) Synchronous request-response via REST API calls
B) An event-driven architecture where S3 emits an object-creation event that triggers independent consumer functions asynchronously
C) Polling an EC2 database every minute for newly created records
D) A monolithic batch job that runs nightly

3. An e-commerce company is coordinating a complex order-fulfillment process involving inventory reservation, payment processing, fraud check, and notification dispatch. The workflow requires sequential steps, conditional branching, automated retries with exponential backoff on transient errors, and full visual auditability of execution history. Which approach should the development team choose?
A) A choreographed architecture where services publish and listen to Amazon EventBridge events independently
B) An orchestrated architecture using an AWS Step Functions state machine to centrally coordinate each step and handle errors
C) A monolithic cron job running on an EC2 instance
D) Direct peer-to-peer synchronous HTTP calls between microservices

4. A developer is designing a system where a single "OrderPlaced" event must trigger three separate downstream systems simultaneously: inventory management, customer notifications, and analytics ingestion. The publisher must not be coupled to the consumers, and new consumers may be added later without modifying the publisher. Which pattern and AWS service combination accomplishes this?
A) Fan-out pattern using an Amazon SNS topic subscribed by multiple Amazon SQS queues
B) Point-to-point messaging using a single Amazon SQS standard queue
C) Direct synchronous HTTP POST requests to each downstream service endpoint
D) Storing events in a local SQLite file on an EC2 instance

5. An application processes financial transactions using AWS Lambda. Due to network retries from upstream services, the Lambda function occasionally receives duplicate event payloads for the same transaction. How should the developer ensure that customers are never charged twice for the same transaction?
A) Increase the Lambda function's timeout to prevent premature retries
B) Implement an idempotency key check using an atomic conditional write in DynamoDB (attribute_not_exists) before executing the charge
C) Configure the Lambda function to use provisioned concurrency
D) Switch the Lambda function from asynchronous to synchronous invocation

6. A developer writes a Lambda function that charges credit cards. If an execution fails due to a downstream payment gateway timeout, the caller retries the request. The developer adds retry logic with exponential backoff on the client. Why is this change alone insufficient to prevent duplicate charges?
A) Exponential backoff only works for read operations, not write operations
B) Retries cause the operation to be attempted multiple times; without an idempotency mechanism, a retry after an unacknowledged successful charge will perform the side effect again
C) AWS Lambda does not support client retries
D) The payment gateway automatically disables retries

7. An architect wants to build a web application that can scale dynamically across hundreds of EC2 instances behind an Application Load Balancer, tolerating the immediate termination of any individual instance without user session loss. Which design principle is required?
A) Stateful architecture storing session data in local server memory
B) Stateless application tier storing session state externally in Amazon DynamoDB or Amazon ElastiCache
C) Sticky sessions configured on the load balancer with local disk persistence on EBS
D) Storing user sessions in the operating system's /tmp directory on each instance

8. An order-placement API directly invokes an external shipping service synchronously over HTTP. When the shipping service experiences degraded performance, the order-placement API exhausts its connection pool and begins dropping incoming customer orders. What is the root architectural problem and the recommended fix?
A) The services are loosely coupled; the team should merge them into a single binary
B) The services are tightly coupled; the team should decouple them by placing an Amazon SQS queue between the order API and the shipping service
C) The order API has insufficient CPU; the team should increase instance size
D) The shipping service should be replaced with an S3 bucket

9. When multiple distributed clients simultaneously retry failed requests to an overloaded backend service at fixed intervals, what phenomenon can occur, and what pattern prevents it?
A) Starvation; prevented by disabling all client retries
B) Thundering herd / synchronized retry storm; prevented by implementing exponential backoff with jitter
C) Hot partitioning; prevented by write sharding
D) Memory leak; prevented by garbage collection

10. A backend worker processes messages from an Amazon SQS queue. Occasionally, a malformed message causes the worker code to throw an unhandled exception and crash, returning the message to the queue repeatedly and blocking downstream processing. Which mechanism isolates these problematic messages?
A) Increasing the SQS visibility timeout to 12 hours
B) Configuring a Dead-Letter Queue (DLQ) with an appropriate maxReceiveCount on the redrive policy
C) Disabling SQS in favor of SNS
D) Setting SQS message retention period to 0 seconds

11. Which two statements correctly describe the difference between choreography and orchestration in distributed application design? (Select TWO.)
A) Choreography relies on decentralized event publishing/subscribing where services react independently
B) Orchestration uses a central coordinator (such as AWS Step Functions) that explicitly controls execution flow and error recovery
C) Choreography provides a centralized visual state machine console for monitoring overall workflow progress
D) Orchestration eliminates all dependencies between services so they have zero knowledge of each other
E) Choreography requires synchronous HTTP communication between all participants

12. A developer needs to ensure that an S3 batch processing workflow is fault-tolerant against transient downstream service failures. Which combination of design patterns should be incorporated? (Select TWO.)
A) Exponential backoff with randomized jitter on retry attempts
B) Fixed 1-second immediate retries in a tight while-loop
C) Dead-letter queues (DLQs) to capture items that exhaust maximum retry attempts
D) Storing processing state only in local memory of the worker instance
E) Disabling timeouts so requests wait indefinitely

13. A company's internal microservice architecture uses Amazon EventBridge for inter-service communication. Service A publishes "InvoiceGenerated" events, while Service B (PDF generator) and Service C (email dispatcher) independently consume these events. What type of architecture is this?
A) Monolithic tightly-coupled architecture
B) Choreographed event-driven architecture
C) Centrally orchestrated batch architecture
D) Client-server polling architecture

14. What is the primary benefit of adding randomized jitter to exponential backoff algorithms in client-side retry logic?
A) It guarantees that retries will always succeed on the second attempt
B) It spreads out retry requests across a time window, preventing synchronized bursts (thundering herds) from re-overwhelming recovering dependencies
C) It compresses the payload size before retrying
D) It converts synchronous requests into asynchronous invocations

15. An application needs to process a continuous stream of millions of clickstream events per hour in strict chronological order per user session. Which AWS service is purpose-built to ingest and retain ordered, high-throughput streaming data for consumption by AWS Lambda?
A) Amazon SQS Standard Queue
B) Amazon Kinesis Data Streams
C) Amazon SNS
D) Amazon SimpleDB

16. A developer wants to run integration tests on an AWS Lambda function locally without deploying code to AWS or incurring cloud costs. Which tool allows invoking Lambda functions locally with simulated event payloads?
A) AWS CloudFormation console
B) AWS SAM CLI using `sam local invoke`
C) AWS CodeDeploy
D) AWS Elastic Beanstalk CLI

17. In an AWS Lambda function written in Python, where should the AWS SDK client (e.g., `boto3.client('dynamodb')`) be initialized for optimal performance across multiple invocations?
A) Inside the handler function on every invocation
B) Outside the handler function at global/module scope so it can be reused across warm invocations
C) In a separate local file on `/tmp`
D) Inside a try/except block within the handler's return statement

18. A developer is building a serverless REST API where API Gateway invokes a Lambda function. The API Gateway integration uses the Lambda proxy integration. Which type of invocation pattern does this represent?
A) Asynchronous invocation
B) Synchronous invocation (RequestResponse)
C) Poll-based invocation via Event Source Mapping
D) Scheduled cron invocation

19. When an AWS Lambda function is invoked asynchronously by Amazon S3 on an object upload, what happens if the function handler throws an unhandled error during execution?
A) Lambda immediately surfaces a 500 error to the client that uploaded the S3 object
B) Lambda automatically retries the invocation up to two more times (three total attempts) before dropping the event or sending it to an on-failure destination/DLQ
C) S3 deletes the uploaded object automatically
D) Lambda permanently disables the function

20. A developer is testing a Lambda function that processes SQS messages. The developer wants to inspect how long the function has been executing and how much time remains before the configured timeout occurs. Which context object method provides this in Python?
A) `context.get_execution_duration()`
B) `context.get_remaining_time_in_millis()`
C) `context.timeout_limit_seconds`
D) `context.check_time_left()`

21. Which architectural characteristic is essential for applications running on serverless compute platforms like AWS Lambda?
A) Stateful local memory retention between user requests
B) Stateless design where each execution relies only on passed event data or external managed datastores
C) Dedicated local persistent disk storage on `/var/log`
D) Manual thread pooling and socket management across servers

22. A team needs to build a notification system where a single payment event triggers SMS alerts, email confirmations, and database audit logs. The system must support easily adding a fourth notification channel in the future without modifying existing producers or consumers. Which pattern should they use?
A) Point-to-point queueing
B) Publish/Subscribe (Pub/Sub) Fan-out pattern
C) Monolithic synchronous RPC
D) Polling database triggers

### Lambda Execution Model & Lifecycle (23–40)

23. Which of the following describes the three phases of the AWS Lambda execution environment lifecycle, in order?
A) Create, Execute, Destroy
B) Init phase, Invoke phase, Shutdown phase
C) Cold phase, Warm phase, Terminate phase
D) Download phase, Run phase, Log phase

24. What is a "cold start" in AWS Lambda?
A) A hardware failure in the AWS data center
B) The latency incurred during the Init phase when AWS provisions a new execution environment, downloads code, and initializes runtime/dependencies before executing the handler
C) An invocation that fails due to cold weather throttling
D) A scheduled invocation triggered by Amazon EventBridge

25. How can a developer minimize cold start latency for an AWS Lambda function written in Node.js or Python? (Select TWO.)
A) Trim unnecessary dependencies and keep the deployment package size small
B) Initialize heavy SDK clients and static configuration outside the handler at global scope
C) Increase the function's timeout from 3 seconds to 15 minutes
D) Use a custom runtime built in C++ without any external libraries
E) Store all application data inside the function's `/tmp` directory

26. An application requires consistently low latency under 50ms for every request, with zero tolerance for cold start delays during morning traffic spikes. Which Lambda configuration eliminates cold starts for a configured number of execution environments?
A) Reserved concurrency
B) Provisioned concurrency
C) Maximum memory allocation (10,240 MB)
D) Dead-letter queues

27. A developer writes temporary scratch files to `/tmp` inside an AWS Lambda function. Which statement accurately describes the behavior and limits of the Lambda `/tmp` directory?
A) `/tmp` data is guaranteed to persist indefinitely across all future invocations regardless of environment reuse
B) `/tmp` provides between 512 MB and 10,240 MB of ephemeral storage that may be preserved across warm invocations of the same execution environment, but must not be relied upon for durable persistence
C) `/tmp` is shared across all concurrent execution environments in real-time
D) `/tmp` is read-only and cannot be written to by the handler

28. What is the maximum execution timeout that can be configured for a single AWS Lambda function invocation?
A) 5 minutes (300 seconds)
B) 15 minutes (900 seconds)
C) 30 minutes (1800 seconds)
D) 1 hour (3600 seconds)

29. A batch data processing job takes approximately 45 minutes to execute. A developer attempts to run this job as a single AWS Lambda function. What will occur?
A) The Lambda function will complete successfully after 45 minutes
B) The Lambda function will be terminated by AWS when it reaches its maximum timeout limit of 15 minutes (900 seconds)
C) Lambda will automatically fork the process into three 15-minute sub-functions
D) Lambda will charge 3x the standard rate for long-running executions

30. How does AWS Lambda allocate CPU power, network bandwidth, and disk I/O to a function?
A) CPU cores are configured independently from memory using the `CpuUnits` parameter
B) CPU, network bandwidth, and I/O scale proportionally with the configured memory allocation (from 128 MB to 10,240 MB)
C) All Lambda functions receive 2 dedicated vCPUs regardless of memory size
D) CPU allocation is determined by the size of the deployed zip file

31. A CPU-intensive image processing Lambda function configured with 512 MB memory runs in 12 seconds. The developer increases the memory allocation to 2048 MB. What is the most likely outcome?
A) Execution time will increase because larger memory environments take longer to start
B) Execution time will decrease significantly because the function receives more proportional CPU power, potentially reducing overall cost per invocation
C) Memory allocation has no effect on CPU-bound performance
D) The function will fail with an out-of-memory exception

32. What happens during the Shutdown phase of an AWS Lambda execution environment?
A) AWS sends a SIGTERM signal to runtime and extensions, allows a brief window for cleanup, and terminates the environment
B) AWS writes the entire memory state of the function to an S3 bucket
C) AWS restarts the physical host machine
D) Lambda immediately deletes the function's CloudWatch log group

33. Which two pieces of information are passed as arguments to the entry-point handler function in an AWS Lambda execution? (Select TWO.)
A) `event` — a JSON object containing the payload and context specific to the triggering service
B) `context` — an object providing runtime information such as remaining time, memory limit, and request ID
C) `credentials` — the plaintext AWS root account access keys
D) `container_id` — the Docker container host IP address
E) `cloudwatch_logs` — an array of previously logged strings

34. A developer needs to share a common authentication helper and standard logging library across 15 different AWS Lambda microservices without duplicating the code in each deployment zip package. Which Lambda feature should be used?
A) Lambda Extensions
B) Lambda Layers
C) Lambda Environment Variables
D) Lambda Aliases

35. What is the maximum number of Lambda Layers that can be attached to a single Lambda function?
A) 2
B) 5
C) 10
D) 20

36. An observability company builds a monitoring agent that collects telemetry directly from the Lambda runtime lifecycle (Init, Invoke, Shutdown) as a separate companion process. Which Lambda capability enables this integration?
A) Lambda Layers alone
B) Lambda Extensions
C) Lambda Container Images only
D) Lambda Destinations

37. A developer configures environment variables on a Lambda function for database credentials. What is the maximum total size of all environment variables combined for a single Lambda function?
A) 1 KB
B) 4 KB
C) 64 KB
D) 256 KB

38. Which statement regarding Lambda execution environment reuse is accurate?
A) Every incoming invocation always starts a brand new execution environment from scratch
B) Subsequent invocations handling traffic while an environment is active can reuse the initialized environment, skipping the Init phase
C) Execution environments are guaranteed to stay alive for exactly 24 hours
D) State stored in global variables is automatically synchronized across all concurrent environments

39. A developer wants to run a background cleanup task when a Lambda execution environment is shutting down. Which Lambda feature provides lifecycle events for extension shutdown?
A) Lambda Destinations
B) Lambda Runtime Extensions API
C) Lambda Versioning
D) Amazon CloudWatch Alarms

40. An application requires a proprietary Linux shared library (`.so` file) to execute its C++ binary. How can this binary be packaged and run on AWS Lambda? (Select TWO.)
A) Package the code and dependencies as an OCI-compliant container image (up to 10 GB) and deploy to Lambda
B) Package the binary and `.so` file inside a custom Lambda Layer and use a custom runtime (provided.al2 or provided.al2023)
C) Upload the binary directly to Amazon Route 53
D) Install the library using Windows PowerShell inside the Lambda console
E) Lambda cannot run compiled binaries under any circumstances

### Triggers, Event Source Mappings & Invocations (41–60)

41. Which of the following AWS services is a push-based, asynchronous trigger for AWS Lambda?
A) Amazon SQS
B) Amazon S3 event notifications
C) Amazon Kinesis Data Streams
D) Amazon DynamoDB Streams

42. How does AWS Lambda integrate with stream-based and queue-based event sources like Amazon SQS, Kinesis, and DynamoDB Streams?
A) The services push HTTP requests directly to Lambda's public IP address
B) Lambda's internal Event Source Mapping polls the source on the developer's behalf and invokes the function with batches of records
C) The developer must run an EC2 instance that reads messages and calls `lambda:Invoke`
D) The services write records directly to the function's `/tmp` folder

43. Which of the following is a push-based, synchronous trigger for AWS Lambda?
A) Amazon API Gateway (REST API / HTTP API)
B) Amazon S3 `s3:ObjectCreated:*`
C) Amazon EventBridge scheduled rule
D) Amazon SNS topic notification

44. When AWS Lambda polls an Amazon SQS standard queue via an Event Source Mapping, what happens when a batch of messages is successfully processed by the function without throwing an error?
A) The Lambda function handler must explicitly call `sqs:DeleteMessage` for each message
B) Lambda's Event Source Mapping automatically deletes the successfully processed messages from the SQS queue
C) The messages remain in the queue until the 14-day retention limit expires
D) SQS moves the messages to a Dead-Letter Queue automatically

45. A Lambda function processes records from an Amazon Kinesis Data Stream. A poison-pill record causes the function to throw an exception on every attempt. What is the default behavior of the stream poller, and what problem does it cause?
A) The record is discarded immediately; downstream processing continues
B) The poller retries the failing batch repeatedly until the data expires (e.g., 24 hours), blocking the entire shard from making progress
C) Kinesis deletes the entire stream
D) Lambda automatically routes the poison-pill record to Amazon S3

46. Which configuration on a stream Event Source Mapping (Kinesis/DynamoDB Streams) automatically breaks a failing batch into two smaller sub-batches to isolate a malformed record?
A) MaximumRecordAgeInSeconds
B) BisectBatchOnFunctionError
C) MaximumRetryAttempts
D) ParallelizationFactor

47. A developer configures an Event Source Mapping between an Amazon SQS queue and a Lambda function. The function handler takes 20 seconds to process a batch of messages. What should the SQS queue's Visibility Timeout be set to, according to AWS best practices?
A) Equal to the function timeout (20 seconds)
B) At least 6 times the Lambda function timeout (e.g., 120 seconds)
C) 0 seconds to allow immediate re-processing
D) Exactly 15 minutes

48. What is the concurrency scaling model when an AWS Lambda function is triggered by an Amazon Kinesis Data Stream without the `ParallelizationFactor` setting?
A) One Lambda worker per message in the stream
B) One concurrent Lambda execution per active shard in the stream
C) Up to 1,000 concurrent executions per shard
D) Concurrency is always locked at 1 for the entire stream

49. A developer wants to increase processing throughput for a high-volume Kinesis Data Stream where partition keys have high cardinality within each shard. Which Event Source Mapping setting allows up to 10 concurrent Lambda invocations per shard?
A) BatchSize
B) ParallelizationFactor (set to 10)
C) MaximumBatchingWindowInSeconds
D) TumblingWindowInSeconds

50. An asynchronous invocation of an AWS Lambda function fails all automatic retry attempts. The developer wants to automatically capture the error details, original payload, and stack trace without writing custom error-handling code. Which feature should be configured?
A) Lambda Function URL
B) Lambda On-Failure Destination (targeting SQS, SNS, EventBridge, or another Lambda)
C) CloudWatch Metric Filters
D) Step Functions Pass State

51. Which two AWS services can be configured as a Lambda Destination for asynchronous invocation outcomes (on-success or on-failure)? (Select TWO.)
A) Amazon SQS queue
B) Amazon EventBridge event bus
C) Amazon EBS volume
D) Amazon Route 53 hosted zone
E) AWS KMS key

52. A developer uses the AWS CLI to trigger a Lambda function asynchronously. Which invocation type parameter must be specified in the `aws lambda invoke` command?
A) `--invocation-type RequestResponse`
B) `--invocation-type Event`
C) `--invocation-type DryRun`
D) `--invocation-type AsyncBatch`

53. When a developer invokes a Lambda function using `--invocation-type Event`, what HTTP status code does the Lambda API return immediately upon accepting the payload?
A) 200 OK
B) 202 Accepted
C) 204 No Content
D) 400 Bad Request

54. A team uses an Amazon SNS topic to notify a Lambda function. If the Lambda function experiences an unhandled runtime exception, who handles the retries?
A) The SNS service retries according to its message delivery policy, and Lambda also applies its internal asynchronous invocation retry behavior (up to 2 retries)
B) The client that published the message to SNS must reconnect and retry
C) The message is immediately deleted without retries
D) SNS converts the message into an email to root

55. A developer is designing a Lambda function triggered by Amazon S3 object uploads. During peak hours, thousands of images are uploaded simultaneously. How does Lambda scale to handle these push events?
A) S3 buffers all events in a single internal queue and invokes one Lambda instance at a time
B) Lambda automatically scales out concurrent execution environments up to the account/burst concurrency limits
C) S3 drops events that exceed 100 uploads per second
D) The developer must pre-allocate EC2 instances for S3 triggers

56. An Event Source Mapping for Amazon SQS has a `BatchSize` of 10 and a `MaximumBatchingWindowInSeconds` of 30. Under what conditions will Lambda invoke the function?
A) Only when exactly 10 messages have arrived
B) Only after 30 seconds have passed, regardless of message count
C) As soon as 10 messages are available OR 30 seconds have elapsed, whichever occurs first
D) When the total payload size reaches 10 MB

57. A Lambda function processes messages from an Amazon SQS standard queue. A batch of 10 messages is received, but message #4 causes an unhandled error. To prevent reprocessing messages #1, #2, and #3, which SQS Event Source Mapping feature should the developer implement?
A) BisectBatchOnFunctionError
B) ReportBatchItemFailures (returning a list of failed message IDs in `batchItemFailures`)
C) Disabling batch processing entirely
D) Setting visibility timeout to 0

58. What happens when an AWS Lambda function triggered synchronously by Amazon API Gateway times out after 29 seconds (API Gateway's integration timeout ceiling)?
A) Lambda continues running for 15 minutes, but API Gateway returns a `504 Gateway Timeout` error to the client
B) API Gateway immediately retries the Lambda function three times
C) The client receives a `200 OK` with an empty body
D) API Gateway automatically provisions more memory to Lambda

59. Which two event sources support Lambda Destinations for on-failure reporting? (Select TWO.)
A) Asynchronous invocations from Amazon S3
B) Event Source Mappings from Amazon Kinesis Data Streams
C) Synchronous invocations from Application Load Balancer
D) Direct synchronous invocations from AWS SDK with `RequestResponse`
E) Invocations from API Gateway REST APIs

60. An application uses a DynamoDB Streams trigger with AWS Lambda. What is the maximum duration that change records remain available in DynamoDB Streams before they expire?
A) 1 hour
B) 24 hours
C) 7 days
D) 14 days

### Concurrency, Scaling & Throttling (61–74)

61. What is the default unreserved concurrency limit for all AWS Lambda functions in an AWS account within a single Region?
A) 100 concurrent executions
B) 1,000 concurrent executions
C) 10,000 concurrent executions
D) Unlimited

62. A developer notices that during a flash sale, an analytics Lambda function consumes 950 out of the account's 1,000 available concurrency units, causing critical customer checkout Lambda functions to fail with `429 TooManyRequestsException`. What should the developer configure to prevent the analytics function from starving the rest of the account?
A) Set a reserved concurrency limit on the analytics function (e.g., 50) and a reserved concurrency allocation on the checkout function
B) Increase the memory of the analytics function to 10,240 MB
C) Set the timeout of the checkout function to 1 second
D) Switch the analytics function to synchronous invocation

63. If a developer sets `ReservedConcurrentExecutions = 0` on an AWS Lambda function, what is the effect?
A) The function can scale infinitely without any concurrency limit
B) The function is effectively disabled and will reject all incoming invocation requests with throttling errors
C) The function only runs when no other function in the account is active
D) The function is permanently deleted from the account

64. What is the formula for calculating the concurrent executions of an AWS Lambda function?
A) `Concurrency = Invocations Per Second × Average Execution Duration (in seconds)`
B) `Concurrency = Memory Allocation / Timeout`
C) `Concurrency = Total Invocations / Number of Shards`
D) `Concurrency = Batch Size × Visibility Timeout`

65. A Lambda function processes 500 requests per second, and each execution takes an average of 200 milliseconds (0.2 seconds). How many concurrent executions does this function consume?
A) 25 concurrent executions
B) 100 concurrent executions
C) 500 concurrent executions
D) 1,000 concurrent executions

66. What error code is returned when a synchronous invocation of AWS Lambda exceeds available concurrency limits?
A) `500 InternalServerError`
B) `429 TooManyRequestsException`
C) `403 ForbiddenException`
D) `503 ServiceUnavailable`

67. What happens when an asynchronous invocation (e.g., from Amazon SNS) is throttled due to reaching account concurrency limits?
A) The event is dropped immediately and permanently lost
B) Lambda automatically places the event in an internal queue and retries the invocation for up to 6 hours with exponential backoff
C) Lambda raises an alert in the AWS Health Dashboard
D) SNS terminates the subscription

68. What is Lambda "burst concurrency"?
A) A temporary boost in memory allocation during heavy network I/O
B) The initial concurrency level that a function can reach immediately (between 500 and 3,000 depending on the Region) before scaling up by 500 additional concurrent executions per minute
C) An emergency failover mode that transfers execution to EC2
D) A feature that allows a single invocation to exceed the 15-minute timeout

69. A company has a backend relational database (Amazon RDS PostgreSQL) that can support a maximum of 50 concurrent database connections. A Lambda function connects directly to this database. During peak traffic, Lambda scales to 800 concurrent executions, causing database connection exhaustion and crashes. Which two solutions prevent Lambda from overwhelming the database? (Select TWO.)
A) Set `ReservedConcurrentExecutions = 50` on the Lambda function
B) Deploy Amazon RDS Proxy between Lambda and the PostgreSQL database to pool and manage database connections
C) Increase the Lambda function's memory to maximum
D) Increase the database timeout to 2 hours
E) Configure Lambda in provisioned concurrency mode with 500 instances

70. How does Provisioned Concurrency differ from Reserved Concurrency in AWS Lambda?
A) Reserved Concurrency allocates a maximum ceiling and guarantees capacity from the account pool; Provisioned Concurrency pre-warms execution environments so handlers respond immediately with zero cold starts
B) Reserved Concurrency eliminates cold starts; Provisioned Concurrency throttles invocations
C) Reserved Concurrency is billed per hour; Provisioned Concurrency is completely free
D) Provisioned Concurrency can only be configured for Python functions

71. A developer configures Application Auto Scaling on Lambda Provisioned Concurrency. What metric is commonly used as the target tracking metric?
A) `ProvisionedConcurrencyUtilization` (e.g., maintain 70% utilization)
B) `InvocationsPerSecond`
C) `DurationMilliseconds`
D) `ErrorCount`

72. An e-commerce API experiences a predictable surge of traffic every day at 9:00 AM. Invocations during this surge suffer from 800ms cold start latency. What is the most cost-effective and reliable solution?
A) Set up scheduled Application Auto Scaling to increase Provisioned Concurrency before 9:00 AM and scale it down after peak hours
B) Keep 1,000 Provisioned Concurrency instances running 24/7
C) Rewrite the entire application in Assembly
D) Run a continuous ping script every 5 seconds to keep all instances warm

73. A developer wants to publish a new version of a Lambda function and assign a human-readable name like `PROD` that points to version 2. Which Lambda resource represents this pointer?
A) Lambda Layer
B) Lambda Alias
C) Lambda Extension
D) Lambda Destination

74. When using Lambda Aliases with weighted routing, what capability does this provide during software releases?
A) Automatic rollback on CloudWatch alarms by shifting traffic (e.g., 90% to v1, 10% to v2) for canary deployments
B) Multi-region active-active replication
C) Automatic memory allocation optimization
D) Zero-cost deployment execution

### Networking, VPC & Security (75–90)

75. By default, what network environment does an AWS Lambda function run in?
A) Inside the default VPC of the account with full access to private RDS databases
B) In a secure, AWS-managed VPC with direct outbound access to the public internet and public AWS endpoints, but no direct access to private VPC resources
C) Inside an isolated on-premises data center
D) On a public EC2 instance with an Elastic IP

76. A developer needs an AWS Lambda function to query an Amazon ElastiCache (Redis) cluster deployed inside a private subnet of a custom VPC. What configuration is required?
A) Configure the Lambda function's VPC settings with the appropriate VPC ID, private Subnet IDs, and Security Group IDs
B) Make the ElastiCache cluster publicly accessible over the internet
C) Attach an Internet Gateway directly to the Lambda function
D) Deploy the Lambda function code onto the ElastiCache node

77. A developer attaches an AWS Lambda function to a private subnet in a VPC to access an internal Amazon RDS database. After this change, the function can query RDS, but calls to a public third-party weather API begin timing out. What is the root cause?
A) Lambda functions in a VPC cannot make HTTP calls
B) Attaching a Lambda function to private subnets removes its default internet route; outbound internet traffic requires a NAT Gateway in a public subnet with appropriate route table entries
C) The third-party API blocked AWS IP addresses
D) The Lambda function's execution role is missing the `ec2:CreateNetworkInterface` permission

78. Which IAM permissions must an AWS Lambda function's execution role have in order to connect to an Amazon VPC?
A) `ec2:CreateNetworkInterface`, `ec2:DescribeNetworkInterfaces`, `ec2:DeleteNetworkInterface` (or the AWS managed policy `AWSLambdaVPCAccessExecutionRole`)
B) `s3:GetObject` and `s3:PutObject`
C) `iam:PassRole` and `sts:AssumeRole`
D) `rds:Connect` and `elasticache:Connect`

79. How does AWS Lambda's Hyperplane ENI architecture improve VPC-enabled Lambda functions?
A) It eliminates the need for security groups
B) It uses shared, pre-provisioned Elastic Network Interfaces (ENIs) per subnet/security-group combination, drastically reducing cold start connection delays when launching new execution environments
C) It provides unlimited free bandwidth to the internet
D) It assigns a dedicated public IPv4 address to each concurrent invocation

80. If an AWS Lambda function inside a VPC needs to access Amazon DynamoDB and Amazon S3 without routing traffic through a NAT Gateway or traversing the public internet, what should the developer configure in the VPC?
A) Direct Connect connection
B) VPC Gateway Endpoints for DynamoDB and S3 (free of data processing charges)
C) A second Internet Gateway
D) An Elastic IP attached to the Lambda function

81. A Lambda function requires a database password. The security team mandates that credentials must never be stored as plaintext in environment variables or code repositories, and must support automatic rotation. Which AWS service should store the password?
A) Amazon S3 Glacier
B) AWS Secrets Manager
C) AWS CloudTrail
D) Amazon DynamoDB local

82. What is the function of the AWS Lambda Execution Role?
A) An IAM role that grants the caller permission to invoke the Lambda function
B) An IAM role assumed by the Lambda service when executing the function, granting permissions to access other AWS services (like DynamoDB, S3, CloudWatch Logs)
C) A role that manages AWS billing for the function
D) A local Linux user account inside the Lambda container

83. Which policy type is used to grant another AWS service or cross-account principal permission to invoke an AWS Lambda function (e.g., allowing Amazon S3 to call `lambda:InvokeFunction`)?
A) IAM Identity-Based User Policy
B) Lambda Resource-Based Policy (Function Policy)
C) S3 Bucket ACL
D) VPC Route Table Policy

84. A developer attempts to configure an S3 bucket notification to invoke a Lambda function. The console returns an error stating that S3 does not have permission to invoke the function. Which command resolves this issue?
A) `aws iam create-user`
B) `aws lambda add-permission --function-name MyFunction --principal s3.amazonaws.com --action lambda:InvokeFunction --source-arn <bucket-arn>`
C) `aws s3api put-bucket-acl --grant-read`
D) `aws sts get-caller-identity`

85. An application processes sensitive HIPAA-compliant medical records using AWS Lambda. The compliance officer requires all data at rest and in transit to be encrypted with customer-managed KMS keys. How should the developer configure Lambda environment variables?
A) Environment variables cannot be encrypted
B) Enable Lambda helper encryption at rest with a customer-managed AWS KMS key and use encryption helpers in the console for client-side decryption
C) Store the variables in a public GitHub repository
D) Save the keys inside the `/tmp` folder

86. A developer needs to restrict a Lambda function inside a VPC so that it can only receive inbound traffic from an Application Load Balancer and initiate outbound calls only to an RDS database port (5432). Which AWS security feature controls this traffic at the ENI level?
A) IAM Roles
B) Security Groups
C) S3 Bucket Policies
D) AWS WAF on S3

87. Which two statements regarding AWS Lambda execution in a VPC are true? (Select TWO.)
A) Lambda functions configured for VPC access should be associated with private subnets across multiple Availability Zones for high availability
B) Placing a Lambda function in a public subnet grants it an automatic public IP and direct internet access
C) VPC-enabled Lambda functions share ENIs created across the same subnet and security group combination
D) Lambda functions in a VPC cannot access Amazon CloudWatch Logs
E) Attaching to a VPC reduces the maximum function execution timeout to 5 minutes

88. A developer wants to invoke a Lambda function over HTTPS via a dedicated, built-in HTTP(S) endpoint without setting up an Application Load Balancer or Amazon API Gateway. Which Lambda feature provides this?
A) Lambda Function URLs
B) Lambda Aliases
C) Lambda Layers
D) Lambda Destinations

89. Which authentication modes are natively supported by Lambda Function URLs? (Select TWO.)
A) `AWS_IAM` (requiring SigV4 signed requests from authorized IAM identities)
B) `NONE` (publicly accessible endpoint, with optional CORS configuration)
C) `COGNITO_USER_POOLS` directly without API Gateway
D) `BASIC_AUTH` with plaintext username and password
E) `MUTUAL_TLS_ONLY` with hardcoded client certs

90. A developer configures a Lambda Function URL with `AuthType: NONE` for a webhook endpoint. How can the developer restrict cross-origin requests from web browsers to only allow invocations from `https://example.com`?
A) Configure CORS headers on the Function URL allowing `Access-Control-Allow-Origin: https://example.com`
B) Create an S3 lifecycle policy
C) Attach an IAM role to the browser
D) Delete the Function URL and switch to Amazon MQ

### Performance Optimization, Monitoring & Debugging (91–108)

91. A developer notices that a Python Lambda function that connects to Amazon RDS PostgreSQL runs slowly on initial requests because creating a new database connection takes 400ms. Subsequent invocations in the same container take only 15ms. How can this connection overhead be minimized across warm invocations?
A) Re-open the database connection inside the handler function on every invocation
B) Initialize the database connection object outside the handler at global scope so warm execution environments reuse the existing open connection
C) Increase the database connection timeout to 1 hour
D) Run the function in an EC2 instance instead

92. Which AWS service provides distributed tracing capabilities to visualize latency bottlenecks across a serverless architecture involving API Gateway, Lambda, and DynamoDB?
A) AWS CloudTrail
B) AWS X-Ray
C) Amazon CloudWatch Synthetics
D) AWS Trusted Advisor

93. How does a developer enable active AWS X-Ray tracing on an AWS Lambda function?
A) Install the X-Ray daemon on an EC2 instance
B) In the Lambda function configuration, set Tracing mode to `Active` (or in SAM `Tracing: Active`) and include the AWS X-Ray SDK in the function code
C) Add `xray:true` as an environment variable
D) X-Ray is automatically enabled on all AWS accounts and cannot be configured

94. What segment does AWS Lambda create in an X-Ray trace, and what is created by the X-Ray SDK inside the function?
A) Lambda creates the service parent segment (recording overhead, cold start init, and invoke duration); the X-Ray SDK creates subsegments for outgoing HTTP/AWS API calls
B) Lambda creates the subsegment; the SDK creates the root trace
C) X-Ray only captures errors and drops successful segments
D) Lambda requires an on-premises agent to generate X-Ray segments

95. In an AWS Lambda function's CloudWatch Logs stream, which log line format is automatically generated by the Lambda runtime at the end of every invocation to summarize billing and performance?
A) `[INFO] Execution successful`
B) `REPORT RequestId: ... Duration: 45.20 ms Billed Duration: 46 ms Memory Size: 128 MB Max Memory Used: 64 MB Init Duration: 150.12 ms`
C) `SUMMARY: Status=200, CPU=10%`
D) `DEBUG: Container terminated`

96. A developer examines a Lambda function's CloudWatch REPORT log line and sees `Memory Size: 512 MB` and `Max Memory Used: 498 MB`. What action should the developer take?
A) Decrease the memory allocation to 256 MB to save money
B) Increase the memory allocation (e.g., to 1024 MB) to provide a safety margin and avoid potential out-of-memory runtime crashes
C) Do nothing, because Lambda automatically allocates more memory when needed
D) Delete the CloudWatch log group

97. An AWS Lambda function is configured with 1024 MB memory and executes in 200ms. If the function is reconfigured to 2048 MB memory and its duration drops to 100ms, how does the compute cost per invocation change (ignoring free tier)?
A) Cost doubles
B) Cost remains approximately the same (1024 MB × 0.2s = 204.8 GB-s vs. 2048 MB × 0.1s = 204.8 GB-s) while user latency is halved
C) Cost is cut in half
D) Cost increases by 4x

98. Which CloudWatch metric indicates the number of Lambda invocations that failed due to unhandled exceptions in function code?
A) `Throttles`
B) `Errors`
C) `ConcurrentExecutions`
D) `DeadLetterErrors`

99. Which CloudWatch metric indicates that invocation requests were rejected because the function or account exceeded concurrency limits?
A) `Duration`
B) `Throttles`
C) `DeadLetterErrors`
D) `IteratorAge`

100. A developer is monitoring an AWS Lambda function that processes an Amazon Kinesis Data Stream. The `IteratorAge` CloudWatch metric is steadily increasing over several hours. What does this indicate?
A) The Lambda function is processing records faster than they arrive
B) The function is falling behind the stream, and records are taking longer to be processed after being written to the shard
C) The Kinesis stream has been deleted
D) The Lambda function execution environment has frozen

101. What two actions can reduce a growing `IteratorAge` on a stream-based Lambda Event Source Mapping (Kinesis/DynamoDB Streams)? (Select TWO.)
A) Increase the `ParallelizationFactor` to process multiple batches per shard concurrently
B) Optimize function execution time (e.g., increase memory or improve code performance)
C) Decrease the Kinesis retention period to 1 hour
D) Switch to an SQS standard queue
E) Set Lambda timeout to 1 second

102. A developer is packaging a Python Lambda function with external dependencies (`requests`, `numpy`, `pandas`). The zipped package size is 75 MB. What is the recommended method to deploy this package?
A) Paste the raw code directly into the Lambda inline code editor
B) Upload the `.zip` archive to an Amazon S3 bucket and configure the Lambda function code to point to the S3 object location
C) Email the zip file to AWS Support
D) Store the zip file inside an SQS message body

103. What is the uncompressed deployment package size limit for an AWS Lambda function (including layers)?
A) 50 MB
B) 250 MB
C) 500 MB
D) 10 GB

104. What is the maximum container image size supported by AWS Lambda when deploying functions packaged as Docker/OCI images?
A) 250 MB
B) 1 GB
C) 10 GB
D) 50 GB

105. A developer wants to optimize a container image deployed to AWS Lambda to minimize cold start download times. Which best practice should be followed?
A) Use multi-stage Docker builds to keep the final image minimal, using an official AWS base image for Lambda
B) Include all development build tools, compilers, and test suites in the final production image
C) Store the container image in a third-party private repository outside AWS
D) Build the image on an EC2 instance with 128 vCPUs

106. Which AWS tool allows developers to automatically analyze Lambda functions across memory configurations and find the optimal balance between execution speed and cost?
A) AWS Cost Explorer
B) AWS Lambda Power Tuning (open-source Step Functions state machine tool)
C) Amazon Inspector
D) AWS Budgets

107. When writing unit tests for a Lambda function that calls Amazon DynamoDB, how should the developer test the business logic without making live AWS network calls?
A) Run the test against production DynamoDB tables using admin credentials
B) Mock the `boto3` client/resource using libraries like `unittest.mock` or `moto`
C) Disable internet access on the development laptop
D) Hardcode mock responses inside the production Lambda handler

108. A developer wants to test a Lambda function in the AWS management console. What feature allows creating and saving reusable JSON event payloads representing different test scenarios (e.g., valid payload, missing fields, malformed data)?
A) CloudWatch Metrics
B) Console Shareable Test Events
C) Lambda Layers
D) Secrets Manager

### Integrative Scenarios & Decision Frameworks (109–125)

109. An online ticketing service anticipates a 50x spike in traffic when concert tickets go on sale at 10:00 AM. The backend is an API Gateway + Lambda architecture writing to DynamoDB. What combination of actions should the team take to guarantee readiness and prevent cold starts and throttling?
A) Pre-warm the system by configuring Provisioned Concurrency on the Lambda function prior to 10:00 AM, ensure DynamoDB has sufficient on-demand/provisioned capacity, and verify account concurrency quotas
B) Increase Lambda function timeout to 15 minutes and disable API Gateway caching
C) Deploy the API onto a single t3.micro EC2 instance
D) Switch the Lambda functions to run on local developer laptops

110. A media company processes user-submitted videos. Users upload files up to 2 GB to Amazon S3. The processing pipeline requires: (1) extracting audio, (2) running speech-to-text, (3) translating subtitles, and (4) encoding the video into multiple bitrates. Steps 1–3 take 2 minutes each; step 4 takes 35 minutes. How should the team architect this workflow?
A) Run the entire pipeline inside a single AWS Lambda function
B) Orchestrate the workflow using AWS Step Functions: use Lambda functions for steps 1–3 (under 15 min), and trigger an AWS Batch or Amazon ECS Fargate task for step 4 (exceeds 15 min limit)
C) Run everything on an SQS worker thread inside a Lambda function with a 60-minute timeout
D) Have S3 execute ffmpeg directly on the storage node

111. A payments microservice needs to: (1) process payment events from SQS, (2) record charges in a private Aurora PostgreSQL database inside a VPC, (3) call an external Stripe API over the public internet, and (4) ensure no duplicate charges occur upon SQS retries. Which architecture meets all requirements?
A) Lambda function attached to VPC private subnets with a NAT Gateway for Stripe access; idempotency key check in DynamoDB; SQS Event Source Mapping with DLQ
B) Lambda function running in default AWS network without VPC attachment, storing credit card numbers in local memory
C) EC2 instance with public IP running cron jobs without database encryption
D) Step Functions state machine with no error handling

112. A financial reporting service uses AWS Lambda to generate end-of-month summaries. The function frequently runs out of memory when processing large customer datasets. What immediate change should the developer make?
A) Split the function across multiple AWS accounts
B) Increase the function's memory configuration in the Lambda console or IaC template (up to 10,240 MB)
C) Compress the operating system files inside `/tmp`
D) Convert the function to an S3 event notification

113. An e-commerce backend needs to notify three independent microservices whenever a user cancels an order: (1) inventory restock, (2) customer refund, (3) CRM update. The order service must publish the event once and return immediately. If any microservice fails, it should retry independently without affecting others. Which architecture implements this?
A) Order service publishes to an Amazon SNS topic; three separate Amazon SQS queues subscribe to the topic; each queue triggers its own dedicated Lambda function
B) Order service calls each Lambda function sequentially using synchronous `RequestResponse` invocations
C) Order service writes the cancellation event to a local text file on an EC2 instance
D) Order service creates three new Lambda functions dynamically on every request

114. A mobile game uses AWS Lambda to calculate daily leaderboards. The function takes 8 minutes to run on 128 MB memory and times out during holiday traffic. Analysis shows the calculation is heavily CPU-bound. What is the most effective way to optimize this function?
A) Increase the memory allocation to 1536 MB or higher, which proportionally increases CPU power and drastically cuts duration
B) Increase the timeout to 3 hours
C) Switch from Python to Bash script
D) Reduce the memory to 64 MB to reduce compute complexity

115. A developer is building a serverless webhook receiver for third-party GitHub pull request events. The webhook receiver must validate HMAC signatures, write the event payload to an S3 bucket, and return a `200 OK` within 2 seconds. Detailed analytics processing on the payload takes up to 4 minutes. How should this be designed?
A) Single synchronous Lambda function that validates, writes to S3, processes analytics for 4 minutes, and then returns 200 OK
B) Webhook Lambda validates signature, puts payload to S3, publishes an event to an Amazon SQS queue, and immediately returns 200 OK; a second worker Lambda asynchronously processes the analytics from SQS
C) Process everything client-side in the GitHub browser tab
D) Store the webhook in an in-memory variable on an EC2 instance

116. A company has 20 Lambda functions in an account. Function A has an unhandled bug that causes an infinite loop of asynchronous retries, consuming 1,000 concurrent executions. Functions B through T start failing with throttling errors. What is the immediate mitigation and the architectural fix?
A) Set `ReservedConcurrentExecutions = 0` on Function A to immediately stop the runaway function, and allocate appropriate reserved concurrency to critical business functions
B) Delete the entire AWS account and recreate it
C) Restart the AWS Lambda regional data center
D) Increase the timeout of Functions B through T

117. An image processing pipeline receives 500 images per second. Each image upload emits an event to an SQS queue. A Lambda function processes the queue with a batch size of 10. The image processing takes 2 seconds per batch. How many concurrent Lambda executions will be active in steady state?
A) 10 concurrent executions
B) 100 concurrent executions (50 batches/sec × 2 sec duration = 100 concurrent executions)
C) 500 concurrent executions
D) 1,000 concurrent executions

118. A developer is designing an AWS Lambda function that must query an Amazon RDS MySQL instance. Under high concurrency, opening hundreds of new database connections causes RDS to run out of memory. Which AWS service should be introduced between Lambda and RDS?
A) Amazon RDS Proxy
B) Amazon DynamoDB Accelerator (DAX)
C) Amazon CloudFront
D) AWS AppSync

119. A developer writes a Lambda function that queries a DynamoDB table. The developer observes high latency on the first invocation after deployment, but subsequent invocations are very fast. What two factors contribute to this initial latency? (Select TWO.)
A) The Lambda runtime initialization and cold start of the execution environment
B) Initializing the DynamoDB SDK client, loading SSL certificates, and establishing the initial TCP/TLS connection
C) DynamoDB rebuilding its primary key index on every deployment
D) The local laptop's network latency affecting the cloud execution
E) AWS billing validation checks

120. A company needs to deploy a legacy 8 GB machine learning model with specialized binary dependencies onto AWS Lambda. The zipped code package exceeds 250 MB. How can this function be deployed?
A) It cannot be deployed to Lambda; it must run on a physical on-premises server
B) Package the model and dependencies into a Docker container image (up to 10 GB), push to Amazon ECR, and configure Lambda to deploy from the container image
C) Split the zip file into 32 separate 25 MB files and upload via FTP
D) Convert the model into plain text environment variables

121. An AWS Lambda function is configured to process an SQS queue. The function fails on a specific message due to a database schema mismatch. The message is retried repeatedly, causing other valid messages in the queue to be delayed. What configuration should be applied to the SQS queue?
A) Set `DelaySeconds = 900`
B) Configure a Dead-Letter Queue (DLQ) with `maxReceiveCount = 3` on the redrive policy
C) Delete the queue and recreate it as a FIFO queue
D) Increase SQS message retention to 30 days

122. A team needs to implement a serverless API where requests are authenticated via custom token logic in a Lambda function before invoking the backend service. Which API Gateway feature accomplishes this?
A) Lambda Authorizer (formerly Custom Authorizer)
B) Lambda Layer
C) Lambda Extension
D) VPC Gateway Endpoint

123. A developer wants to ensure that an AWS Lambda function can safely read and write to an Amazon S3 bucket named `company-analytics-2026`. Which policy and attachment should be configured?
A) Attach an IAM role with an S3 policy granting `s3:GetObject` and `s3:PutObject` on `arn:aws:s3:::company-analytics-2026/*` to the Lambda execution role
B) Make the S3 bucket public to all users
C) Hardcode the AWS root account credentials in the Lambda code
D) Attach an S3 bucket policy allowing all actions to `Principal: "*"`

124. A Lambda function processes orders. When an order fails validation, the developer wants to send a notification to an SNS topic without writing custom SNS publishing code inside the function error handler. Which feature enables this for asynchronous invocations?
A) Lambda On-Failure Destination pointing to the SNS topic ARN
B) Amazon Route 53 Health Checks
C) SQS Dead-Letter Queue with manual polling
D) CloudWatch Alarms sending email to SNS

125. An architect reviews a serverless design and needs to confirm whether Lambda is the right compute choice. Which combination of workload characteristics makes AWS Lambda the ideal compute platform?
A) Predictable 24/7 continuous 100% CPU utilization running for days with no variation
B) Event-driven execution, short-to-medium duration (<15 minutes), bursty or unpredictable traffic, with automatic scaling and zero idle compute costs
C) Long-running monolithic enterprise application requiring 64 GB RAM and 4 hours of uninterrupted execution per transaction
D) Real-time sub-millisecond audio streaming requiring low-level hardware kernel modifications

---

## Answer Key & Explanations

1. B — Decomposing a monolith into independent microservices isolates failure blast radiuses and allows services to scale independently.
2. B — An event-driven architecture with asynchronous S3 events decouples upload acceptance from background processing (resizing, moderation).
3. B — AWS Step Functions provides centralized orchestration with visual state management, branching, and automated error handling/retries.
4. A — The fan-out pattern using an SNS topic subscribed by multiple SQS queues delivers a single published event to multiple independent consumer queues.
5. B — Idempotency keys checked via DynamoDB conditional writes (`attribute_not_exists`) prevent duplicate side-effect execution upon retries.
6. B — Retries simply repeat the invocation; without an idempotency mechanism, retrying an unacknowledged successful operation executes the side effect twice.
7. B — Stateless compute tiers externalize session state to shared stores like DynamoDB or ElastiCache, allowing instances to scale and terminate freely.
8. B — Direct synchronous calls create tight coupling where downstream delays cascade upstream; introducing an SQS queue decouples the components.
9. B — Retrying simultaneously causes a thundering herd; exponential backoff with jitter randomizes delays and spreads out traffic bursts.
10. B — A Dead-Letter Queue (DLQ) captures repeatedly failing poison-pill messages after `maxReceiveCount` attempts, preventing queue blockage.
11. A & B — Choreography is decentralized event-driven pub/sub; orchestration is centralized coordination with explicit control flow (e.g., Step Functions).
12. A & C — Fault tolerance in distributed processing combines exponential backoff with jitter for retries, and DLQs to isolate permanent failures.
13. B — Services reacting independently to published events via an event bus (EventBridge) is a classic choreographed event-driven architecture.
14. B — Jitter randomizes retry intervals across clients, breaking synchronization and preventing thundering-herd spikes against recovering dependencies.
15. B — Amazon Kinesis Data Streams is purpose-built for ingesting, storing, and ordering high-throughput streaming data for Lambda consumption.
16. B — `sam local invoke` executes Lambda functions locally inside Docker containers simulating the real Lambda runtime.
17. B — Initializing SDK clients outside the handler at global/module scope allows them to be reused across warm invocations, avoiding cold connection setup.
18. B — API Gateway Lambda proxy integration is a synchronous (RequestResponse) invocation where the caller waits for the Lambda response.
19. B — For asynchronous invocations, Lambda automatically retries failed executions up to two more times (3 total attempts) before routing to a DLQ or destination.
20. B — `context.get_remaining_time_in_millis()` returns the milliseconds remaining before invocation timeout.
21. B — Serverless compute relies on stateless design where execution environments can be created, destroyed, or scaled horizontally at any time.
22. B — Pub/Sub fan-out (e.g., SNS to multiple SQS queues) allows publishing once to notify multiple independent subscribers, with easy extensibility.
23. B — The Lambda execution lifecycle consists of the Init phase, Invoke phase, and Shutdown phase.
24. B — A cold start is the initialization overhead when AWS creates a new execution environment, downloads code, and runs initialization logic.
25. A & B — Minimizing deployment package size and initializing heavy objects outside the handler both reduce Init phase duration.
26. B — Provisioned Concurrency pre-warms execution environments so they are always initialized and ready to serve requests with zero cold start.
27. B — `/tmp` provides 512 MB to 10,240 MB of ephemeral scratch space that may persist across warm invocations of the same container, but is not durable storage.
28. B — The maximum configurable execution timeout for an AWS Lambda function is 15 minutes (900 seconds).
29. B — Lambda enforces a strict 15-minute hard limit; any invocation exceeding this is terminated automatically.
30. B — CPU power, network bandwidth, and disk I/O scale proportionally with the configured memory allocation (128 MB to 10,240 MB).
31. B — Increasing memory increases proportional CPU power; CPU-bound tasks execute faster and can sometimes cost less overall due to reduced duration.
32. A — During Shutdown, Lambda sends a SIGTERM signal, allows a short window for runtime/extension cleanup, and terminates the environment.
33. A & B — Lambda handlers accept `event` (invocation payload) and `context` (runtime methods and metadata).
34. B — Lambda Layers allow sharing libraries, custom runtimes, and dependencies across multiple functions without duplicating them in deployment packages.
35. B — A single Lambda function can be configured with up to 5 Lambda Layers.
36. B — Lambda Extensions run as companion processes that hook into the Lambda lifecycle (Init, Invoke, Shutdown) for monitoring, security, and governance.
37. B — The total combined size of all environment variables for a Lambda function cannot exceed 4 KB.
38. B — When execution environments are kept warm for subsequent invocations, the Init phase is skipped and global state is preserved.
39. B — The Lambda Runtime Extensions API exposes lifecycle events allowing extensions to perform cleanup during Shutdown.
40. A & B — Compiled binaries and custom dependencies can be deployed via OCI container images (up to 10 GB) or Lambda Layers with custom runtimes (`provided.al2/al2023`).
41. B — Amazon S3 event notifications invoke Lambda asynchronously using a push model.
42. B — Lambda uses internal Event Source Mappings (pollers) to poll queues/streams and batch records into function invocations.
43. A — Amazon API Gateway invokes Lambda synchronously using the `RequestResponse` invocation type, waiting for the HTTP response.
44. B — When a Lambda function processing an SQS Event Source Mapping returns successfully without errors, Lambda automatically deletes the batch from SQS.
45. B — In stream processing (Kinesis/DynamoDB Streams), a failing record blocks the entire shard because records must be processed in order.
46. B — `BisectBatchOnFunctionError` automatically splits a failing stream batch in half upon error to isolate the single bad record.
47. B — AWS recommends setting SQS Visibility Timeout to at least 6 times the Lambda function timeout to allow sufficient time for retries.
48. B — By default, Lambda processes Kinesis data streams with one concurrent worker per active shard to preserve order.
49. B — `ParallelizationFactor` (up to 10) allows concurrent Lambda invocations per shard when partition keys are well-distributed.
50. B — Lambda On-Failure Destinations automatically route async invocation execution records (including errors, stack trace, and payload) to SQS, SNS, EventBridge, or Lambda.
51. A & B — SQS queues, SNS topics, EventBridge event buses, and other Lambda functions are valid targets for Lambda Destinations.
52. B — `--invocation-type Event` specifies asynchronous invocation in the AWS CLI.
53. B — An asynchronous invocation accepted by Lambda immediately returns HTTP status code `202 Accepted`.
54. A — SNS applies its own delivery retry policy, and once delivered to Lambda asynchronously, Lambda applies its 2 automatic retries.
55. B — Lambda automatically scales concurrent execution environments to match incoming push events up to burst and account concurrency limits.
56. C — Event Source Mappings trigger an invocation when either `BatchSize` records are collected OR `MaximumBatchingWindowInSeconds` elapses.
57. B — `ReportBatchItemFailures` allows returning a list of failed message IDs in `batchItemFailures`, ensuring only failed messages are retried.
58. A — API Gateway enforces a maximum integration timeout of 29 seconds, returning a 504 Gateway Timeout if the backend does not respond in time.
59. A & B — Lambda Destinations support asynchronous invocations (e.g., S3) and stream Event Source Mappings (Kinesis/DynamoDB Streams).
60. B — DynamoDB Streams retains change data records for exactly 24 hours.
61. B — The default account concurrency limit for AWS Lambda is 1,000 concurrent executions per Region.
62. A — Setting reserved concurrency on the noisy analytics function limits its concurrency ceiling, while reserving concurrency for checkout protects its capacity.
63. B — Setting `ReservedConcurrentExecutions = 0` completely disables the function and throttles all incoming invocations.
64. A — Concurrency is calculated as `Invocations Per Second × Average Execution Duration (in seconds)`.
65. B — `500 req/sec × 0.2 sec = 100 concurrent executions`.
66. B — When concurrency limits are exceeded, synchronous invocations return `429 TooManyRequestsException`.
67. B — Throttled asynchronous invocations are queued internally by Lambda and retried automatically for up to 6 hours.
68. B — Burst concurrency is the initial burst capacity (500–3,000 depending on Region) available immediately before growing by 500/minute.
69. A & B — Capping Lambda concurrency via `ReservedConcurrentExecutions = 50` and deploying Amazon RDS Proxy for connection pooling both protect the database.
70. A — Reserved Concurrency sets a ceiling and guarantees capacity from the pool; Provisioned Concurrency pre-warms environments to eliminate cold starts.
71. A — `ProvisionedConcurrencyUtilization` is the standard metric used by Application Auto Scaling to adjust warm capacity.
72. A — Scheduled Application Auto Scaling scales up Provisioned Concurrency prior to known morning traffic spikes and scales down afterward.
73. B — A Lambda Alias is a named pointer (e.g., `PROD`) that references a specific published function version.
74. A — Lambda Aliases with weighted routing support canary deployments by shifting traffic percentages between two versions (e.g., 90/10) with automated rollback.
75. B — Lambda runs by default in an AWS-managed VPC with internet access but no access to private customer VPC subnets.
76. A — Accessing private VPC resources like ElastiCache requires configuring the Lambda function with VPC subnets and security groups.
77. B — VPC attachment removes default internet access; outbound internet calls from private subnets require a NAT Gateway in a public subnet.
78. A — The `AWSLambdaVPCAccessExecutionRole` managed policy grants permission to create, describe, and delete network interfaces (ENIs) in the VPC.
79. B — Hyperplane ENIs provide shared, pre-provisioned network interfaces across Lambda functions in the same subnet/SG, eliminating cold-start ENI attachment delays.
80. B — VPC Gateway Endpoints for S3 and DynamoDB allow direct, private access from VPC subnets without NAT Gateways or internet traversal.
81. B — AWS Secrets Manager securely stores database credentials with encryption and supports automated key rotation.
82. B — The Execution Role is an IAM role assumed by Lambda to grant the function permissions to interact with other AWS services.
83. B — A Resource-Based Policy (Function Policy) grants external services or accounts permission to invoke the Lambda function.
84. B — `aws lambda add-permission` adds a statement to the function's resource-based policy granting S3 permission to invoke `lambda:InvokeFunction`.
85. B — Lambda supports environment variable encryption helpers using customer-managed KMS keys for at-rest security.
86. B — Security Groups act as a virtual firewall at the ENI level to control inbound and outbound traffic rules.
87. A & C — Lambda in VPC should use private subnets across multiple AZs for HA, and functions share Hyperplane ENIs with matching subnet/SG configs.
88. A — Lambda Function URLs provide a dedicated HTTPS endpoint directly built into the function without API Gateway or ALB.
89. A & B — Lambda Function URLs support `AWS_IAM` authentication (SigV4) and `NONE` (public access with optional CORS).
90. A — Configuring CORS headers directly on the Function URL restricts web browser cross-origin requests to specified origins like `https://example.com`.
91. B — Initializing database connections outside the handler allows warm execution environments to reuse existing connections across invocations.
92. B — AWS X-Ray provides end-to-end distributed tracing and service maps across serverless components.
93. B — Setting Tracing mode to `Active` and including the X-Ray SDK instruments the function for distributed tracing.
94. A — Lambda generates the parent service segment (init, invoke, overhead); the X-Ray SDK generates subsegments for downstream calls.
95. B — The `REPORT` log line records RequestId, Duration, Billed Duration, Memory Size, Max Memory Used, and Init Duration.
96. B — Using 498 MB out of 512 MB is dangerously close to the limit; increasing memory provides a safety margin against out-of-memory crashes.
97. B — Compute cost is proportional to GB-seconds (`Memory × Duration`); doubling memory while halving duration yields identical cost (`204.8 GB-s`) with better latency.
98. B — The `Errors` metric tracks invocations that failed due to unhandled function exceptions.
99. B — The `Throttles` metric tracks invocation requests rejected due to concurrency limits.
100. B — Increasing `IteratorAge` means the Lambda stream consumer is falling behind and data is aging in the shard before being processed.
101. A & B — Increasing `ParallelizationFactor` (more workers per shard) and optimizing function duration both increase processing throughput and lower IteratorAge.
102. B — Packages larger than 50 MB should be uploaded to an Amazon S3 bucket and referenced in the Lambda function configuration.
103. B — The uncompressed deployment package size limit (code plus all layers) for AWS Lambda is 250 MB.
104. C — AWS Lambda supports OCI container images up to 10 GB in size.
105. A — Multi-stage Docker builds based on official AWS base images strip build-time dependencies, keeping images small and fast to pull.
106. B — AWS Lambda Power Tuning is an open-source Step Functions tool that benchmarks functions across memory sizes to find the best cost/performance balance.
107. B — Mocking the `boto3` client using `unittest.mock` or `moto` isolates business logic without making live cloud network calls.
108. B — Console Shareable Test Events allow saving and sharing JSON payloads for testing different invocation scenarios directly in the console.
109. A — Pre-warming via Provisioned Concurrency, verifying DynamoDB capacity, and checking concurrency quotas ensures readiness for massive traffic spikes.
110. B — Step Functions orchestrates the workflow, using Lambda for short tasks (<15 min) and ECS/Fargate/Batch for long video encoding (>15 min).
111. A — VPC private subnets with NAT Gateway for Stripe, DynamoDB idempotency checks, and SQS with DLQ satisfy all networking and fault-tolerance needs.
112. B — Increasing memory allocation (up to 10,240 MB) resolves out-of-memory errors for memory-intensive data processing.
113. A — SNS topic with three subscribed SQS queues (fan-out pattern) allows publishing once while each consumer retries independently.
114. A — Increasing memory allocation proportionally increases CPU allocation, significantly speeding up CPU-bound tasks.
115. B — Decoupling fast validation (returns 200 OK immediately) from background processing via an SQS queue ensures responsive webhooks.
116. A — Setting `ReservedConcurrentExecutions = 0` immediately halts the runaway function, while reserved concurrency protects critical workloads.
117. B — `500 images/sec ÷ 10 images/batch = 50 batches/sec`. Concurrency = `50 batches/sec × 2 sec = 100 concurrent executions`.
118. A — Amazon RDS Proxy pools and shares database connections, protecting RDS from connection exhaustion under high Lambda concurrency.
119. A & B — Cold start initialization of the runtime/container and the initial TLS/SDK client setup account for the latency on the first invocation.
120. B — Deploying as an OCI container image (up to 10 GB) via Amazon ECR allows running large models and custom dependencies on Lambda.
121. B — A Dead-Letter Queue (DLQ) with `maxReceiveCount = 3` isolates poison messages after 3 failed attempts, unblocking other queue messages.
122. A — Lambda Authorizers execute custom bearer token or request parameter authentication logic in Lambda before routing requests to backend integrations.
123. A — The principle of least privilege requires granting `s3:GetObject` and `s3:PutObject` on the specific bucket ARN via the Lambda execution role.
124. A — Lambda On-Failure Destinations automatically route failed asynchronous invocation details to an SNS topic without writing custom error code.
125. B — Lambda is optimal for event-driven, short/medium duration workloads with bursty/unpredictable traffic seeking zero idle costs and automatic scaling.
