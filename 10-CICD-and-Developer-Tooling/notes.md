# Module 10 — CI/CD & Developer Tooling

Domain focus: **Deployment (24%)** — this module covers Domain 3 Task Statement 1 ("prepare artifacts for deployment") and Task Statement 4 ("deploy code using AWS CI/CD services") almost in their entirety, plus AWS AppConfig, which straddles Development and Deployment. If Module 00 told you CI/CD *pipeline design* is out of scope, this module is the flip side: *using* an existing pipeline — reading a buildspec, wiring a deployment group, choosing a traffic-shifting strategy, configuring a rollback — is squarely, heavily in scope. Expect several questions per exam sitting from this module alone.

## 1. The AWS CI/CD service family, at a glance

AWS's native CI/CD toolchain is a set of loosely-coupled, single-purpose services that compose into a pipeline. Knowing what each one does — and, just as importantly, what it does *not* do — is the foundation for everything else here.

| Service | Role | Analogous to |
|---|---|---|
| **CodeCommit** | Managed Git source repository | GitHub/GitLab (hosting only) |
| **CodeBuild** | Compiles source, runs tests, produces build artifacts | Jenkins/CircleCI (build step) |
| **CodeDeploy** | Deploys built artifacts to compute (EC2, on-prem, Lambda, ECS) | A deployment/release tool |
| **CodePipeline** | Orchestrates the stages above into an end-to-end release workflow | The overall CI/CD orchestrator |
| **CodeArtifact** | Managed package repository (npm, pip, Maven, NuGet) | Artifactory/Nexus |
| **CodeStar** | (Largely superseded) unified project dashboard wrapping the above | A project template/dashboard |
| **AppConfig** | Deploys *application configuration and feature flags*, separately from code | LaunchDarkly-style feature flagging |

The mental model that ties them together: **CodeCommit holds the code → CodePipeline watches it and orchestrates → CodeBuild turns source into a tested artifact → CodeDeploy pushes that artifact onto compute → CodeArtifact supplies the dependencies CodeBuild needs along the way.** AppConfig is deliberately separate from this chain — it changes *configuration* without a code deployment at all.

## 2. AWS CodeCommit

A fully-managed, private Git repository service. Under the hood it's just Git — any Git client, any Git workflow (feature branches, pull requests, merge/rebase) works unmodified.

- **Access control is 100% IAM** — there's no separate CodeCommit user system. You grant `codecommit:GitPull`, `codecommit:GitPush`, etc. via IAM policies, same as any other AWS API action.
- **Two ways to authenticate a Git client:**
  - **HTTPS Git credentials** — IAM generates a username/password pair specifically for Git operations (distinct from console password and access keys), used with a standard Git HTTPS remote.
  - **SSH keys** — you upload a public SSH key to your IAM user, then push/pull via `ssh://` remote URLs.
  - (A third option, **git-remote-codecommit**, uses your existing IAM credentials/roles directly without managing separate Git credentials — handy for CI runners already running under an IAM role.)
- **Branches, tags, pull requests, and approval rule templates** all work as you'd expect from any hosted Git service; CodeCommit supports approval rules requiring N approvers before a pull request can merge.
- **Triggers**: CodeCommit can invoke SNS notifications or Lambda functions on repository events (push, branch creation/deletion), and — the pattern you'll actually build — a **CodePipeline source stage** can be configured to trigger automatically on a push to a specific branch via Amazon EventBridge (the modern mechanism; older docs reference CloudWatch Events polling, which still exists but EventBridge is preferred).

**Exam framing:** CodeCommit questions rarely test Git mechanics — they test *IAM-governed access* (who can push/pull, and how credentials are issued) and *triggering a pipeline on commit*. If you see "least operational overhead" plus "the company doesn't want to manage its own Git server," that's CodeCommit (or, increasingly in newer scenarios, a third-party Git provider like GitHub connected via CodeStar Connections/CodeConnections — know that CodePipeline can source from GitHub too, not only CodeCommit).

## 3. AWS CodeBuild

A fully-managed build service: no build servers to provision or patch. You give it source code and a **buildspec.yml**, and it runs the defined phases inside a managed (or custom) container, producing artifacts.

### buildspec.yml structure

