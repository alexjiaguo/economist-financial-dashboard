#!/bin/bash

# MCP Environment Setup Script
# Run this script to set up all MCP environment variables

echo "🚀 Setting up MCP Environment Variables..."

# Alpha Vantage (Already configured)
export ALPHAVANTAGE_API_KEY="VCQ8ZZHQ7TNOZWZC"
echo "✅ Alpha Vantage API key set"

# Optional: Notion (uncomment and add your token)
# export NOTION_API_KEY="your_notion_integration_token_here"
# echo "✅ Notion API key set"

# Optional: Microsoft 365 (uncomment and add your credentials)
# export MS365_CLIENT_ID="your_client_id_here"
# export MS365_CLIENT_SECRET="your_client_secret_here"
# export MS365_TENANT_ID="your_tenant_id_here"
# echo "✅ Microsoft 365 credentials set"

echo ""
echo "🎯 Current MCP Environment Status:"
echo "Alpha Vantage: ✅ Ready"
echo "Google Drive: ✅ Ready (OAuth configured)"
echo "Filesystem: ✅ Ready"
echo "Sequential Thinking: ✅ Ready"
echo "Notion: ⚠️  Needs API key (optional)"
echo "Microsoft 365: ⚠️  Needs credentials (optional)"
echo ""
echo "📝 To make changes permanent, add the export commands to your ~/.zshrc"
echo "🔄 Restart Cursor after setting up new environment variables"
echo ""
echo "🧪 Test your setup with these commands in Cursor:"
echo "  'Use Alpha Vantage MCP to get AAPL stock price'"
echo "  'Use Google Drive MCP to list my files'"
echo "  'Use filesystem MCP to list files in my Documents'"
