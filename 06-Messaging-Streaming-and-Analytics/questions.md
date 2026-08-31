# Module 06 — Practice Questions (134)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### SQS Fundamentals: Standard vs. FIFO, Ordering & Deduplication (1–18)

1. A logistics company processes warehouse pick-and-pack task messages where the exact order of task execution does not matter, but the company expects extremely high throughput with no realistic upper limit as the business grows. Which SQS queue type should the team choose?
A) A FIFO queue, because ordering guarantees are always preferable
B) A Standard queue, because it offers nearly unlimited throughput and ordering is not a requirement here
C) A FIFO queue with a single message group, to maximize throughput
D) Neither queue type; SNS should be used instead of SQS

2. A financial services company processes sequential account-ledger update commands for a single customer account and must guarantee that these commands are applied in the exact order they were submitted, with no duplicate application of any single command. Which SQS configuration satisfies both requirements?
A) A Standard queue with a short visibility timeout
B) A FIFO queue, using the customer account ID as the message group ID, relying on its ordering and deduplication guarantees
C) A Standard queue with message attributes used for manual ordering
D) A FIFO queue with a different message group ID for every message

3. A developer is troubleshooting a production incident in which the same order-confirmation email was sent to a customer three times. The application uses a Standard SQS queue with a Lambda consumer. What is the most accurate explanation for why this occurred?
A) SQS Standard queues guarantee exactly-once delivery, so this must be a bug unrelated to SQS
B) SQS Standard queues provide at-least-once delivery, meaning a message can be delivered more than once, and the consumer code was not idempotent
C) FIFO queues were used, and FIFO always redelivers messages three times
D) The message was corrupted in transit and SQS resent it as a safety measure

4. Which of the following correctly describes the deduplication mechanism available on an SQS FIFO queue?
A) FIFO queues never deduplicate messages under any configuration
B) FIFO queues can use either content-based deduplication (a hash of the message body) or an explicitly supplied MessageDeduplicationId, within a 5-minute deduplication interval
C) Deduplication is only available on Standard queues
D) Deduplication requires a separate DynamoDB table maintained by the developer in all cases

5. A queue name must end in which suffix to be provisioned as an SQS FIFO queue?
A) .ordered
B) .strict
C) .fifo
D) .seq

6. A team designing a new order-processing pipeline is deciding between Standard and FIFO SQS queues. Which of the following is an accurate tradeoff between the two queue types?
A) FIFO queues offer higher maximum throughput than Standard queues in every configuration
B) FIFO queues provide strict ordering and exactly-once processing within their deduplication window, at a lower maximum throughput ceiling (up to 3,000 msg/sec with batching) compared to Standard's nearly unlimited throughput
C) Standard queues guarantee strict ordering but not deduplication
D) There is no throughput difference between Standard and FIFO queues

7. A developer building a Standard-queue consumer wants to defend against the possibility of processing the same message twice, since Standard queues do not guarantee exactly-once delivery. What is the most robust application-level approach?
A) Reduce the visibility timeout to zero to prevent redelivery
B) Design the message-processing logic to be idempotent, for example by checking whether a unique identifier in the message has already been processed before taking action
C) Switch the queue's region to reduce duplicate delivery
D) Ignore the risk, since duplicates are statistically rare enough to not matter

8. Within an SQS FIFO queue, what does the "message group ID" control?
A) The maximum number of consumers allowed to poll the queue
B) Which messages are guaranteed to be delivered and processed in order relative to one another; messages with different group IDs may be processed in parallel without ordering guarantees between groups
C) The encryption key used for the message body
D) The visibility timeout applied to that specific message

9. A company migrating from a Standard queue to a FIFO queue for a payment-processing pipeline notices their expected throughput of 5,000 messages per second, spread across many unrelated customer accounts as separate message groups, exceeds the batched FIFO throughput ceiling for a single queue. Which approach addresses this while retaining per-account ordering?
A) Switch back to a Standard queue and accept out-of-order processing
B) Shard the workload across multiple FIFO queues (for example, by a hash of the customer account ID), since ordering is only guaranteed within a single queue's message groups, not across queues
C) Increase the FIFO queue's visibility timeout to raise its throughput ceiling
D) FIFO queues have no throughput ceiling, so this scenario is not possible

10. Which of the following statements about SQS Standard queues is accurate?
A) They guarantee messages are delivered in the exact order sent
B) They provide at-least-once delivery and make a best effort to preserve order, but do not guarantee strict ordering
C) They guarantee exactly-once delivery with no possibility of duplicates
D) They require a message group ID on every message

11. A developer is deciding whether an application's use case requires SQS FIFO or Standard. The application processes independent image-resizing jobs where each job is entirely self-contained and processing order between different jobs has no bearing on correctness. Which two statements support choosing Standard over FIFO for this case?
A) Standard offers substantially higher throughput ceilings, which benefits a high-volume, order-independent workload
B) FIFO's ordering guarantees provide no benefit here since jobs are independent, making the added complexity and lower throughput ceiling unnecessary
C) FIFO queues cannot be used with Lambda under any circumstance
D) Standard queues cannot be consumed by more than one consumer
E) FIFO queues are always more expensive per message regardless of workload

12. What is the maximum deduplication interval within which SQS FIFO content-based or explicit deduplication is applied?
A) 30 seconds
B) 5 minutes
C) 1 hour
D) 24 hours

13. A team observes that under normal conditions, messages in their Standard SQS queue are usually processed in the order sent, but occasionally are not. What best explains this behavior?
A) Standard queues are fundamentally broken and should never be used
B) Standard queues make a best effort to preserve ordering but do not guarantee it, unlike FIFO queues, so occasional reordering under distributed load is expected behavior, not a bug
C) The consumer application has a bug that must be fixed to restore guaranteed order
D) This only happens if a dead-letter queue is configured

14. Which SQS queue type would be the correct choice for a scenario explicitly requiring "no duplicate processing of any message under any circumstance, and strict preservation of submission order"?
A) Standard queue with a long visibility timeout
B) Standard queue with message attributes for ordering
C) FIFO queue
D) Either queue type works equally well for this requirement

15. A developer wants to send messages to a Standard SQS queue from multiple independent producer services without any coordination between them regarding ordering or deduplication identifiers. Which queue type requires the least additional producer-side logic to function correctly?
A) FIFO, since it requires no producer configuration at all
B) Standard, since it does not require a message group ID or deduplication ID from producers
C) Neither; SQS always requires a message group ID
D) FIFO, but only if all producers coordinate through a shared DynamoDB lock table

16. Which of the following are true statements about SQS FIFO queues? (Select TWO)
A) They guarantee that messages are processed in the exact order they are sent within a message group
B) They provide exactly-once processing within their deduplication interval
C) They support unlimited throughput identical to Standard queues in all cases
D) They allow any queue name without restriction
E) They guarantee ordering across all message groups in the queue, not just within a group

17. A company's e-commerce checkout system currently uses a Standard SQS queue and has started seeing rare cases where an inventory-decrement message is processed twice, oversubtracting stock. Which combination of fixes addresses the root cause most directly? (Select TWO)
A) Make the inventory-decrement operation idempotent, for example using a conditional update keyed on an order ID that has already been applied
B) Migrate to a FIFO queue if strict exactly-once semantics and ordering are required for this specific operation
C) Delete the queue and recreate it with the same name
D) Increase the number of consumers polling the queue
E) Disable the dead-letter queue

18. Which statement accurately compares throughput characteristics between SQS Standard and FIFO queues?
A) Standard queues offer nearly unlimited throughput, while FIFO queues support up to 3,000 messages per second per API action with batching (300 without)
B) FIFO queues always outperform Standard queues in raw throughput
C) Both queue types have an identical fixed throughput cap of 300 messages per second
D) Throughput is not a meaningful distinction between the two queue types

### SQS Visibility Timeout, Polling, DLQs & Delay Queues (19–38)

19. A consumer application polls an SQS queue, receives a message, and begins a processing routine that reliably takes about 90 seconds to complete. The queue's visibility timeout is left at the default value. What is the most likely operational consequence?
A) No consequence; SQS automatically detects long-running consumers and adjusts
B) Because the default visibility timeout (30 seconds) is shorter than the processing time, the message becomes visible again and a second consumer may pick it up and process it concurrently, causing duplicate processing
C) The message will be permanently deleted after 30 seconds regardless of processing status
D) The queue will automatically convert to a FIFO queue to prevent duplicates

20. Which SQS API call allows a consumer to extend the invisibility period of a message it is still actively processing, without needing to delete and re-send it?
A) ExtendMessageLifetime
B) ChangeMessageVisibility
C) UpdateQueueAttributes
D) RenewMessage

