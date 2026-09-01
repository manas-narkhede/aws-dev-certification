# Module 09 — Practice Questions (125)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### Caching Patterns: Lazy Loading, Write-Through & Read-Through (1–25)

1. A developer is building an e-commerce catalog service where product details are read frequently but updated infrequently. The team wants to implement an in-memory cache using Amazon ElastiCache for Redis. To avoid filling the cache with products that customers never view, data should only be loaded into the cache when a customer actually requests it. If a product is updated, the stale cache entry must be deleted. Which caching pattern is being implemented?
A) Write-Through
B) Lazy Loading (Cache-Aside)
C) Read-Through with DAX
D) Refresh-Ahead

2. An application developer writes the following pseudocode function to retrieve customer profile records:
```
function getCustomer(customerId):
    data = cache.get(customerId)
    if data is not null:
        return data
    data = database.find(customerId)
    cache.set(customerId, data, ttl=600)
    return data
```
Which caching pattern does this code represent?
A) Write-Through
B) Lazy Loading (Cache-Aside)
C) Read-Through
D) Write-Behind

3. A financial reporting service requires that all write operations to a transaction database immediately update the in-memory cache at the exact same time the database is updated. The team can tolerate slightly higher write latency in exchange for guaranteeing that subsequent reads immediately observe the newly written data without a cache miss. Which caching pattern meets these requirements?
A) Lazy Loading
B) Write-Through
C) Read-Through
D) Exponential Backoff

4. A developer is evaluating whether to adopt Write-Through caching or Lazy Loading for an application where 90% of written records are archived data that will never be queried again by users. What is the primary disadvantage of using Write-Through caching in this scenario?
A) Write-Through caching fails to maintain data freshness after database updates
B) Write-Through caching consumes unnecessary cache memory by storing cold data that is never read
C) Write-Through caching results in high cache miss rates for popular read keys
D) Write-Through caching requires changes to the database engine's storage engine

5. A developer is reviewing an application using Lazy Loading with an in-memory cache. A separate administrative batch job directly updates 10,000 records in the underlying relational database without invoking the application API or deleting any cache keys. What will happen when users read those updated records through the application API before the cache entries expire?
A) The application will immediately query the database and retrieve the updated values
B) The application will continue to serve stale, un-updated values from the cache until the cache entries expire or are invalidated
C) The in-memory cache will automatically detect the database change via binlog replication
D) The application will throw a CacheConsistencyException

6. A developer needs to implement a caching architecture where application code does not contain any branching logic to check the cache or query the database on a cache miss. Instead, the application makes standard API calls to a caching layer, and the caching layer transparently queries the backend database when a miss occurs. Which caching pattern is described?
A) Read-Through
B) Write-Behind
C) Client-Side In-Memory Map
D) Lazy Loading

7. An application uses DynamoDB Accelerator (DAX) in front of an Amazon DynamoDB table. When the application issues a `GetItem` request for an item not currently in DAX, DAX fetches the item from DynamoDB, stores it in memory, and returns it to the client without requiring custom cache-miss code in the application. Which caching pattern does DAX implement for read operations?
A) Lazy Loading (Cache-Aside)
B) Read-Through
C) Refresh-Ahead
D) Write-Around

8. A developer is comparing the operational characteristics of Lazy Loading and Write-Through caching. Which two statements accurately describe the trade-offs between these two strategies? (Select TWO.)
A) Lazy Loading only caches requested data, preventing cache churn from cold writes
B) Write-Through caching eliminates all read latency on initial misses for keys that have never been written
C) Write-Through caching introduces higher write latency because every write must update both the database and the cache
D) Lazy Loading ensures that newly written data is immediately populated in cache before any read occurs
E) Lazy Loading requires the caching layer to be fully API-compatible with the backend database SDK

9. A social media application updates user profile bios. The developer implements the write path for a Lazy Loading caching strategy. What sequence of operations should the write function execute when a user updates their bio?
A) Update the database first, then write the new bio directly into the cache with a 24-hour TTL
B) Update the database first, then delete (invalidate) the user's cached profile entry
C) Delete the database record first, then update the cache entry
D) Write to the cache only, and allow a background worker to persist the data to the database asynchronously

10. A backend service implements a Write-Through caching strategy. What is a key failure mode that developers must handle in their application code during a write operation?
A) The cache read failing due to missing TTL parameters
B) A partial failure where the database write succeeds but the subsequent cache write fails, leaving the cache stale
C) A cache miss during a write operation triggering an unhandled database lock
D) Inability to read from the database when the cache cluster reaches maximum memory

11. An architect wants to minimize development effort by accelerating reads for an existing DynamoDB table without rewriting data access methods or managing Redis client connections. Which solution provides transparent Read-Through caching with full DynamoDB API compatibility?
A) Amazon ElastiCache for Memcached
B) DynamoDB Accelerator (DAX)
C) Amazon CloudFront with Lambda@Edge
D) Amazon S3 Select

12. A developer wants to implement a hybrid caching strategy that combines Write-Through and Lazy Loading. How does combining these two patterns benefit the application?
A) Write-Through guarantees freshness for written items, while Lazy Loading handles cache misses for legacy items that have not been modified recently
B) The combination removes the need for any in-memory caching infrastructure
C) The combination reduces all write operations to single-digit microsecond latency
D) The combination eliminates the need for database storage

13. In a Lazy Loading architecture, what occurs on the first read request for an item that has never been queried since the cache was flushed?
A) The application returns a null response immediately
B) A cache miss occurs; the application queries the primary database, populates the cache with the retrieved item, and returns it
C) The caching layer rejects the request with an HTTP 404 error
D) The database automatically pushes all table rows into the cache

14. A team is designing a high-throughput ticketing platform. When ticket prices change, the system must ensure that no customer sees an outdated price, but during regular browsing, read traffic must be offloaded from the database. The team selects Write-Through caching. Why is Write-Through preferred over pure Lazy Loading without invalidation for this use case?
A) Write-Through eliminates database writes completely
B) Write-Through guarantees that the cache is synchronized with the new price immediately upon writing to the database
C) Write-Through is completely serverless and requires no compute instances
D) Write-Through allows reading directly from disk replicas instead of memory

15. An engineer is reviewing code that implements a cache-aside pattern. The code catches network exceptions when communicating with the ElastiCache cluster and falls back directly to the primary database. What design principle does this implementation follow?
A) Strong Consistency Isolation
B) Graceful Degradation / Fault Tolerance
C) Zero-Downtime Replication
D) Sharded Partitioning

16. Which of the following pseudocode blocks accurately illustrates a Write-Through caching pattern for an item update?
A)
```
function updateItem(id, data):
    database.save(id, data)
    cache.delete(id)
```
B)
```
function updateItem(id, data):
    database.save(id, data)
    cache.set(id, data)
```
C)
```
function updateItem(id, data):
    cache.set(id, data)
    queue.push(id, data)
```
D)
```
function updateItem(id, data):
    if cache.exists(id):
        database.save(id, data)
```

17. A developer is designing a caching strategy for a microservice where cached objects must be structured differently than raw database rows (e.g., aggregating data from three separate SQL tables). Which caching pattern and service combination is most appropriate?
A) DynamoDB Accelerator (DAX) with Read-Through
B) Amazon ElastiCache (Redis) with Lazy Loading implemented in application code
C) Amazon S3 Glacier Flexible Retrieval with direct queries
D) Amazon RDS Read Replica with automatic JSON formatting

18. What is the primary difference in code location between Lazy Loading and Read-Through caching?
A) In Lazy Loading, the miss-handling logic is written inside the application code; in Read-Through, it is handled transparently by the caching layer or client library
B) In Lazy Loading, logic lives in the database trigger; in Read-Through, logic lives in CloudFront
C) In Read-Through, the application must manage TCP socket connections manually
D) Lazy Loading cannot be used with Python or Node.js runtimes

19. A developer notices that after deploying a Write-Through caching pattern, the average latency of `PUT /products/{id}` API requests increased by 15ms. What is the root cause of this increase?
A) Write-Through caching forces the database to flush all tables to disk
B) The API must now wait for both the database update and the cache update to complete before returning a response
C) Write-Through caching encrypts data twice using AWS KMS
D) The caching engine locks all read operations during a write

20. An application uses Lazy Loading with ElastiCache for Redis. A developer reports that whenever a new product is added to the database, the product is not found in the cache until someone visits the product page. Is this expected behavior?
A) No, Redis should automatically discover new database records
B) Yes, because Lazy Loading only populates cache entries on-demand upon a read cache miss
C) No, this indicates a broken connection between Redis and the RDS instance
D) Yes, but only if the database is running Amazon Aurora Serverless

21. A developer is architecting a news feed caching solution. Which two criteria indicate that Lazy Loading is a better choice than Write-Through? (Select TWO.)
A) The majority of published articles are never read by more than one or two users
B) The application requires absolute zero tolerance for stale reads immediately after an article is edited
C) Memory capacity on the cache cluster is limited and should only store actively read articles
D) Write latency must be maximized while read latency is completely unconstrained
E) The backend database does not support primary keys

