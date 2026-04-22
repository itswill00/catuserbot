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
if [ ! -f ".env" ]; then
    if [ -f ".env.sample" ]; then
        echo -e "${CYAN}[*] Creating .env from .env.sample template...${NC}"
        cp .env.sample .env
        echo -e "${GREEN}[+] .env file created successfully.${NC}"
    else
        echo -e "${RED}[!] .env.sample not found. Creating a basic .env template...${NC}"
        cat > .env << EOF
APP_ID=
API_HASH=
STRING_SESSION=
TG_BOT_TOKEN=
EOF
    fi
    echo -e "\n${YELLOW}NEXT STEPS:${NC}"
    echo -e "1. Edit the ${CYAN}.env${NC} file and fill in your details (APP_ID, API_HASH, etc.)"
    echo -e "2. Run ${CYAN}python3 stringsetup.py${NC} to generate your STRING_SESSION"
    echo -e "3. Start the bot with ${CYAN}python3 -m userbot${NC}"
else
    echo -e "${GREEN}[+] .env configuration detected.${NC}"
fi

echo -e "\n${CYAN}===================================================="
echo -e "      SETUP COMPLETED SUCCESSFULLY!"
echo -e "===================================================="
echo -e "${GREEN}1. FILL DATA IN .env${NC}"
echo -e "${GREEN}2. RUN: ${CYAN}python3 stringsetup.py${NC}"
echo -e "${GREEN}3. START: ${CYAN}python3 -m userbot${NC}"
echo -e "====================================================${NC}"
