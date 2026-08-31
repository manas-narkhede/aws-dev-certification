# Module 02 — S3 & Storage

Domain focus: mostly **Development with AWS Services (32%)** — Domain 1, Task Statement 3 ("Develop code for interacting with AWS services... implement code to make use of AWS data stores"). Encryption content (SSE-S3/SSE-KMS/SSE-C, client-side vs server-side, AWS-managed vs customer-managed KMS keys) also feeds directly into **Security (26%)** — Domain 2, Task Statement 2. S3 is one of the most heavily tested services on DVA-C02: it's the default answer for "durable, cheap, internet-scale storage" across dozens of scenarios in later modules (static assets behind CloudFront, Lambda deployment packages, data lake sources, CI/CD artifacts), so a shaky mental model here costs you points throughout the whole exam, not just in this module.

## 1. What S3 actually is

Amazon S3 (Simple Storage Service) is **object storage**, not a filesystem and not a block device. You put whole objects (files, effectively — up to 5TB each) into **buckets**, addressed by a **key** (the full "path-like" string, e.g. `images/2024/cover.jpg`) — there is no real directory tree under the hood, just keys that happen to contain slashes, which the console renders as folders for convenience.

- **Bucket names are globally unique** across all of AWS (not just your account) — this is why `my-app-bucket` is almost always taken. A bucket lives in **one Region** you choose at creation; data doesn't leave that Region unless you explicitly replicate or copy it.
- **Durability**: S3 Standard is engineered for **99.999999999%** (11 nines) durability — it redundantly stores objects across a minimum of **three Availability Zones** in the Region. Losing an object is treated as effectively impossible under normal operation; this durability figure is identical across all S3 storage classes except One Zone-IA.
- **Availability**: how often the *service* is reachable/responsive — this varies by storage class (99.99% for Standard, down to 99.5% for One Zone-IA) and is a different number from durability. The exam likes to test that you know these are two distinct concepts.
- **No capacity planning** — you never provision "how much S3 you need." You pay for what you store, per GB-month, plus request and transfer charges. Contrast this explicitly with EBS (module 01), where you provision a fixed volume size up front.
- Every object also carries **metadata** (system-defined like `Content-Type`, and up to 2KB of user-defined key-value pairs) alongside its data.

## 2. S3 storage classes (tiers) — the core of this module

All classes offer the same 11-nines durability (except One Zone-IA, which is AZ-scoped and thus loses that guarantee if the AZ is destroyed). What changes across classes is **availability, retrieval latency, retrieval cost, and minimum storage duration** — the classic "hot vs. cold" storage tradeoff.

| Storage class | Availability | Retrieval | Min. storage duration | Best for |
|---|---|---|---|---|
| S3 Standard | 99.99% | Milliseconds, no fee | None | Frequently accessed, actively-used data |
| S3 Intelligent-Tiering | 99.9% | Milliseconds (Frequent/Infrequent tiers), varies for optional archive tiers | None | Unknown or changing access patterns — lets AWS pick the tier for you |
| S3 Standard-IA (Infrequent Access) | 99.9% | Milliseconds, per-GB retrieval fee | 30 days | Backups, DR files accessed occasionally but needed fast when accessed |
| S3 One Zone-IA | 99.5% | Milliseconds, per-GB retrieval fee | 30 days | Reproducible/non-critical data (thumbnails you could regenerate) — single AZ, ~20% cheaper than Standard-IA |
| S3 Glacier Instant Retrieval | 99.9% | Milliseconds, higher retrieval fee than Standard-IA | 90 days | Archive data needed instantly but accessed roughly quarterly |
| S3 Glacier Flexible Retrieval | 99.99% (after retrieval) | Minutes to hours (see retrieval tiers below) | 90 days | True archives, not needed instantly, cost-sensitive |
| S3 Glacier Deep Archive | 99.99% (after retrieval) | 12–48 hours | 180 days | Long-term compliance/regulatory archives, rarely if ever accessed |

