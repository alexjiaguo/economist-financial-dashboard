# 🇨🇳 CNY/USD Trading Dashboard

## 🎯 **Purpose**
Real-time dashboard to monitor CNY/USD exchange rates and key economic indicators to help you **maximize USD gains** when selling Chinese Yuan.

## 🚀 **Quick Start**

### **1. Set up API Key**
```bash
export ALPHAVANTAGE_API_KEY="your_api_key_here"
```

### **2. Launch Dashboard**
```bash
./launch_dashboard.sh
```

### **3. Open Browser**
Navigate to: http://localhost:8501

## 📊 **Dashboard Features**

### **Real-Time Monitoring**
- ✅ **Live CNY/USD exchange rate**
- ✅ **Trading signals and recommendations**
- ✅ **Fed policy expectations**
- ✅ **Economic indicators**
- ✅ **Profit calculator**

### **Trading Signals**
- 🟢 **SELL**: When CNY/USD ≤ 7.0 (Excellent rate)
- 🟡 **HOLD**: When CNY/USD 7.0-7.2 (Wait for better rate)
- 🔴 **SELL**: When CNY/USD ≥ 7.3 (Stop-loss)

### **Key Indicators**
- **Fed Funds Rate**: Current and expected rates
- **Inflation**: PCE and CPI data
- **Unemployment**: Labor market conditions
- **GDP Growth**: Economic health
- **Treasury Yields**: Bond market signals
- **VIX**: Market volatility
- **USD Index**: Dollar strength

## 🎯 **Trading Strategy**

### **Current Recommendation (October 2025)**
- **Action**: **WAIT** (70% probability of Fed rate cuts)
- **Target Rate**: CNY/USD below 7.0
- **Stop Loss**: CNY/USD above 7.3
- **Expected Gain**: $400-500 more USD per 100,000 CNY

### **Key Dates**
- **October 29, 2025**: Fed meeting (90% cut probability)
- **December 17, 2025**: Fed meeting (60% cut probability)
- **January 28, 2026**: Fed meeting (40% cut probability)

## 📈 **Charts & Visualizations**

### **1. Exchange Rate Chart**
- Historical CNY/USD rates
- Moving averages (20-day)
- Target levels and stop-losses
- Trading signals

### **2. Fed Policy Chart**
- Rate cut probabilities
- Expected Fed funds rates
- Meeting schedule

### **3. Economic Indicators**
- Radar chart of key metrics
- Current vs target values
- Fed mandate indicators

### **4. Profit Calculator**
- Real-time profit calculations
- What-if scenarios
- Risk assessment

## 🔔 **Alerts & Notifications**

### **Automatic Alerts**
- ✅ Rate drops below target
- ✅ Fed meeting announcements
- ✅ Economic data releases
- ✅ Stop-loss triggers

### **Customizable Settings**
- Alert thresholds
- Refresh intervals
- Position sizing
- Risk parameters

## ⚙️ **Configuration**

### **Sidebar Settings**
- **Refresh Interval**: 30s, 1m, 2m, 5m
- **Auto Refresh**: Enable/disable
- **Position Size**: Your CNY amount
- **Target Rate**: Desired exchange rate
- **Alerts**: Enable/disable notifications

### **API Configuration**
- **Alpha Vantage**: Real-time data
- **Rate Limits**: 5 calls/minute, 500/day
- **Data Sources**: Forex, economic indicators

## 📊 **Data Sources**

### **Real-Time Data**
- **Alpha Vantage API**: Exchange rates, economic data
- **Federal Reserve**: Policy rates, meeting schedules
- **Market Data**: Treasury yields, VIX, S&P 500

### **Historical Data**
- **5,000+ days** of CNY/USD history
- **Technical indicators**: Moving averages, volatility
- **Economic cycles**: Fed policy changes

## 🎯 **Trading Recommendations**

### **Based on Current Analysis**

#### **🟢 SELL Signals (High Confidence)**
- CNY/USD ≤ 7.0: **Excellent rate** - Sell immediately
- CNY/USD ≤ 7.1: **Good rate** - Consider selling

#### **🟡 HOLD Signals (Medium Confidence)**
- CNY/USD 7.1-7.2: **Wait for Fed cuts** - Hold position

#### **🔴 SELL Signals (Risk Management)**
- CNY/USD ≥ 7.3: **Stop-loss** - Sell to limit losses

### **Risk Management**
- **Position Sizing**: Don't risk more than you can afford
- **Stop Losses**: Set at 7.3 CNY/USD
- **Diversification**: Consider splitting position
- **Monitoring**: Watch Fed communications closely

## 📱 **Mobile Support**
- ✅ **Responsive design** - Works on all devices
- ✅ **Touch-friendly** - Easy mobile navigation
- ✅ **Real-time updates** - Stay informed anywhere

## 🔧 **Troubleshooting**

### **Common Issues**

#### **API Key Error**
```bash
export ALPHAVANTAGE_API_KEY="your_key_here"
```

#### **Port Already in Use**
```bash
streamlit run cny_usd_dashboard.py --server.port 8502
```

#### **Missing Dependencies**
```bash
pip3 install -r dashboard_requirements.txt
```

### **Performance Tips**
- Use 60-second refresh for better performance
- Close unused browser tabs
- Monitor API rate limits

## 📚 **Educational Resources**

### **Understanding the Dashboard**
- **Exchange Rates**: How CNY/USD affects your conversion
- **Fed Policy**: Why interest rates matter
- **Economic Indicators**: What drives currency movements
- **Technical Analysis**: Chart patterns and signals

### **Trading Psychology**
- **Patience**: Wait for optimal rates
- **Discipline**: Stick to your strategy
- **Risk Management**: Protect your capital
- **Emotional Control**: Don't panic sell

## 🎉 **Success Tips**

### **Maximize Your Gains**
1. **Monitor daily** - Check dashboard regularly
2. **Set alerts** - Don't miss opportunities
3. **Be patient** - Wait for optimal rates
4. **Manage risk** - Use stop-losses
5. **Stay informed** - Watch Fed communications

### **Common Mistakes to Avoid**
- ❌ **Panic selling** on temporary volatility
- ❌ **Getting greedy** - take profits at target levels
- ❌ **Ignoring stop-losses** - protect your capital
- ❌ **Over-leveraging** - don't risk more than you can afford

## 📞 **Support**

### **Getting Help**
- Check the troubleshooting section
- Review the analysis reports
- Monitor economic news
- Consult financial professionals

### **Updates**
- Dashboard updates automatically
- New features added regularly
- Bug fixes and improvements
- Enhanced data sources

---

## 🎯 **Bottom Line**

This dashboard is designed to help you **maximize USD gains** when selling CNY by:

1. **Monitoring real-time rates** and market conditions
2. **Providing clear trading signals** based on analysis
3. **Tracking Fed policy** that drives currency movements
4. **Calculating potential profits** for different scenarios
5. **Alerting you** to optimal selling opportunities

**Remember**: The goal is to sell CNY when you get the **most USD possible**. Use this dashboard to make informed decisions and maximize your gains! 🚀

---

*This dashboard is for informational purposes only and should not be considered as financial advice. Always consult with financial professionals for investment decisions.*
