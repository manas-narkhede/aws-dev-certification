# Module 01 — Practice Questions (116)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Instance Types, Families & AMIs (1–12)

1. A team runs a nightly batch job that performs heavy video transcoding for exactly 45 minutes, requiring high sustained CPU throughput, then sits idle for the rest of the day. Cost efficiency matters, but so does finishing the transcoding quickly. Which EC2 instance family is the best fit for the compute profile during the active window?
A) T-family (burstable)
B) C-family (compute-optimized)
C) R-family (memory-optimized)
D) D-family (dense storage)

2. A company runs an in-memory session cache on EC2 that requires a very large amount of RAM relative to CPU, supporting millions of small session lookups per minute. Which instance family should they choose to match this profile?
A) C-family
B) R-family (memory-optimized)
C) T-family
D) G-family

3. A platform team wants to standardize new microservices on ARM-based EC2 instances to take advantage of better price-performance for compatible workloads, after confirming their container base images support the architecture. Which instance type naming element identifies an ARM-based (Graviton) instance?
A) A "g" suffix in the instance type, such as m6g.large
B) A "d" suffix, such as m6d.large
C) An "n" suffix, such as m6n.large
D) An "a" suffix, such as m6a.large

4. A developer builds and fully configures an EC2 instance with custom software, security patches, and application dependencies, and wants every new instance launched by their Auto Scaling group to start from this exact, pre-baked state rather than repeating lengthy configuration via user data at every boot. What should they create from the configured instance?
A) A security group
B) A custom AMI (a "golden AMI")
C) A new VPC
D) An IAM role

5. Which EC2 instance family is purpose-built for GPU-accelerated machine learning model training workloads?
A) T-family
B) P-family
C) M-family
D) I-family

6. A NoSQL database cluster running on self-managed EC2 nodes needs extremely high local disk IOPS for its working data set, and the team has already designed the application to tolerate node replacement without data loss (data is replicated elsewhere). Which instance family's local NVMe storage is best suited to this need?
A) T-family
B) I-family (storage-optimized)
C) R-family
D) C-family

7. A web application has generally low, unpredictable CPU usage throughout the day with brief spikes during business hours, and the team wants the most cost-effective instance family for this bursty-but-mostly-idle profile.
A) C-family
B) T-family (burstable)
C) I-family
D) P-family

8. Which of the following is an accurate description of what an Amazon Machine Image (AMI) contains?
A) Only network routing rules
B) The operating system, pre-installed software, and configuration used as a template to launch EC2 instances
C) Only IAM role definitions
D) Only a billing profile

9. A team stops an EC2 instance that has data stored only on its instance store volume (no EBS volumes attached for that data), intending to resume work the next day. What happens to that data when the instance is stopped?
A) It persists indefinitely, since instance store survives any stop/start cycle
B) It is lost, because instance store is ephemeral and does not survive a stop (though it does survive a simple reboot)
C) It automatically migrates to S3
D) It is preserved only if the instance has an IAM role attached

10. A company wants a general-purpose instance family with a balanced ratio of compute, memory, and network performance for a typical web application with no unusual resource skew. Which family should be the default starting point?
A) M-family (general purpose)
B) G-family
C) I-family
D) Dedicated Hosts

11. Which of the following is NOT a legitimate source from which an EC2 AMI can originate?
A) AWS-provided public AMIs
B) AWS Marketplace
C) A community-published AMI
D) An IAM policy document

12. A cost-conscious engineering team decides to standardize on Graviton (ARM-based) instances wherever their workloads are compatible, after benchmarking shows equivalent performance. What is the primary justification typically cited for this kind of migration?
A) Graviton instances have no compute limitations of any kind
B) Better price-performance for compatible workloads compared to equivalent x86 instances
C) Graviton instances are required for Auto Scaling to function
D) Graviton instances cannot use EBS storage

### Purchasing Options (13–24)

13. A company runs a fleet of on-call engineers' load-testing scripts that spin up compute for a few hours at unpredictable times, with no ability to forecast when they'll run next. Which EC2 pricing model best matches this usage pattern?
A) Standard Reserved Instances
B) On-Demand Instances
C) Dedicated Hosts
D) 3-year Savings Plans

14. A finance team commits to running a steady fleet of application servers for the next three years in exchange for the deepest possible discount, and is comfortable locking into a specific instance family without flexibility to change it later. Which purchasing option fits?
A) Convertible Reserved Instances
B) Standard Reserved Instances
C) Spot Instances
D) On-Demand Instances

15. A company runs commercial relational database software under a license that is billed per physical CPU socket and requires visibility into the specific physical server the software runs on for compliance auditing. Which EC2 purchasing option satisfies this licensing model?
A) Spot Instances
B) Dedicated Hosts
C) Savings Plans
D) On-Demand Instances

16. A distributed video-rendering farm processes jobs from a queue, checkpoints progress periodically, and can tolerate a node being reclaimed with two minutes' notice, resuming the job elsewhere. The team wants to minimize compute cost as aggressively as possible for this workload.
A) On-Demand Instances
B) Spot Instances
C) Standard Reserved Instances
D) Dedicated Hosts

17. Which of the following EC2 pricing models is LEAST appropriate for a single-node, non-clustered production database with no automated failover configured?
A) On-Demand Instances
B) Standard Reserved Instances
C) Spot Instances
D) Savings Plans

18. A team wants a compute discount that flexibly applies across a changing mix of EC2 instance families and AWS Fargate usage over the commitment period, rather than locking into one specific configuration. Which purchasing option is designed for this flexibility?
A) Standard Reserved Instances
B) Compute Savings Plans
C) Dedicated Instances
D) Spot Instances

19. An application running on Spot Instances needs to gracefully drain in-flight requests and checkpoint its work before the underlying instance is reclaimed. Where can the application detect an impending Spot interruption before it happens?
A) By polling the instance metadata service for a Spot interruption notice
B) By subscribing to an RDS event notification
C) By checking the EC2 console manually every few minutes
D) Spot interruptions cannot be detected in advance under any circumstance

20. Which two statements accurately distinguish Savings Plans from Reserved Instances?
A) Savings Plans commit to a consistent dollar-per-hour spend applied flexibly across eligible usage, rather than one fixed instance configuration
B) Standard Reserved Instances commit to a specific instance family in exchange for their discount, trading away some flexibility
C) Savings Plans are only available with a 6-month minimum term
D) Reserved Instances automatically convert to Spot pricing when unused
E) Savings Plans and Reserved Instances are functionally identical with no differences

