# Module 05 — API Gateway & AppSync

Domain focus: heavily **Development with AWS Services (32%)** and **Deployment (24%)** — API Gateway stages/stage variables are the exam's favorite way to test "how do you deploy the same API config across dev/test/prod without duplicating resources." There's also a serious slice of **Security (26%)** here: authorizers, resource policies, and IAM/SigV4 access patterns for APIs show up constantly, including the exact cross-account scenario in AWS's own official sample questions. This module builds directly on module 04's Lambda basics (handler, event/context, aliases) — API Gateway is the most common way a Lambda function gets invoked by anything other than another AWS service.

## 1. Why API Gateway exists

Amazon API Gateway is a fully managed service for creating, publishing, securing, and monitoring APIs at any scale, without running or patching servers yourself. It sits in front of a backend — most often Lambda, but also HTTP endpoints, other AWS services, or a VPC-internal ALB/NLB — and handles everything a hand-rolled API layer would otherwise need: routing, authentication/authorization, request/response shaping, throttling, caching, and per-environment deployment.

There are three API types you need to know for the exam: **REST APIs**, **HTTP APIs**, and **WebSocket APIs**. AppSync is a separate, sibling service for GraphQL rather than a fourth API Gateway type — covered in its own section below.

## 2. REST APIs vs. HTTP APIs

Both let you expose HTTP(S) endpoints backed by Lambda, HTTP backends, or other AWS services, but they differ meaningfully in features, cost, and latency.

| | REST API | HTTP API |
|---|---|---|
| Latency/cost | Slightly higher latency, higher cost | Lower latency, up to ~70% cheaper for comparable traffic |
| Usage plans / API keys | Supported | **Not supported** |
| Request validation (JSON Schema models) | Supported | Limited/not supported |
| Native OIDC/OAuth2 JWT authorizer | Not built-in (use Lambda authorizer or Cognito authorizer) | **Built-in JWT authorizer** |
| Lambda / IAM / Lambda-custom authorizers | Supported | Supported (Lambda authorizers + JWT authorizers; IAM auth supported) |
| Private APIs (VPC endpoint only) | Supported | Not supported |
| Resource policies | Supported | Not supported |
| WAF integration | Supported | Supported (added later; REST is still the "default" exam answer when WAF is central to the scenario) |
| Mapping templates / VTL transformations | Full support (non-proxy integration) | Simplified/limited — HTTP APIs lean on proxy integration |
| Canary deployments | Supported | Not supported |
| CORS | Manual (create OPTIONS mock method + headers, or "Enable CORS" wizard) | Built-in, simple CORS configuration block |
| Caching | Supported (per-stage response caching) | Not supported |

**Exam trap:** if a scenario says "lowest possible latency and cost, simple Lambda-proxy backend, no need for usage plans, API keys, or request-body validation" → **HTTP API**. If it mentions usage plans, API keys, request validation, a private VPC-only API, resource policies, or response caching → **REST API**. "Needs the richest, most mature feature set" almost always points to REST API; "needs the cheapest, fastest, simplest option" points to HTTP API.

## 3. Resources, methods, and integration types

A REST/HTTP API is built from **resources** (URL path segments, e.g. `/orders`, `/orders/{id}`) and **methods** (HTTP verbs — GET, POST, PUT, DELETE, etc.) attached to each resource. Each method is wired to a backend via an **integration**. There are four integration types you must be able to distinguish:

| Integration type | What happens |
|---|---|
| **Lambda proxy integration** | The entire raw HTTP request (headers, query string, path params, body, request context) is passed to Lambda as a single structured event; Lambda's response must match a specific shape. No mapping templates involved — simplest, most common. |
| **Lambda custom (non-proxy) integration** | You define a request mapping template (VTL) to shape what Lambda receives, and a response mapping template to shape what the client receives. Gives fine-grained control but requires more setup and maintenance. |
| **HTTP integration** (proxy or non-proxy) | Forwards the request to another HTTP endpoint — an on-prem system via VPC Link, another API, an ALB, etc. Same proxy/non-proxy distinction applies. |
| **AWS service integration** | Calls an AWS service API directly (e.g., writing straight to DynamoDB or publishing to SQS) using mapping templates, with no Lambda function in between at all. |
| **Mock integration** | API Gateway returns a canned response without touching any backend. Used to test client behavior before a backend exists, or to handle CORS preflight `OPTIONS` requests. |

