# Module 14 — Security Deep Dive

Domain focus: **Domain 2 — Security (26%) in its entirety**. This is the second highest-weighted domain on the AWS Certified Developer – Associate (DVA-C02) exam. It covers three foundational task statements:
- **Task Statement 2.1**: Authenticate and authorize application access to AWS services (Identity Federation, OIDC, SAML 2.0, Bearer Tokens / JWTs, OAuth 2.0, AWS STS, Cognito User Pools vs. Identity Pools, IAM Policies, Resource-based Policies, Principal Policies, RBAC, ACLs, and Least Privilege).
- **Task Statement 2.2**: Implement encryption at rest and in transit (ACM vs. ACM Private CA, Key Management Service / AWS KMS, Customer Managed Keys vs. AWS Managed Keys, Automatic Key Rotation, Envelope Encryption mechanisms `GenerateDataKey`/`Decrypt`, Client-side vs. Server-side encryption models `SSE-S3`/`SSE-KMS`/`SSE-C`, Key Policies, and Cross-Account Key Sharing).
- **Task Statement 2.3**: Manage sensitive data in application code (Data classification for PII/PHI, Lambda environment variable encryption with helper keys, AWS Secrets Manager vs. AWS Systems Manager Parameter Store with automated credential rotation templates, Data Sanitization in logging pipelines, and AWS WAF integration).

Security is not an isolated afterthought on the DVA-C02 exam; it is woven into every architecture and code implementation question. While Module 00 established basic IAM primitives, this module dives deep into developer-level security mechanics: token structure, cryptographic workflows, policy evaluation logic, secret lifecycle management, and defensive web application filtering.

---

## 1. Authentication and Authorization (Task Statement 2.1)

Authentication establishes **who you are** (identity verification); Authorization establishes **what you are allowed to do** (permissions evaluation). In modern cloud applications, hardcoding static credentials into source code or config files is an immediate security vulnerability. AWS provides identity federation, token-based authentication, and temporary credential assumption to ensure least-privilege, dynamic access.

```
+------------------+         1. Authenticate         +-----------------------+
|  End User / App  | ------------------------------> | Identity Provider IdP |
|  (Client/Device) |                                 | (Cognito/OIDC/SAML)   |
+------------------+ <------------------------------ +-----------------------+
        |                2. Returns JWT / SAML Token
        |
        | 3. Exchange Token for AWS Credentials (AssumeRoleWithWebIdentity)
        v
+------------------+                                 +-----------------------+
|     AWS STS      | ------------------------------> | Temporary Credentials |
| (Security Token) |                                 | (AccessKey,Secret,Tok)|
+------------------+                                 +-----------------------+
        |
        | 4. Sign API Requests with SigV4
        v
+------------------+
|   AWS Service    | (DynamoDB, S3, SQS, etc.)
+------------------+
```

### 1.1 Identity Federation: SAML 2.0 and OIDC

Identity Federation allows users outside of AWS (such as corporate employees in Microsoft Active Directory or consumer users with Google/Facebook accounts) to access AWS resources or custom applications without creating separate IAM users in the AWS account.

1. **Enterprise Identity Federation (SAML 2.0)**:
   - Uses the Security Assertion Markup Language (SAML 2.0) XML standard.
   - Typically used for workforce identity management (e.g., Okta, Ping Identity, Microsoft Entra ID / Azure AD, Active Directory Federation Services).
   - **Flow**: The client authenticates against the corporate IdP. The IdP issues a signed SAML assertion. The client sends this assertion to the AWS Security Token Service (STS) via `AssumeRoleWithSAML`. STS validates the assertion signature and returns temporary AWS credentials (`AccessKeyId`, `SecretAccessKey`, `SessionToken`).
   - The developer does not manage usernames or passwords in AWS.

2. **Web Identity Federation (OpenID Connect / OIDC)**:
   - Built on top of OAuth 2.0 using lightweight JSON Web Tokens (JWTs).
   - Used for consumer-facing identities (Google, Apple, Amazon, Facebook) and OIDC-compliant providers (like GitHub Actions, GitLab CI, or custom OpenID servers).
   - **Flow**: The client authenticates with the OIDC IdP and receives an ID Token (JWT). The application passes this token to AWS STS via `AssumeRoleWithWebIdentity` (or through Amazon Cognito Identity Pools) to obtain temporary, scoped AWS credentials.

### 1.2 Bearer Tokens, JWT Architecture & OAuth 2.0

A **Bearer Token** is a security token where possession of the token is sufficient for access (whoever "bears" the token is granted the access it describes). The standard format used across modern web APIs and AWS Cognito is the **JSON Web Token (JWT)** (RFC 7519).

