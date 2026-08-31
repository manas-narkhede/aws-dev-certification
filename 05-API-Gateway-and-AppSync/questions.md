# Module 05 — Practice Questions (124)

Calibrated to AWS's official DVA-C02 sample question style: scenario stems, plausible parallel-structured options, multi-response where natural. Answer key with explanations at the end.

### REST APIs vs. HTTP APIs (1–12)

1. A startup is building a new public API backed entirely by Lambda proxy integrations, with no need for usage plans, API keys, request-body validation, or a private VPC-only endpoint. The team's top priorities are the lowest possible latency and the lowest possible cost per request. Which API Gateway API type should they choose?
A) REST API
B) HTTP API
C) WebSocket API
D) A private REST API with a VPC endpoint

2. A financial services company needs to expose an API that enforces per-partner request quotas using API keys, applies JSON Schema request validation before invoking the backend, and caches GET responses per stage to reduce backend load. Which API Gateway API type supports all of these requirements?
A) HTTP API
B) REST API
C) WebSocket API
D) None of API Gateway's types support response caching

3. Which of the following is a capability available on REST APIs but NOT available on HTTP APIs in API Gateway?
A) Lambda proxy integration
B) Usage plans and API keys
C) Custom domain names
D) IAM authorization

4. A company needs an API that is reachable only from within its VPC via a VPC endpoint, with no public internet exposure whatsoever. Which API Gateway API type supports this private endpoint configuration?
A) HTTP API
B) REST API
C) WebSocket API
D) AppSync

5. A team migrating a simple Lambda-backed microservice from REST API to HTTP API is evaluating the tradeoffs. Which statement accurately describes what they gain and lose in this migration?
A) They gain usage plans and lose Lambda proxy integration support
B) They gain lower latency and lower cost, but lose usage plans, API keys, request validation, and response caching
C) They gain response caching but lose the ability to use Lambda at all
D) There is no functional difference between REST APIs and HTTP APIs

6. Which authorizer capability is built natively into HTTP APIs without requiring a custom Lambda authorizer?
A) A native JWT (OIDC/OAuth2) authorizer
B) A native SAML authorizer
C) A native API key validator
D) A native mutual TLS certificate authority

7. A company wants to implement a canary deployment on their API, shifting a small percentage of traffic to a newly deployed version of the API configuration before promoting it fully to all traffic. Which API Gateway API type supports canary deployments?
A) HTTP API
B) REST API
C) Both support canary deployments identically
D) Neither supports canary deployments

8. A developer is deciding between REST API and HTTP API for a new internal microservice that only needs simple Lambda proxy integration, IAM authorization, and does not need usage plans, request validation, or caching. Which choice minimizes cost while still meeting all stated requirements?
A) REST API, since it is the only option supporting IAM authorization
B) HTTP API, since it supports Lambda proxy integration and IAM authorization at lower cost and latency than REST API
C) WebSocket API, since it is always the cheapest option
D) Neither type supports IAM authorization

9. Which statement correctly compares response caching support between REST APIs and HTTP APIs?
A) Both support per-stage response caching identically
B) Only REST APIs support built-in per-stage response caching; HTTP APIs do not offer this feature
C) Only HTTP APIs support response caching
D) Neither API type supports any form of caching

10. A company needs to attach a resource policy to their API restricting invocation to requests originating from a specific VPC endpoint, in addition to IAM authorization. Which API Gateway API type must they use?
A) HTTP API, since resource policies are a universal feature
B) REST API, since resource policies are supported there but not on HTTP APIs
C) WebSocket API exclusively
D) Resource policies are not supported by any API Gateway type

11. Which two of the following are true when comparing REST APIs to HTTP APIs in Amazon API Gateway?
A) REST APIs support usage plans and API keys; HTTP APIs do not
B) HTTP APIs generally offer lower latency and lower cost for comparable Lambda-proxy-backed traffic
C) HTTP APIs support private VPC-endpoint-only access while REST APIs do not
D) REST APIs cannot use Lambda as a backend integration
E) HTTP APIs and REST APIs have completely identical feature sets

12. A team's scenario requirements state: "the API must support request body validation against a JSON Schema model before invoking the backend, to reject malformed payloads early." Which API type should the team select?
A) HTTP API, because JSON Schema validation is its primary built-in feature
B) REST API, because full request validation against JSON Schema models is a REST API feature not available on HTTP APIs
C) WebSocket API, because validation only applies to persistent connections
D) Any API type, because validation is unrelated to API Gateway type

### Resources, Methods & Integration Types (13–30)

13. A developer configures a method's integration so that the entire raw HTTP request — headers, query string, path parameters, and body — is passed to a Lambda function as a single structured event, and the function's return value must match a specific `{statusCode, headers, body}` shape. Which integration type is being used?
A) Lambda custom (non-proxy) integration
B) Lambda proxy integration
C) Mock integration
D) AWS service integration

14. A Lambda function behind a proxy integration returns the following from its handler: `{"orderId": "42", "status": "created"}`. What will the client actually receive from API Gateway?
A) A 200 response with that exact JSON body
B) A 502 error, because the response does not match the required `{statusCode, headers, body}` envelope shape
C) A 403 error, because the response is missing an IAM signature
D) A 401 error, because the response is missing an Authorization header

15. Which integration type allows API Gateway to write directly to a DynamoDB table using a mapping template, without invoking any Lambda function?
A) Lambda proxy integration
B) Mock integration
C) AWS service integration
D) WebSocket integration

16. A frontend team needs to begin testing against an API's request/response shape, but the backend Lambda function has not been implemented yet. Which integration type lets API Gateway return a static, predefined response without invoking any backend?
A) Lambda proxy integration
B) Mock integration
C) HTTP proxy integration
D) AWS service integration

17. In a Lambda proxy integration, which of the following fields must the client-facing HTTP response body be encoded as, within the object Lambda returns?
A) A raw JSON object, not a string
B) A JSON-stringified string assigned to the "body" key
C) A base64-encoded binary blob only, regardless of content type
D) An XML document, regardless of the Accept header

18. A developer wants fine-grained control to transform an incoming request into a completely different shape (renaming fields, restructuring nested objects) before it reaches a Lambda function, and also wants to reshape the Lambda function's raw output before it reaches the client. Which integration type supports this level of control via mapping templates?
A) Lambda proxy integration
B) Lambda custom (non-proxy) integration
C) Mock integration
D) HTTP proxy integration

19. Which of the following is a legitimate backend target for an API Gateway HTTP integration (as opposed to Lambda or AWS service integrations)?
A) An on-premises system or another HTTP API reachable directly or via a VPC Link
B) Only Lambda functions
C) Only DynamoDB tables
D) Only Amazon S3 buckets

20. A REST API method is configured with a Mock integration returning a static 200 response with sample JSON. What is the primary tradeoff of this configuration compared to a real backend integration?
A) It costs significantly more per request than a Lambda integration
B) It always returns the identical static response regardless of the request, since no backend logic actually runs
C) It cannot be used for testing CORS preflight OPTIONS requests
D) It requires a Cognito User Pool authorizer to function

21. A company's API method uses a Lambda custom (non-proxy) integration. The client sends a request, but the Lambda function receives a payload that doesn't resemble the raw HTTP request at all — instead, it's a reshaped object with renamed and restructured fields. What explains this behavior?
A) This indicates a misconfiguration; non-proxy integrations should always pass the raw request
B) This is expected: a request mapping template written in VTL transformed the raw request into this custom shape before invoking Lambda
C) This means the method is actually using a Mock integration
D) This means IAM authorization failed silently

22. Which of the following correctly distinguishes Lambda proxy integration from Lambda custom (non-proxy) integration in terms of configuration effort?
A) Proxy integration requires mapping templates for every request and response; non-proxy does not
B) Proxy integration passes the request/response through with a fixed envelope shape and requires no mapping templates, while non-proxy integration requires explicit request/response mapping templates for full control
C) Both require identical mapping template configuration
D) Non-proxy integration cannot invoke Lambda functions at all