22. What happens in a Read-Through cache when the backend database is temporarily unreachable during a cache miss?
A) The cache automatically invents synthetic data to return to the caller
B) The cache returns an error or exception indicating that the underlying source of truth could not be queried
C) The cache converts the request into a Write-Through operation
D) The cache drops the client connection without an HTTP response code

23. A gaming application stores player scores in an Amazon RDS PostgreSQL database. The developer wants to implement caching using Amazon ElastiCache for Redis. What must the developer do in the application code to implement Lazy Loading?
A) Configure PostgreSQL to publish write-ahead log events directly to Redis port 6379
B) Write code that checks Redis for the player score, queries RDS if not found, and saves the score to Redis with a TTL before returning
C) Install the DAX client library in the application
D) Enable the Multi-AZ feature on the RDS DB instance

24. An application uses a Write-Through caching pattern. During a network partition between the application and ElastiCache, the database write succeeds, but the cache update fails. Which strategy best maintains eventual consistency without crashing the write request?
A) Roll back the database transaction, return an error, and retry the entire operation
B) Invalidate/delete the cache key (or log the key for asynchronous invalidation) so the next read triggers a fresh fetch from the database
C) Delete the database record and restart the ElastiCache cluster
D) Switch the application immediately to local disk caching

25. Which statement best summarizes the fundamental trade-off between Lazy Loading and Write-Through caching?
A) Lazy Loading optimizes for storage capacity; Write-Through optimizes for database security
B) Lazy Loading optimizes write latency and cache memory efficiency at the cost of initial read latency and potential staleness; Write-Through optimizes read freshness and eliminates read misses for written keys at the cost of higher write latency and potential cache pollution
C) Lazy Loading is designed for relational databases; Write-Through is designed exclusively for NoSQL databases
D) Lazy Loading requires AWS IAM authentication; Write-Through requires Amazon Cognito

---

### TTL, Cache Invalidation, Stampedes & Strategies (26–45)

26. A developer configures an Amazon ElastiCache for Redis key with a Time-To-Live (TTL) of 300 seconds. What occurs when an application attempts to read this key 350 seconds after it was set?
A) Redis returns the cached data along with a warning header
B) Redis treats the key as absent (expired), resulting in a cache miss
C) Redis throws an ExpiredKeyException to the application
D) Redis automatically refreshes the key from the backend database

27. A company’s product pricing updates once per hour. The development team wants to ensure that customers never see a price that is older than 60 seconds, even if an explicit cache invalidation call fails during a price update. How should the team configure their Lazy Loading cache?
A) Set a TTL of 60 seconds on every cached pricing item
B) Increase the cache memory size by 60%
C) Use Memcached instead of Redis
D) Remove the database and store all prices exclusively in memory

28. A developer notices that setting a very long TTL (e.g., 24 hours) on cached user permissions results in users experiencing delayed role updates after an administrator changes their access level. Setting a very short TTL (e.g., 2 seconds) causes excessive database CPU utilization. What does this scenario demonstrate regarding TTL configuration?
A) TTL values have no impact on database load
B) TTL represents a direct trade-off between data freshness (avoiding stale reads) and cache hit ratio (protecting backend database load)
C) Caching should never be used for authorization or user permission data
D) ElastiCache requires manual cluster reboots to apply new TTL settings

29. A high-traffic sports website caches live match statistics in ElastiCache with a 10-second TTL. When the key expires during a live championship game, hundreds of concurrent Lambda functions simultaneously experience a cache miss and execute identical heavy SQL queries against the database, causing database CPU utilization to spike to 100%. What term describes this phenomenon?
A) Cache Poisoning
B) Cache Stampede (Thundering Herd)
C) Split-Brain Condition
D) Memory Fragmentation

30. Which two techniques effectively mitigate the risk of a Cache Stampede (Thundering Herd) in a high-concurrency application? (Select TWO.)
A) Implementing distributed locking (mutex) so only one worker queries the database to repopulate the cache while other requests wait or return stale data
B) Reducing the cache cluster size to a single node with no read replicas
C) Using probabilistic early expiration (XFetch / background pre-warming) to refresh the cache before the TTL expires
D) Disabling TTL completely on all keys in the cache
E) Converting all read requests from GET to POST methods

31. A media streaming application stores video metadata in DynamoDB. When a video editor modifies a title, an event is written to DynamoDB Streams. A Lambda function consumes the stream and issues a `DEL` command to the ElastiCache cluster for the corresponding video ID. Which invalidation strategy does this architecture represent?
A) Scheduled Periodic Eviction
B) Event-Driven Cache Invalidation
C) Pure TTL Expiration
D) Write-Through with Synchronous Blocking

32. An application uses ElastiCache for Redis with the `volatile-lru` eviction policy. What happens when the Redis node runs out of memory and a new item is added?
A) Redis crashes and restarts in safe mode
B) Redis evicts the least recently used keys that have an explicit expiration (TTL) set
C) Redis automatically provisions an additional shard in the cluster
D) Redis rejects all read requests with an out-of-memory error

33. A developer wants to ensure that if the cache cluster reaches maximum capacity, the oldest, least active keys are removed regardless of whether they have a TTL set. Which Redis `maxmemory-policy` should be configured?
A) `noeviction`
B) `allkeys-lru`
C) `volatile-ttl`
D) `volatile-random`

34. A developer is designing a cache invalidation strategy for a system where multiple microservices and legacy batch jobs write directly to an Amazon Aurora database. The developer wants to ensure that ElastiCache entries are purged whenever any row in Aurora changes, without modifying legacy batch code. Which solution meets these requirements with minimal operational overhead?
A) Configure Aurora to invoke Lambda via database triggers or capture changes via AWS DMS / Debezium to publish invalidation events to an SNS topic that clears cache keys
B) Rewrite all legacy batch jobs in Node.js to use Write-Through caching
C) Configure ElastiCache to poll Aurora tables every 100 milliseconds
D) Disable caching entirely for all tables modified by batch jobs

35. A developer is implementing probabilistic early expiration (pre-warming) to prevent cache stampedes. What is the core principle behind this algorithm?
A) It randomly deletes 50% of cache keys every minute
B) As a key approaches its expiration time, read requests have an increasing probability of triggering a background refresh of the key before it officially expires
C) It prevents any client from reading the cache if the database is busy
D) It routes all cache misses to Amazon S3 Glacier

36. An e-commerce platform uses Redis to store user shopping carts. Shopping carts must be preserved across sessions for 14 days of inactivity, but if a user accesses their cart on day 13, the expiration countdown must reset to 14 days from that moment. Which Redis command should the developer use when updating or reading the cart?
A) `EXPIRE cart:user123 1209600`
B) `FLUSHDB`
C) `PERSIST cart:user123`
D) `RENAME cart:user123`

37. A developer configures an ElastiCache Redis cluster with the `noeviction` policy. What will happen when the cluster memory becomes full and an application attempts to execute a `SET` command to add a new key?
A) The oldest key in the database is automatically deleted
B) Redis returns an OOM (Out Of Memory) error and refuses to save the new key
C) The cluster automatically adds a read replica node
D) Redis writes the new key to an attached EBS volume

38. A company caches weather forecast data in ElastiCache with a 15-minute TTL. The weather data provider issues an urgent severe weather alert for a specific city. The team needs the updated alert to appear immediately on the website without waiting for the 15-minute TTL to expire. What action should the developer take?
A) Reboot the entire ElastiCache cluster
B) Issue an explicit `DEL` command for the specific city's cache key in Redis
C) Wait for the TTL to elapse, as cached items cannot be deleted manually
D) Decrease the AWS Lambda memory allocation

39. In a microservices architecture, Service A updates an item in DynamoDB and publishes an event to Amazon EventBridge. Service B listens to the event and deletes the corresponding key in its local ElastiCache instance. What is a key benefit of this event-driven cache invalidation approach?
A) It couples Service A directly to Service B's internal cache implementation
B) It decouples the data modification service from the caching layer of downstream consumer services
C) It eliminates the need for Amazon EventBridge rules
D) It guarantees sub-microsecond write consistency across multiple AWS Regions

40. An application caches search query results. 80% of search queries are unique and never repeated, while 20% are repeated frequently. If the developer uses Write-Through caching with no TTL, what problem will occur in the cache?
A) High cache hit ratios exceeding 99%
B) Cache pollution, where memory is consumed by one-off query results that are never read again
C) Automatic deletion of hot query results
D) Unhandled SQL injection vulnerabilities

