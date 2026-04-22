#!/bin/bash

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Comprehensive Setup Script (Modern Edition)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Colors for better UI
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}===================================================="
echo -e "      CATUSERBOT SMART SETUP MANAGER (2026)"
echo -e "====================================================${NC}"

# Function to check OS and Package Manager
detect_manager() {
    if command -v apt &> /dev/null; then
        echo "apt"
    elif command -v pkg &> /dev/null; then
        echo "pkg"
    elif command -v pacman &> /dev/null; then
        echo "pacman"
    else
        echo "unknown"
    fi
}

PM=$(detect_manager)
echo -e "${GREEN}[*] Detected Package Manager: $PM${NC}"

# 1. System Dependencies Installation
echo -e "${YELLOW}[1/4] Installing System Dependencies...${NC}"
case $PM in
    apt)
        sudo apt-get update -y
        sudo apt-get install -y git python3 python3-pip python3-venv ffmpeg libmagickwand-dev libwebp-dev libxml2-dev libxslt1-dev zlib1g-dev g++ curl neofetch
        ;;
    pkg)
        pkg update -y
        pkg install -y git python ffmpeg imagemagick libwebp libxml2 libxslt zlib make clang curl neofetch
        ;;
    pacman)
        sudo pacman -Syu --noconfirm git python-pip python-venv ffmpeg imagemagick libwebp libxml2 libxslt zlib gcc curl neofetch
        ;;
    *)
        echo -e "${RED}[!] Unknown OS. Please install git, python3, ffmpeg, and ImageMagick manually.${NC}"
        ;;
esac

# 2. Python Virtual Environment Setup (Best Practice)
echo -e "${YELLOW}[2/4] Setting up Python Environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}[+] Virtual Environment created.${NC}"
fi

# Activate Venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# 3. Installing Python Requirements
echo -e "${YELLOW}[3/4] Installing Python Packages (Requirements)...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}[+] Python dependencies installed successfully.${NC}"
else
    echo -e "${RED}[!] requirements.txt not found!${NC}"
    exit 1
fi

# 4. Configuration Check (.env)
echo -e "${YELLOW}[4/4] Verifying Configuration...${NC}"
if [ ! -f ".env" ] && [ ! -f "config.py" ]; then
    echo -e "${CYAN}[!] Configuration (.env) not found. Starting Interactive Setup...${NC}"
    python3 -m userbot
else
    echo -e "${GREEN}[+] Configuration detected.${NC}"
fi

echo -e "${CYAN}===================================================="
echo -e "      SETUP COMPLETED SUCCESSFULLY!"
echo -e "===================================================="
echo -e "${GREEN}To start your bot, use:${NC}"
echo -e "${CYAN}source venv/bin/activate && python3 -m userbot${NC}"
echo -e "====================================================${NC}"
