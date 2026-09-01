# Module 14 — Practice Questions (135)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Task Statement 2.1: Authentication and Authorization (1–45)

1. A mobile application needs to authenticate users using Google and Apple social identity providers, as well as an internal user directory with email/password authentication. Once authenticated, the application must obtain user profile attributes and authorization tokens. Which Amazon Cognito component should the developer use as the identity provider?
A) Amazon Cognito User Pools
B) Amazon Cognito Identity Pools
C) AWS IAM Identity Center only
D) AWS Secrets Manager

2. A single-page web application (SPA) authenticates users via Amazon Cognito User Pools. Which OAuth 2.0 grant type is the MOST secure industry standard for authenticating public web clients without exposing client secrets?
A) Authorization Code Grant with Proof Key for Code Exchange (PKCE)
B) Implicit Grant
C) Resource Owner Password Credentials Grant
D) Client Credentials Grant

3. An application receives a JSON Web Token (JWT) from Amazon Cognito. The developer needs to inspect the token's claims on the server side to determine if the user belongs to the "Admins" group. In which section of the JWT is this claim located?
A) Header
B) Payload
C) Signature
D) Digest

4. What cryptographic mechanism does a backend microservice use to verify that an incoming JSON Web Token (JWT) was genuinely issued by an Amazon Cognito User Pool and has not been tampered with?
A) Verifying the JWT signature against the public JSON Web Key Set (JWKS) retrieved from `https://cognito-idp.<region>.amazonaws.com/<userPoolId>/.well-known/jwks.json`
B) Calling `sts:AssumeRole` with the token string
C) Encrypting the token with an AWS KMS Customer Managed Key
D) Querying Amazon DynamoDB for the raw password hash

5. A developer is designing an authorization flow for mobile users to upload photos directly to an Amazon S3 bucket (`my-photo-app-bucket`). Users authenticate with Amazon Cognito User Pools. How should the developer obtain temporary AWS credentials for the mobile app to call the S3 API directly?
A) Pass the Cognito User Pool ID Token to an Amazon Cognito Identity Pool to exchange it for temporary AWS IAM credentials via AWS STS
B) Store AWS IAM user access keys in the mobile application binary
C) Generate a static IAM user for each registered mobile user
D) Use AWS Systems Manager Parameter Store to download root credentials

6. Which claim inside a Cognito-issued JWT indicates whether the token is intended for identity verification (`id`) or API authorization (`access`)?
A) `token_use`
B) `sub`
C) `iss`
D) `aud`

7. What is the primary difference between Amazon Cognito User Pools and Amazon Cognito Identity Pools?
A) User Pools handle authentication (user directory and JWT issuance); Identity Pools handle authorization (exchanging tokens for temporary AWS IAM credentials)
B) User Pools are for EC2; Identity Pools are for Lambda
C) Identity Pools are only for corporate SAML federation; User Pools are for social login only
D) User Pools issue IAM access keys; Identity Pools issue JWTs

8. A developer wants to restrict authenticated mobile app users so that each user can ONLY query and write items in an Amazon DynamoDB table where the partition key matches their unique Cognito Identity ID. Which condition key must be included in the IAM policy attached to the authenticated role?
A) `"Condition": { "ForAllValues:StringEquals": { "dynamodb:LeadingKeys": ["${cognito-identity.amazonaws.com:sub}"] } }`
B) `"Condition": { "StringEquals": { "aws:username": "${aws:PrincipalArn}" } }`
C) `"Condition": { "NumericEquals": { "dynamodb:Select": 1 } }`
D) `"Condition": { "Bool": { "aws:MultiFactorAuthPresent": "true" } }`

9. An enterprise uses Microsoft Active Directory Federation Services (AD FS) for employee authentication. The company wants employees to access the AWS Management Console and CLI using their existing corporate credentials. Which AWS STS API is used for enterprise identity federation using SAML 2.0?
A) `AssumeRoleWithSAML`
B) `AssumeRoleWithWebIdentity`
C) `GetSessionToken`
D) `GetCallerIdentity`

10. A GitHub Actions CI/CD workflow needs to deploy infrastructure to an AWS account without storing long-lived AWS Access Keys in GitHub repository secrets. Which AWS STS API action and identity pattern enables secure, keyless OIDC authentication?
A) Configure an OIDC Identity Provider in IAM for GitHub Actions, and have the workflow call `AssumeRoleWithWebIdentity` to exchange the GitHub OIDC token for temporary AWS credentials
B) Store IAM root access keys in GitHub Secrets
C) Use `GetSessionToken` with hardcoded credentials
D) Create an S3 pre-signed URL for the repository

11. A developer is configuring an IAM policy. The policy contains an `Allow` statement for `s3:GetObject`, but an attached Permissions Boundary contains a `Deny` statement for `s3:*`. What is the result when the user attempts to download an S3 object?
A) Access is Denied, because an explicit Deny in any applicable policy (including permissions boundaries and SCPs) overrides any Allow statement
B) Access is Allowed because identity policies take precedence over boundaries
C) S3 prompts the user for MFA
D) The object is downloaded in encrypted format

12. What does an IAM Permissions Boundary define for an IAM entity (user or role)?
A) The maximum permissions that an identity-based policy can grant to the entity
B) The password expiration policy
C) The maximum number of EC2 instances the user can launch
D) The encryption key used by the user

13. A company uses AWS Organizations. The administrator attaches a Service Control Policy (SCP) to an Organizational Unit (OU) that denies `dynamodb:*`. A developer in a member account in that OU is assigned the `AdministratorAccess` IAM policy. Can the developer create a DynamoDB table?
A) No, SCPs act as guardrails that set the maximum allowable permissions for all accounts in an OU; an explicit Deny in an SCP cannot be overridden by account administrators or IAM policies
B) Yes, because `AdministratorAccess` overrides SCPs
C) Yes, if the table is created using CloudFormation
D) Only if the developer uses the AWS CLI

14. An application running on an Amazon EC2 instance needs to read messages from an Amazon SQS queue. What is the AWS best practice for providing AWS credentials to the application?
A) Assign an IAM Role with an attached least-privilege policy to the EC2 instance via an Instance Profile
B) Hardcode the AWS Access Key ID and Secret Access Key in the application configuration file
C) Store credentials in an unencrypted S3 bucket
D) Embed the root account password in EC2 User Data

15. What are two advantages of using IAM Roles with temporary credentials over long-lived IAM User Access Keys? (Select TWO.)
A) Credentials rotate automatically without requiring manual credential updates or application redeployment
B) Eliminates the security risk of hardcoded or leaked static access keys in source control
C) Eliminates the need for IAM policies
D) Bypasses all AWS KMS encryption fees
E) Increases EC2 network bandwidth

16. A developer needs to grant an AWS Lambda function in Account A (`111122223333`) permission to write objects to an Amazon S3 bucket located in Account B (`444455556666`). What two configurations are required? (Select TWO.)
A) Attach an IAM policy to the Lambda execution role in Account A allowing `s3:PutObject` on the Account B bucket ARN
B) Configure the S3 Bucket Policy in Account B allowing `s3:PutObject` from the Lambda Execution Role ARN in Account A
C) Create an IAM User in Account B with administrator privileges
D) Enable S3 Transfer Acceleration on the bucket
E) Delete all security groups in Account A

17. Which AWS STS API call allows an IAM user with MFA enabled to generate temporary credentials that include MFA validation metadata for calling privileged APIs?
A) `GetSessionToken`
B) `AssumeRoleWithWebIdentity`
C) `DecodeAuthorizationMessage`
D) `GetAccessKeyInfo`

18. A developer receives an encoded authorization failure message when an API call is denied. Which AWS STS API action can decrypt the error message to inspect the exact policy evaluation details?
A) `sts:DecodeAuthorizationMessage`
B) `sts:GetCallerIdentity`
C) `sts:AssumeRole`
D) `sts:GetSessionToken`

19. In Amazon Cognito User Pools, what feature allows developers to run custom business logic (such as auto-confirming users, migrating legacy passwords, or enriching JWT tokens with custom claims) during the authentication lifecycle?
A) Cognito Lambda Triggers (e.g., Pre-Authentication, Pre-Token Generation, Post-Confirmation)
B) Amazon S3 Event Notifications
C) AWS Step Functions only
D) Amazon SNS SMS publishing

20. A developer wants to inject a custom claim `tenant_id` into the Cognito ID Token during user login. Which Cognito Lambda Trigger should be configured?
A) Pre Token Generation Lambda Trigger
B) Post Authentication Lambda Trigger
C) Pre Sign-up Lambda Trigger
D) Custom Message Lambda Trigger