21. A company purchases Reserved Instances in one member account of an AWS Organization with consolidated billing enabled. Can the RI discount benefit matching instance usage running in a different, linked member account?
A) No, RI discounts are strictly locked to the purchasing account
B) Yes, RI (and Savings Plan) discounts can be shared across linked accounts under AWS Organizations consolidated billing
C) Only if both accounts are in the same Availability Zone
D) Only if the second account also purchases identical RIs

22. Dedicated Instances differ from Dedicated Hosts primarily in that:
A) Dedicated Instances provide visibility into the physical server layout, while Dedicated Hosts do not
B) Dedicated Instances run on hardware dedicated to a single customer but without visibility into or control over the specific physical server, unlike Dedicated Hosts
C) Dedicated Instances are always more expensive than Spot Instances
D) Dedicated Instances cannot be launched in any VPC

23. A CI/CD build fleet processes short-lived, independent build jobs that can simply be retried from scratch if interrupted, and the team's top priority is minimizing compute spend for this fleet. Which purchasing option best matches this priority and workload shape?
A) Standard Reserved Instances
B) Spot Instances
C) Dedicated Hosts
D) On-Demand exclusively, to guarantee zero interruptions

24. A team is evaluating three separate workloads for EC2 purchasing strategy: a 24/7 steady-state production fleet, an unpredictable ad-hoc analytics workload with no fixed schedule, and a fault-tolerant nightly ETL batch job. Which pairing of pricing models correctly matches each workload in that order?
A) Spot, On-Demand, Reserved Instances
B) Reserved Instances/Savings Plans, On-Demand, Spot Instances
C) On-Demand, Reserved Instances, Dedicated Hosts
D) All three should use the same pricing model for simplicity

### Instance Metadata, User Data & IMDS (25–38)

25. A developer wants to pass a startup script to an EC2 instance that installs required packages and starts the application service automatically the first time the instance boots, without baking those steps permanently into a custom AMI. Which EC2 feature is designed for this?
A) A security group rule
B) EC2 user data, executed once on first boot via cloud-init on typical Linux AMIs
C) An IAM permissions boundary
D) A VPC endpoint policy

26. A penetration test finds that a web application running on an EC2 instance with IMDSv1 enabled can be tricked, via a server-side request forgery (SSRF) vulnerability, into fetching and returning the contents of the instance metadata service, including the attached IAM role's temporary credentials. What configuration change most directly closes this specific attack path?
A) Disabling the IAM role entirely
B) Enforcing IMDSv2 by setting HttpTokens to required, which requires an initial token-granting PUT request that a simple SSRF redirect typically cannot perform
C) Rotating the EC2 key pair
D) Switching the instance to a larger instance type

27. Application code running on an EC2 instance needs to determine its own instance ID and the IAM role currently attached to it, at runtime, without any hardcoded configuration. Where does this information come from?
A) A CloudFormation output value
B) The EC2 instance metadata service, queried locally from the instance itself
C) An IAM policy document stored in S3
D) The Route 53 hosted zone for the VPC

28. How does an EC2 instance profile actually make temporary IAM credentials available to an AWS SDK running in application code on that instance?
A) The credentials are baked permanently into the AMI at build time
B) The SDK automatically retrieves temporary, auto-rotated credentials from the instance metadata service based on the attached role
C) A developer must manually run aws configure on the instance after every reboot
D) The credentials are emailed to the instance's root account

29. A security team wants to enforce, account-wide, that all new EC2 instances only accept instance metadata requests that first obtain a session token via a PUT request, rather than allowing simple unauthenticated GET requests to the metadata endpoint. Which setting accomplishes this?
A) Disabling the metadata service entirely
B) Setting the instance metadata option HttpTokens to required, enforcing IMDSv2
C) Attaching a stricter security group
D) Enabling EBS encryption

30. Which of the following pieces of information can typically be retrieved from the EC2 instance metadata service by code running on that instance?
A) Only the instance's public IP address and nothing else
B) Instance ID, AMI ID, attached security groups, and the temporary credentials of any attached IAM role, among other properties
C) Only billing information for the AWS account
D) The root user's console password

31. A developer notices their application logs occasionally include the full raw JSON response returned by a call to the instance metadata service, for debugging purposes. What security risk does this practice introduce?
A) No risk; the metadata response never contains sensitive information
B) Potential leakage of the instance's temporary IAM role credentials into log storage, which may be less tightly access-controlled than the credentials themselves
C) It could cause the EC2 instance to restart unexpectedly
D) It only matters for Windows-based instances

32. Which of the following correctly describes typical EC2 user data behavior on a standard Linux AMI using cloud-init?
A) The user data script re-executes on every stop/start cycle
B) The user data script executes once, on the instance's first boot after launch
C) User data replaces the AMI's operating system entirely
D) User data requires an S3 bucket to function

33. A developer wants to supply a database connection string to an application at launch time without hardcoding it into the AMI or into user data in plaintext. Following AWS best practice, what should the application do instead?
A) Hardcode the connection string in the AMI
B) At boot, use the instance's IAM role to retrieve the connection string at runtime from a secrets/configuration service such as Secrets Manager or Parameter Store
C) Email the connection string to the instance after launch
D) Store the connection string as the instance's IAM role name

34. What HTTP method must a client first send to the IMDSv2 endpoint in order to obtain the session token required for subsequent metadata GET requests?
A) DELETE
B) PUT
C) PATCH
D) OPTIONS

35. Is the EC2 instance metadata endpoint at 169.254.169.254 reachable over the public internet?
A) Yes, it is publicly routable from anywhere
B) No, it is a link-local address reachable only from within the instance itself, not routed over the public internet
C) Only in the us-east-1 Region
D) Only if a public IP is attached to the instance

36. A company's security policy mandates that IMDSv1 be disabled account-wide for all new EC2 launches going forward, while allowing existing workloads time to migrate. Which configuration achieves the "disabled for new launches" requirement most directly at the instance level?
A) Deleting all existing IAM roles
B) Setting the instance metadata option HttpTokens to required on new launch templates/configurations
C) Disabling all security groups
D) Switching all new instances to Spot pricing

37. Which two of the following are true regarding EC2 user data and the instance metadata service?
A) User data can be used to run a bootstrap script once on first boot
B) The metadata service can expose the credentials of the instance's attached IAM role
C) User data and the metadata service are the exact same feature with different names
D) The metadata service is only accessible via the AWS Management Console
E) User data must always contain valid IAM policy JSON

38. A company migrating a legacy application to EC2 wants the application, once running, to automatically retrieve a rotating database password without any developer intervention after each rotation. Which combination of AWS capabilities supports this pattern?
A) A hardcoded password baked into the AMI, updated manually after every rotation
B) An IAM role attached to the instance, used at runtime to retrieve the current secret value from Secrets Manager, which handles rotation independently
C) Storing the password as EC2 user data, which is re-read on every application request
D) Emailing the new password to the operations team after each rotation

