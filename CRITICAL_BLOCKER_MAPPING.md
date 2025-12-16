# Critical Blocker Patterns Mapping

## Mapping of User Requirements to Rule IDs

This document maps the critical blocker patterns specified in the requirements to the corresponding rule IDs from `java-rcp-detect-rules.json`.

---

## HIGH Priority Blockers (Must Fix)

### ✅ ECS Service Discovery
**Requirement:** Applications using AWS Cloud Map API instead of Kubernetes DNS

**Mapped Rules:**
- **rcp-java-0001**: ECS Cloud Map Service Discovery
  - Patterns: `servicediscovery.client`, `servicediscovery.discover_instances`, `Cloud Map`
  - Severity: HIGH (15 points)
  - Effort: 8 hours

**Additional Service Discovery Patterns:**
- **rcp-java-0002**: Consul Service Discovery (HIGH, 15 points, 8 hours)
- **rcp-java-0003**: Eureka Service Discovery (HIGH, 15 points, 12 hours)

---

### ✅ ECS Task Metadata
**Requirement:** Code accessing ECS metadata endpoint (169.254.170.2) for container info

**Mapped Rule:**
- **rcp-java-0007**: ECS Task Metadata Access
  - Patterns: `169.254.170.2`, `ECS_CONTAINER_METADATA_URI`, `ECS_TASK_METADATA`, `/v[234]/metadata`
  - Severity: HIGH (15 points)
  - Effort: 4 hours

---

### ✅ AWS Parameter Store Direct Access
**Requirement:** SDK calls to retrieve configuration instead of EG Vault

**Mapped Rule:**
- **rcp-java-0004**: AWS Parameter Store Usage
  - Patterns: `ssm.get_parameter`, `GetParameter`, `get_parameters_by_path`
  - Severity: HIGH (15 points)
  - Effort: 6 hours

---

### ✅ AWS Secrets Manager Direct Access
**Requirement:** Direct API calls for secrets instead of EG Vault integration

**Mapped Rule:**
- **rcp-java-0005**: AWS Secrets Manager Usage
  - Patterns: `secretsmanager.get_secret_value`, `GetSecretValue`
  - Severity: HIGH (15 points)
  - Effort: 6 hours

---

### ✅ ECS Orchestration APIs
**Requirement:** Applications calling ECS APIs (describe_tasks, run_task) for automation

**Mapped Rule:**
- **rcp-java-0014**: ECS-Specific API Calls
  - Patterns: `ecs.describe_tasks`, `ecs.list_tasks`, `ecs.run_task`
  - Severity: HIGH (15 points)
  - Effort: 12 hours

---

### ✅ Hardcoded Service IPs
**Requirement:** Applications with hardcoded IP addresses instead of service names

**Note:** This pattern is partially covered by:
- **rcp-java-0007**: ECS Task Metadata Access (169.254.170.2)
- **rcp-java-0008**: EC2 Instance Metadata Access (169.254.169.254)

**Recommendation:** May need additional rule for general hardcoded IP detection beyond metadata endpoints.

---

### ✅ Platform-Specific Vault Endpoints
**Requirement:** Apps pointing to HCOM/EWE/VRBO Vault instead of EG Vault

**Mapped Rule:**
- **rcp-java-0006**: Direct Vault Access (HCOM/EWE/VRBO)
  - Patterns: `HCOM Vault`, `EWE Vault`, `VRBO Vault`, `hvac.Client.*vault.hcom`, `hvac.Client.*vault.ewe`
  - Severity: HIGH (15 points)
  - Effort: 4 hours

---

## MEDIUM Priority Blockers (Should Fix)

### ✅ Missing Kubernetes Health Endpoints
**Requirement:** No /healthz (liveness) or /ready (readiness) endpoints

**Mapped Rule:**
- **rcp-java-0009**: Missing Health Check Endpoints
  - Patterns: `/health`, `/healthz`, `@GetMapping.*health`, `@RequestMapping.*health`
  - Detection: **INVERSE** (triggers when patterns are NOT found)
  - Severity: MEDIUM (8 points)
  - Effort: 2 hours

---

### ✅ CloudWatch Direct Logging
**Requirement:** Using watchtower or CloudWatch SDK instead of stdout/stderr

**Mapped Rule:**
- **rcp-java-0010**: CloudWatch Direct Logging
  - Patterns: `import watchtower`, `CloudWatchLogHandler`, `put_log_events`
  - Severity: MEDIUM (8 points)
  - Effort: 3 hours

**Additional Logging Pattern:**
- **rcp-java-0011**: Platform-Specific Logging Drivers (LOW, 3 points, 2 hours)
  - Patterns: `awslogs`, `log_driver.*awslogs`, `fluentd.*ecs`

---

### ✅ EC2 Instance Metadata
**Requirement:** Accessing EC2 metadata service (169.254.169.254) for instance info

**Mapped Rule:**
- **rcp-java-0008**: EC2 Instance Metadata Access
  - Patterns: `169.254.169.254`, `instance-identity`, `ec2.metadata`
  - Severity: MEDIUM (8 points)
  - Effort: 3 hours

---

### ✅ ECS Task Role Assumptions
**Requirement:** Code expecting ambient IAM credentials instead of IRSA

