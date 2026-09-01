# Module 03 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Primary Keys & Table Design (1–16)

1. An e-commerce company is designing a DynamoDB table to store order data. Each order has a unique order ID, and the team needs to retrieve individual orders by ID. Which primary key design is the simplest fit?
A) A composite primary key with orderId as the partition key and orderStatus as the sort key
B) A simple primary key with orderId as the partition key
C) A composite primary key with orderStatus as the partition key and orderId as the sort key
D) A simple primary key with orderStatus as the partition key

2. A messaging application needs to store messages, where each message belongs to a conversation and has a timestamp. The most frequent access pattern is "retrieve all messages in a conversation, ordered by time." Which primary key design supports this pattern most efficiently?
A) A simple primary key with messageId as the partition key
B) A composite primary key with conversationId as the partition key and sentAt as the sort key
C) A simple primary key with sentAt as the partition key
D) A composite primary key with sentAt as the partition key and conversationId as the sort key

3. What is the maximum size of a single DynamoDB item, including all attribute names and values?
A) 1 MB
B) 400 KB
C) 64 KB
D) 4 GB

4. Which of the following is a valid DynamoDB data type?
A) BLOB (Binary Large Object) as a first-class type name
B) Map (a nested structure of key-value pairs, similar to JSON objects)
C) ARRAY (an ordered, indexed collection identical to SQL arrays)
D) DATETIME (a built-in timestamp type with timezone support)

5. A team designs a DynamoDB table with a composite primary key using customerId as the partition key and orderDate as the sort key. Which statement correctly describes how items with the same customerId are stored?
A) Items sharing the same partition key are distributed randomly across different physical partitions
B) Items sharing the same partition key are co-located on the same physical partition and sorted by their sort key value
C) Items sharing the same partition key are always stored in alphabetical order by attribute name
D) The sort key has no effect on physical storage or query ordering

6. An IoT platform stores sensor readings in DynamoDB with deviceId as the partition key and readingTimestamp as the sort key. Which of the following sort key conditions is valid in a Query operation against this table?
A) readingTimestamp LIKE '2026%'
B) readingTimestamp BETWEEN '2026-01-01' AND '2026-06-30'
C) readingTimestamp IN ('2026-01-01', '2026-02-01', '2026-03-01')
D) readingTimestamp IS NOT NULL

7. A developer creates a DynamoDB table with a simple primary key (partition key only). Two items are inserted with the same partition key value. What happens?
A) Both items coexist in the table with the same partition key value
B) The second PutItem silently overwrites the first, since the partition key is the entire primary key and must be unique
C) DynamoDB returns a ValidationException rejecting the duplicate
D) The second item is placed in a different partition automatically

8. Which two of the following attributes about DynamoDB's schema flexibility are accurate? (Select TWO.)
A) Only the primary key attributes are required to be declared at table creation time; other attributes can vary freely between items
B) Every item in a DynamoDB table must have exactly the same set of attributes
C) DynamoDB supports nested document types (Maps and Lists) as attribute values
D) All attributes in a DynamoDB item must be scalar values (String, Number, or Binary)
E) DynamoDB requires a fixed schema defined for all columns before any data can be written

9. A developer wants to store a JSON document with deeply nested objects and arrays as a single DynamoDB item attribute. Which DynamoDB data type supports this?
A) A String attribute containing the raw JSON as text (losing queryability of nested fields)
B) A Map attribute, which natively supports nested key-value structures including Lists within Maps
C) DynamoDB does not support any form of nested data within a single item
D) A Binary attribute only, with the application serializing the JSON to bytes

10. A table uses a composite primary key with userId as the partition key and action as the sort key. A developer wants to retrieve all items for a specific user. Which operation is most efficient?
A) A Scan with a FilterExpression on userId
B) A Query specifying only the partition key (userId), which returns all items for that user sorted by the sort key
C) A GetItem call without specifying the sort key
D) A BatchGetItem call with every possible action value listed

11. Can the primary key of a DynamoDB table be changed after the table is created?
A) Yes, by running an ALTER TABLE command
B) No, the primary key is immutable after table creation; changing it requires creating a new table with the desired key schema and migrating data
C) Yes, by disabling provisioned capacity temporarily
D) Yes, but only if the table is empty

12. A developer stores user session data in DynamoDB. Each session has a unique sessionId. The application's only access pattern is retrieving a single session by its sessionId. Which primary key design is the best fit?
A) A composite key with userId as the partition key and sessionId as the sort key
B) A simple key with sessionId as the partition key
C) A composite key with sessionId as the partition key and expirationTime as the sort key
D) A simple key with expirationTime as the partition key

13. A gaming application stores player scores with playerId as the partition key and gameId as the sort key. Which Query would retrieve all scores for a specific player in games whose IDs begin with "BATTLE-"?
A) A Query on playerId with a sort key condition begins_with(gameId, "BATTLE-")
B) A Scan filtering on playerId and gameId
C) A GetItem specifying only playerId
D) A Query using gameId as the partition key

14. Which two statements correctly describe the role of the partition key in DynamoDB? (Select TWO.)
A) DynamoDB hashes the partition key to determine which physical partition stores the item
B) The partition key determines the sort order of items within a partition
C) Items with the same partition key value are guaranteed to be stored on the same physical partition
D) The partition key is optional and can be omitted from individual items
E) The partition key must be a Number type

15. A table has a composite primary key with orderId as the partition key and lineItemId as the sort key. A developer needs to delete a specific line item. What key information must be provided to the DeleteItem call?
A) Only the orderId
B) Both the orderId (partition key) and lineItemId (sort key) — the full composite primary key
C) Only the lineItemId
D) The orderId plus a filter expression

16. A company stores IoT device telemetry in DynamoDB. Each device sends readings every second. What primary key design supports efficient queries for "all readings from device X in the last hour"?
A) deviceId as the partition key and timestamp as the sort key
B) timestamp as the partition key and deviceId as the sort key
C) A simple key with a randomly generated readingId
D) A simple key with timestamp as the partition key

### Hot Partitions & High-Cardinality Keys (17–28)

17. An e-commerce company's Orders table uses orderStatus (values: PENDING, SHIPPED, DELIVERED, CANCELLED) as the partition key. During a flash sale, writes spike and the table begins throttling with ProvisionedThroughputExceededException, even though CloudWatch shows the table's total provisioned WCU is far from its limit. What is the root cause?
A) The table's total provisioned capacity is too low
B) The low-cardinality partition key (only 4 distinct values) concentrates all new orders onto the PENDING partition, creating a hot partition that throttles independently of the table's aggregate capacity
C) The sort key is misconfigured
D) DynamoDB is experiencing a Region-wide outage

18. What is the primary characteristic of a "high-cardinality" partition key, and why does it matter for DynamoDB performance?
A) A high-cardinality key has very few distinct values, concentrating traffic on few partitions
B) A high-cardinality key has many distinct values (such as userId or orderId), distributing traffic evenly across physical partitions and avoiding hot partitions
C) Cardinality refers to the data type of the key, not the number of distinct values
D) High-cardinality keys are always numeric

19. A social media platform's Posts table uses category (e.g., "Sports", "Tech", "Food") as the partition key because it seemed convenient for a "trending in category" dashboard. Under heavy load, the Sports category gets 80% of all writes, causing throttling. Which fix most directly addresses the hot partition problem?
A) Increase the table's provisioned WCU by 10x
B) Change the base table's partition key to a high-cardinality attribute like postId, and create a GSI with category as its partition key for the dashboard query
C) Switch to on-demand capacity mode, which eliminates all hot partition issues
D) Add a sort key to the existing table

