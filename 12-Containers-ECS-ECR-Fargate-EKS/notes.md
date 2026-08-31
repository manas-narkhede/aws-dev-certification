# Module 12 — Containers: ECS, ECR, Fargate & EKS

Domain focus: primarily **Development with AWS Services (32%)** — containers are simply another compute/packaging pattern you deploy code into, alongside EC2 (module 01), Lambda (module 04), and Elastic Beanstalk (module 11) — with meaningful overlap into **Deployment (24%)**, since container image tags are explicitly called out in the exam guide (Task Statement 3.3) as an "approved-version environment" mechanism: promoting a specific, immutable image tag through dev → staging → prod is a deployment pattern the exam expects you to recognize. If this is your first exposure to containers, read section 1 slowly before jumping to the AWS-specific services — everything after it assumes you understand what an image and a container actually are.

## 1. Container fundamentals (the primer)

### What a container actually is
A **container** is a lightweight, isolated unit of running software that packages an application together with everything it needs to run — code, runtime, system libraries, configuration — so it behaves identically no matter where it's run. Unlike a virtual machine, a container does **not** include its own copy of the operating system kernel; it shares the host machine's kernel and is isolated from other containers using OS-level features (Linux namespaces and cgroups). This makes containers dramatically lighter and faster to start than a VM — typically starting in under a second, versus the minute-plus boot time of a full EC2 instance — while still giving each container its own isolated filesystem, process space, and network interface.

**Container vs. VM, the practical distinction:**
| | Virtual Machine (e.g. EC2 instance) | Container |
|---|---|---|
| Includes own OS kernel | Yes | No — shares host kernel |
| Typical startup time | Minutes | Seconds or less |
| Isolation mechanism | Hypervisor | OS namespaces/cgroups |
| Typical size | GBs | MBs to low GBs |
| What you patch | Full guest OS + runtime + app | Just the image's runtime + app layers |

### Docker images and the Dockerfile
A **Docker image** is a read-only, portable template that contains an application and its dependencies — it's the "AMI" of the container world, except far smaller and faster to build/ship. A **container** is simply a running instance of an image (the same relationship an EC2 instance has to an AMI, or a class has to an object in programming).

You define an image with a **Dockerfile** — a plain-text list of instructions describing how to build it. A minimal Dockerfile for a Node.js API might look like:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

Walking it: `FROM` picks a base image (here, a minimal Alpine Linux with Node 20 pre-installed); `WORKDIR` sets the working directory inside the image; `COPY` brings files from your build context into the image; `RUN` executes a command at build time (installing dependencies); `EXPOSE` documents the port the container listens on; `CMD` is the command that runs when a container is started from this image.

### Image layers
Each instruction in a Dockerfile produces a **layer** — a diff on top of the previous layer, cached and reused across builds. This is why Dockerfiles conventionally copy dependency manifests (`package.json`) and install dependencies *before* copying the rest of the application source: as long as dependencies haven't changed, Docker reuses the cached "install" layer on the next build instead of re-running `npm ci`, making rebuilds much faster. Layers are also what make image *pulls* efficient — if a host already has the base `node:20-alpine` layer cached from another image, pulling a new image built on the same base only needs to download the layers on top of it, not the whole image again.

**Why this matters for the exam:** you won't be asked to write a Dockerfile from scratch, but you're expected to recognize what an image, a Dockerfile, and a layer are, and to understand that a **container image tag is a versioned, immutable deployment artifact** — exactly the kind of "known-good version" you promote through environments in a CI/CD pipeline, parallel to an AMI ID or a Lambda function version.

## 2. Amazon ECR — Elastic Container Registry

ECR is AWS's fully managed **Docker/OCI container image registry** — the place your images live, analogous to what an S3 bucket is for objects or CodeArtifact is for packages (module 10). Every ECS task and EKS pod that runs a container pulls its image from a registry, and ECR is the AWS-native, IAM-integrated choice (though ECS/EKS can also pull from Docker Hub or any other registry).

### Private vs. public repositories
- **ECR Private repository** — the default; access controlled by IAM and (optionally) repository policies, used for your organization's proprietary images.
- **ECR Public repository (Amazon ECR Public Gallery)** — for images you want to make publicly available (open-source projects, base images you maintain for others), similar in spirit to Docker Hub's public repos.

