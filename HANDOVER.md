# Handover — AWS DVA-C02 Prep Repo (continuing in a new AI session)

This repo is being handed off from a Claude session to a different assistant (Gemini). This file is the complete brief: what the project is, what's already done, the exact quality bar to match, and precisely what's left. Read this whole file before writing anything. Don't re-research the exam from scratch — everything you need is captured below.

## 1. What this project is

A complete, self-contained study system for the **AWS Certified Developer – Associate (DVA-C02)** exam, built for a beginner doing a 10-day study sprint. Every module folder has exactly three files:
- `notes.md` — thorough, beginner-safe explanation of the topic
- `questions.md` — 110+ scenario-style practice questions with an answer key
- `quiz.html` — a self-contained, interactive, self-grading HTML version of the same questions (no build step, no server — opens directly in a browser)

**Non-negotiable ground rules the user has stated explicitly, twice:**
1. **Do not skip or compress any topic** to fit the 10-day schedule. The schedule flexes; the syllabus doesn't.
2. **Match the depth and question style of the reference modules** (00 and 01, detailed below) — the very first draft of this repo was rejected by the user for being too shallow (short bullet notes, one-line trivia questions) compared to real DVA-C02 prep material. This got fixed by grounding everything in AWS's *official* exam guide and *official* sample questions instead of generating from general knowledge. That research is reproduced in full below — use it directly, don't skip it or re-derive it more loosely.

**Also important — a git incident happened on this repo already, read this before touching git:** a background agent working on this repo previously ran `git init`/`git remote add`/`git push` inside a nested folder without being asked, which turned out to be fine because the user had actually set this up themselves for backup/persistence (repo: `git@github.com:manas-narkhede/aws-dev-certification.git`, this folder). The repo is correctly configured now — `origin` points at that URL, `main` is tracked, working tree is clean. **Do not run `git init` again, do not add a different remote, and never force-push.** Just `git add -A && git commit -m "..." && git push` as you complete work, on top of the existing history. If you want to check status first: `git log --oneline`, `git status`.

## 2. Official AWS exam guide — reference data (fetched directly from AWS, don't skip this)

**Format:** 65 questions (50 scored + 15 unscored, indistinguishable), 130 minutes. Scaled score 100–1000, pass at 720. Multiple choice (1 correct of 4) and multiple response (2+ correct of 5+, marked "(Select TWO)" etc.).

