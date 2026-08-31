# Module 12 — Practice Questions (123)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Container Fundamentals: Images, Dockerfiles & Layers (1–12)

1. A platform engineer explains to a team migrating from EC2-based deployments to containers that unlike a virtual machine, a container does not include its own copy of the operating system kernel. What isolation mechanism allows multiple containers to run safely on a single host while sharing that host's kernel?
A) A hypervisor virtualizing separate kernels for each container
B) OS-level namespaces and cgroups that isolate each container's processes, filesystem, and resource usage
C) A dedicated physical CPU core assigned to each container
D) Each container running its own nested virtual machine

2. A developer is new to containers and asks a colleague to explain the relationship between a Docker image and a container. Which statement correctly describes that relationship?
A) An image and a container are the same thing, just different names
B) A container is a running instance of an image; the image itself is a read-only, portable template
C) An image is generated only after a container is deleted
D) A container contains multiple images, but an image never runs directly

3. A developer opens a project's Dockerfile for the first time and sees a line reading `FROM node:20-alpine` as the very first instruction. What does this instruction do?
A) It publishes port 20 on the Alpine operating system
B) It selects the base image the new image will be built on top of, in this case a minimal Alpine Linux image with Node.js 20 preinstalled
C) It permanently deletes any existing Node.js installation before starting
D) It configures the container's IAM role

4. A team's Docker build for a Node.js application takes several minutes on every single code change, even when only application source files (not dependencies) have changed, because their Dockerfile copies the entire project directory and runs the dependency install step immediately afterward, in a single combined step. Which change to the Dockerfile's instruction order would most directly speed up rebuilds after a source-only change?
A) Copy only the dependency manifest (e.g., package.json) and run the dependency install before copying the rest of the application source, so the cached dependency layer is reused when only source files change
B) Remove the FROM instruction entirely
C) Combine every instruction into a single RUN command
D) Switch the base image to a larger, general-purpose Linux distribution

5. Which statement accurately describes how Docker image layers work?
A) Each Dockerfile instruction produces a new image layer that is cached, and unchanged layers are reused on subsequent builds, speeding up rebuilds and reducing what needs to be pulled from a registry
B) An image consists of exactly one layer regardless of how many instructions the Dockerfile contains
C) Layers are only relevant when pushing an image to Amazon EFS, not to a container registry
D) Every layer is always rebuilt from scratch on every build, with no caching behavior available

6. A team compares startup times between launching a new EC2 instance from an AMI and starting a new container from an existing image on a host that is already running Docker. Why does the container typically start in a fraction of a second, while the EC2 instance takes over a minute?
A) Containers use faster network cards than EC2 instances
B) The container does not need to boot a full operating system kernel; it starts a process that shares the host's already-running kernel, whereas the EC2 instance must fully boot a guest operating system
C) EC2 instances always use larger AMIs than container images
D) Containers do not require any image to be pulled beforehand

7. In a Dockerfile, which instruction specifies the command that actually runs when a container is started from the built image, as opposed to a command that runs only once at image build time?
A) RUN
B) COPY
C) CMD
D) FROM

8. Which two of the following statements accurately describe containers as compared to traditional virtual machines? (Select TWO)
A) Containers share the host operating system's kernel rather than including their own
B) Containers generally start in a fraction of the time a full virtual machine takes to boot
C) Containers require a dedicated hypervisor for every individual container
D) Containers always require more disk space than an equivalent virtual machine image
E) Containers cannot be isolated from one another on the same host

9. A CI/CD pipeline builds a container image and tags it `my-app:2.1.7` before pushing it to a registry, rather than only ever pushing to a mutable tag like `latest`. What is the primary benefit of tagging with a specific, immutable-style version like this for deployment purposes?
A) It reduces the image's file size on disk
B) It creates a versioned, identifiable deployment artifact that can be promoted through environments and rolled back to precisely, unlike a mutable tag whose underlying image content can silently change
C) It automatically encrypts the image at rest
D) It is required before Docker will allow the image to be built at all

10. A Dockerfile includes the line `EXPOSE 3000`. What does this instruction actually do?
A) It documents which port the containerized application listens on and enables that port for inter-container linking, but does not by itself publish or map the port to the host — that mapping is a separate runtime configuration
B) It permanently opens port 3000 on the internet with no further configuration needed
C) It disables all other ports on the container
D) It configures a load balancer listener automatically

11. A developer writing a Dockerfile for a Python application needs to decide the order of two steps: copying the application's `requirements.txt` and running the dependency installer, versus copying the rest of the application source code. To maximize Docker's build-layer caching on future rebuilds where only source code changes, which order is correct?
A) Copy all application source code first, then copy requirements.txt and install dependencies last, every time
B) Copy requirements.txt and install dependencies first, then copy the remaining application source code afterward
C) The order makes no difference to build caching behavior
D) Install dependencies without ever copying a requirements file

12. A team new to containerization is evaluating whether to package their application as a Docker image for deployment. Which two of the following are accurate characteristics of a well-built container image? (Select TWO)
A) It packages the application code together with its runtime and dependencies so it behaves consistently across environments
B) It is composed of a series of cached, reusable layers built from Dockerfile instructions
C) It must always include a complete guest operating system kernel of its own
D) It can only ever be run on the exact same physical machine where it was built
E) It requires a Kubernetes cluster to build, even before ever being deployed

### Amazon ECR: Registries, Scanning & CI/CD Integration (13–32)

13. A company maintains two categories of container images: proprietary internal microservice images that must never be publicly accessible, and a small open-source CLI tool image the company wants anyone on the internet to be able to pull without AWS credentials. Which Amazon ECR repository types should the company use for each, respectively?
A) A single ECR private repository for both, controlled entirely through bucket policies
B) An ECR private repository for the proprietary images, and an ECR public repository for the open-source CLI image
C) Amazon S3 for both, since ECR does not support public access
D) An ECR public repository for both, with IAM restricting internal image access

14. A security team wants container images pushed to ECR to be continuously re-evaluated against newly disclosed CVEs after the push, not just scanned once at push time, using Amazon Inspector's deeper OS and language-package vulnerability coverage. Which ECR scanning configuration meets this requirement?
A) Basic scanning, which uses the open-source Clair scanner and only scans once at push time
B) Enhanced scanning, powered by Amazon Inspector, which continuously reassesses images as new vulnerabilities are published
C) Disabling scanning and relying on manual review
D) A third-party scanner outside of AWS, since ECR has no native scanning capability

15. A developer needs to authenticate their local Docker client to push an image to a private ECR repository. Following AWS's recommended approach, which command sequence should they use?
A) Manually create a static ECR username and password in the console and run docker login with those credentials
B) Run aws ecr get-login-password to retrieve a temporary authorization token derived from their current IAM credentials, and pipe it into docker login --username AWS --password-stdin
C) Email AWS Support to request registry credentials
D) Use their AWS account's root user password directly with docker login

16. An ECR repository accumulates hundreds of untagged image layers from every CI build, most of which are superseded within days and never referenced again, steadily increasing storage costs. Which ECR feature should the team configure to automatically expire old, untagged images without writing custom cleanup automation?
A) An ECR lifecycle policy defining expiration rules, such as removing untagged images older than a set number of days
B) An IAM permissions boundary on the repository
C) Manually deleting images from the console every week
D) Enabling S3 Intelligent-Tiering on the repository

17. A CodeBuild project's build role needs to push newly built images to an ECR repository as the final step of a build. Which category of IAM permissions must be granted to that CodeBuild service role for the push to succeed?
A) Permissions to invoke Lambda functions only
B) ECR permissions including obtaining an authorization token and uploading image layers, such as ecr:GetAuthorizationToken, ecr:InitiateLayerUpload, and ecr:PutImage
C) Permissions to modify Route 53 hosted zones
D) No IAM permissions are required if the CodeBuild project is in the same account as the ECR repository

18. A company's shared services account hosts a central ECR repository that a separate application account's ECS tasks need to pull images from. Which mechanism allows the application account's IAM principals to pull images from a repository that lives in a different AWS account?
A) An ECR repository policy on the shared repository granting pull permissions (e.g., ecr:GetDownloadUrlForLayer, ecr:BatchGetImage) to the application account's principals
B) Copying the image into the application account's default VPC
C) Granting root user access to the shared services account
D) ECR does not support any form of cross-account access

