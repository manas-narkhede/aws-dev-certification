# Module 02 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Storage Classes & Tiers (1–20)

1. A media company stores user-uploaded images that are accessed heavily for the first month after upload, then rarely afterward. The team wants the most cost-effective storage class for images that are older than 30 days but still need millisecond-level retrieval when occasionally accessed. Which S3 storage class should they transition to after 30 days?
A) S3 Glacier Flexible Retrieval
B) S3 Standard-IA
C) S3 Glacier Deep Archive
D) S3 One Zone-IA

2. A company stores millions of objects in S3 with access patterns that change unpredictably — some objects are accessed frequently for weeks, then go dormant for months, while others show the opposite pattern. The team does not want to manage lifecycle rules to move objects between classes manually. Which storage class is designed for this scenario?
A) S3 Standard
B) S3 Intelligent-Tiering
C) S3 Standard-IA
D) S3 Glacier Instant Retrieval

3. A healthcare company must store compliance records for 7 years. The records are never accessed after initial upload unless a regulatory audit occurs, which happens roughly once every 2–3 years. Retrieval within 12 hours is acceptable during an audit, and cost must be minimized. Which storage class fits best?
A) S3 Standard
B) S3 Standard-IA
C) S3 Glacier Deep Archive
D) S3 One Zone-IA

4. A developer stores temporary thumbnail images in S3. These thumbnails can be regenerated from the original source images at any time, and the team wants to save approximately 20% compared to Standard-IA pricing. Which storage class is the best fit, given the data is reproducible?
A) S3 Standard
B) S3 One Zone-IA
C) S3 Glacier Flexible Retrieval
D) S3 Glacier Deep Archive

5. Which two statements correctly describe the relationship between durability and availability in Amazon S3?
A) Durability (11 nines for Standard) measures how likely an object is to be lost; availability measures how often the service is reachable and responsive
B) Availability varies by storage class (99.99% for Standard down to 99.5% for One Zone-IA), while durability is the same 11 nines across all classes except One Zone-IA
C) Durability and availability are the same metric expressed in different units
D) One Zone-IA has higher availability than S3 Standard
E) S3 Standard-IA has the same availability as S3 Standard

6. A company's application writes new objects to an S3 bucket every few minutes, then deletes and replaces them within hours. A developer suggested moving these objects to S3 Standard-IA to reduce storage costs. What is the primary problem with this suggestion?
A) Standard-IA does not support object deletion
B) Standard-IA has a minimum storage duration charge (30 days) and a per-GB retrieval fee, making it more expensive than Standard for frequently-deleted, frequently-accessed objects
C) Standard-IA only stores objects up to 1 MB in size
D) Standard-IA is not available in any AWS Region

7. A data analytics team stores large CSV files in S3. The files are accessed heavily when first created, then go untouched for months, and the team is unsure exactly when access will drop off for any given file. They want AWS to automatically optimize storage costs without any manual tier management or retrieval fees. Which S3 feature is designed for this?
A) S3 lifecycle policies with manually configured transitions
B) S3 Intelligent-Tiering, which moves objects between Frequent and Infrequent Access tiers automatically based on access patterns with no retrieval fees
C) S3 One Zone-IA with manual monitoring
D) S3 Glacier Flexible Retrieval with expedited retrieval

8. Which S3 storage class stores objects in only a single Availability Zone rather than redundantly across at least three AZs?
A) S3 Standard
B) S3 Standard-IA
C) S3 One Zone-IA
D) S3 Glacier Deep Archive

9. A company stores quarterly financial reports in S3. The reports are accessed frequently in the quarter they cover, rarely in the subsequent year, and almost never after that — but compliance requires 7-year retention with millisecond retrieval available at all times. Which storage class is the best fit for reports older than one year?
A) S3 Glacier Flexible Retrieval
B) S3 Glacier Deep Archive
C) S3 Glacier Instant Retrieval
D) S3 Standard

10. A developer notices that S3 Intelligent-Tiering charges a small per-object monitoring and automation fee. Under what circumstance would this fee make Intelligent-Tiering more expensive than simply using S3 Standard?
A) When storing a very large number of very small objects that are all accessed frequently — the per-object fee exceeds the savings from tiering
B) Intelligent-Tiering is always cheaper than Standard regardless of the number of objects
C) The monitoring fee only applies in the first month after enabling Intelligent-Tiering
D) The monitoring fee is waived for objects larger than 128 KB

11. What is the minimum billable object size for S3 Standard-IA?
A) 1 KB
B) 128 KB
C) 1 MB
D) There is no minimum billable object size

12. A startup wants to store log files that might be needed for debugging but are accessed less than once per month. The team wants fast retrieval when needed and the lowest possible cost. Which two storage classes should they evaluate? (Select TWO.)
A) S3 Standard-IA
B) S3 Glacier Instant Retrieval
C) S3 Standard
D) S3 Glacier Deep Archive
E) S3 One Zone-IA

13. A company is evaluating whether to use S3 Glacier Instant Retrieval or S3 Glacier Flexible Retrieval for archived audit data. The key difference affecting their decision is retrieval latency. Which statement correctly describes this difference?
A) Both classes offer millisecond retrieval with no difference in latency
B) Glacier Instant Retrieval provides millisecond retrieval; Glacier Flexible Retrieval requires minutes to hours depending on the retrieval tier chosen
C) Glacier Flexible Retrieval is faster than Glacier Instant Retrieval
D) Neither class supports retrieval without restoring from tape backup

14. A team stores reproducible data (generated thumbnails) that is rarely accessed. They want the cheapest infrequent-access storage class and are comfortable with the data being stored in a single Availability Zone. If the AZ experiences a total failure, the data can be regenerated. Which class fits?
A) S3 Standard-IA
B) S3 One Zone-IA
C) S3 Standard
D) S3 Glacier Deep Archive

15. Which S3 Intelligent-Tiering capability must be explicitly enabled and is not active by default?
A) Automatic movement between Frequent and Infrequent Access tiers
B) Optional Archive Instant Access, Archive Access, and Deep Archive Access tiers
C) The per-object monitoring fee
D) Millisecond retrieval from the Frequent Access tier

16. A developer wants to understand the cost implications of storing 1 million objects, each 64 KB, in S3 Standard-IA. What billing concern should they be aware of?
A) No concern — Standard-IA is always cheaper than Standard for any object size
B) Each object is billed at the 128 KB minimum, meaning the actual storage cost is roughly double what the raw data size suggests
C) Standard-IA does not accept objects smaller than 128 KB
D) Standard-IA bills only for the actual bytes stored, with no minimum

17. A company needs to archive data for regulatory compliance. The data must be retained for 180 days minimum, and retrieval is never expected to be needed in less than 48 hours. Cost must be minimized above all else. Which storage class is the best fit?
A) S3 Standard
B) S3 Glacier Flexible Retrieval
C) S3 Glacier Deep Archive
D) S3 Standard-IA

18. Which two statements about S3 storage classes are accurate? (Select TWO.)
A) S3 Standard offers 99.99% availability and stores objects across at least three Availability Zones
B) S3 Glacier Flexible Retrieval objects can be directly downloaded without a restore request
C) S3 One Zone-IA offers the same 11-nines durability as S3 Standard
D) S3 Standard-IA has no per-GB retrieval fee
E) S3 Intelligent-Tiering eliminates retrieval fees by automatically managing tier transitions

19. A news organization's articles reference images stored in S3. Images linked to trending articles are accessed millions of times per day, while older images may not be accessed for months. Which storage class is the correct choice for the trending images during their high-access period?
A) S3 Standard
B) S3 Standard-IA
C) S3 Glacier Instant Retrieval
D) S3 One Zone-IA

20. A developer argues that S3 One Zone-IA provides the same durability as S3 Standard. Is this accurate?
A) Yes, both provide 99.999999999% (11 nines) durability
B) No, One Zone-IA stores data in a single AZ and thus loses the multi-AZ durability guarantee that protects against an entire AZ's destruction
C) One Zone-IA provides higher durability than Standard
D) Durability is not a meaningful metric for any S3 storage class

