# Module 01 — EC2 & Compute Basics

Domain focus: mostly **Development with AWS Services (32%)**, with pieces of **Deployment** and **Troubleshooting**. EC2 itself is lightly tested on DVA-C02 (this is a developer exam, not SysOps), but you need to know it well enough to reason about instance metadata, roles, scaling, load balancing, and — critically — when EC2 is the *wrong* answer versus Lambda/Beanstalk/ECS.

## 1. What EC2 is
Elastic Compute Cloud = resizable virtual servers ("instances") running on AWS-managed physical hardware. You choose the OS (via an AMI), the hardware profile (instance type), storage, and networking; AWS handles the physical layer per the Shared Responsibility Model (module 00).

### Instance type naming
`m6g.large` → **family** (m = general purpose) + **generation** (6) + **processor variant** (g = Graviton/ARM; nothing = Intel; a = AMD) + **size** (large).

| Family | Purpose |
|---|---|
| T (t3, t4g) | Burstable, low-cost, for variable/low average CPU (uses CPU credits) |
| M | General purpose, balanced compute/memory/network |
| C | Compute-optimized (batch processing, gaming servers, HPC) |
| R | Memory-optimized (in-memory caches, big data processing) |
| I / D | Storage-optimized (high IOPS local NVMe, dense storage) |
| G / P | GPU-accelerated (ML training/inference, graphics) |

**Exam trap:** T-family "burstable" instances earn CPU credits when idle and spend them under load; if credits run out, performance is throttled (unless "Unlimited" mode is enabled, which can incur extra charges). A sustained high-CPU workload on a `t3` instance is a common "why is my app suddenly slow" troubleshooting scenario.

### AMIs (Amazon Machine Images)
A template containing OS + preinstalled software + configuration used to launch instances. Sources: AWS-provided, AWS Marketplace, community, or **your own** (built by taking a snapshot of a configured instance — "golden AMI" pattern, common for fast, consistent Auto Scaling launches).

## 2. Purchasing options (recap + developer-relevant detail)
| Option | Best for | Key trait |
|---|---|---|
| On-Demand | Unpredictable/short-term workloads | Pay per second, no commitment |
| Reserved Instances | Steady-state, known workloads, 1-3yr | Up to ~72% discount, can be Standard (less flexible, cheaper) or Convertible (can change instance family) |
| Savings Plans | Steady-state spend across EC2/Fargate/Lambda | Commit to $/hr, more flexible than RIs, still deep discount |
| Spot Instances | Fault-tolerant, interruptible workloads | Up to ~90% discount; 2-minute interruption notice via instance metadata + EventBridge event |
| Dedicated Hosts | Licensing tied to physical cores/sockets/VMs | Full visibility/control of the physical server |
| Dedicated Instances | Compliance requiring physical isolation | Isolated hardware, no host visibility |

**Exam trap:** if a question mentions "socket-based" or "per-core" licensing (e.g. certain enterprise software), the answer is **Dedicated Hosts**, not Reserved Instances.

## 3. Instance metadata & user data (heavily tested)
- **User data**: script/config passed at launch, runs once on first boot (e.g. a bootstrap shell script). Retrieved from `http://169.254.169.254/latest/user-data`.
- **Instance metadata service (IMDS)**: lets code running *on* the instance query its own properties (instance ID, AMI ID, security groups, IAM role credentials, etc.) at `http://169.254.169.254/latest/meta-data/`.
- **IMDSv1 vs IMDSv2**: IMDSv1 is a simple GET request; IMDSv2 requires a session token first (`PUT` to get a token, then `GET` with that token in a header) — this defends against SSRF attacks tricking a server into fetching credentials from the metadata endpoint. **The exam wants you to recommend IMDSv2 (or enforce it via "HttpTokens: required") as the more secure choice.**
- Retrieving temporary IAM role credentials from the instance metadata endpoint is exactly how an EC2 instance profile actually delivers credentials to the SDK under the hood.

