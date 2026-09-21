# DVA-C02 Mock Exam 3 — Exam-Level (65 Questions)

Written to match or exceed real DVA-C02 difficulty: multi-requirement scenarios (about 60 words each), full-sentence answer options of similar length, 13 "Select TWO" questions, domains mixed as on the real exam, and correct answers spread evenly across A–D.

- **Time limit**: 130 minutes · **Domain weighting**: 21 / 17 / 16 / 11 questions (32 / 26 / 24 / 18%)
- **Target**: 47+ correct (≈72%) is a solid pass signal on this exam.
- The interactive version (`mock-exam-3.html`) re-shuffles options on every attempt; this key matches the order printed here.

---

**1.** *(Domain 2)* A company protects an Amazon API Gateway REST API with an Amazon Cognito user pool authorizer. Any signed-in user must be able to call GET /reports, but DELETE /reports must be allowed only for app clients that were granted the custom scope reports/admin in the user pool. Which approach will meet these requirements?

- A) Configure the reports/admin OAuth scope on the DELETE method's authorization settings, and have clients send the ID token because it contains the scope claim.
- B) Create a usage plan with an API key for admin clients and associate it with the DELETE method so that only clients with that key can call the method.
- C) Configure the reports/admin OAuth scope on the DELETE method's authorization settings, and have clients send an access token in the Authorization header.
- D) Add a Lambda authorizer to the DELETE method that calls the Cognito AdminGetUser API on every request and checks whether the user belongs to an admin group.

**2.** *(Domain 3)* A developer runs cdk deploy for the first time in a new AWS account and Region. The stack includes an AWS Lambda function with local code assets. The deployment fails with an error stating that the required staging resources, such as the assets bucket and deployment roles, do not exist. What should the developer do?

- A) Run cdk synth before every cdk deploy, because synthesizing the app creates the assets bucket and deployment roles in the target account automatically as part of the process.
- B) Run cdk diff with a force option so that the CDK CLI deploys the stack directly without staging the assets in the target account first.
- C) Run cdk bootstrap once for that account and Region so that the CDKToolkit stack creates the staging bucket, the ECR repository and the IAM roles that deployments use.
- D) Create an Amazon S3 bucket named cdk-assets by hand and add the bucket name to the code property of the Lambda function construct in the stack.

**3.** *(Domain 1)* In an AWS Step Functions state machine, a Task state named ChargeCard calls a Lambda function and is followed by a Task state named SendReceipt, which needs the order_id and email fields from the execution input. After a recent change, SendReceipt fails because its input now contains only the payment confirmation object returned by ChargeCard. Which change to the ChargeCard state fixes this with the fewest changes?

- A) Add a ResultSelector that copies $.order_id into the task result so that the order ID from the input is included in the output.
- B) Add "InputPath": "$" so that the ChargeCard state receives the complete execution input instead of a filtered subset of the fields.
- C) Add "ResultPath": "$.payment" so that the Lambda result is added to the original input under a payment key instead of replacing the whole input.
- D) Add "OutputPath": "$.payment" so that only the payment field of the Lambda result is passed on as the complete input of the SendReceipt state.

**4.** *(Domain 1)* An application invokes an AWS Lambda function asynchronously from Amazon S3 event notifications. The operations team needs a record of every invocation that still fails after Lambda's automatic retries, including the original event, the error message and the stack trace, delivered to an Amazon SQS queue. The team also wants the result of every successful invocation published to an Amazon EventBridge event bus. Which solution will meet these requirements with the LEAST custom code?

- A) Wrap the handler in a try/catch block that sends failures to the queue with SendMessage and sends each success to the event bus with PutEvents before returning.
- B) Configure an on-failure destination that targets the SQS queue and an on-success destination that targets the event bus in the function's asynchronous invocation configuration.
- C) Configure a dead-letter queue that targets the SQS queue so that failed events are captured after the retries, and add code at the end of the handler that calls PutEvents on the event bus after each successful run.
- D) Point the S3 event notification at the SQS queue directly, and create an EventBridge rule that forwards every S3 event on to the Lambda function for processing.

**5.** *(Domain 1)* A developer is building a mobile trading app. The app must push price updates to all connected users in real time, let users fetch a nested portfolio view that combines data from an Amazon DynamoDB table and an existing REST microservice in a single request, and keep working while the phone is briefly offline. The developer wants to minimize custom backend infrastructure. Which solution will meet these requirements?

- A) Build an Amazon API Gateway REST API with a Lambda function that aggregates both data sources, and have the app poll the API every second to pick up the latest price updates for each user.
- B) Build an AWS AppSync GraphQL API with DynamoDB and HTTP data sources, use subscriptions for price updates, and use the Amplify client libraries for offline data synchronization.
- C) Build an Application Load Balancer with sticky sessions in front of Amazon EC2 instances that hold the WebSocket connections and query both data sources for each user.
- D) Build an Amazon API Gateway WebSocket API for price updates, store connection IDs in DynamoDB, and have a Lambda function call the @connections API for every price change.

**6.** *(Domain 3)* A company wants to roll out a new checkout feature flag gradually over one hour to the AWS Lambda functions that read it, and automatically roll the flag back if the checkout error-rate alarm goes off. The rollout must not require deploying new code or publishing new function versions. Which solution will meet these requirements?

- A) Store the flag in an Amazon DynamoDB table that every function reads on each request, and have an operator update the value by hand every 10 minutes during the rollout.
- B) Store the flag in a Lambda environment variable, and use AWS CodeDeploy with a Linear10PercentEvery10Minutes configuration and the alarm to shift traffic to a new version.
- C) Store the flag in an AppConfig feature flag profile, deploy it with a linear strategy and the alarm as a rollback monitor, and read it with the AppConfig Lambda extension.
- D) Store the flag in a Parameter Store parameter, and have a scheduled Lambda function change the flag value every 10 minutes while it checks the state of the alarm.

**7.** *(Domain 1)* A developer configured an AWS Lambda function with an Amazon SQS event source mapping that uses a batch size of 10. When one message in a batch fails validation, the function throws an exception, and all 10 messages become visible again and are reprocessed, which causes messages that already succeeded to be processed repeatedly. The developer must keep the current batch size. Which combination of actions will ensure that only the failed messages are retried? (Select TWO.)

- A) Configure an on-failure destination on the event source mapping so that the successful messages in a failed batch are deleted from the queue.
- B) Set the visibility timeout of each successful message to 0 inside the function before throwing the exception so that the queue removes them.
- C) Enable ReportBatchItemFailures in the function response types of the event source mapping so that Lambda accepts a partial batch response.
- D) Enable long polling on the queue by setting ReceiveMessageWaitTimeSeconds to 20 seconds so that each batch contains fewer messages.
- E) Return a batchItemFailures list containing the message IDs of the failed messages from the handler instead of throwing an exception.

**8.** *(Domain 2)* An application must encrypt 20 MB files client-side before uploading them to Amazon S3, using a customer managed AWS KMS key. The security team requires that file contents never leave the application in plaintext and that each file is encrypted with its own unique key. Which combination of steps should the developer implement? (Select TWO.)

- A) Export the customer managed key's key material once, cache it inside the application, and use it with AES-256 to encrypt all of the files locally.
- B) Store the encrypted data key returned by GenerateDataKey alongside the encrypted file, and call the KMS Decrypt operation on that key whenever the file must be read.
- C) Call the KMS Encrypt operation directly on each 20 MB file with the customer managed key, and upload the ciphertext blob that KMS returns to the S3 bucket.
- D) Upload each file with the x-amz-server-side-encryption header set to aws:kms so that Amazon S3 encrypts every object with the customer managed key.
- E) Call the KMS GenerateDataKey operation for each file, encrypt the file locally with the returned plaintext data key, and remove the plaintext key from memory after use.

**9.** *(Domain 1)* An order service writes a new order to an Amazon DynamoDB table and immediately queries a global secondary index on customer_id to show the customer's full order list. Customers sometimes report that the order they just placed is missing until they refresh. The table holds hundreds of millions of items, lookups must stay efficient as it grows, and the developer must guarantee the new order always appears without adding a cache. Which solution will meet these requirements?

- A) Change the key schema so that customer_id is the table's partition key and order_id is the sort key, migrate the data, and query the base table with ConsistentRead set to true.
- B) Replace the index query with a Scan of the base table that filters on customer_id and sets ConsistentRead to true so that the newest order is always included.
- C) Keep the existing global secondary index and set ConsistentRead to true on each Query against it so that DynamoDB always returns the most recent committed data for the customer.
- D) Enable DynamoDB Streams on the table and make the application wait for the new order's stream record before running the query against the global secondary index.

**10.** *(Domain 2)* A mobile app lets users sign in with an email address and password or with Google. After sign-in, the app must upload photos directly to an Amazon S3 bucket, and each user must be able to write only under a prefix that matches their own identity. The company does not want to operate any backend for authentication or credential issuance. Which combination of steps will meet these requirements? (Select TWO.)

