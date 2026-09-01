# Module 13 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### CloudFormation Core Sections & Intrinsic Functions (1–30)

1. A developer is authoring an AWS CloudFormation template to deploy an application across `dev`, `test`, and `prod` environments. The developer wants to use the exact same template file for all environments while passing different instance types and VPC IDs during stack creation. Which section of the CloudFormation template defines these dynamic runtime inputs?
A) `Mappings`
B) `Parameters`
C) `Conditions`
D) `Outputs`

2. A CloudFormation template requires a static lookup table that maps AWS Regions (e.g., `us-east-1`, `eu-west-1`) to specific regional AMI IDs. This mapping is fixed, known at template authoring time, and should not be passed as user input during stack creation. Which CloudFormation template section should be used?
A) `Parameters`
B) `Mappings`
C) `Resources`
D) `Metadata`

3. In a CloudFormation template, a developer needs to retrieve an AMI ID from a lookup table named `RegionToAmiMap` based on the current deployment Region (`AWS::Region`) and architecture (`HVM64`). Which intrinsic function should the developer use?
A) `!Ref RegionToAmiMap`
B) `!FindInMap [RegionToAmiMap, !Ref "AWS::Region", HVM64]`
C) `!GetAtt RegionToAmiMap.HVM64`
D) `!ImportValue RegionToAmiMap`

4. A developer needs to conditionally provision an Amazon SNS topic named `ProdAlertTopic` only when the `EnvironmentName` parameter is set to `prod`. What combination of template constructs is required?
A) Define a condition `IsProd: !Equals [!Ref EnvironmentName, prod]` in the `Conditions` section, and add `Condition: IsProd` to the `ProdAlertTopic` resource
B) Write an if/else bash script in `UserData`
C) Use AWS Lambda to delete the topic after stack creation if not in prod
D) Define three separate templates for dev, test, and prod

5. A developer wants to construct an S3 bucket name dynamically by combining an environment parameter (`EnvironmentName`) with the account ID and region (e.g., `mycompany-dev-123456789012-us-east-1-data`). Which intrinsic function provides the cleanest string interpolation syntax?
A) `!Sub "mycompany-${EnvironmentName}-${AWS::AccountId}-${AWS::Region}-data"`
B) `!Join ["-", ["mycompany", !Ref EnvironmentName, !Ref "AWS::AccountId", !Ref "AWS::Region", "data"]]`
C) `!Ref EnvironmentName`
D) `!GetAtt EnvironmentName.BucketName`

6. What is the fundamental difference between the `!Ref` function and the `!GetAtt` function when referencing an `AWS::EC2::Instance` resource named `MyInstance`?
A) `!Ref` returns the instance ID (e.g., `i-0123456789abcdef0`), whereas `!GetAtt MyInstance.PublicIp` returns specific named attributes such as the instance's public IP address or Availability Zone
B) `!Ref` can only be used on Parameters; `!GetAtt` can only be used on Resources
C) `!Ref` decrypts KMS keys; `!GetAtt` encrypts S3 objects
D) `!Ref` and `!GetAtt` are completely identical and interchangeable in all scenarios

7. A developer is referencing an `AWS::EC2::SecurityGroup` resource named `AppSecurityGroup` inside an `AWS::EC2::Instance` resource definition. What does `!GetAtt AppSecurityGroup.GroupId` return?
A) The physical ID of the security group (e.g., `sg-0123456789abcdef0`)
B) The VPC CIDR block
C) The list of inbound rules
D) The security group description string

8. Which intrinsic function in CloudFormation allows a template to evaluate whether a condition is true and return one value if true, and a different value if false (e.g., setting instance type to `t3.large` if `IsProd`, otherwise `t3.micro`)?
A) `!If [IsProd, "t3.large", "t3.micro"]`
B) `!Switch [IsProd, "t3.large", "t3.micro"]`
C) `!Select [0, ["t3.large", "t3.micro"]]`
D) `!Condition [IsProd]`

9. Which section of a CloudFormation template is the ONLY mandatory section required for a template to be valid?
A) `Parameters`
B) `Resources`
C) `Outputs`
D) `AWSTemplateFormatVersion`

10. A developer needs to construct a comma-delimited string of subnet IDs from a list parameter `SubnetList`. Which intrinsic function takes a delimiter and a list of values to produce a concatenated string?
A) `!Split`
B) `!Join [",", !Ref SubnetList]`
C) `!Sub`
D) `!GetAZs`

11. A developer is writing a CloudFormation template and needs to split a comma-separated string parameter `SubnetCIDRs` (e.g., `"10.0.1.0/24,10.0.2.0/24"`) into an importable list of strings. Which intrinsic function performs this operation?
A) `!Split [",", !Ref SubnetCIDRs]`
B) `!Join`
C) `!Select`
D) `!FindInMap`

12. In CloudFormation, what pseudo parameter automatically resolves to the 12-digit AWS account ID of the account in which the stack is being created?
A) `AWS::AccountId`
B) `AWS::StackId`
C) `AWS::Region`
D) `AWS::NotificationARNs`

13. Which pseudo parameter in CloudFormation resolves to the name of the current stack being created or updated?
A) `AWS::StackName`
B) `AWS::StackId`
C) `AWS::URLSuffix`
D) `AWS::NoValue`

14. What is the purpose of the `AWS::NoValue` pseudo parameter when used in conjunction with the `!If` intrinsic function on an optional resource property?
A) It causes CloudFormation to remove or omit the property from the resource definition if the condition evaluates to false
B) It sets the property value to an empty string `""`
C) It deletes the entire stack immediately
D) It throws a validation exception during stack creation

15. A developer wants to restrict the allowed values of a `DBInstanceClass` parameter in a CloudFormation template to only `db.t3.micro`, `db.t3.small`, and `db.t3.medium`. Which parameter attribute enforces this constraint?
A) `AllowedValues: [db.t3.micro, db.t3.small, db.t3.medium]`
B) `ConstraintDescription: "Only small instances"`
C) `AllowedPattern: "^db\..*"`
D) `MaxLength: 3`

16. A developer wants to mask sensitive parameter input (such as a database master password) in the AWS Management Console and CLI output during stack creation. Which parameter attribute achieves this?
A) `NoEcho: true`
B) `Secret: true`
C) `Encrypted: true`
D) `MaskInput: true`

17. A CloudFormation template requires the ID of the latest Amazon Linux 2 AMI without hardcoding AMI IDs or updating mappings every month. Which CloudFormation parameter type allows referencing the latest AMI ID directly from the AWS Systems Manager Parameter Store public parameter hierarchy?
A) `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` with Default `/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2`
B) `AWS::EC2::KeyPair::KeyName`
C) `CommaDelimitedList`
D) `List<AWS::EC2::VPC::Id>`

18. A developer wants to ensure that a CloudFormation parameter for `VpcId` only accepts valid, existing Amazon VPC IDs from the target AWS account in the console dropdown. Which AWS-specific parameter type should be used?
A) `String`
B) `AWS::EC2::VPC::Id`
C) `AWS::RDS::DBInstance::Id`
D) `Number`

19. In a CloudFormation template, what is the purpose of the `Outputs` section?
A) To print debug log messages during stack execution
B) To declare output values (such as an ALB DNS name or S3 bucket ARN) that can be viewed in the console, returned by CLI descriptions, or exported for cross-stack references
C) To define database schemas
D) To terminate EC2 instances upon stack completion

20. A developer needs to export an S3 bucket ARN created in a storage stack so that an application stack can reference it. What attribute must be added under the output item in the `Outputs` section?
A) `Export: Name: SharedBucketArn`
B) `Import: Name: SharedBucketArn`
C) `Public: true`
D) `Global: true`

