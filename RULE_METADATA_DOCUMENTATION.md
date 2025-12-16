# Rule Metadata Documentation for RCP Migration Assessment

## Overview
This document provides comprehensive metadata for all 17 detection rules used in the RCP (managed EKS) migration assessment. These rules identify platform-specific dependencies that need to be addressed when migrating applications from ECS, KMC, MPaaS, HCom, and CPI to RCP.

**Extraction Date:** 2024-12-19  
**Total Rules:** 17  
**Category:** Portability > Container Platform Dependencies

---

## Rule Metadata Structure

Each rule contains the following metadata fields:

### Core Fields
- **ruleId**: Unique identifier (e.g., `rcp-java-0001`)
- **ruleName**: Human-readable rule name
- **version**: Rule version (currently `1.0`)
- **status**: Rule status (`active`, `deprecated`, `experimental`)
- **parser**: Detection method (`REGEX`, `AST`, `SEMANTIC`)

### Priority & Severity
- **priority**: Migration priority (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- **severity**: Impact severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- **severityWeight**: Points added to complexity score (CRITICAL: 25, HIGH: 15, MEDIUM: 8, LOW: 3)
- **blockerType**: Classification for dashboard filtering

### Categorization
- **category**: Primary category (SERVICE_DISCOVERY, SECRETS_CONFIG, etc.)
- **subCategory**: Always "Container Platform Dependencies" for these rules

### Language Support
- **language.name**: Supported language (`java`)
- **language.versions**: Supported Java versions (`["8", "11", "17", "21"]`)
- **language.frameworks**: Supported frameworks (`["spring-boot:3.0", "jakarta-ee:10"]`)

### Detection Criteria
- **detectionCriteria.fileType**: File types to scan (`["java", "properties", "yml"]`)
- **detectionCriteria.searchPattern**: Regex patterns to match
- **detectionCriteria.inverse**: If `true`, rule triggers when pattern is NOT found (for missing patterns)

### Migration Guidance
- **migrationGuidance**: Recommended migration approach
- **effortEstimate**: Estimated remediation time
- **dashboardLabel**: Display name for dashboard

---

## Rules by Priority

### CRITICAL Priority (1 rule)
**Severity Weight: 25 points**

| Rule ID | Rule Name | Effort | Blocker Type |
|---------|-----------|--------|--------------|
| rcp-java-0012 | Hardcoded AWS Credentials | 1 hour | CRITICAL Security Blocker |

### HIGH Priority (7 rules)
**Severity Weight: 15 points each**

| Rule ID | Rule Name | Effort | Blocker Type |
|---------|-----------|--------|--------------|
| rcp-java-0001 | ECS Cloud Map Service Discovery | 8 hours | HIGH Priority Blocker |
| rcp-java-0002 | Consul Service Discovery | 8 hours | HIGH Priority Blocker |
| rcp-java-0003 | Eureka Service Discovery | 12 hours | HIGH Priority Blocker |
| rcp-java-0004 | AWS Parameter Store Usage | 6 hours | HIGH Priority Blocker |
| rcp-java-0005 | AWS Secrets Manager Usage | 6 hours | HIGH Priority Blocker |
| rcp-java-0006 | Direct Vault Access (HCOM/EWE/VRBO) | 4 hours | HIGH Priority Blocker |
| rcp-java-0007 | ECS Task Metadata Access | 4 hours | HIGH Priority Blocker |
| rcp-java-0014 | ECS-Specific API Calls | 12 hours | HIGH Priority Blocker |

### MEDIUM Priority (7 rules)
**Severity Weight: 8 points each**

| Rule ID | Rule Name | Effort | Blocker Type |
|---------|-----------|--------|--------------|
| rcp-java-0008 | EC2 Instance Metadata Access | 3 hours | MEDIUM Priority Blocker |
| rcp-java-0009 | Missing Health Check Endpoints | 2 hours | MEDIUM Priority Blocker |
| rcp-java-0010 | CloudWatch Direct Logging | 3 hours | MEDIUM Priority Blocker |
| rcp-java-0013 | ECS Task Role Assumptions | 3 hours | MEDIUM Priority Blocker |
| rcp-java-0016 | Platform-Specific APM Configuration | 3 hours | MEDIUM Priority Blocker |
| rcp-java-0017 | Missing Graceful Shutdown Handling | 4 hours | MEDIUM Priority Blocker |

### LOW Priority (2 rules)
**Severity Weight: 3 points each**

| Rule ID | Rule Name | Effort | Blocker Type |
|---------|-----------|--------|--------------|
| rcp-java-0011 | Platform-Specific Logging Drivers | 2 hours | LOW Priority |
| rcp-java-0015 | Docker Compose Dependencies | 4 hours | LOW Priority |

---

## Rules by Category

### SERVICE_DISCOVERY (3 rules)
- rcp-java-0001: ECS Cloud Map Service Discovery
- rcp-java-0002: Consul Service Discovery
- rcp-java-0003: Eureka Service Discovery

### SECRETS_CONFIG (3 rules)
- rcp-java-0004: AWS Parameter Store Usage
- rcp-java-0005: AWS Secrets Manager Usage
- rcp-java-0006: Direct Vault Access (HCOM/EWE/VRBO)

### METADATA (2 rules)
- rcp-java-0007: ECS Task Metadata Access
- rcp-java-0008: EC2 Instance Metadata Access

### HEALTH_CHECK (1 rule)
- rcp-java-0009: Missing Health Check Endpoints (inverse detection)

### LOGGING (2 rules)
- rcp-java-0010: CloudWatch Direct Logging
- rcp-java-0011: Platform-Specific Logging Drivers

### SECURITY (1 rule)
- rcp-java-0012: Hardcoded AWS Credentials

### AWS_SDK (1 rule)
- rcp-java-0013: ECS Task Role Assumptions

### ORCHESTRATION (2 rules)
- rcp-java-0014: ECS-Specific API Calls
- rcp-java-0015: Docker Compose Dependencies

### OBSERVABILITY (1 rule)
- rcp-java-0016: Platform-Specific APM Configuration

### SIGNAL_HANDLING (1 rule)
- rcp-java-0017: Missing Graceful Shutdown Handling (inverse detection)

---

## Complexity Scoring Logic

### Score Calculation
Applications receive complexity scores (0-100) based on detected patterns:

- **CRITICAL patterns**: 25 points each
- **HIGH patterns**: 15 points each
- **MEDIUM patterns**: 8 points each
- **LOW patterns**: 3 points each

**Formula:** `Score = Σ(severityWeight × patternCount)` capped at 100

### Complexity Levels

| Level | Score Range | Description | Migration Effort |
|-------|-------------|-------------|------------------|
| **MINIMAL** | 0-20 | Config-only changes | 1-2 days |
| **LOW** | 21-40 | Minor code refactoring | 3-5 days |
| **MEDIUM** | 41-60 | Moderate changes | 1-2 weeks |
| **HIGH** | 61-80 | Significant refactoring | 2-4 weeks |
| **CRITICAL** | 81-100 | Major effort needed | 1-2 months |

---

## Readiness Metrics

### Application Readiness Categories

1. **Ready to Migrate** (0 blockers)
   - No platform-specific dependencies detected
   - Can proceed with migration immediately

2. **In Remediation** (1-5 blockers)
   - Minor to moderate issues detected
   - Can be addressed in parallel with migration planning

3. **Requiring Architecture Review** (6+ blockers)
   - Significant platform dependencies
   - Requires architecture review and migration strategy

---

## Dashboard Requirements

### Application Portfolio View
- Total applications by source platform (ECS, KMC, MPaaS, HCom, CPI)
- Complexity distribution (Minimal, Low, Medium, High, Critical)
- Priority distribution (P1, P2, P3, P4)
- Blocker pattern frequency across portfolio

### Priority Mapping (P1-P4)
- **P1**: Critical complexity (81-100) OR ECS with 15+ findings
- **P2**: High complexity (61-80) OR ECS with 8+ findings
- **P3**: Medium complexity (41-60)
- **P4**: Low complexity (0-40)

### Blocker Pattern Frequency
Track frequency of each blocker pattern across the portfolio:
- ECS Service Discovery
- AWS Parameter Store Direct Access
- AWS Secrets Manager Direct Access
- ECS Orchestration APIs
- Hardcoded Service IPs
- Platform-Specific Vault Endpoints
- Missing Kubernetes Health Endpoints
- CloudWatch Direct Logging
- EC2 Instance Metadata
- ECS Task Role Assumptions
- Missing Graceful Shutdown
- Platform-Specific APM Configuration
- Hardcoded AWS Credentials

---

## Migration Guidance Summary

### HIGH Priority Blockers → RCP Equivalents

| ECS Pattern | RCP Equivalent |
|-------------|----------------|
| AWS Cloud Map | Kubernetes DNS (service-name.namespace.svc.cluster.local) |
| ECS Task Metadata (169.254.170.2) | Kubernetes Downward API |
| AWS Parameter Store | EG Vault with CSI driver |
| AWS Secrets Manager | EG Vault integration |
| ECS APIs (describe_tasks, run_task) | Kubernetes API or remove |
| HCOM/EWE/VRBO Vault | EG Vault |

### MEDIUM Priority Blockers → RCP Equivalents

| ECS Pattern | RCP Equivalent |
|-------------|----------------|
| Missing /healthz, /ready | Implement Kubernetes health endpoints |
| CloudWatch SDK logging | stdout/stderr (auto-captured) |
| EC2 Metadata (169.254.169.254) | Kubernetes Downward API or node labels |
| ECS Task Role | IRSA (IAM Roles for Service Accounts) |
| Missing SIGTERM handling | Implement graceful shutdown |
| ECS-specific Datadog config | Kubernetes Datadog agent |

### Security Blockers

| Pattern | RCP Solution |
|---------|--------------|
| Hardcoded AWS Credentials | IRSA (IAM Roles for Service Accounts) |

---

## Integration Notes for Concierto Modernize

### Rule Integration Points
1. **Assessment Engine**: Integrate rules into existing portability assessment
2. **Category Mapping**: Add to "Portability" > "Container Platform Dependencies"
3. **Scoring Engine**: Use severity weights for complexity calculation
4. **Dashboard**: Display findings grouped by priority and category

### Expected Output Format
```json
{
  "ruleId": "rcp-java-0001",
  "ruleName": "ECS Cloud Map Service Discovery",
  "status": "violation",
  "filePath": "src/main/java/ServiceDiscovery.java",
  "lineNumber": 45,
  "codeSnippet": "servicediscovery.client",
  "severity": "HIGH",
  "priority": "HIGH",
  "migrationGuidance": "Replace with Kubernetes DNS...",
  "effortEstimate": "8 hours"
}
```

---

## Next Steps for Demo

1. **Rule Integration**: Import all 17 rules into Concierto Modernize assessment engine
2. **Dashboard Development**: Build Figma screens showing:
   - Application readiness scores by complexity level
   - Code repos assessed by platform
   - Progress tracking of migrated apps
   - Blocker pattern frequency charts
   - Effort estimates and timeline projections
3. **Test Repository**: Use the `ecs-sample-app` repository to validate rule detection
4. **Sample Assessment**: Run assessment on sample ECS applications to generate demo data

---

## ETA for Readiness

**Target Completion:** Next week (before Expedia demo)

**Deliverables:**
- ✅ Rule metadata extraction (this document)
- ⏳ Rule integration into Concierto Modernize
- ⏳ Dashboard Figma designs
- ⏳ Sample assessment results
- ⏳ Demo environment setup

**Critical Path:**
1. Rule integration (2-3 days)
2. Dashboard design (1-2 days)
3. Testing and validation (1 day)
4. Demo environment preparation (1 day)