20. A celebrity user's account on a social platform generates disproportionately high read traffic to the Users table, where userId is the partition key. The rest of the table distributes traffic evenly. Which technique specifically addresses this single-user hot key?
A) Switching to a different partition key entirely
B) Write sharding: append a random suffix to the hot user's partition key at write time (e.g., userId#1 through userId#10), spreading the items across multiple partitions; on read, fan out queries across all suffixes and merge results
C) Deleting the celebrity user's data
D) Enabling DynamoDB Streams on the table

21. A developer responds to hot partition throttling by doubling the table's provisioned WCU from 2000 to 4000. The throttling continues at the same rate. Why doesn't increasing total capacity fix the problem?
A) DynamoDB ignores provisioned capacity settings entirely
B) Provisioned capacity is distributed across physical partitions; if traffic concentrates on one partition due to a low-cardinality or skewed key, that partition still receives only its fraction of the total capacity, regardless of the aggregate
C) The WCU increase hasn't been applied yet; it takes 24 hours
D) DynamoDB only supports read capacity, not write capacity

22. Which two of the following are effective strategies for preventing or mitigating hot partitions? (Select TWO.)
A) Using a high-cardinality partition key (e.g., orderId, deviceId) to distribute traffic evenly
B) Using write sharding with a random suffix for known hot keys
C) Using a low-cardinality attribute like status or region as the partition key
D) Increasing the table's WCU without changing the key design
E) Adding more sort key attributes to the table

23. A logging application writes all log entries to a DynamoDB table with a partition key of logLevel (values: DEBUG, INFO, WARN, ERROR). Under normal operation, 90% of entries are INFO-level. What will happen as write volume increases?
A) Traffic will distribute evenly across all four partitions
B) The INFO partition will become a hot partition, receiving the vast majority of writes and potentially throttling, while other partitions remain underutilized
C) DynamoDB automatically redistributes items across partitions based on write volume
D) LogLevel is an ideal partition key because it has four distinct values

24. An architect proposes using a composite key of date (partition key) and timestamp (sort key) for a high-volume event log. Why is this design problematic under sustained write load?
A) The design is optimal and has no issues
B) All events for the current date land on one partition, creating a hot partition; historical dates' partitions sit idle while today's partition throttles
C) Sort keys cannot store timestamps
D) Composite keys are not supported for event logs

25. A developer designs a table with userId as the partition key. The application has 10 million active users with roughly equal activity. Is this a good partition key choice?
A) No, because userId values are too unique
B) Yes, because 10 million distinct values provide high cardinality, distributing traffic evenly across many physical partitions
C) No, because DynamoDB cannot handle more than 1000 distinct partition key values
D) Yes, but only if the table uses on-demand capacity mode

26. A company's DynamoDB table uses tenantId as the partition key in a multi-tenant application. Most tenants have low traffic, but one large enterprise tenant accounts for 60% of all reads and writes. Which solution addresses this specific imbalance?
A) Delete the large tenant's data
B) Apply write sharding to the large tenant's partition key (e.g., tenantId#0 through tenantId#9) to spread its items across multiple physical partitions
C) Reduce the table's provisioned capacity
D) Change the partition key to a timestamp

27. A developer notices ProvisionedThroughputExceededException errors on a DynamoDB table. CloudWatch shows overall table utilization is at 30%. Which of the following is the most likely explanation?
A) The table is in the wrong Region
B) Traffic is unevenly distributed across partition keys, causing one or more individual partitions to exceed their share of the provisioned capacity while the overall utilization appears low
C) The DynamoDB service is experiencing a global outage
D) The errors are caused by a permissions issue, not a capacity issue

28. An application needs to query all orders with status = "SHIPPED" frequently. A junior developer suggests making orderStatus the base table's partition key for efficient queries. What is the correct guidance?
A) This is an excellent design; orderStatus is an ideal partition key
B) Use a high-cardinality key (like orderId) as the base table's partition key, and create a GSI with orderStatus as the partition key to support the "orders by status" query without causing hot partitions on the base table
C) Use a Scan with a filter instead of any index
D) orderStatus should be the sort key, not the partition key, with no other changes needed

### Secondary Indexes: GSI vs. LSI (29–42)

29. A chat application's Messages table has been in production for a year with conversationId as the partition key and sentAt as the sort key. Product wants a new feature: "show all messages sent by a specific user across all conversations." Which index type can be added to support this?
A) A Local Secondary Index (LSI), since it can be added at any time
B) A Global Secondary Index (GSI) with senderId as the partition key and sentAt as the sort key, since GSIs can be added to existing tables
C) Neither GSIs nor LSIs can be added after table creation
D) An LSI with senderId as the partition key

30. A table was created with conversationId (partition key) and sentAt (sort key). The team realizes they need to sort messages by a different attribute (priority) within the same conversationId partition. This need was anticipated before the table was created. Which index type could have been defined at creation time to support this?
A) A GSI only
B) An LSI, since LSIs use the same partition key as the base table but with a different sort key, and they can support strongly consistent reads
C) Neither type supports alternate sort keys
D) A Scan with a FilterExpression

31. Which of the following is a key limitation of Local Secondary Indexes?
A) LSIs can be added or removed at any time after table creation
B) LSIs must be defined at table creation time and cannot be added later; all items under one partition key value (across the base table and all LSIs) are limited to 10 GB
C) LSIs have their own independently provisioned throughput
D) LSIs support reads from a completely different partition key than the base table

32. A developer needs to query a production DynamoDB table by a new attribute (email) that wasn't anticipated at design time. The table has been running for months. Which index type supports this requirement?
A) An LSI, which can be added retroactively to production tables
B) A GSI, which can be added to an existing table at any time without downtime
C) Neither index type supports querying by non-key attributes
D) A Scan is the only option and is always efficient enough

33. Which two statements correctly distinguish GSIs from LSIs? (Select TWO.)
A) GSIs can have a completely different partition key from the base table; LSIs must share the base table's partition key
B) GSIs support both eventually and strongly consistent reads; LSIs support only eventually consistent reads
C) GSIs can be created at any time; LSIs must be defined at table creation
D) LSIs have their own independently provisioned throughput; GSIs share the base table's throughput
E) GSIs are limited to 5 per table; LSIs are limited to 20

34. A financial application requires strongly consistent reads when querying by an alternate sort key within the same partition key. Which index type supports this?
A) A GSI, since GSIs support both consistency models
B) An LSI, since LSIs support both eventually and strongly consistent reads (unlike GSIs, which are eventually consistent only)
C) Neither index type supports strongly consistent reads
D) A Scan with ConsistentRead set to true

35. What is the maximum number of GSIs allowed per DynamoDB table by default?
A) 5
B) 10
C) 20
D) Unlimited

36. What is the maximum number of LSIs allowed per DynamoDB table?
A) 20
B) 10
C) 5
D) 1

37. A developer adds a GSI to a table and notices that reads from the GSI occasionally return stale data that was just written to the base table moments ago. What explains this behavior?
A) This is a bug; GSIs should always reflect the latest data instantly
B) GSIs are updated asynchronously from the base table, so there is a small replication lag during which the GSI may not yet reflect the most recent base table writes — this is inherent to GSI eventual consistency
C) The GSI's provisioned capacity is too low
D) The developer forgot to enable streams on the table