### Lambda proxy integration event/response shape
This is the shape you must recognize instantly on the exam. API Gateway sends Lambda an event roughly like:

```json
{
  "httpMethod": "POST",
  "path": "/orders",
  "headers": { "Content-Type": "application/json" },
  "queryStringParameters": { "region": "us-east-1" },
  "pathParameters": { "id": "42" },
  "body": "{\"item\":\"widget\"}",
  "requestContext": { "identity": { "sourceIp": "203.0.113.5" } }
}
```

And Lambda must return exactly this shape back, or API Gateway returns a 502:

```json
{
  "statusCode": 200,
  "headers": { "Content-Type": "application/json" },
  "body": "{\"orderId\":\"42\",\"status\":\"created\"}",
  "isBase64Encoded": false
}
```

**Exam trap:** a Lambda function behind a proxy integration that returns a bare object like `{"orderId": "42"}` instead of the `{statusCode, headers, body}` envelope will cause API Gateway to return a 502 Internal Server Error — this is one of the most common "why is my Lambda-backed API broken" troubleshooting scenarios. The `body` field must also be a **string** (JSON-stringified), not a raw object.

## 4. Stages and stage variables

A **deployment** is a snapshot of your API's configuration (resources, methods, integrations). A **stage** (e.g. `dev`, `test`, `prod`) is a named, addressable reference to a deployment — each stage gets its own invoke URL (`https://api-id.execute-api.region.amazonaws.com/dev`) and its own settings (throttling, caching, logging, stage variables).

**Stage variables** are key-value pairs scoped to a stage, functioning like environment variables for the API's configuration. Their most powerful use is dynamically pointing the *same* API definition at different backend targets per environment — most commonly, selecting a different **Lambda alias** per stage without duplicating the API.

Example: an integration URI referencing a stage variable to pick the Lambda alias matching the stage:
```
arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:111122223333:function:process-order:${stageVariables.lambdaAlias}/invocations
```
With `dev` stage's `lambdaAlias` variable set to `dev-alias` and `prod` stage's set to `prod-alias`, the exact same API deployment routes to entirely different Lambda code versions depending on which stage URL is called. This is the single most-tested "dynamic deployment across environments" pattern on DVA-C02 — it lets one API Gateway definition serve dev/test/prod without three separate copies of every resource and method.

**Exam trap:** stage variables can also select a different HTTP backend endpoint (e.g., pointing at a `dev` vs `prod` ALB DNS name) or toggle other integration settings per stage — not just Lambda aliases. If a scenario says "use the same API Gateway deployment but route to different backends per environment without duplicating resources," the answer is stage variables, not separate APIs.

## 5. Custom domain names and base path mapping

