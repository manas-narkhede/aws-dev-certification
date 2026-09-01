# Module 17 — Practice Questions (115)

Calibrated to AWS's official DVA-C02 sample question style: integrative multi-service scenarios, Well-Architected trade-offs, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Part 1: Well-Architected Pillars & Developer Trade-Offs (1–40)

1. A development team wants to adopt the Operational Excellence pillar of the AWS Well-Architected Framework. Which practice directly aligns with the principle of "performing operations as code"?
A) Defining all application infrastructure, serverless functions, and CI/CD pipelines in AWS CloudFormation or AWS SAM templates checked into version control
B) Manually provisioning EC2 instances and databases through the AWS Management Console
C) Writing bash scripts on local developer laptops that configure live production databases
D) Disabling AWS CloudTrail logging to reduce operational noise

2. A company experiences sudden traffic spikes during marketing campaigns. The developer wants to follow the Reliability pillar to ensure the system automatically handles unpredictable load without manual intervention or over-provisioning compute instances. Which architecture satisfies this requirement?
A) Deploying an Application Load Balancer in front of an Auto Scaling group of EC2 instances with a Target Tracking Scaling Policy based on ALB request count per target
B) Provisioning a single large `m5.24xlarge` EC2 instance that runs continuously
C) Disabling Auto Scaling and relying on manual instance launches during sales
D) Moving all databases onto an EC2 instance in a single public subnet

3. An e-commerce platform wants to optimize performance efficiency by reducing database read load on an Amazon RDS MySQL database for product catalog queries that change infrequently. Which two caching solutions should the developer consider? (Select TWO.)
A) Amazon ElastiCache for Redis in front of the RDS database to cache query results
B) Amazon CloudFront with appropriate TTL cache headers to cache API responses at edge locations
C) Amazon S3 Glacier Flexible Archive
D) AWS Secrets Manager
E) AWS Systems Manager Session Manager

4. A startup wants to minimize cloud expenditure while developing a proof-of-concept application with sporadic, unpredictable traffic. According to the Cost Optimization pillar, which compute and database model should the startup select?
A) Serverless compute using AWS Lambda and Amazon DynamoDB in On-Demand capacity mode, paying only for exact execution time and read/write requests
B) Pre-purchasing three-year Standard Reserved EC2 instances and provisioned DynamoDB capacity
C) Running an Amazon RDS Multi-AZ DB cluster 24/7 with provisioned IOPS
D) Deploying an Amazon Redshift cluster

5. A developer is designing a microservice architecture. The team needs to choose between synchronous REST API calls (API Gateway -> Lambda -> DynamoDB) and asynchronous event-driven messaging (API Gateway -> SQS -> Lambda -> DynamoDB). What is the primary architectural advantage of the asynchronous SQS approach?
A) It decouples the frontend ingestion from backend processing, smoothing out sudden traffic spikes and preventing backend database throttling or timeout failures
B) It guarantees sub-millisecond response times to the client
C) It eliminates the need for IAM execution roles
D) It converts all JSON payloads into XML

6. A financial services application requires strict data protection at rest and in transit to satisfy the Security pillar. Which combination of controls implements these protections?
A) Enforcing HTTPS (TLS 1.2+) using an ACM certificate on the Application Load Balancer and enabling Server-Side Encryption with AWS KMS Customer Managed Keys (SSE-KMS) on all S3 buckets and databases
B) Using unencrypted HTTP on port 80 and relying on VPC private subnets only
C) Storing database credentials in plaintext in the application Dockerfile
D) Disabling IAM policies and using root credentials

7. A team is designing a serverless data processing pipeline. In accordance with the Sustainability pillar of the Well-Architected Framework, which design choice minimizes environmental impact and optimizes resource utilization?
A) Using AWS Graviton-based (ARM64) AWS Lambda functions and configuring functions to scale to zero when idle, avoiding idle energy consumption
B) Running underutilized x86 EC2 instances 24/7 at 5% CPU utilization
C) Storing uncompressed raw log files in S3 indefinitely without lifecycle policies
D) Polling external APIs continuously in an infinite while loop

8. An application needs to perform complex, multi-step business transactions involving multiple microservices. If any step fails, the system must execute compensating transactions to roll back previous steps. Which AWS service orchestrates this Saga pattern with visual workflow management?
A) AWS Step Functions
B) Amazon SQS FIFO queues
C) AWS CodePipeline
D) Amazon EventBridge Pipes

9. What is a key architectural trade-off when implementing caching with Amazon ElastiCache or CloudFront to improve read performance?
A) Data in the cache is eventually consistent and may be stale until the Time to Live (TTL) expires or an explicit cache invalidation occurs
B) Caching increases database write latency by 500%
C) Cached data is automatically encrypted with public keys only
D) Caching requires running all compute on-premises

10. A developer wants to ensure that a Lambda function can recover gracefully from transient downstream API failures without overwhelming the failing service. Which design pattern should be implemented in the client code?
A) Exponential backoff with full jitter on retries
B) Immediate retries in a tight while loop with zero delay
C) Disabling error handling so the function crashes and restarts
D) Increasing Lambda memory to 10 GB

11. According to the Reliability pillar, what is the best practice for deploying application tiers across an AWS Region?
A) Distributing compute resources across at least two or three Availability Zones within the Region behind a multi-AZ load balancer
B) Placing all EC2 instances in a single Availability Zone for lower internal networking latency
C) Running one EC2 instance per AWS account
D) Deploying all instances in a public subnet without security groups

12. A developer is choosing a database strategy for an application with unpredictable read and write spikes. Under the Cost Optimization and Reliability pillars, which DynamoDB capacity mode should be selected?
A) On-Demand Capacity Mode
B) Provisioned Capacity Mode with auto-scaling disabled
C) Reserved Capacity Mode
D) Fixed 1 RCU / 1 WCU

13. An organization wants to enforce that all developer IAM roles cannot grant permissions beyond a specific set of allowable AWS services. Which IAM feature implements this upper limit guardrail?
A) IAM Permissions Boundary
B) IAM User Group
C) KMS Key Policy
D) Route 53 Health Check

14. What is the fundamental operational difference between Amazon CloudWatch Alarms and Amazon EventBridge rules when designing automated alerts?
A) CloudWatch Alarms evaluate numeric metric thresholds over time (e.g., CPU > 80%); EventBridge matches discrete state-change events (e.g., EC2 state change or CodePipeline failure) in near real-time
B) CloudWatch Alarms are for email only; EventBridge is for SMS only
C) EventBridge cannot trigger Lambda functions
D) CloudWatch Alarms only work with S3

15. A developer is designing a containerized application that requires running long-running background batch jobs (taking 45 minutes per execution). Why is AWS Fargate (or Amazon ECS on EC2) chosen over AWS Lambda for this use case?
A) AWS Lambda has a hard maximum execution timeout of 15 minutes (900 seconds), whereas Fargate container tasks have no execution time limit
B) Lambda does not support containers
C) Fargate is completely free of charge
D) Lambda cannot access S3 buckets

16. In accordance with the Operational Excellence pillar, what is the recommended approach for testing infrastructure changes before releasing them to production?
A) Provisioning an identical, isolated staging environment using CloudFormation/CDK templates, running automated integration tests, and tearing down the environment afterward
B) Applying changes directly to production during off-peak hours
C) Testing code on a developer laptop without deploying to AWS
D) Disabling CloudWatch alarms during deployments

17. A media company wants to distribute video content globally. How does combining Amazon S3 with Amazon CloudFront and Origin Access Control (OAC) fulfill both the Security and Performance Efficiency pillars?
A) CloudFront caches video content at global edge locations for low-latency delivery, while OAC ensures that only CloudFront can retrieve objects from S3, keeping the S3 bucket private
B) CloudFront makes the S3 bucket publicly readable by all internet users
C) OAC converts video files to MP4 format automatically
D) CloudFront eliminates the need for Route 53

18. A developer wants to implement automated zero-downtime database credential rotation for an application using Amazon RDS PostgreSQL. Which solution aligns with the Security and Operational Excellence pillars?
A) Storing database credentials in AWS Secrets Manager and enabling built-in automated rotation using an AWS Lambda rotation template
B) Hardcoding database passwords in the application's configuration file
C) Storing the password in a public GitHub repository
D) Manually changing the master password in the RDS console once a year

