# Module 08 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Amazon RDS Fundamentals, Storage & Configuration (1–20)

1. A financial application is migrating an on-premises PostgreSQL database to Amazon RDS. The database administrator needs to modify database engine settings such as `max_connections`, `shared_buffers`, and `log_statement`. Which mechanism in Amazon RDS is used to manage these engine parameters?
A) DB Option Groups
B) DB Parameter Groups
C) IAM Policies
D) Amazon CloudWatch Metric Filters

2. A company is running an Amazon RDS for Oracle database. The security team mandates that Transparent Data Encryption (TDE) and Oracle Native Network Encryption (NNE) must be enabled on the database instance. Which RDS mechanism enables these specific engine features?
A) DB Parameter Groups
B) DB Option Groups
C) AWS Secrets Manager
D) S3 Bucket Policies

3. A developer wants to enable encryption at rest for an existing Amazon RDS for MySQL database that was initially created without encryption. What is the standard AWS-recommended procedure to encrypt the database?
A) Modify the RDS DB instance settings and select "Enable Encryption" directly with no downtime
B) Take a DB snapshot of the unencrypted instance, copy the snapshot while enabling encryption with an AWS KMS key, and restore a new DB instance from the encrypted snapshot
C) Export the database using `mysqldump` to an unencrypted S3 bucket, then import it
D) Attach an encrypted EBS volume directly to the running RDS instance

4. An analytics database running on Amazon RDS experiences sudden spikes in disk usage during monthly report generation. The operations team wants to ensure the database storage expands automatically when free disk space falls below 10%, without taking the instance offline or manually resizing volumes. Which RDS feature solves this?
A) Multi-AZ standby scaling
B) Storage Auto Scaling
C) Read Replica storage bursting
D) Parameter Group disk expansion

5. An application uses an Amazon RDS for PostgreSQL instance. The development team needs consistent, high-throughput I/O performance with guaranteed low latency for a critical transaction-processing database. Which Amazon RDS storage type should they select?
A) General Purpose SSD (gp2)
B) Provisioned IOPS SSD (io1 or io2)
C) Magnetic Storage (standard)
D) Ephemeral Instance Store

6. Which statement accurately describes the difference between DB Parameter Groups and DB Option Groups in Amazon RDS?
A) Parameter Groups manage engine runtime configuration (e.g., timeouts, connection limits); Option Groups enable engine-specific features and extensions (e.g., Oracle TDE, SQL Server Native Backup)
B) Parameter Groups are for Aurora only; Option Groups are for standard RDS engines
C) Parameter Groups manage AWS KMS encryption keys; Option Groups manage IAM database authentication
D) Parameter Groups apply to VPC networking; Option Groups apply to storage sizing

7. An application developer needs to run a temporary development database on Amazon RDS for 3 months. The database uses MySQL. Which of the following responsibilities is managed by AWS rather than the developer?
A) Writing SQL queries and designing relational schema
B) Operating system patching, underlying host hardware maintenance, and automated backup execution
C) Configuring database user table permissions
D) Optimizing application-level query indexes

8. A company is evaluating Amazon RDS licensing options for Oracle and Microsoft SQL Server. What are the two primary licensing models available on RDS for these commercial engines? (Select TWO.)
A) License Included (cost of software license bundled into AWS hourly rate)
B) Bring Your Own License (BYOL) using existing on-premises software licenses
C) Open-Source Community License
D) GNU General Public License (GPL)
E) Unlimited Free Enterprise Tier

9. When restoring an Amazon RDS DB instance to a specific point in time (PITR) using automated backups, what is created as a result of the restore operation?
A) The existing DB instance is rolled back in place, keeping the exact same endpoint
B) A brand-new DB instance with a new endpoint is created from the snapshot and transaction logs
C) An Amazon DynamoDB table is generated
D) An S3 bucket containing raw CSV exports is created

10. What is the maximum retention period configurable for automated daily backups and continuous transaction log capture on Amazon RDS?
A) 7 days
B) 14 days
C) 35 days
D) 365 days

11. A developer creates a manual DB snapshot of an Amazon RDS for PostgreSQL instance before performing a schema migration. What happens to this manual snapshot if the developer later deletes the DB instance?
A) The manual snapshot is automatically deleted along with the instance
B) The manual snapshot persists in Amazon S3 until the developer explicitly deletes it
C) The manual snapshot is converted into an automated backup expiring in 35 days
D) The manual snapshot is transferred to AWS Glacier Deep Archive automatically

12. An Amazon RDS DB instance is deployed with General Purpose SSD (gp3) storage. Which two performance characteristics can be provisioned and scaled independently of storage capacity? (Select TWO.)
A) IOPS
B) Storage Throughput (MB/s)
C) Number of CPU cores
D) Maximum connection count
E) Number of Availability Zones

13. A company requires database backups to be retained for 7 years to meet regulatory compliance requirements. Automated backups on RDS have a maximum retention of 35 days. How should the team satisfy the 7-year retention policy?
A) Increase automated backup retention in the parameter group to 2,555 days
B) Create periodic manual DB snapshots (or use AWS Backup to automate snapshot creation and lifecycle policies) and retain them for 7 years
C) Run a daily `SELECT *` query and log the output to CloudWatch Logs
D) Enable Multi-AZ replication to hold data for 7 years

14. During an scheduled maintenance window, Amazon RDS needs to apply an operating system security patch. The database is a single-AZ instance. What impact will this maintenance have on the application?
A) Zero downtime; single-AZ instances patch with no interruption
B) The database will experience a brief period of unavailability while the instance reboots during the maintenance window
C) The instance will be permanently deleted and recreated with a new endpoint
D) The instance will automatically convert into an Aurora cluster

15. An organization wants to test a major database engine version upgrade on Amazon RDS PostgreSQL from version 13 to version 15. What is the safest way to validate the upgrade before modifying production?
A) Perform the in-place engine upgrade directly on the live production database during peak hours
B) Restore a production DB snapshot to a new test DB instance, perform the upgrade on the test instance, and run application regression tests
C) Modify the production parameter group to version 15 without changing the instance engine
D) Downgrade the production instance to MySQL first

16. A developer needs to access slow query logs for an Amazon RDS for MySQL database. How can these logs be accessed and monitored continuously?
A) SSH into the underlying RDS EC2 operating system host
B) Configure the DB parameter group to enable `slow_query_log` and publish the logs directly to Amazon CloudWatch Logs
C) Slow query logs are not supported on Amazon RDS
D) Inspect the AWS CloudTrail event history for SQL queries

17. Which two relational database engines supported by Amazon RDS are open-source and free of commercial licensing fees? (Select TWO.)
A) Amazon RDS for PostgreSQL
B) Amazon RDS for MySQL
C) Amazon RDS for Oracle
D) Amazon RDS for Microsoft SQL Server
E) Amazon RDS for IBM DB2

18. A database administrator wants to restrict inbound network traffic to an Amazon RDS DB instance so that only application servers residing in a specific security group can connect on port 3306. Which AWS networking mechanism controls this?
A) DB Parameter Group
B) VPC Security Group inbound rules
C) S3 Bucket Policy
D) IAM User Policy

19. What is the minimum number of Availability Zones required when configuring a DB Subnet Group for Amazon RDS in a VPC?
A) 1 Availability Zone
B) At least 2 Availability Zones
C) At least 3 Availability Zones
D) 5 Availability Zones

20. A developer needs to modify an Amazon RDS parameter that is marked as `dynamic` in the DB Parameter Group. When will the change take effect?
A) Immediately after saving the parameter group, without requiring an instance reboot
B) Only after the DB instance is manually stopped and restarted
C) During the next weekly maintenance window
D) Dynamic parameters cannot be modified

### Multi-AZ vs. Read Replicas (21–38)

21. A critical e-commerce database running on Amazon RDS requires high availability and disaster recovery. If the primary Availability Zone experiences a hardware failure, the system must automatically fail over to a standby instance in a different AZ with zero data loss. Which RDS configuration fulfills this requirement?
A) Create an asynchronous Read Replica in the same AZ
B) Deploy the database as an Amazon RDS Multi-AZ DB Instance deployment
C) Create a cross-Region Read Replica
D) Schedule automated snapshots every 5 minutes

22. A reporting dashboard executes complex, long-running analytical SQL queries against an Amazon RDS MySQL database. During peak business hours, these queries slow down the transactional operations on the primary database. What is the most cost-effective and architecturally sound solution?
A) Convert the database to a single-AZ deployment
B) Create an Amazon RDS Read Replica and point the reporting application to the Read Replica endpoint
C) Enable Multi-AZ standby deployment and run reporting queries against the standby instance
D) Increase the primary instance CPU size to the maximum available type