### Lifecycle Policies (21–30)

21. A company wants to automatically move log files from S3 Standard to Standard-IA after 30 days, then to Glacier Flexible Retrieval after 90 days, and permanently delete them after 365 days. Which S3 feature automates this progression?
A) S3 Intelligent-Tiering
B) S3 lifecycle policies with transition and expiration actions
C) S3 versioning
D) S3 Block Public Access

22. A team has versioning enabled on a production bucket. Old versions of objects are consuming significant storage, but the team wants to keep the most recent version on Standard while automatically transitioning noncurrent versions to Glacier after 30 days and deleting them after one year. Which lifecycle rule configuration supports this?
A) A single lifecycle rule targeting current versions only
B) A lifecycle rule with NoncurrentVersionTransitions and NoncurrentVersionExpiration actions
C) Disabling versioning to remove old versions
D) A bucket policy denying access to old versions

23. A developer discovers that their S3 storage bill includes charges for incomplete multipart upload parts from failed uploads that were never completed or aborted. Which lifecycle rule action prevents this ongoing cost?
A) NoncurrentVersionExpiration
B) AbortIncompleteMultipartUpload, configured to clean up parts after a specified number of days
C) Transition to Glacier Flexible Retrieval
D) Enable S3 Intelligent-Tiering

24. Which of the following is NOT a valid lifecycle rule action?
A) Transition objects to a cheaper storage class after N days
B) Expire (permanently delete) objects after N days
C) Transition objects from Glacier back to S3 Standard automatically
D) Abort incomplete multipart uploads after N days

25. A lifecycle rule is configured to transition objects from Standard to Standard-IA after 30 days. An object is deleted after only 10 days. How is the storage billed for the deleted object?
A) Only for the 10 days the object existed
B) For the full 30-day minimum storage duration charge of Standard-IA, since the lifecycle rule had the object marked for IA transition
C) For 10 days at the Standard rate, since the object was deleted before the transition occurred and Standard has no minimum storage duration
D) For 90 days at the Glacier rate

26. A company has a lifecycle rule transitioning objects to Standard-IA at 30 days, then to Glacier Flexible Retrieval at 90 days. A compliance officer asks: can a lifecycle rule move objects from Glacier back to Standard automatically? What is the correct answer?
A) Yes, lifecycle rules support bidirectional transitions between any storage classes
B) No, transitioning from Glacier back to Standard requires an explicit restore request followed by a copy to Standard; lifecycle rules only transition in the archive direction
C) Only with S3 Intelligent-Tiering enabled
D) Only if MFA Delete is configured

27. Which two of the following are valid lifecycle rule filter criteria for scoping which objects a rule applies to? (Select TWO.)
A) Object key prefix (e.g., logs/)
B) Object tags
C) The IAM user who uploaded the object
D) The encryption algorithm used on the object
E) The AWS Region the bucket is located in

28. A team wants to keep only the 3 most recent versions of each object and automatically delete all older versions. Can a single lifecycle rule accomplish this?
A) Yes, lifecycle rules support a NoncurrentVersionExpiration action with a NoncurrentDays parameter that expires versions older than a specified number of days, effectively limiting the version count
B) No, lifecycle rules cannot target noncurrent versions at all
C) Yes, lifecycle rules have a "keep N versions" parameter that directly specifies the number of versions to retain
D) No, this requires a custom Lambda function with no lifecycle rule involvement

29. A developer configures a lifecycle rule with the following transitions: Standard → Standard-IA at 30 days, Standard-IA → Glacier Flexible Retrieval at 90 days, Glacier Flexible Retrieval → Glacier Deep Archive at 180 days. Which statement about this configuration is accurate?
A) Objects must wait in each class for the minimum storage duration before the next transition can occur, and the total days must be cumulative from object creation
B) Each transition timer resets to zero when the object changes class
C) Lifecycle rules cannot chain more than two transitions
D) The transitions execute in reverse order, from cheapest to most expensive

30. A company's bucket has no lifecycle rules and uses multipart upload extensively for large video files. Over time, numerous abandoned uploads accumulate. What is the primary operational risk of not configuring a lifecycle rule to abort incomplete multipart uploads?
A) The abandoned parts will automatically delete themselves after 24 hours
B) The incomplete parts continue to consume storage and incur charges indefinitely until manually aborted or cleaned up by a lifecycle rule
C) Incomplete multipart uploads do not consume any storage
D) The abandoned parts will corrupt existing completed objects

### Versioning (31–40)

31. A developer accidentally overwrites a critical configuration file stored as an S3 object. The bucket has versioning enabled. How can the developer recover the previous version?
A) Contact AWS Support to restore from a backup tape
B) Retrieve the previous version by specifying its version ID in a GET request, since versioning preserves every version of every object
C) The previous version is permanently lost regardless of versioning
D) Delete the bucket and recreate it to trigger a rollback

32. When versioning is enabled, what happens when a DELETE request is sent for an object without specifying a version ID?
A) The object and all its versions are permanently deleted
B) A delete marker is inserted, making the object appear deleted via normal GET/LIST, but all previous versions remain recoverable
C) The most recent version is permanently deleted while older versions are preserved
D) The DELETE request is rejected with an error

33. A security team wants to ensure that even if an administrator's credentials are compromised, no one can permanently delete object versions or change the bucket's versioning state without additional multi-factor authentication. Which S3 feature addresses this?
A) S3 Block Public Access
B) MFA Delete
C) Server-side encryption with SSE-KMS
D) S3 Transfer Acceleration

34. Once versioning is enabled on an S3 bucket, can it be returned to the "unversioned" state?
A) Yes, versioning can be fully disabled and reverted to the unversioned state
B) No, once enabled, versioning can only be suspended (new writes stop getting versioned, but existing versions remain); it cannot revert to the original unversioned state
C) Yes, but only by deleting and recreating the bucket
D) Yes, by contacting AWS Support

35. A company has versioning enabled on a bucket with millions of objects. Each object has been updated dozens of times, resulting in hundreds of millions of noncurrent versions. Storage costs have grown significantly. What is the recommended approach to control these costs while keeping versioning enabled?
A) Disable versioning entirely
B) Configure lifecycle rules with NoncurrentVersionTransitions (to cheaper classes) and NoncurrentVersionExpiration (to delete old versions after a retention period)
C) Delete the bucket and recreate it without versioning
D) Contact AWS Support to request a storage credit

36. Which of the following statements about S3 versioning is accurate?
A) Versioning protects against accidental bucket deletion
B) An S3 bucket must be completely empty — including all versions and delete markers — before it can be deleted
C) Versioning doubles the availability SLA of the bucket
D) Versioning automatically transitions old versions to Glacier

37. A developer wants to undo a delete operation on a versioned object that currently shows a delete marker as its latest version. What action restores the object?
A) Re-upload the object from scratch, since delete markers are permanent
B) Delete the delete marker itself (by specifying its version ID in a DELETE request), which causes the most recent non-deleted version to become current again
C) Enable MFA Delete, which automatically reverses all delete markers
D) Create a new bucket and copy the object from the old bucket

38. Which two of the following are true about S3 versioning behavior? (Select TWO.)
A) When an object is overwritten in a versioned bucket, the new data becomes the current version while all previous versions are preserved
B) A DELETE without a version ID permanently removes the object and all versions
C) A delete marker makes the object appear deleted via standard GET but previous versions remain accessible by version ID
D) Versioning can be enabled on a per-object basis rather than per-bucket
E) Suspended versioning deletes all existing versions from the bucket

39. A company uses S3 versioning as part of their data protection strategy. A junior developer asks whether versioning alone is sufficient to protect against all data loss scenarios. What is the most accurate response?
A) Yes, versioning protects against every possible data loss scenario including accidental bucket deletion and Region-wide outages
B) Versioning protects against accidental overwrites and deletes (of individual objects), but does not protect against bucket deletion (bucket must be empty first), and for cross-Region disaster recovery, cross-Region replication should be added
C) Versioning provides no protection against any form of data loss
D) Versioning is only useful when combined with S3 Glacier

