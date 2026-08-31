# Module 10 — Practice Questions (135)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### AWS CodeCommit (1–14)

1. A startup wants to host private Git repositories for its application source code without operating its own Git server, and wants repository access controlled through the same identity system already used for every other AWS resource in the account. Which AWS service and access model satisfies this?
A) GitHub Enterprise Server running on a self-managed EC2 instance
B) AWS CodeCommit, with access controlled entirely through IAM policies
C) Amazon S3 versioning used as a substitute for Git
D) AWS CodeArtifact configured as a source repository

2. A developer needs to push and pull from a CodeCommit repository using a standard Git HTTPS client, but does not want to use their IAM console password or long-term access keys for this purpose. Which credential type should they generate?
A) A CloudFront signed URL
B) IAM-generated HTTPS Git credentials, a username/password pair scoped specifically to Git operations
C) A root user access key
D) A CodeArtifact authorization token

3. A CI/CD pipeline runner already operates under an IAM role and needs to clone a CodeCommit repository without provisioning or storing any separate Git credentials (HTTPS or SSH) for the operation. Which approach lets the runner authenticate using its existing IAM role directly?
A) git-remote-codecommit, which uses the caller's existing IAM credentials directly for Git operations
B) Generating a new IAM user with console access for the pipeline
C) Embedding the root user's access keys in the buildspec
D) Disabling authentication on the repository entirely

4. A team wants every push to the `main` branch of their CodeCommit repository to automatically start a CodePipeline execution, with minimal latency between the commit and the pipeline starting, and without the pipeline having to continuously poll the repository. Which mechanism achieves this in the modern, recommended configuration?
A) A scheduled CloudWatch cron job that checks the repository every hour
B) An Amazon EventBridge rule that reacts to the repository's push event and starts the pipeline
C) A manual click of "Release change" in the console after every commit
D) An AWS Config rule evaluating repository compliance

5. A team wants to require at least two engineers to approve a pull request in CodeCommit before it can be merged into a protected branch. Which CodeCommit feature enforces this?
A) A resource-based bucket policy
B) An approval rule template attached to the repository
C) A CodeBuild buildspec validation phase
D) An AppConfig validator

6. Which of the following authentication methods is natively supported for connecting a standard Git client to an AWS CodeCommit repository?
A) SSH keys uploaded to an IAM user, or IAM-generated HTTPS Git credentials
B) A shared repository-wide password distributed by email
C) OAuth tokens issued by a third-party identity provider with no IAM involvement
D) Anonymous, unauthenticated HTTPS access enabled by default

7. A company migrating from a self-hosted GitLab server wants a private, managed Git hosting option with the least possible ongoing operational overhead, while keeping repository permissions fully auditable through their existing IAM policies and CloudTrail logs. Which choice best satisfies both requirements?
A) A larger self-hosted GitLab instance on a Reserved Instance
B) AWS CodeCommit
C) A public GitHub repository with branch protection rules
D) An S3 bucket storing zipped source snapshots

8. A security engineer reviewing CodeCommit access wants to confirm that a departed employee's ability to push and pull code was fully revoked. Where should this be verified, given that CodeCommit has no separate user directory of its own?
A) In CodeCommit's own standalone user management console
B) In IAM — by reviewing and removing the departed employee's IAM user, its HTTPS Git credentials, and any uploaded SSH public keys
C) In the CodeBuild service role
D) In the CodeArtifact domain policy

9. A team wants to notify a Slack channel via an SNS topic whenever a new branch is created in their CodeCommit repository, independent of any CodePipeline execution. Which CodeCommit capability supports sending this kind of event notification?
A) CodeCommit triggers, which can invoke SNS notifications or Lambda functions on repository events such as branch creation
B) A CodeBuild post_build phase
C) A CodeDeploy ValidateService hook
D) An AppConfig deployment strategy

10. Which two of the following statements about AWS CodeCommit are accurate? (Select TWO)
A) Repository access is granted through IAM identity-based policies referencing CodeCommit actions such as codecommit:GitPull and codecommit:GitPush
B) CodeCommit maintains its own independent user and password system separate from IAM
C) A CodePipeline source stage can be configured to trigger automatically when a commit lands on a specified branch
D) CodeCommit repositories cannot support multiple branches simultaneously
E) SSH access to CodeCommit requires disabling IAM entirely for the account

11. A company wants to migrate its existing GitHub-hosted source code into a CodePipeline-based release process without first moving the repository itself into CodeCommit. Which statement about CodePipeline source options is accurate?
A) CodePipeline can only source from CodeCommit; GitHub is never supported as a source provider
B) CodePipeline can source directly from a GitHub repository via a CodeStar Connection, without requiring the code to first live in CodeCommit
C) GitHub repositories must be manually zipped and uploaded to S3 before CodePipeline can use them
D) CodePipeline requires converting the GitHub repository's history into CodeArtifact packages first

12. Which two of the following are legitimate ways a CodeCommit repository event can be surfaced to other systems? (Select TWO)
A) An SNS notification triggered by a repository event such as a push
B) An EventBridge rule matching a CodeCommit repository state-change event, used to start a CodePipeline execution
C) A DynamoDB Stream attached directly to the repository
D) A Route 53 health check monitoring repository push activity
E) An ACM certificate renewal event tied to the repository

13. A developer accidentally committed a plaintext database password to a CodeCommit repository's main branch several commits ago, and it has since been merged into multiple downstream branches. What is the most correct characterization of how to remediate this from a security standpoint?
A) Simply deleting the file in a new commit fully removes the exposed credential from all history and no further action is needed
B) The credential must be treated as compromised and rotated immediately (e.g., in Secrets Manager), in addition to any history-cleanup effort, since prior commits may already be cloned or cached elsewhere
C) CodeCommit automatically scrubs credentials from history the moment a new commit is pushed
D) Because CodeCommit is private, an exposed credential in the repository poses no real risk
E) Rotating the credential is unnecessary since git history rewriting alone always fully solves the issue

14. A team wants pipeline executions triggered only when changes are pushed to release branches matching a specific naming pattern (e.g., `release/*`), rather than on every branch. Which capability supports this kind of selective, pattern-based source triggering for a CodePipeline sourced from CodeCommit?
A) CodePipeline source triggers can be scoped to specific branches or, in newer trigger configurations, branch name filters, rather than firing on every branch equally
B) CodeCommit repositories can only ever have one branch, making this moot
C) This requires a fully separate repository per branch
D) Branch-based trigger filtering is not possible under any circumstance in CodePipeline

### AWS CodeBuild (15–36)

15. A team's buildspec.yml needs to install required npm packages, run unit tests before compiling, transpile the TypeScript source, and then upload a test report to S3, in that specific order. Which four buildspec phases, used in the standard order, map to these four steps?
A) build, install, post_build, pre_build
B) install, pre_build, build, post_build
C) pre_build, install, post_build, build
D) post_build, build, pre_build, install

16. A CodeBuild project's build phase fails partway through due to a compilation error, but the team still wants a notification command in post_build to run so the team is alerted regardless of the failure. What is the actual behavior of the post_build phase in this situation?
A) post_build commands are skipped entirely whenever the build phase fails
B) post_build commands still run even after a build-phase failure, though the overall build is still reported as failed
C) The entire CodeBuild project is permanently disabled after any build-phase failure
D) post_build only runs if every previous phase, including build, succeeded with zero warnings

17. A team wants to pin a specific Node.js runtime version for a CodeBuild project using one of AWS's managed build images, without creating and maintaining a custom Docker image. Where in the buildspec is this configured?
A) In the artifacts section, under discard-paths
B) In the install phase, using the runtime-versions setting
C) In the cache section, under paths
D) In the env section, under exported-variables

18. A CodeBuild project needs to build and push a Docker image to Amazon ECR as part of its build phase, which requires running the Docker daemon inside the build container itself. Which CodeBuild project setting must be enabled for this to succeed?
A) Privileged mode
B) VPC connectivity
C) Local caching
D) A larger compute type only, with no other change needed

19. A buildspec needs to inject a database password into the build environment without ever exposing the plaintext value in the CodeBuild console's environment variable list or in build logs as a stored setting. Which buildspec mechanism is designed for this?
A) Defining the password as a plaintext value under env: variables
B) Referencing the secret under env: secrets-manager, pulling the value directly from AWS Secrets Manager at build time
C) Hardcoding the password directly into the build commands
D) Storing the password in the artifacts section

20. A CodeBuild project's service role needs the minimum permissions necessary to pull a specific parameter referenced under a buildspec's parameter-store section. Which IAM action should be granted, scoped to that specific parameter path?
A) ssm:GetParameters
B) secretsmanager:GetSecretValue
C) codecommit:GitPull
D) codedeploy:CreateDeployment

21. A team notices their CodeBuild project's build duration is dominated by re-downloading the same npm dependencies on every single build, even though the dependency versions rarely change between commits. Which CodeBuild feature most directly addresses this?
A) Increasing the compute type to the largest available size
B) Enabling caching (e.g., S3 or local caching) for the node_modules directory between builds
C) Switching the source provider from CodeCommit to S3
D) Disabling the install phase entirely

22. Which two of the following are valid CodeBuild caching approaches for speeding up dependency resolution across builds? (Select TWO)
A) Amazon S3 caching, where CodeBuild uploads and downloads cache contents to/from a specified S3 location between builds
B) Local caching, where cache contents persist on the build host itself when the same host happens to be reused
C) Caching directly inside the CodeCommit repository as committed binary files
D) A CodeDeploy deployment group cache
E) An API Gateway response cache applied to the build project

23. A CodeBuild project needs tooling and dependencies that none of AWS's managed build images provide out of the box. Which CodeBuild capability allows the build to run inside an environment tailored exactly to the team's needs?
A) A custom Docker image, hosted in Amazon ECR or another supported registry, used as the build environment
B) A larger managed compute type, which automatically includes any tooling
C) A CodeArtifact upstream repository
D) An AppConfig configuration profile

24. In a buildspec.yml, which section determines exactly which files CodeBuild packages into the output artifact, and from which base directory?
A) The phases section
B) The artifacts section, using files and base-directory
C) The env section
D) The cache section

