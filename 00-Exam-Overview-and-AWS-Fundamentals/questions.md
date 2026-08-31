# Module 00 — Practice Questions (120)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, ~30% multi-response. Answer key with explanations at the end.

### Exam Mechanics & Strategy (1–6)

1. A candidate is 40 minutes into a 130-minute DVA-C02 exam and has spent 12 minutes stuck on a single multi-response question about IAM cross-account roles, unable to decide between two plausible-looking options. According to recommended exam pacing strategy, what should the candidate do?
A) Continue working the question until certain, since accuracy matters more than pace
B) Flag the question for review, select the best current guess, and move on to the remaining questions
C) Leave the question blank and return to it only if time remains at the very end
D) Restart the exam section to reset the timer for that question

2. A developer reviewing their DVA-C02 score report learns that out of 65 total questions, only 50 contributed to their scaled score. What is the reason for this, and what should the developer's strategy have been during the exam?
A) 15 questions were technical glitches that AWS automatically discarded; no strategy change was needed
B) 15 questions were unscored items AWS was trialing for future exams, indistinguishable from scored ones, so every question should be answered as if it counts
C) The candidate answered 15 questions incorrectly, which AWS excludes from scoring as a courtesy
D) 15 questions were optional bonus questions that only improve the score, never lower it

3. A DVA-C02 question describes a company that needs to reduce compute cost for a fault-tolerant batch job "in the MOST cost-effective way possible," while a second, otherwise similar question about a single-instance production database asks for the "MOST reliable" solution. Why might the correct answer differ between these two questions even though both involve EC2 pricing models?
A) The constraint keyword in each question (cost vs. reliability) changes which pricing/architecture tradeoff is actually being tested, so identical-looking scenarios can have different correct answers
B) DVA-C02 questions about EC2 always have the same correct answer regardless of wording
C) Only the second question is a real scored question; the first is unscored and doesn't need careful reading
D) The constraint keywords are decorative and don't affect the correct answer

4. While reading a DVA-C02 scenario, a candidate notices the stem describes two separate requirements: the solution must be "secure" and must "require no manual intervention to rotate credentials." One answer option satisfies only the security requirement but not the automation requirement. How should this option be treated?
A) Selected, since it partially satisfies the scenario
B) Eliminated, because a correct answer must satisfy every explicitly stated requirement in the stem, not just some of them
C) Selected only if no other option mentions rotation at all
D) Flagged as the best answer if it is the shortest option

5. A test-taker has eliminated two of four options on a multiple-choice DVA-C02 question because they violate the security best practices covered in Module 00, but is still unsure which of the remaining two is correct. Both remaining options use a legitimate AWS secret-storage service. What should the test-taker look for next to break the tie?
A) The option that is worded most simply, regardless of technical accuracy
B) The specific feature-level detail that distinguishes the two services (for example, which one natively supports the exact capability the stem asks for, such as automatic rotation)
C) Whichever option appears first alphabetically
D) Whichever option was also correct on a previous, unrelated question

6. Which combination of exam-day facts should shape a candidate's overall pacing strategy for the 65-question, 130-minute DVA-C02 exam?
A) Roughly two minutes are available per question on average, and unscored questions are indistinguishable from scored ones
B) Only scored questions need to be answered; unscored questions can be skipped entirely
C) There is a strict per-domain minimum score in addition to the overall 720 pass mark
D) Wrong answers subtract points, so leaving uncertain questions blank protects the overall score

### Global Infrastructure (7–18)

7. A company's compliance team requires that a new application "survive the complete loss of a single data center without any downtime." An architect proposes deploying EC2 instances behind a load balancer in only one Availability Zone, arguing this is sufficient. Why does this proposal fail to meet the requirement?
A) A single Availability Zone already spans multiple data centers, so no change is needed
B) An Availability Zone maps to independent data center(s); a failure there would take down every instance in it, so the workload must span at least two AZs to survive that failure
C) Availability Zones cannot host EC2 instances at all
D) Load balancers automatically create redundant Availability Zones when attached

8. A regulated healthcare company must ensure patient records processed by its application never leave a specific country's borders, using AWS's default data-residency behavior rather than a custom replication policy. Which AWS concept, used as-is, satisfies this requirement?
A) Placing all resources in one Availability Zone
B) Deploying only within a single AWS Region located in that country, since Regions are isolated and data does not leave a Region unless explicitly configured to
C) Using only Edge locations within that country
D) Enabling AWS Organizations consolidated billing

9. A developer provisions an EBS volume in the `eu-west-1b` Availability Zone and then attempts to attach it to a running EC2 instance in `eu-west-1c`. The attach operation fails. What is the most likely cause?
A) EBS volumes can only attach to instances launched from the same AMI
B) EBS volumes are Availability Zone-scoped and can only attach to instances within that same AZ
C) EBS volumes require the instance to be stopped for at least 24 hours before attaching
D) EBS volumes can only be attached in the `us-east-1` Region

10. A solutions team is deciding where to deploy a new IAM policy that must apply consistently no matter which AWS Region their application later expands into. Which characteristic of IAM makes this straightforward?
A) IAM policies must be manually copied to every Region an application uses
B) IAM is a global service, so identities and policies are not tied to any single Region
C) IAM policies are Region-scoped like EC2 and must be replicated
D) IAM requires a separate account per Region

11. A media company wants to reduce latency for video content delivered to users across five continents without deploying and managing EC2 fleets in every Region. Which AWS capability directly addresses this?
A) Launching EC2 Auto Scaling groups in every Region worldwide
B) Amazon CloudFront caching content at edge locations close to end users globally
C) Creating additional Availability Zones in each Region
D) Increasing the size of EC2 instances in the primary Region

12. Which two statements about AWS Availability Zones are correct? (Select TWO.)
A) An AWS Region typically provides three or more Availability Zones
B) Availability Zones within a Region are connected by high-bandwidth, low-latency networking links
C) A single Availability Zone spans every Region in a geographic continent
D) Availability Zones share a single point of power and cooling failure with each other
E) An Availability Zone is a billing construct with no relationship to physical infrastructure

13. A gaming company wants ultra-low-latency compute placed physically closer to a specific major metropolitan area than any standard AWS Region can provide, for a small subset of latency-sensitive matchmaking servers. Which AWS infrastructure concept is designed for this use case?
A) A standard Availability Zone
B) An AWS Local Zone
C) A second full Region
D) An S3 bucket with Transfer Acceleration

14. Which of the following AWS services operates as a Regional service rather than a global one?
A) IAM
B) Amazon DynamoDB
C) Amazon Route 53
D) Amazon CloudFront

15. A startup is choosing between deploying its primary application in a single Region with Multi-AZ redundancy versus a full active-active multi-Region architecture. The startup's requirement is only to tolerate the loss of one data center, not an entire geographic Region, and they want to minimize operational complexity. Which approach best matches the actual requirement?
A) Multi-Region active-active, since more redundancy is always better regardless of requirements
B) Single Region with resources spread across multiple Availability Zones, since that directly satisfies the stated data-center-failure requirement with less operational complexity than multi-Region
C) A single Availability Zone with frequent manual backups
D) Multi-Region with only one Availability Zone used per Region

16. An S3 bucket named `acme-invoices-2026` is created in the `ap-southeast-2` Region. A developer on another team, in another AWS account, later tries to create a bucket with the exact same name in `us-east-1`. What happens?
A) It succeeds, because S3 bucket names are unique only within a Region
B) It fails, because S3 bucket names must be globally unique across all AWS accounts and Regions, even though the bucket's data itself resides in one chosen Region
C) It succeeds, because S3 buckets are Availability Zone-scoped, not Regional
D) It fails only if both accounts belong to the same AWS Organization

