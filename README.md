# ECS Sample Application

This is a sample Java Spring Boot application that demonstrates various ECS-specific patterns and dependencies. This application is designed to be scanned for migration compatibility assessment when moving from ECS to RCP (managed EKS).

## Purpose

This repository contains code patterns that should trigger violations when scanned with the rules defined in `java-rcp-detect-rules.json`. It serves as a test repository for validating the migration assessment tooling.

## Detected Patterns

This application intentionally includes the following patterns that need migration:

### Service Discovery
- **ECS Cloud Map Service Discovery** - Uses servicediscovery.client and servicediscovery.discover_instances
- **Consul Service Discovery** - Uses consul.Consul, consul.catalog, and consul.health.service
- **Eureka Service Discovery** - Uses @EnableEurekaClient and eureka.client configuration

### Secrets & Configuration Management
- **AWS Parameter Store Usage** - Uses GetParameter and SSM client
- **AWS Secrets Manager Usage** - Uses GetSecretValue
- **Direct Vault Access** - Accesses HCOM, EWE, and VRBO Vault endpoints

### Metadata Service Access
- **ECS Task Metadata Access** - Accesses 169.254.170.2 and ECS_CONTAINER_METADATA_URI
- **EC2 Instance Metadata Access** - Accesses 169.254.169.254 and instance-identity

### Health Checks
- **Missing Health Check Endpoints** - Intentionally does NOT have /health or /healthz endpoints

### Logging
- **CloudWatch Direct Logging** - Uses CloudWatchLogHandler and put_log_events
- **Platform-Specific Logging Drivers** - Uses awslogs log driver in docker-compose.yml

### AWS SDK & Credentials
- **Hardcoded AWS Credentials** - Contains aws_access_key_id and aws_secret_access_key
- **ECS Task Role Assumptions** - Uses ECS_TASK_ROLE and task-role patterns

### Container/Orchestration Specific
- **ECS-Specific API Calls** - Uses ECS API calls (describe_tasks, list_tasks, run_task)
- **Docker Compose Dependencies** - Uses depends_on in docker-compose.yml

### Observability
- **Platform-Specific APM Configuration** - Uses DD_AGENT_HOST with 169.254.170.2 and DD_ECS_COLLECT

### Signal Handling
- **Missing Graceful Shutdown Handling** - Intentionally does NOT have shutdown hooks or @PreDestroy

## Building the Application

```bash
mvn clean package
```

## Running with Docker Compose

```bash
docker-compose up
```

## Running on ECS

Deploy using the provided `task-definition.json`:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster my-cluster --service-name ecs-sample-app --task-definition ecs-sample-app
```

## Migration Notes

All patterns in this application should be flagged by the migration assessment tool and require updates for RCP compatibility:

1. Service discovery should use Kubernetes DNS
2. Secrets should use EG Vault with CSI driver
3. Metadata should use Kubernetes Downward API
4. Health checks should implement /healthz and /ready endpoints
5. Logging should use stdout/stderr
6. Credentials should use IRSA (IAM Roles for Service Accounts)
7. ECS API calls should be replaced with Kubernetes API or removed
8. Graceful shutdown should be implemented