21. What token issued by Amazon Cognito User Pools is used by a client application to silently obtain a new Access Token and ID Token without forcing the user to re-enter their username and password?
A) Refresh Token
B) Session Token
C) Identity Token
D) Bearer Header

22. What is the default lifespan of an Amazon Cognito User Pool Access Token and ID Token?
A) 60 minutes (1 hour), configurable from 5 minutes up to 24 hours
B) 24 hours fixed
C) 30 days fixed
D) 5 minutes fixed

23. A backend REST API deployed on Amazon API Gateway needs to authorize incoming requests based on user roles embedded in Cognito User Pool JWTs. What API Gateway feature provides native, serverless validation of Cognito JWT tokens?
A) Amazon Cognito User Pool Authorizer
B) API Gateway Usage Plans
C) API Gateway API Keys
D) Route 53 Geolocation

24. If an API Gateway REST API requires custom authorization logic (such as checking an external database or caching authorization decisions), what type of authorizer should be implemented?
A) Lambda Authorizer (Custom Authorizer, returning an IAM policy or simple response)
B) Cognito Authorizer only
C) API Gateway Client Certificate
D) AWS WAF Rate Rule

25. An application uses Amazon Cognito Identity Pools. The developer wants to allow unauthenticated (guest) users to view public catalog items in DynamoDB, while requiring registered users to log in to place orders. Does Cognito Identity Pools support this pattern?
A) Yes, by enabling "Enable access to unauthenticated identities" and assigning distinct IAM roles for Authenticated and Unauthenticated users
B) No, Cognito requires all users to create an account
C) Only if users provide a valid credit card
D) Only via Amazon SQS

26. What condition element in an IAM policy statement can restrict API access based on the source IP address of the caller?
A) `"Condition": { "IpAddress": { "aws:SourceIp": "203.0.113.0/24" } }`
B) `"Condition": { "StringEquals": { "aws:CurrentTime": "2026-01-01" } }`
C) `"Condition": { "Bool": { "aws:SecureTransport": "true" } }`
D) `"Condition": { "ArnEquals": { "aws:PrincipalArn": "arn:aws:iam::..." } }`

27. A developer wants to enforce that all API requests to an Amazon S3 bucket MUST use HTTPS (TLS encryption in transit). What condition block in the S3 bucket policy enforces this requirement?
A) `"Condition": { "Bool": { "aws:SecureTransport": "false" } }` with `Effect: Deny`
B) `"Condition": { "StringEquals": { "s3:x-amz-acl": "public-read" } }`
C) `"Condition": { "NumericLessThan": { "s3:TlsVersion": 1.2 } }`
D) `"Condition": { "Null": { "aws:PrincipalTag": "true" } }`

28. Which policy type is attached directly to resources like Amazon S3 buckets, AWS KMS keys, Amazon SQS queues, and AWS Lambda functions to control access permissions?
A) Resource-Based Policy
B) Identity-Based Policy
C) Permissions Boundary
D) Session Policy

29. What is the key difference between an IAM Identity-Based Policy and an IAM Resource-Based Policy regarding the `Principal` element?
A) Resource-Based policies MUST specify the `Principal` element to define who is allowed access; Identity-Based policies do NOT specify `Principal` because the principal is implicitly the entity the policy is attached to
B) Identity-Based policies must contain `Principal: "*"`
C) Resource-Based policies cannot use conditions
D) Both policies use identical syntax without `Principal`

30. A developer needs to determine the current AWS IAM user or role identity being used by the AWS CLI or SDK for debugging. Which STS API command should be executed?
A) `aws sts get-caller-identity`
B) `aws sts whoami`
C) `aws iam list-users`
D) `aws sts check-login`

31. An enterprise wants to delegate administrative access to third-party consultants to manage an RDS database in the company's AWS account. What is the most secure method to grant this access?
A) Create an IAM Role with a trust policy allowing the third-party AWS Account ID (and an External ID condition for confused deputy protection), allowing the consultants to assume the role
B) Email the third party an IAM user access key
C) Share the root account login credentials
D) Create a public S3 bucket containing the database connection string

32. What is the purpose of the `sts:ExternalId` condition key in an IAM role trust policy when delegating cross-account access to a third-party SaaS vendor?
A) It mitigates the "Confused Deputy" problem by requiring the third party to supply a secret shared identifier when assuming the role on behalf of the customer
B) It encrypts the network connection using TLS 1.3
C) It automatically rotates the IAM role ARN
D) It converts the role into an IAM group

33. A developer is designing role-based access control (RBAC) in Cognito User Pools. The application has two groups: `Students` and `Teachers`. How can different IAM roles be assigned to users in these groups when they authenticate via Cognito Identity Pools?
A) Configure "Role resolution" in the Cognito Identity Pool to use "Choose role from token" based on the user's Cognito group membership
B) Create two separate AWS accounts
C) Manually update IAM policies on each login
D) Store the IAM role secret key in local browser storage

34. What is the maximum session duration that can be configured for temporary credentials issued by `sts:AssumeRole`?
A) 12 hours (configurable from 15 minutes up to 12 hours)
B) 1 hour fixed
C) 30 days
D) 24 hours fixed

35. When an IAM policy has multiple condition blocks, such as checking both `aws:SourceIp` and `aws:PrincipalTag/Department`, how does AWS evaluate multiple conditions within a single statement?
A) All conditions must be satisfied simultaneously (logical AND) for the statement to apply
B) Only one condition needs to match (logical OR)
C) Conditions are evaluated in alphabetical order
D) AWS chooses one condition randomly

36. An application uses ABAC (Attribute-Based Access Control) to allow developers to manage only EC2 instances that have a tag `Project` matching the developer's IAM user tag `Project`. What condition key enables this dynamic tag matching?
A) `"Condition": { "StringEquals": { "aws:ResourceTag/Project": "${aws:PrincipalTag/Project}" } }`
B) `"Condition": { "StringEquals": { "aws:Tag": "Project" } }`
C) `"Condition": { "ArnEquals": { "aws:PrincipalArn": "Project" } }`
D) `"Condition": { "Bool": { "aws:SecureTransport": "true" } }`

37. What type of policy allows an IAM entity in Account A to assume an IAM Role in Account B?
A) A Trust Policy (a specific type of resource-based policy attached to the IAM Role in Account B defining trusted principals)
B) An S3 Bucket Policy
C) An Amazon Route 53 Routing Policy
D) A CloudWatch Metric Filter

38. A company wants to disable access to all AWS services outside of the `us-east-1` and `us-west-2` Regions across all member accounts in an organization. Which AWS Organizations feature implements this guardrail?
A) Service Control Policy (SCP) with a condition `"StringNotEquals": { "aws:RequestedRegion": ["us-east-1", "us-west-2"] }` and `Effect: Deny`
B) IAM Role Permissions Boundary
C) AWS WAF Regional Rule
D) Amazon Route 53 Latency Policy

39. What happens when a user requests an action on an AWS resource where NO matching policy exists (neither Allow nor Deny)?
A) The request is denied by default (Implicit Deny)
B) The request is allowed automatically
C) AWS sends an MFA prompt
D) The resource is deleted

40. An application receives a JWT containing the header `{"alg": "none"}`. How should the backend token validation logic handle this token?
A) Reject the token immediately because the `none` algorithm indicates an unsigned, insecure token that bypasses cryptographic integrity verification
B) Accept the token as an administrator token
C) Encrypt the token with SHA-1
D) Forward the token to Amazon S3

41. A developer wants to authenticate microservice-to-microservice API calls without human user interaction. Which OAuth 2.0 grant type is designed for machine-to-machine (M2M) server communication?
A) Client Credentials Grant
B) Authorization Code Grant
C) Implicit Grant
D) Device Code Grant

42. How does an application using the AWS SDK automatically locate and use temporary credentials provided by an EC2 Instance Profile or ECS Task Role?
A) The AWS SDK's default credential provider chain automatically queries the Instance Metadata Service (IMDSv2 at `http://169.254.169.254/latest/meta-data/iam/security-credentials/`) or ECS container metadata endpoint
B) By reading credentials from `/root/.aws/credentials`
C) By opening an SSH tunnel to IAM
D) By inspecting the DNS server

43. Why is IMDSv2 (Instance Metadata Service Version 2) recommended over IMDSv1 for securing EC2 instance credentials?
A) IMDSv2 is session-oriented and requires a session token acquired via an HTTP PUT request, preventing Server-Side Request Forgery (SSRF) vulnerabilities from stealing IAM role credentials
B) IMDSv2 is free while IMDSv1 costs $1 per request
C) IMDSv2 eliminates the need for IAM roles
D) IMDSv2 only supports IPv6