23. Which statement correctly distinguishes replication behavior between an RDS Multi-AZ standby and an RDS Read Replica?
A) Multi-AZ uses synchronous replication to guarantee zero data loss on failover; Read Replicas use asynchronous replication to offload read traffic
B) Multi-AZ uses asynchronous replication; Read Replicas use synchronous replication
C) Both Multi-AZ and Read Replicas use synchronous replication
D) Both Multi-AZ and Read Replicas use snapshot copies updated once per day

24. An application experiences an Availability Zone outage affecting its primary Amazon RDS Multi-AZ DB instance. What happens during the automatic failover process?
A) The primary database remains offline until an administrator manually promotes the standby via the AWS CLI
B) RDS automatically flips the canonical DNS endpoint of the DB instance to point to the synchronized standby in the second AZ, typically completing in under 2 minutes
C) The database IP address remains identical, but all data must be restored from the latest manual snapshot
D) RDS provisions a brand-new EC2 instance in a different AWS Region

25. Can an application execute `SELECT` read queries directly against the standby instance in a standard Amazon RDS Multi-AZ DB instance deployment?
A) Yes, the standby instance is always open for read-only traffic
B) No, in a standard Multi-AZ deployment, the standby instance is passive, not directly accessible for reads or writes, and exists strictly for high-availability failover
C) Yes, but only if the application connects over SSL on a separate port
D) Yes, if configured with a read-only parameter group

26. An engineering team wants to expand an application to a secondary AWS Region in Europe to serve low-latency read requests to European users, while keeping primary writes in us-east-1. Which Amazon RDS feature supports this cross-Region read scaling?
A) RDS Multi-AZ deployment across Regions
B) RDS Cross-Region Read Replicas
C) DB Option Groups
D) Amazon S3 Cross-Region Replication

27. A developer observes that an Amazon RDS Read Replica is returning data that is slightly out of date compared to the primary writer instance. Which CloudWatch metric should the developer inspect to measure this replication delay?
A) `CPUUtilization`
B) `ReplicaLag`
C) `DatabaseConnections`
D) `FreeStorageSpace`

28. If the primary instance of an Amazon RDS database fails, can a standard RDS Read Replica automatically take over write traffic with automatic DNS failover?
A) Yes, Read Replicas automatically fail over just like Multi-AZ standbys
B) No, Read Replicas do not support automatic failover; a Read Replica must be manually promoted to a standalone database by an administrator or custom automation script
C) Yes, if the replica is in the same Availability Zone
D) Yes, if the replica is configured with Multi-AZ

29. What is the maximum number of Read Replicas that can typically be created for a single Amazon RDS for MySQL or PostgreSQL database instance?
A) 2
B) 5
C) 15
D) 50

30. A company deploys an Amazon RDS Multi-AZ DB cluster with two readable standby instances (Multi-AZ DB Cluster). How does this differ from a traditional Multi-AZ DB Instance deployment?
A) It uses asynchronous replication for failover
B) In addition to high availability, both standby instances can serve read traffic, providing both automatic failover and read scaling in one deployment
C) It runs exclusively on premises
D) It does not support transaction logging

31. An administrator promotes an Amazon RDS Read Replica to a standalone database instance. What is the permanent effect of this promotion on the replica?
A) The replica continues replicating from the original primary
B) The replica stops replicating from the primary, becomes an independent read-write database with its own backup and lifecycle management, and cannot be reverted back to a replica
C) The original primary database is automatically deleted
D) The promoted replica is automatically converted to Aurora Serverless

32. Which two statements regarding Amazon RDS Multi-AZ deployments are true? (Select TWO.)
A) Multi-AZ failover is handled automatically by updating DNS records
B) Multi-AZ standby instances are located in a different Availability Zone within the same Region
C) Multi-AZ standby instances serve read-only reporting traffic by default in standard DB instance deployments
D) Multi-AZ replication is asynchronous, resulting in potential data loss on failover
E) Multi-AZ deployments span across two different AWS Regions

33. A mobile app backend generates 10,000 read queries and 500 write queries per second on an Amazon RDS MySQL database. The primary instance is hitting 95% CPU utilization. What is the recommended strategy to scale the database tier?
A) Enable Multi-AZ to offload 50% of the read traffic
B) Add one or more Read Replicas and modify the application code to route read queries (`SELECT`) to the replica endpoints and write queries (`INSERT`/`UPDATE`) to the primary endpoint
C) Switch the database engine to Microsoft Access
D) Increase the SQS visibility timeout

34. What happens to replication when an Amazon RDS Read Replica runs out of storage space?
A) The replica automatically switches to write-only mode
B) Replication stops, and the replica status changes to `storage-full` or `error` until storage is expanded
C) The primary instance shuts down to prevent data drift
D) Data is discarded from the primary database

35. Which of the following RDS engines support Cross-Region Read Replicas?
A) MySQL, MariaDB, and PostgreSQL
B) Oracle (all editions with no restrictions)
C) SQL Server Express Edition
D) Microsoft Access

36. A company needs to perform maintenance on an Amazon RDS Multi-AZ primary database. How does RDS minimize downtime during an operating system update on a Multi-AZ deployment?
A) RDS patches the standby instance first, promotes the standby to primary (brief failover), and then patches the old primary
B) RDS shuts down both instances simultaneously for 2 hours
C) RDS migrates the entire database to DynamoDB temporarily
D) Multi-AZ instances cannot be patched

37. What is a primary trade-off when enabling an RDS Read Replica for an active write-heavy workload?
A) Read Replicas consume significant write capacity on the primary to ship binary/WAL logs, and asynchronous replication may introduce replica lag
B) Read Replicas permanently lock the primary database tables during creation
C) Read Replicas require disabling automated backups
D) Read Replicas only work over unencrypted connections

38. A developer wants to create a Read Replica of an Amazon RDS for MySQL database, but the option in the AWS Console is disabled. What prerequisite configuration is missing?
A) The primary database must have automated backups enabled (backup retention period > 0) to allow binary logging
B) The primary database must be deployed in us-east-1
C) The primary database must have at least 1 TB of storage
D) The primary database must be running on a dedicated EC2 host

### Secure Database Connections & Authentication (39–54)

39. A company needs to securely store, manage, and automatically rotate database credentials for an Amazon RDS for MySQL instance every 30 days. The credentials must not be stored in application code or configuration files. Which AWS service natively fulfills this requirement?
A) AWS Systems Manager Parameter Store (Standard tier)
B) AWS Secrets Manager with automatic rotation configured using an AWS-provided Lambda rotation template
C) Amazon S3 bucket with versioning
D) AWS IAM Access Keys

40. What is the main difference between AWS Secrets Manager and AWS Systems Manager Parameter Store regarding database credential management?
A) Secrets Manager provides native, out-of-the-box automatic credential rotation for Amazon RDS, Aurora, and Redshift using Lambda templates; Parameter Store does not provide built-in automatic rotation
B) Parameter Store supports automatic rotation; Secrets Manager only supports static text
C) Secrets Manager is free; Parameter Store charges $100 per secret
D) Parameter Store encrypts data with KMS; Secrets Manager stores plaintext

41. A developer writes a Python Lambda function that connects to Amazon RDS PostgreSQL using AWS Secrets Manager. What is the most efficient and secure way for the Lambda function to retrieve the password?
A) Hardcode the secret in the Lambda environment variables
B) Grant the Lambda execution role `secretsmanager:GetSecretValue` permission for the specific secret ARN, and call the Secrets Manager API at connection time (caching the credentials in global scope)
C) Store the database password in a public GitHub repository
D) Email the password to the Lambda handler on every request

42. How does IAM Database Authentication work for Amazon RDS for MySQL and PostgreSQL?
A) Users log in using their AWS root account password
B) The application requests a temporary, short-lived authentication token (valid for 15 minutes) generated from IAM credentials via the AWS SDK, and connects over SSL/TLS using the token instead of a password
C) An IAM role creates a permanent password stored in a local `.txt` file
D) The database allows all IAM users to connect without any password or token

43. What is the validity duration of an authentication token generated for Amazon RDS IAM Database Authentication?
A) 5 minutes
B) 15 minutes
C) 1 hour
D) 24 hours

