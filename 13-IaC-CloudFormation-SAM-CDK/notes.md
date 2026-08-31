# Module 13 — Infrastructure as Code: CloudFormation, SAM, CDK

Domain focus: primarily **Deployment (24%)** — specifically Domain 3 Task Statement 3 ("prepare application artifacts to be deployed to AWS," which includes writing/using SAM and CloudFormation templates) and Task Statement 4 ("deploy code by using AWS CI/CD services," where updating an IaC template is itself the deployment mechanism). You've been deploying Lambda functions (module 04) and API Gateway APIs (module 05) by hand or through the console up to this point — this module is about never doing that again. Everything you provision from here on should be defined as code, versioned in source control, and deployed repeatably.

## 1. Why Infrastructure as Code at all

Clicking through the console to create a Lambda function, an API Gateway API, and a DynamoDB table works exactly once. The moment you need a second environment (staging), a teammate needs the same setup, or you need to tear it down and recreate it identically, manual console work becomes a liability: it's undocumented, unrepeatable, and drifts silently as people make one-off changes nobody tracks. **Infrastructure as Code (IaC)** means describing your infrastructure in a text file — checked into the same repository as your application code, reviewed in pull requests, and applied through automation — rather than clicking buttons.

AWS gives developers three IaC tools that build on each other:
- **CloudFormation** — the foundational, declarative engine. You describe *what* you want (a Lambda function, an S3 bucket, an IAM role) in JSON or YAML, and CloudFormation figures out *how* to create, update, or delete it, tracking every resource it manages as a **stack**.
- **SAM (Serverless Application Model)** — a CloudFormation *extension* (technically a "transform") that adds shorthand resource types purpose-built for serverless apps (Lambda + API Gateway + DynamoDB), plus a CLI for local testing. Every SAM template compiles down into a plain CloudFormation template before deployment.
- **CDK (Cloud Development Kit)** — lets you write infrastructure using an actual programming language (TypeScript, Python, Java, C#, Go) instead of a YAML/JSON DSL. `cdk synth` compiles your code into a CloudFormation template, which is then deployed the normal CloudFormation way.

All three ultimately produce and apply a CloudFormation template — the difference is the *authoring experience* (raw declarative YAML vs. serverless-shorthand YAML vs. imperative code) and how serverless-specific the shorthand is. This layering matters for the exam: you'll be asked to recognize which layer a given template or CLI command belongs to, and CDK/SAM questions frequently hinge on the fact that they still ultimately deploy as a CloudFormation stack, inheriting its rollback and change-set behavior.

## 2. AWS CloudFormation fundamentals

### The core sections of a template
A CloudFormation template (YAML shown, JSON is equivalent) has a handful of top-level sections. Only `Resources` is mandatory; everything else is optional but heavily used in real templates.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Web app infrastructure - EC2 instance behind a security group

Parameters:
  EnvironmentName:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]
    Description: Deployment environment name
  InstanceTypeParam:
    Type: String
    Default: t3.micro

Mappings:
  EnvironmentToInstanceType:
    dev:
      InstanceType: t3.micro
    staging:
      InstanceType: t3.small
    prod:
      InstanceType: m6g.large

Conditions:
  IsProd: !Equals [!Ref EnvironmentName, prod]

Resources:
  AppSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP inbound
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  AppInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !FindInMap [EnvironmentToInstanceType, !Ref EnvironmentName, InstanceType]
      ImageId: ami-0abcdef1234567890
      SecurityGroupIds:
        - !GetAtt AppSecurityGroup.GroupId
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName

  ProdOnlyAlarmTopic:
    Type: AWS::SNS::Topic
    Condition: IsProd

Outputs:
  InstancePublicIp:
    Description: Public IP of the app instance
    Value: !GetAtt AppInstance.PublicIp
    Export:
      Name: !Sub "${EnvironmentName}-AppInstance-PublicIp"
