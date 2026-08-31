# Module 00 — Exam Overview & AWS Fundamentals

This module is your foundation — everything after it assumes you're comfortable with what's here. It's deliberately not mapped to a single exam domain the way later modules are; it sets up the vocabulary, access patterns, and IAM mental model that every one of the four domains leans on.

## 1. The exam itself, in detail

**AWS Certified Developer – Associate (DVA-C02)**, straight from AWS's own exam guide:
- 65 questions, 130 minutes. Of those, **50 are scored and 15 are unscored** (AWS trials future questions on you without telling you which ones) — you cannot tell them apart, so treat every question as if it counts.
- Two question formats:
  - **Multiple choice** — one correct answer out of four options.
  - **Multiple response** — two or more correct answers out of five or more options, usually flagged with "(Select TWO)" or "(Select THREE)" in the question. **No partial credit** — you must get every correct option and no incorrect ones.
- Scaled score 100–1000, **pass at 720** (AWS uses a compensatory scoring model across domains, not a strict per-domain cutoff — you can be weak in one domain if you're strong elsewhere, as long as the overall scaled score clears 720). There's no published raw percentage; 720/1000 is *roughly* equivalent to ~72% but item weighting makes this an approximation, not a formula.
- No penalty for guessing → **never leave a question blank**.
- Delivered via Pearson VUE — test center or online proctored.
- Candidates are expected to have **1+ years of hands-on experience developing and maintaining AWS-hosted applications**. That's a real gap this course has to close for you as a beginner — which is why the notes go heavier on "why" and "how it's actually used" than a quick cheat sheet would.

### What's explicitly OUT of scope (AWS says this directly in the exam guide — don't over-study these)
- Designing architectures, distributed systems, or database schemas from scratch (that's the Solutions Architect exam's job — DVA-C02 tests *implementing against* a given design, not authoring one).
- Designing/creating CI/CD pipelines (using an existing pipeline is in scope; architecting one from zero is not).
- Administering IAM users and groups (day-to-day IAM admin is a SysOps/security-admin task; you need to *use* IAM as a developer, not run an identity program).
- Administering servers and operating systems (again, SysOps territory).
- Designing AWS networking infrastructure (VPC/Direct Connect design is out; using a VPC someone else designed — e.g. putting a Lambda function inside one to reach a private RDS instance — is in).

This matters for how you study: you'll see VPC, IAM roles, and CI/CD *concepts* throughout this course because you need to use them, but this course (correctly) won't turn into a networking or security-admin deep dive.

### Domain breakdown (memorize this table — it tells you where to spend study time)
| # | Domain | Weight |
|---|---|---|
| 1 | Development with AWS Services | 32% |
| 2 | Security | 26% |
| 3 | Deployment | 24% |
| 4 | Troubleshooting and Optimization | 18% |

Security is nearly a third of the exam by itself, and every other domain has security-flavored questions woven through it (least privilege, encryption, credential handling). You cannot pass this exam by only knowing how to write Lambda functions — you must know **how AWS services are secured, deployed, and debugged**, not just how to code against them.

### How DVA-C02 questions are actually written
Every real DVA-C02 question follows a fixed shape, and it's worth internalizing it now because it changes how you should read questions on exam day. Here's the shape, taken directly from AWS's own published sample questions:

1. **2–4 sentences of scenario**, third person, business-and-technical framing: "A company is migrating a legacy application to Amazon EC2 instances. The application uses a user name and password that are stored in the source code to connect to a MySQL database..."
2. **A separate, explicit question line**: "Which solution will meet these requirements?" or "Which combination of steps should the developer take to meet these requirements? (Select TWO.)"
3. **Four (or five, for multi-response) full-sentence options**, structurally parallel to each other, each naming a real, plausible AWS service/feature — the wrong answers are never jokes or nonsense, they're things that *sound* right unless you know the specific detail that rules them out.

### Worked example (this is the actual technique, applied)
> *A company is migrating a legacy application to Amazon EC2 instances. The application uses a user name and password that are stored in the source code to connect to a MySQL database. The company will migrate the database to an Amazon RDS for MySQL DB instance. As part of the migration, the company needs to implement a secure way to store and automatically rotate the database credentials. Which solution will meet these requirements?*
> A) Store the credentials in environment variables in an AMI; rotate by replacing the AMI.
> B) Store the credentials in Systems Manager Parameter Store; configure Parameter Store to auto-rotate.
> C) Store the credentials in environment variables on the EC2 instances; rotate by relaunching the instances.
> D) Store the credentials in Secrets Manager; configure Secrets Manager to auto-rotate.