25. A developer reviews a CodeBuild project's build logs and notices that a teammate had, for convenience during debugging, temporarily set a real production API key as a plaintext environment variable directly in the CodeBuild console. What is the primary security concern with this practice?
A) There is no concern, since CodeBuild environment variables are automatically encrypted and inaccessible to anyone
B) Plaintext environment variables configured this way may be visible to anyone with read access to the CodeBuild project configuration or build logs, unlike a secret referenced from Secrets Manager
C) CodeBuild automatically rejects any environment variable resembling an API key
D) This only matters if the project uses a custom Docker image

26. A CodeBuild project must run automated tests requiring both Python 3.11 and a specific version of a proprietary internal testing tool that is not available in any AWS-managed image nor easily installable via a script. What is the most direct way to satisfy this requirement?
A) Split the build into two entirely separate AWS accounts
B) Build and use a custom Docker image containing the required tool and runtime, and reference it as the CodeBuild project's build environment
C) Use only the install phase's runtime-versions setting, since it can install any arbitrary third-party tool
D) Switch to CodeDeploy instead of CodeBuild for this build step

27. Which of the following buildspec sections is used to reference values stored in Systems Manager Parameter Store so that they are available as environment variables during the build, without hardcoding them in the file?
A) artifacts
B) cache
C) env, under the parameter-store subsection
D) phases, under install

28. A company wants its CodeBuild service role scoped as narrowly as possible while still allowing a specific project to pull one named secret from Secrets Manager referenced in its buildspec. Which principle does this reflect, and what should the policy's Resource element be scoped to?
A) Least privilege — the policy should grant secretsmanager:GetSecretValue scoped to that specific secret's ARN, not a wildcard across all secrets
B) Maximum privilege — the role should be granted full SecretsManagerFullAccess for simplicity
C) The service role does not need any Secrets Manager permissions if the secret is referenced by name
D) The secret should instead be embedded directly in the buildspec.yml file committed to source control

29. A CodeBuild project's pre_build phase is used to run linting and unit tests, and the team wants the overall build to stop and be marked failed if any test fails, before the build phase even begins compiling. What causes a CodeBuild phase to be treated as failed?
A) Only the final phase's exit code is ever evaluated
B) Any phase whose commands return a non-zero exit code causes that phase (and by default the overall build) to be marked as failed
C) CodeBuild ignores exit codes entirely and always reports success
D) A failure can only occur in the build phase, never in pre_build

30. Which two of the following are true regarding CodeBuild build environments? (Select TWO)
A) AWS provides managed Docker images pre-configured with common runtimes such as Node.js, Python, and Java
B) A CodeBuild project can instead use a custom Docker image stored in a container registry such as Amazon ECR
C) CodeBuild requires every build to run on a dedicated, customer-managed EC2 instance provisioned and patched by the customer
D) CodeBuild build environments cannot specify a compute type or vCPU/memory class
E) Managed build images cannot be used for any compiled language, only interpreted ones

31. A CodeBuild project's artifacts section specifies `base-directory: 'dist'` and `discard-paths: no`. What does this configuration produce in the resulting build artifact?
A) The artifact will contain the full repository, ignoring the dist directory entirely
B) The artifact will contain the contents of the dist directory, preserving their internal folder structure rather than flattening it
C) The artifact will be empty, since discard-paths is set to no
D) The artifact will contain only a single randomly chosen file from dist

32. A team wants to give CodeBuild network access to a private RDS database inside a VPC during the build phase, for running integration tests against it. Which CodeBuild capability is needed to allow this?
A) Configuring the CodeBuild project with VPC connectivity — specifying the VPC, subnets, and security groups it should launch into
B) Enabling privileged mode
C) Increasing the artifacts retention period
D) Switching the source provider to CodeArtifact

33. Which of the following is the correct general purpose of the install phase in a buildspec.yml, distinct from pre_build?
A) install is used to install runtime versions and any global tools needed before dependency resolution and testing occur in later phases
B) install is where the final compiled output is always produced
C) install always uploads the finished artifact to S3
D) install is deprecated and no longer a valid buildspec phase

34. A company's CodeBuild project needs to reference a value from Secrets Manager where the secret is a JSON object containing multiple keys, and the buildspec should extract only the "password" key specifically. Which buildspec syntax accomplishes this?
A) secrets-manager: DB_PASSWORD: "myapp/prod/db-credentials:password", referencing the specific JSON key with a colon suffix
B) It is not possible to reference a single key within a JSON secret; the entire secret object must always be pulled as one variable
C) parameter-store: DB_PASSWORD: "myapp/prod/db-credentials:password"
D) artifacts: files: "myapp/prod/db-credentials:password"

35. Which two of the following statements correctly describe how CodeBuild handles environment variables sourced from Secrets Manager or Parameter Store versus plaintext variables? (Select TWO)
A) Secrets Manager and Parameter Store references are resolved at build start using the CodeBuild service role's permissions, keeping the actual secret value out of the project's stored configuration
B) Plaintext environment variables configured on the project are visible in the project configuration and are not treated as securely as a referenced secret
C) Referencing a secret from Secrets Manager requires disabling the buildspec entirely
D) Plaintext and Secrets Manager-sourced variables are cryptographically indistinguishable once the build starts, making the source irrelevant to security posture
E) CodeBuild requires all secrets to be stored as plaintext to be usable at all

36. A build takes an unusually long time because the team's Maven-based Java project re-downloads its entire dependency tree from Maven Central on every single CodeBuild run. Beyond enabling caching for the local Maven repository directory, which additional AWS service could further improve build reliability and speed by fronting Maven Central with a managed, cached proxy?
A) AWS CodeArtifact, configured with an upstream connection to Maven Central
B) AWS CodeStar
C) Amazon CloudFront, configured as a static website
D) AWS Systems Manager Parameter Store

### AWS CodeDeploy (37–58)

37. A company deploying to a fleet of on-premises servers via CodeDeploy needs a hook that runs after new application files have been placed on the server but before the application is started, specifically to adjust file permissions and update configuration files. Which lifecycle hook is appropriate?
A) BeforeInstall
B) AfterInstall
C) ApplicationStart
D) ValidateService

38. A CodeDeploy deployment group targeting Lambda uses a canary traffic-shifting configuration. The team wants to run an automated smoke test against the new function version before any real production traffic is routed to it at all. Which appspec.yml hook should this test be attached to?
A) BeforeInstall
B) AfterInstall
C) BeforeAllowTraffic
D) ApplicationStart

39. Which of the following correctly lists the standard CodeDeploy lifecycle event order for an in-place deployment to EC2/on-premises instances?
A) Install, ApplicationStop, DownloadBundle, BeforeInstall, AfterInstall, ValidateService, ApplicationStart
B) ApplicationStop, DownloadBundle, BeforeInstall, Install, AfterInstall, ApplicationStart, ValidateService
C) ValidateService, ApplicationStart, AfterInstall, Install, BeforeInstall, DownloadBundle, ApplicationStop
D) DownloadBundle, ApplicationStart, BeforeInstall, Install, AfterInstall, ApplicationStop, ValidateService

40. A company wants near-instant rollback capability if a newly deployed EC2 application version turns out to be faulty, and is willing to accept the additional cost of briefly running two full environments during each deployment. Which CodeDeploy deployment type best matches this priority?
A) In-place deployment with AllAtOnce
B) Blue/green deployment, keeping the original environment running until traffic has fully and successfully shifted
C) In-place deployment with OneAtATime
D) A deployment with no deployment group configured

41. A CodeDeploy deployment group for an EC2 fleet is configured with a CloudWatch alarm monitoring the application's 5xx error rate, and automatic rollback is enabled for alarm-triggered failures. During a deployment, the alarm enters ALARM state. What happens next?
A) CodeDeploy ignores the alarm and continues the deployment as planned
B) CodeDeploy automatically halts the deployment and rolls back by redeploying the last known-good revision
C) The alarm is logged but requires a human to manually trigger the rollback
D) The EC2 instances are immediately terminated with no redeployment

42. Which appspec.yml hook is used specifically to verify, as the final step of an EC2/on-premises in-place deployment, that the newly deployed application is functioning correctly — for example, by checking a health endpoint?
A) BeforeInstall
B) ApplicationStart
C) ValidateService
D) DownloadBundle

43. A CodeDeploy appspec.yml for a Lambda deployment specifies Resources and Hooks sections but no files or permissions sections. Why does the Lambda appspec.yml format omit these sections that appear in the EC2/on-premises format?
A) It is a mistake and the deployment will always fail without them
B) Lambda deployments have no filesystem to manage on a target server, so there are no files to copy or permissions to set — the appspec instead describes the function version/alias traffic shift
C) files and permissions are optional even for EC2 deployments and were never actually needed
D) Lambda appspec files must always be written in JSON instead of YAML

44. A deployment group targets an EC2 Auto Scaling group and uses an in-place deployment strategy configured as OneAtATime. What is the practical effect of this deployment configuration during rollout?
A) All instances in the ASG are updated simultaneously
B) Instances are updated one at a time, with each instance completing its deployment lifecycle before the next instance begins
C) Exactly half of the instances are updated, and the other half are left permanently on the old version
D) The ASG is deleted and recreated from scratch

45. Which of the following is true about the Hooks used in a CodeDeploy appspec.yml for an Amazon ECS deployment using blue/green traffic shifting?
A) ECS deployments use the same BeforeInstall/AfterInstall/ApplicationStart/ValidateService hooks as EC2 deployments, unchanged
B) ECS deployments use traffic-shifting hooks such as BeforeAllowTraffic and AfterAllowTraffic, similar in concept to Lambda, rather than the EC2-style install hooks
C) ECS deployments do not support any lifecycle hooks at all
D) ECS deployments require a completely separate service outside of CodeDeploy

46. A CodeDeploy deployment group's ValidateService hook script returns a non-zero exit code during an in-place EC2 deployment. Assuming the deployment group has automatic rollback on deployment failure enabled, what is the expected outcome?
A) The deployment is marked as failed, and automatic rollback redeploys the last known-good revision
B) The failing script is silently ignored and the deployment proceeds as successful
C) Only a warning is logged, with no impact on deployment status
D) The instance is left in an undefined intermediate state with no further action taken by CodeDeploy