21. What is the maximum value that can be configured for an SQS queue's visibility timeout?
A) 30 seconds
B) 15 minutes
C) 12 hours
D) 7 days

22. A team wants to reduce the number of empty responses their polling consumers receive from SQS, in order to lower both API call costs and the latency to notice a newly arrived message. Which SQS feature should they configure?
A) A shorter visibility timeout
B) Long polling, by setting WaitTimeSeconds to a value between 1 and 20 seconds
C) A FIFO queue instead of Standard
D) A dead-letter queue

23. Which of the following best describes the behavior of SQS short polling (WaitTimeSeconds set to 0)?
A) It queries all servers behind the queue and guarantees a message will be returned if one exists
B) It can return an empty response immediately even if messages exist elsewhere in the distributed queue backend, since it does not necessarily query every server
C) It is the only polling mode compatible with FIFO queues
D) It is more cost-effective than long polling in all cases

24. A team configures a dead-letter queue (DLQ) for their SQS source queue with a redrive policy specifying maxReceiveCount of 5. What does this configuration mean?
A) The source queue itself will automatically delete after 5 total messages
B) After a message has been received (without being deleted) 5 times, SQS will move it to the DLQ instead of making it visible for further processing attempts
C) The DLQ will automatically delete messages after 5 minutes
D) Consumers are limited to polling the queue only 5 times total

25. Where is the maxReceiveCount setting for a dead-letter queue redrive policy actually configured?
A) On the dead-letter queue itself
B) On the source queue's redrive policy, which references the DLQ's ARN
C) On the consumer application's IAM role
D) In the AWS account's global SQS settings

26. A message has been moved to a dead-letter queue after repeated processing failures. After a developer identifies and fixes the bug that caused the failures, what is the term for the action of moving that message back to the original source queue for reprocessing?
A) Requeue
B) Redrive
C) Reflow
D) Reprocess-migrate

27. Is a dead-letter queue automatically created by AWS when a redrive policy is configured on a source queue?
A) Yes, AWS provisions a dedicated DLQ resource type automatically
B) No, a DLQ is simply a normal SQS queue that a developer creates and then designates as the redrive target in the source queue's redrive policy
C) Yes, but only for FIFO queues
D) No, DLQs must be purchased as a separate AWS service

28. A developer wants a message sent to an SQS queue today to remain invisible to consumers for the next 10 minutes before becoming available for processing, without affecting other messages in the same queue. Which SQS capability supports this for an individual message on a Standard queue?
A) A queue-level DelaySeconds setting only, which cannot be overridden
B) A per-message DelaySeconds parameter on SendMessage, up to 15 minutes, overriding the queue default for that message
C) A dead-letter queue redrive policy
D) A FIFO message group ID

29. Which of the following is true regarding per-message delay timers on SQS FIFO queues?
A) FIFO queues support per-message delay timers identically to Standard queues
B) FIFO queues do not support per-message delay overrides; only a queue-level delay applies uniformly
C) FIFO queues have no delay capability whatsoever, queue-level or otherwise
D) Delay timers are only available for dead-letter queues

30. A consumer application repeatedly fails to process a specific malformed message, and after several redelivery attempts it is moved to the queue's DLQ. What is the primary architectural benefit of this behavior?
A) It permanently deletes the problematic data so it can never be inspected
B) It prevents a single "poison pill" message from blocking or endlessly looping the processing of the rest of the queue, while preserving the message for later inspection
C) It automatically fixes the bug that caused the processing failure
D) It converts the queue from Standard to FIFO

31. Besides SQS-level dead-letter queues, Lambda functions consuming from an SQS event source mapping have their own separate concept for handling invocation failures. What is this typically called?
A) A visibility timeout override
B) An on-failure destination (which can itself be SQS, SNS, or EventBridge), configured on the Lambda function or event source mapping
C) A FIFO conversion policy
D) A Kinesis checkpoint

32. What is the maximum visibility timeout SQS supports, and why does this matter when selecting a value?
A) 30 seconds maximum; consumers must always complete work within 30 seconds
B) 12 hours maximum; it should be set comfortably above the worst-case processing time for a message to avoid premature redelivery
C) There is no maximum; it can be set to any value
D) 5 minutes maximum, matching the FIFO deduplication interval

33. A message attribute is attached to an SQS message separately from the message body. Which of the following is an accurate description of message attributes?
A) They are limited to a single attribute per message and cannot be typed
B) They are structured key-value metadata (up to 10 per message, typed as String, Number, or Binary) usable for routing/filtering decisions without parsing the message body
C) They replace the need for a message body entirely
D) They are only usable on FIFO queues

34. Which two of the following statements about SQS visibility timeout are accurate? (Select TWO)
A) If a consumer deletes the message before the visibility timeout expires, it will not be redelivered
B) A consumer can extend an in-progress message's invisibility period using ChangeMessageVisibility
C) The visibility timeout applies globally to all queues in an account and cannot be set per queue
D) Visibility timeout has no effect on whether a message can be redelivered
E) Visibility timeout is only configurable on FIFO queues

35. A team wants to reduce the operational risk of one malformed message causing an infinite retry loop that starves the rest of their SQS-based processing pipeline. Which configuration most directly addresses this?
A) Reducing the queue's visibility timeout to 1 second
B) Configuring a dead-letter queue with an appropriate maxReceiveCount so problematic messages are quarantined after a bounded number of attempts
C) Switching to short polling
D) Increasing the number of shards on the queue

36. Which combination of SQS features together supports the pattern of "buffer a burst of producer traffic so a slower downstream consumer isn't overwhelmed, quarantine messages that repeatedly fail, and minimize polling cost"? (Select TWO)
A) Long polling for cost/latency-efficient consumption, combined with a dead-letter queue with a bounded maxReceiveCount for quarantining failures
B) A FIFO queue is mandatory for any buffering use case
C) Message attributes alone solve buffering without a queue
D) Increasing the visibility timeout to the maximum in all cases regardless of processing time
E) Kinesis shards must be used instead of SQS for any buffering scenario

37. A team's SQS consumer is scaled to zero during low-traffic periods and resumes polling every few minutes using short polling. What operational downside does this design have compared to using long polling with a continuously running consumer?
A) Short polling is not compatible with any consumer scaling strategy
B) Messages may sit unprocessed for up to the full polling interval even though long polling could reduce that latency and the number of wasted empty-response API calls if the consumer polled continuously
C) Short polling causes automatic message loss after 30 seconds
D) Short polling is only usable with FIFO queues

38. A company's support team keeps receiving reports of "lost" messages that were, in fact, successfully processed but the consumer crashed immediately after processing and before calling DeleteMessage, causing SQS to redeliver the message once the visibility timeout expired, resulting in duplicate (not lost) processing. Which architectural principle would have prevented the duplicate processing from causing customer-visible harm?
A) Reducing the number of consumers to exactly one
B) Making the downstream processing operation idempotent so that a redelivered, already-completed message has no additional effect
C) Disabling the DeleteMessage API entirely
D) Switching the visibility timeout to zero

### SNS Pub/Sub, Subscription Types & the SQS Fanout Pattern (39–56)

39. What is the fundamental publish/subscribe behavior of an SNS topic when a single message is published to it?
A) Only the first subscriber to poll receives the message; it is then deleted for all others
B) SNS fans the single published message out to every current subscriber of the topic in parallel, without the publisher needing to know who or how many subscribers exist
C) SNS stores the message indefinitely until a subscriber requests it
D) SNS requires each subscriber to individually poll and pull the message, similar to SQS

40. Which of the following is NOT a valid SNS subscription type?
A) Amazon SQS
B) AWS Lambda
C) HTTP/HTTPS endpoint
D) Amazon RDS database table

41. A company wants a single application event to simultaneously trigger an order-fulfillment Lambda function, land in a durable queue for a slower analytics pipeline, and send an email confirmation to an internal team, all from one publish action. Which AWS service is designed for this fanout pattern?
A) Amazon SQS alone, using three separate queues the publisher writes to individually
B) Amazon SNS, publishing once to a topic with three different subscriptions (Lambda, SQS, and email)
C) Amazon Kinesis Data Streams exclusively
D) AWS Step Functions exclusively

42. In the SNS + SQS fanout pattern, why is an SQS queue commonly placed between an SNS topic and a downstream consumer, rather than subscribing the consumer's Lambda function or HTTP endpoint directly to the topic?
A) SNS cannot deliver messages to Lambda or HTTP endpoints under any circumstance
B) The SQS queue provides durability and buffering for that specific subscriber — if the consumer is temporarily unavailable or slow, messages persist in the queue rather than potentially being lost, which a raw HTTP subscriber without a queue would not guarantee
C) SQS queues are required by SNS as a technical prerequisite for any subscription
D) SQS queues automatically encrypt messages while direct Lambda subscriptions cannot be encrypted