40. What is the versioning state of a newly created S3 bucket by default?
A) Enabled
B) Suspended
C) Unversioned
D) MFA Delete required

### Encryption (41–58)

41. A company wants the simplest possible encryption configuration for their S3 bucket, requiring zero setup or key management. All objects should be encrypted at rest automatically. Which server-side encryption method is the default and simplest option?
A) SSE-KMS with a customer-managed key
B) SSE-S3 (AES-256, managed entirely by AWS, default for all new objects since 2023)
C) SSE-C
D) Client-side encryption

42. A financial services company needs an audit trail in CloudTrail for every time an S3 object is encrypted or decrypted, and wants the ability to control which IAM principals can decrypt the data through a key policy, independent of the S3 bucket policy. Which encryption method provides these capabilities?
A) SSE-S3
B) SSE-KMS with a customer-managed key (CMK)
C) SSE-C
D) No S3 encryption method supports CloudTrail auditing of key usage

43. A company's security policy requires that the encryption key never be stored by AWS in any form — the application must provide the key with every PUT and GET request, and AWS discards it immediately after use. Which encryption method meets this requirement?
A) SSE-S3
B) SSE-KMS
C) SSE-C, where the customer supplies the encryption key per request and AWS never stores it
D) Client-side encryption

44. A healthcare company's compliance mandate states that sensitive documents must never exist as plaintext anywhere on AWS infrastructure, even transiently during a server-side encryption operation. Which encryption approach is the only option that satisfies this requirement?
A) SSE-S3
B) SSE-KMS with an AWS-managed key
C) SSE-C
D) Client-side encryption, where the application encrypts data before uploading to S3, ensuring AWS only ever receives ciphertext

45. A high-throughput application using SSE-KMS experiences intermittent throttling errors on S3 PUT and GET operations. The team discovers that each operation generates a separate call to AWS KMS, hitting the KMS request-per-second quota. Which S3 feature reduces the number of KMS API calls without switching away from SSE-KMS?
A) S3 Transfer Acceleration
B) S3 Bucket Keys, which cache a time-limited bucket-level key derived from the CMK, reducing direct KMS calls
C) S3 Intelligent-Tiering
D) Enabling versioning

46. What is the key distinction between an AWS-managed KMS key (aws/s3) and a customer-managed KMS key when used with SSE-KMS?
A) There is no functional difference between the two
B) An AWS-managed key is fully controlled by AWS with automatic yearly rotation, no custom key policy, and cannot be disabled or deleted; a customer-managed key gives you full control over the key policy, rotation schedule, and the ability to disable or delete the key
C) Customer-managed keys cannot be used with S3
D) AWS-managed keys provide stronger encryption than customer-managed keys

47. A developer wants to ensure that no object can be uploaded to a bucket without server-side encryption. Which mechanism enforces this requirement?
A) Enable versioning
B) A bucket policy with a condition denying PutObject requests that lack the required encryption header (s3:x-amz-server-side-encryption)
C) A lifecycle rule
D) S3 Block Public Access

48. Which two of the following are accurate statements about S3 encryption? (Select TWO.)
A) SSE-S3, SSE-KMS, and SSE-C are all server-side encryption methods where S3 performs the encryption operation
B) Client-side encryption means the application encrypts data before uploading, ensuring AWS never sees plaintext
C) SSE-C stores the customer-provided key alongside the encrypted object for future retrieval
D) SSE-KMS does not support CloudTrail auditing of key usage
E) SSE-S3 requires the customer to provide an encryption key with every request

49. A company wants to force all traffic to their S3 bucket to use HTTPS (TLS) and reject any HTTP requests. Which mechanism accomplishes this?
A) Enable SSE-S3 encryption
B) A bucket policy with a Deny for s3:* when aws:SecureTransport is false
C) Enable S3 Transfer Acceleration
D) Configure a lifecycle rule requiring HTTPS

50. A team uses SSE-KMS with a customer-managed key to encrypt objects in a shared bucket. They want to ensure that only a specific IAM role can decrypt these objects, even if other roles have s3:GetObject permission on the bucket. How can they enforce this restriction?
A) This is not possible — any role with s3:GetObject can always decrypt SSE-KMS objects
B) Configure the customer-managed KMS key's key policy to allow kms:Decrypt only for the specific IAM role, thereby preventing other roles from decrypting even if they have S3-level read access
C) Use SSE-S3 instead, which provides per-role decryption control
D) Use a lifecycle rule to restrict decryption

51. A developer using SSE-C accidentally loses the encryption key used to encrypt a specific object. Can the object be recovered?
A) Yes, AWS retains a backup copy of all SSE-C keys
B) No, SSE-C keys are never stored by AWS; if the customer loses the key, the encrypted object is permanently unrecoverable
C) Yes, by contacting AWS Support within 30 days
D) Yes, by using the AWS-managed key as a fallback

52. Which encryption method requires that all requests (both PUT and GET) be made over HTTPS exclusively, as a protocol requirement rather than just a best practice?
A) SSE-S3
B) SSE-KMS
C) SSE-C, because the customer-supplied key travels with the request and must be protected in transit
D) All methods equally require HTTPS with no distinction

53. A scenario requires the team to: (1) control exactly which principals can decrypt objects via a key policy, (2) have per-key usage logged in CloudTrail, and (3) be able to instantly revoke all decrypt access to objects by disabling a single resource. Which encryption configuration satisfies all three requirements?
A) SSE-S3
B) SSE-KMS with an AWS-managed key
C) SSE-KMS with a customer-managed key (CMK), whose key policy controls access, whose usage is logged per-key in CloudTrail, and which can be disabled to instantly block all decryption
D) SSE-C

54. A company runs a machine learning pipeline that processes millions of S3 objects per second, all encrypted with SSE-KMS using a customer-managed key. After enabling S3 Bucket Keys, KMS throttling errors dropped significantly. Which statement best explains why?
A) S3 Bucket Keys bypass KMS entirely, using no key material
B) S3 Bucket Keys cache a time-limited data key derived from the CMK at the S3 layer, so most encrypt/decrypt operations use the cached key instead of calling KMS directly, dramatically reducing KMS API request volume
C) S3 Bucket Keys increase the KMS request quota
D) S3 Bucket Keys switch encryption to SSE-S3 transparently

55. Which of the following scenarios is the strongest fit for choosing SSE-KMS with a customer-managed key over SSE-S3?
A) The team wants the simplest possible encryption with zero key management
B) The team needs to control which principals can decrypt objects through a key policy, wants per-key CloudTrail audit logs, and needs the ability to disable the key to revoke access
C) The team wants to avoid any interaction with AWS KMS
D) The team wants the lowest possible request latency with no additional API calls per operation

56. A developer configures a bucket to use SSE-KMS with an AWS-managed key (aws/s3). A colleague asks whether they can customize the key policy to restrict who can decrypt objects under this key. What is the correct answer?
A) Yes, the AWS-managed key's policy is fully customizable
B) No, the AWS-managed key's policy is controlled by AWS and cannot be customized; for custom key policies, they must use a customer-managed key
C) AWS-managed keys do not actually encrypt anything
D) The key policy applies only to SSE-C, not SSE-KMS

57. Which two statements about encryption in transit for S3 are accurate? (Select TWO.)
A) S3 endpoints support HTTPS, and a bucket policy condition can deny non-HTTPS requests
B) Encryption in transit (HTTPS) and encryption at rest (SSE) are independent — enabling one does not automatically enable the other
C) SSE-S3 automatically enforces HTTPS for all requests
D) Encryption in transit is not supported for S3 in any Region
E) A lifecycle rule can enforce HTTPS requirements