23. A team wants to implement `OPTIONS` preflight handling for CORS on a REST API resource without incurring any Lambda invocation cost. Which integration type is best suited for the `OPTIONS` method?
A) Lambda proxy integration
B) Mock integration returning the appropriate CORS headers
C) AWS service integration targeting IAM
D) HTTP proxy integration to an external CORS validation service

24. Which of the following is NOT one of API Gateway's supported integration types?
A) Lambda proxy integration
B) AWS service integration
C) Mock integration
D) Direct database connection pooling integration

25. A developer troubleshooting a 502 error on a Lambda-proxy-backed API method discovers the Lambda function's handler returns a plain string instead of the required JSON object with `statusCode`, `headers`, and `body` keys. What is the most direct fix?
A) Switch the method to use IAM authorization instead
B) Modify the Lambda handler to return the properly structured `{statusCode, headers, body}` object
C) Increase the Lambda function's memory allocation
D) Add a usage plan to the method

26. A REST API resource uses an AWS service integration to publish directly to an SQS queue when a POST request is received, with no Lambda function involved. What must be configured to make this work correctly?
A) A Cognito User Pool must be attached to the SQS queue
B) A request mapping template transforming the incoming body into the shape SQS's SendMessage API expects, along with an IAM role granting API Gateway permission to call SQS
C) A WebSocket route selection expression
D) A usage plan with an API key requirement

27. Which of the following scenarios is the strongest fit for choosing a Lambda proxy integration over a Lambda custom (non-proxy) integration?
A) The team wants API Gateway to handle all request/response reshaping via VTL so the Lambda function never sees raw HTTP details
B) The team wants minimal API Gateway configuration overhead and is comfortable parsing the full raw request (headers, query params, body) inside the Lambda function itself
C) The team has no Lambda function and wants to call DynamoDB directly
D) The team needs the response to bypass API Gateway entirely

28. A developer configures an HTTP integration pointing to an internal Application Load Balancer that is only reachable from within a VPC. What API Gateway feature is required to allow the API to reach that private ALB?
A) A Lambda authorizer
B) A VPC Link
C) A usage plan
D) A stage variable

29. Which of the following correctly describes what happens when a Lambda proxy integration's function throws an unhandled exception rather than returning normally?
A) API Gateway silently returns a 200 with an empty body
B) API Gateway typically returns a 502 Internal Server Error to the client, since no valid response envelope was produced
C) API Gateway automatically retries the request up to five times
D) The client receives the raw Lambda stack trace unmodified with a 200 status

30. A team wants to build an API resource that returns different static JSON payloads for different HTTP status code test cases (200, 400, 500) purely for contract testing, without any backend code existing yet for any of the three cases. Which integration type most directly supports this?
A) Lambda proxy integration
B) Mock integration, using configured response templates per status code
C) AWS service integration
D) HTTP proxy integration

### Stages, Stage Variables & Deployment (31–44)

31. A team maintains one REST API definition and wants `dev`, `test`, and `prod` environments to each invoke a different Lambda function alias, without duplicating the API's resources and methods three times. Which API Gateway feature enables this?
A) Separate API Gateway accounts per environment
B) Stage variables referenced inside the integration's target ARN, set to a different value per stage
C) A single hardcoded Lambda ARN shared across all stages
D) Usage plans scoped per environment

32. What does a "deployment" represent in API Gateway, as distinct from a "stage"?
A) A deployment is a snapshot of the API's configuration at a point in time; a stage is a named, addressable reference to a specific deployment
B) A deployment and a stage are the exact same resource under different names
C) A deployment is a billing construct with no relation to API configuration
D) A stage is a snapshot of configuration, while a deployment is the addressable URL

33. A company wants their `dev` stage to run with verbose logging and no response caching, while their `prod` stage runs with minimal logging and caching enabled, using the same underlying API definition. Which API Gateway feature makes this possible?
A) Each stage carries its own independent settings (logging, caching, throttling) even though they reference the same API
B) This requires two entirely separate API Gateway APIs
C) Stage-level settings are global across all stages of an API and cannot differ
D) This can only be achieved using AppSync, not API Gateway

34. Which of the following is the correct syntax for referencing a stage variable named `lambdaAlias` inside an integration's target ARN?
A) `#{stageVariables.lambdaAlias}`
B) `${stageVariables.lambdaAlias}`
C) `{{stageVariables:lambdaAlias}}`
D) `%stageVariables.lambdaAlias%`

35. A team wants a small percentage of production traffic to be routed to a newly deployed API configuration for validation, with the ability to roll back instantly if errors increase, before shifting 100% of traffic. Which capability supports this on a REST API?
A) Stage variables
B) Canary release deployment on a stage
C) A Lambda custom integration
D) A usage plan quota

36. Besides pointing to a different Lambda alias, which of the following is also a valid use of a stage variable?
A) Selecting a different backend HTTP endpoint (e.g., a different ALB DNS name) per stage
B) Encrypting the entire API payload
C) Replacing the need for an authorizer entirely
D) Defining the account-level throttle limit

37. A developer publishes a new version of their Lambda function and updates the `prod` alias to point to it, without touching the API Gateway configuration at all. What effect does this have on the API's `prod` stage, assuming the integration ARN references `${stageVariables.lambdaAlias}` and the `prod` stage variable is set to `prod`?
A) No effect; API Gateway configuration must also be redeployed for any change to take effect
B) The `prod` stage automatically invokes the new Lambda version the alias now points to, with no API Gateway redeployment needed
C) The API automatically reverts to a Mock integration
D) The stage variable must be manually changed to a new alias name every time

38. Which statement best explains why using stage variables to select a Lambda alias is preferable to hardcoding a specific Lambda function version ARN directly in the integration?
A) Hardcoded version ARNs are more secure than aliases
B) Stage variables decouple the API's stage from a specific Lambda code version, letting the alias's target version change (via Lambda's own deployment process) without any API Gateway redeployment
C) Hardcoded version ARNs automatically update themselves
D) Aliases cannot be used in API Gateway integrations at all

39. A team accidentally deploys a breaking change to their `prod` stage. Which of the following most directly limits the blast radius of a bad deployment before it's discovered?
A) Using a canary release on the stage so only a small percentage of traffic hits the new deployment initially
B) Deleting the stage entirely
C) Disabling all authorizers
D) Switching to a WebSocket API

40. What is the relationship between an API's invoke URL and its stage?
A) Each stage has its own distinct invoke URL path segment (e.g., `/dev`, `/prod`) appended to the API's base URL
B) All stages share one single URL with no way to distinguish them
C) Stages have no effect on the invoke URL
D) The invoke URL changes only when a custom domain is configured, never based on stage

41. A company wants to test a new version of an API's configuration against 5% of live production traffic, then increase that to 25%, then 100%, monitoring error rates at each step. Which API Gateway REST API feature is designed exactly for this staged rollout?
A) Usage plans
B) Canary deployment stage settings, adjusting the canary traffic percentage over time
C) CORS configuration
D) A Lambda authorizer

42. Which of the following statements about API Gateway stages is accurate?
A) A stage can have its own throttle settings distinct from another stage's throttle settings on the same API
B) All stages on an API must share identical throttle settings
C) Stages cannot have distinct stage variables from one another
D) A REST API can have at most one stage at any time

43. A developer wants to avoid maintaining three near-identical copies of the same API (one per environment) purely to point at three different backend Lambda aliases. Which combination of features minimizes duplication?
A) Three separate APIs, each fully duplicated per environment
B) One API definition with three stages, each carrying a different stage variable value referenced in the integration ARN
C) One API with no stages at all
D) A single stage shared by all three environments with manual toggling

44. True or False: deploying changes to an API automatically updates every stage simultaneously.
A) True — all stages always reflect the latest deployment automatically
B) False — a deployment must be explicitly associated with (deployed to) a specific stage; other stages continue serving their own last-deployed snapshot until separately redeployed
C) True, but only for HTTP APIs
D) False, because stages cannot be redeployed once created

### Custom Domain Names & Base Path Mapping (45–52)

45. A company wants API consumers to call their API at `api.example.com` instead of the default `execute-api` generated URL. Which API Gateway feature enables this?
A) A usage plan
B) A custom domain name, backed by an ACM certificate
C) A stage variable
D) A Lambda authorizer