**Mapped Rule:**
- **rcp-java-0013**: ECS Task Role Assumptions
  - Patterns: `ECS_TASK_ROLE`, `task-role`, `get_credentials.*ecs`
  - Severity: MEDIUM (8 points)
  - Effort: 3 hours

---

### ✅ Missing Graceful Shutdown
**Requirement:** No SIGTERM signal handling for pod termination

**Mapped Rule:**
- **rcp-java-0017**: Missing Graceful Shutdown Handling
  - Patterns: `Runtime.getRuntime().addShutdownHook`, `@PreDestroy`, `shutdown hook`
  - Detection: **INVERSE** (triggers when patterns are NOT found)
  - Severity: MEDIUM (8 points)
  - Effort: 4 hours

---

### ✅ Platform-Specific APM Configuration
**Requirement:** ECS-specific Datadog or APM agent setup

**Mapped Rule:**
- **rcp-java-0016**: Platform-Specific APM Configuration
  - Patterns: `DD_AGENT_HOST.*169.254`, `statsd.*ecs`, `DD_ECS_COLLECT`
  - Severity: MEDIUM (8 points)
  - Effort: 3 hours

---

### ⚠️ ALB-Specific Header Dependencies
**Requirement:** Code relying on X-Amzn-* headers from ALB

**Status:** **NOT CURRENTLY COVERED** by existing rules

**Recommendation:** Add new rule:
- **rcp-java-0018**: ALB-Specific Header Dependencies
  - Patterns: `X-Amzn-`, `X-Amzn-RequestId`, `X-Amzn-Trace-Id`
  - Severity: MEDIUM (8 points)
  - Effort: 2 hours

---

## CRITICAL Security Blockers

### ✅ Hardcoded AWS Credentials
**Requirement:** AWS access keys or secrets in code (immediate security risk)

**Mapped Rule:**
- **rcp-java-0012**: Hardcoded AWS Credentials
  - Patterns: `aws_access_key_id=`, `aws_secret_access_key=`, `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`
  - Severity: **CRITICAL** (25 points)
  - Effort: 1 hour
  - **Highest Priority**: Immediate remediation required

---

## Summary: Coverage Status

| Requirement | Rule ID | Status | Priority |
|-------------|---------|--------|----------|
| ECS Service Discovery | rcp-java-0001, 0002, 0003 | ✅ Covered | HIGH |
| ECS Task Metadata | rcp-java-0007 | ✅ Covered | HIGH |
| AWS Parameter Store | rcp-java-0004 | ✅ Covered | HIGH |
| AWS Secrets Manager | rcp-java-0005 | ✅ Covered | HIGH |
| ECS Orchestration APIs | rcp-java-0014 | ✅ Covered | HIGH |
| Hardcoded Service IPs | rcp-java-0007, 0008 | ⚠️ Partial | HIGH |
| Platform Vault Endpoints | rcp-java-0006 | ✅ Covered | HIGH |
| Missing Health Endpoints | rcp-java-0009 | ✅ Covered | MEDIUM |
| CloudWatch Direct Logging | rcp-java-0010, 0011 | ✅ Covered | MEDIUM |
| EC2 Instance Metadata | rcp-java-0008 | ✅ Covered | MEDIUM |
| ECS Task Role Assumptions | rcp-java-0013 | ✅ Covered | MEDIUM |
| Missing Graceful Shutdown | rcp-java-0017 | ✅ Covered | MEDIUM |
| Platform APM Configuration | rcp-java-0016 | ✅ Covered | MEDIUM |
| ALB Header Dependencies | - | ❌ Missing | MEDIUM |
| Hardcoded AWS Credentials | rcp-java-0012 | ✅ Covered | CRITICAL |

**Coverage:** 14/15 requirements (93.3%)  
**Missing:** ALB-Specific Header Dependencies

---

## Recommendations

1. **Add Missing Rule**: Create `rcp-java-0018` for ALB header dependencies
2. **Enhance Hardcoded IP Detection**: Consider adding specific rule for non-metadata hardcoded IPs
3. **Priority Alignment**: All HIGH priority blockers are correctly mapped to HIGH severity rules
4. **Security Focus**: CRITICAL security blocker (hardcoded credentials) is properly identified with highest weight (25 points)

---

## Dashboard Integration Notes

### Blocker Pattern Frequency Tracking
The dashboard should track these specific patterns:
1. ECS Service Discovery (rcp-java-0001, 0002, 0003)
2. AWS Parameter Store Direct Access (rcp-java-0004)
3. AWS Secrets Manager Direct Access (rcp-java-0005)
4. ECS Orchestration APIs (rcp-java-0014)
5. Hardcoded Service IPs (rcp-java-0007, 0008)
6. Platform-Specific Vault Endpoints (rcp-java-0006)
7. Missing Kubernetes Health Endpoints (rcp-java-0009)
8. CloudWatch Direct Logging (rcp-java-0010, 0011)
9. EC2 Instance Metadata (rcp-java-0008)
10. ECS Task Role Assumptions (rcp-java-0013)
11. Missing Graceful Shutdown (rcp-java-0017)
12. Platform-Specific APM Configuration (rcp-java-0016)
13. Hardcoded AWS Credentials (rcp-java-0012) - **CRITICAL**

### Readiness Calculation
- **0 blockers**: Ready to migrate
- **1-5 blockers**: In remediation
- **6+ blockers**: Requiring architecture review