58. A team wants to encrypt objects using keys they manage entirely outside of AWS, using the AWS Encryption SDK in their application, so that S3 only ever stores ciphertext. Which approach does this describe?
A) SSE-S3
B) SSE-KMS
C) SSE-C
D) Client-side encryption using the AWS Encryption SDK

### Presigned URLs (59–68)

59. A mobile application allows users to upload profile pictures directly to S3 without the mobile device needing any AWS credentials. The backend server generates a short-lived URL that the mobile client uses for the upload. What is this mechanism called?
A) S3 Transfer Acceleration
B) A presigned URL
C) A bucket policy
D) An S3 event notification

60. A developer generates a presigned PUT URL for a mobile client to upload a video file. The URL expires after 5 minutes. If the upload starts within the 5-minute window but takes 10 minutes to complete, what happens?
A) The upload fails because the URL expired before the upload finished
B) The upload succeeds because S3 validates the signature only at the start of the request, not during data transfer
C) The upload is automatically paused and resumed when a new URL is generated
D) S3 permanently blocks the client's IP address

61. A presigned URL is generated by an IAM user who has s3:PutObject permission on a specific bucket. Later, an administrator removes the user's s3:PutObject permission, but a previously issued presigned URL has not yet expired. Can a client still use that URL successfully?
A) Yes, the URL's signature is immutable and always works until expiration regardless of permission changes
B) No, because the presigned URL inherits the generating principal's permissions at the time of use, not at the time of generation; revoking the principal's permission causes the URL to fail even before expiration
C) Only if the bucket has versioning enabled
D) Only if the bucket policy explicitly allows presigned URL usage

62. Which statement correctly describes what a presigned URL is NOT suitable for?
A) Allowing temporary, credential-less access to upload or download a specific object
B) Replacing the need for IAM policies and bucket policies as the primary, permanent access control mechanism for a bucket
C) Enabling a frontend application to bypass the backend server for large file uploads
D) Granting time-limited access to a private object to an external party

63. A team generates presigned URLs for downloading confidential reports. A security auditor asks what controls limit the risk of URL sharing. Which two properties of presigned URLs address this? (Select TWO.)
A) A presigned URL expires after a configured time limit, after which it is no longer valid
B) A presigned URL is scoped to a specific object key and HTTP method (GET or PUT), limiting what operations it can perform
C) A presigned URL automatically rotates the underlying IAM credentials after every use
D) A presigned URL requires the recipient to have their own IAM role
E) A presigned URL is valid indefinitely until manually revoked

64. A developer wants to generate a presigned URL using the AWS CLI. Which command generates a URL that allows downloading an object for the next 300 seconds?
A) aws s3 cp s3://bucket/key --presign 300
B) aws s3 presign s3://bucket/key --expires-in 300
C) aws s3api generate-url --bucket bucket --key key --ttl 300
D) aws s3 share s3://bucket/key --duration 300

65. A company wants end users to upload large files (up to 200 MB) directly to S3 from a browser, bypassing the application servers entirely. The application backend authenticates the user and generates a presigned PUT URL. What additional S3 feature should the client use for resilience during these large uploads?
A) S3 versioning
B) Multipart upload, potentially with per-part presigned URLs, for resilient parallel uploading of large files
C) S3 Block Public Access
D) S3 lifecycle policies

66. What is the maximum expiration time a presigned URL can be configured with when generated using temporary credentials from an IAM role (e.g., via STS AssumeRole)?
A) 7 days
B) The URL's maximum validity is bounded by the temporary credentials' session duration, typically up to 12 hours for role-assumed sessions, not the URL's own expiration parameter
C) There is no maximum; presigned URLs can be valid indefinitely
D) 1 hour, with no exceptions

67. A company generates presigned GET URLs to allow authenticated users to download private files from S3. A developer asks whether CORS headers need to be configured on the bucket for browser-based downloads using these URLs. What is the correct answer?
A) No, presigned URLs bypass CORS entirely
B) Yes, if the browser-based JavaScript code makes the request cross-origin, the bucket must return appropriate CORS headers regardless of whether the URL is presigned
C) CORS only applies to public buckets
D) CORS is never relevant for S3

68. Which of the following is the primary security advantage of using presigned URLs for direct-to-S3 uploads from mobile clients, compared to embedding IAM access keys in the mobile application?
A) Presigned URLs provide permanent access to the bucket
B) Presigned URLs are short-lived, scoped to a specific object and method, and never expose the generating principal's actual AWS credentials to the client
C) Presigned URLs encrypt the uploaded data automatically
D) Presigned URLs are faster than using IAM credentials

### Multipart Upload (69–76)

69. A developer needs to upload a 7 GB file to S3. Which upload mechanism is required for this file size?
A) A single PUT request, since S3 supports objects up to 10 GB in a single upload
B) Multipart upload, because S3's single PUT maximum is 5 GB, and objects larger than that require multipart upload
C) S3 Transfer Acceleration, which replaces the need for multipart upload
D) A presigned URL, which automatically splits the upload

70. At what file size does AWS recommend starting to use multipart upload for improved throughput and resilience, even though it's not strictly required?
A) 1 MB
B) 100 MB
C) 1 GB
D) 5 GB

71. A developer starts a multipart upload, uploads 10 of 20 parts, then the upload process crashes. The 10 uploaded parts remain in S3. What is the operational risk if no cleanup action is taken?
A) The uploaded parts are automatically deleted after 1 hour
B) The incomplete parts continue consuming storage and incurring charges until the upload is explicitly completed, aborted, or cleaned up by a lifecycle rule
C) The incomplete parts do not consume any storage
D) S3 automatically completes the upload using the available parts

72. Which two benefits does multipart upload provide compared to a single PUT for a 500 MB file? (Select TWO.)
A) Parts can be uploaded in parallel, improving throughput
B) A failed individual part can be retried without restarting the entire upload
C) Multipart upload bypasses the need for S3 permissions
D) Multipart upload automatically encrypts each part with a different key
E) Multipart upload reduces storage costs compared to a single PUT

73. What is the recommended lifecycle rule action to prevent abandoned multipart uploads from accumulating storage costs?
A) NoncurrentVersionExpiration
B) AbortIncompleteMultipartUpload
C) Transition to Glacier
D) Enable S3 Intelligent-Tiering

74. A company uploads files ranging from 50 MB to 4 GB to S3. The uploads frequently fail due to network instability. The team wants the ability to resume a failed upload from the last successfully uploaded chunk rather than starting from the beginning. Which S3 feature enables this?
A) S3 versioning
B) Multipart upload, which allows individual parts to be retried independently
C) S3 Transfer Acceleration
D) S3 event notifications

75. What is the size range for individual parts in a multipart upload (excluding the last part)?
A) 1 KB to 1 MB
B) 5 MB to 5 GB
C) 100 MB to 5 GB
D) Any size with no constraints

76. A developer initiates a multipart upload, uploads all parts, but forgets to call the CompleteMultipartUpload API. What is the state of the object?
A) The object is fully visible and accessible in the bucket
B) The object is not assembled or visible; the uploaded parts remain as incomplete upload fragments consuming storage until explicitly completed or aborted
C) S3 automatically completes the upload after 24 hours
D) The parts are automatically deleted after the upload times out

### Event Notifications (77–86)

77. A company wants to automatically generate a thumbnail every time an image is uploaded to their S3 bucket. Which S3 feature triggers the thumbnail generation?
A) S3 lifecycle policies
B) S3 event notifications, configured to invoke a Lambda function on object-created events
C) S3 versioning
D) S3 Transfer Acceleration

78. A developer configures an S3 event notification to send object-created events to an SQS queue. A worker fleet of EC2 instances pulls messages from the queue to process uploaded files. What is the primary benefit of using SQS as the notification destination compared to invoking Lambda directly?
A) SQS is faster than Lambda for processing events
B) SQS provides durable, decoupled queueing with natural backpressure — the worker fleet processes events at its own pace, and messages are retained if workers are temporarily unavailable
C) SQS is the only valid destination for S3 event notifications
D) SQS automatically processes the files without any worker code

