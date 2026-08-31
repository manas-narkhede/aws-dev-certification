# Module 15 — Networking for Developers

Domain focus: primarily **Development with AWS Services (32%)**, specifically Domain 1 Task Statement 2's explicit callout of "the access of private resources in VPCs from Lambda code," plus general application-layer networking (Route 53, CloudFront) that shows up across Domain 1 and Domain 4 (troubleshooting connectivity). Per AWS's own exam guide, **designing AWS networking infrastructure (Amazon VPC, Direct Connect) is explicitly out of scope** for DVA-C02 — that's Solutions Architect territory. This module stays on the developer side of that line: not "how do I carve up CIDR ranges and design subnets," but "how do I get my Lambda function talking to a private database, keep AWS API traffic off the public internet, and configure Route 53/CloudFront as application-layer services." Security Groups, NACLs, and ELB fundamentals were covered in Module 01 — this module builds on top of that, it doesn't repeat it.

## 1. VPCs and subnets — just enough to reason about "where does this live"

A **VPC (Virtual Private Cloud)** is a logically isolated virtual network within a Region, defined by an IP address range (a CIDR block, e.g. `10.0.0.0/16`). A **subnet** is a subdivision of that range, and — critically — every subnet lives in exactly one Availability Zone. You will not be asked to design a VPC's CIDR layout on this exam, but you do need to be able to look at a scenario and reason about where a resource sits and what that implies for reachability.

Every subnet has an associated **route table** that determines where its outbound traffic goes. The single fact that determines whether a subnet is "public" or "private" is not a checkbox — it's what its route table points `0.0.0.0/0` (all non-local traffic) at:

- **Public subnet** — its route table sends `0.0.0.0/0` to an **Internet Gateway (IGW)**. A resource in a public subnet is only actually reachable from the internet if it *also* has a public IP or Elastic IP attached — the route alone doesn't make it internet-facing.
- **Private subnet** — its route table has no route to an IGW. Anything launched here (a database, an internal microservice, a VPC-attached Lambda function) has no direct inbound *or* default outbound path to the internet.

This is the mental model you actually need: **RDS instances, ElastiCache clusters, and internal application tiers almost always live in private subnets** — "put the database in a private subnet, never give it a public IP" is one of the most consistently tested security defaults on this exam, and it's exactly why a Lambda function that needs to talk to that database has to be explicitly attached to the VPC (Section 4).

## 2. Getting traffic in and out: Internet Gateway vs. NAT Gateway

These two are the exam's favorite "sounds similar, does something completely different" pair in this module.

**Internet Gateway (IGW)** — a horizontally scaled, redundant, highly available VPC component, one per VPC, attached directly to the VPC. It provides **two-way** internet connectivity: resources with a public IP in a subnet routed to the IGW can both initiate outbound connections and receive unsolicited inbound connections (subject to Security Group/NACL rules). This is what makes a subnet "public."

**NAT Gateway** — a managed, AWS-operated network address translation service that lives *inside a public subnet* (it needs its own Elastic IP and a route to the IGW) and provides **outbound-only** internet access for resources in private subnets. A private subnet's route table sends `0.0.0.0/0` to the NAT Gateway instead of an IGW; the NAT Gateway rewrites and forwards the request out through the IGW and returns the response to the private resource — but nothing outside can initiate a new connection back in. This is the standard pattern for "a private EC2 instance or a VPC-attached Lambda function needs to call an external API or reach a public AWS service endpoint, but must never be directly reachable from the internet."

A few developer-relevant details:
- NAT Gateway is billed **per hour it's provisioned plus per GB of data it processes** — at scale, that data-processing charge is a real line item, and it's the direct financial motivation behind VPC endpoints (Section 3): traffic to AWS services routed through a VPC endpoint instead of out through the NAT Gateway avoids that per-GB charge entirely.
- NAT Gateway is AZ-scoped (it lives in one subnet/AZ); for high availability, a NAT Gateway is typically provisioned per AZ so a single AZ's failure doesn't take out every private subnet's internet path.
- A **NAT instance** (a self-managed EC2 instance running NAT software) is the legacy, pre-managed-service alternative. It still shows up as a distractor option; the exam-favored answer is always the managed **NAT Gateway** unless a scenario specifically demands something a NAT Gateway can't do.