```

- **Parameters** — input values supplied at stack-creation/update time (via console, CLI `--parameters`, or a parameters file). This is how the *same template* deploys differently across dev/staging/prod without editing the template itself.
- **Mappings** — static, hardcoded lookup tables (like the `EnvironmentToInstanceType` map above), resolved with `Fn::FindInMap`. Unlike Parameters, values aren't supplied at deploy time — they're baked into the template as a fixed key-value lookup, useful for things like Region-to-AMI-ID tables.
- **Conditions** — boolean expressions (built from intrinsic functions like `Fn::Equals`, `Fn::And`, `Fn::Not`) that control whether a resource is created at all (via a `Condition:` key on the resource) or which value a property gets.
- **Resources** — the only required section. Each resource has a logical ID (`AppInstance`), an AWS resource `Type` (`AWS::EC2::Instance`), and `Properties`.
- **Outputs** — values exposed after stack creation, visible in the console/CLI, and consumable by other stacks via `Fn::ImportValue` (see cross-stack references below).

### Intrinsic functions (memorize these — they show up constantly)
| Function | Short form | Purpose |
|---|---|---|
| `Fn::Ref` | `!Ref` | Returns a resource's primary identifier (e.g. an instance ID) or a parameter's value |
| `Fn::GetAtt` | `!GetAtt` | Returns a *specific attribute* of a resource (e.g. `!GetAtt AppSecurityGroup.GroupId`) — richer than `Ref`, which only gives the default identifier |
| `Fn::Sub` | `!Sub` | String interpolation/substitution — `!Sub "${EnvironmentName}-bucket"` |
| `Fn::FindInMap` | `!FindInMap` | Looks up a value in a `Mappings` table |
| `Fn::ImportValue` | `!ImportValue` | Imports a value another stack exported via `Outputs` — the standard mechanism for cross-stack references |
| `Fn::Join` | `!Join` | Concatenates a list of values with a delimiter |
| `Fn::Equals` / `Fn::And` / `Fn::Or` / `Fn::Not` | — | Used inside `Conditions` |
| `Fn::If` | `!If` | Returns one of two values depending on a named condition, usable inside a resource property |

**Exam trap:** `Ref` vs. `GetAtt` is a favorite distinction. `!Ref` on an EC2 instance returns its instance ID; if you need its public IP or ARN, you need `!GetAtt InstanceLogicalId.PublicIp` — `Ref` alone won't get you there for most non-trivial attributes.

### Cross-stack references: Export/ImportValue
When one stack's resource needs to be consumed by another stack (e.g. a networking stack exports a VPC ID that an application stack needs), the exporting stack declares an `Export` under `Outputs`, and the consuming stack uses `Fn::ImportValue` referencing that export name:

```yaml
# In the "networking" stack's Outputs:
Outputs:
  VpcId:
    Value: !Ref MyVpc
    Export:
      Name: SharedVpcId

# In a separate "app" stack's Resources:
Resources:
  AppInstance:
    Type: AWS::EC2::Instance
    Properties:
      SubnetId: !ImportValue SharedVpcSubnetId
