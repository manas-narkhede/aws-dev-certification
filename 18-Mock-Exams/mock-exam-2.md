# DVA-C02 Full Practice Mock Exam 2 (65 Questions)

**Exam Format & Rules**:
- **Total Questions**: 65
- **Time Limit**: 130 minutes (2 minutes per question)
- **Passing Score**: 720 / 1000 (approx. 72% / 47 out of 65 questions)
- **Domain Weighting**:
  - **Domain 1**: Development with AWS Services (32% — Questions 1–21)
  - **Domain 2**: Security (26% — Questions 22–38)
  - **Domain 3**: Deployment (24% — Questions 39–54)
  - **Domain 4**: Troubleshooting & Optimization (18% — Questions 55–65)

---

### Domain 1: Development with AWS Services (Questions 1–21)

1. A developer is designing a serverless payment processing backend. When an order arrives, an AWS Lambda function must deduct money from a customer balance and update an inventory count across two separate DynamoDB tables. Both updates must either succeed simultaneously or fail completely without leaving inconsistent data. Which DynamoDB feature should the developer use?
A) DynamoDB Transactions (`TransactWriteItems`)
B) DynamoDB Batch Operations (`BatchWriteItem`)
C) DynamoDB Global Secondary Indexes
D) DynamoDB Streams

2. An application uploads high-resolution 500 MB video files to Amazon S3. What is the recommended method to upload these files reliably, allowing paused or failed parts to be resumed without restarting the entire upload?
A) S3 Multipart Upload API
B) Single-part `s3:PutObject`
C) S3 Select
D) S3 Batch Operations

3. An application needs to decouple order ingestion from asynchronous background processing. Orders arrive in unpredictable bursts of up to 10,000 per minute. The system must buffer requests and ensure that no orders are dropped if backend worker instances scale slowly. Which AWS service is designed for this point-to-point queuing?
A) Amazon SQS (Simple Queue Service)
B) Amazon SNS Topic
C) Amazon AppStream 2.0
D) AWS AppConfig

4. A developer is configuring an Amazon API Gateway REST API. The developer wants to reduce latency for API callers and decrease the number of requests sent to the backend AWS Lambda function for GET requests that return identical results for 10 minutes. What feature should be enabled?
A) API Gateway Caching (on the stage)
B) API Gateway Usage Plans
C) API Gateway Mutual TLS
D) API Gateway Canary Release

5. An application uses Amazon DynamoDB. The table stores customer support tickets. The partition key is `CustomerId` and the sort key is `TicketId`. The developer wants to query all tickets opened by a specific customer in descending order of `TicketId`. Which parameter in the `Query` API call reverses the sort order?
A) `ScanIndexForward: false`
B) `SortOrder: "DESC"`
C) `ReverseIndex: true`
D) `KeyConditionExpression: "DESC"`

6. An application processes IoT sensor telemetry. Multiple downstream applications (an anomaly detector, an hourly aggregator, and an S3 archiver) all need to consume the exact same stream of sensor data independently with replay capability. Which AWS streaming service supports multiple concurrent consumers reading with distinct shard iterators?
A) Amazon Kinesis Data Streams
B) Amazon SQS Standard Queue
C) Amazon SNS Standard Topic
D) AWS Step Functions

7. A developer is building a notification system. When a new product is announced, a single event must be delivered simultaneously to an email delivery service, a mobile push notification service, and an audit SQS queue. Which AWS messaging pattern implements this fan-out architecture?
A) Amazon SNS topic with subscriptions to Amazon SQS queues, HTTP endpoints, and email addresses
B) Amazon SQS FIFO queue with 3 consumer groups
C) AWS Step Functions Express Workflow
D) Amazon Kinesis Video Streams

8. An order processing workflow requires executing four steps in order: (1) validate payment, (2) check inventory, (3) ship package, and (4) send confirmation email. If step 2 fails due to out-of-stock items, the system must trigger a refund task. Which AWS service orchestrates this multi-step state machine?
A) AWS Step Functions
B) Amazon SQS
C) Amazon SNS
D) AWS CodeBuild

9. An AWS Lambda function executes a CPU-intensive data compression algorithm on incoming JSON files. The developer notices the function execution duration is 12 seconds with 512 MB of memory configured. How can the developer reduce the function's execution time?
A) Increase the Lambda function memory allocation (which proportionally increases allocated vCPU power)
B) Increase the Lambda timeout to 15 minutes
C) Convert the function to an S3 bucket
D) Deploy the function in a private VPC subnet