43. A single SNS topic has three independent subscriptions: an SQS queue for order fulfillment, an SQS queue for the data warehouse, and a Lambda function for real-time fraud scoring. If the fraud-scoring Lambda function begins throwing errors on every invocation, what happens to the other two subscriptions?
A) The entire topic is disabled until the Lambda function is fixed
B) The other two subscriptions continue receiving their fanned-out copy of every published message independently, since each subscription operates independently of the others
C) SNS automatically unsubscribes the failing Lambda function permanently
D) The fulfillment and data warehouse queues stop receiving messages until the Lambda function's errors are resolved

44. Which of the following subscription protocols would be appropriate for sending a human-readable notification of a critical system alert directly to an on-call engineer's phone as a text message?
A) SQS
B) SMS
C) Lambda
D) Kinesis Data Firehose

45. A company wants to stream every message published to an SNS topic directly into a Kinesis Data Firehose delivery stream for eventual archival in S3, without writing custom subscriber code. Which SNS capability supports this?
A) SNS cannot integrate with Kinesis Data Firehose in any way
B) A native SNS subscription type that delivers directly to a Kinesis Data Firehose delivery stream
C) SNS requires an intermediate Lambda function to bridge to Firehose in all cases
D) This is only possible using EventBridge, not SNS

46. A publisher application calls the SNS Publish API once. How many times does that publish operation need to be called if the topic currently has ten different subscriptions across various protocol types?
A) Ten times, once per subscription
B) Once — SNS handles delivering the message to all ten subscriptions from that single publish call
C) It depends on which protocol each subscription uses
D) SNS does not support more than five subscriptions per topic

47. Which of the following statements about SNS topics and subscriptions is accurate?
A) A publisher must know the identity of every subscriber before publishing
B) New subscribers can be added to a topic later without requiring any changes to the publisher's code
C) A topic can have, at most, one subscription of each protocol type
D) Subscribers must poll SNS directly to receive messages, similar to SQS consumers

48. A team is deciding whether to have their web application publish order events directly to three separate SQS queues (one per downstream team) versus publishing once to an SNS topic with three SQS subscriptions. Which two advantages does the SNS-based fanout approach provide over direct multi-queue publishing? (Select TWO)
A) The publisher only needs a single publish call and does not need to be modified when a new subscriber team is added later
B) SNS eliminates the need for any downstream team to use SQS at all
C) Adding a fourth downstream team later requires only a new subscription, not a change to the publisher's code
D) SNS automatically guarantees exactly-once delivery to all three queues regardless of queue type
E) SNS removes the need for IAM permissions on the queues entirely

49. Which SNS subscription type would allow a legacy on-premises system, exposed via a public HTTPS endpoint, to receive a webhook-style push notification whenever a message is published to a topic?
A) SQS
B) HTTP/HTTPS
C) Kinesis Data Streams
D) DynamoDB Streams

50. A mobile application development team wants to send push notifications to iOS and Android devices when specific events occur in their backend. Which SNS capability is designed for this?
A) SNS mobile push notifications via platform application endpoints (e.g., APNs, FCM)
B) SNS SMS delivery, since mobile devices only support SMS
C) SNS does not support mobile push notifications; only email is supported
D) A direct Kinesis Data Streams subscription to the mobile device

51. Which two of the following are accurate statements about the SNS + SQS fanout pattern? (Select TWO)
A) It allows multiple independent consumer groups to each receive a durable, independently-buffered copy of every published message they subscribe to
B) It requires each SQS queue to be manually polled by the SNS service on a fixed schedule chosen by the administrator
C) New consumer groups can be added by creating a new SQS queue and subscribing it to the existing topic, without modifying the publisher
D) It is only possible when all subscribing queues are FIFO queues
E) SNS cannot fan out to more than one SQS queue simultaneously

52. A team currently has an application directly calling a downstream HTTP webhook synchronously whenever an order event occurs, and this design has caused cascading failures when the webhook endpoint is briefly down. Which architectural change using SNS and SQS would improve resilience?
A) Publish the event to an SNS topic with an SQS queue subscription, and have a separate worker process poll that queue and call the webhook with its own retry logic, decoupling the publisher from the webhook's availability
B) Continue calling the webhook synchronously but add more application servers
C) Replace the webhook call with a direct database write with no messaging service involved
D) Increase the webhook's timeout value to 60 seconds

53. Which of the following correctly distinguishes what happens if an SNS topic has zero subscribers when a message is published to it?
A) SNS returns an error and refuses to accept the publish
B) The publish succeeds, but since there are no subscribers, no delivery occurs for that message — new subscribers added afterward do not retroactively receive previously published messages
C) SNS automatically creates a default subscriber
D) The message is stored indefinitely until a subscriber is added, then delivered

54. A company wants email notifications sent to a distribution list whenever a specific business event occurs, without writing any custom subscriber application code. Which SNS subscription type most directly supports this with zero custom code?
A) HTTP/HTTPS
B) Email or Email-JSON subscription
C) Lambda
D) SQS

55. Which two of the following are valid SNS subscriber types that a message published to a topic could be delivered to? (Select TWO)
A) An AWS Lambda function
B) An Amazon SQS queue
C) An Amazon EBS volume
D) An Amazon Route 53 hosted zone
E) A CloudFormation stack

56. A publisher service needs to notify five different downstream systems of the same event, where three subscribers need durable, retriable delivery (best served by SQS) and two subscribers need immediate, low-latency push delivery (best served by Lambda). Which single-topic design supports both delivery needs simultaneously from one publish call?
A) An SNS topic with three SQS subscriptions and two Lambda subscriptions
B) Five separate SNS topics, each with a single subscription
C) A single SQS queue polled by all five systems
D) A Kinesis Data Stream with five shards, one per subscriber

### SNS Filter Policies & Messaging Cost Optimization (57–70)

57. A publisher sends messages to a shared SNS topic tagging each with a message attribute named event_type. A subscription's filter policy is set to {"event_type": ["order_shipped"]}. What happens when a message with event_type set to "order_created" is published to the topic?
A) The subscriber receives the message anyway, since filter policies are advisory only
B) SNS does not deliver that message to this subscription, since it does not match the filter policy, while other subscriptions without this filter (or with a matching filter) may still receive it
C) The publish call fails outright
D) The message is automatically converted to have event_type "order_shipped"

58. What is the primary cost/traffic optimization benefit of using SNS subscription filter policies, as tested under Domain 4 (Troubleshooting and Optimization)?
A) Filter policies reduce the size of the SNS topic's storage footprint
B) Filter policies cause SNS to discard non-matching messages before delivery, preventing subscribers from receiving and having to process/discard irrelevant messages themselves, which reduces wasted invocations, polling cycles, and processing cost
C) Filter policies eliminate the need for IAM permissions on subscribers
D) Filter policies automatically compress message bodies to reduce data transfer costs

59. At what level is an SNS filter policy configured?
A) On the topic itself, applying identically to every subscriber
B) On an individual subscription, allowing different subscribers to the same topic to receive different filtered subsets of published messages
C) On the publisher's IAM role
D) On the SQS queue, independent of SNS entirely

60. By default, what does an SNS filter policy match against?
A) The full message body text only
B) Message attributes attached to the published message (message-body filtering is also available as a separate, newer capability)
C) The publisher's IAM user name
D) The subscriber's AWS account ID only

61. A company has three subscribers to a single SNS topic: one needs only messages where order_value is 100 or greater, one needs only "order_cancelled" events, and one needs every message with no filtering. Which SNS capability allows this differentiated delivery from a single topic without modifying the publisher?
A) Three separate topics must be created, since one topic cannot support differentiated delivery
B) Per-subscription filter policies, using numeric and string matching, applied independently to each subscription
C) SNS delivers identically to all subscribers with no filtering capability
D) The publisher must send three separate messages, one per intended subscriber

62. Before a company implemented SNS filter policies, a finance-focused Lambda function that only cared about roughly 200 "refund" events per day was being invoked for all 50,000 daily events published to the topic, discarding the other 49,800 internally. After implementing a filter policy scoped to the Lambda's subscription, what is the expected operational effect?
A) No change; filter policies do not affect Lambda invocation counts
B) The Lambda function's invocation count drops to approximately the number of matching events (around 200/day), since SNS filters out non-matching messages before delivery rather than after
C) The Lambda function will now be invoked more often than before
D) The topic itself will be deleted and recreated

