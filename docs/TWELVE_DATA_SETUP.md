# 🚀 Twelve Data Setup Guide

## ✨ **WHY TWELVE DATA?**

Twelve Data offers a much better free tier than Alpha Vantage:

| Feature | Alpha Vantage (Free) | Twelve Data (Free) |
|---------|---------------------|-------------------|
| **Daily Requests** | 25 | 800 |
| **Per-minute Limit** | 5 | 8 |
| **Assets Supported** | Limited | Comprehensive |
| **Best For** | Testing only | Active monitoring |

**Result**: You can monitor 10-20 assets with hourly updates!

---

## 📝 **STEP 1: GET YOUR API KEY**

### **Sign Up (2 minutes)**
1. Visit: https://twelvedata.com/
2. Click **"Sign Up Free"** or **"Get Free API Key"**
3. Enter your email address
4. Verify your email
5. Copy your API key

**Example API Key**: `abc123def456ghi789jkl012mno345pq`

---

## 🔧 **STEP 2: INSTALL THE DASHBOARD**

### **Method 1: Using the Python Script (Recommended)**

```bash
# Set your Twelve Data API key
export TWELVEDATA_API_KEY="YOUR_API_KEY_HERE"

# Stop the old dashboard
pkill -f "dashboard"

# Start the new Twelve Data dashboard
python3 twelve_data_dashboard.py
```

### **Method 2: Create a Launcher Script**

Create a file called `start_twelve_data.sh`:

```bash
#!/bin/bash
export TWELVEDATA_API_KEY="YOUR_API_KEY_HERE"
python3 twelve_data_dashboard.py
```

Then run:
```bash
chmod +x start_twelve_data.sh
./start_twelve_data.sh
```

---

## 🎯 **STEP 3: TEST THE DASHBOARD**

1. **Open your browser**: http://localhost:8080
2. **You should see**: Beautiful dashboard with "Powered by Twelve Data"
3. **Add an asset**: 
   - Select "Currency Pair"
   - Choose "USD/CNY"
   - Click "Add Asset"
4. **Wait a few seconds**: Real data should appear!

---

## 📊 **WHAT'S SUPPORTED**

### **✅ Currency Pairs** (800 requests/day = monitor ~15 pairs hourly)
- USD/CNY, EUR/USD, GBP/USD
- USD/JPY, AUD/USD, USD/CAD
- USD/CHF, NZD/USD, EUR/GBP
- EUR/JPY, GBP/JPY, CNY/USD
- And more!

### **✅ Stocks** (All major US stocks)
- AAPL, MSFT, GOOGL, AMZN
- TSLA, META, NVDA, JPM
- V, PG, MA, HD, DIS
- And thousands more!

### **✅ Cryptocurrencies** (Real-time crypto prices)
- BTC/USD, ETH/USD, BNB/USD
- ADA/USD, SOL/USD, XRP/USD
- DOT/USD, DOGE/USD, AVAX/USD
- And more!

### **✅ Market Indices** (Global indices)
- SPX (S&P 500), NDX (NASDAQ 100)
- DJI (Dow Jones), RUT (Russell 2000)
- VIX (Volatility), FTSE (FTSE 100)
- DAX, Nikkei 225, Hang Seng
- And more!

---

## 🎮 **HOW TO USE**

### **Basic Usage**
1. **Select asset type**: Currency, Stock, Crypto, or Index
2. **Choose symbol**: From the dropdown
3. **Click "Add Asset"**: It appears as a card
4. **Monitor**: Auto-updates every 30 seconds

### **Trading Signals**
Each asset shows:
- **Current Price**: Real-time market price
- **Price Change**: Daily % change (with color)
- **Signal**: BUY/SELL/HOLD recommendation
- **Confidence**: 60-80% confidence level
- **Reasoning**: Why the signal was generated
- **Risk Level**: LOW/MEDIUM/HIGH

### **Example Asset Card**
```
USD/CNY - US Dollar to Chinese Yuan
7.1185 +0.15%
🟡 HOLD
Confidence: 60%
Reasoning: Stable price movement (+0.15%)
Risk: MEDIUM
```

---

## 💡 **USAGE OPTIMIZATION**

### **Free Tier Strategy (800 requests/day)**

**Option 1: Intensive Monitoring (5-10 assets)**
- Monitor 5-10 assets
- Auto-refresh every 30 seconds
- Budget: ~50-100 requests/hour
- Total: ~400-800 requests/day
- **Best for**: Active day trading

**Option 2: Balanced Monitoring (10-15 assets)**
- Monitor 10-15 assets
- Auto-refresh every 60 seconds
- Budget: ~30-50 requests/hour
- Total: ~300-600 requests/day
- **Best for**: Regular monitoring