Walking the elimination: the requirement has **two** parts — "secure storage" *and* "automatic rotation." A and C fail immediately because environment variables baked into an AMI or instance aren't "secure storage" in the sense AWS means (no encryption-at-rest-as-a-service, no access auditing, no rotation hook) — and neither replacing an AMI nor relaunching an instance is "automatic." That leaves B and D, both of which are legitimate secret stores. The differentiator: **Secrets Manager has built-in, schedulable automatic rotation (including native RDS rotation Lambda templates); Parameter Store does not have native automatic rotation** — you'd have to build that yourself with a custom Lambda + EventBridge schedule. Because the question explicitly asks for automatic rotation as a first-class requirement, **D** is correct. This exact distinction (Secrets Manager vs. Parameter Store, rotation being the tie-breaker) reappears constantly — it's covered in full in Module 14.

**The general technique:** find the 2-3 *distinct requirements* buried in the stem (here: "secure" + "automatic rotation"), eliminate any option that fails even one of them, and when two options both technically work, look for the specific AWS feature-level detail (not general knowledge) that the question is actually testing.

**Exam strategy tip:** on first pass, answer everything you're confident about, flag anything you have to think hard about, and move on — don't burn 8 minutes on one question. Pearson VUE lets you review flagged questions at the end. Full exam-day strategy and pacing math live in Module 17.

## 2. What is AWS, actually

AWS is a collection of independently-scalable managed services running across a global physical infrastructure, billed on a pay-as-you-go, consumption basis. As a developer, your job is knowing **which service to reach for**, **how it's secured**, **how it's deployed**, and **how to debug it when it breaks** — which maps exactly to the four exam domains.

### Global infrastructure hierarchy
- **Region** — a physical location (e.g. `us-east-1` = N. Virginia, `ap-south-1` = Mumbai). Regions are fully independent; data doesn't leave a region unless you explicitly move it. Most services are region-scoped.
- **Availability Zone (AZ)** — one or more discrete data centers within a region, each with independent power, cooling, and networking, but connected to other AZs in the region by low-latency links. A region has 3+ AZs typically. **Design for AZ failure**: spread resources (EC2 instances, RDS Multi-AZ, subnets) across at least 2 AZs for high availability.
- **Edge location / Local Zone / Wavelength Zone** — CloudFront and Route 53 points of presence, closer to end users than a full region, used for caching and DNS, and (Local/Wavelength Zones) low-latency compute for specific metros or 5G networks.