19. An application processes incoming sensor data. The developer needs to ensure that sensor readings are processed in the exact order they were received, with strict deduplication. Which AWS messaging service satisfies this requirement?
A) Amazon SQS FIFO queue (or Amazon SNS FIFO topic)
B) Amazon SQS Standard queue
C) Amazon SNS Standard topic
D) Amazon EventBridge default bus

20. A company has an application running on EC2 instances that experiences read bottlenecks on an Amazon Aurora PostgreSQL database. Which two architectural changes improve read throughput? (Select TWO.)
A) Adding Aurora Read Replicas (up to 15 replicas) and directing read traffic to the Aurora Reader Endpoint
B) Implementing Amazon ElastiCache (Redis) to cache frequent query results in memory
C) Converting the Aurora database to an S3 Glacier vault
D) Reducing the database instance size
E) Disabling database indexes

21. A developer wants to implement tracing across a distributed microservices application composed of API Gateway, Lambda, SQS, and DynamoDB. Which AWS service provides end-to-end visual request tracing and identifies latency bottlenecks?
A) AWS X-Ray
B) Amazon CloudWatch Metrics
C) AWS CloudTrail
D) AWS Trusted Advisor

22. What is the primary benefit of deploying an Amazon RDS database with Multi-AZ deployment enabled, according to the Reliability pillar?
A) Synchronous data replication to a standby instance in a different Availability Zone with automated failover in the event of primary database failure or AZ outage
B) Increasing read performance by allowing applications to query the standby instance directly
C) Reducing database storage costs by 50%
D) Providing multi-region disaster recovery automatically

23. A developer needs to choose an AWS service to run a Node.js web API container with automatic scaling, zero server management, and automatic HTTPS certificate provisioning directly from a container image. Which service provides this PaaS capability with the lowest operational overhead?
A) AWS App Runner
B) Amazon EC2 with manual Docker installation
C) AWS CloudHSM
D) AWS Storage Gateway

24. In accordance with the Cost Optimization pillar, how can a company automatically transition infrequently accessed Amazon S3 objects to cheaper storage tiers and delete old temporary files after 90 days?
A) Configuring Amazon S3 Lifecycle Configuration rules
B) Writing a nightly Lambda cron job that scans the bucket and deletes objects
C) Changing bucket permissions to private
D) Enabling S3 Transfer Acceleration

25. What is the key advantage of using AWS Systems Manager Parameter Store Standard Tier for storing application configuration flags compared to AWS Secrets Manager?
A) Standard parameters in Parameter Store have zero monthly storage cost, whereas Secrets Manager charges $0.40 per secret per month
B) Parameter Store provides automatic RDS password rotation
C) Parameter Store allows storing files up to 5 TB
D) Parameter Store only works with DynamoDB

26. A developer needs to choose between Amazon SQS and Amazon Kinesis Data Streams for ingesting clickstream data. Which requirement makes Amazon Kinesis the superior choice?
A) The need for multiple independent consumer applications (e.g., real-time analytics, fraud detection, and S3 archival) to read the same streaming data concurrently with replay capability up to 365 days
B) The need to process each message exactly once and delete it immediately upon acknowledgment
C) The need for zero-latency point-to-point queuing
D) The requirement to use standard SQL syntax for queue polling

27. According to the Security pillar, how should sensitive customer data (such as Social Security Numbers) be protected in application log files emitted to Amazon CloudWatch Logs?
A) Implement application-level log sanitization and enable CloudWatch Logs Data Protection Policies with managed data identifier masking
B) Delete the CloudWatch log group
C) Grant all IAM users administrator privileges to view the logs
D) Encode the logs using Base64 without encryption

28. An application needs to run automated unit tests, static code analysis, and build Docker container images on every code commit. Which managed serverless CI/CD service executes these build steps based on a `buildspec.yml` file?
A) AWS CodeBuild
B) AWS CodeDeploy
C) AWS CodeArtifact
D) AWS Cloud9

29. A developer is designing an API that must support full-text search, autocomplete, and complex aggregations over millions of product catalog documents. Which specialized AWS service should be added to the architecture?
A) Amazon OpenSearch Service
B) Amazon S3 Glacier
C) Amazon ElastiCache Memcached
D) Amazon SQS

30. A team wants to implement blue/green deployments for an application running on Amazon ECS. Which AWS service orchestrates traffic shifting between the blue and green task sets with automated rollback support?
A) AWS CodeDeploy
B) AWS CodeCommit
C) Amazon Route 53 simple routing
D) AWS Systems Manager Run Command

31. In the AWS Well-Architected Framework, what is the purpose of the AWS Well-Architected Tool in the AWS Management Console?
A) It provides a formal review process to measure your cloud architectures against AWS best practices, producing an action plan to remediate high-risk issues (HRIs)
B) It automatically writes application code in Python
C) It deletes underutilized EC2 instances
D) It generates SSL certificates

32. A developer wants to decouple two microservices. Service A emits order events, and Service B, Service C, and Service D all need to receive a copy of every event. Which AWS service pattern implements this pub/sub fan-out architecture with the lowest operational overhead?
A) Amazon SNS Topic fanning out to multiple Amazon SQS Queues subscribed to the topic
B) Service A writing to an EC2 text file and other services reading via SSH
C) Creating an SSH tunnel between all instances
D) Using Route 53 weighted records

33. An application needs to store user session state for a web application running on an Auto Scaling group of EC2 instances. Where should session state be stored to make the application stateless and resilient to instance termination?
A) In Amazon ElastiCache (Redis) or an Amazon DynamoDB table
B) In the local `/tmp` directory of the EC2 instance
C) In the EC2 instance RAM memory
D) On the root EBS volume of each instance

34. A developer needs to execute database schema migrations before traffic is routed to a newly deployed AWS Lambda function version. Which deployment hook in AWS CodeDeploy for Lambda executes scripts prior to traffic shifting?
A) `BeforeAllowTraffic`
B) `AfterAllowTraffic`
C) `ValidateService`
D) `ApplicationStart`

35. What is the primary difference between Amazon SQS Visibility Timeout and SQS Message Retention Period?
A) Visibility Timeout is the period during which a message is invisible to other consumers after being received; Message Retention Period is the total duration SQS retains a message (up to 14 days) before deleting it if unprocessed
B) Visibility Timeout deletes the message; Retention Period hides it
C) Visibility Timeout is for FIFO queues only
D) Both terms are identical

36. An application processes payment transactions that must be idempotent (re-submitting the same transaction request multiple times produces the exact same outcome without duplicate charges). How can a developer implement idempotency using DynamoDB?
A) Use Conditional Writes (`attribute_not_exists(TransactionId)`) with a unique client-generated idempotency key
B) Disable DynamoDB encryption
C) Use DynamoDB Scan operations
D) Create an S3 lifecycle rule

37. A developer is designing an asynchronous image processing workflow where an S3 upload triggers an image resizing task. The task can take up to 2 minutes to complete. What is the most cost-effective and scalable serverless architecture?
A) S3 Event Notification -> Amazon SQS Queue -> AWS Lambda (processing the resize) -> S3 Processed Bucket
B) Running an EC2 `c5.9xlarge` instance 24/7 running a polling script
C) S3 Event Notification triggering an on-premises physical server
D) Storing images directly in DynamoDB items

38. According to the Security pillar, what is the best practice for authenticating and authorizing third-party SaaS tools that need temporary access to AWS resources across accounts?
A) Creating an IAM Role with a trust policy requiring an `ExternalId` condition to prevent the Confused Deputy problem
B) Emailing the AWS account root credentials to the SaaS vendor
C) Creating a permanent IAM user with administrator access
D) Generating an S3 pre-signed URL with a 10-year expiration

39. A company needs to deploy a global application with active-active deployments in `us-east-1` and `eu-west-1`. Users must be routed to the closest healthy region with automatic failover if a region becomes unhealthy. Which Route 53 routing policy should be configured?
A) Latency Routing policy with Route 53 Health Checks enabled
B) Simple Routing policy
C) Multivalue Answer routing without health checks
D) Weighted routing with 100% weight on one region