46. For an edge-optimized custom domain name on API Gateway, in which AWS Region must the associated ACM certificate be provisioned?
A) The same Region as the API itself, always
B) us-east-1, regardless of the API's actual Region, because the domain is served via CloudFront
C) Any Region; edge-optimized domains have no certificate Region requirement
D) eu-west-1 specifically

47. For a regional custom domain name on API Gateway, in which Region must the ACM certificate be provisioned?
A) Always us-east-1
B) The same Region as the API itself
C) Any Region, since regional domains do not use certificates
D) A Region chosen at random by AWS

48. A company wants `api.example.com/v1` to route to one API's `prod` stage and `api.example.com/v2` to route to a completely different API's `prod` stage, both under the same custom domain. Which feature accomplishes this?
A) Two separate custom domain names, since one domain cannot serve multiple paths
B) Base path mapping, mapping each path segment under the shared custom domain to a specific API and stage
C) A single stage variable shared across both APIs
D) A Lambda authorizer configured to route by path

49. Which of the following is required before a custom domain name for a REST API can be used with HTTPS?
A) A TLS certificate issued or imported via AWS Certificate Manager
B) A Lambda authorizer
C) A usage plan with an associated API key
D) A WebSocket route selection expression

50. A team configures a regional custom domain but mistakenly requests the ACM certificate in us-east-1 while their API and domain are both intended to be regional in eu-west-1. What is the most likely outcome?
A) It works fine; regional domains accept certificates from any Region
B) The domain mapping will fail or be unusable, because a regional custom domain's certificate must be provisioned in the same Region as the API
C) API Gateway automatically relocates the certificate to the correct Region
D) This only affects WebSocket APIs, not REST APIs

51. What is the primary functional difference between an edge-optimized and a regional API Gateway custom domain?
A) Edge-optimized domains are served through CloudFront's global edge network for reduced latency to geographically distributed clients, while regional domains are served directly from the API's Region
B) Regional domains do not support HTTPS
C) Edge-optimized domains cannot use base path mapping
D) There is no functional difference between the two

52. Which of the following statements about base path mappings is accurate?
A) A base path mapping can only ever point to the same API it was originally created for
B) A base path mapping associates a path under a custom domain with a specific combination of an API and one of its stages
C) Base path mappings eliminate the need for stages entirely
D) Base path mappings are exclusive to WebSocket APIs

### Authorizers — IAM/SigV4, Cognito, and Lambda (53–74)

53. A company wants to allow only specific IAM users and roles — including some belonging to a separate, trusted AWS account — to invoke their REST API, with each caller cryptographically signing their requests using their own AWS credentials. Which authorization mechanism fits this requirement?
A) API key authorization
B) IAM authorization (SigV4), combined with a resource policy allowing the trusted account's principals
C) CORS configuration
D) A stage variable restricting access

54. A mobile app authenticates end users via a Cognito User Pool and wants API Gateway to validate the resulting JWT on every API call without writing any custom authorization Lambda code. Which authorizer type should be configured on the API's methods?
A) A Lambda (custom) authorizer
B) A Cognito User Pool authorizer
C) IAM authorization
D) A resource policy alone, with no authorizer

55. A company needs custom authorization logic validating a third-party-issued JWT with proprietary claims that neither IAM nor Cognito authorizers natively understand. Which authorizer type is designed for this kind of bespoke logic?
A) A Lambda (custom) authorizer
B) A Cognito User Pool authorizer
C) A resource policy
D) A usage plan

56. Which of the following best distinguishes a TOKEN-type Lambda authorizer from a REQUEST-type Lambda authorizer?
A) TOKEN-type receives only a bearer token from a specified header; REQUEST-type receives the full request context, including headers, query string parameters, path parameters, and source IP
B) TOKEN-type receives the full request; REQUEST-type receives only a token
C) TOKEN-type cannot return an IAM policy document; only REQUEST-type can
D) There is no functional difference between the two types

57. A Lambda authorizer's authorization decision needs to depend on both a bearer token AND a custom header plus the caller's source IP address. Which Lambda authorizer type should be used?
A) TOKEN type, since it can access all request data by default
B) REQUEST type, since it receives the full request context needed for this decision
C) Neither type can access source IP under any circumstance
D) A Cognito User Pool authorizer, since only it can inspect source IP

58. What must a Lambda authorizer function return to allow or deny a request?
A) A plain HTTP status code only
B) An IAM policy document (Allow/Deny) for the requested resource, optionally with additional context passed to the backend
C) A JWT token that API Gateway re-validates
D) Nothing; Lambda authorizers only log requests and cannot deny them

59. A company notices their Lambda authorizer is being invoked on every single API request, adding latency and cost, even though most callers reuse the same token repeatedly within a short window. Which built-in feature reduces this overhead?
A) Authorizer result caching, keyed by the identity source, with a configurable TTL
B) Switching to a Mock integration
C) Removing the authorizer entirely
D) Enabling response caching for GET methods

60. What is the maximum commonly configurable authorizer cache TTL for a Lambda authorizer's decision, and what does exceeding real-world token validity risk?
A) There is no cache available for Lambda authorizers under any configuration
B) Up to 3600 seconds (1 hour), configurable; setting it too high risks continuing to authorize a request after the underlying token/permissions should have expired or been revoked
C) Exactly 24 hours with no configurability
D) The cache only applies to Cognito User Pool authorizers, never Lambda authorizers

61. A company's official use case (drawn from AWS's own published sample question) is to allow only IAM principals from a separate AWS account to invoke specific methods on their REST API. Which two actions, taken together, correctly satisfy this requirement?
A) Attach a resource policy to the API allowing the external account's IAM principal to call execute-api:Invoke on the relevant resource
B) Attach an IAM permission policy to the calling IAM users/roles in the external account, granting execute-api:Invoke, and sign requests with SigV4
C) Configure a Cognito User Pool in the external account only
D) Configure CORS to allow the external account's domain
E) Purchase an API key for the external account

62. Why is a resource policy alone, without any permission policy on the calling IAM identity, insufficient to grant a caller access to an IAM-authorized API?
A) Resource policies are purely cosmetic and have no actual effect
B) IAM authorization is evaluated using both the resource policy (on the API) and the caller's own identity-based permission policy; both must independently allow the action for cross-account access to succeed
C) Resource policies can only be attached to S3 buckets, never to APIs
D) A resource policy automatically grants full access regardless of the caller's own IAM policy

63. A company wants to restrict API invocation so that only requests originating from a specific VPC endpoint are allowed, regardless of the caller's IAM identity. Which API Gateway feature supports this kind of network-origin-based restriction?
A) A resource policy with a condition restricting the source VPC endpoint
B) A usage plan
C) CORS configuration
D) A stage variable

64. Which of the following is an accurate statement about API keys and their role in API Gateway security?
A) API keys authenticate the caller's identity and should be used as the primary authorization mechanism for sensitive operations
B) API keys identify a caller for usage plan throttling/quota and metering purposes only; they are not an authentication or authorization mechanism
C) API keys are cryptographically signed using SigV4, just like IAM credentials
D) API keys replace the need for HTTPS

65. A company mistakenly believes that requiring an API key on a method is sufficient to secure it against unauthorized access. What is the flaw in this approach?
A) There is no flaw; API keys are a complete security solution
B) API keys only identify the caller for metering/throttling; anyone possessing a valid key can call the method, and API keys provide no cryptographic proof of identity the way IAM SigV4 signing or a validated JWT does
C) API keys automatically expire after every single request, making them inherently secure
D) API keys cannot be used alongside any other authorization mechanism

66. Which authorizer type would be the best fit for a scenario requiring zero custom code, where end users already authenticate through a fully AWS-managed user directory and receive a token to present on each API call?
A) A Cognito User Pool authorizer
B) A Lambda TOKEN authorizer written from scratch
C) A resource policy alone
D) A usage plan

67. A REST API method requires IAM authorization. A developer testing the API with a valid Cognito User Pool JWT in the Authorization header receives a 403 Forbidden. What is the most likely explanation?
A) The method expects a SigV4-signed request using IAM credentials, not a Cognito JWT — a JWT is not valid for IAM-authorized methods
B) The Lambda function is misconfigured
C) The API key is missing
D) The custom domain is misconfigured