### EC2 & Related Storage (39–54)

39. A team needs an EBS volume type where IOPS and throughput can be provisioned independently of the volume's storage size, for a workload with variable performance needs that doesn't justify Provisioned IOPS pricing. Which volume type fits?
A) gp2
B) gp3
C) st1
D) sc1

40. Which AWS storage option is physically attached to the host and is lost when the instance is stopped or terminated, though it survives a simple reboot?
A) Amazon EBS
B) Instance store
C) Amazon EFS
D) Amazon S3

41. A financial services company runs a relational database on EC2 requiring consistently high, predictable IOPS regardless of variable workload spikes, and is willing to pay a premium for that consistency. Which EBS volume type should they provision?
A) sc1 (Cold HDD)
B) st1 (Throughput Optimized HDD)
C) io1/io2 (Provisioned IOPS SSD)
D) gp2 only, since all SSD types perform identically

42. Where are Amazon EBS snapshots stored, and how does incremental snapshotting behave?
A) Snapshots are stored only on the source instance and are always full copies
B) Snapshots are stored in Amazon S3, and after the first snapshot, subsequent snapshots are incremental (storing only changed blocks) while still representing a complete restorable point-in-time
C) Snapshots are stored in Glacier exclusively and cannot be used to create new volumes
D) Snapshots are stored on a separate EC2 instance dedicated to backups

43. A company needs a shared file system that can be mounted concurrently, over NFS, by dozens of EC2 instances spread across multiple Availability Zones within a Region, growing elastically without manual capacity provisioning. Which storage service fits this requirement?
A) Amazon EBS
B) Amazon EFS
C) Instance store
D) A single gp3 volume shared via a script

44. Which EBS volume type is optimized for high-throughput, sequential workloads such as big data processing and log processing, but cannot be used as a boot volume?
A) gp3
B) st1 (Throughput Optimized HDD)
C) io2
D) Instance store

45. A team needs the cheapest possible EBS storage tier for archival data that is accessed only a few times per year and does not require fast random-access performance. Which volume type fits?
A) io1
B) gp3
C) sc1 (Cold HDD)
D) Instance store

46. Can an EBS volume created in Availability Zone us-east-1a be directly attached to an EC2 instance running in us-east-1b?
A) Yes, EBS volumes can attach across any AZ in the same Region
B) No, EBS volumes are AZ-scoped and can only attach to instances within that same AZ
C) Yes, but only for gp3 volumes
D) Yes, but only if both AZs share a subnet

47. A team needs to increase the size of a live, in-use gp3 EBS volume attached to a production instance, without incurring downtime. Is this possible, and what follow-up step is typically needed?
A) It is not possible; the volume must be detached and recreated
B) Yes, gp3 volumes can be resized live without detaching; the OS/filesystem may then need to be extended to make use of the additional space
C) Yes, but only if the instance is first terminated
D) Yes, but the data is erased during the resize

48. Which is the best-practice default choice for a general-purpose EC2 boot volume today, balancing cost and performance for most workloads?
A) sc1
B) st1
C) gp3
D) Instance store only, for cost savings

49. A workload needs extremely high local IOPS for temporary scratch/cache data, is designed to tolerate data loss on instance replacement (data is not the source of truth), and wants to avoid the network overhead of EBS. Which storage option fits?
A) EFS
B) Instance store
C) sc1
D) A cross-Region EBS volume

50. Which two statements correctly describe the durability relationship between EBS and instance store?
A) EBS volumes persist independently of the instance's lifecycle until explicitly deleted
B) Instance store data does not survive an instance stop or terminate action
C) Instance store is more durable than EBS in every scenario
D) EBS volumes are lost whenever the instance is rebooted
E) Instance store and EBS have identical durability guarantees

51. A team wants to migrate a legacy NFS file server used by multiple on-premises and EC2-based applications to a fully managed AWS service with elastic capacity and POSIX file semantics, avoiding manual volume resizing. Which service is the natural fit?
A) Amazon EBS
B) Amazon EFS
C) Amazon S3
D) Instance store

52. Which of the following is a valid reason to prefer instance store over EBS for a specific EC2 workload component?
A) The data must persist for years regardless of instance lifecycle
B) The workload needs extremely low-latency local disk access for temporary/cache data and can tolerate loss on instance replacement
C) The data needs to be shared across multiple Availability Zones simultaneously
D) The team wants the lowest possible cost for long-term archival

53. A company restoring from an EBS snapshot to create a new volume in a different Availability Zone within the same Region — is this supported?
A) No, snapshots can only restore to the original AZ
B) Yes, EBS snapshots are stored in S3 (Region-level durability) and can be used to create a new volume in any AZ within that Region
C) No, snapshots can only be restored in a different Region
D) Yes, but only for io2 volumes

54. Which two of the following statements about EBS snapshot behavior are accurate?
A) The first snapshot of a volume is a full copy; subsequent snapshots only store changed blocks
B) Each snapshot, regardless of being incremental in storage, represents a complete, independently restorable point-in-time image
C) Snapshots cannot be copied across Regions under any circumstance
D) Deleting an intermediate snapshot in a chain always deletes all data needed for later snapshots too
E) Snapshots are billed identically to full standalone copies regardless of incremental storage

### Elastic Load Balancing (55–70)

55. A company runs a microservices application where requests to /orders should route to one backend service and requests to /accounts should route to a different backend service, all over HTTPS with a single public endpoint. Which AWS load balancer type is designed for this content-based routing?
A) Network Load Balancer
B) Application Load Balancer
C) Gateway Load Balancer
D) A single EC2 instance running as a reverse proxy, since no ELB supports this

56. A trading platform requires extremely low-latency TCP handling capable of millions of requests per second, along with a static IP address for allowlisting by downstream partners. Which load balancer type is the best fit?
A) Application Load Balancer
B) Network Load Balancer
C) Classic Load Balancer
D) Gateway Load Balancer

57. A security team wants to transparently insert third-party virtual security appliances (such as intrusion detection/prevention systems) into the traffic path between the internet and their application, without redesigning the application's own load balancing. Which AWS load balancer type is purpose-built for this pattern?
A) Application Load Balancer
B) Network Load Balancer
C) Gateway Load Balancer
D) Classic Load Balancer

58. Besides EC2 instances, which of the following can an Application Load Balancer's target group route traffic to?
A) Only EC2 instances, nothing else
B) IP addresses, AWS Lambda functions, and ECS tasks, among other target types
C) Only S3 buckets
D) Only RDS database instances

59. Which load balancer type is generally considered legacy and is not recommended for new application designs on the exam or in practice?
A) Application Load Balancer
B) Network Load Balancer
C) Classic Load Balancer
D) Gateway Load Balancer

