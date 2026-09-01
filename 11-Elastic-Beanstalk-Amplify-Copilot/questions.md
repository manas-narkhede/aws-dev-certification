# Module 11 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Elastic Beanstalk Architecture, Environment Tiers & .ebextensions (1–30)

1. A software development team wants to deploy a Node.js web application on AWS without manually configuring VPC routing tables, Elastic Load Balancers, or Auto Scaling groups. However, the operations team requires the ability to SSH into the underlying EC2 instances to inspect logs and install custom monitoring tools when troubleshooting. Which AWS service fulfills these requirements?
A) AWS Lambda
B) AWS Elastic Beanstalk
C) Amazon S3 Static Website Hosting
D) AWS Fargate with no execution role

2. A developer is deploying a Java Spring Boot application using AWS Elastic Beanstalk. The application must process incoming HTTP requests from the public internet, distribute load across multiple Amazon EC2 instances, and automatically scale out when CPU utilization exceeds 75%. Which Elastic Beanstalk environment tier should the developer create?
A) Worker environment tier
B) Web server environment tier
C) Batch processing tier
D) Edge compute tier

3. A media processing company needs to run background video encoding jobs that take 10 to 15 minutes each. The jobs are submitted as messages to an Amazon SQS queue. The processing instances must not accept direct public internet traffic. Which Elastic Beanstalk architecture meets these requirements with the LEAST operational effort?
A) A Web server environment tier with an Application Load Balancer
B) A Worker environment tier configured with an SQS queue and the local SQS daemon
C) An Amazon CloudFront distribution routing traffic to EC2 instances
D) A Lambda function configured with a 30-second execution timeout

4. How does the Elastic Beanstalk worker daemon (SQSD) on an EC2 instance in a worker environment deliver SQS messages to the application code?
A) It writes the message to a local flat file in `/tmp`
B) It sends an HTTP POST request containing the message body to a configurable local endpoint (e.g., `http://localhost/`) on the instance
C) It opens a persistent WebSocket connection to the application process
D) It converts the message into an AWS Lambda invocation

5. A developer wants to customize an Elastic Beanstalk environment by installing an OS package (`htop`), setting custom environment variables (`NODE_ENV=production`), and creating a cron job. Where should these configuration files be placed in the application source bundle?
A) In the root directory named `config.json`
B) In a folder named `.ebextensions` at the root of the source bundle, containing `.config` files written in YAML or JSON
C) In the `/etc/aws/elasticbeanstalk` directory on an external S3 bucket
D) In the `.elasticbeanstalk/saved_configs` directory on the local developer laptop

6. An application deployed on Elastic Beanstalk requires database schema migrations to execute exactly once per deployment across a multi-instance Auto Scaling group. The developer adds a `container_commands` block in an `.ebextensions` configuration file. Which directive ensures the migration script executes on only a single instance rather than every instance in the fleet?
A) `run_once: true`
B) `leader_only: true`
C) `master: true`
D) `singleton: true`

7. What is the execution order of configuration sections in an `.ebextensions` `.config` file during an Elastic Beanstalk deployment?
A) `container_commands` run before application and web server extraction; `commands` run after
B) `commands` run early in the setup process before the application source code is unpacked; `container_commands` run after the application source code has been extracted to the staging directory
C) `container_commands` and `commands` execute in parallel
D) `container_commands` run only during instance termination

8. A developer wants to declare an additional Amazon SQS Dead-Letter Queue directly within an Elastic Beanstalk environment definition so that it is provisioned automatically alongside the environment. How can this be accomplished?
A) It is impossible; Elastic Beanstalk cannot manage additional AWS resources
B) Add a `Resources:` section in an `.ebextensions/*.config` file containing the standard CloudFormation resource definition for `AWS::SQS::Queue`
C) Write a custom shell script in `cron.yaml`
D) Use the EB CLI command `eb sqs create-queue`

9. An operations engineer wants to capture an existing Elastic Beanstalk environment’s settings (instance type, environment variables, scaling triggers) to replicate the identical configuration across multiple staging and production environments. Which Elastic Beanstalk feature should the engineer use?
A) Application Version Lifecycle Policy
B) Saved Configurations
C) CloudWatch Metric Filters
D) Elastic Beanstalk CNAME swap

10. A developer needs to configure scheduled periodic tasks (e.g., running a cleanup job every midnight) in an Elastic Beanstalk worker environment. What file must be included in the root of the application source bundle?
A) `scheduled_tasks.json`
B) `cron.yaml`
C) `.ebextensions/cron.config` with root crontab syntax only
D) `Procfile`

11. Which file can be placed in the root directory of an Elastic Beanstalk source bundle to override the default application startup command on platforms like Node.js, Python, or Go?
A) `Startup.sh`
B) `Procfile`
C) `manifest.yml`
D) `AppSpec.yml`

12. A developer is deploying a single Docker container to AWS Elastic Beanstalk. What file in the source bundle tells Elastic Beanstalk how to build or pull the container image?
A) A `Dockerfile` or a `Dockerrun.aws.json` file placed in the root of the source bundle
B) `buildspec.yml`
C) `template.yaml`
D) `task-definition.json`

13. An application running on Elastic Beanstalk needs to connect to an Amazon RDS database. The developer is deciding whether to provision the RDS database directly inside the Elastic Beanstalk environment or provision it externally and pass the connection string via environment variables. What is the primary disadvantage of creating the RDS database inside the Elastic Beanstalk environment for production workloads?
A) The database cannot use Multi-AZ replication
B) If the Elastic Beanstalk environment is terminated or deleted, the RDS database instance is automatically terminated and deleted with it
C) Elastic Beanstalk does not support PostgreSQL databases
D) The database can only be accessed by one EC2 instance at a time

14. A development team wants to deploy application updates using the EB CLI (`eb`). Which command initializes a local directory as an Elastic Beanstalk application workspace and configures the default Region and platform?
A) `eb create`
B) `eb init`
C) `eb config`
D) `eb deploy`

15. What are the two distinct IAM roles required for an Elastic Beanstalk environment to function properly? (Select TWO.)
A) A Service Role that Elastic Beanstalk assumes to create, monitor, and manage AWS resources (ELB, ASG, EC2) on your behalf
B) An EC2 Instance Profile role attached to the underlying EC2 instances, granting them permissions to download application bundles from S3, write logs to CloudWatch, and communicate with SQS
C) An Amazon Cognito Identity Pool Role for guest access
D) An AWS Organizations Master Account Role
E) An IAM User with root administrator privileges

16. A company has deployed an application on Elastic Beanstalk. The operations team notices that the environment health status changes to Yellow (Degraded) and then Red (Severe). Which feature of Elastic Beanstalk provides detailed OS-level metrics, latency percentiles, and application HTTP status code breakdowns directly in the console for troubleshooting?
A) Basic Health Reporting
B) Enhanced Health Reporting
C) AWS CloudTrail Data Events
D) Amazon Inspector

17. How does Elastic Beanstalk collect Enhanced Health metrics from EC2 instances in an environment?
A) By running port scans against the instance public IP
B) By running an Elastic Beanstalk Health Agent daemon on each EC2 instance that gathers OS and web server metrics and publishes them to the Elastic Beanstalk health service
C) By executing an AWS Lambda function every 5 seconds
D) By parsing VPC Flow Logs

18. A developer wants to configure environment variables for an Elastic Beanstalk application using `.ebextensions`. Which namespace should be specified in the `.config` file?
A) `aws:elasticbeanstalk:container:nodejs`
B) `aws:elasticbeanstalk:application:environment`
C) `aws:autoscaling:environment`
D) `aws:ec2:env:variables`

19. A developer runs `eb logs` from the terminal. What information does the EB CLI retrieve by default from the target environment?
A) The full database binlog stream
B) The last 100 lines of standard log files from the EC2 instances (such as `/var/log/eb-engine.log`, `/var/log/nginx/error.log`, or application logs)
C) The AWS CloudTrail management event history for the past 90 days
D) Real-time network packet captures from the Elastic Load Balancer

20. When creating an Elastic Beanstalk web server environment that requires high availability and automatic scaling, which environment type should be selected?
A) Single-instance environment
B) Load-balanced, autoscaling environment
C) Serverless environment
D) Dedicated Host cluster