17. A company operating in the EU wants to use CloudFront to serve static assets to global users while ensuring the origin S3 bucket's actual object data remains stored only in an EU Region. Is this combination possible under AWS's Region/edge-location model?
A) No, CloudFront requires the origin's data to be replicated to every edge location's Region
B) Yes — CloudFront edge locations cache and serve copies of content globally, while the origin S3 bucket's authoritative data still resides only in the EU Region it was created in
C) No, S3 buckets used as CloudFront origins are automatically converted to global storage
D) Yes, but only if the AWS account has Enterprise support

18. Which statement correctly distinguishes a Region from an Availability Zone for exam purposes?
A) They are interchangeable terms for the same concept
B) A Region is a geographic area containing multiple isolated Availability Zones; surviving "a data center failure" requires spanning AZs, while surviving "a Region failure" requires a second Region entirely
C) An Availability Zone contains multiple Regions
D) Regions are used only for billing, and Availability Zones are used only for compute

### Access Methods, Credentials & Dev Environments (19–32)

19. A developer needs to run a handful of AWS CLI commands from a shared workstation that does not have and should not have the CLI installed locally, using their existing console sign-in. Which AWS tool best fits this need?
A) AWS Cloud9
B) AWS CloudShell
C) A new EC2 instance dedicated to running CLI commands
D) AWS CodeArtifact

20. A team wants a full browser-based IDE — code editor, debugger, and terminal together — pre-configured with the AWS CLI and SDKs and backed by an IAM role, so a new contractor can start contributing without setting up a local development environment. Which service is purpose-built for this?
A) AWS CloudShell
B) AWS Cloud9
C) Amazon Cognito
D) AWS CodeStar

21. A developer runs `aws configure --profile staging` and enters a separate access key and secret key from their default profile. They then run `aws s3 ls`. Which credentials are used?
A) The staging profile's credentials, because named profiles are always used regardless of flags
B) The default profile's credentials, because no `--profile staging` flag was passed on the `aws s3 ls` command itself
C) Both profiles' credentials are merged automatically
D) The command fails because two profiles cannot coexist

22. An application deployed on an EC2 instance needs to call the Amazon S3 API. The team is deciding between hardcoding an IAM user's access keys into the application's configuration file versus attaching an IAM role to the EC2 instance. Which approach is correct, and why?
A) Hardcoded access keys, because they never expire and are simpler to manage
B) An IAM role (instance profile), because it provides temporary, automatically-rotated credentials without ever storing a long-term secret on the instance
C) Either approach is equally secure as long as the config file is not committed to source control
D) Hardcoded access keys, because IAM roles cannot be attached to running instances

23. A CI/CD build agent running on AWS CodeBuild needs to call several AWS APIs during a build. Following AWS security best practice, how should it obtain credentials?
A) Store an IAM user's long-term access keys as plaintext environment variables in the build project
B) Attach an IAM service role to the CodeBuild project so it receives temporary credentials automatically
C) Prompt a human to paste in temporary credentials at the start of every build
D) Disable IAM entirely for the build project to simplify configuration

24. Which of the following correctly orders the AWS SDK's default credential resolution behavior from HIGHEST to LOWEST priority, for code running on an EC2 instance with both environment variables set and an instance role attached?
A) Instance role credentials, then environment variables
B) Environment variables, then the shared credentials file, then the instance role (as the last fallback)
C) The instance role is always used regardless of any other configured source
D) Whichever source was configured most recently in time

25. A developer wants to verify, from the command line, exactly which IAM identity (user or role) and which AWS account their currently active credentials belong to, before running a potentially destructive command. Which CLI command accomplishes this?
A) `aws iam list-users`
B) `aws sts get-caller-identity`
C) `aws configure list-profiles`
D) `aws ec2 describe-instances`

26. A security audit flags that a legacy application still authenticates to AWS using a hardcoded access key and secret key embedded directly in its source code repository. What is the recommended remediation, consistent with AWS best practices covered across this exam?
A) Leave it as-is if the repository is private
B) Replace the hardcoded credentials with an IAM role (if running on AWS compute) or, if that isn't possible, retrieve credentials at runtime from a secret-management service rather than embedding them in code
C) Rotate the key once per year and continue embedding it in the code
D) Move the credentials into a code comment for visibility

27. Which AWS access method is most appropriate for an application's runtime code (as opposed to a human operator) to call AWS APIs programmatically?
A) The AWS Management Console
B) An AWS SDK, using credentials obtained via an attached IAM role
C) AWS CloudShell
D) Manually typing AWS CLI commands during each request

28. A developer wants to switch between three different AWS accounts (dev, staging, prod) from their local terminal without repeatedly re-entering credentials. What CLI feature is designed for this?
A) Multiple simultaneous root user logins
B) Named CLI profiles configured via `aws configure --profile <name>`, selected per command with `--profile`
C) A single shared IAM user across all three accounts
D) Disabling IAM in two of the three accounts

29. Which two of the following are true about how the AWS Management Console, AWS CLI, and AWS SDKs relate to each other? (Select TWO.)
A) All three ultimately call the same underlying AWS REST APIs
B) All three are governed by the same IAM permissions, so a denied action fails identically regardless of which one is used
C) The Console has special access that bypasses IAM policy evaluation
D) The CLI and SDKs share credentials but the Console uses a completely separate authorization system
E) Only the SDK is capable of triggering billing charges

30. A junior developer asks why their application code should never read the raw response of the EC2 instance metadata service into application logs. What is the security concern being addressed?
A) It has no security implications; it is purely a performance concern
B) The metadata service can expose the instance's temporary IAM role credentials, and logging that response risks leaking those credentials
C) The metadata service response is always encrypted, so logging it is safe
D) Only Windows instances expose sensitive data via metadata

31. A company wants new engineers to be productive on day one without installing any local tooling, while still being able to write, run, and debug code in an environment that has AWS credentials pre-configured through an IAM role rather than static keys. Which AWS service is the best fit?
A) AWS Cloud9
B) Amazon EC2 with manual SSH key distribution
C) AWS CodeArtifact
D) Amazon Cognito

32. Which statement about AWS CloudShell is accurate?
A) It requires a separate CLI installation on the user's machine
B) It is a browser-based shell, pre-authenticated with the user's console credentials, requiring no local setup
C) It can only run PowerShell commands
D) It provisions a permanent, billed EC2 instance per user

### IAM Core: Policies, Roles & Evaluation (33–62)

33. A developer's IAM identity has one policy attached that grants `s3:*` on all resources, and a second policy that explicitly denies `s3:DeleteObject` on a specific bucket. What is the net effect when the developer attempts to delete an object in that bucket?
A) The delete succeeds because the broad Allow was attached more recently
B) The delete is denied, because an explicit Deny in any applicable policy always overrides an Allow, regardless of how broad the Allow is
C) The delete succeeds because Allow always takes precedence over Deny
D) The result is undefined and depends on which policy is evaluated first

34. An IAM user has no policies attached at all — not directly, not through a group, and no resource-based policy grants them access either. What can this user do when calling any AWS API?
A) Everything, since no explicit Deny exists
B) Nothing, because the default behavior for any action not explicitly allowed is implicit deny
C) Only read-only actions
D) Only actions available through the Console, not the CLI

35. A Lambda function's execution role currently has no permissions policy granting DynamoDB access, and the function's code calls `dynamodb:GetItem`. The call fails with an AccessDenied error. What is the correct fix?
A) Give the Lambda function a set of hardcoded IAM user access keys instead of using a role
B) Attach or expand a permissions policy on the Lambda function's execution role to grant the required DynamoDB actions
C) Delete and recreate the DynamoDB table so it inherits new default permissions
D) Disable IAM enforcement for the Lambda service