44. An application uses Amazon Cognito User Pools with Hosted UI. The developer wants to prevent unauthorized access if an authorization code is intercepted during redirect. What security mechanism accomplishes this?
A) PKCE (Proof Key for Code Exchange) using `code_verifier` and `code_challenge`
B) Disabling HTTPS
C) Storing credentials in plain text in the query string
D) Using unencrypted cookies

45. A developer wants to revoke all active refresh tokens for a specific Cognito user immediately after detecting suspicious account activity. Which Cognito API action achieves this?
A) `AdminUserGlobalSignOut` (or `GlobalSignOut`)
B) `DeleteUser`
C) `UpdateUserAttributes`
D) `ListUsers`

---

### Task Statement 2.2: Encryption at Rest and in Transit (46–90)

46. An e-commerce application stores sensitive credit card transaction logs in an Amazon S3 bucket. Compliance mandates that data must be encrypted at rest, and every encryption and decryption event must be audited with user identity and timestamp in AWS CloudTrail. Which S3 encryption method satisfies these compliance requirements?
A) Server-Side Encryption with AWS KMS Keys (SSE-KMS)
B) Server-Side Encryption with Amazon S3-Managed Keys (SSE-S3)
C) Server-Side Encryption with Customer-Provided Keys (SSE-C)
D) Unencrypted storage with HTTPS

47. What is the maximum data payload size that can be directly encrypted or decrypted using an AWS KMS Customer Master Key (CMK) in a single API call (`kms:Encrypt` or `kms:Decrypt`)?
A) 4 KB
B) 256 KB
C) 5 MB
D) 5 GB

48. A developer needs to encrypt 500 MB video files before uploading them to Amazon S3. Because the file size exceeds KMS's direct 4 KB limit, which cryptographic pattern must be used?
A) Envelope Encryption (using KMS `GenerateDataKey` to generate a plaintext data key for local encryption and storing the encrypted data key alongside the ciphertext)
B) Splitting the file into 4 KB chunks and calling KMS `Encrypt` 125,000 times
C) Base64 encoding the video file
D) Using Route 53 encryption

49. What two values are returned by the AWS KMS `GenerateDataKey` API call? (Select TWO.)
A) `Plaintext` (the 256-bit plaintext data key used by the application to encrypt data locally)
B) `CiphertextBlob` (the data key encrypted under the specified KMS Customer Master Key)
C) The raw private key of the AWS KMS HSM
D) An S3 pre-signed URL
E) An IAM user access key

50. After an application uses the `Plaintext` data key returned by `GenerateDataKey` to encrypt a large file in memory, what is the critical security step the application must perform immediately?
A) Erase/wipe the plaintext data key from memory to prevent memory-dump extraction
B) Print the plaintext data key to CloudWatch Logs for debugging
C) Store the plaintext key in a public S3 bucket
D) Email the plaintext key to the administrator

51. When an application needs to decrypt a file that was encrypted using Envelope Encryption, what API call is made to AWS KMS?
A) `kms:Decrypt` passing the `CiphertextBlob` (encrypted data key), which returns the `Plaintext` data key
B) `kms:GenerateDataKey`
C) `kms:Encrypt`
D) `kms:CreateKey`

52. What is the difference between AWS KMS `GenerateDataKey` and `GenerateDataKeyWithoutPlaintext`?
A) `GenerateDataKey` returns both the plaintext key and the encrypted key; `GenerateDataKeyWithoutPlaintext` returns ONLY the encrypted key (for scenarios where encryption will occur on a different component later)
B) `GenerateDataKeyWithoutPlaintext` is deprecated
C) `GenerateDataKeyWithoutPlaintext` does not use KMS master keys
D) `GenerateDataKey` is free while `GenerateDataKeyWithoutPlaintext` costs $10

53. An application uses Server-Side Encryption with Customer-Provided Keys (SSE-C) on Amazon S3. How does SSE-C manage cryptographic keys?
A) The client provides the raw 256-bit encryption key in the HTTP request headers (`x-amz-server-side-encryption-customer-key`); Amazon S3 performs the encryption/decryption in memory and immediately discards the key without storing it
B) AWS KMS manages and stores the key
C) Amazon S3 saves the customer key in a DynamoDB table
D) The customer key is stored in S3 object metadata in plaintext

54. What is the default encryption behavior for all newly created Amazon S3 buckets in AWS?
A) Default server-side encryption is automatically enabled using SSE-S3 (AES-256) at zero additional cost
B) Buckets are unencrypted by default
C) SSE-C is enforced automatically
D) All buckets require an SSL certificate from ACM

55. A security team enables "Automatic Key Rotation" on a Customer Managed Key (CMK) in AWS KMS. How often does AWS KMS automatically rotate the backing cryptographic key material?
A) Every 365 days (1 year)
B) Every 30 days
C) Every 90 days
D) Every 5 years

56. When a KMS Customer Managed Key undergoes automatic key rotation, what happens to the Key ID, Key ARN, and data previously encrypted with older key versions?
A) The Key ID and ARN remain unchanged; KMS retains previous backing keys to decrypt older data transparently without requiring data re-encryption
B) All previously encrypted data is deleted
C) The Key ARN changes and the application must be redeployed with the new Key ID
D) The developer must manually download and re-encrypt all historical data

57. Can automatic key rotation be enabled on asymmetric KMS keys (e.g., RSA or ECC key pairs)?
A) No, automatic key rotation is supported ONLY for symmetric encryption KMS keys
B) Yes, asymmetric keys rotate every 30 days
C) Yes, but only for ECC keys
D) Only in `us-east-1`

58. What is the difference between an AWS Managed Key (e.g., `aws/s3`, `aws/lambda`) and a Customer Managed Key (CMK) in AWS KMS?
A) AWS Managed Keys are created and rotated automatically by AWS with fixed key policies; Customer Managed Keys are created by the user, support custom key policies, manual rotation schedules, and cross-account sharing
B) Customer Managed Keys are free; AWS Managed Keys cost $1/month
C) AWS Managed Keys can be exported to on-premises servers
D) Customer Managed Keys do not support CloudTrail logging

59. A developer wants to provision a public SSL/TLS certificate for `api.example.com` to bind to an Application Load Balancer and Amazon CloudFront distribution. Which AWS service provides free public certificates with automated renewal?
A) AWS Certificate Manager (ACM)
B) AWS KMS
C) AWS Secrets Manager
D) AWS CloudHSM

60. Can a public SSL/TLS certificate generated by AWS Certificate Manager (ACM) be downloaded and installed directly on an EC2 instance or an Apache web server?
A) No, ACM public certificates are integrated exclusively with AWS managed services (CloudFront, ALB, NLB, API Gateway) and cannot be exported or downloaded as raw private keys
B) Yes, certificates can be exported via the ACM CLI
C) Yes, by paying an export fee of $5
D) Only if the EC2 instance runs Amazon Linux

61. What two domain validation methods are supported by AWS Certificate Manager (ACM) to prove domain ownership when requesting a public certificate? (Select TWO.)
A) DNS Validation (adding a CNAME record to the domain's DNS zone, which supports automated certificate renewal)
B) Email Validation (receiving a verification email sent to registered WHOIS contact addresses)
C) Phone Call Verification
D) Postal Mail Verification
E) In-Person Identity Verification

62. When should an organization choose ACM Private CA (AWS Private Certificate Authority) over standard AWS Certificate Manager public certificates?
A) When the organization needs to issue private SSL/TLS certificates for internal VPC microservices, internal servers, mobile devices, or IoT devices, or needs exportable private keys
B) When the organization wants free public certificates for CloudFront
C) When the application is hosted in Route 53
D) When the organization has no domain name

63. What is the role of an AWS KMS Key Policy?
A) It is a resource-based policy attached directly to the KMS key that defines the primary access controls and permissions for who can manage and use the key
B) It sets the price of the KMS key
C) It configures the VPC route table for KMS endpoints
D) It converts symmetric keys to asymmetric keys

64. What happens if an AWS KMS Customer Managed Key has a Key Policy that does NOT grant permissions to the AWS account root user (`"Principal": { "AWS": "arn:aws:iam::123456789012:root" }`) and does not grant permissions to any other IAM entity?
A) The key becomes unmanageable (orphaned), and only AWS Support can assist in recovering or deleting it
B) The key is automatically converted into an AWS Managed Key
C) IAM administrators can still access the key via `AdministratorAccess`
D) The key is deleted after 5 minutes

65. An application in Account A needs to decrypt S3 objects encrypted with a KMS CMK located in Account B. What two policy configurations are required to enable this cross-account KMS access? (Select TWO.)
A) The KMS Key Policy in Account B must grant `kms:Decrypt` and `kms:DescribeKey` permissions to Account A's IAM Role ARN (or Account A root)
B) The IAM Policy attached to the application's role in Account A must grant `kms:Decrypt` on the KMS Key ARN in Account B
C) Account A must pay Account B's AWS bill
D) Both accounts must merge into a single VPC
E) The KMS key must be moved to Account A