68. Which two of the following statements about Lambda authorizers are accurate?
A) A Lambda authorizer can return additional context values that are passed through to the backend integration
B) A Lambda authorizer's decision can be cached to avoid invoking it on every request
C) Lambda authorizers can only be used with HTTP APIs, never REST APIs
D) Lambda authorizers cannot access query string parameters under any configuration
E) A Lambda authorizer always bypasses IAM policy evaluation entirely

69. A company's REST API needs to support two different classes of caller on the same set of endpoints: internal services calling with IAM-signed requests, and end users calling with Cognito-issued JWTs. Which approach is generally required in API Gateway to support both authorization schemes?
A) API Gateway allows only a single authorizer per method, so the team typically configures separate methods/resources per auth type, or uses a Lambda authorizer implementing custom logic to branch on the credential type presented
B) This is impossible with any AWS service
C) IAM authorization automatically also validates Cognito JWTs
D) A single resource policy handles both cases with no additional configuration

70. What does the "identity source" configuration on a Lambda authorizer define?
A) The IAM role the Lambda function assumes
B) The specific request element (e.g., a header, or a combination of parameters) API Gateway extracts and uses both to invoke the authorizer and as the cache key
C) The Region the authorizer Lambda function runs in
D) The DynamoDB table storing authorization decisions

71. Which statement correctly describes how a resource policy and an identity-based (permission) policy interact for an IAM-authorized API call?
A) Only the resource policy needs to allow the action; the identity-based policy is irrelevant
B) Only the identity-based policy needs to allow the action; the resource policy is irrelevant
C) Both the resource policy (attached to the API) and the identity-based policy (attached to the caller) must permit the action for the request to succeed
D) Neither policy has any bearing on IAM-authorized API calls

72. A Lambda REQUEST-type authorizer needs to make its authorization decision based on a custom header called `x-tenant-id` as well as the request's query string. Which authorizer type correctly supports reading both of these?
A) TOKEN type only
B) REQUEST type, since it receives the full request context including headers and query string parameters
C) Neither type can read custom headers
D) Only a Cognito User Pool authorizer can read custom headers

73. Why might a company choose IAM authorization with a resource policy over a Lambda authorizer for controlling access to internal, service-to-service API calls within their own AWS environment?
A) IAM authorization leverages existing AWS credentials and policies without requiring any custom authorization code to write, test, or maintain
B) IAM authorization is the only mechanism capable of using SigV4 signing
C) Lambda authorizers cannot be used for service-to-service calls under any circumstance
D) IAM authorization is always faster than a cached Lambda authorizer decision

74. A team configures a Lambda TOKEN authorizer but the client sends the bearer token in a custom header named `x-auth-token` rather than the standard `Authorization` header. What must be configured for the authorizer to correctly locate the token?
A) Nothing; TOKEN authorizers always default to reading only the `Authorization` header with no override
B) The authorizer's identity source must be configured to point at the `x-auth-token` header instead of the default
C) The client must switch to a REQUEST-type flow automatically
D) This configuration is not possible under any circumstance

### Request/Response Transformation, Mapping Templates & Validation (75–86)

75. What language is used to write API Gateway mapping templates for non-proxy integrations?
A) Python
B) VTL (Velocity Template Language)
C) YAML
D) GraphQL SDL

76. A REST API method needs to reject any incoming request missing a required `orderId` query string parameter, before the request reaches the backend at all. Which API Gateway feature accomplishes this?
A) A mapping template alone, with no other configuration
B) Request validation, configured to require specific request parameters
C) A usage plan quota
D) A stage variable

77. In addition to validating required parameters, what else can API Gateway's request validation check against a defined model?
A) Whether the request body conforms to a JSON Schema model
B) Whether the caller's AWS account has sufficient billing credit
C) Whether the Lambda function's code has any syntax errors
D) Whether the response will be cached

78. What is a key operational benefit of rejecting malformed requests via request validation before they reach a Lambda-backed integration?
A) It removes the need for any authorizer
B) It avoids unnecessary Lambda invocations (and their associated cost and latency) for requests that would fail anyway
C) It automatically fixes the malformed request and forwards a corrected version
D) It disables logging for invalid requests

79. A response mapping template is used in a non-proxy integration to transform a DynamoDB `GetItem` response (which includes DynamoDB's native attribute-value type wrappers like `{"S": "value"}`) into a clean, simplified JSON object for the client. What is this process an example of?
A) Request validation
B) Response transformation via a mapping template
C) A resource policy
D) A usage plan

80. Which of the following is true about request validation support across API Gateway API types?
A) REST APIs support full request validation against models; HTTP APIs have limited or no equivalent support
B) HTTP APIs have more advanced request validation than REST APIs
C) Neither API type supports any form of request validation
D) Request validation is exclusive to WebSocket APIs

81. A mapping template references `$input.path('$.item')` to extract a specific field from an incoming JSON request body. What is this syntax part of?
A) A Cognito User Pool schema
B) VTL mapping template syntax used to access parts of the incoming request within API Gateway
C) A Lambda proxy integration's automatic parsing (no template needed)
D) A CORS configuration directive

82. Which of the following integration types typically do NOT use VTL mapping templates at all?
A) AWS service integration
B) Lambda custom (non-proxy) integration
C) Lambda proxy integration
D) HTTP non-proxy integration

83. A team wants API Gateway to transform an incoming client request body's field names (e.g., renaming `customer_name` to `customerName`) before forwarding to a Lambda function using a non-proxy integration. Which mechanism accomplishes this transformation?
A) A request mapping template written in VTL
B) A usage plan
C) A resource policy
D) A stage variable

84. What happens to a request that fails API Gateway's configured request validation (e.g., missing a required parameter)?
A) It is forwarded to the backend anyway, with a warning logged
B) API Gateway rejects the request immediately with an error response, without invoking the backend integration
C) It is queued and retried indefinitely
D) It is silently dropped with no response sent to the client

85. Which of the following correctly describes the two-part structure typically used for transforming data in a non-proxy integration?
A) A request mapping template shapes what the backend receives; a response mapping template shapes what the client receives back
B) Only a single combined mapping template exists, shaping both directions simultaneously with no distinction
C) Mapping templates only apply to the request direction; responses are always passed through unmodified
D) Mapping templates are exclusively used for authorization decisions

86. A company's Lambda proxy integration receives malformed input because there is no request validation configured, resulting in unnecessary Lambda invocations for garbage requests. Which change most directly reduces this waste, keeping the proxy integration but reducing invalid invocations?
A) Switching to a WebSocket API
B) Enabling API Gateway request validation (required parameters and/or a body model) so invalid requests are rejected before Lambda is invoked
C) Removing the Lambda function entirely
D) Adding a resource policy allowing all traffic

### Throttling, Usage Plans & API Keys (87–96)

87. A company wants to give a specific partner a maximum of 1,000 requests per day against their API, with a burst limit of 50 requests per second, tracked separately from other callers. Which API Gateway feature combination achieves this?
A) A resource policy alone
B) A usage plan with a quota (1,000/day) and throttle limits (burst 50 rps), associated with an API key issued to that partner
C) A Cognito User Pool with a custom attribute
D) A stage variable set to the partner's identifier

88. What is the purpose of requiring an API key on a specific method, separate from any authorizer configured on that same method?
A) The API key replaces the need for any authorization entirely
B) The API key associates the request with a specific usage plan for throttling/quota enforcement and usage metering, while authorization (if configured) is handled independently by an authorizer
C) The API key encrypts the request body
D) The API key is only relevant for WebSocket APIs

89. Which of the following throttle limit levels can be configured within API Gateway?
A) Only a single Region-wide default; no finer-grained control exists
B) Account-level default limits, with the ability to override at the stage or individual method level
C) Only per-API-key limits, with no stage or method-level control
D) Throttling can only be configured through a separate AWS WAF rule, never natively

90. A request arrives with a missing or invalid API key on a method configured to require one, associated with a usage plan. What is the expected result?
A) The request succeeds normally since usage plans are advisory only
B) The request is rejected, since a valid API key tied to an active usage plan is required for that method
C) The request is automatically retried with a temporary key
D) The request bypasses throttling entirely

