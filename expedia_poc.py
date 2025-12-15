#!/usr/bin/env python3
"""
Platform Migration Assessment Framework and Code Scanner
Identifies platform-specific dependencies in applications migrating to RCP (managed EKS)

Usage:
    python migration_code_scanner.py --repo-path /path/to/repo
    python migration_code_scanner.py --scan-directory /path/to/apps --output report.json
"""

import os
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Finding:
    """Represents a single code pattern finding"""
    category: str
    severity: str  # HIGH, MEDIUM, LOW
    pattern: str
    file_path: str
    line_number: int
    code_snippet: str
    recommendation: str


@dataclass
class AssessmentResult:
    """Overall assessment result for an application"""
    app_name: str
    app_path: str
    source_platform: str
    complexity_score: int  # 0-100
    complexity_level: str  # MINIMAL, LOW, MEDIUM, HIGH, CRITICAL
    findings: List[Finding]
    summary: Dict[str, int]
    estimated_effort_hours: int
    priority: str  # P1, P2, P3, P4

    def to_dict(self):
        return {
            'app_name': self.app_name,
            'app_path': self.app_path,
            'source_platform': self.source_platform,
            'complexity_score': self.complexity_score,
            'complexity_level': self.complexity_level,
            'findings_count': len(self.findings),
            'findings': [asdict(f) for f in self.findings],
            'summary': self.summary,
            'estimated_effort_hours': self.estimated_effort_hours,
            'priority': self.priority
        }