38. A GSI has its own provisioned read and write capacity, separate from the base table. If the GSI's write capacity is insufficient to keep up with the rate of base table writes, what happens?
A) The GSI silently drops the updates it cannot keep up with
B) The base table's writes are throttled to match the GSI's write capacity, potentially causing ProvisionedThroughputExceededException on the base table itself
C) The GSI automatically scales to match the base table
D) Nothing; GSIs share the base table's capacity and cannot be throttled independently

39. A team wants to project only a subset of attributes (orderId, status, totalAmount) into a GSI to minimize the index's storage cost and read consumption. Which GSI projection type should they use?
A) ALL (projects every attribute from the base table)
B) INCLUDE (projects the key attributes plus the specified non-key attributes only)
C) KEYS_ONLY (projects only the base table and index key attributes)
D) GSIs cannot control which attributes are projected

40. A developer queries a GSI projected with KEYS_ONLY, but the application also needs the description attribute, which is not part of any key. What happens?
A) The description attribute is returned automatically from the GSI
B) The query returns only the key attributes; to get description, the application must perform a separate fetch against the base table using the returned key
C) The query fails with an error
D) DynamoDB automatically re-projects the missing attribute into the GSI

41. A table has both a base table and two LSIs. The total size of all items with the same partition key value across the base table and both LSIs approaches 10 GB. What happens if a new item with the same partition key would exceed this limit?
A) DynamoDB automatically expands the limit to 20 GB
B) The write is rejected with an ItemCollectionSizeLimitExceededException
C) The oldest items under that partition key are automatically deleted to make room
D) There is no size limit for items sharing a partition key

42. Which of the following scenarios is the strongest fit for choosing a GSI over an LSI?
A) The team needs strongly consistent reads on an alternate sort key within the same partition key, and the table hasn't been created yet
B) The team needs to query by a completely different attribute than the base table's partition key, on a table that's already in production
C) The team wants to avoid any additional storage cost for the index
D) The team needs the index to share the base table's provisioned throughput

### Query vs. Scan (43–52)

43. A developer needs to retrieve all orders for customerId "CUST-9981" from a table with customerId as the partition key. Which operation is most efficient?
A) A Scan with a FilterExpression on customerId
B) A Query specifying customerId as the partition key, which goes directly to the correct partition
C) A BatchGetItem with customerId specified
D) A GetItem with only customerId specified

44. A developer runs a Scan on a 10 GB DynamoDB table with a FilterExpression to find the 50 items matching a specific attribute value. How many read capacity units are consumed?
A) RCUs for only the 50 matching items
B) RCUs for the entire 10 GB table, since a Scan reads every item and the FilterExpression reduces what is returned but not what is read
C) No RCUs, since Scans are free
D) RCUs for exactly half the table

45. An application performs frequent Scans on a growing DynamoDB table. Response times are increasing linearly with table size. What is the most likely architectural improvement?
A) Increase the table's provisioned RCU
B) Redesign the table's key schema and/or add appropriate indexes so the access pattern can be served by a Query instead of a Scan
C) Enable DynamoDB Streams
D) Switch to on-demand capacity mode

46. A developer needs to perform a full-table export for an analytics pipeline. The table has 100 GB of data. Which Scan optimization can reduce the total time for this export?
A) Using a FilterExpression to reduce the data read
B) Using a parallel scan by specifying Segment and TotalSegments, distributing the scan across multiple workers
C) Switching to a GetItem call for each item
D) Running the scan during peak hours for faster processing

47. Which two statements about Query and Scan in DynamoDB are accurate? (Select TWO.)
A) A Query requires a partition key value and efficiently reads only the items on the matching partition
B) A Scan reads every item in the table (or index) regardless of any FilterExpression applied
C) A FilterExpression on a Scan reduces the number of items read from storage, saving RCU
D) A Query does not support FilterExpression
E) A Scan is always faster than a Query for any workload

48. A developer applies a FilterExpression to a Query that returns 1000 matching items from a partition of 5000. How many items' worth of read capacity is consumed?
A) 1000, because the filter reduces what's read
B) 5000, because a FilterExpression on a Query is applied after the items are read from the partition, consuming capacity for all items in the key-condition range, not just those matching the filter
C) 0, because queries are free
D) 500, half the partition

49. A developer needs to find all items across a table where the attribute region equals "APAC", but region is not part of any key or index. What is the only way to perform this search?
A) A Query on the base table specifying region as the partition key
B) A Scan with a FilterExpression on region — or add a GSI with region as the partition key and then use a Query
C) A GetItem specifying region
D) This is impossible in DynamoDB

50. What does the Limit parameter control on a Query or Scan operation?
A) The total number of items the operation can ever return across all pages
B) The maximum number of items evaluated (before any filter is applied) in a single response page; the application must paginate using LastEvaluatedKey to get remaining results
C) The maximum number of RCUs consumed
D) The total storage size of the table

51. A company has a DynamoDB table with 50 million items. A developer needs to identify items where a non-key attribute exceeds a threshold, but this query runs infrequently (once per month for reporting). Is a Scan acceptable here?
A) No, Scans should never be used under any circumstance
B) Yes, an occasional Scan for a monthly reporting job is acceptable, especially if run during off-peak hours and using parallel scan for efficiency — Scans are inappropriate for hot-path, request-serving operations but reasonable for rare, batch analytics tasks
C) Yes, but only if the table uses on-demand capacity
D) No, a new GSI must always be created for any non-key query

52. A developer designs a table where every access pattern requires a Scan with a FilterExpression. What does this indicate about the table design?
A) The table is perfectly designed
B) The table's key schema and/or indexes are poorly aligned with the application's actual access patterns — the table should be redesigned so that frequent queries are served by key-based Query operations
C) Scans are the intended primary access method for DynamoDB
D) FilterExpressions automatically optimize Scans to be as efficient as Queries

### Capacity Modes: On-Demand vs. Provisioned (53–60)

53. A startup is launching a new application with no historical traffic data to forecast DynamoDB read/write volumes. Which capacity mode minimizes the risk of throttling during unpredictable early traffic?
A) Provisioned capacity with a fixed RCU/WCU value based on estimates
B) On-demand capacity mode, which scales automatically to traffic with no capacity planning required
C) Provisioned capacity with auto scaling disabled
D) On-demand mode with manually set throughput limits

54. A well-established application has steady, predictable DynamoDB traffic of 500 RCU and 200 WCU throughout the day, with minimal variation. Which capacity mode is most cost-effective?
A) On-demand, since it always costs less regardless of traffic pattern
B) Provisioned capacity mode with auto scaling configured to maintain a target utilization, since provisioned mode is generally cheaper per unit for steady, predictable workloads
C) On-demand with reserved capacity
D) Neither mode affects cost

55. How many RCUs does a single strongly consistent read of a 6 KB item consume?
A) 1 RCU
B) 2 RCU (6 KB rounds up to 8 KB = 2 × 4 KB blocks = 2 RCU for strongly consistent)
C) 0.5 RCU
D) 6 RCU

56. How many RCUs does a single eventually consistent read of a 6 KB item consume?
A) 2 RCU
B) 1 RCU (6 KB rounds up to 8 KB = 2 × 4 KB blocks, but eventually consistent reads cost half, so 1 RCU)
C) 0.5 RCU
D) 6 RCU

57. A DynamoDB table in provisioned mode experiences a sudden traffic spike that exceeds the provisioned WCU before auto scaling can react. What happens?
A) DynamoDB automatically switches to on-demand mode
B) Write requests exceeding the provisioned capacity are throttled with ProvisionedThroughputExceededException
C) DynamoDB queues the excess writes for later processing
D) The table is automatically deleted to prevent overcharging

