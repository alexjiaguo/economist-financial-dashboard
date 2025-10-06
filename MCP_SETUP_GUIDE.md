# 🚀 MCP Setup Guide - Fixed Configuration

## ✅ **What's Been Fixed**

### **1. Alpha Vantage MCP** - ✅ READY TO USE
- **API Key**: `VCQ8ZZHQ7TNOZWZC` (set for current session)
- **Status**: Fully configured and ready
- **Test Command**: "Use Alpha Vantage MCP to get AAPL stock price"

### **2. Notion MCP** - ✅ CONFIGURED (Needs API Key)
- **Configuration**: Updated to use official MCP server
- **Needs**: Notion Integration Token
- **Setup**: See instructions below

### **3. Microsoft 365 MCP** - ✅ CONFIGURED (Needs Credentials)
- **Configuration**: Updated with proper environment variables
- **Needs**: MS365 App Registration credentials
- **Setup**: See instructions below

### **4. Cleaned Up Configuration**
- **Removed**: Unused financial MCP configurations
- **Kept**: Working tools (Google Drive, Filesystem, Sequential Thinking, Alpha Vantage)

## 🔧 **Current Working MCP Tools**

| Tool | Status | Test Command |
|------|--------|--------------|
| **Google Drive** | ✅ Working | "Use Google Drive MCP to list my files" |
| **Filesystem** | ✅ Working | "Use filesystem MCP to list files in my Documents" |
| **Sequential Thinking** | ✅ Working | "Use sequential thinking to break down a problem" |
| **Alpha Vantage** | ✅ Working | "Use Alpha Vantage MCP to get AAPL stock price" |

## 🛠 **Optional Setup (If You Want Them)**

### **Notion MCP Setup**
1. Go to [Notion Integrations](https://www.notion.com/my-integrations)
2. Click "New integration"
3. Name it "MCP Integration"
4. Copy the "Internal Integration Token"
5. Set environment variable:
   ```bash
   export NOTION_API_KEY="your_integration_token_here"
   ```
6. Restart Cursor

### **Microsoft 365 MCP Setup**
1. Go to [Azure App Registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
2. Create new app registration
3. Get Client ID, Client Secret, and Tenant ID
4. Set environment variables:
   ```bash
   export MS365_CLIENT_ID="your_client_id"
   export MS365_CLIENT_SECRET="your_client_secret"
   export MS365_TENANT_ID="your_tenant_id"
   ```
5. Restart Cursor

## 🧪 **Test Your Setup**

### **Immediate Tests (No Setup Required)**
```bash
# Test these in Cursor right now:
"Use Google Drive MCP to search for Tesla documents"
"Use filesystem MCP to list files in my Desktop"
"Use Alpha Vantage MCP to get the latest stock price for MSFT"
"Use sequential thinking to plan a project"
```

### **After Optional Setup**
```bash
# If you set up Notion:
"Use Notion MCP to create a new page"

# If you set up MS365:
"Use MS365 MCP to list my emails"
```

## 📁 **Configuration Files**

### **Global MCP Config** (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    },
    "ms365": {
      "command": "npx",
      "args": ["-y", "@softeria/ms-365-mcp-server", "--org-mode"],
      "env": {
        "MS365_CLIENT_ID": "${MS365_CLIENT_ID}",
        "MS365_CLIENT_SECRET": "${MS365_CLIENT_SECRET}",
        "MS365_TENANT_ID": "${MS365_TENANT_ID}"
      }
    },
    "google-drive": {
      "command": "npx",
      "args": ["@piotr-agier/google-drive-mcp"],
      "env": {
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "/Users/boss/Documents/cursor/test-project/gcp-oauth.keys.json"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/boss"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "alphavantage": {
      "url": "https://mcp.alphavantage.co/mcp?apikey=${ALPHAVANTAGE_API_KEY}"
    }
  }
}
```

## 🎯 **Next Steps**

1. **Test the working tools** - Try the test commands above
2. **Set up optional tools** - Only if you need them
3. **Use in your projects** - MCP tools are now available across all projects

## 🚨 **Important Notes**

- **Alpha Vantage API key** is set for current session only
- **Restart Cursor** after setting up new environment variables
- **Google Drive** requires OAuth credentials (already configured)
- **Filesystem access** is limited to `/Users/boss` for security

Your MCP setup is now **optimized and ready to use**! 🎉