## 4. Storage for EC2
| Type | Persistence | Scope | Notes |
|---|---|---|---|
| EBS (Elastic Block Store) | Persists independently of instance lifecycle | AZ-scoped, network-attached | Default for boot volumes; supports snapshots (stored in S3, incremental), can resize/change type live |
| Instance Store | Ephemeral — lost on stop/terminate (survives reboot) | Physically attached | Very high IOPS, used for cache/temp/scratch data only |
| EFS (Elastic File System) | Persists, shared | Regional, multi-AZ | POSIX file system mountable by many instances concurrently (covered more in module 02) |

### EBS volume types
| Type | Use case |
|---|---|
| gp3/gp2 (SSD, general purpose) | Default choice for most workloads; gp3 lets you provision IOPS/throughput independently of size |
| io1/io2 (Provisioned IOPS SSD) | High-performance databases needing consistent, very high IOPS |
| st1 (Throughput Optimized HDD) | Big data, log processing — throughput-focused, not boot-capable |
| sc1 (Cold HDD) | Infrequently accessed data, lowest cost |

**Exam trap:** EBS snapshots are incremental (only changed blocks after the first snapshot) but each snapshot still represents a full point-in-time restore point. Snapshots live in S3 but you don't manage them as S3 objects directly.

## 5. Elastic Load Balancing (ELB)
| Type | Layer | Use case |
|---|---|---|
| Application Load Balancer (ALB) | Layer 7 (HTTP/HTTPS) | Path/host-based routing, microservices, container/Lambda targets, WebSockets |
| Network Load Balancer (NLB) | Layer 4 (TCP/UDP) | Extreme performance, static IP / Elastic IP support, TLS passthrough |
| Gateway Load Balancer (GWLB) | Layer 3/4 | Deploying third-party virtual appliances (firewalls, IDS/IPS) transparently |
| Classic Load Balancer (CLB) | Legacy | Avoid in new designs — retained knowledge only |

**Exam trap:** "Route based on URL path (`/api` vs `/images`)" → ALB. "Need a static IP for the load balancer" or "extreme low-latency TCP" → NLB. Target groups (not raw instances) are what a modern ELB routes to, and target groups can point at EC2 instances, IP addresses, Lambda functions, or ECS tasks.

## 6. Auto Scaling
- **Launch Template** (preferred over the older Launch Configuration — supports versioning, more instance options, mixed instance types) defines what to launch: AMI, instance type, key pair, security groups, user data, IAM instance profile.
- **Auto Scaling Group (ASG)**: manages a fleet across min/desired/max capacity, spread across AZs/subnets you specify, replaces unhealthy instances automatically (health checks can be EC2 status checks or ELB health checks).
- **Scaling policies**:
  - *Target tracking* — e.g. "keep average CPU at 50%" (simplest, most recommended).
  - *Step scaling* — scale by defined increments based on CloudWatch alarm thresholds.
  - *Scheduled scaling* — scale for predictable time-based patterns (e.g. business hours).
  - *Predictive scaling* — uses ML on historical patterns.
- **Lifecycle hooks** let you run custom actions (e.g. deregister from a service, drain connections) before an instance is terminated or after it's launched but before it's put into service.

**Exam trap:** ASG health check type matters — if only EC2 status checks are used, ASG won't replace an instance whose *application* has crashed but whose OS is still fine; switch to ELB health checks (or add a custom health check) for application-level failure detection.

## 7. Security Groups vs. NACLs (deeper coverage in module 15; you need the basics now)
| | Security Group | Network ACL |
|---|---|---|
| Level | Instance (ENI) level | Subnet level |
| Rules | Allow only (no explicit deny) | Allow and Deny |
| State | Stateful — return traffic automatically allowed | Stateless — must explicitly allow both directions |
| Evaluation | All rules evaluated, most permissive wins | Rules evaluated in numbered order, first match wins |

**Exam trap:** "Traffic is allowed in a Security Group but still blocked" → check the NACL; it's stateless and might be blocking the *return* path even if inbound was allowed.