21. A developer is deploying a single-instance Elastic Beanstalk environment for a dev testing sandbox. What network and compute resources are created in a single-instance environment?
A) An Application Load Balancer and an Auto Scaling group with minimum size 1
B) A single EC2 instance with an Elastic IP address, with no load balancer provisioned
C) A fleet of spot instances behind a Network Load Balancer
D) An AWS Fargate cluster with an API Gateway endpoint

22. What happens to the application source code when a developer runs `eb deploy` in a git-initialized repository?
A) The EB CLI creates a zip archive of the committed git repository files (or staged files), uploads it to an S3 bucket managed by Elastic Beanstalk, creates a new Application Version, and deploys it to the environment
B) The EB CLI commits the code directly to an Amazon EFS mount point
C) The EB CLI recompiles the Linux kernel on the EC2 instances
D) The EB CLI pushes the code directly to a GitHub public repository

23. A developer wants to customize the Nginx reverse proxy configuration on an Elastic Beanstalk Amazon Linux 2 platform. What is the standard AWS-recommended directory to place custom Nginx configuration files?
A) `.ebextensions/nginx.conf`
B) `.platform/nginx/conf.d/` in the application source bundle
C) `/etc/httpd/conf.d/`
D) `/root/nginx/`

24. What is the difference between `.ebextensions/` and `.platform/` in Elastic Beanstalk on Amazon Linux 2 platforms?
A) `.ebextensions/` is used for resource provisioning and general option settings; `.platform/` provides platform hooks and web server configuration overrides (Nginx/Apache) that run at specific lifecycle stages
B) `.platform/` is deprecated and replaced by `.ebextensions/`
C) `.platform/` only works on Windows Server instances
D) `.ebextensions/` can only contain JSON files, while `.platform/` only accepts XML

25. A developer wants to execute custom bash scripts during specific deployment phases on Amazon Linux 2 Beanstalk environments (e.g., `prebuild`, `predeploy`, `postdeploy`). Where should these scripts be located in the source bundle?
A) `.platform/hooks/prebuild/`, `.platform/hooks/predeploy/`, and `.platform/hooks/postdeploy/`
B) `/usr/bin/hooks/`
C) `.ebextensions/hooks/`
D) `scripts/deployment/`

26. An organization enforces a compliance policy that all EC2 instances must have IMDSv2 (Instance Metadata Service Version 2) required with token hop limit 1. How can this setting be enforced across all instances in an Elastic Beanstalk environment?
A) Modify the setting in `.ebextensions` under the `aws:autoscaling:launchconfiguration` namespace by setting `DisableIMDSv1: true`
B) Reboot each EC2 instance manually
C) Disable the Elastic Load Balancer
D) Delete the IAM Instance Profile

27. A developer is testing an Elastic Beanstalk application and wants to temporarily SSH into an instance. Which EB CLI command automates opening the SSH connection, configuring the security group rule if necessary?
A) `eb connect`
B) `eb ssh`
C) `eb open-port 22`
D) `eb terminal`

28. When an Elastic Beanstalk worker environment daemon encounters an HTTP 500 error returned by the local application when processing an SQS message, what does the daemon do?
A) It permanently deletes the message from SQS
B) It leaves the message in SQS (or does not delete it), allowing the SQS visibility timeout to expire so the message becomes visible again for retry, eventually moving to a Dead-Letter Queue if configured
C) It reboots the EC2 instance immediately
D) It converts the message into an email alert via Amazon SES

29. A developer wants to deploy an Elastic Beanstalk application using a pre-built zip file located in an S3 bucket via the AWS CLI. What two API calls are required? (Select TWO.)
A) `aws elasticbeanstalk create-application-version` referencing the S3 bucket and object key
B) `aws elasticbeanstalk update-environment` specifying the environment name and the newly created `VersionLabel`
C) `aws ec2 create-image`
D) `aws cloudformation delete-stack`
E) `aws s3 sync` to the root directory of the EC2 instance

30. Which statement accurately describes the underlying infrastructure created by AWS Elastic Beanstalk?
A) Elastic Beanstalk uses a proprietary, non-AWS hypervisor
B) Elastic Beanstalk generates standard AWS resources (CloudFormation stack, EC2, ASG, ELB, CloudWatch) that can be inspected, monitored, and modified using standard AWS management tools
C) Elastic Beanstalk instances run exclusively in AWS-owned VPCs that are invisible to the customer
D) Elastic Beanstalk resources cannot be tagged

---

### Beanstalk Deployment Policies & Version Lifecycles (31–60)

31. A company needs to deploy an updated version of a mission-critical web application on Elastic Beanstalk. The application currently runs on 4 EC2 instances. The deployment must maintain 100% full capacity (4 healthy instances) at all times during the deployment, and cannot tolerate any reduction in available compute instances. Which deployment policy should the developer select?
A) All at once
B) Rolling
C) Rolling with additional batch
D) Re-create

32. An e-commerce platform uses Elastic Beanstalk. The team wants the fastest possible deployment mechanism during a scheduled maintenance window where a brief period of total downtime is acceptable. Which deployment policy is the most suitable?
A) All at once
B) Rolling with additional batch
C) Immutable
D) Traffic splitting

33. A developer selects the Rolling deployment policy for an Elastic Beanstalk environment with 4 EC2 instances and a batch size of 2. What happens to the environment's total serving capacity during the rollout of the new version?
A) Serving capacity remains at 100% because 2 new instances are launched first
B) Serving capacity is reduced to 50% (2 instances) while the first batch of 2 instances is updated, then restored as each batch finishes
C) All 4 instances are taken offline simultaneously
D) Serving capacity doubles to 8 instances throughout the process

34. A financial application requires a deployment strategy that guarantees zero downtime, maintains full capacity, creates an entirely new Auto Scaling group for the new version, and allows instantaneous rollback by simply terminating the new Auto Scaling group if health checks fail. Which deployment policy meets these requirements?
A) All at once
B) Rolling
C) Immutable
D) Single-Instance in-place

35. How does an Immutable deployment in Elastic Beanstalk verify the health of the new application version before affecting production traffic?
A) It prompts the developer to click "Approve" in the AWS Management Console
B) It launches a single temporary instance in a new Auto Scaling group, deploys the new version, tests it against health checks, and if healthy, launches the remaining instances in the new group before shifting the load balancer and terminating the old group
C) It runs unit tests in AWS CodeBuild
D) It deploys to an S3 bucket and verifies file hashes

36. A development team wants to deploy a new version to an Elastic Beanstalk environment and direct 10% of live user traffic to the new version for 15 minutes to monitor error rates in CloudWatch before promoting the version to 100% of the fleet. Which deployment policy provides this canary testing capability?
A) Traffic splitting
B) All at once
C) Rolling with additional batch
D) Re-create

37. A company needs to deploy a major version upgrade of a web application on Elastic Beanstalk that includes breaking database schema changes and a new major platform runtime. The team wants to test the new environment independently with a dedicated URL before switching live production traffic, and requires the ability to roll back immediately if issues occur. Which deployment method is recommended?
A) All at once deployment to the existing environment
B) Create a second, independent Elastic Beanstalk environment running the new version, perform testing on its unique CNAME, and then use the Elastic Beanstalk "Swap Environment URLs" (CNAME swap) feature to redirect live traffic
C) Rolling deployment with a batch size of 1
D) Modify the Launch Configuration AMI directly on running instances

38. What mechanism does Elastic Beanstalk use to execute a "Swap Environment URLs" operation between two environments in the same application?
A) It deletes the old environment's EC2 instances and launches new ones in the new environment
B) It performs an atomic DNS CNAME record swap in Route 53 / Elastic Beanstalk DNS, swapping the public URLs assigned to the two environments
C) It copies all EBS root volumes between environments
D) It reassigns the Elastic IP addresses of the individual EC2 instances

39. What is a key prerequisite when performing a CNAME swap between two Elastic Beanstalk environments connected to an Amazon RDS database?
A) The RDS database must be created inside the source Elastic Beanstalk environment
B) The RDS database must be an external database (decoupled from both environments) so that both the existing and new environments can connect to it independently without data migration during the swap
C) The database must be converted to DynamoDB
D) Both environments must run on Windows Server

40. An automated CI/CD pipeline deploys new application versions to Elastic Beanstalk 20 times per day. After several months, the pipeline begins failing with an error indicating that the application version quota has been reached. What is the root cause and the recommended solution?
A) Elastic Beanstalk accounts have a limit on total application versions (default 1,000 per region); configure an Application Version Lifecycle Policy to automatically delete old, unused application versions by age or count
B) S3 storage is full; upgrade S3 account capacity
C) EC2 instance limit reached; request a vCPU limit increase
D) The pipeline IAM role has expired; generate new access keys