21. In an application stack, how does the developer import the exported value named `SharedBucketArn` from the storage stack?
A) `!Ref SharedBucketArn`
B) `!ImportValue SharedBucketArn`
C) `!GetAtt SharedBucketArn.Arn`
D) `!FindInMap [SharedBucketArn]`

22. A developer is writing a CloudFormation template in YAML and wants to reference a resource in a shorthand format. Which two notations are valid equivalent syntax for calling `Fn::GetAtt` on a resource `MyBucket` to get its `Arn`? (Select TWO.)
A) `!GetAtt MyBucket.Arn`
B) `Fn::GetAtt: [MyBucket, Arn]`
C) `!Ref MyBucket.Arn`
D) `!GetAtt [MyBucket.Arn]`
E) `Fn::Ref: MyBucket.Arn`

23. A developer wants to retrieve the list of Availability Zones available in the Region where the stack is being deployed. Which intrinsic function returns this list?
A) `!GetAZs ""` (or `!GetAZs !Ref "AWS::Region"`)
B) `!ListAZs`
C) `!GetAtt AWS::Region.AZs`
D) `!FindInMap [AZMap]`

24. In CloudFormation, what does the `!Base64` intrinsic function do when applied to a string in the `UserData` property of an `AWS::EC2::Instance`?
A) Encrypts the string using AWS KMS
B) Converts a plain text string into a Base64-encoded representation required by the EC2 UserData API
C) Compresses the string into a ZIP file
D) Hashes the string using SHA-256

25. A developer is authoring a CloudFormation template and wants to include comments and documentation that explain complex logic. Which template format supports native comments using the `#` character?
A) JSON format only
B) YAML format only
C) Both JSON and YAML formats
D) Neither format supports comments

26. When using `!Sub` with a mapping of variable names, which syntax correctly substitutes custom variables?
A) `!Sub ["https://${DomainName}/api", { DomainName: !Ref MyDomainParam }]`
B) `!Sub "https://${MyDomainParam}/api"`
C) `!Sub [!Ref MyDomainParam, "/api"]`
D) `!Join ["https://", !Ref MyDomainParam]`

27. A developer defines a condition `CreateDevResources: !Equals [!Ref EnvironmentName, "dev"]`. How can the developer define a second condition `CreateProdResources` that is the exact logical opposite?
A) `CreateProdResources: !Not [!Condition CreateDevResources]`
B) `CreateProdResources: !Inverse [CreateDevResources]`
C) `CreateProdResources: !Opposite [CreateDevResources]`
D) `CreateProdResources: !If [CreateDevResources, false, true]`

28. Which intrinsic function selects a single object from a list by its zero-based index (e.g., picking the first subnet from a list of subnets)?
A) `!Select [0, !Ref SubnetList]`
B) `!Index [0, !Ref SubnetList]`
C) `!First [!Ref SubnetList]`
D) `!GetItem [0, !Ref SubnetList]`

29. A developer writes a template that includes the `Transform: AWS::Serverless-2016-10-31` macro at the top level. What does this macro tell CloudFormation to do?
A) Execute the AWS Serverless Application Model (SAM) transform to process and expand serverless shorthand resources into standard CloudFormation syntax before deploying
B) Deploy the template to AWS Lambda directly without using CloudFormation
C) Convert the template to Docker Compose syntax
D) Encrypt the template in an S3 bucket

30. A developer wants to add metadata to an EC2 instance in CloudFormation that instructs the `cfn-init` helper script to install packages, create files, and start services. Under which section of the resource is this configured?
A) `Metadata: AWS::CloudFormation::Init`
B) `Properties: UserData: Init`
C) `Parameters: InitConfig`
D) `Outputs: cfn-init`

---

### Cross-Stack References, Nested Stacks, Change Sets & Operations (31–55)

31. A company separates its infrastructure into two CloudFormation stacks: a `NetworkStack` (creates VPC, subnets, route tables) and an `AppStack` (creates EC2 instances and load balancers). The `AppStack` uses `!ImportValue` to reference the VPC ID exported by `NetworkStack`. An engineer attempts to update `NetworkStack` to delete the exported VPC ID output. What happens when the update is executed?
A) `NetworkStack` deletes the output, causing `AppStack` instances to lose network connectivity
B) CloudFormation rejects the update and fails because an exported output cannot be modified or deleted while another stack is actively importing it
C) CloudFormation automatically deletes `AppStack`
D) CloudFormation converts `NetworkStack` into a nested stack

32. What is the recommended operational workflow to safely remove a cross-stack reference between an exporting stack (`StackA`) and an importing stack (`StackB`)?
A) Delete `StackA` first, then delete `StackB`
B) Modify `StackB` to remove the `!ImportValue` call, update `StackB`, and once `StackB` no longer references the export, update `StackA` to remove the `Export` output
C) Run `aws cloudformation force-delete-export`
D) Disable CloudFormation rollback on `StackA`

33. An enterprise has modularized its infrastructure into reusable templates (e.g., a standard VPC template, an ALB template, an ECS cluster template). A master template composes these components together and deploys them as a single cohesive unit using `AWS::CloudFormation::Stack` resources. What architecture pattern is being used?
A) Stack Sets
B) Nested Stacks
C) Cross-Region Replication
D) Dynamic Parameter Mappings

34. Where must the child templates of a Nested Stack be stored so that the parent CloudFormation stack can reference them in its `TemplateURL` property?
A) On a local laptop hard drive
B) In an Amazon S3 bucket accessible by CloudFormation (via HTTPS URL or S3 ARN)
C) In an Amazon DynamoDB table
D) In a Git commit message

35. What is the primary difference between Nested Stacks and Cross-Stack references via `Export`/`ImportValue`?
A) Nested stacks are composed and deployed together as parent-child units sharing the parent lifecycle; cross-stack references connect independently-authored, separately-deployed stacks
B) Nested stacks can only run in `us-east-1`; cross-stack references run in all regions
C) Cross-stack references require AWS SAM; nested stacks require AWS CDK
D) Nested stacks cannot provision EC2 instances

36. An engineer wants to preview the exact changes CloudFormation will make to running infrastructure (e.g., which resources will be added, modified, or replaced) before applying a template update to a production stack. Which CloudFormation feature provides this preview without altering running resources?
A) Stack Drift Detection
B) Change Sets (via `CreateChangeSet`)
C) Stack Events
D) CloudWatch Logs Insights

37. While reviewing a CloudFormation Change Set for a database update, the developer notices that the `AWS::RDS::DBInstance` resource has `Replacement: True`. What does this indicate?
A) CloudFormation will modify the existing database instance in-place with zero downtime
B) CloudFormation will delete the existing database instance and create a brand-new instance, resulting in data loss if no snapshot or retention policy exists
C) CloudFormation will rename the database parameter group
D) The database engine will be updated to a beta version

38. A developer needs to deploy a baseline security configuration (IAM roles, CloudTrail alarms, AWS Config rules) consistently across 50 AWS accounts and multiple AWS Regions within an AWS Organization. Which CloudFormation feature is designed for multi-account, multi-region deployments from a single administrator account?
A) CloudFormation Nested Stacks
B) CloudFormation StackSets
C) CloudFormation Change Sets
D) CloudFormation Macro transforms

39. A junior administrator manually modified a security group rule in the AWS Management Console to allow SSH from `0.0.0.0/0`, bypassing the CloudFormation template that manages the stack. The lead engineer wants to verify whether the live infrastructure matches the template definition. Which CloudFormation feature should the engineer run?
A) Change Set Execution
B) Stack Drift Detection
C) Stack Rollback
D) Template Validation (`aws cloudformation validate-template`)