44. Which AWS CLI command generates an authentication token for IAM database authentication against an Amazon RDS MySQL instance?
A) `aws rds generate-db-auth-token --hostname <endpoint> --port 3306 --username <db_user>`
B) `aws iam create-login-profile --user-name <db_user>`
C) `aws secretsmanager get-secret-value --secret-id <id>`
D) `aws sts assume-role --role-arn <arn>`

45. An application connecting to Amazon RDS PostgreSQL using IAM Database Authentication receives an `Access Denied` error when attempting to connect. Which two configurations must be in place for IAM DB authentication to succeed? (Select TWO.)
A) The IAM identity's policy must explicitly allow the `rds-db:connect` action on the target database resource ARN
B) The PostgreSQL database user must be granted the `rds_iam` role (or `AWSAuthenticationPlugin` in MySQL)
C) The database connection must be made over unencrypted HTTP
D) The database must be deployed in a public subnet with an Internet Gateway
E) Automated backups must be disabled

46. When an application connects to Amazon RDS using IAM Database Authentication, why must the connection use SSL/TLS encryption?
A) Unencrypted connections will expose the plaintext database tables to the internet
B) SSL/TLS is strictly required by RDS when transmitting the signed IAM authentication token to prevent token interception
C) SSL/TLS reduces CPU utilization on the database host
D) IAM DB authentication does not use network connections

47. A developer configures Secrets Manager automatic rotation for an Amazon RDS database. During rotation, Secrets Manager invokes a Lambda function that updates the secret in Secrets Manager and executes SQL statements on the database to change the password. Which credential does the rotation Lambda function use to alter the user's password?
A) The AWS root account credentials
B) A superuser / administrative credential stored in a separate master secret in Secrets Manager
C) A temporary EC2 key pair
D) An IAM user with administrator access

48. An application running on Amazon EC2 instances connects to an Amazon RDS MySQL database. What is the best practice for granting the EC2 instances access to read the database credentials from Secrets Manager?
A) Hardcode IAM access keys and secret keys inside the application configuration file on the EC2 instance
B) Attach an IAM Instance Profile (Role) to the EC2 instances granting least-privilege `secretsmanager:GetSecretValue` permission on the specific database secret ARN
C) Store credentials in an unencrypted S3 bucket
D) Disable IAM and make Secrets Manager public

49. An auditor mandates that all connections between application EC2 instances and an Amazon RDS PostgreSQL database must be encrypted in transit. How can this be enforced at the database configuration level?
A) Set `rds.force_ssl = 1` in the DB parameter group associated with the PostgreSQL instance
B) Enable S3 Block Public Access
C) Configure an AWS WAF rule on port 5432
D) Set `max_connections = 0` in the parameter group

50. Which relational database engines natively support Amazon RDS IAM Database Authentication? (Select TWO.)
A) Amazon RDS for MySQL / Aurora MySQL
B) Amazon RDS for PostgreSQL / Aurora PostgreSQL
C) Amazon RDS for Microsoft SQL Server Express
D) Amazon RDS for Oracle Enterprise Edition
E) Amazon RDS for IBM DB2

51. A security team requires that database passwords stored in AWS Secrets Manager be encrypted at rest. What encryption mechanism does Secrets Manager use?
A) Plaintext base64 encoding
B) AWS Key Management Service (AWS KMS) using either an AWS-managed key (`aws/secretsmanager`) or a customer-managed KMS key (CMK)
C) Client-side RSA-1024 encryption only
D) MD5 hashing

52. An application caches database credentials retrieved from AWS Secrets Manager in memory to reduce API calls and latency. The secret is configured to rotate automatically every 30 days. When rotation occurs, what should the application do if a database connection attempt fails with an authentication error?
A) Crash the application and trigger an EC2 reboot
B) Invalidate the cached secret, fetch the latest secret value from Secrets Manager, and retry the database connection with the newly rotated credentials
C) Send an alert to the CEO
D) Fall back to hardcoded default passwords

53. A developer wants to restrict an IAM policy so that a Lambda function can only generate IAM authentication tokens for a specific database user `app_user` on an RDS instance with resource ID `db-ABC123XYZ`. Which action and resource format should be used?
A) Action: `rds-db:connect`, Resource: `arn:aws:rds-db:region:account:dbuser:db-ABC123XYZ/app_user`
B) Action: `rds:DescribeDBInstances`, Resource: `*`
C) Action: `secretsmanager:GetSecretValue`, Resource: `*`
D) Action: `iam:PassRole`, Resource: `arn:aws:iam::account:role/DBRole`

54. Why does AWS recommend storing database connection strings as a JSON object in AWS Secrets Manager rather than plain strings?
A) JSON is required for KMS encryption
B) Storing structured key-value pairs (e.g., `engine`, `host`, `port`, `username`, `password`, `dbname`) enables automated rotation Lambda templates to update and parse individual fields seamlessly
C) JSON strings load 10x faster over the network
D) Plain strings are not supported in AWS Secrets Manager

### RDS Proxy & Connection Management (55–68)

55. A serverless application consists of hundreds of concurrent AWS Lambda functions executing queries against an Amazon RDS PostgreSQL database. Under high traffic surges, Lambda invocations exhaust the database's `max_connections` limit, causing `Too many connections` errors. Which solution best resolves this issue without scaling up the database instance class?
A) Increase Lambda's `ReservedConcurrentExecutions` to 10,000
B) Deploy Amazon RDS Proxy between the Lambda functions and the PostgreSQL database to pool and multiplex connections
C) Increase the `max_connections` parameter in the DB Parameter Group to 1,000,000
D) Switch the database to single-AZ mode

56. How does Amazon RDS Proxy handle database failover events for Multi-AZ RDS and Aurora clusters?
A) RDS Proxy requires all client applications to disconnect and re-resolve DNS endpoints manually
B) RDS Proxy maintains established client connections, connects to the newly promoted primary instance in the background, and preserves client state, reducing failover time by up to 66%
C) RDS Proxy shuts down the database cluster during failover
D) RDS Proxy converts SQL queries into DynamoDB API calls during failover

57. Where does Amazon RDS Proxy retrieve the database credentials needed to authenticate with the underlying RDS or Aurora DB instance?
A) Hardcoded in the RDS Proxy configuration console
B) From secrets stored in AWS Secrets Manager, accessed via an IAM role assumed by the proxy
C) From the caller's local `/tmp` folder
D) From Amazon S3 Glacier

58. An application connects to Amazon RDS Proxy using IAM authentication. Which component authenticates to what?
A) The client application authenticates to RDS Proxy using IAM credentials/tokens; RDS Proxy authenticates to the native RDS database using credentials retrieved from AWS Secrets Manager
B) The RDS database authenticates to the client using SSH keys
C) RDS Proxy disables all authentication
D) The client application connects directly to RDS, bypassing the proxy

59. Which two relational database engines are supported by Amazon RDS Proxy? (Select TWO.)
A) MySQL (and Aurora MySQL)
B) PostgreSQL (and Aurora PostgreSQL)
C) Microsoft SQL Server 2008
D) Oracle 11g
E) SQLite

60. An architect is designing a high-concurrency serverless microservice on AWS Lambda connecting to an Amazon Aurora MySQL database. Why is traditional client-side connection pooling inside Lambda functions ineffective?
A) Lambda functions run inside ephemeral, isolated execution environments; each concurrent execution environment initializes its own independent connection pool, causing connection proliferation under scale
B) Lambda does not allow network calls to databases
C) Connection pooling is only supported on Windows operating systems
D) Client-side connection pooling corrupts Aurora shared storage

61. What network configuration is required for Amazon RDS Proxy to communicate with an Amazon RDS DB instance?
A) The RDS Proxy and the RDS DB instance must reside in the same VPC (or in peered/connected VPCs with routable private networking)
B) The RDS Proxy must have a public IP address on the public internet
C) The RDS DB instance must have an Internet Gateway attached
D) RDS Proxy must run outside of any VPC

62. Does Amazon RDS Proxy cache SQL query results in memory like Amazon ElastiCache?
A) Yes, RDS Proxy is an in-memory SQL query cache
B) No, RDS Proxy is a database connection pooler and multiplexer that manages connection lifecycles; it does not cache SQL query results
C) Yes, but only for `SELECT *` queries
D) Yes, RDS Proxy replaces Redis and Memcached