19. A platform team wants to prevent developers from accidentally overwriting an already-published, versioned image tag (for example, re-pushing a different image under the tag 1.4.2 after it has already been deployed), to preserve traceability between a tag and its exact image content. Which ECR repository setting enforces this?
A) Enabling image tag immutability on the repository, which rejects any push that attempts to overwrite an existing tag
B) Enabling ECR lifecycle policies
C) Disabling image scanning
D) Setting the repository to public

20. A CodePipeline pipeline includes a CodeBuild stage that builds and pushes a new container image to ECR, followed by a deploy stage that updates an ECS service with the new image. Which artifact does the CodeBuild stage typically produce to tell the ECS deploy action exactly which image URI to deploy?
A) A CloudFormation change set
B) An imagedefinitions.json file naming the container and the new image URI
C) A Dockerfile
D) An IAM policy document

21. Which underlying open-source scanning engine powers Amazon ECR's basic image scanning feature?
A) Amazon Inspector exclusively
B) Clair
C) AWS Config
D) Amazon GuardDuty

22. Compared to ECR basic scanning, what additional capability does ECR enhanced scanning (powered by Amazon Inspector) provide?
A) It scans images only at push time and never again
B) Continuous rescanning as new vulnerabilities are disclosed, without requiring the image to be re-pushed, plus deeper OS and programming-language package coverage
C) It removes the need for a task execution role
D) It automatically deletes vulnerable images without notifying anyone

23. Which two of the following are accurate about the authorization token returned by aws ecr get-login-password? (Select TWO)
A) It is a temporary token derived from the caller's current IAM credentials, not a permanent registry password
B) It is valid for a limited period (12 hours) before it must be refreshed
C) It grants full administrative access to every AWS service in the account
D) It never expires once issued
E) It can only be used from within the AWS Management Console, never from the CLI

24. A team wants to grant a specific cross-account role pull access to just one ECR repository, without granting that account any access to other repositories in the registry. Which approach scopes access most precisely?
A) Granting AdministratorAccess to the entire account
B) Attaching a resource-based repository policy to that specific ECR repository, naming the other account's role as principal with only the needed pull actions
C) Sharing the AWS account's root credentials
D) Making the entire registry public

25. A developer discovers that a previously pushed container image layer contains a hardcoded API key that was later removed from later layers, but the layer with the secret is still part of the image's history in the registry. What is the most effective remediation?
A) Simply deleting the latest tag; the older layer with the secret is no longer a concern once untagged
B) Treat the exposed secret as compromised and rotate it immediately, since any layer with the secret remains retrievable from the registry regardless of later layers removing it from the visible filesystem
C) Enable image scanning, which automatically removes secrets from existing layers
D) Nothing further is needed once the file is deleted in a later layer

26. For an ECS task's execution role to successfully pull a private image from ECR when the task starts, which category of permission must that role include?
A) ecr:GetDownloadUrlForLayer, ecr:BatchGetImage, and ecr:GetAuthorizationToken scoped appropriately, so the ECS agent can authenticate to ECR and download the image layers
B) s3:GetObject only
C) No permissions are required for private repositories
D) lambda:InvokeFunction

27. How is Amazon ECR primarily billed for private repositories, aside from data transfer?
A) A fixed monthly fee per repository regardless of size
B) Based on the amount of data stored in the repository, per GB per month
C) Per image scan only
D) ECR storage itself is entirely free at any scale

28. A team wants an ECR lifecycle policy that retains only the 5 most recently pushed images whose tags start with release-, expiring all older ones automatically. Which lifecycle policy capability supports this?
A) A rule based on image count with a tag prefix match, keeping only the specified number of most recent matching images
B) Manually reviewing images each release
C) S3 Versioning enabled on the repository
D) ECR does not support prefix-based rules, only date-based rules

29. A CodeBuild project that builds a Docker image and pushes it to ECR fails with an error indicating the Docker daemon cannot be started inside the build environment. Which CodeBuild project setting most likely needs to be enabled to resolve this?
A) Enabling privileged mode, which grants the build environment the elevated access needed to run a Docker daemon during the build
B) Increasing the CodeBuild compute type only
C) Switching the build to a different AWS Region
D) Disabling VPC connectivity for the project

30. Which two of the following are native Amazon ECR features that require no additional third-party tooling to use? (Select TWO)
A) Image vulnerability scanning (basic and enhanced tiers)
B) Lifecycle policies to automatically expire old images
C) Automatic conversion of container images into Lambda functions
D) Built-in Kubernetes cluster provisioning
E) Automatic generation of Dockerfiles from source code

31. Does pulling an image from an ECR public repository require the puller to authenticate with AWS credentials?
A) Yes, every pull from any ECR repository always requires IAM authentication
B) No, images in an ECR public repository can be pulled anonymously without AWS credentials, since the repository is intended for public distribution
C) Only Windows containers can pull from public repositories
D) Only if the puller is in the same AWS Organization

32. A platform team wants their ECR setup to (1) automatically flag known vulnerabilities in every pushed image, (2) prevent an already-published version tag from silently being overwritten by a different image, and (3) automatically remove old, untagged images to control storage cost. Which three ECR features together satisfy these three goals, respectively? (Select THREE)
A) Image scanning (basic or enhanced)
B) Image tag immutability
C) A lifecycle policy expiring untagged images
D) Enabling the repository as public
E) Disabling authentication entirely

### ECS Task Definitions & IAM Roles for Containers (33–54)

33. Which statement best describes an Amazon ECS task definition?
A) A running collection of EC2 instances registered to a cluster
B) A JSON blueprint specifying one or more containers to run together, including image, CPU/memory, networking, environment variables, and IAM roles
C) A CloudWatch alarm that triggers container restarts
D) A load balancer target group

34. In an ECS task definition, what is the primary purpose of the task execution role (executionRoleArn)?
A) Granting the application code inside the container permission to call services like S3 or DynamoDB at runtime
B) Granting ECS itself the permissions needed to launch the task, such as pulling the container image from ECR, writing logs to CloudWatch, and retrieving injected secrets at startup
C) Granting IAM users permission to log into the AWS Management Console
D) Granting the ECS service permission to create new VPCs

35. In an ECS task definition, what is the primary purpose of the task role (taskRoleArn)?
A) Granting the application code running inside the container permission to call other AWS services at runtime, such as reading from an S3 bucket or writing to a DynamoDB table
B) Granting ECS permission to pull the container image from the registry
C) Granting the ECS agent permission to write container logs to CloudWatch
D) Granting the underlying EC2 instance permission to join the cluster

36. An ECS service on Fargate is running normally — the desired count of tasks is healthy, the container image pulled successfully, and logs are streaming to CloudWatch — but the application inside the container throws AccessDenied errors every time it calls s3:GetObject. Which change is most likely to resolve this?
A) Expand the permissions attached to the task execution role
B) Expand the permissions attached to the task role to include the needed S3 permissions
C) Attach an EC2 instance profile to the underlying host
D) Restart the ECS cluster

37. A newly registered ECS task definition revision fails to start, with the ECS console reporting an error that the task was unable to pull the container image from the private ECR repository. Assuming the image and repository both exist and the network path is correct, which role most likely needs additional permissions?
A) The task role
B) The task execution role, since it governs ECS's ability to authenticate to ECR and pull the image on the task's behalf
C) An IAM user's console login role
D) A Lambda execution role

38. An ECS task definition references a database password stored in Secrets Manager as a container-level secrets entry, intending for ECS to inject that value as an environment variable when the container starts. Which role must be granted permission to retrieve that secret for the injection to succeed?
A) The task role
B) The task execution role
C) Neither role; Secrets Manager injection requires no IAM permissions
D) The EKS cluster role

39. Which two of the following statements correctly distinguish the ECS task role from the task execution role? (Select TWO)
A) The task role grants permissions the application code inside the container uses at runtime
B) The task execution role grants permissions ECS itself needs to start the task, such as pulling images and writing logs
C) The task role and task execution role are always required to be the exact same IAM role
D) The task execution role is what an application uses to call DynamoDB
E) The task role is used exclusively to pull container images from ECR

40. In a Fargate-compatible ECS task definition, what does the top-level cpu and memory field combination specify?
A) The maximum number of tasks the service can run
B) The total vCPU and memory reserved for the entire task, required for Fargate-compatible task definitions, which containers within the task share
C) The billing tier for the ECS cluster
D) The IAM permissions boundary for the task role

41. An ECS service using the awsvpc network mode assigns each task its own elastic network interface and private IP address. What direct benefit does this provide when integrating the service with an Application Load Balancer target group?
A) It removes the need for a task definition entirely
B) The ALB can route directly to individual tasks by IP, rather than needing to route through a shared host port on an EC2 instance
C) It disables all task-level IAM roles
D) It automatically encrypts all traffic between tasks