40. What is the outcome of running CloudFormation Drift Detection on a stack where resources have been manually altered?
A) CloudFormation automatically reverts the manual changes to match the template
B) CloudFormation reports a status of `DRIFTED` and provides a detailed property-by-property difference between the expected template state and the actual live resource state without modifying the live resources
C) CloudFormation terminates the drifted EC2 instances
D) CloudFormation updates the template file on the developer's laptop

41. During a stack creation, CloudFormation successfully creates 5 resources, but the 6th resource fails due to an invalid subnet configuration. By default, what action does CloudFormation take?
A) It leaves the 5 created resources running and stops
B) It triggers a rollback (`ROLLBACK_IN_PROGRESS`), deleting all 5 previously created resources, and ends in `ROLLBACK_COMPLETE` status
C) It retries the 6th resource indefinitely
D) It converts the stack into a nested stack

42. A developer is testing a complex CloudFormation template and wants to debug a resource failure without CloudFormation immediately deleting all successfully created resources on failure. Which CLI flag should be passed during `aws cloudformation create-stack`?
A) `--disable-rollback` (or `--on-failure DO_NOTHING`)
B) `--force-create`
C) `--skip-errors`
D) `--debug-mode`

43. What is the behavior of CloudFormation when an `update-stack` operation fails midway through updating an existing, healthy production stack?
A) The stack is permanently deleted
B) CloudFormation automatically rolls back the changes, restoring all modified resources to their last known good, working configuration (`UPDATE_ROLLBACK_COMPLETE`)
C) The stack is left in an unrecoverable state
D) CloudFormation halts all network traffic in the VPC

44. A developer attempts to update a stack that is currently in `UPDATE_ROLLBACK_FAILED` status. What action must be taken before the stack can be updated again?
A) Use the `ContinueUpdateRollback` API action (optionally skipping specific unrecoverable resources) to return the stack to a stable state
B) Terminate the AWS account
C) Manually delete the S3 bucket where CloudFormation stores templates
D) Run `aws cloudformation validate-template`

45. How can a developer validate the syntax and structure of a CloudFormation template JSON/YAML file locally before attempting to create a stack in AWS?
A) Run `aws cloudformation validate-template --template-body file://template.yaml` (or use linters like `cfn-lint`)
B) Run `aws ec2 describe-instances`
C) Upload the file to S3 Glacier
D) Execute `cdk bootstrap`

46. What is a CloudFormation Macro?
A) A keyboard shortcut in the AWS Console
B) A custom transform powered by an AWS Lambda function that processes, modifies, or generates template syntax dynamically before CloudFormation processes the template
C) A bash script embedded in UserData
D) An Amazon CloudFront edge function

47. A developer wants to prevent accidental deletion of a production CloudFormation stack via the AWS Console or CLI. Which stack protection feature should be enabled?
A) Stack Termination Protection
B) MFA Delete on the S3 bucket only
C) IAM Deny All policy on root account
D) CloudFormation Drift Lock

48. When Stack Termination Protection is enabled on a CloudFormation stack, what happens if an administrator attempts to delete the stack using `aws cloudformation delete-stack`?
A) The stack is deleted immediately without warning
B) CloudFormation rejects the delete request and returns an error indicating that termination protection is enabled
C) CloudFormation deletes the resources but retains the stack metadata
D) CloudFormation reboots all instances in the stack

49. What is the maximum size of a CloudFormation template passed directly as a string in the `--template-body` parameter, versus uploading the template to an Amazon S3 bucket and passing `--template-url`?
A) 51,200 bytes (51.2 KB) for direct template body; up to 1 MB (1,024,000 bytes) when passed via S3 `TemplateURL`
B) 10 MB for direct template body; 100 MB for S3
C) 1 KB for direct template body; unlimited for S3
D) There is no size limit on template bodies

50. In CloudFormation, what does a Stack Policy do?
A) It defines IAM permissions for users creating stacks
B) It acts as a preventive guardrail that explicitly prevents stack updates from modifying or deleting protected resources (e.g., `Effect: Deny, Action: Update:*, Resource: LogicalResourceId/ProdDatabase`) during stack updates
C) It configures Route 53 DNS routing policies
D) It manages Auto Scaling group capacity

51. A developer wants to pass a specific IAM role to CloudFormation so that CloudFormation assumes this role for all resource provisioning operations, rather than using the credentials of the logged-in user. What is this role called?
A) CloudFormation Service Role
B) EC2 Instance Profile
C) IAM Root Credentials
D) Cognito Identity Pool Role

52. What is the primary benefit of assigning a dedicated Service Role to a CloudFormation stack?
A) It allows developers to deploy stacks without needing broad direct IAM permissions to create EC2, RDS, or IAM resources, adhering to the principle of least privilege
B) It reduces AWS CloudFormation billing costs by 50%
C) It speeds up EC2 boot times
D) It eliminates the need for template parameters

53. An operations team wants to monitor CloudFormation deployment progress and receive real-time notifications on mobile/email whenever a stack event occurs (e.g., `CREATE_IN_PROGRESS`, `CREATE_COMPLETE`). What CloudFormation parameter configures this?
A) `NotificationARNs` pointing to an Amazon SNS topic
B) `EventBridgeRuleArn`
C) `SQSQueueUrl`
D) `CloudWatchLogGroup`

54. How does CloudFormation determine the order in which resources are created when building a stack?
A) It creates resources in random order
B) It analyzes implicit dependencies (via `!Ref` and `!GetAtt`) and explicit dependencies (via the `DependsOn` attribute) to construct a dependency graph and create resources in parallel where possible
C) It creates resources strictly from top to bottom based on line numbers in the YAML file
D) It creates all resources strictly one at a time sequentially

55. When would a developer explicitly add the `DependsOn` attribute to a resource in a CloudFormation template?
A) When a resource relies on another resource being fully created and active first, but does NOT reference it via `!Ref` or `!GetAtt` (e.g., an EC2 instance requiring an Internet Gateway attachment to be active before running UserData scripts that download packages)
B) When a resource is an S3 bucket
C) When creating IAM roles
D) When deleting a stack

---

### Protecting Stateful Resources & Custom Resources (56–75)

56. A developer is writing a CloudFormation template for a production Amazon RDS MySQL database. If the stack is accidentally deleted, the database must NOT be deleted; instead, it should remain running as a standalone resource in AWS. Which attribute must be added to the RDS resource definition?
A) `DeletionPolicy: Retain`
B) `DeletionPolicy: Snapshot`
C) `DeletionPolicy: Delete`
D) `TerminationProtection: true`

57. A company’s security policy mandates that whenever an Amazon RDS DB instance or Amazon EBS volume managed by CloudFormation is deleted upon stack deletion, a final backup snapshot must be created automatically before the resource is removed. Which attribute meets this requirement?
A) `DeletionPolicy: Snapshot`
B) `DeletionPolicy: Retain`
C) `BackupPolicy: Mandatory`
D) `SnapshotPolicy: Enable`

58. What is the default `DeletionPolicy` behavior for an `AWS::S3::Bucket` or `AWS::RDS::DBInstance` if no `DeletionPolicy` attribute is explicitly defined in the CloudFormation template?
A) `Retain`
B) `Delete`
C) `Snapshot`
D) `Archive`

59. What happens if a CloudFormation stack with an `AWS::S3::Bucket` (configured with `DeletionPolicy: Delete`) is deleted, but the S3 bucket currently contains objects?
A) CloudFormation automatically deletes all objects and then deletes the bucket
B) The stack deletion fails with a `BucketNotEmpty` error on the S3 resource because S3 requires buckets to be completely empty before deletion
C) The objects are archived to S3 Glacier
D) The bucket is renamed

