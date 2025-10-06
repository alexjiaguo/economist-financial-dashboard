# How to Get API Keys for Financial MCP Tools

## 🔑 **API Key Setup Guide**

Here's how to get API keys for each financial MCP tool:

## 1. **Alpha Vantage** (✅ Ready to Use)

### **Get Your API Key:**
1. **Visit**: https://www.alphavantage.co/support/#api-key
2. **Sign up** for a free account
3. **Get your API key** (free tier: 5 API calls per minute, 500 calls per day)
4. **Set environment variable**:
   ```bash
   export ALPHAVANTAGE_API_KEY="your_alpha_vantage_key_here"
   ```

### **Test It:**
```bash
# Restart Cursor, then try:
"Use Alpha Vantage MCP to get the current stock price for AAPL"
```

---

## 2. **Financial Datasets** (❓ Needs Verification)

### **Status**: This appears to be a placeholder service. You may need to:
1. **Research alternatives** like:
   - **Quandl** (now Nasdaq Data Link)
   - **IEX Cloud**
   - **Polygon.io**
   - **Finnhub**

### **Alternative - Quandl/Nasdaq Data Link:**
1. **Visit**: https://data.nasdaq.com/
2. **Sign up** for free account
3. **Get API key**
4. **Set environment variable**:
   ```bash
   export FINANCIAL_DATASETS_API_KEY="your_quandl_key"
   export FINANCIAL_DATASETS_MCP_URL="https://api.nasdaq.com/v1"
   ```

---

## 3. **Alpaca** (📈 Trading Platform)

### **Get Your API Keys:**
1. **Visit**: https://alpaca.markets/
2. **Sign up** for free account
3. **Go to**: Dashboard → API Keys
4. **Generate** API Key and Secret
5. **Set environment variables**:
   ```bash
   export ALPACA_API_KEY="your_alpaca_key"
   export ALPACA_API_SECRET="your_alpaca_secret"
   export ALPACA_MCP_URL="https://paper-api.alpaca.markets"  # Paper trading
   # or
   export ALPACA_MCP_URL="https://api.alpaca.markets"  # Live trading
   ```

### **Note**: Alpaca offers paper trading (free) and live trading (requires account funding)

---

## 4. **Octagon AI** (🤖 Financial AI)

### **Status**: This appears to be a placeholder service. Consider alternatives:
- **OpenAI API** for financial analysis
- **Anthropic Claude** for financial reasoning
- **Custom financial AI services**

### **Alternative - OpenAI for Financial Analysis:**
1. **Visit**: https://platform.openai.com/
2. **Sign up** and get API key
3. **Set environment variable**:
   ```bash
   export OCTAGONAI_API_KEY="your_openai_key"
   export OCTAGONAI_MCP_URL="https://api.openai.com/v1"
   ```

---

## 5. **Yahoo Finance** (📊 Market Data)

### **Status**: Yahoo Finance doesn't have an official MCP server. Consider alternatives:

### **Alternative - Yahoo Finance API via RapidAPI:**
1. **Visit**: https://rapidapi.com/apidojo/api/yahoo-finance1/
2. **Sign up** for free account
3. **Get API key**
4. **Set environment variable**:
   ```bash
   export YAHOO_FINANCE_API_KEY="your_rapidapi_key"
   export YAHOO_FINANCE_MCP_URL="https://yahoo-finance1.p.rapidapi.com"
   ```

### **Alternative - Free Yahoo Finance APIs:**
- **yfinance** (Python library)
- **yahoo-finance-api** (Node.js)
- **Direct Yahoo Finance endpoints** (unofficial)

---

## 🚀 **Quick Start (Recommended)**

### **Start with Alpha Vantage (Easiest):**
1. **Get Alpha Vantage API key** (free, 5 minutes)
2. **Set environment variable**:
   ```bash
   export ALPHAVANTAGE_API_KEY="your_key"
   ```
3. **Restart Cursor**
4. **Test immediately**:
   ```
   "Use Alpha Vantage MCP to get AAPL stock price"
   ```

### **Add Alpaca for Trading (Second Priority):**
1. **Sign up for Alpaca** (free paper trading)
2. **Get API keys**
3. **Set environment variables**
4. **Test trading functionality**

---

## 🔧 **Environment Variable Setup**

### **Add to your shell profile** (`~/.zshrc` or `~/.bash_profile`):
```bash
# Alpha Vantage (Ready to use)
export ALPHAVANTAGE_API_KEY="your_alpha_vantage_key"

# Alpaca Trading (Get from alpaca.markets)
export ALPACA_API_KEY="your_alpaca_key"
export ALPACA_API_SECRET="your_alpaca_secret"
export ALPACA_MCP_URL="https://paper-api.alpaca.markets"

# Yahoo Finance (Alternative via RapidAPI)
export YAHOO_FINANCE_API_KEY="your_rapidapi_key"
export YAHOO_FINANCE_MCP_URL="https://yahoo-finance1.p.rapidapi.com"

# OpenAI for Financial AI (Alternative)
export OCTAGONAI_API_KEY="your_openai_key"
export OCTAGONAI_MCP_URL="https://api.openai.com/v1"

# Quandl/Nasdaq for Financial Datasets (Alternative)
export FINANCIAL_DATASETS_API_KEY="your_quandl_key"
export FINANCIAL_DATASETS_MCP_URL="https://data.nasdaq.com/api/v3"
```

### **Reload your shell**:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

---

## 🎯 **Priority Order**

1. **Alpha Vantage** - ✅ Easiest, most reliable
2. **Alpaca** - 📈 Great for trading functionality
3. **Yahoo Finance (RapidAPI)** - 📊 Good market data alternative
4. **OpenAI** - 🤖 For financial AI analysis
5. **Quandl/Nasdaq** - 📈 Comprehensive financial datasets

---

## 🧪 **Testing Your Setup**

After setting up each API key:

1. **Restart Cursor**
2. **Test with simple prompts**:
   ```
   "Use Alpha Vantage MCP to get the current price of AAPL"
   "Use Alpaca MCP to check my account balance"
   "Use Yahoo Finance MCP to get market news"
   ```

3. **Check for errors** in Cursor's output panel

---

## 💡 **Pro Tips**

- **Start with Alpha Vantage** - it's the most straightforward
- **Use paper trading** for Alpaca initially
- **Check rate limits** for each service
- **Keep API keys secure** - never commit them to version control
- **Use environment variables** for security

Ready to get started? Begin with Alpha Vantage - it's the quickest win! 🚀