**Explicitly OUT of scope** (don't over-build these): designing architectures/distributed systems/DB schemas from scratch, designing/creating CI/CD pipelines (using one is in scope), administering IAM users/groups, administering servers/OS, designing VPC/networking infrastructure.

### Domain weights & task statements
- **Domain 1 — Development with AWS Services (32%)**
  - 1.1 Develop code for applications hosted on AWS: architectural patterns (event-driven, microservices, monolithic, choreography, orchestration, fanout), idempotency, stateful vs stateless, tightly vs loosely coupled, fault-tolerant patterns (retry+backoff+jitter, DLQ), sync vs async; skills: resilient app code, building/extending APIs, unit testing (SAM), messaging service code, AWS SDK usage, data streaming.
  - 1.2 Develop code for AWS Lambda: event source mapping, stateless apps, unit testing, event-driven architecture, scalability, VPC private-resource access; skills: configuring functions (env vars, memory, concurrency, timeout, runtime, handler, layers, extensions, triggers, destinations), event/error lifecycle handling (Destinations, DLQ), testing, integration with other services, performance tuning.
  - 1.3 Use data stores in application development: relational vs non-relational, CRUD, high-cardinality partition keys, storage options, consistency models, query vs scan, DynamoDB keys/indexing, caching strategies (write-through, read-through, lazy loading, TTL), S3 tiers/lifecycle, ephemeral vs persistent storage; skills: serialization, data lifecycle management, caching services.
- **Domain 2 — Security (26%)**
  - 2.1 Authn/authz: identity federation (SAML, OIDC, Cognito), bearer tokens (JWT, OAuth, STS), Cognito user pools vs identity pools, resource/service/principal policies, RBAC, ACLs, least privilege, AWS-managed vs customer-managed policies; skills: federated access, securing apps with bearer tokens, programmatic access, assuming roles, defining principal permissions.
  - 2.2 Encryption: at rest/in transit, ACM + ACM Private CA, key rotation, client-side vs server-side encryption, AWS-managed vs customer-managed KMS keys; skills: encrypt/decrypt with keys, generating certs/SSH keys, cross-account encryption, enabling/disabling rotation.
  - 2.3 Sensitive data in app code: data classification (PII/PHI), env vars, Secrets Manager/Parameter Store, secure credential handling; skills: encrypting env vars, using secret services, sanitizing sensitive data.
- **Domain 3 — Deployment (24%)**
  - 3.1 Prepare artifacts: app config access (AppConfig, Secrets Manager, Parameter Store), Lambda packaging/layers, Git/CodeCommit, container images; skills: managing code-module dependencies, directory structure, using repos, applying resource requirements.
  - 3.2 Test in dev environments: deployment-performing service features, integration testing with mock endpoints, Lambda versions/aliases; skills: testing via AWS tools, mock API integration, dev endpoints (API Gateway stages), deploying stack updates.
  - 3.3 Automate deployment testing: API Gateway stages, CI/CD branches/actions, automated testing; skills: test events, deploying API resources per environment, approved-version environments (Lambda aliases, container image tags, Amplify branches, Copilot environments), IaC deployment (SAM/CloudFormation), per-service environment management.
  - 3.4 Deploy via AWS CI/CD services: Git/CodeCommit, CodePipeline manual/automated approvals, AppConfig/Secrets Manager config access, CI/CD workflows, deployment tooling (CloudFormation, CDK, SAM, CodeArtifact, Copilot, Amplify, Lambda), Lambda packaging options, API Gateway stages/custom domains, deployment strategies (canary, blue/green, rolling); skills: updating IaC templates, managing environments, deploying via strategies, committing code to trigger pipelines, rollbacks, dynamic deploys via stage variables.
- **Domain 4 — Troubleshooting and Optimization (18%)**
  - 4.1 Root cause analysis: logging/monitoring systems, CloudWatch Logs Insights query language, data visualizations, code analysis tools, common HTTP error codes, common SDK exceptions, X-Ray service maps; skills: debugging, interpreting metrics/logs/traces, querying logs, custom metrics (EMF), dashboards, troubleshooting deployment failures via logs.
  - 4.2 Instrument for observability: distributed tracing, logging vs monitoring vs observability, structured logging, app metrics; skills: logging strategy, emitting custom metrics, tracing annotations, alerting, implementing tracing.
  - 4.3 Optimize with AWS services/features: caching, concurrency, messaging (SQS/SNS); skills: profiling app performance, sizing memory/compute, SQS/SNS subscription filter policies, caching by request headers.

### In-scope AWS services (every one must appear in some module — gap-check list)
Analytics: Athena, Kinesis, OpenSearch. Application Integration: AppSync, EventBridge, SNS, SQS, Step Functions. Compute: EC2, Elastic Beanstalk, Lambda, SAM. Containers: Copilot, ECR, ECS, EKS. Database: Aurora, DynamoDB, ElastiCache, MemoryDB for Redis, RDS. Developer Tools: Amplify, Cloud9, CloudShell, CodeArtifact, CodeBuild, CodeCommit, CodeDeploy, CodeGuru, CodePipeline, CodeStar, X-Ray. Management/Governance: AppConfig, CDK, CloudFormation, CloudTrail, CloudWatch (+Logs), CLI, Systems Manager. Networking: API Gateway, CloudFront, ELB, Route 53, VPC. Security: ACM (+Private CA), Cognito, IAM, KMS, Secrets Manager, STS, WAF. Storage: EBS, EFS, S3, S3 Glacier.

### Official sample question calibration (verbatim from AWS's own sample PDF — match this style exactly)
> A company is migrating a legacy application to Amazon EC2 instances. The application uses a user name and password that are stored in the source code to connect to a MySQL database. The company will migrate the database to an Amazon RDS for MySQL DB instance. As part of the migration, the company needs to implement a secure way to store and automatically rotate the database credentials.
> Which solution will meet these requirements?
> A) Store credentials in env vars in an AMI; rotate by replacing the AMI. B) Store in Systems Manager Parameter Store; configure auto-rotation. C) Store in env vars on the EC2 instances; rotate by relaunching. D) Store in Secrets Manager; configure auto-rotation.
> *Answer: D*

