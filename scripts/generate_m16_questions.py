#!/usr/bin/env python3
"""Generate 125 practice questions for Module 16: Monitoring, Logging & Observability"""

import os

questions_text = """# Module 16 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### CloudWatch Fundamentals: Metrics, Alarms, Dimensions & Dashboards (1–25)

1. A developer is designing a monitoring strategy for an e-commerce platform hosted on AWS. The application needs to track both AWS infrastructure metrics (such as EC2 CPU utilization) and application business metrics (such as completed checkout transactions). In Amazon CloudWatch, what concept isolates and groups related metrics together to prevent naming collisions?
A) Metric Dimensions
B) Metric Namespaces
C) Log Streams
D) CloudWatch Dashboards

2. Which prefix is reserved exclusively for metrics automatically published by AWS services in Amazon CloudWatch?
A) `Custom/`
B) `AWS/` (e.g., `AWS/Lambda`, `AWS/EC2`, `AWS/DynamoDB`)
C) `System/`
D) `Amazon/`

3. In Amazon CloudWatch, an engineer wants to track error rates separately for different microservices deployed in different environments (e.g., `Environment=Production`, `Service=PaymentService`). What CloudWatch metric component represents these key-value metadata qualifiers?
A) Namespaces
B) Dimensions
C) Units
D) Math Expressions

4. A developer publishes a custom metric named `LoginFailures` with two dimensions: `Environment=Prod` and `Region=us-east-1`. Later, the developer publishes the same metric with only one dimension: `Environment=Prod`. How does Amazon CloudWatch treat these two data streams?
A) It aggregates them automatically into a single metric
B) It treats them as two completely separate, independent metrics because CloudWatch uniquely identifies metrics by the combination of namespace, metric name, and exact dimension set
C) It rejects the second metric with an `InvalidParameterException`
D) It overwrites the first metric

5. A financial trading system needs to detect and alarm on rapid latency spikes occurring within a 5-second window. Standard CloudWatch metrics publish at a default 1-minute granularity. Which feature should the developer enable to publish and evaluate metrics at 1-second intervals?
A) CloudWatch High-Resolution Metrics
B) CloudWatch Basic Monitoring
C) AWS CloudTrail Data Events
D) Amazon Athena High-Throughput Engine

6. What is the minimum storage resolution available for Amazon CloudWatch High-Resolution Custom Metrics?
A) 1 millisecond
B) 1 second
C) 5 seconds
D) 1 minute

7. How does Amazon CloudWatch handle data retention for metrics over time?
A) All metrics are permanently deleted after 24 hours
B) CloudWatch retains metric data at decreasing granularity: 1-second data for 3 hours, 1-minute data for 15 days, 5-minute data for 63 days, and 1-hour data for 15 months
C) Metrics are retained indefinitely at 1-second resolution without data aggregation
D) Metric retention requires configuring an S3 lifecycle policy

8. A developer wants an automated notification sent to an on-call team's email address whenever an application's HTTP 5xx error rate exceeds 2% over a 5-minute evaluation period. What AWS service combination achieves this?
A) Amazon CloudWatch Alarm triggering an Amazon SNS Topic subscription
B) AWS CloudTrail triggering Amazon SES directly
C) Amazon S3 Event Notifications
D) AWS CodeArtifact Webhooks

9. What are the three possible operational states of an Amazon CloudWatch Alarm?
A) `ACTIVE`, `INACTIVE`, `PENDING`
B) `OK`, `ALARM`, `INSUFFICIENT_DATA`
C) `PASS`, `FAIL`, `UNKNOWN`
D) `HEALTHY`, `DEGRADED`, `CRITICAL`

10. When a newly created CloudWatch alarm has not yet received any metric data points from a newly deployed application, what state does the alarm enter by default?
A) `OK`
B) `ALARM`
C) `INSUFFICIENT_DATA`
D) `ERROR`

11. An operations engineer is experiencing alert fatigue because intermittent network blips trigger individual alarms that page the on-call engineer. The engineer wants an alert triggered ONLY when BOTH the CPU utilization exceeds 85% AND the application error rate exceeds 5% simultaneously. Which CloudWatch feature satisfies this requirement?
A) Metric Math Expressions
B) CloudWatch Composite Alarms
C) CloudWatch Anomaly Detection
D) High-Resolution Alarms

12. Which actions can be triggered directly by an Amazon CloudWatch Alarm when transitioning to the `ALARM` state? (Select TWO.)
A) Publishing a message to an Amazon SNS topic
B) Executing an Auto Scaling policy to scale out or scale in an Auto Scaling group
C) Compiling code in AWS CodeBuild
D) Creating an AWS CodeCommit repository
E) Initializing an AWS Amplify hosting branch

13. An application running on an Amazon EC2 instance becomes unresponsive due to memory leaks. The operations team wants CloudWatch to automatically reboot the EC2 instance when a custom memory alarm enters the `ALARM` state. What action type can be attached to the alarm?
A) EC2 Action (`Reboot this instance`)
B) SQS Action
C) S3 Glacier Action
D) Route 53 Action

14. A developer wants to create a single cross-region dashboard in the AWS Management Console that displays CPU utilization of EC2 instances in `us-east-1` alongside Lambda duration metrics in `eu-west-1`. Does Amazon CloudWatch Dashboards support this?
A) No, dashboards are strictly locked to a single AWS Region
B) Yes, CloudWatch Dashboards can visualize metrics and alarms from multiple AWS Regions on a single customized board
C) Only if the accounts are in AWS GovCloud
D) Only when using third-party Grafana plugins

15. What is the primary difference between a CloudWatch Dashboard and a CloudWatch Alarm?
A) A Dashboard is a visual monitoring interface for human observation across metrics, while an Alarm is an automated evaluation engine that triggers actions when metrics breach thresholds
B) Dashboards can send SMS notifications; Alarms cannot
C) Alarms are only available for EC2; Dashboards are only for S3
D) Dashboards only retain data for 1 hour

16. A developer uses CloudWatch Metric Math to calculate the percentage of failed requests in an API. What expression calculates the error percentage given metrics `Errors` (m1) and `TotalRequests` (m2)?
A) `(m1 / m2) * 100`
B) `m1 + m2`
C) `SUM(m1) - SUM(m2)`
D) `DIFF(m1, m2)`

17. What feature in Amazon CloudWatch uses machine learning models to automatically establish a dynamic expected baseline for a metric and detect abnormal spikes or drops without hardcoded threshold numbers?
A) CloudWatch Metric Math
B) CloudWatch Anomaly Detection
C) CloudWatch Contributor Insights
D) CloudWatch Evidently

18. An application needs to track the top 100 most active IP addresses generating traffic to an API Gateway endpoint. Which CloudWatch feature analyzes high-cardinality log data in real-time to identify top talkers and outliers?
A) CloudWatch Contributor Insights
B) CloudWatch Synthetics
C) AWS CloudTrail Lake
D) Amazon Inspector

19. A developer wants to simulate user traffic by running automated, scheduled headless browser scripts against a web application to verify that login flows and checkout buttons are functioning properly 24/7. Which CloudWatch feature provides this synthetic monitoring capability?
A) CloudWatch Synthetics Canaries
B) CloudWatch ServiceLens
C) CloudWatch Metric Filters
D) CloudWatch Logs Insights

20. A developer needs to publish 20 distinct data points to Amazon CloudWatch in a single API call to optimize network efficiency. Which AWS CLI command and parameter should be used?
A) `aws cloudwatch put-metric-data --namespace "MyApp" --metric-data file://metrics.json`
B) `aws cloudwatch send-metrics`
C) `aws cloudwatch write-log-events`
D) `aws cloudwatch post-data`

21. What is the maximum number of metric data points that can be submitted in a single `PutMetricData` API call in Amazon CloudWatch?
A) 100 data points (or up to 1 MB payload size)
B) 1 data point
C) 1,000,000 data points
D) Unlimited

22. A developer wants to publish custom memory and disk utilization metrics from an Amazon EC2 Linux instance to CloudWatch. Why are these metrics not published by default by AWS?
A) CloudWatch only monitors network cards
B) Memory and disk space are operating system-level guest metrics; the underlying hypervisor cannot inspect guest OS memory without an in-guest agent
C) Linux disables all monitoring APIs by default
D) EC2 instances do not support memory metrics

23. Which software agent must be installed and configured on Amazon EC2 instances or on-premises servers to collect internal OS metrics (memory, disk usage, swap) and custom application log files, streaming them to CloudWatch?
A) Unified Amazon CloudWatch Agent
B) AWS CodeDeploy Agent
C) AWS Systems Manager SSM Agent only
D) Amazon Kinesis Agent only

24. Where does the unified CloudWatch Agent store its configuration file on a Linux EC2 instance?
A) `amazon-cloudwatch-agent.json` (managed locally or via AWS Systems Manager Parameter Store)
B) `/etc/hosts`
C) `~/.bashrc`
D) `/dev/null`

25. An application uses CloudWatch alarms to trigger Auto Scaling step scaling policies. What CloudWatch alarm configuration setting determines how missing data points are treated when evaluating alarm status (e.g., during low-traffic periods)?
A) `TreatMissingData` (options: `breaching`, `notBreaching`, `ignore`, `missing`)
B) `DataFormat`
C) `ScaleFactor`
D) `AlarmGranularity`

---

### CloudWatch Logs, Log Groups, Subscriptions & Logs Insights (26–55)

26. An organization has hundreds of microservices running on AWS Lambda. By default, how does AWS Lambda organize log output generated by function code (`console.log`, `print()`)?
A) It writes logs to a shared Amazon S3 bucket in CSV format
B) It automatically creates a dedicated CloudWatch Log Group named `/aws/lambda/<function-name>`, with individual Log Streams created per execution environment instance
C) It stores logs in an unencrypted EC2 instance store
D) It sends all logs to an on-premises syslog server

27. A company’s monthly AWS bill shows steadily increasing storage costs for Amazon CloudWatch Logs. An audit reveals that log groups created three years ago are still consuming terabytes of storage. What is the default retention setting for newly created CloudWatch Log Groups, and how should this cost issue be fixed?
A) Default retention is 30 days; the issue is caused by duplicate log streams
B) Default retention is "Never Expire" (indefinite retention); the team should configure an explicit retention period (e.g., 30, 90, or 365 days) on each log group
C) CloudWatch Logs automatically charges a flat fee regardless of volume
D) The team must delete the AWS account

28. A security team wants to encrypt all log events stored in an Amazon CloudWatch Log Group using a Customer Managed Key (CMK) in AWS KMS. How can this be configured?
A) Associate the AWS KMS Key ARN with the CloudWatch Log Group using the `aws logs associate-kms-key` CLI command or CloudFormation
B) Encryption at rest is not supported for CloudWatch Logs
C) Encrypt the developer's laptop hard drive
D) Re-deploy the Lambda functions with SSL certificates

29. A developer wants to stream error logs from a CloudWatch Log Group in near real-time to an Amazon Kinesis Data Stream for real-time fraud analysis. Which CloudWatch Logs feature provides this continuous push mechanism?
A) CloudWatch Logs Subscription Filters
B) CloudWatch Logs Insights
C) S3 Lifecycle Rules
D) AWS CloudTrail Lake

30. Which three destinations are natively supported as targets for Amazon CloudWatch Logs Subscription Filters? (Select THREE.)
A) AWS Lambda functions
B) Amazon Kinesis Data Streams
C) Amazon Kinesis Data Firehose
D) Amazon DynamoDB directly
E) Amazon SQS directly
F) Amazon EC2 instance store

31. A developer wants to extract a custom metric from plain-text application logs. Whenever a log line in `/var/log/application.log` contains the phrase `[ERROR] DatabaseConnectionFailed`, CloudWatch should increment a metric named `DatabaseFailures` by 1. Which feature achieves this?
A) CloudWatch Logs Metric Filters
B) CloudWatch Subscription Filters
C) Amazon Athena Partition Projection
D) CloudWatch Synthetics

32. What is the difference between a CloudWatch Metric Filter and a CloudWatch Subscription Filter?
A) A Metric Filter scans incoming log streams for patterns and extracts numeric metric data points to plot on graphs and alarm on; a Subscription Filter streams full raw log events to external processing destinations (Lambda, Kinesis) in near real-time
B) Metric Filters are only for Windows; Subscription Filters are only for Linux
C) Both filters perform identical operations
D) Metric Filters delete log data upon match

33. An operations engineer needs to search through 50 GB of application logs across multiple log groups to find all HTTP 500 errors that occurred between 2:00 PM and 3:00 PM, and count how many times each unique customer ID experienced an error. Which tool provides interactive SQL-like querying directly against CloudWatch Logs?
A) Amazon CloudWatch Logs Insights
B) AWS CloudTrail Event History
C) AWS X-Ray Service Map
D) Amazon S3 Glacier Select

34. In CloudWatch Logs Insights, which command is used to filter log events based on specific conditions (such as matching a regex or checking an extracted field value)?
A) `filter` (e.g., `filter level = "ERROR" or @message like /Timeout/`)
B) `where`
C) `having`
D) `match`

35. A developer writes the following query in CloudWatch Logs Insights:
```
fields @timestamp, @message
| filter @message like /Exception/
| stats count(*) as exceptionCount by bin(5m)
| sort exceptionCount desc
```
What does this query do?
A) It deletes all exception logs every 5 minutes
B) It finds all log messages containing the word "Exception", counts the occurrences in 5-minute time buckets, and sorts the buckets by the highest count in descending order
C) It reboots the database if exceptions exceed 5
D) It converts the logs into a PDF report

36. In CloudWatch Logs Insights, what does the `bin()` function do when used inside a `stats ... by bin(1h)` aggregation?
A) It deletes the logs from the recycle bin
B) It groups timestamped log events into discrete, equal-sized time intervals (e.g., 1-hour buckets) for time-series aggregation
C) It compresses binary data
D) It encrypts the logs using Base64

37. A developer is querying unstructured plain-text Apache web server logs in CloudWatch Logs Insights. The log line format is `192.168.1.1 - GET /products HTTP/1.1 200 1420`. Which Logs Insights command extracts the client IP, HTTP method, status code, and response size into queryable fields?
A) `parse @message "* - * * * * *" as clientIp, method, path, protocol, statusCode, responseSize`
B) `select clientIp, method, path`
C) `split(@message, " ")`
D) `extract-all`

38. What built-in fields are automatically generated and present in every log event queried via CloudWatch Logs Insights?
A) `@timestamp`, `@message`, `@logStream`, `@log`
B) `@ip`, `@mac`, `@gateway`
C) `@user`, `@password`, `@role`
D) `@cpu`, `@memory`, `@disk`

39. A developer wants to export historical log data from a CloudWatch Log Group to an Amazon S3 bucket for low-cost compliance archiving. Which method exports the log data?
A) Create an Export Task to Amazon S3 via the CloudWatch Logs console or `aws logs create-export-task` CLI command
B) Take an EBS snapshot of the CloudWatch server
C) Download log files one by one using a web browser
D) CloudWatch Logs cannot be exported to S3

40. How are queries in Amazon CloudWatch Logs Insights priced?
A) Flat rate of $50 per query
B) Billed based on the volume of log data scanned (per GB scanned) during the query
C) Billed per second of query execution time only
D) Free of charge up to 100 TB per month

41. What is the maximum number of CloudWatch Log Groups that can be queried simultaneously in a single CloudWatch Logs Insights query?
A) 1 log group
B) Up to 50 log groups (or up to 10,000 log groups with cross-account queries)
C) Exactly 5 log groups
D) Unlimited

42. A developer wants to mask sensitive customer information (such as credit card numbers and Social Security numbers) automatically in real-time as logs are ingested into CloudWatch Logs. Which feature provides automated PII data protection and masking?
A) CloudWatch Logs Data Protection Policies (using managed data identifiers and audit masking)
B) CloudWatch Metric Math
C) Amazon S3 Versioning
D) AWS WAF Rate Limiting

43. An application writes log events in JSON format: `{"statusCode": 404, "path": "/login", "latency": 150}`. How does CloudWatch Logs Insights handle JSON-formatted log lines?
A) It automatically parses and indexes the JSON fields, allowing the developer to query `statusCode`, `path`, and `latency` directly without writing a custom `parse` statement
B) It rejects JSON logs as malformed
C) It requires converting JSON to XML before querying
D) It only indexes top-level arrays

44. A developer configures a Metric Filter with the filter pattern `{ $.statusCode = 500 }`. What type of log format is this filter pattern designed to match?
A) JSON-structured log events containing a top-level property `statusCode` equal to 500
B) Plain-text CSV logs
C) XML documents with namespace prefixes
D) Binary byte buffers

45. A developer wants to test a metric filter pattern against sample log lines before deploying it to production. How can this be done using the AWS CLI?
A) `aws logs test-metric-filter --filter-pattern "{ $.level = \"ERROR\" }" --log-event-messages "{\"level\":\"ERROR\",\"msg\":\"fail\"}"`
B) `aws cloudwatch test-alarm`
C) `aws lambda invoke-test`
D) `aws logs check-syntax`

46. What happens to a CloudWatch Logs Subscription Filter if the destination AWS Lambda function's resource-based policy does not grant `logs.amazonaws.com` permission to invoke the function?
A) The Lambda function is deleted
B) CloudFormation rolls back the entire AWS account
C) The subscription filter fails to deliver log events and drops them, incrementing delivery error metrics
D) CloudWatch writes logs to an unformatted S3 bucket

47. How can an organization stream CloudWatch Logs across multiple AWS accounts to a central security analysis account in real time?
A) CloudWatch Logs Cross-Account Subscription Filters (streaming logs to a central Amazon Kinesis Data Stream in the security account)
B) Emailing log files daily
C) Storing logs on an EC2 instance in `us-east-1`
D) Using VPC Peering without IAM roles

48. A developer wants to view live log events streaming from a Lambda function in real-time in their terminal window during development. Which AWS CLI command provides live log tailing?
A) `aws logs tail /aws/lambda/MyFunction --follow`
B) `aws logs view-stream`
C) `aws lambda stream-logs`
D) `tail -f /dev/null`

49. What is the maximum payload size of a single log event (including timestamp and UTF-8 message string) accepted by Amazon CloudWatch Logs?
A) 256 KB
B) 10 MB
C) 5 GB
D) 1 KB

50. A developer wants to run automated, scheduled queries in CloudWatch Logs Insights and save the output to Amazon S3 for weekly reporting. Which AWS service can orchestrate scheduled Logs Insights queries?
A) Amazon EventBridge Scheduler invoking an AWS Lambda function or AWS Step Functions state machine that calls the `StartQuery` API
B) Amazon Route 53
C) AWS CodeArtifact
D) Amazon ElastiCache

51. What does the `@logStream` field in CloudWatch Logs Insights represent for an AWS Lambda function?
A) The specific Lambda execution environment instance that processed the invocation
B) The AWS account ID
C) The IP address of the client calling API Gateway
D) The git commit hash

52. In CloudWatch Logs Insights, what command limits the number of query results returned to the caller?
A) `limit <number>` (e.g., `limit 25`)
B) `top <number>`
C) `max <number>`
D) `fetch <number>`

53. An application logs HTTP status codes in plain text: `STATUS=200` or `STATUS=500`. What is the metric filter pattern to match all log events where the status is 500?
A) `[..., status = "STATUS=500", ...]` or `"?STATUS=500"`
B) `SELECT WHERE 500`
C) `STATUS == 500`
D) `500.status.match`

54. If an application outputs logs to standard output (`stdout`) and standard error (`stderr`) in an AWS Lambda function, where do those logs appear in CloudWatch?
A) They are automatically captured and written to the function's CloudWatch Log Group with distinct log events
B) They are discarded unless explicitly forwarded via syslog
C) They are written to local `/tmp` and deleted on cold start
D) They are sent to Amazon SES

55. What is the impact of setting a log retention policy on a CloudWatch Log Group?
A) All log events older than the configured retention period (e.g., 30 days) are automatically and permanently deleted by CloudWatch
B) All log events are encrypted with a public key
C) The log group is converted into an S3 bucket
D) Existing metrics derived from the logs are deleted

---

### Structured Logging & CloudWatch Embedded Metric Format (EMF) (56–75)

56. Why is structured logging (formatting log messages as valid JSON objects) strongly recommended over plain-text logging for microservice applications running on AWS?
A) Structured JSON logs allow downstream tools (CloudWatch Logs Insights, OpenSearch, SIEMs) to automatically parse, filter, aggregate, and index fields without brittle regex patterns
B) JSON logs compress to zero bytes
C) Plain-text logs are prohibited by the AWS Lambda runtime
D) JSON logs eliminate the need for IAM roles

57. A developer is building a high-throughput payment microservice that processes 5,000 transactions per second on AWS Lambda. The developer wants to record custom business metrics (such as transaction latency and payment amounts broken down by merchant ID and card type) in Amazon CloudWatch. Calling the `PutMetricData` API synchronously for every transaction adds latency and incurs significant API costs. Which feature solves this problem?
A) CloudWatch Embedded Metric Format (EMF)
B) Amazon S3 Glacier Select
C) Amazon RDS Multi-AZ replication
D) AWS CodeGuru Reviewer

58. How does CloudWatch Embedded Metric Format (EMF) work under the hood?
A) The application outputs a specially structured JSON log line containing an `_aws` metadata object to `stdout`; CloudWatch Logs automatically parses the log line, extracts the metrics asynchronously, and generates CloudWatch metrics without separate `PutMetricData` API calls
B) It requires launching an EC2 instance in every AZ
C) It stores metrics in a DynamoDB table
D) It sends UDP packets directly to CloudWatch servers

59. What are two major benefits of using CloudWatch Embedded Metric Format (EMF) instead of calling `PutMetricData`? (Select TWO.)
A) Zero additional network latency added to the application request path, as metrics are emitted via asynchronous standard log output
B) Lower cost at high volume, as metric extraction from logs avoids standalone CloudWatch `PutMetricData` per-call API ingestion fees
C) EMF completely eliminates CloudWatch Logs storage fees
D) EMF only works on Windows Server instances
E) EMF automatically writes data to Amazon Redshift

60. In an EMF-formatted JSON log event, which top-level JSON key contains the metadata defining the CloudWatch namespace, dimensions, and metric names?
A) `_aws` (containing `CloudWatchMetrics: [...]`)
B) `metadata`
C) `cloudwatch`
D) `metrics_config`

61. Examine the following EMF payload:
```json
{
  "_aws": {
    "Timestamp": 1693495325183,
    "CloudWatchMetrics": [
      {
        "Namespace": "PaymentService",
        "Dimensions": [["Environment", "PaymentType"]],
        "Metrics": [
          { "Name": "ProcessingTime", "Unit": "Milliseconds" }
        ]
      }
    ]
  },
  "Environment": "Production",
  "PaymentType": "CreditCard",
  "CustomerId": "cust-12345",
  "ProcessingTime": 245,
  "TransactionId": "tx-98765"
}
```
What happens to the fields `"CustomerId"` and `"TransactionId"` that are NOT listed in the `Dimensions` array?
A) They are rejected and cause an error
B) They are preserved in the CloudWatch Log event as searchable structured log context queryable in Logs Insights, but are not graphed as metric dimensions (avoiding high-cardinality metric explosion)
C) They are deleted by CloudWatch
D) They are converted to XML

62. What issue occurs when a developer includes high-cardinality values (such as unique `TransactionId` or `CustomerId` values) as metric dimensions in standard CloudWatch `PutMetricData` calls?
A) Metric cardinality explosion, creating millions of custom metrics and resulting in massive AWS CloudWatch billing charges
B) The Lambda function crashes with a stack overflow
C) CloudWatch drops all network connections
D) The database is locked in read-only mode

63. Which client library provided by AWS simplifies emitting Embedded Metric Format logs in Node.js, Python, and Java applications?
A) AWS Embedded Metrics SDK (`aws-embedded-metrics`)
B) Boto3 Core only
C) AWS Amplify SDK
D) AWS CDK Assertions

64. How does the AWS Embedded Metrics SDK handle metrics in an AWS Lambda environment?
A) It formats the JSON payload and writes it directly to `stdout`, allowing the native Lambda logging pipeline to forward it to CloudWatch Logs
B) It opens a persistent TCP socket to the Lambda service API
C) It creates a local SQLite database
D) It sends an email via Amazon SES

65. When running containerized applications on Amazon ECS or Amazon EKS, how are EMF logs captured and forwarded to CloudWatch?
A) By running the CloudWatch Agent as a sidecar container or DaemonSet, which listens for EMF logs over UDP/TCP or tailing container log files
B) By running `sam local start-api`
C) By configuring an S3 lifecycle policy
D) By manually copying files to `/tmp`

66. What CloudWatch metric unit options are valid in an EMF metric definition?
A) `Seconds`, `Milliseconds`, `Microseconds`, `Bytes`, `Kilobytes`, `Megabytes`, `Count`, `Percent`, and `None`
B) Only `Count`
C) `DollarAmount`
D) `Liters`

67. Can a single EMF JSON log line define multiple metrics simultaneously (e.g., emitting both `OrderValue` and `ProcessingDuration`)?
A) Yes, the `Metrics` array within the `_aws.CloudWatchMetrics` definition can contain multiple metric objects
B) No, each EMF log line can only contain exactly one metric
C) Only if using Java
D) Only in `us-east-1`

68. A developer wants to query historical EMF logs in CloudWatch Logs Insights to calculate the average `ProcessingTime` for a specific `CustomerId = "cust-12345"`. Which query works?
A) `fields ProcessingTime | filter CustomerId = "cust-12345" | stats avg(ProcessingTime)`
B) `select avg(ProcessingTime) where CustomerId = cust-12345`
C) `emf-query ProcessingTime`
D) `get CustomerId`

69. What happens if an EMF JSON payload is malformed (e.g., missing the `Namespace` property inside `_aws`)?
A) CloudWatch Logs stores the log line as a standard log event, but skips metric extraction and records an EMF extraction error
B) CloudWatch deletes the entire log group
C) The Lambda execution environment is terminated
D) The AWS account is blocked

70. How does EMF enable cost-effective observability for serverless architectures?
A) By unifying structured application logging and custom metric emission into a single write path, eliminating redundant API calls and decoupling metric extraction from the critical request path
B) By replacing all database storage with S3 Glacier
C) By disabling encryption across all services
D) By compressing images at edge locations

71. A developer wants to log an error in a structured JSON format in Python. What is the recommended practice?
A) Output a JSON-serialized dictionary containing standard fields (`timestamp`, `level`, `message`, `service`, `error`, `stackTrace`) using the standard logging library or tools like AWS Lambda Powertools
B) Use `print("ERROR: Something bad happened")`
C) Write the error to a local CSV file
D) Send an SMS alert on every error

72. In a distributed microservices environment, what correlation identifier should be included in every structured log line across all services involved in processing a user request?
A) `CorrelationId` (or `RequestId` / `TraceId`) propagated via HTTP headers (such as `X-Correlation-Id` or `X-Amzn-Trace-Id`)
B) The database administrator password
C) The EC2 instance MAC address
D) The local timezone offset

73. How does AWS Lambda Powertools assist developers in implementing structured logging, metrics, and tracing?
A) It provides a suite of lightweight utilities for Python, TypeScript, Java, and .NET that automate structured JSON logging, EMF metric creation, and X-Ray tracing with simple decorators and annotations
B) It compiles Lambda functions into native C++ binaries
C) It provisions EC2 instances automatically
D) It replaces AWS CloudFormation

74. A developer uses AWS Lambda Powertools for Python. How can they automatically log every incoming event and inject standard execution context into structured JSON logs?
A) By decorating the handler with `@logger.inject_lambda_context(log_event=True)`
B) By running `sam build`
C) By configuring Route 53 health checks
D) By adding an S3 bucket policy

75. When comparing standard CloudWatch Custom Metrics (`PutMetricData`) with CloudWatch Logs Metric Filters and EMF, which statement is accurate?
A) `PutMetricData` makes direct synchronous API calls; Metric Filters scan plain-text/JSON logs post-ingestion using filter patterns; EMF embeds metric definitions directly inside structured JSON logs for automatic asynchronous extraction
B) EMF is deprecated and replaced by `PutMetricData`
C) Metric Filters can only be used on Windows Server
D) `PutMetricData` does not support dimensions

---

### AWS X-Ray: Distributed Tracing, Segments, Subsegments & Sampling (76–100)

76. A developer is investigating an e-commerce checkout flow where requests traverse Amazon API Gateway, AWS Lambda, Amazon DynamoDB, and a third-party payment gateway API. Users report intermittent 5-second latency. Which AWS service provides end-to-end distributed tracing and visual call-graph mapping to pinpoint the exact bottleneck?
A) AWS X-Ray
B) Amazon CloudWatch Logs
C) AWS CloudTrail
D) AWS Trusted Advisor

77. In AWS X-Ray, what is the unique identifier that is generated at the start of a request and forwarded across all downstream services in an HTTP header (`X-Amzn-Trace-Id`) to correlate trace segments together?
A) Trace ID
B) Segment ID
C) Session Token
D) Secret Key

78. What is the difference between an X-Ray Segment and an X-Ray Subsegment?
A) A Segment represents the work done by a distinct compute resource/service (e.g., an entire Lambda function execution); a Subsegment provides granular timing breakdowns for specific downstream calls or code blocks within that segment (e.g., a DynamoDB query or external HTTP request)
B) Segments are for frontend; Subsegments are for backend
C) Subsegments are only supported in Java
D) Segments are not recorded in X-Ray

79. A developer wants to attach custom searchable key-value pairs (such as `OrderId` and `CustomerId`) to an X-Ray segment so that specific customer traces can be filtered and queried in the X-Ray console. Which X-Ray feature should the developer use?
A) X-Ray Annotations
B) X-Ray Metadata
C) X-Ray Sampling Rules
D) CloudWatch Alarms

80. What is the key distinction between X-Ray Annotations and X-Ray Metadata?
A) Annotations are indexed key-value pairs that can be searched and used with filter expressions in the X-Ray console; Metadata is non-indexed key-value data that provides contextual debugging details for a specific trace but cannot be queried across traces
B) Metadata is indexed; Annotations are not
C) Annotations can only contain integers; Metadata can only contain strings
D) Metadata is automatically deleted after 5 minutes

81. A developer wants to instrument a Node.js application using the AWS X-Ray SDK to automatically trace all outgoing AWS SDK calls (e.g., DynamoDB, S3, SQS). What code snippet achieves this automatic capture?
A) `const AWSXRay = require('aws-xray-sdk-core'); const AWS = AWSXRay.captureAWS(require('aws-sdk'));`
B) `console.log("Trace started");`
C) `process.env.TRACE_ALL = "true";`
D) `AWS.enableTracing();`

82. In Python, which method from the AWS X-Ray SDK automatically patches all supported libraries (Boto3, Requests, HTTP client) for distributed tracing?
A) `patch_all()` from `aws_xray_sdk.core`
B) `xray.start()`
C) `boto3.enable_xray()`
D) `trace.auto()`

83. A developer wants to enable AWS X-Ray active tracing on an AWS Lambda function using the AWS CLI or CloudFormation. What property must be configured?
A) `TracingConfig: { Mode: "Active" }` (or `Tracing: Active` in SAM)
B) `XRay: true`
C) `EnableTracing: "Yes"`
D) `DebugMode: "Enabled"`

84. What is the role of the AWS X-Ray Daemon?
A) It is a background listening process that receives raw UDP trace packets (port 2000) from the X-Ray SDK, buffers them, and uploads them in batches to the X-Ray API
B) It compiles application code into bytecode
C) It generates SSL certificates for CloudFront
D) It reboots EC2 instances on failure

85. Does a developer need to install or run the X-Ray daemon manually when using AWS Lambda with Active Tracing enabled?
A) No, AWS Lambda manages the X-Ray daemon automatically within the serverless execution environment
B) Yes, the developer must package the daemon binary inside the Lambda zip file
C) Yes, the daemon must run in an EC2 instance in the same VPC
D) Only when running in `us-west-2`

86. When running containerized applications on Amazon ECS on AWS Fargate, how is the X-Ray daemon typically deployed?
A) As a sidecar container in the ECS Task Definition alongside the application container
B) On a physical on-premises server
C) Inside an S3 bucket
D) As a Lambda layer

87. A high-volume web service handles 10,000 requests per second. Tracing 100% of requests would generate excessive trace data and high X-Ray costs. How can the developer control the percentage of requests recorded by X-Ray without redeploying application code?
A) Configure X-Ray Sampling Rules in the AWS X-Ray console or API
B) Delete the X-Ray SDK from the application
C) Throttle incoming HTTP traffic at the load balancer
D) Reduce the EC2 instance count

88. In an AWS X-Ray Sampling Rule, what do the "Reservoir" and "Fixed Rate" parameters control?
A) The Reservoir ensures a minimum number of traces are recorded per second (e.g., 1 trace/sec); the Fixed Rate defines the percentage of additional requests sampled beyond the reservoir (e.g., 5% of subsequent requests)
B) Reservoir sets the memory limit; Fixed Rate sets CPU clock speed
C) Reservoir controls database connection pools; Fixed Rate sets HTTP timeout
D) They configure CloudWatch metric retention

89. A developer opens the AWS X-Ray console and views a visual node graph showing all connected microservices, databases, and external APIs, color-coded by error rate and latency. What is this visual representation called?
A) X-Ray Service Map
B) CloudWatch Metric Dashboard
C) AWS CloudTrail Event Graph
D) VPC Network Topology Map

90. In an X-Ray Service Map, what does a red circle around a service node indicate?
A) A high percentage of HTTP 5xx errors (faults) originated from or were returned by that service
B) The service is running on an outdated Linux kernel
C) The service has been terminated
D) The service is missing an IAM role

91. In an X-Ray Service Map, what does a yellow circle around a service node indicate?
A) HTTP 4xx client errors (throttling or client errors) occurred on that service
B) The service is offline
C) The service has high disk usage
D) The service is in development mode

92. A developer wants to create a custom subsegment in Python to measure the execution time of an internal image processing function `process_image()`. How is this written using the X-Ray SDK?
A)
```python
with xray_recorder.in_subsegment('process_image'):
    process_image()
```
B) `xray.time('process_image')`
C) `console.time('process_image')`
D) `trace(process_image)`

93. If an unhandled exception occurs inside an X-Ray subsegment, what does the X-Ray SDK do automatically?
A) It records the exception details (error message, type, stack trace) in the subsegment metadata and marks the subsegment as a fault (`error: true` or `fault: true`)
B) It crashes the entire server
C) It deletes the trace
D) It reboots the database

94. What IAM permission is required in a Lambda function's execution role to allow it to upload trace data to AWS X-Ray?
A) `xray:PutTraceSegments` and `xray:PutTelemetryRecords` (included in `AWSXRayDaemonWriteAccess` policy)
B) `AdministratorAccess`
C) `s3:PutObject`
D) `ec2:DescribeInstances`

95. How does AWS X-Ray propagate trace context across asynchronous boundaries (such as passing a message through Amazon SQS to a worker Lambda function)?
A) SQS automatically passes the trace header in message system attributes; the consumer SDK extracts the `AWSTraceHeader` to continue the trace segment
B) SQS converts trace data into an XML file
C) Tracing across asynchronous queues is impossible
D) The developer must hardcode the trace ID in the SQS queue URL

96. A developer wants to search for all X-Ray traces that experienced a latency greater than 3 seconds and where the annotation `environment` equals `"production"`. What filter expression syntax is used in the X-Ray console?
A) `responsetime > 3 AND annotation.environment = "production"`
B) `SELECT * WHERE time > 3 AND env = "production"`
C) `filter: latency > 3s`
D) `find traces --slow`

97. An API Gateway REST API is integrated with an AWS Lambda backend. When X-Ray tracing is enabled on both API Gateway and Lambda, what component creates the initial root Trace ID?
A) API Gateway (on the initial incoming HTTP request)
B) Lambda
C) DynamoDB
D) CloudWatch Logs

98. A developer wants to record user IP addresses in X-Ray traces to analyze geographic performance trends. Where are client IP addresses captured by default?
A) In the `http.request.client_ip` field of the entry segment generated by API Gateway or Application Load Balancer
B) In the EC2 BIOS log
C) In the Route 53 DNS query log
D) In the S3 bucket policy

99. What AWS service integrates X-Ray distributed traces, CloudWatch metrics, and CloudWatch Logs into a unified single-pane-of-glass troubleshooting interface?
A) CloudWatch ServiceLens (and Application Signals)
B) AWS Artifact
C) AWS CloudShell
D) Amazon Inspector

100. How long does AWS X-Ray retain trace data by default?
A) 30 days
B) 24 hours
C) 1 year
D) Indefinitely

---

### Root Cause Analysis, Error Codes, SDK Exceptions & Deployment Troubleshooting (101–125)

101. An API client sends a `POST /orders` request with a missing required JSON property in the request body. The server rejects the request. What HTTP status code should the API return?
A) 400 Bad Request
B) 500 Internal Server Error
C) 403 Forbidden
D) 504 Gateway Timeout

102. A frontend web application attempts to access an Amazon S3 bucket, but receives an HTTP 403 Forbidden error. What is the fundamental root cause of an HTTP 403 status code in AWS?
A) An authorization failure where the caller's identity is known (or anonymous), but IAM policies, S3 Bucket Policies, or Access Control Lists explicitly deny or fail to grant permission for the requested action
B) The requested S3 object does not exist
C) The client internet connection failed
D) S3 is experiencing a server outage

103. An API Gateway endpoint backed by a Lambda function returns an HTTP 504 Gateway Timeout error to callers. What does this status code indicate?
A) The Lambda function execution duration exceeded API Gateway's maximum integration timeout limit (fixed at 29 seconds) or a downstream network call hung
B) The Lambda function returned a 404 status code
C) The client sent an invalid query string
D) API Gateway was deleted

104. A developer configures an API Gateway REST API with a Lambda Proxy integration. When calling the API, callers receive an HTTP 502 Bad Gateway error. The Lambda execution logs show that the function executed successfully and returned a plain string `"Hello World"`. What caused the 502 error?
A) Lambda Proxy integration requires the function to return a specific JSON response structure containing `statusCode` (integer), `headers` (object), and `body` (string); returning a plain string violates the proxy integration contract
B) The Lambda function ran out of disk space
C) API Gateway requires all responses to be encrypted with KMS
D) The API Gateway URL is incorrect

105. An application encounters an HTTP 429 Too Many Requests status code when invoking an AWS API. What action should the developer implement in their application code to handle this error gracefully?
A) Retry the request immediately in a tight loop with zero delay
B) Implement exponential backoff with full jitter to retry the request over increasing time intervals
C) Terminate the application process
D) Delete the IAM user credentials

106. A Python application querying Amazon DynamoDB throws a `ProvisionedThroughputExceededException`. CloudWatch metrics show that the table's total consumed capacity is well below the provisioned capacity limits. What is the most likely root cause?
A) A "hot partition" caused by an uneven partition key distribution, where a large percentage of read or write requests target a single physical storage partition that exceeds its per-partition throughput limit
B) The DynamoDB table has too many Global Secondary Indexes
C) The AWS account has run out of DynamoDB storage
D) The application is using an invalid IAM role

107. What are two valid solutions to resolve frequent `ProvisionedThroughputExceededException` errors caused by hot partitions in DynamoDB? (Select TWO.)
A) Redesign the partition key schema to introduce high-cardinality keys or append random suffixes (key salting) to distribute traffic evenly across partitions
B) Deploy Amazon DynamoDB Accelerator (DAX) to cache read requests in memory
C) Reduce the DynamoDB table provisioned capacity to 1 RCU
D) Delete all Global Secondary Indexes
E) Convert the DynamoDB table to Amazon S3 Glacier

108. An application executes a conditional write against a DynamoDB table: `attribute_exists(OrderId) AND OrderStatus = :pending`. The operation fails with a `ConditionalCheckFailedException`. What does this exception mean?
A) An expected application-level optimistic locking condition was not met because the item either did not exist or its `OrderStatus` was not `pending` at the time of write
B) DynamoDB is experiencing an internal hardware fault
C) The IAM execution role lacks `dynamodb:PutItem` permission
D) The DynamoDB table was dropped

109. An application calling AWS KMS to decrypt data throws an `AccessDeniedException`. Which three IAM policy components should the developer inspect to diagnose the permission failure? (Select THREE.)
A) The IAM Identity-Based Policy attached to the calling role/user
B) The AWS KMS Key Policy attached to the KMS Customer Master Key (CMK)
C) Any applicable IAM Permissions Boundaries or Service Control Policies (SCPs) in AWS Organizations
D) The S3 Bucket Lifecycle Policy
E) The VPC Route Table
F) The Route 53 Hosted Zone

110. A developer attempts to invoke a Lambda function using the AWS SDK, but receives a `ResourceNotFoundException`. What is the cause?
A) The specified Lambda function name or ARN does not exist in the targeted AWS Region or account
B) The Lambda function code has a syntax error
C) The Lambda execution role has expired
D) The EC2 instance ran out of memory

111. During an automated CI/CD pipeline execution, an AWS CodeBuild project fails in the `BUILD` phase. The application's CloudWatch runtime logs show no activity. Where should the engineer look to find the root cause of the build failure?
A) In the AWS CodeBuild project build logs streamed to CloudWatch Logs (examining compiler errors, failed unit test steps, or non-zero exit codes in `buildspec.yml`)
B) In the S3 server access logs
C) In the VPC Flow Logs
D) In the AWS Cost Explorer

112. A continuous deployment pipeline using AWS CodeDeploy fails during a deployment to an EC2 Auto Scaling group. The deployment status shows `FAILED` at the `AfterInstall` lifecycle hook. Where can the developer find the detailed script output and error logs from the deployment hooks?
A) In the CodeDeploy agent log files on the EC2 instance (located at `/var/log/aws/codedeploy-agent/codedeploy-agent.log` and `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`)
B) In the Route 53 DNS query log
C) In the AWS CloudTrail management events
D) In the AWS CodeArtifact repository metadata

113. A CloudFormation stack update fails and triggers an automatic rollback (`UPDATE_ROLLBACK_IN_PROGRESS`). Where can the developer immediately see the exact resource and reason that caused the deployment failure?
A) In the CloudFormation console's "Events" tab for the stack, looking for the first resource that transitioned to `CREATE_FAILED` or `UPDATE_FAILED` with its accompanying `Status Reason`
B) In the IAM user login history
C) In the Amazon S3 billing dashboard
D) In the AWS Trusted Advisor security check

114. A developer needs to audit who deleted a production Amazon DynamoDB table at 3:00 AM on Sunday. Which AWS service provides the authoritative audit log recording the IAM identity, API action (`DeleteTable`), timestamp, source IP address, and request parameters?
A) AWS CloudTrail
B) Amazon CloudWatch Logs Insights
C) AWS X-Ray
D) Amazon CodeGuru Profiler

115. What is the difference between AWS CloudTrail Management Events and AWS CloudTrail Data Events?
A) Management Events record control-plane operations on AWS resources (e.g., `CreateBucket`, `DeleteTable`, `ModifySecurityGroupRules`), logged by default; Data Events record high-volume data-plane operations (e.g., `s3:GetObject`, `lambda:Invoke`, DynamoDB item CRUD), which must be explicitly enabled
B) Management Events are for Linux; Data Events are for Windows
C) Data Events are free; Management Events cost $10 per call
D) Both event types are identical

116. A company wants to run SQL queries across historical CloudTrail event logs spanning 3 years across all AWS Regions without setting up complex ETL data pipelines. Which CloudTrail feature provides built-in SQL query capabilities?
A) CloudTrail Lake
B) CloudTrail Event History (limited to past 90 days)
C) Amazon CloudWatch Alarms
D) AWS CodeCommit

117. What is the fundamental difference between Amazon CodeGuru Reviewer and Amazon CodeGuru Profiler?
A) CodeGuru Reviewer performs automated static code analysis on source code during pull requests to detect security flaws, leaked credentials, and anti-patterns; CodeGuru Profiler performs runtime performance analysis on active production applications to find CPU and latency bottlenecks
B) CodeGuru Reviewer is for Python only; CodeGuru Profiler is for Java only
C) CodeGuru Profiler reviews pull requests; CodeGuru Reviewer runs on EC2
D) CodeGuru Reviewer is an antivirus scanner

118. A developer wants to analyze why a Java microservice deployed on Amazon ECS consumes 90% CPU under normal traffic. The developer wants a visual flame graph showing the exact methods and lines of code spending the most CPU cycles. Which AWS tool generates this analysis?
A) Amazon CodeGuru Profiler
B) Amazon CodeGuru Reviewer
C) AWS CloudTrail
D) Amazon Inspector

119. A developer suspects that hardcoded AWS access keys were accidentally committed to a GitHub repository branch. Which tool can automatically scan pull requests and flag hardcoded credentials before merging?
A) Amazon CodeGuru Reviewer (or git-secrets / AWS Secrets Manager secret scanner)
B) Amazon Route 53
C) CloudWatch Alarms
D) AWS DataSync

120. An AWS Lambda function fails with an error `Runtime.HandlerNotFound`. What is the root cause?
A) The handler method specified in the Lambda function configuration does not match the actual file name or exported function name in the deployment package
B) The Lambda function ran out of memory
C) The function's execution role lacks KMS permissions
D) The API Gateway endpoint was deleted

121. A Lambda function fails with `Task timed out after 3.00 seconds`. What are two immediate troubleshooting actions a developer should take? (Select TWO.)
A) Increase the Lambda function `Timeout` setting (up to the 15-minute maximum) to accommodate long-running tasks
B) Check X-Ray traces or CloudWatch Logs to identify slow downstream calls (e.g., hanging database queries or un-cached external API calls) causing the timeout
C) Delete the Lambda execution role
D) Reduce function memory to 128 MB
E) Convert the Lambda runtime to Assembly

122. An application running on EC2 attempts to send messages to an SQS queue, but receives an `AWS.SimpleQueueService.NonExistentQueue` error. What is the root cause?
A) The specified SQS queue URL does not exist in the targeted AWS Region or account, or the queue name in the URL is misspelled
B) The SQS queue is full
C) SQS messages have expired
D) The EC2 instance was rebooted

123. A developer wants to configure automated alerts when an AWS service quota (such as the number of running EC2 instances or Lambda concurrent executions) reaches 85% of its account limit. Which service provides metrics on quota utilization for CloudWatch alarms?
A) AWS Service Quotas integration with Amazon CloudWatch
B) AWS Budgets only
C) AWS Support tickets only
D) Amazon S3 Storage Lens

124. An operations team wants to be notified in a Slack channel whenever an AWS CodePipeline pipeline execution fails. Which AWS architecture pattern implements this event-driven alert?
A) AWS CodePipeline emits a state-change event to Amazon EventBridge; an EventBridge rule matches `state: FAILED` and triggers an Amazon SNS topic or AWS Chatbot integrated with Slack
B) CloudWatch Metrics polling CodePipeline every 10 milliseconds
C) Running an EC2 cron job that checks pipeline status
D) S3 Bucket Notifications

125. An architect is reviewing an end-to-end observability strategy for a serverless microservices application:
1. Distributed request tracing across API Gateway, Lambda, and DynamoDB with visual call-graph mapping.
2. Structured JSON logging with automated metric emission without extra API calls.
3. Interactive ad-hoc log querying for root-cause analysis.
4. Auditing control-plane API activity for compliance.
Which combination of AWS services correctly satisfies these requirements?
A) AWS X-Ray (tracing) + CloudWatch Embedded Metric Format (logging & metrics) + CloudWatch Logs Insights (log querying) + AWS CloudTrail (audit logging)
B) CloudWatch Alarms only for all four requirements
C) AWS CloudTrail for tracing and metrics + AWS CodeGuru for log querying + Amazon S3 for auditing
D) Amazon Athena for tracing + AWS Secrets Manager for metrics + Amazon Route 53 for querying

---

## Answer Key & Explanations

1. B — Namespaces isolate and group related metrics in CloudWatch, preventing naming collisions between services.
2. B — The `AWS/` prefix (e.g., `AWS/Lambda`, `AWS/EC2`) is reserved exclusively for metrics published by AWS services.
3. B — Dimensions are key-value pairs that uniquely identify and qualify a metric within a namespace.
4. B — CloudWatch uniquely identifies metrics by the combination of namespace, metric name, and exact dimension set; differing dimensions create separate metrics.
5. A — High-Resolution Custom Metrics allow publishing and evaluating metric data points down to 1-second intervals.
6. B — 1 second is the finest storage resolution supported for high-resolution metrics in CloudWatch.
7. B — CloudWatch retains metrics at decreasing granularity: 1s for 3h, 1m for 15d, 5m for 63d, and 1h for 15 months.
8. A — A CloudWatch Alarm watching metric thresholds publishes messages to an Amazon SNS topic, notifying subscribers via email or SMS.
9. B — The three standard operational states for a CloudWatch alarm are `OK`, `ALARM`, and `INSUFFICIENT_DATA`.
10. C — Alarms start in `INSUFFICIENT_DATA` until enough metric data points are received to determine status.
11. B — Composite Alarms evaluate multiple underlying alarms using logical AND/OR conditions to reduce alert noise.
12. A & B — CloudWatch Alarms can trigger SNS notifications, Auto Scaling actions, and EC2 instance actions directly.
13. A — CloudWatch Alarms can execute EC2 actions directly, such as rebooting, stopping, terminating, or recovering instances.
14. B — CloudWatch Dashboards can display metrics, alarms, and Logs Insights widgets from multiple AWS Regions on a single board.
15. A — Dashboards provide visual displays for human operators; Alarms evaluate thresholds and execute automated actions.
16. A — CloudWatch Metric Math supports arithmetic expressions like `(m1 / m2) * 100` to calculate error percentages.
17. B — CloudWatch Anomaly Detection applies machine learning algorithms to continuously analyze metric patterns and detect abnormal deviations.
18. A — CloudWatch Contributor Insights analyzes high-cardinality log data in real-time to identify top talkers and contributors.
19. A — CloudWatch Synthetics Canaries run automated, scheduled browser scripts to verify user workflows and endpoints 24/7.
20. A — `aws cloudwatch put-metric-data` submits multiple metric data points in a single API call using a JSON payload.
21. A — `PutMetricData` supports up to 100 metric data points (or 1 MB payload size) in a single request.
22. B — Memory and disk utilization are guest OS metrics that the hypervisor cannot inspect without an in-guest agent.
23. A — The Unified CloudWatch Agent collects system-level metrics (memory, disk, swap) and log files from EC2 instances and on-premises servers.
24. A — The unified CloudWatch Agent configuration is stored in `amazon-cloudwatch-agent.json` or managed via SSM Parameter Store.
25. A — `TreatMissingData` defines how missing data points are handled (`breaching`, `notBreaching`, `ignore`, `missing`).
26. B — Lambda automatically creates a dedicated Log Group `/aws/lambda/<function-name>` with individual Log Streams per execution environment.
27. B — CloudWatch Log Groups default to "Never Expire"; configuring an explicit retention period automatically prunes old log data to control costs.
28. A — CloudWatch Log Groups support encryption at rest with AWS KMS Customer Managed Keys using `associate-kms-key`.
29. A — CloudWatch Logs Subscription Filters stream log events in near real-time to Lambda, Kinesis Data Streams, or Kinesis Data Firehose.
30. A, B & C — AWS Lambda, Amazon Kinesis Data Streams, and Amazon Kinesis Data Firehose are native targets for Subscription Filters.
31. A — CloudWatch Logs Metric Filters scan incoming log lines for specific text/JSON patterns and increment custom CloudWatch metrics.
32. A — Metric Filters extract numeric metrics to graph and alarm on; Subscription Filters forward full raw log events to external streaming targets.
33. A — CloudWatch Logs Insights provides an interactive, purpose-built query language to search and aggregate log data directly.
34. A — The `filter` command filters log events by string matching, boolean logic, or regex expressions.
35. B — The query searches for "Exception", counts matching lines in 5-minute time buckets (`bin(5m)`), and sorts descending.
36. B — `bin()` groups timestamped log events into discrete, equal-sized time buckets for time-series aggregation.
37. A — The `parse` command extracts fields from unstructured text logs using glob-style wildcards into named query variables.
38. A — `@timestamp`, `@message`, `@logStream`, and `@log` are standard built-in fields present in all Logs Insights query results.
39. A — Export tasks (`create-export-task`) asynchronously export log data from CloudWatch Log Groups to Amazon S3 buckets.
40. B — CloudWatch Logs Insights pricing is based on the volume of log data scanned (per GB scanned) per query.
41. B — CloudWatch Logs Insights supports querying up to 50 log groups in a single query (up to 10,000 across accounts).
42. A — CloudWatch Logs Data Protection Policies automatically identify and mask sensitive PII (credit cards, SSNs) upon ingestion.
43. A — CloudWatch Logs Insights automatically parses JSON log events, making top-level keys directly queryable without `parse`.
44. A — `{ $.statusCode = 500 }` matches JSON-structured log events where the `statusCode` property equals 500.
45. A — `test-metric-filter` tests a metric filter pattern against sample log messages via the AWS CLI.
46. C — If permissions are missing, the subscription filter cannot invoke the target and drops log events, incrementing error metrics.
47. A — Cross-Account Subscription Filters stream logs from source accounts to a central Kinesis Data Stream in a security account.
48. A — `aws logs tail <log-group> --follow` tails live log events in real-time in the terminal window.
49. A — The maximum payload size for a single log event in CloudWatch Logs is 256 KB.
50. A — EventBridge Scheduler invoking Lambda or Step Functions can execute the `StartQuery` API to automate scheduled queries.
51. A — In Lambda log groups, `@logStream` identifies the specific execution environment instance that processed the request.
52. A — The `limit` command restricts the number of rows returned by a Logs Insights query.
53. A — `[..., status = "STATUS=500", ...]` matches plain-text tokenized logs for the specified string.
54. A — Standard output and standard error from Lambda function execution are automatically captured and written to CloudWatch Logs.
55. A — Setting a retention policy causes CloudWatch to permanently delete log events older than the specified duration.
56. A — Structured JSON logs enable automated parsing, searching, and aggregation in modern observability tools without brittle regex.
57. A — CloudWatch Embedded Metric Format (EMF) embeds metric definitions inside JSON logs for automatic extraction without separate API calls.
58. A — EMF outputs specially formatted JSON with an `_aws` metadata object; CloudWatch asynchronously extracts and graphs the metrics.
59. A & B — EMF adds zero network latency (emitted via standard log output) and avoids `PutMetricData` per-call ingestion fees.
60. A — The `_aws` key in EMF contains the `CloudWatchMetrics` array defining namespaces, dimensions, and metric names.
61. B — Unmapped fields in an EMF payload are retained as searchable log context without creating high-cardinality metric dimensions.
62. A — High-cardinality dimensions in CloudWatch Custom Metrics cause metric explosion, creating thousands of custom metrics and high costs.
63. A — The AWS Embedded Metrics SDK (`aws-embedded-metrics`) provides helper libraries for emitting EMF logs in Node.js, Python, and Java.
64. A — In Lambda, the Embedded Metrics SDK writes JSON to `stdout`, which Lambda's native logging pipeline streams to CloudWatch Logs.
65. A — On ECS/EKS, the CloudWatch Agent runs as a sidecar or DaemonSet listening for EMF log events over UDP/TCP.
66. A — EMF supports standard CloudWatch units including `Seconds`, `Milliseconds`, `Bytes`, `Count`, and `Percent`.
67. A — The `Metrics` array in an EMF `_aws` definition can declare multiple metric definitions in a single log line.
68. A — Fields in EMF JSON logs are directly accessible in Logs Insights queries using standard `filter` and `stats` syntax.
69. A — Malformed EMF payloads are stored as regular log events; metric extraction is skipped without crashing the application.
70. A — EMF unifies application logging and metric emission into a single write path, reducing API overhead and operational complexity.
71. A — Formatting errors as JSON objects with timestamp, level, message, and error details provides structured, actionable telemetry.
72. A — A `CorrelationId` or `TraceId` propagated across service boundaries correlates related log events for end-to-end request tracing.
73. A — AWS Lambda Powertools provides opinionated utilities for structured logging, EMF metric creation, and X-Ray tracing.
74. A — `@logger.inject_lambda_context(log_event=True)` in Powertools automatically logs incoming events and Lambda context.
75. A — `PutMetricData` makes direct synchronous API calls; Metric Filters scan logs post-ingestion; EMF embeds metric extraction directly in JSON logs.
76. A — AWS X-Ray provides distributed request tracing, subsegment timing analysis, and visual service maps across microservices.
77. A — A Trace ID is generated at request entry and propagated through `X-Amzn-Trace-Id` to correlate segments across services.
78. A — A Segment records the work of a single service/compute node; Subsegments provide granular timing for downstream calls within that segment.
79. A — X-Ray Annotations are indexed key-value pairs used to search and filter traces in the X-Ray console.
80. A — Annotations are indexed and searchable; Metadata is non-indexed contextual debugging data visible on individual traces.
81. A — `AWSXRay.captureAWS(require('aws-sdk'))` wraps the AWS SDK to automatically trace all outgoing AWS API calls in Node.js.
82. A — `patch_all()` in the Python AWS X-Ray SDK automatically instruments supported libraries (Boto3, Requests, HTTP clients).
83. A — Setting `TracingConfig: { Mode: "Active" }` enables X-Ray Active Tracing on an AWS Lambda function.
84. A — The X-Ray Daemon listens for UDP trace packets (port 2000) from SDKs and uploads them in batches to the X-Ray API.
85. A — AWS Lambda automatically provisions and manages the X-Ray daemon in the serverless execution environment.
86. A — On Amazon ECS on Fargate, the X-Ray daemon is deployed as a sidecar container in the task definition.
87. A — X-Ray Sampling Rules dynamically control the rate and volume of traces collected without application redeployment.
88. A — The Reservoir sets a minimum guaranteed number of traces/second; Fixed Rate sets the percentage of additional requests sampled.
89. A — An X-Ray Service Map is a visual representation of all interconnected services and resources participating in traced requests.
90. A — A red circle on an X-Ray Service Map node indicates a high percentage of HTTP 5xx errors or service faults.
91. A — A yellow circle on an X-Ray Service Map node indicates HTTP 4xx client errors (such as throttling or bad requests).
92. A — `with xray_recorder.in_subsegment('process_image'):` creates a custom subsegment to measure internal function execution time.
93. A — The X-Ray SDK automatically captures exception details and marks the subsegment with `error: true` or `fault: true`.
94. A — `xray:PutTraceSegments` and `xray:PutTelemetryRecords` permit Lambda execution roles to upload trace data to X-Ray.
95. A — SQS passes the `AWSTraceHeader` in message system attributes, allowing consumer functions to continue the distributed trace.
96. A — `responsetime > 3 AND annotation.environment = "production"` filters X-Ray traces by duration and custom annotations.
97. A — API Gateway generates the root Trace ID for incoming HTTP requests when X-Ray tracing is enabled.
98. A — Client IP addresses are recorded in the `http.request.client_ip` field of entry segments generated by API Gateway or ALBs.
99. A — CloudWatch ServiceLens integrates X-Ray traces, CloudWatch metrics, and log groups into a unified observability interface.
100. A — AWS X-Ray retains trace data for 30 days by default.
101. A — Missing required client parameters or malformed payloads should return HTTP 400 Bad Request.
102. A — HTTP 403 Forbidden indicates an authorization failure where the caller lacks permission under IAM or resource policies.
103. A — HTTP 504 Gateway Timeout occurs when an integration (e.g., Lambda) exceeds the gateway timeout limit (29s) or hangs.
104. A — Lambda Proxy integration requires returning a specific JSON object (`statusCode`, `headers`, `body`); returning a raw string causes HTTP 502.
105. B — HTTP 429 Too Many Requests should be handled by retrying with exponential backoff and jitter.
106. A — A hot partition occurs when access patterns concentrate on a narrow key range, exceeding single-partition throughput limits.
107. A & B — High-cardinality partition keys (or key salting) distribute traffic across partitions; DAX caches read traffic in memory.
108. A — `ConditionalCheckFailedException` is an expected optimistic locking failure when item attributes do not match the write condition.
109. A, B & C — Diagnosing KMS access denials requires checking the IAM identity policy, the KMS key policy, and any applicable SCPs.
110. A — `ResourceNotFoundException` indicates the targeted AWS resource does not exist in the specified Region or account.
111. A — CodeBuild build logs streamed to CloudWatch Logs detail compiler errors, failed tests, and command exit codes.
112. A — CodeDeploy agent logs on target instances (`/var/log/aws/codedeploy-agent/`) record deployment lifecycle script output and failures.
113. A — The CloudFormation "Events" tab lists resource lifecycle transitions and the specific `Status Reason` for failed resources.
114. A — AWS CloudTrail records control-plane API activity, including identity, API action (`DeleteTable`), timestamp, and IP address.
115. A — CloudTrail Management Events record resource-level operations (logged by default); Data Events record item/object operations (opt-in).
116. A — CloudTrail Lake provides built-in SQL query capabilities across multi-region, multi-account audit logs.
117. A — CodeGuru Reviewer performs static analysis during pull requests; CodeGuru Profiler analyzes runtime CPU/latency hotspots in production.
118. A — Amazon CodeGuru Profiler generates flame graphs identifying specific CPU-intensive methods in running applications.
119. A — CodeGuru Reviewer uses ML models to scan pull requests for hardcoded AWS credentials and security vulnerabilities.
120. A — `Runtime.HandlerNotFound` indicates the configured handler path does not match the actual file or function name in the zip package.
121. A & B — Increasing function timeout and analyzing X-Ray traces/logs to identify slow downstream dependencies resolves timeouts.
122. A — `NonExistentQueue` indicates the specified SQS queue URL does not exist in the targeted Region or is misspelled.
123. A — AWS Service Quotas integration with CloudWatch allows setting alarms when resource usage approaches service quotas.
124. A — CodePipeline emits state-change events to EventBridge, which matches failures and triggers SNS or Chatbot alerts to Slack.
125. A — X-Ray for tracing, EMF for structured logging/metrics, Logs Insights for querying, and CloudTrail for auditing delivers comprehensive observability.
"""

with open("16-Monitoring-Logging-and-Observability/questions.md", "w", encoding="utf-8") as f:
    f.write(questions_text)

print("Successfully wrote 16-Monitoring-Logging-and-Observability/questions.md")