47. Which of the following correctly distinguishes an in-place CodeDeploy deployment from a blue/green CodeDeploy deployment, for EC2/on-premises targets?
A) In-place deploys stop, update, and restart the application on the same existing instances; blue/green provisions a new, separate set of instances and shifts traffic to them once ready
B) In-place and blue/green are simply two names for the exact same deployment mechanism
C) Blue/green deployments are only available for Lambda, never for EC2
D) In-place deployments always provision new instances, identical to blue/green

48. A CodeDeploy deployment group's configuration determines which compute resources a deployment targets. For an EC2-based deployment group, which of the following can be used to identify the target instances?
A) EC2 instance tags, or membership in a specified Auto Scaling group
B) A CloudFront distribution ID
C) A Route 53 hosted zone ID
D) A CodeArtifact domain name

49. Which two of the following statements about CodeDeploy automatic rollback are accurate? (Select TWO)
A) A deployment group can be configured to automatically roll back when the deployment itself fails
B) A deployment group can be configured to automatically roll back when a specified CloudWatch alarm enters the ALARM state during or shortly after the deployment
C) Automatic rollback is only available for deployments targeting Lambda, never EC2
D) Automatic rollback requires manually re-running the entire CodePipeline pipeline from the source stage
E) CodeDeploy has no concept of rollback; failed deployments must always be fixed forward

50. A company deploying to EC2 wants the fastest possible rollback path if a newly deployed blue/green environment shows elevated errors shortly after the traffic shift completes, without needing to redeploy any code. What makes blue/green rollback typically faster than in-place rollback in this situation?
A) Blue/green rollback requires rebuilding the entire application from source
B) The original (blue) environment is generally kept running for a period after cutover, so rollback is simply re-routing traffic back to it rather than redeploying a previous revision
C) Blue/green deployments have no rollback capability at all
D) In-place deployments always roll back faster because there is only one environment involved

51. A CodeDeploy deployment group for a Lambda function is configured with the deployment configuration name CodeDeployDefault.LambdaLinear10PercentEvery1Minute. What traffic-shifting behavior does this configuration describe?
A) All traffic shifts to the new version immediately, with no gradual ramp
B) Traffic shifts to the new version in equal 10% increments every minute until 100% is reached
C) 10% of traffic shifts once, and the remaining 90% never shifts
D) Traffic shifts only after a full 24-hour bake period

52. Which of the following is the correct purpose of the AfterAllowTraffic hook in a Lambda or ECS CodeDeploy appspec.yml?
A) It runs before any traffic shifts to validate the new version is safe to receive traffic
B) It runs after all traffic has shifted to the new version, commonly used for post-deployment smoke tests or cleanup
C) It runs only if the deployment fails
D) It is exclusively used to install operating system patches

53. A team troubleshooting a failed EC2 in-place CodeDeploy deployment finds that the deployment failed during the AfterInstall lifecycle event. Which general category of task is most plausibly being performed at that stage, given its position in the lifecycle?
A) Downloading the initial revision bundle from the deployment's origin location
B) Configuring the application or changing file/directory permissions after files have been installed but before the application starts
C) Validating that the application is fully up and serving traffic correctly
D) Terminating the underlying EC2 instance permanently

54. Which two of the following are valid CodeDeploy compute platforms that a single deployment group is associated with? (Select TWO)
A) EC2/On-Premises
B) AWS Lambda
C) Amazon Route 53
D) Amazon CloudFront
E) AWS Certificate Manager

55. A company's CodeDeploy deployment group needs permission to describe and manage the EC2 instances, Auto Scaling groups, and ELB target groups it deploys to, on the company's behalf. What AWS mechanism grants CodeDeploy these permissions?
A) A CodeDeploy service role, an IAM role that CodeDeploy assumes, with a permissions policy scoped to the actions it needs
B) The root user's long-term access keys embedded in the appspec.yml
C) A CodeCommit approval rule template
D) An S3 bucket policy alone, with no IAM role involved

56. A scenario describes a deployment that "stops the application, deploys the new revision to the same fleet of instances, and restarts it, processing instances in batches." Which CodeDeploy deployment type and general behavior does this describe?
A) Blue/green deployment
B) In-place deployment, deploying to the existing instances in batches according to the configured deployment configuration
C) A Lambda canary deployment
D) A CodeArtifact package promotion

57. Which of the following is a valid reason a company might choose an in-place CodeDeploy deployment over blue/green for an EC2 fleet, despite in-place deployments generally having slower rollback?
A) In-place deployments are always faster to roll back than blue/green under every circumstance
B) The company wants to avoid the additional infrastructure cost of running a full duplicate environment, even temporarily, and can tolerate the slower rollback tradeoff
C) In-place deployments are the only option CodeDeploy supports for EC2
D) In-place deployments automatically include canary traffic shifting

58. Which two of the following statements accurately distinguish the EC2/on-premises appspec.yml hook set from the Lambda/ECS appspec.yml hook set? (Select TWO)
A) EC2/on-premises deployments use hooks such as BeforeInstall, AfterInstall, ApplicationStart, and ValidateService tied to installing files on a server
B) Lambda and ECS deployments use hooks such as BeforeAllowTraffic and AfterAllowTraffic tied to shifting traffic to a new version
C) Both compute platforms use the identical hook names with identical meanings
D) EC2/on-premises appspec files never support any hooks at all
E) Lambda appspec files require a files and permissions section identical to EC2

### Deployment Strategies in Depth (59–80)

59. A company deploying a new Lambda function version wants only 10% of invocations to use the new version initially, followed by a wait period to observe error rates via a CloudWatch alarm, and then an immediate shift of the remaining 90% if no problems are detected. Which deployment strategy does this describe?
A) Linear
B) Canary
C) Rolling
D) All-at-once with no traffic control

60. A company deploying an updated ECS service wants traffic to shift to the new task set in equal, evenly spaced increments on a fixed schedule (for example, 20% every 3 minutes) rather than a single small initial slice followed by a big jump. Which deployment strategy fits this description?
A) Canary
B) Linear
C) Blue/green with no traffic-shifting configuration
D) In-place, batch-by-batch

61. Comparing blue/green deployments to in-place (rolling) deployments for an EC2 fleet, which statement about rollback speed and mechanism is accurate?
A) Blue/green rollback is generally faster because the original environment is kept running and rollback is simply re-routing traffic back to it, while in-place rollback requires redeploying the previous revision to already-updated instances
B) In-place rollback is always faster because fewer instances are involved
C) Both strategies have identical rollback speed and mechanism in all cases
D) Neither strategy supports any form of rollback

62. A company wants to minimize the blast radius of a bad deployment as much as possible by exposing the smallest feasible slice of users to a new version before committing to a full rollout, accepting a somewhat slower time-to-full-rollout as the tradeoff. Which deployment strategy best matches this priority?
A) Rolling, with a large batch size
B) Canary, with a small initial percentage and an adequate bake time
C) Blue/green, with an immediate all-at-once cutover
D) All-at-once, with no staged exposure

63. Which of the following best describes the tradeoff a team accepts when choosing a rolling (in-place, batch-by-batch) deployment strategy for an EC2 fleet over a blue/green deployment?
A) Rolling deployments avoid the cost of running duplicate infrastructure but have slower, more complex rollback, and both old and new versions may run simultaneously mid-deployment
B) Rolling deployments always cost more than blue/green deployments
C) Rolling deployments never allow old and new versions to coexist during rollout
D) Rolling deployments provide faster rollback than blue/green in every case

64. A company's ECS service deployment uses a linear traffic-shifting configuration, and a CloudWatch alarm tied to the deployment enters ALARM state after 40% of traffic has already shifted to the new task set. What is the expected CodeDeploy behavior?
A) The deployment ignores the alarm and completes the shift to 100%
B) The deployment halts and, with automatic rollback configured, shifts traffic back to the original task set
C) The deployment pauses indefinitely with no rollback option available
D) The alarm has no effect unless 100% of traffic has already shifted

65. Which of the following scenarios is the strongest fit for a canary deployment strategy rather than a linear one, given otherwise similar requirements?
A) A team wants a slow, perfectly even ramp with no distinct "small initial slice" behavior
B) A team specifically wants to catch a bad deployment while affecting the smallest possible number of users first, before committing to the rest of the rollout in one larger step
C) A team has no CloudWatch alarms configured and does not want any automated safety mechanism
D) A team is deploying to EC2 instances with no ALB or target-group traffic-shifting capability at all

66. For EC2/on-premises deployments specifically, which statement correctly describes how canary and linear deployment concepts relate to CodeDeploy's EC2 deployment configurations?
A) EC2/on-premises in-place deployments support canary and linear traffic shifting identically to Lambda
B) EC2/on-premises in-place deployments use configurations like OneAtATime, HalfAtATime, and AllAtOnce (a rolling, batch-based model), rather than the canary/linear traffic-shifting configurations used for Lambda and ECS
C) EC2 deployments have no deployment configuration options whatsoever
D) EC2 deployments always default to a canary strategy with no way to change it

67. A company chooses a blue/green deployment for its EC2-based order-processing service specifically because it wants both a fully tested new environment before any customer traffic reaches it, and the fastest possible path back to the previous version if something goes wrong post-cutover. Which tradeoff does the company implicitly accept by choosing blue/green over in-place?
A) No tradeoff exists; blue/green has strictly no downsides compared to in-place
B) The temporary cost of running two full environments simultaneously during the cutover window
C) The loss of any ability to validate the new environment before traffic shifts
D) The requirement to use only Spot Instances for the new environment

68. Which of the following is the most accurate general statement about how canary and linear deployment strategies relate to blue/green deployments on platforms like Lambda and ECS?
A) Canary and linear are unrelated, entirely separate strategies with no connection to blue/green at all
B) Canary and linear describe the shape of the traffic ramp used to cut traffic over from the old version to the new version — they are ways blue/green-style cutovers are executed on these platforms, not a fourth unrelated category
C) Canary and linear can only be used for EC2, never for Lambda or ECS
D) Blue/green cannot be combined with any gradual traffic-shifting behavior under any circumstance