40. An application on EC2 needs to call AWS APIs (such as S3 and DynamoDB). What is the AWS-recommended method for managing credentials?
A) Attach an IAM Role to the EC2 instance via an Instance Profile, allowing the AWS SDK to retrieve temporary credentials automatically via IMDSv2
B) Hardcode access keys in the application source code
C) Store access keys in a public S3 bucket
D) Store the root user password in an unencrypted configuration file

---

### Part 2: Multi-Service Integrative Scenarios & Exam Mechanics (41–115)

41. A company is building a high-volume IoT ingestion pipeline. Devices send sensor metrics via HTTP POST to an API. The architecture must:
1. Ingest up to 20,000 requests per second with sub-second response times.
2. Buffer incoming records durably to protect backend processing workers.
3. Process data in micro-batches and write results to DynamoDB.
4. Scale automatically with zero server management.
Which architecture fulfills all requirements with the LEAST operational overhead?
A) Amazon API Gateway (REST API) with direct AWS Service Integration to Amazon Kinesis Data Streams -> AWS Lambda consumer -> Amazon DynamoDB (On-Demand mode)
B) Amazon EC2 Auto Scaling group behind an ALB running custom Python ingestion scripts -> MySQL on EC2
C) API Gateway -> AWS Step Functions Standard Workflow -> Amazon S3 Glacier
D) Amazon Route 53 -> Amazon RDS PostgreSQL single-AZ instance

42. A company's web application allows users to upload PDF documents. After upload, a machine learning workflow extracts text, generates thumbnails, and updates an Elasticsearch index. The entire extraction pipeline takes 3 to 5 minutes per document. Which architecture decouples the upload from the processing and ensures no document jobs are lost?
A) S3 upload -> S3 Event Notification sends message to Amazon SQS Queue -> AWS Lambda (or ECS Fargate task) polls SQS, processes the document, and deletes the message upon completion
B) Synchronous API Gateway call to a Lambda function with a 30-second timeout
C) Storing the PDF directly in a DynamoDB string attribute
D) EC2 instance polling S3 using an infinite bash while loop

43. A developer is designing a serverless backend for a mobile gaming application. The application requires:
- Player authentication with Google, Apple, and custom guest accounts.
- Direct player photo uploads to S3 with fine-grained access control so players can only access their own uploads folder.
- Real-time leaderboard updates with microsecond read latency.
Which combination of AWS services implements this architecture?
A) Amazon Cognito User Pools & Identity Pools (for auth and temporary scoped S3 IAM credentials) + S3 with `${cognito-identity.amazonaws.com:sub}` bucket prefix policy + Amazon DynamoDB with DynamoDB Accelerator (DAX) for leaderboards
B) IAM Users for every player + S3 public bucket + Amazon RDS MySQL
C) AWS Secrets Manager for auth + Amazon S3 Glacier + Amazon Redshift
D) AWS CodeArtifact + Amazon CloudWatch Dashboards + Amazon Route 53

44. A company operates an e-commerce platform. During flash sales, thousands of customers attempt to purchase limited-quantity items simultaneously. The system must prevent inventory over-selling (race conditions) while maintaining high write throughput. How should the developer implement inventory deduction in DynamoDB?
A) Use DynamoDB TransactWriteItems (or `UpdateItem` with a `ConditionExpression: "InventoryCount >= :qty"`) to atomically deduct inventory only if sufficient stock exists
B) Perform a standard `GetItem` followed by a separate `PutItem` without condition expressions
C) Use DynamoDB Scan operations across the entire table
D) Disable DynamoDB transactions and write to a local CSV file

45. An organization has an application running on Amazon ECS on AWS Fargate that needs to retrieve database credentials from AWS Secrets Manager. What two IAM configurations are required? (Select TWO.)
A) The ECS Task Execution Role must have permissions `secretsmanager:GetSecretValue` and `kms:Decrypt` (on the secret's KMS key)
B) The ECS Task Definition must reference the secret ARN under the `secrets` array in the container definition
C) The EC2 instance root volume must be formatted with ext4
D) The ECS Cluster must be deployed in a public subnet
E) The Fargate task must run with `privileged: true`

46. A developer needs to deploy a serverless REST API using AWS SAM. The SAM template must define an API Gateway, a Lambda function, and an Amazon DynamoDB table. Which SAM resource types should be declared in `template.yaml`?
A) `AWS::Serverless::Function`, `AWS::Serverless::Api`, and `AWS::Serverless::SimpleTable`
B) `AWS::EC2::Instance`, `AWS::RDS::DBInstance`, and `AWS::S3::Bucket`
C) `AWS::CodePipeline::Pipeline` only
D) `AWS::IAM::User` and `AWS::IAM::AccessKey`

47. A developer is troubleshooting an intermittent issue where Lambda functions in a VPC fail to connect to an external payment API. The Lambda function subnets are private subnets. What is the root cause and the correct resolution?
A) Attaching Lambda to private subnets removes default internet access; add a NAT Gateway in a public subnet and add a route `0.0.0.0/0` targeting the NAT Gateway in the private subnet route table
B) Lambda functions cannot run in VPCs
C) The payment API must be moved into the same VPC
D) The Lambda execution role must be granted `AdministratorAccess`

48. A company is redesigning a monolithic application into microservices. Service A needs to notify multiple independent downstream services (Billing, Notifications, Analytics) whenever an order is completed. Downstream services should be able to fail and retry independently without affecting Service A or other services. Which architectural pattern fulfills this requirement?
A) Amazon SNS topic with multiple Amazon SQS queues subscribed (Fan-Out Pattern)
B) Direct synchronous HTTP REST calls from Service A to each downstream service sequentially
C) Writing orders to a shared local text file on an EC2 instance
D) Pointing all downstream services to a single shared SQS Standard queue

49. An application processes confidential financial records in Amazon S3. The compliance department mandates that:
1. All objects must be encrypted at rest using a customer-managed KMS key.
2. The KMS key must automatically rotate annually.
3. Every encryption and decryption event must be recorded in CloudTrail.
4. Direct unencrypted HTTP uploads must be rejected.
Which combination of configurations achieves full compliance?
A) Create a Customer Managed Key (CMK) in AWS KMS with Automatic Key Rotation enabled + Enable default bucket encryption with SSE-KMS using this CMK + Add an S3 bucket policy with `Effect: Deny` on `s3:PutObject` when `aws:SecureTransport: false`
B) Use SSE-S3 default encryption with no bucket policy
C) Use SSE-C customer-provided keys and disable CloudTrail
D) Download all files to on-premises hard drives

50. A developer wants to implement continuous deployment using AWS CodePipeline. The pipeline must:
1. Pull source code from AWS CodeCommit.
2. Compile code and run unit tests in AWS CodeBuild.
3. Deploy the application to an AWS Lambda function using AWS CodeDeploy with a canary traffic shifting strategy (`LambdaCanary10Percent5Minutes`).
4. Automatically roll back if CloudWatch alarms detect elevated error rates.
Which deployment configuration file must be present in the source repository to configure CodeDeploy for this Lambda deployment?
A) `appspec.yaml` (specifying the Lambda function name, alias, and pre/post traffic validation hooks)
B) `buildspec.yml`
C) `template.json`
D) `dockerrun.aws.json`

51. An application using Amazon DynamoDB receives frequent `ProvisionedThroughputExceededException` errors during flash sales. Monitoring shows that overall consumed capacity is well below the table's total provisioned limit. What is the root cause and the best architectural solution?
A) A hot partition caused by poor partition key design; resolve by redesigning the partition key with high-cardinality values or implementing key salting, or deploy DynamoDB Accelerator (DAX)
B) DynamoDB is experiencing an AWS regional outage
C) The table has too many Global Secondary Indexes
D) The IAM policy lacks `dynamodb:PutItem` permission

52. A developer is building a serverless real-time chat application. Mobile clients need to maintain persistent, bidirectional two-way communication with the backend to send and receive chat messages instantly. Which AWS service and protocol is designed for this architecture?
A) Amazon API Gateway WebSocket APIs integrated with AWS Lambda and Amazon DynamoDB
B) Amazon API Gateway REST APIs using HTTP polling every 100 milliseconds
C) Amazon S3 static website hosting
D) Amazon Route 53 DNS queries