79. A team needs to fan out S3 object-created events to three independent processing pipelines simultaneously (a thumbnail generator, a metadata indexer, and a notification sender). Which notification destination enables this fan-out pattern most naturally?
A) Lambda (a single function handling all three)
B) SNS, which can fan out to multiple independent subscribers (Lambda functions, SQS queues, or other targets) from a single topic
C) SQS, which processes events sequentially in one queue
D) S3 Transfer Acceleration

80. A company's existing S3 event notification configuration sends events to a Lambda function filtered by the prefix "uploads/" and suffix ".jpg". The team now needs additional events routed to a different Lambda function based on object metadata tags, plus events sent to an EventBridge rule for cross-account processing. What is the recommended approach?
A) Configure multiple overlapping S3 event notifications on the bucket, each with different tag-based filters
B) Enable EventBridge notifications on the bucket, which supports richer filtering (beyond prefix/suffix) and routing to many targets/rules without per-destination bucket configuration
C) Replace S3 with EFS for event support
D) Disable all notifications and use manual polling instead

81. Which two of the following are valid S3 event notification destinations? (Select TWO.)
A) AWS Lambda
B) Amazon SQS
C) Amazon DynamoDB
D) Amazon EC2 directly
E) AWS CodePipeline directly

82. A developer configures an S3 event notification but notices that the target Lambda function is not being invoked. The function exists and works when invoked manually. What is the most likely cause?
A) S3 event notifications do not support Lambda as a destination
B) The Lambda function's resource-based policy does not grant s3.amazonaws.com permission to invoke it
C) The S3 bucket must be in the same Availability Zone as the Lambda function
D) Event notifications only work with versioned buckets

83. Which S3 event notification event type would trigger when an object is permanently removed from a bucket?
A) s3:ObjectCreated:*
B) s3:ObjectRemoved:*
C) s3:Replication:*
D) s3:ReducedRedundancyLostObject

84. A team wants to trigger a CodePipeline execution whenever a new application artifact is uploaded to a specific S3 bucket prefix. Which approach enables this?
A) Configure a direct S3 event notification to CodePipeline
B) Enable EventBridge notifications on the bucket and create an EventBridge rule that matches the upload event and targets CodePipeline
C) Use a lifecycle rule to trigger CodePipeline
D) Configure S3 Transfer Acceleration to notify CodePipeline

85. A company processes uploaded files using both a real-time Lambda function (for immediate processing) and an SQS-backed worker fleet (for batch processing). They need both to receive the same S3 event. Which architecture supports this?
A) Configure two separate S3 event notifications pointing to Lambda and SQS respectively for the same event type
B) Configure the S3 event notification to publish to SNS, which then fans out to both the Lambda function and the SQS queue as subscribers
C) Configure S3 to call Lambda, which then writes to SQS manually — no fan-out option exists
D) S3 can only send events to one destination per event type

86. Classic S3 event notifications (configured directly on the bucket) support filtering by which criteria?
A) Object key prefix and suffix only
B) Object metadata tags, size, and encryption type
C) The IAM principal who uploaded the object
D) The storage class of the object

### Access Control: Bucket Policies, IAM, ACLs, Block Public Access (87–98)

87. A developer needs to grant a Lambda function in a different AWS account read access to objects in an S3 bucket. Which combination of mechanisms enables cross-account access? (Select TWO.)
A) A bucket policy on the S3 bucket granting s3:GetObject to the other account's IAM role
B) An IAM policy attached to the Lambda function's execution role granting s3:GetObject on the bucket's ARN
C) S3 Block Public Access configured to allow all public access
D) A lifecycle rule granting cross-account permissions
E) S3 versioning with MFA Delete

88. A company wants to guarantee that an S3 bucket can never be made publicly accessible, even if someone accidentally attaches a bucket policy with Principal: "*". Which S3 feature provides this safeguard?
A) S3 versioning
B) S3 Block Public Access
C) SSE-KMS encryption
D) S3 Transfer Acceleration

89. Which statement correctly describes the relationship between IAM policies and S3 bucket policies in determining access to an object?
A) Only the IAM policy matters; bucket policies are ignored
B) Access is determined by the union of what both policies allow, minus any explicit Deny from either — an explicit Deny anywhere overrides any Allow
C) Only the bucket policy matters; IAM policies are ignored
D) IAM policies and bucket policies cannot be used simultaneously on the same bucket

90. AWS now recommends disabling ACLs on S3 buckets in favor of using policies exclusively. Which Object Ownership setting achieves this?
A) Object writer
B) Bucket owner enforced
C) Bucket owner preferred
D) ACL required

91. A developer creates a bucket policy that grants s3:GetObject to Principal: "*" for all objects in the bucket. However, the bucket's S3 Block Public Access settings include "Block public access through any newly created public bucket policies." What is the effective result?
A) The bucket is publicly accessible because the bucket policy overrides Block Public Access
B) The bucket is NOT publicly accessible because Block Public Access acts as a hard override, blocking the bucket policy's public grant
C) Block Public Access only applies to ACLs, not bucket policies
D) The bucket policy is automatically deleted

92. Which of the following is NOT a capability of S3 Block Public Access?
A) Blocking public access granted through ACLs
B) Blocking public access granted through bucket policies
C) Encrypting objects at rest
D) Being applied at the account level to affect all buckets

93. A company has a bucket policy that denies s3:PutObject unless the request includes a specific encryption header. A developer with full s3:* permissions in their IAM policy tries to upload an unencrypted object. What happens?
A) The upload succeeds because the IAM policy's Allow overrides the bucket policy's Deny
B) The upload is denied because an explicit Deny in the bucket policy overrides any Allow from the IAM policy
C) The IAM policy and bucket policy cancel each other out, resulting in no action
D) The bucket policy is ignored for users with full s3:* permissions

94. A company stores sensitive financial data in S3 and wants only a specific IAM role (used by their auditing application) to access the data. All other principals, including administrators, should be denied access. Which mechanism most directly achieves this?
A) S3 Block Public Access
B) A bucket policy with an explicit Deny for all principals except the specific IAM role
C) S3 versioning
D) S3 Intelligent-Tiering

95. Which two statements about S3 ACLs are accurate? (Select TWO.)
A) ACLs are a legacy access control mechanism that AWS recommends replacing with bucket and IAM policies
B) ACLs provide fine-grained, condition-based access control equivalent to bucket policies
C) ACLs can grant predefined permissions like "public-read" at the bucket or object level
D) ACLs are the only way to grant cross-account access to S3 objects
E) ACLs automatically encrypt objects they apply to

96. A team configures S3 Block Public Access at the AWS account level with all four settings enabled. A developer in the same account creates a new bucket and tries to attach a bucket policy with Principal: "*". What is the outcome?
A) The bucket policy is successfully attached and the bucket becomes public
B) The bucket policy is prevented from granting public access because the account-level Block Public Access settings override it
C) Account-level Block Public Access settings do not affect individual buckets
D) The developer's IAM permissions are automatically revoked

97. A bucket policy uses the condition key aws:SecureTransport to deny non-HTTPS requests. A request arrives over HTTP. What happens?
A) The request succeeds because aws:SecureTransport is not a valid condition key
B) The request is denied because the bucket policy explicitly denies requests where aws:SecureTransport is false (i.e., non-HTTPS)
C) The request is automatically redirected to HTTPS
D) The condition key only applies to GET requests, not PUT requests

98. A developer wants to restrict S3 access so that objects can only be accessed from within a specific VPC, not from the public internet. Which mechanism supports this?
A) A lifecycle rule restricting access by VPC ID
B) A bucket policy with a condition restricting access to a specific VPC endpoint (aws:sourceVpce) or VPC ID (aws:sourceVpc)
C) S3 Block Public Access alone, with no additional configuration
D) S3 Transfer Acceleration, which inherently restricts access to VPC traffic

### Static Website Hosting (99–104)