```

**Exam trap:** a stack **cannot delete or modify an exported output value while another stack still imports it** — CloudFormation blocks the update/delete until the importing stack stops referencing it. This is a very commonly tested "why did my stack update fail" scenario.

### Stacks, stack sets, and change sets
- A **stack** is the deployable unit — a named collection of resources CloudFormation creates, updates, and deletes together as a single unit. Deleting a stack deletes its resources (subject to `DeletionPolicy`, below).
- A **stack set** extends this across **multiple accounts and/or Regions** from one place — useful for deploying a baseline (e.g. a security guardrail, a logging configuration) consistently across an entire AWS Organization.
- A **nested stack** is a stack whose template is *referenced from within another (parent) stack* via `AWS::CloudFormation::Stack`, letting you decompose a large template into reusable, independently-authored components (e.g. a shared "networking" nested stack referenced by several application stacks). This is different from cross-stack references via `ImportValue` — nested stacks are composed and deployed together as one unit from the parent's perspective, while cross-stack references connect otherwise-independent, separately-deployed stacks.
- A **change set** is a *preview* of what a stack update would actually do — which resources would be modified, replaced, or deleted — **without applying it**. You generate a change set, review it (critically: check for any resource marked for **replacement**, since replacement means the old resource is deleted and a new one created, which is catastrophic for a stateful resource like a database if unexpected), and then execute it. This is the exam's preferred, safe answer whenever a scenario asks "how do I know what a template change will do before I apply it in production."

### Rollback behavior on failure
If a stack **creation** fails partway through, CloudFormation's default behavior is to **roll back and delete everything it already created** (unless you disable rollback, which leaves the partially-created resources for debugging — useful during development, risky to leave enabled in production automation). If a stack **update** fails, CloudFormation automatically rolls the stack back to its **last known good state** — it doesn't leave your infrastructure half-updated.

### Stack drift detection
Over time, someone might manually change a resource CloudFormation manages (e.g. editing a security group rule directly in the console) without going through a stack update. **Drift detection** compares the stack's actual, live configuration against what the template says it should be, and reports which resources have **drifted** and exactly which properties differ. This is a *read-only* detection mechanism — running drift detection doesn't fix anything, it just tells you where reality has diverged from the template, which is your cue to either update the template to match reality or revert the manual change.

### Protecting stateful resources: DeletionPolicy and UpdateReplacePolicy
By default, deleting a CloudFormation stack deletes every resource in it — including a database that might hold irreplaceable production data. Two properties guard against this:
- **`DeletionPolicy`** controls what happens to a resource **when the stack itself is deleted** (or the resource is removed from the template). Options: `Delete` (default for most resources), `Retain` (leave the resource in place, orphaned from the stack, when the stack is deleted), and `Snapshot` (for resources that support it, like RDS or EBS — take a final snapshot before deleting).
- **`UpdateReplacePolicy`** controls what happens to the *old* resource specifically when a stack **update** causes that resource to be **replaced** (some property changes force replacement rather than an in-place update — e.g. changing an RDS instance's engine). Same options: `Delete`, `Retain`, `Snapshot`.

```yaml
Resources:
  ProdDatabase:
    Type: AWS::RDS::DBInstance
    DeletionPolicy: Snapshot
    UpdateReplacePolicy: Snapshot
    Properties:
      Engine: mysql
      DBInstanceClass: db.t3.medium
      AllocatedStorage: 100
```

**Exam trap:** this is one of the most directly-tested CloudFormation details. "How do you prevent an RDS instance from being deleted when its stack is deleted, but still have a final backup?" → `DeletionPolicy: Snapshot`. "How do you make sure an in-place update never gets silently replaced-and-destroyed?" → `UpdateReplacePolicy: Retain` (or `Snapshot`).

### Custom resources
Sometimes CloudFormation has no native resource type for something you need to provision — a third-party SaaS resource, a piece of logic like "generate a random password and store it," or a step that just isn't modeled as a first-class CloudFormation resource yet. **Custom resources** (`AWS::CloudFormation::CustomResource`, or the shorthand `Custom::YourResourceName`) let you back a "resource" in your template with a **Lambda function** (or an SNS topic) that CloudFormation invokes on Create/Update/Delete, and which must send a response back (success/failure, plus any output data) via a pre-signed S3 URL CloudFormation provides. This is the standard escape hatch whenever the exam describes a requirement CloudFormation can't natively express.

```yaml
Resources:
  RandomPasswordFunction:
    Type: AWS::Lambda::Function
    Properties:
      Handler: index.handler
      Runtime: python3.12
      Role: !GetAtt CustomResourceRole.Arn
      Code:
        ZipFile: |
          import cfnresponse
          def handler(event, context):
              # generate/store a value, then respond
              cfnresponse.send(event, context, cfnresponse.SUCCESS, {"Value": "generated"})

  GeneratedSecret:
    Type: Custom::RandomPassword
    Properties:
      ServiceToken: !GetAtt RandomPasswordFunction.Arn