91. Which two of the following statements about usage plans and API keys are accurate?
A) A usage plan can be associated with multiple API keys, each representing a different caller
B) API keys alone, without an associated usage plan, are the primary authentication mechanism recommended for production APIs
C) A usage plan can define both a request quota (e.g., per day/month) and throttle limits (steady-state rate and burst)
D) Usage plans automatically provide encryption at rest for the API's data
E) API keys cryptographically sign each request using the caller's private key

92. A team wants different throttle limits for their `GET /orders` method versus their `POST /orders` method on the same API stage. Is this level of granularity supported?
A) No, all methods on a stage must share identical throttle settings
B) Yes, API Gateway supports throttle limit overrides at the individual method level, in addition to stage-level and account-level defaults
C) Only if each method is on a separate API entirely
D) Only for HTTP APIs, never REST APIs

93. Why would a company use a usage plan and API keys even though the API also uses a Cognito User Pool authorizer for authentication?
A) Usage plans and authorizers are mutually exclusive; only one can be configured
B) Authorizers handle who is allowed to call the API, while usage plans/API keys separately handle metering and throttling per caller tier (e.g., free tier vs. paid tier) — the two serve complementary purposes
C) Usage plans replace the need for the Cognito authorizer entirely
D) API keys automatically become the JWT used by the Cognito authorizer

94. A burst of traffic exceeds the account-level default steady-state throttle limit for a Region. What is the typical behavior?
A) API Gateway silently processes all requests regardless of the limit
B) API Gateway begins returning 429 Too Many Requests responses for requests exceeding the throttle limit
C) API Gateway automatically and permanently raises the account limit
D) API Gateway shuts down the API entirely until the next billing cycle

95. Which of the following is the correct association order/model for enforcing per-partner API usage limits?
A) API key → associated with a usage plan → usage plan associated with specific API stages
B) Usage plan → associated with a resource policy → resource policy associated with a Lambda function
C) Stage variable → associated with an IAM role → IAM role associated with a Cognito pool
D) Mapping template → associated with a WebSocket route

96. A developer wants to track and limit usage per external customer without requiring those customers to have AWS IAM credentials or Cognito accounts. Which mechanism best fits this need?
A) IAM authorization with a resource policy per customer
B) API keys, each issued per customer, tied to individual usage plans
C) A Cognito User Pool per customer
D) A Lambda authorizer requiring AWS SigV4

### CORS (97–104)

97. A single-page web application hosted at `https://app.example.com` calls an API hosted at `https://api.example.com` directly from browser JavaScript, and the request fails in the browser console with a CORS-related error even though the server-side logs show the request was processed successfully. What does this indicate?
A) The backend logic failed silently
B) The browser blocked the response from being used by the page's JavaScript because the API's response did not include the required CORS headers, even though the request itself was actually processed
C) The API key was invalid
D) The custom domain's certificate expired

98. Which HTTP method does a browser typically send first, as a "preflight" check, before making a cross-origin request with custom headers or certain content types?
A) GET
B) OPTIONS
C) PATCH
D) TRACE

99. On a REST API, which integration type is commonly used to handle the CORS preflight `OPTIONS` request without invoking any backend logic?
A) Lambda proxy integration
B) Mock integration, configured to return the appropriate Access-Control-Allow-* headers
C) AWS service integration
D) HTTP proxy integration

100. A REST API method uses a Lambda proxy integration. The team enables "CORS" via the API Gateway console wizard, but browser calls to this specific method still fail with a CORS error, even though the `OPTIONS` preflight now succeeds. What is the most likely cause?
A) The console wizard does not modify what the actual Lambda function returns; the Lambda function's own response must also include the CORS headers, since proxy integration passes the function's response straight through
B) The wrong AWS Region was selected
C) CORS cannot be resolved for proxy integrations under any configuration
D) The custom domain must be removed

101. Which of the following headers is essential in a CORS response to indicate which origins are permitted to access the resource?
A) X-Amz-Date
B) Access-Control-Allow-Origin
C) Content-Type
D) X-Forwarded-For

102. How does CORS configuration differ between REST APIs and HTTP APIs in API Gateway?
A) REST APIs require manually creating/configuring an OPTIONS method and headers (or using the console wizard); HTTP APIs offer a simpler, built-in CORS configuration block on the API itself
B) HTTP APIs do not support CORS at all
C) REST APIs automatically handle CORS with zero configuration
D) There is no difference; both are configured identically

103. Is CORS a server-side security control that prevents unauthorized backend access, or a browser-enforced restriction?
A) It is a server-side authorization control equivalent to IAM
B) It is a browser-enforced restriction on cross-origin JavaScript access to responses; it does not prevent a request from reaching or being processed by the backend
C) It is enforced exclusively by API Gateway's authorizers
D) It has no relationship to browsers at all and applies only to server-to-server calls

104. Which two of the following statements about CORS in API Gateway are accurate?
A) A Lambda proxy integration's response must itself include CORS headers, since API Gateway does not inject them automatically into the function's output
B) CORS preflight requests are commonly satisfied using a Mock integration on the OPTIONS method
C) CORS is enforced by API Gateway's authorizer layer, not by browsers
D) Enabling CORS automatically disables all authorizers on the resource
E) CORS has no bearing on browser-based JavaScript API calls

### WebSocket APIs (105–112)

105. A company is building a real-time multiplayer game backend requiring persistent, full-duplex connections where the server can push state updates to clients at any time without the client polling. Which API Gateway API type is designed for this?
A) REST API
B) HTTP API
C) WebSocket API
D) A REST API with long-polling configured

106. In a WebSocket API, which special route fires when a client first establishes a connection, commonly used to authorize the connection and store its connection ID?
A) $default
B) $connect
C) $disconnect
D) $init

107. Which special WebSocket API route handles incoming messages that do not match any other defined route?
A) $connect
B) $disconnect
C) $default
D) $catch-all

108. What determines which backend integration handles an incoming WebSocket message, when the message body can represent different types of actions?
A) The client's IP address exclusively
B) The route selection expression, which extracts a value (e.g., from a field in the message body) to select the matching route
C) The stage variable of the API automatically
D) WebSocket APIs cannot route different message types differently

109. A backend Lambda function needs to push a message to a specific, already-connected WebSocket client from outside the normal request/response flow (e.g., in response to a database change). Which mechanism does it use to deliver that message?
A) A standard HTTP GET request to the client's IP address
B) The API Gateway Management API's PostToConnection action, referencing the stored connection ID
C) A Lambda authorizer
D) A stage variable update

110. Why do WebSocket API implementations commonly store active connection IDs in a persistent store such as DynamoDB?
A) DynamoDB is required by AWS for all WebSocket APIs with no alternative
B) Connection IDs must be tracked somewhere so a backend process can later target specific connected clients for server-initiated pushes, since the WebSocket connection itself is stateful and ephemeral per Lambda invocation
C) DynamoDB automatically becomes the WebSocket transport layer
D) This step is unnecessary; API Gateway retains this mapping without any application-level storage

111. Which route fires when a WebSocket client's connection is closed, commonly used to clean up stored connection state?
A) $connect
B) $disconnect
C) $default
D) $close

112. A team is deciding between a raw WebSocket API and AWS AppSync for a real-time feature. Which factor would most directly favor choosing AppSync instead of hand-building a WebSocket API?
A) The data and events are naturally GraphQL-shaped, and the team wants connection tracking and subscription fan-out managed automatically rather than building a DynamoDB connections table and PostToConnection logic themselves
B) The team needs a completely custom, non-GraphQL binary protocol with no schema
C) AppSync does not support any form of real-time push
D) WebSocket APIs are always cheaper and simpler than AppSync in every scenario

### AWS AppSync — GraphQL, Resolvers, Data Sources & Real-Time (113–134)

113. What fundamental difference distinguishes a GraphQL API (such as AppSync) from a typical REST API in terms of client data fetching?
A) GraphQL clients specify exactly which fields they want in a single query, avoiding the over-fetching and under-fetching common with fixed-shape REST endpoints
B) GraphQL APIs can only return XML, never JSON
C) GraphQL APIs require a separate endpoint for every possible field combination, just like REST
D) There is no meaningful difference between GraphQL and REST for client data fetching