63. Which example correctly demonstrates SNS filter policy syntax for matching a numeric message attribute greater than or equal to a threshold?
A) {"order_value": {"gte": 100}}
B) {"order_value": [{"numeric": [">=", 100]}]}
C) {"order_value": ">=100"}
D) {"filter": "order_value >= 100"}

64. A subscription's filter policy is removed entirely (left unset). What is the resulting delivery behavior for that subscription?
A) The subscription receives no messages at all until a filter policy is added
B) The subscription receives every message published to the topic, since no filter policy means no filtering is applied
C) The subscription automatically inherits the filter policy of another subscription
D) SNS rejects publishes to topics with any subscription lacking a filter policy

65. Which two of the following are accurate statements about SNS subscription filter policies? (Select TWO)
A) They are evaluated per-subscription, so different subscribers to the same topic can receive different filtered subsets of the same published stream
B) They reduce unnecessary consumer-side processing and cost by filtering non-matching messages out before delivery
C) They must be identical across every subscription on a given topic
D) They can only match against the literal string "true" or "false"
E) They are configured on the SQS queue rather than the SNS subscription

66. A company wants to eliminate wasted SQS polling and Lambda invocation cost currently incurred because every subscriber to their SNS topic receives and then discards the vast majority of irrelevant messages in code. Which single change addresses this most directly, without altering the publisher?
A) Reduce the number of subscribers
B) Attach an appropriately scoped filter policy to each subscription based on the message attributes each subscriber actually needs
C) Switch the topic to a FIFO SNS topic with no other changes
D) Increase the SQS visibility timeout on each subscribing queue

67. Which of the following filter policy examples would match messages where a region attribute is anything other than "test-region"?
A) {"region": ["test-region"]}
B) {"region": [{"anything-but": "test-region"}]}
C) {"region": {"not": "test-region"}}
D) {"region": "!test-region"}

68. A developer configures a filter policy on a subscription but publishes messages without including the attribute the filter policy checks. What is the resulting behavior for that subscription, by default?
A) The message is always delivered, since a missing attribute is treated as an automatic match
B) The message does not match the filter policy and is not delivered to that subscription, since the referenced attribute is absent
C) SNS raises a publish-time error requiring the attribute to be present
D) The subscription is automatically disabled

69. Which two of the following scenarios are well-suited to SNS filter policies as the correct optimization mechanism, rather than requiring a code change in the subscriber? (Select TWO)
A) A subscriber only cares about a specific subset of event types published to a shared topic and currently discards the rest in its own code
B) A subscriber wants to permanently change the structure of the message body before it is delivered
C) A subscriber only cares about numeric threshold-based events (e.g., order_value >= 100) out of a broader published stream
D) A subscriber wants to encrypt messages at rest using its own KMS key
E) A subscriber wants to change which AWS Region the topic is hosted in

70. A company's monthly Lambda bill unexpectedly spikes because a function subscribed to a busy SNS topic is invoked for every message, even though it only acts on less than 1% of them. Which fix most directly reduces both cost and unnecessary invocations without changing the function's code?
A) Rewrite the Lambda function in a faster runtime
B) Apply a subscription filter policy scoped to the specific message attributes the function actually needs to act on
C) Increase the Lambda function's memory allocation
D) Move the function's logic into the SNS topic's resource policy

### Amazon EventBridge (71–92)

71. What is the default event bus that every AWS account automatically has available, without any setup?
A) The custom event bus
B) The partner event bus
C) The default event bus, which receives events from many AWS services natively
D) The Kinesis event bus

72. A company wants to isolate their own application's custom business events from the higher-volume stream of native AWS service events, to keep rule matching simpler and more scoped. Which EventBridge resource should they create?
A) A partner event bus
B) A custom event bus dedicated to their application's events
C) A new AWS account
D) A second default event bus

73. Which EventBridge resource type allows an AWS account to receive events directly from an integrated SaaS vendor (such as a monitoring or support-ticketing platform) without building a custom webhook receiver?
A) A custom event bus
B) A partner event bus
C) An SQS-backed event bus
D) A Kinesis event bus

74. What two components does an EventBridge rule require in order to route matching events? (Select TWO)
A) An event pattern describing which events the rule should match
B) At least one target that the matching event should be sent to
C) A VPC endpoint policy
D) A Kinesis shard ID
E) An IAM user with console access

75. A developer wants an EventBridge rule to trigger a Lambda function every day at exactly 12:00 UTC, on a fixed calendar schedule. Which expression type should the schedule use?
A) A rate() expression, since it supports exact calendar timing
B) A cron() expression, such as cron(0 12 * * ? *)
C) An event pattern matching a scheduled-event source
D) A Kinesis shard iterator

76. Which of the following is a valid EventBridge rate() expression for triggering a target every 5 minutes?
A) rate(5 minutes)
B) cron(5 minutes)
C) every(5, minutes)
D) schedule(5m)

77. A company wants to reprocess a set of application events that were published to a custom EventBridge bus last week, after fixing a bug in the downstream Lambda function that originally failed to handle them correctly. Which EventBridge capability supports this without asking the original producer to resend the events?
A) EventBridge archive and replay, assuming the relevant events were archived
B) A FIFO SQS redrive policy
C) A Kinesis Data Analytics query
D) SNS message retention

78. Which of the following can serve as a target for an EventBridge rule?
A) Only AWS Lambda functions
B) Lambda functions, SQS queues, SNS topics, Step Functions state machines, Kinesis streams, and 20+ other target types
C) Only Amazon S3 buckets
D) Only another AWS account's root user

79. A team wants to route events based on rich content within the event body — for example, only matching events where a nested "detail.state" field equals "CANCELLED" and a nested "detail.amount" field exceeds 500 — to a specific Lambda target. Which EventBridge capability enables this content-based routing?
A) A rate() expression
B) An event pattern with nested field matching, including numeric comparison operators
C) An SQS message attribute filter
D) A Kinesis partition key

80. What is EventBridge Pipes designed to simplify, compared to a full bus/rule/target setup?
A) Connecting one specific source (such as an SQS queue, DynamoDB stream, or Kinesis stream) directly to one specific target, with optional filtering and an optional enrichment step in between, without needing a separate bus and rule
B) Replacing SNS entirely for all pub/sub use cases
C) Providing a dedicated compute runtime that replaces Lambda
D) Automatically converting Standard SQS queues into FIFO queues

81. Which of the following event sources can natively publish events onto an AWS account's default EventBridge bus with zero developer setup?
A) Only custom application code explicitly configured to do so
B) Many native AWS services (such as EC2 state changes or CodePipeline stage changes), which publish events to the default bus automatically
C) Only Amazon S3
D) Only Lambda functions with a specific IAM permission

82. A company wants to trigger a nightly data-cleanup Lambda function at 2:00 AM UTC without maintaining a dedicated cron server or EC2 instance. Which approach is the modern, serverless-appropriate solution?
A) An EventBridge scheduled rule using a cron() expression targeting the Lambda function
B) A permanently running EC2 instance with a crontab entry
C) A Standard SQS queue with a 24-hour delay
D) An SNS topic subscribed via email, manually triggered each night

83. Which of the following correctly distinguishes EventBridge from SNS in terms of typical source variety?
A) SNS natively integrates with 200+ AWS services out of the box, while EventBridge does not
B) EventBridge natively integrates with a very wide range of AWS services and SaaS partners in addition to custom application events, while SNS is primarily built for publishing from your own application
C) Both services have identical native source integrations
D) Neither service integrates natively with any AWS service

84. A company needs to route different types of structured application events (e.g., OrderCreated, OrderCancelled, InventoryLow) from multiple internal microservices to different targets based on the event's type and content, with some events also needing to reach a partner SaaS analytics platform. Which service is best suited as the central routing layer for this scenario?
A) A single SQS Standard queue shared by all event types
B) Amazon EventBridge, using event patterns on a custom bus to route by event type/content, potentially alongside a partner event bus integration
C) A single SNS topic with no filtering, letting every subscriber discard irrelevant events itself
D) Amazon Athena

85. Which two of the following are accurate about EventBridge archive and replay? (Select TWO)
A) Archived events can be replayed back onto a bus within a specified time window
B) Retention for an archive can be set to a defined period or kept indefinitely
C) Replay requires the original producer application to resend every event manually
D) Archive and replay are only available for the default event bus, never custom buses
E) Replay permanently deletes the archived copy of each event once replayed

86. A rule on an EventBridge custom bus has the following event pattern: {"source": ["myapp.orders"], "detail-type": ["OrderStateChange"], "detail": {"state": ["CANCELLED"]}}. Which of the following incoming events would this rule match?
A) An event with source "myapp.orders", detail-type "OrderStateChange", and detail.state "SHIPPED"
B) An event with source "myapp.orders", detail-type "OrderStateChange", and detail.state "CANCELLED"
C) An event with source "myapp.inventory", detail-type "OrderStateChange", and detail.state "CANCELLED"
D) An event with source "myapp.orders", detail-type "InventoryChange", and detail.state "CANCELLED"