```

## 3. AWS SAM (Serverless Application Model)

SAM is not a separate deployment engine — it's a **CloudFormation transform** that adds a shorthand, serverless-focused vocabulary on top of plain CloudFormation. Every SAM template starts with a `Transform` line, and SAM CLI commands compile your shorthand into a real CloudFormation template before ever touching CloudFormation's API.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Description: Order processing API - Lambda + API Gateway + DynamoDB

Globals:
  Function:
    Runtime: python3.12
    Timeout: 10
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref OrdersTable

Parameters:
  StageName:
    Type: String
    Default: dev

Resources:
  OrdersTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      PrimaryKey:
        Name: orderId
        Type: String

  CreateOrderFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.create_order_handler
      CodeUri: src/create_order/
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref OrdersTable
      Events:
        CreateOrderApi:
          Type: Api
          Properties:
            Path: /orders
            Method: post
            RestApiId: !Ref OrdersApi

  GetOrderFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.get_order_handler
      CodeUri: src/get_order/
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref OrdersTable
      Events:
        GetOrderApi:
          Type: Api
          Properties:
            Path: /orders/{orderId}
            Method: get
            RestApiId: !Ref OrdersApi

  OrdersApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: !Ref StageName

Outputs:
  ApiEndpoint:
    Description: Invoke URL for the Orders API
    Value: !Sub "https://${OrdersApi}.execute-api.${AWS::Region}.amazonaws.com/${StageName}"
```

Notice how much this template is *not* doing by hand: no explicit `AWS::Lambda::Permission` resource wiring API Gateway to invoke each Lambda function (SAM generates it automatically from the `Events: Api` block), no hand-written IAM policy JSON for DynamoDB access (the `DynamoDBCrudPolicy`/`DynamoDBReadPolicy` **SAM policy templates** generate scoped least-privilege IAM policies for you), and no separately-defined API Gateway deployment/stage resources beyond the one `AWS::Serverless::Api` block. This is the entire value proposition of SAM over raw CloudFormation for serverless apps: massively less boilerplate for the Lambda+API Gateway+DynamoDB pattern specifically.

### The three signature SAM resource types
| SAM type | Expands to (roughly) | Purpose |
|---|---|---|
| `AWS::Serverless::Function` | `AWS::Lambda::Function` + execution role + event source mappings/permissions | A Lambda function, with `Events:` blocks wiring up triggers (API Gateway, S3, DynamoDB Streams, SQS, EventBridge, schedule) declaratively |
| `AWS::Serverless::Api` | `AWS::ApiGateway::RestApi` + deployment + stage | A REST API Gateway API, with stage/throttling/CORS/authorizer configuration in one block |
| `AWS::Serverless::SimpleTable` | `AWS::DynamoDB::Table` | A basic DynamoDB table with a single primary key — for anything needing GSIs/LSIs/streams, you drop back to a plain `AWS::DynamoDB::Table` resource, which you can mix freely in the same SAM template |

You can freely mix plain CloudFormation resources (`AWS::S3::Bucket`, `AWS::SNS::Topic`, a full `AWS::DynamoDB::Table` with GSIs, etc.) alongside `AWS::Serverless::*` resources in the same template — SAM doesn't replace CloudFormation, it extends it. Everything from Section 2 (Parameters, Conditions, Outputs, intrinsic functions, DeletionPolicy) still applies inside a SAM template.

### The SAM CLI workflow
```bash
# Scaffold a new SAM app from a starter template (interactive prompts for runtime, template)
sam init

# Build: install dependencies, resolve CodeUri paths into a deployable build artifact
# (equivalent of npm install / pip install into a build directory, per function)
sam build

# Invoke a single function locally, in a Docker container that emulates the Lambda runtime,
# without deploying anything - fast dev-loop for a single function's logic
sam local invoke CreateOrderFunction --event events/create_order_event.json

# Spin up a local API Gateway + Lambda emulator on localhost, so you can curl your
# full API surface (multiple functions/routes) before ever deploying
sam local start-api

# Package: upload build artifacts (function code, etc.) to an S3 bucket and produce
# a CloudFormation template with local paths replaced with the uploaded S3 locations
sam package --s3-bucket my-deployment-artifacts-bucket --output-template-file packaged.yaml

# Deploy: create/update the actual CloudFormation stack from the (packaged) template
sam deploy --guided                       # first deploy - interactively writes samconfig.toml
sam deploy --config-env staging           # subsequent deploys - reuse saved config per environment
```