36. A platform team wants developers to be able to create their own IAM roles for new microservices, but must guarantee that none of those self-created roles can ever be granted permissions broader than a predefined safe maximum, even by accident. Which IAM feature is designed exactly for this?
A) A permissions boundary attached to the roles developers are allowed to create
B) An inline policy on the developer's own IAM user
C) Enabling MFA on the developer's IAM user
D) A resource-based policy on an S3 bucket

37. Which IAM policy type is created and maintained directly by AWS, cannot be edited by customers, and is typically broader in scope than a hand-tailored policy for a specific task?
A) Inline policy
B) Customer managed policy
C) AWS managed policy
D) Permissions boundary

38. A company wants a policy that is reusable across 12 different IAM roles, independently versioned, and centrally auditable from one place. Which policy type best satisfies these requirements?
A) An inline policy duplicated across all 12 roles
B) A customer managed policy, attached to all 12 roles
C) A resource-based bucket policy
D) A permissions boundary

39. Under what circumstance is an inline IAM policy the more appropriate choice over a customer managed policy?
A) When the exact same permission set needs to be reused across many unrelated identities
B) When a tightly-scoped, one-off permission needs to be permanently and exclusively tied to a single identity's lifecycle, being deleted automatically if that identity is deleted
C) Inline policies should never be used under any circumstance
D) When the policy needs to be shared across AWS accounts

40. Which two components must an IAM role assumed by an AWS Lambda function have configured correctly for the function to both be allowed to assume the role AND perform its intended actions? (Select TWO.)
A) A trust policy naming `lambda.amazonaws.com` as a trusted principal allowed to call `sts:AssumeRole`
B) A permissions policy granting the specific actions the function's code needs to perform
C) A long-term IAM user access key embedded in the function's environment variables
D) A Route 53 hosted zone
E) An EC2 key pair

41. A company in Account A wants to grant a partner company in Account B temporary, auditable access to a specific S3 bucket, without creating any IAM user or sharing any long-term credentials across the account boundary. What is the recommended pattern?
A) Create an IAM user in Account A and email its access key to Account B
B) Create an IAM role in Account A with a trust policy naming Account B as a trusted principal; Account B's principals call `sts:AssumeRole` to receive temporary credentials
C) Share Account A's root user password with Account B
D) Disable IAM on the S3 bucket

42. What does a successful call to `sts:AssumeRole` return to the caller?
A) A new, permanent IAM user
B) Temporary security credentials: an access key ID, secret access key, and session token, valid for a limited duration
C) A CloudFormation stack ARN
D) A permanent replacement for the caller's original credentials

43. A policy statement includes the condition block `"Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}}` attached to an Allow statement for a sensitive `iam:DeleteRole` action. What is the effect of this condition?
A) It has no functional effect and is purely documentation
B) It restricts the Allow so the action only succeeds if the caller authenticated using multi-factor authentication
C) It requires the caller to be using a VPN
D) It automatically enables MFA for the caller if they don't already have it

44. Two policy statements apply to the same IAM role: one grants `dynamodb:Query` and `dynamodb:GetItem` scoped to a single table's ARN; a second, broader statement elsewhere grants `dynamodb:*` on `Resource: "*"`. From a least-privilege design perspective, what is the problem with this combination?
A) There is no problem; combining broad and narrow statements is the recommended pattern
B) The broad wildcard statement undermines the least-privilege intent of the narrow statement, since the role effectively has unrestricted DynamoDB access across all tables
C) DynamoDB does not support wildcard resource ARNs, so the broad statement is invalid
D) The narrow statement silently overrides the broad one automatically

45. A company uses AWS Organizations to manage 15 linked AWS accounts and wants to enforce an account-wide guardrail preventing any identity in any of those accounts — even an account administrator — from ever disabling CloudTrail logging. Which mechanism operates at the right scope to enforce this?
A) An IAM permissions boundary applied individually to every user in every account
B) A Service Control Policy (SCP) applied at the AWS Organizations level
C) An S3 bucket policy
D) A Lambda resource-based policy

46. Which statement correctly describes the relationship between Service Control Policies (SCPs) and IAM policies?
A) SCPs replace IAM policies entirely; once SCPs are enabled, IAM policies are ignored
B) SCPs set the maximum available permissions (guardrails) at the account/OU level; IAM policies still must separately grant the actual permissions within whatever an SCP allows
C) SCPs only apply to S3 and have no effect on other services
D) SCPs and IAM policies are evaluated completely independently with no interaction

47. An engineer wants to identify whether any S3 bucket or IAM role in their account has been configured to allow access from outside their AWS account or AWS Organization, possibly unintentionally. Which AWS capability is designed to surface exactly this?
A) AWS Budgets
B) IAM Access Analyzer
C) Amazon Inspector
D) AWS Trusted Advisor (Basic support tier)

48. A resource-based policy is attached directly to an S3 bucket, granting a specific external AWS account read access to objects in that bucket. Which of the following is true about this policy type compared to an identity-based policy?
A) Resource-based policies can only be used with IAM users, never with external accounts
B) A resource-based policy is attached to the resource itself (here, the bucket) rather than to an identity, and can grant access to principals outside the resource owner's own account
C) Resource-based policies cannot include a Principal element
D) Resource-based policies always take lower precedence than identity-based policies

49. Which two of the following actions would violate the principle of least privilege for an IAM role attached to a Lambda function whose only job is to read (not write) items from a single specified DynamoDB table? (Select TWO.)
A) Granting only `dynamodb:GetItem` and `dynamodb:Query` scoped to that table's ARN
B) Granting `dynamodb:*` scoped to `Resource: "*"`
C) Granting `dynamodb:DeleteTable` scoped to that same table's ARN, in addition to the read actions
D) Granting `dynamodb:GetItem` scoped only to that table's ARN
E) Omitting any DynamoDB permissions entirely

50. A policy's `Resource` element is set to `arn:aws:s3:::finance-reports/*`. Which of the following does this scope the statement to?
A) The bucket resource itself only, not any objects inside it
B) The objects stored inside the `finance-reports` bucket, not the bucket resource itself (bucket-level actions like `s3:ListBucket` require the bucket ARN without the `/*` suffix)
C) Every bucket in the AWS account
D) Nothing; this is invalid ARN syntax

51. What is the correct way to interpret "least privilege" when a DVA-C02 question asks which IAM policy a developer should attach to a new role?
A) Attach the broadest AWS managed policy available, to avoid future access issues
B) Grant only the specific actions and resources required for the role's actual task, and nothing more
C) Always attach `AdministratorAccess` for new roles during initial development, then narrow it later
D) Least privilege only applies to production environments, not development

52. An IAM policy simulator check shows that a user is denied `s3:GetObject` on a bucket despite having an identity-based policy that allows `s3:*` on all resources. Investigation reveals the bucket has a bucket policy explicitly denying access from any principal outside a specific VPC endpoint, and the user is connecting from outside that VPC. What determines the final outcome?
A) The identity-based Allow wins because it is more specific
B) The explicit Deny in the bucket's resource-based policy wins over the identity-based Allow, regardless of how broad the Allow is
C) The most recently modified policy wins
D) Bucket policies cannot deny access that an identity policy allows

53. Which of the following is NOT a valid value for the `Effect` element in an IAM policy statement?
A) `Allow`
B) `Deny`
C) `Restrict`
D) Both A and B are the only valid values, making C invalid