69. A retail company's finance team is concerned about the cost of running duplicate infrastructure during deployments and asks the engineering team to minimize infrastructure cost during rollouts, even if it means a slower rollback path if something goes wrong. Which EC2 deployment approach best aligns with this stated priority?
A) Blue/green with an extended wait period before terminating the original environment
B) In-place (rolling) deployment, accepting the tradeoff of slower rollback in exchange for not running duplicate infrastructure
C) Deploying to an entirely new AWS account for every release
D) Doubling the Auto Scaling group's maximum capacity permanently

70. Which two of the following correctly describe rolling (in-place, batch-based) deployments to an EC2 fleet? (Select TWO)
A) Instances are updated in batches, such as one at a time or half at a time, according to the configured deployment configuration
B) During the rollout, it is possible for some capacity to be running the old application version while other capacity runs the new version simultaneously
C) Rolling deployments always provision an entirely separate, duplicate fleet of instances
D) Rolling deployments guarantee zero possibility of a failed batch affecting subsequent batches
E) Rolling deployments are only available for Lambda functions, never EC2

71. A company deploying a Lambda-based API wants to validate the new version with a synthetic test transaction before any production traffic reaches it, and also wants a broader smoke test to run only once all traffic has fully shifted to the new version. Which two appspec.yml hooks correspond to these two respective needs? (Select TWO)
A) BeforeAllowTraffic, for validation before any traffic shifts
B) AfterAllowTraffic, for validation after all traffic has shifted
C) BeforeInstall, for validation before any traffic shifts
D) ApplicationStart, for validation after all traffic has shifted
E) ValidateService, for validation before any traffic shifts

72. Which of the following best explains why a scenario requiring "near-zero downtime and the ability to instantly revert to the exact previous state with no redeployment" almost always points toward blue/green rather than rolling deployment, for an EC2-based service?
A) Rolling deployments cannot run behind a load balancer under any circumstance
B) Blue/green keeps a complete, untouched copy of the previous environment running and simply re-routes traffic, avoiding any need to redeploy or reconstruct the previous state, unlike rolling's batch-by-batch in-place updates
C) Rolling deployments are always faster than blue/green in every measurable way
D) Blue/green deployments do not support automatic rollback

73. A mobile backend team deploying via ECS wants a deployment strategy that offers a middle ground: more caution than an all-at-once cutover, but a steadier, more predictable and observable ramp than a single small canary slice followed by a big jump. Which deployment strategy best matches this description?
A) Linear traffic shifting, moving in equal, evenly-paced increments across the deployment window
B) All-at-once cutover with no ramp
C) A purely manual, unscripted deployment process
D) In-place deployment with no ALB involved

74. Which of the following correctly identifies the primary axis of tradeoff between canary/linear traffic-shifting strategies and a rolling, in-place EC2 deployment strategy?
A) There is no meaningful tradeoff; all four strategies behave identically in every respect
B) Canary/linear operate on a duplicated or traffic-shiftable environment (via target groups, aliases, or task sets) allowing precise, reversible traffic control, while rolling directly updates the same fleet in place, trading that precision for lower infrastructure duplication cost
C) Rolling deployments always use canary traffic percentages internally
D) Canary and linear are exclusively used for database migrations, never for application deployment

75. A company observes that during a recent linear deployment to their ECS service, an alarm tripped at the 60% traffic-shift mark, and rollback correctly reverted all traffic to the original task set. Compared to if the same failure had occurred during a canary deployment configured with a 10% initial slice, what is the key difference in blast radius before the rollback triggered?
A) There would be no difference; both strategies always expose the same percentage of traffic before any alarm can trigger
B) The canary configuration would likely have exposed fewer users to the faulty version before the alarm could trip, since its initial exposure was capped at a small fixed percentage, whereas the linear deployment had already reached 60%
C) Canary deployments never use CloudWatch alarms, making this comparison invalid
D) Linear deployments cannot be rolled back once traffic shifting begins

76. Which of the following is the most accurate statement about deployment strategy applicability across CodeDeploy's supported compute platforms?
A) All four deployment strategy concepts — canary, linear, blue/green, and rolling — apply identically and interchangeably to EC2, Lambda, and ECS with no platform-specific distinctions
B) Canary and linear traffic-shifting configurations apply to Lambda and ECS; EC2/on-premises in-place deployments instead use rolling, batch-based configurations, while EC2 blue/green is its own separate deployment type
C) Rolling deployments are exclusively a Lambda concept
D) Blue/green deployments are exclusively an EC2 concept with no Lambda or ECS equivalent

77. A team is deciding between AllAtOnce and OneAtATime for an EC2 in-place deployment configuration. Which statement correctly characterizes the tradeoff?
A) AllAtOnce updates every instance simultaneously, finishing fastest but temporarily taking the entire fleet offline if the new version has issues; OneAtATime updates a single instance at a time, taking longer but preserving more healthy capacity if a failure is caught early
B) OneAtATime and AllAtOnce behave identically in every respect
C) AllAtOnce guarantees zero downtime under every circumstance
D) OneAtATime always deploys to exactly half the fleet, regardless of fleet size

78. Which two of the following statements correctly summarize how to choose between deployment strategies for a given scenario? (Select TWO)
A) When a requirement emphasizes minimizing the number of users exposed to a bad deployment before detection, favor canary over linear or all-at-once
B) When a requirement emphasizes the fastest, simplest possible rollback with no need to redeploy, favor blue/green over rolling/in-place
C) When cost minimization during deployment is the dominant stated constraint, blue/green is always the correct choice regardless of rollback speed
D) Rolling deployments are appropriate only for Lambda functions
E) Canary deployments are never appropriate for Lambda functions

79. A gaming company deploying a Lambda-based matchmaking service is especially concerned about a subtle bug that only manifests under real production load, and wants the smallest possible number of live matches affected if such a bug appears, even if that means the full rollout takes longer to complete. Which deployment configuration category best serves this priority?
A) AllAtOnce, shifting 100% of traffic immediately
B) A canary configuration with a small initial percentage and an adequately long bake time before the remainder shifts
C) A rolling EC2 deployment configuration, despite the workload running on Lambda
D) Disabling automatic rollback to speed up the deployment

80. Which of the following correctly explains why "some capacity runs the old version and some runs the new version simultaneously" is specifically called out as a characteristic to consider for rolling (in-place, batch-based) deployments?
A) It is irrelevant, since applications never need to tolerate running two versions at once
B) During a batch-based rollout, instances updated in earlier batches run the new version while instances not yet reached still run the old version, so the application and any shared state must tolerate both versions operating concurrently until the rollout completes
C) It only applies to blue/green deployments, never to rolling deployments
D) CodeDeploy automatically pauses all traffic until every batch is updated, avoiding this concern entirely

### AWS CodePipeline (81–98)

81. A company's release pipeline has a Source stage, a Build stage, and a Deploy stage, executed one after another. Within the Deploy stage, they want a unit-test action and a separate security-scan action to run at the same time rather than sequentially, to reduce total pipeline duration. How is this achieved in CodePipeline?
A) By placing both actions in the same stage and assigning them the same run order number, allowing them to execute in parallel
B) By creating two entirely separate pipelines and merging their results manually
C) CodePipeline stages can never contain more than one action
D) By disabling one of the two actions entirely

82. A company wants a human release manager to explicitly approve a deployment before it proceeds from a staging environment to production, and wants approvers automatically notified when their sign-off is needed. Which CodePipeline capability, combined with which notification service, satisfies this?
A) A Manual Approval action, typically configured to publish a notification to an SNS topic subscribed to by approvers
B) A CodeBuild post_build phase combined with Amazon SES
C) A CodeDeploy ValidateService hook combined with Amazon SNS
D) An AppConfig validator combined with Amazon Cognito

83. In CodePipeline, what mechanism actually carries the built application artifact produced by a CodeBuild action to the CodeDeploy action that consumes it in a later stage?
A) A direct, unmanaged network connection between the two AWS services
B) An S3 bucket that CodePipeline manages, where output artifacts from one action become the input artifacts for a subsequent action
C) An email attachment sent automatically between build and deploy stages
D) A CodeCommit branch created specifically to hold each build artifact

84. A company operating a single CodePipeline pipeline in one AWS account wants that pipeline to deploy an application into a completely separate AWS account used for production, without sharing long-term credentials between accounts. Which mechanism supports this cross-account deployment pattern?
A) A cross-account IAM role in the target account that the pipeline's role assumes via sts:AssumeRole, combined with a KMS key policy permitting that role to use the artifact bucket's encryption key
B) Copying the production account's root user credentials into the pipeline's build environment
C) Manually copying files between accounts using the console
D) Disabling IAM entirely in the production account for the duration of each deployment

85. Which of the following best describes how a modern CodePipeline pipeline is typically triggered when new code is pushed to its configured source repository branch?
A) CodePipeline continuously polls the repository every few seconds by default with no other option
B) An Amazon EventBridge rule reacts to the source repository's change event and starts the pipeline execution automatically, with legacy polling still available as an older alternative
C) A human must always manually click a button in the console to start every single pipeline execution
D) Pipelines can only be triggered on a fixed daily schedule, never on a commit

86. A company wants to temporarily prevent any new pipeline executions from reaching their production Deploy stage during an active incident, without deleting or reconfiguring the pipeline itself. Which CodePipeline capability supports this?
A) Manually disabling the stage transition into the production Deploy stage
B) Permanently deleting the CodeDeploy deployment group
C) Deleting the entire pipeline and recreating it after the incident
D) Revoking all IAM permissions account-wide

87. Which of the following correctly describes the relationship between stages and actions within a CodePipeline pipeline?
A) A pipeline consists of one or more sequential stages, and each stage contains one or more actions that operate on the pipeline's artifacts
B) A pipeline can only ever contain a single stage with a single action
C) Stages and actions are the same concept with two different names
D) Actions always run before the stage containing them is defined