66. What is the AWS Encryption SDK?
A) A client-side encryption library provided by AWS that implements envelope encryption best practices, data key caching, and multi-KMS-key encryption across programming languages
B) A compiler plugin for C++
C) An operating system patch for Amazon Linux
D) A hardware appliance for data centers

67. What is Data Key Caching in the AWS Encryption SDK, and why is it used?
A) It caches plaintext and ciphertext data keys in local memory across multiple encryption operations to reduce the number of calls to AWS KMS, cutting KMS costs and latency
B) It saves passwords to a public S3 bucket
C) It permanently stores encryption keys on EC2 hard drives
D) It disables TLS encryption

68. What is an AWS KMS Grant?
A) An advanced mechanism that provides temporary, programmatic, and fine-grained permissions to use a KMS key (commonly used by AWS services like Amazon EBS and Amazon RDS to use customer keys on their behalf)
B) A financial discount on KMS billing
C) An IAM user group
D) A certificate authority

69. What is an Encryption Context in AWS KMS?
A) A set of non-secret key-value pairs passed to `kms:Encrypt` and `kms:GenerateDataKey` that provides authenticated data (AAD) to cryptographically bind the context to the ciphertext and appears in CloudTrail logs for auditing
B) The password of the database
C) The private key of the SSL certificate
D) A JSON file stored in S3 Glacier

70. If an application encrypts data using AWS KMS with an Encryption Context `{"department": "finance"}`, what must the application provide when calling `kms:Decrypt`?
A) The exact same Encryption Context `{"department": "finance"}`; otherwise, KMS will reject the decryption request with an `InvalidCiphertextException`
B) Any random string
C) No context is needed for decryption
D) The root account password

71. A company needs to re-encrypt sensitive database records from an old KMS key (`Key-1`) to a new KMS key (`Key-2`) during a cryptographic migration. Which KMS API action performs this re-encryption atomically on the server side without exposing plaintext to the application?
A) `kms:ReEncrypt`
B) `kms:GenerateDataKey`
C) `kms:Decrypt` followed by `kms:Encrypt`
D) `kms:RotateKey`

72. What is the difference between AWS KMS and AWS CloudHSM?
A) AWS KMS is a multi-tenant managed key service with FIPS 140-2 Level 3 validation; AWS CloudHSM provides dedicated, single-tenant hardware security module (HSM) appliances with FIPS 140-2 Level 3 compliance where the customer has exclusive control of the cryptographic hardware
B) CloudHSM is completely free
C) KMS requires on-premises hardware
D) Both services are identical

73. A developer wants to schedule the deletion of an unused KMS Customer Managed Key. What is the minimum waiting period enforced by AWS KMS before a key is permanently deleted?
A) 7 days (waiting period is configurable between 7 and 30 days)
B) 24 hours
C) Immediate deletion is possible with one click
D) 90 days fixed

74. If a KMS Customer Managed Key is in the `PendingDeletion` state, can applications encrypt or decrypt data using that key?
A) No, keys in `PendingDeletion` cannot be used for cryptographic operations; the deletion must be canceled (`kms:CancelKeyDeletion`) to restore functionality
B) Yes, decryption is allowed for 7 days
C) Yes, but only with root credentials
D) Only in `us-west-2`

75. How can a developer enforce that all objects uploaded to an S3 bucket must be encrypted using `aws:kms` rather than default `AES256`?
A) Add an S3 bucket policy with `Effect: Deny` on `s3:PutObject` with a condition `"StringNotEquals": { "s3:x-amz-server-side-encryption": "aws:kms" }`
B) Delete all IAM users
C) Enable S3 Versioning
D) Block port 80 on the VPC router

76. What is the purpose of S3 Bucket Keys when using SSE-KMS?
A) S3 Bucket Keys reduce KMS request costs by up to 99% by using a bucket-level key to create intermediate data keys for objects, dramatically reducing calls to KMS
B) They replace KMS with passwords
C) They allow public downloads without authentication
D) They disable S3 encryption

77. An application is processing millions of small transactions per minute. Calling AWS KMS `kms:Encrypt` for each transaction causes API throttling exceptions (`ThrottlingException`). What architectural change solves this issue?
A) Use Envelope Encryption with Data Key Caching (via AWS Encryption SDK) to reuse a single data key across multiple transactions before requesting a new key from KMS
B) Increase EC2 CPU count
C) Disable CloudTrail logging
D) Switch to unencrypted HTTP

78. Which S3 header must be specified in the `PutObject` API call to request SSE-KMS encryption with a specific Customer Managed Key?
A) `x-amz-server-side-encryption: aws:kms` and `x-amz-server-side-encryption-aws-kms-key-id: <key-arn>`
B) `x-amz-encryption-type: rsa`
C) `x-amz-kms: true`
D) `x-amz-customer-key: secret`

79. An application encrypts data client-side using the AWS Encryption SDK. When the encrypted message is sent to Amazon S3, what does S3 store?
A) Standard ciphertext byte streams containing the encrypted data, encrypted data key, and algorithm metadata formatted as an AWS Encryption SDK message
B) Plaintext data
C) A pointer to the KMS console
D) An XML file

80. A developer needs to import their own cryptographic key material (generated on an on-premises HSM) into an AWS KMS Customer Managed Key. What type of key origin is configured during creation?
A) `EXTERNAL` (Import Key Material)
B) `AWS_KMS`
C) `AWS_CLOUDHSM`
D) `LOCAL`

81. When key material is imported into an `EXTERNAL` KMS key, does AWS KMS support automatic annual key rotation?
A) No, automatic key rotation is NOT supported for keys with imported key material (`EXTERNAL`); the customer must manually rotate the key material by creating a new key
B) Yes, rotated automatically every 365 days
C) Yes, rotated every 30 days
D) Only if imported using OpenSSL

82. What is an AWS KMS Key Alias?
A) A friendly, displayable name for a KMS key (e.g., `alias/PaymentAppKey`) that can be mapped to different Key IDs over time to simplify application configuration
B) A secondary password for KMS
C) An IAM role name
D) An S3 bucket name

83. What is the difference between AWS KMS Symmetric Keys and Asymmetric Keys?
A) Symmetric keys use the same 256-bit key (AES-256-GCM) for encryption and decryption; Asymmetric keys use a public/private key pair (RSA or ECC) for encryption/decryption or digital signing/verification
B) Symmetric keys are only for passwords
C) Asymmetric keys are free of charge
D) Symmetric keys do not support envelope encryption

84. Can an application use an Asymmetric KMS key pair to verify digital signatures generated outside of AWS?
A) Yes, by exporting the public key (`kms:GetPublicKey`) and using standard cryptographic libraries, or calling `kms:Verify` directly in KMS
B) No, KMS keys cannot interact with external systems
C) Only if using Python
D) Only via Amazon SNS

85. A developer wants to restrict KMS key usage so that a key can ONLY be used when requests originate from a specific VPC via a VPC endpoint. What condition key should be added to the KMS Key Policy?
A) `"Condition": { "StringEquals": { "aws:sourceVpce": "vpce-1a2b3c4d" } }`
B) `"Condition": { "IpAddress": { "aws:SourceIp": "10.0.0.0/16" } }`
C) `"Condition": { "Bool": { "aws:SecureTransport": "true" } }`
D) `"Condition": { "StringEquals": { "aws:PrincipalType": "VPC" } }`

86. What is the effect of the `"kms:ViaService"` condition key in a KMS Key Policy?
A) It restricts key usage to requests coming exclusively through a specified AWS service in a specific region (e.g., `s3.us-east-1.amazonaws.com` or `dynamodb.us-east-1.amazonaws.com`)
B) It routes KMS traffic over a VPN
C) It disables IAM user authentication
D) It converts the key to an AWS Managed Key

87. Which TLS protocol versions are supported and recommended by AWS for encryption in transit to meet modern security compliance standards (such as PCI-DSS and HIPAA)?
A) TLS 1.2 and TLS 1.3
B) SSL 2.0 and SSL 3.0
C) TLS 1.0 and TLS 1.1
D) Plaintext HTTP

88. When an Application Load Balancer terminates HTTPS traffic, what component defines the allowed TLS versions, ciphers, and negotiation protocols?
A) Security Policy (SSL/TLS Cipher Policy, e.g., `ELBSecurityPolicy-TLS13-1-2-2021-06`)
B) Security Group ingress rule
C) Network ACL rule
D) Route 53 Health Check