10. A developer needs to update a single attribute `Status = 'SHIPPED'` on an existing item in an Amazon DynamoDB table without re-writing or overwriting the other attributes of the item. Which DynamoDB API operation should be used?
A) `UpdateItem`
B) `PutItem`
C) `BatchWriteItem`
D) `TransactGetItems`

11. A gaming company requires microsecond read latency for global player leaderboards that receive millions of read queries per second against an Amazon DynamoDB table. Which in-memory caching service integrates seamlessly with DynamoDB without changing application query logic?
A) Amazon DynamoDB Accelerator (DAX)
B) Amazon ElastiCache for Memcached
C) Amazon CloudFront
D) Amazon S3 Standard

12. A developer is designing a serverless REST API that accepts customer registrations. If the database write fails, the application must retry with exponential backoff. Which client-side retry practice prevents retry storms from overwhelming a recovering database?
A) Adding randomized full jitter to the exponential backoff calculation
B) Retrying immediately with 0 delay in a while loop
C) Retrying at fixed 100-millisecond intervals
D) Restarting the client application process

13. An application processes financial transactions from an Amazon Kinesis data stream using AWS Lambda. The team wants to ensure that if an unhandled runtime exception occurs on a batch of records, the failed records are sent to an SQS queue after 3 retries without discarding the rest of the stream. What feature should be configured on the Lambda Event Source Mapping?
A) On-Failure Destination (targeting an SQS queue) with `MaximumRetryAttempts: 3` and `BisectBatchOnFunctionError: true`
B) Deleting the Kinesis shard
C) Increasing Lambda timeout to 15 minutes
D) Disabling Kinesis sharding

14. A developer is designing an asynchronous workflow where an S3 upload triggers an AWS Lambda function. If the Lambda function fails all retry attempts (2 retries for asynchronous invocation), the event payload must be saved for developer inspection. Which Lambda configuration captures these failed async events?
A) Lambda Asynchronous Invocation Dead-Letter Queue (DLQ) or On-Failure Destination (targeting SQS or SNS)
B) Lambda Provisioned Concurrency
C) S3 Cross-Region Replication
D) CloudWatch Logs Insights

15. An application uses Amazon SQS. The developer notices that when a consumer begins processing a message, other consumers do not receive that message for 60 seconds. What SQS setting controls this behavior?
A) Visibility Timeout
B) Delivery Delay
C) Message Retention Period
D) Receive Message Wait Time

16. A developer wants to download only the first 500 bytes of a 2 GB file stored in Amazon S3 to inspect the file header without downloading the entire object. What HTTP request header should be passed to S3 `GetObject`?
A) `Range: bytes=0-499`
B) `Content-Length: 500`
C) `x-amz-limit: 500`
D) `PartNumber: 1`

17. An application uses Amazon DynamoDB. The developer needs to retrieve all items from the `Products` table where `Category = 'Electronics'`. `Category` is NOT the table's partition key. What DynamoDB feature enables efficient querying on `Category` without performing a full table scan?
A) Global Secondary Index (GSI) with `Category` as the partition key
B) Local Secondary Index (LSI) with a different partition key
C) DynamoDB Streams
D) DynamoDB Transactions

18. A developer wants to build a serverless REST API using Amazon API Gateway that passes incoming HTTP requests directly to an Amazon DynamoDB table without writing any intermediate AWS Lambda function code. Which API Gateway integration type enables this direct connection?
A) AWS Service Integration (HTTP/REST direct mapping using VTL mapping templates)
B) Lambda Proxy Integration
C) Mock Integration
D) VPC Link Integration

19. An application running on AWS Lambda writes items to an Amazon DynamoDB table. The developer wants to ensure that a banking withdrawal operation does not reduce a user's account balance below zero. Which parameter in `UpdateItem` ensures the balance is sufficient before deducting funds?
A) `ConditionExpression: "AccountBalance >= :withdrawalAmount"`
B) `KeyConditionExpression: "AccountBalance > 0"`
C) `ProjectionExpression: "AccountBalance"`
D) `FilterExpression: "AccountBalance >= :withdrawalAmount"`