63. What is "connection pinning" in Amazon RDS Proxy, and what causes it?
A) Pinning occurs when a client session executes operations (such as setting session-level variables, temporary tables, or prepared statements) that tie the client connection to a specific underlying DB connection, temporarily preventing multiplexing
B) Pinning is an error that permanently corrupts the database
C) Pinning is a feature that increases network throughput by 10x
D) Pinning occurs when a database instance runs out of storage

64. How does Amazon RDS Proxy improve application security?
A) It enforces TLS/SSL between the client and the proxy, and allows centralizing database credential access in Secrets Manager and IAM rather than embedding credentials across client applications
B) It encrypts hard drives on client laptops
C) It automatically sanitizes all SQL injection attempts
D) It disables all database user accounts

65. A developer modifies an application to connect to an Amazon RDS database through RDS Proxy. What changes are required in the application code?
A) The entire database access layer must be rewritten in DynamoDB syntax
B) Only the database connection endpoint hostname needs to be updated to the RDS Proxy endpoint; standard SQL statements, drivers, and ORMs remain unchanged
C) The application must switch to using UDP sockets
D) All `JOIN` queries must be removed from the application

66. Which CloudWatch metric tracks the number of database connections currently opened by Amazon RDS Proxy to the target database?
A) `DatabaseConnections`
B) `DatabaseConnectionsCurrentlyBorrowed`
C) `QueryResponseTime`
D) `CacheHitRate`

67. A developer configures an RDS Proxy for an Aurora PostgreSQL database. The application needs to enforce that all client connections to the proxy use TLS 1.2. Where is this setting configured?
A) In the RDS Proxy settings under `Require Transport Layer Security (TLS)`
B) In the S3 bucket properties
C) In the IAM user policy
D) In the route table

68. Can Amazon RDS Proxy be used with Amazon EC2 instances and Amazon ECS container tasks, or is it exclusive to AWS Lambda?
A) RDS Proxy is strictly exclusive to AWS Lambda
B) RDS Proxy can be used by Lambda, EC2 instances, ECS tasks, and any application running in a VPC that benefits from connection pooling and fast failover
C) RDS Proxy only works with on-premises servers
D) RDS Proxy only works with AWS Step Functions

### Amazon Aurora Architecture, Scaling & Global Database (69–86)

69. How does the underlying storage architecture of Amazon Aurora differ fundamentally from standard Amazon RDS EBS-backed storage?
A) Aurora uses standard single-AZ gp3 EBS volumes
B) Aurora uses a distributed, log-structured, self-healing storage volume that automatically replicates data 6 ways across 3 Availability Zones within a Region and scales storage automatically up to 128 TiB
C) Aurora stores all data in a single local NVMe instance store on the primary host
D) Aurora requires manual volume provisioning and striping across RAID arrays

70. What is the maximum number of Aurora Replicas that can be added to an Amazon Aurora DB cluster?
A) 5
B) 15
C) 50
D) 100

71. Why is replica lag on Amazon Aurora Replicas significantly lower (typically single-digit milliseconds) compared to standard Amazon RDS Read Replicas?
A) Aurora Replicas share the exact same underlying distributed storage volume as the primary writer, rather than receiving and replaying an asynchronous copy of the data stream
B) Aurora disables transaction logging
C) Aurora Replicas run on faster CPU chips
D) Aurora Replicas only store data in memory without disk persistence

72. What happens when the primary writer instance in an Amazon Aurora Multi-AZ DB cluster experiences an unexpected hardware failure?
A) Aurora requires an administrator to manually restore from the latest automated backup
B) Aurora automatically promotes one of the existing Aurora Replicas to become the new primary writer with zero data loss, typically in under 30 seconds
C) Aurora shuts down the entire cluster permanently
D) All Aurora Replicas are deleted and recreated

73. An e-commerce startup is launching a new application with unpredictable, highly variable traffic. The database experiences long periods of inactivity with sudden, brief traffic surges. Which database configuration provides automatic, fine-grained compute scaling without managing instance sizes?
A) Amazon RDS for MySQL with Multi-AZ
B) Amazon Aurora Serverless v2
C) Amazon RDS for Oracle Enterprise Edition
D) Amazon EC2 with self-hosted MySQL

74. How is compute capacity measured and scaled in Amazon Aurora Serverless v2?
A) vCPUs and Gigabytes of RAM
B) Aurora Capacity Units (ACUs), where 1 ACU provides approximately 2 GiB of memory along with corresponding CPU and networking, scaling dynamically in fine-grained increments
C) Read Capacity Units (RCUs) and Write Capacity Units (WCUs)
D) Number of EC2 instances in an Auto Scaling group

75. Can an Amazon Aurora DB cluster contain a mix of provisioned DB instances and Aurora Serverless v2 instances in the same cluster?
A) No, an Aurora cluster must be 100% provisioned or 100% serverless
B) Yes, Aurora allows combining provisioned instances (e.g., a provisioned writer) and Serverless v2 instances (e.g., auto-scaling readers) within the same cluster
C) Only if deployed in a single Availability Zone
D) Only with Aurora PostgreSQL, not Aurora MySQL

76. A global enterprise requires an Amazon Aurora PostgreSQL database that supports disaster recovery with an RPO under 1 second and low-latency read operations across multiple AWS Regions worldwide. Which feature should they deploy?
A) Amazon Aurora Global Database
B) Amazon RDS Cross-Region Automated Backups
C) AWS DataSync running hourly syncs
D) Amazon S3 Cross-Region Replication

77. How does Amazon Aurora Global Database replicate data from the primary AWS Region to secondary AWS Regions?
A) It uses standard MySQL statement-based replication over public internet endpoints
B) It uses dedicated, storage-level physical replication infrastructure built into the Aurora storage layer, achieving typical replication lag of less than 1 second without impacting compute performance
C) It exports database snapshots to S3 every 15 minutes
D) It routes SQL queries through AWS Lambda

78. In the event of a total regional outage affecting the primary Region of an Amazon Aurora Global Database, how is disaster recovery executed?
A) The secondary Region is automatically deleted
B) A secondary Region can be promoted to take over full read-write operations in typically under 1 minute with no data loss
C) The database must be re-architected from scratch
D) Data must be manually re-indexed over several days

79. What are the two built-in database cluster endpoints provided by an Amazon Aurora DB cluster? (Select TWO.)
A) **Cluster Endpoint (Writer Endpoint)**: points to the current primary DB instance for read-write operations
B) **Reader Endpoint**: load-balances read-only traffic across all available Aurora Replicas in the cluster
C) **Root Endpoint**: provides SSH root shell access to the storage nodes
D) **Internet Endpoint**: exposes the database directly to public search engines
E) **Backup Endpoint**: used exclusively for downloading tape archives

80. A developer needs to route analytical reporting queries to a specific group of high-memory Aurora Replicas while directing standard web application reads to smaller general-purpose replicas. Which Aurora feature creates custom endpoints for designated subsets of DB instances?
A) DB Parameter Groups
B) Custom Endpoints
C) AWS Secrets Manager
D) Route 53 Geolocation routing

81. Which two relational database engines are fully compatible with Amazon Aurora? (Select TWO.)
A) MySQL (5.7 and 8.0 compatible)
B) PostgreSQL (11 through 16+ compatible)
C) Microsoft SQL Server Enterprise
D) IBM DB2
E) MongoDB

82. What is the maximum storage capacity supported by an Amazon Aurora database cluster?
A) 16 TiB
B) 64 TiB
C) 128 TiB
D) 1 PiB

83. A developer wants to execute an SQL query directly from an AWS Lambda function against an Amazon Aurora Serverless database over an HTTP REST endpoint using IAM credentials, without managing persistent database connections or VPC networking. Which Aurora capability enables this?
A) Amazon Aurora Data API
B) Amazon RDS Proxy
C) SSH Tunneling
D) DB Option Groups

84. How does Amazon Aurora handle storage self-healing and data integrity?
A) If an individual storage block or disk fails, Aurora automatically repairs the corrupted block in the background using data from the other 5 copies across the 3 Availability Zones without affecting availability
B) Aurora requires restoring from the daily backup snapshot
C) Aurora halts write traffic until an administrator replaces the failed disk
D) Aurora delegates data integrity to the client application

85. Which statement accurately compares failover speed between Amazon Aurora and standard Amazon RDS Multi-AZ?
A) Standard RDS Multi-AZ fails over in under 5 seconds; Aurora takes 5 minutes
B) Amazon Aurora typically fails over in under 30 seconds (or under 10 seconds with RDS Proxy) because storage is shared and replicas are already warm; standard RDS Multi-AZ takes 60 to 120 seconds due to DNS failover and standby synchronization
C) Both Aurora and RDS have identical 1-hour failover times
D) Neither service supports automated failover