87. Which statement best summarizes when EventBridge is preferred over SNS for a routing scenario?
A) When the scenario involves routing based on the structured content of many different event types from many different sources, including native AWS service events, SaaS partner events, or scheduled triggers
B) When the scenario is a simple one-to-many fanout of a custom application message to email, SMS, and SQS subscribers with no content-based routing needed
C) EventBridge should always be preferred regardless of scenario, since it can fully replace SNS
D) EventBridge cannot integrate with Lambda, unlike SNS

88. A rule's target invocation fails repeatedly (for example, the target Lambda function is throttled). What is the general behavior for handling this kind of target delivery failure on an EventBridge rule?
A) EventBridge silently drops the event permanently with no retry or failure-handling options
B) EventBridge supports retry policies and can be configured with a dead-letter queue for a rule's target to capture events that fail after retries are exhausted
C) The entire event bus is disabled until manually re-enabled
D) EventBridge automatically deletes the failing target

89. Which two of the following are valid uses of EventBridge scheduled rules? (Select TWO)
A) Triggering a Lambda function every hour using a rate(1 hour) expression
B) Triggering a target at a specific calendar time daily using a cron() expression
C) Filtering messages based on SNS message attributes
D) Guaranteeing exactly-once delivery semantics identical to SQS FIFO
E) Providing a managed SQL query engine over a Kinesis stream

90. A company integrates a third-party incident-management SaaS platform so that whenever an incident is created in that external tool, a corresponding event appears in the company's AWS account for automated routing. Which EventBridge concept most directly names this integration point?
A) A custom event bus created entirely by the company
B) A partner event bus, provisioned as part of the SaaS integration
C) An SQS dead-letter queue
D) A Kinesis Data Analytics application

91. Compared to SQS, is an EventBridge bus by itself considered a durable, replayable data store for arbitrary time periods without extra configuration?
A) Yes, EventBridge buses retain all events indefinitely by default with no configuration needed
B) Not by itself — durability/replay requires explicitly configuring archive and replay, or routing to a durable downstream target like SQS; the bus itself is primarily a routing mechanism, not a default long-term store
C) Yes, but only for FIFO-configured event buses
D) EventBridge cannot be combined with SQS as a target under any circumstance

92. A retail company wants: (1) every native AWS CodePipeline stage-change event routed to a Slack-notification Lambda, (2) custom "InventoryLow" events from their own microservice routed to a restocking Lambda, and (3) a nightly cleanup job triggered on a fixed schedule — all managed through one consistent routing mechanism. Which service most directly supports all three requirements together?
A) Amazon SQS, using three separate queues
B) Amazon EventBridge, using rules on the default bus for the native events, a custom bus (or the default bus) with an event pattern for the custom events, and a scheduled rule for the nightly job
C) Amazon SNS, using a single unfiltered topic
D) AWS Direct Connect

### Amazon Kinesis: Data Streams (93–108)

93. What is the base unit of throughput capacity in an Amazon Kinesis Data Stream?
A) A partition
B) A shard
C) A topic
D) A message group

94. In classic (shared-fan-out) mode, what is the approximate write throughput limit per shard in a Kinesis Data Stream?
A) 1 MB/sec or 1,000 records/sec
B) 10 MB/sec or 10,000 records/sec
C) 100 KB/sec or 100 records/sec
D) Unlimited, bounded only by account-level quotas

95. What role does a Kinesis Data Streams partition key play?
A) It encrypts the record body
B) It determines which shard a given record is routed to, and records sharing the same partition key stay ordered within that shard
C) It sets the record's retention period individually
D) It defines the IAM permissions required to read that record

96. A team notices that one shard in their Kinesis Data Stream is consistently near its throughput limit while other shards in the same stream sit mostly idle, even though total account-level throughput needs are well within the stream's overall provisioned capacity. What is the most likely root cause?
A) The stream's retention period is set too low
B) An uneven or low-cardinality partition key choice is routing a disproportionate share of records to a single shard, creating a "hot shard"
C) Kinesis Data Streams cannot have more than one shard active at a time
D) The consumer is using long polling incorrectly

97. Which AWS-provided library is designed to simplify building a custom Kinesis Data Streams consumer, handling shard discovery, checkpointing, and load balancing across multiple consumer instances automatically?
A) The Kinesis Client Library (KCL)
B) The AWS SDK for S3
C) The Systems Manager Agent
D) The Kinesis Producer Library (KPL), which is consumer-side only

98. What is the default data retention period for a Kinesis Data Stream, and what is the maximum it can be extended to?
A) Default 24 hours, extendable up to 365 days
B) Default 7 days, extendable up to 30 days
C) Default 1 hour, extendable up to 24 hours
D) Default 30 days, with no ability to extend further

99. Why does Kinesis Data Streams' retention window matter for enabling "replay" of stream data, in a way that SQS fundamentally cannot support once a message has been consumed?
A) SQS also supports full replay identically to Kinesis
B) A Kinesis record remains available for any consumer to re-read at any position within the retention window, whereas an SQS message is deleted once a consumer successfully processes and deletes it, with no mechanism to re-read it afterward
C) Kinesis retention has no bearing on replay capability
D) Replay in Kinesis requires deleting and recreating the stream every time

100. A media company wants three independent applications — real-time fraud detection, a live dashboard, and nightly batch archival — to each read the full, same set of clickstream events independently, at their own pace, with the ability for any one of them to recover and re-read recent data if it falls behind or fails. Which Kinesis Data Streams characteristic directly supports this requirement?
A) Its ability to support multiple independent consumers each tracking their own read position against the same underlying stream data, within the retention window
B) Its requirement that only one consumer may read from the stream at any given time
C) Its automatic deletion of records immediately after the first consumer reads them
D) Its lack of any retention period

101. Which of the following is a valid way for a Lambda function to consume records from a Kinesis Data Stream?
A) Lambda cannot consume from Kinesis Data Streams under any configuration
B) Via an event source mapping, similar in concept to SQS, where Lambda's poller reads shard iterators and invokes the function with batches of records
C) Only via a manually configured API Gateway proxy in front of the stream
D) Only by first exporting the stream's data to S3

102. A producer application needs to write records to a Kinesis Data Stream. Which of the following are legitimate producer options? (Select TWO)
A) The Kinesis Producer Library (KPL)
B) The AWS SDK's PutRecord/PutRecords API calls
C) An SNS filter policy
D) An SQS visibility timeout extension
E) An EventBridge archive

103. What does Kinesis Data Streams On-Demand capacity mode provide, compared to manually provisioned shard mode?
A) Automatic scaling of stream capacity without the developer manually managing or resizing shard counts
B) A permanently fixed number of shards that can never change
C) Unlimited free throughput with no billing implications
D) Elimination of the need for any consumer application

104. Which statement accurately reflects why Kinesis Data Streams, rather than SQS, is the appropriate choice for a scenario requiring strict ordering across a high-volume stream while supporting multiple independently-scaling downstream analytics consumers reading the same data?
A) SQS FIFO queues cannot be read by more than one consumer type, and even Standard SQS deletes messages upon consumption, preventing multiple independent full reads of the same data — Kinesis retains records for replay by multiple independent consumers within its retention window
B) SQS and Kinesis are functionally identical for this use case
C) Kinesis cannot preserve ordering under any circumstance
D) SQS FIFO provides unlimited independent-consumer replay identical to Kinesis

105. In Kinesis Data Streams, what does "checkpointing" (typically handled by the Kinesis Client Library) refer to?
A) Encrypting records at rest
B) Tracking how far a given consumer application has read within a shard, so it can resume from the correct position after a restart or failure
C) Deleting records once read by any consumer
D) Setting the shard's throughput limit

106. A poorly chosen Kinesis partition key uses a constant literal value for every record regardless of the record's actual content. What is the most likely consequence?
A) Every record is routed to the same single shard, creating a severe hot-shard bottleneck regardless of how many shards the stream has
B) Records are evenly distributed across all shards automatically regardless of partition key value
C) This has no effect on shard distribution
D) The stream automatically rejects records with a constant partition key

107. Which two of the following are true about Kinesis Data Streams consumers? (Select TWO)
A) Multiple independent consumer applications can read the same stream data concurrently, each maintaining its own position
B) A record is permanently deleted from the stream as soon as any single consumer reads it
C) Consumers can use the Kinesis Client Library to handle shard discovery and checkpointing automatically
D) Only one consumer application may ever be attached to a given stream
E) Kinesis Data Streams has no concept of consumer read position