42. An ECS service is running task definition revision 14 when a bug is discovered in the container image it references. The team wants to immediately roll back to the previously known-good configuration. What is the fastest way to do this?
A) Rebuild the container image from scratch and manually recreate the previous task definition by hand
B) Update the service to use the previous task definition revision (e.g., revision 13), since ECS retains prior revisions and a service can be pointed at any of them instantly
C) Delete the ECS cluster and recreate it
D) Manually SSH into each task's underlying host and downgrade the running binary

43. A task definition's container definition includes a logConfiguration block specifying the awslogs log driver along with a log group and stream prefix. What does this configuration accomplish?
A) It configures the container to automatically scale based on log volume
B) It streams the container's stdout/stderr output to a specified CloudWatch Logs log group, which requires the task execution role to have permission to write logs
C) It configures the task role's permissions
D) It disables container logging entirely

44. A security review of an ECS task definition finds two issues: the task role is attached to the broad AWS-managed AdministratorAccess policy even though the application only ever calls a single DynamoDB table, and the task execution role is missing the permissions needed to write logs to CloudWatch, causing intermittent log delivery failures. Which two remediations correctly address each finding, respectively? (Select TWO)
A) Replace the task role's AdministratorAccess policy with a narrowly scoped policy granting only the specific DynamoDB actions and table ARN the application needs
B) Add the CloudWatch Logs permissions (e.g., logs:CreateLogStream, logs:PutLogEvents) to the task execution role
C) Delete the task role entirely, since ECS tasks do not need one
D) Grant AdministratorAccess to the task execution role as well, to be safe
E) Move the DynamoDB permissions to the task execution role instead

45. In an ECS task definition, what does the family field represent?
A) The AWS account family the task belongs to for billing
B) A name grouping together all revisions of a task definition over time, so a service can reference the family and get the latest (or a specific) revision
C) The IAM group attached to the task role
D) The Availability Zone the task must run in

46. A task definition defines two containers within a single task: the main application container and a logging sidecar container that forwards logs to a third-party service. Both containers need to call AWS APIs at runtime. How many task roles does this single task have, and how is it shared between the two containers?
A) Each container automatically gets its own separate task role
B) A single task role is defined at the task level, and both containers within that task share the same task role's permissions
C) Sidecar containers can never be granted IAM permissions
D) The logging sidecar must use the task execution role instead

47. A task definition does not specify a taskRoleArn at all, but the application inside the container attempts to call the AWS SDK to read from DynamoDB. What is the expected outcome?
A) The call succeeds automatically using the task execution role's permissions instead
B) The call fails, because with no task role attached, the application has no AWS credentials available to it via the container's credential provider chain
C) The call succeeds using the underlying EC2 host's IAM role automatically, regardless of launch type
D) ECS automatically creates a broad default task role with full access

48. A container definition can supply configuration to the application either via a plaintext environment entry or via a secrets entry referencing a value in Secrets Manager or Parameter Store. Which type of value should a database password use, and why?
A) A plaintext environment variable, because it is simpler to configure
B) A secrets entry, because it avoids storing the sensitive value in plaintext within the task definition itself, and access to the underlying secret is governed by the task execution role
C) Neither; passwords must be hardcoded into the container image
D) A plaintext environment variable, because Secrets Manager cannot be referenced from ECS

49. Comparing task definitions across ECS launch types, which statement is accurate regarding CPU and memory specification?
A) Fargate-compatible task definitions require top-level task cpu and memory values, while EC2 launch type task definitions can rely on per-container cpu/memory reservations, offering more flexibility in how resources are packed onto a shared EC2 instance
B) Only EC2 launch type requires top-level cpu and memory values
C) Neither launch type ever requires specifying cpu or memory
D) CPU and memory values are irrelevant to ECS and only apply to Lambda

50. A company wants its ECS Fargate tasks to always use the current value of a rotating database password, retrieved securely at container startup, without embedding the value in the task definition or requiring a new task definition revision every time the password rotates. Which configuration achieves this?
A) Hardcoding the password directly as a plaintext environment variable in the task definition
B) Referencing the secret via a secrets entry pointing at the Secrets Manager secret's ARN, so the current value is retrieved by ECS (using the task execution role) at task startup, independent of the task definition's own content
C) Emailing the new password to the development team after every rotation
D) Storing the password as a comment in the Dockerfile

51. Which two of the following statements about Amazon ECS task definitions are accurate? (Select TWO)
A) A task definition can specify one or more containers that run together as a single deployable unit
B) Task definitions are revisioned, and a service can be updated to use a specific prior revision
C) A task definition cannot specify environment variables under any circumstance
D) Every task definition automatically shares one global IAM role across the entire AWS account
E) Task definitions can only ever define exactly one container each

52. Which AWS service principal must be trusted in the trust policy of both an ECS task role and a task execution role for ECS to be able to assume them on behalf of a running task?
A) lambda.amazonaws.com
B) ecs-tasks.amazonaws.com
C) ec2.amazonaws.com
D) eks.amazonaws.com

53. In a container definition's portMappings section, what does the containerPort value specify?
A) The port on which the containerized application listens inside the container
B) The IAM port used for authentication
C) The AWS Region's default networking port
D) The ECR repository's port

54. A team is troubleshooting two separate ECS incidents: Incident 1, where a task fails to launch with an error about being unable to retrieve a secret referenced in the container definition; and Incident 2, where a running, healthy task's application code fails to write an object to S3 with an AccessDenied error. Which two statements correctly identify the role to fix for each incident, respectively? (Select TWO)
A) Incident 1 is resolved by granting the task execution role permission to retrieve the referenced secret
B) Incident 2 is resolved by granting the task role permission to call s3:PutObject on the target bucket
C) Both incidents are resolved by modifying the task role only
D) Both incidents are resolved by modifying the task execution role only
E) Incident 1 requires deleting the ECS cluster and recreating it

### ECS Clusters, Services & Launch Types (55–76)

55. What does an Amazon ECS cluster represent?
A) A single running container
B) A logical grouping/namespace for the tasks and services that run within it, and for the EC2 capacity (if using the EC2 launch type) registered to it
C) A single EC2 instance type
D) A CloudFormation template

56. An ECS service is configured with a desired count of 4. What does ECS do if one of the four running tasks stops unexpectedly (e.g., due to a container crash)?
A) Nothing; ECS never automatically replaces a stopped task
B) ECS automatically launches a new task to bring the running count back up to the desired count of 4
C) ECS reduces the desired count to 3 to match reality
D) ECS deletes the entire service

57. An ECS service is configured to register its tasks with an Application Load Balancer target group. As tasks are launched and stopped by the service (e.g., during a deployment or scaling event), what happens to the target group's registered targets?
A) The target group must be manually updated by an engineer every time
B) ECS automatically registers new tasks with the target group and deregisters stopped tasks, keeping the target group's membership in sync with the running tasks
C) The target group is recreated from scratch on every task change
D) ALB target groups cannot be used with ECS services at all

58. A team wants an ECS service to automatically increase or decrease its number of running tasks to keep average CPU utilization across the service near 60%, without manually defining step thresholds. Which Application Auto Scaling policy type, directly analogous to the EC2 Auto Scaling target tracking policy from module 01, should they configure for the service?
A) Scheduled scaling only
B) Target tracking scaling
C) Step scaling exclusively
D) Manual scaling performed by an engineer

59. On the ECS EC2 launch type, who is responsible for patching the operating system of the underlying EC2 instances that run the tasks?
A) AWS fully manages and patches the underlying EC2 instances automatically
B) The customer is responsible for patching and maintaining the underlying EC2 instances registered to the cluster
C) Patching is not necessary for EC2 instances running containers
D) Amazon ECR patches the instances during image pulls

60. Compared to the ECS EC2 launch type, what is the defining operational characteristic of the Fargate launch type?
A) Fargate requires manually provisioning and patching EC2 instances, just like the EC2 launch type
B) Fargate requires no EC2 instances to be provisioned, patched, or scaled by the customer at all — AWS runs the task without a customer-visible underlying host
C) Fargate only supports Windows containers
D) Fargate requires a separate EKS cluster to function