`sam deploy` (with the `--resolve-s3` flag, or after `sam package`) is really just calling CloudFormation's `CreateChangeSet`/`ExecuteChangeSet` APIs under the hood — SAM deployments get the same change-set preview, rollback-on-failure, and drift-detection behavior as any CloudFormation stack, because a SAM deployment *is* a CloudFormation stack once transformed.

**Local testing is the single most exam-relevant SAM CLI detail**: `sam local invoke` and `sam local start-api` let you test Lambda and API Gateway integration **entirely on your own machine, with no deployment, no AWS charges, and fast iteration** — this is the go-to answer whenever a scenario asks "how can a developer test a Lambda function's logic before deploying it to AWS."

### Deploying to different environments: SAM config environments
Rather than maintaining separate templates per environment (which drifts and duplicates logic), SAM lets one template deploy differently per environment two ways:
1. **Parameter overrides** — pass `--parameter-overrides "StageName=prod MemorySizeParam=512"` on the CLI, or define them per-environment in `samconfig.toml`.
2. **Named config environments** in `samconfig.toml`, each with its own stack name, S3 bucket, region, and parameter overrides:

```toml
version = 0.1

[dev.deploy.parameters]
stack_name = "orders-app-dev"
region = "us-east-1"
parameter_overrides = "StageName=dev"
s3_bucket = "orders-app-artifacts-dev"
confirm_changeset = false

[staging.deploy.parameters]
stack_name = "orders-app-staging"
region = "us-east-1"
parameter_overrides = "StageName=staging"
s3_bucket = "orders-app-artifacts-staging"
confirm_changeset = true

[prod.deploy.parameters]
stack_name = "orders-app-prod"
region = "us-west-2"
parameter_overrides = "StageName=prod MemorySizeParam=512"
s3_bucket = "orders-app-artifacts-prod"
confirm_changeset = true
```

With this file in place, `sam deploy --config-env staging` deploys the *same* `template.yaml` as a completely separate stack (`orders-app-staging`) with staging-specific parameter values, entirely distinct from the `dev` or `prod` stacks. This directly maps to the exam objective "deploying an AWS SAM template to a different staging environment" — the mechanism is parameter overrides plus (optionally) named config environments, not separate templates.

## 4. AWS CDK (Cloud Development Kit)

CDK takes a different approach entirely: instead of writing YAML/JSON, you write **actual code** in TypeScript, Python, Java, C#, or Go, using CDK's libraries to define infrastructure as objects. Running `cdk synth` executes your program, which produces a CloudFormation template as output — CDK is a *code generator* for CloudFormation templates, not a separate execution engine.

### Why developers reach for CDK
- **Loops, conditionals, functions** — want to create five nearly-identical S3 buckets with slightly different names? A `for` loop, not five copy-pasted YAML blocks.
- **Type safety and IDE support** — autocomplete, compile-time checking of property names/types, catching typos before you ever deploy.
- **Reuse via real abstractions** — package a common pattern (e.g. "a Lambda function behind an API Gateway route with standard logging and alarms") as a reusable class/construct that other teams import, instead of copy-pasting YAML.
- **Familiar tooling** — unit tests, existing package managers (`npm`, `pip`), code review tooling — all work the same way they do for application code, because it *is* code.

### Constructs: L1, L2, L3
CDK organizes everything around **constructs** — reusable cloud components — at three levels of abstraction:
| Level | Name | What it is |
|---|---|---|
| L1 | "Cfn resources" | A near-1:1, auto-generated wrapper around a raw CloudFormation resource type (e.g. `CfnFunction`, `CfnBucket`) — every property from the CloudFormation spec is exposed directly, but you get none of CDK's sane defaults |
| L2 | Curated constructs | Hand-crafted, higher-level classes (e.g. `lambda.Function`, `s3.Bucket`, `dynamodb.Table`) that wrap one or more L1 resources with sensible defaults, helper methods (`bucket.grantRead(fn)`), and less boilerplate |
| L3 | Patterns | Whole architectural patterns composed of multiple L2 constructs (e.g. `aws-apigateway.LambdaRestApi`, or the `aws-ecs-patterns.ApplicationLoadBalancedFargateService` construct) — an entire common architecture in a few lines |