114. In an AppSync GraphQL schema, which type defines the operations used to read data?
A) Mutation
B) Query
C) Subscription
D) Directive

115. Which AppSync schema type defines operations used to write or modify data?
A) Query
B) Mutation
C) Subscription
D) Interface

116. Which AppSync schema type defines real-time, push-based operations that notify subscribed clients when specified events occur?
A) Query
B) Mutation
C) Subscription
D) Fragment

117. What is the role of an AppSync resolver?
A) It defines how a specific schema field is fulfilled by connecting the GraphQL operation to a configured data source
B) It exclusively handles user authentication with no relation to data fetching
C) It replaces the schema entirely
D) It is only used for real-time subscriptions, never for queries or mutations

118. Which of the following is a valid AppSync data source type?
A) DynamoDB
B) Lambda
C) An HTTP endpoint
D) All of the above are valid AppSync data source types

119. What are the two primary implementation styles available for writing AppSync resolvers?
A) Python and Node.js runtime resolvers
B) VTL (Velocity Template Language) mapping templates and JavaScript (APPSYNC_JS) resolvers
C) YAML-based and XML-based resolvers
D) SQL and NoSQL resolvers

120. In a JavaScript (APPSYNC_JS) resolver, which two functions are typically exported to define the resolver's behavior?
A) init() and destroy()
B) request() and response()
C) query() and mutate()
D) connect() and disconnect()

121. A resolver needs to perform several sequential operations for a single GraphQL field — first validating input, then writing to DynamoDB, then triggering a notification. Which AppSync resolver capability supports chaining multiple functions together for one field?
A) A pipeline resolver
B) A Mock integration
C) A stage variable
D) A base path mapping

122. Which AppSync data source would be most appropriate for querying an Aurora Serverless relational database from a GraphQL field?
A) The DynamoDB data source
B) The relational database data source, using the RDS Data API
C) The HTTP data source only
D) The None (local) data source

123. How does an AppSync subscription typically notify a connected client when a relevant mutation occurs?
A) The client must poll the API repeatedly to check for changes
B) AppSync automatically pushes the update to subscribed clients over a WebSocket connection it manages, without the client needing to poll
C) The client must manually open a separate REST API connection
D) Subscriptions require the client to re-authenticate before every notification

124. Which schema directive commonly links a Subscription field to the Mutation(s) that should trigger it in AppSync?
A) @aws_subscribe
B) @connect
C) @aws_auth
D) @mock

125. What operational burden does AppSync remove, compared to implementing equivalent real-time functionality on a raw WebSocket API?
A) AppSync removes the need for any backend data source whatsoever
B) AppSync manages the underlying WebSocket transport, connection tracking, and fan-out to subscribed clients automatically, rather than requiring the team to build a connections table and manual push logic
C) AppSync removes the need for a schema
D) AppSync removes the need for any authorization configuration

126. Which AWS Amplify feature works alongside AppSync to support offline-first mobile/web applications that read and write data locally without connectivity, syncing later?
A) Amplify DataStore
B) Amplify Console only
C) AWS CodeArtifact
D) AWS Cloud9

127. In AppSync's conflict resolution for offline sync, which strategy uses a version field (e.g., `_version`) to reject writes based on stale data?
A) Auto Merge
B) Optimistic Concurrency
C) Lambda-based custom resolution
D) Eventual Consistency Override

128. Which AppSync conflict resolution strategy allows a custom Lambda function to implement business-specific logic for resolving conflicting offline/online writes?
A) Auto Merge
B) Optimistic Concurrency only
C) Lambda-based custom resolution
D) None; Lambda cannot be used for conflict resolution

129. Which of the following authorization modes can be configured for an AppSync API?
A) API key
B) IAM
C) Amazon Cognito User Pools and OpenID Connect (OIDC)
D) All of the above are valid AppSync authorization modes

130. Can an AppSync API be configured with more than one authorization mode simultaneously (e.g., API key for public reads and Cognito for authenticated mutations)?
A) No, only a single authorization mode may ever be configured per API
B) Yes, AppSync supports a primary authorization mode plus additional authorization modes, with schema directives controlling which fields/types use which mode
C) Only if the API has no schema defined
D) Only for Lambda data sources

131. A public marketing website needs read-only, unauthenticated access to a subset of AppSync data with no user sign-in required, while authenticated mutations require a logged-in user. Which authorization mode is best suited for the public read-only portion?
A) IAM
B) API key
C) OIDC exclusively
D) Cognito User Pools exclusively, with no anonymous access option

132. Which two of the following are accurate statements about AWS AppSync?
A) AppSync resolvers can be implemented using either VTL mapping templates or JavaScript (APPSYNC_JS)
B) AppSync only supports a single hardcoded data source type: DynamoDB
C) AppSync subscriptions require clients to manually manage WebSocket connection IDs, identical to a raw WebSocket API
D) A pipeline resolver can chain multiple functions together to fulfill a single GraphQL field
E) AppSync cannot be combined with Cognito User Pools for authorization

133. A company wants a Lambda data source in AppSync to implement complex business logic that spans multiple backend calls (e.g., checking inventory, then charging a payment provider, then writing an order) for a single `Mutation.placeOrder` field. Why is a Lambda data source well suited here compared to a direct DynamoDB data source?
A) Lambda data sources cannot be used for mutations, only queries
B) A Lambda data source allows arbitrary custom code and multiple downstream calls within a single resolver invocation, versus a direct DynamoDB resolver limited to a single table operation
C) DynamoDB data sources are always faster for this exact use case
D) Lambda data sources bypass the schema entirely

134. Which of the following is the most accurate summary comparison between choosing AppSync versus API Gateway (REST/HTTP) for a new API?
A) AppSync is strictly superior in every scenario and should always be chosen over API Gateway
B) AppSync fits naturally when clients need flexible, field-level queries and/or built-in real-time subscriptions over a GraphQL schema; API Gateway fits naturally for traditional REST-style request/response APIs, especially when usage plans, resource policies, or private VPC access are required
C) API Gateway cannot integrate with Lambda, unlike AppSync
D) AppSync cannot use IAM authorization, unlike API Gateway

### Integrative Scenarios (135–124 continued)

135. A company's security review of their REST API finds: IMDSv1-style long-lived credentials are not applicable here, but the API currently has no resource policy restricting callers, uses only an API key (no authorizer) on a sensitive `DELETE /accounts/{id}` method, and has CORS wide open to `*` including credentials. Which combination of fixes most directly addresses the actual security gaps?
A) Add an IAM or Cognito authorizer to the sensitive method (since an API key alone isn't authentication), add a resource policy scoping allowed callers, and tighten the CORS origin configuration instead of allowing `*` with credentials
B) Only fix the CORS configuration; the other two findings are not real risks
C) Remove the API key entirely and add nothing else
D) Add a stage variable to encrypt the request

136. A retail company needs three things from their API layer: (1) a public REST API with usage plans limiting free-tier partners to 100 requests/day, (2) internal service-to-service calls authorized via IAM/SigV4 with a resource policy scoping which internal accounts can call it, and (3) a real-time order-status feed pushed to the customer's mobile app the instant status changes. Which combination of AWS services/features satisfies all three needs?
A) A single WebSocket API handling all three requirements identically
B) A REST API with a usage plan/API keys for partners and IAM authorization plus a resource policy for internal calls, combined with AppSync (or a WebSocket API) for the real-time order-status subscription feed
C) AppSync alone, since it can enforce usage plans identically to API Gateway
D) A Lambda function with no API Gateway or AppSync involved at all

137. A team deploying a new API version wants to: minimize duplicated resources across dev/test/prod, avoid breaking existing mobile clients during rollout, and test a small percentage of production traffic against the new version before full cutover. Which combination of API Gateway features addresses all three goals?
A) Stage variables (to point each environment's stage at the right Lambda alias) combined with a canary release deployment on the prod stage (to gradually shift traffic to the new version)
B) A single stage with no variables and no canary support
C) Three entirely separate APIs with no shared configuration
D) A resource policy alone, with no stages or canary settings