> A company is using Amazon API Gateway for its REST APIs in an AWS account. A developer wants to allow only IAM users from another AWS account to access the APIs.
> Which combination of steps should the developer take to meet these requirements? (Select TWO.)
> A) Create an IAM permission policy, attach to each IAM user, set method auth to AWS_IAM, sign requests with SigV4. B) Cognito user pool approach (distractor). C) Cognito identity pool approach (distractor). D) Create a resource policy for the APIs allowing access for each IAM user. E) Cognito authorizer approach (distractor).
> *Answer: A, D*

**Calibration takeaways:** stems are 2–4 sentences of third-person business/technical context ("A developer is...", "A company is..."), a separate bolded question line, 4 options (single-answer) or 5 (multi-response), options are full parallel sentences with one meaningful differentiator, distractors are plausible real AWS terminology — never joke answers. Roughly 20-30% of questions across a module should be multi-response.

## 3. Content standard (what "done" looks like for one module)

**`notes.md`** (~3000-5500 words depending on how much task-statement content the module covers — modules covering a full domain like Security, or two task statements like Lambda, run longer):
- Beginner-safe, assumes earlier modules are known, explains this module's services from scratch
- Explicitly walks through every knowledge/skill sub-bullet from the relevant task statement(s) above — not just service features listed in isolation
- Short realistic code/pseudocode/policy-JSON/CLI/config snippets wherever the task statement implies hands-on skill
- 2-3 worked real-world scenario walkthroughs ("company X needs Y, here's the reasoning")
- Comparison tables vs. adjacent/similar services
- Ends with a "Key exam traps" bullet list

**`questions.md`** — at least 115-130 questions, organized in topic subsections, ending in an "Answer Key & Explanations" section (`N. Letter(s) — 1-2 sentence explanation naming the specific mechanism`, no fabricated doc URLs):
- Every stem 2-4 sentences, ~50-90 words, third person, ending in a separate question line ("Which solution will meet these requirements?" or equivalent)
- 4 options (single) or 5 options marked "(Select TWO)"/"(Select THREE)" (multi) — **aim for ~20-25% multi-response, build this in deliberately**
- Options structurally parallel, plausible AWS terminology, no joke distractors
- Occasional options with short pseudocode/policy snippets where natural

**`quiz.html`** — **do not design a new one.** Open `01-EC2-and-Compute-Basics/quiz.html` in this repo and copy its CSS/HTML/JS **verbatim** as your template — it's a complete, tested, working single-file app (progress saved via `localStorage`, keyboard shortcuts 1-5/A-E, multi-select support, results screen with missed-question review). The only things that change per module:
- `<title>` and the `.eyebrow`/`<h1>` text
- The initial `posNum` text (e.g. "1 / 118")
- `STORAGE_KEY` (use `"aws-dva-quiz-<NN>"`, e.g. `"aws-dva-quiz-03"`)
- The `QUESTIONS` array — transcribe every question from that module's `questions.md` into `{q, o, a, multi, e}` objects: `o` is the options array, `a` is a zero-indexed array of correct option indices, `multi:true` only on multi-response questions, `e` is the explanation.
- Use double-quoted JS strings, escape literal `"` as `\"`, avoid backticks in question/option text, keep any code snippets in options as plain single-line text (not literal multi-line blocks) to keep escaping simple.
- **No publishing step needed** — this is a plain static HTML file. It works by just opening it in a browser (double-click, or any local file server). There's no "Claude Artifact" equivalent to worry about here.