41. A developer wants to invalidate all cached keys matching a specific pattern (e.g., `product:electronics:*`) in an ElastiCache Redis cluster without blocking the Redis server or causing latency spikes for concurrent client requests. Which approach is recommended?
A) Execute the blocking `KEYS product:electronics:*` command followed by `DEL`
B) Use the non-blocking `SCAN` command with the pattern match, and iteratively delete the returned keys using `UNLINK` (or pipelined `DEL`)
C) Run `FLUSHALL` on the primary node
D) Terminate the primary Redis node to trigger a failover

42. What is the key advantage of the Redis `UNLINK` command over the traditional `DEL` command when removing large keys (such as large sets or hashes)?
A) `UNLINK` performs memory deallocation asynchronously in a background thread, preventing the Redis main thread from blocking
B) `UNLINK` writes the deleted data to Amazon S3 before removing it from memory
C) `UNLINK` works on Memcached clusters as well as Redis
D) `UNLINK` guarantees that the key is retained for 24 hours in a recycle bin

43. An analytics API caches aggregated daily metric reports. The reports for "yesterday" are static and never change once finalized at midnight, while "today's" metrics change constantly. How should the developer configure caching for these two types of reports?
A) Use the exact same 30-second TTL for both yesterday's and today's reports
B) Set a long TTL (e.g., several days or infinite with manual purge) for historical finalized reports, and a short TTL (e.g., 60 seconds) or Lazy Loading with active invalidation for current-day reports
C) Disable caching for historical reports to save memory
D) Store both reports in Amazon SQS queues

44. Which metric in Amazon CloudWatch is most useful for determining whether an ElastiCache cluster's TTLs and memory sizing are appropriate?
A) `NetworkBandwidthIn`
B) `CacheHitRate` (or `BytesUsedForCache` / `Evictions`)
C) `SwapUsage` on RDS
D) `LambdaInvocations`

45. A developer implements a cache with a 5-minute TTL. During testing, they observe that every 5 minutes, backend database latency spikes dramatically for 3 seconds. What is the root cause and the best resolution?
A) All cache keys were inserted simultaneously and share the exact same TTL, causing them to expire at the exact same second; adding random jitter to the TTL (e.g., 300s ± 30s) spreads out expiration times
B) The ElastiCache cluster is rebooting every 5 minutes; replace it with an EC2 instance
C) The database is corrupt; restore from snapshot
D) The Lambda function is experiencing cold starts; increase timeout to 15 minutes

---

### Header-Based Caching, Cache Keys & CloudFront Caching Behaviors (46–65)

46. An international news website serves localized content from an origin server behind Amazon CloudFront. The origin returns English content when the `Accept-Language` header is `en-US` and Spanish content when it is `es-ES`. By default, CloudFront forwards requests without including headers in the cache key. What issue will visitors experience?
A) Spanish visitors will always receive an HTTP 500 error
B) CloudFront will cache whichever language version was requested first and serve that single language to all subsequent users regardless of their `Accept-Language` header
C) CloudFront will automatically translate Spanish text into English
D) The origin server will crash due to infinite redirect loops

47. A developer needs to configure Amazon CloudFront to correctly serve and cache distinct responses based on the visitor's `Accept-Language` request header. How should the CloudFront Cache Policy be configured?
A) Add `Accept-Language` to the headers allowlist in the CloudFront Cache Policy, including it in the cache key
B) Set the CloudFront Minimum TTL to 0 and Maximum TTL to 0
C) Create a separate CloudFront distribution for each language
D) Configure an Origin Request Policy to strip all headers before reaching the origin

48. A SaaS application serves personalized user dashboards at the path `/api/v1/dashboard`. The backend API uses the `Authorization` header containing a JWT to identify the user and render their private account data. A developer accidentally puts a CloudFront CDN in front of this endpoint with default caching enabled (URL-only cache key). What critical security flaw results from this configuration?
A) CloudFront will reject all requests containing bearer tokens
B) CloudFront will cache User A's private dashboard response and serve it to User B, User C, and other callers who request `/api/v1/dashboard`
C) The JWT token will be automatically decrypted and logged in CloudWatch Logs
D) The origin database will delete all user records

49. What HTTP response header should an origin server return for highly sensitive, personalized user data (such as bank balances or profile dashboards) to prevent intermediate caches and CDNs from storing the response?
A) `Cache-Control: public, max-age=86400`
B) `Cache-Control: private, no-store, no-cache`
C) `Content-Type: application/json`
D) `Access-Control-Allow-Origin: *`

50. A developer is configuring a CloudFront distribution that serves both static assets (`/static/*`) and dynamic API requests (`/api/*`). How should the developer structure the distribution to optimize caching performance and prevent caching dynamic data?
A) Create one single cache behavior with a 24-hour TTL for all paths
B) Define multiple Cache Behaviors based on path patterns: configure `/static/*` with long TTLs and standard cache keys, and configure `/api/*` with caching disabled (TTL=0, bypass cache) or customized header/query-string cache keys
C) Deploy two separate AWS accounts
D) Block all GET requests to `/api/*`

51. A company’s web application uses Amazon API Gateway in front of AWS Lambda. The developer enables API Gateway stage caching to reduce Lambda invocations. The API method `GET /products` returns different catalog views depending on the query string parameter `category` (e.g., `GET /products?category=shoes`). What configuration is required in API Gateway to ensure responses are cached separately per category?
A) Add `category` as a Query String parameter in the Method Request and check "Caching" on that parameter in the method execution settings
B) Set the stage cache capacity to 0.5 GB
C) Enable AWS WAF on the API Gateway stage
D) Create a separate API Gateway resource for every possible category value

52. A developer wants to forward the `User-Agent` header to the origin server for analytics logging, but does NOT want `User-Agent` to be part of the CloudFront cache key because thousands of different browser strings would fragment the cache and reduce the cache hit ratio to near zero. Which CloudFront configuration achieves this?
A) Include `User-Agent` in the Cache Policy headers list
B) Leave `User-Agent` out of the Cache Policy (cache key), and include `User-Agent` in the Origin Request Policy
C) Disable the Origin Request Policy completely
D) Use Lambda@Edge to append `User-Agent` to the URL path

53. An e-commerce website deploys an updated JavaScript bundle (`app.js`) to Amazon S3 behind CloudFront. After deployment, users report that their browsers continue downloading the old version of the script. The CloudFront distribution has a Default TTL of 86,400 seconds (24 hours). Which two approaches allow the new script to take effect immediately? (Select TWO.)
A) Create a CloudFront invalidation for `/app.js` (or `/*`)
B) Use versioned filenames (e.g., `app.v2.js` or `app.a1b2c3.js`) in application HTML references for subsequent deployments
C) Increase the CloudFront Maximum TTL to 7 days
D) Change the S3 bucket name
E) Delete the CloudFront distribution and recreate it from scratch

54. Why does AWS recommend using versioned object names (e.g., `main.d41d8c.js`) rather than frequent CloudFront invalidations for managing updates to static web assets? (Select TWO.)
A) Invalidation requests can take time to propagate globally across all edge locations, whereas new versioned URLs are fetched instantly on first request
B) Versioned URLs allow old and new versions of assets to coexist seamlessly during rolling application deployments
C) CloudFront charges for invalidations beyond the monthly free tier allowance (first 1,000 invalidation paths/month free)
D) Versioned filenames disable SSL/TLS encryption automatically
E) CloudFront cannot cache files that have dots in their filenames

55. An API Gateway REST API has stage caching enabled. The developer wants to allow administrative clients with appropriate IAM permissions to bypass the cache and fetch fresh data from the backend by passing a `Cache-Control: max-age=0` header. What setting must be configured on the API Gateway method?
A) Enable "Require authorization to invalidate cache" and grant `execute-api:InvalidateCache` IAM permissions to authorized callers
B) Disable API Gateway caching globally
C) Set the HTTP status code to 304 Not Modified
D) Enable CORS on the API Gateway resource

56. A developer configures a CloudFront distribution with a Custom Origin. The origin returns the header `Cache-Control: max-age=300`. The CloudFront Cache Policy has Minimum TTL = 60, Maximum TTL = 3600, and Default TTL = 86400. How long will CloudFront cache the response?
A) 60 seconds
B) 300 seconds (5 minutes)
C) 3,600 seconds (1 hour)
D) 86,400 seconds (24 hours)

57. A developer configures a CloudFront distribution where the origin returns NO `Cache-Control` or `Expires` headers in its responses. The Cache Policy specifies Minimum TTL = 0, Maximum TTL = 31536000, and Default TTL = 86400. How long will CloudFront cache these responses?
A) 0 seconds (responses will not be cached)
B) 86,400 seconds (Default TTL applies when origin headers are missing)
C) 31,536,000 seconds
D) Indefinitely until an explicit invalidation is submitted

58. What is the impact on cache efficiency when an application includes high-cardinality headers (such as unique device IDs or request timestamps) in the CloudFront cache key?
A) The cache hit ratio increases dramatically
B) The cache hit ratio drops significantly because virtually every request generates a unique cache key, causing edge cache misses
C) CloudFront automatically aggregates the requests into a single cache entry
D) Origin server CPU utilization drops to zero