89. What is Server Name Indication (SNI) on an Application Load Balancer or CloudFront distribution?
A) An extension to the TLS protocol that allows a client to specify the hostname it is attempting to connect to during the initial TLS handshake, enabling the load balancer to serve multiple different SSL certificates on a single IP address/port
B) A DNS record type
C) A mechanism to encrypt database passwords
D) An EC2 instance family

90. An application encrypts sensitive customer data using an AWS KMS key. Where can the security audit team find an immutable log of every API call made to this key (including caller identity, timestamp, and encryption context)?
A) AWS CloudTrail
B) Amazon CloudWatch Metrics
C) Amazon Route 53 Resolver logs
D) Amazon S3 Storage Lens

---

### Task Statement 2.3: Sensitive Data in Application Code & Protection (91–135)

91. A developer is designing a serverless microservice that connects to an Amazon Aurora MySQL database. Corporate security requires database credentials to be rotated every 30 days automatically without manual intervention or application restarts. Which AWS service natively supports automated credential rotation for RDS databases?
A) AWS Secrets Manager
B) AWS Systems Manager Parameter Store
C) AWS KMS
D) Amazon DynamoDB

92. What AWS component does AWS Secrets Manager use under the hood to execute automated password rotation against target databases (such as Amazon RDS and Amazon DocumentDB)?
A) An AWS Lambda rotation function (pre-configured from AWS Serverless Application Repository templates)
B) An Amazon EC2 instance running cron
C) AWS CodeBuild
D) Amazon SNS

93. In AWS Secrets Manager automated rotation, what are the four sequential steps executed by the Lambda rotation function?
A) `createSecret`, `setSecret`, `testSecret`, `finishSecret`
B) `init`, `build`, `deploy`, `cleanup`
C) `start`, `rotate`, `verify`, `stop`
D) `read`, `write`, `encrypt`, `decrypt`

94. During automated secret rotation in Secrets Manager, what secret version staging label is assigned to the newly generated credential while it is being tested, before it replaces the current active secret?
A) `AWSPENDING`
B) `AWSCURRENT`
C) `AWSPREVIOUS`
D) `STAGING`

95. Once the `finishSecret` step completes successfully during automated rotation in Secrets Manager, what staging label does the new secret receive, and what label is assigned to the old secret?
A) The new secret is labeled `AWSCURRENT`; the previous secret is moved to `AWSPREVIOUS`
B) The new secret is deleted; the old secret is kept
C) Both secrets are labeled `AWSCURRENT`
D) The old secret is permanently erased from history

96. A developer needs to store application configuration flags (`max_connections = 50`, `feature_x_enabled = true`) and a third-party API key that rarely changes. The developer wants a simple, cost-effective solution with zero monthly storage fees for standard parameters. Which AWS service should be used?
A) AWS Systems Manager Parameter Store (Standard Tier)
B) AWS Secrets Manager
C) Amazon RDS Multi-AZ
D) AWS CloudHSM

97. What parameter types are supported by AWS Systems Manager Parameter Store?
A) `String`, `StringList`, and `SecureString`
B) `Integer`, `Float`, and `Boolean`
C) `XML`, `JSON`, and `YAML` only
D) `Blob` and `Binary` only

98. When creating a `SecureString` parameter in AWS Systems Manager Parameter Store, what service is used to encrypt the parameter value at rest?
A) AWS KMS (using default `aws/ssm` key or a Customer Managed Key)
B) Amazon S3 SSE-S3
C) AWS Certificate Manager
D) Route 53 DNSSEC

99. What are the key differences between the Standard Tier and Advanced Tier in AWS Systems Manager Parameter Store? (Select TWO.)
A) Standard parameters support payloads up to 4 KB and are free; Advanced parameters support payloads up to 8 KB and incur a small monthly fee
B) Advanced parameters support Parameter Policies (such as expiration dates and notification alerts)
C) Standard parameters support up to 100,000 parameters per region; Advanced parameters support up to 10 parameters
D) Standard parameters only work on Windows; Advanced parameters work on Linux
E) Advanced parameters do not support encryption

100. A developer needs to retrieve a `SecureString` parameter from SSM Parameter Store using the AWS CLI or SDK. What parameter must be explicitly passed to return the decrypted plaintext value rather than the encrypted KMS ciphertext?
A) `--with-decryption` (in CLI) or `WithDecryption=True` (in SDK `get_parameter`)
B) `--show-password`
C) `--plaintext`
D) `--decrypt-all`

101. A multi-region application deployed in `us-east-1` and `eu-central-1` requires database credentials to be synchronized and available in both regions with automatic rotation. Which AWS service provides native Multi-Region Secret Replication?
A) AWS Secrets Manager (supports built-in Multi-Region Secret Replication)
B) AWS Systems Manager Parameter Store Standard Tier
C) Amazon DynamoDB Global Tables only
D) AWS CloudTrail

102. An AWS Lambda function needs to read a database connection password from an environment variable. However, junior developers with read-only access to the Lambda console should NOT be able to view the plaintext password in the Lambda configuration console or via `GetFunction` API calls. How should the developer secure this environment variable?
A) Use Lambda Encryption Helpers with a Customer Managed Key (CMK) in KMS to encrypt the environment variable client-side before deployment, and decrypt it programmatically inside the Lambda handler using `kms:Decrypt`
B) Hardcode the password in the Lambda function zip file
C) Delete the environment variable
D) Rename the environment variable to `SECRET`

103. In Python, how should an application running on AWS Lambda retrieve database credentials from AWS Secrets Manager efficiently across multiple invocations?
A) Fetch and cache the secret outside the Lambda handler function during initialization (cold start), so warm invocations reuse the cached secret in memory without calling Secrets Manager on every invocation
B) Call `get_secret_value` 10 times inside the handler loop
C) Hardcode the credentials in the handler arguments
D) Read credentials from an unencrypted S3 bucket

104. What open-source extension provided by AWS can be added to an AWS Lambda function to automatically retrieve, cache, and refresh secrets from Secrets Manager and parameters from SSM Parameter Store via a local HTTP endpoint?
A) AWS Parameters and Secrets Lambda Extension
B) AWS SAM CLI
C) AWS CodeDeploy Agent
D) Amazon Kinesis Producer Library

105. A company wants to prevent SQL Injection (SQLi) and Cross-Site Scripting (XSS) attacks from reaching an Application Load Balancer and Amazon API Gateway. Which AWS service should be placed in front of these endpoints?
A) AWS WAF (Web Application Firewall)
B) AWS Shield Standard only
C) Amazon GuardDuty
D) Amazon Macie

106. What is the difference between AWS WAF and AWS Shield?
A) AWS WAF is a Layer 7 application firewall that filters HTTP/HTTPS traffic based on rules (SQLi, XSS, rate limits); AWS Shield is a managed Distributed Denial of Service (DDoS) protection service for Layer 3 and Layer 4 attacks
B) AWS WAF is for databases; AWS Shield is for S3
C) AWS Shield only protects Windows servers
D) AWS WAF is hardware-based; AWS Shield is software-based

107. Which AWS services can be protected directly by associating an AWS WAF Web Access Control List (Web ACL)? (Select THREE.)
A) Amazon CloudFront distributions
B) Application Load Balancers (ALB)
C) Amazon API Gateway REST APIs and HTTP APIs
D) Amazon EC2 instances directly without a load balancer
E) Amazon S3 buckets directly without CloudFront
F) Amazon DynamoDB tables

108. A developer wants to protect a login API endpoint (`POST /auth/login`) against brute-force password guessing attacks. Which AWS WAF rule type automatically monitors request volume from individual IP addresses over a 5-minute sliding window and temporarily blocks IPs exceeding 100 requests?
A) AWS WAF Rate-Based Rule
B) AWS WAF String Match Rule
C) AWS Shield Advanced
D) Amazon Inspector

109. What is an AWS WAF Managed Rule Group?
A) A pre-configured, AWS-maintained collection of rules (such as `AWSManagedRulesCommonRuleSet`, `AWSManagedRulesSQLiRuleSet`, and `AWSManagedRulesKnownBadInputsRuleSet`) that protect against common vulnerabilities and are updated automatically by AWS
B) A custom bash script written by developers
C) A rule group managed by third-party antivirus vendors
D) An IAM permission set

110. A developer wants to test a new AWS WAF rule in production to observe how many requests would be affected WITHOUT actually blocking legitimate user traffic. What rule action should be configured?
A) `Count`
B) `Allow`
C) `Block`
D) `CAPTCHA`

111. What action types are supported for individual rules inside an AWS WAF Web ACL?
A) `Allow`, `Block`, `Count`, `CAPTCHA`, and `Challenge`
B) `Delete`, `Reboot`, `Archive`
C) `Encrypt`, `Decrypt`, `Sign`
D) `ScaleUp`, `ScaleDown`

