#!/bin/bash
# setup-local-dev.sh
# One-command setup for local development with SDK hot reload

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Flags
SKIP_BACKEND=false
SKIP_FRONTEND=false
SKIP_SDK=false
SKIP_ENV=false
START_SERVERS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-backend)
            SKIP_BACKEND=true
            shift
            ;;
        --skip-frontend)
            SKIP_FRONTEND=true
            shift
            ;;
        --skip-sdk)
            SKIP_SDK=true
            shift
            ;;
        --skip-env)
            SKIP_ENV=true
            shift
            ;;
        --start-servers)
            START_SERVERS=true
            shift
            ;;
        --help|-h)
            echo ""
            echo -e "${CYAN}Local Development Setup Script${NC}"
            echo -e "${CYAN}==============================${NC}"
            echo ""
            echo -e "${YELLOW}Sets up complete local development environment with SDK hot reload.${NC}"
            echo ""
            echo -e "${YELLOW}USAGE:${NC}"
            echo "  ./scripts/setup-local-dev.sh [OPTIONS]"
            echo ""
            echo -e "${YELLOW}OPTIONS:${NC}"
            echo "  --skip-backend    Skip backend setup (Python venv, dependencies, DB)"
            echo "  --skip-frontend   Skip frontend setup (npm install)"
            echo "  --skip-sdk        Skip SDK generation and linking"
            echo "  --skip-env        Skip environment configuration (.env file)"
            echo "  --start-servers   Automatically start backend and frontend servers after setup"
            echo "  --help, -h        Show this help message"
            echo ""
            echo -e "${YELLOW}EXAMPLES:${NC}"
            echo "  ./scripts/setup-local-dev.sh                    # Full setup"
            echo "  ./scripts/setup-local-dev.sh --start-servers    # Full setup + start servers"
            echo "  ./scripts/setup-local-dev.sh --skip-backend     # Skip backend setup"
            echo "  ./scripts/setup-local-dev.sh --skip-sdk         # Skip SDK generation"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run with --help for usage information"
            exit 1
            ;;
    esac
done

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Spearmint Local Development Setup${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Detect repository root and navigate to it if needed
CURRENT_DIR=$(pwd)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if we're in the scripts directory
if [[ "$CURRENT_DIR" == */scripts ]]; then
    echo -e "${YELLOW}Detected script running from scripts directory, navigating to repository root...${NC}"
    cd ..
fi

# Verify we're in the repository root by checking for key directories
if [ ! -d "core-api" ] || [ ! -d "web-app" ] || [ ! -d "sdk" ]; then
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  ERROR: Not in repository root!${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}This script must be run from the repository root directory.${NC}"
    echo ""
    echo -e "${GRAY}Current directory: $CURRENT_DIR${NC}"
    echo ""
    echo -e "${YELLOW}Please run:${NC}"
    echo -e "${CYAN}  cd /path/to/spearmint${NC}"
    echo -e "${CYAN}  ./scripts/setup-local-dev.sh${NC}"
    echo ""
    exit 1
fi

# Track what was done for final summary
SETUP_STEPS=()

# ============================================
# Step 1: Backend Setup
# ============================================
if [ "$SKIP_BACKEND" = false ]; then
    echo -e "${YELLOW}[1/4] Setting up Backend...${NC}"
    echo ""
    
    # Check Python
    echo -e "${GRAY}  Checking Python installation...${NC}"
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        echo -e "${GREEN}  [OK] $PYTHON_VERSION${NC}"
    else
        echo -e "${RED}  [ERROR] Python not found. Please install Python 3.10+${NC}"
        exit 1
    fi
    
    # Create virtual environment
    if [ ! -d ".venv" ]; then
        echo -e "${GRAY}  Creating virtual environment...${NC}"
        python3 -m venv .venv
        echo -e "${GREEN}  [OK] Virtual environment created${NC}"
    else
        echo -e "${GREEN}  [OK] Virtual environment already exists${NC}"
    fi
    
    # Activate virtual environment
    echo -e "${GRAY}  Activating virtual environment...${NC}"
    source .venv/bin/activate
    echo -e "${GREEN}  [OK] Virtual environment activated${NC}"
    
    # Install backend dependencies
    echo -e "${GRAY}  Installing backend dependencies...${NC}"
    cd core-api
    pip install -r requirements.txt -q
    echo -e "${GREEN}  [OK] Backend dependencies installed${NC}"
    cd ..
    
    # Initialize database
    echo -e "${GRAY}  Initializing database...${NC}"
    cd core-api
    python -m src.financial_analysis.database.init_db
    echo -e "${GREEN}  [OK] Database initialized${NC}"
    cd ..
    
    SETUP_STEPS+=("✅ Backend setup complete (Python venv, dependencies, database)")
    echo ""
else
    echo -e "${GRAY}[1/4] Skipping Backend Setup${NC}"
    echo ""
fi

# ============================================
# Step 2: Frontend Setup
# ============================================
if [ "$SKIP_FRONTEND" = false ]; then
    echo -e "${YELLOW}[2/4] Setting up Frontend...${NC}"
    echo ""
    
    # Check Node.js
    echo -e "${GRAY}  Checking Node.js installation...${NC}"
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}  [OK] Node.js $NODE_VERSION${NC}"
    else
        echo -e "${RED}  [ERROR] Node.js not found. Please install Node.js 18+${NC}"
        exit 1
    fi
    
    # Install frontend dependencies
    echo -e "${GRAY}  Installing frontend dependencies...${NC}"
    cd web-app
    npm install
    echo -e "${GREEN}  [OK] Frontend dependencies installed${NC}"
    cd ..
    
    SETUP_STEPS+=("✅ Frontend setup complete (npm dependencies)")
    echo ""