**S3 Intelligent-Tiering mechanics (worth knowing in detail):** it automatically moves objects between a **Frequent Access** tier and an **Infrequent Access** tier based on 30-day access patterns, with **no retrieval fees** ever and no performance impact — you pay a small per-object monthly monitoring/automation fee instead. You can optionally enable it to move objects further into **Archive Instant Access**, **Archive Access**, and **Deep Archive Access** tiers after longer periods of no access. This is the answer whenever a scenario says "access patterns are unknown or unpredictable and we don't want to manage lifecycle rules manually."

**Exam trap:** Standard-IA and One Zone-IA both charge a **per-GB retrieval fee** and have a **minimum billable object size (128KB)** and **minimum storage duration (30 days)** — deleting or transitioning an object out early still bills for the remaining minimum days. A workload that deletes/overwrites objects frequently (e.g., a churny cache) is a bad fit for these classes regardless of how "infrequently accessed" the data seems.

## 3. Lifecycle policies — automating tier transitions and expiration

A **lifecycle configuration** is a set of rules (scoped to a prefix and/or tags) with two kinds of actions:
- **Transition actions** — move an object to a cheaper class after N days (e.g., Standard → Standard-IA at 30 days → Glacier Flexible Retrieval at 90 days → Deep Archive at 180 days).
- **Expiration actions** — permanently delete an object after N days.

```json
{
  "Rules": [
    {
      "ID": "archive-old-logs",
      "Filter": { "Prefix": "logs/" },
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" },
        { "Days": 180, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "Expiration": { "Days": 365 }
    }
  ]
}
```

With **versioning enabled** (next section), lifecycle rules can separately target **noncurrent versions** — e.g., "transition noncurrent versions to Glacier after 30 days, permanently delete them after 365 days" — which is how teams keep versioning's safety net without paying Standard-rate storage forever for every old version. Lifecycle rules can also **abort incomplete multipart uploads** after N days, cleaning up storage silently consumed by uploads that were started but never completed or aborted.

**Exam trap:** transitions only make financial sense in one direction and only across certain jumps AWS allows directly; you cannot transition directly from Standard back down to Standard *cheaper* by re-uploading — and moving from Glacier back to Standard requires an explicit **restore** request (see retrieval tiers below), not a lifecycle rule.

## 4. Versioning

Versioning, once enabled on a bucket, keeps **every version of every object** ever written to a given key. A `DELETE` no longer erases data — it inserts a **delete marker** (the object appears "gone" via normal GET/LIST, but every prior version is still recoverable by version ID). Overwriting a key with a new `PUT` creates a new version rather than destroying the old one.

- Versioning states: **Unversioned (default)** → **Enabled** → **Suspended**. Once enabled, a bucket can never go back to "Unversioned" — only suspended (new writes stop getting versioned, but existing versions remain).
- **MFA Delete** is an extra layer that can be enabled alongside versioning: it requires MFA authentication to permanently delete a version or to change the bucket's versioning state at all — a strong protection against both accidental and malicious permanent deletion.
- This is the mechanism the exam wants you to name whenever a scenario describes "a developer accidentally overwrote/deleted a production object and we need it back."

**Exam trap:** versioning does **not** protect against a *bucket* being deleted (a bucket must be empty — of all versions and delete markers — to be deleted), and it multiplies storage cost if not paired with a lifecycle rule cleaning up noncurrent versions.

## 5. Encryption — server-side vs. client-side, and which KMS key

This is the module's most Domain-2-relevant section: know **who holds the key, who does the encrypting, and how it's expressed as a bucket/request setting.**

| Method | Who encrypts | Key managed by | Key visible to AWS? | Notes |
|---|---|---|---|---|
| SSE-S3 | S3 (server-side) | AWS, fully | N/A (never exposed) | AES-256; **default for all new objects since 2023** — zero configuration required; simplest option |
| SSE-KMS | S3 (server-side) | AWS KMS — AWS-managed (`aws/s3`) or your own customer-managed key (CMK) | No, KMS manages it | Adds an audit trail (CloudTrail logs every key usage), supports key policies for fine-grained control over who can decrypt; a CMK lets you set your own rotation schedule and revoke access independently of S3 permissions |
| SSE-C | S3 (server-side), using a key **you** supply per request | You, entirely — AWS never stores it | No — request-only, discarded after use | You must send the key (base64-encoded, plus its MD5) with every PUT/GET over **HTTPS only**; lose the key and the object is unrecoverable — AWS keeps no copy |
| Client-side encryption | Your application, before the object ever leaves your environment | You, entirely (e.g. via the AWS Encryption SDK or a KMS data key retrieved client-side) | No — AWS only ever sees ciphertext | Highest control/isolation; you own key management and rotation completely; use when compliance requires AWS to never see plaintext, even transiently |