58. How often can a DynamoDB table be switched between on-demand and provisioned capacity modes?
A) Unlimited switches per day
B) Once per 24-hour period
C) Once per week
D) A table's capacity mode is permanent and cannot be changed

59. Which two of the following are accurate statements about DynamoDB capacity units? (Select TWO.)
A) 1 WCU supports 1 write per second of an item up to 1 KB
B) Transactional writes (TransactWriteItems) consume double the WCU of non-transactional writes
C) Eventually consistent reads consume the same RCU as strongly consistent reads
D) 1 RCU supports 1 eventually consistent read per second of an item up to 1 KB
E) On-demand capacity mode has no per-request cost

60. A team configures DynamoDB auto scaling on a provisioned table with a target utilization of 70%, minimum 100 RCU, and maximum 1000 RCU. During a traffic spike, utilization reaches 95%. What happens?
A) Auto scaling immediately adds capacity to bring utilization back toward 70%
B) Auto scaling increases provisioned RCU toward the maximum, but there may be a brief delay during which throttling can occur while auto scaling reacts
C) Auto scaling reduces capacity to enforce the 70% target
D) Auto scaling is only available for on-demand tables

### Consistency Models (61–66)

61. A user submits a form that writes to DynamoDB, and the next page immediately reads the just-written data to display a confirmation. Using the default (eventually consistent) read, the confirmation page occasionally shows stale data. Which change fixes this?
A) Enable DynamoDB Streams
B) Set ConsistentRead: true on the GetItem/Query call to perform a strongly consistent read that reflects all completed writes
C) Add a GSI on the confirmation attribute
D) Switch to on-demand capacity mode

62. A developer wants to read data from a GSI with strong consistency. Is this possible?
A) Yes, GSIs support both eventually and strongly consistent reads
B) No, GSIs only support eventually consistent reads; for strongly consistent reads, the developer must query the base table or an LSI
C) Yes, but only if the GSI uses a KEYS_ONLY projection
D) Yes, but only in on-demand capacity mode

63. An application reads a 12 KB item from DynamoDB using eventually consistent reads. How many RCUs does this consume?
A) 3 RCU
B) 1.5 RCU (12 KB = 3 × 4 KB blocks; eventually consistent reads cost half, so 1.5 RCU)
C) 6 RCU
D) 12 RCU

64. Which statement correctly describes the tradeoff between eventually consistent and strongly consistent reads?
A) Strongly consistent reads are always faster and cheaper
B) Eventually consistent reads cost half the RCU and may have slightly lower latency, but can return stale data for a brief window after a write; strongly consistent reads always reflect the latest completed write but cost double and may have slightly higher latency
C) There is no cost difference between the two
D) Eventually consistent reads are never used in production applications

65. A developer notices that reads from a DynamoDB table sometimes return data that was written a fraction of a second ago, and sometimes don't. Which consistency model is this behavior characteristic of?
A) Strongly consistent reads
B) Eventually consistent reads, which may return slightly stale data for a brief window after a write
C) Transactional reads
D) This indicates a service bug

66. A team needs "read-your-writes" correctness on a specific access pattern that currently uses a GSI. Since GSIs don't support strong consistency, what should the team do?
A) Set ConsistentRead: true on the GSI query
B) Redesign the access pattern to query the base table (or an LSI that supports the required key structure) instead of the GSI, since only the base table and LSIs support strongly consistent reads
C) Enable DynamoDB Streams to achieve strong consistency on the GSI
D) Switch to on-demand capacity mode for the GSI

### DynamoDB Streams (67–76)

67. A company needs to trigger a Lambda function every time an item in a DynamoDB table is inserted, modified, or deleted, to replicate changes into an Elasticsearch (OpenSearch) search index. Which DynamoDB feature enables this?
A) TTL
B) DynamoDB Streams with a Lambda event source mapping, which invokes the function with a batch of change records
C) A GSI configured to replicate data to OpenSearch
D) DynamoDB auto scaling

68. Which StreamViewType captures both the old and new images of an item whenever it is modified?
A) KEYS_ONLY
B) NEW_IMAGE
C) OLD_IMAGE
D) NEW_AND_OLD_IMAGES

69. How long are DynamoDB Stream records retained before they expire?
A) 7 days
B) 24 hours
C) 1 hour
D) Indefinitely

70. A developer enables DynamoDB Streams on a table with StreamViewType set to NEW_IMAGE. A Lambda function processes the stream and needs to compute the difference between an item's old and new states. Can it do this with the NEW_IMAGE view type?
A) Yes, NEW_IMAGE includes both the old and new states
B) No, NEW_IMAGE only includes the new state of the item; to compare old and new states, the StreamViewType must be set to NEW_AND_OLD_IMAGES
C) Yes, all view types include both states by default
D) No, stream records never include item data

71. Which of the following is NOT a typical use case for DynamoDB Streams?
A) Replicating changes to a search index like OpenSearch
B) Maintaining a materialized view or derived aggregate
C) Directly querying the stream as a replacement for the base table
D) Triggering downstream event-driven processing via Lambda

72. A developer configures a Lambda function as a DynamoDB Streams consumer. The function processes each batch of records and updates an analytics dashboard. If the function fails to process a batch, what happens?
A) The failed records are permanently lost
B) Lambda retries the batch (records are not removed from the stream until successfully processed), potentially blocking newer records on the same shard until the failure is resolved
C) DynamoDB automatically deletes the stream
D) The records are sent to an SQS queue automatically

73. Which two of the following are accurate statements about DynamoDB Streams? (Select TWO.)
A) DynamoDB Streams provides a time-ordered log of item-level changes on a table
B) DynamoDB Streams retains records indefinitely with no expiration
C) The most common integration pattern is a Lambda event source mapping polling the stream
D) DynamoDB Streams replaces the need for any indexes on the table
E) Stream records are only generated for insert operations, not updates or deletes

74. A TTL expiration deletes an item from a DynamoDB table. Does this deletion appear in the DynamoDB Stream?
A) No, TTL-triggered deletions are not captured by DynamoDB Streams
B) Yes, TTL-triggered deletions appear in the stream with a special identity marker indicating the system (not a user) performed the deletion
C) Only if the stream's view type is set to KEYS_ONLY
D) Only if the table uses provisioned capacity mode

75. A company uses DynamoDB Global Tables for multi-Region replication. What underlying mechanism does Global Tables use to replicate changes across Regions?
A) S3 Cross-Region Replication
B) DynamoDB Streams, which captures changes and propagates them to replica tables in other Regions
C) Lambda functions manually copying items between tables
D) SQS queues bridging the Regions

76. A developer enables DynamoDB Streams and sets up a Lambda consumer. The Lambda function takes too long to process large batches, causing the event source mapping to fall behind. What should the developer do to improve throughput?
A) Disable DynamoDB Streams
B) Increase the Lambda function's batch size, increase parallelization factor, or optimize the function's processing code to handle records faster
C) Switch to a Scan-based polling approach
D) Delete the table and recreate it

### Transactions (77–84)

77. A banking application needs to atomically transfer funds between two accounts stored in DynamoDB — debiting one account and crediting another. If either operation fails, neither should apply. Which DynamoDB feature supports this?
A) BatchWriteItem
B) TransactWriteItems, which provides all-or-nothing ACID transactions across multiple items
C) A conditional PutItem on each item separately
D) DynamoDB Streams

78. How many items can a single TransactWriteItems or TransactGetItems call span?
A) Up to 10 items
B) Up to 100 items (or 4 MB total)
C) Up to 1000 items
D) Unlimited items