99. A company hosts a static website (HTML, CSS, JavaScript, images) on S3. Users report that the site loads over HTTP but not HTTPS. What explains this limitation?
A) S3 static website endpoints do not support HTTPS natively; HTTPS with a custom domain requires placing CloudFront in front of the S3 bucket
B) S3 static websites always support HTTPS by default
C) The bucket policy is blocking HTTPS requests
D) S3 does not support hosting static files

100. A developer enables static website hosting on an S3 bucket but users receive 403 Forbidden errors when trying to access the site. What is the most likely cause?
A) The bucket does not have versioning enabled
B) The bucket does not have a bucket policy granting s3:GetObject to Principal: "*", and/or S3 Block Public Access settings are blocking the required public access
C) Static website hosting requires SSE-KMS encryption
D) The bucket is in the wrong AWS Region

101. A company wants to host a static website at www.example.com with HTTPS, a custom domain, and global caching. Which architecture is the standard solution?
A) S3 static website hosting alone, which supports all of these
B) S3 for storage with CloudFront as the CDN providing HTTPS (via ACM certificate), custom domain (via Route 53 alias), and global edge caching
C) EC2 instances serving the static files
D) API Gateway with a Lambda backend rendering the HTML

102. Which two files are typically configured when enabling S3 static website hosting? (Select TWO.)
A) An index document (e.g., index.html) specifying the default page
B) An error document (e.g., error.html) specifying the page shown for 4xx errors
C) A Lambda function handler for server-side rendering
D) A database connection string for dynamic content
E) A CodePipeline configuration file

103. A single-page application (SPA) hosted on S3 behind CloudFront uses client-side routing (e.g., React Router). Users navigating to deep links like /dashboard/settings receive a 403 error because no S3 object exists at that path. What is the standard fix?
A) Create an S3 object for every possible client-side route
B) Configure CloudFront to return the index.html page for 403/404 errors (custom error responses), allowing the client-side router to handle the path
C) Disable client-side routing in the application
D) Switch from S3 to EC2 for hosting

104. A company is serving a static website from S3 with CloudFront in front. They want to prevent users from bypassing CloudFront and accessing the S3 bucket's website endpoint directly. Which CloudFront feature restricts access to the S3 origin?
A) S3 Block Public Access alone
B) CloudFront Origin Access Control (OAC), which restricts the S3 bucket to accept requests only from CloudFront
C) A lifecycle rule
D) S3 Transfer Acceleration

### S3 Transfer Acceleration & S3 Select (105–112)

105. A global user base uploads video files to an S3 bucket in us-east-1. Users in Asia and Europe experience slow upload speeds due to the geographic distance. Which S3 feature uses CloudFront's global edge network to speed up these uploads?
A) S3 event notifications
B) S3 Transfer Acceleration
C) S3 Intelligent-Tiering
D) S3 versioning

106. Which endpoint format does a client use when uploading via S3 Transfer Acceleration?
A) bucket-name.s3.amazonaws.com
B) bucket-name.s3-accelerate.amazonaws.com
C) bucket-name.s3-website.amazonaws.com
D) bucket-name.s3-edge.amazonaws.com

107. A developer stores a 10 GB CSV file in S3 and needs to retrieve only the rows where the status column equals "FAILED". Downloading the entire file and filtering client-side would be slow and expensive. Which S3 feature allows filtering the data server-side before transfer?
A) S3 Transfer Acceleration
B) S3 Select, which runs a SQL-like query on CSV, JSON, or Parquet objects and returns only the matching subset
C) S3 Intelligent-Tiering
D) S3 versioning

108. S3 Select supports which data formats for server-side querying?
A) Only CSV
B) CSV, JSON, and Parquet
C) Only Parquet and Avro
D) Any binary format

109. A company regularly queries a 50 GB JSON file stored in S3 to extract a small subset of records. Using S3 Select instead of downloading the full file would reduce which two cost/performance factors? (Select TWO.)
A) Data transfer costs and bandwidth consumption
B) Client-side parsing and processing time
C) S3 storage costs for the file itself
D) The number of AZs the file is replicated across
E) The object's encryption key rotation schedule

110. Which of the following correctly describes S3 Transfer Acceleration's pricing model?
A) Transfer Acceleration is included at no additional cost with every S3 bucket
B) Transfer Acceleration has an additional per-GB fee for accelerated transfers, and AWS provides a speed comparison tool to verify that a given source location would benefit before enabling it
C) Transfer Acceleration is free for uploads but charges for downloads
D) Transfer Acceleration charges a flat monthly fee regardless of usage

111. A developer wants to query archived data stored in Glacier without performing a full restore. Which AWS feature supports this?
A) S3 lifecycle policies
B) Glacier Select, which allows running SQL-like queries on Glacier data without a full restore
C) S3 Transfer Acceleration
D) S3 versioning

112. When would S3 Transfer Acceleration NOT provide a meaningful speed improvement?
A) When uploading from a location geographically close to the bucket's Region
B) When uploading from a location far from the bucket's Region
C) When uploading large files
D) When uploading from multiple geographic locations simultaneously

### Storage Decision Framework: S3 vs. EBS vs. EFS vs. Instance Store (113–120)

113. A company needs to store application logs that are accessed via HTTP API calls from multiple microservices across different AWS Regions, with no capacity planning required. Which storage service is the best fit?
A) Amazon EBS
B) Amazon S3
C) Amazon EFS
D) Instance store

114. A relational database running on EC2 requires a persistent block storage volume with consistent low-latency IOPS, attached to a single instance. Which storage service fits?
A) Amazon S3
B) Amazon EBS
C) Amazon EFS
D) Instance store

115. A container-based application running on multiple EC2 instances across two Availability Zones needs a shared POSIX-compliant filesystem for reading and writing configuration files concurrently. Which storage service fits?
A) Amazon S3
B) Amazon EBS
C) Amazon EFS
D) Instance store

116. A high-performance computing application needs the fastest possible local disk I/O for temporary scratch data used during computation. The data can be regenerated if lost. Which storage option fits?
A) Amazon S3
B) Amazon EBS
C) Amazon EFS
D) Instance store

117. Which two statements correctly distinguish S3 from EBS? (Select TWO.)
A) S3 is object storage accessed via HTTP API; EBS is block storage attached to EC2 instances
B) S3 requires capacity provisioning; EBS does not
C) EBS volumes are scoped to a single Availability Zone; S3 objects are durably stored across multiple AZs within a Region
D) S3 can serve as a boot volume for EC2 instances
E) EBS provides higher durability (more nines) than S3

118. A developer needs to choose between S3 and EFS for storing user-uploaded documents that will be processed by a fleet of EC2 instances. The instances need to read and write the documents using standard filesystem operations (open, read, write, close). Which storage service supports this requirement?
A) S3, since it supports standard filesystem operations natively
B) EFS, since it provides a POSIX-compliant filesystem mountable by multiple instances
C) Instance store, since it provides the fastest filesystem access
D) EBS, since it can be attached to multiple instances simultaneously

119. A Lambda function needs to read a configuration file at startup. The file is updated weekly by a separate deployment process. Which storage service is the most practical choice for this use case?
A) Instance store
B) EBS
C) S3
D) EFS

120. Which of the following one-line decision rules for AWS storage services is accurate?
A) Need a traditional attached disk for one instance → S3; need HTTP-addressable object storage → EBS
B) Need HTTP-addressable object storage at any scale with no capacity planning → S3; need a block volume for one instance → EBS; need shared POSIX filesystem across instances → EFS; need fastest local disk tolerant of data loss → instance store
C) EFS is the default choice for all storage needs
D) Instance store provides the highest durability of any AWS storage option

### Integrative Scenarios (121–125)