60. A request from a client reaches the target's Security Group successfully (inbound allowed), but the client never receives a response, and the target's application logs show the request was processed correctly. After confirming the Security Group is correctly configured, what should be checked next?
A) The AMI version of the target instance
B) The subnet's Network ACL rules, since NACLs are stateless and might be silently blocking the return traffic even though the Security Group allowed the inbound request
C) The Region's list of Availability Zones
D) The IAM role attached to the load balancer

61. A real-time multiplayer game backend needs to load balance a UDP-based protocol used for low-latency game state updates. Which AWS load balancer type supports UDP traffic?
A) Application Load Balancer
B) Network Load Balancer
C) Classic Load Balancer
D) None of the ELB types support UDP

62. A team wants to terminate TLS at the client-facing edge for compliance visibility, while passing the raw, unmodified TCP stream through to backend targets that perform their own additional processing. Which capability, tied to a specific load balancer type, supports this pattern?
A) ALB path-based routing
B) NLB TLS passthrough
C) Gateway Load Balancer inline inspection only
D) Classic Load Balancer sticky sessions

63. Which ELB feature allows a client's subsequent requests during a session to consistently reach the same backend target, useful for applications that store session state locally on the instance rather than in an external store?
A) Cross-zone load balancing
B) Sticky sessions
C) Path-based routing
D) TLS passthrough

64. A company wants to gradually shift 10% of production traffic to a new application version deployed in a separate target group, increasing the percentage over time if no errors are observed, without redeploying the load balancer itself. Which ALB capability supports this canary-style pattern?
A) Cross-zone load balancing
B) Weighted target group routing rules on a listener rule
C) A Network Load Balancer TLS listener
D) Gateway Load Balancer appliance routing

65. What does enabling cross-zone load balancing on an ELB accomplish?
A) It encrypts traffic between the load balancer and targets
B) It distributes incoming traffic evenly across targets in all enabled Availability Zones, rather than only among targets in the AZ that received the request
C) It disables health checks for improved performance
D) It is exclusively a Network Load Balancer feature with no equivalent elsewhere

66. Which AWS resource must be configured on an Application Load Balancer to allow clients to connect over HTTPS using a valid, AWS-managed TLS certificate?
A) A Network ACL rule referencing the certificate
B) An HTTPS listener referencing a certificate issued or imported through AWS Certificate Manager (ACM)
C) A Security Group rule containing the certificate
D) A Route 53 alias record containing the certificate

67. What determines whether a specific backend target receives traffic from a load balancer at any given moment?
A) The instance's billing tier
B) The target's current health check status within its target group
C) The Availability Zone's total instance count
D) The AMI used to launch the target

68. A company needs WebSocket support for a real-time chat application behind a load balancer, in addition to standard HTTP/HTTPS routing. Which load balancer type natively supports WebSockets?
A) Application Load Balancer
B) Gateway Load Balancer exclusively
C) Classic Load Balancer exclusively
D) No AWS load balancer supports WebSockets

69. A team troubleshoots intermittent connection failures to a load-balanced application and confirms both the Security Group and Network ACL rules correctly allow the traffic in both directions. Health checks on the target group show the target as healthy. Which of the following is the LEAST likely remaining cause, given the checks already performed?
A) An application-level bug causing intermittent 5xx errors under load
B) Target group deregistration delay during a deployment causing brief connection drops
C) The Security Group is blocking inbound traffic (already ruled out by the scenario)
D) Insufficient target capacity causing connection queuing under peak load

70. Which two of the following are accurate statements about Application Load Balancers?
A) They operate at Layer 7 and support content-based routing using path or host rules
B) They can route traffic to Lambda functions as a target type
C) They support raw TCP passthrough with no visibility into HTTP semantics
D) They cannot use HTTPS listeners under any configuration
E) They are limited to a single target group with no routing rules

### Auto Scaling (71–86)

71. A team is configuring a new Auto Scaling group and wants the most current, flexible way to define what gets launched, including support for mixing instance types and versioning the launch configuration over time. Which resource should they use?
A) A Launch Configuration (legacy)
B) A Launch Template
C) A raw AMI reference with no template
D) A CloudFormation parameter file only

72. A team wants the simplest Auto Scaling policy that automatically adjusts capacity to keep average CPU utilization near a target value, without manually defining step thresholds. Which scaling policy type fits?
A) Scheduled scaling
B) Target tracking scaling
C) Step scaling
D) Manual scaling only

73. An Auto Scaling group needs to run a custom script to gracefully deregister an instance from an internal service registry before that instance is actually terminated during a scale-in event. Which ASG feature supports running custom logic at this specific point in the instance lifecycle?
A) A scheduled scaling action
B) A lifecycle hook
C) A target tracking policy
D) A Launch Template version

74. An Auto Scaling group is configured with only EC2 status checks (not ELB health checks) as its health check type. An application process on one instance crashes due to an unhandled exception, but the underlying instance and OS remain healthy. What will the ASG do?
A) Immediately replace the instance, since EC2 status checks detect application-level failures
B) Take no action, since EC2 status checks only detect infrastructure-level failures (like a hardware or OS failure), not application-level crashes
C) Automatically switch the health check type to ELB checks
D) Terminate the entire Auto Scaling group

75. A retail company knows from historical data that traffic reliably spikes every weekday morning at 9 AM as stores open, and wants capacity to increase just before that predictable spike rather than reactively after load increases. Which scaling approach fits best?
A) Target tracking scaling only
B) Scheduled scaling, timed just ahead of the known daily spike
C) Step scaling triggered only by memory alarms
D) Manual scaling performed by an on-call engineer each morning

76. What do the minimum, desired, and maximum capacity settings on an Auto Scaling group collectively define?
A) Only the billing tier for the group
B) The boundaries within which the ASG will automatically scale the number of instances
C) The number of Availability Zones available to the account
D) The maximum number of Load Balancers that can attach to the group

77. Which AWS Auto Scaling capability uses machine learning on historical load patterns to proactively provision capacity ahead of anticipated demand, rather than reacting to real-time metrics alone?
A) Step scaling
B) Predictive scaling
C) Scheduled scaling
D) Target tracking scaling

78. Why is it recommended to configure an Auto Scaling group's instances across multiple subnets in different Availability Zones rather than a single subnet in one AZ?
A) It is required to use Spot Instances
B) It provides high availability, allowing the workload to tolerate the loss of a single Availability Zone
C) It disables health checks by default
D) It is only relevant for Network Load Balancers