else
    echo -e "${GRAY}[2/4] Skipping Frontend Setup${NC}"
    echo ""
fi

# ============================================
# Step 3: SDK Setup
# ============================================
if [ "$SKIP_SDK" = false ]; then
    echo -e "${YELLOW}[3/4] Setting up SDK...${NC}"
    echo ""

    # Check LibLab
    echo -e "${GRAY}  Checking LibLab installation...${NC}"
    if command -v liblab &> /dev/null; then
        echo -e "${GREEN}  [OK] LibLab installed${NC}"
    else
        echo -e "${YELLOW}  [WARNING] LibLab not found. Installing globally...${NC}"
        npm install -g liblab
        echo -e "${GREEN}  [OK] LibLab installed${NC}"
    fi

    # Check for LibLab token
    echo -e "${GRAY}  Checking LibLab token...${NC}"
    if [ ! -f "sdk/.env" ]; then
        echo -e "${YELLOW}  [WARNING] sdk/.env not found${NC}"
        echo ""
        echo -e "${YELLOW}  LibLab token is required for SDK generation.${NC}"
        echo -e "${YELLOW}  Please create sdk/.env with your LibLab token:${NC}"
        echo ""
        echo "  1. Copy the example file:"
        echo -e "${GRAY}     cp sdk/.env.example sdk/.env${NC}"
        echo ""
        echo "  2. Edit sdk/.env and add your token:"
        echo -e "${GRAY}     LIBLAB_TOKEN=your-token-here${NC}"
        echo ""
        echo "  3. Get your token from: https://developers.liblab.com/"
        echo ""
        echo -e "${YELLOW}  Then run this script again.${NC}"
        echo ""
        exit 1
    fi
    echo -e "${GREEN}  [OK] LibLab token configured${NC}"

    # Generate SDK
    echo -e "${GRAY}  Generating SDK from OpenAPI spec...${NC}"
    ./sdk/scripts/generate-sdk.sh
    echo -e "${GREEN}  [OK] SDK generated${NC}"

    # Install SDK dependencies
    echo -e "${GRAY}  Installing SDK dependencies...${NC}"
    cd sdk/output/typescript
    npm install
    echo -e "${GREEN}  [OK] SDK dependencies installed${NC}"

    # Create global npm link
    echo -e "${GRAY}  Creating global npm link...${NC}"
    npm link
    echo -e "${GREEN}  [OK] Global npm link created${NC}"
    cd ../../..

    # Link SDK to web-app
    echo -e "${GRAY}  Linking SDK to web-app...${NC}"
    cd web-app
    npm link @spearmint-finance/sdk
    echo -e "${GREEN}  [OK] SDK linked to web-app${NC}"
    cd ..

    # Verify link
    echo -e "${GRAY}  Verifying SDK link...${NC}"
    cd web-app
    if npm ls @spearmint-finance/sdk 2>&1 | grep -q "-> ./../sdk/output/typescript"; then
        echo -e "${GREEN}  [OK] SDK link verified${NC}"
    else
        echo -e "${YELLOW}  [WARNING] SDK link verification failed${NC}"
    fi
    cd ..

    SETUP_STEPS+=("✅ SDK setup complete (generated, linked to web-app)")
    echo ""
else
    echo -e "${GRAY}[3/4] Skipping SDK Setup${NC}"
    echo ""
fi