86. An application uses Amazon Aurora MySQL. The development team needs to spin up an isolated, temporary copy of the 10 TB production database for integration testing. The copy must be created in minutes without duplicating storage costs until data is modified. Which Aurora feature accomplishes this?
A) Database Cloning (Copy-on-Write)
B) Manual DB Snapshot Restore
C) Point-in-Time Recovery to a new cluster
D) Exporting data to Amazon S3 via `SELECT INTO OUTFILE`

### Amazon ElastiCache (Redis & Memcached) & Caching Patterns (87–104)

87. A high-traffic social media application needs to cache user profile records in front of Amazon RDS to reduce read latency from 15ms down to sub-millisecond response times. Which AWS service is a managed, in-memory caching service designed for this purpose?
A) Amazon ElastiCache
B) Amazon EBS
C) Amazon S3 Standard-IA
D) Amazon Athena

88. A gaming company requires an in-memory data store to manage a real-time leaderboard of player high scores ranked in descending order. Which ElastiCache engine and data structure natively supports sorted ranking operations?
A) ElastiCache for Memcached with plain strings
B) ElastiCache for Redis with Sorted Sets (ZSET)
C) ElastiCache for Memcached with multithreaded key-value pairs
D) Amazon RDS PostgreSQL with JSONB

89. Which two architectural capabilities are supported by Amazon ElastiCache for Redis but are NOT supported by Amazon ElastiCache for Memcached? (Select TWO.)
A) Multi-AZ replication with automatic failover
B) Rich data structures (lists, sets, sorted sets, hashes, bitmaps)
C) Multithreaded execution across multiple CPU cores on a single node
D) Purely ephemeral, non-persistent in-memory caching
E) Simple key-value string storage

90. An application implements the **Cache-Aside (Lazy-Loading)** pattern with Amazon ElastiCache. What is the correct sequence of operations when a client requests data?
A) The application writes data to the database first, then writes to the cache
B) The application checks the cache first; on a cache hit, it returns the cached data; on a cache miss, it queries the database, writes the result to the cache with a TTL, and returns the data to the client
C) The database automatically intercepts the request and checks ElastiCache
D) The application deletes all cached keys before querying the database

91. What is the primary risk associated with the Cache-Aside caching pattern if cached keys do not have a Time-To-Live (TTL) configured, and how is it mitigated?
A) Cache memory will never be used
B) Data in the cache can become stale if the underlying database is updated without invalidating the corresponding cache keys; mitigated by setting an appropriate TTL on cached entries and invalidating keys on write operations
C) The database will automatically shut down
D) Memcached will convert into Redis

92. An architect is designing a high-throughput caching tier using Amazon ElastiCache for Memcached. What is a key architectural advantage of Memcached's multithreaded architecture?
A) It supports multi-region automatic failover
B) A single Memcached node can utilize multiple CPU cores and handle massive concurrent operations without sharding
C) It natively persists all data to Amazon S3
D) It supports complex geospatial queries

93. A company uses Amazon ElastiCache for Redis in Cluster Mode Disabled. The cache tier experiences extreme write volume that exceeds the throughput limits of the single primary node. How can write capacity be scaled horizontally across multiple nodes?
A) Add 5 read replicas to the existing shard
B) Enable ElastiCache for Redis Cluster Mode Enabled to partition (shard) keys across multiple shards, each with its own primary writer
C) Switch from Redis to Memcached
D) Increase the SQS visibility timeout

94. What feature of Amazon ElastiCache for Redis provides point-in-time snapshots and data durability to recover from node failures or create new clusters?
A) Redis Backup and Restore using RDB snapshots stored in Amazon S3
B) AWS CloudTrail event history
C) Amazon Route 53 health checks
D) EC2 instance store swapping

95. An application uses Amazon ElastiCache for Redis as a publish/subscribe (Pub/Sub) messaging broker for live chat rooms. Why is Redis suitable for this use case compared to Memcached?
A) Memcached only supports video streaming
B) Redis natively supports Pub/Sub commands (`PUBLISH`, `SUBSCRIBE`, `PSUBSCRIBE`), allowing clients to push and receive messages on named channels in real time
C) Redis requires zero network connectivity
D) Redis automatically writes every chat message to tape backup

96. A developer needs to secure network access to an Amazon ElastiCache for Redis cluster deployed in a VPC. Which two security mechanisms should be implemented? (Select TWO.)
A) Enable in-transit encryption (TLS) and configure Redis `AUTH` token (password protection) or IAM authentication
B) Restrict inbound access using VPC Security Groups so that only authorized application EC2/Lambda security groups can connect on port 6379
C) Place the ElastiCache cluster in a public subnet with an Internet Gateway
D) Disable all encryption to improve latency
E) Allow `0.0.0.0/0` inbound access on port 6379

97. An e-commerce web application running on multiple EC2 instances behind an Application Load Balancer needs a centralized, shared session store so that users stay logged in even if an EC2 instance terminates. Which AWS service is the most common choice for managing session state?
A) Amazon EBS gp3 volume attached to one instance
B) Amazon ElastiCache for Redis
C) Amazon S3 Glacier Flexible Retrieval
D) AWS CodeCommit

98. In Amazon ElastiCache for Redis, what happens during an automatic failover in a Multi-AZ cluster when the primary node fails?
A) The cluster enters read-only mode permanently
B) ElastiCache detects the primary node failure, promotes an existing read replica to become the new primary writer, and updates internal DNS records, typically completing in under a minute
C) All cached data is permanently erased and the cluster is deleted
D) The application must deploy a new Redis cluster from scratch

99. An engineer is tuning the memory management of an Amazon ElastiCache for Redis cluster. When the cache reaches its memory limit (`maxmemory`), what parameter controls which keys are evicted to make room for new writes?
A) `maxmemory-policy` (e.g., `volatile-lru`, `allkeys-lru`, `volatile-ttl`, `noeviction`)
B) `max_connections`
C) `rds.force_ssl`
D) `shared_buffers`

100. What is the difference between Write-Through and Lazy-Loading (Cache-Aside) caching strategies?
A) Write-Through updates the cache synchronously whenever data is written to the database (ensuring cache freshness at the cost of write latency); Lazy-Loading populates the cache only on a cache miss during a read operation
B) Write-Through only caches data for 1 second; Lazy-Loading caches data forever
C) Write-Through is for Memcached only; Lazy-Loading is for Redis only
D) There is no functional difference between the two strategies

101. Which Amazon ElastiCache engine supports User Group Management and Role-Based Access Control (RBAC) to enforce fine-grained permissions per user and command?
A) ElastiCache for Redis (version 6.0 and later)
B) ElastiCache for Memcached
C) Amazon S3 Standard
D) Amazon Athena

102. An application experiences a "cache stampede" (thundering herd) when a popular cached key expires, causing thousands of concurrent requests to hit the backend RDS database simultaneously. Which two techniques prevent or mitigate cache stampedes? (Select TWO.)
A) Use early key expiration / probabilistic early re-computation (refreshing the cache before it hard-expires)
B) Implement mutex locking (locking the cache key so only one worker queries the database to repopulate the cache while others wait or return stale data)
C) Delete all cached keys on the primary node every minute
D) Disable caching completely
E) Reduce database memory to force fast query aborts

103. A developer configures ElastiCache for Redis with Auto Scaling. Which metrics can trigger automatic scaling of read replicas or shards?
A) `CPUUtilization` and `FreeableMemory` (or `EngineCPUUtilization` and `DatabaseMemoryUsagePercentage`)
B) `S3BucketSizeBytes`
C) `BillingAmountUSD`
D) `LambdaColdStarts`

104. Which port is the standard default port for Redis, and which is for Memcached?
A) Redis: 3306; Memcached: 5432
B) Redis: 6379; Memcached: 11211
C) Redis: 80; Memcached: 443
D) Redis: 1521; Memcached: 1433

### Amazon MemoryDB for Redis (105–112)

105. An application requires an in-memory, microsecond-read, low-latency database compatible with the Redis API. The data store must serve as the primary, authoritative database (system of record) with guaranteed multi-AZ durability and zero data loss on node failure. Which AWS service fulfills this requirement?
A) Amazon ElastiCache for Redis
B) Amazon MemoryDB for Redis
C) Amazon ElastiCache for Memcached
D) Amazon S3 Standard