**Exam trap:** "Internet Gateway" and "NAT Gateway" being swapped in an answer option is one of the most common distractor tricks in this domain — IGW = two-way, public subnet; NAT Gateway = outbound-only, private subnet.

## 3. VPC Endpoints — keeping AWS API traffic off the public internet

Without a VPC endpoint, a private-subnet resource calling an AWS service API (S3, DynamoDB, Secrets Manager, SNS — anything) has to route that traffic out through the NAT Gateway, out the Internet Gateway, and back in to the AWS service's public endpoint. A **VPC endpoint** creates a private, direct path from inside your VPC straight to an AWS service, without touching a NAT Gateway, an Internet Gateway, or the public internet at all.

There are two kinds, and the exam expects you to know which services use which, and why.

### Interface endpoints
Powered by **AWS PrivateLink**. An interface endpoint provisions one or more **Elastic Network Interfaces (ENIs)** with private IP addresses directly inside your chosen subnets — that ENI becomes the private entry point for the service. You attach a Security Group to it (controlling what can reach the endpoint) and can attach an **endpoint policy** (a resource policy controlling exactly which API actions/resources are permitted through it, independent of and in addition to the calling principal's own IAM permissions). Interface endpoints cover the overwhelming majority of AWS services — Secrets Manager, Systems Manager, SNS, SQS, KMS, CloudWatch, API Gateway, Step Functions, ECR, EventBridge, and dozens more. They're billed per hour per AZ plus per GB processed — not free, but typically far cheaper than the NAT Gateway data-processing charges they replace, and the security/compliance win (never touching the public internet) often matters more than the cost delta. Because they present a private IP, they're also reachable from outside the VPC over Direct Connect or VPN, unlike Gateway endpoints.

### Gateway endpoints
Only available for **Amazon S3 and Amazon DynamoDB**. A gateway endpoint doesn't create an ENI at all — instead, it adds a target to your **route table** (a special prefix-list entry representing the service), and traffic destined for S3 or DynamoDB is routed directly to the service over AWS's internal network instead of out to the internet. Gateway endpoints have **no additional cost** whatsoever, and are reachable only from within the VPC itself (not from on-premises networks).

**Why S3 and DynamoDB specifically get the cheaper, simpler Gateway model:** both predate AWS PrivateLink (which launched in 2017) — Gateway endpoints for S3 shipped back in 2015 as the original mechanism for private VPC access to an AWS service, built on the route-table primitive that was available at the time. They're also two of the highest-throughput, most foundational services accessed from inside VPCs, and a route-table-based approach scales that traffic without consuming per-AZ ENI capacity or adding PrivateLink's per-hour/per-GB charge. AWS has simply had no reason to migrate them onto the newer Interface model — they work, they're free, and switching would remove a cost advantage customers rely on. Every other service introduced since PrivateLink's launch uses the Interface model instead.

| | Interface Endpoint | Gateway Endpoint |
|---|---|---|
| Powered by | AWS PrivateLink | Route table entry (prefix list target) |
| Mechanism | ENI with a private IP in your subnet | No ENI — routes via the VPC route table |
| Services supported | Most AWS services (Secrets Manager, SNS, SQS, KMS, SSM, API Gateway, ECR, EventBridge, etc.) | Only **Amazon S3** and **Amazon DynamoDB** |
| Cost | Hourly charge per AZ + per-GB data processed | **No additional cost** |
| Access control | Security Group on the ENI + optional endpoint policy | Optional endpoint policy + route table association |
| Reachable from on-premises (via VPN/Direct Connect) | Yes | No — VPC-internal only |

**Why a developer reaches for either one:** to stop AWS API traffic from crossing the public internet path for security/compliance reasons (a common ask: "must not traverse the public internet" or "must stay within the AWS network"), to eliminate or reduce NAT Gateway data-processing costs for high-volume AWS API traffic, and to keep a fully private-subnet architecture functional for the specific AWS services it still needs without depending on a NAT Gateway or Internet Gateway at all.

**Exam trap:** if a scenario says "reduce data transfer costs for an application that reads heavily from S3 from within a VPC" or "must not route DynamoDB traffic over the internet, at no additional cost," the answer is almost always a **Gateway endpoint**, not an Interface endpoint — "no additional cost" is usually the tiebreaker phrase.

## 4. Attaching a Lambda function to a VPC

By default, every Lambda function runs in an AWS-managed execution environment with a route straight out to the public internet and to every AWS service's public API endpoint — meaning **a Lambda function does not need to be attached to your VPC just to call S3, DynamoDB, SNS, or any other AWS service API.** VPC attachment exists to solve exactly one problem: reaching something that has **no public endpoint at all** and only exists inside your VPC — a private RDS instance, an internal ElastiCache cluster, an internal-only ALB, or an EC2-hosted internal service.

When you attach a function to a VPC, you specify **subnets** (private ones, always — see below) and one or more **Security Groups**. AWS then provisions and attaches **ENIs** in those subnets for the function's execution environments to route traffic through. Once VPC-attached, this even affects traffic to services the function relies on implicitly, like **CloudWatch Logs** — a VPC-attached function in private subnets needs a NAT Gateway or a CloudWatch Logs VPC endpoint to keep shipping logs, the same as for any other AWS API call.

**The cold-start history the exam still probes:** in the original design, ENI creation and attachment happened per function/security-group combination and was genuinely slow — this could add tens of seconds to a cold start, and was for years the single biggest reason developers avoided VPC-attaching a Lambda function unless they had no choice. In 2019, AWS re-architected this using what's internally called **Hyperplane ENIs**: a shared, pre-provisioned pool of ENIs per unique subnet + security-group combination, reused across many functions and execution environments instead of created fresh per function. This dramatically reduced (though didn't fully eliminate) the VPC-attachment cold-start penalty. The exam-relevant takeaway: **VPC attachment is not the cold-start disaster it used to be, but it's also still not "free" — don't attach a function to a VPC unless it actually needs to reach a private resource.**