20. An application uses Amazon SQS FIFO queues to process stock trading orders. The developer wants orders for stock ticker `AAPL` to be processed in strict chronological sequence, while orders for `GOOG` are processed in parallel. How should the messages be structured?
A) Set `MessageGroupId` to the stock ticker symbol (e.g., `AAPL` or `GOOG`)
B) Create a separate AWS account for each stock ticker
C) Set `MessageDeduplicationId` to the stock ticker symbol
D) Enable SQS Delay Queue

21. A developer wants to deploy a REST API on Amazon API Gateway that connects privately to an Application Load Balancer inside a private Amazon VPC without exposing the ALB to the public internet. Which API Gateway feature enables this private connectivity?
A) API Gateway VPC Link (for Private REST/HTTP APIs)
B) API Gateway Edge-Optimized Endpoint
C) Route 53 Public Hosted Zone
D) AWS WAF Rate-Based Rule

---

### Domain 2: Security (Questions 22–38)

22. A mobile application authenticates users using Amazon Cognito User Pools. Once authenticated, users must be granted temporary AWS IAM credentials allowing them to upload files to their personal folder in an Amazon S3 bucket (`s3://my-bucket/${cognito-identity.amazonaws.com:sub}/*`). Which Amazon Cognito component issues these temporary scoped AWS credentials?
A) Amazon Cognito Identity Pools (Federated Identities)
B) Amazon Cognito User Pools alone
C) AWS Secrets Manager
D) AWS IAM User Groups

23. A developer is deploying an AWS Lambda function with environment variables containing an API key. To comply with corporate policy, the API key must not be visible in plaintext in the AWS Lambda console or in `GetFunction` API responses. How should the developer protect this variable?
A) Use Lambda Encryption Helpers with an AWS KMS Customer Managed Key to encrypt the environment variable client-side before deployment, decrypting it inside the function code using `kms:Decrypt`
B) Base64 encode the variable in the console
C) Delete the environment variable after deployment
D) Use AWS Systems Manager Parameter Store Standard Tier with `String` type

24. What is the maximum data payload size that can be directly encrypted or decrypted using an AWS KMS Customer Master Key (CMK) in a single `kms:Encrypt` API call?
A) 4 KB
B) 256 KB
C) 5 MB
D) 5 GB

25. An application needs to encrypt 50 MB PDF files before uploading them to Amazon S3. What cryptographic mechanism must the application implement to encrypt data exceeding KMS's direct 4 KB payload limit?
A) Envelope Encryption (using KMS `GenerateDataKey` to obtain a plaintext data key for local encryption and storing the encrypted data key alongside the ciphertext)
B) Calling `kms:Encrypt` in a loop for each 4 KB chunk
C) Base64 encoding the PDF file
D) Using S3 Object Lock

26. An enterprise requires database credentials for an Amazon Aurora MySQL database to be rotated automatically every 60 days with zero application downtime. Which AWS service natively manages this automated credential rotation?
A) AWS Secrets Manager (using an automated Lambda rotation template)
B) AWS Systems Manager Parameter Store Standard Tier
C) AWS KMS Key Rotation
D) Amazon DynamoDB TTL

27. A developer is storing a third-party API secret in AWS Systems Manager Parameter Store as a `SecureString`. Which AWS service is used to encrypt and decrypt the parameter value?
A) AWS Key Management Service (AWS KMS)
B) AWS Certificate Manager (ACM)
C) Amazon S3 SSE-S3
D) Amazon Cognito

28. An application running in a Docker container on Amazon ECS on AWS Fargate needs to make API calls to Amazon DynamoDB and Amazon S3. What is the AWS best practice for providing credentials to the application?
A) Assign an IAM Role to the ECS Task Definition's `taskRoleArn` (ECS Task Role)
B) Hardcode IAM access keys in the Dockerfile `ENV` instructions
C) Store AWS access keys in an unencrypted S3 bucket
D) Embed root account credentials in the container entrypoint script

29. A developer wants to restrict authenticated mobile users so that each user can read and write ONLY items in an Amazon DynamoDB table where the partition key matches their unique Cognito Identity ID. What condition key must be included in the IAM policy?
A) `"Condition": { "ForAllValues:StringEquals": { "dynamodb:LeadingKeys": ["${cognito-identity.amazonaws.com:sub}"] } }`
B) `"Condition": { "StringEquals": { "aws:username": "${aws:PrincipalArn}" } }`
C) `"Condition": { "NumericEquals": { "dynamodb:Select": 1 } }`
D) `"Condition": { "Bool": { "aws:MultiFactorAuthPresent": "true" } }`