112. An application logs incoming HTTP request payloads to Amazon CloudWatch Logs for debugging. A security audit discovers that user passwords and credit card numbers are being printed to logs in plain text. What two actions should the development team take? (Select TWO.)
A) Implement application-level logging interceptors/filters to sanitize, mask, or redact sensitive fields before outputting log events
B) Configure CloudWatch Logs Data Protection Policies on the log group to automatically detect and mask PII/PCI data identifiers upon ingestion
C) Delete all CloudWatch log groups permanently and disable logging
D) Switch to unencrypted HTTP
E) Email the log files to developers

113. What is the role of Amazon Macie in securing sensitive data in AWS?
A) It uses machine learning and pattern matching to automatically discover, classify, and protect sensitive data (such as PII, credit cards, and API keys) stored in Amazon S3 buckets
B) It rotates RDS database passwords
C) It compiles Lambda code
D) It monitors EC2 CPU usage

114. How can an organization enforce that all Amazon S3 buckets in an AWS account have "Block Public Access" enabled and reject any policy that attempts to make a bucket public?
A) Enable S3 Block Public Access at the AWS Account level (and enforce it via AWS Organizations SCP or AWS Config rule `s3-bucket-public-read-prohibited`)
B) Delete the Internet Gateway
C) Disable DNS in the VPC
D) Remove all IAM roles

115. A developer is designing a secure REST API with Amazon API Gateway. The developer wants to ensure that only an authorized backend microservice can invoke a specific API resource, using mutual TLS (mTLS) authentication. Does API Gateway support mTLS?
A) Yes, API Gateway supports mutual TLS (mTLS) on Custom Domain Names by verifying client certificates against a truststore uploaded to Amazon S3
B) No, API Gateway only supports username/password
C) Only when running on EC2
D) Only via Route 53

116. When an API client calls an API Gateway endpoint using Mutual TLS (mTLS), what cryptographic handshake occurs?
A) Both the API Gateway server and the API client present and validate each other's X.509 digital certificates to establish two-way identity authentication before exchanging data
B) API Gateway emails a password to the client
C) The client authenticates via SMS
D) The database generates a temporary IAM access key

117. An application receives sensitive customer Social Security Numbers (SSNs). Compliance mandates that SSNs must be tokenized (replaced with non-sensitive surrogate tokens) before being stored in the database. What is the primary security advantage of tokenization over encryption?
A) Tokenized surrogate values have no mathematical relationship to the original sensitive data, meaning compromised tokens cannot be decrypted without access to the isolated token vault
B) Tokenization eliminates the need for databases
C) Tokenization is completely free
D) Tokens can be reversed using standard AES algorithms

118. A developer wants to restrict access to an Amazon API Gateway REST API so that it can ONLY be invoked from within a specific Amazon VPC via a VPC endpoint. Which API Gateway endpoint type must be selected?
A) Private API Endpoint (using `execute-api` Interface VPC Endpoint and an API Gateway Resource Policy)
B) Edge-Optimized API Endpoint
C) Regional API Endpoint
D) Public Custom Domain

119. What policy must be configured on a Private API Gateway REST API to allow traffic from a specific VPC Endpoint (`vpce-1a2b3c4d`)?
A) An API Gateway Resource Policy with `Effect: Allow` on `execute-api:Invoke` and a condition `"StringEquals": { "aws:sourceVpce": "vpce-1a2b3c4d" }`
B) An S3 Bucket Policy
C) A Route 53 CNAME record
D) A Security Group on the IAM user

120. A developer wants to ensure that API requests passing through an Application Load Balancer contain a custom HTTP header (`X-Custom-Secret: MySecret123`) before forwarding them to an internal microservice, dropping all requests lacking the header. Where can this rule be configured?
A) On the Application Load Balancer Listener Rules (HTTP Header condition)
B) On the EC2 BIOS
C) In Route 53 DNS settings
D) In the VPC route table

121. An e-commerce platform wants to prevent automated bots from scraping product prices and submitting fraudulent account signups. Which AWS WAF feature provides advanced bot detection, CAPTCHA challenges, and machine learning-driven bot classification?
A) AWS WAF Bot Control managed rule group
B) AWS CodeDeploy
C) Amazon CloudWatch Alarms
D) Amazon S3 Storage Lens

122. When an AWS WAF rule evaluates an incoming HTTP request, what are the primary request components that can be inspected?
A) IP address, URI path, HTTP method, query strings, headers, cookies, and request body payload
B) EC2 hypervisor memory
C) IAM user passwords
D) S3 bucket replication status

123. A company wants to enforce that all developer laptop connections to the AWS Management Console require Multi-Factor Authentication (MFA). What condition key in an IAM policy enforces MFA validation?
A) `"Condition": { "Bool": { "aws:MultiFactorAuthPresent": "true" } }`
B) `"Condition": { "StringEquals": { "aws:MFA": "active" } }`
C) `"Condition": { "NumericEquals": { "aws:AuthLevel": 2 } }`
D) `"Condition": { "Bool": { "aws:SecureTransport": "true" } }`

124. What is the purpose of AWS Secrets Manager Secret Replication across regions?
A) It automatically replicates secrets (and their rotating versions) to secondary AWS Regions to support multi-region disaster recovery and localized low-latency secret retrieval
B) It creates duplicate AWS accounts
C) It converts SQL databases to DynamoDB
D) It compresses files into zip archives

125. A developer is designing a secure, multi-tier serverless application architecture:
1. Mobile users authenticate and receive JWT tokens with social login support.
2. Web API is protected against Layer 7 exploits, SQL injection, and brute-force traffic.
3. Database credentials rotate every 30 days automatically with zero downtime.
4. Data files stored in S3 are encrypted at rest with full per-operation CloudTrail audit logging.
Which combination of AWS security services correctly fulfills this architecture?
A) Amazon Cognito User Pools (Auth) + AWS WAF attached to API Gateway (Exploit & DDoS protection) + AWS Secrets Manager with Lambda rotation (DB Credential rotation) + Amazon S3 with SSE-KMS Customer Managed Key (Audited Encryption)
B) IAM static users + Route 53 simple routing + SSM Parameter Store standard + S3 SSE-S3
C) Amazon Cognito Identity Pools only + Security Groups on S3 + AWS CloudTrail Lake + AWS CodeGuru
D) AWS Secrets Manager for authentication + AWS KMS for DDoS protection + AWS WAF for database storage + S3 SSE-C

126. An application needs to securely pass sensitive API keys into a Docker container running on Amazon ECS on AWS Fargate without hardcoding them in the Dockerfile. How should the developer configure the ECS Task Definition?
A) Reference the secret stored in AWS Secrets Manager or SSM Parameter Store in the `secrets` section of the ECS Container Definition, referencing the parameter ARN and container environment variable name
B) Hardcode the API key in the container `CMD` command
C) Commit the secret to a public GitHub repository
D) Store the key in `/etc/hosts` in the container image

127. What IAM permission is required in the Amazon ECS Task Execution Role to allow ECS to retrieve secrets from Secrets Manager on behalf of a Fargate container at startup?
A) `secretsmanager:GetSecretValue` and `kms:Decrypt` (on the KMS key used to encrypt the secret)
B) `AdministratorAccess`
C) `s3:GetObject`
D) `ec2:DescribeInstances`

128. What is the difference between an ECS Task Execution Role and an ECS Task Role?
A) The Task Execution Role is used by the ECS container agent to pull images from ECR and fetch secrets from Secrets Manager/SSM; the Task Role is assumed by the application code running inside the container to make AWS API calls (e.g., DynamoDB, S3)
B) Task Execution Role is for Linux; Task Role is for Windows
C) Both roles are identical
D) Task Roles cannot access S3

129. A developer suspects that a compromised IAM user access key is being used to make unauthorized API calls. What is the FIRST emergency action the developer should take?
A) In the IAM console or CLI, set the Access Key status to `Inactive` or delete the access key immediately to revoke all further access
B) Send an email to the user
C) Reboot the EC2 instances
D) Increase CloudWatch metric retention

130. How does AWS Config help developers maintain security compliance in AWS accounts?
A) It continuously monitors, records, and evaluates AWS resource configurations against desired security baselines and rules (e.g., ensuring S3 buckets are encrypted and IAM policies do not allow `*`)
B) It compiles application code
C) It replaces AWS KMS
D) It acts as a DNS server

131. A developer wants to run automated vulnerability scans on container images stored in Amazon Elastic Container Registry (ECR) to detect known CVE software vulnerabilities before deployment. Which ECR feature provides this capability?
A) Amazon ECR Image Scanning (Basic Scanning via Clair or Enhanced Scanning via Amazon Inspector)
B) AWS WAF Rate Rules
C) Route 53 Health Checks
D) CloudWatch Logs Insights