**Exam trap:** "Region" ≠ "Availability Zone." If a question says "highly available across data center failure," they mean multi-AZ, not multi-region (that's disaster recovery, a bigger ask).

### Global vs. Regional vs. AZ-scoped services
| Scope | Examples |
|---|---|
| Global | IAM, Route 53, CloudFront, AWS WAF (mostly), S3 (bucket names are globally unique but data lives in one region) |
| Regional | Lambda, DynamoDB, API Gateway, SNS, SQS, most services |
| AZ-scoped | EC2 instances, EBS volumes (an EBS volume only attaches to instances in the same AZ) |

## 3. Setting up and accessing AWS

### Root user vs. IAM users
- The **root user** is created with the AWS account (tied to the account's email). It has unrestricted access and **cannot be permission-restricted**. Best practice: enable MFA on it, don't use it for daily work, lock away its credentials, and create an IAM admin user/role for everyday tasks instead.
- **IAM users** are identities you create for people or applications, with permissions attached explicitly via policies.

### Ways to access AWS (all developer-relevant, all IAM-governed)
1. **Management Console** — browser UI.
2. **AWS CLI** — command-line tool (`aws s3 ls`, `aws lambda invoke ...`), configured via `aws configure`, which stores an access key ID + secret access key (and optionally a session token) in `~/.aws/credentials`, with default region/output format in `~/.aws/config`. Supports named profiles: `aws configure --profile dev` then `aws s3 ls --profile dev`.
3. **SDKs** — language-specific libraries (boto3 for Python, AWS SDK for JavaScript/Java/.NET/Go/etc.) that wrap the same underlying REST APIs the CLI and console use. This is what your actual application code calls at runtime.
4. **AWS CloudShell** — a browser-based shell pre-authenticated with your console credentials, no local install needed, persists a small amount of storage between sessions. Great for a one-off CLI command when you're on a machine without the CLI installed.
5. **AWS Cloud9** — a full browser-based IDE (not just a shell) backed by an EC2 instance (or, for some setups, run without a backing instance) — code editor, debugger, and terminal in one, pre-configured with the AWS CLI/SDKs and an IAM role for the environment. Useful when you want an actual development environment, not just command execution, without provisioning a local machine.

All five ultimately call the same **AWS APIs** and are governed by the same IAM permissions — there's no "console-only" backdoor around IAM. If your IAM user can't call `s3:PutObject`, it doesn't matter whether you try it from the console, the CLI, CloudShell, or a Python script — it fails identically everywhere.

### Credential resolution order (important for both exam and real life)
When you use the CLI or an SDK, credentials are resolved in this order (first found wins):
1. Explicit code parameters (hardcoded — **never do this**; the exam will flag this as an anti-pattern every time it appears as an option).
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
3. Shared credentials file (`~/.aws/credentials`).
4. Shared config file (`~/.aws/config`).
5. **Instance profile / IAM role** — for code running on EC2, ECS, or Lambda, credentials come from the attached role's temporary, auto-rotated credentials via the instance metadata service (EC2) or environment injection (Lambda, ECS task roles).

**Exam trap:** "What is the MOST secure way for an application running on EC2 to access S3?" → attach an **IAM role** to the instance (instance profile), never store long-lived access keys on the instance.

## 4. IAM fundamentals (you will see this in nearly every module)

IAM (Identity and Access Management) is global, free, and controls **who can do what** on **which resources**. Domain 2 (Security, 26% of the exam) leans on this constantly, so get it solid now.

### Core entities
- **User** — a persistent identity (person or service) with long-term credentials (password for console, access keys for API).
- **Group** — a collection of users; policies attached to a group apply to all members. Groups cannot be nested and cannot be referenced as a principal in a resource policy.
- **Role** — an identity *without* long-term credentials, assumed temporarily (via AWS STS) by users, applications, or AWS services (EC2, Lambda, etc.). This is how AWS services get permissions to call other AWS services, and how cross-account access works.
- **Policy** — a JSON document defining permissions. Attached to users, groups, or roles (identity-based policies) or directly to a resource like an S3 bucket (resource-based policies).

### Policy anatomy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadOnObjectsInOneBucket",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
      "Condition": {
        "IpAddress": { "aws:SourceIp": "203.0.113.0/24" }
      }
    }
  ]
}
```
- **Effect**: `Allow` or `Deny`.
- **Action**: the API call(s), `service:Action` format, wildcards allowed (`s3:Get*`).
- **Resource**: ARN(s) the statement applies to.
- **Condition** (optional): extra constraints — IP range, MFA presence, tags, time of day, etc.

### Evaluation logic (memorize this — it's tested directly and indirectly constantly)
1. Default is **implicit deny**.
2. An explicit **Deny** anywhere (identity policy, resource policy, SCP, permissions boundary) always wins — nothing overrides it.
3. Otherwise, an explicit **Allow** in *any* applicable policy grants access.
4. If nothing explicitly allows it, it's denied (implicit deny).

So evaluation order in effect: **explicit deny > explicit allow > implicit deny**.

### Managed vs. inline policies
- **AWS managed policies** — created/maintained by AWS (e.g. `AmazonS3ReadOnlyAccess`). Easy but sometimes broader than needed.
- **Customer managed policies** — you create and version them; reusable across many identities; best practice for anything beyond trivial permissions.
- **Inline policies** — embedded directly in a single user/group/role, 1:1 relationship, deleted when the identity is deleted. Used for one-off, tightly-scoped permissions that shouldn't be reused.

### Roles for services (the pattern you'll use constantly)
A Lambda function, EC2 instance, or ECS task doesn't use IAM users — it **assumes an IAM role**. The role has two attached policy types working together:
- A **trust policy** (who/what can assume it):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```
- A **permissions policy** (what it can do once assumed — e.g. read a specific DynamoDB table).

**Exam trap:** if a Lambda function can't access a resource it should be able to, the fix is almost always "attach/expand the execution role's permissions policy," not "give it access keys."

### Cross-account access (a real-world pattern worth internalizing now)
Say Company A's application needs to write to an S3 bucket that lives in Company B's AWS account. Company B creates a role in *their* account with a trust policy naming Company A's account ID as a trusted principal, plus a permissions policy scoping exactly what that role can do. Company A's application then calls `sts:AssumeRole` against that role's ARN and receives back temporary credentials (access key, secret key, session token) valid for a limited duration. No long-term credentials ever cross the account boundary — this is the standard, exam-favored way to grant a third party (a SaaS vendor, a partner account, a CI/CD pipeline in another account) scoped access without sharing secrets.

### Other IAM concepts you must know
- **MFA** — extra auth factor; can be *required* via policy `Condition` (`aws:MultiFactorAuthPresent`).
- **Permissions boundary** — a managed policy that sets the *maximum* permissions an identity can ever have, regardless of what its other policies grant. Used to let teams create their own IAM roles without escalating privilege.
- **Service Control Policies (SCPs)** — set at the AWS Organizations level, apply to entire accounts/OUs, also define maximum permissions. Not IAM policies themselves, but interact the same way (explicit deny wins).
- **IAM Access Analyzer** — flags resources shared with entities outside your account/org.
- **Least privilege** — the exam's favorite phrase; the "correct" answer usually grants the narrowest permission set that satisfies the requirement, nothing broader.
- A forward pointer: Module 14 goes deep on **federation (SAML/OIDC), Cognito user pools vs. identity pools, and bearer tokens (JWT/OAuth/STS)** — the "how does a mobile app's end user authenticate" side of security, distinct from the "how does my backend code authenticate to AWS" side covered here.