30. A developer is assigned an IAM policy that allows `s3:GetObject` on all buckets. However, an attached Permissions Boundary does NOT include `s3:GetObject` in its allowed actions. What is the result when the developer attempts to download an S3 object?
A) Access is Denied, because an IAM entity can only perform actions that are allowed by BOTH the identity-based policy AND the Permissions Boundary
B) Access is Allowed
C) S3 prompts the user for MFA
D) The object is downloaded in ciphertext

31. A security policy requires that all requests to an Amazon S3 bucket must use TLS encryption in transit. Which S3 bucket policy statement enforces this requirement?
A) `Effect: Deny`, `Action: s3:*`, `Condition: { "Bool": { "aws:SecureTransport": "false" } }`
B) `Effect: Allow`, `Action: s3:GetObject`, `Condition: { "StringEquals": { "s3:x-amz-acl": "public-read" } }`
C) `Effect: Deny`, `Action: s3:PutObject`, `Condition: { "NumericLessThan": { "s3:TlsVersion": 1.3 } }`
D) `Effect: Allow`, `Action: s3:*`, `Condition: { "Null": { "aws:PrincipalTag": "true" } }`

32. An application deployed on an Application Load Balancer needs protection against SQL injection attacks, Cross-Site Scripting (XSS), and automated web scraping bots. Which AWS service should be associated with the ALB?
A) AWS WAF (Web Application Firewall)
B) Amazon GuardDuty
C) AWS Shield Standard only
D) Amazon Inspector

33. An application running in Account A needs to decrypt S3 objects encrypted with an AWS KMS Customer Managed Key (CMK) in Account B. Which two policy configurations are required? (Select TWO.)
A) The KMS Key Policy in Account B must grant `kms:Decrypt` permissions to Account A's IAM Role ARN
B) The IAM Policy attached to the application role in Account A must grant `kms:Decrypt` on the KMS Key ARN in Account B
C) Account A must assume the root account of Account B
D) S3 Block Public Access must be disabled in Account B
E) The KMS key must be deleted and recreated in Account A

34. A security team enables "Automatic Key Rotation" on a Customer Managed Key (CMK) in AWS KMS. What happens to the Key ID, Key ARN, and historical data encrypted with previous versions of the key?
A) The Key ID and ARN remain unchanged; KMS automatically retains previous backing keys to decrypt older data transparently without requiring re-encryption
B) All previously encrypted data is permanently erased
C) The Key ARN changes and the application must be redeployed with the new Key ID
D) The user must manually download and re-encrypt all historical data

35. A developer wants to provision a public SSL/TLS certificate for an API domain name (`api.mycompany.com`) to terminate HTTPS on an Application Load Balancer. Which service provides free public certificates with automated DNS-based renewal?
A) AWS Certificate Manager (ACM)
B) AWS KMS
C) AWS Secrets Manager
D) AWS CloudHSM

36. An application uses Amazon Cognito User Pools. The developer wants to automatically enrich the Cognito ID Token with custom claims (such as `user_tier = 'premium'`) during user login before the token is returned to the client. Which Cognito feature should be used?
A) Pre Token Generation Lambda Trigger
B) Post Authentication Lambda Trigger
C) Pre Sign-up Lambda Trigger
D) Custom Message Lambda Trigger

37. A developer executes an AWS CLI command that fails with an encoded authorization failure message. Which AWS STS API action decrypts the error message to display detailed evaluation reasons?
A) `sts:DecodeAuthorizationMessage`
B) `sts:GetCallerIdentity`
C) `sts:AssumeRole`
D) `sts:GetSessionToken`

38. A company allows a third-party SaaS management platform to assume an IAM role in its AWS account. What condition key should be added to the IAM role trust policy to protect against the "Confused Deputy" vulnerability?
A) `sts:ExternalId`
B) `aws:SourceIp`
C) `aws:PrincipalTag`
D) `aws:SecureTransport`

---

### Domain 3: Deployment (Questions 39–54)

39. A developer is preparing an `appspec.yml` file for deploying an application to Amazon EC2 instances using AWS CodeDeploy. Which lifecycle hook is executed to run health checks and verify that the application is functioning properly before traffic is routed to it?
A) `ValidateService`
B) `ApplicationStart`
C) `BeforeInstall`
D) `AfterInstall`

