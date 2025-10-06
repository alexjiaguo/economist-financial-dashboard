# 📊 Economist Financial Dashboard

A professional, real-time financial dashboard inspired by The Economist magazine. Track currencies, stocks, cryptocurrencies, indices, and precious metals with interactive charts, economic indicators, and AI-powered forecasts.

![Dashboard](https://img.shields.io/badge/Dashboard-Live-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production-success)

## ✨ Features

### 📈 34 Financial Instruments
- **8 Currency Pairs**: USD/CNY, EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF, NZD/USD
- **10 Major Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, JPM, V, WMT
- **6 Cryptocurrencies**: BTC, ETH, BNB, SOL, XRP, ADA
- **4 Market Indices**: DIA, QQQ, IWM, VTI
- **6 Precious Metals**: Gold, Silver, Platinum, Palladium, Gold ETF, Silver ETF

### 🎯 Real-Time Data & Analysis
- ✅ **Live Prices** from Twelve Data API
- ✅ **60-Day Historical Charts** with real market data
- ✅ **30-Day Forecasts** using advanced algorithms
- ✅ **14 Economic Indicators** with interactive tooltips
- ✅ **Hourly Auto-Refresh** with manual refresh option

### 🎨 Economist Magazine Design
- Professional typography and layout
- Clean, minimalistic interface
- Interactive Chart.js visualizations
- Responsive design for all devices

### 💡 Smart Features
- **Economic Indicators**: Fed Rate, Inflation, Unemployment, GDP, VIX, Treasury Yields, and more
- **Asset-Specific Analysis**: Trends, volatility, predictions
- **Interactive Tooltips**: Understand what each indicator means
- **Forecasting Algorithm**: Linear regression + mean reversion + random walk

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Twelve Data API key (free tier: 800 requests/day)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/alexjiaguo/economist-financial-dashboard.git
cd economist-financial-dashboard
```

2. **Install dependencies**
```bash
cd src
pip install -r requirements.txt
```

3. **Set up API key**
```bash
export TWELVEDATA_API_KEY='your_api_key_here'
```

Or create a `.env` file in the `src` directory:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. **Start the dashboard**
```bash
./start.sh
```

Or directly:
```bash
python3 app.py
```

5. **Open your browser**
```
http://localhost:8080
```

## 📁 Project Structure

```
economist-financial-dashboard/
├── src/                           # Source code
│   ├── app.py                     # Main Flask application (1,200+ lines)
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── start.sh                  # Quick start script
│
├── docs/                         # Documentation
│   ├── SETUP.md                 # Detailed setup guide
│   ├── ECONOMIST_DASHBOARD_GUIDE.md  # Complete user manual
│   ├── FEATURES_QUICK_REFERENCE.md   # Feature lookup
│   ├── REAL_DATA_UPDATE.md      # Real data implementation details
│   ├── NEW_FEATURES_SUMMARY.md  # All features explained
│   ├── QUICK_START.md           # 5-minute setup
│   └── ...                      # Additional guides
│
├── scripts/                      # Helper scripts
│   ├── push_to_github.sh        # GitHub deployment
│   └── ...                      # Other utilities
│
├── old_versions/                 # Previous iterations (archived)
│
├── README.md                    # This file
├── LICENSE                      # MIT License
└── .gitignore                   # Git ignore rules
```

## 🎯 How to Use

1. **Select Asset Type**: Choose from Currencies, Stocks, Crypto, Indices, or Metals
2. **Pick an Asset**: Select from the dropdown (e.g., USD/CNY, AAPL, BTC/USD)
3. **View Real-Time Data**:
   - Current price and 24h change
   - 60-day historical chart
   - 30-day forecast
   - Technical analysis
4. **Check Economic Indicators**: Hover over indicators to see tooltips with definitions
5. **Refresh**: Auto-refreshes hourly, or use "Refresh Now" button (1-min cooldown)

## 📊 Economic Indicators Tracked

### Global Economy
- 🏛️ **Federal Reserve Rate**: Impact on USD and markets
- 📈 **US Inflation (CPI)**: Consumer price changes
- 👥 **US Unemployment**: Labor market health
- 💰 **US GDP Growth**: Economic expansion rate

### Market Sentiment
- 📉 **VIX Index**: Market volatility and fear gauge
- 🛍️ **Consumer Confidence**: Spending optimism
- 💵 **US Dollar Index**: USD strength vs basket
- 📊 **Treasury Yields**: 2-year and 10-year bonds

### Regional (China-specific for CNY)
- 🏭 **China GDP**: Economic growth
- 🏢 **China PMI**: Manufacturing health
- 🚢 **Trade Balance**: Export/import dynamics

### European (EUR-specific)
- 🏦 **ECB Rate**: European Central Bank policy
- 📊 **EU Inflation**: Eurozone price changes
- 🏭 **EU PMI**: Manufacturing activity

## 🔧 Technical Details

### Tech Stack
- **Backend**: Python 3.9+, Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js 3.9+
- **Data Source**: Twelve Data API
- **Algorithms**: NumPy, scikit-learn

### Forecasting Algorithm
1. **Linear Regression**: Trend identification
2. **Mean Reversion**: Long-term average pull
3. **Random Walk**: Uncertainty modeling with sqrt(time) scaling
4. **Constraints**: Max 30% change to prevent unrealistic predictions

### API Rate Limits
- **Free Tier**: 800 requests/day
- **Dashboard Usage**: ~336 requests/day (hourly refresh for 14 assets)
- **Buffer**: 464 requests for manual refreshes

## 📚 Documentation

Comprehensive guides in the `docs/` folder:

- **[Setup Guide](docs/SETUP.md)**: Installation and troubleshooting
- **[User Manual](docs/ECONOMIST_DASHBOARD_GUIDE.md)**: Complete feature walkthrough
- **[Feature Reference](docs/FEATURES_QUICK_REFERENCE.md)**: Quick lookup
- **[Real Data Details](docs/REAL_DATA_UPDATE.md)**: How real data is fetched
- **[Success Guide](docs/SUCCESS.md)**: Post-setup tips

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8080
lsof -ti:8080 | xargs kill -9
```

### API Key Not Set
```bash
export TWELVEDATA_API_KEY='your_key_here'
```

### Dependencies Missing
```bash
cd src
pip install -r requirements.txt
```

### Python Version
```bash
python3 --version  # Should be 3.9 or higher
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Twelve Data** for providing the financial data API
- **The Economist** for design inspiration
- **Chart.js** for beautiful interactive charts
- **Flask** for the web framework

## 📧 Contact

**Alex Guo** - [@alexjiaguo](https://github.com/alexjiaguo)

**Project Link**: [https://github.com/alexjiaguo/economist-financial-dashboard](https://github.com/alexjiaguo/economist-financial-dashboard)

---

## 🎯 API Key Setup

Get your free Twelve Data API key:

1. Go to [https://twelvedata.com/](https://twelvedata.com/)
2. Sign up for free account
3. Navigate to API dashboard
4. Copy your API key
5. Set environment variable:
   ```bash
   export TWELVEDATA_API_KEY='your_key_here'
   ```

Free tier includes:
- ✅ 800 API requests per day
- ✅ Real-time data
- ✅ Historical data
- ✅ Technical indicators
- ✅ No credit card required

---

## ⭐ Star This Repository

If you find this project useful, please consider giving it a star! It helps others discover the project.

[![GitHub stars](https://img.shields.io/github/stars/alexjiaguo/economist-financial-dashboard?style=social)](https://github.com/alexjiaguo/economist-financial-dashboard/stargazers)

---

**Built with ❤️ by Alex Guo**