## 8. Systems Manager (SSM) essentials for developers
- **Session Manager**: shell access to an instance **without opening SSH port 22 or needing a bastion host** — access is governed entirely by IAM, and sessions are logged. This is the exam's preferred answer whenever a scenario asks "how do I securely access an instance without exposing SSH."
- **Run Command**: execute commands/scripts across many instances without SSH, via IAM-controlled API calls.
- **Parameter Store**: hierarchical, free (standard tier) key-value config/secrets store, integrates with KMS for encryption (SecureString). Covered in depth in module 14 alongside Secrets Manager.
- Requires the **SSM Agent** running on the instance and an IAM role with the right SSM permissions attached (no inbound network access needed).

## 9. EC2 vs. everything else — the exam's favorite decision table
| Need | Best fit |
|---|---|
| Full OS control, long-running, custom runtime/licensing | EC2 |
| Event-driven, short-lived, no server management | Lambda |
| Simple web app deploy, minimal ops, still want visibility into resources | Elastic Beanstalk |
| Containerized microservices, need orchestration | ECS/Fargate (or EKS) |
| Batch jobs at massive scale with flexible scheduling | AWS Batch (built on ECS/EC2/Fargate) |

The phrase **"least operational overhead"** almost always eliminates EC2 in favor of a managed/serverless option when the workload fits (short-running, event-driven, stateless). EC2 is the right answer when you need OS-level control, specific licensing, persistent local state, or workloads that don't fit the serverless execution model (e.g. long-running processes >15 min that also need full OS access, unlike Lambda's 15-minute cap).

## 10. Worked real-world scenarios

**Scenario A — the throttled T-instance.** A team runs their staging API on a `t3.medium` instance. After a load test, response times balloon from 80ms to 4 seconds with no code changes and no error logs. CPU utilization graphs show it pinned at 100% for the last 20 minutes of the test. The team suspects a memory leak and starts profiling code — the wrong first move. The actual cause: `t3.medium` is a burstable instance; sustained load exhausted its CPU credit balance, and once credits hit zero the instance is throttled to its baseline performance (a fraction of full CPU). The fix isn't code — it's either switching to a non-burstable family (M or C) for a workload with sustained CPU needs, or enabling "Unlimited" credit mode (at extra cost) if the burstiness is only occasional. **Lesson:** always check CloudWatch CPU credit balance/CPU surplus metrics before profiling code on a T-family instance exhibiting a sudden slowdown.

**Scenario B — the SSRF that almost leaked credentials.** A web application running on EC2 has a feature that fetches a URL supplied by the user (e.g., "import an image from this link") and returns its contents. A penetration test discovers the app will happily fetch `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>` if given that URL — a classic Server-Side Request Forgery (SSRF) vulnerability turning into a credential-theft vector, because the instance still has IMDSv1 enabled (a simple GET request, no token required). The remediation: enforce IMDSv2 account-wide (`HttpTokens: required` in the instance metadata options), which requires a PUT request with a custom header to first obtain a session token — something a simple SSRF redirect typically can't perform, closing this specific attack path even if the SSRF bug in the app itself isn't fixed yet.

**Scenario C — the ASG that didn't notice the app had crashed.** An Auto Scaling Group behind an ALB is configured with only EC2 status checks as its health check type. The application process on one instance crashes due to an unhandled exception, but the underlying EC2 instance itself is still running fine (OS healthy, network reachable) — so the EC2 status check keeps passing, and the ASG never replaces the broken instance, silently sending a fraction of user traffic into a black hole. The fix: switch the ASG's health check type to include ELB health checks (which poll the actual application, e.g. an HTTP health check endpoint), so an application-level failure — not just an infrastructure-level one — triggers instance replacement.

## Key exam traps from this module
- T-family CPU credit exhaustion silently throttles performance — a classic "why did my app slow down" scenario.
- IMDSv2 (token-required) is the secure answer over IMDSv1 whenever metadata access comes up.
- Dedicated Hosts (not Reserved Instances) for per-core/socket licensing requirements.
- ALB for HTTP path/host routing; NLB for static IP/extreme performance/TCP passthrough.
- ASG with only EC2 health checks won't catch application-level failures — use ELB or custom health checks.
- Security Groups are stateful and allow-only; NACLs are stateless and support explicit deny, evaluated in order.
- Session Manager is the go-to "no open SSH port" secure access answer.
- "Least operational overhead" pulls the answer away from EC2 toward Lambda/Beanstalk/containers whenever the workload allows it.