40. An AWS CodeBuild project needs to run unit tests, compile Java code, and create a deployment artifact. In which file at the root of the source repository must these build commands and phases be defined?
A) `buildspec.yml`
B) `appspec.yaml`
C) `template.json`
D) `Dockerfile`

41. A developer wants to deploy a new version of an AWS Lambda function using AWS CodeDeploy. The deployment must shift 10% of traffic every 1 minute until 100% of traffic is on the new version. If any CloudWatch alarms fire during deployment, the deployment must automatically roll back. Which deployment configuration should be selected?
A) `LambdaLinear10PercentEvery1Minute`
B) `LambdaCanary10Percent10Minutes`
C) `LambdaAllAtOnce`
D) `LambdaBlueGreenImmediate`

42. A developer is defining a serverless application using AWS SAM. Which resource type in `template.yaml` declares a serverless DynamoDB table with a single primary key?
A) `AWS::Serverless::SimpleTable`
B) `AWS::DynamoDB::Table`
C) `AWS::Serverless::Database`
D) `AWS::S3::Bucket`

43. A developer wants to test a SAM-based Lambda function locally against a running local HTTP server simulating Amazon API Gateway. Which SAM CLI command starts a local HTTP server on `http://localhost:3000`?
A) `sam local start-api`
B) `sam local invoke`
C) `sam deploy --guided`
D) `sam build`

44. A developer is writing an AWS CloudFormation template. The developer wants to reference the value of a parameter named `EnvironmentName` inside a string resource name (e.g., `my-bucket-${EnvironmentName}`). Which intrinsic function should be used?
A) `!Sub` (or `Fn::Sub`)
B) `!Ref`
C) `!GetAtt`
D) `!Select`

45. A developer wants to preview the exact AWS resources that will be modified, added, or deleted before applying updates to an existing CloudFormation stack. Which CloudFormation feature provides this preview?
A) CloudFormation Change Sets
B) CloudFormation StackSets
C) CloudFormation Drift Detection
D) CloudFormation Rollback

46. An application is deployed to AWS Elastic Beanstalk. The development team needs to deploy updates by provisioning an entirely new environment, deploying the new code there, running integration tests, and then swapping DNS URLs to shift traffic with zero downtime. Which deployment strategy does this describe?
A) Blue/Green Deployment
B) All-at-Once Deployment
C) Rolling Deployment
D) In-Place Deployment

47. A developer has 15 AWS Lambda functions written in Python that all share the same common database access library. The developer wants to manage and update this shared library in a single central location without bundling it into each function's individual zip package. Which Lambda feature should be used?
A) AWS Lambda Layers
B) Lambda Environment Variables
C) Lambda Extensions
D) Amazon S3 Glacier

48. A CI/CD deployment pipeline in AWS CodePipeline fails when deploying an AWS CloudFormation template that creates an IAM Role, returning an `InsufficientCapabilitiesException`. How can this error be resolved?
A) Add `CAPABILITY_IAM` or `CAPABILITY_NAMED_IAM` to the CloudFormation deployment action configuration in CodePipeline
B) Add `CAPABILITY_AUTO_EXPAND`
C) Disable CloudFormation rollbacks
D) Grant the root user administrator privileges

49. An AWS CodeBuild project builds a Docker container image that must be pushed to Amazon Elastic Container Registry (ECR). What command in the `pre_build` phase authenticates Docker with the Amazon ECR registry?
A) `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com`
B) `docker login -u admin -p secret`
C) `aws ecr login`
D) `aws iam create-access-key`

50. A developer wants to use AWS AppConfig to deploy dynamic application configuration changes at runtime without restarting application processes or redeploying code. What AppConfig feature allows validating configuration syntax against a JSON schema before deployment?
A) AppConfig Validators (JSON Schema or Lambda validator)
B) AppConfig Deployment Strategies
C) AppConfig Profiles
D) CloudWatch Alarms

51. A developer is deploying a containerized application to Amazon ECS on AWS Fargate using AWS CodeDeploy for blue/green deployments. Which file defines the task definition ARN, container name, and container port for the replacement task set?
A) `appspec.yaml`
B) `buildspec.yml`
C) `dockerrun.aws.json`
D) `template.yaml`

52. In an AWS CloudFormation template, which section defines the input values that users can customize when creating or updating a stack?
A) `Parameters`
B) `Resources`
C) `Outputs`
D) `Mappings`