### Authentication — `docker login` via IAM
ECR authentication is short-lived and IAM-driven, not a static username/password. The standard flow to push an image:

```bash
# 1. Authenticate the local Docker client to ECR (token valid for 12 hours)
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# 2. Build the image locally, tagging it for the ECR repo
docker build -t my-app:latest .
docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:1.4.2

# 3. Push it
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:1.4.2
```

`aws ecr get-login-password` returns a temporary authorization token derived from your current IAM credentials, which is piped into `docker login` — no long-lived registry password ever exists. Whatever IAM principal runs this needs `ecr:GetAuthorizationToken` plus `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, and `ecr:CompleteLayerUpload` (commonly granted via the AWS-managed `AmazonEC2ContainerRegistryPowerUser` policy or a scoped custom policy) to actually push.

### Image scanning for vulnerabilities
ECR can scan images for known OS and application-package vulnerabilities (CVEs):
- **Basic scanning** — powered by the open-source Clair scanner, runs on push (or on a schedule), free.
- **Enhanced scanning** — powered by Amazon Inspector, continuous rather than point-in-time (automatically re-scans images as new CVEs are published against packages already in your images, without you re-pushing anything), and also covers OS + programming-language package vulnerabilities in more depth.

The exam-relevant point: **scanning is a built-in, no-extra-infrastructure security control** for the "did I just ship a container with a known-vulnerable base image" problem — the correct answer to "how do we automatically catch vulnerable dependencies in our container images before they run in production" is almost always "enable ECR image scanning (and gate the pipeline on its findings)," not a custom third-party tool bolted onto the pipeline.

### Lifecycle policies
Registries accumulate old, untagged, or superseded image versions quickly (every CI build can push a new tag), which costs storage and clutters the repo. A **lifecycle policy** is a JSON rule set attached to a repository that automatically expires images matching criteria you define — e.g., "expire any untagged image older than 14 days" or "keep only the most recent 10 images matching the prefix `release-`." This is the exam's answer to "how do we automatically clean up old container images without a scheduled Lambda or manual deletion" — it's a native ECR feature, no external automation needed.

### CI/CD integration (CodeBuild/CodePipeline)
ECR is almost always the last step of a container build stage in a CI/CD pipeline (module 10 covers CodePipeline/CodeBuild in depth — this is the container-specific piece of that puzzle). A typical CodeBuild `buildspec.yml` for a containerized app authenticates to ECR, builds the image, tags it with the CodeBuild source version (often the Git commit SHA, for full traceability), and pushes:

```yaml
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI
  build:
    commands:
      - docker build -t $ECR_REPO_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION .
  post_build:
    commands:
      - docker push $ECR_REPO_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION
      - printf '[{"name":"my-app","imageUri":"%s"}]' $ECR_REPO_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION > imagedefinitions.json
```

The `imagedefinitions.json` output is the standard hand-off artifact CodePipeline's ECS deploy action consumes to know exactly which new image tag to roll out — this is the mechanical link between "a developer pushed code" and "ECS is now running a new container version." For CodeBuild's own execution role to push to ECR, it needs the same `ecr:*` push permissions described above; for the *CodeBuild environment itself* to pull a Docker-in-Docker capable build image, it typically needs `privileged mode` enabled in its project configuration.

## 3. Amazon ECS — Elastic Container Service

ECS is AWS's own container **orchestrator** — the system that decides where containers run, keeps the desired number running, replaces failed ones, and wires them into load balancers, service discovery, and logging. It's AWS-proprietary (not Kubernetes) and deliberately simpler to operate than a self-managed Kubernetes cluster.

### Clusters
An **ECS cluster** is a logical grouping — a namespace for the tasks and services that run within it, plus (for the EC2 launch type) the pool of EC2 instances registered to it. A cluster itself doesn't cost anything; it's the tasks and underlying compute (EC2 instances or Fargate capacity) running inside it that incur charges.

### Task definitions
A **task definition** is a JSON blueprint describing one or more containers that should run together as a unit — the container image(s), CPU/memory allocation, networking mode, environment variables, log configuration, and (critically) the IAM roles the task uses. It's revisioned: every update creates a new numbered revision, and you can roll back to a prior revision instantly, which is exactly the kind of "known-good, versioned deployment artifact" behavior the exam likes to test.

A simplified task definition sketch:

```json
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/myAppTaskRole",
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:1.4.2",
      "portMappings": [{ "containerPort": 3000, "protocol": "tcp" }],
      "environment": [{ "name": "LOG_LEVEL", "value": "info" }],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Note the **top-level `cpu`/`memory`** (the total the task reserves, required for Fargate) versus per-container resource limits you could optionally set inside each container definition when a task runs multiple containers sharing that total budget.

