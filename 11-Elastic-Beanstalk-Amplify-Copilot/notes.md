# Module 11 — Elastic Beanstalk, Amplify & Copilot

Domain focus: primarily **Deployment (24%)**, with a direct hit on **Domain 3 Task Statement 3** ("Deploy code using AWS CI/CD services," which explicitly names **approved-version environments** — Lambda aliases, container image tags, **Amplify branches**, and **Copilot environments** — as exam-testable concepts) and a supporting hit on **Domain 1 Task Statement 1** (choosing the right architectural abstraction for a given team and application). This module is about three different "don't hand-write the infrastructure yourself" tools that sit at different points on the abstraction spectrum, each aimed at a different kind of application and team. The exam's real test here is rarely "define Elastic Beanstalk" — it's "given this team profile and this app shape, which of these tools (or none of them) is the right reach."

## 1. Why these three tools exist together

All three are **developer-facing deployment abstractions** that generate and manage lower-level AWS resources (EC2, ASGs, ELBs, ECS services, CloudFormation stacks) on your behalf, so you interact with an application concept instead of individual resources:

- **Elastic Beanstalk (EB)** — upload application code, EB provisions and wires together EC2/Auto Scaling/ELB (and optionally RDS) underneath it, while leaving those resources fully inspectable and tunable in the console or CLI. It is *not* pure serverless — you can still SSH into the underlying instances if you need to.
- **Amplify** — a full-stack toolchain (CLI, Console/Studio, Hosting, and client libraries) aimed at frontend-heavy applications that need a backend of Cognito (auth), AppSync/API Gateway (API), S3 (storage), and Lambda (functions), plus fully managed Git-based hosting for the frontend itself.
- **Copilot** — a CLI that deploys containerized applications to ECS on Fargate (or to App Runner for simpler request-driven services) by generating and managing CloudFormation for you, so you describe a service in a small `manifest.yml` instead of writing ECS task definitions and service definitions by hand.

All three ultimately produce standard AWS resources and, under the hood, all three lean on CloudFormation (Amplify and Copilot explicitly; EB uses its own orchestration but exposes environments that map cleanly to CFN-describable resources). None of them is "more real" AWS than the others — they're convenience layers, and the exam wants you to know when each layer's convenience is worth the loss of raw control, and when you should skip the layer entirely and write CloudFormation/SAM/CDK yourself.

## 2. AWS Elastic Beanstalk

### 2.1 What it is
Elastic Beanstalk is AWS's PaaS-style (Platform as a Service) deployment tool: you upload your application code (a ZIP, WAR, or JAR — a "source bundle"), select a supported platform, and Beanstalk provisions everything needed to run it — EC2 instances (via an Auto Scaling group), an Elastic Load Balancer, security groups, and (optionally) an RDS database — while still giving you inspectable, tunable access to every one of those resources. This is the key differentiator from pure serverless (Lambda) or from a fully hidden black-box platform: **Beanstalk is a convenience layer over resources you still own and can reach into**, not a new execution model.

### 2.2 Supported platforms
Beanstalk ships "platforms" for common runtimes: Java SE, Java with Tomcat, Node.js, PHP, Python, Ruby, Go, .NET on Windows Server / .NET Core on Linux, and Docker (single-container). If your stack matches a supported platform, Beanstalk is a fast on-ramp; if it doesn't, you're back to raw EC2 or a container-based service.

### 2.3 Environment tiers — web server vs. worker
This is a frequently tested, easy-to-miss detail: an EB **environment** comes in one of two tiers, and they behave very differently.