41. When configuring an Elastic Beanstalk Application Version Lifecycle Policy, what option should be enabled to prevent deleting an application version that is actively running on a live environment?
A) `Delete source bundle from S3`
B) `Retain versions currently deployed to environments` (or `Keep source bundle in S3 if deployed`)
C) `Enable Multi-AZ deletion`
D) `Force delete active versions`

42. A developer initiates a deployment to an Elastic Beanstalk environment using the Immutable deployment policy. During the deployment, the health check on the newly launched test instance fails repeatedly with HTTP 500 errors. What automated action does Elastic Beanstalk take?
A) It continues the deployment and terminates the old healthy instances
B) It rolls back the deployment by terminating the new Auto Scaling group and temporary instances, leaving the original Auto Scaling group and production traffic completely unaffected
C) It reboots the Elastic Load Balancer
D) It deletes the entire Elastic Beanstalk application

43. Which two deployment policies in AWS Elastic Beanstalk result in temporary additional infrastructure costs during the rollout process? (Select TWO.)
A) All at once
B) Rolling with additional batch
C) Immutable
D) Rolling (standard without additional batch)
E) Re-create

44. A developer wants to roll back an Elastic Beanstalk environment to a previous stable release after a buggy version was deployed. What is the fastest and cleanest way to perform this rollback in Elastic Beanstalk?
A) Re-deploy the previously successful Application Version label to the environment via the console or `eb deploy --version <label>`
B) Manually SSH into each instance and use `git checkout`
C) Terminate all EC2 instances and let Auto Scaling recreate them from the same bad AMI
D) Delete the Elastic Beanstalk application and rebuild from scratch

45. How does Elastic Beanstalk determine if an instance in an updated batch is healthy before proceeding to the next batch during a Rolling deployment?
A) By checking if the instance has been powered on for 60 seconds
B) By waiting for the load balancer health checks to report the instance as `InService` (Healthy) and meeting the configured Command Timeout and Health Check thresholds
C) By sending an email to the AWS account administrator
D) By inspecting the git commit log on the instance

46. What parameter in Elastic Beanstalk rolling deployment configuration determines whether batches are calculated as a fixed number of instances or a percentage of the total fleet size?
A) `BatchSizeType` (`Fixed` or `Percentage`)
B) `RollingPolicyMode`
C) `InstanceScaleFactor`
D) `DeploymentStepSize`

47. A developer configures an Elastic Beanstalk environment with a Rolling deployment policy. The batch size is set to 50% and the Minimum Instances in Service is set to 50%. The fleet has 4 instances. How many instances are updated in the first batch?
A) 1 instance
B) 2 instances
C) 4 instances
D) 0 instances

48. A developer wants to test a new version of an application on Elastic Beanstalk with zero downtime and no DNS TTL propagation delay. The developer is considering between an Immutable deployment and a Blue/Green CNAME swap. What is a key advantage of an Immutable deployment over a CNAME swap?
A) Immutable deployments do not require maintaining or creating a second independent Elastic Beanstalk environment with separate configurations and URLs
B) Immutable deployments never launch new EC2 instances
C) Immutable deployments do not use CloudFormation
D) Immutable deployments are 100% free of charge

49. What happens if a CNAME swap is executed between two environments located in different AWS Regions?
A) The swap succeeds in under 1 second
B) Elastic Beanstalk does not support CNAME swaps between environments in different Regions; both environments must reside in the same Region and application
C) The instances in both Regions are merged into a single VPC
D) The source environment is migrated to S3 Glacier

50. A company deploys an update to an Elastic Beanstalk environment using the Traffic Splitting deployment policy with an evaluation period of 10 minutes and a 15% traffic split. During the 10-minute evaluation, CloudWatch alarms report a spike in 5xx errors from the canary instances. What occurs automatically?
A) Elastic Beanstalk shifts 100% of traffic to the canary instances
B) Elastic Beanstalk automatically cancels the deployment, routes 100% of traffic back to the original instances, and terminates the canary instances
C) Elastic Beanstalk disables all health checks
D) Elastic Beanstalk reboots the primary RDS database

51. Which deployment policy should be avoided for production environments that require continuous availability and cannot tolerate reduced capacity during peak traffic hours?
A) Rolling with additional batch
B) Immutable
C) All at once (and standard Rolling if capacity is tightly provisioned)
D) Traffic splitting

52. In an Elastic Beanstalk application, an Application Version artifact consists of which component?
A) A complete virtual machine disk image (.vmdk)
B) A zip file (or WAR/JAR) containing the application source code and deployment descriptors stored in an Amazon S3 bucket managed by Elastic Beanstalk
C) A Docker daemon binary
D) An AWS CloudTrail log file

53. An operations engineer wants to configure automated health checks for an Elastic Beanstalk application behind an Application Load Balancer. Where is the health check path (e.g., `/health`) configured?
A) In `.ebextensions` under the `aws:elasticbeanstalk:environment:process:default` namespace with `HealthCheckPath: /health`
B) In `route53.json`
C) In the database connection pool settings
D) In the local `package.json` file only

54. A team uses Elastic Beanstalk for a microservices architecture. When deploying updates to a service, the team notices that deployments take over 25 minutes because health checks take a long time to stabilize. What setting can be tuned in Elastic Beanstalk deployment options to adjust the maximum wait time for an instance to become healthy before failing?
A) `Timeout` in `aws:elasticbeanstalk:command` namespace
B) `TTL` in Route 53
C) `MaxDuration` in AWS Lambda
D) `RetentionPeriod` in Amazon SQS

55. Can an Elastic Beanstalk environment be cloned to create a replica with identical configuration settings?
A) No, cloning is not supported in Elastic Beanstalk
B) Yes, the "Clone Environment" feature provisions a new environment with the same platform, environment variables, tier, and resource configuration as the original
C) Yes, but only if the application is written in PHP
D) No, cloning requires an AWS Support ticket

56. A developer wants to re-deploy the currently deployed version to an Elastic Beanstalk environment without uploading a new source bundle (e.g., to re-run configuration scripts). Which action in the Elastic Beanstalk console or CLI achieves this?
A) `eb rebuild` or "Rebuild Environment"
B) `eb terminate`
C) `eb delete`
D) `eb clone`

57. What is the effect of the "Rebuild Environment" action in AWS Elastic Beanstalk?
A) It deletes the application version from S3
B) It terminates all running resources (EC2 instances, ELB, Auto Scaling group) and provisions brand new resources from scratch using the saved configuration and current application version
C) It converts the environment to AWS Lambda
D) It renames the AWS account

58. Why is it recommended to decouple state (such as user session data and file uploads) from the EC2 instances in an Elastic Beanstalk environment?
A) EC2 instances in an Elastic Beanstalk Auto Scaling group are ephemeral and can be terminated during scaling in, deployments, or health replacement; storing state in external services like ElastiCache, DynamoDB, or S3 prevents data loss
B) Elastic Beanstalk instances do not have local hard drives
C) Local session storage disables SSL/TLS
D) Storing files locally doubles network latency

59. A developer is deploying a containerized application to Elastic Beanstalk using a multi-container Docker environment. What configuration file defines the container composition and port mappings?
A) `Dockerrun.aws.json` (v2) specifying container definitions, memory allocations, and port mappings
B) `docker-compose.yml` only
C) `Dockerfile.prod`
D) `Kubernetes.yaml`

60. An application deployed on Elastic Beanstalk uses Rolling deployments with a batch size of 1 on a 2-instance fleet. If the deployment to Instance 1 fails, what is the state of the deployment?
A) Elastic Beanstalk immediately updates Instance 2 anyway
B) Elastic Beanstalk halts the deployment, marks the command as failed, and leaves Instance 2 running the old stable version while Instance 1 remains in the failed/unhealthy state for investigation
C) Elastic Beanstalk deletes the Auto Scaling group
D) Elastic Beanstalk triggers an immutable deployment

---

### AWS Amplify Framework, CLI & Client Libraries (61–85)

61. A frontend development team is building a single-page React web application that needs user authentication, a GraphQL API, and cloud file storage. The team has no dedicated backend or cloud infrastructure engineers. Which AWS full-stack framework and developer toolchain is specifically designed to accelerate building, configuring, and deploying this architecture?
A) AWS Cloud9
B) AWS Amplify
C) AWS OpsWorks
D) Amazon EMR