#### Task role vs. task execution role — the single most commonly confused ECS concept
This distinction is tested constantly, so internalize the mental model precisely:

- **Task execution role** (`executionRoleArn`) — permissions **ECS itself** (the underlying agent/infrastructure) needs *on the task's behalf* to actually start the task: pulling the container image from ECR (`ecr:GetAuthorizationToken`, `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer`), writing container logs to CloudWatch Logs, and retrieving secrets injected as environment variables from Secrets Manager or Parameter Store at container startup. Your application code never directly uses this role.
- **Task role** (`taskRoleArn`) — permissions **your application code running inside the container** needs at runtime to call other AWS services — e.g., reading an S3 bucket, writing to a DynamoDB table, publishing to an SNS topic. This is the direct container equivalent of an EC2 instance profile role, scoped per-task instead of per-instance (a real advantage over EC2: different services in the same cluster can have entirely different, tightly-scoped permissions, rather than sharing one instance-wide role).

**The mnemonic:** *execution* role = "can ECS start me" (infrastructure plumbing); *task* role = "what can I do once I'm running" (application permissions). If a container's application code gets an Access Denied calling S3, you fix the **task role**. If the task fails to even launch with an error about not being able to pull the image or write logs, you fix the **execution role**.

### Services
A **service** keeps a specified number of task instances (the **desired count**) running continuously, replacing any that stop or fail health checks — it's the ECS analog of an EC2 Auto Scaling Group, except it manages *tasks* instead of *instances*. A service can:
- Register its tasks with an **ALB target group** (using the `awsvpc` networking mode, each task gets its own elastic network interface and private IP, so the ALB routes directly to individual tasks rather than to a shared host port) — enabling the same path/host-based routing, HTTPS termination, and health checks you already know from module 01.
- Use **service auto scaling** — an Application Auto Scaling target tracking policy (e.g., "keep average CPU utilization at 60% across the service's tasks," directly parallel to ASG target tracking) that adjusts the service's desired count automatically.
- Support **deployment configurations** like rolling updates (replace old tasks with new ones incrementally, controlled by minimum/maximum healthy percent) or, integrated with CodeDeploy, **blue/green deployments** that shift traffic between an old and new task set behind the same ALB.

### Launch types: EC2 vs. Fargate
A task definition's `requiresCompatibilities` and how you run a service determine which **launch type** the tasks use:
- **EC2 launch type** — tasks run on EC2 instances you provision, patch, and scale yourself (typically via an Auto Scaling Group registered to the cluster). You get full control over the instance (custom AMIs, instance types, GPU instances, placement strategies bin-packing multiple tasks per instance for density), at the cost of managing that EC2 fleet's patching, scaling, and capacity planning.
- **Fargate launch type** — serverless; no EC2 instances to manage at all (full detail in section 4).

### ECS Exec — debugging running containers
**ECS Exec** lets you open an interactive shell (or run a one-off command) inside a running container in a running task — the direct container-world parallel to Systems Manager **Session Manager** for EC2 instances (module 01): no SSH, no exposed ports, access governed entirely by IAM, and sessions can be logged for audit. It works over the same SSM infrastructure under the hood, and requires the task's task role to include SSM messaging permissions and the ECS agent/task definition to have `enableExecuteCommand` set. Exam framing: whenever a scenario asks "how do I get a shell into a running ECS container to debug it, without opening inbound ports or managing SSH keys," the answer is **ECS Exec**, exactly the way "how do I shell into an EC2 instance securely" pointed you to Session Manager in module 01.

## 4. AWS Fargate

