# Conformity Scanner Demo

A demonstration repository showing how to integrate [Trend Micro Cloud One Conformity](https://www.trendmicro.com/en_us/business/products/hybrid-cloud/cloud-one-conformity.html) Template Scanner into a CI/CD pipeline to automatically scan CloudFormation templates for security and compliance issues before deployment.

## Overview

This project demonstrates a complete CI/CD pipeline that:
- Scans CloudFormation templates using Trend Micro Cloud One Conformity Template Scanner API
- Identifies security and compliance issues before deployment
- Fails the build if critical issues are found
- Generates detailed scan reports

## Prerequisites

1. **AWS Account** - For running the CloudFormation template (optional)
2. **Trend Micro Cloud One Account** - Sign up at [Cloud One](https://cloudone.trendmicro.com/)
3. **Conformity API Key** - Generate from your Cloud One Conformity account
4. **AWS CodeBuild** (or any CI/CD system that can run the buildspec.yml)

## Repository Structure

```
├── buildspec.yml       # AWS CodeBuild specification with Conformity scanning
├── template.yaml       # Sample CloudFormation template (intentionally has issues)
└── README.md          # This file
```

## Getting Your Conformity API Key

1. Log in to [Trend Micro Cloud One](https://cloudone.trendmicro.com/)
2. Navigate to Conformity
3. Go to **Settings** > **API Keys**
4. Click **New API Key**
5. Give it a name (e.g., "CI/CD Scanner")
6. Select appropriate permissions (Template Scanner access required)
7. Copy the API key (you won't be able to see it again)

## Setup Instructions

### Option 1: Using AWS CodeBuild

1. **Fork or clone this repository**

2. **Create a CodeBuild project:**
   - Source: Connect to your GitHub repository
   - Environment: Use the Amazon Linux 2 image
   - Buildspec: Use the `buildspec.yml` from this repository

3. **Configure environment variables in CodeBuild:**
   - `CONFORMITY_API_KEY`: Your Conformity API key (mark as secret)
   - `CONFORMITY_REGION`: Your Conformity region (e.g., `us-west-2`, `eu-west-1`, `ap-southeast-2`)

4. **Run the build**

### Option 2: Running Locally

1. **Install prerequisites:**
   ```bash
   python3 --version  # Requires Python 3.9 or later
   pip install requests
   ```

2. **Set environment variables:**
   ```bash
   export CONFORMITY_API_KEY="your-api-key-here"
   export CONFORMITY_REGION="us-west-2"  # or your region
   ```

3. **Run the scanner:**
   ```bash
   python3 << 'EOF'
   import requests
   import json
   import os
   
   API_KEY = os.environ['CONFORMITY_API_KEY']
   REGION = os.environ['CONFORMITY_REGION']
   
   headers = {
       'Authorization': f'ApiKey {API_KEY}',
       'Content-Type': 'application/vnd.api+json'
   }
   
   with open('template.yaml', 'r') as f:
       template_content = f.read()
   
   scan_data = {
       'data': {
           'type': 'template-scanner',
           'attributes': {
               'type': 'cloudformation-template',
               'contents': template_content
           }
       }
   }
   
   response = requests.post(
       f'https://{REGION}-api.cloudconformity.com/v1/template-scanner/scan',
       headers=headers,
       json=scan_data
   )
   
   if response.status_code == 200:
       results = response.json()
       with open('scan-results.json', 'w') as f:
           json.dump(results, f, indent=2)
       
       failures = [item for item in results.get('data', []) if item.get('attributes', {}).get('status') == 'FAILURE']
       
       if failures:
           print(f"Template scan found {len(failures)} issues:")
           for failure in failures:
               attrs = failure.get('attributes', {})
               print(f"- {attrs.get('rule-title', 'Unknown')}: {attrs.get('message', 'No message')}")
       else:
           print("Template scan passed successfully!")
   else:
       print(f"Scan failed with status {response.status_code}")
       print(response.text)
   EOF
   ```

## About the Sample Template

The `template.yaml` file contains a CloudFormation template with **intentional security issues** for demonstration purposes:

- ❌ S3 bucket without encryption
- ❌ EC2 instance without security group
- ❌ Missing monitoring configurations
- ✅ Free tier resources only (to avoid costs)
- ✅ Auto-cleanup after 7 days

## Expected Scanner Results

When you run the scanner, it should detect issues like:
- S3 bucket encryption not enabled
- EC2 instance missing security group configuration
- Missing logging/monitoring configurations
- Other security and compliance violations

## Conformity Regions

Available regions for the Conformity API:
- `us-west-2` - US West (Oregon)
- `eu-west-1` - Europe (Ireland)
- `ap-southeast-2` - Asia Pacific (Sydney)

Make sure to use the region where your Conformity account is located.

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Conformity Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Run Conformity Scanner
        env:
          CONFORMITY_API_KEY: ${{ secrets.CONFORMITY_API_KEY }}
          CONFORMITY_REGION: us-west-2
        run: |
          # Run the scanner script from buildspec.yml
```

## Troubleshooting

### Authentication Errors
- Verify your API key is correct
- Check that the API key has Template Scanner permissions
- Ensure you're using the correct region

### Connection Errors
- Verify you're using the correct region endpoint
- Check your network allows HTTPS connections to cloudconformity.com

### Template Validation Errors
- Ensure your CloudFormation template is valid YAML
- Check that the template follows CloudFormation syntax

## Security Best Practices

1. **Never commit API keys to version control**
2. Store API keys in CI/CD secrets or environment variables
3. Use least-privilege access for API keys
4. Rotate API keys regularly
5. Enable CloudFormation drift detection in production

## Learn More

- [Cloud One Conformity Documentation](https://cloudone.trendmicro.com/docs/conformity/)
- [Template Scanner API Reference](https://cloudone.trendmicro.com/docs/conformity/api-reference/)
- [AWS CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

## License

This is a demonstration project. Use at your own risk.

## Contributing

This is a demo repository. Feel free to fork and modify for your own use.