88. A company's pipeline must deploy the same application into three separate AWS Regions to support regional failover. Which CodePipeline capability directly supports deploying across multiple Regions from a single pipeline?
A) Cross-region actions, where CodePipeline automatically replicates artifacts to a bucket in each target Region as configured
B) Manually re-running the pipeline three separate times, once per Region, with no built-in support otherwise
C) CodePipeline does not support any form of multi-Region deployment
D) Deploying to multiple Regions requires three fully independent, disconnected pipelines with no artifact sharing

89. Which two of the following are accurate statements about CodePipeline manual approval actions? (Select TWO)
A) A pipeline execution pauses at a manual approval action until a human explicitly approves or rejects it
B) Manual approval actions can be configured to publish a notification (commonly via SNS) alerting approvers that action is needed
C) Manual approval actions automatically approve themselves after exactly sixty seconds with no human involvement
D) Manual approval actions can only be placed as the very first action in a pipeline's very first stage
E) Manual approval actions require disabling all subsequent stages permanently

90. A pipeline's Test stage contains a unit-test action and an integration-test action, both currently configured with the same run order and therefore running in parallel. The team later needs the integration-test action to run only after the unit-test action completes successfully. What change accomplishes this?
A) Deleting the integration-test action entirely
B) Assigning the integration-test action a later (higher) run order number than the unit-test action, so it runs sequentially after the unit-test action within the same stage
C) Moving both actions into entirely separate, unrelated pipelines
D) Renaming the actions, since names alone determine execution order

91. Which of the following is the most accurate description of what happens to a pipeline execution if a required action within a stage fails (for example, a CodeBuild action returns a non-zero exit code)?
A) The pipeline automatically retries the failed action indefinitely without ever stopping
B) The pipeline execution stops at that point by default, and later stages do not proceed, until the issue is addressed and the pipeline is re-run or a new source change triggers a fresh execution
C) The pipeline silently skips the failed action and proceeds directly to production regardless
D) The entire pipeline definition is automatically deleted upon any action failure

92. A company wants its CodePipeline pipeline's Deploy stage to use CodeDeploy with a blue/green EC2 deployment configuration, including an automatic rollback tied to a CloudWatch alarm. Where is this alarm-based automatic rollback actually configured?
A) Directly on the CodePipeline stage definition, with no involvement from CodeDeploy
B) On the underlying CodeDeploy deployment group that the pipeline's Deploy action targets, since CodePipeline invokes CodeDeploy to perform the actual deployment and its rollback behavior
C) On the CodeCommit repository's trigger configuration
D) On the CodeArtifact domain's security configuration

93. Which of the following is an accurate statement about artifact handling between CodePipeline stages?
A) Every action in every stage must always produce an output artifact, with no exceptions
B) An action typically consumes one or more input artifacts (produced by an earlier action) and, when relevant to that action's purpose, produces an output artifact for later stages to consume
C) Artifacts are never versioned and each pipeline execution overwrites the same single artifact permanently
D) Artifacts can only be JSON files, never zip archives

94. A security-conscious company wants to ensure that only a specific, tightly-scoped IAM role can approve or reject the Manual Approval action for their production Deploy stage, rather than any authenticated user in the account. How is this access restricted?
A) Manual approval actions cannot be access-restricted; anyone in the account can always approve them
B) Through an IAM policy scoping the codepipeline:PutApprovalResult (and related) permissions to the specific pipeline/stage/action, granted only to the intended approvers' role
C) By deleting the IAM policies of everyone except the intended approver, account-wide
D) By moving the approval action into a completely different AWS account with no relationship to the pipeline

95. Which two of the following are legitimate source providers CodePipeline can be configured to use for its Source stage? (Select TWO)
A) AWS CodeCommit
B) A GitHub repository connected via a CodeStar Connection
C) An AWS Direct Connect circuit
D) An Amazon Route 53 hosted zone
E) An AWS Certificate Manager certificate

96. A pipeline's Build stage action fails intermittently due to a flaky integration test, and the team wants to understand exactly which build logs correspond to a specific failed pipeline execution for debugging. Where would a developer look to trace a specific CodeBuild action's logs from within a CodePipeline execution?
A) CodePipeline links each action's execution details to the underlying CodeBuild build, whose logs are available (commonly in CloudWatch Logs) for that specific build run
B) CodePipeline logs are only ever available by contacting AWS Support directly
C) Build logs are permanently deleted the moment a pipeline execution completes, with no way to review them afterward
D) Build logs can only be viewed by recreating the entire pipeline from scratch

97. Which of the following best explains why a company might configure a CodePipeline Deploy stage with two sequential CodeDeploy actions — one targeting a staging deployment group, followed by a manual approval action, followed by a second CodeDeploy action targeting a production deployment group — rather than a single action deploying directly to production?
A) CodePipeline requires at least three stages in every pipeline regardless of design intent
B) It allows automated validation in a lower-risk staging environment first, followed by a deliberate human checkpoint, before the higher-risk production deployment occurs
C) CodeDeploy cannot deploy to production under any circumstance without first deploying to staging
D) It is required purely for artifact storage reasons with no relation to risk management

98. A team wants their pipeline's Source stage to trigger only on pushes to the `main` branch of their CodeCommit repository, ignoring pushes to feature branches. Where is this branch scoping configured?
A) It cannot be configured; CodePipeline always triggers on every branch equally
B) In the Source action's configuration, which specifies the exact branch (e.g., main) the source stage should watch for changes on
C) In the CodeArtifact domain policy
D) In the AppConfig deployment strategy

### AWS CodeArtifact (99–108)

99. A company wants to host its internally developed private npm packages while also transparently caching packages pulled from the public npm registry, so that a public registry outage doesn't block their builds. Which AWS service and configuration pattern satisfies this?
A) AWS CodeArtifact, with a repository configured with an upstream connection to the public npmjs registry
B) AWS CodeCommit, storing npm packages as repository files
C) Amazon S3 with public read access enabled
D) AWS CodeStar, with no further configuration

100. In AWS CodeArtifact, what is the relationship between a domain and the repositories within it?
A) A domain is a single repository with a different name; there is no distinction
B) A domain is an organizational container that can hold multiple repositories, sharing security configuration and enabling package metadata deduplication across those repositories
C) A repository can belong to multiple domains simultaneously with no restriction
D) Domains are used only for billing and have no effect on repository organization

101. A CodeBuild buildspec needs to authenticate npm against a CodeArtifact repository before running `npm ci`. Which command is used as a convenience wrapper to fetch an authorization token and configure the local tool's config file accordingly?
A) aws codeartifact login --tool npm --domain <domain> --domain-owner <account-id> --repository <repo>
B) aws codecommit git-remote-codecommit
C) aws codedeploy create-deployment
D) aws codepipeline start-pipeline-execution

102. Which of the following package ecosystems does AWS CodeArtifact natively support as repository formats?
A) npm, pip, Maven, and NuGet, among others
B) Only Docker container images, with no support for language package managers
C) Only AWS Lambda deployment packages
D) Only CloudFormation templates

103. A company wants centralized control over which specific versions of open-source dependencies its engineering teams are allowed to pull into their builds, rather than allowing direct, ungoverned access to public package registries. How does fronting public registries with a CodeArtifact upstream repository support this goal?
A) It has no effect on version governance; CodeArtifact only mirrors whatever the public registry currently has
B) All build traffic flows through the CodeArtifact repository, giving the organization a single, IAM-governed control point where allowed package sources and caching behavior can be centrally managed
C) CodeArtifact requires disabling all public registry access entirely, with no caching capability
D) CodeArtifact only works for internally authored packages and cannot interact with any public registry

104. Which two of the following are accurate benefits of using AWS CodeArtifact as a caching proxy in front of a public package registry, compared to builds pulling directly from that public registry each time? (Select TWO)
A) Protection against a public registry outage or an accidentally deleted public package version breaking the build
B) Faster, more consistent dependency resolution since previously fetched packages are cached within the CodeArtifact repository
C) CodeArtifact eliminates the need for any IAM permissions related to package access
D) CodeArtifact automatically rewrites application source code to remove all third-party dependencies
E) CodeArtifact guarantees zero cost for all package downloads regardless of usage

105. A developer's CodeBuild service role lacks the codeartifact:GetAuthorizationToken permission needed to authenticate against a CodeArtifact repository during the build's install phase. What is the most likely observed result?
A) The build succeeds normally, since CodeArtifact does not require any authentication
B) The authentication step fails, causing the dependency-resolution commands relying on it (such as npm ci) to fail as well
C) CodeArtifact automatically grants temporary anonymous access in this situation
D) The build silently substitutes a different, unrelated repository

106. Which of the following best describes what happens the first time a specific package version is requested from a CodeArtifact repository configured with an upstream connection to a public registry, if that version has not been requested before?
A) The request always fails permanently, since CodeArtifact never fetches anything from a public upstream
B) CodeArtifact fetches the package version from the configured upstream registry and caches it in the repository for that and future requests
C) The package must first be manually uploaded by an administrator before any request can succeed
D) CodeArtifact deletes the upstream configuration automatically after the first request

107. A company operates repositories for npm, pip, and Maven packages, all within a single CodeArtifact domain, and wants consistent security and access policy management applied across all three without configuring each repository's security independently from scratch. Which CodeArtifact concept enables this kind of shared configuration?
A) The domain-level security configuration and policy sharing that CodeArtifact provides across repositories within the same domain
B) A separate CodeStar project must be created for each repository individually
C) CodeArtifact does not support any shared configuration; every repository must be configured in complete isolation
D) AppConfig deployment strategies applied to each repository

108. Which two of the following statements about AWS CodeArtifact authentication are accurate? (Select TWO)
A) Clients authenticate using a short-lived authorization token obtained via the CodeArtifact API (e.g., get-authorization-token)
B) Access to CodeArtifact repositories and domains is governed by IAM, consistent with the rest of AWS
C) CodeArtifact requires a permanent, non-expiring API key generated outside of IAM
D) CodeArtifact authentication tokens never expire and require no refresh
E) CodeArtifact is exempt from IAM policy evaluation entirely

### AWS CodeStar (109–113)