By default, an API is reachable only at the ugly generated `execute-api` URL. A **custom domain name** (e.g. `api.example.com`) maps a friendlier domain to your API, backed by a TLS certificate from **AWS Certificate Manager (ACM)**:
- **Edge-optimized** custom domain → certificate must be in `us-east-1` (regardless of the API's actual Region), served via CloudFront.
- **Regional** custom domain → certificate must be in the same Region as the API.

A **base path mapping** then maps a path segment under that custom domain (e.g. `api.example.com/v1`) to a specific API + stage combination. This lets you host multiple APIs, or multiple versions of the same API, under one custom domain — e.g. `/v1` → stage `prod` of API A, `/v2` → stage `prod` of API B.

## 6. Authorizers — controlling who can call your API

DVA-C02 tests three authorization mechanisms for API Gateway, plus resource policies as a complementary layer.

| Authorizer type | How it works | Typical use case |
|---|---|---|
| **IAM authorization (SigV4)** | Caller must sign the request with valid AWS credentials (SigV4); API Gateway checks the caller's IAM policy permissions for `execute-api:Invoke`. | Service-to-service calls, or known AWS-principal callers including cross-account access. |
| **Cognito User Pool authorizer** | Client sends a JWT (ID or access token) issued by a Cognito User Pool in the `Authorization` header; API Gateway validates it natively — no Lambda code needed. | End-user-facing apps where users sign up/sign in via Cognito. |
| **Lambda authorizer (custom authorizer)** | A Lambda function receives the incoming request (or just a token) and returns an IAM policy document (Allow/Deny) plus optional context passed to the backend. | Custom auth logic — validating a third-party JWT, an API key stored elsewhere, mTLS certs, or any bespoke scheme. |

Lambda authorizers come in two flavors:
- **Token-based (`TOKEN`)**: receives only a bearer token (e.g., from the `Authorization` header). Simpler, and results are more easily cacheable by token value.
- **Request-based (`REQUEST`)**: receives the full request context — headers, query string parameters, path parameters, stage variables, source IP. Needed when the authorization decision depends on more than just a single token.

Both types can **cache** their Allow/Deny decision (default TTL up to 3600 seconds, configurable) keyed by the identity source, avoiding a Lambda invocation on every single request — a meaningful cost/latency optimization worth calling out on the exam.

### Resource policies + IAM auth = cross-account access
A **resource policy** is a JSON policy document attached to the API itself (not to a caller's IAM identity), controlling which principals, source VPCs, VPC endpoints, or IP ranges may invoke it — independent of what any individual caller's own IAM policy says. This is exactly the mechanism AWS's own official sample question tests: allowing IAM principals from a *different* AWS account to call your REST API.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::444455556666:root" },
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:us-east-1:111122223333:abc123xyz/prod/GET/orders"
    }
  ]
}
```

To make cross-account IAM access actually work end-to-end you need **both** pieces: (1) the API's resource policy allowing the other account's principal, **and** (2) an IAM permission policy attached to the calling IAM user/role in the other account granting `execute-api:Invoke` on that API, with the caller signing every request using SigV4. Either piece alone is insufficient — this two-sided requirement (resource policy on the API + permission policy on the caller, both pointing at each other) is precisely the "(Select TWO)" pattern the official exam question tests.

**Exam trap:** API keys are **not** an authorization mechanism — they identify a caller for throttling/metering purposes only (see usage plans below). A scenario asking for actual *authentication/authorization* should never have "attach an API key" as the correct answer.

## 7. Request/response transformation, mapping templates, and validation

For non-proxy integrations, **mapping templates** written in **VTL (Velocity Template Language)** transform the incoming request into whatever shape the backend expects, and transform the backend's response back into whatever shape the client expects. This is how you can, for example, expose a clean REST-ish `POST /orders` endpoint backed directly by a DynamoDB `PutItem` call, with API Gateway doing the JSON reshaping in between — no Lambda required.

A simplified request mapping template turning a JSON body into a DynamoDB `PutItem` request:
```
{
  "TableName": "Orders",
  "Item": {
    "orderId": { "S": "$context.requestId" },
    "item": { "S": "$input.path('$.item')" }
  }
}
```

**Request validation** lets API Gateway reject malformed requests (missing required parameters/headers, or a body that fails a JSON Schema **model**) *before* the request ever reaches the backend. This matters for cost control (no wasted Lambda invocations on garbage input) and for pushing basic validation logic out of application code and into the API layer itself. REST APIs support this natively; it's one of the feature gaps on HTTP APIs.

## 8. Throttling, usage plans, and API keys

API Gateway enforces **throttling** at the account level (a Region-wide default steady-state rate + burst limit) and can be further tuned per-stage or per-method. Beyond the account default, a **usage plan** lets you define, per API client, how much and how fast they may call one or more deployed APIs/stages:
- **Throttle limits** — steady-state requests/second and burst capacity for that plan.
- **Quota** — a longer-window cap, e.g. 10,000 requests per month.

An **API key** identifies which caller is making the request so the usage plan can be enforced and usage metered — it is a metering/throttling identifier, **not** an authentication credential. To require a key, you enable "API key required" on a method *and* associate the key with a usage plan tied to that stage; a request with a missing or invalid key is rejected regardless of whether it would have otherwise passed authorization.

**Exam trap:** "limit how many requests a third-party partner can make per day, and bill/report on their usage separately from other callers" → usage plan + API key. "Prove the caller is who they claim to be" → IAM/Cognito/Lambda authorizer, never an API key alone.

## 9. CORS (Cross-Origin Resource Sharing)

CORS is a *browser-enforced* security mechanism, not an AWS-specific concept — it becomes relevant whenever a web app served from one origin (e.g. `https://app.example.com`) calls an API on a different origin (e.g. `https://api.example.com`) directly from client-side JavaScript. The browser sends a preflight `OPTIONS` request, and the API must respond with the right `Access-Control-Allow-Origin` / `-Methods` / `-Headers` values or the browser blocks the real request client-side (the server-side call may have actually succeeded — the browser just refuses to hand the response to the page's JS).

