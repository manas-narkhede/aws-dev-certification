# AWS Certified Developer – Associate (DVA-C02) — 10-Day Prep

Your one-stop prep set for the **AWS Certified Developer – Associate (DVA-C02)** exam. Grounded directly in AWS's official exam guide and official sample questions (not just general knowledge) — full syllabus, zero shortcuts, built for a 10-day sprint with heavier sessions on the weekend.

## Exam facts
| | |
|---|---|
| Code | DVA-C02 |
| Format | 65 questions (50 scored + 15 unscored, indistinguishable) — multiple choice & multiple response |
| Time | 130 minutes |
| Score | Scaled 100–1000, **pass at 720** |
| Cost | $150 USD |
| Delivery | Pearson VUE (testing center or online proctored) |
| Candidate profile | AWS expects 1+ years hands-on experience — this course closes that gap from a beginner starting point |

**Explicitly out of scope** per AWS's own exam guide (so don't over-study these): designing architectures/distributed systems/DB schemas from scratch, designing/creating CI/CD pipelines (using one is fine), administering IAM users/groups, administering servers/OS, designing VPC/networking infrastructure. This course still touches these lightly where you need to *use* them as a developer, but doesn't go architect-deep.

### Domain weighting
| Domain | Weight | Covered in modules |
|---|---|---|
| 1. Development with AWS Services | 32% | 01–13 |
| 2. Security | 26% | 00, 14 (+ security notes threaded through every module) |
| 3. Deployment | 24% | 10, 11, 12, 13 |
| 4. Troubleshooting and Optimization | 18% | 09, 16 |

## How to use this repo
Each numbered folder is one module and always has the same three files:
- **`notes.md`** — read this first. Thorough, beginner-safe explanation of the topic: how it works, key limits/features, pricing gotchas, comparison tables, worked real-world scenarios, and the traps the exam likes to set.
- **`questions.md`** — 110+ scenario-style practice questions per module, calibrated to AWS's own official sample-question style (multi-sentence business scenarios, not one-line trivia), with an answer key + explanation at the end. Use for offline review, re-reads, and spaced repetition.
- **`quiz.html`** — an interactive, self-grading version of the same questions. Open it (or ask Claude to publish/open it) for instant right/wrong feedback and a running score, including proper multiple-select "(Select TWO)" style questions. Your progress is saved locally in your browser.

Study order: work top-to-bottom by module number — later modules assume you've read the earlier ones (e.g. Lambda notes assume you already know IAM basics from module 00).

`18-Mock-Exams/` holds two full 65-question timed simulations, weighted across domains exactly like the real exam — save these for days 9–10.

## In-scope AWS services (gap-check list)
Every service below is covered in at least one module. If you can't place a service in this list to a module, ask.

| Category | Services | Module(s) |
|---|---|---|
| Analytics | Athena, Kinesis, OpenSearch | 06 |
| Application Integration | AppSync, EventBridge, SNS, SQS, Step Functions | 05, 06, 07 |
| Compute | EC2, Elastic Beanstalk, Lambda, SAM | 01, 04, 11, 13 |
| Containers | Copilot, ECR, ECS, EKS | 11, 12 |
| Database | Aurora, DynamoDB, ElastiCache, MemoryDB, RDS | 03, 08 |
| Developer Tools | Amplify, Cloud9, CloudShell, CodeArtifact, CodeBuild, CodeCommit, CodeDeploy, CodeGuru, CodePipeline, CodeStar, X-Ray | 00, 10, 11, 16 |
| Management/Governance | AppConfig, CDK, CloudFormation, CloudTrail, CloudWatch, CLI, Systems Manager | 00, 01, 10, 13, 16 |
| Networking | API Gateway, CloudFront, ELB, Route 53, VPC | 01, 05, 15 |
| Security | ACM, Cognito, IAM, KMS, Secrets Manager, STS, WAF | 00, 14 |
| Storage | EBS, EFS, S3, S3 Glacier | 01, 02 |