59. An API returns data in either JSON or XML format depending on the client’s `Accept` header (`application/json` vs `application/xml`). To ensure CloudFront caches both JSON and XML responses correctly without collision, what must the developer do?
A) Add `Accept` to the headers allowlist in the CloudFront Cache Policy
B) Change the HTTP request method to PUT
C) Instruct all clients to only request JSON
D) Store the XML responses in an S3 Glacier vault

60. A web application serves personalized user profile pictures at `/users/me/avatar.png` using a session cookie `session_id`. If CloudFront is configured to forward all cookies in the cache key for this behavior, what will happen?
A) All users will share a single cached avatar image
B) Each user with a distinct `session_id` will have their avatar cached separately, preventing cross-user data leakage at the cost of a lower overall cache hit ratio across users
C) CloudFront will reject the cookie and strip it from the request
D) The origin server will stop receiving requests completely

61. Which HTTP status codes are cached by default by Amazon CloudFront when returned by an origin?
A) Only HTTP 200 OK
B) HTTP 200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, and 501 (with configurable negative caching TTLs for 4xx/5xx errors)
C) Only HTTP 500 Internal Server Error
D) No HTTP error codes can ever be cached by CloudFront

62. A developer notices that when their backend origin returns HTTP 404 Not Found errors during a deployment, CloudFront caches those 404 responses for 10 seconds (the default Error Caching Minimum TTL), causing users to see 404s even after the missing resource is uploaded. How can the developer customize this behavior?
A) Configure Custom Error Responses in CloudFront and set the Error Caching Minimum TTL for error code 404 to 0 seconds
B) Switch the origin from S3 to EC2
C) Reissue an ACM SSL certificate
D) Delete the CloudFront distribution

63. An application uses Amazon CloudFront to serve content from an Application Load Balancer. The developer wants to inspect incoming request headers and normalize the `Accept-Language` header to only `en`, `fr`, or `es` before the cache key is computed, maximizing the edge cache hit ratio. Which compute feature should the developer use at edge locations?
A) AWS Step Functions
B) CloudFront Functions (or Lambda@Edge) on Viewer Request
C) Amazon Athena
D) AWS Glue ETL Job

64. What is the difference between CloudFront Functions and Lambda@Edge for manipulating cache keys and request headers?
A) CloudFront Functions run in milliseconds at edge PoPs with ultra-low cost and sub-millisecond execution for simple header rewrites; Lambda@Edge runs in regional edge caches with longer runtimes and full network/filesystem access
B) CloudFront Functions only support Java; Lambda@Edge only supports Python
C) Lambda@Edge cannot modify request headers
D) CloudFront Functions can only be triggered on Origin Response events

65. A developer is testing an API Gateway deployment with caching enabled. The developer submits a `GET` request with query parameters in different orders: `GET /items?sort=asc&limit=10` followed by `GET /items?limit=10&sort=asc`. By default, how does API Gateway treat these parameters in the cache key?
A) It treats them as different keys unless query parameter order is normalized or handled consistently
B) It converts all query parameters into JSON payloads
C) It rejects the second request with an HTTP 400 error
D) It routes the second request directly to AWS X-Ray

---

### DAX (DynamoDB Accelerator) Architecture & Use Cases (66–85)

66. A mobile gaming company’s DynamoDB table experiences intense read spikes during weekend tournaments. The team wants to reduce read latency from single-digit milliseconds to sub-millisecond (microseconds) without changing the data access logic in their application code. Which AWS service should they deploy?
A) Amazon ElastiCache for Memcached
B) Amazon DynamoDB Accelerator (DAX)
C) Amazon RDS Read Replica
D) Amazon Redshift Serverless

67. How does a developer integrate an existing Node.js application with a newly created DAX cluster?
A) Rewrite all database operations to use standard SQL `SELECT` queries
B) Replace the standard AWS DynamoDB SDK client initialization with the DAX SDK client, pointing to the DAX cluster endpoint
C) Configure an AWS Lambda function to poll DAX every second
D) Change the DynamoDB table billing mode from On-Demand to Provisioned

68. What types of caches does Amazon DAX maintain internally within each cluster node?
A) Item Cache (stores individual items from `GetItem`/`BatchGetItem`) and Query Cache (stores query and scan results based on parameter sets)
B) Block Cache and Inode Cache
C) Disk Cache and S3 Cache
D) Relational Table Cache and Foreign Key Cache

69. An application writes a new item to DynamoDB through DAX using the `PutItem` API. How does DAX handle this write operation?
A) DAX rejects write operations; writes must be sent directly to DynamoDB
B) DAX writes the item to DynamoDB first, and upon successful write, updates its own item cache (Write-Through behavior)
C) DAX writes to memory only and discards the write if the power fails
D) DAX buffers the write in an Amazon SQS queue for 24 hours

70. What is the recommended minimum number of nodes for a production Amazon DAX cluster to ensure high availability across multiple Availability Zones?
A) 1 node
B) 3 nodes (1 primary node and 2 read replica nodes deployed across different AZs)
C) 10 nodes
D) 50 nodes

71. An application issues a strongly consistent read (`ConsistentRead: true`) using `GetItem` against a DAX cluster endpoint. How does DAX process this request?
A) DAX returns the value from its in-memory item cache immediately
B) DAX does not serve strongly consistent reads from its cache; it passes the request directly through to DynamoDB and does not cache the result
C) DAX throws an UnsupportedConsistencyException
D) DAX queries all nodes in the cluster and computes a majority quorum

72. A developer is designing a caching layer for an application. The workload consists of read-heavy queries across both an Amazon RDS MySQL database and a DynamoDB table. Why is Amazon ElastiCache a better fit than DAX for this specific scenario?
A) DAX is strictly purpose-built for Amazon DynamoDB and cannot cache data from Amazon RDS or other heterogeneous data sources
B) DAX does not support in-memory caching
C) ElastiCache does not support VPC security groups
D) ElastiCache only works with NoSQL databases

73. A developer notices that when performing `Query` operations on a DAX cluster, an update to an individual item in DynamoDB does not immediately invalidate the Query Cache in DAX. Why does this occur?
A) The Query Cache in DAX is indexed by query parameter sets, not individual item keys; query results remain in the Query Cache until their TTL expires or the cache is evicted
B) DAX disables all caching for Query operations
C) DynamoDB does not support secondary indexes when DAX is enabled
D) The DAX cluster is configured in single-node mode

74. What is the default TTL for items stored in the DAX Item Cache if not explicitly customized?
A) 0 seconds (disabled)
B) 5 minutes (300 seconds)
C) 24 hours
D) 7 days

75. Which two operations are NOT cached in DAX's in-memory cache and are always passed directly through to DynamoDB? (Select TWO.)
A) `GetItem` with `ConsistentRead: false`
B) `GetItem` with `ConsistentRead: true`
C) `Query` with `ConsistentRead: false`
D) `Scan` with `ConsistentRead: true`
E) `BatchGetItem` with eventually consistent reads

76. A developer needs to deploy a DAX cluster for an application running in a VPC. Where must the DAX cluster nodes be placed?
A) In a public subnet with an Internet Gateway route
B) In subnets within the same VPC as the application (or a peered VPC), associated with a DAX Subnet Group
C) In an on-premises data center connected via dial-up
D) In an S3 bucket

77. How does DAX handle cluster node failure when Multi-AZ replication is configured?
A) The cluster shuts down until an administrator manually promotes a replica
B) An automatic failover occurs: one of the read replica nodes is promoted to primary, and internal DNS routing is updated
C) All data in the DynamoDB table is deleted
D) The application falls back to Amazon S3 Glacier

78. A financial trading system requires microsecond read latency on stock tickers. The reads are eventually consistent and heavily concentrated on the top 50 stocks. Which solution provides the best performance and lowest operational overhead?
A) Amazon Aurora Global Database with 15 read replicas
B) DynamoDB with Amazon DAX
C) Amazon RDS for SQL Server
D) Amazon S3 with Athena partitioned queries

79. An application uses DAX. A background process writes updates directly to DynamoDB bypassing the DAX cluster endpoint. What will happen when application clients read those updated items through DAX?
A) DAX will immediately invalidate its cache using database triggers
B) DAX may serve stale data from its item cache until the item's TTL expires or it is evicted due to memory pressure
C) DAX will crash with a StaleDataException
D) DynamoDB will reject the direct write operation

80. What security mechanism encrypts data at rest within an Amazon DAX cluster?
A) AWS KMS customer managed or AWS owned keys enabled at cluster creation
B) S3 Client-Side Encryption SDK
C) DynamoDB Local Secondary Indexes
D) HTTPS TLS certificates only

81. A developer is evaluating DAX pricing. How is Amazon DAX billed?
A) Per million DynamoDB read request units only
B) Hourly per provisioned DAX node instance type (e.g., `dax.r5.large`), independent of request volume
C) Flat rate of $500 per month per table
D) Based on the number of Lambda functions connected to the cluster

