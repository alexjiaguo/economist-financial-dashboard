# Global Financial MCP Tools Setup

## ✅ **Financial MCP Tools Now Global!**

I've successfully moved all your financial MCP tools to the **global configuration**, making them available across **all your projects**!

## 🌍 **Your Complete Global MCP Arsenal**

### **Productivity Tools:**
- **Notion** - Documentation and note-taking
- **Microsoft 365** - Office integration
- **Google Drive** - File management and collaboration
- **Filesystem** - File operations (access to `/Users/boss`)
- **Sequential Thinking** - Problem-solving and reasoning

### **Financial Data Tools:**
- **Alpha Vantage** - Real-time and historical financial data
- **Financial Datasets** - Comprehensive market data
- **Alpaca** - Trading platform integration
- **Octagon AI** - Financial AI and analysis
- **Yahoo Finance** - Market data and news

## 🔧 **Environment Variables Required**

To use the financial MCP tools, you need to set these environment variables:

```bash
# Alpha Vantage (Required - has working URL)
export ALPHAVANTAGE_API_KEY="your_alpha_vantage_key"

# Financial Datasets (Placeholder - needs real URL)
export FINANCIAL_DATASETS_MCP_URL="https://<provider>/mcp"
export FINANCIAL_DATASETS_API_KEY="your_financialdatasets_key"

# Alpaca (Placeholder - needs real URL)
export ALPACA_MCP_URL="https://<provider>/mcp"
export ALPACA_API_KEY="your_alpaca_key"
export ALPACA_API_SECRET="your_alpaca_secret"

# Octagon AI (Placeholder - needs real URL)
export OCTAGONAI_MCP_URL="https://<provider>/mcp"
export OCTAGONAI_API_KEY="your_octagonai_key"

# Yahoo Finance (Placeholder - needs real URL)
export YAHOO_FINANCE_MCP_URL="https://<provider>/mcp"
```

## 🚀 **How to Use Financial MCP Tools**

### **Alpha Vantage (Ready to Use):**
```bash
# Set your API key
export ALPHAVANTAGE_API_KEY="your_key_here"

# Restart Cursor, then use:
"Use Alpha Vantage MCP to get the latest stock price for AAPL"
"Get RSI technical indicator for MSFT using Alpha Vantage"
"Fetch daily closing prices for TSLA for the last 30 days"
```

### **Other Financial Tools (Need Setup):**
Once you have the real MCP URLs and API keys:
```bash
"Use Financial Datasets MCP to analyze market trends"
"Get trading signals from Alpaca MCP"
"Use Octagon AI MCP for financial analysis"
"Fetch market news from Yahoo Finance MCP"
```

## 📁 **Configuration Structure**

### **Global Config** (`~/.cursor/mcp.json`):
- ✅ All productivity tools
- ✅ All financial data tools
- ✅ Available in every project

### **Project Config** (`.cursor/mcp.json`):
- ✅ Project-specific filesystem access
- ✅ Can override global settings if needed

## 🎯 **Benefits of Global Financial Tools**

### **Cross-Project Financial Analysis:**
- **Research projects** - Get market data for any analysis
- **Trading projects** - Access trading platforms from anywhere
- **Documentation** - Include financial data in any project
- **Portfolio management** - Track investments across projects

### **Consistent Financial Workflow:**
- Same financial tools in every project
- No need to reconfigure for each project
- Unified financial data access
- Enhanced AI financial analysis capabilities

## 🔑 **Getting Started**

### **Step 1: Set Alpha Vantage API Key**
```bash
export ALPHAVANTAGE_API_KEY="your_alpha_vantage_key"
```

### **Step 2: Restart Cursor**
Close and reopen Cursor to load the global configuration.

### **Step 3: Test Alpha Vantage**
Try this prompt in any project:
```
"Use Alpha Vantage MCP to get the current stock price for Apple (AAPL)"
```

### **Step 4: Set Up Other Financial Tools**
As you get API keys and MCP URLs for the other services, add them to your environment variables.

## 📊 **Example Use Cases**

### **Market Research:**
```
"Use Alpha Vantage MCP to compare the performance of AAPL, MSFT, and GOOGL over the last 6 months"
```

### **Technical Analysis:**
```
"Get RSI, MACD, and moving averages for TSLA using Alpha Vantage MCP"
```

### **Portfolio Analysis:**
```
"Use Alpha Vantage MCP to analyze my portfolio: AAPL, MSFT, GOOGL, AMZN, TSLA"
```

### **Financial Documentation:**
```
"Use Notion MCP to create a financial analysis report with data from Alpha Vantage"
```

## 🎉 **You're All Set!**

Your MCP tools are now **globally available** across all projects:

- ✅ **Productivity tools** - Notion, Google Drive, Office 365
- ✅ **Financial data tools** - Alpha Vantage (ready), others (need setup)
- ✅ **File operations** - Available everywhere
- ✅ **AI reasoning** - Sequential thinking in all projects

**Start with Alpha Vantage** (it's ready to use) and gradually add the other financial tools as you get their API keys and MCP URLs!