79. What is the WCU cost of a transactional write compared to a non-transactional write of the same item?
A) The same cost
B) Double the WCU of a non-transactional write
C) Half the WCU
D) 10x the WCU

80. A developer uses TransactWriteItems for a single-item conditional update. A colleague suggests this is inefficient. Why?
A) TransactWriteItems does not support conditions
B) A simple conditional UpdateItem or PutItem with a ConditionExpression achieves the same single-item atomicity at half the WCU cost, since transactions are for multi-item/cross-table atomicity
C) TransactWriteItems is faster for single items
D) Conditional writes are not supported in DynamoDB

81. What is the purpose of a ConditionCheck action within a TransactWriteItems call?
A) It writes a new item to the table
B) It verifies a condition on an item without writing to it, useful for enforcing invariants on items other than those being modified in the transaction
C) It deletes an item from the table
D) It reads an item and returns it to the application

82. Can a TransactWriteItems call span multiple DynamoDB tables?
A) No, transactions are limited to a single table
B) Yes, TransactWriteItems can include Put, Update, Delete, and ConditionCheck actions across multiple tables within the same AWS account and Region
C) Yes, but only across tables in different Regions
D) Only if all tables share the same partition key

83. Which two of the following are accurate statements about DynamoDB transactions? (Select TWO.)
A) TransactWriteItems provides all-or-nothing atomicity — either every action succeeds, or none apply
B) TransactGetItems provides an atomic, consistent snapshot read across multiple items
C) Transactional operations consume the same WCU/RCU as non-transactional operations
D) DynamoDB transactions support cross-Region operations
E) TransactWriteItems can include up to 1000 items per call

84. A developer attempts to use TransactWriteItems to update 200 items in a single call. What happens?
A) The transaction succeeds normally
B) The call fails, because TransactWriteItems supports a maximum of 100 items per call
C) DynamoDB automatically splits it into two 100-item transactions
D) The call succeeds but only the first 100 items are updated

### DAX (DynamoDB Accelerator) (85–92)

85. A read-heavy e-commerce application needs microsecond-level read latency from DynamoDB for product catalog lookups. Which AWS service provides an in-memory caching layer purpose-built for DynamoDB?
A) Amazon ElastiCache
B) DAX (DynamoDB Accelerator)
C) Amazon CloudFront
D) Amazon MemoryDB

86. A developer switches their application from using the standard DynamoDB SDK client to a DAX client. How much code refactoring is typically required?
A) The entire data access layer must be rewritten with a completely different API
B) Minimal — DAX is API-compatible with the DynamoDB SDK, so typically only the client/endpoint construction changes, not the Get/Put/Query calls themselves
C) The application must switch to a REST API instead of the SDK
D) DAX requires a completely different query language

87. What type of cache consistency does DAX provide?
A) Strong consistency — DAX always returns the most recent data
B) Eventually consistent — DAX is a cache layer, and cached items may be briefly stale until the cache TTL expires or the item is refreshed
C) No caching at all; DAX passes every request through to DynamoDB
D) DAX provides strong consistency for writes and eventual consistency for reads simultaneously

88. A developer configures DAX to cache Query results. Which two types of cache does DAX maintain? (Select TWO.)
A) An item cache for individual GetItem results
B) A query cache for Query and Scan results
C) A write cache that batches writes for later processing
D) A metadata cache for table schema information
E) A stream cache for DynamoDB Streams records

89. When a write is made through DAX, what happens?
A) The write goes directly to DynamoDB, bypassing DAX entirely
B) DAX is write-through: the write passes through DAX to DynamoDB, and DAX updates its item cache with the newly written data
C) The write is cached in DAX only and never reaches DynamoDB
D) DAX queues the write for batch processing later

90. A team has a write-heavy workload with minimal reads. Would DAX provide meaningful performance improvement?
A) Yes, DAX significantly accelerates writes
B) No, DAX primarily accelerates reads by caching results; it does not meaningfully speed up write operations
C) Yes, DAX batches writes for improved throughput
D) No, DAX cannot be used with tables that have any writes

91. An application requires strongly consistent reads on every request. Is DAX appropriate for this use case?
A) Yes, DAX supports strongly consistent reads from the cache
B) No, DAX is an eventually consistent cache layer; if every read must be strongly consistent, DAX's cached responses may not meet the requirement, and strongly consistent reads should go directly to DynamoDB
C) Yes, but only if the DAX cluster has more than 3 nodes
D) DAX automatically switches between consistency modes

92. Which statement best describes the relationship between DAX and DynamoDB in terms of data durability?
A) DAX replaces DynamoDB as the durable data store
B) DynamoDB is the durable source of truth; DAX is a volatile, in-memory cache layer — losing/restarting a DAX node doesn't lose data because DynamoDB retains everything
C) DAX provides higher durability than DynamoDB
D) DAX stores data on disk for durability, not in memory

### Conditional Writes & Optimistic Locking (93–100)

93. A developer wants to prevent a PutItem operation from silently overwriting an existing item with the same primary key. Which mechanism achieves this?
A) Enabling versioning on the DynamoDB table
B) Adding a ConditionExpression: "attribute_not_exists(pk)" to the PutItem call, which fails the write if an item with that primary key already exists
C) Using a BatchWriteItem instead
D) Setting the table to read-only mode

94. Two concurrent requests both read item X with version=3, then both attempt to update it. Using optimistic locking with a version attribute, what happens?
A) Both updates succeed, and the version remains 3
B) The first update succeeds (setting version=4); the second fails with ConditionalCheckFailedException because its ConditionExpression expects version=3, which is now stale
C) Both updates fail
D) DynamoDB automatically merges the two updates

95. What exception does DynamoDB return when a ConditionExpression on a write evaluates to false?
A) ProvisionedThroughputExceededException
B) ConditionalCheckFailedException
C) ValidationException
D) ResourceNotFoundException

96. Does DynamoDB support native pessimistic locking (e.g., "lock this row until I'm done")?
A) Yes, DynamoDB has built-in row-level locking
B) No, DynamoDB does not provide native pessimistic locking; the idiomatic approach is optimistic locking using conditional writes with a version attribute
C) Yes, but only in on-demand capacity mode
D) Yes, through DynamoDB Streams

97. A Java developer uses the DynamoDB SDK's @DynamoDBVersionAttribute annotation on a version field. What does this annotation enable?
A) Server-side encryption of the version field
B) Automatic optimistic locking: the SDK automatically adds a ConditionExpression checking the version and increments it on every update
C) DynamoDB Streams tracking for the version field only
D) Automatic TTL expiration based on the version value

98. Which two of the following are valid uses of ConditionExpressions in DynamoDB? (Select TWO.)
A) Preventing overwrites of existing items by checking attribute_not_exists(pk)
B) Implementing optimistic locking by requiring version = :expectedVersion before allowing an update
C) Defining the partition key for a Query operation
D) Configuring the table's provisioned throughput
E) Setting the TTL attribute for an item

99. A developer implements optimistic locking and the second concurrent update fails with ConditionalCheckFailedException. What should the application do?
A) Immediately retry the same update without re-reading the item
B) Re-read the item to get the current version, apply the business logic to the current state, and retry the update with the new version — the standard optimistic locking retry pattern
C) Delete the item and recreate it
D) Switch to a Scan operation

100. A ConditionExpression on an UpdateItem checks attribute_exists(email). The item does not have an email attribute. What happens?
A) The update succeeds, and the email attribute is created
B) The update fails with ConditionalCheckFailedException because the condition attribute_exists(email) evaluates to false
C) The condition is ignored
D) DynamoDB automatically adds a null email attribute