82. Which of the following read operations will benefit MOST from the DAX Item Cache?
A) Repeated `GetItem` requests for hot user profile records by primary key
B) Broad `Scan` operations over millions of cold records
C) Strongly consistent reads across multiple tables
D) Full table backups using AWS Backup

83. When scaling a DAX cluster to handle increased read throughput, which dimension should be scaled?
A) Add read replica nodes horizontally to the DAX cluster (up to 10 nodes per cluster)
B) Increase the S3 bucket quota
C) Convert the DynamoDB table to Global Tables
D) Decrease the DAX node memory size

84. Can an application write directly to DynamoDB while reading through DAX?
A) No, DAX blocks all direct DynamoDB writes
B) Yes, but writes bypassing DAX will not update the DAX cache, creating potential staleness until the DAX TTL expires
C) Yes, and DAX will automatically update its cache synchronously on direct writes
D) No, DAX requires exclusive ownership of the DynamoDB table

85. Which statement accurately contrasts DAX with ElastiCache for Redis?
A) DAX requires creating custom Redis key-value serialization logic in the application
B) DAX is a drop-in, API-compatible cache specifically for DynamoDB, whereas ElastiCache is a general-purpose in-memory data store supporting rich data structures (lists, sets, hashes) for any backend
C) ElastiCache provides lower latency than DAX for DynamoDB operations
D) DAX cannot be deployed in a VPC

---

### Lambda Concurrency, Sizing & Connection Pooling (RDS Proxy) (86–105)

86. A sudden marketing campaign causes a serverless application to scale to 800 concurrent AWS Lambda executions. The Lambda functions open direct connections to an Amazon RDS MySQL database. Within seconds, database queries begin failing with `Too many connections` errors. What is the root cause?
A) RDS storage ran out of free space
B) Each concurrent Lambda execution environment opened its own independent database connection, quickly exceeding MySQL’s `max_connections` limit
C) MySQL automatically restarts when more than 10 Lambda functions execute
D) Lambda execution roles cannot access RDS databases

87. Which managed AWS service should be deployed between AWS Lambda and Amazon RDS to solve database connection exhaustion by pooling and sharing database connections?
A) Amazon ElastiCache for Redis
B) Amazon RDS Proxy
C) AWS Secrets Manager alone
D) Network Load Balancer

88. A developer wants to ensure that a critical payment processing Lambda function is never starved of compute capacity during traffic spikes caused by other non-critical functions in the same AWS account. Which configuration should the developer apply?
A) Set Reserved Concurrency on the payment Lambda function to guarantee a dedicated slice of account concurrency
B) Increase the Lambda function timeout to 15 minutes
C) Lower the payment function memory to 128 MB
D) Disable dead-letter queues on the function

89. An e-commerce API experiences severe latency spikes during the first few seconds of a flash sale because hundreds of Lambda execution environments must be initialized from scratch (cold starts). Which Lambda feature eliminates cold-start latency for predictable traffic surges?
A) Provisioned Concurrency
B) Reserved Concurrency set to 0
C) Unreserved Account Concurrency
D) Ephemeral storage (`/tmp`) expansion

90. How does Provisioned Concurrency differ from Reserved Concurrency in AWS Lambda? (Select TWO.)
A) Provisioned Concurrency pre-warms execution environments so functions respond with double-digit millisecond latency without cold starts
B) Reserved Concurrency guarantees an allocation limit and acts as a ceiling on concurrent executions to protect downstream systems
C) Provisioned Concurrency is completely free of charge
D) Reserved Concurrency pre-warms execution environments in all AWS Regions globally
E) Provisioned Concurrency can only be configured for Node.js runtimes

91. A developer is writing a Lambda function in Python that queries an Amazon RDS database on every invocation. Where should the database connection initialization code be placed to optimize performance across multiple warm invocations?
A) Inside the handler function body so a new connection is created on every single invocation
B) Outside the handler function (in global/initialization scope) so warm execution environments reuse the existing database connection across invocations
C) Inside an S3 bucket lifecycle rule
D) In a separate CloudWatch Logs subscription filter

92. An engineer needs an emergency "kill switch" to immediately stop all invocations of a malfunctioning Lambda function without deleting the function or modifying application code. What is the fastest method?
A) Set the function's Reserved Concurrency to 0
B) Change the function's runtime to Java 8
C) Delete the IAM execution role
D) Reduce the function timeout to 1 second

93. A legacy backend database can only support a maximum of 20 concurrent connections without crashing. A serverless application processes order events from Amazon SQS using Lambda. How can the developer protect the database from being overwhelmed by Lambda invocations?
A) Set the Lambda function's Reserved Concurrency to 20
B) Increase the SQS batch size to 10,000
C) Set the Lambda timeout to 1 second
D) Configure SQS Long Polling to 0 seconds

94. What is the default unreserved concurrency limit per Region for an AWS account in Lambda?
A) 10 concurrent executions
B) 1,000 concurrent executions (raisable via Service Quotas request)
C) 100,000 concurrent executions
D) Unlimited

95. An application using Amazon RDS Proxy needs to handle database credentials securely and rotate passwords automatically every 30 days. Which AWS service does RDS Proxy integrate with to manage and retrieve database credentials?
A) AWS Systems Manager Parameter Store (Standard)
B) AWS Secrets Manager
C) Amazon S3 Glacier
D) AWS Key Management Service (AWS KMS) directly without Secrets Manager

96. When configuring Amazon RDS Proxy with AWS Lambda, how does RDS Proxy improve application resilience during an RDS Multi-AZ database failover?
A) RDS Proxy automatically converts the database into a DynamoDB table
B) RDS Proxy maintains client connections on the application side while seamlessly reconnecting to the newly promoted primary database instance, reducing failover downtime by up to 66%
C) RDS Proxy caches all failed transactions in local Lambda memory
D) RDS Proxy disables database replication during failover

97. A developer allocates 1,024 MB of memory to a compute-heavy Lambda function. What is the relationship between configured memory and CPU power in AWS Lambda?
A) CPU power is fixed at 1 vCPU regardless of memory allocation
B) Lambda allocates CPU power proportionally to the configured memory; increasing memory increases available vCPU cores and compute speed
C) Increasing memory reduces CPU clock speed to save power
D) CPU allocation only increases when memory exceeds 10,240 MB

98. A developer notices that a CPU-intensive encryption function running on Lambda takes 12 seconds to complete at 256 MB of memory ($0.00005 per invocation). When memory is increased to 1,024 MB, the function finishes in 2.5 seconds ($0.000042 per invocation). What does this demonstrate?
A) Higher memory allocation can result in both faster performance AND lower total execution cost for CPU-bound workloads
B) Lower memory is always more cost-effective regardless of runtime
C) Lambda charges a flat fee per execution independent of duration
D) Memory allocation does not affect execution time

99. An asynchronous Lambda function processing events from Amazon S3 encounters throttling because the account concurrency limit has been reached. What is Lambda's default behavior for throttled asynchronous invocations?
A) The event is immediately discarded and lost
B) Lambda automatically retries the throttled event for up to 6 hours with exponential backoff before sending it to an On-Failure Destination or Dead-Letter Queue (DLQ) if configured
C) Lambda returns an HTTP 500 error to Amazon S3
D) S3 deletes the source object

100. A developer observes that their Lambda function experiences connection timeouts when connecting to Amazon RDS through RDS Proxy. The Lambda function is deployed inside a VPC. What VPC networking configuration is required for the Lambda function to reach RDS Proxy?
A) The Lambda function must be deployed in the same VPC (or a routed VPC) with Security Groups allowing outbound traffic to the RDS Proxy security group on the database port (e.g., 3306 or 5432)
B) The Lambda function must be assigned a public IP address and communicate over an Internet Gateway
C) The Lambda function must be removed from the VPC entirely
D) RDS Proxy must have a public DNS endpoint exposed to the internet

101. An API Gateway endpoint backed by a Lambda function with Provisioned Concurrency configured receives 500 concurrent requests. The Provisioned Concurrency level is set to 300. How will the remaining 200 requests be handled?
A) The 200 requests will be rejected with an HTTP 429 Too Many Requests error
B) The 200 requests will be handled by standard on-demand Lambda scaling from the unreserved concurrency pool (experiencing standard cold-start initialization if new environments are spun up)
C) The 200 requests will be buffered in an S3 bucket
D) The entire batch of 500 requests will fail

102. What metric in CloudWatch indicates that a Lambda function's invocations are being throttled due to exceeding concurrency limits?
A) `Errors`
B) `Throttles`
C) `Duration`
D) `ConcurrentExecutions`

103. A developer wants to automatically scale Provisioned Concurrency for a Lambda function based on predictable daily traffic schedules (e.g., scaling up at 8:00 AM and scaling down at 6:00 PM). Which AWS service provides scheduled and target-tracking auto-scaling for Lambda Provisioned Concurrency?
A) Application Auto Scaling
B) AWS Elastic Beanstalk
C) AWS Step Functions only
D) Amazon Route 53