109. Which of the following most accurately describes the historical role of AWS CodeStar?
A) A distinct deployment engine that fully replaces CodeBuild and CodeDeploy
B) A unified project-management dashboard and template that provisioned and wrapped CodeCommit, CodeBuild, CodeDeploy, and CodePipeline together from a project template
C) A container orchestration service comparable to ECS
D) A managed relational database service

110. A company evaluating whether to use AWS CodeStar for a brand-new project in current AWS guidance should be aware of which of the following?
A) CodeStar is AWS's actively promoted, primary recommendation for all new CI/CD projects going forward
B) CodeStar is largely superseded in newer AWS guidance, which instead favors composing CodeCommit, CodeBuild, CodeDeploy, and CodePipeline directly (or using tools like the CDK/SAM/Amplify for scaffolding)
C) CodeStar has been fully removed from the AWS platform and no longer exists in any form
D) CodeStar replaced IAM as the primary access-control mechanism for CI/CD services

111. If a DVA-C02 exam question presents AWS CodeStar as an answer option alongside directly-composed CodeCommit/CodeBuild/CodeDeploy/CodePipeline resources, how should a candidate generally interpret CodeStar's role?
A) As a fundamentally different deployment technology with entirely separate underlying mechanics
B) As essentially the same underlying Code* services, just provisioned together and presented through a project-scaffolding dashboard, rather than a distinct deployment engine
C) As a service unrelated to any of the other AWS developer tools
D) As a replacement for IAM policies entirely

112. Which two of the following capabilities were part of AWS CodeStar's original unified project experience? (Select TWO)
A) Provisioning a CodeCommit repository, CodeBuild project, CodeDeploy deployment, and CodePipeline pipeline together from a project template
B) A basic project dashboard providing visibility into the provisioned resources
C) Full replacement of Amazon RDS for all relational database needs
D) Native container orchestration equivalent to Amazon EKS
E) Acting as a DNS resolution service equivalent to Route 53

113. A team already has a fully custom-built pipeline composed of separately configured CodeCommit, CodeBuild, CodeDeploy, and CodePipeline resources, each tuned to specific project needs. Would introducing AWS CodeStar into this existing, already-composed setup provide meaningful additional deployment capability beyond what already exists?
A) Yes, CodeStar would add entirely new deployment mechanics not otherwise available
B) Not meaningfully — CodeStar's primary value is as a scaffolding/dashboard wrapper around the same underlying services already in use, not as a source of new deployment capability
C) Yes, because CodeStar is required for any pipeline to function at all
D) No, because CodeStar cannot coexist with any manually configured Code* resource

### AWS AppConfig (114–128)

114. A company wants to roll out a new feature flag value to its already-running application fleet gradually, with the ability to automatically halt and revert if error rates spike, but explicitly without triggering a new code deployment or restarting any running processes. Which AWS service is purpose-built for this requirement?
A) AWS CodeDeploy, using a blue/green deployment
B) AWS AppConfig, using a deployment strategy with a bake time and an alarm-based automatic rollback
C) AWS CodePipeline, using a manual approval action
D) AWS CodeArtifact, using an upstream repository

115. In AWS AppConfig, what is the primary purpose of a validator attached to a configuration profile?
A) To automatically deploy the configuration to 100% of the fleet immediately, bypassing any staged rollout
B) To check a new configuration value's correctness (for example, via a JSON Schema or a Lambda function) before it is allowed to deploy, catching malformed configuration before it reaches production
C) To encrypt the configuration value using a hardcoded key
D) To permanently delete any configuration profile that fails a health check

116. A Lambda function needs to check a feature flag stored in AppConfig on every single invocation, and the team is concerned that calling the AppConfig API directly on each invocation would add unacceptable latency and cost. Which AWS-provided mechanism addresses this concern?
A) The AppConfig Lambda extension, a Lambda layer that caches configuration locally and serves it over localhost with minimal added latency
B) Increasing the Lambda function's memory allocation, which has no relation to this concern
C) Switching the feature flag storage to a CodeCommit repository read on every invocation
D) Disabling the feature flag check entirely to avoid the API call

117. Which of the following deployment strategies, in the context of AWS AppConfig configuration rollouts, most closely mirrors the "small percentage, then a jump to full rollout" traffic-shifting shape used for code deployments?
A) AppConfig.AllAtOnce
B) A canary-equivalent AppConfig deployment strategy with a defined initial percentage and bake time before completing the rollout
C) A deployment strategy is not a concept that exists in AppConfig
D) Only a fully manual, non-automatable process is available in AppConfig

118. A company deploys a new AppConfig configuration using the predefined strategy AppConfig.Linear50PercentEvery30Seconds. What does this deployment strategy name indicate about the rollout's pace?
A) The configuration reaches 100% of the fleet instantly with no incremental steps
B) The configuration is applied to 50% of the fleet, then the remaining 50% every 30 seconds thereafter, in a linear, evenly-paced progression
C) The configuration is deployed only once every 50 days
D) The configuration is never actually deployed, only previewed

119. Which of the following most accurately distinguishes AWS AppConfig from AWS Systems Manager Parameter Store, for the specific use case of safely rolling out a configuration change to a live application fleet?
A) They are functionally identical with no meaningful differences for this use case
B) AppConfig provides native staged/gradual rollout with bake time and CloudWatch alarm-based automatic rollback for configuration changes, a safety model Parameter Store does not natively provide
C) Parameter Store natively provides staged rollout and alarm-based rollback, while AppConfig does not
D) Neither service can be used for configuration management of any kind

120. An AppConfig deployment is underway using a linear strategy, and a CloudWatch alarm tied to the deployment's environment enters ALARM state partway through the rollout. Assuming automatic rollback is configured, what is the expected behavior?
A) AppConfig ignores the alarm and completes the rollout to 100% of the fleet
B) AppConfig halts the deployment and automatically reverts fetching clients to the prior known-good configuration value
C) AppConfig requires a human to manually intervene before any rollback can occur, even with automatic rollback configured
D) The alarm has no defined relationship to AppConfig deployments under any configuration

121. Which of the following is the correct relationship between an AppConfig "application," "environment," and "configuration profile"?
A) An application is a logical namespace that can contain multiple environments (such as beta and prod) and multiple configuration profiles (pointers to specific configuration data, such as a feature-flag document)
B) An environment is always a physical AWS Region, with no other meaning
C) A configuration profile is only usable by a single environment ever, across all AppConfig accounts globally
D) Applications, environments, and configuration profiles are interchangeable terms for the same object

122. A retail company wants to reject any configuration update that sets a numeric "maxCartItems" value below zero, before that update is ever allowed to reach production. Which AppConfig feature is designed to enforce this kind of business-rule validation prior to deployment?
A) An AppConfig deployment strategy
B) An AppConfig validator, implemented as a JSON Schema constraint or a custom Lambda function
C) A CodeDeploy ValidateService hook
D) A CodeBuild pre_build phase

123. Which two of the following are accurate characteristics of AWS AppConfig? (Select TWO)
A) Configuration changes deployed through AppConfig do not require redeploying application code or restarting the running process
B) AppConfig deployments can use a bake time after reaching full rollout, during which monitored alarms can still trigger an automatic rollback
C) AppConfig can only be used with Amazon EC2 instances and has no Lambda-specific integration
D) AppConfig configuration profiles cannot have any validation applied to them
E) AppConfig requires every configuration change to go through a full CodePipeline execution

124. A development team is deciding whether a particular change belongs in a CodeDeploy-orchestrated release or an AppConfig-orchestrated configuration rollout. The change in question flips an already-deployed, dormant `if` branch in the running application code from disabled to enabled. Which service is the better fit for making this specific change?
A) AWS CodeDeploy, since any behavioral change must always go through a full code deployment
B) AWS AppConfig, since the code implementing the new behavior is already deployed and only the runtime flag controlling it needs to change
C) AWS CodeArtifact, since this is fundamentally a dependency-management concern
D) AWS CodeStar, since it is required for any behavioral change

125. Which of the following best describes the purpose of AppConfig's "bake time" concept within a deployment strategy?
A) It defines how long the build phase of a CodeBuild project is allowed to run
B) It defines an observation window, after a rollout step (or after reaching full deployment), during which the deployment is still monitored and can still be automatically rolled back if a tied alarm trips
C) It is the amount of time before a configuration profile is permanently deleted
D) It refers to the time CodeArtifact takes to cache a new package version

126. A company is deciding between a plain Parameter Store SecureString parameter and an AppConfig configuration profile for storing a value that controls a gradual, monitored feature rollout across a fleet of application instances, with automatic rollback if error rates spike during the rollout. Which choice correctly matches the stated requirement?
A) Parameter Store, because SecureString values are inherently safer for any use case
B) AppConfig, because it natively supports staged/gradual deployment strategies and alarm-based automatic rollback for exactly this kind of monitored rollout, which Parameter Store does not natively provide
C) Either choice is functionally identical for this specific requirement
D) Neither service supports any form of configuration rollout

127. Which two of the following are valid formats or sources AppConfig configuration profile data can take? (Select TWO)
A) A free-form configuration document, such as JSON or YAML, authored and stored as the configuration data
B) A feature-flag-specific configuration profile representing on/off (or more complex) flag data
C) A live, unmodifiable snapshot of the entire AWS account's billing history
D) A direct binary copy of an EC2 AMI
E) A CodeCommit approval rule template

128. A company's Lambda function begins consistently returning malformed responses shortly after an AppConfig configuration deployment reaches 100% of the fleet, but the associated CloudWatch alarm was scoped only to a metric that doesn't reflect this particular failure mode, so it never entered ALARM state. What does this scenario illustrate about AppConfig's automatic rollback safety net?
A) AppConfig will always detect and roll back any bad configuration regardless of alarm scope
B) The automatic rollback safety net is only as effective as the CloudWatch alarms actually configured and tied to the deployment — a failure mode not covered by any tied alarm will not trigger an automatic rollback
C) AppConfig deployments cannot fail in any way once they reach 100%
D) This scenario is impossible because AppConfig does not use CloudWatch alarms