61. A machine learning team runs GPU-accelerated inference containers at large, steady-state scale and wants to tightly bin-pack multiple tasks per GPU-equipped EC2 instance to maximize utilization and minimize cost, while also applying Reserved Instance discounts at the instance level. Which two considerations correctly support choosing the ECS EC2 launch type over Fargate for this workload? (Select TWO)
A) The EC2 launch type exposes GPU-equipped instance types that Fargate does not support
B) The EC2 launch type allows Reserved Instance / Savings Plan discounts to apply at the instance level, and supports custom task placement strategies for dense bin-packing
C) Fargate always provides denser bin-packing than the EC2 launch type
D) Fargate is required for any GPU workload
E) The EC2 launch type eliminates the need for a task definition

62. A startup runs a customer-facing API with highly variable, unpredictable traffic throughout the day and wants to minimize the operational overhead of managing container infrastructure, with no interest in provisioning or patching EC2 instances themselves. Which ECS launch type best fits these priorities?
A) The EC2 launch type, for maximum control
B) The Fargate launch type, which eliminates host provisioning, patching, and capacity planning
C) Dedicated Hosts
D) A self-managed on-premises Kubernetes cluster

63. An ECS service performing a rolling deployment is configured with a minimum healthy percent of 100 and a maximum percent of 200. What does this configuration achieve during a deployment?
A) It causes the deployment to take down all existing tasks before starting any new ones
B) It ensures the service never drops below its full desired capacity while new tasks are launched alongside old ones (up to double capacity temporarily) before old tasks are drained and stopped
C) It disables health checks during the deployment
D) It has no effect on how the deployment proceeds

64. A team wants ECS service deployments to shift all production traffic from an old task set to a new task set behind the same Application Load Balancer only after automated validation checks pass, with the ability to instantly roll back by shifting traffic back if something goes wrong. Which ECS deployment approach supports this?
A) A standard ECS rolling update with no traffic-shifting controls
B) A blue/green deployment integrated with AWS CodeDeploy, which manages traffic shifting between the old and new task sets
C) Manually replacing tasks one at a time via the console with no validation
D) Deleting and recreating the entire cluster for every deployment

65. What is the purpose of an ECS capacity provider?
A) It defines the scaling behavior and infrastructure (EC2 Auto Scaling group or Fargate/Fargate Spot) that a cluster uses to run tasks, and can be associated with a cluster to manage how capacity is provisioned for tasks
B) It is a billing construct with no effect on where tasks run
C) It replaces the need for a task definition
D) It is exclusively used for EKS clusters, not ECS

66. Which two of the following correctly distinguish an ECS service from simply running a standalone ECS task directly? (Select TWO)
A) A service maintains a specified desired count of tasks over time, automatically replacing any that stop
B) A service can integrate with a load balancer target group and Application Auto Scaling, while a manually run standalone task does neither on its own
C) A standalone task automatically restarts itself if it stops, exactly like a service does
D) Services cannot be used with the Fargate launch type
E) A standalone task run outside of a service also receives automatic Application Auto Scaling

67. A team runs a batch-style ECS workload on Fargate that can tolerate interruption and wants to reduce Fargate compute costs for this specific, interruption-tolerant workload. Which Fargate capacity option is analogous to EC2 Spot Instances and offers a discount in exchange for potential interruption?
A) Fargate Spot
B) Fargate Reserved Capacity
C) Fargate Dedicated
D) There is no Spot-equivalent option for Fargate

68. Can a single ECS cluster contain some services running on the EC2 launch type and other services running on the Fargate launch type simultaneously?
A) No, a cluster must use exactly one launch type for every service within it
B) Yes, an ECS cluster can run a mix of services using different launch types (EC2 and Fargate) as needed
C) Only if the cluster is also registered with EKS
D) Only during a migration window, after which one launch type must be fully removed

69. Which two of the following are examples of ECS task placement strategies or constraints available on the EC2 launch type for controlling how tasks are distributed across a cluster's EC2 instances? (Select TWO)
A) binpack — placing tasks on the fewest possible instances to maximize resource utilization
B) spread — distributing tasks evenly across a specified field such as Availability Zone, for resilience
C) A lifecycle policy expiring old container images
D) An ECR repository policy
E) A task execution role permissions boundary

70. An ECS service is updated to reference a new task definition revision. What does ECS do by default?
A) Nothing changes until an administrator manually restarts each task
B) ECS initiates a new deployment, incrementally replacing running tasks based on the old task definition with new tasks based on the updated revision, according to the configured deployment settings
C) The service is deleted and must be recreated from scratch
D) The change only takes effect after the next scheduled maintenance window

71. When Application Auto Scaling is enabled on an ECS service, what do the configured minimum and maximum task counts define?
A) The exact number of tasks that will always run regardless of load
B) The boundaries within which the service's desired count is automatically adjusted in response to the configured scaling policy (e.g., target tracking)
C) The number of Availability Zones the cluster spans
D) The maximum number of clusters in the account

72. During a rolling ECS deployment, an old task is being stopped and replaced by a new one. Which ALB target group setting helps ensure in-flight requests to that old task are allowed to complete before it is fully deregistered and terminated?
A) Target group deregistration delay (connection draining)
B) ECR lifecycle policy
C) Task execution role permissions
D) Cluster capacity provider strategy

73. Which two of the following accurately describe tradeoffs between the ECS EC2 launch type and the Fargate launch type? (Select TWO)
A) The EC2 launch type gives the team control over instance type selection (including GPU instances) that Fargate does not expose
B) The Fargate launch type removes the operational burden of patching and scaling underlying EC2 instances
C) The EC2 launch type has no operational overhead whatsoever
D) Fargate always costs less per vCPU-hour than an equivalent EC2 instance
E) Both launch types require the customer to manage a Kubernetes control plane

74. A team running multiple ECS services that need to discover and call each other by a stable DNS name, without hardcoding IP addresses that change as tasks are replaced, wants a built-in AWS service discovery mechanism integrated with ECS. Which capability provides this?
A) AWS Cloud Map integration with ECS service discovery, which registers each task's IP under a DNS name automatically as tasks start and stop
B) ECR lifecycle policies
C) Task execution roles
D) EC2 instance metadata

75. An ECS service using the EC2 launch type reports that new tasks are stuck in a PENDING state and never transition to RUNNING, while CloudWatch shows the cluster's registered EC2 instances are already near full CPU and memory reservation from existing tasks. What is the most likely cause?
A) The task execution role is misconfigured
B) There is insufficient unreserved CPU/memory capacity across the cluster's registered EC2 instances to place the new task, requiring either scaling out the underlying Auto Scaling group or switching to Fargate to avoid this class of problem entirely
C) The ECR repository is unreachable
D) The VPC has run out of available Regions

76. Referring to the PENDING-task capacity scenario above, why does the Fargate launch type structurally avoid this specific class of failure?
A) Fargate tasks share the same underlying capacity-planning model as the EC2 launch type
B) Fargate has no customer-managed underlying EC2 fleet to run out of reservable CPU/memory on — AWS provisions the exact capacity each task needs behind the scenes
C) Fargate tasks never require any CPU or memory to be specified
D) Fargate is simply a rebranding of the EC2 launch type with no functional difference

### ECS Exec & Debugging Running Containers (77–84)

77. What does AWS ECS Exec allow a developer to do?
A) Automatically scale a service based on custom metrics
B) Open an interactive shell or run a one-off command inside a running container within a running ECS task, for debugging purposes
C) Permanently modify a container image in place
D) Create a new ECR repository

78. Which EC2-focused AWS Systems Manager capability from module 01 is ECS Exec most directly analogous to, in terms of the access pattern it provides?
A) Systems Manager Parameter Store
B) Systems Manager Session Manager, providing IAM-governed shell access without opening inbound ports or requiring SSH
C) Systems Manager Patch Manager
D) Systems Manager Inventory

79. Which two conditions must be true for ECS Exec to work against a running ECS task? (Select TWO)
A) The task definition/service must have been launched with execute command enabled (enableExecuteCommand)
B) The task role must include the SSM messaging permissions required for the ECS Exec session channel
C) The task must be using the EC2 launch type exclusively; ECS Exec does not work with Fargate
D) The container's Dockerfile must expose port 22
E) The cluster must be running Kubernetes

80. A developer needs to inspect environment variables and check running processes inside a live, misbehaving container running on Fargate, without redeploying it or opening any inbound network port to reach it. Which AWS capability directly supports this?
A) SSH directly into the Fargate task's underlying host
B) ECS Exec, which opens an interactive session into the running container via IAM-governed, SSM-based tooling with no inbound ports required
C) Rebuilding and repushing the image with debug logging enabled, then redeploying
D) Fargate does not support any form of live debugging