108. A stream architecture needs a producer to write IoT sensor telemetry at high volume, with strict per-device ordering (all readings from the same device processed in the order they were generated) while allowing several independent downstream systems to each process the full stream. Which partition key strategy best achieves the per-device ordering requirement?
A) A constant partition key shared by every device
B) A randomly generated partition key on every record, unrelated to the device
C) The device ID used as the partition key, ensuring all of a given device's records land on and stay ordered within the same shard
D) No partition key at all, since Kinesis does not use partition keys

### Kinesis Data Firehose & Data Analytics (109–122)

109. What best describes the core function of Amazon Kinesis Data Firehose?
A) A fully managed delivery service that buffers and delivers streaming data near-real-time to fixed destinations such as S3, Redshift, or OpenSearch Service, without requiring shard management
B) A raw, low-level shard-based streaming storage service identical to Kinesis Data Streams
C) A relational database service for transactional workloads
D) A service exclusively for running ad-hoc SQL queries against S3 data

110. Which of the following is NOT a native delivery destination for Kinesis Data Firehose?
A) Amazon S3
B) Amazon Redshift
C) Amazon OpenSearch Service
D) Amazon DynamoDB as a direct native destination for streamed records

111. A team needs to transform incoming JSON records into Parquet format and enrich each record with an additional computed field before Firehose delivers them to S3. Which Firehose capability supports this?
A) Firehose cannot transform data in any way; only raw pass-through delivery is supported
B) An inline data transformation step using an attached Lambda function, invoked by Firehose before delivery
C) A Kinesis Data Streams partition key change
D) An SNS filter policy applied to the delivery stream

112. Which statement accurately contrasts the operational overhead of Kinesis Data Streams versus Kinesis Data Firehose?
A) Both require identical manual shard management
B) Data Streams requires the developer to manage shard count/scaling (or use On-Demand mode) and write custom consumer logic; Firehose is fully managed, auto-scales, and delivers directly to fixed destinations with no shard management or custom consumer code required
C) Firehose requires more manual operational management than Data Streams
D) Neither service requires any configuration whatsoever

113. A company wants streaming clickstream data delivered reliably into S3 for later batch analysis, with minimal custom code and no desire to manage stream shard capacity themselves. Which Kinesis service best fits this specific requirement?
A) Kinesis Data Streams with a custom KCL consumer
B) Kinesis Data Firehose, configured with S3 as the destination
C) Kinesis Data Analytics alone, with no delivery destination
D) Amazon Athena, since it can ingest streaming data directly

114. What is the typical minimum buffering interval characteristic of Kinesis Data Firehose before it delivers buffered records to its destination, making it "near-real-time" rather than instantaneous?
A) Firehose delivers every record with zero buffering delay, identical to Data Streams
B) Firehose buffers by size or time interval (with a minimum around 60 seconds, configurable higher) before flushing to the destination
C) Firehose buffers for exactly 24 hours before every delivery
D) Firehose has no buffering mechanism at all

115. Which AWS capability allows a developer to run continuous SQL or Apache Flink queries directly against a live Kinesis Data Stream or Firehose delivery stream, such as computing a rolling 5-minute average in real time?
A) Amazon Athena
B) Kinesis Data Analytics
C) Amazon OpenSearch Service
D) AWS Glue Data Catalog alone

116. A company currently has a Kinesis Data Analytics application computing a real-time aggregate over a Kinesis Data Stream. Which of the following accurately describes how Data Analytics relates to the underlying stream's storage?
A) Data Analytics maintains its own separate, independently retained copy of every record indefinitely
B) Data Analytics queries the source stream's data in real time and can output results to another stream/Firehose, but does not itself serve as the stream's durable storage layer
C) Data Analytics replaces the need for a Kinesis Data Stream entirely
D) Data Analytics can only run batch queries once every 24 hours

117. Which two of the following are accurate statements comparing Kinesis Data Streams to Kinesis Data Firehose? (Select TWO)
A) Data Streams supports replay/re-reading of data by multiple independent consumers within its retention window; Firehose does not retain a separately re-readable copy once delivered
B) Firehose requires the developer to provision and manage shard count manually
C) Data Streams is fully managed with automatic delivery to S3/Redshift/OpenSearch and no custom consumer code
D) Firehose supports inline Lambda-based transformation of records before delivery to its destination
E) Both services have an identical operational model with no meaningful difference

118. A company's security logs need to be delivered continuously into an OpenSearch Service domain for near-real-time search and dashboarding, with minimal custom ingestion code. Which Kinesis service is the most direct fit for this specific delivery requirement?
A) Kinesis Data Streams with a hand-written OpenSearch client consumer
B) Kinesis Data Firehose, configured with OpenSearch Service as its destination
C) Kinesis Data Analytics exclusively
D) Amazon Athena

119. Which of the following scenarios most clearly calls for Kinesis Data Firehose rather than Kinesis Data Streams?
A) A scenario requiring multiple independent consumer applications to each replay the last 7 days of raw event data at their own pace
B) A scenario requiring strict, application-managed shard-level consumer checkpointing for a custom real-time fraud-detection engine
C) A scenario simply requiring reliable, minimally-managed delivery of streaming data into S3 with light transformation, and no need to replay or have multiple independent readers of the raw stream
D) A scenario requiring records to be reprocessed by three separate custom-built consumer applications independently

120. What happens to a record once Kinesis Data Firehose has successfully delivered it to its configured destination (for example, S3)?
A) The record remains available for further independent reads by other consumer applications directly from Firehose, similar to Data Streams
B) Firehose itself does not retain a separately queryable copy of the record for other consumers; the delivered copy now lives at the destination (e.g., S3), which can itself be queried later, e.g., via Athena
C) The record is automatically deleted from S3 after delivery
D) Firehose converts the record into an SNS notification automatically

121. A retail company needs both (1) a durable stream that three independent applications can each replay from the last 48 hours, and (2) a simple, low-maintenance pipeline delivering the same data into S3 for occasional Athena queries. Which combination of Kinesis services addresses both needs together?
A) Kinesis Data Streams alone, with no Firehose involved for the S3 delivery need
B) Kinesis Data Firehose alone, since it also supports full independent replay
C) A Kinesis Data Stream (for the three replaying consumer applications) with a Kinesis Data Firehose consumer attached to the same stream, delivering to S3 for the Athena use case
D) Amazon SQS for both needs simultaneously

122. Which of the following is an accurate, developer-level summary distinguishing the three Kinesis family services?
A) Data Streams = you manage shards/consumers/replay; Firehose = fully managed delivery with no shard management; Data Analytics = real-time SQL/Flink queries over a stream
B) All three Kinesis services are functionally identical with different names
C) Firehose provides shard-based replay identical to Data Streams
D) Data Analytics is a raw storage layer with no query capability

### Kinesis vs. SQS vs. SNS vs. EventBridge — Integrative Decision Scenarios (123–130)

123. A team needs a simple task queue where each unit of work (a video-transcoding job) should be picked up and processed by exactly one worker, with no requirement for multiple independent consumers to see the same job or for historical jobs to be replayed. Which service is the most appropriately scoped choice?
A) Amazon Kinesis Data Streams, for its replay capability
B) Amazon SQS, since the workload is a straightforward decoupled work queue with single-consumer-group semantics
C) Amazon EventBridge, for its content-based routing
D) Amazon OpenSearch Service

124. A company's IoT platform ingests continuous sensor telemetry that must be (1) processed in real time by a fraud/anomaly detector, (2) simultaneously archived raw to S3 for compliance, and (3) independently fed into a live aggregation dashboard — all three consuming the same underlying data independently. Which service family is purpose-built for this multi-independent-consumer streaming requirement?
A) Amazon SQS Standard queues
B) Amazon Kinesis (Data Streams feeding independent consumers, potentially with Firehose for the S3 archival leg)
C) Amazon SNS with a single unfiltered topic
D) AWS Direct Connect

125. A scenario states: "Various internal microservices emit different structured event types; a scheduled nightly job must also run; and events from a third-party SaaS incident-management tool must be ingested and routed based on content." Which service most directly satisfies all three needs through one consistent mechanism?
A) Amazon SQS
B) Amazon EventBridge, using its content-based event patterns, scheduled rules, and partner event bus support
C) Amazon Kinesis Data Streams
D) Amazon Athena

126. A single application event must reach an email distribution list, an SMS number for on-call paging, and a durable SQS queue for later audit processing — all from one publish action, with no need for content-based routing across many different event sources. Which service is the best-scoped fit?
A) Amazon EventBridge, since it should always be preferred over SNS
B) Amazon SNS, publishing once to a topic with email, SMS, and SQS subscriptions
C) Amazon Kinesis Data Streams
D) Amazon Athena