### TTL (Time to Live) (101–104)

101. A session management system stores session records in DynamoDB and wants sessions to be automatically deleted after 24 hours without any application-side cleanup logic. Which DynamoDB feature supports this?
A) DynamoDB Streams
B) TTL (Time to Live), which automatically deletes items when a designated timestamp attribute indicates they have expired
C) A GSI with a time-based sort key
D) Conditional writes

102. A developer sets a TTL attribute on items to expire at midnight. At 12:01 AM, the developer queries for those items and finds they are still present. Is this expected behavior?
A) No, this indicates TTL is misconfigured
B) Yes, TTL deletion is a background process and items are typically deleted within 48 hours of expiration, not instantly at the exact expiration time
C) No, TTL always deletes items at the exact second of expiration
D) Yes, but only in provisioned capacity mode

103. Does a TTL-triggered deletion consume write capacity units?
A) Yes, TTL deletions consume WCU like any other delete operation
B) No, TTL-triggered deletions do not consume any additional write capacity
C) Only if the table is in provisioned mode
D) Only if DynamoDB Streams is enabled

104. A developer needs items to disappear from query results at the exact moment they expire, not within the 48-hour TTL background deletion window. How should this be implemented?
A) Rely solely on TTL for real-time query filtering
B) Add a FilterExpression or application-level check against the expiry attribute to exclude expired items from query results, while still using TTL for background storage cleanup
C) Disable TTL and manually delete items with a scheduled Lambda
D) Use a Scan to find and delete expired items in real time

### Fine-Grained Access Control & dynamodb:LeadingKeys (105–110)

105. A mobile application authenticates users through Amazon Cognito. Each user stores personal notes in a DynamoDB table. The team wants each user to access only their own notes, enforced at the IAM layer without server-side authorization code in the application. Which mechanism supports this?
A) A bucket policy on the DynamoDB table
B) An IAM policy with a dynamodb:LeadingKeys condition restricting access to items whose partition key matches the caller's Cognito identity, combined with temporary credentials from a Cognito identity pool
C) A GSI filtering by user ID
D) DynamoDB Streams filtering by user ID

106. For the dynamodb:LeadingKeys condition to enforce per-user access, what must be true about the table's partition key?
A) The partition key must be a Number type
B) The partition key must be (or be prefixed by) the user's identity value that the IAM policy variable resolves to
C) The partition key can be any attribute unrelated to the user's identity
D) The partition key must be a GSI key, not a base table key

107. Which IAM policy variable is commonly used with dynamodb:LeadingKeys to represent the authenticated Cognito Identity Pool user's unique identifier?
A) ${aws:username}
B) ${cognito-identity.amazonaws.com:sub}
C) ${aws:PrincipalTag/userId}
D) ${s3:prefix}

108. Which two statements about dynamodb:LeadingKeys are accurate? (Select TWO.)
A) It restricts a caller to items whose partition key matches a specific value, typically derived from the caller's identity
B) It eliminates the need for any custom server-side authorization code to check data ownership
C) It works with any partition key design, regardless of whether the key relates to the user's identity
D) It is a feature of S3 bucket policies, not DynamoDB IAM policies
E) It provides row-level encryption for DynamoDB items

109. A developer designs a DynamoDB table for a multi-user note-taking app but uses noteId (a random UUID) as the partition key. Can dynamodb:LeadingKeys be used to restrict each user to their own notes in this design?
A) Yes, dynamodb:LeadingKeys works with any partition key regardless of its value
B) No, because noteId doesn't correspond to the user's identity; the table's partition key must be (or contain) the user identifier for LeadingKeys to enforce per-user isolation
C) Yes, but only if a GSI is added
D) No, because DynamoDB does not support IAM conditions

110. A company wants users to access their own data through a mobile app backed by DynamoDB, using Cognito identity pools for authentication. Which combination of features enforces per-user data isolation at the IAM layer?
A) DynamoDB Streams + Lambda for authorization
B) Cognito identity pool issuing temporary credentials scoped by an IAM role with a dynamodb:LeadingKeys condition matching the Cognito user's identity, against a table whose partition key is the user identifier
C) A bucket policy on the DynamoDB table
D) DynamoDB auto scaling with per-user throughput limits

### Batch Operations & SDK Patterns (111–118)

111. A developer uses BatchGetItem to retrieve 120 items in a single call. What happens?
A) The call succeeds and returns all 120 items
B) The call fails, because BatchGetItem supports a maximum of 100 items per call
C) DynamoDB automatically splits it into two calls
D) The call succeeds but only returns the first 50 items

112. A BatchWriteItem call partially succeeds, with some items written and others failing due to insufficient capacity. Where are the failed items reported?
A) In a DynamoDB Stream record
B) In the response's UnprocessedItems field, which the application must retry with exponential backoff
C) They are silently dropped with no indication
D) In a CloudWatch alarm notification

113. Does BatchWriteItem support UpdateItem operations?
A) Yes, BatchWriteItem supports Put, Update, and Delete
B) No, BatchWriteItem only supports Put and Delete operations — not partial updates (UpdateItem)
C) Yes, but only for items smaller than 1 KB
D) No, BatchWriteItem only supports Delete operations

114. Which Python boto3 interface transparently handles DynamoDB's wire-format attribute-value serialization (e.g., {"S": "value"}), so the developer works with plain Python dictionaries?
A) boto3.client("dynamodb") — the low-level client
B) boto3.resource("dynamodb") — the higher-level resource client with built-in marshalling
C) Both handle serialization identically
D) Neither; serialization must always be done manually

115. A developer reads a 3.5 KB item using eventually consistent reads. How many RCUs are consumed?
A) 1 RCU
B) 0.5 RCU (3.5 KB rounds up to 4 KB = 1 RCU for strongly consistent, but eventually consistent costs half = 0.5 RCU)
C) 3.5 RCU
D) 2 RCU

116. A developer writes a 2.5 KB item to DynamoDB. How many WCUs are consumed?
A) 2.5 WCU
B) 3 WCU (2.5 KB rounds up to 3 KB = 3 WCU)
C) 1 WCU
D) 0.5 WCU

117. Which two features of the DynamoDB SDK's higher-level document clients (e.g., Java DynamoDBMapper, JS DynamoDBDocumentClient) are accurate? (Select TWO.)
A) They automatically serialize/deserialize application objects to/from DynamoDB's native attribute-value format
B) They can implement optimistic locking via version attributes with built-in annotations
C) They bypass all DynamoDB API quotas and limits
D) They eliminate the need for any IAM permissions
E) They use a proprietary protocol incompatible with the standard DynamoDB API

118. A developer encounters UnprocessedKeys in a BatchGetItem response. What should the application do?
A) Ignore the unprocessed items permanently
B) Retry the request for the items listed in UnprocessedKeys, using exponential backoff to avoid continued throttling
C) Delete the unprocessed items from the table
D) Switch to a Scan operation to retrieve them

### Integrative Scenarios (119–125)

119. A company's DynamoDB table is throttling during peak hours. Investigation reveals: (1) the partition key is a low-cardinality attribute (status), (2) the table uses provisioned capacity with no auto scaling, and (3) a dashboard frequently Scans the entire table. Which combination of changes addresses all three issues?
A) Increase provisioned WCU only
B) Change the partition key to a high-cardinality attribute, enable auto scaling on provisioned capacity, and replace the full-table Scan with a targeted Query against a GSI
C) Switch to on-demand capacity only
D) Disable DynamoDB Streams