| Tier | Traffic source | Underlying resources | Typical use |
|---|---|---|---|
| **Web server tier** | Public HTTP(S) requests via a load balancer | ELB + Auto Scaling group of EC2 instances | Standard web apps and APIs |
| **Worker tier** | Messages pulled from an **SQS queue** — not direct public traffic | Auto Scaling group of EC2 instances running the "beanstalk worker daemon," an SQS queue (created automatically if you don't supply one), optional `cron.yaml` for scheduled/periodic tasks | Background/async processing decoupled from the request path |

**Exam trap:** if a scenario describes an application that needs to process long-running background jobs pulled from a queue, without exposing anything to the public internet, the answer is an EB **worker environment**, not a web server environment with a queue bolted on. The worker tier is purpose-built for this and handles the SQS polling and message deletion for you (including a configurable HTTP path the daemon posts the message body to on your instance).

### 2.4 Environment configuration — `.ebextensions` and saved configurations
- **`.ebextensions`**: a folder at the root of your source bundle containing `.config` files (YAML or JSON) that customize the environment beyond the defaults — setting environment variables, tuning Auto Scaling group settings, installing OS packages, running commands during deployment, or even declaring additional AWS resources via an embedded `Resources:` section (which is literally a CloudFormation snippet merged into the environment's underlying stack).
- **Saved configurations**: a snapshot of an environment's configuration (platform, instance type, scaling settings, environment variables, etc.) saved as a template (stored in S3) that can be applied when creating new environments — useful for keeping dev/staging/prod environments consistent, or quickly recreating an environment after `eb terminate`.

Example `.ebextensions/01-environment.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    NODE_ENV: production
    LOG_LEVEL: info
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.small
    IamInstanceProfile: aws-elasticbeanstalk-ec2-role
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 6

container_commands:
  01_run_migrations:
    command: "npm run migrate"
    leader_only: true
```

`leader_only: true` ensures a command (like a DB migration) runs on only one instance during a multi-instance deployment, not once per instance.

### 2.5 Deployment policies
When you deploy a new application version to an existing environment, Beanstalk offers several deployment policies, each trading off deployment speed against downtime/risk and infrastructure cost:

| Policy | How it works | Downtime | Extra cost during deploy | Rollback speed |
|---|---|---|---|---|
| **All at once** | Deploys to every instance simultaneously | Brief downtime while instances update | None | Slow — must redeploy previous version |
| **Rolling** | Deploys in batches; each batch is taken out of service during its update | No full downtime, but reduced capacity during the rollout | None | Slow — must roll forward again |
| **Rolling with additional batch** | Launches one new batch of instances *before* taking any existing batch out of service, maintaining full capacity throughout | None, and no capacity dip | Yes — temporary extra instances | Slow — must roll forward again |
| **Immutable** | Launches an entirely new, fully separate Auto Scaling group with the new version, health-checks it, then shifts traffic and terminates the old group | None | Yes — briefly doubles capacity | Fast — just terminate the new (bad) group |
| **Traffic splitting** | Immutable-style new group, but shifts only a configurable percentage of traffic to it first (canary), monitoring before a full cutover | None | Yes, temporarily | Fast |

**Blue/Green via environment swap** is a related but distinct pattern, not one of the deployment-policy dropdown options above: you create an entirely **new, separate EB environment** running the new application version, test it independently (it has its own URL), and then use **"swap environment URLs"** (an EB CNAME swap) to atomically redirect production traffic to it. This gives you the cleanest possible separation and instant rollback (swap back), at the cost of running two full environments during the transition. The exam sometimes lists this as a fifth deployment "policy" in casual phrasing — know that mechanically it's a CNAME swap between two independent environments, not a same-environment rolling mechanism.

**Exam trap:** "must maintain full capacity throughout the deployment, no reduction in available instances" → **rolling with additional batch** (not plain rolling). "Needs the fastest possible full rollback if something goes wrong, and cost isn't the primary concern" → **immutable** or **blue/green swap**. "Fastest deploy, some downtime acceptable" → **all at once**.

### 2.6 Application versions and version lifecycle
Every time you deploy, Beanstalk packages your source bundle as an **application version** — a specific, labeled, immutable artifact stored as an object in an EB-managed S3 bucket, associated with a logical **application** (the container for all versions and environments of one product). Because every past version stays in S3, rolling back is as simple as re-deploying an older application version label to an environment (subject to the deployment policy above still applying to *how* that redeploy rolls out).

Regions impose a **soft quota on the number of application versions** you can retain (historically around 1,000 per application per region); left unmanaged, this can be exhausted by frequent CI/CD deploys. Beanstalk supports an **application version lifecycle policy** that automatically expires old versions by age or by count, deleting the S3 source bundle too (with an option to retain versions currently deployed to a running environment even if they'd otherwise expire).

### 2.7 Health monitoring
- **Basic health reporting** — health is inferred from ELB and Auto Scaling signals (instance status checks, load balancer health checks). Environment health is shown as a simple color: Green (OK), Yellow (Warning/Degraded), Red (Severe), Grey (Info/Pending/Unknown).
- **Enhanced health reporting** — a health agent on each instance publishes more granular OS-level and application-level metrics (CPU, latency, HTTP status code counts, deployment status) to CloudWatch and to the EB console's health dashboard, giving much richer troubleshooting detail than basic reporting.

### 2.8 CLI and CI/CD parity
The **EB CLI** (`eb`) mirrors what you can do in the console, which matters for automation: `eb init` (configure the local project/region/platform), `eb create` (create a new environment), `eb deploy` (push a new application version to an existing environment), `eb config` (edit a saved configuration), `eb logs`, `eb ssh`, `eb terminate`. Because the exact same commands and configuration files (`.elasticbeanstalk/config.yml`, `.ebextensions/*.config`) work identically whether run by a developer locally, invoked from a CI/CD pipeline (e.g., a CodeBuild buildspec step running `eb deploy`, tying back to module 10's CI/CD concepts), or triggered through the console, there's no drift between "how a developer deploys" and "how the pipeline deploys" — this console/CLI/CI parity is itself a testable point: Beanstalk doesn't require a separate automation-only interface.

## 3. AWS Amplify

### 3.1 What it is
Amplify is a full-stack development framework, CLI, and hosting platform aimed squarely at **frontend-heavy applications** (web and mobile) that need a managed backend without the team hand-building it. A typical Amplify-backed app pairs a frontend (React, Vue, Next.js, Flutter, iOS/Android native, etc.) with a backend Amplify provisions and wires up for you: **Cognito** for authentication, **AppSync** (GraphQL) or **API Gateway** (REST) for the API layer, **S3** for file storage, and **Lambda** for custom business logic — all deployed as CloudFormation stacks that the `amplify` CLI manages (`amplify add auth`, `amplify add api`, `amplify push` to provision/update).

### 3.2 Amplify Hosting and branch-based environments
**Amplify Hosting** is Amplify's fully managed CI/CD and static/SSR web hosting service. You connect a Git repository (GitHub, GitLab, Bitbucket, or CodeCommit), and Amplify automatically builds and deploys on every push. The exam-relevant detail, matching the official exam guide's phrase **"Amplify branches"** under approved-version environments: **each connected Git branch becomes its own deployed environment with its own unique URL** — push to `main` and Amplify deploys and serves the `main` environment; push to a `dev` branch and Amplify deploys a completely separate, independently addressable `dev` environment, often with its own backend resources if you've enabled per-branch backend environments. Amplify Hosting can additionally spin up **ephemeral preview environments per pull request**, letting reviewers click through a live, deployed version of a proposed change before merging.

**Exam trap:** "each Git branch should map to an isolated, independently deployed environment reachable at its own URL, with no manual environment-provisioning step" is describing **Amplify Hosting's branch model**, almost word for word — this is one of the exam guide's explicitly named concepts, so expect it tested directly.

### 3.3 Amplify libraries
The **Amplify client libraries** (JavaScript, iOS, Android, Flutter) give frontend code high-level, category-based APIs — `Auth`, `API`, `Storage`, `DataStore`, `Analytics`, `PubSub` — that talk to the backend resources Amplify provisioned, handling the plumbing a developer would otherwise hand-roll: Cognito token refresh and session management for `Auth`, signed request generation for `API`/`Storage`, and (via `DataStore`) local-first offline data with automatic sync and conflict resolution against AppSync/DynamoDB once connectivity returns. This is the piece that makes Amplify a *full-stack* tool rather than just a hosting product — the frontend code and the backend it calls are generated and kept in sync by the same toolchain.

### 3.4 `amplify.yml` build settings
Amplify Hosting builds are driven by an `amplify.yml` file (auto-generated, but editable) analogous in spirit to a CodeBuild buildspec — it defines build phases for the frontend (and, if backend deploys are part of the pipeline, a `backend` phase too):

```yaml
version: 1
backend:
  phases:
    build:
      commands:
        - amplifyPush --simple
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

`baseDirectory` tells Amplify Hosting which folder holds the final built static assets to publish; `cache.paths` speeds up subsequent builds by persisting dependency caches between runs, just like caching in a CodeBuild buildspec.

## 4. AWS Copilot

### 4.1 What it is
Copilot is a CLI tool for deploying **containerized applications to ECS on Fargate** (or to **App Runner** for simple request-driven HTTP services) without hand-writing CloudFormation, ECS task definitions, or service definitions. You describe a service declaratively in a `manifest.yml`, and Copilot generates and manages the underlying CloudFormation stacks (VPC, ECS cluster, service, task definition, ALB, IAM roles, autoscaling policies) on your behalf — conceptually the container-world sibling of Elastic Beanstalk, aimed at teams who want ECS/Fargate's flexibility without the CloudFormation authoring overhead.

### 4.2 Service types and `manifest.yml`
`copilot init` scaffolds an application and a first service, asking you to choose a service type: **Load Balanced Web Service** (public HTTP service behind an ALB), **Backend Service** (internal-only, no public load balancer, reachable from other services via service discovery), **Worker Service** (subscribes to SQS/SNS for async processing — the Copilot analog of Beanstalk's worker tier), or **Request-Driven Web Service** (deploys to App Runner instead of ECS, for the simplest possible container-to-HTTPS-endpoint path).

Example `copilot/api/manifest.yml` for a Load Balanced Web Service:

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

The `environments:` block lets a single manifest override settings (instance count, environment variables, CPU/memory) per deployment target — which leads directly into Copilot's environment model.

### 4.3 Environments
A Copilot **environment** (`copilot env init`) is a named deployment target — typically `test`, `staging`, `prod` — each backed by its own isolated infrastructure (its own VPC, ECS cluster, and related resources) within the same Copilot **application** (the logical grouping of services and environments, analogous to an EB "application"). This is the exam guide's explicitly named **"Copilot environments"** concept under approved-version environments: a service is deployed independently into each environment via `copilot deploy --env <name>`, giving clean separation between dev/test/prod without the team manually provisioning parallel infrastructure by hand each time.

### 4.4 Pipelines
`copilot pipeline init` (backed by CodePipeline and CodeBuild, tying directly into module 10's CI/CD material) sets up an automated promotion pipeline: a commit to your source repo triggers a build (Docker image build + push to ECR), then automatically deploys through your environments in order (e.g., `test` → `staging` → `prod`), optionally requiring manual approval gates between stages. This gives containerized services the same "approved-version environment" promotion story that Amplify branches and Lambda aliases give their respective compute models — the exam's Domain 3.3 grouping isn't a coincidence; all four (Lambda aliases, container image tags, Amplify branches, Copilot environments) are the same underlying pattern — a named, stable pointer to a specific approved build — expressed differently per compute type.

## 5. Choosing the right abstraction — comparison table

| | Elastic Beanstalk | Amplify | Copilot | Raw CloudFormation / SAM / CDK |
|---|---|---|---|---|
| **Target app shape** | Traditional web apps/APIs on EC2 (Java, Node, Python, .NET, Docker, etc.) | Frontend-heavy web/mobile apps needing a Cognito+AppSync+S3-style backend | Containerized microservices on ECS/Fargate or App Runner | Anything — no assumptions about app shape |
| **Underlying compute** | EC2 (ASG + ELB), optional RDS | Static/SSR hosting (frontend) + Lambda/AppSync/Cognito (backend) | ECS Fargate tasks, or App Runner | Whatever you declare |
| **Abstraction level** | Medium — resources are provisioned for you but fully inspectable/tunable | High for the backend categories (Auth/API/Storage); high for hosting/CI | Medium — CFN generated for you, service concepts exposed via manifest | Low — you author every resource explicitly |
| **Best-fit team profile** | Teams wanting fast EC2-based deploys with some ops comfort/visibility, not ready for containers or full serverless | Frontend/mobile teams without dedicated backend engineers, wanting managed auth/API/storage and instant Git-based hosting | Platform/backend teams already committed to containers who want ECS without hand-writing CFN | Teams needing full architectural control, complex/custom resource graphs, or resources no higher-level tool models yet |
| **IaC visibility** | Environment config visible/editable via console, CLI, `.ebextensions` | Backend resources are CFN stacks under the hood, mostly abstracted away by the CLI/Studio | CFN generated and managed by Copilot, visible via `copilot svc show`/`copilot app show` | Full and explicit — you own every template line |
| **CI/CD story** | `eb deploy` from any pipeline; console/CLI/CI parity | Amplify Hosting has CI/CD built in per branch; `amplify push` for backend | `copilot pipeline init` wires CodePipeline automatically | You build the pipeline yourself (module 10 tools) |
| **When to reach for it** | "Deploy this app quickly, but let us tune the instance type/scaling/health checks later" | "We're a frontend team, give us auth/API/storage and hosting without backend engineers" | "We're already on containers, stop making us hand-write ECS CloudFormation" | "This doesn't fit any higher-level tool's model, or we need precise control over every resource" |

**Exam trap:** none of these four tools is strictly "better" than the others — the exam almost always frames the choice around the *team's* starting shape (existing EC2 app vs. frontend team vs. containerized microservices team vs. bespoke architecture), not around performance or cost. Picking Copilot for a team with no container images yet, or Amplify for a backend-heavy service with no real frontend, is a classic wrong-answer pattern.

## 6. Worked real-world scenarios

**Scenario A — the EC2 monolith that needs zero-downtime deploys and a background job.** A team is migrating a Node.js monolith off a hand-managed EC2 instance. They want fast, low-effort deploys, the ability to occasionally SSH in to debug, and a separate background worker that processes image-resizing jobs off a queue without being publicly reachable. They set up two Elastic Beanstalk environments in the same application: a **web server tier** environment for the public API (with an `.ebextensions/01-environment.config` setting `NODE_ENV` and tuning the ASG's min/max size), and a **worker tier** environment pointed at an SQS queue for the image-resizing jobs (Beanstalk provisions the queue automatically and the worker daemon polls it, posting each message to a local HTTP endpoint the app exposes). For deploys to the web tier, they choose **rolling with additional batch** so capacity never dips during business hours; for a major version bump they're nervous about, they instead spin up a parallel environment and use a **CNAME swap** for instant, safe cutover with instant rollback if metrics look wrong. **Lesson:** web vs. worker tier is a real architectural choice, not a checkbox — the worker tier is what turns "SQS + EC2" from something you'd build by hand into a managed pattern.

**Scenario B — the frontend team without backend engineers.** A startup's frontend team is building a customer-facing React app and needs authentication, a GraphQL API, and file uploads, but has no backend engineers and a tight deadline. They use `amplify add auth` (provisions Cognito), `amplify add api` (provisions AppSync + DynamoDB), and `amplify add storage` (provisions S3), then `amplify push` to deploy all of it as CloudFormation stacks they never had to write. The frontend calls these through the **Amplify libraries'** `Auth`, `API`, and `Storage` categories, which handle token refresh and signed requests automatically. For hosting, they connect their GitHub repo to **Amplify Hosting**: pushes to `main` deploy to the production URL, pushes to `develop` deploy to a completely separate, independently testable environment at its own URL, and every pull request gets an automatic preview deployment reviewers can click through before approving. **Lesson:** Amplify's value here isn't any single service — it's that a frontend-only team gets a working, isolated-per-branch backend and hosting pipeline without ever provisioning infrastructure by hand.

**Scenario C — the platform team standardizing on containers.** A platform team is migrating a set of microservices to ECS Fargate and wants consistent `dev` → `staging` → `prod` promotion without every service team hand-writing CloudFormation for task definitions, services, and load balancers. They standardize on Copilot: each service gets a `manifest.yml` declaring it as a **Load Balanced Web Service** with autoscaling bounds and a health check path, `copilot env init` creates isolated `dev`, `staging`, and `prod` **environments** (separate VPCs/clusters), and `copilot pipeline init` wires a CodePipeline that builds each service's Docker image, pushes it to ECR, and promotes it through the three environments with a manual approval gate before `prod`. A service-specific override in the manifest's `environments: prod:` block bumps `prod` to a higher instance count and different log level than `dev`/`staging` without duplicating the whole manifest. **Lesson:** Copilot environments give containerized services the same "promote a specific, approved build through named stages" story that EB application versions and Amplify branches give their respective compute models — it's the same underlying pattern (a stable, named pointer to an approved build) the exam groups together under Domain 3.3.

## Key exam traps

- EB's **worker tier** (not web server tier) is the answer whenever a scenario describes background processing off an SQS queue with no direct public traffic — Beanstalk provisions the queue and polling daemon for you.
- Deployment policy nuance: **rolling with additional batch** is the one that maintains full capacity throughout (at extra temporary cost); plain **rolling** briefly reduces capacity; **all at once** has full downtime risk but is fastest; **immutable** (and environment-swap blue/green) give the safest, fastest rollback at the highest temporary resource cost.
- Blue/green in Beanstalk is a **CNAME swap between two separate environments**, not one of the four same-environment deployment-policy dropdown options — know the distinction if a question tests it precisely.
- `.ebextensions` config files can embed a real CloudFormation `Resources:` section — Beanstalk environments are still CloudFormation-backed under the hood, same as Amplify and Copilot.
- Application version lifecycle policies matter for teams deploying frequently via CI/CD — without one, you can hit the per-region application version quota.
- The exam guide's exact phrase **"Amplify branches"** maps to Amplify Hosting's Git-branch-per-environment model — memorize this pairing, it's directly testable.
- The exam guide's exact phrase **"Copilot environments"** maps to named, isolated deployment targets (`dev`/`test`/`prod`) each with their own infrastructure — memorize this pairing too.
- Lambda aliases, container image tags, Amplify branches, and Copilot environments are grouped together in the official exam guide as the same underlying concept — a stable, named pointer to an approved build — expressed per compute model. Recognizing this pattern helps on scenario questions that swap the compute type but ask the same underlying "how do you promote a tested build to production safely" question.
- None of EB/Amplify/Copilot is a universally "better" choice — the exam frames the decision around the **team's existing shape and app type** (EC2-comfortable team vs. frontend-only team vs. container-committed team), not around raw performance. When a scenario doesn't fit any of the three cleanly, raw CloudFormation/SAM/CDK (module 13) is the correct fallback answer, not forcing a mismatched higher-level tool.
- All three tools ultimately provision standard, inspectable AWS resources — none of them is "not real AWS" or a black box you should distrust on the exam; the difference is authoring convenience, not the resulting infrastructure.
