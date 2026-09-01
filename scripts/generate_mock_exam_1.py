#!/usr/bin/env python3
"""Generate mock-exam-1.md and mock-exam-2.md for Module 18: Mock Exams"""

import os

mock1_text = """# DVA-C02 Full Practice Mock Exam 1 (65 Questions)

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

1. A developer is building a serverless e-commerce application. When an order is placed, an AWS Lambda function must read user profile information from an Amazon DynamoDB table. The application requires consistent, single-digit millisecond latency for reads, and the developer wants to minimize read cost. Which read consistency model should be used by default?
A) Strongly Consistent Reads
B) Eventually Consistent Reads
C) Transactional Reads
D) Global Secondary Index Reads

2. An application writes large payload objects (between 10 MB and 50 MB) to an Amazon S3 bucket. The developer wants to optimize upload throughput and resilience to network interruptions. Which Amazon S3 feature should the developer implement?
A) Multipart Upload API
B) S3 Transfer Acceleration alone without multipart
C) S3 Select
D) Single-part `PutObject` with increased socket timeout

3. A developer is designing an order processing pipeline using AWS Lambda and Amazon SQS. The Lambda function polls messages from an SQS queue. If the Lambda function encounters an unhandled runtime error while processing a message, what happens to the message in SQS?
A) The message is immediately deleted from the queue
B) The message remains in the queue and becomes visible to other consumer instances once the Visibility Timeout expires
C) The message is moved to Amazon S3 Glacier
D) SQS automatically pauses all queue operations for 1 hour

4. A developer is configuring an Amazon API Gateway REST API with AWS Lambda integration. The frontend web client needs to access the API from a different domain name (`https://www.myfrontend.com`). When making requests, the browser blocks responses with a CORS error. What must the developer configure on API Gateway?
A) Enable CORS on the API Gateway resource and ensure the Lambda proxy response returns an `Access-Control-Allow-Origin: "https://www.myfrontend.com"` header (or `"*"`)
B) Disable HTTPS on API Gateway
C) Create a Route 53 CNAME record for the Lambda function
D) Switch API Gateway to Private endpoint mode

5. A developer is writing an application that queries an Amazon DynamoDB table named `Orders`. The query needs to filter results by `OrderStatus = 'PENDING'` and `OrderDate >= '2026-01-01'`. The table's partition key is `CustomerId` and the sort key is `OrderDate`. Which DynamoDB API operation and parameter should the developer use for the lowest latency and cost?
A) `Query` operation specifying `KeyConditionExpression` on `CustomerId` and `OrderDate`, with a `FilterExpression` for `OrderStatus`
B) `Scan` operation with `FilterExpression` across the entire table
C) `BatchGetItem` specifying all possible order IDs
D) `TransactGetItems` without key conditions

6. An application processes real-time financial market data streams. Multiple independent consumer applications need to process the same streaming records concurrently with custom offsets and replay capability up to 7 days. Which AWS service should be used for data ingestion?
A) Amazon Kinesis Data Streams
B) Amazon SQS Standard Queue
C) Amazon SNS Topic
D) AWS Step Functions

7. A developer is building an application that sends transactional emails to customers when account events occur. The developer wants to publish email messages asynchronously to a topic that fans out to both an email delivery service and an audit queue. Which AWS messaging service should be used?
A) Amazon SNS (Simple Notification Service)
B) Amazon SQS FIFO Queue
C) Amazon Kinesis Video Streams
D) AWS AppConfig

8. A developer wants to implement a stateful serverless workflow that coordinates multiple AWS Lambda functions, executes parallel tasks, and waits for a human manager approval step via email (up to 7 days). Which AWS service should be selected?
A) AWS Step Functions (Standard Workflow)
B) AWS Step Functions (Express Workflow)
C) Amazon SQS Delay Queue
D) Amazon EventBridge Pipes

9. An application running on AWS Lambda needs to write temporary image files during processing. The images can be up to 3 GB in size. Lambda's default `/tmp` directory has 512 MB of storage. How can the developer accommodate these files?
A) Increase the Lambda Ephemeral Storage (`/tmp`) setting up to 10,240 MB (10 GB)
B) Attach an Amazon EBS volume to the Lambda function
C) Mount an Amazon S3 Glacier vault
D) Increase Lambda function timeout to 15 minutes

10. A developer needs to retrieve 50 specific items from an Amazon DynamoDB table by their primary keys in a single network round-trip. Which DynamoDB API operation should be used?
A) `BatchGetItem`
B) `Query`
C) `Scan`
D) `TransactWriteItems`

11. A developer is building a web application that requires sub-millisecond read access to relational SQL query results from an Amazon Aurora PostgreSQL database. The query results change infrequently. Which caching service should be placed between the application and database?
A) Amazon ElastiCache for Redis
B) Amazon CloudFront
C) Amazon DynamoDB Accelerator (DAX)
D) Amazon S3 Standard-IA

12. An application uses Amazon DynamoDB. The developer needs to ensure that when a customer's account balance is updated, an audit log entry is simultaneously written to an audit table. Both operations must either succeed together or fail together with ACID guarantees. Which DynamoDB API operation should be used?
A) `TransactWriteItems`
B) `BatchWriteItem`
C) `PutItem` with a conditional expression
D) `UpdateItem` with optimistic locking

13. A developer is writing an AWS Lambda function that processes incoming events from an Amazon Kinesis data stream. If the Lambda function encounters a poison pill record that causes a failure, what configuration prevents the entire shard from being blocked indefinitely?
A) Enable `BisectBatchOnFunctionError: true`, configure `MaximumRetryAttempts`, and set an On-Failure Destination to an SQS Dead-Letter Queue
B) Increase Lambda memory to 10 GB
C) Delete the Kinesis data stream
D) Disable Kinesis sharding

14. A developer is designing a serverless API using Amazon API Gateway and AWS Lambda. The API must handle sudden spikes of 10,000 requests per second. The developer wants to avoid cold-start latency for time-critical endpoints. What Lambda feature should be configured?
A) Provisioned Concurrency
B) Reserved Concurrency
C) Increasing Lambda function timeout to 15 minutes
D) Deploying Lambda inside an Amazon VPC

15. An application uses Amazon SQS to process background jobs. The developer notices that when a worker EC2 instance takes 40 seconds to process a message, another worker receives and begins processing the same message after 30 seconds. What is the cause of this duplicate processing?
A) The SQS queue Visibility Timeout is set to 30 seconds, which is shorter than the application processing time of 40 seconds
B) The SQS Message Retention Period expired
C) SQS Standard queues only deliver messages once every 5 minutes
D) The worker instances lack IAM permissions

16. A developer wants to query an Amazon S3 bucket containing 100 GB of CSV files to extract only the rows where `country = 'US'` without downloading the entire dataset to local compute instances. Which S3 feature should be used?
A) Amazon S3 Select
B) Amazon S3 Glacier Select
C) Amazon S3 Transfer Acceleration
D) Amazon S3 Multipart Download

17. An application uses Amazon DynamoDB. The developer needs to calculate the total sum of all orders placed in the last 24 hours across the entire table. Which operation retrieves all matching items across all partitions?
A) `Scan` operation (or Parallel Scan) with a `FilterExpression` on `OrderDate`
B) `GetItem` operation
C) `Query` operation on the table without a partition key
D) `BatchGetItem`

18. A developer wants to deploy a real-time collaborative whiteboard application where connected browser clients receive instant drawing updates over persistent, bi-directional connections. Which API Gateway endpoint type supports this architecture?
A) Amazon API Gateway WebSocket API
B) Amazon API Gateway REST API with polling
C) Amazon API Gateway HTTP API
D) Amazon CloudFront Distribution

19. An application running on AWS Lambda needs to write items to an Amazon DynamoDB table. The developer wants to ensure that an item is only inserted if an item with the same `OrderId` does NOT already exist in the table. Which expression should be included in the `PutItem` request?
A) `ConditionExpression: "attribute_not_exists(OrderId)"`
B) `KeyConditionExpression: "OrderId = :id"`
C) `FilterExpression: "OrderId != :id"`
D) `ProjectionExpression: "OrderId"`

20. A developer is configuring an Amazon SQS FIFO queue. The application sends messages containing updates for 500 different user accounts. The developer wants messages for the same user account to be processed strictly in order, but messages for different user accounts to be processed concurrently. How should messages be formatted?
A) Set the `MessageGroupId` to the unique `UserId` for each message
B) Use a different SQS queue for each user
C) Set the `MessageDeduplicationId` to the `UserId`
D) Enable SQS Long Polling

21. A developer is designing a serverless microservice that connects to an Amazon Aurora MySQL database. Under heavy traffic, hundreds of concurrent Lambda executions exhaust the database's available connection pool. Which service resolves this connection management issue?
A) Amazon RDS Proxy
B) DynamoDB Accelerator (DAX)
C) Amazon ElastiCache for Memcached
D) AWS Systems Manager Parameter Store

---

### Domain 2: Security (Questions 22–38)

22. A mobile application needs to authenticate users and obtain temporary AWS credentials to upload profile images directly to an Amazon S3 bucket. Which combination of Amazon Cognito services implements this secure flow?
A) Amazon Cognito User Pools (for authentication and JWT issuance) + Amazon Cognito Identity Pools (for exchanging JWTs for temporary AWS IAM credentials)
B) Amazon Cognito User Pools only
C) Amazon Cognito Identity Pools only with hardcoded IAM keys
D) AWS Secrets Manager only

23. A developer needs to encrypt sensitive database passwords stored in an AWS Lambda function's environment variables so that unauthorized IAM users cannot view them in plaintext in the AWS Management Console. Which feature should the developer use?
A) Lambda Encryption Helpers with a Customer Managed Key (CMK) in AWS KMS, decrypting the ciphertext in code using `kms:Decrypt`
B) Storing the password in a public S3 bucket
C) Setting the environment variable name to `SECRET_PASSWORD`
D) Base64 encoding the password in the console

24. What is the maximum payload size that can be directly encrypted using an AWS KMS Customer Master Key (CMK) in a single API call?
A) 4 KB
B) 256 KB
C) 5 MB
D) 5 GB

25. An application needs to encrypt 100 MB data files before uploading them to Amazon S3. What cryptographic technique must the developer implement to encrypt data exceeding KMS's direct payload limit?
A) Envelope Encryption (using KMS `GenerateDataKey` to obtain a data key, encrypting the file locally, and storing the encrypted data key alongside the ciphertext)
B) Calling `kms:Encrypt` in a loop for each byte
C) Base64 encoding the file twice
D) Storing the KMS private key in the application repository

26. An organization requires database master credentials for an Amazon RDS PostgreSQL instance to be rotated automatically every 30 days without application downtime. Which AWS service natively supports automated credential rotation using Lambda rotation templates?
A) AWS Secrets Manager
B) AWS Systems Manager Parameter Store Standard Tier
C) AWS KMS Key Rotation
D) Amazon DynamoDB TTL

27. A developer is configuring a `SecureString` parameter in AWS Systems Manager Parameter Store. When retrieving the parameter via the AWS SDK `get_parameter` API, what parameter must be explicitly passed to return the decrypted plaintext secret?
A) `WithDecryption=True` (or `--with-decryption` in CLI)
B) `ShowSecret=True`
C) `Decrypt=All`
D) `Plaintext=True`

28. An application running on an Amazon EC2 instance needs to access an Amazon S3 bucket. What is the AWS best practice for granting permissions to the application?
A) Attach an IAM Role with an S3 least-privilege policy to the EC2 instance via an Instance Profile
B) Hardcode IAM access keys in the application source code
C) Store AWS secret keys in a local `.env` file on the EC2 instance root volume
D) Use root account credentials

29. A developer is designing an IAM policy for mobile app users accessing an Amazon DynamoDB table. The developer wants users to be able to read and write ONLY items where the partition key matches their unique Cognito Identity ID. Which condition key enforces this fine-grained access control?
A) `"Condition": { "ForAllValues:StringEquals": { "dynamodb:LeadingKeys": ["${cognito-identity.amazonaws.com:sub}"] } }`
B) `"Condition": { "StringEquals": { "aws:username": "${aws:PrincipalArn}" } }`
C) `"Condition": { "NumericEquals": { "dynamodb:Select": 1 } }`
D) `"Condition": { "Bool": { "aws:MultiFactorAuthPresent": "true" } }`

30. What is the effect of an explicit `Deny` statement in an IAM policy attached to a user when another policy attached to the same user contains an `Allow` statement for the same action?
A) The request is Denied, because an explicit Deny overrides any and all Allow statements unconditionally
B) The request is Allowed
C) AWS prompts the user for MFA
D) The request is placed in an SQS queue

31. A developer wants to restrict access to an Amazon S3 bucket so that objects can ONLY be uploaded if the request is encrypted in transit over HTTPS. What condition in the S3 bucket policy enforces this?
A) `"Condition": { "Bool": { "aws:SecureTransport": "false" } }` with `Effect: Deny`
B) `"Condition": { "StringEquals": { "s3:x-amz-acl": "public-read" } }`
C) `"Condition": { "NumericLessThan": { "s3:TlsVersion": 1.2 } }`
D) `"Condition": { "Null": { "aws:PrincipalTag": "true" } }`

32. A company wants to protect an Application Load Balancer and Amazon API Gateway against common web exploits, SQL injection (SQLi), Cross-Site Scripting (XSS), and HTTP flood DDoS attacks. Which AWS service should be deployed?
A) AWS WAF (Web Application Firewall)
B) Amazon GuardDuty
C) AWS Shield Standard only
D) Amazon Inspector

33. An application in Account A needs to decrypt S3 objects encrypted with an AWS KMS Customer Managed Key (CMK) in Account B. What two permissions are required? (Select TWO.)
A) The KMS Key Policy in Account B must grant `kms:Decrypt` to Account A's IAM Role ARN
B) The IAM Policy attached to the application role in Account A must grant `kms:Decrypt` on the KMS Key ARN in Account B
C) Account A must assume the root user of Account B
D) S3 Block Public Access must be disabled in Account B
E) The KMS key must be moved into Account A

34. What is the difference between an AWS Managed Key (e.g., `aws/s3`) and a Customer Managed Key (CMK) in AWS KMS?
A) AWS Managed Keys are created and managed by AWS with automatic rotation and no monthly key storage fee; Customer Managed Keys support custom key policies, manual rotation schedules, deletion control, and cross-account access
B) Customer Managed Keys are free; AWS Managed Keys cost $1/month
C) AWS Managed Keys can be exported as raw private keys
D) Customer Managed Keys do not support CloudTrail logging

35. A developer wants to provision a public SSL/TLS certificate for an Application Load Balancer domain name (`api.example.com`). Which service provides free public certificates with automated DNS-based renewal?
A) AWS Certificate Manager (ACM)
B) AWS KMS
C) AWS Secrets Manager
D) AWS CloudHSM

36. An application uses Amazon Cognito User Pools. The developer wants to automatically execute custom validation logic (such as checking if an email domain is allowed) during user registration before the user is confirmed. Which Cognito feature provides this capability?
A) Pre Sign-up Lambda Trigger
B) Post Authentication Lambda Trigger
C) Cognito Hosted UI
D) Amazon SNS SMS verification

37. A developer needs to decode an authorization failure message returned by an AWS CLI command to identify which IAM policy denied access. Which AWS STS API action should be used?
A) `sts:DecodeAuthorizationMessage`
B) `sts:GetCallerIdentity`
C) `sts:AssumeRole`
D) `sts:GetSessionToken`

38. A company is connecting an external SaaS vendor to manage resources in its AWS account via an IAM role. What condition key in the role's trust policy prevents the "Confused Deputy" vulnerability?
A) `sts:ExternalId`
B) `aws:SourceIp`
C) `aws:PrincipalTag`
D) `aws:SecureTransport`

---

### Domain 3: Deployment (Questions 39–54)

39. A developer is preparing an `appspec.yml` file for deploying an application to an Amazon EC2 Auto Scaling group using AWS CodeDeploy. Which lifecycle hook is executed to start application services after software files are copied to the instance?
A) `ApplicationStart`
B) `BeforeInstall`
C) `AfterInstall`
D) `ValidateService`

40. A developer is configuring an AWS CodeBuild project. Where should the build phases (`install`, `pre_build`, `build`, `post_build`), environment variables, and artifact definitions be declared?
A) In a `buildspec.yml` file placed at the root of the source code repository
B) In the `appspec.yaml` file
C) In the Dockerfile `CMD` instruction
D) In the AWS CloudTrail event log

41. A developer wants to deploy a new version of an AWS Lambda function using AWS CodeDeploy. The deployment must shift 10% of traffic to the new version, wait 10 minutes, and then shift the remaining 90% of traffic if no CloudWatch alarms trigger. Which deployment preference type should be selected?
A) `LambdaCanary10Percent10Minutes`
B) `LambdaLinear10PercentEvery1Minute`
C) `LambdaAllAtOnce`
D) `LambdaBlueGreenImmediate`

42. A developer is defining a serverless application using the AWS Serverless Application Model (SAM). Which SAM template resource type declares a serverless Lambda function with an API Gateway event source?
A) `AWS::Serverless::Function`
B) `AWS::Lambda::Function`
C) `AWS::Serverless::Api` only
D) `AWS::EC2::Instance`

43. A developer wants to test a SAM-based serverless application locally on their developer laptop against sample event JSON files before deploying to AWS. Which SAM CLI command executes the Lambda function locally?
A) `sam local invoke`
B) `sam deploy --guided`
C) `sam package`
D) `sam build --debug`

44. A developer is writing an AWS CloudFormation template. The template needs to dynamically fetch the latest Amazon Linux 2023 AMI ID maintained by AWS in Systems Manager Parameter Store. Which CloudFormation parameter type enables this dynamic lookup?
A) `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>`
B) `AWS::EC2::AMI::Latest`
C) `String` with hardcoded AMI ID
D) `CommaDelimitedList`

45. A developer wants to preview the exact changes that AWS CloudFormation will make to existing infrastructure resources before executing a stack update. Which CloudFormation feature generates this preview?
A) CloudFormation Change Sets
B) CloudFormation StackSets
C) CloudFormation Drift Detection
D) CloudFormation Rollback Triggers

46. An application is deployed using AWS Elastic Beanstalk. The development team needs to deploy updates with zero downtime and ensure that new application versions are tested on a fresh fleet of instances before redirecting user traffic. If issues arise, rollback must be instantaneous via DNS swap. Which Elastic Beanstalk deployment policy should be selected?
A) Blue/Green Deployment (using Swap Environment URLs)
B) All-at-Once Deployment
C) Rolling Deployment
D) Immutable Deployment

47. A developer is packaging an AWS Lambda function written in Node.js that depends on several large third-party npm libraries. The developer wants to reuse these shared libraries across 10 different Lambda functions without bundling them in each function's deployment zip file. What Lambda feature should be used?
A) AWS Lambda Layers
B) Lambda Environment Variables
C) Lambda Extensions
D) Amazon S3 Glacier

48. A continuous delivery pipeline in AWS CodePipeline fails during the deployment stage to AWS CloudFormation with the error `InsufficientCapabilitiesException`. What parameter was missing when creating the CloudFormation change set in the pipeline?
A) `CAPABILITY_IAM` or `CAPABILITY_NAMED_IAM` (authorizing CloudFormation to create IAM resources)
B) `CAPABILITY_AUTO_EXPAND` only
C) `DISABLE_ROLLBACK`
D) `FORCE_DEPLOY`

49. A developer is building a Docker container image in AWS CodeBuild. The build process needs to push the resulting container image to an Amazon ECR repository. What AWS CLI command authenticates the Docker CLI to the Amazon ECR registry?
A) `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com`
B) `docker login -u root -p password`
C) `aws ecr authenticate`
D) `aws iam create-login-profile`

50. A developer wants to store and version control application configuration parameters using AWS AppConfig. What capability does AWS AppConfig provide to prevent bad configurations from causing outages?
A) Deployment Strategies with gradual rollout percentages, baking periods, and automated CloudWatch Alarm rollbacks
B) Automatic compilation of C++ source code
C) Database indexing
D) DNS health checking

51. A developer is configuring an AWS CodeDeploy deployment for an Amazon ECS service. Which deployment configuration shifts traffic from the original task set to the replacement task set in two increments?
A) `CodeDeployDefault.ECSCanary10Percent5Minutes`
B) `CodeDeployDefault.ECSAllAtOnce`
C) `CodeDeployDefault.OneAtATime`
D) `CodeDeployDefault.HalfAtATime`

52. In an AWS CloudFormation template, what intrinsic function is used to concatenate strings and reference resource attributes together (e.g., creating an S3 bucket name dynamically as `my-app-prod-us-east-1`)?
A) `!Sub` (or `Fn::Sub` / `!Join`)
B) `!Ref`
C) `!GetAtt`
D) `!Select`

53. A developer wants to detect whether manual changes were made to AWS infrastructure resources outside of AWS CloudFormation management. Which CloudFormation feature detects discrepancies between the template configuration and actual live resource properties?
A) CloudFormation Drift Detection
B) CloudFormation Change Sets
C) CloudFormation StackSets
D) CloudFormation Rollback

54. An application is deployed to an Amazon ECS cluster running on AWS Fargate. What configuration in the ECS Task Definition specifies the CPU and memory limits allocated to the serverless container task?
A) Task-level `cpu` and `memory` parameters (e.g., `cpu: "256"`, `memory: "512"`)
B) The EC2 instance type in the Auto Scaling group
C) The VPC subnet CIDR size
D) The Dockerfile `EXPOSE` port

---

### Domain 4: Troubleshooting & Optimization (Questions 55–65)

55. An application encounters an HTTP 502 Bad Gateway error when users invoke an Amazon API Gateway REST API backed by an AWS Lambda function with Lambda Proxy Integration. CloudWatch logs show the Lambda function executed successfully. What is the root cause?
A) The Lambda function returned a response payload that did not match the expected API Gateway proxy format (missing `statusCode`, `headers`, or stringified `body`)
B) The Lambda function ran out of memory
C) API Gateway timed out after 29 seconds
D) S3 bucket public access was blocked

56. An application querying an Amazon DynamoDB table receives frequent `ProvisionedThroughputExceededException` errors during peak traffic. Monitoring reveals that total consumed capacity is well below the table's total provisioned limits. What is the root cause?
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

1. B — Eventually consistent reads (default) deliver single-digit ms latency and consume half the Read Capacity Units (0.5 RCU per 4 KB) compared to strongly consistent reads.
2. A — Multipart Upload API optimizes throughput and resilience for objects > 100 MB (and supports objects from 5 MB to 5 TB) by uploading parts in parallel.
3. B — Upon unhandled Lambda failure, the message returns to SQS and becomes visible again to other workers after the Visibility Timeout expires.
4. A — Enabling CORS on API Gateway and returning `Access-Control-Allow-Origin` headers from Lambda proxy integrations resolves browser CORS blocks.
5. A — `Query` specifying `KeyConditionExpression` on partition/sort keys is the most efficient and cost-effective method; `FilterExpression` filters results post-query.
6. A — Amazon Kinesis Data Streams supports multiple concurrent consumers with independent read pointers and 24h to 365d data replay capabilities.
7. A — Amazon SNS is a pub/sub fan-out messaging service that delivers messages asynchronously to multiple subscribers (SQS, email, HTTP, Lambda).
8. A — AWS Step Functions Standard Workflows support long-running state machine workflows (up to 1 year) and human approval callback tasks.
9. A — Lambda Ephemeral Storage (`/tmp`) is configurable between 512 MB and 10,240 MB (10 GB) for large temporary files.
10. A — `BatchGetItem` retrieves up to 100 items (or 16 MB) across one or more DynamoDB tables in a single network round-trip.
11. A — Amazon ElastiCache for Redis provides sub-millisecond in-memory caching for relational database queries.
12. A — `TransactWriteItems` executes all-or-nothing atomic transactions across multiple DynamoDB items with full ACID guarantees.
13. A — `BisectBatchOnFunctionError` isolates poison pill records by splitting failed batches recursively and sending failed records to a Dead-Letter Queue.
14. A — Provisioned Concurrency keeps Lambda execution environments initialized and ready, eliminating cold-start latency during traffic spikes.
15. A — If processing time exceeds the Visibility Timeout, SQS makes the message visible to other consumers, causing duplicate concurrent processing.
16. A — Amazon S3 Select runs SQL expressions directly on S3 data to retrieve only the required subset of data, reducing network transfer and latency.
17. A — A `Scan` operation reads every item in the entire DynamoDB table, filtering results with a `FilterExpression`.
18. A — API Gateway WebSocket APIs maintain persistent, bidirectional connections for real-time applications.
19. A — `ConditionExpression: "attribute_not_exists(OrderId)"` ensures an item is inserted only if no item with the same primary key already exists.
20. A — Setting `MessageGroupId` to the unique `UserId` ensures strict in-order processing per user while allowing concurrent processing across different users.
21. A — Amazon RDS Proxy pools and multiplexes database connections, preventing serverless Lambda functions from exhausting MySQL connection limits.
22. A — Cognito User Pools handle user authentication and JWT issuance; Identity Pools exchange JWTs for temporary AWS IAM credentials.
23. A — KMS Encryption Helpers encrypt Lambda environment variables client-side before deployment, masking them from console viewers.
24. A — AWS KMS Customer Master Keys can directly encrypt or decrypt payloads up to 4 KB per API call.
25. A — Envelope Encryption uses KMS `GenerateDataKey` to encrypt large files locally with data keys protected by KMS master keys.
26. A — AWS Secrets Manager provides built-in native automated password rotation for Amazon RDS using AWS Lambda rotation templates.
27. A — `--with-decryption` (or `WithDecryption=True`) must be specified when calling `get_parameter` to return decrypted plaintext for `SecureString` parameters.
28. A — Assigning an IAM Role via an Instance Profile provides secure, automatically rotated temporary credentials via IMDSv2.
29. A — `dynamodb:LeadingKeys` matching `${cognito-identity.amazonaws.com:sub}` limits users to reading/writing items matching their own identity ID.
30. A — An explicit `Deny` in any applicable IAM policy overrides all `Allow` statements unconditionally.
31. A — Denying `s3:PutObject` when `aws:SecureTransport: false` strictly enforces HTTPS encryption in transit on S3 buckets.
32. A — AWS WAF protects Layer 7 applications (ALB, API Gateway, CloudFront) against SQLi, XSS, and rate-based DDoS attacks.
33. A & B — Cross-account KMS access requires permissions in the KMS Key Policy (Account B) AND the caller's IAM Policy (Account A).
34. A — AWS Managed Keys are maintained by AWS; Customer Managed Keys support custom policies, rotation schedules, and cross-account access.
35. A — AWS Certificate Manager (ACM) provisions free public SSL/TLS certificates with automated DNS-based renewal for integrated AWS services.
36. A — Cognito Pre Sign-up Lambda Triggers execute custom validation logic before confirming new user registrations.
37. A — `sts:DecodeAuthorizationMessage` decodes and displays authorization failure details for permission troubleshooting.
38. A — The `sts:ExternalId` condition prevents the Confused Deputy vulnerability during third-party cross-account role assumption.
39. A — The `ApplicationStart` lifecycle hook in CodeDeploy executes scripts to start application services after files are installed.
40. A — `buildspec.yml` placed at the repository root defines CodeBuild build phases, environment variables, and artifact outputs.
41. A — `LambdaCanary10Percent10Minutes` shifts 10% of traffic to the new Lambda version, waits 10 minutes, and shifts the remaining 90%.
42. A — `AWS::Serverless::Function` is the SAM resource type for declaring serverless Lambda functions and API event triggers.
43. A — `sam local invoke` runs Lambda functions locally inside Docker containers against sample event payloads.
44. A — `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` dynamically fetches the latest AMI ID from SSM Parameter Store during stack deployment.
45. A — CloudFormation Change Sets generate a detailed preview of proposed resource modifications and replacements prior to execution.
46. A — Blue/Green deployment using Elastic Beanstalk Swap Environment URLs provides zero-downtime deployment with instant DNS rollback.
47. A — AWS Lambda Layers allow sharing common dependencies, libraries, and custom runtimes across multiple Lambda functions.
48. A — CloudFormation requires `CAPABILITY_IAM` or `CAPABILITY_NAMED_IAM` acknowledgment when templates create or modify IAM resources.
49. A — `aws ecr get-login-password` pipes an authentication token to `docker login` to authenticate the Docker client with ECR.
50. A — AWS AppConfig provides deployment strategies with gradual traffic rollouts, baking periods, and automated CloudWatch alarm rollbacks.
51. A — `ECSCanary10Percent5Minutes` shifts 10% of traffic to the replacement ECS task set, waits 5 minutes, and shifts the remainder.
52. A — `!Sub` (or `Fn::Sub`) substitutes variables and concatenates strings dynamically in CloudFormation templates.
53. A — CloudFormation Drift Detection identifies differences between the expected template configuration and actual live resource properties.
54. A — Task-level `cpu` and `memory` parameters in ECS Task Definitions specify compute limits for Fargate tasks.
55. A — Lambda Proxy integration requires returning a specific JSON object (`statusCode`, `headers`, `body`); returning raw strings causes HTTP 502.
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
"""

with open("18-Mock-Exams/mock-exam-1.md", "w", encoding="utf-8") as f:
    f.write(mock1_text)

print(f"Successfully wrote 18-Mock-Exams/mock-exam-1.md ({len(mock1_text.split())} words)")