106. How does Amazon MemoryDB for Redis achieve full transactional durability across multiple Availability Zones, unlike Amazon ElastiCache for Redis?
A) By writing data directly to tape archives
B) By using a distributed, multi-AZ transactional log that persists every write to storage across multiple AZs before acknowledging the write to the client
C) By taking automated manual snapshots once a week
D) By disabling all memory caching and using hard drives only

107. Which statement accurately describes the architectural role difference between Amazon ElastiCache for Redis and Amazon MemoryDB for Redis?
A) ElastiCache is a high-speed cache placed in front of an authoritative persistent database; MemoryDB is a durable, primary in-memory database designed to be the system of record
B) ElastiCache is durable; MemoryDB is purely ephemeral
C) ElastiCache is for relational SQL data; MemoryDB is for unstructured video files
D) MemoryDB does not support the Redis API

108. An e-commerce platform uses Redis data structures for real-time inventory reservation during checkout. If an in-memory node restarts, the reserved inventory counts must not be lost under any circumstances. Which AWS service is designed for this authoritative in-memory workload?
A) Amazon ElastiCache for Memcached
B) Amazon MemoryDB for Redis
C) Amazon CloudFront
D) Amazon RDS for SQL Server

109. What are the performance characteristics of Amazon MemoryDB for Redis?
A) Single-digit millisecond reads and 1-minute writes
B) Microsecond read latency (from memory) and single-digit millisecond write latency (due to multi-AZ transactional log persistence)
C) 10-second read latency and 5-minute write latency
D) Sub-millisecond reads with zero write support

110. Which Redis-compatible features are supported by Amazon MemoryDB for Redis?
A) Redis data types (hashes, lists, sets, sorted sets, streams), transactions, Pub/Sub, and Redis Cluster sharding
B) Only plain string key-value pairs
C) Only MySQL relational queries
D) GraphQL schema validation

111. Can an application migrate an existing Redis RDB snapshot file into Amazon MemoryDB for Redis when seeding a new cluster?
A) No, MemoryDB cannot import data
B) Yes, MemoryDB supports restoring from an existing Redis RDB snapshot stored in Amazon S3 during cluster creation
C) Only by manually typing the data into the AWS console
D) Only through an AWS Direct Connect cable

112. A financial technology firm is deciding between ElastiCache for Redis and MemoryDB for Redis. They have a relational database (Amazon Aurora) as their source of truth, and need an ephemeral cache strictly to offload read queries. Which service should they choose?
A) Amazon MemoryDB for Redis
B) Amazon ElastiCache for Redis (simpler, cost-effective caching tier in front of an existing source of truth)
C) Amazon RDS for Oracle
D) AWS Glacier

### Relational (RDS/Aurora) vs. NoSQL (DynamoDB) Decision Framework (113–120)

113. A company is designing a new customer analytics portal that requires running ad-hoc SQL queries with complex multi-table `JOIN` operations, aggregations, and strict relational integrity across 20 normalized tables. Which AWS database service is the best fit?
A) Amazon DynamoDB
B) Amazon RDS (or Amazon Aurora)
C) Amazon ElastiCache for Memcached
D) Amazon SimpleDB

114. A mobile gaming backend requires storing millions of player state records with high-frequency reads and writes. The access pattern is strictly key-value lookups by `player_id`. Traffic fluctuates unpredictably from 100 to 500,000 requests per second. The team wants a fully serverless, zero-maintenance database with single-digit millisecond latency at any scale. Which service is the best fit?
A) Amazon RDS for PostgreSQL (Single-AZ)
B) Amazon DynamoDB
C) Amazon RDS for Oracle
D) Amazon ElastiCache for Memcached

115. An enterprise order management system requires strict ACID transactions across multiple parent and child tables with foreign key constraints, using an existing Hibernate ORM framework. Which database should be selected?
A) Amazon DynamoDB
B) Amazon Aurora (or Amazon RDS)
C) Amazon MemoryDB for Redis
D) Amazon S3

116. Which two requirements would strongly favor selecting Amazon DynamoDB over Amazon RDS? (Select TWO.)
A) Extreme, unpredictable horizontal scale with simple, predefined partition-key-based access patterns
B) Need for a fully managed, serverless database with zero instance sizing, storage provisioning, or OS patching overhead
C) Need for complex relational `JOIN` queries across dozens of normalized tables
D) Need for database-enforced foreign key cascading deletes
E) Legacy application designed specifically for Microsoft SQL Server stored procedures

117. An application stores unstructured product catalog data where items have widely varying attributes (e.g., electronics have `screen_size` and `battery_life`, books have `author` and `isbn`, apparel has `size` and `fabric`). The schema evolves weekly. Which database accommodates this flexible schema with minimal friction?
A) Amazon RDS for MySQL with rigid SQL table definitions
B) Amazon DynamoDB (schema-less document store where items can have varying attributes)
C) Amazon RDS for Oracle
D) Amazon Redshift

118. A developer is designing a microservice architecture. Service A handles user authentication and session management (key-value lookups, TTL session expiration, high concurrency). Service B handles financial accounting and ledger balances (complex relational joins, strict foreign keys, audit reporting). Which database strategy aligns with microservices best practices?
A) Force both services to share a single monolithic Amazon RDS MySQL database
B) Polyglot persistence: use Amazon DynamoDB (or ElastiCache) for Service A, and Amazon Aurora PostgreSQL for Service B
C) Force both services to use Amazon S3 flat files
D) Use Amazon MemoryDB for accounting and Oracle for sessions

119. Which AWS service is the optimal choice for a relational database workload that requires MySQL compatibility, automatic storage scaling up to 128 TiB, fast sub-second cross-Region replication, and automatic failover in under 30 seconds?
A) Amazon RDS for MySQL Single-AZ
B) Amazon Aurora Global Database (MySQL-compatible)
C) Amazon DynamoDB Global Tables
D) Amazon ElastiCache for Memcached

120. Which of the following statements correctly compares DynamoDB and Amazon RDS?
A) RDS scales compute and storage automatically without capacity planning; DynamoDB requires manual instance provisioning
B) DynamoDB is designed for horizontal scaling with single-digit millisecond latency on known access patterns; RDS is designed for complex relational SQL queries, joins, and multi-table integrity
C) DynamoDB does not support any form of encryption at rest
D) RDS does not support automated backups

### Integrative Scenarios & Troubleshooting (121–125)

121. An online banking platform experiences intermittent connection timeouts on an Amazon RDS for PostgreSQL instance when Lambda-based microservices scale up during morning hours. Furthermore, security compliance mandates that database passwords must be rotated every 60 days without application downtime, and all database traffic must be encrypted in transit. Which combination of architectural changes resolves all issues?
A) Deploy Amazon RDS Proxy to pool Lambda connections, store credentials in AWS Secrets Manager with automatic 60-day rotation enabled, and enforce TLS/SSL connection requirements
B) Increase the PostgreSQL `max_connections` parameter, hardcode the new password in the Lambda zip file, and disable TLS
C) Switch the database to single-AZ mode and use Memcached for password storage
D) Replace the database with Amazon S3 Glacier

122. A global media company runs an Amazon Aurora MySQL database. The company is opening a new office in Tokyo and needs Japanese employees to run read-only reporting dashboards against the database with sub-second latency. If a disaster affects the primary US Region, the Tokyo database must be capable of becoming the primary read-write database in under 1 minute. Which architecture meets these requirements?
A) Amazon Aurora Global Database with the primary cluster in the US and a secondary replica cluster in the Tokyo Region
B) Amazon RDS for MySQL with daily manual snapshots copied to Tokyo
C) Single-AZ RDS PostgreSQL with S3 Cross-Region Replication
D) Amazon ElastiCache for Memcached deployed in Tokyo

123. A financial analytics application queries an Amazon RDS for MySQL database. Heavy reporting queries run during business hours cause high CPU utilization (98%) on the primary instance, slowing down customer transactions. The database is already configured in a Multi-AZ deployment. What should the developer do to relieve primary database load?
A) Route reporting queries to the Multi-AZ standby instance
B) Create an Amazon RDS Read Replica, configure the reporting application to query the Read Replica endpoint, and implement Amazon ElastiCache (Redis) to cache frequent query results
C) Delete the database and recreate it without Multi-AZ
D) Increase the database backup retention period to 35 days

