#!/usr/bin/env python3
"""Generate 125 practice questions for Module 15: Networking for Developers"""

import os

questions_text = """# Module 15 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### VPC Fundamentals, Subnets, Internet Gateways & NAT Gateways (1–25)

1. A developer is deploying a three-tier web application consisting of a web tier, an application tier, and an Amazon RDS database. The company's security policy requires that the database must not be directly reachable from the public internet. Where should the developer place the database instances?
A) In a public subnet with an Internet Gateway route
B) In private subnets with no route to an Internet Gateway
C) In a public subnet with an Elastic IP address attached
D) On an S3 bucket with public read access enabled

2. What specific routing configuration distinguishes a public subnet from a private subnet in an Amazon VPC?
A) A public subnet has a route in its route table pointing non-local traffic (`0.0.0.0/0`) to an attached Internet Gateway (IGW)
B) A public subnet uses 10.0.0.0/8 CIDR blocks while a private subnet uses 192.168.0.0/16
C) A public subnet has Network ACLs completely disabled
D) A public subnet must span at least three AWS Regions

3. An EC2 instance resides in a public subnet with a route table entry pointing `0.0.0.0/0` to an Internet Gateway. However, external users cannot connect to the web server running on the instance over HTTP. What is the most likely networking requirement missing from the instance?
A) The instance does not have a public IPv4 address or an Elastic IP address assigned
B) The VPC must be attached to an AWS Direct Connect gateway
C) The instance must have an IAM instance profile with Administrator privileges
D) The instance must be in an Amazon S3 storage class

4. An application running on EC2 instances in a private subnet needs to download security patches and software updates from the public internet. The instances must NEVER accept unsolicited inbound connections from the internet. Which VPC component provides this outbound-only internet connectivity?
A) Internet Gateway (IGW)
B) NAT Gateway
C) Customer Gateway
D) Virtual Private Gateway (VGW)

5. Where must a managed NAT Gateway be deployed in an Amazon VPC to function properly?
A) In a private subnet with a route to a database
B) In a public subnet that has an allocated Elastic IP (EIP) and a route to an Internet Gateway
C) Directly inside an Amazon S3 bucket
D) On an on-premises router

6. A developer notices that a company's monthly AWS bill includes significant data transfer and hourly charges for a NAT Gateway. Which two architectural strategies help reduce or eliminate NAT Gateway data processing costs? (Select TWO.)
A) Create Gateway VPC Endpoints for Amazon S3 and Amazon DynamoDB traffic so that requests bypass the NAT Gateway entirely at no additional cost
B) Create Interface VPC Endpoints (AWS PrivateLink) for high-volume AWS services (such as Amazon SQS, SNS, or Secrets Manager) accessed from private subnets
C) Move all private databases into public subnets with public IP addresses
D) Attach two Internet Gateways to the same VPC
E) Disable encryption on all network packets

7. An EC2 instance in a private subnet needs to access a third-party payment gateway API on the public internet. What route table entry is required in the private subnet's route table?
A) `0.0.0.0/0` targeting the Internet Gateway (`igw-xxxx`)
B) `0.0.0.0/0` targeting the NAT Gateway (`nat-xxxx`)
C) `10.0.0.0/16` targeting the NAT Gateway
D) `0.0.0.0/0` targeting a Customer Gateway

8. What is the primary operational difference between an AWS-managed NAT Gateway and a self-managed NAT Instance running on Amazon EC2?
A) NAT Gateway is a fully managed, highly available service that automatically scales bandwidth up to 100 Gbps without requiring OS patching or software maintenance; NAT Instances require manual instance sizing, AMI patching, and custom failover scripts
B) NAT Gateway only works with IPv6 traffic
C) NAT Instances are completely free of charge
D) NAT Gateway allows unsolicited inbound connections from the public internet

9. How does an organization achieve high availability for outbound internet traffic when deploying NAT Gateways in a multi-AZ VPC?
A) Deploy a single NAT Gateway in one public subnet and route all private subnets across all AZs to it
B) Deploy an independent NAT Gateway in a public subnet in EACH Availability Zone, and configure each private subnet's route table to use the NAT Gateway in its respective AZ
C) Deploy a NAT Gateway on an S3 Glacier vault
D) Attach multiple Internet Gateways to a single subnet

10. A developer is troubleshooting an issue where an EC2 instance in a private subnet cannot connect to the internet through a newly provisioned NAT Gateway. The private subnet route table has a route for `0.0.0.0/0` pointing to the NAT Gateway ID. What check should the developer perform next?
A) Verify that the public subnet hosting the NAT Gateway has a route for `0.0.0.0/0` pointing to an Internet Gateway and that an Elastic IP is associated with the NAT Gateway
B) Recreate the VPC from scratch
C) Reboot the EC2 instance in safe mode
D) Change the instance tenancy to Dedicated

11. An application requires two-way internet communication: it must accept incoming customer requests on port 443 and initiate outbound API calls to external vendors. Where should the application's EC2 instances be hosted?
A) In a private subnet behind a NAT Gateway
B) In a public subnet with a route to an Internet Gateway, assigned public IP addresses, and appropriate Security Group ingress rules
C) In an on-premises data center with no internet access
D) In an isolated subnet with no route tables

12. In an Amazon VPC, what is the maximum number of Internet Gateways that can be attached to a single VPC at any given time?
A) 1
B) 2
C) 5
D) Unlimited

13. A company has a private subnet containing application servers and a database subnet containing Amazon RDS instances. The application servers need to communicate with the database. How is routing between subnets within the same VPC handled?
A) Through a NAT Gateway
B) Automatically by the local VPC route (e.g., `10.0.0.0/16` -> `local`), allowing subnets within the same VPC to communicate by default unless restricted by Security Groups or NACLs
C) Via an Internet Gateway
D) Using Route 53 public hosted zones

14. What happens when an EC2 instance in a private subnet attempts to communicate with another EC2 instance in a different private subnet within the same VPC?
A) The traffic is dropped because private subnets cannot communicate with each other
B) The traffic flows directly over the internal VPC network via the default `local` route
C) The traffic must pass through an Internet Gateway
D) The traffic is routed through AWS CloudTrail

15. An engineer is configuring a VPC. Which component acts as a stateful virtual firewall that operates at the individual Elastic Network Interface (ENI) / instance level?
A) Network Access Control List (NACL)
B) Security Group
C) Internet Gateway
D) Route Table

16. Which component acts as a stateless subnet-level firewall that inspects traffic entering and exiting an entire subnet in an Amazon VPC?
A) Security Group
B) Network Access Control List (NACL)
C) NAT Gateway
D) Route 53

17. If a Security Group allows inbound traffic on TCP port 443 from `0.0.0.0/0`, what outbound rule is required to allow the response traffic back to the client?
A) An explicit outbound rule allowing ephemeral ports (1024–65535)
B) No outbound rule is required because Security Groups are stateful; return traffic for an allowed inbound request is automatically permitted
C) An outbound rule allowing all ICMP traffic
D) A custom NACL rule only

18. A developer configures a custom NACL on a public subnet. The inbound rule allows HTTP traffic on port 80. When testing the web server from a browser, the request hangs and times out. What missing NACL configuration is the root cause?
A) NACLs are stateless, so an explicit outbound rule allowing traffic to ephemeral ports (1024–65535) is required for the server to send responses back to clients
B) The Internet Gateway was deleted
C) The Security Group must be converted to stateless mode
D) The subnet must be placed in multiple AWS Regions

19. In a microservices architecture, a web service running on EC2 needs to communicate with an internal backend API running on EC2 in the same VPC. How should the backend API's Security Group be configured to follow the principle of least privilege?
A) Allow inbound TCP on the API port from `0.0.0.0/0`
B) Allow inbound TCP on the API port referencing the Security Group ID of the web service as the source
C) Allow all traffic from the VPC CIDR block without restrictions
D) Disable Security Groups and use IAM policies only

20. What is an Elastic IP (EIP) address in AWS?
A) A temporary private IP address that changes upon instance reboot
B) A static, public IPv4 address allocated to an AWS account that can be dynamically remapped between instances or NAT Gateways in a Region
C) An IPv6 address used exclusively for S3 Glacier
D) A dedicated hardware firewall appliance

21. A developer wants to ensure that database instances in a private subnet cannot be reached directly from the internet under any circumstances, even if an administrator accidentally adds an Elastic IP. What VPC design guarantees this isolation?
A) Keeping the database subnet associated with a route table that has NO route to an Internet Gateway
B) Enabling S3 Block Public Access
C) Installing antivirus software on the database host
D) Creating an IAM user without administrator access

22. What happens to traffic destined for an external IP address if a subnet's route table contains only the default `local` route (e.g., `10.0.0.0/16` -> `local`) and no default gateway route for `0.0.0.0/0`?
A) The traffic is automatically sent to the nearest AWS edge location
B) The traffic is dropped immediately because there is no route to non-local IP addresses (creating an isolated subnet)
C) The traffic is broadcast to all instances in the VPC
D) The traffic is forwarded to Amazon CloudFront

23. A company is connecting its on-premises corporate network to an Amazon VPC using an AWS Site-to-Site VPN. Which VPC component is attached to the VPC to terminate the VPN connection on the AWS side?
A) Virtual Private Gateway (VGW) or AWS Transit Gateway
B) Internet Gateway (IGW)
C) NAT Gateway
D) Elastic Load Balancer

24. What is the maximum transmission unit (MTU) supported for traffic traversing an Internet Gateway, NAT Gateway, or Inter-Region VPC Peering?
A) 1,500 bytes (standard Ethernet frame)
B) 9,001 bytes (jumbo frames)
C) 64,000 bytes
D) 512 bytes

25. An application requires instances in two separate VPCs in the same AWS Region to communicate using private IP addresses with low latency and no internet traversal. Which AWS networking feature connects the two VPCs directly?
A) VPC Peering (or AWS Transit Gateway)
B) Internet Gateway
C) Amazon CloudFront
D) Route 53 Public Hosted Zone

---

### VPC Endpoints: Gateway vs Interface Endpoints (PrivateLink) (26–50)

26. An application hosted on EC2 instances in a private subnet reads and writes millions of images to an Amazon S3 bucket daily. The security team mandates that S3 traffic must not traverse the public internet or pass through a NAT Gateway. Which solution meets these requirements at NO additional cost?
A) Provision an S3 Interface VPC Endpoint (AWS PrivateLink)
B) Provision an S3 Gateway VPC Endpoint and attach it to the private subnet's route table
C) Assign public IP addresses to all private EC2 instances
D) Deploy an AWS Site-to-Site VPN to Amazon S3

27. Which two AWS services support Gateway VPC Endpoints? (Select TWO.)
A) Amazon S3
B) Amazon DynamoDB
C) Amazon SQS
D) AWS Secrets Manager
E) AWS KMS

28. How does a Gateway VPC Endpoint route traffic to Amazon S3 or Amazon DynamoDB from within a VPC?
A) It assigns an Elastic Network Interface (ENI) with a private IP to each subnet
B) It adds a prefix list entry for the AWS service (e.g., `pl-63a5400a` for S3) to the VPC route table as a route target pointing to the Gateway Endpoint ID
C) It creates a public DNS record in Route 53
D) It routes all traffic through an on-premises proxy server

29. A developer needs to allow an application running in a private subnet to retrieve secrets from AWS Secrets Manager without routing traffic through a NAT Gateway or traversing the public internet. Which type of VPC endpoint is required?
A) Gateway VPC Endpoint
B) Interface VPC Endpoint (powered by AWS PrivateLink)
C) Internet Gateway Endpoint
D) S3 Select Endpoint

30. What infrastructure component is provisioned inside your VPC subnets when an Interface VPC Endpoint (AWS PrivateLink) is created for an AWS service?
A) An Elastic Network Interface (ENI) with a private IP address from the subnet's CIDR range
B) A new EC2 instance running Linux
C) A physical router appliance
D) A public Internet Gateway

31. How does an application running in a private subnet resolve the standard public endpoint hostname (e.g., `secretsmanager.us-east-1.amazonaws.com`) to the private IP of an Interface VPC Endpoint?
A) By enabling "Private DNS" on the Interface VPC Endpoint, which creates an AWS-managed private hosted zone that resolves the service's public DNS name to the endpoint's private ENI IP
B) By manually editing the `/etc/hosts` file on every EC2 instance
C) By configuring an S3 bucket policy
D) By purchasing a public domain name in Route 53

32. How is access control enforced on an Interface VPC Endpoint? (Select TWO.)
A) Attaching a VPC Endpoint Policy (a resource-based JSON policy) that restricts which principals, actions, and resources are allowed through the endpoint
B) Attaching Security Groups to the endpoint's Elastic Network Interfaces (ENIs) to restrict incoming traffic by IP or source security group
C) Enabling MFA Delete on the endpoint
D) Disabling IPv4 across the entire VPC
E) Configuring Route 53 latency routing

33. An enterprise with an on-premises data center connected via AWS Direct Connect wants on-premises servers to query Amazon S3 buckets privately using private IP addresses. Why must the company use an S3 Interface Endpoint (PrivateLink) instead of an S3 Gateway Endpoint for this on-premises use case?
A) Gateway Endpoints are accessible only from within the VPC and cannot be accessed over Direct Connect or AWS Site-to-Site VPN from on-premises; Interface Endpoints have private IPs reachable over Direct Connect
B) Gateway Endpoints do not support encryption
C) Interface Endpoints are completely free of charge
D) Gateway Endpoints only work with DynamoDB

34. A developer is designing a security policy for a Gateway VPC Endpoint to Amazon S3. The developer wants to ensure that instances in the VPC can ONLY access the company's specific S3 bucket (`my-company-data`) and cannot exfiltrate data to external S3 buckets. How can this be enforced?
A) Attach an Endpoint Policy to the Gateway Endpoint with `Effect: Allow`, `Action: s3:*`, and `Resource: [arn:aws:s3:::my-company-data, arn:aws:s3:::my-company-data/*]`
B) Delete all other S3 buckets in the AWS account
C) Disable DNS resolution in the VPC
D) Block port 443 in the subnet NACL

35. What is the pricing model for Gateway VPC Endpoints for Amazon S3 and DynamoDB?
A) $0.01 per hour plus $0.05 per GB processed
B) There is NO hourly fee and NO data processing fee for Gateway VPC Endpoints
C) Flat fee of $100 per month per VPC
D) Billed based on the number of Lambda functions in the account

36. What is the pricing model for Interface VPC Endpoints (AWS PrivateLink)?
A) Free for all AWS services
B) An hourly charge per provisioned endpoint ENI (per AZ) plus a per-GB data processing charge
C) $500 per month flat fee
D) Billed based on the number of IAM users in the account

37. An application in a private subnet communicates with Amazon SQS, Amazon SNS, and AWS KMS. The developer wants all communication to remain strictly within the AWS network. How many Interface VPC Endpoints must be created?
A) 1 shared endpoint for all services
B) 3 distinct Interface VPC Endpoints (one for SQS, one for SNS, and one for KMS)
C) 0, because these services use Gateway Endpoints
D) 10 endpoints per AZ

38. What AWS feature allows an organization to create their own custom service behind an Application Load Balancer or Network Load Balancer in one VPC and expose it securely to consumers in other VPCs via Interface Endpoints (AWS PrivateLink) without VPC peering?
A) VPC Peering
B) VPC Endpoint Services (PrivateLink)
C) Route 53 Resolver
D) NAT Gateway

39. When an Interface VPC Endpoint is created in multiple Availability Zones, how does PrivateLink ensure high availability?
A) By creating an Elastic Network Interface (ENI) with a private IP address in each specified Availability Zone's subnet
B) By launching an EC2 instance in each AZ
C) By replicating data across S3 Glacier
D) By creating multiple VPCs automatically

40. An engineer attempts to associate a Gateway VPC Endpoint with a private subnet, but the route is not added. What VPC configuration must be selected when creating a Gateway Endpoint?
A) The specific Route Table(s) associated with the subnets that should route traffic through the Gateway Endpoint
B) The IAM Instance Profile
C) The Elastic IP address
D) The CloudFront distribution ID

41. Which of the following AWS services can be accessed privately from a VPC via an Interface VPC Endpoint?
A) Amazon CloudWatch Logs, AWS Secrets Manager, Amazon Kinesis Data Streams, and AWS CodeCommit
B) Only Amazon S3 and DynamoDB
C) Only third-party SaaS applications outside of AWS
D) No AWS services support Interface Endpoints

42. A developer wants to restrict access to an Amazon S3 bucket so that objects can ONLY be accessed from within a specific VPC via a Gateway VPC Endpoint (`vpce-1a2b3c4d`). What condition key should be added to the S3 bucket policy?
A) `"Condition": { "StringEquals": { "aws:sourceVpce": "vpce-1a2b3c4d" } }`
B) `"Condition": { "IpAddress": { "aws:SourceIp": "10.0.0.0/16" } }`
C) `"Condition": { "StringEquals": { "aws:PrincipalType": "VPC" } }`
D) `"Condition": { "Bool": { "aws:SecureTransport": "true" } }`

43. What happens if a VPC contains both a Gateway Endpoint for S3 in its route table and a NAT Gateway with a route for `0.0.0.0/0`?
A) All S3 traffic is dropped due to routing conflict
B) Traffic destined for Amazon S3 matches the more specific S3 prefix list route and goes directly through the Gateway Endpoint, while general internet traffic routes to the NAT Gateway
C) Traffic is randomly split 50/50 between the two gateways
D) The NAT Gateway overrides the Gateway Endpoint

44. A developer configures an Interface VPC Endpoint for Amazon SQS. The application running on private EC2 instances attempts to send messages to SQS, but the connection times out. What is the most likely cause?
A) The Security Group attached to the Interface Endpoint ENI does not allow inbound HTTPS (port 443) traffic from the application instances
B) Amazon SQS is offline
C) SQS only accepts unencrypted HTTP traffic on port 80
D) The EC2 instances must be in a public subnet

45. Can an Interface VPC Endpoint be used to connect to an Amazon API Gateway Private REST API?
A) No, API Gateway only supports public endpoints
B) Yes, an Interface VPC Endpoint for `execute-api` enables private access to Private REST APIs from within the VPC or over Direct Connect
C) Only if the API Gateway uses SOAP protocol
D) Only when paired with an Internet Gateway

46. What is the difference between `aws:sourceVpc` and `aws:sourceVpce` condition keys in IAM and S3 bucket policies?
A) `aws:sourceVpc` restricts requests originating from a specific VPC ID (e.g., `vpc-xxxx`); `aws:sourceVpce` restricts requests flowing through a specific VPC Endpoint ID (e.g., `vpce-xxxx`)
B) `aws:sourceVpc` is used for EC2; `aws:sourceVpce` is used for Lambda
C) `aws:sourceVpc` is deprecated
D) Both condition keys are identical

47. When an application in a VPC accesses DynamoDB through a Gateway VPC Endpoint, does the application code need to change its DynamoDB endpoint URL or SDK configuration?
A) Yes, the application must specify the private IP address of the gateway
B) No, the application continues calling the standard regional DynamoDB endpoint (e.g., `dynamodb.us-east-1.amazonaws.com`), and routing is handled transparently at the VPC route table level
C) Yes, the developer must switch to JDBC drivers
D) Yes, the table name must be prefixed with `vpce-`

48. A developer wants to verify whether S3 requests from a private EC2 instance are utilizing the Gateway VPC Endpoint. What tool or data source can confirm this?
A) S3 Server Access Logs or VPC Flow Logs, checking that the requester IP is a private VPC IP and/or the endpoint ID matches
B) Route 53 query logs
C) CloudFront edge metrics
D) AWS CodeArtifact logs

49. An enterprise mandates that all CloudWatch Logs emitted by containerized microservices in private subnets must never leave the AWS internal network. Which VPC endpoint should be deployed?
A) Interface VPC Endpoint for `logs` (CloudWatch Logs)
B) Gateway Endpoint for CloudWatch
C) NAT Gateway with TLS 1.3
D) Internet Gateway with WAF

50. What is a key architectural benefit of using VPC Endpoints over NAT Gateways for AWS API traffic?
A) Increased security and compliance (traffic never leaves the private AWS network), lower latency, and reduced data processing costs
B) Automatic conversion of all REST APIs to GraphQL
C) Ability to run EC2 instances without EBS volumes
D) Elimination of all IAM permission requirements

---

### Lambda in VPC: ENIs, Routing, Private Databases & Troubleshooting (51–75)

51. By default, what network environment does an AWS Lambda function run in when NO VPC configuration is specified?
A) Inside the default VPC of the AWS account
B) In a secure, AWS-managed VPC with direct access to the public internet and public AWS service endpoints (S3, DynamoDB, SQS)
C) In a private subnet with no internet access
D) On an on-premises server

52. When does an AWS Lambda function NEED to be configured with VPC access?
A) Whenever the function needs to call Amazon S3 or Amazon DynamoDB
B) Only when the function needs to access private resources that reside inside a VPC and have no public endpoint (such as an Amazon RDS database in a private subnet or an internal ElastiCache cluster)
C) Whenever the function runtime is Python or Node.js
D) Whenever the function uses environment variables

53. A developer attaches a Lambda function to an Amazon VPC by specifying private subnets and a Security Group so it can query a private Amazon RDS MySQL instance. Immediately after this configuration, the function can query RDS, but its existing HTTP call to a public third-party weather API begins timing out. What is the root cause?
A) The Lambda function runtime ran out of memory
B) Attaching a Lambda function to private subnets routes all outbound traffic through the VPC, removing its default public internet route; without a NAT Gateway in the VPC, external internet calls fail
C) MySQL blocks all outbound HTTP connections from the Lambda function
D) The third-party weather API blocked AWS IP ranges

54. How can the developer resolve the issue in the previous question so the Lambda function can access BOTH the private RDS database AND the public weather API?
A) Deploy a NAT Gateway in a public subnet of the VPC, and add a route in the private subnet's route table directing `0.0.0.0/0` to the NAT Gateway
B) Move the Lambda function into a public subnet
C) Assign an Elastic IP address directly to the Lambda function
D) Disable the Security Group on the RDS database

55. Why does placing a VPC-attached Lambda function in a public subnet NOT grant it direct internet access?
A) Lambda functions attached to a VPC do not receive public IP addresses; even in a public subnet, without a public IP, traffic cannot be routed through an Internet Gateway
B) Public subnets do not support Lambda execution roles
C) Internet Gateways block all Lambda traffic
D) Lambda only supports private subnets

56. What underlying technology did AWS introduce in 2019 (Hyperplane ENIs) to dramatically reduce cold-start latency for VPC-enabled Lambda functions?
A) Pre-provisioned, shared Elastic Network Interfaces (ENIs) created per unique subnet and security group combination, shared across multiple execution environments and functions rather than creating a new ENI per function instance
B) Moving all Lambda functions onto physical bare-metal servers
C) Running Lambda exclusively in AWS CloudFront edge locations
D) Eliminating VPC security groups

57. When configuring a Lambda function for VPC access, what two networking attributes must be specified in the function configuration? (Select TWO.)
A) At least two private subnets across different Availability Zones (for high availability)
B) One or more Security Groups to control network access for the function's ENIs
C) The root password of the VPC Internet Gateway
D) An Elastic IP address allocated to the Lambda function
E) A public Route 53 domain name

58. An order processing Lambda function in a VPC needs to query an Amazon RDS PostgreSQL database in a private subnet. How should the RDS database's Security Group be configured to allow connections from Lambda?
A) Add an inbound rule on TCP port 5432 with the source set to `0.0.0.0/0`
B) Add an inbound rule on TCP port 5432 with the source set to the Security Group ID assigned to the Lambda function
C) Add an inbound rule allowing all ICMP traffic from the Internet Gateway
D) Disable the RDS Security Group completely

59. What IAM permissions must be included in a Lambda function's execution role to allow it to create and manage Elastic Network Interfaces (ENIs) when attached to a VPC?
A) `AWSLambdaVPCAccessExecutionRole` managed policy (which grants `ec2:CreateNetworkInterface`, `ec2:DescribeNetworkInterfaces`, and `ec2:DeleteNetworkInterface`)
B) `AdministratorAccess`
C) `AmazonS3FullAccess`
D) `AWSLambdaBasicExecutionRole` only

60. What happens if a Lambda function configured for VPC access has an execution role that lacks the `ec2:CreateNetworkInterface` permission?
A) The function executes without VPC access
B) Function invocations fail with an `InvalidParameterValueException` or `EC2AccessDeniedException` indicating missing ENI creation permissions
C) The VPC is automatically deleted
D) The function switches to an on-premises execution environment

61. A VPC-attached Lambda function needs to write execution logs to Amazon CloudWatch Logs. The private subnets do NOT have a NAT Gateway. How can the developer ensure CloudWatch Logs continue to be captured?
A) Create an Interface VPC Endpoint for CloudWatch Logs (`com.amazonaws.<region>.logs`) in the VPC private subnets
B) CloudWatch Logs cannot be used with VPC-attached Lambda functions
C) Store logs in local `/tmp` storage only
D) Re-deploy the Lambda function every 5 minutes

62. An application experiences intermittent Lambda throttling and failures when creating VPC connections during sudden traffic spikes. What VPC subnet configuration issue could cause this?
A) The specified private subnets ran out of available private IP addresses, preventing the creation or scaling of Hyperplane ENIs
B) The VPC CIDR block is too large
C) The NAT Gateway was assigned an Elastic IP
D) The Lambda function memory was set to 10 GB

63. What is the AWS best practice recommendation for sizing VPC subnets used by VPC-attached Lambda functions?
A) Use small `/28` subnets with only 11 available IP addresses
B) Use adequately sized subnets (such as `/24` or `/22`) across multiple Availability Zones to ensure sufficient free IP addresses for ENI allocation during scaling
C) Share a single `/30` subnet with all RDS databases
D) Use public subnets exclusively

64. A developer wants a VPC-attached Lambda function to access an Amazon DynamoDB table without sending traffic through a NAT Gateway. What should the developer configure?
A) Add a Gateway VPC Endpoint for DynamoDB and associate it with the route table of the Lambda function's subnets
B) Assign an Elastic IP to the DynamoDB table
C) Connect DynamoDB to the Lambda function via an SSH tunnel
D) Disable encryption on the DynamoDB table

65. A developer is testing a VPC-attached Lambda function that communicates with an Amazon ElastiCache for Redis cluster. The function times out after 15 seconds. What is the most common misconfiguration?
A) The ElastiCache security group does not allow inbound traffic on port 6379 from the Lambda function's security group, or the subnets lack network connectivity
B) Redis does not support Lambda connections
C) Lambda functions cannot run in the same VPC as ElastiCache
D) ElastiCache requires an Internet Gateway

66. How does AWS Lambda handle ENI lifecycle management for VPC-attached functions when functions are deleted or updated?
A) Lambda automatically reclaims and deletes unused Hyperplane ENIs after a period of inactivity
B) Developers must manually delete ENIs using the EC2 console
C) ENIs remain forever and incur continuous billing
D) The VPC must be deleted to release ENIs

67. A Lambda function attached to a VPC needs to retrieve database credentials from AWS Secrets Manager on every cold start. The VPC has no NAT Gateway. What solution provides the fastest, most secure, and cost-effective access?
A) Interface VPC Endpoint for Secrets Manager (`com.amazonaws.<region>.secretsmanager`) deployed in the Lambda subnets
B) Hardcoding the database password in the Lambda environment variables in plain text
C) Creating an Internet Gateway in the private subnet
D) Emailing the password to the Lambda function via SNS

68. When deploying a VPC-attached Lambda function using AWS SAM or CloudFormation, how is the VPC configuration defined in YAML?
A) Under `VpcConfig: { SubnetIds: [...], SecurityGroupIds: [...] }`
B) Under `Network: { VPC: "vpc-xxxx" }`
C) In `Parameters: VPC:`
D) In `Outputs: VPC:`

69. What is a key architectural reason to AVOID attaching a Lambda function to a VPC if it only interacts with Amazon S3, Amazon DynamoDB, and Amazon SQS?
A) Lambda functions cannot access S3 from within a VPC
B) Lambda by default can access S3, DynamoDB, and SQS securely over AWS service endpoints without the added complexity, ENI management, or potential cold-start overhead of VPC attachment
C) SQS requires physical server hardware
D) DynamoDB requires public IP addresses

70. If a Lambda function in a VPC needs to communicate with an external SaaS service that requires IP whitelisting (firewall allowlist), how can the developer provide a fixed, predictable public IP for the Lambda traffic?
A) Route the Lambda function's outbound traffic through a NAT Gateway with an associated static Elastic IP (EIP), and provide that EIP to the SaaS provider
B) Assign an Elastic IP directly to the Lambda function
C) Lambda cannot support IP whitelisting
D) Ask the SaaS provider to allow all AWS IP ranges

71. A developer observes that Lambda function execution duration increased by 200ms after configuring VPC access. What is the primary contributor to this duration increase?
A) Network hop latency through ENIs and VPC routing compared to direct internal AWS service endpoints
B) Lambda allocating less CPU when in a VPC
C) CloudWatch disabling metrics
D) DynamoDB throttling the function

72. An organization requires that all Lambda functions accessing sensitive patient health data (PHI) in an Aurora PostgreSQL database must be isolated from the public internet entirely (no NAT Gateway, no IGW). How can the function still download required data from an S3 bucket in the same Region?
A) Create an S3 Gateway VPC Endpoint in the VPC and attach it to the private route table
B) Enable public access on the S3 bucket
C) Copy the data to an EBS volume attached to Lambda
D) Send the data over an unencrypted email

73. What tool can a developer use to capture and inspect IP traffic flowing to and from a VPC-attached Lambda function's network interface for security auditing?
A) VPC Flow Logs
B) AWS Cloud9 terminal
C) S3 Select
D) Route 53 Health Checks

74. A developer is designing a serverless backend. The architecture includes an API Gateway, Lambda functions in a VPC, Amazon RDS Proxy, and Amazon Aurora. What is the role of Amazon RDS Proxy in this VPC architecture?
A) It manages a shared connection pool between the bursty Lambda execution environments and the Aurora database, preventing connection exhaustion on Aurora
B) It converts SQL queries into GraphQL
C) It replaces the need for a VPC Security Group
D) It acts as an Internet Gateway

75. If a developer removes the VPC configuration from a Lambda function, what immediate change occurs to its networking?
A) The function is terminated immediately
B) The function's execution environments revert to running in the standard AWS-managed Lambda network with direct public internet access and no access to private VPC resources
C) All S3 buckets in the account are deleted
D) The Lambda function code is deleted

---

### Elastic Load Balancing, Route 53 & CloudFront for Developers (76–125)

76. A developer is deploying an Application Load Balancer (ALB) to route public HTTP and HTTPS traffic to an application running on EC2 instances in private subnets. In which subnets must the ALB itself be provisioned?
A) In at least two public subnets across different Availability Zones
B) In private subnets only
C) In a single subnet in `us-east-1a`
D) On an on-premises router

77. What is the primary difference between an Internet-Facing Load Balancer and an Internal Load Balancer in AWS?
A) An internet-facing load balancer has public IP addresses and routes public internet traffic to targets; an internal load balancer has private IP addresses only and routes traffic strictly within a VPC or connected networks
B) Internal load balancers do not support HTTP
C) Internet-facing load balancers cannot perform health checks
D) Internal load balancers are only available in GovCloud

78. A company wants to register a root domain name `example.com` (zone apex) and point it to an Application Load Balancer. Standard DNS specification (RFC 1034) prohibits CNAME records at the zone apex. Which Amazon Route 53 record type solves this limitation?
A) A Record (standard IPv4) with a hardcoded IP
B) Route 53 Alias Record (pointing to the ALB's dualstack DNS name)
C) PTR Record
D) TXT Record

79. What are two key advantages of using Route 53 Alias records instead of standard CNAME records when pointing to AWS resources like CloudFront, ALBs, or S3 website endpoints? (Select TWO.)
A) Alias records can be created at the zone apex (`example.com`)
B) Route 53 does not charge for queries to Alias records that resolve to AWS resources (e.g., ALBs, CloudFront distributions, S3 buckets)
C) Alias records work with external non-AWS servers
D) Alias records disable SSL/TLS requirements
E) Alias records eliminate the need for Route 53 Hosted Zones

80. What is the difference between a Route 53 Public Hosted Zone and a Private Hosted Zone?
A) A Public Hosted Zone resolves DNS queries on the public internet; a Private Hosted Zone resolves DNS queries only within one or more specified Amazon VPCs
B) Private Hosted Zones do not support A records
C) Public Hosted Zones are completely free of charge
D) Private Hosted Zones can only be queried from on-premises

81. A company runs an active-passive disaster recovery architecture. Primary traffic goes to an ALB in `us-east-1`, while backup traffic routes to a static error site hosted on Amazon S3 in `us-west-2`. Which Route 53 routing policy automatically redirects traffic to the backup site when the primary ALB fails a health check?
A) Simple routing
B) Failover routing policy (with a Route 53 Health Check on the primary record)
C) Geolocation routing policy
D) Multivalue answer routing policy

82. A developer wants to split user traffic 80/20 between an existing production version (80%) and a newly deployed canary version (20%) of a web application to test stability under real load. Which Route 53 routing policy supports this traffic splitting?
A) Latency routing policy
B) Weighted routing policy
C) Geoproximity routing policy
D) Failover routing policy

83. A global web service has application deployments in `us-east-1`, `eu-west-1`, and `ap-southeast-1`. The team wants users in Europe to be routed to the European deployment and users in Asia to the Asian deployment to achieve the lowest network latency. Which Route 53 routing policy should be used?
A) Latency-based routing policy (or Geolocation routing policy)
B) Simple routing policy
C) Failover routing policy
D) Weighted routing policy with equal weights

84. How does a Route 53 Health Check monitor the health of an endpoint?
A) By sending periodic HTTP, HTTPS, or TCP requests to the specified IP address or domain name and path from global Route 53 health checkers, verifying response status codes within a timeout threshold
B) By running an SSH script on the server
C) By checking the S3 bucket size
D) By inspecting IAM policies

85. A media company hosts video files on Amazon S3 behind an Amazon CloudFront distribution. The company wants to ensure that users CANNOT bypass CloudFront and download videos directly from the S3 bucket URL. Which CloudFront feature restricts S3 bucket access exclusively to the CloudFront distribution?
A) CloudFront Origin Access Control (OAC)
B) Route 53 Latency Routing
C) S3 Cross-Region Replication
D) S3 Transfer Acceleration alone

86. What bucket policy configuration is required when using CloudFront Origin Access Control (OAC) to secure an S3 bucket?
A) A bucket policy granting `s3:GetObject` to the CloudFront service principal (`cloudfront.amazonaws.com`) with a condition matching the distribution's ARN (`StringEquals: { "AWS:SourceArn": "arn:aws:cloudfront::.../distribution/<id>" }`)
B) A bucket policy granting `s3:*` to `Principal: "*"`
C) Disabling S3 Block Public Access completely
D) A bucket policy allowing access to all IAM users

87. Why is Origin Access Control (OAC) recommended over the legacy Origin Access Identity (OAI) for securing S3 origins in CloudFront?
A) OAC supports all Amazon S3 buckets in all AWS Regions, supports SSE-KMS encrypted objects, supports dynamic HTTP methods (PUT, POST, DELETE), and provides enhanced security via SigV4 signing
B) OAI is slower than OAC
C) OAI requires an EC2 instance
D) OAC is completely free while OAI charges $10 per month

88. A premium video-on-demand platform wants to grant paying subscribers temporary access to download a specific high-resolution movie file through CloudFront. The download link must expire after 2 hours and be restricted to the user. Which CloudFront feature should the backend use to generate this secure link?
A) CloudFront Signed URL
B) CloudFront Origin Request Policy
C) S3 Bucket ACL
D) Route 53 Weighted Record

89. A subscription streaming website delivers HLS (HTTP Live Streaming) video content consisting of hundreds of `.ts` media segments and a master `.m3u8` playlist. Which CloudFront mechanism is BEST suited for controlling subscriber access across multiple related media files without rewriting hundreds of individual URLs?
A) CloudFront Signed Cookies
B) CloudFront Signed URLs for every `.ts` segment file
C) AWS WAF Rate Limiting
D) S3 Object Versioning

90. What cryptographic component is used by an application server to generate CloudFront Signed URLs and Signed Cookies?
A) A private key from a CloudFront Key Group (or public/private key pair associated with an authorized account)
B) An AWS KMS customer master key directly without CloudFront integration
C) The root user password of the AWS account
D) An Amazon Cognito Identity Pool ID

91. What are the two primary edge compute options available in Amazon CloudFront for running code close to end users? (Select TWO.)
A) CloudFront Functions
B) AWS Lambda@Edge
C) AWS Step Functions Edge
D) Amazon EC2 Spot Fleet
E) Amazon EMR on EKS

92. A developer needs to inspect incoming HTTP request headers, normalize the `Accept-Language` header to 2-character country codes, and rewrite URL paths at edge locations before the CloudFront cache key is computed. The operation must execute in sub-milliseconds with ultra-low cost and requires no network access. Which edge compute solution is the BEST fit?
A) CloudFront Functions (executed on Viewer Request)
B) Lambda@Edge
C) Amazon Athena
D) AWS CodeBuild

93. A developer needs to authenticate incoming requests at the CloudFront edge by validating JWT tokens against an external OAuth authorization server, and perform dynamic image resizing on origin response before returning the image to the client. Which edge compute solution is required?
A) AWS Lambda@Edge (supports third-party network calls, external libraries, and origin-request/origin-response trigger events)
B) CloudFront Functions
C) S3 Select
D) Route 53 Resolver

94. What are the four trigger lifecycle events supported by Lambda@Edge in a CloudFront distribution?
A) Viewer Request, Origin Request, Origin Response, and Viewer Response
B) PreBuild, Build, PostBuild, and Deploy
C) ClientInit, ServerInit, Handshake, and Close
D) GET, POST, PUT, and DELETE

95. Which two trigger events are supported by CloudFront Functions? (Select TWO.)
A) Viewer Request
B) Viewer Response
C) Origin Request
D) Origin Response
E) Edge Failover

96. In which AWS Region must an AWS Lambda function be authored and published as a numbered version before it can be associated with a CloudFront distribution as a Lambda@Edge function?
A) `us-east-1` (N. Virginia)
B) `us-west-2` (Oregon)
C) Any Region where the user resides
D) `eu-west-1` (Ireland)

97. An e-commerce website uses CloudFront in front of an Application Load Balancer. The developer wants to automatically redirect all HTTP traffic to HTTPS at the edge before requests reach the origin. Which setting in the CloudFront Cache Behavior enforces this?
A) Viewer Protocol Policy set to `Redirect HTTP to HTTPS` (or `HTTPS Only`)
B) Origin Protocol Policy set to HTTP Only
C) Invalidation of `/*`
D) S3 Transfer Acceleration

98. A company wants to restrict access to a CloudFront distribution so that users from specific sanctioned countries cannot access the content. Which CloudFront feature enforces geographic access restrictions?
A) CloudFront Geographic Restrictions (Geo-blocking allowlist or blocklist)
B) Route 53 Simple Routing
C) Amazon RDS Parameter Groups
D) S3 Bucket Encryption

99. A developer wants to cache static images (`/images/*`) for 30 days in CloudFront, while routing dynamic API calls (`/api/*`) directly to an ALB without caching. How is this configured in a single CloudFront distribution?
A) Create multiple Cache Behaviors with distinct Path Patterns: configure `/images/*` with high TTLs and `/api/*` with caching disabled (TTL=0 / Managed-CachingDisabled policy) pointing to the ALB origin
B) Deploy two separate CloudFront distributions
C) Disable CloudFront caching globally
D) Write custom bash scripts in EC2 UserData

100. What is a CloudFront Cache Policy?
A) A configuration object that defines which query strings, headers, and cookies are included in the cache key, as well as minimum, maximum, and default TTL settings
B) An IAM user permission policy
C) A database backup schedule
D) A VPC route table entry

101. What is the difference between a CloudFront Cache Policy and an Origin Request Policy?
A) A Cache Policy defines what values participate in the cache key to determine cache hits; an Origin Request Policy defines which headers, cookies, and query strings are forwarded to the origin on a cache miss without affecting the cache key
B) A Cache Policy is for S3; an Origin Request Policy is for EC2
C) Both policies are identical
D) Origin Request Policies only apply to Route 53

102. An API Gateway REST API is deployed in `us-west-2`. The developer wants to reduce latency for global API callers by using CloudFront. What type of API Gateway endpoint type automatically provisions and manages an integrated CloudFront distribution in front of the API?
A) Edge-Optimized API Endpoint
B) Regional API Endpoint
C) Private API Endpoint
D) VPC Endpoint

103. When should a developer choose a Regional API Gateway endpoint paired with a custom CloudFront distribution instead of a standard Edge-Optimized API Gateway endpoint?
A) When the developer needs custom cache behaviors, AWS WAF rules, Lambda@Edge functions, or multi-origin routing under a single domain name
B) When the API must only be called from inside a VPC
C) When the API is written in Python
D) When the API has fewer than 10 users

104. A developer configures Custom Error Responses in Amazon CloudFront. What capability does this feature provide for Single Page Applications (SPAs)?
A) It intercepts HTTP 403 or 404 errors from an S3 origin and returns `index.html` with an HTTP 200 status code, allowing client-side routers (e.g., React Router) to handle the URL route
B) It reboots the origin server upon receiving a 500 error
C) It deletes corrupt S3 objects
D) It converts XML responses to JSON

105. What is the maximum file size supported for a single object uploaded or downloaded through Amazon CloudFront?
A) 30 GB
B) 5 GB
C) 5 TB (matching Amazon S3 maximum object size)
D) 100 MB

106. An ALB targets EC2 instances in private subnets across two AZs. The ALB is internet-facing and has Cross-Zone Load Balancing enabled. How does Cross-Zone Load Balancing improve application traffic distribution?
A) It distributes incoming traffic evenly across all registered backend targets in all enabled Availability Zones, preventing unbalanced load when AZ traffic is uneven
B) It routes traffic to instances in other AWS accounts
C) It replicates EBS volumes across AZs
D) It converts HTTP requests to UDP

107. Which load balancer type operates at Layer 7 (Application Layer) of the OSI model and supports path-based routing, host-based routing, HTTP/2, and native WebSocket protocols?
A) Application Load Balancer (ALB)
B) Network Load Balancer (NLB)
C) Gateway Load Balancer (GWLB)
D) Classic Load Balancer (CLB)

108. Which load balancer type operates at Layer 4 (Transport Layer), is capable of handling millions of requests per second with ultra-low latency, and provides static IP addresses per Availability Zone?
A) Network Load Balancer (NLB)
B) Application Load Balancer (ALB)
C) Classic Load Balancer (CLB)
D) Gateway Load Balancer (GWLB)

109. How does an Application Load Balancer verify whether an EC2 target is healthy before routing user traffic to it?
A) By sending periodic health check requests to a configured path (e.g., `GET /health`) and verifying that the target responds with a success HTTP status code (e.g., 200) within the threshold
B) By pinging the instance using ICMP
C) By checking the instance CPU utilization in CloudWatch
D) By inspecting the git commit history

110. A developer wants an ALB to route requests for `example.com/api/*` to an API Target Group and requests for `example.com/static/*` to a Static Target Group. What ALB feature enables this routing?
A) Path-Based Listener Rules
B) Host-Based Listener Rules
C) Route 53 Weighted Records
D) Security Group ingress rules

111. What HTTP header does an Application Load Balancer append to incoming client requests so that backend EC2 instances know the original IP address of the calling client?
A) `X-Forwarded-For`
B) `X-Amzn-Trace-Id`
C) `User-Agent`
D) `Authorization`

112. What HTTP header does an Application Load Balancer append to incoming requests to support end-to-end distributed tracing with AWS X-Ray?
A) `X-Amzn-Trace-Id`
B) `X-Forwarded-Proto`
C) `Content-Type`
D) `Host`

113. An application running on EC2 instances behind an ALB requires sticky sessions (session affinity) so that requests from the same user are consistently routed to the same backend instance. What mechanism does the ALB use to maintain stickiness?
A) An HTTP cookie (either ALB-generated duration-based cookie or application-based cookie)
B) Client IP address hashing only
C) DNS round-robin
D) Hardcoding the instance ID in the URL

114. A developer wants to terminate SSL/TLS encryption at the Application Load Balancer and use a free SSL certificate that automatically renews. Which AWS service provides and manages this certificate?
A) AWS Certificate Manager (ACM)
B) AWS Secrets Manager
C) AWS KMS
D) AWS Directory Service

115. What ALB feature allows hosting multiple websites with different SSL/TLS certificates on the same ALB listener and port (443)?
A) Server Name Indication (SNI)
B) Cross-Origin Resource Sharing (CORS)
C) Route 53 Geolocation
D) VPC Peering

116. When an ALB targets AWS Lambda functions in a Target Group, what data format does the ALB use to pass incoming HTTP requests to the Lambda handler?
A) A standardized JSON event object containing HTTP method, path, headers, query string parameters, and body
B) Raw TCP byte stream
C) An XML document
D) A CSV string

117. What status code does an ALB return to clients when all target instances in a Target Group fail health checks?
A) 503 Service Unavailable (or 502 Bad Gateway)
B) 200 OK
C) 404 Not Found
D) 301 Moved Permanently

118. A developer wants to register an Amazon Route 53 private hosted zone `corp.internal` to resolve internal domain names. Which requirement must be met?
A) The private hosted zone must be associated with at least one Amazon VPC in the AWS account
B) The domain must be registered through an external registrar
C) The VPC must have an Internet Gateway attached
D) Public DNS queries must be allowed from `0.0.0.0/0`

119. What Route 53 routing policy should be used when a developer wants to return up to 8 randomly selected healthy IP addresses in response to DNS queries, providing DNS-level load balancing with health checking?
A) Multivalue Answer routing policy
B) Simple routing policy
C) Geolocation routing policy
D) Failover routing policy

120. How does Amazon Route 53 Resolver handle DNS queries from resources within an Amazon VPC?
A) By querying the VPC Route 53 Resolver (the `.2` IP address of the VPC CIDR block, e.g., `10.0.0.2` or AmazonProvidedDNS)
B) By querying public Google DNS `8.8.8.8`
C) By routing DNS queries through an S3 bucket
D) By executing a Lambda function on every query

121. An application deployed across two AWS accounts needs to share a private Route 53 hosted zone. Is this supported?
A) Yes, by authorizing the VPC in the second account to associate with the private hosted zone using the Route 53 API (`CreateVPCAssociationAuthorization`)
B) No, private hosted zones can only be associated with VPCs in the same AWS account
C) Yes, but only if both accounts use the same credit card
D) No, Route 53 does not support multiple VPCs

122. A developer wants to invalidate a cached file `/index.html` in an Amazon CloudFront distribution immediately following a software update. What is the syntax of the invalidation path?
A) `/index.html` (or `/*` for all files)
B) `s3://bucket/index.html`
C) `DELETE /index.html`
D) `RESET CACHE`

123. How are CloudFront invalidation requests priced?
A) The first 1,000 invalidation paths submitted each month are free; subsequent invalidation paths incur a small fee per path
B) $10 per invalidation request
C) Invalidation is completely free without limits
D) Invalidation is only available to Enterprise Support customers

124. An application uses Amazon CloudFront to serve videos. The developer wants to restrict access so that requests are only served if they arrive over HTTPS. What setting enforces this in the CloudFront distribution?
A) Set Viewer Protocol Policy to `HTTPS Only`
B) Delete all HTTP ports
C) Disable DNS
D) Block port 80 in the client browser

125. An architect is reviewing an end-to-end secure networking design for a corporate web portal:
1. Public internet traffic must terminate at CloudFront with global edge caching and WAF inspection.
2. The S3 origin must ONLY accept requests from the CloudFront distribution.
3. API Gateway must securely invoke a Lambda function deployed in a VPC.
4. The Lambda function must access an Amazon RDS PostgreSQL database in private subnets and fetch credentials from Secrets Manager without leaving the AWS network.
Which combination of networking features correctly fulfills this architecture?
A) CloudFront with Origin Access Control (OAC) + VPC-attached Lambda function in private subnets + Interface VPC Endpoint for Secrets Manager + RDS Security Group allowing inbound traffic from Lambda Security Group
B) Public S3 bucket + Lambda with no VPC + NAT Gateway for RDS + Route 53 Simple routing
C) CloudFront without OAC + Lambda in public subnet + RDS with public IP + Gateway Endpoint for Secrets Manager
D) Internet Gateway for RDS + Elastic Beanstalk single instance + S3 website hosting

---

## Answer Key & Explanations

1. B — Placing databases in private subnets without an Internet Gateway route prevents direct inbound access from the public internet.
2. A — A public subnet has a route in its route table pointing default outbound traffic (`0.0.0.0/0`) to an attached Internet Gateway (IGW).
3. A — Instances in a public subnet must have a public IPv4 or Elastic IP assigned in addition to the IGW route to communicate with the internet.
4. B — A NAT Gateway provides outbound-only internet connectivity for instances in private subnets while blocking unsolicited inbound traffic.
5. B — A NAT Gateway must be located in a public subnet with an allocated Elastic IP (EIP) and a route to an Internet Gateway.
6. A & B — Gateway Endpoints for S3/DynamoDB are free, and Interface Endpoints keep AWS service traffic private, bypassing NAT Gateway data transfer fees.
7. B — The private subnet route table must route `0.0.0.0/0` to the NAT Gateway (`nat-xxxx`) to enable outbound internet access.
8. A — NAT Gateways are managed, auto-scaling up to 100 Gbps, and require no OS patching; NAT Instances are self-managed EC2 instances with manual scaling.
9. B — High availability requires deploying a dedicated NAT Gateway in each Availability Zone and routing each private subnet to its AZ's NAT Gateway.
10. A — For a NAT Gateway to work, its hosting public subnet must route `0.0.0.0/0` to an IGW and have an associated Elastic IP address.
11. B — Instances requiring two-way internet communication must reside in a public subnet with an IGW route, public IP, and open security group rules.
12. A — An Amazon VPC can have exactly one Internet Gateway attached at a time.
13. B — The default `local` route in every VPC route table automatically enables communication between all subnets within that VPC.
14. B — Subnets within the same VPC communicate privately and directly via the VPC's internal `local` route.
15. B — Security Groups operate at the individual instance/ENI level as stateful virtual firewalls.
16. B — Network ACLs (NACLs) operate at the subnet boundary as stateless packet-filtering firewalls.
17. B — Security Groups are stateful; return traffic for an allowed inbound connection is automatically allowed outbound regardless of outbound rules.
18. A — NACLs are stateless, requiring explicit outbound rules for ephemeral client ports (1024–65535) to allow response traffic back to clients.
19. B — Referencing the web service's Security Group ID as the source in the backend Security Group enforces least-privilege security-group chaining.
20. B — An Elastic IP (EIP) is a static, persistent public IPv4 address allocated to an AWS account that can be dynamically remapped to instances.
21. A — If a subnet has no route to an Internet Gateway, resources in it cannot be reached from the internet, even if an EIP is attached.
22. B — Without a route for `0.0.0.0/0`, any non-local traffic is dropped, resulting in an isolated private subnet.
23. A — A Virtual Private Gateway (VGW) or AWS Transit Gateway terminates Site-to-Site VPN connections on the AWS VPC side.
24. A — The maximum MTU for traffic crossing an Internet Gateway, NAT Gateway, or Inter-Region peering connection is 1,500 bytes.
25. A — VPC Peering connects two VPCs directly using AWS's private network infrastructure without internet traversal.
26. B — An S3 Gateway VPC Endpoint routes traffic privately from VPC subnets to S3 over AWS internal networks at zero additional cost.
27. A & B — Amazon S3 and Amazon DynamoDB are the only two AWS services that support Gateway VPC Endpoints.
28. B — Gateway Endpoints add a prefix list route (e.g., `pl-63a5400a`) to VPC route tables directing S3/DynamoDB traffic to the gateway.
29. B — AWS Secrets Manager supports Interface VPC Endpoints (AWS PrivateLink), creating private ENIs inside VPC subnets.
30. A — Interface VPC Endpoints create Elastic Network Interfaces (ENIs) with private IP addresses from the chosen subnets.
31. A — Enabling Private DNS on an Interface Endpoint resolves the standard public service DNS name to the private endpoint ENI IP.
32. A & B — Interface Endpoints are secured using attached Security Groups (on ENIs) and Endpoint Policies (restricting IAM actions/resources).
33. A — Interface Endpoints have private IPs reachable over Direct Connect/VPN from on-premises; Gateway Endpoints are VPC-internal only.
34. A — An Endpoint Policy with an explicit `Allow` on `Resource: [arn:aws:s3:::my-company-data/*]` restricts access to the designated bucket only.
35. B — Gateway VPC Endpoints for S3 and DynamoDB have no hourly or data processing charges.
36. B — Interface VPC Endpoints (PrivateLink) are billed per hourly ENI provisioned per AZ plus per-GB data processed.
37. B — Each distinct AWS service requires its own dedicated Interface VPC Endpoint (one for SQS, one for SNS, one for KMS).
38. B — VPC Endpoint Services (PrivateLink) allow exposing custom services behind an NLB/ALB to other VPCs privately.
39. A — PrivateLink provisions an ENI with a private IP in each selected AZ's subnet to ensure Multi-AZ fault tolerance.
40. A — Gateway Endpoints must be associated with the specific Route Tables used by the subnets that need private access.
41. A — CloudWatch Logs, Secrets Manager, Kinesis, CodeCommit, and dozens of other AWS services support Interface Endpoints.
42. A — The `aws:sourceVpce` condition key restricts S3 bucket access to requests routed through the specified VPC Endpoint ID.
43. B — The more specific S3 prefix list route takes precedence over the default `0.0.0.0/0` route, directing S3 traffic to the Gateway Endpoint.
44. A — The Security Group attached to the Interface Endpoint ENI must permit inbound HTTPS (port 443) from the application instances.
45. B — An Interface VPC Endpoint for `execute-api` allows private access to API Gateway Private REST APIs from within the VPC.
46. A — `aws:sourceVpc` restricts by VPC ID; `aws:sourceVpce` restricts by VPC Endpoint ID.
47. B — The application uses standard DynamoDB SDK calls and URLs; traffic routing to the Gateway Endpoint is handled transparently by route tables.
48. A — S3 Server Access Logs and VPC Flow Logs record private IP addresses and endpoint identifiers for verified private routing.
49. A — An Interface VPC Endpoint for `logs` keeps all CloudWatch Logs traffic within the AWS private network.
50. A — VPC Endpoints enhance security (traffic stays on private AWS network), lower latency, and eliminate NAT Gateway data processing fees.
51. B — By default, Lambda runs in a managed execution environment with direct outbound access to the internet and public AWS endpoints.
52. B — Lambda requires VPC configuration only when it needs to reach private resources with no public endpoint (e.g., RDS in private subnets).
53. B — VPC attachment routes all outbound Lambda traffic through the private subnet; without a NAT Gateway, internet calls fail.
54. A — Adding a NAT Gateway in a public subnet and routing private subnet `0.0.0.0/0` traffic to it restores internet connectivity for Lambda.
55. A — VPC-attached Lambda functions do not receive public IP addresses, so they cannot route through an Internet Gateway even in a public subnet.
56. A — Hyperplane ENIs use shared, pre-provisioned network interfaces per subnet/security group, drastically reducing cold-start latency.
57. A & B — Configuring VPC access for Lambda requires selecting private subnets (across multiple AZs) and Security Groups.
58. B — The RDS Security Group should allow inbound traffic on port 5432 sourcing the Lambda function's Security Group ID.
59. A — The `AWSLambdaVPCAccessExecutionRole` policy grants permissions to create, describe, and delete ENIs.
60. B — Without `ec2:CreateNetworkInterface` permissions, VPC-attached Lambda function invocations fail with authorization errors.
61. A — Deploying an Interface VPC Endpoint for CloudWatch Logs allows VPC-attached Lambda functions to ship logs without a NAT Gateway.
62. A — Exhausting available private IP addresses in the configured subnets prevents Lambda from allocating Hyperplane ENIs during scaling.
63. B — AWS recommends using sufficiently large subnets (e.g., `/24`) across multiple AZs to ensure adequate IP availability.
64. A — An S3 or DynamoDB Gateway VPC Endpoint associated with the Lambda subnets provides private access without a NAT Gateway.
65. A — Timeouts connecting to ElastiCache are typically caused by missing inbound rules on port 6379 in the Redis Security Group.
66. A — AWS Lambda automatically reclaims and deletes unneeded Hyperplane ENIs after periods of inactivity.
67. A — An Interface VPC Endpoint for Secrets Manager provides secure, private, and low-latency credential retrieval without internet egress.
68. A — In CloudFormation/SAM, VPC settings are configured under `VpcConfig: { SubnetIds: [...], SecurityGroupIds: [...] }`.
69. B — If Lambda only interacts with public AWS services (S3, DynamoDB, SQS), VPC attachment adds unnecessary complexity and ENI overhead.
70. A — Routing Lambda outbound traffic through a NAT Gateway with a fixed Elastic IP allows whitelisting that static IP on external services.
71. A — Network hops through ENIs and VPC routing introduce minor additional latency compared to direct AWS service endpoints.
72. A — An S3 Gateway VPC Endpoint enables private S3 access for fully isolated VPC subnets with no internet gateways.
73. A — VPC Flow Logs capture network traffic metadata at the ENI level for security analysis and connection troubleshooting.
74. A — Amazon RDS Proxy pools and multiplexes database connections, preventing Lambda concurrency spikes from overwhelming RDS.
75. B — Removing VPC configuration returns the Lambda function to the standard AWS-managed network with direct internet access.
76. A — An internet-facing ALB must be deployed in at least two public subnets across different Availability Zones.
77. A — Internet-facing load balancers route public internet traffic; internal load balancers have private IPs and route internal VPC traffic.
78. B — Route 53 Alias records resolve directly to the ALB's dualstack DNS name, supporting zone apex (`example.com`) mapping.
79. A & B — Alias records work at the zone apex (`example.com`) and queries to AWS resource targets are free of charge.
80. A — Public Hosted Zones resolve queries on the internet; Private Hosted Zones resolve queries strictly within associated VPCs.
81. B — A Failover routing policy coupled with a Route 53 Health Check automatically routes traffic to a secondary target upon primary failure.
82. B — Weighted routing policies split traffic based on assigned weight ratios (e.g., 80% to production, 20% to canary).
83. A — Latency-based routing directs users to the AWS Region that delivers the lowest round-trip network latency.
84. A — Route 53 Health Checks send periodic HTTP/HTTPS/TCP probes to endpoints and evaluate response codes against thresholds.
85. A — CloudFront Origin Access Control (OAC) restricts S3 bucket access so objects can only be fetched through CloudFront.
86. A — The S3 bucket policy must grant `s3:GetObject` to `cloudfront.amazonaws.com` with a condition matching the distribution ARN.
87. A — OAC supports all S3 buckets, SSE-KMS encryption, all HTTP methods, and enhanced SigV4 authentication over legacy OAI.
88. A — CloudFront Signed URLs provide temporary, authenticated access to individual files for authorized users.
89. A — CloudFront Signed Cookies grant access to multiple related files (like HLS video streams) without requiring individual signed URLs.
90. A — CloudFront Signed URLs and Cookies are signed using a private key from an authorized CloudFront Key Group.
91. A & B — CloudFront Functions (lightweight JS) and AWS Lambda@Edge (full Node.js/Python) are the two edge compute mechanisms in CloudFront.
92. A — CloudFront Functions execute in sub-milliseconds at edge PoPs, ideal for lightweight header and URL manipulation without network calls.
93. A — Lambda@Edge supports third-party network calls, external libraries, and complex compute at Regional Edge Caches.
94. A — Lambda@Edge can be triggered on Viewer Request, Origin Request, Origin Response, and Viewer Response events.
95. A & B — CloudFront Functions only support Viewer Request and Viewer Response triggers.
96. A — Lambda@Edge functions must be created and published as numbered versions in the `us-east-1` (N. Virginia) Region.
97. A — Setting Viewer Protocol Policy to `Redirect HTTP to HTTPS` automatically redirects insecure requests to HTTPS at the edge.
98. A — CloudFront Geographic Restrictions (Geo-blocking) allow or restrict content delivery based on viewer country codes.
99. A — Defining multiple Cache Behaviors in CloudFront allows applying distinct TTL and caching rules based on path patterns.
100. A — A CloudFront Cache Policy defines the cache key (headers, cookies, query strings) and TTL settings for cached responses.
101. A — A Cache Policy defines the cache key; an Origin Request Policy defines what headers/cookies are forwarded to the origin on a miss.
102. A — Edge-Optimized API Gateway endpoints automatically provision and manage an integrated CloudFront distribution.
103. A — Combining a Regional API Gateway with a custom CloudFront distribution allows custom cache behaviors, WAF rules, and edge compute.
104. A — CloudFront Custom Error Responses return `index.html` with a 200 status for 403/404 errors, enabling client-side SPA routing.
105. C — CloudFront supports objects up to 5 TB in size, matching the Amazon S3 maximum object size.
106. A — Cross-Zone Load Balancing distributes traffic evenly across all backend instances in all enabled AZs, balancing instance utilization.
107. A — Application Load Balancers operate at Layer 7 and support path/host routing, HTTP/2, and WebSockets.
108. A — Network Load Balancers operate at Layer 4, handling millions of requests per second with ultra-low latency and static IPs.
109. A — ALBs send periodic HTTP/HTTPS health checks to a designated path (e.g., `/health`) to verify target health.
110. A — Path-Based Listener Rules on an ALB route requests to specific Target Groups based on URL path patterns.
111. A — ALBs append the client's original IP address to the `X-Forwarded-For` HTTP request header.
112. A — ALBs append the `X-Amzn-Trace-Id` header to enable distributed request tracing with AWS X-Ray.
113. A — ALBs maintain session stickiness using HTTP cookies (either duration-based or application-based).
114. A — AWS Certificate Manager (ACM) provisions and automatically renews free SSL/TLS certificates for use with ALBs and CloudFront.
115. A — Server Name Indication (SNI) enables hosting multiple domains with distinct SSL certificates on a single ALB listener.
116. A — ALBs pass incoming HTTP requests to Lambda functions as structured JSON event objects.
117. A — When all backend targets in a Target Group fail health checks, the ALB returns HTTP 503 Service Unavailable (or 502).
118. A — A Route 53 Private Hosted Zone must be associated with at least one Amazon VPC to resolve DNS queries.
119. A — Multivalue Answer routing returns up to 8 healthy records randomly, providing DNS-based load balancing with health checks.
120. A — VPC instances query the Route 53 Resolver at the base VPC network CIDR `.2` address (e.g., `10.0.0.2` or AmazonProvidedDNS).
121. A — `CreateVPCAssociationAuthorization` allows associating VPCs from different AWS accounts with a shared Private Hosted Zone.
122. A — CloudFront invalidation uses the path format `/index.html` (or wildcard `/*`) to purge cached files from edge locations.
123. A — The first 1,000 invalidation paths per month are free; subsequent paths incur a small fee.
124. A — Setting Viewer Protocol Policy to `HTTPS Only` ensures CloudFront rejects unencrypted HTTP requests.
125. A — OAC secures S3 to CloudFront; VPC-attached Lambda reaches private RDS; Interface Endpoint keeps Secrets Manager traffic private.
"""

with open("15-Networking-for-Developers/questions.md", "w", encoding="utf-8") as f:
    f.write(questions_text)

print("Successfully wrote 15-Networking-for-Developers/questions.md")