#### Structure of a JSON Web Token (JWT)
A JWT consists of three distinct parts separated by dots (`.`): `Header.Payload.Signature`

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFiYzEyMyJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkphbmUgRG9lIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUuY29tIiwiaXNzIjoiaHR0cHM6Ly9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbS91c19lYXN0XzFfWHhYIiwiZXhwIjoxNjkzNDk1MzI1LCJ0b2tlbl91c2UiOiJpZCJ9.dGhpcyBpcyBhIG1vY2sgc2lnbmF0dXJlIHZlcmlmaWVkIGJ5IHRoZSBwdWJsaWMga2V5
```

1. **Header**: Base64URL-encoded JSON specifying the cryptographic algorithm and key ID:
   ```json
   {
     "alg": "RS256",
     "typ": "JWT",
     "kid": "abc123keyId"
   }
   ```
2. **Payload (Claims)**: Base64URL-encoded JSON containing entity attributes and token metadata:
   - `sub` (Subject): The unique identifier for the user (UUID in Cognito).
   - `iss` (Issuer): The URL of the token issuer (e.g., `https://cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdef`).
   - `exp` (Expiration time): Unix epoch timestamp when the token becomes invalid.
   - `iat` (Issued at): Timestamp when the token was created.
   - `token_use`: Cognito-specific claim (`id`, `access`, or `refresh`).
   - `cognito:groups`: Array of Cognito User Pool user groups the user belongs to (e.g., `["Admins", "Managers"]`).
   - Custom claims: `email`, `custom:tenant_id`, etc.
3. **Signature**: Cryptographic hash calculated over the encoded header and payload using the issuer's private key (`RS256` or `HS256`).

#### How an Application Validates a JWT Server-Side:
1. Decode the unverified header to extract the `kid` (Key ID).
2. Download the JSON Web Key Set (JWKS) public keys from the provider's well-known endpoint:
   `https://cognito-idp.<region>.amazonaws.com/<user-pool-id>/.well-known/jwks.json`
3. Verify the cryptographic signature using the matching public key.
4. Verify standard claims:
   - Check that `exp` is in the future (token is not expired).
   - Check that `iss` matches your expected User Pool URL.
   - Check that `aud` (or `client_id`) matches your registered App Client ID.
   - Check `token_use` (e.g., ensure an API endpoint requiring authorization expects an `access` token rather than an `id` token).

#### OAuth 2.0 Grant Types (Flows) Relevant to Developers
- **Authorization Code Grant with PKCE** (Proof Key for Code Exchange): The most secure standard flow for Single Page Applications (SPAs) and mobile apps. Replaces the legacy Implicit Grant. The client generates a code verifier and code challenge to prevent authorization code interception attacks.
- **Client Credentials Grant**: Used for machine-to-machine (M2M) communication without user interaction (e.g., a backend daemon microservice calling another backend API).
- **Refresh Token Grant**: Exchanges a valid long-lived Refresh Token for a new short-lived ID/Access Token pair when the access token expires.

### 1.3 AWS Security Token Service (STS)

AWS STS is a global web service that provides short-lived temporary security credentials to IAM users or authenticated federated users. Temporary credentials consist of an **Access Key ID**, a **Secret Access Key**, and a mandatory **Security Token** (`SessionToken`).

| STS API Action | Use Case | Typical Caller | Max Duration |
|---|---|---|---|
| `AssumeRole` | Cross-account access, EC2 instance profiles, Lambda execution roles, delegating permissions to IAM users | IAM User, EC2, Lambda, Automation | 1 hour (default) up to 12 hours |
| `AssumeRoleWithWebIdentity` | Authenticating mobile/web users using OpenID Connect (OIDC) or social identity tokens (Google, Apple, Cognito) | Mobile app, SPA, GitHub Actions CI/CD | 1 hour (default) up to 12 hours |
| `AssumeRoleWithSAML` | Enterprise Single Sign-On (SSO) using SAML 2.0 assertions from corporate IdP | Corporate browser client | 1 hour (default) up to 12 hours |
| `GetSessionToken` | Generating temporary credentials for IAM users, typically to add Multi-Factor Authentication (MFA) validation | IAM User with MFA device | 15 minutes to 36 hours (default 12h) |
| `GetFederationToken` | Custom identity broker issuing scoped temporary credentials to federated users | On-premises backend broker | 15 minutes to 36 hours |
| `GetCallerIdentity` | Validating the current active IAM identity ARN, account ID, and user ID (debugging/sanity check) | Developer CLI / Application SDK | N/A (read-only) |