81. Is AWS ECS Exec supported for tasks running on the Fargate launch type, in addition to the EC2 launch type?
A) No, ECS Exec only works with the EC2 launch type
B) Yes, ECS Exec is supported on both the EC2 and Fargate launch types, provided the task meets the required platform version and configuration
C) ECS Exec is exclusive to EKS
D) ECS Exec requires disabling the task execution role

82. A compliance requirement mandates that every interactive debugging session opened into a production container be logged for audit purposes. Which ECS Exec capability supports this requirement?
A) ECS Exec sessions cannot be logged under any configuration
B) ECS Exec session activity can be configured to log to CloudWatch Logs or S3, similar to Session Manager session logging
C) Only console-based access can ever be logged
D) Logging requires a third-party agent installed inside every container

83. A developer with appropriate IAM permissions attempts to start an ECS Exec session into a running task but the session fails to start, even though enableExecuteCommand was set when the service was created. What is a likely root cause to check first?
A) The ECR repository has been deleted
B) The task role is missing the SSM messaging permissions required to establish the ECS Exec channel
C) The task execution role has too many permissions
D) The container's CPU allocation is too high

84. Why is ECS Exec generally preferred over baking an SSH server directly into a container image for debugging access?
A) It avoids the extra attack surface, image bloat, and key-management burden of running an SSH server in every container, while still centralizing access control through IAM
B) SSH servers are required for containers to start at all
C) ECS Exec is slower than SSH in every scenario
D) Baking in an SSH server is the AWS-recommended default

### AWS Fargate (85–96)

85. How is AWS Fargate primarily billed?
A) A flat monthly fee per cluster, regardless of usage
B) Per task, based on the vCPU and memory provisioned for that task, billed per second (with a minimum billing duration)
C) Per EC2 instance-hour, identical to the EC2 launch type
D) Fargate has no cost; it is included free with any AWS account

86. Which of the following does a team using the Fargate launch type NOT need to do, unlike a team using the ECS EC2 launch type?
A) Define a task definition
B) Provision, patch, and scale the underlying EC2 instances that run the tasks
C) Attach a task role for application permissions
D) Specify container images to run

87. Which phrase, when it appears in a DVA-C02 scenario about container compute, most strongly signals that Fargate is favored over the ECS EC2 launch type?
A) "Full control over the underlying host operating system is required"
B) "Least operational overhead" or "no interest in managing the underlying servers"
C) "Requires GPU-accelerated instances"
D) "Requires custom AMIs with specialized kernel modules"

88. Which requirement would most strongly point away from Fargate and toward the ECS EC2 launch type instead?
A) Unpredictable, bursty traffic with no desire to manage host capacity
B) A need for GPU-accelerated instance types or very high-density bin-packing to minimize cost at large steady-state scale, both of which require host-level control Fargate does not expose
C) A desire to eliminate all EC2 patching responsibilities
D) A small team with no dedicated infrastructure staff

89. Is AWS Fargate exclusively an ECS feature, or can it also be used with Amazon EKS?
A) Fargate is exclusive to ECS and cannot be used with EKS
B) Fargate can also run Kubernetes pods for EKS clusters via Fargate profiles, avoiding the need to manage EC2 worker nodes for matching pods
C) Fargate can only be used with AWS Lambda
D) Fargate requires a Kubernetes cluster to function under ECS

90. A finance team compares the raw per-vCPU-hour cost of Fargate against an equivalent EC2 instance type running the same container workload and finds Fargate's rate is higher. Which two statements correctly explain this tradeoff? (Select TWO)
A) Fargate's higher per-unit rate reflects the elimination of EC2 host provisioning, patching, and capacity-planning overhead
B) Choosing between Fargate and the EC2 launch type should weigh operational overhead savings against raw per-unit compute cost, not compute cost alone
C) Fargate provides no operational benefit in exchange for its higher rate
D) The EC2 launch type always has zero operational overhead, making it strictly superior
E) Fargate's higher rate means it is never the correct exam answer

91. What does a Fargate platform version control?
A) The version of Kubernetes running the cluster
B) The specific runtime environment and feature set (such as ECS Exec support) available to Fargate tasks, which AWS periodically updates
C) The IAM policy version attached to the task role
D) The version of the ECR repository

92. Which two of the following are accurate characteristics of AWS Fargate? (Select TWO)
A) It eliminates the need to provision or patch underlying EC2 instances for running containers
B) It bills based on the vCPU and memory resources a task actually reserves, per second
C) It requires the customer to manually install and patch a hypervisor
D) It is only compatible with the EC2 launch type, never used as a launch type itself
E) It guarantees a lower total bill than the EC2 launch type in every scenario, regardless of workload shape

93. A Fargate task is being OOM-killed (terminated for exceeding its memory allocation) under normal load. What is the appropriate fix?
A) SSH into the underlying host and manually add more RAM
B) Update the task definition to increase the task's provisioned memory value to an amount sufficient for the workload, then redeploy the service with the updated task definition revision
C) Nothing can be done; Fargate memory limits cannot be changed
D) Switch the AWS Region

94. A company runs two distinct ECS workloads: Workload X has stable, predictable, 24/7 resource needs at large scale, where the team is willing to invest engineering time to bin-pack tasks tightly onto Reserved Instances for maximum cost efficiency. Workload Y has highly unpredictable, spiky traffic and the team wants to avoid any host-capacity planning. Which launch type pairing best fits Workload X and Workload Y, respectively?
A) Fargate for X, EC2 launch type for Y
B) EC2 launch type for X, Fargate for Y
C) Fargate for both
D) EC2 launch type for both

95. A workload requires running containers in privileged mode with direct access to host-level device drivers not exposed through the standard container runtime. Which ECS launch type is appropriate given this requirement?
A) Fargate, since it always supports every container configuration
B) The EC2 launch type, since it provides the underlying host access that certain privileged or device-driver-dependent configurations require, unlike Fargate's more restricted environment
C) Neither launch type can ever run privileged containers
D) AWS Lambda

96. A team runs two ECS workloads on Fargate: a customer-facing checkout API that must never be abruptly interrupted, and an internal nightly report-generation batch job that can tolerate being interrupted and simply retried. Which Fargate capacity choice fits each workload, respectively?
A) Standard Fargate for the checkout API, and Fargate Spot for the batch job
B) Fargate Spot for both workloads, to minimize cost uniformly
C) Standard Fargate for both workloads, since Fargate Spot cannot run batch jobs
D) The EC2 launch type is required for any interruption-tolerant workload

### Amazon EKS (97–111)

97. What does Amazon EKS (Elastic Kubernetes Service) provide?
A) A fully managed, AWS-proprietary container orchestration API with no relation to Kubernetes
B) A managed Kubernetes control plane, run and patched by AWS across multiple Availability Zones, on which customers run standard, open-source Kubernetes workloads
C) A tool exclusively for building container images
D) A replacement for IAM

98. What is the fundamental architectural difference between Amazon ECS and Amazon EKS?
A) ECS uses AWS's own proprietary container orchestration API and concepts, while EKS runs the open-source Kubernetes API, which is portable across other Kubernetes-conformant platforms
B) ECS and EKS are simply two different names for the exact same underlying service
C) EKS does not support container images, only virtual machines
D) ECS requires Kubernetes knowledge, while EKS does not

99. A company has an established on-premises Kubernetes footprint, existing Helm charts, custom Kubernetes operators, and a stated goal of maintaining the ability to run the same workload on another cloud provider in the future. Which AWS container orchestration service best aligns with these constraints?
A) Amazon ECS, because it is simpler to learn
B) Amazon EKS, because it preserves compatibility with the company's existing Kubernetes tooling and the portability of the open-source Kubernetes API across providers
C) AWS Lambda
D) Amazon EC2 with no orchestrator at all

100. A small team building a new application from scratch on AWS, with no prior Kubernetes experience and no multi-cloud requirement, wants to run containers with the simplest possible AWS-native orchestration setup. Which service best fits, absent any other constraints?
A) Amazon EKS, for its larger open-source ecosystem
B) Amazon ECS, since it avoids the added complexity of learning Kubernetes concepts when there is no existing Kubernetes investment or portability requirement
C) AWS Batch exclusively
D) A self-managed Kubernetes cluster on raw EC2

101. A company adopts Amazon EKS for Kubernetes-API portability but does not want to provision or manage EC2 worker nodes for a specific set of stateless microservices. Which EKS capability lets specific pods run without customer-managed EC2 worker nodes?
A) EKS does not support any serverless compute option; worker nodes are always required
B) EKS with Fargate, using a Fargate profile to match specific namespaces/labels so those pods run on Fargate instead of self-managed EC2 worker nodes
C) AWS Lambda functions replacing the pods entirely
D) ECS Exec