60. An engineer updates a CloudFormation template to change an RDS DB instance property that requires resource replacement (such as changing the underlying DB engine). The engineer wants to ensure that the old database instance is backed up as a final snapshot before being replaced and destroyed. Which attribute must be configured on the resource?
A) `UpdateReplacePolicy: Snapshot`
B) `DeletionPolicy: Retain`
C) `AutoRollback: true`
D) `UpdatePolicy: Rolling`

61. What are the three valid values for the `UpdateReplacePolicy` attribute in AWS CloudFormation?
A) `Delete`, `Retain`, `Snapshot`
B) `Ignore`, `Replace`, `Abort`
C) `True`, `False`, `Maybe`
D) `Backup`, `Restore`, `Archive`

62. A developer needs to execute a custom task during a CloudFormation deployment that is not supported natively by any CloudFormation resource type (e.g., looking up a third-party SSL certificate, generating an RSA key pair, or populating an initial dataset into an external database). Which CloudFormation mechanism solves this?
A) AWS CloudFormation Custom Resources (backed by an AWS Lambda function or Amazon SNS topic)
B) CloudFormation Drift Detection
C) EC2 Launch Templates
D) CloudFormation Nested Stacks

63. In a CloudFormation Custom Resource definition, what property specifies the ARN of the Lambda function that handles the resource lifecycle events?
A) `ServiceToken`
B) `FunctionArn`
C) `HandlerToken`
D) `ExecutionRole`

64. What event types does CloudFormation send to the Lambda function backing a Custom Resource during stack operations?
A) `Create`, `Update`, and `Delete`
B) `Start`, `Stop`, and `Restart`
C) `GET`, `POST`, and `DELETE`
D) `Init`, `Build`, and `Deploy`

65. How does a Lambda function backing a CloudFormation Custom Resource notify CloudFormation of success or failure and return output attributes?
A) By sending an HTTP PUT request containing a JSON payload (status `SUCCESS` or `FAILED`, `PhysicalResourceId`, `Data`) to the pre-signed S3 URL provided in the `ResponseURL` field of the event object (commonly using the `cfnresponse` library)
B) By printing to `stdout` in CloudWatch Logs
C) By throwing a Python runtime exception
D) By sending an email via Amazon SES

66. What happens if a Lambda function backing a CloudFormation Custom Resource fails to send a response to the `ResponseURL` (e.g., due to a function timeout or unhandled exception)?
A) CloudFormation assumes success after 10 seconds
B) CloudFormation hangs in `CREATE_IN_PROGRESS` (or `UPDATE_IN_PROGRESS`) until the stack operation timeout elapses (default 1 hour), after which the stack fails and rolls back
C) CloudFormation automatically restarts the Lambda function 50 times
D) The AWS account is suspended

67. A developer is writing a Custom Resource in Python. What built-in utility module provided by AWS can be imported to easily send success/failure responses back to CloudFormation?
A) `cfnresponse`
B) `aws_cdk`
C) `boto3_cfn`
D) `cloudformation_helper`

68. How can other resources in a CloudFormation template retrieve data values returned by a Custom Resource in its response `Data` dictionary?
A) `!GetAtt MyCustomResource.DataAttributeName`
B) `!Ref MyCustomResource`
C) `!ImportValue MyCustomResource`
D) `!FindInMap [MyCustomResource]`

69. What is the importance of properly handling the `Delete` event in a Custom Resource Lambda function?
A) It ensures that external resources created by the custom resource (e.g., external DNS records or database users) are cleanly cleaned up, and that a `SUCCESS` response is always sent so stack deletion can complete cleanly
B) It triggers an automatic backup of the Lambda function code
C) It deletes the CloudFormation template
D) It reboots the AWS Region

70. When a stack update modifies properties on a Custom Resource, what does CloudFormation do?
A) It invokes the backing Lambda function with `RequestType: Update`, passing the `OldResourceProperties` and `ResourceProperties`
B) It skips the custom resource
C) It deletes the stack
D) It converts the custom resource to an S3 bucket

71. A developer wants to manage an Amazon OpenSearch index creation via CloudFormation. Since CloudFormation does not have an `AWS::OpenSearch::Index` resource type, what is the best practice solution?
A) Write a Custom Resource backed by a Python Lambda function that uses the OpenSearch SDK to create, update, and delete the index
B) Ask developers to create the index manually after deployment
C) Store the index in Amazon S3
D) Use AWS Step Functions outside of CloudFormation

72. An `AWS::AutoScaling::AutoScalingGroup` in a CloudFormation template needs to perform rolling updates when the launch template changes. Which CloudFormation attribute controls how the Auto Scaling group handles updates?
A) `UpdatePolicy` (specifically `AutoScalingRollingUpdate` or `AutoScalingReplacingUpdate`)
B) `DeletionPolicy`
C) `UpdateReplacePolicy`
D) `Metadata`

73. A developer configures `CreationPolicy` on an `AWS::EC2::Instance` in CloudFormation. What is the purpose of this attribute?
A) It tells CloudFormation to pause stack creation and wait for a success signal from the instance (sent via `cfn-signal`) within a configured timeout before marking the instance as `CREATE_COMPLETE`
B) It sets the instance creation date
C) It determines which AZ the instance is created in
D) It automatically formats the EBS volume

74. If an EC2 instance configured with a `CreationPolicy` fails to send a `cfn-signal` within the specified `Timeout` duration (e.g., `PT15M`), what occurs?
A) CloudFormation marks the resource as failed (`Failed to receive 1 resource signal(s) within the specified duration`) and initiates a stack rollback
B) CloudFormation assumes the instance is healthy
C) CloudFormation sends an SMS alert
D) CloudFormation switches the instance to an ARM processor

75. What command does a developer include in an EC2 instance's `UserData` script to signal CloudFormation that application setup is complete and successful?
A) `cfn-signal -e $? --stack ${AWS::StackName} --resource MyInstance --region ${AWS::Region}`
B) `aws cloudformation complete-instance`
C) `systemctl status ec2`
D) `echo "SUCCESS"`

---

### AWS Serverless Application Model (SAM) (76–105)

76. A developer is building a serverless REST API consisting of multiple AWS Lambda functions, Amazon API Gateway endpoints, and Amazon DynamoDB tables. What AWS IaC framework provides serverless shorthand syntax, automatic IAM policy generation, and local testing tools?
A) AWS Cloud Development Kit (CDK) only
B) AWS Serverless Application Model (AWS SAM)
C) AWS OpsWorks
D) AWS Elastic Beanstalk

77. What header line is required in a YAML file to identify it as an AWS SAM template?
A) `Transform: AWS::Serverless-2016-10-31`
B) `Framework: Serverless-v1`
C) `SAMVersion: 2.0`
D) `Engine: SAM-Transform`

78. Which SAM resource type simplifies declaring a Lambda function along with its execution role, environment variables, and event source triggers (such as API Gateway, SQS, or S3)?
A) `AWS::Lambda::Function`
B) `AWS::Serverless::Function`
C) `AWS::Serverless::Lambda`
D) `AWS::Compute::Serverless`

79. A developer wants to define common configuration settings (such as `Runtime: nodejs20.x`, `Timeout: 30`, and `MemorySize: 512`) once so they apply automatically to all `AWS::Serverless::Function` resources in a SAM template. Which top-level section of the SAM template should be used?
A) `Parameters`
B) `Globals`
C) `Mappings`
D) `Metadata`