```python
import boto3

# Example: Assuming a cross-account role in production
sts_client = boto3.client("sts")

assumed_role_object = sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/CrossAccountDynamoDBAccess",
    RoleSessionName="AppOrderProcessingSession",
    DurationSeconds=3600
)

# Extract temporary credentials
credentials = assumed_role_object["Credentials"]

# Initialize a target service client using the temporary credentials
dynamodb = boto3.client(
    "dynamodb",
    aws_access_key_id=credentials["AccessKeyId"],
    aws_secret_access_key=credentials["SecretAccessKey"],
    aws_session_token=credentials["SessionToken"],
    region_name="us-east-1"
)
```

### 1.4 Amazon Cognito: User Pools vs. Identity Pools

Amazon Cognito is divided into two distinct services that serve complementary purposes in application architecture:

```
+-----------------------------------------------------------------------------------+
|                            AMAZON COGNITO ARCHITECTURE                            |
+-----------------------------------------------------------------------------------+

   +--------------------------+                      +--------------------------+
   |   COGNITO USER POOLS     |                      |  COGNITO IDENTITY POOLS  |
   |     (Authentication)     |                      |     (Authorization)      |
   +--------------------------+                      +--------------------------+
   | - User directory         |                      | - Issues temporary AWS   |
   | - Sign-up / Sign-in      |                      |   IAM credentials (STS)  |
   | - MFA, Email/SMS verify  |                      | - Maps users/groups to   |
   | - Social/SAML/OIDC login |                      |   specific IAM Roles     |
   | - Issues JWT Tokens:     |                      | - Supports Authenticated |
   |   (ID, Access, Refresh)  |                      |   and Guest access       |
   +--------------------------+                      +--------------------------+
                |                                                 ^
                | 1. User signs in, receives JWT                  |
                +-------------------------------------------------+
                  2. App passes JWT to Identity Pool
                     to exchange for temporary AWS IAM Credentials!
```

#### Detailed Comparison:
| Feature | Cognito User Pools (CUP) | Cognito Identity Pools (Federated Identities) |
|---|---|---|
| **Primary Purpose** | **Authentication** (Identity Provider / User Directory) | **Authorization** (Access Control to AWS Resources) |
| **Output Token / Credential** | Issues **JWTs** (ID Token, Access Token, Refresh Token) | Issues **AWS IAM Credentials** (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) |
| **Target Consumers** | Web/mobile app user database, API Gateway Authorizers, ALB OIDC Auth | Direct SDK calls from mobile/web clients to AWS services (S3 upload, DynamoDB read) |
| **Federation Sources** | Hosted UI with Google, Apple, Facebook, SAML 2.0, OIDC | Cognito User Pools, Google, Apple, SAML 2.0, OIDC, Developer Authenticated Identities |
| **Guest Access** | Not supported (users must register/authenticate) | Supported (unauthenticated / guest roles for anonymous users) |
| **Fine-Grained Access** | Custom attributes, groups, pre/post Lambda triggers | Role mapping based on claims, `dynamodb:LeadingKeys` IAM policies |

#### How They Connect Together in a Modern Mobile/Web Architecture:
1. User enters username and password in the mobile app.
2. The app authenticates against **Cognito User Pool** and receives an ID Token, Access Token, and Refresh Token.
3. The app presents the ID Token to the **Cognito Identity Pool**.
4. The Identity Pool evaluates the token claims (and user groups), assumes the configured IAM Role via STS `AssumeRoleWithWebIdentity`, and returns temporary AWS IAM credentials.
5. The mobile app uses these temporary AWS credentials directly in the AWS SDK to upload a photo to an S3 bucket (`s3://my-app-uploads/${cognito-identity.amazonaws.com:sub}/*`).

### 1.5 IAM Policies, Principal Policies & Permission Boundaries

AWS evaluates policies using a strict deterministic decision model:
1. By default, all requests are **implicitly denied**.
2. An **explicit allow** in any applicable policy overrides the default implicit deny.
3. An **explicit deny** anywhere overrides ANY and ALL allows, no matter what.

```
       [ Request arrives at AWS API ]
                     |
                     v
   +------------------------------------+
   |   Is there an EXPLICIT DENY?       | ---- YES ----> [ DENY ACCESS ]
   +------------------------------------+
                     |
                    NO
                     v
   +------------------------------------+
   |   Is there an EXPLICIT ALLOW?      | ---- NO -----> [ DENY ACCESS (Implicit) ]
   +------------------------------------+
                     |
                    YES
                     v
   +------------------------------------+
   |   Within Permissions Boundary &    | ---- NO -----> [ DENY ACCESS ]
   |   Organization SCP Limits?         |
   +------------------------------------+
                     |
                    YES
                     v
             [ ALLOW ACCESS ]
```