53. A developer wants to identify whether an AWS resource managed by CloudFormation had its properties modified directly in the AWS console outside of CloudFormation. Which CloudFormation feature detects this configuration drift?
A) CloudFormation Drift Detection
B) CloudFormation Change Sets
C) CloudFormation StackSets
D) CloudFormation Rollback

54. An application is deployed on Amazon ECS on AWS Fargate. What two parameters in the ECS Task Definition specify the compute resources allocated to the task? (Select TWO.)
A) `cpu`
B) `memory`
C) `instance_type`
D) `ebs_volume_size`
E) `ami_id`

---

### Domain 4: Troubleshooting & Optimization (Questions 55–65)

55. An application returns an HTTP 504 Gateway Timeout error when calling an Amazon API Gateway REST API integrated with an AWS Lambda function. What is the most likely root cause?
A) The Lambda function execution duration exceeded API Gateway's maximum integration timeout limit of 29 seconds
B) The Lambda function returned invalid JSON syntax
C) The client sent an invalid query parameter
D) API Gateway ran out of memory

56. An application querying an Amazon DynamoDB table receives frequent `ProvisionedThroughputExceededException` errors during flash sales. Monitoring reveals that total consumed capacity is well below the table's total provisioned limits. What is the root cause?
A) A hot partition caused by an uneven distribution of read/write traffic across partition keys
B) The DynamoDB table is encrypted with KMS
C) The table has too many Local Secondary Indexes
D) The application is using eventually consistent reads

57. A developer is investigating an issue where requests to a microservices application experience high latency. The architecture includes API Gateway, Lambda, and DynamoDB. Which AWS tool provides a visual Service Map displaying nodes color-coded by error rate and latency to pinpoint the exact bottleneck?
A) AWS X-Ray Service Map
B) Amazon CloudWatch Dashboards
C) AWS CloudTrail Event History
D) Amazon Inspector

58. In AWS X-Ray, what is the difference between an Annotation and Metadata attached to a trace segment?
A) Annotations are indexed key-value pairs that can be searched and used with filter expressions in the X-Ray console; Metadata is non-indexed contextual debugging data that cannot be searched across traces
B) Metadata is indexed; Annotations are not
C) Annotations can only contain numbers; Metadata contains strings
D) Annotations are deleted after 5 minutes

59. A developer writes a query in Amazon CloudWatch Logs Insights to find the 20 slowest requests in an application log group. Which query syntax accomplishes this?
A)
```
fields @timestamp, requestId, latencyMs
| filter latencyMs > 1000
| sort latencyMs desc
| limit 20
```
B) `select * from logs where latency > 1000 order by latency desc limit 20`
C) `find slowest 20`
D) `get logs --slow`

60. An application logs error events in structured JSON: `{"statusCode": 500, "errorType": "DatabaseTimeout", "service": "orders"}`. Which CloudWatch feature extracts a custom metric `OrderDatabaseErrors` from these logs in real time as they arrive?
A) CloudWatch Logs Metric Filters
B) CloudWatch Synthetics
C) CloudWatch Metric Math
D) Amazon Athena

61. A developer wants to record custom business metrics (such as `CompletedOrders` and `OrderValue`) from an AWS Lambda function with zero additional network latency and without incurring `PutMetricData` per-call API fees. Which pattern should be implemented?
A) CloudWatch Embedded Metric Format (EMF) outputting structured JSON with an `_aws` metadata object to standard output
B) Synchronous `PutMetricData` API calls inside the handler loop
C) Writing metrics to local `/tmp` and deleting them on exit
D) Sending metrics via Amazon SES email

62. A developer needs to audit who deleted an Amazon DynamoDB table at 2:00 AM on a weekend. Which AWS service records the IAM identity, API action (`DeleteTable`), timestamp, source IP address, and request parameters?
A) AWS CloudTrail
B) Amazon CloudWatch Logs
C) AWS X-Ray
D) Amazon CodeGuru Profiler

63. An application running on Amazon ECS consumes 95% CPU under normal load. The developer wants a visual flame graph identifying the exact methods and lines of code consuming the most CPU cycles at runtime. Which AWS service provides this profiling?
A) Amazon CodeGuru Profiler
B) Amazon CodeGuru Reviewer
C) AWS CloudTrail
D) AWS Trusted Advisor