80. How does a developer attach an API Gateway HTTP trigger to an `AWS::Serverless::Function` in a SAM template?
A) Add an entry under the function's `Events:` property with `Type: Api` (or `Type: HttpApi`), specifying the `Path` and `Method`
B) Write an explicit `AWS::Lambda::Permission` and `AWS::ApiGateway::Method` resource by hand
C) Write a bash script in `samconfig.toml`
D) Configure Route 53 DNS records

81. A SAM template defines an `AWS::Serverless::Function` that needs read and write permissions to an Amazon DynamoDB table. Instead of authoring a 30-line IAM policy statement in JSON, what SAM feature provides pre-canned, scoped policy templates?
A) SAM Policy Templates (e.g., `DynamoDBCrudPolicy: { TableName: !Ref MyTable }` or `DynamoDBReadPolicy`)
B) IAM Root Access
C) AWS Managed Policy `AdministratorAccess`
D) DynamoDB Local Secondary Indexes

82. Which SAM policy template grants a Lambda function permissions to decrypt data using an AWS KMS key?
A) `KMSDecryptPolicy: { KeyId: !Ref MyKey }`
B) `KMSEncryptAllPolicy`
C) `S3ReadPolicy`
D) `SecretsManagerWritePolicy`

83. A developer wants to test an `AWS::Serverless::Function` locally on their laptop by passing a mock JSON event payload, without deploying the function to AWS. Which SAM CLI command executes this local invocation?
A) `sam local invoke <FunctionName> --event <event.json>`
B) `sam test <FunctionName>`
C) `sam run <FunctionName>`
D) `aws lambda invoke-local`

84. How does the SAM CLI simulate the Lambda execution environment locally when running `sam local invoke` or `sam local start-api`?
A) It runs the function inside a local Docker container that mirrors the official AWS Lambda runtime environment
B) It connects to an active EC2 instance in `us-east-1`
C) It compiles the code to WebAssembly
D) It uploads the code to S3 and runs it on AWS

85. A developer wants to run a local HTTP server that emulates Amazon API Gateway and routes local HTTP requests to corresponding local Lambda functions on `localhost:3000`. Which SAM CLI command starts this local API emulator?
A) `sam local start-api`
B) `sam local start-lambda`
C) `sam serve`
D) `sam http-server`

86. Which SAM CLI command compiles application dependencies (e.g., executing `npm install` for Node.js or `pip install` for Python) and packages the artifacts into a `.aws-sam/build` directory?
A) `sam init`
B) `sam build`
C) `sam package`
D) `sam validate`

87. A developer wants to package local Lambda source code artifacts, upload them to an Amazon S3 deployment bucket, and generate an updated CloudFormation template referencing the S3 object locations. Which SAM CLI command performs these actions?
A) `sam package --s3-bucket <bucket-name> --output-template-file packaged.yaml`
B) `sam upload`
C) `sam s3 sync`
D) `sam bundle`

88. What configuration file does `sam deploy --guided` interactively generate to save deployment settings (such as stack name, region, S3 bucket, parameter overrides, and confirmation preferences) for future non-interactive deployments?
A) `samconfig.toml`
B) `sam.json`
C) `config.yaml`
D) `buildspec.yml`

89. A development team wants to use a single SAM `template.yaml` file to deploy to three distinct environments: `dev`, `staging`, and `prod`. How does `samconfig.toml` support multi-environment deployments?
A) By defining separate configuration environment sections (e.g., `[dev.deploy.parameters]`, `[staging.deploy.parameters]`, `[prod.deploy.parameters]`), invoked using `sam deploy --config-env <env-name>`
B) By creating three copies of the SAM CLI binary
C) By requiring three separate AWS accounts for each developer
D) By creating three separate Git repositories

90. How can a developer override specific template parameters on the command line during a `sam deploy` command?
A) `--parameter-overrides "StageName=prod DatabaseCapacity=10"`
B) `--set-param StageName=prod`
C) `--params "StageName: prod"`
D) `--env-vars StageName=prod`

91. What SAM resource type represents a serverless DynamoDB table with a single primary key?
A) `AWS::Serverless::SimpleTable`
B) `AWS::Serverless::DynamoDB`
C) `AWS::NoSQL::Table`
D) `AWS::DynamoDB::Simple`

92. When should a developer use standard CloudFormation `AWS::DynamoDB::Table` instead of `AWS::Serverless::SimpleTable` in a SAM template?
A) Whenever the table requires advanced features such as Global Secondary Indexes (GSIs), Local Secondary Indexes (LSIs), DynamoDB Streams, or Point-in-Time Recovery
B) `AWS::Serverless::SimpleTable` is deprecated and should never be used
C) Only when using Java runtimes
D) `AWS::DynamoDB::Table` cannot be used in a SAM template

93. A developer wants to configure automated traffic shifting (e.g., Canary or Linear deployments) for an `AWS::Serverless::Function` using AWS CodeDeploy when updating function versions. What property under `AWS::Serverless::Function` enables this?
A) `DeploymentPreference: { Type: Canary10Percent10Minutes }`
B) `AutoScaling: { Policy: Linear }`
C) `TrafficShift: true`
D) `CodeDeploy: { Mode: BlueGreen }`

94. What pre-traffic and post-traffic verification mechanism can be configured in a SAM `DeploymentPreference` to validate that a new Lambda version is working before and after traffic shifting?
A) `Hooks: { PreTraffic: !Ref PreTrafficLambdaFunction, PostTraffic: !Ref PostTrafficLambdaFunction }`
B) `HealthCheckPath: /health`
C) `Alarms: CloudWatch5xx`
D) `UnitTests: npm_test`

95. Which SAM resource type defines a serverless state machine managed by AWS Step Functions?
A) `AWS::Serverless::StateMachine`
B) `AWS::Serverless::StepFunction`
C) `AWS::StepFunctions::ServerlessWorkflow`
D) `AWS::Serverless::Workflow`

96. A developer wants to sync local code changes directly to an active development stack in AWS in near real-time without running a full CloudFormation deployment pipeline on every keystroke. Which SAM CLI command provides this accelerated development synchronization?
A) `sam sync --watch --stack-name <stack-name>`
B) `sam deploy --fast`
C) `sam live-reload`
D) `sam push`

97. What SAM resource type defines a serverless GraphQL API managed by AWS AppSync?
A) `AWS::Serverless::GraphQLApi`
B) `AWS::AppSync::ServerlessApi`
C) `AWS::Serverless::AppSync`
D) `AWS::GraphQL::Api`

98. How can a developer declare environment variables that are available to all Lambda functions in a SAM template?
A) In `Globals: Function: Environment: Variables:`
B) In `Parameters: EnvVars:`
C) In `Mappings: EnvironmentVariables:`
D) In `Outputs: Env:`

99. Which SAM CLI command initializes a new serverless project from a curated starter template for a specified runtime (e.g., Python, Node.js, Java, Go)?
A) `sam init`
B) `sam new`
C) `sam create`
D) `sam bootstrap`

100. When `sam deploy` executes, what underlying AWS service does it interact with to provision and update the cloud resources?
A) AWS CloudFormation (by creating and executing Change Sets)
B) AWS OpsWorks
C) Amazon EC2 API directly
D) AWS Systems Manager Run Command

101. A developer wants to validate that a SAM template is valid against the AWS SAM specification. Which command performs this validation?
A) `sam validate`
B) `sam check`
C) `sam lint`
D) `sam test-template`

102. Can standard CloudFormation resources (e.g., `AWS::S3::Bucket`, `AWS::SQS::Queue`, `AWS::RDS::DBInstance`) be included inside the same `template.yaml` file as `AWS::Serverless::*` resources?
A) Yes, SAM is a superset/transform of CloudFormation, allowing full mixing of standard CloudFormation resources and SAM shorthand resources in the same template
B) No, SAM templates can only contain `AWS::Serverless::*` resources
C) Only if the template is written in JSON
D) Only if the resources are in `us-east-1`