**SSE-KMS quota/cost detail (a real exam trap):** every SSE-KMS `PUT`/`GET` is a call to KMS under the hood, which is billed per-request and subject to KMS API request-per-second quotas — a high-throughput workload can actually get throttled by KMS limits. **S3 Bucket Keys** solve this: a time-limited bucket-level key derived from your CMK is cached at the S3 layer, drastically cutting the number of calls that hit KMS directly, at no meaningful loss of security.

**AWS-managed vs. customer-managed KMS keys, decision points:**
- **AWS-managed key (`aws/s3`)** — zero setup, AWS rotates it automatically yearly, but you **cannot** control its key policy, cannot restrict which principals may decrypt beyond default S3 service permissions, and cannot disable/delete it.
- **Customer-managed key (CMK)** — you author the key policy (who can `kms:Decrypt`, `kms:Encrypt`, `kms:GenerateDataKey`), you control rotation, you get **per-key** CloudTrail visibility, and you can revoke/disable it instantly to cut off access to every object encrypted under it — the answer whenever a scenario requires "only specific roles may decrypt this data" or "must control and audit exactly who can access the encryption key."

**Encryption in transit:** independent of at-rest encryption — every S3 endpoint supports HTTPS, and you can **force TLS-only access** with a bucket policy condition:

```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
  "Condition": { "Bool": { "aws:SecureTransport": "false" } }
}
```

You can also **require encryption at upload time** with a `s3:x-amz-server-side-encryption` condition in a bucket policy, denying any `PutObject` that doesn't specify the required encryption header.

## 6. Presigned URLs

A presigned URL grants **temporary, credential-less access** to a specific object (GET or PUT) to whoever holds the URL, without that requester needing any AWS credentials or IAM identity of their own. The URL is generated by a principal (your backend, using its own IAM credentials) that already has permission on the object, and it embeds a signature valid until a specified **expiration time**.

```bash
aws s3 presign s3://my-bucket/uploads/user123-avatar.png --expires-in 300
```

This is the standard pattern for letting an **end user upload directly to S3** (e.g., a profile picture) without routing the file's bytes through your application server: your backend authenticates the user, generates a short-lived presigned PUT URL scoped to one key, and returns it to the client, which then uploads straight to S3. This reduces load on your servers and avoids ever handing the client real AWS credentials.

**Exam trap:** a presigned URL inherits the **permissions of the principal that generated it** and is only valid until it expires — it is not a substitute for a bucket policy or IAM policy, and if the generating principal's own permissions are revoked, previously issued (but not yet expired) URLs can stop working too.

## 7. Multipart upload

For large objects, S3 supports splitting an upload into independently-uploaded **parts** (each 5MB–5GB, except the last), uploaded in parallel, then reassembled server-side once all parts complete.