54. A company wants every new IAM role created by its development teams to automatically be prevented from ever being granted `iam:*` (full IAM administration) permissions, no matter what policies a developer later attaches to that role. Which single IAM feature enforces this at role-creation time?
A) A permissions boundary set to deny/exclude `iam:*` actions, attached to every role developers create
B) A customer managed policy attached after the fact
C) An inline policy attached to the developer's own user
D) MFA enforcement on the developer's user

55. Two IAM policies are evaluated for a single API call: Policy X allows the action with no conditions; Policy Y denies the same action only when the request does not originate from a specific corporate IP range. A request arrives from outside that IP range. What is the result?
A) Allowed, because Policy X is unconditional
B) Denied, because Policy Y's explicit Deny condition is met by this request, and explicit Deny always overrides Allow
C) Allowed, because two policies conflicting always defaults to Allow
D) The system throws an error and the request is discarded

56. Which best explains why AWS recommends using IAM roles instead of IAM users for workloads running on EC2, Lambda, or ECS?
A) Roles are cheaper than users
B) Roles provide temporary, automatically-rotated credentials obtained via assumption, eliminating the need to store and manage long-term secrets on compute resources
C) Roles support more total permissions than users can ever have
D) Roles are required for the console to function at all

57. A condition key of `aws:SourceIp` is added to a Deny statement in an S3 bucket policy, denying all access to requests NOT originating from `198.51.100.0/24`. What does this achieve?
A) It encrypts all objects in the bucket automatically
B) It restricts bucket access to only the specified IP range by explicitly denying everything outside it
C) It only affects the AWS Management Console, not the CLI or SDK
D) It has no effect on S3, since S3 does not support IP-based conditions

58. Fine-grained access control that lets each authenticated end user of an application access only the DynamoDB items belonging to their own user ID, using a single shared IAM role rather than one role per user, is best achieved using:
A) A separate IAM role manually created for every application end user
B) IAM policy condition keys such as `dynamodb:LeadingKeys`, mapping the caller's identity to the partition key they're allowed to access
C) Removing IAM entirely for that table
D) A permissions boundary with no condition keys

59. Which two statements correctly describe IAM groups? (Select TWO.)
A) Groups allow applying a shared set of policies to many IAM users at once
B) Groups can be nested inside other groups for hierarchical permission management
C) Groups cannot be used as a principal in a resource-based policy
D) Groups can be assumed by EC2 instances the same way roles can
E) Groups replace the need for any IAM policy entirely

60. A new employee's IAM user is added to a group that grants read-only S3 access, and separately has an inline policy directly on their user granting `s3:DeleteBucket`. With no explicit Deny anywhere, what can this user do?
A) Only read-only S3 actions, since group policies always take precedence over inline policies
B) Both the read-only group-granted actions and the individually-granted `s3:DeleteBucket` action, since without conflicting explicit Denies, all applicable Allows across every attached policy combine
C) Nothing, because a user cannot have both a group policy and an inline policy simultaneously
D) Only `s3:DeleteBucket`, since inline policies override group policies entirely

61. A company's security team wants to periodically verify that no IAM policy in the account grants overly permissive access (such as `"Action": "*", "Resource": "*"`) before it causes an incident. Besides manual review, which AWS-native capability supports this kind of proactive analysis?
A) AWS Budgets
B) IAM Access Analyzer, which can also validate policies against AWS best practices
C) Amazon Route 53 health checks
D) AWS CodeArtifact

62. Which of the following is the most accurate summary of IAM policy evaluation order for a single API request touching one resource?
A) Random order between all applicable policies
B) Explicit Deny (in any applicable identity-based, resource-based, permissions boundary, or SCP policy) beats explicit Allow, which beats the default implicit deny
C) Whichever policy was created first always wins
D) Resource-based policies are always ignored if an identity-based policy exists

### Shared Responsibility Model (63–76)

63. A company runs its application on self-managed EC2 instances. During a security review, the team is asked who is responsible for patching the guest operating system running on those instances. According to the Shared Responsibility Model, who owns this task?
A) AWS, as part of "security of the cloud"
B) The customer, since guest OS patching on EC2 falls under "security in the cloud"
C) Neither party; AWS EC2 instances patch themselves automatically with no configuration
D) AWS Support, but only on the Enterprise support plan

64. A team migrating a workload from EC2 to AWS Lambda asks how their patching responsibilities change. Which statement accurately describes the shift?
A) Responsibilities are identical on both services; nothing changes
B) On Lambda, AWS patches the underlying execution environment and manages the runtime host, while the customer still owns their function code, chosen runtime version, dependencies, and the IAM permissions granted to the function
C) On Lambda, the customer becomes responsible for patching the physical hardware
D) Moving to Lambda eliminates all customer security responsibilities entirely

65. For an Amazon RDS database with "auto minor version upgrade" enabled, who is responsible for applying the database engine's minor version patches?
A) The customer must manually apply every minor patch
B) AWS applies them automatically as part of the managed RDS service
C) A third-party contractor selected by AWS
D) The patches are optional and never required

66. Regardless of which AWS service is used — EC2, Lambda, RDS, or DynamoDB — which of the following always remains the customer's responsibility under the Shared Responsibility Model?
A) Patching the hypervisor
B) IAM configuration and classification/protection of the customer's own data
C) Physical data center security
D) Maintaining the global network backbone

67. A company enables server-side encryption on an S3 bucket using an AWS KMS customer-managed key. Which parts of this setup are the customer's responsibility versus AWS's?
A) AWS is responsible for everything, including key policy configuration
B) The customer is responsible for choosing to enable encryption, configuring the KMS key and its policy/rotation settings; AWS is responsible for the underlying encryption implementation and physical security of the storage
C) The customer has no responsibility once encryption is enabled once
D) Encryption at rest is impossible on S3 regardless of configuration

68. Who is responsible for configuring TLS/HTTPS so that data is encrypted in transit between a client and an application's own API endpoints?
A) AWS automatically encrypts all traffic with no customer configuration required, for every service
B) The customer must explicitly configure TLS/HTTPS for their own application endpoints
C) This responsibility does not exist on AWS
D) Only AWS Support can configure this, upon request

69. Which phrase pairing correctly matches "security OF the cloud" and "security IN the cloud" to their respective owners?
A) "OF the cloud" = customer; "IN the cloud" = AWS
B) "OF the cloud" = AWS (physical infrastructure, hypervisor, managed-service internals); "IN the cloud" = customer (data, IAM config, guest OS where applicable, application-level security)
C) Both phrases refer to AWS's responsibilities only
D) Both phrases refer to the customer's responsibilities only

70. A company using DynamoDB (a fully managed NoSQL database) asks whether the Shared Responsibility Model still applies, given how much AWS manages. Which statement is correct?
A) The model no longer applies once a service is "fully managed"
B) The model still applies — AWS manages more of the underlying infrastructure (servers, OS, patching, scaling) for a fully managed service, but the customer still owns IAM permissions, data content, and access configuration
C) The customer has zero responsibilities on any fully managed service
D) AWS becomes responsible for the customer's IAM policies once a service is fully managed

71. A startup's new backend developer assumes that because AWS "handles security," they don't need to configure IAM policies carefully for their Lambda functions. Why is this assumption incorrect?
A) It is actually correct; AWS configures all IAM policies automatically
B) IAM configuration (least-privilege permissions, role scoping) is explicitly a customer responsibility under the Shared Responsibility Model, regardless of how managed the compute service is
C) Only EC2-based workloads require IAM configuration by the customer
D) IAM only matters for AWS Support cases, not application security

72. Which of these responsibilities shifts from the customer toward AWS as a workload moves from EC2 → Elastic Beanstalk → Lambda, in terms of increasing service abstraction?
A) IAM permission configuration
B) Underlying server/OS/infrastructure management
C) Application code correctness
D) Data classification decisions