103. A developer wants to configure an SQS queue trigger on an `AWS::Serverless::Function`. What event type should be used under `Events:`?
A) `Type: SQS` with `Properties: { Queue: !GetAtt MyQueue.Arn, BatchSize: 10 }`
B) `Type: MessageQueue`
C) `Type: SQSStream`
D) `Type: EventBridge`

104. In SAM, what does the `AutoPublishAlias` property on an `AWS::Serverless::Function` do?
A) It automatically publishes a new Lambda function version and updates a named alias (e.g., `live` or `prod`) to point to the new version on every code update
B) It publishes the code to GitHub
C) It creates a public Route 53 DNS record
D) It sends an SNS notification

105. A developer wants to trace incoming requests across API Gateway and Lambda functions declared in a SAM template. What property enables AWS X-Ray tracing globally across all functions and APIs?
A) `Globals: Function: Tracing: Active` and `Globals: Api: TracingEnabled: true`
B) `Globals: XRay: Enable`
C) `Parameters: Trace: true`
D) `Outputs: XRayArn`

---

### AWS CDK (Cloud Development Kit) & Comparative IaC Selection (106–125)

106. A software engineering team wants to define AWS infrastructure using familiar, general-purpose programming languages (such as TypeScript, Python, Java, C#, or Go) rather than writing declarative YAML or JSON files. Which AWS framework allows defining infrastructure as code using object-oriented abstractions?
A) AWS Cloud Development Kit (AWS CDK)
B) AWS SAM
C) AWS Elastic Beanstalk
D) AWS CloudFormation Templates (YAML)

107. When a developer executes `cdk synth` in an AWS CDK project, what artifact is produced?
A) An AWS CloudFormation template (JSON/YAML) generated from the construct tree
B) A compiled binary executable for Linux
C) An Amazon Machine Image (AMI)
D) A Docker container image in Amazon ECR

108. In AWS CDK, what are the three levels of Constructs and what do they represent?
A) L1 (Cfn primitives, 1:1 with raw CloudFormation resources); L2 (AWS curated constructs with sane defaults, helper methods, and security policies); L3 (Higher-level opinionated architectural patterns combining multiple services)
B) L1 (Frontend), L2 (Backend), L3 (Database)
C) L1 (Development), L2 (Staging), L3 (Production)
D) L1 (Small), L2 (Medium), L3 (Large)

109. A developer writes the following TypeScript code in an AWS CDK stack:
```typescript
const table = new dynamodb.Table(this, 'UsersTable', {
  partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING }
});
const fn = new lambda.Function(this, 'UserHandler', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda')
});
table.grantReadWriteData(fn);
```
What does the `table.grantReadWriteData(fn)` method call do?
A) It automatically creates and attaches a least-privilege IAM policy to the Lambda function's execution role, granting it permissions to perform read and write actions on the `UsersTable` DynamoDB table
B) It connects the database via a physical fiber optic cable
C) It makes the DynamoDB table public
D) It reboots the Lambda function

110. Which AWS CDK construct level does `aws_lambda.Function` belong to, as opposed to `aws_lambda.CfnFunction`?
A) L2 construct (curated with defaults and helper methods)
B) L1 construct (low-level CloudFormation primitive)
C) L3 construct (architectural pattern)
D) L0 construct

111. What is an example of an L3 construct (pattern) in the AWS CDK?
A) `ApplicationLoadBalancedFargateService` from `@aws-cdk/aws-ecs-patterns` (provisions an ALB, ECS Fargate cluster, task definition, service, and security groups in a single class)
B) `CfnBucket`
C) `s3.Bucket`
D) `iam.Role`

112. What one-time command must be executed in an AWS account and Region before deploying CDK applications that contain assets (such as Lambda code bundles or Docker container images)?
A) `cdk bootstrap` (provisions an S3 bucket, ECR repository, and IAM roles for the CDK toolkit)
B) `cdk init`
C) `cdk install`
D) `cdk setup-account`

113. Which AWS CDK CLI command compares the synthesized CloudFormation template of the local code against the currently deployed stack in AWS, displaying a visual diff of additions, modifications, and deletions?
A) `cdk diff`
B) `cdk compare`
C) `cdk status`
D) `cdk test`

114. Which CDK CLI command compiles the application, synthesizes the CloudFormation template, and creates or updates the stack in AWS?
A) `cdk deploy`
B) `cdk push`
C) `cdk release`
D) `cdk apply`

115. How does a developer define multiple deployment environments (e.g., `dev` in `us-east-1` and `prod` in `us-west-2`) in an AWS CDK application?
A) By instantiating the Stack class multiple times with different `env: { account: '...', region: '...' }` properties in the CDK App entry point
B) By creating two separate CDK installations on their machine
C) By modifying the Linux `/etc/hosts` file
D) By deleting the `cdk.json` file

116. What is the root construct of an AWS CDK application that serves as the container for one or more Stacks?
A) `App` (`cdk.App`)
B) `Stage`
C) `RootConstruct`
D) `Cluster`

117. What is a key advantage of writing Infrastructure as Code in AWS CDK compared to raw CloudFormation YAML?
A) CDK allows using standard programming language constructs (like `for` loops, `if` statements, functions, classes, and inheritance) to dynamically generate repetitive infrastructure without copy-pasting YAML blocks
B) CDK bypasses CloudFormation entirely, reducing deployment times to zero seconds
C) CDK does not require an AWS account
D) CDK generates infrastructure for Google Cloud and Microsoft Azure automatically

118. How does AWS CDK support unit testing infrastructure code?
A) Through assertions and snapshot testing libraries (`aws-cdk-lib/assertions` or `jest`), allowing developers to assert that synthesized CloudFormation templates contain specific resource types and properties
B) By launching live EC2 instances on every test run
C) By sending requests to the production database
D) Unit testing is not supported in CDK

119. What file in an AWS CDK project defines how to execute the CDK application (e.g., specifying `"app": "npx ts-node bin/my-app.ts"`)?
A) `cdk.json`
B) `template.yaml`
C) `samconfig.toml`
D) `Dockerrun.aws.json`

120. A developer needs to reference an existing Amazon VPC created outside of the CDK application (e.g., in a separate networking stack) to launch ECS tasks inside it. Which CDK method imports an existing VPC by its ID?
A) `ec2.Vpc.fromLookup(this, 'ExistingVpc', { vpcId: 'vpc-0123456789' })`
B) `new ec2.Vpc(this, 'ExistingVpc')`
C) `ec2.Vpc.createFromScratch()`
D) `cdk.import('vpc-0123456789')`

121. An organization wants to create a company-wide library of standardized, compliant infrastructure constructs (e.g., an S3 bucket that always enforces SSE-KMS encryption and public access block) and publish it as an NPM/PyPI package for internal teams. Which AWS tool is designed for authoring and distributing multi-language CDK construct libraries?
A) JSII (used by AWS CDK to compile TypeScript constructs into Python, Java, C#, and Go packages)
B) AWS SAM CLI
C) AWS CloudFormation Designer
D) AWS OpsWorks

122. A development team is building a serverless web application consisting of 4 Lambda functions, an API Gateway REST API, and a DynamoDB table. The team wants rapid local development with the ability to emulate API Gateway on their local machines and test Lambda functions locally using Docker. Which IaC tool is the BEST fit?
A) AWS SAM (Serverless Application Model)
B) Raw CloudFormation JSON
C) AWS OpsWorks Stacks
D) HashiCorp Nomad