Fargate is a **serverless compute engine for containers** — you define a task (CPU, memory, image), and AWS runs it without you ever provisioning, patching, or scaling an underlying EC2 instance. There is no visible "host" to manage: no AMI to patch, no instance type to pick, no Auto Scaling Group of hosts to size.

### Pricing model
Fargate bills **per task, per second**, based on the vCPU and memory you provision for that task (rounded up to a minimum billing duration) — not per underlying EC2 instance. This is a fundamentally different cost model from EC2 launch type: with EC2, you pay for the instances you've provisioned whether or not they're fully utilized (bin-packing multiple tasks per instance is how you improve EC2-launch-type cost efficiency); with Fargate, you pay for exactly the resources each task consumes, with no host-level over-provisioning to manage — at a higher effective per-vCPU/GB rate than raw EC2 pricing, since you're trading raw compute cost for eliminated operational overhead.

### When Fargate is favored over EC2 launch type
Reach for Fargate when:
- The team wants **zero host management** — no patching, no capacity planning, no instance-type selection.
- Workloads are **spiky or unpredictable** and you don't want to over-provision an EC2 fleet to absorb bursts, or manage bin-packing density yourself.
- **"Least operational overhead"** appears in the requirements — this phrase pulls the answer toward Fargate over EC2 launch type exactly the way it pulled EC2-vs-Lambda answers toward Lambda in module 01.

Reach for EC2 launch type instead when you need **control over the underlying host** that Fargate doesn't expose — GPU instances for ML inference, custom AMIs, specific instance families for cost optimization via Reserved Instances/Savings Plans at the instance level, privileged host-level access, or very high-density bin-packing to minimize cost at large, steady-state scale.

## 5. Amazon EKS — Elastic Kubernetes Service

EKS is AWS's **managed Kubernetes control plane** — Kubernetes is the dominant open-source container orchestration platform (originally from Google), and EKS runs and manages the Kubernetes control plane components (API server, etcd, scheduler) for you, patched and highly available across multiple AZs, while you (or, with EKS on Fargate, AWS) run the worker nodes that actually execute your containerized workloads ("pods," in Kubernetes terminology).