#### Types of IAM Policies:
- **Identity-Based Policies**: Attached directly to IAM users, groups, or roles (e.g., Managed Policies or Inline Policies). Specifies what the identity can do.
- **Resource-Based Policies**: Attached directly to an AWS resource (e.g., S3 Bucket Policy, KMS Key Policy, SQS Queue Policy, Lambda Resource-Based Policy). Specifies who (which `Principal`) can access that resource and what actions they can perform.
- **Permissions Boundaries**: An advanced feature that uses a managed policy to set the **maximum possible permissions** an identity-based policy can grant to an IAM user or role. It acts as an upper limit guardrail (e.g., allowing developers to create IAM roles for Lambda functions, but enforcing a boundary so the created roles cannot grant `AdministratorAccess`).
- **Service Control Policies (SCPs)**: Organization-level guardrails applied to AWS Accounts or Organizational Units (OUs). SCPs specify the maximum permissions for an entire AWS account, overriding account administrators.

#### Fine-Grained Access Control: `dynamodb:LeadingKeys`
In multi-tenant or mobile applications, you can restrict an authenticated user to reading or writing ONLY their own partition key in a DynamoDB table using the `${cognito-identity.amazonaws.com:sub}` context variable:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/UserProfiles",
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": [
            "${cognito-identity.amazonaws.com:sub}"
          ]
        }
      }
    }
  ]
}
```

---

## 2. Encryption at Rest and in Transit (Task Statement 2.2)

Encryption protects data confidentiality. The DVA-C02 exam tests your knowledge of symmetric vs. asymmetric cryptographic keys, AWS Certificate Manager (ACM), AWS Key Management Service (KMS), and the mechanics of **Envelope Encryption**.

```
+-----------------------------------------------------------------------------------+
|                          ENVELOPE ENCRYPTION MECHANISM                            |
+-----------------------------------------------------------------------------------+

 1. App calls KMS GenerateDataKey(KeyId='alias/MyKmsKey', KeySpec='AES_256')
 2. KMS returns:
    - Plaintext Data Key (used in memory to encrypt large data)
    - Ciphertext (Encrypted) Data Key (encrypted under the KMS Master Key)

      +----------------------+          +--------------------------+
      |  Plaintext Data Key  |          |  Encrypted Data Key (EK) |
      +----------------------+          +--------------------------+
                 |                                   |
                 v                                   |
      +----------------------+                       |
      | Encrypt Data (Local) |                       |
      +----------------------+                       |
                 |                                   |
                 v                                   v
      +----------------------+          +--------------------------+
      |    Encrypted Data    | ++++++++ |  Encrypted Data Key (EK) |
      +----------------------+          +--------------------------+
                 |
                 +--> Stored together in Database / S3!
                 
 (Plaintext Data Key is immediately wiped from application memory!)