127. Which service would NOT be an appropriate fit for a requirement stating "data must be replayable by multiple independently-scaling consumer applications, each reading the full stream at its own pace"?
A) Amazon Kinesis Data Streams
B) Amazon SQS, since a message is removed from visibility/deleted once a single consumer successfully processes it, preventing independent full replay by multiple separate consumer applications
C) A Kinesis Data Stream with multiple KCL-based consumer applications
D) Kinesis, generally, given its retention-window-based replay model

128. A company is deciding how to notify downstream systems of state changes to native AWS resources (such as an EC2 instance stopping) without writing any custom polling code to detect those changes. Which service natively publishes such AWS resource state-change events with no custom producer code required?
A) Amazon SQS
B) Amazon EventBridge's default event bus, which already receives many native AWS service events automatically
C) Amazon Kinesis Data Streams
D) Amazon Athena

129. Which two of the following statements correctly distinguish SQS from Kinesis Data Streams as decoupling mechanisms? (Select TWO)
A) SQS is best suited to a work-queue pattern where a message is processed once by one logical consumer group and then removed
B) Kinesis is best suited when multiple independent consumer applications need to replay and process the same data at their own pace
C) SQS supports unlimited historical replay identical to Kinesis
D) Kinesis cannot be consumed by more than one application under any circumstance
E) SQS and Kinesis are interchangeable in every scenario with no meaningful architectural difference

130. A scenario describes a requirement for "guaranteed ordering of commands issued against a single customer's account, with each command processed exactly once, and no need for multiple independent applications to replay the command history." Which service and configuration is the best fit, as opposed to a broader Kinesis-based design?
A) A Kinesis Data Stream with one shard per customer
B) An SQS FIFO queue, using the customer account ID as the message group ID
C) An SNS topic with no filtering
D) Amazon Athena querying S3 on a schedule

### Amazon Athena & Amazon OpenSearch Service (131–134)

131. What does Amazon Athena allow a developer to do with data already stored in Amazon S3?
A) Run standard SQL queries directly against the S3 data (e.g., CSV, JSON, Parquet) without provisioning a database cluster or loading the data elsewhere first
B) Automatically convert the S3 bucket into a relational database engine
C) Replace the need for S3 entirely by migrating the data into Athena's own storage
D) Provide real-time transactional writes directly into S3 objects

132. How is Amazon Athena typically billed?
A) A flat monthly subscription fee regardless of usage
B) Per query, based on the amount of data scanned — which is why using columnar formats like Parquet and partitioning the data can directly reduce cost
C) Per hour that a dedicated Athena cluster is running, whether or not queries are executed
D) Athena has no billing model; it is included free with any AWS account

133. A team wants to occasionally run ad-hoc SQL reports over application access logs that a Kinesis Data Firehose delivery stream has been landing in S3. Which AWS service is the natural fit for this occasional, serverless SQL analysis, without provisioning a dedicated database or Redshift cluster?
A) Amazon Athena
B) Amazon DynamoDB
C) AWS Direct Connect
D) Amazon Route 53

134. A platform team wants to centralize log output from many microservices into one place where engineers can run near-real-time full-text search and view operational dashboards during an incident. Which AWS service is most directly suited to this developer-relevant log analytics and dashboarding use case, commonly fed via a Kinesis Data Firehose delivery stream?
A) Amazon Athena, exclusively
B) Amazon OpenSearch Service, including its Dashboards feature for visualization
C) Amazon Kinesis Data Streams, with no other service involved
D) AWS Direct Connect

---

## Answer Key & Explanations

