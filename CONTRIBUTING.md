# Contributing to Conformity Scanner Demo

Thank you for your interest in contributing to this project!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your changes
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.9 or later
- Git
- Trend Micro Cloud One Conformity account (for testing)

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/conformity-scanner-demo.git
cd conformity-scanner-demo

# Install Python dependencies
pip install requests

# Copy the example environment file
cp .env.example .env

# Edit .env with your Conformity API key
# NEVER commit your actual .env file!
```

## Testing Your Changes

### Test the scanner script

```bash
# Set your environment variables
export CONFORMITY_API_KEY="your-key-here"
export CONFORMITY_REGION="us-west-2"

# Run the scanner
python scan.py template.yaml
```

### Test with the buildspec

If you have AWS CodeBuild configured, push your changes to test the full CI/CD flow.

## Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add details in the body if needed

Examples:
```
Add support for Terraform templates
Fix API error handling for timeout scenarios
Update documentation with new regions
```

## Pull Request Process

1. Update the README.md if you add new features
2. Ensure your code follows the existing style
3. Test your changes thoroughly
4. Update documentation as needed
5. Create a pull request with a clear description

## What to Contribute

Ideas for contributions:
- Support for additional template types (Terraform, ARM templates, etc.)
- Better error handling and reporting
- Additional CI/CD platform examples
- Improved documentation
- Bug fixes
- Performance improvements

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Check existing issues for similar questions
- Review the README.md for usage information

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow GitHub's Community Guidelines

Thank you for contributing! 🎉
