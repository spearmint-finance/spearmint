#!/bin/bash
# restart-docker.sh
# Script to update and restart the local Docker Compose cluster

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse arguments
BUILD=false
CLEAN=false
LOGS=false
HELP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --build|-b)
            BUILD=true
            shift
            ;;
        --clean|-c)
            CLEAN=true
            shift
            ;;
        --logs|-l)
            LOGS=true
            shift
            ;;
        --help|-h)
            HELP=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            HELP=true
            shift
            ;;
    esac
done

function show_help {
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    echo -e "${CYAN}  Spearmint Docker Compose - Update & Restart Script${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  ./scripts/restart-docker.sh [OPTIONS]"
    echo ""
    echo -e "${YELLOW}OPTIONS:${NC}"
    echo "  -b, --build      Force rebuild of all Docker images"
    echo "  -c, --clean      Remove volumes and perform clean start (WARNING: deletes data)"
    echo "  -l, --logs       Show logs after starting services"
    echo "  -h, --help       Show this help message"
    echo ""
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo "  ./scripts/restart-docker.sh                # Quick restart"
    echo "  ./scripts/restart-docker.sh --build        # Rebuild and restart"
    echo "  ./scripts/restart-docker.sh --clean        # Clean restart (deletes data)"
    echo "  ./scripts/restart-docker.sh --build --logs # Rebuild and show logs"
    echo ""
    echo -e "${YELLOW}SERVICES:${NC}"
    echo "  - gateway    (API Gateway)      http://localhost:8080"
    echo "  - core-api   (Backend API)      http://localhost:8000"
    echo "  - web-app    (Frontend)         http://localhost:80"
    echo "  - db         (PostgreSQL)       localhost:5432"
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    exit 0
}

if [ "$HELP" = true ]; then
    show_help
fi

echo ""
echo -e "${CYAN}================================================================================${NC}"
echo -e "${CYAN}  Spearmint Docker Compose - Update & Restart${NC}"
echo -e "${CYAN}================================================================================${NC}"
echo ""

# Check if docker compose is available
echo -e "${YELLOW}Checking Docker Compose...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ ERROR: Docker is not installed or not in PATH${NC}"
    echo -e "${YELLOW}  Please install Docker: https://www.docker.com/products/docker-desktop${NC}"
    exit 1
fi

DOCKER_COMPOSE_VERSION=$(docker compose version 2>&1)
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ ERROR: Docker Compose is not available${NC}"
    echo -e "${YELLOW}  Please install Docker Compose${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found: $DOCKER_COMPOSE_VERSION${NC}"
echo ""

# Step 1: Stop running containers
echo -e "${YELLOW}Step 1: Stopping running containers...${NC}"
docker compose down
echo -e "${GREEN}✓ Containers stopped${NC}"
echo ""

# Step 2: Clean volumes if requested
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}Step 2: Removing volumes (CLEAN MODE)...${NC}"
    echo -e "${RED}  WARNING: This will delete all database data!${NC}"
    read -p "  Are you sure? (yes/no): " confirmation
    if [ "$confirmation" = "yes" ]; then
        docker compose down -v
        echo -e "${GREEN}✓ Volumes removed${NC}"
    else
        echo -e "${YELLOW}  Skipping volume removal${NC}"
    fi
    echo ""
fi

# Step 3: Pull latest images (if not building)
if [ "$BUILD" = false ]; then
    echo -e "${YELLOW}Step 3: Pulling latest images...${NC}"
    docker compose pull || echo -e "${YELLOW}⚠ Warning: Failed to pull some images (may not exist in registry)${NC}"
    echo -e "${GREEN}✓ Images pulled${NC}"
    echo ""
fi

# Step 4: Build images if requested
if [ "$BUILD" = true ]; then
    echo -e "${YELLOW}Step 3: Building Docker images...${NC}"
    docker compose build --no-cache
    echo -e "${GREEN}✓ Images built${NC}"
    echo ""
fi

# Step 5: Start services
echo -e "${YELLOW}Step 4: Starting services...${NC}"
docker compose up -d
echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Step 6: Show status
echo -e "${YELLOW}Step 5: Checking service status...${NC}"
docker compose ps
echo ""

# Step 7: Show access URLs
echo -e "${CYAN}================================================================================${NC}"
echo -e "${GREEN}  Services are now running!${NC}"
echo -e "${CYAN}================================================================================${NC}"
echo ""
echo -e "${YELLOW}Access your services at:${NC}"
echo "  - API Gateway:     http://localhost:8080"
echo "  - API Docs:        http://localhost:8080/api/docs"
echo "  - Frontend:        http://localhost:80"
echo "  - Core API:        http://localhost:8000"
echo "  - PostgreSQL:      localhost:5432"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  - View logs:       docker compose logs -f"
echo "  - Stop services:   docker compose down"
echo "  - Restart service: docker compose restart <service-name>"
echo ""
echo -e "${CYAN}================================================================================${NC}"
echo ""

# Step 8: Show logs if requested
if [ "$LOGS" = true ]; then
    echo -e "${YELLOW}Showing logs (press Ctrl+C to exit)...${NC}"
    echo ""
    docker compose logs -f
fi