1. B — Standard queues offer nearly unlimited throughput and are appropriate when strict ordering is not required.
2. B — FIFO queues, grouped by account ID as the message group, provide the ordering and deduplication this scenario requires.
3. B — Standard queues are at-least-once by design; the fix is idempotent consumer logic, not a queue "bug."
4. B — FIFO deduplication uses either content-based hashing or an explicit MessageDeduplicationId within a 5-minute window.
5. C — FIFO queue names must end in the literal ".fifo" suffix.
6. B — FIFO trades a lower throughput ceiling for strict ordering and exactly-once processing within its dedup window.
7. B — Idempotent processing logic is the robust, application-level defense against at-least-once duplicate delivery.
8. B — The message group ID scopes ordering guarantees; different groups may process in parallel with no cross-group ordering.
9. B — Sharding across multiple FIFO queues preserves per-account ordering while scaling beyond a single queue's throughput ceiling.
10. B — Standard queues provide at-least-once delivery and best-effort (not guaranteed) ordering.
11. A & B — Standard's higher throughput ceiling and the lack of any real benefit from FIFO ordering for independent jobs both favor Standard here.
12. B — The FIFO deduplication interval is 5 minutes.
13. B — Occasional reordering under load is expected, standard-queue behavior, not a bug, since Standard only makes a best effort at ordering.
14. C — Strict ordering plus guaranteed no-duplicate processing is exactly what FIFO queues are designed to provide.
15. B — Standard queues require no message group ID or deduplication ID from producers, unlike FIFO.
16. A & B — FIFO guarantees in-group ordering and exactly-once processing within its deduplication interval.
17. A & B — Idempotent inventory logic addresses duplicates directly; FIFO addresses it structurally if strict exactly-once/ordering is required for this operation.
18. A — Standard offers nearly unlimited throughput; FIFO caps out around 3,000 msg/sec batched (300 unbatched).
19. B — A processing time exceeding the default 30-second visibility timeout allows a second consumer to pick up and process the same message concurrently.
20. B — ChangeMessageVisibility extends the invisibility window for a message still being processed.
21. C — The maximum configurable SQS visibility timeout is 12 hours.
22. B — Long polling (WaitTimeSeconds 1–20) reduces empty responses, cutting cost and pickup latency.
23. B — Short polling does not necessarily query every server and can return empty even when messages exist.
24. B — After maxReceiveCount receipt attempts without deletion, SQS routes the message to the configured DLQ instead of redelivering it further.
25. B — maxReceiveCount is part of the source queue's redrive policy, referencing the DLQ's ARN.
26. B — "Redrive" is the term for moving DLQ messages back to the source queue for reprocessing.
27. B — A DLQ is just a normal SQS queue a developer creates and designates as the redrive target; it is not auto-provisioned.
28. B — SendMessage's per-message DelaySeconds (up to 15 minutes) overrides the queue default for that message on Standard queues.
29. B — FIFO queues support only a queue-level delay, not per-message delay overrides.
30. B — DLQs quarantine a repeatedly failing "poison pill" message so it can't block the rest of the queue, while preserving it for inspection.
31. B — Lambda's SQS event source mapping supports its own on-failure destination (SQS, SNS, or EventBridge), separate from the queue's own DLQ concept.
32. B — 12 hours is the maximum; it should exceed worst-case processing time to prevent premature redelivery.
33. B — Message attributes are typed, structured metadata (up to 10 per message) separate from the body.
34. A & B — Timely deletion prevents redelivery, and ChangeMessageVisibility lets a consumer extend an in-progress message's invisibility.
35. B — A DLQ with a bounded maxReceiveCount quarantines malformed messages instead of looping them indefinitely.
36. A — Long polling handles cost/latency-efficient buffering, and a bounded DLQ handles quarantining repeated failures.
37. B — Infrequent short-polling bursts can leave messages unprocessed longer and waste more empty-response calls than continuous long polling.
38. B — Idempotent downstream logic neutralizes the harm of a redelivered, already-completed message.
39. B — SNS fans a single published message out to every current subscriber in parallel, transparently to the publisher.
40. D — An RDS database table is not a valid SNS subscription protocol.
41. B — SNS publishing once to a topic with three heterogeneous subscriptions is exactly the fanout pattern described.
42. B — An SQS queue buffers messages durably for its specific subscriber, unlike a raw HTTP/Lambda subscription with no built-in durability.
43. B — Each subscription operates independently; one failing subscriber does not affect delivery to the others.
44. B — SMS is the subscription protocol for delivering a text message notification to a phone number.
45. B — SNS has a native subscription type delivering directly into a Kinesis Data Firehose delivery stream.
46. B — A single Publish call is fanned out by SNS to all subscriptions automatically.
47. B — New subscribers can be added later with zero publisher-side code changes.
48. A & C — A single publish call handles all current and future subscribers, and adding a new team only requires a new subscription, not publisher changes.
49. B — HTTP/HTTPS subscriptions deliver a webhook-style push to a public endpoint.
50. A — SNS mobile push uses platform application endpoints (APNs/FCM) for iOS/Android notifications.
51. A & C — Each subscriber gets its own durable buffered copy, and new consumer groups can subscribe without touching the publisher.
52. A — Decoupling via SNS+SQS with an independent worker and its own retry logic prevents webhook downtime from cascading back to the publisher.
53. B — The publish succeeds but is simply not delivered to any subscriber; new subscribers do not retroactively receive past messages.
54. B — Email/Email-JSON subscriptions deliver human-readable notifications with zero custom subscriber code.
55. A & B — Lambda functions and SQS queues are both valid SNS subscriber types; EBS volumes and Route 53 zones are not.
56. A — A single topic can mix SQS and Lambda subscriptions, satisfying both durable-retriable and low-latency-push needs from one publish call.
57. B — The non-matching message is filtered out for this subscription only; other subscriptions are unaffected by this one's filter policy.
58. B — Filtering discards non-matching messages before delivery, saving the subscriber the cost/effort of receiving and discarding them itself.
59. B — Filter policies are attached per-subscription, enabling differentiated delivery from one topic.
60. B — Filter policies match message attributes by default; message-body filtering is a separate, newer capability.
61. B — Independent per-subscription filter policies (numeric and string matching) enable this differentiated delivery from a single topic.
62. B — Filtering before delivery drops the Lambda's invocation count to roughly the matching subset, around 200/day.
63. B — SNS numeric filter syntax uses {"attribute": [{"numeric": [">=", 100]}]}.
64. B — No filter policy means the subscription receives every message published to the topic.
65. A & B — Filter policies are per-subscription (enabling differentiated delivery) and reduce consumer-side cost/processing by filtering before delivery.
66. B — Scoping each subscription's filter policy to what that subscriber actually needs eliminates the wasted delivery/processing without touching the publisher.
67. B — The "anything-but" operator matches any value except the specified one(s).
68. B — A message lacking the attribute the filter checks does not match and is not delivered to that subscription.
69. A & C — Both are content-based delivery-scoping needs that filter policies solve without any subscriber code change.
70. B — A filter policy scoped to the attributes the function needs stops SNS from invoking it for non-matching messages at all.
71. C — Every account has a default event bus that receives many native AWS service events automatically.
72. B — A custom event bus isolates an application's own events from the higher-volume default bus.
73. B — A partner event bus is the integration point for receiving events directly from an integrated SaaS partner.
74. A & B — A rule needs both an event pattern (or schedule) to match against and at least one target to invoke.
75. B — cron() expressions support exact calendar-based timing, such as a fixed daily time.
76. A — rate(5 minutes) is valid EventBridge rate syntax.
77. A — EventBridge archive and replay lets previously archived events be replayed onto a bus without producer involvement.
78. B — EventBridge rules support Lambda, SQS, SNS, Step Functions, Kinesis, and 20+ other target types.
79. B — Event patterns support nested field matching, including numeric comparison operators, for content-based routing.
80. A — Pipes simplifies wiring one specific source to one specific target with optional filtering/enrichment, without a full bus/rule setup.
81. B — Many native AWS services publish state-change events to the default bus automatically, with zero developer setup.
82. A — An EventBridge scheduled rule with a cron() expression targeting Lambda is the modern, serverless-appropriate nightly-job solution.
83. B — EventBridge's native source integration (AWS services + SaaS partners) is far broader than SNS, which is primarily for your own application's publishes.
84. B — EventBridge's content-based routing on a custom bus, plus optional partner bus integration, directly fits this multi-source, multi-target scenario.
85. A & B — Archived events can be replayed within a specified window, and archive retention can be time-bound or indefinite.
86. B — Only the event matching source, detail-type, and detail.state exactly as specified satisfies the pattern.
87. A — EventBridge fits scenarios needing content-based routing across many event types/sources, native AWS integration, or scheduling — not every scenario, contrary to option C.
88. B — EventBridge rules support retry policies and an optional dead-letter queue for a target's exhausted-retry failures.
89. A & B — Both rate() and cron() expressions are valid ways to define an EventBridge scheduled rule's trigger timing.
90. B — A partner event bus is the named integration point for a SaaS platform's events to appear in the account.
91. B — The bus itself is a routing mechanism; durable replay requires explicit archive/replay configuration or a durable downstream target.
92. B — EventBridge covers native AWS events, custom event routing, and scheduled rules all through one consistent rule-based mechanism.
93. B — A shard is the base throughput unit of a Kinesis Data Stream.
94. A — Each shard supports roughly 1 MB/sec or 1,000 records/sec of write throughput in classic mode.
95. B — The partition key determines shard routing, and same-key records stay ordered within that shard.
96. B — An uneven/low-cardinality partition key creates a hot shard even when overall provisioned capacity is sufficient.
97. A — The Kinesis Client Library (KCL) handles shard discovery, checkpointing, and load balancing for custom consumers.
98. A — Default retention is 24 hours, extendable up to 365 days.
99. B — Kinesis records remain re-readable within the retention window; SQS deletes a message once successfully consumed, with no replay mechanism.
100. A — Multiple independent consumers, each tracking their own position within the retention window, is the defining Kinesis Data Streams capability this requires.
101. B — Lambda consumes Kinesis via an event source mapping conceptually similar to SQS, reading shard iterators in batches.
102. A & B — The KPL and direct SDK PutRecord/PutRecords calls are both legitimate ways to write records to a stream.
103. A — On-Demand mode auto-scales stream capacity without manual shard management.
104. A — SQS's single-read/delete model prevents multiple independent full replays, while Kinesis retains records for exactly that purpose within its retention window.
105. B — Checkpointing tracks a consumer's read progress within a shard so it can resume correctly after a restart.
106. A — A constant partition key routes every record to the same shard, creating a severe bottleneck.
107. A & C — Multiple independent consumers can read the same data at their own pace, and KCL automates shard discovery/checkpointing.
108. C — Using the device ID as the partition key keeps each device's records ordered together on a single shard.
109. A — Firehose is a fully managed delivery service to fixed destinations, requiring no shard management.
110. D — DynamoDB is not one of Firehose's native delivery destinations (S3, Redshift, and OpenSearch Service are).
111. B — An attached Lambda function performs inline transformation before Firehose delivers the records.
112. B — Data Streams requires shard/consumer management; Firehose is fully managed with automatic delivery and no shard management.
113. B — Firehose configured with S3 as the destination directly fits this minimal-code, no-shard-management delivery need.
114. B — Firehose buffers by size or time (minimum around 60 seconds, configurable) before flushing to its destination.
115. B — Kinesis Data Analytics runs continuous SQL/Flink queries directly against a live stream.
116. B — Data Analytics queries the source stream in real time and can output elsewhere, but is not itself the stream's durable storage.
117. A & D — Data Streams supports multi-consumer replay that Firehose does not retain, and Firehose supports inline Lambda transformation before delivery.
118. B — Firehose configured with OpenSearch Service as the destination is the direct, minimal-code fit for this delivery need.
119. C — Simple, minimally-managed delivery into S3 with no replay/multi-reader need is Firehose's sweet spot.
120. B — Once delivered, the record lives at the destination (e.g., S3); Firehose itself doesn't retain a separately re-readable copy like Data Streams does.
121. C — A Data Stream serving the three replaying consumers, with a Firehose consumer also attached for S3/Athena delivery, satisfies both needs together.
122. A — Data Streams = self-managed shards/consumers/replay; Firehose = fully managed delivery; Data Analytics = real-time SQL/Flink over a stream.
123. B — A single-consumer-group work queue with no replay need is squarely SQS's use case.
124. B — Multiple independent consumers reading the same continuous telemetry data, with archival, is the Kinesis family's defining strength.
125. B — EventBridge's content-based patterns, scheduled rules, and partner bus support together cover all three stated needs.
126. B — A single SNS publish fanning out to email, SMS, and SQS subscriptions is the best-scoped fit with no content-based routing requirement.
127. B — SQS's consume-once/delete model does not support independent full replay by multiple separate consumer applications.
128. B — The default EventBridge bus already receives many native AWS resource state-change events automatically, with no custom producer code.
129. A & B — SQS fits a single-consumer-group work queue; Kinesis fits multiple independent consumers replaying the same data.
130. B — An SQS FIFO queue keyed by account ID as the message group ID directly provides ordering and exactly-once processing without needing Kinesis's broader replay model.
131. A — Athena runs standard SQL directly against S3 data with no cluster provisioning or data loading step.
132. B — Athena bills per query based on data scanned, making columnar formats and partitioning direct cost levers.
133. A — Athena is the natural serverless, ad-hoc SQL fit for occasional reporting over S3-resident log data.
134. B — OpenSearch Service (with Dashboards) is the developer-relevant fit for centralized near-real-time log search and operational dashboards.