121. A company stores user-uploaded documents in S3 with the following requirements: (1) documents must be encrypted with a key the company controls via a key policy, (2) access patterns are unpredictable — some documents are accessed daily while others are never accessed again, (3) the company wants AWS to handle tier optimization automatically, and (4) all uploads must go directly from the client browser to S3 without passing through the application server. Which combination of S3 features addresses all four requirements?
A) SSE-S3 encryption, S3 Standard storage class, a bucket policy granting public write access
B) SSE-KMS with a customer-managed key, S3 Intelligent-Tiering, presigned PUT URLs for direct browser uploads
C) Client-side encryption, S3 Glacier Deep Archive, S3 Transfer Acceleration
D) SSE-C encryption, S3 Standard-IA, a hardcoded IAM access key in the browser JavaScript

122. A media company's workflow is as follows: a photographer uploads a 500 MB RAW image from a remote location to S3, which triggers a Lambda function to generate a compressed web-ready version. The photographer is in Australia and the bucket is in us-east-1, resulting in slow uploads. The team also discovers that several abandoned multipart uploads from failed upload attempts are accumulating storage charges. Which combination of changes addresses both the slow uploads and the orphaned parts?
A) Enable S3 Transfer Acceleration for faster uploads from distant locations, and add a lifecycle rule with AbortIncompleteMultipartUpload to clean up failed uploads automatically
B) Switch from S3 to EBS for faster uploads
C) Enable versioning to speed up uploads
D) Move the bucket to the Australia Region and disable event notifications

123. A company's security review of an S3 bucket finds the following issues: (1) objects are encrypted with SSE-S3, but the security team requires per-key CloudTrail audit logs and the ability to revoke decrypt access through a key policy, (2) the bucket has no Block Public Access configured, and a junior developer recently attached a bucket policy granting Principal: "*", and (3) incomplete multipart uploads are consuming significant storage. Which combination of changes addresses all three findings?
A) Switch to SSE-KMS with a customer-managed key for audit/revocation control, enable S3 Block Public Access to prevent public bucket policies, and add a lifecycle rule to abort incomplete multipart uploads
B) Switch to SSE-C for audit logs, disable versioning, and delete the bucket
C) Keep SSE-S3 and add a lifecycle rule only
D) Enable S3 Transfer Acceleration to address all three issues

124. A startup is building a content management system. User-uploaded images are accessed millions of times in the first week, then rarely accessed for the next year, and must be retained for 3 years with instant retrieval always available. The images are served globally via CloudFront. When an image is accidentally deleted or overwritten, the content team needs to recover the previous version. Finally, all images must be encrypted with a key the company can audit per-key in CloudTrail. Which combination of S3 features builds this system?
A) Versioning for recovery, a lifecycle rule (Standard → Standard-IA at 30 days → Glacier Instant Retrieval at 365 days, expire at 3 years), SSE-KMS with a customer-managed key, and CloudFront with OAC for global delivery
B) No versioning, S3 Glacier Deep Archive from day one, SSE-S3, and S3 Transfer Acceleration
C) Versioning, Standard-IA from day one, client-side encryption, and direct S3 website hosting
D) No versioning, S3 Standard only, SSE-C, and a bucket policy granting public access

125. A company migrating from on-premises to AWS needs a storage solution for three distinct workloads: (1) a public-facing static website with HTTPS and a custom domain, (2) a relational database requiring low-latency attached block storage, and (3) a shared configuration directory mounted concurrently by 50 EC2 instances across multiple AZs. Which AWS storage services correctly match each workload, in order?
A) EBS for the website, S3 for the database, instance store for the shared directory
B) S3 (with CloudFront for HTTPS/custom domain) for the website, EBS for the database, EFS for the shared directory
C) EFS for all three workloads
D) Instance store for the website, EFS for the database, S3 for the shared directory

---

## Answer Key & Explanations