## 4. Current status (verified file-by-file, not just claimed)

| Module | notes.md | questions.md | quiz.html | Notes |
|---|---|---|---|---|
| 00 Exam Overview & Fundamentals | ✅ | ✅ (120 Q) | ✅ | **Complete — the reference standard, read this first** |
| 01 EC2 & Compute Basics | ✅ | ✅ (116 Q) | ✅ | **Complete — the reference standard, read this first** |
| 02 S3 & Storage | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 03 DynamoDB | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 04 App Design Patterns & Lambda | ✅ | ❌ | ❌ | notes.md exists (6500+ words, covers 2 task statements), needs questions.md + quiz.html |
| 05 API Gateway & AppSync | ✅ | ✅ (142 Q) | ❌ | Just needs quiz.html — transcribe from questions.md |
| 06 Messaging, Streaming & Analytics | ✅ | ✅ (134 Q) | ❌ | Just needs quiz.html |
| 07 Step Functions & Orchestration | ✅ | ✅ (125 Q) | ❌ | Just needs quiz.html |
| 08 Relational & In-Memory Databases | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 09 Caching Strategies & Performance | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 10 CI/CD & Developer Tooling | ✅ | ✅ (135 Q) | ❌ | Just needs quiz.html |
| 11 Elastic Beanstalk, Amplify & Copilot | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 12 Containers (ECS/ECR/Fargate/EKS) | ✅ | ✅ (123 Q) | ❌ | Just needs quiz.html |
| 13 IaC (CloudFormation/SAM/CDK) | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 14 Security Deep Dive | ❌ | ❌ | ❌ | **Nothing yet — full domain (26% of exam), see scope below, this is the biggest remaining module** |
| 15 Networking for Developers | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 16 Monitoring, Logging & Observability | ✅ | ❌ | ❌ | notes.md exists, needs questions.md + quiz.html |
| 17 Well-Architected & Exam Strategy | ❌ | ❌ | ❌ | **Nothing yet — capstone/review module, see scope below** |
| 18 Mock Exams | ❌ | ❌ | ❌ | Build last, see section 6 below |

**Root `README.md`** (one level up, in `AWS Certification/`, not inside this git repo) has the schedule/checklist — update its checkboxes as you finish each module.

## 5. Recommended execution order