104. A team implements RDS Proxy for their PostgreSQL database. What is a key consideration when using prepared statements with RDS Proxy?
A) RDS Proxy does not support PostgreSQL databases
B) When a client executes certain session-pinning operations (like prepared statements or temporary tables), RDS Proxy pins the connection to a specific database instance, temporarily reducing multiplexing efficiency
C) Prepared statements disable all encryption in transit
D) Prepared statements double database storage consumption

105. How can a developer monitor the active connection pool utilization of an Amazon RDS Proxy instance?
A) Monitor CloudWatch metrics for the RDS Proxy, such as `DatabaseConnections`, `QueryRequests`, and `ConnectionBorrowLatency`
B) Check S3 access logs
C) Inspect the Lambda handler's local `/tmp` directory
D) Run `traceroute` from an EC2 instance

---

### Profiling, Bottleneck Analysis & Power Tuning (106–125)

106. A developer investigates a slow microservice where API response times average 4.5 seconds. CloudWatch metrics show that the EC2 instance CPU utilization is under 5% and memory utilization is at 18%. What type of bottleneck is the application experiencing?
A) CPU-bound bottleneck
B) Memory-bound bottleneck
C) I/O-bound bottleneck (e.g., waiting on slow database queries, external HTTP APIs, or un-cached network calls)
D) Storage volume corruption

107. An image processing application running on EC2 crashes repeatedly during peak load with `OutOfMemoryError: Java heap space` messages. CloudWatch shows CPU utilization at 45% prior to each crash. What type of bottleneck is this, and what is the primary resolution?
A) CPU-bound; upgrade to a compute-optimized instance family (C6i)
B) Memory-bound; increase Java heap size / upgrade to a memory-optimized instance family (R6g) or optimize image buffer handling
C) I/O-bound; add an Internet Gateway
D) Network-bound; enable Enhanced Networking

108. An e-commerce service executes a distributed workflow across Amazon API Gateway, AWS Lambda, Amazon DynamoDB, and an external payment gateway. Users report intermittent 8-second delays. Which AWS observability tool produces a visual service map showing the exact latency breakdown for each downstream hop in a request?
A) Amazon CloudWatch Logs Insights
B) AWS X-Ray
C) AWS CloudTrail
D) Amazon GuardDuty

109. What open-source, Step Functions-based tool helps developers find the optimal balance between performance (duration) and cost for AWS Lambda functions by running automated benchmarks across multiple memory configurations?
A) AWS Lambda Power Tuning
B) AWS CodeDeploy
C) Amazon Inspector
D) AWS Systems Manager Run Command

110. A developer uses AWS Lambda Power Tuning to analyze a data transformation function. The tool generates the following results:
- At 128 MB: Duration = 6,000 ms, Cost = $0.0000125
- At 512 MB: Duration = 1,200 ms, Cost = $0.0000100
- At 1,024 MB: Duration = 600 ms, Cost = $0.0000100
- At 2,048 MB: Duration = 580 ms, Cost = $0.0000193
Which memory configuration provides the best combination of speed and cost efficiency?
A) 128 MB (slowest and highest cost)
B) 1,024 MB (10x faster than 128 MB, tied for lowest cost at $0.0000100)
C) 2,048 MB (minimal speed gain over 1,024 MB but nearly double the cost)
D) 10,240 MB

111. Which AWS developer tool continuously profiles live production application CPU usage and identifies the specific lines of code or expensive methods consuming the most CPU cycles?
A) Amazon CodeGuru Profiler
B) AWS CodeBuild
C) AWS CodeArtifact
D) Amazon CloudWatch Synthetics

112. A developer uses AWS X-Ray to diagnose high latency in an API. In the X-Ray trace details, a subsegment named `DynamoDB::GetItem` has a duration of 3,800 ms with an HTTP status code 200, while the Lambda handler itself executed for 3,850 ms. What does this trace demonstrate?
A) The Lambda runtime environment is missing memory
B) The latency bottleneck is caused almost entirely by the DynamoDB `GetItem` call (an I/O bottleneck), pointing to a need for caching (e.g., DAX) or partition key optimization
C) The client's internet connection is slow
D) The API Gateway stage has a syntax error

113. An application processes large CSV files by loading the entire 2 GB file into an in-memory array before parsing. Under heavy load, the EC2 instance starts heavy disk swapping, and response times degrade severely. What software design optimization should the developer implement?
A) Upgrade to an instance with 128 GB of RAM and continue loading the entire file into memory
B) Refactor the code to stream and process the CSV line-by-line (or in small chunks) rather than buffering the entire file in memory
C) Change the file format to uncompressed BMP
D) Disable virtual memory on the operating system

114. A developer configures AWS X-Ray tracing on a Lambda function. What two steps are required to trace downstream HTTP calls made by the AWS SDK inside the Lambda function? (Select TWO.)
A) Enable Active Tracing on the Lambda function configuration
B) Wrap the AWS SDK client (or HTTP client) using the AWS X-Ray SDK (e.g., `AWSXRay.captureAWS(require('aws-sdk'))` in Node.js or `patch_all()` in Python)
C) Install the X-Ray daemon on an on-premises server
D) Convert all JSON API responses to XML
E) Grant the Lambda execution role `xray:PutTraceSegments` and `xray:PutTelemetryRecords` permissions

115. A developer notices that an API Gateway endpoint backed by Lambda has high p99 latency but low p50 latency. The CloudWatch metric `InitDuration` shows that initial cold-start invocations take 2,200 ms, while warm invocations take 45 ms. Which optimization directly targets reducing `InitDuration`?
A) Reduce the deployment package size, remove unused dependencies/libraries, and initialize heavy objects in global scope (or enable Provisioned Concurrency)
B) Increase the Lambda timeout to 15 minutes
C) Convert the Lambda runtime from Node.js to Java with Spring Boot
D) Switch from API Gateway REST API to HTTP API without changing Lambda code

116. In Amazon CloudWatch, what metric filter pattern or tool allows developers to extract structured metrics from application logs without writing custom CloudWatch API emission code?
A) CloudWatch Embedded Metric Format (EMF)
B) S3 Select
C) AWS CloudTrail Data Events
D) Amazon Athena partition projection

117. A developer is diagnosing an issue where an application running on Amazon ECS on AWS Fargate occasionally becomes unresponsive. The ECS task CPU utilization reaches 100% whenever cryptographic hashing functions are executed. Which type of bottleneck is present, and what is the best architectural mitigation?
A) I/O-bound; attach an Amazon EFS volume
B) CPU-bound; increase the task CPU allocation in the ECS Task Definition or offload cryptographic hashing to an asynchronous worker queue (e.g., SQS + worker fleet)
C) Memory-bound; decrease task memory to 512 MB
D) Network-bound; enable IPv6 on the VPC subnet

118. What information does an AWS X-Ray Annotation provide compared to X-Ray Metadata?
A) Annotations are indexed key-value pairs that can be used with filter expressions to search and group traces in the X-Ray console; Metadata is not indexed and cannot be used for searching
B) Metadata is indexed for search; Annotations are plain text comments
C) Annotations can only contain binary image data
D) Metadata is automatically deleted after 1 hour

119. A developer runs a load test on a web service. CloudWatch metrics indicate:
- Request count: 5,000 req/sec
- 5xx error rate: 0.01%
- Database CPU: 12%
- Web Server CPU: 94%
- Average response time: 2.1 seconds
What is the primary bottleneck and the recommended scaling action?
A) Database I/O bottleneck; deploy Amazon ElastiCache
B) Web server CPU bottleneck; configure Auto Scaling to add more web server instances or increase task CPU capacity
C) Network throughput bottleneck; request a Route 53 quota increase
D) Memory bottleneck on the database primary node

120. A Python Lambda function imports several heavy libraries (`pandas`, `numpy`, `scipy`) at the top of the file, but only 10% of invocations actually execute the data science code path. How can the developer optimize invocation latency for the other 90% of requests?
A) Lazy-import the heavy libraries inside the specific handler branch where they are needed, rather than at the top-level module scope
B) Combine all functions into a single 500 MB zip file
C) Increase the Lambda function ephemeral storage (`/tmp`) to 10 GB
D) Switch the Lambda architecture from ARM64 to x86_64

121. An enterprise application has a latency requirement of under 20ms for global users. The database is Amazon Aurora in `us-east-1`. Users in Europe and Asia experience 180ms latency. Analysis shows that 95% of requests are read-only queries for product catalogs. What combination of optimizations achieves the latency requirement? (Select TWO.)
A) Deploy Amazon CloudFront with caching enabled for catalog API responses at edge locations worldwide
B) Deploy Aurora Global Database with read replicas in European and Asian AWS Regions to serve read queries locally
C) Migrate the entire database to an on-premises MySQL server
D) Increase Lambda function execution timeout to 900 seconds
E) Convert all GET requests to GraphQL mutations