73. A company stores personally identifiable information (PII) in an application database and asks AWS Support who is responsible for classifying that data as sensitive and applying appropriate access controls. What is the correct answer?
A) AWS Support classifies and protects all customer data automatically
B) The customer is responsible for data classification (e.g., identifying PII/PHI) and for applying the appropriate access controls and encryption
C) Data classification is not necessary on AWS
D) Only Amazon Macie users need to classify data; everyone else is exempt

74. Under the Shared Responsibility Model, which of the following is always AWS's responsibility, with no service-dependent exceptions?
A) The customer's application-level authentication logic
B) Physical security of AWS data centers and the global network infrastructure
C) The customer's choice of IAM policy scope
D) The customer's encryption key rotation schedule

75. Which two of the following are customer responsibilities on Amazon RDS, even with automated backups and Multi-AZ enabled? (Select TWO.)
A) Configuring IAM database authentication or credential management appropriately
B) Choosing appropriate instance sizing and monitoring for the workload
C) Patching the underlying hypervisor
D) Replacing failed physical storage hardware
E) Building the RDS service's internal replication engine

76. A company assumes that enabling Multi-AZ on RDS makes patch management no longer necessary. Why is this assumption wrong?
A) Multi-AZ has nothing to do with patching, and even with auto minor version upgrade, the customer is still responsible for approving/scheduling major version upgrades and overall database configuration decisions
B) Multi-AZ disables all patching permanently
C) Multi-AZ transfers all future responsibilities to the customer instead
D) Multi-AZ is unrelated to RDS entirely

### Pricing, Billing & Support (77–96)

77. A company runs a batch video-rendering workload that can tolerate interruption and automatically resume from checkpoints, and wants to minimize compute cost as much as possible. Which EC2 pricing model offers the deepest discount for this profile?
A) On-Demand Instances
B) Standard Reserved Instances
C) Spot Instances
D) Dedicated Hosts

78. A finance team commits to running a fixed fleet of application servers 24/7 for the next three years and wants the largest possible discount in exchange for that commitment, while accepting reduced flexibility to change instance families later. Which purchasing option best fits?
A) Spot Instances
B) Standard Reserved Instances
C) On-Demand Instances
D) Dedicated Instances with no commitment

79. A company runs commercial database software licensed per physical CPU socket, a licensing model that requires visibility into and control over the specific physical server the software runs on. Which EC2 purchasing option satisfies this licensing requirement?
A) On-Demand Instances
B) Spot Instances
C) Dedicated Hosts
D) Savings Plans

80. A team wants a compute discount that flexibly applies across a mix of EC2 instances, Fargate tasks, and Lambda invocations, without committing to a specific instance family or service ahead of time. Which pricing construct is designed for this flexibility?
A) Standard Reserved Instances
B) Compute Savings Plans
C) Spot Instances
D) Dedicated Hosts

81. Which of the following workloads is the LEAST appropriate candidate for Spot Instances?
A) A CI/CD build fleet that can restart failed jobs automatically
B) A distributed batch-rendering farm designed for node loss
C) A single-node production database with no replica and no automated failover
D) An ad-hoc data analysis cluster that checkpoints progress periodically

82. An AWS Organization with consolidated billing has 8 linked accounts. One account purchases a set of Reserved Instances. Under default settings, can the RI discount apply to matching instance usage in the other 7 linked accounts?
A) No, RI discounts never share across accounts under any configuration
B) Yes, RI (and Savings Plan) discounts can be shared across linked accounts within an AWS Organization under consolidated billing
C) Only if each account separately purchases its own identical RIs
D) Only if all 8 accounts are in the same Availability Zone

83. A small team is testing AWS services in a non-production sandbox account and wants email-based, business-hours support access if they run into a service question, without paying for 24/7 guaranteed response times. Which AWS Support plan tier fits this need most cost-effectively?
A) Basic
B) Developer
C) Business
D) Enterprise

84. A company running a production workload experiences an outage and needs guaranteed access to a support engineer 24/7 with fast response times, but does not require a named Technical Account Manager. Which is the minimum support tier that satisfies this?
A) Basic
B) Developer
C) Business
D) None of the paid tiers include 24/7 engineer access

85. Which AWS Support plan is the only one that includes a dedicated Technical Account Manager (TAM)?
A) Business
B) Developer
C) Enterprise
D) Basic

86. A finance team wants automatic email alerts whenever forecasted AWS spend is on track to exceed a monthly threshold, before the month closes. Which AWS service is purpose-built for this?
A) AWS Cost Explorer alone, with no alerting capability
B) AWS Budgets, which supports threshold-based and forecasted-spend alerts
C) AWS CloudTrail
D) AWS Trusted Advisor Basic checks only

87. Which AWS service is best suited for visualizing and forecasting historical AWS spend trends over time, without configuring proactive alerts?
A) AWS Cost Explorer
B) Amazon CloudWatch Logs
C) AWS Config
D) AWS X-Ray

88. A workload has highly unpredictable, bursty traffic, and the team explicitly does not want to make any capacity commitment. Which EC2 pricing model matches this requirement, accepting a higher per-unit cost in exchange for maximum flexibility?
A) Standard Reserved Instances
B) On-Demand Instances
C) 3-year Savings Plans
D) Dedicated Hosts

89. Which two statements correctly distinguish Savings Plans from Reserved Instances? (Select TWO.)
A) Savings Plans commit to a consistent dollar-per-hour spend, applied flexibly across eligible usage, rather than to one specific instance configuration
B) Reserved Instances commit to specific instance attributes (family, in the case of Standard RIs) in exchange for their discount
C) Savings Plans can only be purchased for exactly 6 months
D) Reserved Instances can never be resold or exchanged under any circumstance
E) Savings Plans and Reserved Instances provide identical discounts with zero differences

90. A company's AWS Free Tier 12-month period has expired, but their monthly Lambda usage remains under 1 million requests and under 400,000 GB-seconds of compute time. What happens to their Lambda charges for usage within those limits?
A) They are billed normally since the 12-month Free Tier has expired
B) They remain free, because certain Lambda usage is part of an "Always Free" tier that does not expire after 12 months
C) They are billed at double the standard rate as a post-Free-Tier penalty
D) Free Tier eligibility is determined solely by account age, unrelated to usage amount

91. Dedicated Hosts, compared to Dedicated Instances, provide which additional capability that matters for certain enterprise licensing scenarios?
A) A larger discount over On-Demand pricing in all cases
B) Visibility into and control over the specific physical server and its socket/core layout
C) Automatic conversion to Spot pricing
D) Free data transfer between Regions

92. A company wants to reduce EC2 compute costs by up to approximately 90% for a workload consisting of many small, independent, restartable worker processes, and is willing to accept instance interruption with a short notice period. Which pricing model delivers this level of discount?
A) On-Demand Instances
B) Spot Instances
C) Standard Reserved Instances
D) Dedicated Hosts

93. Which AWS Support plan tier provides access to the complete set of Trusted Advisor checks (not just the limited free checks)?
A) Basic only
B) Business and above
C) Developer only
D) No support tier includes Trusted Advisor

94. A team wants to set a hard monthly spending limit alert of $5,000 for a specific project, tagged accordingly, with a notification sent once forecasted spend is projected to cross that limit before month-end. Which AWS capability, combined with cost allocation tags, achieves this?
A) AWS Budgets scoped by cost allocation tag, with a forecasted-spend alert
B) AWS CloudTrail event filtering
C) Amazon GuardDuty findings
D) AWS Config conformance packs

