#!/bin/bash
# Quick setup script for Conformity Scanner Demo

set -e

echo "=================================================="
echo "Conformity Scanner Demo - Quick Setup"
echo "=================================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if requests is installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo ""
    echo "📦 Installing Python dependencies..."
    pip install requests
    echo "✓ Dependencies installed"
else
    echo "✓ Python dependencies already installed"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Conformity API key!"
    echo "   1. Open .env in a text editor"
    echo "   2. Replace 'your-api-key-here' with your actual API key"
    echo "   3. Set the correct region (us-west-2, eu-west-1, or ap-southeast-2)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Get your API key from: https://cloudone.trendmicro.com/"
echo "2. Edit .env file with your API key and region"
echo "3. Run: source .env && python3 scan.py"
echo ""
echo "For more information, see README.md"
echo ""