### Integrative Scenarios (129–135)

129. A company's release process is: a developer pushes to CodeCommit, which triggers CodePipeline; CodePipeline runs a CodeBuild project that lints, tests, and packages the application using a buildspec.yml that references a database password from Secrets Manager; the built artifact is deployed to a staging deployment group via CodeDeploy; a manual approval action (notifying approvers via SNS) gates the next stage; and finally the artifact is deployed to production via CodeDeploy using a blue/green strategy with alarm-based automatic rollback. Which AWS service is responsible for orchestrating the overall sequence of these stages?
A) AWS CodeBuild
B) AWS CodePipeline
C) AWS CodeArtifact
D) AWS AppConfig

130. In the pipeline described in the previous scenario, which service is directly responsible for pulling the database password referenced in the buildspec.yml at build time, and which service is directly responsible for executing the blue/green traffic shift with alarm-based rollback in production?
A) CodeArtifact pulls the secret; CodePipeline executes the traffic shift
B) CodeBuild resolves the Secrets Manager reference at build time; CodeDeploy executes the blue/green deployment and its alarm-based rollback
C) CodeCommit resolves the secret; CodeArtifact executes the traffic shift
D) AppConfig resolves the secret; CodeStar executes the traffic shift

131. A company wants to add a step to its existing pipeline so that, before every build, dependencies are resolved from a centrally governed, IAM-authenticated package repository that also caches packages from the public npm registry to protect against upstream outages. Which AWS service should be integrated into the CodeBuild install phase to satisfy this?
A) AWS CodeArtifact, authenticated via aws codeartifact login within the buildspec's install phase
B) AWS CodeStar, with no further buildspec changes
C) AWS AppConfig, referenced as a buildspec artifacts setting
D) Amazon Route 53, configured as a private hosted zone

132. A company running a Lambda-based checkout service wants two independent safety mechanisms active during any change: one that gradually shifts traffic to a new Lambda function version with an automatic rollback if error-rate alarms trip, and a separate one that allows a feature flag inside that same code to be toggled and gradually rolled out to a percentage of users with its own independent alarm-based rollback, without needing a new Lambda deployment for the flag change. Which two AWS services respectively provide these two mechanisms? (Select TWO)
A) AWS CodeDeploy, for the gradual Lambda version traffic shift with rollback
B) AWS AppConfig, for the gradual feature-flag rollout with rollback, independent of a code deployment
C) AWS CodeArtifact, for the gradual Lambda version traffic shift with rollback
D) AWS CodeCommit, for the gradual feature-flag rollout with rollback
E) AWS CodeStar, for both mechanisms simultaneously

133. A security review of a company's CI/CD setup finds: a CodeBuild project with a production database password stored as a plaintext environment variable in the console, a CodePipeline production Deploy stage with no manual approval action before it, a CodeDeploy deployment group with no CloudWatch alarm or automatic rollback configured, and engineers using long-lived IAM user access keys copy-pasted into local `.npmrc` files to reach a private package feed. Which combination of changes most directly addresses all four findings?
A) Reference the password from Secrets Manager in the buildspec instead of a plaintext variable, add a manual approval action before the production Deploy stage, configure a CloudWatch alarm with automatic rollback on the deployment group, and move the private package feed to CodeArtifact authenticated via short-lived tokens instead of long-lived keys
B) Delete the CodePipeline pipeline entirely and perform all deployments manually going forward
C) Only fix the plaintext password; the other three findings are acceptable operational tradeoffs
D) Rotate the IAM access keys more frequently, but leave the other three findings unaddressed

134. A company wants to design a release process for a Lambda-based service where: code changes go through full build/test/deploy automation with a canary traffic shift and alarm-based rollback, while separate, lower-risk configuration tweaks (such as adjusting a rate limit or toggling a flag) can be rolled out by a different team, on a different cadence, without waiting for or triggering the full CI/CD pipeline. Which architecture correctly separates these two concerns?
A) Route both code changes and configuration tweaks through the same CodePipeline pipeline and CodeDeploy deployment, since AWS provides no way to separate them
B) Use CodePipeline/CodeBuild/CodeDeploy with a Lambda canary configuration for code changes, and use AppConfig (with its own deployment strategy and alarm) for the independent configuration/flag changes, decoupling the two release cadences entirely
C) Use CodeArtifact for both code changes and configuration tweaks
D) Use CodeStar exclusively, since it removes the need for any other service

135. Reflecting on this module as a whole, which single statement best captures the unifying theme across CodeCommit, CodeBuild, CodeDeploy, CodePipeline, CodeArtifact, and AppConfig as tested on the DVA-C02 exam?
A) Each service is tested in total isolation, with no scenario ever requiring understanding of how they work together
B) These services form a composable toolchain — source control, build, deploy, orchestration, dependency management, and configuration rollout — where the exam consistently tests recognizing which specific service (and which specific mechanism within it, such as a buildspec phase, an appspec hook, or a deployment strategy) correctly matches a given requirement, especially around safe, gradual, and reversible delivery of both code and configuration
C) Only CodePipeline matters for the exam; the other services are never independently tested
D) None of these services are relevant to the DVA-C02 exam, which focuses exclusively on application code

---

## Answer Key & Explanations