1. **Fastest wins first**: write `quiz.html` for modules 05, 06, 07, 10, 12 — the content already exists in their `questions.md`, this is pure mechanical transcription into the template. Do these first to lock in that progress.
2. **Finish the notes-only modules**: 02, 03, 04, 08, 09, 11, 13, 15, 16 — for each, **read the existing `notes.md` first** (don't rewrite it) and write `questions.md` + `quiz.html` consistent with what's already there.
3. **Build 14 (Security Deep Dive) from scratch** — all three files. This is the largest remaining module (a full 26%-weighted domain), budget accordingly: target ~5000-6500 word notes.md and 130-150 questions.
4. **Build 17 (Well-Architected & Exam Strategy) from scratch** — all three files. This is a capstone/review module, different in character (see scope below).
5. **Build 18 (Mock Exams) last**, once everything else is done — see section 6.
6. Commit and push after each module (or small batch) completes: `git add -A && git commit -m "feat: add module NN" && git push`.
7. Update the checkboxes in the root `README.md` as you go.

## 6. Per-module scope for everything still needed

*(For modules 02, 03, 04, 08, 09, 11, 13, 15, 16 — the notes.md already covers this scope; use it as the source of truth for what questions.md needs to test. Scope is restated here for the two from-scratch modules and mock exams.)*

**Module 02 — S3 & Storage** (questions.md + quiz.html only): S3 storage classes/tiers, lifecycle policies, versioning, encryption (SSE-S3/KMS/C vs client-side), presigned URLs, multipart upload, event notifications, bucket policies vs ACLs, S3 Glacier retrieval tiers, EBS/EFS/S3 decision framework. Maps to Domain 1.3 + Domain 2.2.

**Module 03 — DynamoDB** (questions.md + quiz.html only): partition/sort keys, high-cardinality key design, GSI vs LSI, Query vs Scan, consistency models, Streams, transactions, DAX, capacity modes, `dynamodb:LeadingKeys` for per-user access. Maps to Domain 1.3 almost entirely.

**Module 04 — App Design Patterns & Lambda** (questions.md + quiz.html only — this notes.md covers TWO task statements, so target 125-140 questions, split into "Architectural Patterns & Resilience" and "Lambda Deep Dive" subsections): architectural patterns (event-driven/microservices/monolithic/choreography/orchestration/fanout), idempotency, stateful/stateless, coupling, retry-with-backoff-and-jitter, DLQs, sync/async — PLUS Lambda event source mapping, configuration (env vars, memory, concurrency, timeout, layers, extensions, destinations), VPC access, tuning. Maps to Domain 1.1 + 1.2 in full.

**Module 08 — Relational & In-Memory Databases** (questions.md + quiz.html only): RDS (Multi-AZ vs Read Replicas, IAM DB auth, RDS Proxy), Aurora (Serverless v2, Global Database), ElastiCache (Redis vs Memcached), MemoryDB for Redis (durable primary DB vs cache — the key distinction to test). Maps to Domain 1.3 + Domain 2.3 (Secrets Manager + RDS credential rotation).

**Module 09 — Caching Strategies & Performance** (questions.md + quiz.html only): write-through/read-through/lazy-loading/TTL caching patterns (include pseudocode-identification questions like the official AWS sample style — "which pseudocode implements lazy loading"), cache invalidation, caching by request headers, concurrency, profiling, Lambda memory/compute sizing. Maps to Domain 1.3 (caching) + Domain 4.3 in full.

**Module 11 — Elastic Beanstalk, Amplify & Copilot** (questions.md + quiz.html only): Beanstalk (web vs worker tier, deployment policies: all-at-once/rolling/immutable/blue-green), Amplify (Hosting, branch-per-environment), Copilot (manifest.yml, environments). Maps to Domain 3.3 ("approved-version environments" — Lambda aliases, container tags, Amplify branches, Copilot environments, verbatim from the exam guide).

**Module 13 — IaC (CloudFormation/SAM/CDK)** (questions.md + quiz.html only): CloudFormation (Parameters/Resources/Outputs, intrinsic functions, change sets, DeletionPolicy, nested stacks, custom resources), SAM (SAM CLI, local testing, `AWS::Serverless::Function`, deploying to different stages), CDK (constructs L1/L2/L3, synth/diff/deploy). Maps to Domain 3.3 + 3.4.

**Module 15 — Networking for Developers** (questions.md + quiz.html only — **stay at developer-usage level, VPC design is explicitly out of scope**): Internet Gateway vs NAT Gateway, VPC Endpoints (Interface vs Gateway — S3/DynamoDB use Gateway), Lambda-in-VPC (ENI, cold starts, why/why-not), Route 53 (Alias vs CNAME, routing policies), CloudFront (OAC, signed URLs). Maps to Domain 1.2's "access of private resources in VPCs from Lambda code."

**Module 16 — Monitoring, Logging & Observability** (questions.md + quiz.html only): CloudWatch (Logs Insights query syntax, EMF, custom metrics, alarms), X-Ray (service maps, annotations vs metadata, sampling), CloudTrail (audit log, management vs data events), CodeGuru (Reviewer + Profiler), structured logging, common HTTP error codes (400/403/404/429/5xx), common SDK exceptions (ThrottlingException, AccessDeniedException, ConditionalCheckFailedException, etc.). Maps to Domain 4.1 + 4.2 in full. Target 122-135 questions.

**Module 14 — Security Deep Dive** (ALL THREE FILES, from scratch — this is the biggest remaining module, covers an entire 26%-weighted domain, all 3 of its task statements):
- notes.md target ~5000-6500 words. Cover: identity federation (SAML/OIDC concepts), bearer tokens (JWT structure, OAuth grant types, STS), Cognito user pools vs identity pools (and how they connect), resource/identity/principal policies (build on module 00's IAM section, don't repeat it), RBAC, ACLs; ACM public certs vs ACM Private CA, key rotation, client-side vs server-side encryption, AWS-managed vs customer-managed KMS keys, envelope encryption (Encrypt/Decrypt/GenerateDataKey); data classification (PII/PHI), Lambda env var encryption, Secrets Manager vs Parameter Store (deepen module 01's comparison — native rotation, RDS rotation templates), sanitizing sensitive data from logs; brief AWS WAF coverage (rate-based rules, common web exploits).
- questions.md target 130-150 questions in 3 subsections matching the 3 task statements (Authn/Authorization, Encryption, Sensitive Data Management), heavy on multi-step "which combination of steps" questions (this domain favors them).
- quiz.html per the standard template.

**Module 17 — Well-Architected & Exam Strategy** (ALL THREE FILES, from scratch — capstone module, different in character):
- notes.md (~3200-4500 words): all six Well-Architected pillars in real depth (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) — for each, core principles + 2-3 concrete examples pulling in services from earlier modules; a "pillar tradeoff" section (Security vs Cost, Reliability vs Cost); detailed exam-day strategy (time budgeting, flag-and-return, handling Select TWO/THREE differently, parsing constraint keywords like "LEAST operational overhead"/"MOST cost-effective"); a cross-module "service selection cheat sheet" mapping requirement phrases to services/modules; an exam-day checklist.
- questions.md (105-120 questions in two parts): ~40 Well-Architected pillar/tradeoff questions, then ~65-80 **integrative** questions that each combine concepts from 2+ different earlier modules (e.g. Lambda concurrency + SQS DLQs, or IAM roles + Secrets Manager) — read like genuinely meaty synthesis questions, not single-fact recall.
- quiz.html per the standard template.

## 7. Module 18 — Mock Exams (build last)

Once every topic module (00-17) has a complete questions.md, assemble two full 65-question timed mock exams:
- `mock-exam-1.md` / `mock-exam-1.html` and `mock-exam-2.md` / `mock-exam-2.html`
- Draw questions from across all 18 modules' question banks (rephrase/adapt rather than copy verbatim, so the mocks feel fresh, not a rerun) at the **real exam's domain weighting**: ~21 questions from Domain 1 topics (32%), ~17 from Domain 2 (26%), ~16 from Domain 3 (24%), ~11 from Domain 4 (18%) — that's 65 total.
- The `.html` versions need a countdown timer (130:00 minutes) in addition to the standard quiz template, plus a final results screen with a **domain-by-domain score breakdown** (not just overall score) so the user knows which domain to restudy.
- Base the timer/countdown addition on the same `01-EC2-and-Compute-Basics/quiz.html` template — add a `setInterval`-based countdown display and an auto-submit-when-time-expires behavior; keep everything else (progress bar, answer feedback, localStorage persistence, multi-select support) the same.

## 8. Final QA checklist before calling this done

- Every module folder 00-17 has all three files, questions.md has ≥110 questions with a matching answer key.
- Every service in the section 2 in-scope list appears in at least one module's notes.md (grep for it if unsure).
- Spot-check a handful of questions per module against the calibration in section 2/3 (word count, third-person framing, Select TWO ratio) — don't just trust a self-reported count.
- Root `README.md` checklist fully ticked.
- `git status` clean, everything committed and pushed.