102. For an EKS cluster using self-managed (non-Fargate) EC2 worker nodes, which two statements accurately describe operational responsibility for those nodes? (Select TWO)
A) The customer is ultimately responsible for the worker nodes as EC2 resources, including OS-level patching
B) AWS-managed node groups can automate much of the worker node lifecycle (such as provisioning and updates) while the underlying instances remain customer-owned EC2 resources
C) AWS fully and automatically patches every self-managed worker node with no customer involvement
D) Worker nodes never require patching once launched
E) Worker node management is identical to Fargate's fully serverless model

103. What does AWS manage on behalf of the customer for an Amazon EKS cluster's control plane?
A) Nothing; the customer manages every control plane component themselves
B) The Kubernetes control plane components (such as the API server and etcd), which AWS runs highly available across multiple Availability Zones and patches
C) Only the container images stored in the customer's repositories
D) The customer's on-premises data center

104. Which EKS mechanism most closely parallels the ECS task role, allowing individual Kubernetes pods (rather than an entire node) to be granted scoped IAM permissions for calling AWS services?
A) IAM Roles for Service Accounts (IRSA), which maps a Kubernetes service account to an IAM role
B) The EKS cluster IAM role
C) The task execution role
D) EKS does not support per-pod IAM scoping; all pods share the worker node's role

105. Approximately how deep does the DVA-C02 exam go into Kubernetes-specific architecture (such as detailed pod scheduling internals or custom resource definitions) when testing knowledge of Amazon EKS?
A) Extremely deep — candidates must be able to design multi-cluster Kubernetes networking topologies
B) Developer-level awareness only — knowing what EKS is, how it differs from ECS, and when a team would choose it, without deep Kubernetes architecture (that is out of scope for this associate-level developer exam)
C) The exam requires writing custom Kubernetes controllers from memory
D) EKS is not mentioned on the exam at all

106. Which two of the following statements accurately distinguish Amazon ECS from Amazon EKS? (Select TWO)
A) EKS runs the open-source Kubernetes API, making workloads more portable to other Kubernetes-conformant platforms than ECS's proprietary model
B) ECS generally has a simpler learning curve for teams with no existing Kubernetes investment
C) ECS is built on top of Kubernetes internally, with a different name
D) EKS cannot be used with Fargate under any configuration
E) ECS and EKS charge identical hourly control-plane fees

107. Regarding cost structure, which statement accurately compares Amazon ECS and Amazon EKS?
A) Both charge an identical hourly control-plane fee
B) Amazon EKS charges an hourly fee for the managed Kubernetes control plane (in addition to the cost of worker nodes or Fargate tasks), whereas ECS does not charge a separate fee for the ECS control plane itself — customers pay only for the underlying compute (EC2 or Fargate) their tasks consume
C) ECS charges more than EKS in every scenario
D) Neither service has any associated cost beyond data transfer

108. A startup building an entirely new application on AWS has no existing Kubernetes experience today, but explicitly states a long-term strategic goal of avoiding vendor lock-in and wanting the option to run the same workload on a different cloud provider in the future if business needs change. Despite the added learning curve, which orchestration choice best supports this stated strategic goal?
A) Amazon ECS, since it is simpler to start with
B) Amazon EKS, since its Kubernetes API foundation is the AWS option most aligned with cross-cloud portability, even though it requires learning Kubernetes concepts the team doesn't have today
C) AWS Lambda, since serverless functions are inherently more portable than any container orchestrator
D) Elastic Beanstalk

109. How does an EKS Fargate profile determine which pods run on Fargate instead of on self-managed EC2 worker nodes?
A) By randomly assigning pods to Fargate or EC2 worker nodes
B) By matching pods based on configured Kubernetes namespace and/or label selectors defined in the Fargate profile
C) By the size of the container image alone
D) EKS Fargate profiles apply to the entire cluster uniformly with no selective matching

110. Does the Amazon EKS control plane run across multiple Availability Zones for resilience, without the customer having to configure this themselves?
A) No, the customer must manually deploy and manage redundant control plane instances across AZs
B) Yes, AWS runs the managed EKS control plane across multiple Availability Zones automatically as part of the managed service
C) The control plane always runs in a single AZ with no redundancy
D) EKS has no concept of Availability Zones

111. An EKS cluster uses self-managed EC2 worker nodes. A specific pod's application code needs permission to read from an S3 bucket, but the team does not want to grant that broad permission to every pod running on the same worker node via the node's shared IAM role. Which mechanism achieves pod-scoped, rather than node-wide, permissions?
A) Broadening the worker node's IAM role, accepting that every pod on that node gains the same access
B) IAM Roles for Service Accounts (IRSA), mapping the specific pod's Kubernetes service account to a narrowly scoped IAM role
C) Attaching an ECS task role to the pod
D) There is no way to scope permissions below the node level in EKS

### Integrative Scenarios & Comparison (112–123)

112. A team is choosing among ECS EC2 launch type, ECS Fargate, and Amazon EKS for a brand-new containerized workload with no existing Kubernetes investment and a strong preference for minimal infrastructure management. Which option best fits, absent other constraints?
A) ECS EC2 launch type, for maximum control
B) ECS Fargate, since it combines AWS-native simplicity with no host management, and there's no stated need for Kubernetes portability
C) Amazon EKS with self-managed worker nodes
D) A self-managed Kubernetes cluster on raw EC2 instances

113. A CI/CD pipeline builds a container image, pushes it to ECR tagged with the Git commit SHA, and updates an ECS service to deploy that exact image tag. Which two statements correctly describe why this pattern satisfies the exam's expectations for a controlled, traceable container deployment? (Select TWO)
A) Tagging the image with the immutable commit SHA (rather than only a mutable tag like latest) creates a precise, traceable, versioned deployment artifact
B) Updating the ECS service to a new task definition revision referencing that specific tag is the mechanism that actually promotes the new version into the running environment
C) The Git commit SHA tag is only cosmetic and has no bearing on deployment traceability
D) ECS always deploys the latest image automatically regardless of which tag the task definition references
E) Container image tags are irrelevant to the exam's Deployment domain

114. Following a bad deployment where an ECS service was updated to a new, buggy image tag via a new task definition revision, what is the fastest, most direct way to roll back?
A) Rebuild the previous image from source and manually re-push it under a brand-new tag
B) Update the ECS service to reference the previous, known-good task definition revision, which still points at the previous image tag
C) Delete the ECS cluster and recreate it from a backup
D) Manually SSH into the underlying hosts and downgrade the running binary

115. A security review of a company's container pipeline finds: (1) ECR image scanning is disabled, allowing known-vulnerable images to be deployed unnoticed, and (2) the ECS task role for a customer-facing service is attached to a broad, unscoped policy far beyond what the application actually calls. Which two remediations correctly address these two findings, respectively? (Select TWO)
A) Enable ECR image scanning (basic or enhanced) and gate the pipeline on its findings
B) Replace the task role's broad policy with a narrowly scoped policy limited to the specific AWS actions and resources the application actually needs
C) Disable the task execution role entirely, since it is unrelated to application permissions
D) Make the ECR repository public to simplify scanning
E) Grant the task role AdministratorAccess to eliminate future permission errors

116. A company migrating an existing on-premises Kubernetes workload to AWS wants to preserve its Helm-based deployment tooling and avoid provisioning or patching any EC2 worker nodes for the migrated service. Which two AWS capabilities together satisfy both requirements? (Select TWO)
A) Amazon EKS, preserving Kubernetes API compatibility (and thus Helm compatibility)
B) An EKS Fargate profile matching the migrated service's namespace, avoiding EC2 worker node management for those pods
C) Amazon ECS with the EC2 launch type
D) AWS Lambda container image support
E) ECS Fargate, since it also runs the Kubernetes API

117. Summarizing the module's most heavily tested distinction, which two statements correctly capture the difference between an ECS task role and a task execution role? (Select TWO)
A) The task execution role is used by ECS/the container agent to pull images, write logs, and retrieve injected secrets before and during task startup
B) The task role is used by the application code running inside the container to call AWS services at runtime, such as S3 or DynamoDB
C) Both roles are always identical and interchangeable in every task definition
D) The task role is responsible for pulling the container image from ECR
E) The task execution role is what an application uses to read from a DynamoDB table