1. B — CodeCommit provides managed private Git hosting with access governed entirely by IAM policies.
2. B — IAM-generated HTTPS Git credentials are a dedicated username/password pair for Git operations, distinct from console or API credentials.
3. A — git-remote-codecommit lets a caller authenticate with their existing IAM credentials/role directly, no separate Git credential needed.
4. B — An EventBridge rule reacting to the repository's push event starts the pipeline automatically without polling.
5. B — Approval rule templates enforce a minimum number of approvers on pull requests before merge.
6. A — SSH keys uploaded to an IAM user and IAM-generated HTTPS Git credentials are CodeCommit's supported authentication methods.
7. B — CodeCommit offers managed, low-overhead private Git hosting fully governed by IAM and logged via CloudTrail.
8. B — Since CodeCommit has no separate user directory, access is fully controlled and revoked through IAM.
9. A — CodeCommit triggers can invoke SNS notifications or Lambda functions on events like branch creation.
10. A & C — Access is governed by IAM actions like codecommit:GitPull/GitPush, and a source stage can trigger automatically on a branch commit.
11. B — CodePipeline supports GitHub as a source provider via a CodeStar Connection, no CodeCommit migration required.
12. A & B — SNS notifications via triggers and EventBridge rules matching repository events are both legitimate ways to surface events.
13. B — An exposed credential must be treated as compromised and rotated immediately, regardless of any history cleanup.
14. A — CodePipeline source triggers can be scoped to specific branches or branch name filters, not just "every branch."
15. B — The standard order is install, pre_build, build, post_build, matching the described install/test/build/upload sequence.
16. B — post_build commands still execute after a build-phase failure, though the overall build remains marked failed.
17. B — runtime-versions is configured within the install phase to pin a managed image's runtime version.
18. A — Privileged mode must be enabled for a CodeBuild project to run Docker itself inside the build container.
19. B — Referencing the value under env: secrets-manager pulls it directly from Secrets Manager at build time, avoiding console/plaintext exposure.
20. A — ssm:GetParameters is the action needed to retrieve values referenced under a buildspec's parameter-store section.
21. B — Enabling caching for the dependency directory avoids re-downloading unchanged dependencies on every build.
22. A & B — S3 caching and local (host-persisted) caching are both valid CodeBuild caching approaches.
23. A — A custom Docker image, hosted in a registry like ECR, lets the build run with exactly the tooling required.
24. B — The artifacts section, via files and base-directory, determines what gets packaged into the output artifact.
25. B — Plaintext console environment variables are visible to anyone with read access to the project, unlike a Secrets Manager reference.
26. B — A custom Docker image can bundle a specific runtime plus a proprietary tool unavailable in managed images or via simple install scripts.
27. C — The env section's parameter-store subsection maps buildspec variables to Parameter Store values.
28. A — Least privilege means scoping secretsmanager:GetSecretValue to the specific secret ARN needed, not a wildcard.
29. B — Any phase's commands returning a non-zero exit code marks that phase, and by default the build, as failed.
30. A & B — AWS provides managed images with common runtimes, and projects can alternatively use a custom image from a registry like ECR.
31. B — With discard-paths set to no, the artifact preserves the internal folder structure of the dist directory's contents.
32. A — VPC connectivity configuration lets the CodeBuild project reach private VPC resources like an RDS database during the build.
33. A — The install phase is for installing runtime versions and global tools needed before later dependency resolution and testing.
34. A — The secrets-manager section supports a colon-suffixed JSON key reference to extract a single field from a JSON secret.
35. A & B — Secret references are resolved at build start via the service role, keeping the value out of stored config; plaintext variables are visible in the project configuration.
36. A — CodeArtifact configured with an upstream to Maven Central provides a managed, cached, more resilient proxy for Maven dependencies.
37. B — AfterInstall is used to configure the application and adjust permissions after files are placed but before the app starts.
38. C — BeforeAllowTraffic runs before any traffic shifts, making it the right place for pre-traffic validation.
39. B — The standard in-place order is ApplicationStop, DownloadBundle, BeforeInstall, Install, AfterInstall, ApplicationStart, ValidateService.
40. B — Blue/green keeps the original environment running, enabling near-instant rollback by re-routing traffic.
41. B — With alarm-based automatic rollback enabled, an ALARM state halts the deployment and redeploys the last known-good revision.
42. C — ValidateService is the final hook, used to confirm the deployed application is functioning correctly.
43. B — Lambda deployments have no server filesystem to manage, so appspec.yml instead describes the function version/alias traffic shift via Resources and Hooks.
44. B — OneAtATime updates a single instance at a time, each completing its lifecycle before the next begins.
45. B — ECS deployments use traffic-shifting hooks like BeforeAllowTraffic/AfterAllowTraffic, conceptually similar to Lambda, not the EC2-style install hooks.
46. A — A non-zero ValidateService exit code marks the deployment failed, and automatic rollback (if enabled) redeploys the last known-good revision.
47. A — In-place updates the existing instances directly; blue/green provisions a separate new set and shifts traffic once ready.
48. A — EC2 deployment groups can target instances by tag or by Auto Scaling group membership.
49. A & B — Rollback can be triggered by deployment failure itself or by a tied CloudWatch alarm entering ALARM state.
50. B — The blue environment is kept running, so rollback is simply re-routing traffic back rather than redeploying a previous revision.
51. B — LambdaLinear10PercentEvery1Minute shifts traffic in equal 10% increments every minute until reaching 100%.
52. B — AfterAllowTraffic runs once all traffic has shifted, commonly used for post-deployment smoke tests or cleanup.
53. B — AfterInstall's position (after Install, before ApplicationStart) fits configuring the app or setting permissions post-file-placement.
54. A & B — EC2/On-Premises and AWS Lambda (along with ECS) are valid CodeDeploy compute platforms; Route 53, CloudFront, and ACM are not.
55. A — A CodeDeploy service role, assumed by CodeDeploy, grants it the permissions needed to manage the target compute resources.
56. B — This describes an in-place deployment updating the existing fleet in batches per the deployment configuration.
57. B — Avoiding duplicate infrastructure cost, while accepting slower rollback, is a valid reason to choose in-place over blue/green.
58. A & B — EC2/on-premises uses install-oriented hooks; Lambda/ECS use traffic-shifting hooks like BeforeAllowTraffic/AfterAllowTraffic.
59. B — A small initial percentage, a bake time, then an all-at-once shift of the remainder describes a canary deployment.
60. B — Equal, evenly-paced increments on a fixed schedule describes a linear deployment.
61. A — Blue/green rollback re-routes to the still-running original environment; in-place rollback requires redeploying the previous revision.
62. B — Canary, with a small initial slice and adequate bake time, minimizes blast radius before a wider commitment.
63. A — Rolling avoids duplicate infrastructure cost but has slower rollback and possible mixed-version coexistence mid-rollout.
64. B — With automatic rollback configured, an alarm trip during the shift halts the deployment and reverts traffic to the original version.
65. B — Canary's defining strength is minimizing initial exposure before a larger commitment, unlike linear's steadier full-window ramp.
66. B — EC2/on-premises in-place deployments use rolling, batch-based configurations (OneAtATime/HalfAtATime/AllAtOnce), not canary/linear traffic shifting.
67. B — Running two full environments simultaneously during cutover is the cost tradeoff blue/green accepts for its validation and rollback benefits.
68. B — Canary and linear describe the traffic-ramp shape used to execute a blue/green-style cutover on platforms like Lambda and ECS.
69. B — In-place deployment avoids duplicate infrastructure cost, directly matching a cost-minimization priority despite slower rollback.
70. A & B — Batch-based updates (e.g., one/half at a time) can leave old and new versions running concurrently mid-rollout.
71. A & B — BeforeAllowTraffic supports pre-traffic validation; AfterAllowTraffic supports validation after the full shift completes.
72. B — Blue/green keeps an untouched previous environment ready, so rollback is a traffic re-route rather than a reconstruction.
73. A — Linear's evenly-paced, predictable increments are the described middle ground between all-at-once and a small canary slice.
74. B — Canary/linear rely on a traffic-shiftable duplicated environment for reversible control; rolling updates the same fleet in place at lower duplication cost.
75. B — Canary's capped small initial exposure likely limits blast radius more than a linear rollout that had already reached 60%.
76. B — Canary/linear apply to Lambda and ECS; EC2/on-premises in-place deployments use rolling configurations, and EC2 blue/green is its own type.
77. A — AllAtOnce is fastest but riskiest fleet-wide; OneAtATime is slower but preserves more healthy capacity if a failure is caught early.
78. A & B — Canary minimizes exposure before detection; blue/green offers the fastest, simplest rollback without redeployment.
79. B — A canary configuration with a small initial percentage and adequate bake time minimizes live matches affected by a subtle production-only bug.
80. B — Batch-based rollouts mean earlier-updated batches run the new version while later batches still run the old version concurrently.
81. A — Actions in the same stage sharing the same run order number execute in parallel.
82. A — A Manual Approval action, typically notifying approvers via an SNS topic, provides the human sign-off gate.
83. B — CodePipeline manages an S3 bucket where an action's output artifact becomes a later action's input artifact.
84. A — A cross-account IAM role assumed via sts:AssumeRole, plus a KMS key policy permitting its use, enables cross-account deployment without shared long-term credentials.
85. B — An EventBridge rule reacting to the source change event triggers the pipeline automatically; polling remains a legacy alternative.
86. A — Manually disabling a stage transition blocks further executions from reaching that stage without altering the pipeline definition.
87. A — A pipeline consists of sequential stages, each containing one or more actions operating on pipeline artifacts.
88. A — Cross-region actions let CodePipeline automatically replicate artifacts to buckets in each configured target Region.
89. A & B — Execution pauses until a human decision, and approval actions commonly publish an SNS notification to alert approvers.
90. B — Assigning a later run order number makes the integration-test action run after the unit-test action instead of in parallel.
91. B — By default, a failed required action stops the pipeline execution at that point; later stages do not proceed until re-run.
92. B — The CloudWatch alarm and automatic rollback are configured on the CodeDeploy deployment group that CodePipeline's Deploy action targets.
93. B — Actions typically consume input artifacts and, when relevant, produce output artifacts for subsequent stages.
94. B — IAM policy scoping of codepipeline:PutApprovalResult (and related actions) to the intended approvers' role restricts who can approve.
95. A & B — CodeCommit and a GitHub repository connected via CodeStar Connection are both valid CodePipeline source providers.
96. A — CodePipeline links each action to its underlying CodeBuild build, whose logs (commonly in CloudWatch Logs) are traceable for that run.
97. B — Staging validation followed by a human checkpoint before production reduces risk compared to deploying directly to production.
98. B — The Source action's configuration specifies the exact branch the source stage watches for changes.
99. A — A CodeArtifact repository with an upstream to npmjs provides both private hosting and resilient caching of public packages.
100. B — A domain is an organizational container holding multiple repositories, sharing security configuration and enabling metadata deduplication.
101. A — aws codeartifact login fetches an authorization token and configures the tool's config file to point at the repository.
102. A — CodeArtifact natively supports npm, pip, Maven, and NuGet repository formats, among others.
103. B — Routing all build traffic through CodeArtifact gives a single, IAM-governed control point for managing allowed package sources.
104. A & B — Caching protects against upstream outages/deletions and speeds up dependency resolution via previously cached packages.
105. B — Without the required permission, the authentication step fails, causing dependent commands like npm ci to fail as well.
106. B — CodeArtifact fetches the not-yet-cached version from the upstream registry and caches it for that and future requests.
107. A — Domain-level security configuration sharing lets consistent policy apply across multiple repositories within the same domain.
108. A & B — Authentication uses a short-lived token from the CodeArtifact API, and access is governed by IAM like other AWS services.
109. B — CodeStar was a unified project-management dashboard/template wrapping CodeCommit, CodeBuild, CodeDeploy, and CodePipeline together.
110. B — Newer AWS guidance favors composing the underlying services directly (or using CDK/SAM/Amplify), with CodeStar largely superseded.
111. B — CodeStar represents the same underlying services provisioned together via a scaffolding dashboard, not a distinct deployment engine.
112. A & B — CodeStar provisioned the four core Code* resources together from a template and offered a basic project dashboard.
113. B — CodeStar's value is primarily as a scaffolding/dashboard wrapper, not a source of new deployment capability beyond the underlying services.
114. B — AppConfig's deployment strategies with bake time and alarm-based rollback are purpose-built for gradual configuration rollout without a code deployment.
115. B — A validator checks a new configuration value's correctness before deployment, catching malformed configuration early.
116. A — The AppConfig Lambda extension caches configuration locally and serves it over localhost with minimal added latency.
117. B — A canary-equivalent AppConfig strategy (initial percentage plus bake time before completion) mirrors the code-deployment canary shape.
118. B — Linear50PercentEvery30Seconds applies configuration to 50% of the fleet, then the remainder in evenly-paced 30-second increments.
119. B — AppConfig natively provides staged rollout and alarm-based automatic rollback for configuration changes; Parameter Store does not.
120. B — With automatic rollback configured, an alarm trip halts the deployment and reverts clients to the prior known-good configuration.
121. A — An application is a namespace containing multiple environments and multiple configuration profiles pointing to specific configuration data.
122. B — A validator (JSON Schema or Lambda function) enforces business-rule constraints like a minimum value before deployment is allowed.
123. A & B — Configuration changes don't require redeploying code or restarting processes, and a bake time after rollout still allows alarm-triggered rollback.
124. B — Since the code is already deployed and dormant, only the runtime flag needs to change — AppConfig's exact use case.
125. B — Bake time is the post-step observation window during which a tied alarm can still trigger an automatic rollback.
126. B — AppConfig natively supports the staged, alarm-monitored rollout described; Parameter Store has no equivalent native capability.
127. A & B — Free-form JSON/YAML configuration documents and feature-flag-specific profiles are both valid AppConfig configuration profile data types.
128. B — Automatic rollback only responds to alarms actually tied to the deployment; an uncovered failure mode won't trigger a rollback.
129. B — CodePipeline is the orchestrator sequencing the source, build, staging deploy, approval, and production deploy stages described.
130. B — CodeBuild resolves the Secrets Manager reference at build time; CodeDeploy executes the blue/green shift and its alarm-based rollback.
131. A — CodeArtifact, authenticated via aws codeartifact login in the install phase, provides governed, cached dependency resolution.
132. A & B — CodeDeploy handles the gradual Lambda version traffic shift with rollback; AppConfig handles the independent feature-flag rollout with rollback.
133. A — Referencing the secret properly, adding an approval gate, configuring alarm-based rollback, and moving to CodeArtifact with short-lived tokens address all four findings.
134. B — CodePipeline/CodeBuild/CodeDeploy with Lambda canary handles code changes, while AppConfig independently handles configuration/flag changes on its own cadence.
135. B — The exam consistently tests matching a scenario's requirement to the specific service and mechanism enabling safe, gradual, reversible delivery of code and configuration.