1. B — Standard-IA provides millisecond retrieval with lower storage cost than Standard, ideal for infrequently accessed data still needing fast access.
2. B — Intelligent-Tiering automatically moves objects between tiers based on access patterns with no retrieval fees, matching unpredictable patterns perfectly.
3. C — Glacier Deep Archive is the cheapest class, with 180-day minimum and 12-48 hour retrieval, matching the stated tolerance for slow retrieval and minimal cost.
4. B — One Zone-IA is ~20% cheaper than Standard-IA and suitable for reproducible, non-critical data.
5. A & B — Durability measures data loss probability; availability measures service reachability. Availability varies by class while durability is consistently 11 nines except One Zone-IA's AZ-scope risk.
6. B — Standard-IA's 30-day minimum charge and retrieval fee make it more expensive than Standard for frequently-deleted, frequently-accessed objects.
7. B — Intelligent-Tiering automatically optimizes without manual lifecycle management and charges no retrieval fees.
8. C — One Zone-IA stores data in a single AZ, unlike all other classes which use at least three AZs.
9. C — Glacier Instant Retrieval provides millisecond access at low cost for data accessed roughly quarterly, with a 90-day minimum.
10. A — The per-object monitoring fee can exceed savings when many small objects are all frequently accessed and wouldn't benefit from tiering.
11. B — Standard-IA bills at a minimum of 128 KB per object.
12. A & B — Standard-IA and Glacier Instant Retrieval both provide fast retrieval for infrequently accessed data at different price/access-frequency tradeoffs.
13. B — Glacier Instant Retrieval is milliseconds; Glacier Flexible Retrieval ranges from minutes (Expedited) to hours (Standard/Bulk).
14. B — One Zone-IA is the cheapest IA option and suits reproducible data where single-AZ risk is acceptable.
15. B — Archive-tier options within Intelligent-Tiering must be explicitly opted into.
16. B — 64 KB objects are billed at the 128 KB minimum, roughly doubling effective storage cost.
17. C — Glacier Deep Archive has a 180-day minimum matching the requirement and the lowest cost, with 48-hour retrieval acceptable.
18. A & E — S3 Standard uses 3+ AZs with 99.99% availability; Intelligent-Tiering's automatic tier management eliminates retrieval fees.
19. A — S3 Standard provides the highest availability and throughput for frequently accessed, high-traffic content.
20. B — One Zone-IA stores data in a single AZ, so an AZ-level failure could cause data loss, unlike Standard's multi-AZ design.
21. B — Lifecycle policies with transition and expiration actions automate the described tiered progression.
22. B — NoncurrentVersionTransitions and NoncurrentVersionExpiration target old versions specifically.
23. B — AbortIncompleteMultipartUpload cleans up orphaned parts after a configured number of days.
24. C — Lifecycle rules cannot transition objects from Glacier back to Standard; that requires an explicit restore request.
25. C — The object was deleted before the transition occurred, so only Standard-rate billing applies for the 10 days it existed.
26. B — Lifecycle rules transition toward archive classes only; returning from Glacier requires a restore request followed by a copy.
27. A & B — Lifecycle rules can be scoped by key prefix and/or object tags.
28. A — NoncurrentVersionExpiration with NoncurrentDays expires versions older than a specified number of days, indirectly controlling version count over time.
29. A — Transition days are cumulative from object creation, and objects must stay in each class for its minimum storage duration.
30. B — Incomplete parts consume storage and incur charges until explicitly cleaned up.
31. B — Versioning preserves every version; the previous version is retrieved by specifying its version ID.
32. B — A DELETE without a version ID inserts a delete marker; previous versions remain recoverable.
33. B — MFA Delete requires multi-factor authentication for permanent version deletion or versioning state changes.
34. B — Once enabled, versioning can only be suspended, never returned to the unversioned state.
35. B — Lifecycle rules with NoncurrentVersionTransitions and NoncurrentVersionExpiration control old-version costs.
36. B — A bucket must be completely empty (all versions and delete markers) before it can be deleted.
37. B — Deleting the delete marker by its version ID restores the most recent non-deleted version.
38. A & C — Overwrites create new versions while preserving old ones; delete markers hide objects while versions remain accessible by ID.
39. B — Versioning protects individual objects from accidental overwrites/deletes but not against bucket deletion or Region-level disasters.
40. C — New buckets start in the unversioned state by default.
41. B — SSE-S3 is the default encryption (since 2023), requiring zero setup or key management.
42. B — SSE-KMS with a CMK provides CloudTrail audit logs per-key and custom key policies for access control.
43. C — SSE-C requires the customer to supply the key per request; AWS never stores it.
44. D — Client-side encryption ensures AWS only receives ciphertext, never handling plaintext even transiently.
45. B — S3 Bucket Keys cache a derived key, reducing the number of direct KMS API calls.
46. B — AWS-managed keys offer zero setup but no custom control; CMKs offer full key policy, rotation, and disable/delete control.
47. B — A bucket policy condition on s3:x-amz-server-side-encryption denies unencrypted uploads.
48. A & B — SSE-S3/KMS/C are all server-side; client-side encryption keeps plaintext off AWS entirely.
49. B — A bucket policy denying requests where aws:SecureTransport is false enforces HTTPS.
50. B — The CMK's key policy can restrict kms:Decrypt to a specific role, independent of S3 bucket permissions.
51. B — SSE-C keys are never stored by AWS; loss means permanent data inaccessibility.
52. C — SSE-C requires HTTPS as a protocol requirement since the key travels with the request.
53. C — A CMK provides key policy control, per-key CloudTrail logging, and the ability to disable the key to block all decryption.
54. B — S3 Bucket Keys cache a derived data key at the S3 layer, reducing direct KMS API calls.
55. B — CMK provides key policy control, per-key audit, and revocation capability that SSE-S3 cannot offer.
56. B — AWS-managed key policies are controlled by AWS and not customizable; CMKs provide custom key policies.
57. A & B — HTTPS is supported and enforceable via bucket policy; encryption in transit and at rest are independent mechanisms.
58. D — Client-side encryption with the AWS Encryption SDK encrypts data before upload; S3 only stores ciphertext.
59. B — A presigned URL grants temporary, credential-less access to a specific object.
60. B — S3 validates the presigned URL's signature at request initiation, not during data transfer.
61. B — Presigned URLs inherit the generating principal's permissions at the time of use; revoking permissions causes the URL to fail.
62. B — Presigned URLs are a temporary delegation mechanism, not a replacement for permanent IAM/bucket policies.
63. A & B — Presigned URLs expire after a configured time and are scoped to a specific object and HTTP method.
64. B — aws s3 presign s3://bucket/key --expires-in 300 generates a presigned URL valid for 300 seconds.
65. B — Multipart upload with presigned URLs enables resilient parallel uploading of large files directly to S3.
66. B — When generated with STS temporary credentials, the URL's validity is bounded by the session duration.
67. B — Browser-based cross-origin requests require CORS headers on the bucket regardless of presigned URL usage.
68. B — Presigned URLs are short-lived, narrowly scoped, and never expose real AWS credentials to the client.
69. B — Multipart upload is required for objects over 5 GB (S3's single-PUT maximum).
70. B — AWS recommends multipart upload starting around 100 MB for improved throughput and resilience.
71. B — Incomplete parts consume storage and incur charges until completed, aborted, or cleaned up by a lifecycle rule.
72. A & B — Parallel part uploads improve throughput; individual failed parts can be retried without restarting the entire upload.
73. B — AbortIncompleteMultipartUpload is the lifecycle action that cleans up abandoned multipart uploads.
74. B — Multipart upload allows resuming from the last successful part rather than restarting the entire upload.
75. B — Individual parts must be between 5 MB and 5 GB (the last part can be smaller).
76. B — Without CompleteMultipartUpload, the object is not assembled; parts remain as fragments consuming storage.
77. B — S3 event notifications invoke a Lambda function when a new object is created.
78. B — SQS provides durable, decoupled queueing with natural backpressure for asynchronous processing.
79. B — SNS fans out events to multiple independent subscribers from a single notification.
80. B — EventBridge offers richer filtering and flexible multi-target routing beyond S3's native prefix/suffix filtering.
81. A & B — Lambda and SQS are valid S3 event notification destinations (SNS and EventBridge are also valid).
82. B — The Lambda function's resource-based policy must grant s3.amazonaws.com permission to invoke it.
83. B — s3:ObjectRemoved:* events fire when an object is permanently deleted.
84. B — EventBridge rules can match S3 events and target CodePipeline (S3 cannot notify CodePipeline directly).
85. B — SNS fans out the same event to both Lambda and SQS as independent subscribers.
86. A — Classic S3 event notifications filter by key prefix and suffix only; richer filtering requires EventBridge.
87. A & B — Cross-account S3 access requires both a bucket policy granting the external role and an IAM policy on that role.
88. B — S3 Block Public Access prevents public access regardless of bucket policy or ACL configuration.
89. B — Access is the union of IAM and bucket policy Allows, minus any explicit Deny from either.
90. B — "Bucket owner enforced" disables ACLs, making policies the sole access control mechanism.
91. B — Block Public Access overrides the bucket policy's public grant, keeping the bucket private.
92. C — Block Public Access controls public access; it does not encrypt objects.
93. B — An explicit Deny in a bucket policy overrides any Allow from IAM policies.
94. B — A bucket policy with an explicit Deny for all except the specific role enforces exclusive access.
95. A & C — ACLs are legacy and provide coarse-grained predefined grants; AWS recommends policies instead.
96. B — Account-level Block Public Access prevents any bucket in the account from being made public.
97. B — The condition denies requests where aws:SecureTransport is false (HTTP requests).
98. B — A bucket policy with aws:sourceVpce or aws:sourceVpc conditions restricts access to VPC-originated requests.
99. A — S3 static website endpoints are HTTP-only; HTTPS requires CloudFront in front.
100. B — Static website hosting requires a bucket policy granting public GetObject access, and Block Public Access must not block it.
101. B — S3 + CloudFront (with ACM for HTTPS, Route 53 for the domain, and edge caching) is the standard architecture.
102. A & B — An index document and an optional error document are configured when enabling static website hosting.
103. B — CloudFront custom error responses returning index.html for 403/404 errors let the SPA's client-side router handle deep links.
104. B — CloudFront Origin Access Control (OAC) restricts the S3 bucket to accept requests only from CloudFront.
105. B — S3 Transfer Acceleration uses edge locations to speed up uploads from geographically distant clients.
106. B — bucket-name.s3-accelerate.amazonaws.com is the Transfer Acceleration endpoint.
107. B — S3 Select runs SQL-like queries on the object server-side, returning only matching data.
108. B — S3 Select supports CSV, JSON, and Parquet formats.
109. A & B — S3 Select reduces data transfer costs and client-side processing by filtering server-side.
110. B — Transfer Acceleration charges a per-GB fee and offers a speed comparison tool to verify benefit.
111. B — Glacier Select queries archived data without a full restore.
112. A — Transfer Acceleration provides minimal benefit when the source is already close to the bucket's Region.
113. B — S3 is HTTP-addressable, globally accessible, requires no capacity planning, ideal for log storage.
114. B — EBS provides persistent, low-latency block storage attached to a single EC2 instance.
115. C — EFS provides a shared POSIX filesystem mountable concurrently by multiple instances across AZs.
116. D — Instance store offers the fastest local I/O for temporary, loss-tolerant data.
117. A & C — S3 is HTTP-based object storage; EBS is AZ-scoped block storage. S3 is multi-AZ durable.
118. B — EFS provides POSIX filesystem semantics (open/read/write/close) mountable by multiple instances.
119. C — S3 is the practical choice for a file read by Lambda at startup, updated weekly.
120. B — This accurately maps each storage service to its ideal use case.
121. B — CMK for key policy control, Intelligent-Tiering for automatic optimization, presigned URLs for direct browser uploads.
122. A — Transfer Acceleration speeds distant uploads; AbortIncompleteMultipartUpload cleans up failed uploads.
123. A — CMK for audit/revocation, Block Public Access for safety, lifecycle rule for multipart cleanup.
124. A — Versioning for recovery, tiered lifecycle for cost optimization, CMK for auditable encryption, CloudFront with OAC for global HTTPS delivery.
125. B — S3+CloudFront for static website, EBS for database block storage, EFS for shared concurrent filesystem.