118. Which statement correctly compares the pricing models of the ECS EC2 launch type and the ECS Fargate launch type?
A) Both are billed identically, per vCPU-second, with no distinction
B) The EC2 launch type bills for the provisioned EC2 instances themselves (On-Demand, Reserved, or Spot), regardless of per-task utilization, while Fargate bills per task based on the vCPU/memory actually reserved, per second
C) Fargate is billed as a flat monthly subscription unrelated to usage
D) The EC2 launch type has no cost at all; only Fargate incurs charges

119. A platform team runs one steady-state, high-density service and one highly bursty, unpredictable service on the same ECS cluster, and wants each to use the most cost-appropriate capacity model without operating two separate clusters. Which two approaches correctly achieve this within a single ECS cluster? (Select TWO)
A) Configure the cluster with both an EC2 Auto Scaling group capacity provider (for the steady-state, bin-packed service) and a Fargate capacity provider (for the bursty service), assigning each service the appropriate one
B) Run the steady-state service on the EC2 launch type and the bursty service on Fargate, both within the same cluster
C) Require every service in a cluster to use the exact same launch type
D) Migrate the bursty service to a separate AWS account to use Fargate
E) Disable Application Auto Scaling entirely to simplify capacity planning

120. Consistent with the DVA-C02 exam guide's general emphasis on implementing against existing designs rather than architecting from scratch, which of the following is most likely OUT of scope for this exam regarding EKS?
A) Recognizing what EKS is and when a team would choose it over ECS
B) Designing detailed Kubernetes cluster networking topology and custom controller architecture from scratch
C) Knowing that EKS runs the open-source Kubernetes API
D) Knowing that EKS supports a Fargate compute option

121. Which two statements accurately describe how a CodeBuild project authenticates and pushes a newly built image to a private ECR repository as part of a pipeline? (Select TWO)
A) The CodeBuild service role must have ECR push permissions, and privileged mode must typically be enabled to run the Docker daemon during the build
B) The build script obtains a temporary registry authentication token via aws ecr get-login-password and pipes it into docker login before pushing
C) ECR authentication requires a permanent, manually rotated username and password stored in the buildspec file
D) CodeBuild cannot interact with ECR under any configuration
E) The pushed image is automatically scanned by CodePipeline itself rather than ECR

122. Per the DVA-C02 exam guide's deployment domain, which two practices together represent a sound "approved-version environment" pattern when deploying containerized applications? (Select TWO)
A) Deploying a specific, versioned container image tag (ideally pinned to an immutable digest or commit SHA) that has been validated and promoted through environments
B) Referencing that specific image tag explicitly in the task definition revision the service is updated to use, rather than relying on a mutable tag like latest
C) Always deploying whichever image was most recently pushed to the registry, regardless of tag
D) Manually editing files inside a running container to apply a fix in place
E) Deleting the task definition after every deployment to avoid version drift

123. A company evaluating its container strategy wants: (1) the simplest possible path for a brand-new, AWS-only service with no host management, (2) continuous vulnerability rescanning for all pushed images, and (3) a path to bring an existing, portable Kubernetes-based workload from another cloud with minimal rework. Which three choices correctly satisfy these three needs, respectively? (Select THREE)
A) ECS Fargate for the new, AWS-only, no-host-management service
B) ECR enhanced scanning (powered by Amazon Inspector) for continuous vulnerability rescanning
C) Amazon EKS for the portable, existing Kubernetes workload
D) The ECS EC2 launch type for the new, no-host-management service
E) ECR basic scanning for continuous rescanning without re-pushing images

---

## Answer Key & Explanations