122. A developer uses Amazon CloudWatch Logs Insights to analyze API latency. Which query syntax calculates the 95th and 99th percentile durations of requests from log events containing a `@duration` field?
A) `fields @timestamp, @message | sort @timestamp desc | limit 20`
B) `stats pct(@duration, 95), pct(@duration, 99) by bin(5m)`
C) `filter @message like /error/ | count()`
D) `display @logStream, @duration`

123. A financial analytics application running on EC2 performs matrix computations. The developer observes that CPU utilization is at 99% across all 4 vCPUs of a `c5.xlarge` instance. The developer wants to test if moving to AWS Graviton-based instances (`c7g.xlarge`) improves price-performance. What consideration must the developer address?
A) Graviton instances require compiling or running application binaries on ARM64 architecture rather than x86_64
B) Graviton instances do not support Linux operating systems
C) Graviton instances cannot run inside an Amazon VPC
D) Graviton instances require migrating all data to Amazon DynamoDB

124. An application uses a distributed lock in Redis to coordinate access to a shared resource across multiple workers. If a worker crashes while holding the lock, what mechanism prevents the resource from remaining locked forever (deadlock)?
A) Setting an automatic expiration (TTL) on the lock key when acquiring it (e.g., using `SET resource_lock my_random_token NX PX 30000`)
B) Rebooting the Redis cluster every hour
C) Storing the lock in an S3 Glacier vault
D) Using unencrypted Redis AUTH tokens

125. An architect is reviewing an end-to-end e-commerce application architecture for performance optimization. The system has four key workloads: (1) Static web assets (HTML/CSS/JS), (2) High-traffic product catalog queries (read-heavy, updated daily), (3) User shopping cart data (read/write, session-scoped), and (4) Order checkout transactions requiring strict relational integrity. Which combination of caching and storage technologies represents the optimal AWS architecture?
A) CloudFront for static assets + ElastiCache (Redis) Lazy Loading for catalog queries + DynamoDB with DAX for shopping carts + Amazon Aurora with RDS Proxy for order checkouts
B) S3 only for all storage and caching
C) Amazon RDS for MySQL Single-AZ for all four components with no caching
D) DAX for static assets + CloudFront for relational order checkouts

---

## Answer Key & Explanations

