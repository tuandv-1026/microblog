#!/bin/bash
# Quick start script for Microblog application

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Microblog - Quick Start Setup        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker is running"

# Create .env files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}→${NC} Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓${NC} Created backend/.env"
fi

if [ ! -f "frontend/.env" ]; then
    echo -e "${YELLOW}→${NC} Creating frontend/.env from template..."
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓${NC} Created frontend/.env"
fi

# Start Docker services
echo ""
echo -e "${YELLOW}→${NC} Starting Docker containers..."
docker-compose up -d

# Wait for MySQL to be ready
echo -e "${YELLOW}→${NC} Waiting for MySQL to be ready..."
sleep 10

# Install backend dependencies
echo -e "${YELLOW}→${NC} Installing backend dependencies..."
docker-compose exec -T backend pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Backend dependencies installed"

# Run database migrations
echo -e "${YELLOW}→${NC} Running database migrations..."
docker-compose exec -T backend alembic upgrade head || {
    echo -e "${YELLOW}→${NC} Creating initial migration..."
    docker-compose exec -T backend alembic revision --autogenerate -m "Initial migration"
    docker-compose exec -T backend alembic upgrade head
}
echo -e "${GREEN}✓${NC} Database migrations complete"

# Seed database
echo -e "${YELLOW}→${NC} Seeding database with sample data..."
docker-compose exec -T backend python scripts/seed_data.py
echo -e "${GREEN}✓${NC} Database seeded"

# Install frontend dependencies
echo -e "${YELLOW}→${NC} Installing frontend dependencies..."
docker-compose exec -T frontend npm install --silent
echo -e "${GREEN}✓${NC} Frontend dependencies installed"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Setup Complete!                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "Your microblog is now running!"
echo ""
echo -e "  Frontend:  ${BLUE}http://localhost:3000${NC}"
echo -e "  Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "  API Docs:  ${BLUE}http://localhost:8000/api/docs${NC}"
echo ""
echo -e "Default login:"
echo -e "  Username:  ${YELLOW}admin${NC}"
echo -e "  Password:  ${YELLOW}admin123${NC}"
echo ""
echo -e "Useful commands:"
echo -e "  ${YELLOW}docker-compose logs -f${NC}          View logs"
echo -e "  ${YELLOW}docker-compose stop${NC}             Stop services"
echo -e "  ${YELLOW}docker-compose down${NC}             Stop and remove containers"
echo -e "  ${YELLOW}docker-compose restart backend${NC}  Restart backend"
echo ""