62. A developer uses the AWS Amplify CLI to add user registration and login functionality (including email verification and multi-factor authentication) to a mobile application. Which Amplify CLI command provisions these authentication resources?
A) `amplify add api`
B) `amplify add auth`
C) `amplify add storage`
D) `amplify add hosting`

63. Which underlying AWS security and directory service is automatically provisioned and configured when a developer executes `amplify add auth`?
A) AWS Identity and Access Management (IAM) Identity Center
B) Amazon Cognito (User Pools and Identity Pools)
C) AWS Directory Service for Microsoft Active Directory
D) Amazon GuardDuty

64. A developer executes `amplify add api` and selects "GraphQL". Which managed AWS service is provisioned to host the GraphQL API endpoint, resolvers, and connected data sources?
A) Amazon API Gateway
B) AWS AppSync
C) Amazon CloudFront
D) Amazon SNS

65. After defining new backend features locally using the Amplify CLI (`amplify add auth`, `amplify add api`), what command must the developer run to provision and update the actual cloud resources in AWS?
A) `amplify build`
B) `amplify push`
C) `amplify deploy-backend`
D) `amplify commit`

66. What technology does the AWS Amplify CLI use behind the scenes to generate, orchestrate, and deploy backend infrastructure stacks in a repeatable manner?
A) HashiCorp Terraform
B) AWS CloudFormation
C) Ansible playbooks
D) Bash scripts running on EC2 instances

67. A mobile developer is using the AWS Amplify JavaScript client library to manage user sessions. How does the Amplify `Auth` category simplify authentication code in the client application?
A) It bypasses authentication completely in development
B) It provides high-level methods (e.g., `Auth.signUp`, `Auth.signIn`, `Auth.currentAuthenticatedUser`) that automatically handle JWT token acquisition, local secure storage, and token refresh against Amazon Cognito
C) It stores user passwords in plain text in browser cookies
D) It routes all user passwords through an unencrypted SQS queue

68. A developer wants to enable users to upload and download profile images from an S3 bucket in a React Native app. Which AWS Amplify library category provides simple APIs for managing files in Amazon S3?
A) `Amplify.Analytics`
B) `Amplify.Storage` (e.g., `Storage.put`, `Storage.get`, `Storage.remove`)
C) `Amplify.PubSub`
D) `Amplify.Predictions`

69. A mobile application needs to provide a seamless offline experience: users must be able to read and write data when disconnected from the internet, and the application must automatically synchronize changes and resolve data conflicts with the backend database when connectivity is restored. Which AWS Amplify feature provides this local-first, offline synchronization?
A) Amplify DataStore (backed by AWS AppSync and Amazon DynamoDB)
B) Amplify S3 Static Sync
C) Amplify CloudWatch Insights
D) AWS DataSync

70. How does Amplify DataStore detect and resolve data conflicts between multiple clients that modify the same record while offline?
A) It deletes both records to prevent corruption
B) It uses conflict resolution strategies configured in AWS AppSync (such as Automerge, Optimistic Concurrency, or custom Lambda resolver logic) using record versioning metadata (`_version`, `_lastChangedAt`, `_deleted`)
C) It halts the client application until an administrator manually intervenes
D) It overrides all server records with the oldest client timestamp

71. A developer is configuring the build settings for an AWS Amplify application. Where are the frontend build phases, build commands, and output artifact directories defined?
A) In `buildspec.yml`
B) In `amplify.yml`
C) In `package.json`
D) In `template.yaml`

72. In an `amplify.yml` build configuration file, what does the `frontend.artifacts.baseDirectory` property specify?
A) The directory containing the git source code repository
B) The output directory holding the compiled, production-ready static assets (e.g., `build`, `dist`, or `.next`) that Amplify Hosting should publish to the CDN
C) The location of the local Node.js executable
D) The S3 bucket ARN for database backups

73. A developer wants to speed up build times in AWS Amplify Hosting CI/CD builds by persisting the `node_modules` directory across builds. What section of `amplify.yml` enables this caching?
A) `frontend.cache.paths`
B) `backend.storage.cache`
C) `global.performance.fast_build`
D) `cache.control.headers`

74. An engineer runs `amplify status` from the terminal. What information does the Amplify CLI output?
A) Real-time CPU utilization of backend Lambda functions
B) A summary table listing all configured backend categories (Auth, API, Storage, Function), their resource names, operation status (`Create`, `Update`, `No Change`), and the current environment name
C) The monthly AWS billing invoice
D) The git commit history of the main branch

75. How can multiple developers on the same team collaborate on backend features without interfering with each other's AWS cloud resources when using the Amplify CLI?
A) All developers must share a single root AWS account credential
B) Each developer creates their own isolated Amplify backend environment using `amplify env add <env_name>` (e.g., `amplify env add alice_dev`), which provisions a dedicated set of CloudFormation stacks in AWS
C) Developers are not allowed to use Amplify simultaneously
D) Developers must export CloudFormation templates and edit them manually

76. A developer wants to switch their local Amplify CLI workspace to an existing shared backend environment named `staging`. Which command should they execute?
A) `amplify env checkout staging`
B) `amplify checkout staging`
C) `amplify switch staging`
D) `amplify pull staging`

77. An application built with Amplify requires custom server-side business logic to run in response to a REST API endpoint. Which Amplify CLI command adds a serverless AWS Lambda function to the backend project?
A) `amplify add function`
B) `amplify add compute`
C) `amplify add lambda`
D) `amplify add serverless`

78. A developer wants to pull down the cloud backend metadata and generated configuration files (`aws-exports.js` or `amplifyconfiguration.json`) into a new local project workspace. Which command achieves this?
A) `amplify fetch`
B) `amplify pull`
C) `amplify clone`
D) `amplify download`

79. What is the role of the auto-generated `aws-exports.js` (or `amplifyconfiguration.json`) file in an Amplify client project?
A) It contains the root AWS account password
B) It contains the client-side configuration parameters (Cognito User Pool ID, AppSync GraphQL endpoint URL, S3 Bucket name, Region) that initialize the Amplify client libraries (`Amplify.configure(awsExports)`)
C) It stores database encryption keys
D) It acts as the Docker entrypoint script

80. A developer wants to add real-time, bidirectional messaging to a web app using GraphQL subscriptions in AWS Amplify. Which Amplify category and client method handle listening for new data in real time?
A) `Amplify.Auth.subscribe`
B) `API.graphql(graphqlOperation(subscriptionQuery)).subscribe({ next: (data) => ... })`
C) `Amplify.Storage.listen`
D) `Amplify.Analytics.stream`

81. A company’s frontend team wants to use the AWS Amplify Studio visual interface to model data types and generate React UI components directly from Figma designs. How does Amplify Studio persist data models created in the visual builder?
A) It saves them as XML files on EC2 instances
B) It converts the data models into a GraphQL schema (`schema.graphql`) and generates the corresponding CloudFormation stacks and DynamoDB tables via Amplify CLI integration
C) It exports them to a local SQLite database
D) It posts them to a public Slack channel

82. Which command in the Amplify CLI creates mock backend services (AppSync GraphQL API, DynamoDB, Lambda) locally on a developer’s workstation for offline testing without deploying to AWS?
A) `amplify mock`
B) `amplify test-local`
C) `amplify emulate`
D) `amplify dev`

83. A developer wants to configure fine-grained access control on an Amplify GraphQL schema so that only the owner (the user who created the record) can read, update, or delete their own posts. Which Amplify GraphQL authorization directive should be used on the model?
A) `@auth(rules: [{ allow: owner }])`
B) `@permission(type: private)`
C) `@security(role: user)`
D) `@access(level: owner_only)`

84. An Amplify project needs to allow unauthenticated (guest) users to read blog posts, but requires authenticated users (via Cognito) to create posts. Which Amplify authorization rule configuration achieves this?
A) `@auth(rules: [{ allow: public, operations: [read] }, { allow: private, operations: [create, read, update, delete] }])`
B) `@auth(rules: [{ allow: all }])`
C) `@auth(rules: [{ allow: admin }])`
D) `@auth(rules: [{ allow: root }])`

