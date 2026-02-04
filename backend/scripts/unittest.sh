#!/bin/bash
# Unit test runner script

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running unit tests...${NC}"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run pytest with coverage
if pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-report=html; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
    exit 0
else
    echo -e "${RED}❌ Tests failed!${NC}"
    exit 1
fi