```

### 2.1 Encryption in Transit & AWS Certificate Manager (ACM)

Encryption in transit ensures that data cannot be intercepted or modified while moving across network connections (using TLS 1.2 / TLS 1.3).

- **AWS Certificate Manager (ACM)**:
  - Provisions, manages, and automatically renews public and private SSL/TLS certificates.
  - **Public Certificates**: Free of charge when used with supported AWS services (Amazon CloudFront distributions, Application Load Balancers, Network Load Balancers with TLS listeners, API Gateway Custom Domains).
  - Public certificates issued by ACM **cannot be exported or downloaded** as raw private key files; they can only be bound to integrated AWS services.
  - Domain validation is performed via **DNS validation** (creating a CNAME record in Route 53 or your DNS registrar) or **Email validation**. DNS validation is strongly recommended because it enables automated certificate renewal.
- **ACM Private CA (AWS Private Certificate Authority)**:
  - Managed private CA for issuing internal certificates for microservices, internal VPC servers, mobile devices, and IoT endpoints.
  - Charges a monthly fee per private CA plus a per-certificate fee.
  - Private certificates can be exported and installed directly on EC2 instances or container hosts.

### 2.2 AWS Key Management Service (KMS) & Key Types

AWS KMS is a managed service that uses FIPS 140-2 validated Hardware Security Modules (HSMs) to generate and manage cryptographic keys.

#### KMS Key Types:
1. **AWS Owned Keys**:
   - Internal keys used and managed exclusively by AWS services (e.g., default DynamoDB encryption).
   - Free of charge, invisible in the KMS console, cannot be tracked in CloudTrail or managed by customers.
2. **AWS Managed Keys**:
   - Created automatically by AWS services when you enable encryption (e.g., `aws/s3`, `aws/rds`, `aws/lambda`).
   - Named with the service prefix: `aws/<service-name>`.
   - Free monthly key storage fee, but API requests incur standard KMS request fees.
   - Rotated automatically by AWS every **1 year** (365 days) — cannot be disabled or customized.
   - Key policies cannot be modified by the customer.
3. **Customer Managed Keys (CMKs)**:
   - Created, owned, and managed by the customer.
   - Incurs a $1/month storage fee per key plus per-request API fees.
   - Full control over Key Policies, IAM policies, aliases, tags, and deletion schedules (7 to 30 days pending deletion).
   - **Automatic Key Rotation**: Can be enabled on symmetric CMKs (rotates every **1 year / 365 days** or custom 90-730 days depending on modern settings; previously fixed at 365 days). When rotated, the KMS Key ARN and Key ID remain identical; KMS retains backing keys to decrypt older data transparently.
   - Can be used for **Cross-Account Access** (requires granting permissions in both the KMS Key Policy and the external account's IAM policy).

### 2.3 Envelope Encryption: `GenerateDataKey` & `Decrypt`

AWS KMS enforces a hard limit: **a KMS Customer Master Key can only directly encrypt up to 4 KB of data per API call.**
To encrypt files, database rows, or payloads larger than 4 KB, AWS uses **Envelope Encryption** (encrypting plaintext data with a unique Data Key, and encrypting the Data Key under a KMS Key).

#### How Envelope Encryption Works (Step-by-Step):

#### Encryption Path:
1. Application calls the KMS API: `GenerateDataKey(KeyId="alias/MyKey", KeySpec="AES_256")`.
2. KMS returns two items:
   - `Plaintext`: A 256-bit random data key.
   - `CiphertextBlob`: The same data key, encrypted under the specified KMS Customer Master Key.
3. The application uses the `Plaintext` data key to encrypt the large file locally in memory using AES-256-GCM.
4. The application **immediately erases the plaintext data key from memory**.
5. The application stores the encrypted data alongside the `CiphertextBlob` (Encrypted Data Key) in the storage target (e.g., S3 object metadata or a DynamoDB column).

#### Decryption Path:
1. The application retrieves the encrypted data and the `CiphertextBlob` (Encrypted Data Key).
2. The application calls the KMS API: `Decrypt(CiphertextBlob=encryptedDataKey)`.
3. KMS uses the backing master key in its HSM to decrypt the data key and returns the `Plaintext` data key to the application.
4. The application uses the `Plaintext` data key to decrypt the payload locally.
5. The application immediately wipes the plaintext data key from memory.

#### KMS API Summary for Developers:
- `Encrypt`: Encrypts small data (< 4 KB) directly in KMS HSMs.
- `Decrypt`: Decrypts ciphertext (< 4 KB, or an encrypted data key) directly in KMS HSMs.
- `GenerateDataKey`: Returns both the Plaintext Data Key and Encrypted Data Key.
- `GenerateDataKeyWithoutPlaintext`: Returns ONLY the Encrypted Data Key (useful when encryption will happen on a separate worker node later).
- `ReEncrypt`: Decrypts and re-encrypts data under a new KMS key in a single atomic server-side operation inside KMS without exposing plaintext to the caller.

### 2.4 Server-Side vs. Client-Side Encryption Models

```
+-----------------------------------------------------------------------------------+
|                        S3 ENCRYPTION MODELS COMPARISON                            |
+-----------------------------------------------------------------------------------+

 1. SSE-S3 (Default)   : Key managed by S3 (AES-256). Free, automatic.
 2. SSE-KMS            : Key managed in AWS KMS. Audit trail in CloudTrail, role-based access.
 3. SSE-C              : Customer provides raw 256-bit key in HTTP header (x-amz-server-side-encryption-customer-key). S3 does encryption, discards key.
 4. Client-Side        : App encrypts data BEFORE sending to S3 (AWS Encryption SDK). S3 only sees ciphertext.