```yaml
version: 0.2

env:
  variables:
    NODE_ENV: "production"
  parameter-store:
    DB_HOST: "/myapp/prod/db-host"
  secrets-manager:
    DB_PASSWORD: "myapp/prod/db-credentials:password"

phases:
  install:
    runtime-versions:
      nodejs: 18
    commands:
      - echo "Installing dependencies"
      - npm ci
  pre_build:
    commands:
      - echo "Running lint and unit tests"
      - npm run lint
      - npm test
  build:
    commands:
      - echo "Building application"
      - npm run build
  post_build:
    commands:
      - echo "Build completed on `date`"
      - aws s3 cp build/report.xml s3://my-build-reports-bucket/

artifacts:
  files:
    - '**/*'
  base-directory: 'dist'
  discard-paths: no

cache:
  paths:
    - 'node_modules/**/*'
```

### The four phases (know these by name and purpose)
- **install** — install runtime versions and any global tools needed before dependency resolution (e.g. `runtime-versions` pins Node/Python/Java versions inside the managed image).
- **pre_build** — commands to run *before* the actual build: installing dependencies, logging into a registry, running linters/unit tests.
- **build** — the actual compile/package/transpile commands — this is the phase whose failure most directly means "the build failed."
- **post_build** — cleanup, packaging final artifacts, pushing a Docker image to ECR, sending a notification. Notably, post_build commands still run even if the build phase fails (useful for cleanup/notification), though the overall build is still marked failed.

### Build environments
- **Managed images** — AWS provides preconfigured Docker images per runtime (Ubuntu/Amazon Linux with Node, Python, Java, Go, .NET, Docker-in-Docker, etc.), versioned and patched by AWS.
- **Custom Docker images** — you can point CodeBuild at your own image (in ECR or Docker Hub) when you need dependencies or tooling the managed images don't provide. Requires the image to have basic OS tooling CodeBuild needs to operate.
- **Compute type** — you choose the vCPU/memory class for the build container (general1.small/medium/large, or GPU-enabled classes for specialized builds).
- **Privileged mode** must be enabled if the build needs to run Docker itself (e.g., building and pushing a container image from within the build) — this is a common "why did my Docker build fail in CodeBuild" root cause when unchecked.

### Environment variables and secrets at build time
Three ways to supply values into a build, all shown in the buildspec above:
1. **Plaintext env vars** — fine for non-sensitive config (`NODE_ENV`).
2. **Parameter Store references** — `parameter-store` section pulls values by name at build start; the CodeBuild service role needs `ssm:GetParameters` on that path.
3. **Secrets Manager references** — `secrets-manager` section pulls a secret (optionally a specific JSON key within it, as shown: `myapp/prod/db-credentials:password`); the service role needs `secretsmanager:GetSecretValue`.

**Exam trap:** never put a real secret as a plaintext environment variable directly in the buildspec or in the CodeBuild project's console-configured environment variables — those are visible in the build's environment/logs. The tested best practice is always: reference Secrets Manager or Parameter Store (SecureString), and grant the *service role* least-privilege access to just that secret/parameter path.

### Build artifacts
The `artifacts` section defines what CodeBuild packages up after a successful build and where it lands (an S3 bucket, or handed directly to the next CodePipeline stage as an input artifact). `base-directory` scopes which folder's contents get zipped; `discard-paths: yes` flattens the directory structure in the resulting artifact.