79. An unhealthy instance managed by an Auto Scaling group is terminated and replaced. The application stored active user session data only in that instance's local memory, with no external session store. What happens to that session data?
A) It is automatically migrated to the replacement instance
B) It is lost, illustrating why stateless application design or an external session store (such as ElastiCache) matters for ASG-managed fleets
C) It is preserved in the instance's EBS root volume permanently
D) The ASG pauses replacement until the data is manually backed up

80. Comparing step scaling to target tracking scaling, which statement is accurate?
A) Step scaling requires manually defined capacity increments tied to CloudWatch alarm thresholds, offering more granular control at the cost of more manual tuning than target tracking
B) Step scaling and target tracking are functionally identical
C) Step scaling cannot use CloudWatch alarms
D) Step scaling is deprecated and cannot be configured in new Auto Scaling groups

81. A team wants to balance cost savings with a guaranteed baseline of availability for a variable-traffic web tier. Which Auto Scaling / EC2 purchasing combination achieves both goals simultaneously?
A) A fixed-size fleet of On-Demand instances only, with no scaling
B) An Auto Scaling group using a Launch Template's mixed instances policy, combining a baseline of On-Demand capacity with Spot Instances for the remainder, scaled via target tracking
C) A single large Dedicated Host with no Auto Scaling
D) Manually launched instances added and removed by an engineer as needed

82. What triggers a scaling action under a target tracking Auto Scaling policy?
A) A human manually clicking "scale up" in the console every time
B) A CloudWatch metric (such as average CPU utilization) crossing the configured target value, evaluated automatically
C) A Lambda function that must be manually invoked on a fixed schedule
D) A Route 53 health check failure with no relation to the ASG's own metrics

83. During a scale-in event, an Auto Scaling group must choose which specific instance to terminate among several eligible candidates. What determines this choice?
A) The ASG's termination policy, which can consider factors like instance age or proximity to the next billing hour
B) A purely random selection with no configurable logic
C) Always the instance with the highest instance ID
D) Always the first instance that was ever launched, regardless of configuration

84. Which of the following can a Launch Template specify for instances an Auto Scaling group launches?
A) An IAM instance profile, AMI ID, instance type, and security groups
B) The literal JSON content of an entirely new IAM policy authored inline within the template
C) A permanent Reserved Instance discount applied retroactively
D) A manually assigned static private IP shared across all launched instances

85. Which two of the following are true about AWS Auto Scaling lifecycle hooks?
A) They allow custom actions (such as draining connections or deregistering from a service) to run before an instance is terminated or before it's put into service
B) They can pause an instance in a wait state until a custom action completes or a timeout is reached
C) They are only usable with Network Load Balancers
D) They automatically rewrite the AMI used by the Launch Template
E) They eliminate the need for any health checks

86. A company observes that during a sudden, brief traffic spike, their target-tracking Auto Scaling group takes a few minutes to add capacity, resulting in temporary degraded performance before scaling catches up. Which combination of adjustments would most directly help absorb the spike more quickly without switching away from target tracking?
A) Lowering the target metric threshold and/or increasing the ASG's minimum baseline capacity to provide more headroom before scaling is needed
B) Switching the health check type to EC2 status checks only
C) Removing the Launch Template entirely
D) Disabling CloudWatch metrics for the group

### Security Groups vs. Network ACLs (87–96)

87. Which statement correctly describes AWS Security Groups?
A) They are stateless and support explicit Deny rules
B) They are stateful (return traffic is automatically allowed) and support only Allow rules, with anything not explicitly allowed being implicitly denied
C) They operate at the subnet level, not the instance/ENI level
D) They are a global resource, not scoped to a VPC

88. Which statement correctly describes Network ACLs?
A) They are stateful, like Security Groups
B) They are stateless, meaning return traffic must be explicitly allowed by a separate rule in the opposite direction, and they support both Allow and Deny rules evaluated in numbered order
C) They can only be applied at the instance level
D) They evaluate all rules simultaneously with no defined order

89. A request from a client is permitted by the target instance's Security Group, but the client never receives a response. Investigation reveals the subnet's Network ACL has no explicit outbound rule allowing return traffic on the ephemeral port range back to the client. What is the most likely explanation?
A) Security Groups always override NACL behavior, so this shouldn't be possible
B) Because NACLs are stateless, the missing outbound rule for return traffic blocks the response even though the Security Group allowed the original inbound request
C) IAM permissions are blocking the response
D) The AMI does not support responding to requests

90. Which of the following correctly distinguishes the scope at which Security Groups and Network ACLs operate?
A) Both operate at the VPC level with no distinction
B) Security Groups operate at the instance/ENI level; Network ACLs operate at the subnet level
C) Security Groups operate at the subnet level; Network ACLs operate at the instance level
D) Both operate only at the Region level

91. Can a Security Group contain an explicit rule that denies specific traffic?
A) Yes, Security Groups support both Allow and Deny rules equally
B) No, Security Groups only support Allow rules; any traffic not explicitly allowed is implicitly denied
C) Only for outbound traffic
D) Only when attached to a NAT Gateway

92. A subnet's Network ACL has an explicit Deny rule blocking inbound traffic on port 22 (SSH), while the target instance's Security Group explicitly allows inbound port 22. What is the actual result when someone attempts to SSH into the instance?
A) SSH access is allowed, because the Security Group's Allow takes precedence
B) SSH access is blocked, because the NACL's explicit Deny takes effect at the subnet boundary regardless of what the instance's Security Group allows
C) The result is undefined and varies by request
D) SSH access alternates between allowed and blocked randomly

93. What is the typical default behavior of a newly created custom Security Group before any rules are added?
A) It allows all inbound and outbound traffic from any source
B) It denies all inbound traffic by default while typically allowing all outbound traffic by default, until inbound rules are explicitly added
C) It blocks all traffic in both directions permanently with no way to change it
D) It behaves identically to a Network ACL

94. When troubleshooting a connectivity failure to an EC2 instance inside a VPC, which combination of checks is necessary to confirm network-layer access is not the blocker?
A) Only the Security Group needs to be checked; NACLs are irrelevant
B) Both the instance's Security Group rules AND the subnet's Network ACL rules (in both directions, given NACL statelessness) must permit the traffic
C) Only the Network ACL needs to be checked; Security Groups are irrelevant
D) Only IAM policies need to be checked; network configuration is irrelevant to connectivity

95. Which two of the following statements about Security Groups and Network ACLs are correct?
A) Security Groups evaluate all applicable rules together, with the most permissive matching rule effectively governing the outcome (since only Allow rules exist)
B) Network ACL rules are evaluated in numbered order, and the first matching rule (Allow or Deny) is applied
C) Network ACLs are stateful, requiring no return-traffic rule
D) Security Groups can include explicit Deny rules alongside Allow rules
E) Security Groups and NACLs are the exact same resource type under different names