132. What is the principle of Least Privilege in AWS security architecture?
A) Granting an identity (user, role, service) only the absolute minimum permissions required to perform its specific task, on specific resources, and under specific conditions, and no more
B) Giving all developers `AdministratorAccess` to speed up deployment
C) Allowing public read access on all S3 buckets
D) Disabling all IAM policies

133. When configuring an Amazon Cognito User Pool App Client for a mobile application, why should the "Generate client secret" option be UNCHECKED?
A) Mobile applications and Single Page Applications are public clients that cannot securely hide or protect a client secret from decompilation or inspection; generating a secret is reserved for confidential server-side backends
B) Client secrets are deprecated in Cognito
C) It makes the app slower
D) Mobile apps do not support OAuth 2.0

134. An application uses AWS Secrets Manager. The developer wants to be alerted immediately whenever a database secret is deleted or modified. Which AWS architecture pattern implements this security alert?
A) AWS CloudTrail captures the Secrets Manager API call (`DeleteSecret`, `PutSecretValue`) -> Amazon EventBridge matches the event pattern -> triggers an Amazon SNS topic notifying the security team
B) CloudWatch Logs polling every 24 hours
C) S3 Lifecycle Rules
D) Route 53 DNS failover

135. An application uses Amazon Cognito User Pools. The company wants to enforce that users must enter a one-time SMS or TOTP code in addition to their password when logging in from an unrecognized device. Which Cognito feature provides this adaptive risk-based authentication?
A) Amazon Cognito Advanced Security Features (Adaptive Authentication and compromised credentials check)
B) Amazon Route 53 Geolocation
C) AWS WAF CAPTCHA only
D) Amazon S3 Object Lock

---

## Answer Key & Explanations