124. A team deploys an AWS Lambda function inside a VPC to query an Amazon Aurora database. The Lambda function works properly, but when the database administrator enables IAM Database Authentication, the Lambda function fails to connect with an `Access Denied` error. What two troubleshooting steps should the developer verify? (Select TWO.)
A) Ensure the Lambda execution role has an IAM policy granting `rds-db:connect` on the target database resource ARN
B) Ensure the Lambda function generates a temporary authentication token using `generate_db_auth_token` and connects over SSL/TLS using the token as the password
C) Ensure the Lambda function is removed from the VPC
D) Ensure the Lambda memory is set to 10,240 MB
E) Ensure the database password is saved in a local file on `/tmp`

125. An architect is reviewing an application architecture with the following requirements: (1) low-latency sub-millisecond leaderboard queries with ranked scores, (2) automatic session state caching across web servers, and (3) transactional SQL relational storage with automatic failover and connection pooling for Lambda. Which set of AWS services correctly fulfills these needs?
A) Amazon ElastiCache for Redis (for leaderboard & sessions) + Amazon Aurora with Amazon RDS Proxy (for relational data & connection pooling)
B) Amazon DynamoDB only
C) Amazon RDS for SQL Server Single-AZ + Memcached
D) Amazon S3 + Amazon Athena + AWS Glue

---

## Answer Key & Explanations