96. A company wants an extra layer of subnet-level defense that can explicitly block traffic from a known-malicious IP range, in addition to their existing Security Group rules. Which resource is best suited to add an explicit Deny for this specific IP range at the subnet level?
A) A Security Group Deny rule, since Security Groups support Deny
B) A Network ACL rule explicitly denying that IP range, since NACLs (unlike Security Groups) support explicit Deny rules
C) An IAM permissions boundary
D) A Route 53 DNS filtering rule

### Systems Manager for Developers (97–106)

97. A company wants to eliminate SSH access entirely from their EC2 fleet's Security Groups, closing port 22, while still allowing engineers to open a shell on an instance when needed, with every session centrally logged for audit purposes. Which AWS capability satisfies this?
A) A bastion host with a shared SSH key
B) AWS Systems Manager Session Manager, which provides IAM-governed shell access without requiring any inbound ports to be open
C) Disabling all remote access permanently
D) A VPN concentrator requiring a static IP allowlist

98. What must be present on an EC2 instance for Systems Manager Session Manager and Run Command to function?
A) Nothing beyond a running operating system
B) The SSM Agent running on the instance, along with an IAM role attached to the instance granting the necessary Systems Manager permissions
C) A permanently open SSH port
D) A dedicated bastion host in the same subnet

99. A team needs to apply the same patch script across 300 EC2 instances simultaneously, without SSH access to any of them, using IAM-controlled API calls rather than manual login. Which Systems Manager capability is designed for this?
A) Systems Manager Parameter Store
B) Systems Manager Run Command
C) Systems Manager Session Manager, for scripted fleet-wide changes
D) EC2 Auto Scaling termination policies

100. Why does the exam favor Systems Manager Session Manager over a traditional bastion host with SSH key distribution for secure instance access?
A) It requires no IAM configuration whatsoever
B) It avoids exposing any inbound SSH port and centralizes access control and audit logging through IAM and CloudTrail
C) It disables CloudWatch logging entirely
D) It only works for Windows instances

101. Systems Manager Parameter Store SecureString parameter values are encrypted using which AWS service?
A) A hardcoded key embedded in the AMI
B) AWS Key Management Service (KMS)
C) No encryption is actually applied; "SecureString" is only a label
D) TLS only, with no encryption at rest

102. A developer wants to retrieve a piece of non-secret application configuration (such as a feature flag value) at runtime from a centralized, hierarchical key-value store, without paying for a full secrets-management service. Which AWS capability is well suited and cost-effective for this use case?
A) AWS Secrets Manager exclusively
B) Systems Manager Parameter Store (Standard tier, at no additional charge)
C) Amazon Cognito
D) AWS CodeArtifact

103. Which two of the following are accurate about AWS Systems Manager Session Manager?
A) It requires opening inbound port 22 or 3389 to function
B) Session activity can be logged to CloudWatch Logs or S3 for auditing
C) Access to start a session is governed by IAM policy
D) It requires a shared SSH key distributed to every engineer
E) It cannot be used for Linux instances, only Windows

104. A fleet of EC2 instances is missing the SSM Agent, and attempts to use Run Command against them fail silently with no response. What is the most likely root cause?
A) The instances are using the wrong instance family
B) The SSM Agent is not installed/running, or the instance's IAM role lacks the required Systems Manager permissions
C) Security Groups always block Systems Manager regardless of configuration
D) Run Command requires a Reserved Instance purchase

105. Which of the following is a security benefit of Systems Manager Run Command over manually SSHing into each instance to run an identical command?
A) It requires storing a shared SSH private key on every engineer's laptop
B) Every invocation is authorized via IAM and recorded, without needing to distribute or manage SSH keys at all
C) It bypasses all IAM permission checks for speed
D) It disables logging to reduce noise

106. A team wants Parameter Store to automatically rotate a stored secret's value on a schedule, similar to native rotation available elsewhere. What should they be aware of regarding Parameter Store's native capabilities?
A) Parameter Store natively provides scheduled automatic rotation identical to Secrets Manager, with zero extra configuration
B) Parameter Store does not provide native automatic rotation; achieving scheduled rotation typically requires custom automation (e.g., a Lambda function on an EventBridge schedule), whereas Secrets Manager offers this natively for supported services
C) Parameter Store cannot store any value related to secrets under any circumstance
D) Rotation is only possible for parameters tagged as "SecureString" and never for Standard strings

### EC2 vs. Other Compute Choices & Integrative Scenarios (107–116)

107. A company needs to process short-lived, event-driven work triggered by S3 object uploads, with unpredictable and bursty invocation rates, and wants zero server management overhead. Which compute option best fits, compared to provisioning EC2 with Auto Scaling?
A) EC2 with a large fixed fleet
B) AWS Lambda
C) EC2 Dedicated Hosts
D) EC2 Spot Fleet permanently sized at maximum capacity

108. A team wants to deploy a web application quickly with minimal day-to-day operations overhead, while still retaining the ability to inspect and occasionally tune the underlying EC2 instances, load balancer, and Auto Scaling group the platform provisions on their behalf. Which compute option best matches this balance?
A) AWS Lambda exclusively
B) AWS Elastic Beanstalk
C) Manually provisioned EC2 with no automation whatsoever
D) Dedicated Hosts

109. Which phrase, when it appears in a DVA-C02 scenario's requirements, most strongly signals that the correct answer favors a managed or serverless compute option over raw EC2?
A) "Full control over the underlying operating system is required"
B) "Least operational overhead"
C) "Custom kernel modules must be installed"
D) "Persistent local state on the instance is required"

110. A batch workload requires full operating system access, runs for approximately 45 minutes per job, and needs to scale to hundreds of concurrent jobs at peak. Because 45 minutes exceeds Lambda's maximum execution duration, which compute approach is appropriate instead?
A) AWS Lambda regardless of the duration limit, since limits can be waived on request
B) EC2 (potentially orchestrated via AWS Batch) or a container-based service like ECS/Fargate designed for longer-running, full-OS-access workloads
C) Amazon API Gateway
D) Amazon Route 53

111. A team is deciding between attaching an IAM role to an EC2 instance versus embedding an IAM user's access keys in the instance's user data script, for an application that calls S3 and DynamoDB. Which two considerations support choosing the IAM role?
A) The role provides temporary, automatically rotated credentials with no long-term secret stored on the instance
B) User data is visible to anyone who can call the EC2 DescribeInstanceAttribute API for that instance (with appropriate permissions), making embedded long-term keys there a greater exposure risk than role-derived temporary credentials
C) IAM roles are always free while access keys always incur a cost
D) Access keys embedded in user data automatically rotate every 24 hours
E) IAM roles cannot be used by EC2 instances, only by Lambda