**The trade-off the exam loves to test:** once a function is attached to *private* subnets, it **loses its default internet route**. If that same function also needs to call a public third-party API, or an AWS service it isn't reaching via a VPC endpoint, it now needs an explicit outbound path — a **NAT Gateway** reachable from its subnet's route table (for general internet/public-API access) or a **VPC endpoint** (for specific AWS services, avoiding the NAT Gateway entirely for that traffic). This is additive-and-subtractive: VPC attachment *grants* private-resource access and *removes* the default public path in the same move.

### Worked example — Lambda reaching a private RDS instance

A company runs an order-processing Lambda function that needs to (1) query a private Amazon RDS for MySQL instance for inventory data, (2) call an external payment processor's public API, and (3) read the current database credentials from Secrets Manager.

- The RDS instance has no public accessibility and lives in private subnets across two AZs, referenced by a DB subnet group — completely unreachable from Lambda's default execution environment.
- The developer attaches the Lambda function to the **same VPC**, selecting the **private subnets** (never a public subnet — a VPC-attached Lambda function doesn't get a public IP the way an EC2 instance in a public subnet would, so there's no benefit and only complexity in choosing a public one) and a **Security Group** scoped to the function.
- RDS's own Security Group is updated to allow inbound MySQL traffic (port 3306) **from the Lambda function's Security Group** — a security-group-to-security-group reference, not an IP range, which is both the standard and the most maintainable pattern.
- At invocation, AWS attaches (or reuses, thanks to Hyperplane pooling) ENIs in those subnets for the function's traffic. The RDS query now works.
- But the moment those private subnets became the function's only path, its default internet route disappeared. The call to the external payment API times out. The fix: add a **NAT Gateway** in a public subnet of the same VPC, and add a route in the private subnets' route table sending `0.0.0.0/0` to it, restoring outbound internet access for the payment API call while keeping the function's ENIs — and its private RDS path — inside the private subnets.
- Separately, the call to Secrets Manager for the rotating DB credentials is *also* now routed out through that same NAT Gateway unless the team adds an **Interface VPC endpoint for Secrets Manager** — doing so keeps that credential-fetch traffic off the NAT Gateway entirely (cheaper, and it never touches the public internet, which is usually the actual compliance driver behind adding it).

The general shape to recognize: **VPC attachment for private-resource access, NAT Gateway for what still needs the public internet, VPC endpoints for what doesn't need to leave AWS's network at all** — and use each only where it's actually needed.

## 5. Elastic Load Balancing in the networking picture (cross-reference to Module 01)