123. A platform engineering team needs to provision 50 identical microservice environments containing S3 buckets, SQS queues, and IAM roles. The team requires type-safe reusable classes, object-oriented inheritance, and unit test coverage in TypeScript. Which IaC tool is the BEST fit?
A) AWS Cloud Development Kit (AWS CDK)
B) AWS SAM
C) AWS Elastic Beanstalk
D) AWS Amplify Studio only

124. An enterprise operations team is deploying baseline compliance guardrails (IAM password policies, CloudTrail logging) across 100 AWS accounts in an AWS Organization. Which tool natively orchestrates multi-account, multi-region CloudFormation deployments?
A) CloudFormation StackSets
B) AWS SAM Local
C) AWS CDK `cdk synth`
D) AWS Amplify CLI

125. An architect is evaluating IaC tooling for three different project requirements:
1. Requirement 1: Serverless Lambda and API Gateway application requiring local invocation testing before deployment.
2. Requirement 2: Complex enterprise microservices requiring object-oriented abstractions, loops, and TypeScript compile-time type checking.
3. Requirement 3: Multi-account compliance guardrails deployed across an entire AWS Organization.
Which mapping of requirements to AWS tools is correct?
A) Requirement 1: AWS SAM; Requirement 2: AWS CDK; Requirement 3: CloudFormation StackSets
B) Requirement 1: AWS CDK; Requirement 2: AWS SAM; Requirement 3: AWS Amplify
C) Requirement 1: CloudFormation StackSets; Requirement 2: AWS SAM; Requirement 3: AWS CDK
D) Requirement 1: AWS Amplify; Requirement 2: CloudFormation; Requirement 3: AWS SAM

---

## Answer Key & Explanations