Most day-to-day CDK code lives at **L2** — enough abstraction to avoid boilerplate, while still exposing individual resources when you need to drop down and tweak something specific.

### The same infrastructure as imperative code (TypeScript)
This defines the same shape of app as the SAM template above — a Lambda function, an API Gateway REST API, and a DynamoDB table — but as CDK code:

```typescript
import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

export class OrdersAppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const ordersTable = new dynamodb.Table(this, "OrdersTable", {
      partitionKey: { name: "orderId", type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    const createOrderFn = new lambda.Function(this, "CreateOrderFunction", {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: "app.create_order_handler",
      code: lambda.Code.fromAsset("src/create_order"),
      environment: { TABLE_NAME: ordersTable.tableName },
    });
    ordersTable.grantWriteData(createOrderFn);

    const getOrderFn = new lambda.Function(this, "GetOrderFunction", {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: "app.get_order_handler",
      code: lambda.Code.fromAsset("src/get_order"),
      environment: { TABLE_NAME: ordersTable.tableName },
    });
    ordersTable.grantReadData(getOrderFn);

    const api = new apigateway.RestApi(this, "OrdersApi");
    const orders = api.root.addResource("orders");
    orders.addMethod("POST", new apigateway.LambdaIntegration(createOrderFn));
    const order = orders.addResource("{orderId}");
    order.addMethod("GET", new apigateway.LambdaIntegration(getOrderFn));

    new cdk.CfnOutput(this, "ApiEndpoint", { value: api.url });
  }
}
```

Compare this to the SAM template: `ordersTable.grantWriteData(createOrderFn)` is doing the same job as SAM's `DynamoDBCrudPolicy` — generating a scoped IAM policy — but as a method call on an object, not a declarative policy-template reference. The `for`-loop-friendliness becomes obvious the moment you need, say, ten near-identical Lambda functions differing only by handler name: in CDK that's a five-line loop; in raw CloudFormation/SAM it's ten near-duplicate resource blocks.

### The CDK CLI workflow
```bash
# One-time per account/Region: provisions the S3 bucket + IAM roles CDK itself needs
# to store synthesized templates and deployment assets
cdk bootstrap

# Synthesize: run your app code and produce the CloudFormation template (no deployment)
cdk synth

# Diff: compare your current code's synthesized template against what's currently
# deployed, showing exactly what would change - the CDK-code equivalent of a change set
cdk diff

# Deploy: synthesize, then hand the resulting template to CloudFormation to create/update
# the stack (internally uses change sets, same rollback semantics as any CFN stack)
cdk deploy
```

### Stacks and apps
A CDK **App** is the root of the construct tree — the thing `cdk deploy`/`cdk synth` operate on. An app contains one or more **Stacks** (each mapping 1:1 to a CloudFormation stack), and each stack contains constructs. Multi-environment deployment in CDK is typically done by instantiating the *same stack class* multiple times with different `env` (account/Region) and configuration props — conceptually similar to SAM's parameter-overrides-per-environment pattern, but expressed as constructor arguments in code rather than a config file.

## 5. Comparison table — when to reach for which

