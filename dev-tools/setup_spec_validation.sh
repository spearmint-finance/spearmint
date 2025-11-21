#!/bin/bash
# Setup script for OpenAPI spec validation with Postman
# This script installs and configures the Postman CLI for spec validation

set -e

echo "=========================================="
echo "OpenAPI Spec Validation Setup"
echo "=========================================="
echo ""

# Check if Postman CLI is installed
if command -v postman &> /dev/null; then
    echo "✓ Postman CLI is already installed"
    postman --version
else
    echo "Installing Postman CLI..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl -o- "https://dl-cli.pstmn.io/install/osx_64.sh" | sh
    else
        echo "❌ Unsupported OS: $OSTYPE"
        echo "Please install Postman CLI manually:"
        echo "https://learning.postman.com/docs/postman-cli/postman-cli-installation/"
        exit 1
    fi
    
    echo "✓ Postman CLI installed successfully"
fi

echo ""

# Check if user is logged in
echo "Checking Postman authentication..."
if postman login --help &> /dev/null; then
    echo "✓ Postman CLI is ready"
else
    echo "❌ Postman CLI not found in PATH"
    echo "Please restart your terminal or add Postman CLI to your PATH"
    exit 1
fi

echo ""

# Prompt for API key if not logged in
echo "To validate specs, you need to login to Postman."
echo ""
read -p "Do you have a Postman API key? (y/n): " has_key

if [[ "$has_key" == "y" || "$has_key" == "Y" ]]; then
    read -sp "Enter your Postman API key: " api_key
    echo ""
    
    if [ -n "$api_key" ]; then
        echo "Logging in to Postman..."
        postman login --with-api-key "$api_key"
        echo "✓ Successfully logged in to Postman"
    else
        echo "❌ No API key provided"
        exit 1
    fi
else
    echo ""
    echo "To get a Postman API key:"
    echo "1. Go to https://postman.co/settings/me/api-keys"
    echo "2. Click 'Generate API Key'"
    echo "3. Copy the key and run this script again"
    echo ""
    echo "Or login manually with:"
    echo "  postman login --with-api-key YOUR_API_KEY"
    exit 0
fi

echo ""

# Prompt for workspace ID
echo "To apply workspace-specific governance rules, you need a workspace ID."
echo ""
read -p "Do you want to set a workspace ID? (y/n): " set_workspace

if [[ "$set_workspace" == "y" || "$set_workspace" == "Y" ]]; then
    read -p "Enter your Postman workspace ID: " workspace_id
    
    if [ -n "$workspace_id" ]; then
        # Add to .env file or shell profile
        if [ -f ".env" ]; then
            echo "POSTMAN_WORKSPACE_ID=$workspace_id" >> .env
            echo "✓ Added POSTMAN_WORKSPACE_ID to .env file"
        else
            echo "export POSTMAN_WORKSPACE_ID=$workspace_id" >> ~/.bashrc
            echo "✓ Added POSTMAN_WORKSPACE_ID to ~/.bashrc"
            echo "  Run 'source ~/.bashrc' to apply"
        fi
    fi
else
    echo "Skipping workspace ID setup"
    echo "Validation will use 'All workspaces' governance rules"
fi

echo ""

# Install pre-commit if not installed
if command -v pre-commit &> /dev/null; then
    echo "✓ pre-commit is already installed"
else
    echo "Installing pre-commit..."
    pip install pre-commit
    echo "✓ pre-commit installed successfully"
fi

echo ""

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test the validation:"
echo "   python dev-tools/validate_spec.py --spec-file sdk/openapi.json"
echo ""
echo "2. Run pre-commit hooks manually:"
echo "   pre-commit run --all-files"
echo ""
echo "3. Commit changes to trigger automatic validation:"
echo "   git add ."
echo "   git commit -m 'Your commit message'"
echo ""
echo "For more information, see:"
echo "  dev-tools/docs/SPEC_VALIDATION.md"
echo ""