120. A mobile app developer needs to implement: (1) per-user row isolation without custom authorization code, (2) microsecond-level read latency for frequently accessed profile data, and (3) automatic cleanup of expired session records without a cleanup Lambda. Which combination of DynamoDB features satisfies all three requirements?
A) GSI for isolation, ElastiCache for caching, lifecycle rules for cleanup
B) dynamodb:LeadingKeys with a Cognito identity pool for per-user isolation, DAX for microsecond read latency, and TTL for automatic session expiration
C) A Scan with FilterExpression for isolation, DynamoDB Streams for caching, conditional writes for cleanup
D) S3 for storage, CloudFront for caching, SQS for cleanup

121. A social media company stores posts in DynamoDB. The most critical access patterns are: (1) get all posts by a user in reverse chronological order, and (2) get all posts in a specific category sorted by likes. The table has been in production for 6 months. Which key and index design satisfies both patterns?
A) A base table with userId as the partition key and createdAt as the sort key (for pattern 1), plus a GSI with category as the partition key and likeCount as the sort key (for pattern 2, added to the existing table)
B) A base table with category as the partition key for both patterns
C) Two separate tables, one for each access pattern
D) A single Scan with filters for both patterns

122. A financial platform needs: (1) atomically transfer funds between two accounts (debit one, credit another), (2) prevent double-spending by ensuring the source account has sufficient funds before the debit, and (3) maintain a version attribute to prevent concurrent conflicting transfers. Which DynamoDB feature combination satisfies all three requirements?
A) Two separate UpdateItem calls with no transaction
B) A TransactWriteItems call containing a ConditionCheck on the source account's balance and version, an Update debiting the source, and an Update crediting the destination — all-or-nothing atomicity with conditional checks
C) A BatchWriteItem call
D) DynamoDB Streams with a Lambda function

123. A developer migrates a relational database to DynamoDB and wants to maintain a search index in OpenSearch, synchronized with DynamoDB changes. Which approach provides near-real-time synchronization with minimal operational overhead?
A) A scheduled Lambda function that Scans the DynamoDB table hourly and updates OpenSearch
B) DynamoDB Streams with a Lambda event source mapping that processes change records and updates the OpenSearch index in near-real-time
C) A manual export/import process run weekly
D) A GSI that automatically replicates to OpenSearch

124. A team reviews their DynamoDB table design and finds: (1) Queries on the base table are efficient, but a new access pattern requires querying by a non-key attribute on a table that's been live for a year, (2) reads from the proposed index must be strongly consistent, and (3) the table already has 5 LSIs defined. What is the correct approach?
A) Add another LSI for the new access pattern
B) Since the table already exists (ruling out LSI addition), and the existing 5 LSIs are at the maximum, the only option is a GSI — but GSIs cannot provide strongly consistent reads, so the application must either accept eventual consistency on this pattern or redesign to query the base table directly
C) Add a 6th LSI by requesting a quota increase
D) Perform a Scan with a FilterExpression instead

125. A company runs an application with a DynamoDB backend that exhibits all of the following issues: (1) throttling errors despite aggregate capacity appearing sufficient, (2) growing response times on a frequently-executed operation as the table grows, (3) stale data occasionally shown to users immediately after a write. For each issue, which DynamoDB concept explains the root cause?
A) (1) is caused by Region-level throttling, (2) by table fragmentation, (3) by TTL delays
B) (1) is likely a hot partition problem from a low-cardinality partition key, (2) is likely a Scan operation that gets slower as the table grows (should be a Query), (3) is likely eventually consistent reads returning stale data (should be strongly consistent reads where needed)
C) All three are caused by insufficient provisioned WCU
D) All three are caused by missing DynamoDB Streams

---

## Answer Key & Explanations