112. A company's ASG is scaling reactively but too slowly during sudden traffic spikes, causing brief performance degradation, and separately, their T3 instances used for the compute-heavy portion of the workload are being throttled under sustained load. Which two changes together address both issues?
A) Increase the ASG's minimum baseline capacity or lower the target tracking threshold to add headroom, and switch the compute-heavy workload from a T-family (burstable) instance to a non-burstable family like C or M
B) Switch to EC2 status checks only and keep the T3 instances unchanged
C) Disable Auto Scaling entirely and rely on a single large instance
D) Move the compute-heavy workload to Spot Instances with no On-Demand baseline
E) Increase the T3 instance's storage size, which resolves CPU credit exhaustion

113. A security review of an EC2-based application finds: IMDSv1 still enabled account-wide, an ASG using only EC2 status checks, hardcoded IAM user access keys in application code, and a Network ACL with no explicit rules beyond the default allow-all. Which of the following changes correctly addresses each finding, in order?
A) Enforce IMDSv2, add ELB health checks to the ASG, replace hardcoded keys with an IAM role, and review/tighten the NACL rules as an additional layer of defense
B) Disable the metadata service entirely, remove the ASG, delete the IAM role, and delete the NACL
C) Only fix the hardcoded keys; the other three findings are not real risks
D) Only fix the NACL; Security Groups alone are always sufficient

114. A company wants to run a fleet of EC2 instances that automatically replace themselves on both infrastructure failure and application-level failure, are spread across multiple Availability Zones for resilience, cost-optimize by blending Spot and On-Demand capacity, and expose a single HTTPS endpoint that performs path-based routing to multiple backend services. Which combination of AWS features together satisfies all of these requirements?
A) A single EC2 instance with a Security Group and no load balancer
B) An Auto Scaling group (with ELB health checks and a mixed instances policy) spanning multiple AZs, behind an Application Load Balancer configured with HTTPS listeners and path-based routing rules
C) A Network Load Balancer alone with no Auto Scaling group
D) Dedicated Hosts with manual instance replacement

115. Which of the following best explains why a candidate should check both the Security Group AND the Network ACL when troubleshooting a connectivity issue to an EC2 instance in a custom VPC, rather than assuming a Security Group Allow rule guarantees the traffic will succeed?
A) Only the Security Group matters; NACLs are irrelevant to instance connectivity
B) Both layers must independently permit the traffic; a NACL's stateless nature means even a fully permissive Security Group can still be undermined by a missing or blocking NACL rule in either traffic direction
C) NACLs only apply to traffic leaving the VPC entirely, never to intra-VPC traffic
D) Security Groups are deprecated in favor of NACLs

116. Summarizing this module's exam-relevant EC2 concepts for a teammate studying separately, which single sentence best captures the recurring theme across instance metadata security, health check configuration, storage AZ-scoping, and IAM role usage?
A) EC2 is largely irrelevant to the DVA-C02 exam and can be skipped
B) Nearly every EC2 "gotcha" on this exam involves either a security misconfiguration (long-lived credentials, open metadata access) or a scope mismatch (AZ-bound resources, infrastructure-only health checks) that a more correctly-configured, still-EC2-based setup would have avoided
C) Only pricing model selection matters for EC2 questions; everything else is untested
D) EC2 questions never involve IAM at all

---

## Answer Key & Explanations