**Option 3: Extended Monitoring (15-20 assets)**
- Monitor 15-20 assets
- Auto-refresh every 2 minutes
- Budget: ~20-30 requests/hour
- Total: ~200-400 requests/day
- **Best for**: Long-term tracking

---

## 🔒 **API KEY MANAGEMENT**

### **Keep Your Key Safe**
```bash
# Good: Environment variable
export TWELVEDATA_API_KEY="your_key_here"

# Bad: Hardcoded in script
api_key = "your_key_here"  # DON'T DO THIS!
```

### **Permanent Setup (Optional)**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export TWELVEDATA_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## 📈 **UPGRADING TO PAID TIER**

If you need more requests, Twelve Data offers paid plans:

| Plan | Requests/Day | Price/Month | Best For |
|------|--------------|-------------|----------|
| **Free** | 800 | $0 | Testing, light use |
| **Basic** | 10,000 | $8 | Active monitoring |
| **Pro** | 20,000 | $29 | Day trading |
| **Business** | 40,000 | $69 | Professional use |

Visit: https://twelvedata.com/pricing

---

## 🆚 **COMPARISON: TWELVE DATA vs ALPHA VANTAGE**

### **Free Tier Comparison**
| Feature | Alpha Vantage | Twelve Data | Winner |
|---------|--------------|-------------|--------|
| Daily Requests | 25 | 800 | 🏆 Twelve Data |
| Asset Coverage | Good | Excellent | 🏆 Twelve Data |
| Real-time Data | Yes | Yes | ⚖️ Tie |
| Historical Data | Yes | Yes | ⚖️ Tie |
| Crypto Support | Limited | Full | 🏆 Twelve Data |
| Documentation | Good | Better | 🏆 Twelve Data |

### **Your Use Case: Currency Trading**
- **Alpha Vantage**: 25 requests = 2-3 checks per day only
- **Twelve Data**: 800 requests = Monitor all day with 10+ assets
- **Recommendation**: 🏆 **Twelve Data wins easily!**

---

## 🛠️ **TROUBLESHOOTING**

### **Error: "Invalid API key"**
**Solution**: Check your API key is correct
```bash
# Test your API key
curl "https://api.twelvedata.com/quote?symbol=USD/CNY&apikey=YOUR_KEY"
```

### **Error: "Rate limit exceeded"**
**Solution**: You've used your 800 daily requests
- Wait until midnight UTC for reset
- Or upgrade to paid plan

### **No Data Showing**
**Solution**: 
1. Check your internet connection
2. Verify API key is set: `echo $TWELVEDATA_API_KEY`
3. Check browser console for errors (F12)

### **Dashboard Won't Start**
**Solution**:
```bash
# Kill any existing dashboard
pkill -f "dashboard"

# Check if port 8080 is free
lsof -i :8080

# If occupied, kill it
kill <PID>

# Restart dashboard
python3 twelve_data_dashboard.py
```

---

## 📱 **MOBILE ACCESS**

Your dashboard is responsive and works on mobile!

**Access from phone/tablet:**
1. Find your computer's local IP: `ifconfig | grep "inet "`
2. On mobile browser: `http://YOUR_IP:8080`
3. Example: `http://192.168.1.100:8080`

---

## 🎉 **QUICK START CHECKLIST**

- [  ] Sign up at https://twelvedata.com/
- [  ] Copy your API key
- [  ] Set environment variable: `export TWELVEDATA_API_KEY="your_key"`
- [  ] Stop old dashboard: `pkill -f "dashboard"`
- [  ] Start new dashboard: `python3 twelve_data_dashboard.py`
- [  ] Open browser: http://localhost:8080
- [  ] Add USD/CNY asset
- [  ] Verify real data appears
- [  ] Add more assets you want to monitor
- [  ] Start trading with confidence! 🚀

---

## 💬 **SUPPORT**

### **Twelve Data Support**
- Email: support@twelvedata.com
- Docs: https://twelvedata.com/docs
- Status: https://status.twelvedata.com/

### **Dashboard Issues**
- Check terminal output for errors
- Verify API key is set correctly
- Ensure port 8080 is available

---

## ✅ **YOU'RE ALL SET!**

Your new Universal Trading Dashboard with Twelve Data is ready to use!

**Benefits:**
- ✅ 800 free requests/day (vs 25 with Alpha Vantage)
- ✅ Monitor 10-20 assets simultaneously  
- ✅ Real-time data for currencies, stocks, crypto, indices
- ✅ Beautiful modern UI with trading signals
- ✅ No daily limits frustration!

**Open http://localhost:8080 and start trading!** 🎯