1. B — Namespaces and cgroups provide process, filesystem, and resource isolation while every container shares the host's single kernel.
2. B — An image is the read-only template; a container is a running instance created from it.
3. B — FROM selects the base image (Alpine + Node 20 here) that subsequent instructions build on top of.
4. A — Copying the dependency manifest and installing dependencies before the rest of the source lets Docker reuse the cached dependency layer when only source changes.
5. A — Every instruction produces a cached layer, and unchanged layers are reused on rebuild and not re-downloaded on pull.
6. B — A container shares the host's already-running kernel and starts a process, while an EC2 instance must boot a full guest OS.
7. C — CMD defines the command that runs when a container starts; RUN executes only at build time.
8. A & B — Containers share the host kernel (no hypervisor-per-container) and start dramatically faster than a full VM boot.
9. B — A specific, versioned tag is a stable, traceable deployment artifact, unlike a mutable tag whose content can change silently.
10. A — EXPOSE documents/enables the listening port for container linking but does not itself publish the port to the host.
11. B — Installing dependencies before copying source maximizes layer-cache reuse on source-only rebuilds.
12. A & B — A container image bundles code with its runtime/dependencies and is composed of cached, reusable Dockerfile-instruction layers.
13. B — Private repositories keep proprietary images access-controlled; a public repository is designed for anonymous public distribution.
14. B — Enhanced scanning (Amazon Inspector) continuously reassesses images against newly published CVEs without requiring a re-push.
15. B — aws ecr get-login-password issues a temporary, IAM-derived token piped into docker login; there is no static registry password.
16. A — A lifecycle policy natively automates expiration of old/untagged images without custom cleanup scripting.
17. B — Pushing requires ECR permissions like GetAuthorizationToken, InitiateLayerUpload, and PutImage on the CodeBuild service role.
18. A — A resource-based ECR repository policy can grant pull permissions to principals in another AWS account.
19. A — Image tag immutability rejects pushes that would overwrite an existing tag, preserving tag-to-content traceability.
20. B — imagedefinitions.json is the standard hand-off artifact naming the container and new image URI for the ECS deploy action.
21. B — ECR basic scanning is powered by the open-source Clair scanner.
22. B — Enhanced scanning adds continuous rescanning as new CVEs are published, plus deeper OS/language-package coverage, via Amazon Inspector.
23. A & B — The token is a temporary, IAM-credential-derived token, valid for up to 12 hours before needing refresh.
24. B — A repository-scoped resource policy grants precise cross-account pull access to just that one repository.
25. B — Once pushed, any layer (including removed-later content) remains retrievable from the registry, so the exposed secret must be rotated.
26. A — The task execution role needs ECR authentication/pull permissions so the ECS agent can retrieve the image on the task's behalf.
27. B — ECR private repository storage is billed per GB stored per month, aside from data transfer charges.
28. A — A count-based lifecycle rule with a tag-prefix match keeps only the specified number of most recent matching images.
29. A — Privileged mode grants the CodeBuild environment the access needed to run a Docker daemon during the build.
30. A & B — Both image scanning and lifecycle policies are native ECR capabilities requiring no external tooling.
31. B — ECR public repositories allow anonymous, credential-free pulls, matching their public-distribution purpose.
32. A, B & C — Scanning flags vulnerabilities, tag immutability prevents silent tag overwrites, and a lifecycle policy expires old untagged images.
33. B — A task definition is the JSON blueprint describing containers, resources, networking, and IAM roles for a task.
34. B — The task execution role covers ECS's own startup needs: pulling images, writing logs, and fetching injected secrets.
35. A — The task role governs what the application code inside the container can call at runtime.
36. B — Application-level AWS API failures (like S3 AccessDenied) are fixed via the task role, not the execution role, which already did its job by launch time.
37. B — Failure to pull the image points to the task execution role, which governs ECS's ECR authentication and pull permissions.
38. B — The task execution role must be able to retrieve the secret value so ECS can inject it as an environment variable at startup.
39. A & B — Task role = application runtime permissions; task execution role = ECS's own startup-time plumbing permissions.
40. B — Top-level cpu/memory reserves the total resources for the task, required for Fargate and shared across its containers.
41. B — With awsvpc, each task gets its own ENI/IP, letting the ALB route directly to individual tasks rather than a shared host port.
42. B — ECS retains prior task definition revisions, so pointing the service back at revision 13 rolls back instantly.
43. B — The awslogs driver streams container output to CloudWatch Logs, requiring log-write permissions on the task execution role.
44. A & B — Narrow the task role to only the needed DynamoDB actions/resource, and add CloudWatch Logs write permissions to the execution role.
45. B — The family groups all revisions of a task definition under one name so a service can reference the latest or a specific revision.
46. B — A task definition has one task-level role that all containers within that single task share.
47. B — With no task role attached, the container has no AWS credentials available via its credential provider chain, so the call fails.
48. B — A secrets entry avoids storing the sensitive value in plaintext in the task definition, retrieved via the task execution role's permissions.
49. A — Fargate requires top-level task cpu/memory; EC2 launch type additionally allows per-container reservations for flexible host bin-packing.
50. B — A secrets reference to the Secrets Manager ARN retrieves the current value at startup via the execution role, independent of the task definition content.
51. A & B — A task definition groups one or more containers as a unit and is revisioned, with services able to reference any prior revision.
52. B — ecs-tasks.amazonaws.com is the service principal ECS uses to assume both the task role and task execution role.
53. A — containerPort specifies the port the application listens on inside the container.
54. A & B — Incident 1 (secret retrieval failure) is an execution-role fix; Incident 2 (application S3 AccessDenied) is a task-role fix.
55. B — A cluster is the logical grouping/namespace for a set of tasks, services, and (for EC2 launch type) registered instance capacity.
56. B — A service continuously reconciles running task count against desired count, launching a replacement for any stopped task.
57. B — ECS automatically registers newly launched tasks and deregisters stopped ones from the associated target group.
58. B — Target tracking automatically maintains a target metric value (like CPU) without manually defined step thresholds, mirroring ASG target tracking.
59. B — On the EC2 launch type, the customer owns patching and maintaining the underlying registered EC2 instances.
60. B — Fargate removes all customer-visible host provisioning, patching, and scaling — there is no EC2 fleet to manage.
61. A & B — EC2 launch type exposes GPU instance types and instance-level RI/Savings Plan discounts plus custom placement for dense bin-packing.
62. B — Fargate eliminates host provisioning/patching/capacity planning, matching a "least operational overhead" priority for spiky traffic.
63. B — Minimum 100%/maximum 200% keeps full capacity available throughout the deployment while new and old tasks briefly coexist.
64. B — A CodeDeploy-integrated blue/green deployment manages controlled traffic shifting (and rollback) between old and new task sets.
65. A — A capacity provider defines and associates the underlying infrastructure (ASG or Fargate/Fargate Spot) a cluster uses to place tasks.
66. A & B — A service maintains desired count automatically and can integrate with a load balancer and Application Auto Scaling; a standalone task does neither.
67. A — Fargate Spot offers a discount for interruption-tolerant workloads, directly analogous to EC2 Spot Instances.
68. B — A single ECS cluster can mix services across both the EC2 and Fargate launch types simultaneously.
69. A & B — binpack and spread are ECS task placement strategies controlling task distribution across a cluster's EC2 instances.
70. B — Updating a service's task definition triggers a new deployment that incrementally replaces tasks per the deployment configuration.
71. B — Min/max task counts bound the range within which the service's desired count is automatically adjusted by its scaling policy.
72. A — Target group deregistration delay lets in-flight requests complete before a deregistering task is fully removed.
73. A & B — EC2 launch type exposes host/instance-type control (including GPU); Fargate removes host patching/scaling burden.
74. A — AWS Cloud Map integration provides automatic DNS-based service discovery tracking task IPs as they start and stop.
75. B — Tasks stay PENDING when the cluster's registered EC2 instances lack sufficient unreserved CPU/memory to place them; scale the ASG or use Fargate.
76. B — Fargate has no customer-managed host fleet to exhaust capacity on — AWS provisions exactly the capacity each task needs.
77. B — ECS Exec opens an interactive shell or runs a command inside a running container for live debugging.
78. B — ECS Exec parallels Session Manager: IAM-governed access with no inbound ports or SSH required.
79. A & B — ECS Exec requires enableExecuteCommand on the task/service and SSM messaging permissions on the task role.
80. B — ECS Exec provides IAM/SSM-based interactive access into a running Fargate container with no inbound ports needed.
81. B — ECS Exec works on both EC2 and Fargate launch types, subject to platform version/configuration requirements.
82. B — ECS Exec session activity can be logged to CloudWatch Logs or S3 for audit, mirroring Session Manager logging.
83. B — A missing SSM messaging permission on the task role is a common reason an enabled ECS Exec session still fails to start.
84. A — ECS Exec avoids the attack surface, image bloat, and key management of embedding SSH servers, while centralizing access via IAM.
85. B — Fargate bills per task based on provisioned vCPU/memory, per second, with a minimum billing duration.
86. B — Fargate removes the need to provision, patch, or scale underlying EC2 instances, unlike the EC2 launch type.
87. B — "Least operational overhead" / no interest in host management signals Fargate over the EC2 launch type.
88. B — GPU instance needs and deep bin-packing for cost at scale require host-level control that Fargate does not expose.
89. B — Fargate profiles let EKS run Kubernetes pods on Fargate without customer-managed EC2 worker nodes.
90. A & B — The higher per-unit rate reflects eliminated host management overhead, so the choice should weigh overhead savings against raw cost.
91. B — A Fargate platform version controls the runtime/feature set (including capabilities like ECS Exec) available to tasks.
92. A & B — Fargate removes EC2 provisioning/patching and bills per task based on actual vCPU/memory reserved, per second.
93. B — Increasing the task definition's provisioned memory and redeploying is the correct fix for a Fargate task being OOM-killed.
94. B — Steady-state, bin-packable Workload X fits the EC2 launch type's RI/density advantages; bursty Workload Y fits Fargate's no-capacity-planning model.
95. B — The EC2 launch type provides underlying host access needed for privileged or device-driver-dependent container configurations.
96. A — Standard Fargate suits an interruption-intolerant workload; Fargate Spot suits the interruption-tolerant batch job, minimizing its cost.
97. B — EKS is a managed, multi-AZ Kubernetes control plane on which customers run standard open-source Kubernetes workloads.
98. A — ECS uses an AWS-proprietary orchestration API; EKS runs the portable, open-source Kubernetes API.
99. B — Existing Kubernetes tooling and a multi-cloud portability goal both point to EKS's open-source Kubernetes API foundation.
100. B — With no existing Kubernetes investment or portability need, ECS's simpler AWS-native model is the more direct fit.
101. B — An EKS Fargate profile matches namespaces/labels so those pods run on Fargate without customer-managed worker nodes.
102. A & B — The customer ultimately owns self-managed worker nodes as EC2 resources, though AWS-managed node groups can automate much of that lifecycle.
103. B — AWS runs and patches the Kubernetes control plane components (API server, etcd) across multiple AZs on the customer's behalf.
104. A — IAM Roles for Service Accounts (IRSA) map a Kubernetes service account to an IAM role, scoping permissions per pod, paralleling the ECS task role.
105. B — DVA-C02 expects developer-level EKS awareness (what it is, how it differs from ECS, when to choose it), not deep Kubernetes architecture.
106. A & B — EKS's open API is more portable; ECS has a simpler learning curve absent existing Kubernetes investment.
107. B — EKS charges an hourly control-plane fee on top of worker node/Fargate costs; ECS has no separate control-plane fee.
108. B — Despite the learning curve, EKS's Kubernetes API foundation is the AWS option best aligned with future cross-cloud portability.
109. B — A Fargate profile selects pods by Kubernetes namespace and/or label selectors to route them onto Fargate.
110. B — AWS runs the managed EKS control plane across multiple Availability Zones automatically, with no customer configuration needed.
111. B — IRSA maps a specific pod's Kubernetes service account to a narrowly scoped IAM role, avoiding node-wide permission sharing.
112. B — With no Kubernetes investment and a preference for minimal management, Fargate's no-host-management, AWS-native model fits best.
113. A & B — An immutable commit-SHA tag creates a traceable artifact, and updating the service to a new revision referencing it is what actually promotes it.
114. B — Pointing the service back at the previous task definition revision (and thus the previous image tag) is the fastest rollback.
115. A & B — Enabling ECR scanning addresses the vulnerability-detection gap; narrowing the task role addresses the over-permissioned application role.
116. A & B — EKS preserves Kubernetes/Helm compatibility, and a Fargate profile avoids managing EC2 worker nodes for the migrated service.
117. A & B — The execution role handles ECS's own startup plumbing (pulling images, logging, secrets); the task role handles the application's runtime AWS calls.
118. B — EC2 launch type bills for provisioned instances regardless of per-task utilization; Fargate bills per task for actual vCPU/memory reserved, per second.
119. A & B — Capacity providers (or simply running each service under its appropriate launch type) let one cluster mix EC2- and Fargate-backed services.
120. B — Deep Kubernetes networking/controller design from scratch is out of scope; recognizing what EKS is and when to use it is in scope.
121. A & B — The CodeBuild role needs ECR push permissions (and typically privileged mode for the Docker daemon), authenticating via get-login-password piped into docker login.
122. A & B — A specific, promoted, immutable-style image tag referenced explicitly by the task definition revision is the approved-version deployment pattern.
123. A, B & C — Fargate fits the no-host-management new service, ECR enhanced scanning provides continuous rescanning, and EKS fits the portable existing Kubernetes workload.