| | CloudFormation (raw) | SAM | CDK |
|---|---|---|---|
| **Authoring format** | Declarative YAML/JSON | Declarative YAML/JSON (a CloudFormation transform/superset) | Imperative code (TypeScript, Python, Java, C#, Go) |
| **Best fit** | Any AWS resource, general infrastructure, when you want the template to be the literal source of truth | Serverless apps specifically (Lambda, API Gateway, DynamoDB, Step Functions) needing less boilerplate and strong local-testing tooling | Complex infra needing loops/conditionals/reuse, teams that want type safety and to stay in a familiar programming language |
| **What it deploys as** | A CloudFormation stack, directly | A CloudFormation stack, after the SAM transform expands shorthand resources | A CloudFormation stack, after `cdk synth` compiles code to a template |
| **Local testing story** | None built-in | `sam local invoke` / `sam local start-api` — genuinely strong local Lambda/API Gateway emulation | None built-in for running Lambda locally (though CDK apps can still be tested with unit-test assertions against the synthesized template) |
| **Boilerplate for Lambda+API Gateway+DynamoDB** | High — every permission, integration, and deployment resource written out by hand | Low — `AWS::Serverless::Function`'s `Events` block and SAM policy templates auto-generate the wiring | Low-to-medium — L2 constructs and grant methods (`grantReadData`) remove most boilerplate, but you're still explicitly wiring routes/integrations |
| **Learning curve** | Must learn the YAML/JSON DSL and every resource's property schema | Same DSL as CloudFormation, plus a small set of `Serverless::*` shorthand types | Must know the chosen programming language plus the CDK construct library API |
| **When it's the wrong tool** | Verbose/repetitive for large serverless apps with many near-identical functions | Not designed for non-serverless-centric infrastructure (e.g. a complex VPC/networking-only stack is awkward to express as "serverless") | Overkill/unnecessary ceremony for a small, static, rarely-changed template a team is happy to hand-edit as YAML |

**Rule of thumb the exam rewards:** if a scenario says "serverless application" and mentions wanting to **test Lambda functions locally before deployment**, the answer is SAM. If a scenario emphasizes **using loops, conditionals, or an existing programming language** to define infrastructure, or reusing infrastructure patterns across many similar resources, the answer is CDK. If the scenario is a **generic infrastructure requirement** with no serverless or "developer wants to code it" framing — or mentions **stack sets across many accounts**, **drift detection**, **nested stacks**, or **DeletionPolicy** by name — the answer is CloudFormation directly.

## 6. Worked real-world scenarios

**Scenario A — the same SAM app, three environments, one template.** A team builds the Orders API from Section 3 above. In `dev`, they want cheap, disposable, quickly-iterable infrastructure — smaller Lambda memory, a `dev` API stage, deployed to `us-east-1`. In `staging`, they want a closer-to-production setup for QA sign-off before a release, with `confirm_changeset = true` so nothing deploys without a human reviewing the change set first. In `prod`, they want larger Lambda memory for lower cold-start-sensitive latency, a separate Region (`us-west-2`) for disaster-recovery posture, and mandatory change-set confirmation. Rather than maintaining three template.yaml files (which would drift out of sync over time as someone updates one and forgets the others), the team keeps **one** `template.yaml` with a `StageName` and `MemorySizeParam` parameter, and defines three named environments in `samconfig.toml` (as shown in Section 3) with different `parameter_overrides`, `stack_name`, `region`, and `s3_bucket` values per environment. A developer runs `sam deploy --config-env dev` while iterating locally, and the same command with `--config-env staging` or `--config-env prod` from a CI/CD pipeline promotes the *exact same, already-tested* template to the next environment — the template never changes between environments, only the parameter values do. This is precisely what Domain 3 Task Statement 2 means by "deploying an AWS SAM template to a different staging environment."

**Scenario B — the change set that caught a database replacement before it happened.** An engineer needs to change an RDS instance's `DBInstanceClass` in a CloudFormation-managed stack, and separately (in the same template edit) accidentally changes the `Engine` property from `mysql` to `mariadb` — a change that CloudFormation cannot apply in-place, because switching engines requires **replacing** the RDS resource entirely (delete the old instance, create a new one). If the engineer ran `aws cloudformation update-stack` directly, this replacement would proceed silently and the production database — along with all its data — would be destroyed and recreated empty (unless `DeletionPolicy`/`UpdateReplacePolicy` happened to be set to `Snapshot`, which only preserves a snapshot, not zero-downtime continuity). Instead, the team's deployment pipeline is required to run `aws cloudformation create-change-set` first, and a teammate reviews the output before anyone calls `execute-change-set`. The change set output explicitly flags the RDS resource with `"Replacement": "True"` and lists `Engine` as the property forcing it — the reviewer catches the accidental typo immediately, fixes it back to `mysql`, and regenerates the change set, which now shows only a `Modify` (in-place, no replacement) for `DBInstanceClass`. **Lesson:** change sets exist specifically to surface silent-but-catastrophic actions like an unintended resource replacement before they execute, and any pipeline touching stateful resources should make change-set review a mandatory gate.

**Scenario C — CDK loops replacing forty lines of copy-pasted YAML.** A data-processing team needs eight nearly-identical Lambda functions, one per data source (`orders`, `inventory`, `shipping`, `returns`, and four more), each reading from its own S3 prefix, writing to its own DynamoDB table, and alarming on errors via the same CloudWatch alarm pattern. Written as raw CloudFormation or SAM YAML, this means eight near-duplicate `AWS::Serverless::Function` blocks (or eight duplicate `Function`+`Table`+`Alarm` triples), differing only by name and a couple of parameters — tedious to keep in sync when the *shared* configuration (timeout, runtime version, alarm threshold) needs to change across all eight at once. In CDK, the team instead writes one small function that takes a data-source name and returns a configured Lambda+DynamoDB+Alarm construct group, then calls it in a loop over an array of the eight source names:
```typescript
const sources = ["orders", "inventory", "shipping", "returns", "payments", "refunds", "catalog", "pricing"];
for (const source of sources) {
  new DataSourceProcessor(this, `${source}Processor`, { sourceName: source });
}
```
Updating the shared timeout or alarm threshold for all eight now means changing it in one place (`DataSourceProcessor`'s definition) rather than eight YAML blocks, and `cdk diff` shows exactly what changes across all eight stacks' worth of resources before `cdk deploy` applies it. **Lesson:** the moment infrastructure has real repetition with shared logic, CDK's use of an actual programming language starts paying for itself over hand-written YAML.

## 7. Key exam traps

- SAM and CDK both ultimately deploy as a **CloudFormation stack** — change sets, rollback-on-failure, drift detection, `DeletionPolicy`, and nested-stack behavior all still apply underneath either tool.
- `Ref` vs. `GetAtt`: `Ref` returns a resource's primary/default identifier; `GetAtt` is required for any other attribute (like an ARN or public IP).
- `DeletionPolicy: Retain` (or `Snapshot`) protects a **stateful resource from being deleted when the stack is deleted**; `UpdateReplacePolicy` protects it specifically from an **update-triggered replacement**. These are two different triggers and the exam tests the distinction.
- A stack **cannot delete/modify an exported Output value while another stack still imports it** via `Fn::ImportValue` — this is the classic "why won't my stack update" scenario.
- **Change sets preview, they don't apply** — always the correct answer when a scenario asks how to safely verify what a template update will do before committing to it in production, especially around potential resource replacement.
- Drift detection is **read-only** — it reports divergence between the live stack and the template; it does not remediate anything automatically.
- `sam local invoke` / `sam local start-api` are the go-to answer for **testing Lambda/API Gateway locally without deploying** — a very frequently tested capability.
- Deploying a SAM template to a new environment/stage is done via **parameter overrides / SAM config environments**, not by hand-editing or duplicating the template.
- Custom resources (Lambda-backed) are the escape hatch whenever CloudFormation has no native resource type for something the scenario needs.
- CDK's `cdk synth` produces a CloudFormation template; `cdk deploy` is not a separate deployment engine, it hands that template to CloudFormation.
- Choosing between the three tools on the exam: **serverless + local testing emphasis → SAM**; **loops/conditionals/existing programming language/pattern-reuse emphasis → CDK**; **generic/non-serverless infra, stack sets, or explicit CloudFormation-feature naming → raw CloudFormation**.
- Nested stacks (composed within one parent, deployed together) are a different mechanism from cross-stack `Fn::ImportValue` references (independent stacks, loosely coupled via exported Outputs) — don't conflate the two when a question asks specifically about either.