```

| Model | Who manages Keys? | Who does the Encryption work? | Key Features / Trade-offs |
|---|---|---|---|
| **SSE-S3** | Amazon S3 (AWS Owned Key) | S3 (Server-side) | Free, zero configuration, default for all new S3 buckets. No fine-grained key access control or CloudTrail key audit. |
| **SSE-KMS** | AWS KMS (AWS Managed or CMK) | S3 (Server-side) | Provides per-key CloudTrail audit logging, key rotation, and separate IAM/Key Policy access control. Subject to KMS API request limits/costs. |
| **SSE-C** | Customer (Customer-Provided) | S3 (Server-side) | Customer passes raw encryption key in HTTPS headers (`x-amz-server-side-encryption-customer-key`). AWS encrypts data, discards key immediately. Customer must track which key encrypted which object. |
| **Client-Side Encryption** | Customer / AWS Encryption SDK | Application Client (Client-side) | Data is encrypted in memory before network transmission. S3 never sees plaintext or encryption keys. Highest compliance security. |

### 2.5 KMS Key Policies & Cross-Account Sharing

Every KMS key **MUST have a Key Policy**. IAM policies alone are not sufficient to grant access to a KMS key; the Key Policy itself must explicitly allow the IAM principal or delegate access to the root account.

```json
{
  "Version": "2012-10-17",
  "Id": "CrossAccountKmsPolicy",
  "Statement": [
    {
      "Sid": "Enable IAM User Permissions",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::111122223333:root" },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "AllowExternalAccountAccess",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::444455556666:role/CrossAccountLambdaRole" },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Cross-Account KMS Access Prerequisites (Two-Way Handshake):
1. **Account A (KMS Owner)**: The KMS Key Policy must explicitly grant `kms:Decrypt`, `kms:GenerateDataKey` to Account B's IAM Role ARN (or Account B's root).
2. **Account B (Consumer)**: The IAM Policy attached to the Lambda Execution Role / EC2 Instance Profile must grant `kms:Decrypt`, `kms:GenerateDataKey` on the KMS Key ARN in Account A.

---

## 3. Sensitive Data in Application Code (Task Statement 2.3)

Handling credentials, tokens, and personally identifiable information (PII) securely is a critical developer responsibility. This section covers secure configuration storage, automated rotation, log sanitization, and edge application firewalls.

### 3.1 Data Classification: PII and PHI
- **PII (Personally Identifiable Information)**: Social Security Numbers, Credit Card Numbers, Full Names, Home Addresses, Driver's License Numbers.
- **PHI (Protected Health Information)**: Medical records, health insurance IDs, biometric data (subject to HIPAA compliance).
- **Developer Guardrails**:
  - Never log PII/PHI in plaintext to CloudWatch Logs or application traces.
  - Encrypt all PII/PHI in transit (TLS 1.3) and at rest (KMS with Customer Managed Keys).
  - Use tokenization or client-side masking before storage.

### 3.2 Secrets Manager vs. Systems Manager Parameter Store

A core DVA-C02 comparison topic is choosing between **AWS Secrets Manager** and **AWS Systems Manager Parameter Store**.

| Feature | AWS Secrets Manager | SSM Parameter Store |
|---|---|---|
| **Primary Use Case** | Database credentials, OAuth API tokens, third-party API keys requiring **automated rotation** | Application configuration parameters, license codes, environment flags, static secrets |
| **Native Automatic Rotation** | **Built-in native integration** with AWS Lambda rotation templates (RDS MySQL/PostgreSQL, Aurora, DocumentDB, Redshift) | No native automated rotation (requires custom manual EventBridge + Lambda trigger) |
| **Cost** | **$0.40 per secret per month** + $0.05 per 10,000 API calls | **Standard tier: Free** (up to 10,000 params, 4 KB size). Advanced tier: $0.05/month (up to 8 KB size) |
| **Cross-Account / Cross-Region** | Native **Multi-Region Secret Replication** (replicates secret and rotates automatically across regions) | Replicate manually via custom scripts / CI/CD pipelines |
| **Encryption** | Always encrypted using AWS KMS | Supports `String`, `StringList`, and `SecureString` (encrypted via KMS) |
| **Max Payload Size** | Up to **64 KB** per secret | Standard: **4 KB**; Advanced: **8 KB** |
| **Integration with RDS Proxy** | **Native direct integration** (RDS Proxy retrieves DB credentials directly from Secrets Manager) | Not supported natively by RDS Proxy |

```python
# Retrieving a secret from AWS Secrets Manager in Python (Boto3)
import boto3
from botocore.exceptions import ClientError
import json

def get_db_credentials(secret_name, region_name="us-east-1"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    if "SecretString" in response:
        secret = json.loads(response["SecretString"])
        return secret["username"], secret["password"]
```

### 3.3 Automated Secret Rotation in Secrets Manager

Secrets Manager uses an **AWS Lambda function** to rotate credentials without application downtime:
1. Secrets Manager triggers the Lambda rotation function with four distinct step lifecycle events:
   - `createSecret`: Generates a new version of the secret password in the database and stages it in Secrets Manager with version stage `AWSPENDING`.
   - `setSecret`: Modifies the database user password in the target database to match the new `AWSPENDING` secret.
   - `testSecret`: Tests the connection to the database using the new `AWSPENDING` secret to verify functionality.
   - `finishSecret`: Promotes `AWSPENDING` to `AWSCURRENT` and moves the previous version to `AWSPREVIOUS`.

```
[ Secrets Manager Schedule ] ---> [ Lambda Rotation Function ]
                                         |
                                         | 1. createSecret (generates new password)
                                         | 2. setSecret (updates password in RDS)
                                         | 3. testSecret (validates connection)
                                         | 4. finishSecret (marks AWSCURRENT)
                                         v
                                  [ Amazon RDS Database ]
```

### 3.4 Encrypting Lambda Environment Variables

When deploying AWS Lambda functions with environment variables containing sensitive values (like API endpoints or tokens):
- **Server-Side Encryption at Rest**: By default, AWS Lambda encrypts all environment variables at rest using an AWS Managed KMS key (`aws/lambda`) after deployment.
- **Client-Side Helper Encryption (KMS Encryption Helpers)**: If sensitive environment variables must be protected against unauthorized IAM users viewing them in the AWS Lambda console or `GetFunction` API calls:
  1. The developer uses a Customer Managed Key (CMK) in KMS.
  2. In the Lambda console, enable "Encryption Helpers" to encrypt the variable values client-side before deployment.
  3. Inside the Lambda function code, import Boto3 KMS and explicitly call `kms.decrypt(CiphertextBlob=base64.b64decode(os.environ['MY_SECRET']))` during runtime initialization.

### 3.5 Sanitizing Sensitive Data in Logging Pipelines

Application logs frequently leak sensitive data (such as API keys, authorization tokens, credit card numbers, or passwords) when raw request objects are dumped to `stdout`.

#### Best Practices for Developers:
1. **Application-Level Interceptors**: Implement logging interceptors/middleware that redact or hash sensitive fields (e.g., replacing `password: "secret"` with `password: "********"` or masking credit cards `****-****-****-1234`) before serializing log events.
2. **CloudWatch Logs Data Protection Policies**: Configure automated data masking at the CloudWatch Log Group level using managed data identifiers (identifying credit cards, SSNs, AWS access keys) and replacing them with `[MASKED]`.

### 3.6 AWS WAF (Web Application Firewall)

AWS WAF is a Layer 7 (Application Layer) firewall that inspects incoming HTTP/HTTPS traffic to protect web applications against common web exploits and bots.

- **Deployment Targets**:
  - Amazon CloudFront distributions
  - Amazon API Gateway REST APIs and HTTP APIs
  - Application Load Balancers (ALB)
  - AWS AppSync GraphQL APIs
  - Amazon Cognito User Pools
- **Core Components**:
  - **Web ACL (Web Access Control List)**: The container containing a collection of rules and a default action (`Allow` or `Block`).
  - **AWS Managed Rules (AMR)**: Pre-configured rule sets maintained by AWS threat intelligence (e.g., `AWSManagedRulesCommonRuleSet`, `AWSManagedRulesSQLiRuleSet`, `AWSManagedRulesKnownBadInputsRuleSet`).
  - **Custom Rules**: Inspect request headers, HTTP methods, query strings, cookies, or URI paths using string matching or regular expressions.
  - **Rate-Based Rules**: Automatically tracks request volume from individual IP addresses over a 5-minute sliding window and temporarily blocks (or challenges via CAPTCHA) any IP exceeding a configured threshold (e.g., > 2,000 requests per 5 minutes to mitigate brute-force and HTTP flood DDoS attacks).
  - **IP Sets and Regex Pattern Sets**: Reusable collections of CIDR blocks (whitelists/blacklists) or regular expressions.

---

## 4. Worked Real-World Scenarios

### Scenario A — Cross-Account S3 Upload with Customer Managed KMS Encryption
**Context**: A multi-account enterprise architecture where an ingestion Lambda function in Account A (`111122223333`) uploads sensitive customer financial records to an Amazon S3 bucket in Account B (`444455556666`). The objects must be encrypted at rest using an AWS KMS Customer Managed Key (CMK) owned by Account B.
**Implementation Steps**:
1. In Account B, create a Customer Managed KMS Key. In the KMS **Key Policy**, add a statement granting `kms:Encrypt`, `kms:GenerateDataKey`, and `kms:DescribeKey` to Account A's Lambda execution role ARN.
2. In Account B, update the **S3 Bucket Policy** to allow `s3:PutObject` and `s3:PutObjectAcl` from Account A's Lambda execution role.
3. In Account A, attach an **IAM Policy** to the Lambda execution role granting `s3:PutObject` on the Account B bucket AND `kms:GenerateDataKey`, `kms:Encrypt` on the Account B KMS Key ARN.
4. In the Lambda function code, when calling `s3.put_object()`, explicitly specify `ServerSideEncryption="aws:kms"` and `SSEKMSKeyId="<Account-B-KMS-Key-ARN>"`.

### Scenario B — Automated Zero-Downtime RDS Credential Rotation
**Context**: An enterprise application connects to an Amazon Aurora PostgreSQL database. The corporate compliance department mandates that all database passwords must be rotated every 30 days automatically with zero application downtime.
**Implementation Steps**:
1. Deploy **Amazon RDS Proxy** in front of the Aurora PostgreSQL database.
2. Store the database master credentials in **AWS Secrets Manager**.
3. Enable **Automatic Rotation** in Secrets Manager, choosing the AWS-managed PostgreSQL rotation Lambda template with a 30-day schedule.
4. Configure RDS Proxy to retrieve credentials directly from the Secrets Manager secret ARN, and grant RDS Proxy's IAM role permission to decrypt the secret via KMS.
5. Point application microservices to the RDS Proxy endpoint using IAM database authentication or retrieving credentials from Secrets Manager. During the 30-day rotation, the rotation Lambda updates the password in Aurora and Secrets Manager, while RDS Proxy seamlessly drains and updates connections without dropping user transactions.

### Scenario C — Securing a Public API with CloudFront, WAF & Cognito Authorization
**Context**: A SaaS company provides an API for mobile applications. The company wants to prevent SQL injection and DDoS attacks, authenticate users via mobile sign-in, and ensure that only authenticated users can invoke backend microservices.
**Implementation Steps**:
1. Configure **Amazon Cognito User Pool** with OAuth 2.0 PKCE flow for mobile user registration and login.
2. Deploy **Amazon API Gateway** with a **Cognito User Pool Authorizer** attached to the `/api/*` resources, validating the incoming `Authorization: Bearer <ID_Token>` header.
3. Place an **Amazon CloudFront** distribution in front of API Gateway for edge caching and SSL termination.
4. Attach an **AWS WAF Web ACL** to the CloudFront distribution containing:
   - `AWSManagedRulesCommonRuleSet` and `AWSManagedRulesSQLiRuleSet` to block malicious payloads.
   - A **Rate-Based Rule** limiting requests to 1,000 per 5 minutes per IP address to block brute-force attempts.

---

## 5. Key Exam Traps from this Module

- **Cognito User Pools vs. Identity Pools**: User Pools = Authentication / User Directory (returns JWTs); Identity Pools = Authorization / AWS Credentials (returns temporary IAM STS credentials).
- **Public Certificates in ACM**: Free of charge, but cannot be downloaded/exported to EC2 instances directly; they can only be attached to ALB, CloudFront, or API Gateway.
- **KMS 4 KB Limit**: A KMS key can only encrypt up to 4 KB directly. For files/data > 4 KB, you **must use Envelope Encryption** with `GenerateDataKey`.
- **KMS Key Policy Requirement**: An IAM policy alone cannot grant access to a KMS CMK; the KMS **Key Policy** must delegate permissions to the root account or explicitly name the IAM principal.
- **KMS Key Rotation**: Automatic rotation for CMKs creates a new backing key version every 365 days; the Key ID and ARN do NOT change, and previous backing keys are retained to decrypt old data.
- **Secrets Manager vs. Parameter Store**: If a question mentions **native automatic rotation** or **multi-region replication**, the answer is **Secrets Manager**. If the question mentions **free configuration storage** or **storing static non-rotating strings**, the answer is **Parameter Store**.
- **SSE-C**: The customer supplies the 256-bit key in HTTP request headers; AWS does the encryption/decryption on S3 but never stores the key.
- **`dynamodb:LeadingKeys`**: The condition key used in IAM policies to restrict a user to accessing only the DynamoDB items matching their own Cognito Identity ID partition key.
- **Explicit Deny Overrides All**: If an IAM policy allows an action but a Service Control Policy (SCP), Permissions Boundary, or Resource Policy explicitly denies it, access is strictly denied.
- **AWS WAF Deployment Scope**: WAF attaches to CloudFront (global), ALB, API Gateway, AppSync, and Cognito User Pools (regional). WAF does NOT attach directly to EC2 instances or S3 buckets (attach to ALB or CloudFront instead).
- **Lambda Environment Variable Encryption**: Variables are encrypted at rest with an AWS managed key (`aws/lambda`) by default; masking them from console viewers requires KMS Encryption Helpers and client-side `kms:Decrypt` code.