### Caching for build speed
CodeBuild supports two caching approaches:
- **Amazon S3 caching** — CodeBuild uploads/downloads cache contents (e.g., `node_modules`, `.m2` for Maven, pip's cache dir) to/from a specified S3 location between builds. Simple, works everywhere, but has S3 upload/download overhead on every build.
- **Local caching** — caches persist on the build host itself (Docker layer cache, source cache, custom directory cache) for faster reuse, but only helps if CodeBuild happens to reuse the same underlying build host, which isn't guaranteed — so it's a "best-effort" speedup, not a guarantee.
Either way, the exam's angle is simple: **caching dependency directories (`node_modules`, `.m2`, pip cache) is the standard way to cut CodeBuild build times** when a scenario says "the build takes too long because dependencies are re-downloaded every time."

## 4. AWS CodeDeploy

Automates deploying an already-built application revision onto compute — EC2/on-premises instances, Lambda functions, or ECS services. Where CodeBuild answers "how do I turn source into an artifact," CodeDeploy answers "how do I get that artifact running."

### appspec.yml — the deployment instruction file

For **EC2/on-premises** deployments:
```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/html
permissions:
  - object: /var/www/html
    pattern: "**"
    owner: ec2-user
    group: ec2-user
hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
  AfterInstall:
    - location: scripts/change_permissions.sh
      timeout: 300
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 300
  ValidateService:
    - location: scripts/validate_service.sh
      timeout: 300
```

For **Lambda** deployments (structure is different — no `files`/`permissions`, since there's no filesystem to manage):
```yaml
version: 0.0
Resources:
  - myLambdaFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: "my-function"
        Alias: "live"
        CurrentVersion: "3"
        TargetVersion: "4"
Hooks:
  - BeforeAllowTraffic: "validateBeforeTrafficShiftFunction"
  - AfterAllowTraffic: "validateAfterTrafficShiftFunction"
```

### Deployment hooks by compute platform (memorize the ordering — this is directly tested)

**EC2/on-premises, in-place deployment lifecycle event order:**
`ApplicationStop → DownloadBundle → BeforeInstall → Install → AfterInstall → ApplicationStart → ValidateService`
- **BeforeInstall** — typically used for pre-install tasks: decrypting files, backing up the current version.
- **AfterInstall** — configure the application, change file permissions, after files are in place but before it's running.
- **ApplicationStart** — commands needed to start the application (start a service, restart a web server).
- **ValidateService** — the last hook; verify the deployment succeeded (e.g., hit a health endpoint). If this fails, the deployment is marked failed and can trigger rollback.

**Lambda / ECS traffic-shifting hooks (different set, because there's no "install" step in the OS sense):**
- **BeforeAllowTraffic** — runs before traffic starts shifting to the new version; commonly used to run a validation Lambda that checks the new version's health before any real traffic reaches it.
- **AfterAllowTraffic** — runs after all traffic has shifted; used for post-deployment smoke tests or cleanup.

**Exam trap:** don't mix up the two hook sets. If a scenario says "EC2 instance" or "on-premises server," think `BeforeInstall/AfterInstall/ApplicationStart/ValidateService`. If it says "Lambda" or "ECS," think `BeforeAllowTraffic/AfterAllowTraffic`.

### In-place vs. blue/green deployment (EC2/on-premises)
- **In-place** — CodeDeploy stops the app, installs the new revision, restarts it, *on the same instances*, typically batch by batch (this is effectively CodeDeploy's version of a "rolling" deployment for EC2). Downtime per-instance during the update; if it fails partway, you're stuck between versions unless you deploy the previous revision again.
- **Blue/green** — CodeDeploy provisions a brand-new set of instances (the "green" environment) alongside the existing "blue" fleet, deploys the new revision there, optionally runs validation, then reroutes traffic (via an ELB/ALB) from blue to green — either all at once or on a schedule. The original blue fleet is kept around (terminated after a specified wait period), which is what makes **near-instant rollback** possible: just route traffic back to blue.

### Deployment groups
A CodeDeploy **deployment group** ties together: which instances/Lambda alias/ECS service to target (by tag or ASG membership for EC2; by alias for Lambda; by service for ECS), the deployment configuration (traffic-shifting rules, described below), the service role CodeDeploy assumes to make changes, and — critically — the **CloudWatch alarms and automatic rollback configuration** for that group.

### Automatic rollback
A deployment group can be configured to automatically roll back on:
- **Deployment failure** — any lifecycle hook script returns a non-zero exit code, or the deployment doesn't finish within its window.
- **A CloudWatch alarm going into ALARM state** during or shortly after deployment (e.g., an alarm on elevated 5xx rate or error count).
Rollback works by **redeploying the last known-good revision** as a new deployment (for in-place) or, for blue/green, simply routing traffic back to the still-running blue environment — which is why blue/green rollback is typically much faster than an in-place rollback.

## 5. Deployment strategies in depth (heavily tested — this is the section to know cold)

This is one of the highest-yield topics on the whole exam. AWS names these strategies slightly differently depending on the compute platform, but the underlying concepts are universal.

| Strategy | Mechanism | Typical use | Rollback behavior |
|---|---|---|---|
| **Canary** | Shift a small, fixed percentage of traffic (e.g., 10%) to the new version, wait/"bake" for a specified time to observe metrics, then shift the remaining 90% all at once if healthy | Lambda (`CodeDeployDefault.LambdaCanary10Percent5Minutes`), API Gateway stage/canary release, ECS | Fast — if the alarm trips during the bake window, traffic is routed back to the original version before the bulk of users ever see the new one; blast radius during the canary phase is small |
| **Linear** | Shift traffic in equal-sized increments on a fixed schedule (e.g., 10% every 1 minute until 100%) | Lambda (`CodeDeployDefault.LambdaLinear10PercentEvery1Minute`), ECS | Similar to canary — an alarm trip at any increment halts and can roll back, but more of the fleet may have already received traffic compared to a canary's single small initial slice |
| **Blue/green** | Two full, separate environments; traffic cut over from old (blue) to new (green) — all at once or gradually — with the old environment kept warm for a period | EC2/on-premises, ECS, Lambda (blue/green is really the umbrella that canary/linear traffic-shifting live under, for Lambda/ECS) | Fastest and safest — the old environment is untouched and fully running, so rollback is just re-pointing traffic/DNS/target group back to blue; no redeployment needed |
| **Rolling** | Replace instances in batches (e.g., 3 at a time, or 25% of the fleet at a time), in-place, waiting for each batch to succeed before moving to the next | EC2/ASG in-place deployments (`OneAtATime`, `HalfAtATime`, `AllAtOnce` are CodeDeploy's built-in EC2 deployment configs — "rolling" is the general term for the batch-by-batch behavior `OneAtATime`/`HalfAtATime` produce) | Slowest — a failure requires redeploying the previous revision to already-updated batches; some capacity runs the old version and some the new version simultaneously during the rollout, which the application must tolerate |

### Decision framework — how the exam wants you to choose

Ask, in order:
1. **Does the platform even support traffic-shifting?** EC2/on-prem in-place deployments don't get canary/linear — that's a Lambda/ECS (and API Gateway stage) concept, layered on top of blue/green infrastructure. For EC2, your real choice is **in-place (rolling-style) vs. blue/green**.
2. **How fast and safe does rollback need to be, and can you afford double infrastructure cost?** Blue/green gives you the fastest, cleanest rollback (nothing to "undo," just re-route) but costs more because both environments exist simultaneously, even briefly. If the scenario says "minimize risk" or "near-zero downtime rollback," blue/green is usually the answer, cost concerns notwithstanding — unless the scenario *explicitly* flags cost as the binding constraint.
3. **How cautious should the traffic ramp be?** Canary is the most conservative for catching a bad deployment with minimal blast radius (small % first, then all-or-nothing) — favor it when the requirement emphasizes "detect problems before most users are affected." Linear is a good middle ground when you want a steady, observable ramp rather than a single small-then-all jump — favor it when the requirement emphasizes "gradual, controlled rollout" without needing the extra caution of a long canary bake.
4. **Is this EC2 with no ALB/target-group traffic-shifting involved, just in-place updates across a fleet?** Then you're choosing among CodeDeploy's `OneAtATime`, `HalfAtATime`, or `AllAtOnce` EC2 deployment configs — "rolling" behavior — trading rollout speed against how much of the fleet is ever running the old vs. new version at once (and thus how much capacity is preserved if a batch fails healthy).

**Exam trap:** "Blue/green" and "canary" are not mutually exclusive on Lambda/ECS — a canary or linear traffic shift is *how* the cutover from blue to green happens on those platforms. Don't treat them as four totally separate silos; the table above is really "two axes" (whole-environment swap vs. in-place batch, and how the traffic ramp is shaped) that combine differently per compute platform.

## 6. AWS CodePipeline

The orchestrator that ties CodeCommit (or GitHub/S3), CodeBuild, and CodeDeploy (or CloudFormation, ECS, S3, Elastic Beanstalk, and other deploy providers) into a single, automated, multi-stage release process.

### Stage/action structure sketch

```
Pipeline: "my-app-pipeline"
├── Stage: Source
│   └── Action: CodeCommit (or GitHub via CodeStar Connections)
│       — triggers on push to "main"; output artifact = SourceOutput
├── Stage: Build
│   └── Action: CodeBuild
│       — input artifact = SourceOutput; runs buildspec.yml
│       — output artifact = BuildOutput
├── Stage: Test
│   ├── Action: CodeBuild (unit/integration tests)      ┐
│   └── Action: Third-party security scan                ┘ run in parallel (same run order)
├── Stage: DeployToStaging
│   └── Action: CodeDeploy → staging deployment group
├── Stage: ManualApproval
│   └── Action: Manual Approval
│       — publishes to an SNS topic notifying approvers
│       — pipeline execution pauses here until approved/rejected
└── Stage: DeployToProduction
    └── Action: CodeDeploy → production deployment group
        — deployment strategy: canary/linear/blue-green per CodeDeploy deployment config
```

Key structural facts:
- A pipeline is made of **stages**, executed sequentially; each stage contains one or more **actions**.
- **Actions within the same stage can run in parallel** if you give them the same "run order" number — useful for running unit tests and a security scan side by side rather than serially, cutting overall pipeline time.
- Every action consumes **input artifacts** and (usually) produces **output artifacts**, passed via an S3 bucket CodePipeline manages — this is *how* the built zip from CodeBuild actually reaches the CodeDeploy action downstream.
- **Manual approval actions** pause the pipeline until a human approves or rejects, typically wired to publish an **SNS notification** so approvers know a gate is waiting. This is the standard, exam-favored pattern for "require a human sign-off before deploying to production."
- **Triggering**: a pipeline's source stage is triggered automatically (via EventBridge rule under the hood) whenever a new commit lands on the watched branch of the source repo — no polling required in the modern setup, though CodePipeline still supports polling as a legacy option.
- **Cross-region pipelines**: a single pipeline can deploy to multiple AWS Regions — CodePipeline automatically replicates artifacts to a bucket in each target Region for you when you configure a cross-region action.
- **Cross-account pipelines**: a pipeline in Account A can deploy into Account B by using a cross-account IAM role in Account B (assumed via `sts:AssumeRole`) plus a KMS key policy that permits the pipeline's role to use the artifact-bucket encryption key — the same cross-account role pattern from Module 00, just applied to a pipeline action.
- **Stage transitions can be manually disabled** (e.g., freeze deployments to production during an incident) without touching the pipeline definition itself.

## 7. AWS CodeArtifact

A fully-managed artifact/package repository for your team's private packages and as a caching proxy in front of public registries (npm's registry, PyPI, Maven Central, NuGet.org).

- **Domains and repositories**: a **domain** is an organizational container that can hold multiple **repositories**; packages and their metadata are deduplicated and share security configuration at the domain level, simplifying permission management across many repos.
- **Upstream repositories**: a CodeArtifact repository can be configured with an **upstream** — either another CodeArtifact repository or a supported *external connection* (npmjs, PyPI, Maven Central, NuGet Gallery). When a package isn't already cached locally, CodeArtifact fetches it from the upstream automatically and caches it for future requests — this is what gives you both **private package hosting** and **faster, more resilient public dependency resolution** (protection against a public registry outage or an accidentally-deleted public package) from a single tool.
- **Authentication**: clients authenticate using a short-lived authorization token obtained via `aws codeartifact get-authorization-token`, which the CLI/build tooling then hands to `npm`, `pip`, `mvn`, etc. as a standard registry credential — governed by IAM the same as everything else.

### Using CodeArtifact from a CodeBuild buildspec

```yaml
version: 0.2
phases:
  install:
    commands:
      - aws codeartifact login --tool npm --domain my-domain --domain-owner 111122223333 --repository my-npm-repo
  pre_build:
    commands:
      - npm ci   # resolves against the CodeArtifact repo, not npmjs.org directly
```

`aws codeartifact login` is a convenience wrapper that fetches the auth token and configures the tool's config file (`.npmrc`, `pip.conf`, `settings.xml`) to point at the CodeArtifact repository endpoint — the CodeBuild service role needs `codeartifact:GetAuthorizationToken` and related repository-read permissions.

**Exam framing:** CodeArtifact questions usually center on *why* a company would front public package registries with it — reproducible builds immune to an upstream registry's outage/deletion, centralized vulnerability/version control over what versions of a dependency the org allows, and hosting genuinely private internal packages, all through one IAM-governed endpoint instead of scattered `.npmrc` tokens.

## 8. AWS CodeStar (brief — largely superseded, but still an exam term)

CodeStar was AWS's earlier attempt at a **unified project-management console** that provisioned a CodeCommit repo, a CodeBuild project, a CodeDeploy deployment, and a CodePipeline pipeline together from a project template, plus a basic dashboard and issue tracking. **AWS's newer guidance steers customers toward composing CodeCommit/CodeBuild/CodeDeploy/CodePipeline directly** (or using the CDK/SAM/Amplify for scaffolding), and CodeStar is not actively pushed for new projects. For the exam: know that CodeStar's role was as a **project-template wrapper/dashboard around the other Code* services**, not a distinct deployment engine of its own — if you see it in an answer option, mentally translate it to "the same underlying services, just project-scaffolded together." Don't expect deep mechanical questions on it.

## 9. AWS AppConfig — configuration and feature flags, decoupled from code deployment

AppConfig deploys **application configuration** (feature flags, operational parameters, allow/deny lists, free-form config data) to running applications **without requiring a code deployment or a restart** — this is the single most important distinction to hold onto: a CodeDeploy/CodePipeline release changes *code*; AppConfig changes *behavior/configuration* on top of code that's already running.

### Core concepts
- **Application** — a logical namespace (usually matching a real application).
- **Configuration profile** — a pointer to where the configuration data actually lives (a free-form JSON/YAML/text document you author, or a feature-flag-specific profile), plus an optional **validator**.
- **Environment** — a logical deployment target (e.g., beta, prod) that can have its own monitors/alarms attached.
- **Deployment strategy** — controls *how fast* a configuration change rolls out to the fleet, using the same conceptual shapes as code deployment strategies: a percentage grows over time (deployment time), with a **bake time** afterward to watch for problems before considering the deployment fully complete. AWS ships predefined strategies like `AppConfig.Linear50PercentEvery30Seconds` and `AppConfig.AllAtOnce`, or you define a custom one — this is conceptually the linear/canary idea applied to config rather than code.
- **Validators** — a JSON Schema or a Lambda function that validates a new configuration value *before* it's allowed to deploy, catching a malformed config before it reaches production (e.g., reject a config that sets a numeric timeout to a negative value).
- **Automatic rollback on alarm** — exactly like CodeDeploy, an AppConfig deployment can be tied to a CloudWatch alarm; if the alarm trips during rollout, AppConfig halts and rolls the configuration back to the prior known-good value automatically.

### Fetching configuration fast: the Lambda extension
Calling the AppConfig API directly on every request would add latency and cost. For Lambda specifically, AWS provides the **AppConfig Lambda extension** — a Lambda layer that runs alongside your function, caches the current configuration locally, and serves it to your function code over `localhost` with negligible latency, refreshing in the background on a poll interval. This is the exam's preferred answer whenever a scenario says "a Lambda function needs to check a feature flag on every invocation without adding significant latency."

**Exam trap:** don't confuse AppConfig with Parameter Store. Parameter Store is a generic key-value config/secrets store you read directly (no built-in staged rollout, no validators, no bake-time/alarm-based auto-rollback of a config change). AppConfig is purpose-built for **safely, gradually rolling out a configuration or feature-flag change to a fleet, with the same staged-rollout-and-rollback safety net CodeDeploy gives you for code** — that's the differentiator the exam tests.

## 10. Worked real-world scenarios

**Scenario A — building the full pipeline with a manual approval gate before production.**
A company runs a Node.js API and wants every merge to `main` in their CodeCommit repository to automatically build, test, deploy to a staging environment, and then wait for a release manager's sign-off before touching production. The pipeline: (1) **Source stage** — CodePipeline's CodeCommit source action watches the `main` branch, triggered via EventBridge on push, producing a `SourceOutput` artifact (the zipped repo contents). (2) **Build stage** — a CodeBuild action consumes `SourceOutput`, runs a buildspec with `install`/`pre_build` (npm ci, lint, unit tests)/`build` (webpack bundle)/`post_build` (zip the bundle) phases, and produces a `BuildOutput` artifact. (3) **DeployStaging stage** — a CodeDeploy action deploys `BuildOutput` to the staging deployment group, using an in-place `AllAtOnce` config since staging doesn't need careful traffic shifting. (4) **Approval stage** — a Manual Approval action publishes to an SNS topic the release managers are subscribed to; the pipeline execution literally pauses here, showing "in progress" indefinitely until someone approves or rejects it in the console (or via the API). (5) **DeployProd stage** — only runs after approval, another CodeDeploy action targeting the production deployment group, this time configured for blue/green with a CloudWatch alarm on 5xx rate wired to automatic rollback. **Why this shape:** it satisfies "automate everything that's safe to automate" (source through staging) while keeping a deliberate human gate exactly where the blast radius is highest (production), with the alarm-based rollback as a second automated safety net even after human approval.

**Scenario B — canary deployment for a Lambda-based payments API.**
A fintech company's payments-processing logic runs as a Lambda function behind API Gateway. Deployment mistakes here are expensive (financial, reputational), so "deploy the new version to everyone at once" is unacceptable, but so is a deployment process slow enough to leave the team unable to ship fixes quickly. The team configures CodeDeploy with `CodeDeployDefault.LambdaCanary10Percent5Minutes`: the new Lambda version's alias receives 10% of invocations immediately, CodeDeploy waits 5 minutes while a CloudWatch alarm watches the function's error rate, and — if the alarm never trips — automatically shifts the remaining 90% to the new version. The appspec.yml's `BeforeAllowTraffic` hook runs a small validation Lambda that calls a synthetic test transaction against the new version before *any* real customer traffic reaches it; `AfterAllowTraffic` runs a broader smoke-test suite once 100% of traffic has shifted. If the error-rate alarm trips at any point during the 5-minute bake, CodeDeploy automatically shifts all traffic back to the previous version's alias — no redeploy needed, because the old version's Lambda code was never removed, only de-weighted. **Why canary specifically, not linear or blue/green:** the requirement is "catch a bad deployment while it's only affecting a small slice of customers," which is exactly canary's design point — a small fixed exposure window before the big jump, rather than linear's steadier-but-longer ramp or an EC2-style full-environment swap that doesn't apply to Lambda's execution model in the first place.

**Scenario C — decoupling a feature flag from a deployment using AppConfig.**
A retail company wants to launch a new checkout flow to 5% of users initially, watch conversion and error metrics, then ramp to 100% over the following day — without redeploying any code, because the feature flag check is already built into the currently-running application code (an `if (featureFlags.newCheckout) {...}` branch reading from AppConfig on each relevant request via the Lambda extension for low latency). They create an AppConfig configuration profile for a JSON document containing `{"newCheckoutEnabled": true}`, attach a validator (a Lambda function confirming the JSON is well-formed and the flag is boolean), and deploy it to the "prod" environment using the `AppConfig.Linear10PercentEvery1Hour` deployment strategy with a CloudWatch alarm on checkout error rate and cart-abandonment spikes wired for automatic rollback. Ten hours later, exposure is at 100% with the alarm never having tripped, so the change is complete — and if it *had* tripped at, say, hour 3 (30% exposure), AppConfig would have automatically reverted every fetching client back to `newCheckoutEnabled: false` without anyone touching CodeDeploy, CodePipeline, or redeploying a single line of Lambda code. **Why AppConfig instead of CodeDeploy/CodePipeline here:** the thing changing is a runtime toggle already present in already-deployed code, not the code itself — exactly the boundary the exam wants you to recognize between "deploying an artifact" (CodeDeploy's job) and "changing configuration/feature-flag state safely" (AppConfig's job), even though both use a strikingly similar staged-rollout-plus-alarm-rollback safety model.

## 11. Domain 3 task-statement mapping (how this module lines up with the exam guide)

- **Task Statement 1 (prepare artifacts for deployment)**: covered here via CodeCommit (source/versioning), CodeBuild (packaging Lambda deployment zips/container images, resolving dependencies via CodeArtifact), and application configuration/secrets access patterns (Parameter Store/Secrets Manager references inside a buildspec, AppConfig for runtime config). Managing dependencies specifically maps to CodeArtifact's upstream-repository caching model.
- **Task Statement 4 (deploy code using AWS CI/CD services)**: covered via CodePipeline's stage/approval/trigger model, CodeDeploy's deployment strategies and rollback mechanics, and dynamic-deploy concepts like Lambda aliases/versions and API Gateway stage variables (a stage variable can point a given API Gateway stage at a specific Lambda alias, letting you route a `beta` stage's traffic at a `beta` alias independently of what `prod` points at — the API Gateway-side analog of a CodeDeploy traffic shift).

## Comparison table — the four deployment strategies (quick reference)

| Strategy | Traffic shift shape | Platforms | Speed to full rollout | Rollback speed/mechanism |
|---|---|---|---|---|
| Canary | Small % first, bake, then rest all at once | Lambda, ECS (also API Gateway canary release stages) | Slower than linear at first (bake time), then instant jump | Fast — only a small % was ever exposed; alarm trip during bake reroutes traffic back before the bulk shift |
| Linear | Equal increments on a fixed schedule | Lambda, ECS | Steady, predictable pace across the whole window | Moderate — depends how far along the ramp was when the alarm tripped; more of the fleet may have already seen the new version than in a canary's initial slice |
| Blue/green | Full second environment; traffic cut over (all at once or gradually) then old env retired | EC2/on-prem, ECS, Lambda (as the umbrella traffic-shift model) | Fast — new environment is fully live before any traffic moves | Fastest — just re-point traffic/target group back to the still-running blue environment; no redeploy |
| Rolling | Batch-by-batch in-place replacement (OneAtATime/HalfAtATime/etc.) | EC2/on-prem (in-place), ASG instance refresh | Depends on batch size — smaller batches are slower but safer | Slowest — must redeploy the previous revision to already-updated batches; mixed old/new versions coexist mid-rollout |

## Key exam traps
- EC2/on-prem CodeDeploy hooks are `BeforeInstall/AfterInstall/ApplicationStart/ValidateService`; Lambda/ECS hooks are `BeforeAllowTraffic/AfterAllowTraffic` — don't mix the two sets up when the scenario names the compute platform.
- Canary and linear are traffic-shifting *shapes* layered on top of blue/green-style dual-environment infrastructure for Lambda/ECS — they aren't a separate fourth category unrelated to blue/green.
- Blue/green gives the fastest, simplest rollback (re-point traffic) at the cost of running two environments briefly; rolling/in-place is cheapest but slowest to roll back and risks mixed-version coexistence mid-deployment.
- Never put a real secret as a plaintext CodeBuild environment variable — reference Secrets Manager or Parameter Store SecureString from the buildspec instead, and scope the CodeBuild service role to just that secret.
- Manual approval actions in CodePipeline are the standard "human sign-off before prod" pattern, typically paired with an SNS notification so approvers actually know a gate is waiting.
- CodeDeploy automatic rollback triggers on deployment failure OR a CloudWatch alarm going into ALARM state — a scenario needing "automatically undo a bad deploy" almost always wants an alarm wired to the deployment group, not a person watching a dashboard.
- AppConfig changes runtime configuration/feature flags without a code deployment; CodeDeploy/CodePipeline change the deployed code/artifact itself — don't reach for CodeDeploy when the scenario is really describing a feature-flag rollout.
- Parameter Store has no native staged-rollout-with-alarm-rollback for configuration changes; AppConfig does — that's the deciding detail whenever a scenario asks for a *safely, gradually rolled out* config or flag change.
- CodeArtifact's upstream mechanism gives you both private package hosting and a caching, more resilient front-end for public registries (npm, PyPI, Maven, NuGet) from one IAM-governed endpoint — favor it whenever a scenario mentions dependency reliability, reproducibility, or centralizing approved package versions.
- CodeStar is a project-scaffolding/dashboard wrapper around the other Code* services, not a distinct deployment engine — treat it as a thin, largely-superseded layer if it appears as an answer option.
- "Least operational overhead" for build/deploy scenarios almost always points toward the managed AWS Code* service over a self-hosted Jenkins/build-server alternative, mirroring the same phrase's effect in Module 01's EC2-vs-managed-compute decisions.