53. An application running on EC2 instances processes sensitive health records. The application needs to encrypt records locally before storing them in DynamoDB. The records vary in size from 10 KB to 2 MB. Which encryption approach should the developer implement?
A) Envelope Encryption using the AWS Encryption SDK, calling KMS `GenerateDataKey` to get a data key, encrypting records in memory, and storing the encrypted data key alongside the ciphertext
B) Calling KMS `Encrypt` directly for every record
C) Base64 encoding the data
D) Storing the KMS master key in the EC2 instance root directory

54. A developer wants to automate the deployment of a full multi-tier web application stack (VPC, subnets, ALB, Auto Scaling group, RDS database) in a single command. The architecture must be repeatable across multiple AWS accounts and Regions. Which AWS service should be used?
A) AWS CloudFormation (or AWS CDK)
B) AWS Systems Manager Session Manager
C) AWS Shield
D) Amazon Inspector

55. A developer wants to optimize a high-traffic Lambda function that reads user settings from an Amazon RDS MySQL database. Currently, each Lambda invocation establishes a new TCP connection to MySQL, resulting in database connection exhaustion under load. Which service resolves this connection management bottleneck?
A) Amazon RDS Proxy
B) Amazon DynamoDB Accelerator (DAX)
C) AWS Systems Manager Parameter Store
D) Amazon Route 53 Resolver

56. An application hosted on Amazon ECS on AWS Fargate needs to securely communicate with an Amazon DynamoDB table and an Amazon S3 bucket. How should AWS credentials be provided to the containerized application?
A) Assign an IAM Role with least-privilege permissions to the ECS Task Definition's `taskRoleArn` (ECS Task Role)
B) Hardcode AWS Access Keys in the Docker container image
C) Store credentials in an unencrypted environment variable in the task definition
D) Embed the root account password in the container startup script

57. A media company wants to serve static website assets (HTML, CSS, JS, images) with low latency worldwide and enforce HTTPS. The company wants to minimize hosting and compute costs. Which serverless architecture is the MOST cost-effective?
A) Amazon S3 bucket configured as an origin behind an Amazon CloudFront distribution with an ACM SSL/TLS certificate and Origin Access Control (OAC)
B) An EC2 instance running Nginx in `us-east-1` with an Elastic IP
C) AWS Elastic Beanstalk single-instance deployment
D) Amazon EKS cluster with 10 worker nodes

58. A developer is implementing an API that allows users to download private, paid digital audiobooks through Amazon CloudFront. Access must expire after 4 hours and be restricted to the specific authorized purchaser. Which CloudFront feature should the backend use?
A) CloudFront Signed URLs (generated using a private key from a trusted CloudFront Key Group)
B) S3 Bucket ACLs set to public-read
C) Route 53 Geolocation routing
D) AWS WAF IP Blacklist

59. A developer is investigating an issue where an application receives HTTP 504 Gateway Timeout errors when calling an Amazon API Gateway endpoint backed by an AWS Lambda function. What is the most likely cause?
A) The Lambda function execution duration exceeded the API Gateway integration timeout limit (maximum 29 seconds)
B) The Lambda function returned invalid JSON syntax
C) The client sent an invalid query parameter
D) API Gateway ran out of disk space

60. An application generates 50,000 log events per second. The developer needs to extract custom metrics (such as payment processing latency and failure counts) without paying per-call `PutMetricData` API fees or adding network latency to the request path. Which logging pattern meets these requirements?
A) CloudWatch Embedded Metric Format (EMF) outputting structured JSON with an `_aws` metadata object to standard output
B) Calling `PutMetricData` synchronously in a loop for each transaction
C) Writing logs to a local text file and uploading to S3 once a month
D) Sending metrics via email using Amazon SES

61. A company needs to run a daily batch data transformation job that takes 4 hours to complete. The job requires 32 GB of RAM and 8 vCPUs. The job should execute automatically at 2:00 AM every night. Which serverless architecture has the LEAST operational overhead?
A) Amazon EventBridge Scheduler triggering an AWS Batch job running on AWS Fargate
B) AWS Lambda function with a 4-hour timeout
C) A dedicated EC2 instance running 24/7 with a Linux cron job
D) Amazon S3 Lifecycle rule

62. A developer wants to publish a new version of an AWS Lambda function and test it with 10% of production traffic for 10 minutes before routing 100% of traffic to the new version. If errors occur, traffic must automatically roll back. Which AWS service combination manages this deployment?
A) AWS CodeDeploy with a `LambdaCanary10Percent10Minutes` deployment configuration and CloudWatch Alarm rollback triggers
B) Amazon Route 53 Simple Routing
C) AWS Elastic Beanstalk All-at-Once deployment
D) CloudFormation stack update with no rollback alarms

63. An application needs to process incoming orders from an Amazon SQS queue. If a worker Lambda function encounters a processing error due to a corrupted message payload, the message returns to the queue. After 3 failed attempts, the corrupted message must be isolated for developer debugging without blocking other orders. Which SQS feature implements this?
A) Dead-Letter Queue (DLQ) with a `maxReceiveCount` set to 3
B) SQS Delay Queue set to 15 minutes
C) Increasing SQS Message Retention Period to 14 days
D) Deleting the queue automatically

64. A developer is designing a microservice backend that must execute a workflow consisting of 8 sequential steps with branching logic, error retries, and parallel execution branches. Which AWS service should coordinate this workflow?
A) AWS Step Functions
B) Amazon SQS
C) Amazon SNS
D) Amazon CloudWatch Alarms

65. A developer is building an application that needs to store and query user profiles in Amazon DynamoDB. The query pattern requires searching by `EmailAddress` (which is not the table's partition key). Which DynamoDB feature enables efficient querying on non-key attributes across the entire table?
A) Global Secondary Index (GSI)
B) Local Secondary Index (LSI)
C) DynamoDB Scan with client-side filtering
D) DynamoDB Streams

66. What is the fundamental difference between a DynamoDB Global Secondary Index (GSI) and a Local Secondary Index (LSI)?
A) A GSI can be created at any time, has a different partition key and sort key from the base table, and has its own provisioned/on-demand capacity; an LSI must be created at table creation time and must share the same partition key as the base table
B) LSIs can have up to 20 indexes; GSIs are limited to 5
C) GSIs are free of charge; LSIs carry hourly fees
D) LSIs support strongly consistent reads across regions

67. A developer is creating a continuous integration pipeline in AWS CodeBuild. The build process requires downloading proprietary private npm packages from a centralized repository within the AWS organization. Which AWS service securely stores, manages, and publishes private software packages?
A) AWS CodeArtifact
B) AWS CodeCommit
C) AWS CodeDeploy
D) Amazon ECR

68. A developer needs to inspect the detailed execution timing of individual database queries and third-party HTTP calls made inside an AWS Lambda function. What AWS X-Ray construct breaks down the duration of operations within a segment?
A) Subsegment
B) Trace Header
C) Sampling Rule
D) Service Map

69. An application running on EC2 instances in an Auto Scaling group needs to receive a webhook notification whenever an instance is about to be terminated by Auto Scaling, allowing the application 5 minutes to gracefully finish in-flight requests and drain connections. Which Auto Scaling feature provides this capability?
A) Auto Scaling Lifecycle Hooks (terminating lifecycle hook with an SNS/EventBridge notification)
B) Auto Scaling Target Tracking Policy
C) CloudWatch Metric Math
D) EC2 Instance Recovery

70. A company wants to run a containerized microservice on Amazon ECS. The team wants zero server management, automatic OS patching, and per-second billing based on CPU and memory allocated to tasks. Which ECS launch type should be selected?
A) AWS Fargate
B) EC2 Launch Type
C) On-Premises VMware
D) Amazon Lightsail