- On a **REST API**, you enable CORS per resource — either via the console's "Enable CORS" action (which creates a Mock-integration `OPTIONS` method returning the right headers) or by hand-authoring it yourself.
- On an **HTTP API**, CORS is a simple built-in configuration block on the API itself — no manual mock method needed.
- **Critical trap for Lambda proxy integrations**: because proxy integration passes the Lambda response straight through unmodified, enabling "CORS" in the console does *not* automatically inject CORS headers into your actual method's response — your Lambda function itself must include `Access-Control-Allow-Origin` (etc.) in the headers it returns. Forgetting this is one of the most common real-world "CORS error but everything looks configured" bugs.

## 10. WebSocket APIs

REST/HTTP APIs are request/response — a client asks, the server answers, the connection ends. A **WebSocket API** keeps a persistent, full-duplex connection open, letting either side push messages at any time — used for chat apps, live dashboards, multiplayer game state, and stock ticker-style feeds.

Key concepts:
- **Route selection expression** determines which backend integration handles an incoming message, based on a field in the message body (e.g. `$request.body.action`).
- Three special built-in routes: **`$connect`** (fires when a client opens a connection — good place to authorize and store the connection), **`$disconnect`** (fires on close — clean up stored state), and **`$default`** (catches messages matching no other route).
- Because the connection is stateful, a common pattern stores each active `connectionId` in a DynamoDB table on `$connect`, removes it on `$disconnect`, and a backend Lambda later pushes messages to specific clients using the **API Gateway Management API**'s `PostToConnection` call, referencing the stored connection IDs.

**Exam trap:** "needs true two-way, server-initiated push to specific connected clients over a raw protocol" → WebSocket API. If the scenario is really about GraphQL-shaped real-time data with subscriptions tied to a schema, AppSync's built-in subscriptions (below) are usually the better, lower-effort fit — you'd have to build the connection-tracking table yourself with a raw WebSocket API, whereas AppSync manages that for you.

## 11. Mock integrations for pre-backend testing

A **Mock integration** returns a static, API-Gateway-defined response without invoking any backend at all. Two big uses: (1) letting frontend developers build and test against an API's shape before the real backend (e.g. a Lambda function) is finished, and (2) implementing `OPTIONS` preflight responses for CORS without any compute cost. This is the exam's answer whenever a scenario says something like "the backend team hasn't finished the Lambda function yet, but the frontend team needs to start integrating against the API today."

## 12. AWS AppSync — managed GraphQL