## 10-day schedule (today: Mon 2026-08-31)
Weekdays ~2-3 hrs/day; the two weekend days are your **heavy-lift** days — plan for more hours since there's an extra module.

- [ ] **Day 1 — Mon Aug 31**: `00-Exam-Overview-and-AWS-Fundamentals`, `01-EC2-and-Compute-Basics`
- [ ] **Day 2 — Tue Sep 01**: `02-S3-and-Storage`, `03-DynamoDB`
- [ ] **Day 3 — Wed Sep 02**: `04-App-Design-Patterns-and-Lambda`, `05-API-Gateway-and-AppSync`
- [ ] **Day 4 — Thu Sep 03**: `06-Messaging-Streaming-and-Analytics`, `07-Step-Functions-and-Orchestration`
- [ ] **Day 5 — Fri Sep 04**: `08-Relational-and-InMemory-Databases`, `09-Caching-Strategies-and-Performance`
- [ ] **Day 6 — Sat Sep 05 (heavy)**: `10-CICD-and-Developer-Tooling`, `11-Elastic-Beanstalk-Amplify-Copilot`, `12-Containers-ECS-ECR-Fargate-EKS`
- [ ] **Day 7 — Sun Sep 06 (heavy)**: `13-IaC-CloudFormation-SAM-CDK`, `14-Security-Deep-Dive`, `15-Networking-for-Developers`
- [ ] **Day 8 — Mon Sep 07**: `16-Monitoring-Logging-and-Observability`, `17-Well-Architected-and-Exam-Strategy`
- [ ] **Day 9 — Tue Sep 08**: Full review pass + redo any question you got wrong across all modules + **Mock Exam 1** (timed, 130 min)
- [ ] **Day 10 — Wed Sep 09**: **Mock Exam 2** (timed, 130 min) + final weak-spot review + exam-day checklist

## Module checklist
Status legend: ✅ complete (all 3 files) · 🟡 partial (see note) · ⬜ not started. See `HANDOVER.md` for the full continuation brief if you're picking this project back up in a new session.

- [x] ✅ 00 — Exam Overview & AWS Fundamentals
- [x] ✅ 01 — EC2 & Compute Basics
- [x] ✅ 02 — S3 & Storage
- [x] ✅ 03 — DynamoDB
- [x] ✅ 04 — App Design Patterns & AWS Lambda
- [x] ✅ 05 — API Gateway & AppSync
- [x] ✅ 06 — Messaging, Streaming & Analytics (SQS, SNS, EventBridge, Kinesis, Athena, OpenSearch)
- [x] ✅ 07 — Step Functions & Orchestration
- [x] ✅ 08 — Relational & In-Memory Databases (RDS, Aurora, ElastiCache, MemoryDB)
- [x] ✅ 09 — Caching Strategies & Performance
- [x] ✅ 10 — CI/CD & Developer Tooling (CodeCommit, CodeBuild, CodeDeploy, CodePipeline, CodeArtifact, CodeStar, AppConfig)
- [x] ✅ 11 — Elastic Beanstalk, Amplify & Copilot
- [x] ✅ 12 — Containers (ECS, ECR, Fargate, EKS)
- [x] ✅ 13 — IaC (CloudFormation, SAM, CDK)
- [ ] ⬜ 14 — Security Deep Dive (IAM, KMS, Secrets Manager, Cognito, STS, ACM, WAF) — not started, biggest remaining module
- [x] ✅ 15 — Networking for Developers (VPC, Route 53, CloudFront)
- [ ] 🟡 16 — Monitoring, Logging & Observability (CloudWatch, X-Ray, CloudTrail, CodeGuru) — notes.md done, needs questions.md + quiz.html
- [ ] ⬜ 17 — Well-Architected & Exam Strategy — not started
- [ ] ⬜ 18 — Mock Exams (×2) — build last, once 00-17 are complete

Tick a box in either checklist as you finish it — it's your progress tracker for the sprint.