138. A company migrating from a REST API to an HTTP API for cost savings discovers their existing API relies on usage plans with per-partner API keys and JSON Schema request validation. What should they conclude?
A) HTTP APIs fully support both features, so the migration can proceed with no changes
B) These two specific features (usage plans/API keys and full request validation) are not supported by HTTP APIs, so the team must either keep those endpoints on REST API or re-architect around HTTP API's more limited feature set
C) They must delete the usage plans and accept unlimited access from all partners
D) HTTP APIs will automatically convert usage plans to a different mechanism transparently

139. A GraphQL API built on AppSync needs to support: public unauthenticated read access to product listings, authenticated Cognito-based access for placing orders, and secure backend-to-backend calls from an internal Lambda pipeline using AWS credentials. Which AppSync configuration satisfies all three needs simultaneously?
A) A single authorization mode cannot satisfy this, so multiple auth modes must be configured: API key for public reads, Cognito User Pools for authenticated mutations, and IAM for internal backend calls
B) Only IAM can be configured, and all three use cases must share IAM credentials
C) AppSync requires a separate API per authorization mode
D) API key alone satisfies all three requirements

142. A developer is debugging a REST API where the Lambda proxy integration intermittently returns 502 errors under specific inputs, while other inputs succeed normally. Investigation shows the failing inputs trigger a code path where the Lambda handler returns a bare Python dictionary without the required envelope. Which fix directly resolves the intermittent 502s?
A) Ensure every code path in the handler returns the `{statusCode, headers, body}` structure consistently, including error-handling branches
B) Increase the API's throttle limit
C) Add a stage variable
D) Switch to a Mock integration for all methods

143. A company's Lambda authorizer occasionally denies legitimate users immediately after a permissions change is made in their identity provider, because the previous Allow decision is still cached. What adjustment most directly reduces this staleness window while still retaining some caching benefit?
A) Reduce the authorizer's cache TTL to a shorter duration that better balances staleness risk against invocation overhead
B) Disable IAM entirely
C) Switch the method to a Mock integration
D) Add a usage plan quota

144. Reflecting on this module as a whole, which single statement best captures the recurring theme across stage variables, resource policies, request validation, and AppSync's multi-mode authorization?
A) API Gateway and AppSync configuration is rigid and offers no environment- or caller-specific flexibility
B) Both services are built around flexibly separating "one API/schema definition" from "who can call it, how much they can call it, and which backend/environment it targets" — stages/stage variables handle environment targeting, resource policies/authorizers handle callers, and usage plans/request validation handle traffic quality and volume
C) Only IAM matters for either service; all other mechanisms are decorative
D) AppSync and API Gateway are functionally identical in every respect

---

## Answer Key & Explanations