Module 01 covered ALB/NLB/GWLB types, target groups, and listener behavior in depth — that doesn't repeat here. What's new in this module is the networking placement question: **which subnets does a load balancer actually live in, and what does that determine?**

- An **internet-facing** load balancer is provisioned into **public subnets** (at least one per AZ you want it active in) and gets a public DNS name resolving to public IPs at each AZ's node. This is the entry point for external traffic.
- An **internal** load balancer is provisioned into **private subnets** and only gets private IPs — it's unreachable from the internet, used for internal/east-west traffic (e.g., a public-facing service calling an internal microservice through its own ALB rather than calling it directly), and is a common pattern for enforcing that only the "front door" service is ever internet-facing.
- Critically, **the load balancer's own subnet placement is independent of its targets' subnet placement** — an internet-facing ALB routinely forwards to targets (EC2 instances, IPs, Lambda functions, ECS tasks) sitting in *private* subnets. The load balancer is the only thing that needs to be reachable from outside; the backend never does.

## 6. Amazon Route 53

Route 53 is AWS's DNS service — global, highly available, and (like IAM) not Region-scoped.

**Hosted zones:**
- A **public hosted zone** defines how a domain resolves on the public internet — anyone can query it.
- A **private hosted zone** defines how a domain resolves **only within one or more VPCs** you explicitly associate it with — it's invisible to the public internet and to any VPC not associated. This is the pattern for internal service discovery (e.g., `orders.internal.mycompany.com` resolving only inside your application's VPCs).

