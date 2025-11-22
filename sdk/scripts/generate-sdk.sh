#!/bin/bash
# generate-sdk.sh
# Generates the SDK locally using LibLab (matches CI/CD workflow process)

set -e

SKIP_SPEC=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-spec)
            SKIP_SPEC=true
            shift
            ;;
        --help)
            echo ""
            echo "SDK Generation Script"
            echo "====================="
            echo ""
            echo "Generates the TypeScript and Python SDKs using LibLab."
            echo ""
            echo "USAGE:"
            echo "  ./sdk/scripts/generate-sdk.sh [OPTIONS]"
            echo ""
            echo "OPTIONS:"
            echo "  --skip-spec    Skip OpenAPI spec generation (use existing sdk/openapi.json)"
            echo "  --help         Show this help message"
            echo ""
            echo "EXAMPLES:"
            echo "  ./sdk/scripts/generate-sdk.sh              # Generate spec + SDK"
            echo "  ./sdk/scripts/generate-sdk.sh --skip-spec  # Only generate SDK"
            echo ""
            echo "REQUIREMENTS:"
            echo "  - LibLab CLI installed: npm install -g liblab"
            echo "  - LIBLAB_TOKEN environment variable set"
            echo "  - Python virtual environment activated (if generating spec)"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo ""
echo "========================================"
echo "  Spearmint SDK Generation"
echo "========================================"
echo ""

# Check LibLab CLI
echo "Checking LibLab CLI..."
if ! command -v liblab &> /dev/null; then
    echo "[ERROR] LibLab CLI not found"
    echo "Install with: npm install -g liblab"
    exit 1
fi
LIBLAB_VERSION=$(liblab --version)
echo "[OK] LibLab CLI found: $LIBLAB_VERSION"

# Check LIBLAB_TOKEN
echo "Checking LIBLAB_TOKEN..."
if [ -z "$LIBLAB_TOKEN" ]; then
    echo "[ERROR] LIBLAB_TOKEN environment variable not set"
    echo "Set it with: export LIBLAB_TOKEN='your-token'"
    exit 1
fi
echo "[OK] LIBLAB_TOKEN is set"
echo ""

# Step 1: Generate OpenAPI Spec (unless skipped)
if [ "$SKIP_SPEC" = false ]; then
    echo "Step 1: Generating OpenAPI Spec..."
    echo "-----------------------------------"
    
    # Check if we're in a virtual environment
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "[WARNING] Python virtual environment not detected"
        echo "Attempting to activate .venv..."
        
        if [ -f ".venv/bin/activate" ]; then
            source .venv/bin/activate
        else
            echo "[ERROR] Virtual environment not found at .venv"
            echo "Please activate your virtual environment first"
            exit 1
        fi
    fi
    
    # Navigate to core-api and generate spec
    cd core-api
    
    echo "Installing dependencies..."
    pip install -r requirements.txt -q
    pip install -e . -q
    
    echo "Generating OpenAPI spec..."
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    python scripts/generate_openapi.py ../sdk/openapi.json
    
    echo "[OK] OpenAPI spec generated successfully"
    cd ..
    echo ""
else
    echo "Step 1: Skipping OpenAPI spec generation (using existing)"
    echo ""
fi

# Step 2: Build SDK with LibLab
echo "Step 2: Building SDK with LibLab..."
echo "------------------------------------"

cd sdk

# Ensure config points to local openapi.json
echo "Updating liblab.config.json..."
sed -i 's|"specFilePath": ".*"|"specFilePath": "./openapi.json"|' liblab.config.json

echo "Running liblab build..."
liblab build

echo "[OK] SDK built successfully"
cd ..

echo ""
echo "========================================"
echo "  SDK Generation Complete!"
echo "========================================"
echo ""
echo "Output locations:"
echo "  - TypeScript SDK: sdk/output/typescript/"
echo "  - Python SDK:     sdk/output/python/"
echo ""