1. B — The `Parameters` section enables custom runtime input values to be passed to a CloudFormation template during stack creation or updates.
2. B — The `Mappings` section provides static key-value lookup tables (such as mapping Regions to AMI IDs) defined at template authoring time.
3. B — `!FindInMap [MapName, TopLevelKey, SecondLevelKey]` retrieves values from a named table in the `Mappings` section.
4. A — Conditions are declared under `Conditions:` using intrinsic condition functions and attached to resources via the `Condition:` property.
5. A — `!Sub` performs clean variable substitution/string interpolation using `${VariableName}` syntax.
6. A — `!Ref` returns the primary resource identifier (e.g., instance ID), while `!GetAtt` retrieves specific named attributes (e.g., `PublicIp`).
7. A — `!GetAtt AppSecurityGroup.GroupId` returns the physical ID of the security group (`sg-xxxx`).
8. A — `!If [ConditionName, ValueIfTrue, ValueIfFalse]` returns one of two values depending on the evaluation of the named condition.
9. B — The `Resources` section is the only required section in a CloudFormation template; all other sections are optional.
10. B — `!Join [delimiter, [list]]` concatenates an array of values into a single string separated by the specified delimiter.
11. A — `!Split [delimiter, source_string]` splits a string into an array of string values based on the specified delimiter.
12. A — `AWS::AccountId` is a CloudFormation pseudo parameter that returns the 12-digit AWS account ID where the stack is deployed.
13. A — `AWS::StackName` resolves to the name assigned to the CloudFormation stack.
14. A — Returning `AWS::NoValue` inside an `!If` expression instructs CloudFormation to omit the optional property from the resource.
15. A — `AllowedValues` defines a fixed list of permitted string or numeric values for a CloudFormation parameter.
16. A — Setting `NoEcho: true` masks parameter values with asterisks in the console, CLI descriptions, and event logs.
17. A — The `AWS::SSM::Parameter::Value<...>` parameter type dynamically fetches the latest parameter value from SSM Parameter Store.
18. B — `AWS::EC2::VPC::Id` is an AWS-specific parameter type that validates and populates existing VPC IDs in the console dropdown.
19. B — The `Outputs` section declares output values visible after deployment and exportable for cross-stack references.
20. A — Adding `Export: Name: <ExportName>` under an output item exposes it for cross-stack importation via `!ImportValue`.
21. B — `!ImportValue <ExportName>` imports a value exported by another stack's `Outputs` section.
22. A & B — `!GetAtt Resource.Attribute` and `Fn::GetAtt: [Resource, Attribute]` are the two valid shorthand and full YAML syntaxes.
23. A — `!GetAZs ""` returns an array of Availability Zones for the current deployment Region.
24. B — `!Base64` encodes plain text into a Base64 string required by EC2 UserData.
25. B — YAML supports native `#` comments, whereas standard JSON does not support comments.
26. A — `!Sub [String, { VarMap }]` substitutes explicit mapping variables defined in the second argument dictionary.
27. A — `!Not [!Condition ConditionName]` inverts the boolean result of an existing condition.
28. A — `!Select [index, list]` retrieves a single element from an array by its zero-based index.
29. A — `Transform: AWS::Serverless-2016-10-31` instructs CloudFormation to execute the SAM macro and expand serverless shorthand resources.
30. A — The `Metadata: AWS::CloudFormation::Init` section defines configuration directives processed by the `cfn-init` helper script.
31. B — CloudFormation prevents modifying or deleting an exported output while another active stack imports it via `!ImportValue`.
32. B — To break a cross-stack dependency, update the importing stack first to remove `!ImportValue`, then update the exporting stack to remove `Export`.
33. B — Nested Stacks compose multiple templates together using `AWS::CloudFormation::Stack` resources managed under a parent stack lifecycle.
34. B — Child templates in a Nested Stack must be uploaded to an Amazon S3 bucket accessible by CloudFormation.
35. A — Nested stacks are composed and deployed together as parent-child units; cross-stack references loosely couple independent stacks.
36. B — CloudFormation Change Sets preview the exact additions, modifications, and replacements before executing a stack update.
37. B — `Replacement: True` in a change set indicates the resource will be deleted and recreated, which causes data loss for databases.
38. B — CloudFormation StackSets deploys stacks across multiple AWS accounts and Regions from a central administrator account.
39. B — Stack Drift Detection compares the live state of AWS resources against the template definition and reports drifted properties.
40. B — Drift detection is read-only; it reports differences between actual and expected configurations without modifying live resources.
41. B — On stack creation failure, CloudFormation initiates a rollback by default, deleting all created resources (`ROLLBACK_COMPLETE`).
42. A — Passing `--disable-rollback` preserves successfully created resources on failure for easier troubleshooting.
43. B — On update failure, CloudFormation rolls back to the last known good configuration (`UPDATE_ROLLBACK_COMPLETE`).
44. A — `ContinueUpdateRollback` resumes a failed rollback, allowing unrecoverable resources to be skipped to restore stack stability.
45. A — `aws cloudformation validate-template` verifies the syntax and structure of a template file before deployment.
46. B — A CloudFormation Macro is a custom Lambda-backed transform that manipulates template syntax dynamically before stack processing.
47. A — Stack Termination Protection prevents a stack from being deleted accidentally via the console or API.
48. B — With Termination Protection enabled, CloudFormation blocks delete requests until protection is explicitly disabled.
49. A — Direct template bodies are limited to 51,200 bytes; templates up to 1 MB can be deployed by uploading to S3 (`TemplateURL`).
50. B — A Stack Policy prevents stack updates from accidentally modifying or replacing critical protected resources.
51. A — A CloudFormation Service Role allows CloudFormation to assume a dedicated IAM role for resource provisioning operations.
52. A — A dedicated Service Role enables least-privilege deployments without granting broad direct permissions to developers.
53. A — `NotificationARNs` publishes stack event notifications to specified Amazon SNS topics.
54. B — CloudFormation builds a dependency graph using implicit references (`!Ref`/`!GetAtt`) and explicit `DependsOn` declarations.
55. A — `DependsOn` enforces ordering when resources depend on each other without an explicit `!Ref` or `!GetAtt` reference.
56. A — `DeletionPolicy: Retain` preserves the resource when its CloudFormation stack is deleted.
57. A — `DeletionPolicy: Snapshot` takes a final backup snapshot of supported resources (RDS, EBS) before deletion.
58. B — The default `DeletionPolicy` is `Delete` for resources if not explicitly specified.
59. B — Deleting an S3 bucket resource fails if the bucket contains objects; S3 requires buckets to be empty before deletion.
60. A — `UpdateReplacePolicy: Snapshot` creates a final snapshot of a resource before it is replaced during a stack update.
61. A — The three valid options for `UpdateReplacePolicy` are `Delete`, `Retain`, and `Snapshot`.
62. A — CloudFormation Custom Resources (Lambda-backed) execute custom logic during stack creation, update, and deletion.
63. A — `ServiceToken` specifies the ARN of the Lambda function or SNS topic that handles custom resource events.
64. A — CloudFormation sends `Create`, `Update`, and `Delete` request types to Custom Resource handlers.
65. A — The Lambda function must send an HTTP PUT request with status and data to the pre-signed S3 `ResponseURL`.
66. B — Failing to respond to `ResponseURL` causes CloudFormation to hang until the 1-hour stack timeout elapses, then fail.
67. A — The `cfnresponse` Python module provides helper functions to send success/failure responses to CloudFormation.
68. A — Values returned in the `Data` object of a Custom Resource response are accessed using `!GetAtt ResourceName.AttributeName`.
69. A — Properly handling `Delete` ensures external resources are cleaned up and stack deletion is not blocked.
70. A — During updates, CloudFormation invokes the custom resource Lambda with `RequestType: Update` and previous/new properties.
71. A — A Lambda-backed Custom Resource manages non-native resources (like OpenSearch indexes) within the CloudFormation lifecycle.
72. A — `UpdatePolicy` controls rolling update and replacement behaviors for Auto Scaling groups in CloudFormation.
73. A — `CreationPolicy` pauses stack creation until a specified number of success signals are received from instances.
74. A — Failing to receive required signals within the timeout causes CloudFormation to fail and roll back the stack.
75. A — The `cfn-signal` helper script sends success/failure signals back to CloudFormation from within EC2 UserData.
76. B — AWS SAM is an open-source framework extending CloudFormation with shorthand serverless syntax and local testing tools.
77. A — `Transform: AWS::Serverless-2016-10-31` is the required header that activates the SAM transform.
78. B — `AWS::Serverless::Function` defines a Lambda function, its IAM role, environment variables, and event triggers.
79. B — The `Globals` section defines common configuration properties (runtime, timeout, memory) shared by all SAM functions.
80. A — Adding an event of `Type: Api` under `Events:` automatically generates the API Gateway route and invocation permissions.
81. A — SAM Policy Templates (e.g., `DynamoDBCrudPolicy`) generate scoped IAM policies with minimal boilerplate.
82. A — `KMSDecryptPolicy` grants permissions to decrypt data using the specified AWS KMS key ID.
83. A — `sam local invoke <Function>` invokes a Lambda function locally with an event payload without deploying to AWS.
84. A — The SAM CLI runs local invocations inside Docker containers that emulate official AWS Lambda runtime environments.
85. A — `sam local start-api` starts a local HTTP server on `localhost:3000` emulating Amazon API Gateway.
86. B — `sam build` installs dependencies and compiles source artifacts into `.aws-sam/build`.
87. A — `sam package` uploads local build artifacts to S3 and outputs a template with updated S3 URIs.
88. A — `samconfig.toml` stores default parameters and environment configurations generated by `sam deploy --guided`.
89. A — `samconfig.toml` defines named environment sections (`[env.deploy.parameters]`) selected via `--config-env <name>`.
90. A — `--parameter-overrides` passes parameter key-value overrides during `sam deploy`.
91. A — `AWS::Serverless::SimpleTable` creates a basic DynamoDB table with a single primary key.
92. A — Standard `AWS::DynamoDB::Table` is used when tables require GSIs, LSIs, Streams, or complex configurations.
93. A — `DeploymentPreference: { Type: Canary... }` configures automated CodeDeploy traffic shifting for SAM functions.
94. A — `Hooks: { PreTraffic: ..., PostTraffic: ... }` executes Lambda validation functions before and after traffic shifting.
95. A — `AWS::Serverless::StateMachine` defines a serverless Step Functions workflow in SAM.
96. A — `sam sync --watch` synchronizes local code changes directly to an active development stack in near real-time.
97. A — `AWS::Serverless::GraphQLApi` defines an AWS AppSync GraphQL API in SAM.
98. A — Declaring variables under `Globals: Function: Environment: Variables:` makes them available across all SAM functions.
99. A — `sam init` scaffolds a new serverless application from curated starter templates.
100. A — `sam deploy` interacts with AWS CloudFormation by creating and executing Change Sets.
101. A — `sam validate` validates SAM templates against the JSON schema specification.
102. A — Standard CloudFormation resources and SAM shorthand resources can be freely mixed in the same template.
103. A — `Type: SQS` under `Events:` configures an Amazon SQS event source mapping for a Lambda function.
104. A — `AutoPublishAlias` automatically creates new function versions and points a named alias to the latest version on deploy.
105. A — Setting `Tracing: Active` under `Globals` enables AWS X-Ray tracing across SAM functions and APIs.
106. A — AWS Cloud Development Kit (AWS CDK) enables defining cloud infrastructure using general-purpose programming languages.
107. A — `cdk synth` synthesizes the CDK construct tree into a standard AWS CloudFormation template.
108. A — L1 = raw CloudFormation Cfn primitives; L2 = curated constructs with defaults; L3 = architectural patterns.
109. A — `table.grantReadWriteData(fn)` generates and attaches a scoped IAM policy granting read/write access to the table.
110. A — `aws_lambda.Function` is an L2 curated construct; `aws_lambda.CfnFunction` is an L1 primitive.
111. A — `ApplicationLoadBalancedFargateService` is an L3 pattern combining ALB, ECS, Fargate, and IAM resources.
112. A — `cdk bootstrap` provisions the S3 bucket, ECR repository, and IAM roles required by the CDK toolkit.
113. A — `cdk diff` compares the synthesized local template against the deployed CloudFormation stack in AWS.
114. A — `cdk deploy` synthesizes and deploys the CloudFormation stack to AWS.
115. A — Instantiating Stack classes with different `env: { account, region }` properties creates multi-environment stacks.
116. A — `cdk.App` is the root construct containing one or more CDK Stacks.
117. A — CDK allows using standard programming logic (loops, functions, classes) to generate repetitive infrastructure cleanly.
118. A — CDK supports unit and assertion testing against synthesized templates using `@aws-cdk/assertions`.
119. A — `cdk.json` specifies configuration and the entry point command used by the CDK CLI.
120. A — `ec2.Vpc.fromLookup` imports an existing VPC into a CDK stack without managing its lifecycle.
121. A — JSII compiles TypeScript CDK constructs into multiple programming languages (Python, Java, C#, Go).
122. A — AWS SAM is ideal for serverless apps requiring local API Gateway and Lambda emulation.
123. A — AWS CDK is ideal for complex infrastructure requiring object-oriented abstractions, loops, and type checking in TypeScript.
124. A — CloudFormation StackSets orchestrates multi-account, multi-region compliance deployments.
125. A — Requirement 1 maps to SAM (serverless/local testing), Requirement 2 to CDK (TypeScript/loops), and Requirement 3 to StackSets (multi-account).