95. Which of the following is NOT one of the standard EC2 purchasing options?
A) On-Demand
B) Spot
C) "Guaranteed" Instances
D) Reserved Instances / Savings Plans

96. A billing analyst notices Reserved Instance coverage is at 60% for steady-state workloads, while some short-lived dev/test instances remain uncovered and running On-Demand. Is this mixed approach considered a cost-optimization anti-pattern?
A) Yes, everything should always run as Reserved Instances
B) No — matching predictable steady-state usage to Reserved Instances/Savings Plans while leaving unpredictable short-lived usage on On-Demand is the recommended cost-optimization pattern, not an anti-pattern
C) Yes, all workloads should run exclusively On-Demand
D) No, but only because Spot Instances were not used instead

### Well-Architected Framework & Tagging (97–108)

97. A company is deciding between a cheaper single-AZ RDS deployment and a more expensive Multi-AZ deployment with automatic failover for a production order-processing database. Choosing Multi-AZ despite the added cost primarily reflects a deliberate tradeoff favoring which Well-Architected pillar over Cost Optimization?
A) Sustainability
B) Reliability
C) Performance Efficiency
D) Operational Excellence

98. Which Well-Architected Framework pillar is most directly concerned with encryption choices, IAM least-privilege design, and identity/access management decisions?
A) Cost Optimization
B) Security
C) Performance Efficiency
D) Sustainability

99. A team automates infrastructure deployments and replaces error-prone manual server configuration steps with repeatable, version-controlled infrastructure-as-code templates. This change is best described as optimizing for which pillar?
A) Operational Excellence
B) Security only
C) Cost Optimization only
D) None of the six pillars directly

100. How many pillars does the AWS Well-Architected Framework currently define?
A) 4
B) 5
C) 6
D) 8

101. A company tags all of its AWS resources with `env`, `owner`, and `cost-center` keys. Which two practical benefits does this tagging strategy directly enable? (Select TWO.)
A) Cost allocation reports broken down by team or environment
B) Automatic relocation of resources to a different AWS Region
C) Automation scripts that can identify and act on resources by tag (for example, stopping all `env=dev` resources overnight)
D) Replacing the need for any IAM policy
E) Automatic encryption of all tagged resources

102. Can an IAM policy grant or restrict access based on a resource's tag value, rather than only its ARN?
A) No, tags have no relationship to IAM at all
B) Yes, using condition keys such as `aws:ResourceTag` to scope access based on a resource's tags
C) Only for EC2 instances, no other service
D) Only when using the root user

103. A team consistently over-provisions EC2 instance sizes "to be safe," without ever reviewing actual CPU/memory utilization data to right-size afterward. This practice most directly conflicts with which Well-Architected pillar?
A) Security
B) Cost Optimization
C) Reliability
D) Sustainability is entirely unrelated to compute sizing

104. Which AWS capability allows viewing and managing resources across multiple different AWS services together, grouped by a shared tag rather than by service type?
A) AWS Resource Groups
B) Amazon Route 53
C) AWS Certificate Manager
D) AWS X-Ray

105. A company's leadership asks the cloud team to reduce the carbon footprint of its workloads by choosing efficient instance types, right-sizing, and using managed services where practical. This objective maps most directly to which Well-Architected pillar, introduced as the sixth pillar?
A) Reliability
B) Sustainability
C) Security
D) Performance Efficiency

106. Which Well-Architected pillar is best demonstrated by a multi-AZ Auto Scaling Group with automated health-check-based instance replacement, ensuring the application recovers automatically from an instance or AZ failure?
A) Cost Optimization
B) Reliability
C) Sustainability
D) Security

107. A newly created AWS account has no tagging strategy in place, making it difficult for the finance team to determine which department's project is responsible for a given month's EC2 spend. What is the most direct remedy?
A) Disable EC2 entirely until a strategy is defined
B) Implement a consistent resource tagging strategy (e.g., `cost-center`, `project`, `owner` tags) enforced at resource creation, enabling cost allocation reporting
C) Switch all workloads to a single shared IAM user
D) Move all resources to a single Availability Zone

108. Choosing Compute Savings Plans and right-sizing over-provisioned instances after reviewing CloudWatch utilization metrics is an example of applying which Well-Architected pillar in practice?
A) Cost Optimization
B) Security
C) Sustainability exclusively
D) Reliability exclusively

### Integrative Scenarios (109–120)

109. A newly created AWS account's root user credentials are currently used by three different engineers for day-to-day development work, with no MFA enabled. A new cloud lead is asked to fix this before any other work proceeds. Which combination of actions should they take first? (Select TWO.)
A) Enable MFA on the root user and secure its credentials so they are no longer used for daily work
B) Create individual IAM users or roles for each engineer with appropriately scoped permissions for their daily work
C) Delete the root user entirely, since AWS accounts do not require one
D) Share the root user's MFA device physically between the three engineers
E) Grant `AdministratorAccess` directly to the root user to simplify management

110. A company operating in a single Region wants its new application to remain available if one data center becomes unavailable, without needing to survive the loss of the entire Region, and wants to minimize both cost and operational complexity relative to a full multi-Region design. Which architecture best matches these stated requirements?
A) Single Availability Zone with frequent snapshots
B) Resources spread across at least two Availability Zones within the Region, behind a load balancer
C) Active-active deployment across three separate Regions
D) A single EC2 instance with Spot pricing for cost savings

111. A startup's application currently authenticates to AWS using an IAM user's long-term access keys hardcoded into its source code, running on an EC2 instance, with no MFA on any account, and using the root user occasionally for convenience. Which combination of changes brings this into line with AWS best practices covered in this module? (Select TWO.)
A) Replace the hardcoded access keys with an IAM role attached to the EC2 instance
B) Enable MFA on the root user and stop using it for routine tasks
C) Continue using the root user, but rotate its password monthly
D) Store the same hardcoded access keys in an environment variable instead, and consider the issue resolved
E) Grant the IAM role `AdministratorAccess` to avoid future permission errors

112. A regulated company must guarantee that data never leaves a specific Region (satisfied by default Regional isolation), that IAM access follows least privilege, and that spend is tracked per project via tags. Which three module 00 concepts together satisfy these three requirements respectively?
A) Availability Zones; SCPs; Resource Groups
B) Regions (default data residency); least-privilege IAM policy design; consistent resource tagging with cost allocation
C) Edge locations; root user usage; Reserved Instances
D) CloudFront; permissions boundaries; Spot Instances

113. A company wants developers to create their own IAM roles for new services (for velocity), while guaranteeing via an account-wide guardrail that no identity in the account — including any newly self-created role — can ever disable CloudTrail, and additionally wants each individual role capped at a safe maximum permission set. Which two controls together satisfy both goals? (Select TWO.)
A) A Service Control Policy at the Organizations level preventing CloudTrail from being disabled account-wide
B) A permissions boundary applied to roles that developers are allowed to create, capping their maximum possible permissions
C) A single shared IAM user with `AdministratorAccess` for all developers
D) Disabling IAM entirely for developer-created roles
E) Storing all developer credentials in source control for easy access

114. An application running on Lambda needs to read a secret database password at runtime and call an internal company API in another AWS account. Which two practices are consistent with this module's guidance? (Select TWO.)
A) Retrieve the database password from a secret-management service at runtime rather than hardcoding it in the function
B) Use IAM role assumption (`sts:AssumeRole`) with a cross-account trust relationship to call the API in the other account, rather than sharing long-term credentials
C) Hardcode both the database password and the other account's access keys directly in the function code for simplicity
D) Store the database password in a public S3 bucket for easy retrieval
E) Use the root user's credentials for the cross-account call since it always has permission