85. A developer is migrating an Amplify application from one AWS account to another. What is the cleanest approach using the Amplify CLI?
A) Manually copy the CloudFormation JSON templates from the AWS Console
B) Initialize the project in the new account using `amplify init` with the target account's AWS credentials, and run `amplify push` to deploy the entire backend stack into the new account
C) Use AWS DataSync to copy the Lambda functions
D) Re-type all code from scratch

---

### Amplify Hosting, Branch Environments & Ephemeral Previews (86–100)

86. A company hosts a Next.js web application using AWS Amplify Hosting. The repository is connected to GitHub. When a developer pushes code to the `main` Git branch, what actions does Amplify Hosting perform automatically?
A) It sends an email to the AWS account owner requesting manual deployment approval
B) It automatically triggers a managed CI/CD build pipeline, executes the build commands defined in `amplify.yml`, and deploys the resulting static assets and SSR Lambda functions to a globally distributed CDN
C) It converts the Next.js app to an EC2 AMI
D) It deploys the application to an Elastic Beanstalk worker tier

87. In AWS Amplify Hosting, what is the relationship between connected Git branches and deployed application environments (matching the official exam concept of "Amplify branches")?
A) All Git branches share a single production URL and overwrite each other's deployments
B) Each connected Git branch (e.g., `main`, `staging`, `dev`, `feature-x`) is automatically mapped to an independent, isolated web hosting environment with its own unique, globally accessible URL
C) Only the `main` branch can ever be deployed in Amplify Hosting
D) Branches can only be deployed to local developer laptops

88. A development team wants to configure per-branch backend environments in Amplify Hosting. When code is pushed to the `develop` Git branch, the frontend should connect to a dedicated `dev` backend environment (Cognito, AppSync, DynamoDB), while the `main` branch connects to the `prod` backend environment. How is this configured in Amplify Hosting?
A) By hardcoding backend URLs in JavaScript source code
B) By linking the `develop` frontend branch to the `dev` Amplify backend environment in the Amplify Hosting console settings
C) By deleting the `prod` environment whenever `develop` is updated
D) By creating two separate AWS accounts for every Git branch

89. A software team wants to review frontend visual changes for every Pull Request (PR) submitted to their GitHub repository before the PR is merged into `main`. Which feature of AWS Amplify Hosting automatically provisions an ephemeral, fully functioning deployment environment for each opened PR?
A) Amplify Ephemeral Storage
B) Amplify Web Previews (Pull Request Previews)
C) Route 53 Weighted Routing
D) CodeDeploy Blue/Green Canary

90. What happens to the ephemeral preview environment created by Amplify Hosting when a Pull Request in GitHub is closed or merged?
A) The preview environment remains online forever and incurs continuous hosting fees
B) Amplify Hosting automatically tears down and deletes the ephemeral preview deployment and releases its associated resources
C) The preview environment is archived to an S3 Glacier vault
D) The preview environment is promoted to production immediately

91. A developer wants to restrict access to a staging environment hosted on AWS Amplify Hosting so that external users cannot view work-in-progress features. Which Amplify Hosting feature provides quick access control without writing custom authentication code?
A) Access Control Lists (ACLs) in S3
B) Amplify Hosting Password Protection (Basic HTTP Authentication) enabled on the specific branch
C) AWS WAF Rate Limiting rules only
D) IAM User credentials required on every HTTP GET request

92. A single-page application (SPA) built with Vue.js is hosted on AWS Amplify Hosting. When users refresh the page on deep routes like `/dashboard/analytics`, they receive an HTTP 404 error because the static file does not exist at that path. How can this be resolved in Amplify Hosting?
A) Upload dummy HTML files for every route in the application
B) Configure a Redirect/Rewrite rule in Amplify Hosting with Source: `</^[^.]+$|\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|woff2|ttf|map|json)$)([^.]+$)/>`, Target: `/index.html`, and Type: `200 (Rewrite)`
C) Switch the hosting provider to Amazon EBS
D) Disable client-side routing in Vue.js

93. A company purchases a custom domain `www.example.com` through Amazon Route 53. How does Amplify Hosting support custom domains and SSL/TLS certificates?
A) Developers must purchase an SSL certificate from an external third-party vendor and manually install it on EC2 instances
B) Amplify Hosting provides managed custom domain configuration with automatic issuance and auto-renewal of free SSL/TLS certificates via AWS Certificate Manager (ACM)
C) Amplify Hosting only supports HTTP on custom domains
D) Custom domains require setting up an Application Load Balancer in front of Amplify Hosting

94. A developer needs to pass environment variables (such as `API_URL` or `FEATURE_FLAG_ENABLED`) to the frontend build process in Amplify Hosting. Where should these variables be defined?
A) Hardcoded in the Git repository's `README.md`
B) In the Amplify Console under App Settings > Environment Variables, configurable globally or overridden per branch
C) In the browser's local storage
D) In a public S3 bucket

95. How does AWS Amplify Hosting distribute static web content to achieve low latency and high availability for global end users?
A) By serving all requests directly from a single EC2 instance in `us-east-1`
B) By automatically leveraging Amazon CloudFront's global content delivery network (CDN) of edge locations
C) By replicating the S3 bucket to 50 AWS Regions manually
D) By sending static assets via Amazon SES email attachments

96. A company wants to run server-side rendered (SSR) React components using Next.js on AWS Amplify Hosting. How does Amplify Hosting execute the server-side rendering logic?
A) By launching a fleet of dedicated EC2 instances running Node.js
B) By automatically provisioning and executing managed AWS Lambda compute functions at edge/regional locations for SSR routes while serving static assets via CloudFront
C) By converting the Next.js application into static HTML files only
D) By running Docker containers on Amazon EKS

97. An operations engineer wants to configure notifications (e.g., Slack or email alerts) whenever an Amplify Hosting build succeeds or fails. Which integration does Amplify Hosting use for build status notifications?
A) AWS CloudTrail and AWS Glue
B) Amazon SNS topic integration / Amplify Email Notifications configurable in App Settings
C) SQS Dead-Letter Queues only
D) Amazon Inspector

98. A developer wants to trigger an Amplify Hosting build manually or from an external webhook (e.g., from a headless CMS like Contentful when content is published). What feature of Amplify Hosting enables external build triggering?
A) Incoming Webhooks (a unique POST URL generated in Amplify Hosting)
B) Amazon RDS Triggers
C) S3 Select
D) AWS CodeStar Notifications

99. In an enterprise setting, an auditor requires all web traffic to the Amplify-hosted application to pass through custom security rules that block common SQL injection and cross-site scripting (XSS) attacks. Which AWS security service integrates directly with Amazon CloudFront and AWS Amplify Hosting to enforce these rules?
A) AWS Shield Standard and AWS WAF (Web Application Firewall)
B) AWS KMS
C) AWS Secrets Manager
D) Amazon Macie

100. A developer observes that changes pushed to a feature branch (`feature-login`) are not automatically building in Amplify Hosting. What is the most likely reason?
A) The `feature-login` branch has not been connected to Amplify Hosting in the console (branch auto-detection / connected branches setting)
B) Amplify only supports branches named `main`
C) Git does not support feature branches
D) The developer must run `amplify push` from every client machine

---

### AWS Copilot CLI, Service Types, manifest.yml & Pipelines (101–125)

101. A backend engineering team has packaged their microservices into Docker container images. They want to deploy these containers to Amazon ECS on AWS Fargate without authoring thousands of lines of CloudFormation or managing ECS Task Definitions, Service Definitions, and Application Load Balancers by hand. Which official AWS CLI tool provides this high-level container management experience?
A) AWS SAM CLI
B) AWS Copilot CLI
C) AWS Elastic Beanstalk CLI (`eb`)
D) AWS Amplify CLI

102. What is the fundamental architecture pattern that AWS Copilot builds when creating a new application workspace using `copilot app init`?
A) A single monolithic EC2 instance
B) A logical grouping of containerized services, jobs, and shared infrastructure (VPC, subnets, IAM roles) managed through generated CloudFormation stacks across multiple deployment environments
C) An Amazon S3 static website
D) An AWS Step Functions state machine only

103. When initializing a new service in AWS Copilot using `copilot svc init`, which service type should a developer choose for a public-facing containerized REST API that requires internet routing, an Application Load Balancer, and path-based routing?
A) Backend Service
B) Load Balanced Web Service
C) Worker Service
D) Request-Driven Web Service