# ============================================
# Step 4: Environment Configuration
# ============================================
if [ "$SKIP_ENV" = false ]; then
    echo -e "${YELLOW}[4/4] Configuring Environment...${NC}"
    echo ""

    # Create .env file if it doesn't exist
    if [ ! -f "web-app/.env" ]; then
        echo -e "${GRAY}  Creating .env file from template...${NC}"
        cp web-app/.env.example web-app/.env
        echo -e "${GREEN}  [OK] .env file created${NC}"

        # Configure for Vite Proxy (recommended)
        echo -e "${GRAY}  Configuring for Vite Proxy (recommended)...${NC}"
        # Comment out VITE_API_URL to use Vite proxy
        sed -i 's/^VITE_API_URL=/# VITE_API_URL=/' web-app/.env
        echo -e "${GREEN}  [OK] Configured for Vite Proxy (VITE_API_URL unset)${NC}"

        SETUP_STEPS+=("✅ Environment configured (Vite Proxy mode)")
    else
        echo -e "${GREEN}  [OK] .env file already exists${NC}"
        SETUP_STEPS+=("✅ Environment already configured")
    fi

    echo ""
else
    echo -e "${GRAY}[4/4] Skipping Environment Configuration${NC}"
    echo ""
fi

# ============================================
# Setup Complete!
# ============================================
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Show summary
echo -e "${CYAN}Summary:${NC}"
for step in "${SETUP_STEPS[@]}"; do
    echo "  $step"
done
echo ""

# Start servers if requested
if [ "$START_SERVERS" = true ]; then
    echo ""
    echo -e "${CYAN}Starting Development Servers...${NC}"
    echo ""

    # Detect OS for terminal command
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo -e "${YELLOW}  Starting backend API server...${NC}"
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && ./start_api.sh"'
        echo -e "${GREEN}  [OK] Backend started in new terminal${NC}"

        sleep 2

        echo -e "${YELLOW}  Starting frontend dev server...${NC}"
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)/web-app"' && npm run dev"'
        echo -e "${GREEN}  [OK] Frontend started in new terminal${NC}"
    else
        # Linux
        echo -e "${YELLOW}  Starting backend API server...${NC}"
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd) && ./start_api.sh; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd $(pwd) && ./start_api.sh; bash" &
        else
            echo -e "${YELLOW}  [WARNING] Could not detect terminal emulator${NC}"
            echo -e "${YELLOW}  Please start backend manually: ./start_api.sh${NC}"
        fi
        echo -e "${GREEN}  [OK] Backend started in new terminal${NC}"

        sleep 2

        echo -e "${YELLOW}  Starting frontend dev server...${NC}"
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd)/web-app && npm run dev; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd $(pwd)/web-app && npm run dev; bash" &
        else
            echo -e "${YELLOW}  [WARNING] Could not detect terminal emulator${NC}"
            echo -e "${YELLOW}  Please start frontend manually: cd web-app && npm run dev${NC}"
        fi
        echo -e "${GREEN}  [OK] Frontend started in new terminal${NC}"
    fi

    echo ""
    echo -e "${CYAN}Servers are starting up...${NC}"
    echo "  Backend:  http://localhost:8000/api/docs"
    echo "  Frontend: http://localhost:5173"
    echo ""
    echo -e "${GRAY}Note: It may take a few seconds for servers to be ready.${NC}"
    echo -e "${GRAY}      Check the new terminal windows for server status.${NC}"
    echo ""
else
    # Show next steps
    echo -e "${CYAN}Next Steps:${NC}"
    echo ""
    echo -e "${YELLOW}  1. Start Backend (Terminal 1):${NC}"
    echo "     ./start_api.sh"
    echo ""
    echo -e "${YELLOW}  2. Start Frontend (Terminal 2):${NC}"
    echo "     cd web-app"
    echo "     npm run dev"
    echo ""
    echo -e "${YELLOW}  3. Access the application:${NC}"
    echo "     Frontend:  http://localhost:5173"
    echo "     API Docs:  http://localhost:8000/api/docs"
    echo ""
    echo -e "${YELLOW}  4. After API changes, regenerate SDK:${NC}"
    echo "     ./sdk/scripts/generate-sdk.sh"
    echo -e "${GRAY}     (Frontend will auto-reload!)${NC}"
    echo ""
    echo -e "${CYAN}TIP: Run with --start-servers flag to automatically start both servers:${NC}"
    echo "     ./scripts/setup-local-dev.sh --start-servers"
    echo ""
fi

echo -e "${CYAN}Documentation:${NC}"
echo "  - Complete Guide: dev-tools/docs/LOCAL_DEVELOPMENT_GUIDE.md"
echo "  - Quick Start:    docs/LOCAL_DEVELOPMENT_QUICKSTART.md"
echo "  - SDK Guide:      docs/LOCAL_SDK_DEVELOPMENT.md"
echo ""