1. B — Sustained heavy CPU throughput for a defined window favors compute-optimized C-family over burstable or memory-optimized options.
2. B — R-family is memory-optimized, ideal for large in-memory caches.
3. A — The "g" suffix (e.g., m6g) denotes Graviton (ARM) processors.
4. B — A custom "golden AMI" captures the fully configured state for fast, consistent launches.
5. B — P-family is GPU-accelerated, used for ML training workloads.
6. B — I-family offers high local NVMe IOPS, matching this data-tolerant, high-performance need.
7. B — T-family suits low, bursty CPU usage cost-effectively.
8. B — An AMI is the OS + software + configuration template for launching instances.
9. B — Instance store is ephemeral and does not survive a stop (though it survives reboot).
10. A — M-family is the balanced, general-purpose default.
11. D — An IAM policy document is not a source for an AMI.
12. B — Better price-performance for compatible workloads is the typical Graviton migration justification.
13. B — On-Demand suits unpredictable, short-notice usage with no forecast.
14. B — Standard RIs trade flexibility for the deepest discount on a long-term commitment.
15. B — Dedicated Hosts expose the physical server, satisfying socket-based licensing audits.
16. B — Spot Instances suit checkpointable, interruption-tolerant workloads prioritizing lowest cost.
17. C — Spot is the worst fit for a single-node database with no failover.
18. B — Compute Savings Plans flexibly apply across EC2 families and Fargate.
19. A — The instance metadata service surfaces a Spot interruption notice before reclamation.
20. A & B — Savings Plans commit to flexible $/hour spend; Standard RIs commit to a specific family for their discount.
21. B — RI/Savings Plan discounts can share across linked accounts under consolidated billing.
22. B — Dedicated Instances lack the physical server visibility/control that Dedicated Hosts provide.
23. B — Retryable, short-lived build jobs are a strong Spot fit for minimizing cost.
24. B — Reserved/Savings Plans for steady-state, On-Demand for unpredictable ad-hoc, Spot for fault-tolerant batch.
25. B — User data runs a bootstrap script once on first boot via cloud-init.
26. B — Enforcing IMDSv2 (HttpTokens required) closes this SSRF-to-credential-theft path since it requires a token PUT first.
27. B — The instance metadata service exposes properties like instance ID and role information locally.
28. B — The SDK automatically retrieves temporary, auto-rotated credentials from the metadata service.
29. B — HttpTokens required enforces IMDSv2-only access account-wide via launch template/instance settings.
30. B — Metadata includes instance/AMI/security group details and attached role credentials, among other data.
31. B — Logging the raw metadata response risks leaking the instance's temporary IAM credentials.
32. B — Standard cloud-init behavior runs user data once, on first boot.
33. B — Retrieve secrets at runtime via the instance role from Secrets Manager/Parameter Store, not hardcoding.
34. B — IMDSv2 requires an initial PUT to obtain a session token before GETs succeed.
35. B — 169.254.169.254 is link-local, reachable only from the instance itself, not the public internet.
36. B — Setting HttpTokens to required on new launch templates enforces IMDSv2 for new launches.
37. A & B — User data supports one-time bootstrap scripts, and the metadata service can expose role credentials.
38. B — An attached IAM role retrieving secrets at runtime from Secrets Manager supports automatic, code-transparent rotation.
39. B — gp3 decouples IOPS/throughput provisioning from volume size.
40. B — Instance store is ephemeral, tied to the host, lost on stop/terminate.
41. C — io1/io2 provide consistent, high provisioned IOPS for demanding databases.
42. B — Snapshots live in S3, are incremental after the first, and each represents a complete restore point.
43. B — EFS is a shared, elastic, multi-AZ POSIX file system mountable by many instances.
44. B — st1 is throughput-optimized for big data/log workloads and is not bootable.
45. C — sc1 is the cheapest EBS tier, suited for infrequently accessed archival data.
46. B — EBS volumes only attach to instances within their own AZ.
47. B — gp3 volumes can be resized live; the filesystem may need a follow-up extend step.
48. C — gp3 is the modern default general-purpose boot volume choice.
49. B — Instance store offers very high local IOPS for temporary/cache data tolerant of loss.
50. A & B — EBS persists independently until deleted; instance store does not survive stop/terminate.
51. B — EFS provides fully managed, elastic, POSIX-compliant shared file storage.
52. B — Instance store fits low-latency, temporary/cache data tolerant of loss on replacement.
53. B — Snapshots reside in S3 (Region-durable) and can create volumes in any AZ within that Region.
54. A & B — First snapshot is full, later ones incremental in storage, but each is a fully restorable point-in-time.
55. B — Path-based routing over HTTPS is a defining ALB capability.
56. B — NLB suits extreme-performance TCP with static IP support.
57. C — Gateway Load Balancer is purpose-built for transparent third-party appliance insertion.
58. B — ALB target groups can route to IPs, Lambda functions, and ECS tasks, not just EC2.
59. C — Classic Load Balancer is legacy and not recommended for new designs.
60. B — Stateless NACLs can silently block the return leg even when the Security Group allowed the request.
61. B — NLB supports UDP; ALB does not.
62. B — NLB TLS passthrough delivers the raw TCP stream to backend targets unmodified.
63. B — Sticky sessions route a client's requests to the same target for session duration.
64. B — Weighted routing rules on ALB listener rules enable canary-style traffic shifting.
65. B — Cross-zone load balancing spreads traffic evenly across targets in all enabled AZs.
66. B — An HTTPS listener referencing an ACM certificate enables HTTPS termination on ALB.
67. B — A target's health check status determines whether it currently receives traffic.
68. A — ALB natively supports WebSockets.
69. C — That cause is explicitly ruled out by the scenario, making it the least likely remaining explanation.
70. A & B — ALB operates at Layer 7 with content-based routing and supports Lambda as a target type.
71. B — Launch Templates are the modern, versioned option supporting mixed instance types.
72. B — Target tracking automatically maintains a target metric value without manual step thresholds.
73. B — Lifecycle hooks allow custom actions at defined points in the launch/terminate lifecycle.
74. B — EC2 status checks catch infrastructure failures, not application-level crashes.
75. B — Scheduled scaling proactively adds capacity ahead of a known, predictable spike.
76. B — Min/desired/max define the boundaries within which the ASG scales automatically.
77. B — Predictive scaling uses ML on historical patterns to proactively provision capacity.
78. B — Multi-AZ spread provides high availability against a single AZ's failure.
79. B — In-memory session data is lost on replacement without an external store; design for statelessness.
80. A — Step scaling uses manually tuned, alarm-driven increments, offering more control at more manual cost.
81. B — Mixed instances policy blending On-Demand and Spot under target tracking balances cost and availability.
82. B — A CloudWatch metric crossing the target value automatically triggers target tracking scaling actions.
83. A — The ASG's termination policy determines which instance is chosen during scale-in.
84. A — Launch Templates specify instance profile, AMI, instance type, security groups, and similar launch parameters.
85. A & B — Lifecycle hooks support custom pre-transition actions and can pause an instance in a wait state.
86. A — Lowering the target threshold or raising baseline minimum capacity provides more headroom to absorb spikes faster.
87. B — Security Groups are stateful and allow-only, with implicit deny for anything unlisted.
88. B — NACLs are stateless, support Allow and Deny, and are evaluated in numbered order.
89. B — The stateless NACL's missing return-traffic rule blocks the response despite the Security Group's allow.
90. B — Security Groups are instance/ENI-scoped; NACLs are subnet-scoped.
91. B — Security Groups support only Allow rules; everything else is implicitly denied.
92. B — The NACL's explicit Deny blocks the traffic at the subnet boundary regardless of the Security Group's Allow.
93. B — A new custom Security Group denies inbound by default and typically allows outbound by default.
94. B — Both Security Group and NACL rules (bidirectionally, due to NACL statelessness) must permit the traffic.
95. A & B — SGs combine Allow rules permissively; NACL rules are evaluated in numbered order, first match applies.
96. B — Only NACLs support explicit Deny rules, making them the tool for blocking a specific IP range at the subnet level.
97. B — Session Manager provides IAM-governed, portless shell access with centralized session logging.
98. B — Requires the SSM Agent running plus an IAM role granting the needed Systems Manager permissions.
99. B — Run Command executes scripts across many instances via IAM-controlled API calls, no SSH needed.
100. B — It avoids open SSH ports and centralizes access control/audit logging through IAM and CloudTrail.
101. B — SecureString parameters are encrypted using AWS KMS.
102. B — Parameter Store Standard tier is free and well suited to non-secret hierarchical configuration.
103. B & C — Session activity can be logged, and starting sessions is governed by IAM policy.
104. B — Missing/inactive SSM Agent or insufficient IAM role permissions are the most likely causes.
105. B — Every invocation is IAM-authorized and recorded without distributing or managing SSH keys.
106. B — Parameter Store lacks native automatic rotation; Secrets Manager provides this natively for supported services.
107. B — Short-lived, event-driven, bursty, zero-server-management work is a strong Lambda fit.
108. B — Elastic Beanstalk offers quick deployment while retaining visibility into the underlying provisioned resources.
109. B — "Least operational overhead" signals a managed/serverless answer over raw EC2 management.
110. B — Exceeding Lambda's duration limit with full-OS needs points to EC2/Batch or container-based compute.
111. A & B — Role-derived temporary credentials avoid long-term secrets, and user data can be read via the EC2 API, increasing exposure of embedded keys.
112. A — Adding ASG headroom and moving the CPU-heavy workload off burstable T-family both directly address the two described issues.
113. A — Enforce IMDSv2, add ELB health checks, replace hardcoded keys with a role, and tighten NACL rules as defense-in-depth.
114. B — A multi-AZ ASG with ELB health checks and mixed instances, behind an ALB with HTTPS and path-based routing, satisfies every stated requirement.
115. B — Both layers must independently permit traffic; a stateless NACL can undermine an otherwise-permissive Security Group.
116. B — The recurring theme is security misconfiguration or AZ/health-check scope mismatches, not EC2 itself being flawed.