AppSync is a fully managed service for building **GraphQL APIs**. GraphQL differs fundamentally from REST: instead of many fixed-shape endpoints, there's a single endpoint and clients specify exactly which fields they want in a **query**, avoiding the classic REST problems of over-fetching (getting fields you don't need) and under-fetching (needing several round trips to assemble one screen's data).

### Schema, resolvers, and data sources
A GraphQL **schema** defines `Query` (reads), `Mutation` (writes), and `Subscription` (real-time push) types, plus the object types they return:

```graphql
type Order {
  orderId: ID!
  item: String!
  status: String!
}

type Query {
  getOrder(orderId: ID!): Order
}

type Mutation {
  createOrder(item: String!): Order
}

type Subscription {
  onOrderCreated: Order
    @aws_subscribe(mutations: ["createOrder"])
}
```

A **resolver** attaches to a specific field (e.g. `Query.getOrder`) and defines how to fetch/write the data by calling a **data source**:
- **DynamoDB** — the most common data source; a resolver can do a direct `GetItem`/`PutItem`/`Query` against a table with no Lambda in between.
- **Lambda** — for arbitrary custom logic, multiple backend calls, or business rules too complex for a simple mapping.
- **Relational database (RDS Data API)** — typically Aurora Serverless, queried via the RDS Data API.
- **HTTP** — calls any HTTP endpoint, including other AWS service APIs.

Resolvers come in two implementation styles:
- **VTL resolvers** (the original mechanism) — a request mapping template (turns the GraphQL field arguments into a data source request) and a response mapping template (turns the data source result into the GraphQL response), conceptually identical to API Gateway's VTL mapping templates.
- **JavaScript (APPSYNC_JS) resolvers** — newer, simpler: a JS module exporting a `request()` function (build the data source request) and a `response()` function (shape the result), avoiding VTL's steeper learning curve.

A minimal JS resolver for a DynamoDB `GetItem`:
```javascript
export function request(ctx) {
  return {
    operation: "GetItem",
    key: { orderId: { S: ctx.args.orderId } }
  };
}
export function response(ctx) {
  return ctx.result;
}
```

**Pipeline resolvers** chain multiple functions together (e.g., validate input → write to DynamoDB → publish a notification) for a single GraphQL field, when one data source call isn't enough.

### Real-time subscriptions
A GraphQL **subscription** lets a client register interest in an event (e.g. `onOrderCreated`); AppSync manages the underlying WebSocket connection transparently — the client just issues a subscription operation through the AppSync SDK, and whenever a matching mutation fires, AppSync automatically pushes the updated data to every subscribed client. This is a major operational advantage over building a raw WebSocket API by hand: you don't manage connection IDs, routes, or a connections table yourself — AppSync does it.

### Offline sync
Combined with **AWS Amplify DataStore**, AppSync supports offline-first apps: local reads/writes work against an on-device store even without connectivity, and changes sync back to AppSync when the connection returns. **Conflict detection and resolution** handles the case where the same record was edited both offline and on the server in the meantime, using strategies like **Optimistic Concurrency** (a `_version` field rejects stale writes), **Auto Merge** (field-level merge when possible), or a custom **Lambda-based** resolution function for business-specific conflict logic.

### Authorization modes
AppSync supports the same four authorization concepts as API Gateway, named slightly differently, and — importantly — supports **multiple auth modes on one API simultaneously** (a primary mode plus additional modes), with schema directives controlling which mode(s) apply to which fields/types:

| Mode | Parallels |
|---|---|
| **API key** | Simple, expiring key — good for public/dev access, no user identity |
| **IAM** | SigV4-signed requests — service-to-service or AWS-authenticated callers |
| **Amazon Cognito User Pools** | End-user sign-in; supports group-based field-level authorization |
| **OpenID Connect (OIDC)** | Third-party identity provider issuing tokens, similar role to a custom/JWT authorizer |

## 13. Comparison table — choosing among the four

| | REST API | HTTP API | WebSocket API | AppSync (GraphQL) |
|---|---|---|---|---|
| Protocol/style | Request/response, REST-ish | Request/response, REST-ish | Persistent, full-duplex | Request/response + native subscriptions |
| Best for | Feature-rich REST APIs needing usage plans, validation, caching, private access | Simple, cheap, low-latency Lambda/HTTP-backed APIs | Bidirectional real-time over a custom protocol | Flexible client-driven queries + built-in real-time push |
| Real-time push | No (needs polling or a separate WebSocket API) | No | Yes, manually managed connections | Yes, built-in subscriptions, connections managed for you |
| Auth options | IAM, Cognito, Lambda authorizer, resource policy | IAM, JWT (built-in), Lambda authorizer | IAM, Cognito, Lambda authorizer (at `$connect`) | API key, IAM, Cognito, OIDC — multiple at once |
| Relative cost/latency | Higher | Lower | Pay for connection-minutes + messages | Pay per query/mutation/subscription message |
| Client fetches | Fixed response shape per endpoint | Fixed response shape per endpoint | N/A (message-based) | Client chooses exact fields returned |

## 14. Worked real-world scenarios

**Scenario A — the cross-account partner integration.** A company exposes a REST API on API Gateway and needs to let IAM principals in a partner's separate AWS account call specific methods, without creating individual users in the company's own account. The two-sided fix mirrors AWS's official sample question exactly: first, attach a **resource policy** to the API allowing the partner account's IAM principal (or specific roles) to call `execute-api:Invoke` on the relevant resource ARN; second, the partner's own IAM administrator must attach a permission policy to their calling IAM users/roles granting `execute-api:Invoke` on that same API ARN, and their SDK/CLI calls must be SigV4-signed. Skipping either side fails: a resource policy alone doesn't grant the partner's IAM identity permission to call *any* API, and a permission policy alone in the partner's account doesn't override the fact that the API's own resource policy hasn't allowlisted them.

**Scenario B — one API definition, three environments.** A team maintains a single REST API definition but needs `dev`, `test`, and `prod` stages to invoke three different Lambda function aliases (each alias pointing at a different published version), without triplicating every resource and method. The fix: define a stage variable (e.g. `lambdaAlias`) on each stage with a different value (`dev-alias`, `test-alias`, `prod-alias`), and reference `${stageVariables.lambdaAlias}` inside the Lambda proxy integration's target ARN. Deploying a new API change becomes "deploy once, the stage variable resolves the right backend automatically" instead of maintaining parallel API definitions — and because each stage also carries its own throttling/logging/caching settings, `dev` can run verbose logging and no caching while `prod` runs the opposite, all from the same underlying API.

**Scenario C — building the frontend before the backend exists.** A mobile team needs to start integration testing against an API's exact request/response shape, but the backend engineering team is still two weeks from finishing the real Lambda implementation. Rather than blocking the mobile team, the API team stands up the resources and methods with **Mock integrations** that return realistic, hardcoded sample JSON matching the eventual real shape. The mobile team builds and tests against those mocked responses immediately; once the real Lambda function is ready, the team swaps the integration type from Mock to Lambda proxy on each method with zero change to the API's public contract — the mobile app doesn't need to change anything.

**Scenario D — real-time order status without hand-rolled connection tracking.** A retail app needs to push live order-status updates to a customer's app the instant an order's status changes, and the team is deciding between a raw WebSocket API and AppSync. Building it on a WebSocket API would require them to hand-roll a DynamoDB connections table, wire up `$connect`/`$disconnect` handlers, and manually call `PostToConnection` whenever status changes. Choosing **AppSync** instead — with a `Mutation.updateOrderStatus` that triggers an `@aws_subscribe`-linked `Subscription.onOrderStatusChanged` — gets the same real-time push with none of that plumbing: AppSync manages the WebSocket transport, the connection registry, and the fan-out to every subscribed client automatically, backed by a DynamoDB data source for the underlying order record.

## Key exam traps
- HTTP APIs are cheaper and lower-latency but drop usage plans, API keys, request validation, private APIs, resource policies, and caching — REST API is the answer whenever any of those features are named.
- A Lambda proxy integration response that isn't shaped exactly `{statusCode, headers, body (string), isBase64Encoded}` causes a 502, not a generic error — recognize this failure mode instantly.
- Stage variables are the mechanism for pointing one API definition at different Lambda aliases (or different backend endpoints) per environment — this is the exam's core "dynamic deployment across environments" pattern.
- Cross-account IAM access to an API requires **both** a resource policy on the API allowing the other account's principal **and** a permission policy on the caller's IAM identity in their own account, plus SigV4 signing — this is a verbatim official AWS sample question topic.
- API keys are for usage-plan metering/throttling identification only — never the answer to an authentication/authorization requirement.
- Enabling "CORS" in the console does not inject headers into a Lambda proxy integration's actual response — the Lambda function itself must return the CORS headers.
- Lambda authorizers: TOKEN type gets just a bearer token; REQUEST type gets full request context (headers, query/path params, source IP) — pick REQUEST when the decision needs more than the token alone, and remember both support result caching.
- Mock integrations are the answer whenever a scenario needs to test/build against an API's shape before the real backend exists.
- WebSocket APIs require you to manage connection state (typically a DynamoDB table + `PostToConnection`) yourself; AppSync subscriptions give equivalent real-time push with that plumbing managed for you — favor AppSync when the data is naturally GraphQL-shaped and favor a WebSocket API when you need a custom, non-GraphQL bidirectional protocol.
- AppSync can run multiple authorization modes simultaneously (e.g., API key for public reads plus Cognito for authenticated mutations) — don't assume only one auth mode is possible per API, unlike a naive read of API Gateway's single-authorizer-per-method model.
