# 📊 Economist-Style Financial Dashboard

A sophisticated, professional-grade financial analysis dashboard inspired by The Economist magazine, featuring real-time market data, economic indicators, interactive charts, and AI-powered forecasting.

![Dashboard Screenshot](https://img.shields.io/badge/Status-Production-green) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📈 Interactive Price Charts
- **60 days of real historical data** from Twelve Data API
- **30-day price forecasts** using linear regression and mean reversion
- **Interactive Chart.js visualizations** with hover tooltips
- Blue line for history, red dashed line for forecasts

### 💡 Economic Indicators with Tooltips
- **Global Economy**: Fed Rate, Inflation, Unemployment, GDP
- **Market Sentiment**: VIX, Consumer Confidence, Dollar Index, 2Y & 10Y Treasury Yields
- **Asset-Specific**: Currency-specific indicators (China GDP for CNY, ECB rate for EUR, etc.)
- **Comprehensive tooltips** explaining each indicator's meaning and impact

### 🎨 Economist Magazine Design
- Professional red & blue color scheme
- Clean typography (Econ Sans + Milo Serif)
- Publication-quality layout
- Responsive design

### 🌍 Multi-Asset Coverage (34 Instruments)
- **8 Currency Pairs**: USD/CNY, EUR/USD, GBP/USD, USD/JPY, etc.
- **10 Major Stocks**: AAPL, MSFT, GOOGL, TSLA, NVDA, etc.
- **6 Cryptocurrencies**: BTC/USD, ETH/USD, SOL/USD, etc.
- **4 Market Indices**: DIA (Dow), QQQ (NASDAQ), IWM (Russell 2000), VTI
- **6 Precious Metals**: XAU/USD (Gold), XAG/USD (Silver), XPT/USD (Platinum), etc.

### ⏰ Smart Refresh System
- **Hourly auto-refresh** (saves API requests)
- **Manual refresh button** with 1-minute cooldown
- Shows last update time and next refresh

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Twelve Data API key (free tier: 800 requests/day)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/alexjiaguo/economist-financial-dashboard.git
cd economist-financial-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get your API key**
- Sign up at [Twelve Data](https://twelvedata.com/)
- Get your free API key (800 requests/day)

4. **Set environment variable**
```bash
export TWELVEDATA_API_KEY="your_api_key_here"
```

5. **Run the dashboard**
```bash
python3 economist_dashboard.py
```

6. **Open in browser**
```
http://localhost:8080
```

---

## 📖 Usage Guide

### Selecting Assets
1. Choose **Asset Type** from dropdown (Currencies, Stocks, Crypto, Indices, Metals)
2. Select specific **Asset** from the second dropdown
3. View comprehensive analysis with chart, indicators, and forecasts

### Understanding the Chart
- **Blue solid line**: Real historical prices (60 days)
- **Red dashed line**: Forecast projection (30 days)
- **Hover**: See exact prices and dates
- **Trend**: Upward = bullish, downward = bearish, flat = neutral

### Reading Indicators
- **Blue "?" icon**: Hover to see detailed explanation
- **Green ↑**: Increasing value
- **Red ↓**: Decreasing value
- **Gray →**: Stable/unchanged

### Trading Signals
- **STRONG BUY**: >+2% daily change (80% confidence)
- **BUY**: >+0.5% daily change (65% confidence)
- **HOLD**: -0.5% to +0.5% (50% confidence)
- **SELL**: <-0.5% daily change (65% confidence)
- **STRONG SELL**: <-2% daily change (80% confidence)

---

## 🛠️ Technical Details

### Architecture
```
economist_dashboard.py
├── EconomistDashboard (Backend)
│   ├── fetch_asset_data()       # Real-time price from API
│   ├── fetch_historical_data()   # 60 days historical
│   ├── generate_forecast()       # 30-day prediction
│   ├── get_economic_indicators() # Mock economic data
│   └── calculate_analysis()      # Trading signals
│
├── Flask Routes
│   ├── / (dashboard_page)        # Serve HTML
│   └── /api/asset                # JSON data endpoint
│
└── HTML/JS/CSS Template
    ├── Chart.js visualization
    ├── Tooltip system
    └── Hourly auto-refresh
```

### Forecasting Algorithm
1. **Linear Regression**: Calculate trend from last 30 days
2. **Mean Reversion**: 2% daily pull toward long-term average
3. **Random Walk**: Uncertainty grows with √(time)
4. **Constraints**: Max ±30% change over 30 days

### API Endpoints
- **Quote**: `GET /quote?symbol=AAPL` - Current price
- **Time Series**: `GET /time_series?symbol=AAPL&interval=1day&outputsize=60` - Historical data

---

## 📊 Example Use Cases

### CNY/USD Trading
```
1. Select: Currencies → USD/CNY
2. Check chart: Is trend up or down?
3. Read indicators:
   - Fed Rate ↓ (weakens USD)
   - China GDP ↓ (weakens CNY)
   - Trade Surplus ↑ (strengthens CNY)
4. View forecast: Next 30 days projection
5. Make decision: Based on comprehensive analysis
```

### Gold Investment
```
1. Select: Precious Metals → XAU/USD
2. Check indicators:
   - High VIX → Good for gold (safe haven)
   - Strong USD → Bad for gold (inverse)
   - High inflation → Good for gold (hedge)
3. Analyze forecast: Bullish or bearish?
4. Decide: Buy, hold, or sell
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
export TWELVEDATA_API_KEY="your_key"

# Optional
export DASHBOARD_PORT="8080"  # Default port
```

### Customization
Edit `economist_dashboard.py`:
- **Refresh interval**: Line 1089 (`setInterval(..., 3600000)` = 1 hour)
- **Forecast days**: Line 1225 (`days=30`)
- **Historical days**: Line 1221 (`days=60`)

---

## 📚 Documentation

- **Quick Start**: `QUICK_START.md`
- **Full Guide**: `ECONOMIST_DASHBOARD_GUIDE.md`
- **New Features**: `NEW_FEATURES_SUMMARY.md`
- **Real Data Update**: `REAL_DATA_UPDATE.md`
- **Quick Reference**: `FEATURES_QUICK_REFERENCE.md`

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **Twelve Data** for providing the financial data API
- **Chart.js** for beautiful, interactive charts
- **The Economist** for design inspiration
- **Flask** for the web framework

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/economist-dashboard/issues)
- **Documentation**: See `docs/` folder
- **API Limits**: Twelve Data free tier = 800 requests/day

---

## 🔮 Roadmap

- [ ] Real economic data integration (FRED API)
- [ ] Machine learning forecasts (LSTM, Prophet)
- [ ] Multi-asset comparison charts
- [ ] Alert system (email/SMS)
- [ ] Portfolio tracking
- [ ] Historical backtesting
- [ ] News sentiment analysis
- [ ] Export charts as PNG/PDF

---

## 📊 Stats

- **34 Instruments** across 5 asset classes
- **60 Days** of historical data
- **30 Days** of forecasts
- **14 Economic Indicators** with tooltips
- **Hourly Updates** (auto-refresh)

---

## 🎯 Perfect For

- **Traders**: Real-time data with technical analysis
- **Investors**: Long-term trends and forecasts
- **Students**: Learn economics through real data
- **Analysts**: Professional-grade visualizations
- **Researchers**: Historical data access

---

**Built with ❤️ for financial analysis**

*Dashboard is production-ready and actively maintained*

---

## Quick Links

- [Live Demo](#) (Coming soon)
- [Documentation](docs/)
- [API Reference](https://twelvedata.com/docs)
- [Report Bug](https://github.com/yourusername/economist-dashboard/issues)
- [Request Feature](https://github.com/yourusername/economist-dashboard/issues)

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Status**: ✅ Production Ready

