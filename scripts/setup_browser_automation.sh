#!/bin/bash

echo "Setting up Browser Automation Environment"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
python3 -m playwright install

# Install ChromeDriver for Selenium (if on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing ChromeDriver for Selenium..."
    if command -v brew &> /dev/null; then
        brew install chromedriver
    else
        echo "Homebrew not found. Please install ChromeDriver manually from https://chromedriver.chromium.org/"
    fi
fi

echo ""
echo "Setup complete! You can now run browser automation scripts."
echo ""
echo "To run the example script:"
echo "python3 browser_automation_example.py"
echo ""
echo "To test Playwright installation:"
echo "python3 -c \"from playwright.sync_api import sync_playwright; print('Playwright is working!')\""