64. A developer is testing an AWS Lambda function attached to a VPC that queries an Amazon ElastiCache for Redis cluster in private subnets. The function invocation times out after 15 seconds. What is the most common misconfiguration?
A) The ElastiCache Security Group does not allow inbound TCP traffic on port 6379 from the Lambda function's Security Group
B) Redis does not support VPC connections
C) Lambda functions cannot access ElastiCache
D) ElastiCache requires an Internet Gateway

65. An application calling an external AWS API receives an HTTP 429 Too Many Requests status code (`ThrottlingException`). What retry strategy should the developer implement in the client application code?
A) Exponential backoff with full jitter
B) Immediate retries in an infinite loop with zero delay
C) Crashing the application process
D) Hardcoding a fixed 1-second sleep before retrying once

---

## Answer Key & Explanations

1. A — `TransactWriteItems` executes atomic all-or-nothing writes across multiple DynamoDB tables with ACID compliance.
2. A — Multipart Upload API optimizes upload throughput and fault tolerance for objects > 100 MB by uploading independent parts in parallel.
3. A — Amazon SQS decouples application components, buffering high-volume traffic bursts and ensuring zero message loss.
4. A — API Gateway Stage Caching stores responses in memory, reducing backend Lambda executions and lowering latency for repeat GET requests.
5. A — Setting `ScanIndexForward: false` reverses the query result order to sort descending based on the sort key.
6. A — Amazon Kinesis Data Streams supports multiple independent consumers with separate shard iterators and up to 365 days of data replay.
7. A — Amazon SNS is a pub/sub fan-out service that delivers messages simultaneously to multiple subscribed endpoints (SQS, email, HTTP).
8. A — AWS Step Functions Standard Workflows coordinate multi-step state machines with branching logic, retries, and compensation states.
9. A — Increasing Lambda memory proportionally scales allocated vCPU power, accelerating CPU-bound compression algorithms.
10. A — `UpdateItem` modifies specific attributes of an existing item in-place without overwriting unaffected attributes.
11. A — Amazon DynamoDB Accelerator (DAX) provides seamless in-memory microsecond read caching without application code changes.
12. A — Exponential backoff with randomized jitter spreads out retry intervals, preventing thundering herds on struggling downstream services.
13. A — `BisectBatchOnFunctionError` isolates failed records by recursively splitting batches and sending failed records to an SQS DLQ.
14. A — Asynchronous Lambda dead-letter queues (DLQs) or On-Failure Destinations capture failed event payloads for analysis after all retries fail.
15. A — Visibility Timeout hides messages during processing; if processing exceeds this duration, the message becomes visible to other consumers.
16. A — Amazon S3 Select runs SQL expressions directly on S3 data to retrieve only the required subset of data, reducing network transfer and latency.
17. A — A Global Secondary Index (GSI) allows querying DynamoDB tables on non-key attributes (like `Category`).
18. A — API Gateway AWS Service Integration connects directly to DynamoDB using VTL mapping templates without Lambda compute costs.
19. A — `ConditionExpression: "AccountBalance >= :withdrawalAmount"` validates balance sufficiency before executing the update atomically.
20. A — Setting `MessageGroupId` to the stock ticker symbol ensures strict in-order processing per ticker while processing different tickers concurrently.
21. A — API Gateway VPC Links connect REST/HTTP APIs privately to Application Load Balancers inside private VPC subnets.
22. A — Cognito Identity Pools exchange authenticated User Pool tokens for temporary, scoped AWS IAM credentials via AWS STS.
23. A — KMS Encryption Helpers encrypt Lambda environment variables client-side before deployment, masking them from console viewers.
24. A — AWS KMS Customer Master Keys can directly encrypt or decrypt payloads up to 4 KB per API call.
25. A — Envelope Encryption uses KMS `GenerateDataKey` to encrypt large files locally with data keys protected by KMS master keys.
26. A — AWS Secrets Manager provides built-in native automated password rotation for Amazon RDS using AWS Lambda rotation templates.
27. A — AWS KMS is the underlying cryptographic service used to encrypt and decrypt `SecureString` parameters in Parameter Store.
28. A — The ECS Task Role (`taskRoleArn`) grants container application code temporary credentials to access DynamoDB and S3.
29. A — `dynamodb:LeadingKeys` matching `${cognito-identity.amazonaws.com:sub}` limits users to reading/writing items matching their own identity ID.
30. A — An IAM entity can only perform actions that are allowed by BOTH the identity-based policy AND the Permissions Boundary.
31. A — Denying `s3:*` when `aws:SecureTransport: false` strictly enforces HTTPS encryption in transit on S3 buckets.
32. A — AWS WAF protects Layer 7 applications (ALB, API Gateway, CloudFront) against SQLi, XSS, and rate-based DDoS attacks.
33. A & B — Cross-account KMS access requires permissions in the KMS Key Policy (Account B) AND the caller's IAM Policy (Account A).
34. A — KMS key rotation keeps the Key ID and ARN unchanged and retains historical backing keys to decrypt older data transparently.
35. A — AWS Certificate Manager (ACM) provisions free public SSL/TLS certificates with automated DNS-based renewal for integrated AWS services.
36. A — The Pre Token Generation Lambda Trigger customizes and enriches ID token claims with custom attributes before issuance.
37. A — `sts:DecodeAuthorizationMessage` decodes and displays authorization failure details for permission troubleshooting.
38. A — The `sts:ExternalId` condition prevents the Confused Deputy vulnerability during third-party cross-account role assumption.
39. A — The `ValidateService` lifecycle hook in CodeDeploy executes health check scripts to verify application functionality after installation.
40. A — `buildspec.yml` placed at the repository root defines CodeBuild build phases, environment variables, and artifact outputs.
41. A — `LambdaLinear10PercentEvery1Minute` shifts 10% of traffic every minute until all traffic is routed to the new version.
42. A — `AWS::Serverless::SimpleTable` is the SAM resource type for declaring a lightweight serverless DynamoDB table.
43. A — `sam local start-api` spawns a local HTTP server emulating API Gateway endpoints on `http://localhost:3000`.
44. A — `!Sub` (or `Fn::Sub`) substitutes variables and concatenates strings dynamically in CloudFormation templates.
45. A — CloudFormation Change Sets generate a detailed preview of proposed resource modifications and replacements prior to execution.
46. A — Blue/Green deployment using Elastic Beanstalk Swap Environment URLs provides zero-downtime deployment with instant DNS rollback.
47. A — AWS Lambda Layers allow sharing common dependencies, libraries, and custom runtimes across multiple Lambda functions.
48. A — CloudFormation requires `CAPABILITY_IAM` or `CAPABILITY_NAMED_IAM` acknowledgment when templates create or modify IAM resources.
49. A — `aws ecr get-login-password` pipes an authentication token to `docker login` to authenticate the Docker client with ECR.
50. A — AppConfig Validators (JSON Schema or Lambda) validate configuration syntax prior to deployment, preventing invalid deployments.
51. A — `appspec.yaml` defines the task definition ARN, container name, and port for ECS blue/green deployments in CodeDeploy.
52. A — The `Parameters` section in CloudFormation templates defines customizable user input values for stack deployments.
53. A — CloudFormation Drift Detection identifies differences between the expected template configuration and actual live resource properties.
54. A & B — Task-level `cpu` and `memory` parameters in ECS Task Definitions specify compute limits for Fargate tasks.
55. A — HTTP 504 Gateway Timeout occurs when the backend Lambda function exceeds the API Gateway 29-second timeout.
56. A — A hot partition occurs when access patterns concentrate on a narrow key range, exceeding single-partition throughput limits.
57. A — AWS X-Ray Service Maps visually display interconnected service nodes, latency metrics, and error rates to pinpoint bottlenecks.
58. A — Annotations are indexed and searchable; Metadata is non-indexed contextual debugging data visible on individual traces.
59. A — The query filters for `latencyMs > 1000`, sorts descending, and limits results to 20 rows in CloudWatch Logs Insights.
60. A — CloudWatch Logs Metric Filters scan incoming log lines for patterns and extract custom metrics to graph and alarm on.
61. A — Embedded Metric Format (EMF) extracts custom metrics asynchronously from JSON logs without `PutMetricData` API fees or latency.
62. A — AWS CloudTrail records an authoritative audit log of control-plane API activity, including identity, API action, timestamp, and IP.
63. A — Amazon CodeGuru Profiler generates runtime flame graphs identifying specific CPU-intensive methods in running applications.
64. A — Connection timeouts to ElastiCache are typically caused by missing inbound rules on port 6379 in the Redis Security Group.
65. A — HTTP 429 / `ThrottlingException` errors should be handled by retrying with exponential backoff and jitter.
