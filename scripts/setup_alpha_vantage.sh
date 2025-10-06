#!/bin/bash

# Alpha Vantage API Key Setup Script
# Run this script to set up your Alpha Vantage API key

echo "Setting up Alpha Vantage API key..."

# Set the API key for current session
export ALPHAVANTAGE_API_KEY="VCQ8ZZHQ7TNOZWZC"

# Add to shell profile for persistence
echo "export ALPHAVANTAGE_API_KEY=\"VCQ8ZZHQ7TNOZWZC\"" >> ~/.zshrc

echo "✅ Alpha Vantage API key set up successfully!"
echo ""
echo "Current session: API key is now available"
echo "Permanent setup: Added to ~/.zshrc for future sessions"
echo ""
echo "Next steps:"
echo "1. Restart Cursor to load the MCP configuration"
echo "2. Test with: 'Use Alpha Vantage MCP to get AAPL stock price'"
echo ""
echo "To reload your shell profile now, run:"
echo "source ~/.zshrc"