104. A microservice in an ECS cluster processes internal RPC requests from other services within the same VPC. It must NOT be reachable from the public internet and does not need an external load balancer. Which AWS Copilot service type is designed for this internal service pattern?
A) Load Balanced Web Service
B) Backend Service (using AWS Cloud Map service discovery for internal DNS routing)
C) Worker Service
D) Request-Driven Web Service

105. A containerized worker application pulls image-processing tasks from an Amazon SQS queue and writes output to Amazon S3. Which AWS Copilot service type automatically provisions and configures an SQS queue and IAM permissions for the ECS Fargate worker task?
A) Load Balanced Web Service
B) Backend Service
C) Worker Service
D) App Runner Service

106. A developer wants to deploy a simple, containerized HTTP web service that automatically scales from zero instances up based on incoming requests with zero infrastructure management, utilizing AWS App Runner underneath rather than an ECS Fargate cluster. Which Copilot service type should be selected?
A) Request-Driven Web Service
B) Backend Service
C) Worker Service
D) Scheduled Job

107. Where does AWS Copilot store the declarative infrastructure and deployment configuration for a service?
A) In `copilot/<service_name>/manifest.yml`
B) In `Dockerfile`
C) In `docker-compose.yml`
D) In `.ebextensions/config.yml`

108. A developer is reviewing the `copilot/api/manifest.yml` file below:
```yaml
name: api
type: Load Balanced Web Service

image:
  build: Dockerfile
  port: 8080

http:
  path: '/'
  healthcheck: '/health'

cpu: 256
memory: 512
count:
  range: 1-10
  cpu_percentage: 70

environments:
  prod:
    count: 3
    variables:
      LOG_LEVEL: warn
```
What does the `environments.prod` section in this manifest achieve?
A) It deletes the `prod` environment
B) It overrides the base service configuration specifically for the `prod` environment, setting a fixed task count of 3 and `LOG_LEVEL=warn` without modifying other environments
C) It converts the production service to run on Amazon EC2 instead of Fargate
D) It routes 100% of traffic to a local staging server

109. What is the definition of a "Copilot Environment" (e.g., created via `copilot env init --name test`), matching the official AWS DVA-C02 concept of "Copilot environments"?
A) A git branch on GitHub
B) A distinct, isolated deployment target containing its own VPC, subnets, ECS cluster, security groups, and shared resources (e.g., `test`, `staging`, `prod`) managed under the same Copilot application
C) A Docker container running on a local developer laptop
D) An IAM user policy

110. How does a developer deploy an updated container image and manifest configuration to a specific Copilot environment named `staging`?
A) `copilot deploy --env staging` (or `copilot svc deploy --env staging`)
B) `copilot push staging`
C) `copilot upload staging`
D) `git push staging`

111. A developer wants to set up a continuous delivery pipeline that automatically builds a container image upon code commit, runs automated integration tests in a `test` environment, and automatically promotes the container to a `prod` environment upon approval. Which AWS Copilot command generates the pipeline configuration?
A) `copilot pipeline init` (followed by `copilot pipeline deploy`)
B) `copilot ci create`
C) `copilot action setup`
D) `copilot codepipeline build`

112. Which underlying AWS CI/CD services are provisioned when a developer deploys a Copilot pipeline using `copilot pipeline deploy`?
A) AWS CodePipeline, AWS CodeBuild, and Amazon ECR (Elastic Container Registry)
B) Jenkins on an EC2 instance
C) GitHub Actions runners on on-premises hardware
D) AWS Elastic Beanstalk worker environments

113. In an AWS Copilot pipeline definition (`copilot/pipelines/<pipeline_name>/buildspec.yml`), what happens during the build phase?
A) The pipeline downloads a virtual machine image from VirtualBox
B) AWS CodeBuild builds the Docker container images for all services in the application, runs unit tests, and pushes the tagged images to Amazon ECR repositories
C) S3 buckets are formatted
D) The database is deleted

114. A developer wants to run a containerized task on a periodic schedule (e.g., every night at 2:00 AM) in AWS Copilot. Which Copilot job type should be created?
A) Scheduled Job (using Amazon EventBridge and AWS Fargate tasks)
B) Worker Service
C) Backend Service
D) Load Balanced Web Service

115. A developer wants to provision an Amazon Aurora Serverless PostgreSQL database or a DynamoDB table and attach it directly to a Copilot service. Which Copilot command adds a managed storage resource to a service manifest?
A) `copilot storage init`
B) `copilot db create`
C) `copilot add database`
D) `copilot rds attach`

116. How does AWS Copilot inject the database credentials and endpoint connection strings of an attached storage resource into a service's running container?
A) It prints the password in the public console log
B) It exposes the connection details and secret ARNs as standard environment variables and AWS Secrets Manager secrets within the container's ECS Task Definition
C) It writes a text file to `/root/credentials.txt` on the host OS
D) It emails the database password to the developer

117. An engineer wants to inspect live container logs for an ECS service named `api` running in the `prod` environment directly from their local terminal. Which Copilot command streams these logs?
A) `copilot svc logs --name api --env prod --follow`
B) `copilot tail api`
C) `copilot monitor prod`
D) `docker logs prod`

118. A developer wants to open an interactive shell inside a running Fargate container task in the `staging` environment to debug a file permission issue. Which command enables this using ECS Exec?
A) `copilot svc exec --name api --env staging`
B) `ssh fargate.amazonaws.com`
C) `copilot connect`
D) `copilot bash`

119. What is the fundamental difference between AWS Elastic Beanstalk, AWS Amplify, and AWS Copilot in terms of target workload and underlying compute?
A) Beanstalk targets traditional web applications on EC2; Amplify targets full-stack frontend/mobile applications backed by serverless (Cognito/AppSync/S3); Copilot targets containerized microservices running on ECS Fargate/App Runner
B) Beanstalk is only for mobile apps; Amplify is only for relational databases; Copilot is only for machine learning
C) All three tools use the exact same compute model and cannot be distinguished
D) Copilot requires managing physical server hardware in an on-premises data center

120. A development team with extensive Docker container experience is building a microservice-based application. They do not want to manage EC2 instances or write raw ECS CloudFormation templates. Which tool should they choose?
A) AWS Amplify
B) AWS Copilot
C) AWS Elastic Beanstalk single-instance worker tier
D) Amazon S3 Static Website Hosting

121. A frontend React developer with no AWS backend experience needs to quickly add user authentication (Cognito), a GraphQL API (AppSync), and cloud hosting with Git-branch preview environments. Which tool should they choose?
A) AWS Copilot
B) AWS Amplify
C) AWS Elastic Beanstalk Docker platform
D) Raw CloudFormation templates

122. A company is migrating an existing legacy Python Django application running on EC2. The team wants automated provisioning of load balancers and auto-scaling groups while retaining full SSH access to the underlying virtual machines to install proprietary OS packages. Which tool is the best fit?
A) AWS Amplify
B) AWS Elastic Beanstalk (Web server tier on Python platform)
C) AWS Copilot
D) AWS Lambda with container images

123. In the official AWS DVA-C02 exam guide, what core architectural pattern do "Lambda aliases", "container image tags", "Amplify branches", and "Copilot environments" all represent?
A) Approved-version environments (stable, named pointers to tested builds enabling safe promotion across development, staging, and production stages)
B) Data encryption mechanisms
C) Network subnet masks
D) Database indexing strategies

124. How does AWS Copilot handle secret configuration values (such as third-party API keys) without exposing them in plain text inside `manifest.yml`?
A) By hardcoding the API keys in git commit messages
B) By referencing secret names stored in AWS Secrets Manager or AWS Systems Manager Parameter Store under the `secrets:` section of the `manifest.yml`
C) By disabling encryption across all Fargate tasks
D) By storing keys in the Docker image layers

125. An architect is selecting the appropriate AWS developer deployment tool for three separate projects:
1. Project 1: A Flutter mobile application needing Cognito authentication, S3 image uploads, and branch-based web hosting.
2. Project 2: A fleet of containerized microservices running on ECS Fargate with automated CodePipeline promotion across `test` and `prod`.
3. Project 3: A legacy Java Tomcat enterprise application running on EC2 requiring Rolling deployments with additional batch to maintain full capacity.
Which mapping of AWS deployment tools is correct?
A) Project 1: AWS Copilot; Project 2: AWS Elastic Beanstalk; Project 3: AWS Amplify
B) Project 1: AWS Amplify; Project 2: AWS Copilot; Project 3: AWS Elastic Beanstalk
C) Project 1: AWS Elastic Beanstalk; Project 2: AWS Amplify; Project 3: AWS Copilot
D) Project 1: Raw CloudFormation; Project 2: AWS Amplify; Project 3: AWS Copilot