class MigrationPatternRules:
    """
    Defines patterns to detect platform-specific code that needs modification
    """

    # Category: Service Discovery
    SERVICE_DISCOVERY_PATTERNS = {
        'ecs_cloud_map': {
            'patterns': [
                r'servicediscovery\.client',
                r'servicediscovery\.discover_instances',
                r'Cloud\s*Map',
                r'boto3\.client\([\'"]servicediscovery[\'"]\)',
            ],
            'severity': 'HIGH',
            'effort_hours': 8,
            'recommendation': 'Replace with Kubernetes DNS-based service discovery (service-name.namespace.svc.cluster.local)'
        },
        'consul_discovery': {
            'patterns': [
                r'import\s+consul',
                r'consul\.Consul',
                r'consul\.catalog',
                r'consul\.health\.service',
            ],
            'severity': 'HIGH',
            'effort_hours': 8,
            'recommendation': 'Migrate to Kubernetes service discovery'
        },
        'eureka_discovery': {
            'patterns': [
                r'@EnableEurekaClient',
                r'eureka\.client',
                r'netflix\.eureka',
            ],
            'severity': 'HIGH',
            'effort_hours': 12,
            'recommendation': 'Replace Eureka with Kubernetes service discovery'
        }
    }

    # Category: Secrets & Configuration Management
    SECRETS_CONFIG_PATTERNS = {
        'aws_parameter_store': {
            'patterns': [
                r'ssm\.get_parameter',
                r'boto3\.client\([\'"]ssm[\'"]\)',
                r'GetParameter',
                r'get_parameters_by_path',
            ],
            'severity': 'HIGH',
            'effort_hours': 6,
            'recommendation': 'Migrate to EG Vault with CSI driver or Vault SDK'
        },
        'aws_secrets_manager': {
            'patterns': [
                r'secretsmanager\.get_secret_value',
                r'boto3\.client\([\'"]secretsmanager[\'"]\)',
                r'GetSecretValue',
            ],
            'severity': 'HIGH',
            'effort_hours': 6,
            'recommendation': 'Migrate to EG Vault integration'
        },
        'vault_direct_access': {
            'patterns': [
                r'HCOM[_\s]*Vault',
                r'EWE[_\s]*Vault',
                r'VRBO[_\s]*Vault',
                r'hvac\.Client.*vault\.hcom',
                r'hvac\.Client.*vault\.ewe',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 4,
            'recommendation': 'Update Vault endpoint to EG Vault'
        }
    }

    # Category: Metadata Service Access
    METADATA_PATTERNS = {
        'ecs_task_metadata': {
            'patterns': [
                r'169\.254\.170\.2',
                r'ECS_CONTAINER_METADATA_URI',
                r'ECS_TASK_METADATA',
                r'\/v[234]\/metadata',
            ],
            'severity': 'HIGH',
            'effort_hours': 4,
            'recommendation': 'Replace with Kubernetes Downward API'
        },
        'ec2_instance_metadata': {
            'patterns': [
                r'169\.254\.169\.254',
                r'instance-identity',
                r'ec2\.metadata',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 3,
            'recommendation': 'Use Kubernetes Downward API or node labels'
        }
    }

    # Category: Health Checks
    HEALTH_CHECK_PATTERNS = {
        'missing_health_endpoints': {
            'patterns': [
                r'/health',
                r'/healthz',
                r'@GetMapping.*health',
                r'@RequestMapping.*health',
                r'app\.route\([\'"].*health',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 2,
            'recommendation': 'Implement /healthz (liveness) and /ready (readiness) endpoints',
            'inverse': True  # This is a check for ABSENCE of pattern
        }
    }

    # Category: Logging
    LOGGING_PATTERNS = {
        'cloudwatch_direct': {
            'patterns': [
                r'import\s+watchtower',
                r'CloudWatchLogHandler',
                r'boto3\.client\([\'"]logs[\'"]\)',
                r'put_log_events',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 3,
            'recommendation': 'Use stdout/stderr logging; RCP captures container logs automatically'
        },
        'platform_specific_logging': {
            'patterns': [
                r'awslogs',
                r'log_driver.*awslogs',
                r'fluentd.*ecs',
            ],
            'severity': 'LOW',
            'effort_hours': 2,
            'recommendation': 'Remove platform-specific log drivers; use standard container logging'
        }
    }

    # Category: AWS SDK & Credentials
    AWS_SDK_PATTERNS = {
        'hardcoded_credentials': {
            'patterns': [
                r'aws_access_key_id\s*=',
                r'aws_secret_access_key\s*=',
                r'AWS_ACCESS_KEY',
                r'AWS_SECRET_KEY',
            ],
            'severity': 'CRITICAL',
            'effort_hours': 1,
            'recommendation': 'Remove hardcoded credentials; use IRSA (IAM Roles for Service Accounts)'
        },
        'ecs_task_role_assumptions': {
            'patterns': [
                r'ECS_TASK_ROLE',
                r'task[_-]role',
                r'get_credentials.*ecs',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 3,
            'recommendation': 'Update to use IRSA; ensure service account annotations'
        }
    }

    # Category: Container/Orchestration Specific
    ORCHESTRATION_PATTERNS = {
        'ecs_specific_apis': {
            'patterns': [
                r'boto3\.client\([\'"]ecs[\'"]\)',
                r'ecs\.describe_tasks',
                r'ecs\.list_tasks',
                r'ecs\.run_task',
            ],
            'severity': 'HIGH',
            'effort_hours': 12,
            'recommendation': 'Replace ECS API calls with Kubernetes API or remove if not needed'
        },
        'docker_compose_dependencies': {
            'patterns': [
                r'depends_on:',
                r'docker-compose',
                r'docker_compose',
            ],
            'severity': 'LOW',
            'effort_hours': 4,
            'recommendation': 'Convert to Kubernetes init containers or pod dependencies'
        }
    }

    # Category: Observability
    OBSERVABILITY_PATTERNS = {
        'platform_specific_apm': {
            'patterns': [
                r'DD_AGENT_HOST.*169\.254',
                r'statsd.*ecs',
                r'DD_ECS_COLLECT',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 3,
            'recommendation': 'Update Datadog agent configuration for Kubernetes (EG Datadog)'
        }
    }

    # Category: Signal Handling
    SIGNAL_HANDLING_PATTERNS = {
        'missing_graceful_shutdown': {
            'patterns': [
                r'signal\.SIGTERM',
                r'signal\.SIGINT',
                r'@PreDestroy',
                r'shutdown\s*hook',
                r'process\.on\([\'"]SIGTERM',
            ],
            'severity': 'MEDIUM',
            'effort_hours': 4,
            'recommendation': 'Implement graceful shutdown handling for SIGTERM',
            'inverse': True
        }
    }

    @classmethod
    def get_all_patterns(cls) -> Dict:
        """Returns all pattern categories"""
        return {
            'SERVICE_DISCOVERY': cls.SERVICE_DISCOVERY_PATTERNS,
            'SECRETS_CONFIG': cls.SECRETS_CONFIG_PATTERNS,
            'METADATA': cls.METADATA_PATTERNS,
            'HEALTH_CHECK': cls.HEALTH_CHECK_PATTERNS,
            'LOGGING': cls.LOGGING_PATTERNS,
            'AWS_SDK': cls.AWS_SDK_PATTERNS,
            'ORCHESTRATION': cls.ORCHESTRATION_PATTERNS,
            'OBSERVABILITY': cls.OBSERVABILITY_PATTERNS,
            'SIGNAL_HANDLING': cls.SIGNAL_HANDLING_PATTERNS,
        }


class CodeScanner:
    """Scans application code for platform-specific patterns"""

    SUPPORTED_EXTENSIONS = {
        '.py', '.java', '.js', '.ts', '.go', '.rb', '.php',
        '.cs', '.scala', '.kt', '.groovy', '.yaml', '.yml',
        '.json', '.properties', '.xml', '.conf', '.config'
    }

    EXCLUDE_DIRS = {
        'node_modules', 'venv', 'virtualenv', '.git', 'target',
        'build', 'dist', '__pycache__', '.terraform', 'vendor'
    }

    def __init__(self):
        self.patterns = MigrationPatternRules.get_all_patterns()

    def scan_directory(self, directory: Path) -> List[Finding]:
        """Scan all files in directory for patterns"""
        findings = []

        for file_path in self._get_files_to_scan(directory):
            findings.extend(self._scan_file(file_path))

        return findings

    def _get_files_to_scan(self, directory: Path) -> List[Path]:
        """Get list of files to scan"""
        files = []

        for root, dirs, filenames in os.walk(directory):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in self.EXCLUDE_DIRS]

            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    files.append(file_path)

        return files

    def _scan_file(self, file_path: Path) -> List[Finding]:
        """Scan a single file for patterns"""
        findings = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                content = ''.join(lines)

                for category, patterns_dict in self.patterns.items():
                    for pattern_name, pattern_config in patterns_dict.items():
                        is_inverse = pattern_config.get('inverse', False)

                        if is_inverse:
                            # Check for ABSENCE of pattern
                            has_pattern = any(
                                re.search(p, content, re.IGNORECASE)
                                for p in pattern_config['patterns']
                            )
                            if not has_pattern:
                                findings.append(Finding(
                                    category=category,
                                    severity=pattern_config['severity'],
                                    pattern=pattern_name,
                                    file_path=str(file_path),
                                    line_number=0,
                                    code_snippet='Pattern not found (expected)',
                                    recommendation=pattern_config['recommendation']
                                ))
                        else:
                            # Check for PRESENCE of pattern
                            for pattern in pattern_config['patterns']:
                                for line_num, line in enumerate(lines, 1):
                                    if re.search(pattern, line, re.IGNORECASE):
                                        findings.append(Finding(
                                            category=category,
                                            severity=pattern_config['severity'],
                                            pattern=pattern_name,
                                            file_path=str(file_path),
                                            line_number=line_num,
                                            code_snippet=line.strip()[:100],
                                            recommendation=pattern_config['recommendation']
                                        ))

        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")

        return findings


class AssessmentEngine:
    """Analyzes findings and generates assessment results"""

    SEVERITY_WEIGHTS = {
        'CRITICAL': 25,
        'HIGH': 15,
        'MEDIUM': 8,
        'LOW': 3
    }

    COMPLEXITY_LEVELS = {
        (0, 20): 'MINIMAL',
        (21, 40): 'LOW',
        (41, 60): 'MEDIUM',
        (61, 80): 'HIGH',
        (81, 100): 'CRITICAL'
    }

    def assess_application(self, app_name: str, app_path: str,
                           findings: List[Finding], source_platform: str) -> AssessmentResult:
        """Generate comprehensive assessment for an application"""

        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(findings)
        complexity_level = self._get_complexity_level(complexity_score)

        # Calculate effort
        estimated_hours = self._estimate_effort(findings)

        # Generate summary
        summary = self._generate_summary(findings)

        # Determine priority
        priority = self._determine_priority(complexity_score, source_platform, len(findings))

        return AssessmentResult(
            app_name=app_name,
            app_path=app_path,
            source_platform=source_platform,
            complexity_score=complexity_score,
            complexity_level=complexity_level,
            findings=findings,
            summary=summary,
            estimated_effort_hours=estimated_hours,
            priority=priority
        )

    def _calculate_complexity_score(self, findings: List[Finding]) -> int:
        """Calculate complexity score (0-100) based on findings"""
        score = 0

        for finding in findings:
            score += self.SEVERITY_WEIGHTS.get(finding.severity, 0)

        # Cap at 100
        return min(score, 100)

    def _get_complexity_level(self, score: int) -> str:
        """Map score to complexity level"""
        for (min_score, max_score), level in self.COMPLEXITY_LEVELS.items():
            if min_score <= score <= max_score:
                return level
        return 'UNKNOWN'

    def _estimate_effort(self, findings: List[Finding]) -> int:
        """Estimate effort in hours"""
        patterns = MigrationPatternRules.get_all_patterns()
        total_hours = 0

        # Track unique patterns to avoid double counting
        unique_patterns = set()

        for finding in findings:
            if finding.pattern not in unique_patterns:
                # Find effort for this pattern
                for category in patterns.values():
                    if finding.pattern in category:
                        total_hours += category[finding.pattern].get('effort_hours', 0)
                        unique_patterns.add(finding.pattern)
                        break

        return total_hours

    def _generate_summary(self, findings: List[Finding]) -> Dict[str, int]:
        """Generate summary statistics"""
        summary = {
            'total_findings': len(findings),
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'categories': defaultdict(int)
        }

        for finding in findings:
            summary[finding.severity.lower()] += 1
            summary['categories'][finding.category] += 1

        summary['categories'] = dict(summary['categories'])
        return summary

    def _determine_priority(self, complexity_score: int, source_platform: str,
                            findings_count: int) -> str:
        """Determine migration priority"""
        # P1: Critical complexity or ECS with high findings
        if complexity_score >= 80 or (source_platform == 'ECS' and findings_count > 15):
            return 'P1'

        # P2: High complexity or ECS with medium findings
        elif complexity_score >= 60 or (source_platform == 'ECS' and findings_count > 8):
            return 'P2'

        # P3: Medium complexity
        elif complexity_score >= 40:
            return 'P3'

        # P4: Low complexity
        else:
            return 'P4'


class ReportGenerator:
    """Generates various report formats"""

    @staticmethod
    def generate_json_report(results: List[AssessmentResult], output_file: str):
        """Generate JSON report"""
        report_data = {
            'total_applications': len(results),
            'summary': ReportGenerator._generate_overall_summary(results),
            'applications': [r.to_dict() for r in results]
        }

        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"JSON report generated: {output_file}")

    @staticmethod
    def generate_csv_summary(results: List[AssessmentResult], output_file: str):
        """Generate CSV summary"""
        import csv

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'App Name', 'Source Platform', 'Complexity Level', 'Complexity Score',
                'Total Findings', 'Critical', 'High', 'Medium', 'Low',
                'Estimated Hours', 'Priority'
            ])

            for result in results:
                writer.writerow([
                    result.app_name,
                    result.source_platform,
                    result.complexity_level,
                    result.complexity_score,
                    result.summary['total_findings'],
                    result.summary['critical'],
                    result.summary['high'],
                    result.summary['medium'],
                    result.summary['low'],
                    result.estimated_effort_hours,
                    result.priority
                ])

        logger.info(f"CSV summary generated: {output_file}")

    @staticmethod
    def generate_console_summary(results: List[AssessmentResult]):
        """Print summary to console"""
        overall = ReportGenerator._generate_overall_summary(results)

        print("\n" + "=" * 80)
        print("PLATFORM MIGRATION ASSESSMENT SUMMARY")
        print("=" * 80)
        print(f"\nTotal Applications Scanned: {len(results)}")
        print(f"\nComplexity Distribution:")
        for level, count in overall['complexity_distribution'].items():
            print(f"  {level}: {count}")

        print(f"\nPriority Distribution:")
        for priority, count in overall['priority_distribution'].items():
            print(f"  {priority}: {count}")

        print(f"\nTotal Estimated Effort: {overall['total_effort_hours']} hours")
        print(f"Average Effort per App: {overall['avg_effort_hours']:.1f} hours")

        print("\n" + "=" * 80 + "\n")

    @staticmethod
    def _generate_overall_summary(results: List[AssessmentResult]) -> Dict:
        """Generate overall summary statistics"""
        complexity_dist = defaultdict(int)
        priority_dist = defaultdict(int)
        total_effort = 0

        for result in results:
            complexity_dist[result.complexity_level] += 1
            priority_dist[result.priority] += 1
            total_effort += result.estimated_effort_hours

        return {
            'complexity_distribution': dict(complexity_dist),
            'priority_distribution': dict(priority_dist),
            'total_effort_hours': total_effort,
            'avg_effort_hours': total_effort / len(results) if results else 0
        }


def detect_platform(app_path: Path) -> str:
    """Attempt to detect source platform from application artifacts"""

    # Check for ECS task definitions
    if any(app_path.glob('**/task-definition.json')) or any(app_path.glob('**/ecs-*.json')):
        return 'ECS'

    # Check for Kubernetes manifests (could be KMC, MPaaS, etc.)
    if any(app_path.glob('**/k8s/**/*.yaml')) or any(app_path.glob('**/kubernetes/**/*.yaml')):
        # Try to detect specific platform
        k8s_files = list(app_path.glob('**/k8s/**/*.yaml')) + list(app_path.glob('**/kubernetes/**/*.yaml'))
        for k8s_file in k8s_files:
            content = k8s_file.read_text()
            if 'kmc' in content.lower():
                return 'KMC'
            elif 'mpaas' in content.lower():
                return 'MPaaS'
            elif 'hcom' in content.lower():
                return 'HCom'
        return 'Kubernetes'

    # Check for Docker Compose (might indicate older platform)
    if any(app_path.glob('**/docker-compose*.yml')):
        return 'Docker-Compose'

    return 'Unknown'


def main():
    parser = argparse.ArgumentParser(
        description='Scan applications for platform migration complexity'
    )
    parser.add_argument(
        '--repo-path',
        type=str,
        help='Path to single repository to scan'
    )
    parser.add_argument(
        '--scan-directory',
        type=str,
        help='Path to directory containing multiple applications'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='migration_assessment.json',
        help='Output file for JSON report'
    )
    parser.add_argument(
        '--csv',
        type=str,
        help='Output file for CSV summary'
    )
    parser.add_argument(
        '--platform',
        type=str,
        choices=['ECS', 'KMC', 'MPaaS1', 'MPaaS2', 'HCom', 'CPI', 'Unknown'],
        help='Source platform (auto-detected if not specified)'
    )

    args = parser.parse_args()

    scanner = CodeScanner()
    assessor = AssessmentEngine()
    results = []

    if args.repo_path:
        # Scan single repository
        repo_path = Path(args.repo_path)
        app_name = repo_path.name
        platform = args.platform or detect_platform(repo_path)

        logger.info(f"Scanning {app_name} (Platform: {platform})...")
        findings = scanner.scan_directory(repo_path)
        result = assessor.assess_application(app_name, str(repo_path), findings, platform)
        results.append(result)

    elif args.scan_directory:
        # Scan multiple applications
        scan_dir = Path(args.scan_directory)
        app_dirs = [d for d in scan_dir.iterdir() if d.is_dir()]

        logger.info(f"Found {len(app_dirs)} applications to scan...")

        for app_dir in app_dirs:
            app_name = app_dir.name
            platform = args.platform or detect_platform(app_dir)

            logger.info(f"Scanning {app_name} (Platform: {platform})...")
            findings = scanner.scan_directory(app_dir)
            result = assessor.assess_application(app_name, str(app_dir), findings, platform)
            results.append(result)

    else:
        parser.print_help()
        return

    # Generate reports
    ReportGenerator.generate_json_report(results, args.output)

    if args.csv:
        ReportGenerator.generate_csv_summary(results, args.csv)

    ReportGenerator.generate_console_summary(results)


if __name__ == '__main__':
    main()