## 5. Shared Responsibility Model
AWS secures the **cloud** (physical infra, hypervisor, managed-service internals). You secure what's **in** the cloud (your data, IAM configuration, OS patching on EC2, network configuration, encryption choices, application-level security). For serverless/managed services (Lambda, DynamoDB, RDS), AWS takes on more (patching, OS) but you still own IAM, data, and application code — the line shifts by service but never disappears.

**Worked scenario:** a company runs a Node.js API both on self-managed EC2 instances and, for a newer microservice, on Lambda. A security review asks: "who patches the runtime?" On EC2, the customer owns OS and any language-runtime patching entirely (AWS never touches the guest OS). On Lambda, AWS patches the underlying execution environment and managed runtime versions, but the customer still owns *which* runtime version they select, their function code, its dependencies, and the IAM permissions granted to it. The shared-responsibility line moved, but "your code, your IAM config, your data" never moves to AWS, on any service.

## 6. Pricing & billing basics
- **On-Demand** — pay per second/hour, no commitment, most flexible, most expensive per unit.
- **Savings Plans / Reserved Instances** — commit to 1 or 3 years for a discount (up to ~72%), used for steady-state workloads. Compute Savings Plans apply flexibly across EC2, Fargate, and Lambda.
- **Spot Instances** — bid on spare EC2 capacity for up to ~90% discount; AWS can reclaim with a 2-minute warning. Good for fault-tolerant, interruptible workloads (batch jobs, CI runners), never for stateful/critical single-instance workloads.
- **Free Tier** — 12 months free for some services, always-free limits for others (e.g. Lambda's 1M free requests/month, forever).
- **AWS Budgets / Cost Explorer** — set alerts and visualize/forecast spend.
- **Billing is consolidated** across an AWS Organization, and Reserved Instance/Savings Plan discounts can share across linked accounts.

### Support plans
| Plan | Notes |
|---|---|
| Basic | Free, docs + forums only |
| Developer | Business-hours email support, for testing/dev |
| Business | 24/7, faster response, access to Trusted Advisor full checks |
| Enterprise | 24/7, TAM (Technical Account Manager), fastest response for production-down |

## 7. Well-Architected Framework (preview — full depth in Module 17)
Six pillars: **Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability**. Exam questions frequently test whether you recognize *which pillar* a design decision optimizes for, especially Security vs. Cost tradeoffs, or Reliability vs. Cost (e.g. Multi-AZ RDS costs more but survives an AZ failure that a single-AZ instance wouldn't).

## 8. Tagging & resource organization
Tags are key-value pairs on resources, used for cost allocation, automation (e.g. "shut down anything tagged `env=dev` after hours"), and access control (IAM policies can key off `aws:ResourceTag`). **Resource Groups** let you view/manage resources across services by tag.

## 9. Core service map (where everything else in this course fits)
| Category | Key services | Module |
|---|---|---|
| Compute | EC2, Lambda, Elastic Beanstalk, ECS/Fargate/EKS | 01, 04, 11, 12 |
| Storage | S3, EBS, EFS | 02 |
| Database | DynamoDB, RDS, Aurora, ElastiCache, MemoryDB | 03, 08 |
| API / Application Integration | API Gateway, AppSync, SQS, SNS, EventBridge, Kinesis, Step Functions | 05, 06, 07 |
| Deployment/IaC | CodeCommit, CodeBuild, CodeDeploy, CodePipeline, CodeArtifact, CloudFormation, SAM, CDK | 10, 13 |
| Security | IAM, KMS, Secrets Manager, Cognito, STS, ACM, WAF | 14 |
| Networking | VPC, Route 53, CloudFront, ELB | 15 |
| Observability | CloudWatch, X-Ray, CloudTrail, CodeGuru | 16 |

You'll go one level deep into every row of this table over the next 9 days.

## Key exam traps from this module
- Region ≠ Availability Zone; "survive a data center outage" = multi-AZ, not multi-region.
- Root user should never be used day-to-day; enable MFA and lock it away.
- Hardcoded access keys in code/EC2 = always the wrong answer when an IAM role is an option.
- Explicit Deny always wins, everywhere, regardless of how many Allows exist elsewhere.
- Spot instances = never for stateful, non-interruptible, single-point-of-failure workloads.
- "Least privilege" and "least operational overhead" are the two phrases that most often decide between two technically-valid answers.
- When a stem has multiple distinct requirements (e.g. "secure" *and* "automatic"), an option must satisfy **all** of them, not just the most obvious one.