1. B — DB Parameter Groups manage database engine configuration settings (e.g., `max_connections`, memory buffers, timeouts).
2. B — DB Option Groups enable engine-specific features and extensions such as Oracle Transparent Data Encryption (TDE) and Native Network Encryption.
3. B — You cannot encrypt an existing unencrypted RDS instance directly; the procedure is: snapshot the instance, copy the snapshot with KMS encryption enabled, and restore a new instance from the encrypted snapshot.
4. B — RDS Storage Auto Scaling automatically increases allocated storage capacity when free space falls below a threshold without downtime.
5. B — Provisioned IOPS SSD (io1/io2) delivers dedicated, consistent high IOPS and low-latency performance for critical I/O-intensive workloads.
6. A — Parameter Groups control engine parameters and configuration; Option Groups enable engine-specific features and bundled software options.
7. B — AWS manages infrastructure provisioning, OS patching, hardware maintenance, and automated backups; the customer manages schema, queries, and optimization.
8. A & B — Commercial engines on RDS (Oracle and SQL Server) support License Included and Bring Your Own License (BYOL) models.
9. B — Point-in-Time Recovery (PITR) restores automated backup snapshots and transaction logs to create a brand-new DB instance with a new endpoint.
10. C — The maximum configurable retention period for Amazon RDS automated backups is 35 days.
11. B — Manual DB snapshots persist in Amazon S3 independently of the instance lifecycle until explicitly deleted by the user.
12. A & B — General Purpose SSD (gp3) allows provisioning storage capacity, IOPS, and throughput (MB/s) independently of each other.
13. B — Automated backups have a 35-day limit; retaining backups for 7 years requires periodic manual snapshots or AWS Backup lifecycle policies.
14. B — Operating system patching during a maintenance window on a single-AZ instance requires an instance reboot, causing a brief period of unavailability.
15. B — Restoring a snapshot to a separate test instance allows safe validation of engine major version upgrades and regression testing without risking production.
16. B — Setting `slow_query_log = 1` in the DB parameter group and enabling CloudWatch Logs export allows continuous publishing and monitoring of slow queries.
17. A & B — PostgreSQL and MySQL are open-source engines supported on Amazon RDS without software licensing fees.
18. B — VPC Security Groups control inbound and outbound network access to the RDS DB instance at the virtual firewall layer.
19. B — A DB Subnet Group must contain subnets from at least 2 Availability Zones in the chosen Region.
20. A — Dynamic parameters take effect immediately upon saving the parameter group without requiring an instance reboot.
21. B — Amazon RDS Multi-AZ deployments provide synchronous replication to a standby instance in a different AZ with automatic DNS failover for high availability.
22. B — Read Replicas offload read-only and analytical traffic from the primary writer instance using asynchronous replication.
23. A — Multi-AZ uses synchronous replication to a passive standby for HA/failover; Read Replicas use asynchronous replication for read scaling.
24. B — During Multi-AZ failover, RDS automatically flips the canonical CNAME DNS record to point to the standby instance in the second AZ (typically <2 minutes).
25. B — In a standard Multi-AZ DB instance deployment, the standby instance is purely passive, does not accept connections, and exists strictly for failover.
26. B — Amazon RDS Cross-Region Read Replicas allow read scaling in secondary AWS Regions with asynchronous replication.
27. B — The `ReplicaLag` CloudWatch metric measures the time lag (in seconds) between the primary instance and the Read Replica.
28. B — Read Replicas do not support automatic failover; promoting a replica to an independent standalone database requires manual or scripted intervention.
29. B — Amazon RDS for MySQL and PostgreSQL support up to 5 Read Replicas per DB instance.
30. B — A Multi-AZ DB Cluster includes two readable standby instances that serve read traffic in addition to providing automated failover.
31. B — Promoting a Read Replica permanently severs replication from the primary, turning it into a standalone read-write database.
32. A & B — Multi-AZ failover updates DNS records automatically, and the standby instance resides in a different AZ in the same Region.
33. B — Offloading read queries (`SELECT`) to Read Replica endpoints while directing writes to the primary scales database throughput horizontally.
34. B — When a Read Replica runs out of storage, replication stops and the replica enters an error/storage-full state until storage is expanded.
35. A — Cross-Region Read Replicas are natively supported for MySQL, MariaDB, and PostgreSQL engines on RDS.
36. A — On Multi-AZ deployments, RDS minimizes downtime by patching the standby first, performing a brief failover, and then patching the original primary.
37. A — Read Replicas incur binary log / WAL shipping overhead on the primary and are subject to asynchronous replication lag under heavy writes.
38. A — Automated backups (backup retention period > 0) must be enabled on the primary database to enable binary logging required for Read Replicas.
39. B — AWS Secrets Manager natively integrates with RDS to store, manage, and automatically rotate database credentials via Lambda rotation templates.
40. A — Secrets Manager provides built-in automated credential rotation for RDS, Aurora, and Redshift; Parameter Store requires custom rotation logic.
41. B — Granting `secretsmanager:GetSecretValue` on the secret ARN and calling the API at connection time (caching in memory) is the secure, best-practice approach.
42. B — IAM DB Authentication uses temporary, 15-minute signed authentication tokens generated from IAM credentials and transmitted over SSL/TLS.
43. B — Authentication tokens generated for RDS IAM Database Authentication are valid for 15 minutes.
44. A — `aws rds generate-db-auth-token` generates an IAM database authentication token.
45. A & B — The IAM policy must allow `rds-db:connect` on the database resource ARN, and the DB user must be configured with `rds_iam` (PostgreSQL) or `AWSAuthenticationPlugin` (MySQL).
46. B — SSL/TLS encryption is mandatory when using IAM DB Authentication to protect the authentication token in transit.
47. B — The rotation Lambda function uses administrative master credentials stored in a separate secret to execute `ALTER USER` commands on the database.
48. B — Attaching an IAM Instance Profile (Role) granting least-privilege `secretsmanager:GetSecretValue` permission avoids embedding static credentials on the host.
49. A — Setting `rds.force_ssl = 1` in the PostgreSQL parameter group enforces SSL/TLS encryption for all client connections.
50. A & B — IAM Database Authentication is natively supported on Amazon RDS for MySQL, PostgreSQL, Aurora MySQL, and Aurora PostgreSQL.
51. B — Secrets Manager encrypts secrets at rest using AWS KMS (either the default service key or a customer-managed CMK).
52. B — The application should catch authentication errors, invalidate its cached secret, retrieve the fresh rotated secret from Secrets Manager, and retry connecting.
53. A — `rds-db:connect` with resource format `arn:aws:rds-db:<region>:<account>:dbuser:<dbi-resource-id>/<db_user>` grants granular database connection permissions.
54. B — Storing JSON structured key-value pairs enables automated rotation functions and SDKs to parse and update connection details seamlessly.
55. B — Amazon RDS Proxy pools and multiplexes database connections, preventing connection exhaustion from highly concurrent Lambda executions.
56. B — RDS Proxy maintains client connections during Multi-AZ failovers and connects to the new primary in the background, reducing failover time by up to 66%.
57. B — RDS Proxy retrieves database credentials from AWS Secrets Manager using an IAM execution role assumed by the proxy.
58. A — The client authenticates to RDS Proxy via IAM; RDS Proxy authenticates to the native database using credentials retrieved from Secrets Manager.
59. A & B — Amazon RDS Proxy supports MySQL, PostgreSQL, MariaDB, Aurora MySQL, and Aurora PostgreSQL.
60. A — Lambda execution environments are isolated; each concurrent instance creates its own connection pool, causing connection proliferation without a central proxy.
61. A — RDS Proxy must have routable private network connectivity (same VPC or peered VPC) with the target RDS database.
62. B — RDS Proxy is purely a connection pooler and multiplexer; it does not cache SQL query results (caching is ElastiCache's job).
63. A — Connection pinning occurs when session-specific state (e.g., temporary tables, prepared statements, user variables) locks a client to an underlying DB connection.
64. A — RDS Proxy enforces TLS/SSL and centralizes database credential management using Secrets Manager and IAM.
65. B — Applications only need to change their connection string endpoint to the RDS Proxy endpoint; SQL syntax and ORMs remain identical.
66. A — `DatabaseConnections` tracks the number of connections opened between RDS Proxy and the target database.
67. A — TLS requirements are configured directly in RDS Proxy under `Require Transport Layer Security (TLS)`.
68. B — RDS Proxy can be used by Lambda, EC2 instances, ECS container tasks, and any VPC-based application needing connection pooling.
69. B — Aurora features a distributed, log-structured storage volume that automatically replicates data 6 ways across 3 AZs and auto-scales up to 128 TiB.
70. B — Amazon Aurora DB clusters support up to 15 Aurora Replicas.
71. A — Aurora Replicas share the same distributed storage volume as the primary writer, eliminating the need to replay copied data streams.
72. B — Aurora automatically promotes an existing warm Aurora Replica to writer with zero data loss in under 30 seconds.
73. B — Aurora Serverless v2 auto-scales compute capacity near-instantly in fine-grained increments to handle variable and unpredictable workloads.
74. B — Aurora Serverless v2 capacity scales in Aurora Capacity Units (ACUs), where 1 ACU provides ~2 GiB RAM plus proportional CPU and networking.
75. B — Aurora clusters support mixed configurations, combining provisioned instances and Serverless v2 instances in the same cluster.
76. A — Amazon Aurora Global Database provides dedicated storage-level replication across multiple Regions with sub-second replication lag.
77. B — Aurora Global Database uses dedicated storage-level replication built into the storage tier, avoiding compute overhead and keeping lag <1 second.
78. B — In a regional disaster, a secondary Region in an Aurora Global Database can be promoted to primary read-write in under 1 minute.
79. A & B — Aurora provides a Cluster (Writer) Endpoint for read-write traffic and a Reader Endpoint that load-balances reads across replicas.
80. B — Custom Endpoints allow grouping specific subsets of Aurora Replicas for dedicated workloads (such as heavy analytical queries).
81. A & B — Amazon Aurora is fully compatible with MySQL and PostgreSQL engines.
82. C — Amazon Aurora storage automatically scales up to 128 TiB per database cluster.
83. A — The Amazon Aurora Data API allows executing SQL over a secure HTTPS REST endpoint using IAM credentials, ideal for serverless Lambda workflows.
84. A — Aurora's storage layer continuously self-heals by repairing corrupted blocks using the remaining copies across the 3 AZs.
85. B — Aurora fails over in <30 seconds (or <10 seconds with RDS Proxy) due to shared storage; standard RDS takes 60–120 seconds.
86. A — Aurora Database Cloning uses copy-on-write technology to create isolated, point-in-time database clones in minutes with no initial storage duplication.
87. A — Amazon ElastiCache provides managed in-memory caching (Redis or Memcached) delivering sub-millisecond response times.
88. B — ElastiCache for Redis natively supports Sorted Sets (ZSET) with commands like `ZADD` and `ZRANGEBYSCORE` for real-time ranked leaderboards.
89. A & B — Redis supports Multi-AZ replication with automatic failover and rich data structures (sets, sorted sets, hashes); Memcached supports neither.
90. B — Cache-Aside checks cache first; on a miss, it queries the DB, writes to the cache with a TTL, and returns the result to the caller.
91. B — Without a TTL or invalidation strategy, cached data becomes stale; setting a TTL and invalidating on write keeps data fresh.
92. B — Memcached is multithreaded and can fully utilize multiple CPU cores and memory channels on a single large node.
93. B — Enabling Cluster Mode Enabled partitions data across multiple shards, enabling horizontal scaling of both read and write capacity.
94. A — ElastiCache for Redis supports automated and manual RDB snapshots stored in Amazon S3 for backup and recovery.
95. B — Redis natively supports Pub/Sub messaging commands (`PUBLISH`/`SUBSCRIBE`) for real-time message distribution.
96. A & B — Redis security combines in-transit TLS encryption with AUTH tokens/IAM auth, and VPC Security Groups restricting access to port 6379.
97. B — Amazon ElastiCache for Redis is widely used as a fast, centralized, distributed session store for web application fleets.
98. B — During Multi-AZ failover, ElastiCache for Redis promotes a read replica to primary and updates DNS endpoints in under a minute.
99. A — The `maxmemory-policy` parameter controls eviction behavior (e.g., `allkeys-lru`, `volatile-ttl`, `noeviction`) when memory is full.
100. A — Write-Through writes to DB and cache synchronously; Lazy-Loading loads data into cache only upon read cache misses.
101. A — ElastiCache for Redis (v6.0+) supports Role-Based Access Control (RBAC) and User Groups for granular command permissions.
102. A & B — Probabilistic early expiration and mutex locking on cache misses prevent thundering-herd cache stampedes from overwhelming the database.
103. A — ElastiCache for Redis Auto Scaling uses CPU utilization and memory usage metrics to scale replicas or shards.
104. B — The default network port for Redis is 6379; the default port for Memcached is 11211.
105. B — Amazon MemoryDB for Redis is a Redis-compatible, durable, primary in-memory database with multi-AZ transactional log persistence.
106. B — MemoryDB persists writes across multiple AZs using a distributed transactional log before confirming success, guaranteeing durability.
107. A — ElastiCache is a cache tier in front of a primary database; MemoryDB is a durable primary database in its own right.
108. B — MemoryDB for Redis combines Redis microsecond performance with guaranteed multi-AZ persistence for authoritative data like inventory.
109. B — MemoryDB provides microsecond read latency from memory and single-digit millisecond write latency due to multi-AZ logging.
110. A — MemoryDB supports standard Redis data types, transactions, Pub/Sub, streams, and cluster sharding.
111. B — MemoryDB allows restoring from standard Redis RDB snapshot files stored in Amazon S3 during cluster provisioning.
112. B — For a cache placed in front of an existing Aurora database, ElastiCache for Redis is the standard, cost-effective caching solution.
113. B — Workloads requiring complex multi-table SQL `JOIN` operations, ad-hoc queries, and relational schemas are best served by Amazon RDS or Aurora.
114. B — Amazon DynamoDB provides serverless, single-digit millisecond latency at massive scale for simple key-value lookups by partition key.
115. B — Strict multi-table ACID transactions, foreign keys, and relational ORM frameworks require a relational database like Amazon Aurora or RDS.
116. A & B — DynamoDB is favored for massive horizontal scale with key-based access patterns and fully serverless, zero-maintenance operations.
117. B — DynamoDB is a schema-less document store where items in the same table can carry different attributes, accommodating evolving schemas.
118. B — Microservices best practices encourage polyglot persistence: DynamoDB/ElastiCache for session state, and Aurora PostgreSQL for transactional ledgers.
119. B — Amazon Aurora Global Database provides MySQL compatibility, auto-scaling storage up to 128 TiB, sub-second cross-Region replication, and fast failover.
120. B — DynamoDB is optimized for horizontal scaling and key-based lookups; RDS is built for complex SQL, joins, and relational integrity.
121. A — RDS Proxy resolves Lambda connection exhaustion; Secrets Manager with rotation handles 60-day password rotation; TLS enforces encryption in transit.
122. A — Aurora Global Database allows low-latency local reads in Tokyo with sub-second replication and cross-Region disaster recovery failover in <1 minute.
123. B — Adding a Read Replica offloads analytical queries, and ElastiCache caches frequent queries to relieve primary CPU load.
124. A & B — The Lambda execution role must allow `rds-db:connect`, and the function must generate an auth token and connect over SSL/TLS.
125. A — ElastiCache for Redis handles ranked leaderboards and session caching; Aurora with RDS Proxy handles relational data and connection pooling.
