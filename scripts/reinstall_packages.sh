#!/bin/bash

# Script to reinstall all dependencies in the scrappers-mock monorepo
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Reinstalling scrappers-mock dependencies ===${NC}"

# Get the repository root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo -e "${YELLOW}Repository root: $REPO_ROOT${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}No virtual environment found. Creating one...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip, setuptools, and wheel
echo -e "${YELLOW}Upgrading pip, setuptools, and wheel...${NC}"
pip install --upgrade pip setuptools wheel

# Uninstall existing packages (if any)
echo -e "${YELLOW}Uninstalling existing packages...${NC}"
pip uninstall -y scrapper-service job-scrapper-contracts scrapper-messaging 2>/dev/null || true

# Clear pip cache for git dependencies
echo -e "${YELLOW}Clearing pip cache for git dependencies...${NC}"
pip cache remove job-scrapper-contracts 2>/dev/null || true
pip cache remove scrapper-messaging 2>/dev/null || true

# Install packages in editable mode with dev dependencies
echo -e "${YELLOW}Installing packages in editable mode...${NC}"
for pkg in packages/*/; do
    if [ -f "$pkg/pyproject.toml" ]; then
        echo -e "${GREEN}Installing $(basename $pkg)...${NC}"
        pip install -e "$pkg[dev]"
    fi
done

echo -e "${GREEN}=== Dependencies reinstalled successfully! ===${NC}"
echo -e "${YELLOW}Virtual environment: $REPO_ROOT/.venv${NC}"
echo -e "${YELLOW}To activate: source .venv/bin/activate${NC}"