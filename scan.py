#!/usr/bin/env python3
"""
Conformity Template Scanner
Scans CloudFormation templates using Trend Micro Cloud One Conformity API
"""

import requests
import json
import os
import sys
from typing import Dict, List, Any


def load_template(template_path: str) -> str:
    """Load CloudFormation template from file."""
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading template file '{template_path}'")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)


def scan_template(api_key: str, region: str, template_content: str) -> Dict[str, Any]:
    """Submit template to Conformity scanner."""
    headers = {
        'Authorization': f'ApiKey {api_key}',
        'Content-Type': 'application/vnd.api+json'
    }
    
    scan_data = {
        'data': {
            'type': 'template-scanner',
            'attributes': {
                'type': 'cloudformation-template',
                'contents': template_content
            }
        }
    }
    
    url = f'https://{region}-api.cloudconformity.com/v1/template-scanner/scan'
    
    try:
        response = requests.post(url, headers=headers, json=scan_data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Conformity API: {e}")
        sys.exit(1)


def save_results(results: Dict[str, Any], output_path: str) -> None:
    """Save scan results to JSON file."""
    try:
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to: {output_path}")
    except Exception as e:
        print(f"Warning: Could not save results to file: {e}")


def print_results(results: Dict[str, Any]) -> int:
    """Print scan results and return exit code."""
    data = results.get('data', [])
    
    if not data:
        print("\n✓ No issues found - template is compliant!")
        return 0
    
    # Categorize findings by severity
    critical = []
    high = []
    medium = []
    low = []
    success = []
    
    for item in data:
        attrs = item.get('attributes', {})
        status = attrs.get('status', '')
        risk_level = attrs.get('risk-level', 'MEDIUM').upper()
        
        finding = {
            'title': attrs.get('rule-title', 'Unknown'),
            'message': attrs.get('message', 'No message'),
            'resource': attrs.get('resource', 'N/A'),
            'risk': risk_level
        }
        
        if status == 'SUCCESS':
            success.append(finding)
        elif status == 'FAILURE':
            if risk_level == 'CRITICAL':
                critical.append(finding)
            elif risk_level == 'HIGH':
                high.append(finding)
            elif risk_level == 'MEDIUM':
                medium.append(finding)
            else:
                low.append(finding)
    
    # Print summary
    total_failures = len(critical) + len(high) + len(medium) + len(low)
    print(f"\n{'='*70}")
    print(f"CONFORMITY SCAN RESULTS")
    print(f"{'='*70}")
    print(f"Total Checks: {len(data)}")
    print(f"✓ Passed: {len(success)}")
    print(f"✗ Failed: {total_failures}")
    print(f"  - Critical: {len(critical)}")
    print(f"  - High: {len(high)}")
    print(f"  - Medium: {len(medium)}")
    print(f"  - Low: {len(low)}")
    print(f"{'='*70}\n")
    
    # Print failures by severity
    def print_findings(findings: List[Dict], severity: str, icon: str):
        if findings:
            print(f"\n{icon} {severity} Severity Issues ({len(findings)}):")
            print("-" * 70)
            for i, finding in enumerate(findings, 1):
                print(f"{i}. {finding['title']}")
                print(f"   Resource: {finding['resource']}")
                print(f"   Message: {finding['message']}")
                print()
    
    print_findings(critical, "CRITICAL", "🔴")
    print_findings(high, "HIGH", "🟠")
    print_findings(medium, "MEDIUM", "🟡")
    print_findings(low, "LOW", "🔵")
    
    # Return exit code (non-zero if there are failures)
    return 1 if total_failures > 0 else 0


def main():
    """Main function."""
    # Get configuration from environment
    api_key = os.environ.get('CONFORMITY_API_KEY')
    region = os.environ.get('CONFORMITY_REGION', 'us-west-2')
    template_path = sys.argv[1] if len(sys.argv) > 1 else 'template.yaml'
    output_path = 'scan-results.json'
    
    # Validate configuration
    if not api_key:
        print("Error: CONFORMITY_API_KEY environment variable not set")
        print("\nUsage:")
        print("  export CONFORMITY_API_KEY='your-api-key'")
        print("  export CONFORMITY_REGION='us-west-2'  # optional")
        print(f"  python3 {sys.argv[0]} [template.yaml]")
        sys.exit(1)
    
    print(f"Scanning CloudFormation template: {template_path}")
    print(f"Using Conformity region: {region}")
    print("-" * 70)
    
    # Load and scan template
    template_content = load_template(template_path)
    results = scan_template(api_key, region, template_content)
    
    # Save and display results
    save_results(results, output_path)
    exit_code = print_results(results)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