1. B — Lowest latency/cost with only basic Lambda-proxy needs, no advanced features, is the classic HTTP API fit.
2. B — Usage plans, request validation, and response caching are REST API features not available on HTTP APIs.
3. B — Usage plans and API keys are supported on REST APIs but not on HTTP APIs.
4. B — Private (VPC-endpoint-only) APIs are a REST API feature.
5. B — Migrating to HTTP API gains latency/cost benefits but loses usage plans, API keys, validation, and caching.
6. A — HTTP APIs include a native JWT (OIDC/OAuth2) authorizer with no custom Lambda code required.
7. B — Canary release deployments are a REST API stage feature, not available on HTTP APIs.
8. B — HTTP API meets all stated needs (proxy integration, IAM auth) at lower cost/latency than REST API.
9. B — Only REST APIs offer built-in per-stage response caching.
10. B — Resource policies are supported on REST APIs, not HTTP APIs.
11. A & B — REST APIs uniquely support usage plans/API keys, and HTTP APIs generally offer lower latency/cost.
12. B — Full JSON Schema model request validation is a REST API capability not available on HTTP APIs.
13. B — Passing the raw request as a single event with a fixed response envelope defines Lambda proxy integration.
14. B — A response missing the required envelope shape causes API Gateway to return a 502.
15. C — AWS service integration lets API Gateway call DynamoDB (or other AWS APIs) directly via mapping templates.
16. B — Mock integration returns a static response without invoking any backend.
17. B — The proxy integration response's "body" must be a JSON-stringified string.
18. B — Lambda custom (non-proxy) integration uses mapping templates for full request/response reshaping.
19. A — HTTP integrations can target external/on-prem systems or other APIs, often via a VPC Link for private targets.
20. B — A Mock integration always returns the same static response since no backend logic executes.
21. B — A VTL request mapping template reshaped the raw request before it reached Lambda, as expected in non-proxy integration.
22. B — Proxy integration needs no mapping templates; non-proxy requires explicit request/response templates for control.
23. B — A Mock integration is the standard, cost-free way to handle OPTIONS preflight responses.
24. D — "Direct database connection pooling integration" is not a real API Gateway integration type.
25. B — The Lambda handler must return the structured `{statusCode, headers, body}` object to avoid a 502.
26. B — A mapping template shaping the SQS request body plus an IAM role permitting API Gateway to call SQS are both required.
27. B — Proxy integration minimizes API Gateway configuration at the cost of the Lambda function handling raw request parsing itself.
28. B — A VPC Link is required to let API Gateway reach a private, VPC-only backend like an internal ALB.
29. B — An unhandled Lambda exception in a proxy integration typically results in a 502 to the client.
30. B — A Mock integration with per-status-code response templates supports exactly this contract-testing use case.
31. B — Stage variables referenced in the integration ARN let one API definition target different Lambda aliases per stage.
32. A — A deployment is a configuration snapshot; a stage is a named, addressable reference to a specific deployment.
33. A — Each stage independently carries its own logging, caching, and throttling settings.
34. B — `${stageVariables.lambdaAlias}` is the correct syntax for referencing a stage variable in an integration ARN.
35. B — Canary release deployment settings on a stage support gradual, percentage-based traffic shifting with rollback.
36. A — Stage variables can also select different backend HTTP endpoints per stage, not just Lambda aliases.
37. B — Because the alias itself moved to point at the new version, the stage automatically invokes the new version with no API Gateway redeployment needed.
38. B — Stage variables decouple the stage from a specific Lambda version, letting alias updates apply without redeploying the API.
39. A — A canary release limits the blast radius by exposing the new deployment to only a percentage of traffic initially.
40. A — Each stage has its own path segment appended to the API's base invoke URL.
41. B — Canary deployment settings allow exactly this kind of staged percentage rollout with monitoring at each step.
42. A — Stages can have independent throttle settings from one another on the same API.
43. B — One API with per-stage stage variables referencing the integration ARN avoids duplicating resources across environments.
44. B — A deployment must be explicitly deployed to a given stage; other stages are unaffected until separately redeployed.
45. B — A custom domain name backed by an ACM certificate provides a friendly, branded API URL.
46. B — Edge-optimized domains are served via CloudFront, which requires the ACM certificate to be in us-east-1.
47. B — Regional domains require the ACM certificate to be in the same Region as the API.
48. B — Base path mapping associates a path segment under a shared custom domain with a specific API and stage.
49. A — An ACM-issued or imported TLS certificate is required for HTTPS on a custom domain.
50. B — A regional domain's certificate must match the API's own Region; a mismatched Region breaks the mapping.
51. A — Edge-optimized domains route through CloudFront's edge network; regional domains serve directly from the API's Region.
52. B — A base path mapping ties a custom domain path to a specific API and one of its stages.
53. B — IAM authorization (SigV4) combined with a resource policy allowing the trusted account's principals is the correct mechanism.
54. B — A Cognito User Pool authorizer natively validates the JWT with no custom Lambda code required.
55. A — A Lambda (custom) authorizer is designed for bespoke logic like validating a proprietary third-party JWT.
56. A — TOKEN type gets only the bearer token; REQUEST type gets the full request context.
57. B — REQUEST type is needed since the decision depends on more than just the token (custom header, source IP).
58. B — A Lambda authorizer must return an IAM policy document (Allow/Deny), optionally with extra context.
59. A — Authorizer result caching (keyed by identity source, with a TTL) avoids invoking the authorizer on every request.
60. B — The cache TTL is configurable up to 3600 seconds; setting it too high risks stale authorization decisions outliving real permission changes.
61. A & B — A resource policy allowing the external principal, plus a permission policy and SigV4 signing on the caller's side, together satisfy cross-account IAM access — mirroring AWS's own official sample question.
62. B — Both the resource policy and the caller's identity-based policy must independently allow the action for cross-account IAM authorization to succeed.
63. A — A resource policy with a source VPC endpoint condition restricts invocation by network origin regardless of IAM identity.
64. B — API keys identify a caller for usage plan metering/throttling only, not authentication or authorization.
65. B — An API key provides no cryptographic identity proof; anyone holding the key can call the method, unlike SigV4 or a validated JWT.
66. A — A Cognito User Pool authorizer requires no custom code when using AWS's own managed user directory.
67. A — IAM-authorized methods require SigV4-signed requests, not a Cognito-issued JWT, causing a 403 when a JWT is presented instead.
68. A & B — Lambda authorizers can pass extra context to the backend and support caching their decision.
69. A — API Gateway ties one authorizer per method, so mixed auth schemes typically require separate methods/resources or custom Lambda authorizer branching logic.
70. B — The identity source defines which request element is extracted for invoking the authorizer and used as the cache key.
71. C — Both the resource policy and the caller's identity-based policy must permit the action for an IAM-authorized call to succeed.
72. B — REQUEST-type authorizers receive the full request context, including custom headers and query string parameters.
73. A — IAM authorization reuses existing AWS credentials/policies, avoiding custom authorization code entirely.
74. B — The authorizer's identity source must be reconfigured to point at the custom header instead of the default Authorization header.
75. B — VTL (Velocity Template Language) is used for API Gateway's non-proxy mapping templates.
76. B — Request validation configured to require specific parameters rejects requests missing them before the backend is invoked.
77. A — Request validation can also check the request body against a defined JSON Schema model.
78. B — Rejecting malformed requests early avoids unnecessary Lambda invocation cost and latency.
79. B — Reshaping a backend's raw response into a client-friendly format via a mapping template is response transformation.
80. A — REST APIs support full model-based request validation; HTTP APIs have limited or no equivalent.
81. B — `$input.path(...)` is VTL mapping template syntax for extracting values from the incoming request.
82. C — Lambda proxy integration passes the request/response through directly and does not use VTL mapping templates.
83. A — A request mapping template written in VTL can rename/restructure fields before forwarding to the backend.
84. B — A request failing validation is rejected immediately by API Gateway without invoking the backend.
85. A — A request mapping template shapes the backend-bound data; a response mapping template shapes the client-bound data.
86. B — Enabling request validation filters out malformed requests before they trigger unnecessary Lambda invocations.
87. B — A usage plan with a defined quota and throttle limits, tied to an API key, enforces exactly this per-partner limit.
88. B — The API key associates the request with a usage plan for throttling/quota/metering, separate from any authorizer's authentication role.
89. B — Throttle limits can be set at the account-level default and overridden at the stage or method level.
90. B — A missing/invalid required API key causes the request to be rejected under a method requiring one.
91. A & C — A usage plan can have multiple associated API keys, and it can define both quota and throttle limits.
92. B — API Gateway supports throttle overrides at the individual method level beyond stage/account defaults.
93. B — Authorizers control who may call the API; usage plans/API keys separately control metering and throttling tiers — complementary, not redundant.
94. B — Exceeding the throttle limit results in 429 Too Many Requests responses for the excess requests.
95. A — The correct model is API key → usage plan → usage plan applied to specific API stages.
96. B — API keys tied to individual usage plans let you track/limit usage per external customer without requiring IAM or Cognito identities for them.
97. B — CORS is a browser-side restriction; the request may have succeeded server-side while the browser still blocks the response from JS.
98. B — Browsers send an OPTIONS preflight request before certain cross-origin requests.
99. B — A Mock integration is the standard way to answer OPTIONS preflight requests with the needed CORS headers.
100. A — In proxy integration, the Lambda function's own response must include CORS headers; the console wizard alone doesn't inject them into the function's output.
101. B — Access-Control-Allow-Origin specifies which origins are permitted to access the response.
102. A — REST APIs require manual/wizard-based OPTIONS + header configuration; HTTP APIs offer a simpler built-in CORS block.
103. B — CORS is enforced by browsers to restrict cross-origin JS access to responses; it doesn't block the backend from processing the request.
104. A & B — Proxy integration responses must include their own CORS headers, and Mock integrations commonly satisfy OPTIONS preflight requests.
105. C — WebSocket APIs support persistent, full-duplex, server-push-capable connections.
106. B — The $connect route fires when a client establishes a new WebSocket connection.
107. C — The $default route handles messages that don't match any other defined route.
108. B — The route selection expression extracts a value from the message to determine which route/integration handles it.
109. B — PostToConnection on the API Gateway Management API delivers a message to a specific stored connection ID.
110. B — Connection IDs must be persisted somewhere (e.g., DynamoDB) so a separate backend process can target specific clients later.
111. B — The $disconnect route fires when a connection closes, commonly used for cleanup.
112. A — GraphQL-shaped data plus a desire to avoid building connection tracking/fan-out favors AppSync over a raw WebSocket API.
113. A — GraphQL clients request exactly the fields they need, avoiding REST's over-fetching/under-fetching.
114. B — Query defines read operations in a GraphQL schema.
115. B — Mutation defines write/modify operations in a GraphQL schema.
116. C — Subscription defines real-time, push-based operations for subscribed clients.
117. A — A resolver connects a schema field to a data source, defining how that field's data is fetched or written.
118. D — DynamoDB, Lambda, and HTTP endpoints are all valid AppSync data source types (along with relational databases and OpenSearch).
119. B — VTL mapping templates and JavaScript (APPSYNC_JS) are the two resolver implementation styles.
120. B — request() and response() are the two functions exported by a JavaScript AppSync resolver.
121. A — A pipeline resolver chains multiple functions together to fulfill a single GraphQL field.
122. B — The relational database data source, using the RDS Data API, is designed for querying Aurora Serverless.
123. B — AppSync manages the WebSocket transport and automatically pushes updates to subscribed clients without client polling.
124. A — The @aws_subscribe directive links a Subscription field to the Mutation(s) that trigger it.
125. B — AppSync manages connection tracking and fan-out automatically, unlike a hand-built WebSocket API.
126. A — AWS Amplify DataStore supports offline-first local reads/writes that sync with AppSync later.
127. B — Optimistic Concurrency uses a version field (e.g., _version) to reject stale writes.
128. C — Lambda-based custom resolution allows arbitrary business logic for handling conflicts.
129. D — API key, IAM, Cognito User Pools, and OIDC are all valid AppSync authorization modes.
130. B — AppSync supports a primary auth mode plus additional auth modes, controlled via schema directives.
131. B — API key access is well suited for simple, unauthenticated public read access with no user sign-in.
132. A & D — Resolvers can be VTL or JS-based, and pipeline resolvers chain multiple functions for one field.
133. B — A Lambda data source supports arbitrary custom code and multiple downstream calls in one resolver, unlike a single-table DynamoDB resolver.
134. B — AppSync suits flexible field-level GraphQL queries and built-in subscriptions; API Gateway suits traditional REST needs like usage plans, resource policies, and private access.
135. A — Adding a real authorizer, a resource policy, and tightening CORS together address the three actual gaps described.
136. B — REST API with usage plans/API keys and IAM+resource policy for internal calls, plus AppSync or a WebSocket API for real-time push, covers all three needs.
137. A — Stage variables handle per-environment Lambda alias targeting, while canary deployment handles gradual, monitored traffic shifting.
138. B — Usage plans/API keys and full request validation are unsupported on HTTP APIs, forcing a choice between keeping REST API or re-architecting.
139. A — Multiple AppSync auth modes (API key, Cognito, IAM) together satisfy the three distinct caller types described.
142. A — Ensuring every code path (including error branches) returns the proper response envelope eliminates the intermittent 502s.
143. A — Lowering the authorizer cache TTL reduces the staleness window after a permissions change while retaining some caching benefit.
144. B — The recurring theme is cleanly separating "what the API/schema is" from "who may call it, how much, and which backend/environment it targets."