---

## Answer Key & Explanations

1. B — Elastic Beanstalk automates provisioning of EC2, ASG, and ELB while allowing developers to SSH into the underlying EC2 instances for deep inspection.
2. B — The Web server environment tier in Elastic Beanstalk is designed for applications that handle public HTTP(S) requests via an Elastic Load Balancer.
3. B — The Worker environment tier is purpose-built for non-public background processing, polling tasks from an SQS queue via the local SQS daemon.
4. B — The Beanstalk SQS daemon (SQSD) polls SQS messages and delivers them by making HTTP POST requests to a local endpoint (e.g., `http://localhost/`) on the instance.
5. B — Elastic Beanstalk configuration files must be placed in a `.ebextensions/` directory at the root of the source bundle with a `.config` extension (YAML or JSON).
6. B — `leader_only: true` inside `container_commands` ensures that the specified command (such as a DB migration) runs on only one instance in the Auto Scaling group.
7. B — In `.ebextensions`, `commands` run early in the setup process before application extraction; `container_commands` run after the source bundle is extracted to the staging directory.
8. B — An `.ebextensions/*.config` file can contain a standard CloudFormation `Resources:` section defining additional AWS resources (such as `AWS::SQS::Queue`).
9. B — Saved Configurations capture an Elastic Beanstalk environment's settings as a template stored in S3 to replicate identical environments easily.
10. B — Periodic scheduled tasks in an Elastic Beanstalk worker environment are configured using a `cron.yaml` file in the root of the application bundle.
11. B — A `Procfile` at the root of the source bundle defines custom application execution commands on modern Elastic Beanstalk platforms.
12. A — A single-container Docker environment in Elastic Beanstalk requires a `Dockerfile` or a `Dockerrun.aws.json` in the root of the source bundle.
13. B — If an RDS DB instance is created inside an Elastic Beanstalk environment, deleting or terminating the environment also terminates the database, risking data loss.
14. B — `eb init` initializes a local directory as an Elastic Beanstalk application workspace and configures the default Region and platform settings.
15. A & B — Elastic Beanstalk requires a Service Role to manage AWS resources on your behalf, and an EC2 Instance Profile role for instances to access S3, CloudWatch, and SQS.
16. B — Enhanced Health Reporting publishes granular OS metrics, latency distributions, and HTTP response code counts to CloudWatch and the EB console.
17. B — Enhanced Health Reporting relies on an Elastic Beanstalk Health Agent running on each EC2 instance that publishes detailed OS and web server metrics.
18. B — Environment variables in `.ebextensions` are specified under the `aws:elasticbeanstalk:application:environment` namespace.
19. B — `eb logs` retrieves the tail (last 100 lines) of standard system and application logs from the environment's EC2 instances.
20. B — A load-balanced, autoscaling environment distributes traffic across multiple instances and automatically scales capacity based on demand.
21. B — A single-instance environment launches a single EC2 instance with an Elastic IP and no load balancer, suitable for development testing.
22. A — `eb deploy` packages committed git files into a zip archive, uploads it to S3, creates an Application Version, and deploys it to the environment.
23. B — On Amazon Linux 2 platforms, custom Nginx proxy configuration files should be placed in `.platform/nginx/conf.d/` in the source bundle.
24. A — `.ebextensions/` manages general configuration and AWS resources; `.platform/` provides platform hooks and server config files for Amazon Linux 2 platforms.
25. A — Custom platform lifecycle scripts on Amazon Linux 2 must be placed in `.platform/hooks/prebuild/`, `predeploy/`, or `postdeploy/`.
26. A — IMDSv2 requirements can be enforced via `.ebextensions` under the `aws:autoscaling:launchconfiguration` namespace by setting `DisableIMDSv1: true`.
27. B — `eb ssh` opens an SSH shell into an Elastic Beanstalk EC2 instance, automatically managing temporary security group access.
28. B — When an application returns an error on a worker message, SQSD leaves the message in SQS to be retried after the visibility timeout expires.
29. A & B — Deploying a pre-built zip via AWS CLI requires `create-application-version` to register the S3 bundle, followed by `update-environment` to deploy it.
30. B — Elastic Beanstalk uses CloudFormation to provision standard AWS resources that can be inspected, tuned, and monitored like any other AWS infrastructure.
31. C — Rolling with additional batch launches an extra batch of instances first to maintain 100% capacity throughout the entire deployment process.
32. A — All at once updates all instances simultaneously; it is the fastest deployment method but incurs downtime during the update.
33. B — Standard Rolling deployment updates instances in batches without launching extra instances first, temporarily reducing capacity during the rollout.
34. C — Immutable deployments launch a brand new Auto Scaling group for the new version, ensuring zero downtime, full capacity, and instant rollback on failure.
35. B — Immutable deployments test a single temporary instance in a new Auto Scaling group; if healthy, they launch the rest of the fleet and terminate the old group.
36. A — Traffic splitting shifts a small percentage of live traffic (e.g., 10%) to canary instances in a new Auto Scaling group before full rollout.
37. B — Performing a CNAME swap between two independent environments provides a safe, zero-downtime blue/green deployment for major platform/database upgrades.
38. B — "Swap Environment URLs" performs an atomic DNS CNAME record swap between two environments in the same application, instantly redirecting traffic.
39. B — For a seamless CNAME swap, the database must be external to both environments so both versions can connect to it independently without data migration.
40. A — Regions have a soft quota of 1,000 application versions; configuring an Application Version Lifecycle Policy automatically purges old versions from S3.
41. B — The lifecycle policy setting "Retain versions currently deployed to environments" prevents deleting bundles currently in use by active environments.
42. B — If health checks fail during an Immutable deployment, Elastic Beanstalk terminates the new Auto Scaling group, leaving existing production traffic untouched.
43. B & C — Rolling with additional batch and Immutable deployments launch temporary additional EC2 instances during the rollout, incurring brief extra costs.
44. A — Rolling back in Elastic Beanstalk is achieved by re-deploying a previously successful Application Version label to the environment.
45. B — Elastic Beanstalk verifies that instances in a batch report as `InService` (Healthy) on the load balancer before proceeding to the next batch.
46. A — `BatchSizeType` (`Fixed` or `Percentage`) controls how batch sizes are calculated during rolling deployments.
47. B — With a fleet of 4 instances and a 50% batch size, Elastic Beanstalk updates 2 instances in the first batch.
48. A — Immutable deployments manage the entire new-instance rollout within a single environment, avoiding the overhead of maintaining two separate environments.
49. B — Elastic Beanstalk CNAME swaps are only supported between environments in the same AWS Region and application.
50. B — If CloudWatch alarms fire during Traffic Splitting evaluation, Elastic Beanstalk immediately cancels the deployment and routes 100% of traffic back.
51. C — All at once incurs full downtime, and standard Rolling temporarily reduces capacity; both should be avoided for high-availability production systems.
52. B — An Application Version is an immutable source bundle (zip/WAR/JAR) stored in an Elastic Beanstalk-managed S3 bucket.
53. A — ALB health check paths are configured in `.ebextensions` under `aws:elasticbeanstalk:environment:process:default` with `HealthCheckPath`.
54. A — The `Timeout` option in `aws:elasticbeanstalk:command` sets the maximum duration Elastic Beanstalk waits for a command or deployment to complete.
55. B — "Clone Environment" creates a duplicate environment with identical platform, configuration, and environment variable settings.
56. A — "Rebuild Environment" (or `eb rebuild`) re-provisions the environment's resources from scratch using the current version and configuration.
57. B — Rebuilding an environment terminates all underlying EC2/ELB resources and provisions brand new resources using the current configuration.
58. A — EC2 instances in Auto Scaling groups are ephemeral; externalizing state to DynamoDB, S3, or ElastiCache prevents data loss during scaling and deployments.
59. A — `Dockerrun.aws.json` (v2) defines multi-container Docker compositions, port mappings, and container memory limits in Elastic Beanstalk.
60. B — If a batch fails during a rolling deployment, Elastic Beanstalk halts the deployment to protect the remaining healthy instances running the old version.
61. B — AWS Amplify is a full-stack development framework, CLI, and hosting platform designed to accelerate frontend and mobile app development on AWS.
62. B — `amplify add auth` configures authentication resources (Amazon Cognito User Pools and Identity Pools) via guided CLI prompts.
63. B — `amplify add auth` automatically provisions and configures Amazon Cognito User Pools (for directory/auth) and Identity Pools (for AWS credentials).
64. B — `amplify add api` with GraphQL provisions an AWS AppSync API endpoint with connected DynamoDB data sources and resolvers.
65. B — `amplify push` compiles local backend definitions into CloudFormation stacks and deploys/updates the cloud resources in AWS.
66. B — The Amplify CLI generates and executes nested AWS CloudFormation templates to provision all backend resources.
67. B — The Amplify `Auth` client category provides high-level methods that manage authentication flows, tokens, and session refresh against Cognito.
68. B — The `Amplify.Storage` client category provides simple APIs (`Storage.put`, `Storage.get`, `Storage.remove`) for managing files in Amazon S3.
69. A — Amplify DataStore provides local-first offline storage and automated bidirectional synchronization/conflict resolution via AppSync and DynamoDB.
70. B — DataStore utilizes AppSync conflict resolution strategies (Automerge, Optimistic Concurrency, Lambda) backed by versioning metadata.
71. B — `amplify.yml` defines the frontend and backend build phases, commands, output artifacts, and cache paths for Amplify Hosting.
72. B — `frontend.artifacts.baseDirectory` specifies the directory containing compiled static output files that Amplify Hosting publishes to the CDN.
73. A — Adding `node_modules/**/*` to `frontend.cache.paths` in `amplify.yml` caches dependencies between builds, significantly reducing build times.
74. B — `amplify status` displays a summary table of configured backend resources, their categories, operation statuses, and the active environment name.
75. B — `amplify env add <name>` allows team members to create independent backend environments with dedicated CloudFormation stacks in AWS.
76. A — `amplify env checkout <name>` switches the local Amplify workspace context to an existing backend environment.
77. A — `amplify add function` scaffolds a serverless AWS Lambda function and wires it into the Amplify backend project.
78. B — `amplify pull` downloads cloud backend metadata and regenerates local configuration files (`aws-exports.js` / `amplifyconfiguration.json`).
79. B — `aws-exports.js` contains client configuration details (Cognito IDs, AppSync endpoints, S3 bucket names) needed to initialize the Amplify SDK.
80. B — Real-time GraphQL subscriptions in Amplify are initiated using `API.graphql(graphqlOperation(...)).subscribe(...)`.
81. B — Amplify Studio data models are compiled into a `schema.graphql` file and deployed as CloudFormation stacks and DynamoDB tables.
82. A — `amplify mock` runs local mock instances of AppSync, DynamoDB, S3, and Lambda on the developer workstation for rapid local testing.
83. A — `@auth(rules: [{ allow: owner }])` restricts read, update, and delete access to the user who created the record.
84. A — Specifying `{ allow: public, operations: [read] }` alongside `{ allow: private }` permits unauthenticated guest reads while restricting writes to authenticated users.
85. B — Running `amplify init` with new account credentials followed by `amplify push` cleanly reproduces the entire infrastructure stack in the new account.
86. B — Pushing to a connected branch triggers Amplify Hosting's CI/CD pipeline, building and deploying static assets and SSR compute to CloudFront.
87. B — In Amplify Hosting, each connected Git branch maps to an independent, isolated hosting environment with its own unique URL.
88. B — In the Amplify Hosting console, developers can map specific frontend Git branches (e.g., `develop`) to dedicated backend environments (e.g., `dev`).
89. B — Amplify Pull Request Previews automatically spin up an ephemeral deployed environment for every opened PR to facilitate visual review before merging.
90. B — When a Pull Request is closed or merged, Amplify Hosting automatically tears down the ephemeral preview environment.
91. B — Amplify Hosting Password Protection enables basic HTTP authentication on specific branches (like staging) with a simple username/password.
92. B — SPAs require a 200 Rewrite rule in Amplify Hosting redirecting all non-file route requests to `/index.html` so client-side routers can handle them.
93. B — Amplify Hosting manages custom domains with automatic issuance and renewal of free SSL/TLS certificates via AWS Certificate Manager (ACM).
94. B — Environment variables in Amplify Hosting are configured in App Settings > Environment Variables and can be customized per branch.
95. B — Amplify Hosting automatically hosts and accelerates web applications globally using Amazon CloudFront edge locations.
96. B — Amplify Hosting runs Next.js server-side rendering using managed AWS Lambda compute functions while serving static files from CloudFront.
97. B — Amplify Hosting integrates with Amazon SNS and email notifications to broadcast build success and failure alerts.
98. A — Incoming Webhooks in Amplify Hosting provide unique POST URLs that trigger builds from external systems or headless CMS platforms.
99. A — AWS WAF integrates directly with CloudFront and Amplify Hosting to protect applications against web exploits, SQL injection, and XSS.
100. A — Branches must be explicitly connected or branch auto-detection enabled in the Amplify Console for pushes to trigger builds.
101. B — AWS Copilot is an opinionated CLI tool for building, releasing, and operating production containerized apps on ECS Fargate and App Runner.
102. B — `copilot app init` sets up an application container holding multiple services, environments (VPCs/clusters), and shared infrastructure managed via CloudFormation.
103. B — A Load Balanced Web Service in Copilot provisions an Application Load Balancer in front of an ECS Fargate service for public HTTP(S) traffic.
104. B — A Backend Service in Copilot creates an internal-only ECS service accessible solely from within the VPC via AWS Cloud Map service discovery.
105. C — A Worker Service in Copilot provisions an ECS Fargate task with an integrated Amazon SQS queue and IAM policies for asynchronous job processing.
106. A — A Request-Driven Web Service in Copilot deploys a containerized service to AWS AppRunner for simple request-driven auto-scaling.
107. A — Copilot stores declarative service definitions and infrastructure overrides in `copilot/<service_name>/manifest.yml`.
108. B — The `environments.prod` block in `manifest.yml` overrides base settings specifically for the `prod` environment (such as setting task count to 3).
109. B — A Copilot Environment is an isolated infrastructure target (`dev`, `staging`, `prod`) containing its own VPC, subnets, and ECS cluster.
110. A — `copilot deploy --env staging` deploys the local container and manifest configuration to the specified environment.
111. A — `copilot pipeline init` generates automated CI/CD pipeline definitions for multi-environment promotion using AWS CodePipeline.
112. A — Copilot pipelines use AWS CodePipeline to orchestrate stages, AWS CodeBuild to build Docker images, and Amazon ECR to store container images.
113. B — The CodeBuild build phase in a Copilot pipeline builds Docker images, runs tests, and pushes tagged images to Amazon ECR.
114. A — A Scheduled Job in Copilot runs a containerized task on a defined cron schedule using Amazon EventBridge and ECS Fargate.
115. A — `copilot storage init` provisions databases (DynamoDB or Aurora Serverless) or S3 buckets and attaches them to a Copilot service.
116. B — Copilot injects storage connection strings and Secrets Manager secret ARNs as standard environment variables inside the ECS Task Definition.
117. A — `copilot svc logs --name <svc> --env <env> --follow` tails real-time CloudWatch logs from running ECS tasks in that environment.
118. A — `copilot svc exec` initiates an interactive shell inside a running Fargate container using Amazon ECS Exec.
119. A — Beanstalk targets EC2 web apps; Amplify targets full-stack frontend/serverless apps; Copilot targets containerized services on ECS Fargate/App Runner.
120. B — AWS Copilot is designed for containerized workflows on ECS Fargate without requiring manual CloudFormation template management.
121. B — AWS Amplify provides complete tooling for frontend developers needing managed authentication, GraphQL APIs, and Git-branch hosting.
122. B — Elastic Beanstalk Python platform provides automated ELB/ASG management while retaining full SSH access to underlying EC2 instances.
123. A — Lambda aliases, container image tags, Amplify branches, and Copilot environments all represent approved-version environments for safe promotion.
124. B — Copilot references secrets in Secrets Manager or Parameter Store under the `secrets:` section in `manifest.yml` without exposing them in plain text.
125. B — Project 1 maps to Amplify (mobile/auth/hosting), Project 2 to Copilot (Fargate/pipelines), and Project 3 to Elastic Beanstalk (EC2/Tomcat/Rolling deploys).