- **Required** for any object over **5GB** (S3's single-PUT maximum).
- **Recommended** by AWS starting around **100MB**, for improved throughput (parallelism) and resilience (a failed part can be retried individually instead of restarting the whole upload).
- Uploads can be **paused and resumed**; an upload that's abandoned mid-way leaves orphaned parts consuming storage and billing until explicitly aborted or cleaned up.
- **Exam trap:** always pair multipart upload usage with a lifecycle rule action `AbortIncompleteMultipartUpload` — otherwise failed/abandoned multipart uploads silently accumulate storage cost with nothing to show for it, since incomplete parts aren't visible via a normal object listing.

```bash
aws s3api create-multipart-upload --bucket my-bucket --key big-video.mp4
# ... upload-part for each chunk, each returns an ETag ...
aws s3api complete-multipart-upload --bucket my-bucket --key big-video.mp4 \
  --upload-id "<id>" --multipart-upload file://parts.json
```

## 8. S3 event notifications

S3 can publish an event whenever an action happens on a bucket — object created, removed, restored, or a replication event, among others — to one of several destinations:

| Destination | Best for |
|---|---|
| AWS Lambda | Direct, immediate processing (e.g., generate a thumbnail on upload) |
| Amazon SQS | Decoupled, durable queueing — a worker fleet pulls events at its own pace, natural backpressure |
| Amazon SNS | Fan-out to multiple independent subscribers at once (email, SMS, multiple Lambda functions, SQS queues) |
| Amazon EventBridge | Advanced filtering (by key prefix/suffix, metadata) and routing to many possible targets/rules, without needing per-destination S3 configuration for each one; also enables cross-account/cross-service event buses |

**Exam trap:** classic S3 event notifications (configured directly on the bucket, targeting Lambda/SQS/SNS) support a useful but limited filter (prefix/suffix only). If a scenario needs **richer filtering** (e.g., route only events for objects with a specific tag or metadata value, or fan events out to many independent rules/targets without bucket reconfiguration each time), the answer is to **enable EventBridge notifications** on the bucket and build EventBridge rules — this is the more modern, flexible pattern AWS steers new designs toward.

## 9. Access control: bucket policies vs. IAM policies vs. ACLs vs. Block Public Access

| Mechanism | Type | Scope | Notes |
|---|---|---|---|
| IAM policy | Identity-based | Attached to a user/group/role | Governs what that identity can do across any S3 bucket/resource it's granted |
| Bucket policy | Resource-based | Attached to the bucket itself, JSON | Can grant access to **other AWS accounts** or make objects public; evaluated alongside IAM policies (explicit Deny anywhere wins, per module 00's evaluation logic) |
| ACL (Access Control List) | Legacy, resource-based | Bucket or individual object | Coarse-grained (predefined grants like `public-read`); **AWS now recommends disabling ACLs entirely** via the "Bucket owner enforced" Object Ownership setting, using only policies instead |
| S3 Block Public Access | Account or bucket-level setting | Overrides everything | Can force-block public bucket policies/ACLs even if one is misconfigured to allow public access — the exam's preferred "prevent accidental public exposure" answer |

Access to any given request is the union of what identity-based (IAM) and resource-based (bucket) policies allow, minus any explicit Deny anywhere (including Block Public Access, which behaves like a hard override) — same evaluation model as core IAM from module 00.

**Exam trap:** "How do we guarantee a bucket can never accidentally become public, even if someone attaches an overly permissive bucket policy later?" → **S3 Block Public Access**, not just "write a careful bucket policy." It's a dedicated safety net layered on top of policy correctness, not a replacement for it.

## 10. Static website hosting

S3 buckets can serve static content (HTML/CSS/JS/images) directly over HTTP as a website: you enable the **static website hosting** property, specify an index document (e.g. `index.html`) and optionally an error document, and the bucket gets a website endpoint (`bucket-name.s3-website-region.amazonaws.com`). Because this is public web content, it typically requires a bucket policy granting `s3:GetObject` to everyone (`Principal: "*"`), which means Block Public Access must be selectively relaxed for that bucket.

**Exam trap:** the native S3 website endpoint is **HTTP only** — no HTTPS, no custom domain with a valid cert out of the box. To get HTTPS + a custom domain + caching + lower latency, put **CloudFront** in front of the bucket (covered in depth in module 15). This CloudFront-in-front-of-S3 pattern is extremely common across scenarios in later modules; recognize it as the answer whenever a stem mentions "HTTPS," "custom domain," or "reduce latency for global users" alongside S3-hosted static content.

## 11. S3 Transfer Acceleration

Uses CloudFront's global network of edge locations as entry points for uploads: a client uploads to a nearby edge location over a distinct accelerated endpoint (`bucket-name.s3-accelerate.amazonaws.com`), and the data travels the rest of the way to the bucket's Region over AWS's optimized backbone network instead of the public internet. This meaningfully speeds up uploads (and downloads) for users **geographically far from the bucket's Region** — think a global user base uploading to a bucket in a single Region. It's a bucket-level opt-in setting, has an extra per-GB fee for the acceleration itself, and AWS provides a speed-comparison tool to check whether a given source location would actually benefit before enabling it.

## 12. S3 Select (and Glacier Select)

**S3 Select** lets you run a simple SQL-like query (`SELECT`, `WHERE`, basic expressions) directly against a **CSV, JSON, or Parquet** object stored in S3, returning only the matching subset of data instead of the whole object. Because filtering happens inside S3, this cuts both the data transferred over the network and the amount your application has to parse/process client-side — often a large cost and latency win for big files where you only need a slice. **Glacier Select** provides the equivalent capability for querying archived Glacier data without a full restore.

```bash
aws s3api select-object-content \
  --bucket my-bucket --key data/events.csv \
  --expression "SELECT * FROM S3Object s WHERE s.status = 'FAILED'" \
  --expression-type SQL \
  --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}}' \
  --output-serialization '{"CSV": {}}' output.csv
```

## 13. Glacier retrieval tiers — how "cold" translates to wait time

Every Glacier-family class trades retrieval speed for cost. Retrieval tiers determine **how fast** you can get an object back once you request a restore:

| Class | Retrieval tier | Typical retrieval time |
|---|---|---|
| Glacier Instant Retrieval | (always instant) | Milliseconds |
| Glacier Flexible Retrieval | Expedited | 1–5 minutes |
| Glacier Flexible Retrieval | Standard | 3–5 hours |
| Glacier Flexible Retrieval | Bulk | 5–12 hours |
| Glacier Deep Archive | Standard | Within 12 hours |
| Glacier Deep Archive | Bulk | Within 48 hours |

An object in Glacier Flexible Retrieval or Deep Archive isn't directly downloadable — you must first submit a **restore request** naming the retrieval tier, wait for the restore to complete (a temporary copy becomes available for a duration you specify), and then download it as normal. **Exam trap:** "we need this specific archived compliance file back within a couple of hours, occasionally, without paying full Expedited-tier prices constantly" is the Standard retrieval tier's exact use case; "we need it back in minutes, rarely, cost is secondary" is Expedited; "we need it back in days and cost is the only thing that matters" is Bulk or Deep Archive.

## 14. Recap: S3 vs. EBS vs. EFS vs. instance store — which storage service when

Module 01 introduced EBS and instance store as EC2-attached storage; here's the full decision framework now that S3 and EFS are both in play.

| | S3 | EBS | EFS | Instance store |
|---|---|---|---|---|
| Type | Object storage | Block storage | File storage (NFS, POSIX) | Block storage (local) |
| Scope | Global namespace, Region-durable | AZ-scoped | Regional, multi-AZ | Physically tied to one host |
| Attach model | Accessed via HTTP(S) API/SDK, not "mounted" like a disk | Attaches to exactly one EC2 instance at a time (Multi-Attach io1/io2 is a narrow exception) | Mounted concurrently by many instances/AZs at once | Attached only to its own host |
| Durability/persistence | 11 nines, independent of any compute resource | Persists independently of instance lifecycle until deleted | Persists independently, elastic, no capacity planning | Ephemeral — lost on stop/terminate |
| Typical use | Static assets, backups, data lake, Lambda deployment packages, logs, any "store a file, fetch it later via API" need | Boot volumes, databases needing low-latency block access from one instance | Shared config/content across a fleet, CMS uploads, home directories, big data pipelines needing shared POSIX access | Cache, scratch space, buffers — data you can afford to lose |

**The one-line decision rule:** need it addressable over HTTP from anywhere, at any scale, with no capacity planning → **S3**. Need a traditional attached disk for one instance (especially a boot volume or database) → **EBS**. Need many instances mounting the *same* filesystem concurrently → **EFS**. Need the fastest possible local disk and can lose the data on replacement → **instance store**.

## 15. Worked real-world scenarios

**Scenario A — the media company's cost-vs-access tradeoff.** A media company stores millions of user-uploaded images. Images are accessed heavily for the first 30 days after upload (article is "current"), rarely afterward, and almost never after 6 months, but compliance requires keeping every image for 3 years, and editors occasionally need to instantly recover an image that was accidentally overwritten by a bad re-upload. The design: enable **versioning** on the bucket (protects against the accidental-overwrite scenario — editors restore a prior version by version ID), then attach a **lifecycle rule**: Standard for the first 30 days (matches heavy initial access), transition to Standard-IA at 30 days (still millisecond access, cheaper, matches the "rarely accessed but occasionally needed fast" pattern), transition to Glacier Deep Archive at 180 days (matches "almost never accessed," cheapest long-term option), and expire at 3 years to satisfy the retention requirement exactly — with a **separate noncurrent-version rule** transitioning and eventually expiring old versions so versioning's safety net doesn't balloon storage cost indefinitely.

**Scenario B — the compliance team that doesn't trust AWS with plaintext, even briefly.** A healthcare-adjacent company's compliance team mandates that sensitive documents must never exist as plaintext anywhere AWS's infrastructure could theoretically inspect them, even transiently during a server-side encryption operation. SSE-S3 and SSE-KMS are both immediately disqualified: both require the object to arrive at S3 as plaintext over TLS and get encrypted **server-side**, meaning AWS's infrastructure necessarily handles the plaintext bytes for the encryption step, even if only momentarily and even though the data is encrypted-at-rest afterward. SSE-C is also disqualified for the same reason — S3 still performs the actual encryption operation using the customer-supplied key. The only design that satisfies "AWS never sees plaintext" is **client-side encryption**: the application encrypts the document locally (e.g., using the AWS Encryption SDK with a data key sourced from a customer-managed KMS key) before it ever leaves the application's environment, and uploads only ciphertext. S3 stores ciphertext and has no ability to decrypt it without the application separately calling KMS.

**Scenario C — the upload bottleneck.** A mobile app lets users upload short video clips (up to 200MB) directly from their phones. The current design proxies every upload through the application's EC2 fleet, which is now the throughput bottleneck and a single point of failure during traffic spikes, and the security team is uncomfortable with the app ever holding long-lived AWS credentials on a mobile device. The fix: the mobile app authenticates to the backend as it already does, the backend (holding its own IAM permissions) generates a **presigned URL** scoped to a single object key with a short expiration (e.g., 5 minutes — just long enough to start the upload), and returns it to the device. The device uploads the video **directly to S3** using that URL — bypassing the EC2 fleet entirely for the actual bytes — and because the clip exceeds the ~100MB recommended threshold, the client uses **multipart upload** against that same presigned flow (presigned URLs can be generated per-part) for resilience against a dropped connection mid-upload. A lifecycle rule aborts any incomplete multipart upload after 24 hours to avoid orphaned-part storage costs from abandoned uploads.

## Key exam traps
- Durability (11 nines, same across nearly all classes) and availability (varies by class, 99.5%–99.99%) are two different numbers — don't conflate them.
- Standard-IA / One Zone-IA: 30-day minimum storage duration and a per-GB retrieval fee — bad fit for frequently-changing or frequently-deleted data.
- SSE-S3/SSE-KMS/SSE-C are all **server-side** (S3 or S3-with-your-key does the encrypting); only **client-side encryption** guarantees AWS never touches plaintext.
- A customer-managed KMS key (not the AWS-managed `aws/s3` key) is required whenever a scenario demands custom key policies, per-key audit trail, or the ability to independently revoke decrypt access.
- S3 Bucket Keys reduce KMS request volume/cost/throttling risk for high-throughput SSE-KMS workloads — remember this when a scenario mentions KMS request throttling alongside S3.
- Multipart upload is required over 5GB, recommended over ~100MB; always pair with a lifecycle rule to abort incomplete uploads.
- Presigned URLs inherit the generating principal's permissions and expire — they're a delegation mechanism, not a standalone access-control system.
- Block Public Access is the dedicated safety net against accidental public exposure — prefer it over "just write the bucket policy carefully" whenever a scenario asks for a guarantee.
- The native S3 static website endpoint is HTTP-only; HTTPS + custom domain + caching means CloudFront in front of the bucket.
- Glacier retrieval tier (Expedited/Standard/Bulk, or Deep Archive's Standard/Bulk) is chosen by balancing "how fast do we need it back" against "how much are we willing to pay" — match the scenario's stated urgency to the tier.
- Storage decision framework: S3 for API-addressable object storage at any scale, EBS for one instance's attached block volume, EFS for concurrent multi-instance shared file access, instance store for ephemeral local scratch/cache data.