115. A company evaluating EC2 purchasing options has three distinct workloads: (1) a steady 24/7 production API server fleet, (2) an interruption-tolerant nightly batch analytics job, and (3) unpredictable ad-hoc load-testing sessions with no fixed schedule. Which pricing model pairing correctly matches each workload?
A) All three should use On-Demand for simplicity
B) (1) Reserved Instances/Savings Plans, (2) Spot Instances, (3) On-Demand Instances
C) (1) Spot Instances, (2) On-Demand, (3) Reserved Instances
D) All three should use Dedicated Hosts for consistency

116. A mid-sized company wants: 24/7 engineer access for production issues, forecasted spend alerts before a monthly budget is exceeded, and resources tagged so each team's spend can be reported separately. Which three capabilities respectively satisfy these three needs?
A) Enterprise support tier; AWS CloudTrail; permissions boundaries
B) Business (or higher) support tier; AWS Budgets with forecasted alerts; a consistent tagging strategy with cost allocation tags
C) Basic support; AWS Config; Availability Zones
D) Developer support tier; AWS X-Ray; Service Control Policies

117. Reading a dense DVA-C02 scenario, a candidate identifies three requirements in the stem: "secure," "requires no ongoing manual credential rotation," and "auditable per environment." Two answer options both use a legitimate AWS secrets service, but only one explicitly supports native automatic rotation. Applying the elimination technique from this module, what should the candidate do?
A) Pick either option since both mention a secrets service
B) Eliminate the option lacking native automatic rotation support, since it fails one of the three explicitly stated requirements
C) Pick the option with the shortest wording
D) Skip the question since two options seem valid

118. A company wants to combine strong reliability (survive an AZ failure) with strong cost control (avoid paying for idle standby capacity) for a stateless web tier. Which combination of concepts from this module addresses both goals simultaneously?
A) A single large On-Demand instance in one AZ
B) An Auto Scaling group spanning multiple AZs, sized dynamically to actual demand, mixing On-Demand baseline capacity with Spot Instances where interruption is tolerable
C) Dedicated Hosts in a single AZ
D) Manually launched instances with no scaling policy

119. A security review of a three-month-old AWS account finds: the root user is used weekly without MFA, IAM users have broad `AdministratorAccess` policies "for convenience," no resource tagging exists, and Reserved Instances were purchased for a workload that turned out to be short-lived and interruption-tolerant. Which of the following is the LEAST accurate characterization of this account's issues?
A) The root user usage without MFA is a security risk regardless of other factors
B) Broad `AdministratorAccess` grants for convenience violate least privilege
C) The Reserved Instance purchase was optimal because Reserved Instances are always the cheapest option for any workload
D) Lack of tagging will make it difficult to attribute costs or automate resource management later

120. A company completes this module and must summarize, in one sentence for a new hire, why understanding IAM evaluation logic, the Shared Responsibility Model, Regions/AZs, and pricing options together matters for the rest of the DVA-C02 exam. Which summary best captures it?
A) These are unrelated trivia topics only tested in Module 00 and nowhere else
B) These foundational concepts recur throughout every later domain — security questions lean on IAM evaluation logic, deployment and troubleshooting questions assume knowledge of Regions/AZs and shared responsibility, and cost-aware answers assume familiarity with pricing tradeoffs
C) Only the IAM content matters; Regions, shared responsibility, and pricing are exam-irrelevant
D) These topics are only relevant to the Solutions Architect exam, not DVA-C02

---

## Answer Key & Explanations