1. B — A simple primary key with orderId provides direct, unique access to each order.
2. B — A composite key with conversationId (partition) and sentAt (sort) groups messages by conversation and orders them by time.
3. B — DynamoDB's maximum item size is 400 KB including all attribute names and values.
4. B — Map is a valid DynamoDB document type supporting nested key-value structures.
5. B — Items with the same partition key are co-located on the same partition and sorted by sort key.
6. B — BETWEEN is a valid sort key condition in a Query; LIKE, IN, and IS NOT NULL are not supported.
7. B — With a simple primary key, a second PutItem with the same key silently overwrites the first.
8. A & C — Only key attributes are required; other attributes vary freely. Maps and Lists support nested structures.
9. B — Map attributes natively store nested key-value structures including nested Lists and Maps.
10. B — A Query on the partition key efficiently retrieves all items for that user, sorted by sort key.
11. B — The primary key is immutable; changing it requires creating a new table and migrating data.
12. B — A simple key with sessionId directly supports the only access pattern (retrieve by sessionId).
13. A — begins_with is a valid sort key condition in a Query operation.
14. A & C — DynamoDB hashes the partition key for placement; items with the same key are on the same partition.
15. B — DeleteItem on a composite-key table requires both the partition key and sort key.
16. A — deviceId as partition key with timestamp as sort key supports efficient time-range queries per device.
17. B — A low-cardinality partition key causes hot partitions, throttling individual partitions despite sufficient aggregate capacity.
18. B — High-cardinality keys have many distinct values, distributing traffic evenly across physical partitions.
19. B — A high-cardinality base key avoids hot partitions; a GSI supports the category-based dashboard query.
20. B — Write sharding spreads a single hot key across multiple physical partitions using suffixed keys.
21. B — Provisioned capacity is divided across partitions; a hot partition only receives its fraction regardless of total capacity.
22. A & B — High-cardinality keys and write sharding are both effective hot-partition mitigation strategies.
23. B — 90% of writes landing on one of four partition key values creates a severely hot partition.
24. B — All events for the current date land on one partition, creating a hot partition.
25. B — 10 million distinct values provide excellent cardinality for even traffic distribution.
26. B — Write sharding on the large tenant's key spreads its items across multiple physical partitions.
27. B — Low overall utilization with throttling indicates traffic skew causing individual hot partitions.
28. B — A high-cardinality base key prevents hot partitions; a GSI enables the status-based query.
29. B — GSIs can be added to existing tables at any time with a different partition key.
30. B — LSIs share the base table's partition key with a different sort key and support strong consistency.
31. B — LSIs must be created at table creation; items under one partition key are capped at 10 GB across table + LSIs.
32. B — GSIs can be added to existing production tables without downtime.
33. A & C — GSIs have different partition keys and can be added anytime; LSIs share the base key and are creation-time only.
34. B — LSIs support both eventually and strongly consistent reads; GSIs are eventually consistent only.
35. C — The default limit is 20 GSIs per table.
36. C — The limit is 5 LSIs per table.
37. B — GSIs are updated asynchronously, so there's an inherent replication lag (eventual consistency).
38. B — Insufficient GSI write capacity causes throttling on the base table itself.
39. B — INCLUDE projection specifies which non-key attributes to include, minimizing storage and read cost.
40. B — Non-projected attributes must be fetched from the base table using the returned key.
41. B — Exceeding the 10 GB per-partition-key limit across base table + LSIs returns ItemCollectionSizeLimitExceededException.
42. B — GSIs support different partition keys on existing tables — the most common use case.
43. B — A Query on the partition key goes directly to the correct partition, making it the most efficient option.
44. B — A Scan reads every item in the table; the FilterExpression only reduces what's returned, not what's read and billed.
45. B — Replacing Scans with Queries (via proper key design and indexes) addresses growing response times.
46. B — Parallel scan distributes the work across multiple workers, reducing total scan time.
47. A & B — Query efficiently reads matching partition items; Scan reads every item regardless of filters.
48. B — FilterExpression on a Query applies after reading; capacity is consumed for all items in the key-condition range.
49. B — Without a key or index on region, a Scan is needed — or add a GSI with region as the partition key.
50. B — Limit controls items per page; pagination via LastEvaluatedKey retrieves subsequent pages.
51. B — Occasional Scans for batch/analytics jobs are acceptable; Scans are problematic on hot request paths.
52. B — Reliance on Scans indicates the key schema doesn't match access patterns and should be redesigned.
53. B — On-demand mode scales automatically with no capacity planning, ideal for unpredictable traffic.
54. B — Provisioned mode with auto scaling is generally cheaper per unit for steady, predictable workloads.
55. B — 6 KB rounds up to 8 KB (2 × 4 KB blocks); strongly consistent = 2 RCU.
56. B — Same 2 blocks, but eventually consistent reads cost half = 1 RCU.
57. B — Excess writes are throttled with ProvisionedThroughputExceededException.
58. B — Capacity mode can be switched once per 24-hour period.
59. A & B — 1 WCU = 1 write/sec up to 1 KB; transactional writes cost double WCU.
60. B — Auto scaling increases capacity toward maximum, but brief throttling may occur during the reaction delay.
61. B — ConsistentRead: true ensures the read reflects all completed writes (read-your-writes correctness).
62. B — GSIs only support eventually consistent reads; strongly consistent reads require the base table or an LSI.
63. B — 12 KB = 3 × 4 KB blocks; eventually consistent = half cost = 1.5 RCU.
64. B — Eventually consistent reads are cheaper and faster but may return stale data briefly; strongly consistent reads always reflect the latest write at double cost.
65. B — Intermittent stale data after recent writes is characteristic of eventually consistent reads.
66. B — Since GSIs can't provide strong consistency, the access pattern must be redesigned to use the base table or an LSI.
67. B — DynamoDB Streams with a Lambda event source mapping captures and processes item-level changes.
68. D — NEW_AND_OLD_IMAGES captures both the before and after states of an item on every change.
69. B — DynamoDB Streams records are retained for 24 hours.
70. B — NEW_IMAGE only includes the new state; NEW_AND_OLD_IMAGES is needed to compare old and new.
71. C — Streams are for change data capture, not as a queryable data store replacement.
72. B — Lambda retries failed batches; records aren't removed until successfully processed, potentially blocking the shard.
73. A & C — Streams are time-ordered item-level change logs; Lambda event source mapping is the most common consumer pattern.
74. B — TTL-triggered deletions appear in the stream with a system identity marker distinguishing them from user-driven deletes.
75. B — DynamoDB Global Tables use Streams as the underlying replication mechanism.
76. B — Increasing batch size, parallelization factor, or optimizing function code improves stream processing throughput.
77. B — TransactWriteItems provides all-or-nothing ACID transactions across multiple items.
78. B — Transactions support up to 100 items or 4 MB per call.
79. B — Transactional writes cost double the WCU of non-transactional writes.
80. B — A simple conditional UpdateItem achieves single-item atomicity at half the WCU cost of a transaction.
81. B — ConditionCheck verifies a condition without writing, useful for invariants on related items within a transaction.
82. B — TransactWriteItems can span multiple tables within the same account and Region.
83. A & B — TransactWriteItems is all-or-nothing; TransactGetItems provides atomic, consistent snapshot reads.
84. B — TransactWriteItems supports a maximum of 100 items per call.
85. B — DAX is a fully managed in-memory cache purpose-built for DynamoDB with microsecond read latency.
86. B — DAX is API-compatible with the DynamoDB SDK; typically only the client construction changes.
87. B — DAX is an eventually consistent cache; cached items may be briefly stale.
88. A & B — DAX maintains an item cache (GetItem) and a query cache (Query/Scan results).
89. B — DAX is write-through: writes pass through to DynamoDB, and the item cache is updated.
90. B — DAX primarily accelerates reads; it doesn't meaningfully speed up writes.
91. B — DAX is eventually consistent; if every read must be strongly consistent, DAX's cache may not meet the requirement.
92. B — DynamoDB is the durable source of truth; DAX is a volatile in-memory cache layer.
93. B — attribute_not_exists(pk) prevents the write if the item already exists — preventing silent overwrites.
94. B — The first update succeeds; the second fails ConditionalCheckFailedException because the version is now stale.
95. B — ConditionalCheckFailedException is returned when a ConditionExpression evaluates to false.
96. B — DynamoDB has no native pessimistic locking; optimistic locking via conditional writes is the idiomatic approach.
97. B — @DynamoDBVersionAttribute enables automatic optimistic locking with condition checks and version increments.
98. A & B — ConditionExpressions prevent overwrites (attribute_not_exists) and implement optimistic locking (version checks).
99. B — The standard pattern is re-read, re-apply logic, and retry with the current version.
100. B — attribute_exists(email) evaluates to false if email doesn't exist, failing the condition check.
101. B — TTL automatically deletes items when their designated timestamp attribute passes the current time.
102. B — TTL deletion is background/eventual, typically within 48 hours of expiration, not instant.
103. B — TTL-triggered deletions do not consume write capacity.
104. B — Add a filter or application check on the expiry attribute for real-time query exclusion; TTL handles background cleanup.
105. B — dynamodb:LeadingKeys with Cognito identity pool credentials enforces per-user row-level access at the IAM layer.
106. B — The partition key must correspond to the user's identity for LeadingKeys to restrict access correctly.
107. B — ${cognito-identity.amazonaws.com:sub} resolves to the authenticated Cognito Identity Pool user's unique ID.
108. A & B — LeadingKeys restricts by partition key matching the caller's identity, eliminating custom authorization code.
109. B — A random noteId doesn't correspond to any user identity, so LeadingKeys cannot enforce per-user isolation.
110. B — Cognito identity pool + IAM role with LeadingKeys + user-identifier partition key enforces per-user isolation.
111. B — BatchGetItem supports a maximum of 100 items per call.
112. B — Partially failed items appear in UnprocessedItems for the application to retry with backoff.
113. B — BatchWriteItem supports only Put and Delete, not UpdateItem.
114. B — boto3.resource("dynamodb") transparently handles attribute-value serialization/deserialization.
115. B — 3.5 KB rounds to 4 KB = 1 RCU (strongly consistent); eventually consistent = 0.5 RCU.
116. B — 2.5 KB rounds up to 3 KB = 3 WCU.
117. A & B — Higher-level clients handle serialization and support optimistic locking via version annotations.
118. B — Retry UnprocessedKeys with exponential backoff to handle throttling.
119. B — A high-cardinality key fixes hot partitions, auto scaling adjusts capacity dynamically, and a GSI-backed Query replaces the expensive Scan.
120. B — LeadingKeys for isolation, DAX for microsecond reads, TTL for automatic cleanup.
121. A — Base table key supports user-posts query; a GSI (addable to existing table) supports category-sorted query.
122. B — TransactWriteItems with ConditionCheck on balance/version, plus debit and credit updates, ensures atomic transfer with conflict detection.
123. B — DynamoDB Streams + Lambda provides near-real-time change data capture for OpenSearch synchronization.
124. B — LSIs can't be added post-creation and are maxed out; a GSI is the only option but can't provide strong consistency — accept eventual consistency or redesign the base table query.
125. B — Hot partition (low-cardinality key), growing Scan times, and eventually consistent read staleness each explain one symptom.