1. A — Amazon Cognito User Pools acts as the identity provider (user directory) supporting social, SAML, OIDC, and username/password sign-in.
2. A — Authorization Code Grant with PKCE is the recommended OAuth 2.0 flow for public web/mobile clients without client secrets.
3. B — Token claims, user groups (`cognito:groups`), and attributes are located in the Payload (Claims) section of a JWT.
4. A — JWT signatures are validated server-side by downloading and checking the public JWKS JSON file from the Cognito User Pool endpoint.
5. A — Cognito Identity Pools exchange authenticated User Pool tokens for temporary AWS IAM credentials via AWS STS.
6. A — The `token_use` claim indicates whether a Cognito token is an `id` or `access` token.
7. A — User Pools manage authentication (user directory & JWT issuance); Identity Pools manage authorization (issuing AWS IAM credentials).
8. A — `dynamodb:LeadingKeys` matching `${cognito-identity.amazonaws.com:sub}` limits users to rows matching their own identity ID.
9. A — `AssumeRoleWithSAML` exchanges a corporate SAML 2.0 assertion for temporary AWS IAM credentials.
10. A — Configuring an IAM OIDC Identity Provider allows GitHub Actions to assume roles via `AssumeRoleWithWebIdentity` without static keys.
11. A — An explicit `Deny` in any policy (including Permissions Boundaries) overrides all `Allow` statements unconditionally.
12. A — Permissions Boundaries set the maximum permissible boundaries that identity-based policies can grant to an IAM entity.
13. A — Service Control Policies (SCPs) define the maximum permission boundaries for all accounts in an AWS Organization OU.
14. A — Attaching an IAM Role via an Instance Profile provides secure, automatic temporary credentials to applications on EC2.
15. A & B — IAM Roles provide automatically rotated temporary credentials and eliminate the security risk of static hardcoded access keys.
16. A & B — Cross-account S3 access requires an IAM policy on the caller in Account A AND an S3 Bucket Policy allowing the role in Account B.
17. A — `GetSessionToken` generates temporary credentials with MFA validation metadata for IAM users.
18. A — `sts:DecodeAuthorizationMessage` decodes and displays authorization failure details for permission troubleshooting.
19. A — Cognito Lambda Triggers execute custom business logic at various stages of registration, authentication, and token generation.
20. A — The Pre Token Generation Lambda Trigger customizes and enriches ID token claims before issuance.
21. A — The Refresh Token silently retrieves new ID and Access tokens without requiring the user to re-authenticate.
22. A — Cognito User Pool ID and Access Tokens default to a 1-hour (60 min) lifespan, configurable between 5 min and 24 hours.
23. A — API Gateway Cognito User Pool Authorizers natively validate incoming JWT tokens without custom Lambda code.
24. A — A Lambda Authorizer executes custom code to validate bearer tokens or request parameters and returns an IAM policy.
25. A — Cognito Identity Pools support guest access by assigning separate IAM roles to Authenticated and Unauthenticated identities.
26. A — The `aws:SourceIp` condition key restricts access based on caller IP address or CIDR range.
27. A — An S3 bucket policy with `Effect: Deny` and `"aws:SecureTransport": "false"` strictly enforces HTTPS connections.
28. A — Resource-Based Policies are attached directly to AWS resources (S3, KMS, SQS, Lambda) to govern access.
29. A — Resource-Based policies require an explicit `Principal` element; Identity-Based policies do not because the principal is implicit.
30. A — `aws sts get-caller-identity` returns the active IAM user, role, and account ARN for debugging.
31. A — An IAM Role with a Trust Policy requiring an `ExternalId` provides secure cross-account access and protects against confused deputies.
32. A — The `sts:ExternalId` condition prevents the Confused Deputy vulnerability during third-party cross-account role assumption.
33. A — Setting Identity Pool role resolution to "Choose role from token" dynamically maps Cognito groups to distinct IAM roles.
34. A — `sts:AssumeRole` sessions can be configured from 15 minutes up to a maximum duration of 12 hours.
35. A — Multiple conditions in an IAM statement must all evaluate to true (logical AND) for the policy to take effect.
36. A — ABAC matches resource tags (`aws:ResourceTag/Project`) with caller principal tags (`aws:PrincipalTag/Project`) dynamically.
37. A — A Trust Policy attached to an IAM Role defines which external principals are trusted to assume the role.
38. A — An SCP denying actions when `aws:RequestedRegion` does not match permitted regions enforces regional restrictions across accounts.
39. A — AWS uses a default Implicit Deny model; requests lacking an explicit Allow are denied.
40. A — The `none` algorithm indicates an unsigned token and must be rejected immediately to prevent forged token attacks.
41. A — The OAuth 2.0 Client Credentials Grant is designed for machine-to-machine (M2M) server-to-server communication.
42. A — The AWS SDK default credential provider chain automatically fetches temporary credentials from IMDSv2 or ECS container metadata.
43. A — IMDSv2 requires session tokens created via HTTP PUT, preventing SSRF attacks from stealing EC2 IAM credentials.
44. A — PKCE (Proof Key for Code Exchange) protects authorization codes from interception during browser redirects.
45. A — `AdminUserGlobalSignOut` invalidates all issued refresh tokens for a user across all devices immediately.
46. A — SSE-KMS encrypts data at rest while providing individual CloudTrail audit logs for every key use.
47. A — AWS KMS Customer Master Keys can directly encrypt or decrypt payloads up to 4 KB per API call.
48. A — Envelope Encryption uses `GenerateDataKey` to encrypt large payloads locally with data keys protected by KMS master keys.
49. A & B — `GenerateDataKey` returns a plaintext data key (for immediate encryption) and a ciphertext blob (for storage).
50. A — The application must immediately wipe the plaintext data key from memory after encrypting the payload.
51. A — `kms:Decrypt` takes the encrypted data key (`CiphertextBlob`) and returns the plaintext key to decrypt the payload.
52. A — `GenerateDataKeyWithoutPlaintext` returns only the encrypted data key, deferring plaintext decryption until needed.
53. A — Under SSE-C, the customer sends the raw encryption key in HTTP headers; S3 encrypts the object and discards the key.
54. A — Amazon S3 automatically applies default server-side encryption with SSE-S3 (AES-256) to all new buckets at no extra cost.
55. A — Automatic Key Rotation for Customer Managed KMS Keys rotates the backing key material every 365 days (1 year).
56. A — KMS key rotation keeps the Key ID and ARN unchanged and retains historical backing keys to decrypt older data transparently.
57. A — Automatic key rotation is supported ONLY for symmetric encryption KMS keys.
58. A — AWS Managed Keys are maintained by AWS; Customer Managed Keys support custom policies, rotation, and cross-account access.
59. A — AWS Certificate Manager (ACM) provides free public SSL/TLS certificates with automated renewal for integrated AWS services.
60. A — ACM public certificates are private-key protected within AWS services and cannot be downloaded or installed on EC2 directly.
61. A & B — ACM supports DNS Validation (via Route 53 CNAME records) and Email Validation for proving domain ownership.
62. A — ACM Private CA issues internal certificates for VPC services, IoT, and mobile devices with exportable private keys.
63. A — Every KMS key requires a Key Policy as the primary access control mechanism defining permissions on the key.
64. A — A KMS key without permissions granted to the root account or IAM principals becomes permanently unmanageable.
65. A & B — Cross-account KMS access requires permissions in the KMS Key Policy (Account B) AND the caller's IAM Policy (Account A).
66. A — The AWS Encryption SDK is a client-side library implementing envelope encryption and data key caching best practices.
67. A — Data Key Caching caches plaintext/encrypted data keys in memory to reduce KMS API calls, latency, and costs.
68. A — A KMS Grant is a programmatic delegation of key permissions, used extensively by AWS services (EBS, RDS).
69. A — An Encryption Context is authenticated data (AAD) that cryptographically binds context to ciphertext and is logged in CloudTrail.
70. A — Decryption requires the exact matching Encryption Context provided during encryption, or KMS rejects the request.
71. A — `kms:ReEncrypt` decrypts and re-encrypts data under a new KMS key server-side inside KMS without exposing plaintext.
72. A — KMS is a managed multi-tenant key service; CloudHSM provides dedicated, single-tenant hardware security modules.
73. A — AWS KMS enforces a mandatory 7 to 30 day waiting period before permanently deleting a Customer Managed Key.
74. A — Keys in the `PendingDeletion` state are disabled and cannot perform cryptographic operations unless deletion is canceled.
75. A — Denying `s3:PutObject` unless `s3:x-amz-server-side-encryption` equals `aws:kms` enforces SSE-KMS across the bucket.
76. A — S3 Bucket Keys reduce KMS request costs by up to 99% by using intermediate bucket-level encryption keys.
77. A — Data Key Caching reuses data keys in memory across multiple transactions, preventing KMS throttling exceptions.
78. A — `x-amz-server-side-encryption: aws:kms` specifies KMS encryption; `x-amz-server-side-encryption-aws-kms-key-id` specifies the key ARN.
79. A — Client-side encryption produces formatted ciphertext messages stored by S3 as standard binary objects.
80. A — Importing external key material from an on-premises HSM requires selecting the `EXTERNAL` key origin.
81. A — Automatic key rotation is not supported for `EXTERNAL` keys with imported key material; manual rotation is required.
82. A — A Key Alias is a display name (e.g., `alias/AppKey`) pointing to a Key ID, allowing key remapping without code changes.
83. A — Symmetric keys use AES-256 for both encryption/decryption; Asymmetric keys use public/private key pairs (RSA/ECC).
84. A — Asymmetric public keys can be exported via `kms:GetPublicKey` to verify digital signatures in external client applications.
85. A — The `aws:sourceVpce` condition key restricts KMS key operations to requests originating from a specific VPC endpoint.
86. A — The `kms:ViaService` condition restricts KMS operations to requests arriving through a specific AWS service (e.g., S3).
87. A — TLS 1.2 and TLS 1.3 are modern cryptographic protocols recommended for secure in-transit communication.
88. A — An ALB Security Policy (SSL/TLS Cipher Policy) defines the allowed TLS versions and cipher suites on HTTPS listeners.
89. A — Server Name Indication (SNI) enables serving multiple SSL certificates on a single load balancer listener by hostname.
90. A — AWS CloudTrail records an immutable audit log of every API call made to AWS KMS keys.
91. A — AWS Secrets Manager provides native automated credential rotation for Amazon RDS, Aurora, and DocumentDB.
92. A — Secrets Manager uses an AWS Lambda rotation function to execute password rotation workflows against target databases.
93. A — Secrets Manager rotation executes four lifecycle steps: `createSecret`, `setSecret`, `testSecret`, and `finishSecret`.
94. A — During rotation testing, the newly generated secret version is assigned the `AWSPENDING` staging label.
95. A — Upon rotation completion, the new secret becomes `AWSCURRENT` and the previous secret becomes `AWSPREVIOUS`.
96. A — SSM Parameter Store Standard Tier stores configuration parameters and static secrets with zero monthly storage fees.
97. A — SSM Parameter Store supports `String`, `StringList`, and `SecureString` parameter types.
98. A — `SecureString` parameters are encrypted at rest using AWS KMS Customer Managed Keys or the default `aws/ssm` key.
99. A & B — Standard parameters are free (up to 4 KB); Advanced parameters support up to 8 KB, parameter policies, and carry a fee.
100. A — `--with-decryption` (or `WithDecryption=True`) must be specified to return plaintext for `SecureString` parameters.
101. A — AWS Secrets Manager natively supports Multi-Region Secret Replication with automatic synchronization across regions.
102. A — KMS Encryption Helpers encrypt Lambda environment variables client-side, hiding them from console viewers.
103. A — Fetching and caching secrets outside the Lambda handler during initialization reuses cached values across warm invocations.
104. A — The AWS Parameters and Secrets Lambda Extension caches secrets and parameters locally via an in-memory HTTP endpoint.
105. A — AWS WAF filters HTTP/HTTPS traffic on ALBs, CloudFront, and API Gateway to block SQLi, XSS, and exploit traffic.
106. A — AWS WAF protects Layer 7 (Application); AWS Shield protects Layer 3 and Layer 4 (Network/Transport DDoS).
107. A, B & C — AWS WAF Web ACLs attach directly to CloudFront distributions, Application Load Balancers, and API Gateway APIs.
108. A — An AWS WAF Rate-Based Rule tracks IP request rates over a 5-minute sliding window and blocks IPs exceeding thresholds.
109. A — AWS Managed Rule Groups are pre-configured, AWS-maintained rule sets protecting against common web exploits.
110. A — Setting rule action to `Count` logs and evaluates traffic without blocking legitimate requests during testing.
111. A — AWS WAF rule actions include `Allow`, `Block`, `Count`, `CAPTCHA`, and `Challenge`.
112. A & B — Sanitizing logs via application interceptors and enabling CloudWatch Data Protection Policies prevents PII/PCI leakage.
113. A — Amazon Macie uses machine learning to discover, classify, and protect sensitive PII and data stored in S3 buckets.
114. A — Enabling S3 Block Public Access at the account level prevents public bucket policies and ACLs account-wide.
115. A — API Gateway supports Mutual TLS (mTLS) on custom domains by verifying client certificates against an S3 truststore.
116. A — Mutual TLS performs two-way X.509 certificate validation between the client and server during the TLS handshake.
117. A — Tokenized surrogate tokens carry no mathematical link to original sensitive data and cannot be mathematically decrypted.
118. A — Private API Gateway endpoints are accessible exclusively from within a VPC via an `execute-api` Interface VPC Endpoint.
119. A — API Gateway Resource Policies with `aws:sourceVpce` conditions restrict invocation to specified VPC endpoints.
120. A — Application Load Balancer HTTP Header Listener Rules verify custom headers before forwarding requests to target groups.
121. A — AWS WAF Bot Control uses managed rule sets and machine learning to detect, classify, and challenge automated bot traffic.
122. A — AWS WAF inspects IP addresses, URIs, HTTP methods, headers, cookies, query parameters, and request body payloads.
123. A — `"aws:MultiFactorAuthPresent": "true"` enforces Multi-Factor Authentication validation in IAM policies.
124. A — Secrets Manager Secret Replication copies secrets and rotation metadata to secondary regions for DR and low latency.
125. A — Cognito for authentication, WAF for Layer 7 defense, Secrets Manager for rotation, and S3 SSE-KMS for audited encryption.
126. A — ECS Task Definitions inject secrets into container environment variables by referencing parameter ARNs in `secrets`.
127. A — The ECS Task Execution Role requires `secretsmanager:GetSecretValue` and `kms:Decrypt` to fetch container secrets.
128. A — Task Execution Role is used by the ECS agent (pulling images/secrets); Task Role is used by container application code.
129. A — Inactivating or deleting a compromised IAM access key immediately terminates its ability to authenticate API calls.
130. A — AWS Config continuously evaluates resource configurations against security baselines and compliance rules.
131. A — Amazon ECR Image Scanning detects known software vulnerabilities (CVEs) in pushed container images.
132. A — Least Privilege restricts identities to only the specific permissions and resources necessary to perform their role.
133. A — Public clients (mobile apps, SPAs) cannot securely store client secrets; unchecking this option prevents secret exposure.
134. A — CloudTrail capturing secret events combined with EventBridge and SNS delivers real-time alerts on secret modifications.
135. A — Cognito Advanced Security Features provides adaptive authentication, assessing risk signals to prompt for step-up MFA.