1. B — Flag it, guess your current best answer, and move on; Pearson VUE allows returning to flagged questions, and burning excessive time on one question risks not reaching later ones.
2. B — 15 of 65 are unscored trial questions, indistinguishable from scored ones, so treat every question as if it counts.
3. A — The constraint keyword (cost vs. reliability) is exactly what determines which tradeoff, and therefore which answer, is correct.
4. B — A correct answer must satisfy every explicitly stated requirement, not just some of them; partial satisfaction means elimination.
5. B — When two legitimate options remain, the tie-breaker is the specific AWS feature-level detail the stem is actually testing.
6. A — About two minutes per question on average, and unscored questions look identical to scored ones so all must be treated as counting.
7. B — An AZ maps to independent data center(s); single-AZ deployment doesn't survive that AZ's failure, so at least two AZs are required.
8. B — Regions are isolated by default; choosing a Region within the required country satisfies default data residency with no extra configuration.
9. B — EBS volumes are AZ-scoped and only attach to instances within the same AZ.
10. B — IAM is a global service; identities and policies aren't Region-specific.
11. B — CloudFront's edge locations cache content close to users globally without deploying compute in every Region.
12. A & B — Regions provide 3+ AZs, and AZs are interconnected with high-bandwidth, low-latency links.
13. B — AWS Local Zones bring compute physically closer to specific metro areas for latency-sensitive use cases.
14. B — DynamoDB is Regional; IAM, Route 53, and CloudFront are global services.
15. B — The stated requirement (survive one data center's loss, minimize complexity) is exactly satisfied by Multi-AZ within a single Region; multi-Region is unnecessary added complexity here.
16. B — S3 bucket names are globally unique across all accounts and Regions, even though the underlying data resides in one Region.
17. B — CloudFront edge locations cache copies globally while the S3 origin's authoritative data stays in its one chosen Region.
18. B — A Region contains multiple isolated AZs; "data center failure" maps to multi-AZ, "Region failure" maps to multi-Region.
19. B — CloudShell provides a browser-based, pre-authenticated shell with no local install needed.
20. B — Cloud9 is a full browser IDE (editor, debugger, terminal) pre-configured with AWS tooling and an IAM role.
21. B — Without the `--profile staging` flag on that specific command, the default profile's credentials are used.
22. B — An IAM role/instance profile provides temporary, auto-rotated credentials, avoiding any long-term secret on the instance.
23. B — Attach an IAM service role to the CodeBuild project rather than embedding static long-term keys.
24. B — The default chain checks env vars and the credentials file before falling back to the instance role last.
25. B — `aws sts get-caller-identity` reports the account, ARN, and user/role ID behind the active credentials.
26. B — Replace hardcoded credentials with an IAM role where possible, or retrieve secrets at runtime from a secret-management service.
27. B — Application runtime code should use an SDK backed by role-derived credentials, not manual console/CLI steps.
28. B — Named CLI profiles let you switch between multiple accounts'/credential sets easily via `--profile`.
29. A & B — All three access paths call the same underlying APIs and are governed by identical IAM permissions.
30. B — The metadata service can expose temporary IAM role credentials; logging its raw response risks leaking them.
31. A — Cloud9 offers a ready-to-code browser IDE preconfigured with an IAM role, no local setup required.
32. B — CloudShell is browser-based and pre-authenticated with the user's console credentials, no local install needed.
33. B — An explicit Deny in any applicable policy always overrides an Allow, no matter how broad that Allow is.
34. B — With zero applicable policies, the default implicit deny applies to everything.
35. B — Expand the Lambda execution role's permissions policy rather than introducing static credentials.
36. A — A permissions boundary caps the maximum permissions any role created under it can ever have.
37. C — AWS managed policies are authored/maintained by AWS and can't be edited by customers.
38. B — A customer managed policy is reusable, independently versioned, and centrally auditable across many identities.
39. B — Inline policies suit a tightly-scoped, one-off permission permanently tied to a single identity's lifecycle.
40. A & B — A trust policy (who can assume the role) and a permissions policy (what it can do) are both required.
41. B — Cross-account role assumption via a trust policy avoids ever sharing long-term credentials.
42. B — `AssumeRole` returns temporary credentials: access key, secret key, and session token.
43. B — This condition restricts the Allow to only succeed when the caller authenticated with MFA.
44. B — The broad wildcard statement undermines the least-privilege intent of the narrower one, since Allows combine.
45. B — SCPs, applied at the Organizations/OU level, are the right scope for an account-wide, unbypassable guardrail.
46. B — SCPs set maximum available permissions as guardrails; IAM policies still grant actual permissions within that boundary.
47. B — IAM Access Analyzer identifies resources shared with entities outside the account/organization.
48. B — A resource-based policy attaches to the resource and can grant access to principals outside the owner's account.
49. B & C — A wildcard grant and an unnecessary `DeleteTable` permission both exceed what a read-only function needs.
50. B — The `/*` suffix scopes to objects inside the bucket; bucket-level actions need the bare bucket ARN.
51. B — Least privilege means granting only what's actually required for the task, nothing broader.
52. B — The resource-based policy's explicit Deny overrides the identity-based Allow regardless of its breadth.
53. C — "Restrict" is not a valid Effect value; only Allow and Deny are valid.
54. A — A permissions boundary constrains the maximum permissions any role created under it can ever receive, including `iam:*`.
55. B — Policy Y's Deny condition is met by this request, and an explicit Deny always overrides an Allow.
56. B — Roles provide temporary, auto-rotated credentials, removing the need to manage long-term secrets on compute resources.
57. B — This Deny statement restricts bucket access to only the specified IP range.
58. B — `dynamodb:LeadingKeys` scopes per-user access to items matching the caller's own partition key via a single shared role.
59. A & C — Groups apply shared policies to many users, and cannot act as a principal in a resource-based policy.
60. B — Without conflicting explicit Denies, all Allows across every attached policy (group and inline) combine.
61. B — IAM Access Analyzer supports proactive policy validation against best practices, beyond manual review.
62. B — Explicit Deny (from any applicable policy source) beats explicit Allow, which beats implicit deny by default.
63. B — Guest OS patching on EC2 is the customer's "security in the cloud" responsibility.
64. B — On Lambda, AWS manages the execution host/runtime patching, but code, dependencies, runtime choice, and IAM stay with the customer.
65. B — With auto minor version upgrade enabled, AWS applies RDS engine minor patches as part of the managed service.
66. B — IAM configuration and data classification/protection are always customer responsibilities, across every service.
67. B — The customer configures encryption and key settings; AWS implements and physically secures the underlying mechanism.
68. B — Customers must explicitly configure TLS/HTTPS for their own application endpoints; it isn't automatic for arbitrary apps.
69. B — "OF the cloud" is AWS's job (infrastructure); "IN the cloud" is the customer's job (data, IAM, app security).
70. B — The model still applies; AWS manages more infrastructure on fully managed services, but IAM/data ownership stays with the customer.
71. B — IAM configuration remains a customer responsibility regardless of how managed the underlying compute service is.
72. B — Underlying server/OS/infrastructure management increasingly shifts to AWS as abstraction increases; IAM, code, and data classification stay with the customer.
73. B — The customer is responsible for classifying sensitive data and applying appropriate controls.
74. B — Physical data center and global network security are always AWS's responsibility, with no service-dependent exceptions.
75. A & B — Credential/IAM database auth configuration and appropriate instance sizing/monitoring remain customer responsibilities even with Multi-AZ.
76. A — Multi-AZ addresses availability, not patch/version management; major version upgrade decisions remain a customer responsibility.
77. C — Spot Instances offer the deepest discount for interruption-tolerant, checkpointable workloads.
78. B — Standard RIs trade reduced flexibility for the largest discount on a 1-3 year commitment.
79. C — Dedicated Hosts expose the physical server, satisfying socket-based licensing requirements.
80. B — Compute Savings Plans flexibly apply across EC2, Fargate, and Lambda usage.
81. C — A single-node production database with no failover is the worst fit for Spot's interruption model.
82. B — RI/Savings Plan discounts can be shared across linked accounts under AWS Organizations consolidated billing.
83. B — Developer support provides business-hours email access appropriate for sandbox/testing use.
84. C — Business support is the minimum tier including 24/7 engineer access with fast response times.
85. C — Only Enterprise support includes a dedicated Technical Account Manager.
86. B — AWS Budgets supports threshold and forecasted-spend alerting.
87. A — Cost Explorer is designed for visualizing and forecasting historical spend trends.
88. B — On-Demand suits unpredictable, bursty usage with no commitment, at a higher per-unit cost.
89. A & B — Savings Plans commit to flexible $/hour spend; RIs commit to specific instance attributes for their discount.
90. B — Some Lambda usage falls under an "Always Free" tier that persists beyond the initial 12 months.
91. B — Dedicated Hosts provide visibility/control over the physical server's socket and core layout.
92. B — Spot Instances can offer up to roughly 90% savings for interruption-tolerant, restartable workloads.
93. B — Business support (and above) includes access to the full set of Trusted Advisor checks.
94. A — AWS Budgets, scoped by cost allocation tag, with a forecasted-spend alert, satisfies this exactly.
95. C — "Guaranteed" Instances is not a real EC2 purchasing option.
96. B — Matching steady-state usage to RIs/Savings Plans while leaving unpredictable usage On-Demand is the recommended pattern.
97. B — Paying more for Multi-AZ failover is a deliberate Reliability-over-Cost tradeoff.
98. B — Encryption and IAM least-privilege design fall under the Security pillar.
99. A — Automating deployments and removing manual, error-prone steps maps to Operational Excellence.
100. C — The framework currently defines six pillars.
101. A & C — Tags enable cost allocation reporting and tag-based automation.
102. B — `aws:ResourceTag` condition keys allow tag-based access control in IAM policies.
103. B — Chronic over-provisioning without right-sizing review is a Cost Optimization anti-pattern.
104. A — AWS Resource Groups let you view/manage resources across services by shared tag.
105. B — Sustainability, the sixth pillar, addresses environmental/carbon-footprint impact of workloads.
106. B — Automated, multi-AZ failure recovery is a textbook Reliability pattern.
107. B — A consistent, enforced tagging strategy directly enables cost allocation reporting by department/project.
108. A — Reviewing utilization metrics and applying Savings Plans/right-sizing is Cost Optimization in practice.
109. A & B — Secure and stop using the root user for daily work, and create properly-scoped individual IAM identities instead.
110. B — Multi-AZ within a single Region directly satisfies "survive one data center's loss" with lower cost/complexity than multi-Region.
111. A & B — Replace hardcoded keys with an instance role, and secure/stop routine root user usage.
112. B — Regions provide default data residency, least-privilege IAM design satisfies access control, and tagging enables cost tracking per project.
113. A & B — An Organizations-level SCP blocks disabling CloudTrail account-wide, while a permissions boundary caps each self-created role's maximum permissions.
114. A & B — Retrieve secrets at runtime from a secrets service, and use cross-account role assumption rather than sharing long-term credentials.
115. B — Steady-state fits Reserved Instances/Savings Plans, interruption-tolerant batch fits Spot, and unpredictable ad-hoc fits On-Demand.
116. B — Business+ support gives 24/7 engineer access, Budgets gives forecasted alerts, and tagging enables per-team cost reporting.
117. B — Eliminate the option that fails one of the three explicitly stated requirements (native automatic rotation).
118. B — A multi-AZ Auto Scaling group sized to demand, mixing On-Demand and Spot, balances reliability and cost simultaneously.
119. C — Reserved Instances are NOT always optimal; they're poorly suited to short-lived, interruption-tolerant workloads, making this the least accurate statement.
120. B — These foundational concepts recur across every domain of the exam, not just Module 00.