71. A developer wants to restrict an Amazon S3 bucket so that objects can ONLY be uploaded if they are encrypted using an AWS KMS Customer Managed Key (`arn:aws:kms:us-east-1:123456789012:key/abc-123`). What bucket policy statement enforces this?
A) Deny `s3:PutObject` if `s3:x-amz-server-side-encryption-aws-kms-key-id` does not equal `arn:aws:kms:us-east-1:123456789012:key/abc-123`
B) Allow `s3:*` to `Principal: "*"`
C) Delete all IAM roles
D) Disable versioning on S3

72. An application uses Amazon Cognito User Pools for user authentication. The developer wants to migrate 100,000 users from an existing legacy database to Cognito WITHOUT requiring users to reset their passwords on their first login. Which Cognito feature enables this seamless migration?
A) User Migration Lambda Trigger (invoked on authentication to verify legacy credentials and silently create the Cognito user)
B) CSV bulk import (which requires users to reset passwords)
C) Amazon S3 Transfer Acceleration
D) AWS DataSync

73. A developer is designing a serverless application using AWS SAM. How can the developer test and debug the Lambda function locally on their laptop against simulated API Gateway events before deploying to AWS?
A) Use the SAM CLI command `sam local invoke` or `sam local start-api`
B) Upload the code to an EC2 instance in production
C) Run `git push` to production
D) SAM functions cannot be tested locally

74. A developer is building a high-throughput financial ingestion application on AWS Lambda. The application experiences sporadic latency spikes (cold starts) when traffic surges. Which Lambda configuration eliminates cold-start latency by keeping execution environments initialized and ready to respond in double-digit milliseconds?
A) Provisioned Concurrency
B) Reserved Concurrency
C) Increasing Lambda timeout to 15 minutes
D) Deploying Lambda in a private VPC subnet

75. An application uses Amazon DynamoDB. The developer needs to capture every insert, update, and delete operation on the table in real-time and trigger a Lambda function to update an OpenSearch search index. Which DynamoDB feature streams item-level changes?
A) Amazon DynamoDB Streams with an AWS Lambda event source mapping
B) DynamoDB Global Secondary Indexes
C) DynamoDB Point-in-Time Recovery
D) Amazon S3 Event Notifications

76. A developer wants to protect an Amazon CloudFront distribution against common web exploits, SQL injection attacks, and HTTP flood DDoS attacks. Which AWS service should be attached to the CloudFront distribution?
A) AWS WAF (Web Application Firewall)
B) Amazon GuardDuty
C) AWS Shield Standard only
D) Amazon Inspector

77. An application running on EC2 instances needs to access an Amazon Aurora database in a private subnet. How should Security Groups be configured following the principle of least privilege?
A) Configure the Aurora Security Group to allow inbound traffic on port 5432 with the source set to the Security Group ID of the EC2 instances
B) Configure the Aurora Security Group to allow port 5432 from `0.0.0.0/0`
C) Open all TCP ports on the VPC route table
D) Disable Security Groups on both instances

78. A developer wants to deploy a Single Page Application (SPA) built with React. When users navigate directly to a sub-route (e.g., `https://example.com/dashboard`), CloudFront returns an HTTP 403 or 404 error because the file does not exist in S3. How should the developer configure CloudFront to support client-side routing?
A) Configure a Custom Error Response in CloudFront that intercepts HTTP 403 and 404 errors and returns `/index.html` with an HTTP 200 OK status code
B) Create an S3 bucket for every sub-route
C) Disable CloudFront caching completely
D) Convert the React app into a bash script

79. A company needs to store database credentials that rotate automatically every 60 days. An ECS Fargate container needs to read this credential at startup. Which combination of services provides this capability?
A) AWS Secrets Manager (with automated Lambda rotation) + ECS Task Definition referencing the secret ARN in the `secrets` section
B) AWS Systems Manager Parameter Store Standard Tier
C) Hardcoded credentials in the Docker image
D) Amazon S3 unencrypted text file

80. A developer is optimizing an application that queries an Amazon DynamoDB table. The application performs frequent read queries that return the exact same items. The developer wants to achieve microsecond read latency without changing the application's query code or logic. Which solution should be deployed?
A) Amazon DynamoDB Accelerator (DAX)
B) Amazon ElastiCache Memcached
C) Increasing DynamoDB Read Capacity Units to 10,000
D) Converting DynamoDB to Amazon Redshift

81. A developer needs to deploy an infrastructure change using AWS CloudFormation. Before executing the update, the developer wants to preview the exact resources that will be created, modified, or deleted, including whether any resources will require replacement. Which CloudFormation feature provides this preview?
A) CloudFormation Change Sets
B) CloudFormation StackSets
C) CloudFormation Drift Detection
D) CloudFormation Rollback Triggers

82. An application running on AWS Lambda writes temporary video files during processing. The files can be up to 4 GB in size. Lambda's default `/tmp` storage is 512 MB. How can the developer accommodate these large temporary files?
A) Increase the Lambda ephemeral storage (`/tmp`) configuration setting (up to 10,240 MB / 10 GB)
B) Mount an EBS volume to Lambda
C) Increase Lambda timeout to 15 minutes
D) Use Amazon S3 Glacier

83. A developer wants to implement continuous integration for a Python application. Whenever code is pushed to the `main` branch of an AWS CodeCommit repository, an AWS CodePipeline pipeline must automatically start. Which AWS service detects the code push and triggers CodePipeline?
A) Amazon EventBridge (matching CodeCommit repository state-change events)
B) Amazon CloudWatch Alarms
C) Amazon Route 53
D) AWS STS

84. An application needs to process payments by coordinating three distinct microservices. If any step fails, the system must retry with exponential backoff up to 3 times before transitioning to an error-handling compensation state. Which AWS service is designed for this visual state machine logic?
A) AWS Step Functions (Standard Workflow)
B) Amazon SQS
C) Amazon SNS
D) AWS CodeBuild

85. A developer is designing an Amazon API Gateway REST API. The developer wants to cache responses for 5 minutes to reduce backend Lambda invocations. However, authenticated administrative requests must be able to bypass the cache and fetch fresh backend data. What HTTP header should the administrator pass?
A) `Cache-Control: max-age=0` (with appropriate IAM authorization to invalidate cache)
B) `Authorization: None`
C) `Accept: application/xml`
D) `X-Forwarded-For: 127.0.0.1`

86. An application processes messages from an Amazon SQS FIFO queue. The developer observes that messages are being processed one at a time sequentially, causing a processing backlog. The queue contains messages for 1,000 distinct customer accounts. How can the developer increase processing concurrency while maintaining strict ordering per customer?
A) Set the `MessageGroupId` to the unique `CustomerId` for each message, allowing multiple Lambda consumers to process messages from different groups in parallel
B) Convert the FIFO queue to an SQS Standard queue
C) Delete all messages in the queue
D) Increase the SQS Visibility Timeout to 12 hours