**Developer-level awareness only** — DVA-C02 does not test deep Kubernetes architecture (that's a specialty-level concern), but you're expected to know what EKS is, how it differs from ECS, and when a team would reach for it.

### EKS vs. ECS — the core distinction
| | Amazon ECS | Amazon EKS |
|---|---|---|
| Orchestration API | AWS-proprietary | Open-source Kubernetes API |
| Portability | AWS-only | Kubernetes API is portable across clouds/on-prem — workloads can theoretically move to any Kubernetes-conformant platform |
| Learning curve | Simpler, fewer moving parts, AWS-native concepts (tasks, services, clusters) | Steeper — full Kubernetes concept set (pods, deployments, services, ingress, etc.) |
| Ecosystem | AWS-integrated tooling only | Massive open-source Kubernetes ecosystem (Helm charts, operators, third-party tools) works largely unmodified |
| Best fit | Teams already in the AWS ecosystem with no existing Kubernetes investment, wanting the simplest path to running containers | Teams with existing Kubernetes expertise/tooling, multi-cloud or hybrid-cloud portability requirements, or dependencies on the Kubernetes ecosystem |

**The exam's decision rule, distilled:** if the scenario says a team is *already* running Kubernetes (on-premises, in another cloud, or has existing Kubernetes-specific tooling/expertise) and wants to bring that workload to AWS with minimal re-architecture, the answer is **EKS**. If the scenario is "we're starting fresh on AWS and just need to run containers with the least complexity," the answer is usually **ECS**.

### EKS with Fargate
Just as ECS can run tasks on Fargate instead of self-managed EC2 instances, **EKS also supports Fargate as a compute option for pods** — you define a Fargate profile matching certain namespaces/labels, and matching pods run on Fargate with no worker-node EC2 instances to manage, combining Kubernetes-API portability with Fargate's serverless operational model. This is the answer when a scenario wants "Kubernetes API compatibility" *and* "no EC2 worker nodes to manage" simultaneously.

## 6. IAM roles for containers — recap and cross-service view

The task role / task execution role distinction (section 3) is ECS-specific terminology, but the underlying pattern — "a role for the orchestrator's own plumbing" vs. "a role for the application code" — recurs across every AWS compute option in this course:

| Service | "Plumbing" role (infra-facing) | "Application" role (code-facing) |
|---|---|---|
| EC2 (module 01) | N/A (no separate plumbing role) | Instance profile role |
| Lambda (module 04) | N/A | Execution role (does double duty — both concepts collapse into one role for Lambda) |
| ECS/Fargate | Task execution role | Task role |
| EKS | Cluster IAM role (control plane) / node IAM role (worker nodes) | IAM Roles for Service Accounts (IRSA) — maps a Kubernetes service account to an IAM role, giving individual pods scoped permissions (conceptually the EKS equivalent of an ECS task role) |

**Exam trap:** ECS is the one service on this exam where "the container can't call S3" and "the task won't even start" point to two *different* roles to fix — don't reflexively widen the task execution role when the actual problem is the task role, or vice versa.

## 7. Worked real-world scenarios

**Scenario A — "the task starts but the app can't reach S3."** A team deploys a new revision of an ECS service on Fargate. The task definition change deploys cleanly — the service shows the desired count of running tasks, CloudWatch shows successful image pulls and log delivery — but the application immediately throws `AccessDenied` errors every time it tries to read a configuration file from an S3 bucket. A developer's first instinct is to widen the task's *execution* role, which does nothing (the task already started fine — that role already worked). The actual fix: the **task role** (`taskRoleArn`), which governs what the running application code can do, is either missing the `s3:GetObject` permission or is pointed at the wrong role ARN entirely. Attaching an `s3:GetObject` permission scoped to that specific bucket/prefix on the task role resolves it immediately, with no execution-role change needed. **Lesson:** "task starts fine but the app's own AWS calls fail" is always a task-role problem, never an execution-role problem — the execution role's job was already done by the time the container's code runs.

**Scenario B — "why is our container fleet suddenly expensive, and how do we simplify it."** A startup originally deployed its API on the ECS **EC2 launch type**, running a modestly sized Auto Scaling Group of `m6g.large` instances bin-packed with multiple tasks each. As traffic became spikier (heavy during business hours, near-zero overnight) and the small platform team spent increasing time tuning ASG scaling policies and patching the underlying AMI, leadership asks for a design that "minimizes operational overhead" even if the raw per-vCPU compute cost is somewhat higher. The team migrates the service to the **Fargate** launch type: the task definitions stay almost identical (same image, same CPU/memory, same task role), but there's no more EC2 fleet to patch, no ASG to tune for host-level scaling, and Fargate tasks scale up and down per-task within seconds to match the service's target-tracking policy, billing only for the vCPU/memory-seconds each task actually consumes — trading a higher per-unit compute rate for materially less operational burden, which is exactly the tradeoff "least operational overhead" signals on the exam.

**Scenario C — "the platform team already runs Kubernetes everywhere else."** A company with a large on-premises Kubernetes footprint, extensive internal tooling built against the Kubernetes API (custom operators, Helm-based deployment pipelines, existing runbooks written by their SRE team), and workloads that may eventually need to run in a second cloud provider for disaster-recovery purposes is migrating one workload to AWS. A well-meaning architect proposes ECS, citing its simplicity — but the team's existing Helm charts, custom Kubernetes operators, and staff Kubernetes expertise would all have to be rebuilt or retrained for ECS's proprietary task/service model, and any future multi-cloud portability goal is off the table on ECS. **EKS** is the correct fit here specifically *because* of the existing Kubernetes investment and portability requirement — not because EKS is inherently "better" than ECS (it isn't, for a team without that context; it's simply the right tool given this team's specific constraints). The team further chooses **EKS with Fargate** for their newer, stateless services to avoid also having to manage worker-node EC2 capacity, while keeping self-managed EKS worker nodes only for a smaller set of workloads needing GPU instance types Fargate doesn't support.

## 8. ECS-on-EC2 vs. Fargate vs. EKS — the exam's core comparison table

| | ECS (EC2 launch type) | ECS (Fargate launch type) | EKS |
|---|---|---|---|
| Orchestration API | AWS-proprietary | AWS-proprietary | Open-source Kubernetes API |
| Underlying host management | You manage the EC2 fleet (patching, scaling, AMIs) | None — fully serverless, no visible host | You manage worker nodes (EC2 or self-managed), unless using EKS with Fargate |
| Operational overhead | Higher — you own instance patching/scaling | Lowest — no host to manage at all | Highest for the control plane concepts, though AWS manages the Kubernetes control plane itself; worker-node ops still apply unless paired with Fargate |
| Control over host | Full (custom AMI, instance type, GPU, placement) | None (no host-level access) | Full for self-managed worker nodes; none if using EKS with Fargate |
| Pricing model | Pay for provisioned EC2 instances (On-Demand/RI/Spot), regardless of bin-packing efficiency | Pay per task, per vCPU/memory-second actually provisioned | EC2 costs for worker nodes (or Fargate per-task pricing) plus an hourly EKS cluster/control-plane fee |
| Portability | AWS-only | AWS-only | Portable Kubernetes API — workloads can move to other Kubernetes-conformant platforms |
| Best exam answer when... | Need GPU/specific instance types, very high-density bin-packing for cost at scale, or full host control | "Least operational overhead," spiky/unpredictable load, no interest in managing hosts | Team already has Kubernetes investment, needs multi-cloud/hybrid portability, or relies on the Kubernetes ecosystem |

## 9. How this connects to Domain 3 (Deployment)

The exam guide's Task Statement 3.3 explicitly calls out deploying code with a **container image tag as an "approved-version environment"** mechanism — meaning you should recognize that a specific, immutable image tag (e.g., `my-app:1.4.2`, or better, one pinned to an immutable digest/commit SHA rather than a mutable tag like `latest`) is how you promote a known-good build through dev → staging → production, exactly parallel to promoting a specific Lambda version/alias or CodeDeploy application revision. A CI/CD pipeline (module 10) that builds an image, pushes it to ECR tagged with the Git commit SHA, and updates an ECS service's task definition to reference that exact tag is the canonical "deploy code via a container image" pattern the exam expects you to recognize — and rolling back means simply pointing the service back at the previous task definition revision (referencing the previous image tag), not rebuilding anything.

## Key exam traps

- **Task role vs. task execution role** is the single most tested ECS distinction: execution role = ECS pulling the image + writing logs + fetching injected secrets (infrastructure plumbing); task role = what your application code inside the container can call (S3, DynamoDB, etc. at runtime). An app-level `AccessDenied` is a task-role fix; a failure to even launch (image pull / logging failure) is an execution-role fix.
- **"Least operational overhead"** for containers pulls the answer toward **Fargate**, the same way it pulled EC2-vs-Lambda answers toward Lambda in module 01 — don't default to the EC2 launch type when the scenario emphasizes minimal host management.
- **ECS ≠ Kubernetes.** ECS uses AWS's own proprietary orchestration API; EKS runs actual open-source Kubernetes. A scenario mentioning existing Kubernetes tooling, Helm charts, or multi-cloud portability points to **EKS**, not ECS.
- **EKS with Fargate** exists and combines Kubernetes-API portability with no worker-node management — don't assume EKS always means managing EC2 worker nodes.
- **ECS Exec**, not SSH, is the exam's answer for shelling into a running container to debug it — parallel to Session Manager for EC2, governed by IAM, no inbound ports required.
- **ECR image scanning** (basic via Clair, enhanced via Inspector) is the native, no-extra-infrastructure answer for automatically catching known vulnerabilities in container images — prefer it over a bespoke third-party scanning step when the exam asks for the AWS-native solution.
- **ECR lifecycle policies** automatically expire old/untagged images — the native answer for "clean up old container images automatically," not a custom Lambda cleanup script.
- `aws ecr get-login-password` piped into `docker login` is how registry authentication actually works day to day — it's short-lived and IAM-derived, never a static registry password.
- A container **image tag** (ideally pinned to an immutable digest or commit SHA) is a deployment artifact in the same family as an AMI ID or a Lambda version — recognize it as the "approved-version" mechanism the exam associates with container-based deployments (Domain 3, Task Statement 3.3).
- Fargate's higher per-unit compute price versus EC2 launch type is a deliberate tradeoff for eliminated host management — don't assume "cheaper" is always the right answer; the question's actual priority (cost minimization at scale vs. operational simplicity) determines which launch type is correct.