- A) Attach a bucket policy that allows s3:PutObject for the Cognito user pool ID as the principal, and send each user's ID token with every S3 request.
- B) Generate a presigned URL for every photo from a Lambda function that trusts the Google ID token sent by the app without validating its signature.
- C) Create an Amazon Cognito identity pool that trusts the user pool, with an authenticated role that allows s3:PutObject on bucket/${cognito-identity.amazonaws.com:sub}/*.
- D) Create an IAM user for each app user during sign-up, and deliver that IAM user's access keys to the app after the user signs in for the first time.
- E) Create an Amazon Cognito user pool with Google configured as a federated identity provider, and have the app sign users in through the user pool.

**11.** *(Domain 2)* A web application on AWS Lambda generates Amazon S3 presigned URLs with a 24-hour expiration so that customers can download invoices from an email link. Customers report that many links stop working after a few hours with an ExpiredToken error. The application signs the URLs with the credentials of the function's execution role. What is the cause of the problem?

- A) Presigned URLs that are generated inside a Lambda function are always limited to a maximum expiration of 1 hour, whatever expiration value is passed in the SDK call.
- B) The bucket's default SSE-S3 encryption invalidates presigned URLs whenever the object's encryption key is rotated, which happens every few hours.
- C) A presigned URL signed with temporary credentials stops working when those credentials expire, which can be much sooner than the 24-hour expiration set in the URL.
- D) Customers' email clients add an Authorization header when opening links, which overrides the signature in the presigned URL's query string.

**12.** *(Domain 4)* A security team must find out which IAM principal downloaded a confidential file from an Amazon S3 bucket last week. An organization trail in AWS CloudTrail is enabled with default settings and delivers logs to a central bucket, but the team cannot find any GetObject entries. What is the reason, and what should be done for future investigations?

- A) GetObject calls appear only in the CloudTrail console's 90-day event history, so the team should search the event history instead of the trail's log files.
- B) S3 object downloads are recorded only in VPC Flow Logs, so the team should enable flow logs on the VPC that contains the bucket for future investigations.
- C) CloudTrail delivers data events after a 30-day delay, so the team should wait and then search the trail's log files again for the GetObject entries.
- D) The trail logs only management events by default; enable S3 data events for the bucket on the trail so that object-level calls such as GetObject are recorded.

**13.** *(Domain 2)* An analytics pipeline writes about 20,000 small objects per second to an Amazon S3 bucket that uses SSE-KMS with a customer managed key. The pipeline starts failing with KMS ThrottlingException errors, and the KMS bill has grown significantly. The security team requires that the customer managed key remain in use for every object. Which solution will reduce both the errors and the cost with the LEAST effort?

- A) Enable S3 Bucket Keys for SSE-KMS on the bucket so that S3 uses a short-lived bucket-level key derived from the KMS key and sends far fewer requests to KMS.
- B) Switch the bucket's default encryption to SSE-S3, and use the customer managed key only for the objects that contain sensitive customer data.
- C) Create ten more customer managed keys and have the pipeline spread its objects across all of them to distribute the KMS request load evenly.
- D) Request a KMS request quota increase for the Region and add exponential backoff with jitter to the pipeline so that throttled PutObject requests are retried later.

**14.** *(Domain 1)* A developer's application writes to Amazon DynamoDB and Amazon SQS in short, heavy bursts. Under load, some calls fail with ThrottlingException and ProvisionedThroughputExceededException. The application's own retry loop retries each failed call immediately, up to 10 times, and this makes the throttling worse. The developer wants the most resilient behavior with the least code. What should the developer do?

- A) Remove the custom retry loop and configure the AWS SDK's standard or adaptive retry mode, which retries throttling errors with exponential backoff and jitter.
- B) Remove all retries and send every failed request to a dead-letter queue so that the operations team can reprocess the requests manually later.
- C) Keep the custom retry loop but add a fixed 1-second sleep between attempts so that every client retries at the same predictable interval after a failure.
- D) Keep the custom retry loop and raise its maximum number of attempts to 50 so that more of the requests eventually succeed during each burst of traffic.

**15.** *(Domain 3)* A team deploys the same Lambda function code to test and production. Production must always run a specific tested build that later deployments cannot change by accident, and the team must be able to promote a newer build or roll back to the previous one in seconds without changing the API Gateway integration. Which solution will meet these requirements?

- A) Publish a numbered version for each tested build, point a prod alias at that version, integrate API Gateway with the alias ARN, and update the alias to promote or roll back.
- B) Integrate API Gateway with $LATEST for production, and record which build is currently deployed in an environment variable so that the team can roll back by hand if needed.
- C) Create a separate function for each build, and use a Route 53 weighted record to move production traffic between the function URLs of the different builds.
- D) Integrate API Gateway with the numbered version ARN directly, and change the integration and redeploy the stage every time the team promotes or rolls back a build.

**16.** *(Domain 3)* A company's Elastic Beanstalk application must process image-resizing jobs that users submit through the web application, and a nightly job must clean up expired uploads. Each resize job takes up to 3 minutes and must not slow down web requests. The team wants the least additional infrastructure to manage. Which solution will meet these requirements?

- A) Launch an Amazon EC2 instance from a custom AMI that polls an SQS queue for jobs, and add a cron job on that same instance for the nightly cleanup task.
- B) Create a separate Elastic Beanstalk worker environment that processes jobs from its Amazon SQS queue, and define the nightly job in a cron.yaml file in the worker's source bundle.
- C) Run the resize jobs in background threads on the web server environment's instances, and schedule the nightly job with a crontab entry that is added to every instance through .ebextensions.
- D) Create a second web server environment that exposes a /jobs endpoint, and have the web application call it synchronously for each image with a 3-minute timeout.

**17.** *(Domain 2)* A company runs its web application in the eu-west-1 Region behind an Application Load Balancer and is adding an Amazon CloudFront distribution for the custom domain shop.example.com. The developer requested a public certificate for shop.example.com in AWS Certificate Manager (ACM) in eu-west-1, but the certificate does not appear when the developer configures the distribution. What should the developer do?

- A) Export the eu-west-1 certificate's private key from ACM, and upload the certificate to the IAM certificate store so that CloudFront can use it.
- B) Attach the eu-west-1 certificate only to the Application Load Balancer, because CloudFront uses its origin's certificate for viewers automatically.
- C) Request or import a certificate for shop.example.com in ACM in the us-east-1 Region, and then select that certificate in the distribution's settings.
- D) Enable ACM cross-Region replication for the eu-west-1 certificate so that CloudFront can use a replica of it at every edge location.

**18.** *(Domain 1)* A developer is sizing an Amazon DynamoDB table in provisioned capacity mode. The application must perform 80 strongly consistent reads per second of items that are 7 KB each and 40 standard writes per second of items that are 1.5 KB each. The application does not use transactions. What is the minimum provisioned capacity that meets these requirements?

- A) 140 read capacity units and 60 write capacity units
- B) 80 read capacity units and 40 write capacity units
- C) 160 read capacity units and 60 write capacity units
- D) 160 read capacity units and 80 write capacity units

**19.** *(Domain 2)* A payment service writes JSON request logs to Amazon CloudWatch Logs. An audit finds that some log events contain full credit card numbers and email addresses. The company must mask this data in all future log events for most users, still allow a small security team to see the unmasked values, and avoid changing application code. Which solution will meet these requirements?

- A) Set the log group's retention period to one day so that log events containing sensitive data are deleted before most users have a chance to view them.
- B) Encrypt the log group with a customer managed KMS key and grant kms:Decrypt only to the security team so that all other users see only ciphertext when they view log events in the console.
- C) Create a metric filter that matches credit card number patterns and publishes a metric, and configure an alarm that notifies the security team whenever that metric increases.
- D) Create a CloudWatch Logs data protection policy on the log group with managed data identifiers for credit card numbers and email addresses, and grant only the security team logs:Unmask.

**20.** *(Domain 1)* A company collects clickstream events from its website at about 5,000 events per second. Three teams need the same events independently: one computes metrics within one second of each event, one trains a model on the last 7 days of events and re-reads them several times, and one archives everything to Amazon S3. The company wants a single ingestion point. Which solution will meet these requirements?

- A) Ingest into a Kinesis Data Streams stream with 7-day retention, give the metrics and training teams enhanced fan-out consumers, and archive to S3 with a Firehose stream that reads from it.
- B) Ingest into an Amazon Data Firehose stream that delivers to S3, and have the metrics and training teams read the objects that Firehose writes into the bucket.
- C) Ingest into an Amazon SNS topic with three SQS queue subscriptions, one per team, and set each queue's retention period to 7 days so that the training team can re-read the events whenever it needs to.
- D) Ingest into an Amazon SQS standard queue, and have each team's consumer receive messages from the same queue and delete each message after it has been processed.

**21.** *(Domain 3)* An Amazon ECS service on AWS Fargate pulls its image from a private Amazon ECR repository and injects a database password from AWS Secrets Manager through the task definition's secrets field. At run time, the application writes files to an Amazon S3 bucket. New tasks fail to start with an error that the secret could not be retrieved, and after that is fixed, the application logs AccessDenied for s3:PutObject. Which combination of changes will fix both problems? (Select TWO.)

- A) Grant s3:PutObject on the bucket to the task execution role, because that role is used for every AWS call made by a task.
- B) Grant s3:PutObject on the bucket to the task role that is referenced by taskRoleArn in the task definition.
- C) Grant both permissions to the ECS service-linked role, because Fargate uses that role instead of task roles for all calls.
- D) Grant secretsmanager:GetSecretValue on the secret to the task role, because the application container reads it at startup.
- E) Grant secretsmanager:GetSecretValue on the secret to the task execution role that is referenced by executionRoleArn.

**22.** *(Domain 4)* After a code change, an Amazon API Gateway REST API that uses a Lambda proxy integration returns HTTP 502 for every request. The Lambda function's CloudWatch logs show that each invocation finishes successfully and returns an object with a status field set to 200 and a data field that contains the results. What is the most likely cause?

- A) The API's usage plan throttle limit is being exceeded, so API Gateway rejects the requests with a bad gateway error for each client.
- B) The function's response does not match the proxy integration format, which requires a statusCode field and a body field that contains a string.
- C) The function's execution role lacks permission to call API Gateway, so the response cannot be written back to the client.
- D) The function exceeds the API Gateway integration timeout of 29 seconds for each request, so API Gateway returns a bad gateway error to the client.

**23.** *(Domain 2)* A developer can create AWS Lambda functions but receives an AccessDenied error when running aws lambda create-function with --role set to an existing execution role named OrdersFunctionRole. The developer can already list and read that role. The security team wants to grant the minimum additional permission. Which permission should be added to the developer's IAM policy?

- A) iam:CreateRole and iam:PutRolePolicy on the ARN of OrdersFunctionRole so that the developer can re-create the role while the function is being created
- B) iam:AttachRolePolicy on the ARN of OrdersFunctionRole so that the developer can attach the AWSLambdaBasicExecutionRole policy to it
- C) sts:AssumeRole on the ARN of OrdersFunctionRole so that the developer can assume the role before calling the create-function API
- D) iam:PassRole on the ARN of OrdersFunctionRole, optionally restricted with a condition that iam:PassedToService equals lambda.amazonaws.com

**24.** *(Domain 2)* A company stores the credentials for an Amazon RDS for MySQL DB instance in AWS Secrets Manager and enabled automatic rotation with the AWS-provided rotation function, which runs in the database's VPC. The private subnets have no NAT gateway. Rotation keeps failing with a timeout because the function cannot reach Secrets Manager. The company must not allow internet access from the VPC. Which solution will fix the rotation?

- A) Move the secret to AWS Systems Manager Parameter Store as a SecureString, which rotates automatically without needing any network access.
- B) Move the rotation function out of the VPC so that it can reach Secrets Manager through its public endpoint while still connecting to the private database.
- C) Create a gateway VPC endpoint for Secrets Manager, and add it to the private subnets' route tables so that the rotation function can reach the service.
- D) Create an interface VPC endpoint for Secrets Manager in the VPC, and allow HTTPS from the rotation function's security group to the endpoint's security group.

**25.** *(Domain 3)* A developer must update a production AWS CloudFormation stack that contains an Amazon DynamoDB table and several Lambda functions. The developer is unsure whether the template change will replace the table, which would delete its data, and wants to know exactly which resources will be modified or replaced before anything in production changes. What should the developer do?

- A) Deploy the updated template as a new stack in production first, compare the resources of both stacks, and then delete the old stack if the new one looks correct.
- B) Update the stack with rollback disabled so that the developer can inspect any replaced resources afterwards and restore them manually if something went wrong.
- C) Create a change set for the update, check the Replacement value for each resource in the change set, and execute the change set only if the table is not being replaced.
- D) Run drift detection on the stack, which reports which resources the pending template change will modify or replace before the update is actually applied to production.

**26.** *(Domain 1)* A company exposes a report-generation endpoint through an Amazon API Gateway REST API with a Lambda proxy integration. Some reports take up to 4 minutes to build. Clients receive HTTP 504 errors for those requests, even though the Lambda function completes successfully within its 5-minute timeout. The company wants clients to get a response immediately and download the finished report later. Which solution will meet these requirements with the LEAST operational overhead?

- A) Return 202 with a job ID after queuing the request in Amazon SQS, have a Lambda function build the report into Amazon S3, and add a status endpoint that returns a presigned URL.
- B) Raise the method's integration timeout to 300 seconds in the integration request settings so that the synchronous Lambda proxy integration can wait for every report to finish before responding.
- C) Replace the REST API with an HTTP API, which supports integration timeouts of up to 15 minutes for Lambda proxy integrations, and keep the synchronous request design.
- D) Move report generation to Amazon EC2 instances behind an Application Load Balancer with a 300-second idle timeout, and point clients at the load balancer's DNS name.

**27.** *(Domain 1)* A retail application running on AWS Lambda reads product records from an Amazon DynamoDB table by key millions of times per hour, and catalog read latency must drop from milliseconds to microseconds. The team uses the AWS SDK's DynamoDB client and wants the fewest code changes. Checkout reads must always return the latest committed value. Which solution will meet these requirements?

- A) Switch the table to on-demand capacity mode, which automatically caches frequently read items in memory and returns them with microsecond latency.
- B) Add an Amazon ElastiCache (Memcached) cluster, rewrite the data access layer to implement lazy loading, and read checkout data from the cache with a 1-second TTL so that it is almost never stale.
- C) Enable DynamoDB global tables in a second Region and route all read traffic to the replica table, which serves reads from memory with microsecond latency.
- D) Add a DynamoDB Accelerator (DAX) cluster, switch catalog reads to the DAX client, and keep checkout reads as strongly consistent requests, which DAX passes through to DynamoDB.

**28.** *(Domain 1)* An e-commerce platform publishes order events to an Amazon SNS topic that has three Amazon SQS queue subscriptions, one per microservice. The shipping service needs only events whose order_status message attribute is SHIPPED, but it currently receives every event and discards 95% of them, which adds cost. The queues must also keep messages safely if a service is down for several hours. Which combination of actions will meet these requirements? (Select TWO.)

- A) Add a subscription filter policy to the shipping queue's subscription that matches messages whose order_status attribute equals SHIPPED.
- B) Add filtering logic to the shipping consumer so that it deletes messages that are not SHIPPED immediately after receiving them from the queue.
- C) Create a separate SNS topic for each order status and change the publisher to send every event to all of the topics at the same time.
- D) Replace the SQS subscriptions with HTTPS subscriptions to each service so that SNS keeps retrying delivery until the service recovers.
- E) Keep each service's SQS queue subscribed to the topic, and set each queue's message retention period long enough to cover the expected downtime.

**29.** *(Domain 3)* A REST API in Amazon API Gateway has dev and prod stages. Each stage must invoke a different alias of the same Lambda function through a single integration definition. After the developer sets the integration's function ARN to end with :${stageVariables.alias}, calls to the prod stage fail with an 'Invalid permissions on Lambda function' error. Which combination of steps will fix the problem and meet the requirements? (Select TWO.)

- A) Define a stage variable named alias with the value prod on the prod stage and the value dev on the dev stage.
- B) Run aws lambda add-permission for each alias so that API Gateway is allowed to invoke that qualified alias ARN.
- C) Enable Lambda proxy integration on the method so that API Gateway grants itself permission to invoke every alias.
- D) Create a usage plan for each stage and associate the matching Lambda alias with it so that the alias is resolved.
- E) Redeploy the API to the dev stage only, because stage variables are resolved when the API is deployed, not per request.

**30.** *(Domain 3)* An AWS CodeBuild project builds a Node.js application. Builds take 12 minutes, mostly spent downloading the same npm dependencies, and buildspec.yml contains an npm registry token in plaintext under env: variables. The team wants faster builds and wants to remove the plaintext token without changing the build steps. Which combination of changes will meet these requirements? (Select TWO.)

- A) Commit the node_modules directory to the source repository so that CodeBuild no longer needs to download any dependencies during the builds.
- B) Enable caching for the project (Amazon S3 or local cache), and list the npm cache or node_modules directory under the cache: paths section of buildspec.yml.
- C) Store the token in AWS Secrets Manager, reference it in buildspec.yml under env: secrets-manager, and allow the CodeBuild service role to read that secret.
- D) Move the token into the CodeBuild project settings as a PLAINTEXT environment variable, because CodeBuild encrypts project settings at rest by default.
- E) Change the project to the largest available compute type so that the npm dependency downloads finish faster during the install phase of each build.

**31.** *(Domain 2)* An AWS Lambda function reads a database password from an environment variable. A security review finds that any IAM user who can view the function's configuration in the Lambda console can read the password in plaintext. The company must keep using an environment variable and must ensure that only principals who can use a specific KMS key can read the value. Which solution will meet these requirements?

- A) Rename the variable so that it starts with SECRET_, which makes the Lambda console mask the value for users who do not have the lambda:GetFunction permission.
- B) Rely on the default at-rest encryption that Lambda applies to environment variables with the AWS managed aws/lambda key, which already hides the value from console users.
- C) Encrypt the value with a customer managed KMS key using the console's encryption helpers, and call kms:Decrypt in the function's initialization code with the execution role.
- D) Store the password in an encrypted file inside the deployment package, and decrypt the file with a key that is included in the same deployment package.

**32.** *(Domain 1)* A data science team is deploying a Python AWS Lambda function that depends on machine learning libraries totaling 1.8 GB unzipped. Deployment as a .zip file fails. The team wants to keep using Lambda, keep deployments repeatable through its CI pipeline, and avoid managing any servers. Which solution will meet these requirements?

- A) Configure 10,240 MB of ephemeral storage and have the function download all of the libraries into /tmp from Amazon S3 on every invocation.
- B) Split the libraries across five Lambda layers of about 360 MB each and attach all five layers to the function so that the total size fits.
- C) Upload the .zip file to Amazon S3 and create the function from the S3 object, which raises the unzipped deployment size limit to 10 GB.
- D) Package the function and its libraries as a container image, push the image to Amazon ECR, and create the function from that container image.

**33.** *(Domain 1)* A company must run a cleanup AWS Lambda function every weekday at 02:00 UTC and must start an AWS Step Functions workflow whenever any Amazon EC2 instance in the account enters the stopped state. The developer wants to avoid running any servers or writing polling code. Which solution will meet these requirements?

- A) Create an Amazon CloudWatch alarm on the StatusCheckFailed metric for every instance that starts the state machine, and a second alarm with a 24-hour evaluation period that invokes the Lambda function at 02:00 UTC.
- B) Create an Amazon SNS topic that EC2 publishes state changes to automatically, subscribe the state machine to it, and use a delivery delay to run the Lambda function each night.
- C) Use an EventBridge Scheduler cron schedule to invoke the Lambda function, and an EventBridge rule on the default bus that matches EC2 state-change events for stopped and targets the state machine.
- D) Create an AWS Config rule that detects stopped instances and starts the state machine, and add a crontab entry on a small EC2 instance to invoke the Lambda function each weekday.

**34.** *(Domain 1)* A developer is adding Amazon ElastiCache (Redis OSS) in front of an Amazon RDS database for a product catalog. Product prices change a few times per day and must never be shown stale for more than a few seconds after an update. Most products are rarely viewed, and the cache must stay as small as possible. Which caching approach meets these requirements?

- A) Use lazy loading to populate the cache on reads, update or delete the cached item in the same code path that writes a price change to the database, and set a TTL on every key.
- B) Load every product into the cache at startup with write-through caching and no TTL so that the cache always contains the full catalog with the current prices.
- C) Use lazy loading only, with a 24-hour TTL on every key, so that rarely viewed products are evicted automatically and the cache memory footprint stays as small as possible.
- D) Use write-through caching only, with a 24-hour TTL, so that every price change reaches the cache and products that are never updated are always read from the database.

**35.** *(Domain 2)* A SaaS monitoring vendor needs read-only access to Amazon CloudWatch metrics in a customer's AWS account. The customer wants to avoid sharing long-term credentials and wants to make sure that another customer of the same vendor cannot trick the vendor into accessing this customer's account. Which solution will meet these requirements?

- A) Create an IAM role with read-only permissions and a trust policy that allows the vendor's AWS account to assume it only when the sts:ExternalId value matches a unique ID from the vendor.
- B) Create an IAM role with read-only permissions and a trust policy that allows any AWS principal to assume it as long as the aws:SecureTransport condition key is true for every request.
- C) Create a resource-based policy on the CloudWatch metrics that allows the vendor's account to call GetMetricData, and require MFA for every request made by the vendor.
- D) Create an IAM user with read-only permissions, generate an access key, and send the key to the vendor through encrypted email so that it can store the key in a secrets manager.

**36.** *(Domain 4)* A high-traffic AWS Lambda function calls the Amazon CloudWatch PutMetricData API on every invocation to publish a checkout latency metric with a dimension for the payment provider. These calls add latency and are occasionally throttled. The team wants to keep the same custom metric and dimension but remove the metric API calls from the request path. Which solution will meet these requirements?

- A) Write the metric to stdout in CloudWatch embedded metric format (EMF), which CloudWatch extracts into custom metrics asynchronously from the function's log events.
- B) Keep the metric values in the function's memory and call PutMetricData once when the execution environment is shut down after it has been idle for several minutes.
- C) Increase the function's memory setting so that the PutMetricData calls complete faster and are less likely to be throttled during traffic spikes.
- D) Enable Lambda Insights on the function, which automatically publishes custom business metrics such as checkout latency with custom dimensions.

**37.** *(Domain 3)* A developer uses AWS CodeDeploy for in-place deployments to Amazon EC2 instances. After the application starts, a script must confirm that the application responds correctly on port 8080 and must fail the deployment if the check fails. In which appspec.yml lifecycle event hook should this script run?

- A) AfterInstall
- B) ApplicationStart
- C) BeforeInstall
- D) ValidateService

**38.** *(Domain 1)* A gaming company stores match events in an Amazon DynamoDB table that uses provisioned capacity with auto scaling. The partition key is game_id, and a newly launched game now generates 90% of all writes. CloudWatch shows WriteThrottleEvents even though consumed write capacity is far below the table's provisioned capacity. The company must eliminate the throttling and still be able to retrieve all events for a single game. Which combination of steps will meet these requirements? (Select TWO.)

- A) Append a random suffix from a fixed range, such as 0 to 9, to the game_id value when writing each event so that writes for one game spread across partitions.
- B) Read all events for a game by issuing a Query for every suffix value in parallel and merging the results in the application before returning them.
- C) Switch the table to on-demand capacity mode, which removes the per-partition throughput limit for any single partition key value.
- D) Increase the table's provisioned write capacity to twice the current peak so that the partition holding the new game receives more throughput.
- E) Add a global secondary index with game_id as its partition key so that writes for the new game are distributed across the index's partitions.

**39.** *(Domain 4)* A developer instruments a Node.js order service with the AWS X-Ray SDK. Support engineers need to find every trace for a given customer ID and order ID in the X-Ray console when they investigate complaints, and they also want the full order payload attached to each trace for reference. Which approach should the developer use?

- A) Record the customer ID and order ID as annotations on the segment, and add the full order payload to the segment as metadata.
- B) Record the customer ID, the order ID and the order payload as metadata so that all three values can be used in filter expressions.
- C) Write the customer ID and order ID to CloudWatch Logs, and add the order payload to the trace header of each downstream call.
- D) Record the order payload as an annotation, and add the customer ID and the order ID as metadata on a custom subsegment.

**40.** *(Domain 2)* A public login API runs on an Amazon API Gateway REST API behind an Amazon CloudFront distribution. Attackers send thousands of credential-stuffing requests per minute from a changing set of IP addresses, and some requests contain SQL injection payloads. The company wants to block this traffic at the edge with managed protections and no custom code. Which solution will meet these requirements?

- A) Configure API Gateway usage plans with a low per-client throttle limit, and require an API key on the login method to block requests from unknown clients.
- B) Add security group rules to the API Gateway endpoint that deny the attacking IP ranges and allow only the IP addresses of known customers.
- C) Create an Amazon CloudWatch alarm on 4XXError that invokes a Lambda function to add each attacking IP address to a network ACL.
- D) Associate an AWS WAF web ACL with the CloudFront distribution that includes a rate-based rule keyed on source IP and the AWS managed SQL database rule group.

**41.** *(Domain 1)* A media company stores user-uploaded videos in Amazon S3 Standard. Each video is accessed frequently for 30 days, occasionally for the next 60 days, and almost never after that. Legal requirements state that every video must be retrievable within 12 hours for 7 years and can then be deleted. Objects average 400 MB. Which lifecycle configuration provides the lowest storage cost that meets these requirements?

- A) Transition objects to S3 One Zone-IA after 30 days, transition them to S3 Glacier Instant Retrieval after 90 days, and expire them after 7 years.
- B) Transition objects to S3 Standard-IA after 30 days, transition them to S3 Glacier Deep Archive after 90 days, and expire them after 7 years.
- C) Transition objects to S3 Glacier Flexible Retrieval after 30 days, transition them to S3 Glacier Deep Archive after 60 days, and expire them after 7 years.
- D) Transition objects to S3 Intelligent-Tiering after 30 days with the Deep Archive Access tier activated, and keep them without any expiration rule.

**42.** *(Domain 4)* A team runs microservices on Amazon ECS with AWS Fargate and wants end-to-end traces in AWS X-Ray, including downstream calls to Amazon DynamoDB. The services are instrumented with the X-Ray SDK, but no traces appear in the X-Ray console. Which combination of steps is required? (Select TWO.)

- A) Grant the task role permission for xray:PutTraceSegments and xray:PutTelemetryRecords, for example with the AWSXRayDaemonWriteAccess policy.
- B) Run the X-Ray daemon, or the AWS Distro for OpenTelemetry collector, as a sidecar container in each task definition listening on UDP port 2000.
- C) Enable VPC Flow Logs on the task subnets so that X-Ray can build the service map from the recorded network connections between the tasks.
- D) Grant the task execution role permission for xray:GetTraceSummaries so that the SDK can confirm that each trace was received by X-Ray.
- E) Turn on active tracing for each ECS service in the console, which installs the X-Ray daemon on the underlying Fargate hosts automatically.

**43.** *(Domain 3)* A team pushes a new container image to Amazon ECR on every commit, tags it with the Git commit SHA, and also moves a latest tag. The ECR storage bill keeps growing, and one deployment ran the wrong image because latest was overwritten during the rollout. The team wants to keep only the 30 most recent images automatically and make sure a deployed tag always points to the same image. Which solution will meet these requirements?

- A) Enable ECR cross-Region replication to a cheaper Region, and delete the images from the source repository after they have been replicated successfully.
- B) Write a nightly Lambda function that lists the images and deletes all but the newest 30, and add a pipeline step that pushes the latest tag again after every deployment has finished.
- C) Enable image scanning on push so that outdated images are flagged and removed, and keep deploying with the latest tag but pin the task definition revision instead.
- D) Add an ECR lifecycle policy that keeps the 30 most recent images and expires older ones, enable tag immutability on the repository, and deploy by the commit SHA tag instead of latest.

**44.** *(Domain 4)* An Amazon DynamoDB table in provisioned mode has plenty of unused write capacity, yet writes to the table are being throttled. The table has a global secondary index whose partition key is a status attribute with only three possible values, and the index has much lower provisioned write capacity than the table. Which explanation and fix are correct?

- A) Writes are throttled because the table's partition key is too random; change it to the status attribute so that related writes are grouped together.
- B) Base-table writes are throttled because DynamoDB Streams is enabled on the table; disable the stream until the write backlog on the table has cleared.
- C) Writes are throttled because provisioned tables support only one index; delete the GSI and use a Scan with a filter to find items by status instead.
- D) Base-table writes are throttled because the GSI cannot keep up; increase the GSI's write capacity and use a higher-cardinality partition key for the index.

**45.** *(Domain 1)* A developer attached an existing AWS Lambda function to two private subnets in a VPC so that it can query an Amazon RDS for PostgreSQL instance. After the change, database queries succeed, but every call the function makes to a third-party HTTPS API on the internet now fails with a timeout. The function's security group allows all outbound traffic. Which change will fix the issue?

- A) Create an interface VPC endpoint for the third-party API's domain name so that the traffic stays on the AWS network and never crosses the public internet.
- B) Add a route in the private subnets' route table that sends 0.0.0.0/0 traffic to a NAT gateway that is located in a public subnet with a route to an internet gateway.
- C) Assign an Elastic IP address to each of the function's elastic network interfaces so that the function can reach the internet directly from the private subnets.
- D) Move the function into public subnets that have a route to an internet gateway so that its network interfaces receive public IP addresses automatically.

**46.** *(Domain 3)* A developer wants to test an AWS Lambda function that is defined in an AWS SAM template on a laptop before deploying anything. The test must use a sample Amazon S3 put event, override the TABLE_NAME environment variable to point at a test table, and use the same runtime as production without creating the function in AWS. Which solution will meet these requirements?

- A) Run sam sync --watch against the production stack so that code changes are pushed within seconds and tested against the real S3 bucket's events.
- B) Run sam local generate-event s3 put to create an event file, then run sam local invoke with --event set to that file and --env-vars pointing to a JSON file that sets TABLE_NAME.
- C) Run sam deploy --guided into a sandbox account with a TABLE_NAME parameter override, and invoke the deployed function with the AWS CLI using a saved sample S3 put event file.
- D) Run sam build, and then upload the build output to the Lambda console's test feature together with a saved test event and edited environment variables.

**47.** *(Domain 2)* An AWS Lambda function in account 111111111111 must read objects from an Amazon S3 bucket in account 222222222222. The objects are encrypted with SSE-KMS using a customer managed key that account 222222222222 owns. The bucket policy already allows the function's role to read the objects, but GetObject calls fail with AccessDenied. Which combination of changes will resolve the issue? (Select TWO.)

- A) Update the KMS key policy in account 222222222222 to allow kms:Decrypt for the Lambda execution role's ARN in account 111111111111.
- B) Enable automatic rotation on the key in account 222222222222 so that account 111111111111 receives its own newly rotated key version.
- C) Add a statement to the S3 bucket policy in account 222222222222 that allows kms:Decrypt for the Lambda execution role in account 111111111111.
- D) Create a new KMS key in account 111111111111 and re-encrypt every object in the bucket in account 222222222222 with that new key.
- E) Update the Lambda execution role's IAM policy in account 111111111111 to allow kms:Decrypt on the ARN of the key in account 222222222222.

**48.** *(Domain 3)* An AWS CloudFormation stack manages an Amazon RDS DB instance that has DeletionPolicy: Snapshot. A developer changes a template property that requires the DB instance to be replaced. The team wants to be sure that a snapshot of the old instance is always taken when CloudFormation replaces it during this or any future update. What should the developer add to the DB instance resource?

- A) DeletionPolicy: Retain, because Retain also applies to resources that are replaced during a stack update and keeps the old instance running.
- B) UpdateReplacePolicy: Snapshot, because DeletionPolicy applies only when the resource is removed from the template or the whole stack is deleted.
- C) A stack policy that denies Update:Replace on the DB instance, because a stack policy takes a snapshot automatically before it blocks the update.
- D) Nothing, because the existing DeletionPolicy: Snapshot already creates a snapshot whenever the resource is replaced during a stack update.

**49.** *(Domain 2)* A development team needs to store 150 configuration values for several microservices, organized by environment paths such as /prod/orders/timeout. About 10 of the values are third-party API keys that must be encrypted at rest; they are rotated manually once a year. The team wants the lowest cost and must be able to load all values for one service with a single API call. Which solution will meet these requirements?

- A) Store all values in one encrypted JSON object in Amazon S3, and give every service an IAM policy that allows reading the entire object at startup.
- B) Store the plain values in Parameter Store and the API keys in Secrets Manager with automatic rotation configured on a 365-day schedule for each key.
- C) Store all values as individual secrets in AWS Secrets Manager, and load them for each service at startup with the BatchGetSecretValue API operation.
- D) Store all values in Parameter Store standard tier, use SecureString parameters for the API keys, and load each service's values with GetParametersByPath.

**50.** *(Domain 3)* A team deploys an AWS Lambda function with AWS SAM. Each deployment must shift 10% of production traffic to the new version for 5 minutes, automatically roll back if the function's error-rate alarm goes off during that time, and run a validation function before any traffic shifts. Which combination of changes to the SAM template will meet these requirements? (Select TWO.)

- A) Add a DeploymentPreference with Type: Linear10PercentEvery5Minutes, and configure the validation function as a PostTraffic hook for the alarm.
- B) Add an AWS::CodePipeline::Pipeline resource with a manual approval action that watches the error-rate alarm during every deployment.
- C) Add a DeploymentPreference with Type: Canary10Percent5Minutes, the error-rate alarm under Alarms, and the validation function under Hooks as PreTraffic.
- D) Add AutoPublishAlias: live to the function resource so that SAM publishes a new version and moves the alias to it on each deployment.
- E) Add ProvisionedConcurrencyConfig to the function so that CodeDeploy keeps the previous version warm and can roll back to it instantly.

**51.** *(Domain 3)* A networking stack exports a VPC ID with an Outputs Export name, and five application stacks import it with Fn::ImportValue. A developer tries to update the networking stack to change the export name and receives an error that the export cannot be updated because it is in use. The developer must rename the export without deleting any application stacks. What should the developer do?

- A) Run aws cloudformation update-stack with the --force option so that the networking stack overrides the imports that the five dependent application stacks are currently using.
- B) Add the new export name alongside the old one, update each application stack to import the new name, and then remove the old export from the networking stack.
- C) Convert the networking stack into a nested stack of each application stack so that the export can be renamed in a single stack deployment.
- D) Enable termination protection on the application stacks, which allows the networking stack to rename exports that those stacks import safely.

**52.** *(Domain 4)* A developer needs the 10 slowest requests from the last hour in an AWS Lambda function's log group. The function writes structured JSON logs that include a durationMs field and a requestId field for every request. Which CloudWatch Logs Insights query returns this result?

- A) filter durationMs > 10 | fields requestId | sort requestId asc | limit 10
- B) fields requestId, durationMs | sort durationMs desc | limit 10
- C) fields requestId, durationMs | stats max(durationMs) by requestId | limit 10
- D) fields requestId | parse @message "durationMs" as duration | sort duration asc | limit 10

**53.** *(Domain 4)* Consumers running on Amazon EC2 poll an Amazon SQS queue in a tight loop. CloudWatch shows millions of ReceiveMessage calls per day, and most of them return no messages, which drives up cost. Messages must still be processed within a few seconds of arriving. Which change will reduce cost the most while meeting the latency requirement?

- A) Set the queue's DelaySeconds to 60 so that messages become available in larger groups and each poll returns more of them.
- B) Add a 60-second sleep between polls in each consumer so that the number of empty responses drops by roughly 60 times.
- C) Set ReceiveMessageWaitTimeSeconds to 20 on the queue or on each ReceiveMessage call so that the consumers use long polling.
- D) Increase the visibility timeout to 12 hours so that each message is received once and the number of ReceiveMessage calls drops.

**54.** *(Domain 1)* An AWS Lambda function processes records from an Amazon Kinesis data stream that has 4 shards. One malformed record causes the function to throw an error every time it is processed. Processing for that shard has stopped for several hours while the other shards continue, and the IteratorAge metric keeps growing. The team wants the shard to keep flowing and wants a record of the failed data for later investigation. Which solution will meet these requirements with the LEAST operational effort?

- A) Add a second Lambda function that reads the same shard through enhanced fan-out and deletes the malformed record from the stream as soon as it detects the processing error.
- B) Configure a dead-letter queue in the function's asynchronous invocation settings so that failed Kinesis records are sent to an Amazon SQS queue after two automatic retries.
- C) Configure the event source mapping with BisectBatchOnFunctionError enabled, a MaximumRetryAttempts value, and an on-failure destination that sends details of the failed batch to an Amazon SQS queue.
- D) Increase the ParallelizationFactor of the event source mapping to 10 so that the other records in the shard are processed by additional concurrent executions while the malformed record keeps retrying in the background.

**55.** *(Domain 2)* A containerized backend that is not behind Amazon API Gateway receives Amazon Cognito user pool access tokens from a single-page application in the Authorization header. A security review requires the backend to reject forged, expired, and wrong-app tokens without calling Cognito on every request. Which approach will meet these requirements?

- A) Decrypt each token with the user pool's KMS key by calling kms:Decrypt, and accept the request whenever that decryption call completes successfully.
- B) Base64-decode the token payload and accept the request when the email claim in the payload matches a registered user in the application's own database.
- C) Call the Cognito GetUser API with the access token for every request, and accept the request whenever that call returns the user's attributes successfully.
- D) Verify each token's signature with the public keys from the user pool's JWKS endpoint, cache those keys, and check the exp, iss, client_id and token_use claims.

**56.** *(Domain 4)* An AWS CodeDeploy in-place deployment to Amazon EC2 instances fails at the ApplicationStart lifecycle event on every instance. The application's own logs on the instances are empty because the application never starts. The developer needs the specific error output from the start script to find the root cause. Where should the developer look first?

- A) In the VPC Flow Logs for the instances' subnets, which show whether the application began listening on its port during the ApplicationStart event.
- B) In the Elastic Load Balancing access logs for the target group, which record the error returned by the start script when the first health check fails.
- C) In the deployment's lifecycle event details in the CodeDeploy console and in the CodeDeploy agent logs on an instance, which capture the output of the hook script.
- D) In the CloudTrail event history for the deployment group, which records the stdout and stderr of every lifecycle hook script that CodeDeploy runs on each instance.

**57.** *(Domain 3)* A pipeline in AWS CodePipeline deploys to a staging environment and then to production. The release manager must review the staging test report and explicitly approve each release before the production deployment starts, and must be notified automatically when a release is waiting. Which solution will meet these requirements with the LEAST effort?

- A) Add a manual approval action between the staging and production stages, configure it with an Amazon SNS topic that the release manager subscribes to, and set the test report link as its review URL.
- B) Split the pipeline into two pipelines, and have the release manager start the production pipeline manually after reading an email that a Lambda function sends through Amazon SES when the staging deployment finishes.
- C) Configure the production CodeDeploy deployment group to require a manual approval for every instance before CodeDeploy installs the new revision on that instance.
- D) Add an AWS CodeBuild action that runs a sleep command for 24 hours between the stages so that the release manager has enough time to review the staging environment.

**58.** *(Domain 2)* A developer's CI job calls ec2:RunInstances and fails with an UnauthorizedOperation error that contains an encoded authorization failure message. The developer needs to see which policy and condition caused the denial without guessing. What should the developer do?

- A) Call aws sts decode-authorization-message with the encoded message, using credentials that are allowed to perform the sts:DecodeAuthorizationMessage action.
- B) Search AWS CloudTrail Lake for the encoded message, which automatically returns the full evaluated policy for any request that failed authorization.
- C) Turn on IAM Access Analyzer policy validation for the CI role, which replaces encoded authorization messages with plaintext errors in later responses.
- D) Base64-decode the message locally with a standard command-line tool, because the encoded message is simply the Base64 text of the evaluated policy document and its condition keys.

**59.** *(Domain 1)* A customer-facing API runs on Amazon API Gateway and AWS Lambda. The functions use Java and load a large dependency-injection framework at startup, so P99 latency spikes to 6 seconds every morning when traffic ramps up from almost zero. Traffic follows a predictable daily schedule. The company must guarantee that up to 200 concurrent requests are served by already-initialized execution environments, at the lowest cost that meets this requirement. Which solution will meet these requirements?

- A) Increase the function's memory from 1,024 MB to 10,240 MB so that initialization completes faster, and leave provisioned concurrency disabled to avoid extra charges.
- B) Configure provisioned concurrency of 200 on the production alias, and use Application Auto Scaling scheduled actions to raise it before the morning ramp and lower it at night.
- C) Create an Amazon EventBridge rule that invokes the function every minute with a test event so that at least 200 execution environments always stay warm.
- D) Configure reserved concurrency of 200 on the function so that Lambda keeps 200 execution environments initialized and ready before the morning traffic arrives each day, at no extra charge.

**60.** *(Domain 4)* A developer created a CloudWatch Logs metric filter today that counts log events containing ERROR in an application's log group, and created an alarm on the resulting metric. The developer expected the metric graph to show last week's error spike, but the metric has data only from the time the filter was created. The developer still needs to investigate last week's errors. What should the developer do?

- A) Increase the metric's resolution to 1 second so that CloudWatch reads historical log events at a higher frequency and fills in last week's data.
- B) Query last week's log events directly with CloudWatch Logs Insights, because metric filters only evaluate log events that arrive after the filter is created.
- C) Delete and re-create the metric filter with its backfill option turned on so that CloudWatch reprocesses the log group's existing events into the metric.
- D) Change the metric filter's default value to 0, which causes CloudWatch to recalculate the metric from all of the existing log events in the log group.

**61.** *(Domain 1)* A company processes customer payments with an AWS Lambda function that is triggered by an Amazon SQS standard queue. Each message contains an order ID and an amount, and the function calls a third-party payment API. During a recent traffic spike, several customers were charged twice for the same order, although the application logs show no function errors or timeouts. The company must prevent duplicate charges without reducing throughput. Which solution will meet these requirements?

- A) Convert the queue to an SQS FIFO queue with content-based deduplication enabled, and so that SQS discards repeated messages, and keep the Lambda function's batch size and concurrency settings unchanged.
- B) Record each order ID in an Amazon DynamoDB table with a conditional write before calling the payment API, and skip the charge when the conditional write fails because the ID already exists.
- C) Configure a dead-letter queue with a maxReceiveCount of 1 so that any message that is received more than once is moved out of the source queue automatically.
- D) Increase the queue's visibility timeout to six times the function timeout so that messages are not delivered to a second consumer while they are still being processed.

**62.** *(Domain 2)* A compliance team requires that all requests to an Amazon S3 bucket use TLS and that every new object be encrypted with a specific customer managed KMS key, even when an application does not send any encryption headers. Which combination of actions will meet these requirements with the LEAST ongoing effort? (Select TWO.)

- A) Set the bucket's default encryption to SSE-KMS with the customer managed key so that uploads without encryption headers are encrypted with that key.
- B) Enable S3 Object Lock in compliance mode so that the bucket rejects any object that is uploaded without being encrypted by a KMS key.
- C) Enable S3 Transfer Acceleration on the bucket, because accelerated endpoints accept client connections only over TLS 1.2 or later.
- D) Add a bucket policy statement that denies all s3:* actions on the bucket and its objects when the aws:SecureTransport condition key is false.
- E) Add a Lambda function triggered by s3:ObjectCreated events that re-uploads each new object with SSE-KMS encryption using the customer managed key.

**63.** *(Domain 4)* An account runs many AWS Lambda functions. During a marketing event, a critical order-processing function that API Gateway invokes synchronously starts returning TooManyRequestsException errors because a batch-analytics function has consumed most of the account's concurrency. The company must guarantee capacity for the order function and stop the analytics function from starving other functions, without changing the analytics code. Which combination of actions will meet these requirements? (Select TWO.)

- A) Configure provisioned concurrency on the batch-analytics function so that its invocations no longer count toward the account quota.
- B) Set the order function's asynchronous maximum retry attempts to 2 so that throttled API Gateway requests are retried automatically.
- C) Configure reserved concurrency on the order-processing function that is equal to its expected peak concurrency.
- D) Configure reserved concurrency on the batch-analytics function to cap the number of execution environments it can use.
- E) Increase the timeout of the order-processing function to 15 minutes so that throttled requests wait for capacity to free up.

**64.** *(Domain 1)* A company is automating employee onboarding. After an HR system creates an account, a manager must approve the equipment request in an internal web app, which can take up to 5 days. The workflow must then call three AWS services in sequence, retry failed calls, and give the HR team a visual history of every execution. Which solution will meet these requirements with the LEAST custom code?

- A) Use an Amazon SQS queue for approval requests, have a Lambda function poll the queue every hour for approved requests, and call the three services from that function.
- B) Use Amazon EventBridge rules that react to each step's completion event and invoke the next Lambda function, and store each approval status in an Amazon DynamoDB table.
- C) Use a Step Functions Standard workflow with a .waitForTaskToken task that the web app completes by calling SendTaskSuccess after approval, and add Retry fields to each service task.
- D) Use an AWS Step Functions Express workflow with a Wait state set to 5 days, followed by three Task states that call the services, and add Catch fields and CloudWatch Logs logging to handle and record any failed calls.

**65.** *(Domain 3)* A company runs a production web application on AWS Elastic Beanstalk with 10 instances. For every release, the environment must keep serving traffic at full capacity during the deployment, and a failed deployment must roll back quickly without redeploying the previous version to the existing instances. Which deployment policy meets these requirements?

- A) Immutable, because it deploys the new version to a fresh set of instances in a temporary Auto Scaling group and terminates them if the deployment fails.
- B) All at once, because it deploys to every instance at the same time, which is the fastest way to replace a failed version with the previous one.
- C) Rolling, because it updates one batch at a time and keeps the remaining batches in service until each updated batch passes its health checks.
- D) Rolling with additional batch, because it launches an extra batch of instances first so that full capacity is maintained throughout the deployment.

---

## Answer Key & Explanations

1. **C** — When a method lists OAuth scopes, the Cognito authorizer checks the scopes in an access token, and ID tokens don't carry them. Calling AdminGetUser on every request adds latency and checks groups, not scopes. API keys only identify and throttle clients; they don't authorize.

2. **C** — Every account/Region needs a one-time cdk bootstrap, which creates the CDKToolkit stack (asset bucket, ECR repository, deployment roles). synth only produces the template locally, and the other options don't create the required bootstrap resources.

3. **C** — By default a task's result replaces the state's entire input. ResultPath places the result under a key and keeps the original input. OutputPath and InputPath filter data, so they can't bring the input back. ResultSelector's $ refers to the task result, not the state input.

4. **B** — Async destinations handle both outcomes with no code, and the failure record includes the request payload plus the error message, type and stack trace. A DLQ captures only failures, with just the original event, so success publishing still needs code. A try/catch runs on every attempt, not once after the final retry.

5. **B** — AppSync handles real-time subscriptions, a single GraphQL request across several data sources, and offline sync through the client libraries, with no connection management on your side. A WebSocket API means managing connection state yourself. Polling isn't real time. EC2 adds infrastructure to manage.

6. **C** — AppConfig delivers configuration separately from code, rolls it out gradually with a deployment strategy, and rolls back automatically on a CloudWatch alarm. The Lambda extension caches the flag for the functions. Changing an environment variable publishes a new version, which breaks the requirement. The other options need custom or manual work.

7. **C, E** — Partial batch responses need both pieces: ReportBatchItemFailures turned on in the event source mapping, and the function returning batchItemFailures with the failed messageIds. Setting visibility to 0 makes the messages visible again immediately, which is the opposite of deleting them. Long polling doesn't change how failures are handled. Destinations don't delete successful messages from the queue.

8. **B, E** — Envelope encryption: a new data key for each file, encryption done locally, and the encrypted data key stored with the object and decrypted by KMS when needed. KMS Encrypt accepts at most 4 KB. SSE-KMS encrypts on the server, so plaintext leaves the app. KMS key material can't be exported.

9. **A** — GSIs support only eventually consistent reads (a strongly consistent GSI query is rejected). Querying the base table by a customer_id partition key with ConsistentRead guarantees read-after-write and stays efficient. Waiting for the stream record doesn't make the GSI consistent. A Scan is correct but doesn't stay efficient at hundreds of millions of items.

10. **C, E** — The user pool handles email/password and Google sign-in. The identity pool exchanges the user pool token for temporary AWS credentials, and the policy variable limits each user to their own prefix. S3 doesn't accept Cognito JWTs as credentials or principals. Per-user IAM users and unvalidated tokens are both insecure.

11. **C** — A presigned URL is valid only as long as the credentials that signed it. An execution role's session credentials expire after a few hours, so the URL breaks early even though its own expiration is 24 hours. Neither the Lambda limit nor the key-rotation behaviour described exists.

12. **D** — Object-level S3 operations are data events, which trails don't log unless you turn them on. Event history shows management events only. Flow logs record network traffic, not API calls, and there's no 30-day delay.

13. **A** — Bucket Keys cut KMS calls (and cost) by up to 99% while still using the customer managed key. SSE-S3 breaks the requirement. A quota increase and backoff address the errors but not the cost. Spreading across many keys adds complexity without fixing the cost.

14. **A** — Exponential backoff with jitter spreads retries out so they don't hit the service at the same moment, and the SDK's retry modes do this with no custom code. Fixed delays make clients retry in sync, and more immediate retries add load. Dropping retries means manual work.

15. **A** — Published versions can't be changed, and an alias is a movable pointer to a version. API Gateway integrates once with the alias, and promotion or rollback is just an alias update. $LATEST changes with every deployment, and the other options change the integration or DNS on every release.

16. **B** — Worker environments run the SQS polling daemon for you and support periodic tasks through cron.yaml, and the work stays off the web tier. Background threads compete with web requests, and a crontab added through .ebextensions runs on every instance. A self-managed EC2 instance adds infrastructure to manage.

17. **C** — CloudFront uses only ACM certificates from us-east-1 (N. Virginia). ACM has no cross-Region replication, free public ACM certificates can't be exported, and CloudFront doesn't pass the origin's certificate on to viewers.

18. **D** — Reads: 7 KB rounds up to 8 KB, which is 2 RCU per strongly consistent read, and 80 × 2 = 160 RCU. Writes: 1.5 KB rounds up to 2 KB, which is 2 WCU per write, and 40 × 2 = 80 WCU. The other options forget to round item sizes up to the next 4 KB (reads) or 1 KB (writes) boundary.

19. **D** — Data protection policies mask matching data in log events with no code changes, and only principals with logs:Unmask can see the original values. A metric filter only detects the data. Short retention still exposes it. KMS encryption of a log group is transparent to readers: people without decrypt rights see nothing at all, not a masked version.

20. **A** — Only Kinesis Data Streams gives several independent consumers, sub-second processing and replay within the retention window, and Firehose can read from the stream to archive it. SQS deletes messages once they are consumed, so they can't be re-read. Firehose-to-S3 buffering can't deliver per-event results within one second.

21. **B, E** — The execution role is what ECS uses to pull the image, send logs and fetch the secrets injected into the task definition, which is why the tasks failed to start. The task role is the identity your application code uses for runtime calls such as S3 PutObject.

22. **B** — Lambda proxy integrations must return statusCode, headers and a string body. Any other shape makes API Gateway return 502. Timeouts return 504, throttling returns 429, and functions don't need permission to return responses.

23. **D** — Giving a role to an AWS service (Lambda, EC2, ECS) requires iam:PassRole on that role, and iam:PassedToService narrows it further. The developer doesn't need to assume, create or modify the role.

24. **D** — The rotation function needs a private path to the Secrets Manager API, which an interface endpoint (PrivateLink) provides. Gateway endpoints exist only for S3 and DynamoDB. Outside the VPC, the function can't reach the private DB instance. Parameter Store has no built-in rotation.

25. **C** — A change set previews exactly what will be added, modified or replaced before you apply anything. Drift detection compares the live resources with the current template and says nothing about pending changes. The other options change production before you've checked.

26. **A** — API Gateway's integration timeout (29 seconds by default) causes the 504s. An asynchronous request/poll pattern answers immediately and needs no servers. The other options keep the client waiting synchronously, which breaks the 'respond immediately' requirement, and HTTP APIs max out at 30 seconds.

27. **D** — DAX is API-compatible with DynamoDB (few code changes) and serves eventually consistent reads in microseconds. It passes strongly consistent reads straight to DynamoDB, so checkout stays correct. Memcached means rewriting the data layer, and a 1-second TTL is still stale. Neither global tables nor on-demand mode is an in-memory cache.

28. **A, E** — A subscription filter policy drops non-matching messages before delivery, so you stop paying to deliver and process them. SQS queues buffer messages for up to 14 days while a consumer is down. Filtering in consumer code still pays for every delivery. HTTPS subscriptions have a limited retry policy and no durable buffer. Extra topics add work for the publisher.

29. **A, B** — A stage variable picks the alias for each stage. Because the function ARN is resolved at request time, API Gateway can't add invoke permission automatically, so you must add a resource-based permission for each alias ARN. Proxy integration doesn't grant permissions, usage plans don't resolve aliases, and stage variables are evaluated on every request.

30. **B, C** — The secrets-manager env type pulls the token at build time, so it never appears in plaintext. Build caching reuses downloaded dependencies across builds. A PLAINTEXT variable is still visible to anyone who can view the project. Bigger compute doesn't fix repeated downloads, and committing node_modules is poor practice.

31. **C** — The default encryption protects the value at rest, but anyone allowed to read the function's configuration still sees plaintext. Encrypting the value itself with a customer managed key (encryption helpers) and decrypting it in code limits access to principals who can use the key. There's no masking-by-name feature, and a key shipped in the package protects nothing.

32. **D** — Container images can be up to 10 GB. Zip deployments, including all layers, are limited to 250 MB unzipped no matter where they're uploaded from. Downloading 1.8 GB into /tmp on every invocation would be slow and wasteful.

33. **C** — EventBridge handles both: Scheduler for cron schedules, and rules that match the EC2 state-change events AWS publishes to the default event bus, with Step Functions as a target. Status-check alarms don't track instance state and can't run on a schedule. A crontab needs a server. EC2 doesn't publish state changes to SNS on its own.

34. **A** — Lazy loading caches only the products people actually read, which keeps the cache small. Updating or invalidating the key on every price write removes the staleness window, and the TTL is a safety net. Preloading everything wastes memory. Lazy loading alone can serve prices up to 24 hours stale. Write-through alone never caches read-heavy items that aren't updated.

35. **A** — A cross-account role with an ExternalId condition is the standard defence against the 'confused deputy' problem, and it uses no long-term credentials. Any-principal trust is dangerous, and CloudWatch metrics don't support resource-based policies.

36. **A** — With EMF, the function writes structured log lines, and CloudWatch turns them into custom metrics with dimensions, so the function makes no metric API calls. Buffering until shutdown loses data because shutdown isn't guaranteed. More memory keeps the calls, and Lambda Insights publishes system metrics, not your business metrics.

37. **D** — The EC2 hook order is ApplicationStop, BeforeInstall, AfterInstall, ApplicationStart, ValidateService. ValidateService runs after the application has started and is the hook meant for verifying the deployment. A script that fails there fails the deployment.

38. **A, B** — One hot key is limited by per-partition throughput (1,000 WCU per partition), whatever the table's total capacity. Write sharding with a suffix spreads the writes, and a parallel query per suffix reads them back. More capacity or on-demand mode doesn't lift the per-partition limit for a single key. A GSI on the same key would be just as hot and would throttle base-table writes.

39. **A** — Annotations are indexed key-value pairs that you can search with filter expressions. Metadata can hold whole objects but isn't indexed. So the IDs go in annotations and the payload goes in metadata.

40. **D** — AWS WAF on CloudFront blocks traffic at the edge: rate-based rules throttle abusive IPs even as they change, and the managed SQL database rule group blocks injection payloads. API keys aren't security controls, API Gateway has no security groups, and the alarm-plus-Lambda approach is custom code that reacts too slowly.

41. **B** — Standard-IA suits the occasional-access period, and Deep Archive is the cheapest class whose standard retrieval finishes within 12 hours. Expiring after 7 years avoids paying beyond the requirement. Glacier Instant Retrieval costs more than Deep Archive, and One Zone-IA weakens resilience. Glacier Flexible Retrieval at day 30 makes the occasional-access period slow and adds retrieval fees. Keeping objects forever costs more than necessary.

42. **A, B** — On Fargate you must run the daemon (or the ADOT collector) yourself as a sidecar, and the task role needs permission to send segments. ECS has no active-tracing toggle, X-Ray doesn't read flow logs, and GetTraceSummaries is a read API the SDK doesn't use.

43. **D** — A lifecycle policy expires old images with no code. Immutable tags and deploying by commit SHA guarantee a tag always means the same image. A custom cleanup function is more work, scanning finds vulnerabilities rather than deleting images, and replication adds storage instead of reducing it.

44. **D** — When a GSI runs out of write capacity (made worse by a hot, low-cardinality index key), DynamoDB throttles writes to the base table. Give the index enough capacity and a well-distributed key. Streams don't throttle writes, and tables can have up to 20 GSIs.

45. **B** — A VPC-attached Lambda function has no public IP address, even in a public subnet, so it needs a NAT gateway for outbound internet access. You can't attach Elastic IPs to Lambda-managed ENIs. Interface endpoints serve AWS and PrivateLink services, not arbitrary internet APIs.

46. **B** — sam local invoke runs the function in a local container that uses the production runtime image, with a generated sample event and environment-variable overrides from a JSON file. The other options deploy the function to AWS, and one of them touches production.

47. **A, E** — Cross-account KMS use needs both sides: the key policy in the owning account must allow the external principal, and that principal's IAM policy must allow the action on the key. A bucket policy can't grant KMS permissions. Rotation and re-encryption are unrelated to this error.

48. **B** — Replacement during an update is controlled by UpdateReplacePolicy. DeletionPolicy covers only deletion of the resource or the stack. A stack policy can block the update but never takes a snapshot.

49. **D** — Parameter Store standard tier is free, supports path hierarchies and KMS-encrypted SecureStrings, and GetParametersByPath loads a whole path in one call. 150 Secrets Manager secrets cost money every month, and rotation isn't needed here. A single S3 object gives every service access to every value, which breaks least privilege.

50. **C, D** — SAM's traffic shifting runs through CodeDeploy. It needs AutoPublishAlias, plus a DeploymentPreference with the canary type, the rollback alarm, and a PreTraffic hook that runs validation before any traffic shifts. Linear10PercentEvery5Minutes is a different traffic shape, and a PostTraffic hook runs too late. The other options don't provide canary rollback.

51. **B** — CloudFormation won't change or delete an export that another stack imports. Migrate step by step: add the new export, move each importing stack over to it, then remove the old one. update-stack has no --force option, and termination protection is unrelated.

52. **B** — Logs Insights automatically discovers JSON fields. Sorting by durationMs in descending order and limiting to 10 gives the slowest requests. The stats query without a sort returns an arbitrary 10 rows, and the others sort the wrong field or in the wrong direction.

53. **C** — Long polling waits up to 20 seconds for a message and returns as soon as one arrives, which removes most empty responses without adding delay. A delay queue or a sleep adds up to 60 seconds of latency. The visibility timeout doesn't change how often consumers poll.

54. **C** — With stream sources, Lambda retries a failing batch until the record expires, which blocks the shard. Bisecting the batch, limiting retries and adding an on-failure destination (which receives the shard ID and sequence numbers of the failed records) unblocks the shard. The async DLQ setting doesn't apply to event source mappings. A higher ParallelizationFactor still retries the failing partition key forever. You can't delete individual records from a Kinesis stream.

55. **D** — Cognito tokens are signed JWTs. Checking the signature against the cached JWKS public keys and then checking the expiry, issuer, client and token-use claims validates them locally. Decoding without checking the signature accepts forged tokens. GetUser works but calls Cognito on every request. The tokens are signed, not KMS-encrypted.

56. **C** — CodeDeploy captures each hook script's output in the lifecycle event details and in the agent's deployment logs on the instance. CloudTrail records API calls, not script output, and flow logs and ELB logs can't show why a script failed.

57. **A** — The manual approval action is built for this: it pauses the pipeline, notifies through SNS and links reviewers to the test report. The other options need custom work, waste build time, or rely on a CodeDeploy per-instance approval feature that doesn't exist.

58. **A** — Encoded authorization messages can only be decoded with STS DecodeAuthorizationMessage, and the caller needs permission for that action. The message is encrypted, not Base64 text, and the other features don't decode it.

59. **B** — Only provisioned concurrency keeps initialized environments ready, and scheduling it around the predictable ramp keeps the cost down. Reserved concurrency only guarantees and caps capacity; it doesn't pre-initialize anything. More memory speeds up initialization but doesn't eliminate it. A ping every minute keeps about one environment warm, not 200.

60. **B** — Metric filters work only on data that arrives after they're created and never backfill. Logs Insights can query the stored history directly. There's no backfill option, and the default value and resolution settings don't reprocess old logs.

61. **B** — Standard queues deliver at least once, so duplicates can arrive even when nothing fails. Making the side effect idempotent (a conditional write on the order ID before charging) is the only option that guarantees one charge per order. FIFO lowers throughput and deduplicates only identical messages within 5 minutes. The visibility timeout doesn't prevent at-least-once duplicates. A maxReceiveCount of 1 sends messages to the DLQ after any failure but doesn't stop duplicate processing.

62. **A, D** — Denying requests where aws:SecureTransport is false enforces TLS. Default encryption with SSE-KMS applies the customer managed key whenever a client omits encryption headers. Re-uploading objects after the fact is custom and slow. Object Lock controls retention, not encryption. Transfer Acceleration doesn't block plain-HTTP requests to the bucket.

63. **C, D** — Reserved concurrency sets aside capacity for the order function and caps the analytics function so it can't starve everything else. Provisioned concurrency still counts toward the account quota. Timeouts don't queue throttled requests, and async retry settings don't apply to synchronous API Gateway invocations.

64. **C** — Standard workflows can run for up to a year. The task token pauses the workflow until the web app reports the approval, Retry handles transient failures, and the console keeps each execution's visual history. Express workflows are limited to 5 minutes. EventBridge choreography and hourly polling both need more code and give no single visual history.

65. **A** — Immutable deployments keep the original instances in service, so rollback just terminates the new instances. Rolling with additional batch keeps full capacity but rolls back by redeploying to the updated instances. Rolling reduces capacity, and all-at-once causes downtime.