**Record types a developer actually works with:**
- **A / AAAA** — maps a name directly to an IPv4 / IPv6 address.
- **CNAME** — maps a name to *another domain name* (not an IP), which is then resolved separately. Two hard restrictions: a CNAME **cannot be created at the zone apex** (the bare root domain, e.g. `example.com` — only a subdomain like `www.example.com`), and a CNAME **cannot coexist with any other record for that same name**.
- **Alias record** — a Route 53–specific record type, not a standard DNS record type. It behaves like a CNAME (points at another AWS resource's name) but resolves directly to that resource's current IP address(es) at query time, without an extra client-visible DNS hop. Alias records can point at an ALB/NLB, a CloudFront distribution, an S3 static website endpoint, an API Gateway custom domain, another record in the same hosted zone, and a few other AWS resource types.

**Why Alias over CNAME whenever the target is an AWS resource:** two concrete reasons, not just style preference. First, **Alias records work at the zone apex** — you can point `example.com` itself (not just `www.example.com`) directly at a CloudFront distribution or an ALB, which a CNAME structurally cannot do. Second, **queries for Alias records that resolve to supported AWS resources are free of charge** — Route 53 doesn't bill the standard per-query rate for them the way it does for A/CNAME/etc. Anytime a scenario shows a company wanting a domain's root to point at an ALB or a CloudFront distribution, "Alias record" is the answer, not CNAME.

**Routing policies** (conceptual level — you're not doing CIDR/latency math on this exam, just matching the *use case* to the *policy*):

| Policy | What it does | When a team picks it |
|---|---|---|
| Simple | Returns one record (or one of several values in random order), no health-check logic | A single-endpoint app with no failover/traffic-splitting needs |
| Weighted | Splits traffic across multiple resource sets by assigned weight | Canary/gradual rollouts, A/B testing, blue/green traffic shifting |
| Latency-based | Routes each user to the Region/endpoint with the lowest measured latency for them | Global multi-Region applications optimizing for user-perceived speed |
| Failover | Active/passive — serves the primary record unless its health check fails, then serves the secondary | Disaster recovery: a static "site unavailable" page or a secondary Region as backup |
| Geolocation | Routes based on the requester's geographic location (country/continent/state) | Content localization, or regulatory requirements (e.g., "EU traffic must be served from an EU-hosted stack") |

**Health checks** are what make Failover (and, optionally, other policies) actually reactive: Route 53 can monitor an endpoint via an HTTP/HTTPS/TCP request, monitor another health check's status (a "calculated" health check aggregating several), or watch a CloudWatch alarm, and automatically stop returning an unhealthy resource's record until it recovers.

## 7. Amazon CloudFront

CloudFront is AWS's CDN — a global network of edge locations that cache and serve content close to end users, cutting latency and reducing load on the origin. Modules 02 and 09 touch it briefly (S3-behind-CloudFront for HTTPS/custom domains, caching strategy); this is the deeper, application-layer-networking treatment.

**Distributions and origins.** A **distribution** is the CloudFront configuration tying one or more **origins** to caching/routing rules. Common origin types a developer configures:
- An **S3 bucket** — the classic pattern for static assets/websites, almost always paired with **Origin Access Control (OAC)**.
- An **Application Load Balancer** or other **custom HTTP(S) origin** — for dynamic content or an API that still benefits from edge caching, TLS offload, or CloudFront's other edge features (WAF integration, geo-restriction) in front of it.

**Cache behaviors and TTL.** A distribution can define multiple **cache behaviors**, each matched by a URL path pattern (e.g., `/images/*` handled differently than `/api/*`), each with its own origin, TTL settings (minimum/default/maximum, or "respect the origin's own `Cache-Control`/`Expires` headers" instead), and cache key policy (which headers, cookies, and query strings are allowed to vary the cached response). This is how a single distribution serves both aggressively-cached static assets and pass-through/short-TTL dynamic API responses from different paths.

**Origin Access Control (OAC).** By default, an S3 bucket with any public access would be reachable both through CloudFront *and* directly via its S3 URL — bypassing every CloudFront-layer control (WAF rules, signed URLs, geo-restriction, cache offload). **OAC** locks this down: the bucket stays fully private (Block Public Access enabled), and the bucket policy grants `s3:GetObject` only to the CloudFront service principal, scoped by condition to your specific distribution's ARN. CloudFront then signs its origin requests (SigV4) so only *that* distribution can retrieve objects — any direct request to the S3 URL is denied. OAC is the current recommended approach and replaces the older **Origin Access Identity (OAI)**, which had gaps (no SSE-KMS support, no support for all HTTP methods) that OAC closes.

**Signed URLs and signed cookies** — for restricting access to private content (paid content, entitled-user-only downloads) *through* CloudFront, separate from the S3-level access control OAC provides. A backend that already knows a user is entitled to the content generates a signed URL or signed cookie using a CloudFront **key pair/trusted key group**, embedding a policy (allowed resource(s), expiration time, optionally a restricted source IP range). **Signed URLs** suit granting access to a single file (or a small number); **signed cookies** suit granting access to *many* related files at once (e.g., every segment of a video stream, plus subtitle files) without having to individually sign and rewrite every URL a client requests.

**Lambda@Edge vs. CloudFront Functions** — both let you run custom logic at the edge instead of only at the origin, but they're not interchangeable:
- **CloudFront Functions** — lightweight JavaScript, sub-millisecond execution, runs at every CloudFront edge location, no network access, small code footprint. Built for simple, high-volume tasks: manipulating request/response headers, URL rewrites/redirects, normalizing the cache key, simple viewer-facing checks. Cheaper and faster than Lambda@Edge for anything that fits this profile.
- **Lambda@Edge** — actual Lambda functions (Node.js/Python) deployed to CloudFront's edge network, with four possible trigger points (viewer request, origin request, origin response, viewer response — vs. CloudFront Functions' two: viewer request/response only), able to make network calls and do heavier processing, but with tighter execution-time and resource limits than a standard Lambda invocation, especially on viewer-facing triggers. Used for logic CloudFront Functions can't do: calling out to another service for an auth decision, on-the-fly image resizing at the origin-request stage, more complex A/B testing logic.

**Guidance for reading a scenario:** if the requirement is simple, viewer-facing, and doesn't need network access — CloudFront Functions. If it needs to call another service, run more complex logic, or act at the origin-facing trigger points — Lambda@Edge.

## 8. Worked real-world scenarios

**Scenario A — the payment call that started timing out.** An order-processing Lambda function is VPC-attached to reach a private RDS instance (detailed as the worked example in Section 4). The RDS query starts working immediately, but the function's existing call to an external payment API — which worked fine before the change — now times out on every invocation. The root cause isn't the RDS integration; it's that attaching the function to private subnets silently removed its default internet route. **Fix:** add a NAT Gateway in a public subnet of the same VPC and route the private subnets' `0.0.0.0/0` traffic to it, restoring outbound internet access while keeping the function's private-resource access intact. **Lesson:** VPC attachment is never purely additive — always ask "what did this function used to reach by default that it can't reach anymore?"

**Scenario B — DNS-driven disaster recovery.** A company's primary application runs behind an ALB in `us-east-1`. For resilience against a regional outage, they stand up a lightweight static "we'll be back shortly" page on S3, served through a small CloudFront distribution, in a separate setup that doesn't depend on `us-east-1`. In Route 53, they configure a **Failover routing policy**: the primary record is an Alias pointing at the ALB, associated with a **health check** that polls the ALB's health endpoint; the secondary record is an Alias pointing at the CloudFront distribution in front of the static page. As long as the health check passes, Route 53 only ever returns the primary. If the primary ALB starts failing its health check, Route 53 automatically starts answering DNS queries with the secondary record instead — no application code change, no manual intervention. **Caveat worth knowing:** this is DNS-level failover, so it's bounded by DNS caching behavior on resolvers and clients — it's fast (Alias records to AWS resources use short, AWS-managed TTLs), but it is not instantaneous the way an in-Region load balancer removing an unhealthy target is.

**Scenario C — locking down "private" video content that wasn't actually private.** A media company serves paid subscriber video content from an S3 bucket through CloudFront, expecting only paying users to reach it. A security review finds that the bucket itself is still publicly readable — anyone who discovers (or guesses) the direct S3 object URL can download the video without ever going through CloudFront, completely bypassing the application's entitlement checks. The fix has two layers: first, enable **Origin Access Control (OAC)** and update the bucket policy so only the specific CloudFront distribution (via its service principal and a source-ARN condition) can call `s3:GetObject`, with S3 Block Public Access fully enabled — this closes the "hit the S3 URL directly" bypass entirely. Second, because OAC alone only proves a request came through *that distribution*, not that the *requesting user* is entitled to the content, the backend issues **signed cookies** scoped to a subscriber's session (rather than signed URLs, since the video is split across many segment files) after verifying entitlement, so CloudFront itself rejects any request lacking a valid, unexpired signature — closing the "logged-out or non-paying user still reaches CloudFront" gap too. **Lesson:** OAC secures the *origin*; signed URLs/cookies secure the *distribution* against unauthorized viewers — a fully private content pipeline typically needs both, not one or the other.

## Key exam traps from this module

- Internet Gateway = two-way, public subnet, requires a public IP on the resource. NAT Gateway = outbound-only, private subnet, no inbound path ever. Don't let the names blur together.
- Gateway VPC endpoints exist **only** for S3 and DynamoDB, and are free; every other AWS service that supports VPC endpoints uses the ENI-based Interface model (billed per hour/AZ + per GB).
- "Reduce NAT Gateway data-processing cost" or "must not traverse the public internet" for S3/DynamoDB traffic → Gateway endpoint, not Interface endpoint, and "no additional cost" is usually the tiebreaker phrase.
- Lambda does **not** need VPC attachment to call other AWS service APIs (S3, DynamoDB, SNS, etc.) — only to reach a resource with no public endpoint, like a private RDS instance or ElastiCache cluster.
- VPC-attaching a Lambda function removes its default internet route (including the path to CloudWatch Logs) — a function that needs both private-resource access and public-API/internet access needs a NAT Gateway (or the specific VPC endpoints) added back in, not just VPC attachment alone.
- Hyperplane ENIs (2019) greatly reduced, but did not eliminate, the VPC-attachment cold-start penalty — the exam still expects awareness that VPC attachment isn't a zero-cost decision.
- Alias records (not CNAME) are the answer whenever a scenario points a domain — especially the zone apex — at an AWS resource like an ALB or CloudFront distribution: CNAME can't be used at the apex, and Alias queries to AWS resources are free.
- Failover routing policy + a Route 53 health check is the standard DNS-level disaster-recovery pattern; it's automatic but still DNS-propagation-bound, not instantaneous like an in-Region load balancer health check.
- OAC restricts an S3 origin to only be reachable through its specific CloudFront distribution; it does **not** by itself restrict which end users can reach that distribution — that's what signed URLs/cookies are for. A fully private content pipeline typically needs both.
- CloudFront Functions for lightweight, viewer-facing, no-network-call logic; Lambda@Edge for heavier logic, more trigger points, and the ability to make network calls — picking the heavier tool for a simple header rewrite is the wrong answer whenever both are offered.