1. B — Lazy Loading (Cache-Aside) only populates data on-demand when a read miss occurs, preventing cache pollution from unread data, and invalidates stale keys on write.
2. B — The pseudocode checks cache first, queries DB on miss, and writes result to cache with a TTL — the textbook Lazy Loading (Cache-Aside) read pattern.
3. B — Write-Through synchronously writes to both the database and the cache on every write operation, guaranteeing immediate freshness on subsequent reads.
4. B — Write-Through caches every written record regardless of whether it is ever read, consuming valuable memory on cold or archived records.
5. B — Because Lazy Loading relies on application-level invalidation during writes, out-of-band database writes bypass cache deletion, leaving stale data until TTL expiry.
6. A — In Read-Through caching, the caching layer/client transparently fetches missing data from the database on a miss without application-level branching logic.
7. B — DAX acts as a transparent Read-Through cache for DynamoDB; the application calls standard DynamoDB SDK methods against DAX without custom miss-handling code.
8. A & C — Lazy Loading only caches requested data (saving cache memory), while Write-Through incurs higher write latency because every write updates both DB and cache.
9. B — The standard write path for Lazy Loading updates the source of truth (DB) first, then invalidates (deletes) the cached key so the next read fetches fresh data.
10. B — In Write-Through caching, a failure during the secondary cache write can leave the cache out of sync with the newly updated database record.
11. B — DynamoDB Accelerator (DAX) provides managed, API-compatible, transparent Read-Through in-memory caching specifically for DynamoDB.
12. A — Combining Write-Through with Lazy Loading ensures fresh data for updated items while allowing cold/legacy items to be loaded on-demand on first read.
13. B — On a cache miss in Lazy Loading, the application queries the database, writes the fetched data into the cache with a TTL, and returns it to the caller.
14. B — Write-Through synchronizes the cache immediately upon every database write, ensuring no caller receives outdated price data.
15. B — Catching cache communication failures and falling back directly to the primary database is an example of graceful degradation and fault tolerance.
16. B — Write-Through updates both the database and the cache synchronously as part of the write operation.
17. B — ElastiCache with application-level Lazy Loading allows custom data transformations and aggregations across multiple backend tables before caching.
18. A — In Lazy Loading, miss-handling is written explicitly in application code; in Read-Through, the caching layer or SDK handles misses transparently.
19. B — Write-Through requires waiting for two network round trips (database write + cache write) to complete before returning a response.
20. B — Lazy Loading is reactive; new items are only cached when a client issues a read request that triggers a cache miss.
21. A & C — Lazy Loading avoids caching articles that are rarely read (saving memory) and is ideal when cache capacity is constrained.
22. B — If the primary source of truth is unreachable during a cache miss, the Read-Through cache returns an error because it cannot fulfill the fetch.
23. B — Implementing Lazy Loading requires application code to check Redis, query RDS on miss, and write the fetched result to Redis with a TTL.
24. B — Deleting the cache key upon a write failure ensures that subsequent reads will re-fetch the fresh value from the database.
25. B — Lazy Loading optimizes write speed and memory usage with potential read misses; Write-Through optimizes read freshness at the cost of write latency and cache pollution.
26. B — Once a key's TTL expires, Redis automatically treats the key as absent, resulting in a cache miss on the next read.
27. A — Setting a 60-second TTL bounds the maximum staleness window to 60 seconds even if explicit invalidation is missed.
28. B — TTL is a direct trade-off: longer TTLs improve hit ratios and protect the database, while shorter TTLs improve data freshness.
29. B — A Cache Stampede (or Thundering Herd) occurs when a popular key expires and multiple concurrent requests simultaneously overwhelm the database.
30. A & C — Distributed locking (mutex) and probabilistic early expiration (pre-warming) prevent multiple workers from simultaneously querying the database on key expiration.
31. B — Using DynamoDB Streams and Lambda to delete cache keys on data modification is an event-driven cache invalidation pattern.
32. B — The `volatile-lru` policy evicts the least recently used keys among those that have an explicit expiration (TTL) configured.
33. B — `allkeys-lru` evicts the least recently used keys out of all keys in the database, regardless of whether a TTL is set.
34. A — Capturing database modifications via triggers/DMS and publishing invalidation events decouples cache clearing from legacy batch write paths.
35. B — Probabilistic early expiration computes a probability of refreshing a key in the background as its expiration time nears, avoiding simultaneous misses.
36. A — The `EXPIRE` command in Redis sets or resets the time-to-live countdown on a key.
37. B — Under `noeviction`, Redis returns an Out Of Memory (OOM) error for write commands when memory is exhausted.
38. B — Issuing an explicit `DEL` command immediately removes the key from Redis, forcing the next read to fetch the latest alert from the database.
39. B — Event-driven cache invalidation decouples write services from the caching mechanisms of downstream consumers.
40. B — Caching one-off, non-repeated search queries leads to cache pollution, consuming memory without providing hit-ratio benefits.
41. B — Using `SCAN` and `UNLINK` avoids blocking the single-threaded Redis event loop while cleaning up matching keys.
42. A — `UNLINK` unbinds keys from the keyspace immediately and reclaims memory asynchronously in background threads.
43. B — Finalized historical data can be cached with long/infinite TTLs, while active/changing data requires short TTLs or active invalidation.
44. B — CloudWatch `CacheHitRate`, `BytesUsedForCache`, and `Evictions` indicate whether cache sizing and TTL policies are effective.
45. A — When keys share an identical TTL and insertion time, they expire simultaneously; adding random jitter spreads expiration over time.
46. B — If `Accept-Language` is excluded from the cache key, CloudFront caches the first response seen and serves it to all subsequent requests regardless of language.
47. A — Including `Accept-Language` in the CloudFront Cache Policy headers allowlist makes it part of the cache key, caching language variants separately.
48. B — Excluding `Authorization` from the cache key allows personalized responses to be cached under the shared URL and served to other users.
49. B — `Cache-Control: private, no-store, no-cache` instructs CDNs and intermediate caches never to store or serve the personalized response.
50. B — Path-based Cache Behaviors allow static assets (`/static/*`) to use long TTLs while dynamic endpoints (`/api/*`) bypass caching or use custom keys.
51. A — In API Gateway, adding query parameters to the Method Request and checking "Caching" incorporates them into the cache key.
52. B — Leaving `User-Agent` out of the Cache Policy prevents cache fragmentation, while adding it to the Origin Request Policy forwards it to the backend.
53. A & B — Invalidating CloudFront cache paths forces immediate edge re-fetching, while versioned asset filenames provide clean cache busting for deployments.
54. A & B — Versioned URLs are instantly available globally without invalidation propagation delays and allow seamless coexistence during rolling updates.
55. A — Enabling "Require authorization to invalidate cache" and granting `execute-api:InvalidateCache` allows authorized clients to bypass the cache.
56. B — CloudFront respects the origin's `Cache-Control: max-age=300` because it falls within the configured Minimum (60) and Maximum (3600) TTL bounds.
57. B — When origin caching headers are absent, CloudFront applies the Default TTL (86,400 seconds) specified in the Cache Policy.
58. B — High-cardinality values in the cache key create unique keys for every request, fragmenting the cache and destroying the hit ratio.
59. A — Adding `Accept` to the Cache Policy header allowlist caches JSON and XML representations separately under their respective content types.
60. B — Forwarding `session_id` cookies in the cache key isolates cached responses per user, preventing cross-user leakage at the expense of global caching.
61. B — CloudFront caches successful responses as well as specific 3xx, 4xx, and 5xx status codes according to error caching rules.
62. A — Configuring Custom Error Responses in CloudFront allows setting the Error Caching Minimum TTL to 0 seconds for specific error codes.
63. B — CloudFront Functions on Viewer Request execute lightweight code at edge PoPs to normalize headers before the cache key is evaluated.
64. A — CloudFront Functions run in sub-milliseconds at edge PoPs for lightweight header rewrites; Lambda@Edge provides complex compute at Regional Edge Caches.
65. A — By default, differing query parameter orders can result in separate cache entries unless normalized before key computation.
66. B — Amazon DAX delivers microsecond read latency for DynamoDB with drop-in SDK compatibility and no application logic rewrite.
67. B — Integrating DAX only requires initializing the DAX SDK client with the cluster endpoint in place of the standard DynamoDB client.
68. A — DAX maintains an Item Cache for individual `GetItem` calls and a Query Cache for `Query`/`Scan` result sets.
69. B — DAX performs Write-Through on `PutItem`: it writes to DynamoDB first, then updates its own Item Cache upon success.
70. B — Production DAX clusters should have at least 3 nodes across multiple AZs (1 primary + 2 read replicas) for Multi-AZ fault tolerance.
71. B — Strongly consistent reads (`ConsistentRead: true`) bypass the DAX cache and are passed directly through to DynamoDB.
72. A — DAX is strictly designed for Amazon DynamoDB, whereas ElastiCache is a versatile cache for RDS, APIs, and custom data stores.
73. A — DAX Query Cache is keyed by query parameters, so item updates do not automatically invalidate the Query Cache until TTL expiry.
74. B — The default TTL for the DAX Item Cache is 5 minutes (300 seconds) unless explicitly modified.
75. B & D — Strongly consistent `GetItem` and `Scan` operations bypass the DAX cache and pass directly through to DynamoDB.
76. B — DAX cluster nodes must be deployed within VPC subnets associated with a DAX Subnet Group.
77. B — On primary node failure, DAX automatically promotes a read replica to primary and updates internal routing.
78. B — DynamoDB with DAX provides microsecond latency for hot read keys with minimal operational overhead.
79. B — Bypassing DAX on writes leaves the DAX cache unaware of changes, potentially serving stale data until the item TTL expires.
80. A — DAX supports encryption at rest using AWS KMS customer managed or AWS owned keys enabled at cluster creation.
81. B — DAX is billed on an hourly basis per provisioned node instance type, independent of the number of requests processed.
82. A — The DAX Item Cache is optimized for repeated key-based `GetItem` lookups for hot records.
83. A — Adding read replica nodes horizontally to a DAX cluster (up to 10 nodes) scales read throughput.
84. B — Direct writes to DynamoDB succeed but will not update the DAX cache, creating potential staleness until DAX TTL expires.
85. B — DAX is a drop-in, API-compatible cache for DynamoDB; ElastiCache is a general-purpose data store for multiple backends.
86. B — High Lambda concurrency creates hundreds of independent database connections, quickly exhausting RDS `max_connections`.
87. B — Amazon RDS Proxy manages and multiplexes connection pools between Lambda and relational databases to prevent exhaustion.
88. A — Setting Reserved Concurrency on a Lambda function guarantees dedicated capacity and prevents starvation from other functions.
89. A — Provisioned Concurrency pre-warms execution environments to eliminate cold-start latency for predictable traffic surges.
90. A & B — Provisioned Concurrency pre-warms execution environments to prevent cold starts; Reserved Concurrency guarantees an allocation ceiling.
91. B — Initializing database connections outside the handler in global scope allows warm Lambda environments to reuse connections across invocations.
92. A — Setting Reserved Concurrency to 0 instantly throttles all incoming invocations, acting as an immediate kill switch.
93. A — Setting Lambda Reserved Concurrency to 20 restricts maximum concurrent executions, preventing database connection exhaustion.
94. B — The default unreserved concurrency pool for an AWS account in a Region is 1,000, which can be increased via Service Quotas.
95. B — RDS Proxy integrates natively with AWS Secrets Manager to store, retrieve, and automatically rotate database credentials.
96. B — RDS Proxy maintains client connections and seamlessly redirects traffic to the promoted primary during Multi-AZ failovers, reducing downtime.
97. B — Lambda allocates CPU power proportionally to configured memory; increasing memory increases vCPU allocation and compute performance.
98. A — For CPU-bound tasks, increasing memory can dramatically reduce execution time, resulting in faster performance AND lower total cost.
99. B — Throttled asynchronous Lambda invocations are automatically retried for up to 6 hours with backoff before routing to a DLQ or Destination.
100. A — VPC-enabled Lambda functions require Security Groups that permit outbound traffic to the RDS Proxy Security Group on the DB port.
101. B — Requests exceeding the Provisioned Concurrency level are handled by standard on-demand Lambda scaling from the unreserved concurrency pool.
102. B — The `Throttles` CloudWatch metric increments when invocations are rejected due to exceeding concurrency limits.
103. A — Application Auto Scaling manages scheduled and target-tracking auto-scaling policies for Lambda Provisioned Concurrency.
104. B — Session-pinning operations (like prepared statements) cause RDS Proxy to temporarily pin connections, reducing multiplexing efficiency.
105. A — CloudWatch metrics such as `DatabaseConnections` and `ConnectionBorrowLatency` provide visibility into RDS Proxy connection pools.
106. C — Low CPU and low memory utilization paired with high latency indicates an I/O-bound bottleneck (waiting on external systems/databases).
107. B — OutOfMemory errors with moderate CPU usage indicate a memory-bound bottleneck requiring increased memory allocation or heap tuning.
108. B — AWS X-Ray generates visual service maps with detailed latency breakdowns across distributed microservice architectures.
109. A — AWS Lambda Power Tuning is an open-source Step Functions tool that benchmarks Lambda performance and cost across memory settings.
110. B — 1,024 MB provides a 10x speedup over 128 MB while matching the lowest execution cost ($0.0000100).
111. A — Amazon CodeGuru Profiler analyzes live production CPU usage to pinpoint inefficient methods and expensive lines of code.
112. B — An X-Ray subsegment showing 3,800 ms spent in `DynamoDB::GetItem` proves that the bottleneck is downstream I/O latency.
113. B — Streaming large datasets line-by-line or in chunks prevents memory exhaustion and heavy disk swapping.
114. A & B — Tracing downstream SDK calls requires enabling Active Tracing on Lambda and wrapping SDK clients with the AWS X-Ray SDK.
115. A — Reducing deployment package size, trimming unused dependencies, and global scope initialization directly minimize `InitDuration` (cold starts).
116. A — CloudWatch Embedded Metric Format (EMF) allows structured JSON logs to be automatically ingested as CloudWatch metrics.
117. B — 100% CPU utilization on cryptographic tasks indicates a CPU-bound bottleneck; increasing CPU allocation or offloading to workers resolves it.
118. A — X-Ray Annotations are indexed key-value pairs used for filtering and searching traces; Metadata is non-indexed data for debugging.
119. B — 94% Web Server CPU with low DB load indicates a compute bottleneck on the web tier; adding instances via Auto Scaling resolves it.
120. A — Lazy-importing heavy libraries inside specific code branches avoids loading them on invocations that do not use them.
121. A & B — CloudFront caches catalog responses globally, while Aurora Global Database read replicas provide sub-millisecond regional reads.
122. B — CloudWatch Logs Insights uses `stats pct(@duration, 95), pct(@duration, 99) by bin(5m)` to calculate percentile durations.
123. A — Migrating to AWS Graviton instances requires software compatibility or recompilation for ARM64 architecture.
124. A — Setting a TTL on Redis distributed locks ensures locks automatically expire if a worker crashes, preventing deadlocks.
125. A — CloudFront for static assets, ElastiCache for catalog queries, DynamoDB/DAX for session carts, and Aurora/RDS Proxy for ACID checkouts follows AWS best practices.