87. A developer is configuring an AWS CodeBuild project that needs to pull base Docker images from Amazon ECR in a different AWS account. What configuration is required?
A) An ECR Repository Policy in the target account allowing `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, and `ecr:BatchCheckLayerAvailability` for the CodeBuild service role ARN
B) Hardcoding IAM access keys in the `buildspec.yml` file
C) Moving the CodeBuild project into the target account's VPC
D) Disabling IAM policies on ECR

88. A developer wants to ensure that a CloudFormation stack deployment rolls back automatically if an application health alarm trips during stack creation or update. Which CloudFormation feature implements this?
A) CloudFormation Rollback Triggers (associated with CloudWatch Alarms)
B) CloudFormation StackSets
C) CloudFormation Termination Protection
D) CloudFormation Macros

89. A developer is designing a serverless data ingestion pipeline that processes 50 MB files uploaded to Amazon S3. The processing step takes 8 minutes. What is the most cost-effective compute service for this task?
A) AWS Lambda (configured with sufficient memory and timeout up to 15 minutes)
B) Amazon EC2 `m5.metal` instance running 24/7
C) Amazon EMR cluster with 10 master nodes
D) AWS Cloud9

90. An application running on AWS Lambda needs to query an Amazon RDS PostgreSQL database located in a private subnet in a VPC. The Lambda function also needs to call an external public weather API. What is the correct networking configuration?
A) Attach the Lambda function to private subnets in the VPC; configure a NAT Gateway in a public subnet with a route in the private subnet route table directing `0.0.0.0/0` to the NAT Gateway
B) Attach the Lambda function to a public subnet
C) Assign an Elastic IP directly to the Lambda function
D) Move the RDS database into a public subnet with public accessibility enabled

91. A developer wants to restrict access to an Amazon API Gateway REST API so that only requests originating from an Amazon CloudFront distribution are accepted, blocking direct requests to the API Gateway URL. What combination of features implements this?
A) Configure CloudFront to send a custom secret header (e.g., `X-Origin-Verify: <secret>`) and configure a Web ACL in AWS WAF (or an API Gateway Resource Policy) that allows requests only when the header matches
B) Disable HTTPS on CloudFront
C) Use Route 53 Simple Routing
D) Set API Gateway to Private mode without VPC endpoints

92. An e-commerce platform uses Amazon DynamoDB. The developer wants to automatically purge expired user shopping cart sessions after 7 days without consuming write capacity units or writing custom deletion scripts. Which DynamoDB feature accomplishes this?
A) DynamoDB Time to Live (TTL) with an epoch timestamp attribute
B) DynamoDB Streams
C) DynamoDB Global Tables
D) DynamoDB Local Secondary Indexes

93. A developer is designing a continuous deployment pipeline for an AWS Lambda function using AWS SAM. In `template.yaml`, which property under `AutoPublishAlias` enables automated traffic shifting with CodeDeploy?
A) `DeploymentPreference: { Type: "Linear10PercentEvery1Minute" }`
B) `DeploymentStrategy: "AllAtOnce"`
C) `CodeDeploy: "Enabled"`
D) `TrafficShift: "True"`

94. What is the primary purpose of AWS KMS Envelope Encryption?
A) It allows encrypting data of any size locally using a data key, protecting the data key under a KMS Customer Master Key, and overcoming KMS's direct 4 KB encryption limit
B) It encrypts network cables between data centers
C) It replaces TLS 1.3
D) It eliminates the need for IAM roles

95. An application receives unpredictable spikes in traffic. The backend consists of an AWS Lambda function querying an Amazon DynamoDB table. What capacity mode should be configured on DynamoDB to handle instant traffic spikes without throttling or capacity planning?
A) On-Demand Capacity Mode
B) Provisioned Capacity Mode with fixed 5 RCU / 5 WCU
C) Reserved Capacity Mode
D) Global Secondary Index Mode

96. A developer wants to view real-time log streams from an AWS Lambda function in the local terminal window during development. Which AWS CLI command provides live log streaming?
A) `aws logs tail /aws/lambda/<FunctionName> --follow`
B) `aws lambda get-logs`
C) `aws cloudwatch stream-events`
D) `tail -f /var/log/messages`

97. An organization wants to implement blue/green deployments for a containerized application running on Amazon ECS on AWS Fargate. The Application Load Balancer has two Target Groups: `TargetGroup-1` (Blue/Production) and `TargetGroup-2` (Green/Test). Which service orchestrates shifting production traffic from TargetGroup-1 to TargetGroup-2?
A) AWS CodeDeploy
B) AWS CodeBuild
C) AWS CodeCommit
D) Amazon Route 53 Simple Routing

98. A developer wants to publish application metrics directly from structured JSON logs without incurring per-call `PutMetricData` API fees or adding synchronous network latency to Lambda execution. Which CloudWatch feature satisfies this requirement?
A) CloudWatch Embedded Metric Format (EMF)
B) CloudWatch Metric Math
C) CloudWatch Alarms
D) CloudWatch Synthetics

99. A developer is troubleshooting an issue where an application throwing an `AccessDeniedException` when calling AWS KMS to decrypt an S3 object. What two policy components must be checked? (Select TWO.)
A) The IAM identity policy attached to the calling role
B) The KMS Key Policy attached to the KMS Customer Master Key
C) The VPC Route Table
D) The Route 53 Hosted Zone
E) The S3 Lifecycle Configuration

100. A developer needs to distribute user requests evenly across a fleet of EC2 instances in an Auto Scaling group across multiple Availability Zones. Which load balancer operates at Layer 7 (Application Layer) and supports path-based and host-based routing?
A) Application Load Balancer (ALB)
B) Network Load Balancer (NLB)
C) Gateway Load Balancer (GWLB)
D) Classic Load Balancer (CLB)

101. An application needs to process clickstream events. The system must support real-time data analysis with windowed aggregations and immediately archive raw data to Amazon S3. Which combination of AWS services implements this?
A) Amazon Kinesis Data Streams -> Amazon Managed Service for Apache Flink (real-time analytics) + Amazon Kinesis Data Firehose (delivery to S3)
B) Amazon SQS -> Amazon S3 Glacier directly
C) Amazon RDS MySQL single instance
D) AWS Secrets Manager -> AWS CloudTrail

102. A developer is deploying a single-page web application to Amazon S3. The web assets are cached by Amazon CloudFront. When the developer deploys a new version of `index.html`, users continue seeing the old version. How should the developer immediately force CloudFront edge locations to serve the new file?
A) Create a CloudFront Invalidation for `/index.html` (or `/*`)
B) Delete the S3 bucket
C) Reboot the CloudFront edge servers
D) Change the Route 53 hosted zone

103. An application uses Amazon DynamoDB with strongly consistent reads. What is the impact of strongly consistent reads on DynamoDB read capacity unit (RCU) consumption compared to eventually consistent reads?
A) Strongly consistent reads consume 1 RCU per 4 KB item; eventually consistent reads consume 0.5 RCU per 4 KB item (strongly consistent reads cost twice as much RCU)
B) Strongly consistent reads are free of charge
C) Strongly consistent reads consume 10 times more RCUs
D) Both read types consume identical RCUs

104. A developer is designing a serverless application where users submit expense reports. The expense report must be approved by a human manager via email before payment is issued. Which AWS service natively supports human approval steps and long-running workflows that pause for days or weeks?
A) AWS Step Functions (Standard Workflow using Task Tokens / Activity Tasks)
B) AWS Lambda (running continuously for 2 weeks)
C) Amazon SQS
D) Amazon EventBridge Pipes

105. A company operates an Amazon DynamoDB table in `us-east-1`. The company wants to expand globally and provide low-latency local read and write access for users in `eu-west-1` and `ap-southeast-1` with automated multi-master replication. Which DynamoDB feature should be enabled?
A) Amazon DynamoDB Global Tables
B) DynamoDB Accelerator (DAX)
C) DynamoDB Local Secondary Indexes
D) DynamoDB Point-in-Time Recovery

106. A developer wants to run automated headless browser scripts every 5 minutes to verify that the user login workflow and shopping cart checkout buttons are functioning properly 24/7. Which CloudWatch feature provides this capability?
A) CloudWatch Synthetics Canaries
B) CloudWatch Metric Filters
C) CloudWatch Contributor Insights
D) CloudWatch Logs Insights

107. An application running on EC2 instances behind an Application Load Balancer requires sticky sessions so that requests from a specific user are consistently forwarded to the same backend target instance. What mechanism does the ALB use to maintain stickiness?
A) HTTP Cookies (either duration-based ALB cookies or application-based cookies)
B) Client IP address hashing only
C) DNS round-robin
D) Hardcoded instance IDs in the URL

108. A developer wants to ensure that an Amazon S3 bucket cannot have public read access enabled under any circumstances, even if an administrator accidentally adds a public bucket policy. Which S3 feature enforces this account-wide or bucket-wide guardrail?
A) S3 Block Public Access
B) S3 Versioning
C) S3 Object Lock
D) S3 Transfer Acceleration

109. An application using Amazon SQS needs to delay the delivery of new messages to consumers by 5 minutes after they are published. Which SQS feature implements this initial delay?
A) SQS Delay Queues (setting `DeliveryDelay` to 300 seconds)
B) SQS Visibility Timeout
C) SQS Dead-Letter Queue
D) SQS Long Polling

110. A developer is writing an AWS Lambda function that processes items from an Amazon Kinesis Data Stream. If a poison pill record causes the Lambda function to fail, how can the developer prevent the entire shard from being blocked while ensuring the failed record is captured for debugging?
A) Configure `BisectBatchOnFunctionError: true`, set a `MaximumRetryAttempts` limit, and configure an On-Failure Destination (such as an SQS Dead-Letter Queue)
B) Increase Lambda memory to 10 GB
C) Delete the Kinesis stream
D) Disable Kinesis sharding

111. An application running on AWS Lambda needs to store session data in Amazon ElastiCache (Redis) inside a VPC. What configuration is required on the Lambda function?
A) Configure the Lambda function for VPC access by specifying private subnets and a Security Group that has network access to the ElastiCache cluster port (6379)
B) Assign a public Elastic IP to the Lambda function
C) Move ElastiCache to the public internet
D) Open port 80 to `0.0.0.0/0`

112. A developer wants to configure an Amazon Route 53 DNS record pointing `example.com` (zone apex) to an Application Load Balancer. Which Route 53 record type must be created?
A) Route 53 Alias Record (A type)
B) CNAME Record
C) PTR Record
D) TXT Record

113. An application processes orders using Amazon DynamoDB. The developer wants to automatically create an audit trail record in an Amazon S3 bucket whenever an item in DynamoDB is modified or deleted. Which serverless architecture implements this?
A) Amazon DynamoDB Streams -> AWS Lambda consumer -> Amazon S3 bucket
B) S3 Lifecycle Rules
C) Route 53 DNS Query Logs
D) AWS WAF Logs

114. A developer is designing a secure REST API with Amazon API Gateway. The developer wants to authenticate users using their corporate Microsoft Active Directory credentials via SAML 2.0. Which architecture fulfills this requirement?
A) Amazon Cognito User Pools federated with Microsoft Active Directory (SAML 2.0 IdP) + API Gateway Cognito Authorizer
B) Storing Active Directory passwords in plaintext in SSM Parameter Store
C) IAM User access keys distributed to all employees
D) Amazon S3 static website hosting

115. An architect is reviewing an end-to-end serverless e-commerce architecture for maximum resilience, security, and cost efficiency:
1. Static web frontend hosted on S3 behind CloudFront with OAC and WAF protection.
2. User authentication via Cognito User Pools with OAuth 2.0 PKCE.
3. API Gateway routing orders asynchronously into an SQS FIFO Queue.
4. AWS Lambda processing orders from SQS and saving to DynamoDB On-Demand.
5. Secrets stored in Secrets Manager with automated 30-day rotation.
6. Full distributed tracing with X-Ray and structured JSON logging with EMF.
Which of the six AWS Well-Architected Framework pillars does this architecture satisfy?
A) All six pillars: Operational Excellence (IaC/EMF/X-Ray), Security (WAF/Cognito/KMS/Secrets), Reliability (SQS decoupling/Multi-AZ/DynamoDB), Performance (CloudFront/Lambda), Cost Optimization (Serverless/On-Demand), and Sustainability (Scale to zero)
B) Security only
C) Cost Optimization only
D) None of the pillars

---

## Answer Key & Explanations

1. A — Defining infrastructure in version-controlled CloudFormation or SAM templates directly aligns with "perform operations as code."
2. A — ALB with an Auto Scaling group using Target Tracking automatically matches compute capacity to demand.
3. A & B — ElastiCache caches database query results, and CloudFront caches API responses at the edge, offloading the database.
4. A — Serverless compute (Lambda) and DynamoDB On-Demand charge only for actual executions and requests, ideal for unpredictable workloads.
5. A — Asynchronous SQS buffering decouples ingestion from processing, absorbing traffic spikes and protecting downstream databases.
6. A — ACM SSL/TLS certificates enforce in-transit encryption, while KMS Customer Managed Keys (SSE-KMS) enforce at-rest encryption.
7. A — Graviton processors deliver higher energy efficiency, and serverless architectures scale to zero to prevent idle energy waste.
8. A — AWS Step Functions coordinates multi-step Saga transactions with visual state machines, retries, and compensation rollbacks.
9. A — Caching introduces eventual consistency where cached data may be slightly stale until the TTL expires or cache is invalidated.
10. A — Exponential backoff with full jitter spreads out retry attempts, preventing retry storms on struggling downstream dependencies.
11. A — Multi-AZ deployments distribute resources across multiple independent data centers for regional fault tolerance.
12. A — DynamoDB On-Demand capacity mode automatically scales up and down to handle unpredictable spikes without throttling.
13. A — Permissions Boundaries set the maximum permissible permissions that identity-based policies can grant to an IAM entity.
14. A — CloudWatch Alarms evaluate numeric metric thresholds; EventBridge matches discrete state-change events in real-time.
15. A — AWS Lambda has a hard 15-minute execution limit; long-running batch jobs (45 mins) require Fargate or ECS on EC2.
16. A — Testing in an identical, isolated environment provisioned via IaC and tearing it down afterwards is a core Operational Excellence practice.
17. A — CloudFront edge caching optimizes performance, while Origin Access Control (OAC) keeps S3 origin access secure and private.
18. A — Secrets Manager provides native, automated password rotation using AWS Lambda rotation templates with zero downtime.
19. A — SQS FIFO queues ensure strict first-in, first-out message ordering with message deduplication IDs.
20. A & B — Aurora Read Replicas scale SQL read throughput horizontally, and ElastiCache caches frequent query results in memory.
21. A — AWS X-Ray provides end-to-end distributed tracing across API Gateway, Lambda, SQS, and DynamoDB.
22. A — RDS Multi-AZ synchronously replicates to a standby instance in another AZ for automated failover during outages.
23. A — AWS AppRunner provides a fully managed container-to-HTTPS PaaS with zero server configuration and automatic scaling.
24. A — S3 Lifecycle Configuration rules automate tier transitions (e.g., S3 Standard to Glacier) and object expirations.
25. A — SSM Parameter Store Standard Tier stores configuration parameters and static secrets with zero monthly storage fees.
26. A — Kinesis Data Streams supports multiple concurrent consumers with 24h to 365d data replay capabilities.
27. A — Application-level sanitization and CloudWatch Data Protection Policies prevent sensitive PII from leaking into logs.
28. A — AWS CodeBuild is a fully managed build service that compiles code, runs tests, and produces deployable artifacts.
29. A — Amazon OpenSearch Service is purpose-built for full-text search, autocomplete, and log analytics.
30. A — AWS CodeDeploy orchestrates blue/green traffic shifting with automated health checks and instant rollback.
31. A — The AWS Well-Architected Tool reviews workloads against AWS best practices and provides remediation guidance.
32. A — SNS Topic pub/sub fanning out to multiple SQS queues provides reliable, decoupled event distribution.
33. A — Storing session state in ElastiCache or DynamoDB makes the compute tier stateless and resilient to instance termination.
34. A — The `BeforeAllowTraffic` hook in CodeDeploy for Lambda executes pre-traffic validation or database migration scripts.
35. A — Visibility Timeout hides messages during processing; Message Retention Period is the total storage lifespan in SQS (up to 14 days).
36. A — Conditional writes with client idempotency keys prevent duplicate database updates from retried requests.
37. A — S3 Event Notifications triggering SQS and Lambda provides a decoupled, resilient, and cost-effective image processing pipeline.
38. A — An IAM Role requiring an `ExternalId` in its trust policy prevents the Confused Deputy problem for third-party cross-account access.
39. A — Route 53 Latency routing with health checks directs users to the lowest-latency healthy AWS Region.
40. A — Attaching an IAM Role via an Instance Profile provides secure, automatically rotated temporary credentials via IMDSv2.
41. A — Direct API Gateway service integration with Kinesis and Lambda with DynamoDB On-Demand handles 20,000 req/s serverlessly.
42. A — S3 Event Notifications to SQS with Lambda/Fargate workers ensures asynchronous processing without lost jobs.
43. A — Cognito for auth/scoped IAM credentials, S3 prefix policies for isolation, and DynamoDB + DAX for microsecond leaderboards.
44. A — Atomic conditional updates (`ConditionExpression: "InventoryCount >= :qty"`) prevent race conditions and overselling.
45. A & B — The Task Execution Role requires `secretsmanager:GetSecretValue` and `kms:Decrypt`, referenced in the `secrets` array.
46. A — SAM declares serverless components with `AWS::Serverless::Function`, `AWS::Serverless::Api`, and `AWS::Serverless::SimpleTable`.
47. A — Attaching Lambda to private subnets removes internet access; a NAT Gateway in a public subnet restores external connectivity.
48. A — SNS Fan-Out to multiple SQS queues allows each downstream microservice to process events independently at its own pace.
49. A — Customer Managed KMS Keys with annual rotation, S3 default SSE-KMS encryption, and bucket policy enforcing HTTPS.
50. A — `appspec.yaml` specifies Lambda deployment parameters, function aliases, and validation hooks for AWS CodeDeploy.
51. A — A hot partition is caused by uneven access keys; redesigning keys with high cardinality or adding DAX solves throughput bottlenecks.
52. A — API Gateway WebSocket APIs maintain persistent bidirectional connections for real-time chat applications.
53. A — Envelope Encryption with the AWS Encryption SDK encrypts payloads up to 2 MB locally using data keys protected by KMS.
54. A — AWS CloudFormation (or CDK) automates multi-tier stack provisioning reproducibly across accounts and Regions.
55. A — Amazon RDS Proxy pools and multiplexes database connections, preventing Lambda concurrency spikes from overwhelming MySQL.
56. A — The ECS Task Role (`taskRoleArn`) grants container application code temporary credentials to access DynamoDB and S3.
57. A — S3 static website hosting behind CloudFront with ACM and OAC provides global low-latency delivery at minimal cost.
58. A — CloudFront Signed URLs grant temporary, authenticated access to individual private files for authorized users.
59. A — HTTP 504 Gateway Timeout occurs when the backend Lambda function exceeds the API Gateway 29-second timeout.
60. A — Embedded Metric Format (EMF) extracts custom metrics asynchronously from JSON logs without `PutMetricData` API fees or latency.
61. A — EventBridge Scheduler triggering an AWS Batch job on Fargate runs 4-hour compute tasks with zero server management.
62. A — CodeDeploy manages canary deployments (`LambdaCanary10Percent10Minutes`) with automated CloudWatch alarm rollbacks.
63. A — SQS Dead-Letter Queues (DLQs) isolate poison pill messages after a configured number of failed receive attempts (`maxReceiveCount`).
64. A — AWS Step Functions coordinates multi-step branching, retries, and parallel execution with serverless state machines.
65. A — A Global Secondary Index (GSI) allows querying DynamoDB tables on non-key attributes (like `EmailAddress`).
66. A — GSIs can be created anytime with distinct partition/sort keys and dedicated capacity; LSIs must be created with the table.
67. A — AWS CodeArtifact is a secure, managed artifact repository for publishing and sharing private software packages.
68. A — X-Ray Subsegments provide granular timing breakdowns of specific database queries and HTTP calls within a segment.
69. A — Auto Scaling Lifecycle Hooks pause termination, allowing instances time to drain connections and complete tasks.
70. A — AWS Fargate runs containers serverlessly with per-second billing and zero EC2 infrastructure management.
71. A — An S3 bucket policy denying `s3:PutObject` unless the specific KMS Key ARN is provided enforces designated CMK encryption.
72. A — Cognito User Migration Lambda Trigger authenticates users against legacy databases and migrates them seamlessly upon first login.
73. A — `sam local invoke` and `sam local start-api` run and test Lambda functions locally inside Docker containers.
74. A — Provisioned Concurrency keeps Lambda execution environments initialized, eliminating cold-start latency.
75. A — DynamoDB Streams captures item-level mutations in real-time, triggering Lambda to synchronize search indexes.
76. A — AWS WAF protects CloudFront distributions against web exploits, SQLi, XSS, and rate-based DDoS attacks.
77. A — Allowing database port ingress from the application's Security Group ID follows the principle of least privilege.
78. A — CloudFront Custom Error Responses return `/index.html` with a 200 OK status for 403/404 errors, enabling client-side routing.
79. A — AWS Secrets Manager with automated rotation securely injects credentials into ECS Fargate containers via task definitions.
80. A — DynamoDB Accelerator (DAX) provides seamless microsecond in-memory caching without modifying application code.
81. A — CloudFormation Change Sets generate a detailed preview of proposed resource modifications and replacements.
82. A — Lambda ephemeral storage (`/tmp`) can be configured up to 10 GB to accommodate large temporary files.
83. A — Amazon EventBridge detects CodeCommit repository state changes and triggers CodePipeline automatically.
84. A — AWS Step Functions Standard Workflows provide visual state machine orchestration with built-in retries and error catchers.
85. A — Passing `Cache-Control: max-age=0` (with appropriate IAM permissions) bypasses the API Gateway cache to fetch fresh data.
86. A — Setting `MessageGroupId` to unique customer IDs allows SQS FIFO queues to process different customer groups concurrently.
87. A — An ECR Repository Policy in the target account must grant image download permissions to the CodeBuild service role ARN.
88. A — CloudFormation Rollback Triggers monitor CloudWatch alarms and roll back stack deployments if alarms fire during creation/updates.
89. A — AWS Lambda configured with sufficient memory and timeout (up to 15 mins) is the most cost-effective compute for 8-minute tasks.
90. A — VPC-attached Lambda functions in private subnets require a NAT Gateway in a public subnet for outbound internet access.
91. A — Requiring a custom secret header in CloudFront verified by AWS WAF or an API Gateway resource policy blocks direct URL access.
92. A — DynamoDB Time to Live (TTL) automatically deletes expired items based on a timestamp attribute without consuming WCU.
93. A — `DeploymentPreference` in SAM templates specifies CodeDeploy traffic shifting strategies (e.g., `Linear10PercentEvery1Minute`).
94. A — Envelope Encryption encrypts data locally with data keys protected by KMS master keys, overcoming the 4 KB direct KMS limit.
95. A — DynamoDB On-Demand capacity mode automatically accommodates unpredictable traffic spikes without manual provisioning.
96. A — `aws logs tail /aws/lambda/<FunctionName> --follow` streams live Lambda log events directly to the terminal.
97. A — AWS CodeDeploy orchestrates blue/green traffic shifting between ECS target groups with automated rollback.
98. A — CloudWatch Embedded Metric Format (EMF) extracts custom metrics asynchronously from JSON logs without `PutMetricData` fees.
99. A & B — KMS access requires permissions in the IAM identity policy (caller) AND the KMS Key Policy (resource).
100. A — Application Load Balancer operates at Layer 7 and supports path-based and host-based routing rules.
101. A — Kinesis Data Streams with Apache Flink performs real-time analytics; Kinesis Firehose delivers records to S3 for archival.
102. A — Creating a CloudFront Invalidation for `/index.html` (or `/*`) immediately purges cached objects from edge locations.
103. A — Strongly consistent reads consume 1 RCU per 4 KB; eventually consistent reads consume 0.5 RCU per 4 KB (half the cost).
104. A — AWS Step Functions Standard Workflows support long-running processes (up to 1 year) and human approval task tokens.
105. A — Amazon DynamoDB Global Tables provides fully managed multi-region, multi-master active-active replication.
106. A — CloudWatch Synthetics Canaries run scheduled browser scripts to monitor user flows and checkout endpoints 24/7.
107. A — Application Load Balancers maintain session stickiness using HTTP cookies (duration-based or application-based).
108. A — S3 Block Public Access enforces centralized protection preventing public bucket policies and ACLs account-wide.
109. A — SQS Delay Queues postpone initial message delivery to consumers by up to 15 minutes (`DeliveryDelay: 300`).
110. A — `BisectBatchOnFunctionError` splits failed Kinesis batches recursively, isolating poison pill records to a Dead-Letter Queue.
111. A — VPC-attached Lambda functions require private subnets and security groups with inbound access to the Redis port (6379).
112. A — A Route 53 Alias Record (A type) maps a zone apex domain (`example.com`) directly to an Application Load Balancer.
113. A — DynamoDB Streams streaming table mutations to a Lambda consumer writing to Amazon S3 creates an automated audit trail.
114. A — Cognito User Pools federated with SAML 2.0 Identity Providers allows authenticating users with corporate Active Directory credentials.
115. A — This end-to-end architecture satisfies all six Well-Architected Framework pillars through serverless resilience, security, and efficiency.
