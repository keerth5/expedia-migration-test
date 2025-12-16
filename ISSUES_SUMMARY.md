# Issues Summary - Modified Repository

This repository has been modified to identify only the following issues:

## CRITICAL Issues (1)

### rcp-java-0012: Hardcoded AWS Credentials
- **Severity**: CRITICAL (25 points)
- **Location**: 
  - `docker-compose.yml` (lines 10-11)
  - `src/main/resources/application.properties` (lines 11-14)
  - `src/main/resources/application.yml` (lines 16-27)
  - `src/main/java/com/expedia/ecs/service/AwsConfigService.java` (lines 26-35)
- **Patterns Detected**: `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `aws.access.key.id`, `aws.secret.access.key`

## HIGH Issues (1)

### rcp-java-0003: Eureka Service Discovery
- **Severity**: HIGH (15 points)
- **Location**:
  - `src/main/java/com/expedia/ecs/EcsSampleApplication.java` (line 12: `@EnableEurekaClient`)
  - `src/main/resources/application.properties` (lines 5-8)
  - `src/main/resources/application.yml` (lines 4-11)
- **Patterns Detected**: `@EnableEurekaClient`, `eureka.client`

## MEDIUM Issues (5)

### rcp-java-0009: Missing Health Check Endpoints
- **Severity**: MEDIUM (8 points)
- **Location**: Intentionally missing from `src/main/java/com/expedia/ecs/controller/ApiController.java`
- **Patterns**: No `/healthz` or `/ready` endpoints found

### rcp-java-0010: CloudWatch Direct Logging
- **Severity**: MEDIUM (8 points)
- **Location**: `src/main/java/com/expedia/ecs/logging/CloudWatchLogHandler.java`
- **Patterns Detected**: `CloudWatchLogHandler`, `put_log_events`, `boto3.client("logs")`

### rcp-java-0013: ECS Task Role Assumptions
- **Severity**: MEDIUM (8 points)
- **Location**:
  - `src/main/java/com/expedia/ecs/service/TaskRoleService.java`
  - `src/main/resources/application.properties` (line 17)
  - `src/main/resources/application.yml` (lines 29-33)
  - `Dockerfile` (line 8)
  - `docker-compose.yml` (line 9)
- **Patterns Detected**: `ECS_TASK_ROLE`, `task-role`, `get_credentials.ecs`

### rcp-java-0016: Platform-Specific APM Configuration
- **Severity**: MEDIUM (8 points)
- **Location**:
  - `Dockerfile` (lines 11-12)
  - `docker-compose.yml` (lines 12-13)
  - `src/main/resources/application.properties` (lines 31-34)
  - `src/main/resources/application.yml` (lines 56-65)
- **Patterns Detected**: `DD_AGENT_HOST.*169.254`, `DD_ECS_COLLECT`, `statsd.ecs`

### rcp-java-0017: Missing Graceful Shutdown Handling
- **Severity**: MEDIUM (8 points)
- **Location**: Intentionally missing from application code
- **Patterns**: No `Runtime.getRuntime().addShutdownHook`, `@PreDestroy`, or `spring.lifecycle.timeout-per-shutdown-phase` found

## Removed Issues

The following issues have been removed from the repository:

### HIGH Priority (Removed)
- **rcp-java-0007**: ECS Task Metadata Access (removed from Dockerfile, application.properties, application.yml; MetadataService.java deleted)
- **rcp-java-0014**: ECS-Specific API Calls (EcsApiService.java deleted)
- **rcp-java-0006**: Direct Vault Access (VaultService.java deleted, removed from application.yml)
- **rcp-java-0004**: AWS Parameter Store Usage (removed from AwsConfigService.java)
- **rcp-java-0005**: AWS Secrets Manager Usage (removed from AwsConfigService.java)

### MEDIUM Priority (Removed)
- **rcp-java-0008**: EC2 Instance Metadata Access (removed from application.properties, application.yml; MetadataService.java deleted)

### LOW Priority (Removed)
- **rcp-java-0011**: Platform-Specific Logging Drivers (removed awslogs from docker-compose.yml)
- **rcp-java-0015**: Docker Compose Dependencies (removed depends_on from docker-compose.yml)

## Total Issues Count

- **CRITICAL**: 1 issue
- **HIGH**: 1 issue
- **MEDIUM**: 5 issues
- **LOW**: 0 issues

**Total**: 7 issues

