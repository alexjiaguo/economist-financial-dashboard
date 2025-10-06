#!/usr/bin/env python3
"""
Extended CNY/USD Analysis with Longer-term Predictions and Fed Rate Impact
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ExtendedCNYUSDAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.data = None
        
    def fetch_exchange_rate_data(self, symbol="USDCNY", outputsize="full"):
        """Fetch historical CNY/USD exchange rate data from Alpha Vantage"""
        print("🔄 Fetching CNY/USD exchange rate data from Alpha Vantage...")
        
        params = {
            'function': 'FX_DAILY',
            'from_symbol': 'USD',
            'to_symbol': 'CNY',
            'outputsize': outputsize,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Error Message' in data:
                raise Exception(f"API Error: {data['Error Message']}")
            if 'Note' in data:
                raise Exception(f"API Limit: {data['Note']}")
            if 'Information' in data:
                raise Exception(f"API Info: {data['Information']}")
                
            # Extract time series data
            time_series = data.get('Time Series FX (Daily)', {})
            if not time_series:
                raise Exception("No time series data found")
                
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Rename columns (API returns numbered keys)
            df.columns = ['Open', 'High', 'Low', 'Close']
            df = df.astype(float)
            
            # Calculate additional metrics
            df['Daily_Change'] = df['Close'].pct_change() * 100
            df['Volatility'] = df['Daily_Change'].rolling(window=20).std()
            df['MA_20'] = df['Close'].rolling(window=20).mean()
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['MA_200'] = df['Close'].rolling(window=200).mean()
            
            self.data = df
            print(f"✅ Successfully fetched {len(df)} days of data")
            print(f"📅 Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching data: {str(e)}")
            return None
    
    def create_extended_predictions(self):
        """Create predictions for 30, 60, 90, and 120 days ahead"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return None
            
        print(f"\n🔮 CREATING EXTENDED PREDICTIONS (30, 60, 90, 120 days)")
        print("=" * 60)
        
        # Use last 2 years of data for prediction
        prediction_data = self.data.tail(500).copy()
        prediction_data = prediction_data.dropna()
        
        # Prepare features (time-based)
        X = np.arange(len(prediction_data)).reshape(-1, 1)
        y = prediction_data['Close'].values
        
        # Linear regression
        lr_model = LinearRegression()
        lr_model.fit(X, y)
        
        # Polynomial regression (degree 2)
        poly_features = PolynomialFeatures(degree=2)
        X_poly = poly_features.fit_transform(X)
        poly_model = LinearRegression()
        poly_model.fit(X_poly, y)
        
        # Calculate model performance
        lr_predictions = lr_model.predict(X)
        poly_predictions = poly_model.predict(X_poly)
        lr_r2 = r2_score(y, lr_predictions)
        poly_r2 = r2_score(y, poly_predictions)
        
        print(f"📊 MODEL PERFORMANCE:")
        print(f"Linear Regression R²: {lr_r2:.4f}")
        print(f"Polynomial Regression R²: {poly_r2:.4f}")
        
        # Predictions for different timeframes
        timeframes = [30, 60, 90, 120]
        current_rate = y[-1]
        
        predictions = {}
        
        print(f"\n🎯 EXTENDED PREDICTIONS:")
        print(f"Current Rate: {current_rate:.4f} CNY per USD")
        print("-" * 60)
        
        for days in timeframes:
            # Linear prediction
            lr_future = lr_model.predict(np.arange(len(prediction_data), len(prediction_data) + days).reshape(-1, 1))
            lr_final_pred = lr_future[-1]
            
            # Polynomial prediction
            poly_future = poly_model.predict(poly_features.transform(np.arange(len(prediction_data), len(prediction_data) + days).reshape(-1, 1)))
            poly_final_pred = poly_future[-1]
            
            # Average prediction
            avg_pred = (lr_final_pred + poly_final_pred) / 2
            
            # Calculate changes
            lr_change = ((lr_final_pred - current_rate) / current_rate) * 100
            poly_change = ((poly_final_pred - current_rate) / current_rate) * 100
            avg_change = ((avg_pred - current_rate) / current_rate) * 100
            
            predictions[days] = {
                'linear_prediction': lr_final_pred,
                'polynomial_prediction': poly_final_pred,
                'average_prediction': avg_pred,
                'linear_change_pct': lr_change,
                'polynomial_change_pct': poly_change,
                'average_change_pct': avg_change
            }
            
            print(f"📅 {days} Days Ahead:")
            print(f"   Linear Model: {lr_final_pred:.4f} ({lr_change:+.2f}%)")
            print(f"   Polynomial Model: {poly_final_pred:.4f} ({poly_change:+.2f}%)")
            print(f"   Average Prediction: {avg_pred:.4f} ({avg_change:+.2f}%)")
            print()
        
        return predictions
    
    def analyze_fed_rate_impact(self):
        """Analyze the potential impact of Federal Reserve interest rate cuts"""
        print("\n🏦 FEDERAL RESERVE INTEREST RATE IMPACT ANALYSIS")
        print("=" * 60)
        
        # Historical context and theoretical impact
        fed_impact_analysis = {
            'rate_cut_impact': {
                'usd_weakening': {
                    'description': 'Fed rate cuts typically weaken USD',
                    'mechanism': 'Lower US interest rates reduce USD attractiveness to foreign investors',
                    'historical_precedent': 'Fed rate cuts in 2019-2020 led to USD weakening against major currencies',
                    'cny_usd_impact': 'USD weakening = CNY strengthening = Lower CNY/USD rate'
                },
                'capital_flows': {
                    'description': 'Rate cuts affect capital flows between US and China',
                    'mechanism': 'Lower US rates may reduce capital outflow from China to US',
                    'cny_support': 'Reduced capital outflow supports CNY strength'
                },
                'trade_balance': {
                    'description': 'Rate cuts affect trade competitiveness',
                    'mechanism': 'Weaker USD makes US exports more competitive, Chinese imports more expensive',
                    'cny_pressure': 'Could put upward pressure on CNY/USD rate'
                }
            },
            'current_context': {
                'fed_policy': 'Federal Reserve has been in a tightening cycle, but may pivot to cuts',
                'china_policy': 'People\'s Bank of China maintains relatively loose monetary policy',
                'rate_differential': 'US rates higher than China rates creates USD strength pressure'
            },
            'scenarios': {
                'aggressive_cuts': {
                    'description': 'Fed cuts rates by 100-150 basis points',
                    'cny_usd_impact': 'Significant USD weakening, CNY/USD could drop to 6.8-7.0 range',
                    'probability': 'Medium (if recession concerns increase)'
                },
                'moderate_cuts': {
                    'description': 'Fed cuts rates by 50-75 basis points',
                    'cny_usd_impact': 'Moderate USD weakening, CNY/USD could drop to 7.0-7.1 range',
                    'probability': 'High (most likely scenario)'
                },
                'no_cuts': {
                    'description': 'Fed maintains current rates or continues tightening',
                    'cny_usd_impact': 'USD strength continues, CNY/USD could rise to 7.2-7.4 range',
                    'probability': 'Low (given current economic conditions)'
                }
            }
        }
        
        print("📊 THEORETICAL IMPACT OF FED RATE CUTS:")
        print()
        
        for category, details in fed_impact_analysis.items():
            if category == 'rate_cut_impact':
                print("🔍 MECHANISMS:")
                for mechanism, info in details.items():
                    print(f"   • {info['description']}")
                    print(f"     {info['mechanism']}")
                    if 'cny_usd_impact' in info:
                        print(f"     → CNY/USD Impact: {info['cny_usd_impact']}")
                    print()
            
            elif category == 'current_context':
                print("🌍 CURRENT CONTEXT:")
                for key, value in details.items():
                    print(f"   • {key.replace('_', ' ').title()}: {value}")
                print()
            
            elif category == 'scenarios':
                print("🎯 SCENARIO ANALYSIS:")
                for scenario, details in details.items():
                    print(f"   📈 {scenario.replace('_', ' ').title()}:")
                    print(f"      Description: {details['description']}")
                    print(f"      CNY/USD Impact: {details['cny_usd_impact']}")
                    print(f"      Probability: {details['probability']}")
                    print()
        
        return fed_impact_analysis
    
    def create_comprehensive_report(self):
        """Generate comprehensive report with extended analysis"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return
            
        print("\n📋 GENERATING COMPREHENSIVE EXTENDED REPORT")
        print("=" * 70)
        
        # Get current rate
        current_rate, last_updated = self.get_current_rate()
        if current_rate is None:
            current_rate = self.data['Close'].iloc[-1]
            last_updated = "From historical data"
        
        # Analyze trends
        trend_analysis = self.analyze_trends()
        
        # Create extended predictions
        predictions = self.create_extended_predictions()
        
        # Analyze Fed impact
        fed_analysis = self.analyze_fed_rate_impact()
        
        # Generate comprehensive report
        report = f"""
# Extended CNY/USD Exchange Rate Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Current Market Status
- **Current Rate**: {current_rate:.4f} CNY per USD
- **Last Updated**: {last_updated}
- **52-Week High**: {trend_analysis['high_52w']:.4f}
- **52-Week Low**: {trend_analysis['low_52w']:.4f}
- **Current Trend**: {trend_analysis['trend']}

## 📈 Performance Metrics
- **1-Year Change**: {trend_analysis['yearly_change']:+.2f}%
- **Daily Volatility**: {trend_analysis['volatility']:.2f}%
- **20-Day MA**: {trend_analysis['ma_20']:.4f}
- **50-Day MA**: {trend_analysis['ma_50']:.4f}
- **200-Day MA**: {trend_analysis['ma_200']:.4f}

## 🔮 Extended Predictions (30, 60, 90, 120 Days)
"""
        
        for days, pred in predictions.items():
            report += f"""
### {days} Days Ahead
- **Linear Model**: {pred['linear_prediction']:.4f} ({pred['linear_change_pct']:+.2f}%)
- **Polynomial Model**: {pred['polynomial_prediction']:.4f} ({pred['polynomial_change_pct']:+.2f}%)
- **Average Prediction**: {pred['average_prediction']:.4f} ({pred['average_change_pct']:+.2f}%)

**Impact on 100,000 CNY:**
- **Today**: 100,000 ÷ {current_rate:.4f} = **{100000/current_rate:.2f} USD**
- **In {days} days**: 100,000 ÷ {pred['average_prediction']:.4f} = **{100000/pred['average_prediction']:.2f} USD**
- **Difference**: **{100000/current_rate - 100000/pred['average_prediction']:+.2f} USD**
"""
        
        report += f"""

## 🏦 Federal Reserve Interest Rate Impact Analysis

### 📊 Theoretical Impact of Fed Rate Cuts

**Primary Mechanisms:**
1. **USD Weakening**: Fed rate cuts typically weaken USD as lower interest rates reduce USD attractiveness
2. **Capital Flows**: Lower US rates may reduce capital outflow from China to US, supporting CNY
3. **Trade Balance**: Weaker USD affects trade competitiveness between US and China

### 🎯 Scenario Analysis

**🟢 Aggressive Cuts (100-150 bps):**
- **Impact**: Significant USD weakening
- **CNY/USD Range**: 6.8 - 7.0
- **Probability**: Medium
- **Your Strategy**: Wait for rate cuts, CNY will strengthen significantly

**🟡 Moderate Cuts (50-75 bps):**
- **Impact**: Moderate USD weakening  
- **CNY/USD Range**: 7.0 - 7.1
- **Probability**: High
- **Your Strategy**: Consider waiting 2-3 months for better rates

**🔴 No Cuts/Continued Tightening:**
- **Impact**: USD strength continues
- **CNY/USD Range**: 7.2 - 7.4
- **Probability**: Low
- **Your Strategy**: Sell CNY now, rates will get worse

## 🎯 Strategic Recommendations

### **Immediate Action (Next 30 Days)**
"""
        
        # Add strategic recommendations based on analysis
        avg_30d_change = predictions[30]['average_change_pct']
        if avg_30d_change > 0:
            report += "- **SELL CNY NOW** - Models predict CNY weakening (rate increasing)\n"
            report += "- **Don't wait** - You'll get less USD for your CNY\n"
        else:
            report += "- **CONSIDER WAITING** - Models predict CNY strengthening (rate decreasing)\n"
            report += "- **Monitor Fed signals** - Rate cuts could accelerate CNY strength\n"
        
        report += f"""
### **Medium-term Strategy (60-120 Days)**
- **Monitor Fed policy signals** closely
- **Watch for rate cut announcements** - these will significantly impact CNY/USD
- **Consider dollar-cost averaging** if you have large amounts to convert
- **Set target levels**: 
  - If CNY/USD drops below 7.0 → Strong buy signal for CNY
  - If CNY/USD rises above 7.3 → Strong sell signal for CNY

### **Key Risk Factors**
- **Fed policy uncertainty** - Rate decisions can cause sudden moves
- **US-China trade tensions** - Can override interest rate effects
- **Chinese economic data** - PBOC policy responses
- **Global risk sentiment** - Safe-haven flows to USD

## 📚 Methodology
- **Data Source**: Alpha Vantage API (5,000+ days of historical data)
- **Prediction Models**: Linear and Polynomial Regression
- **Analysis Period**: Last 2 years of daily data
- **Technical Indicators**: 20, 50, 200-day moving averages
- **Volatility**: 20-day rolling standard deviation

---
*This analysis is for informational purposes only and should not be considered as financial advice. Always consult with financial professionals for investment decisions.*
"""
        
        # Save report
        with open('/Users/boss/Documents/cursor/placeholder/extended_cny_usd_report.md', 'w') as f:
            f.write(report)
            
        print("✅ Extended report saved as 'extended_cny_usd_report.md'")
        print("\n" + "="*70)
        print(report)
    
    def get_current_rate(self):
        """Get current CNY/USD exchange rate"""
        print("🔄 Fetching current CNY/USD exchange rate...")
        
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': 'USD',
            'to_currency': 'CNY',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Realtime Currency Exchange Rate' in data:
                rate_data = data['Realtime Currency Exchange Rate']
                current_rate = float(rate_data['5. Exchange Rate'])
                last_refreshed = rate_data['6. Last Refreshed']
                print(f"✅ Current CNY/USD Rate: {current_rate:.4f}")
                print(f"🕐 Last Updated: {last_refreshed}")
                return current_rate, last_refreshed
            else:
                raise Exception("No exchange rate data found")
                
        except Exception as e:
            print(f"❌ Error fetching current rate: {str(e)}")
            return None, None
    
    def analyze_trends(self):
        """Analyze historical trends and patterns"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return None
            
        print("\n📊 ANALYZING CNY/USD TRENDS")
        print("=" * 50)
        
        # Basic statistics
        recent_data = self.data.tail(252)  # Last year
        current_rate = recent_data['Close'].iloc[-1]
        year_ago_rate = recent_data['Close'].iloc[0]
        yearly_change = ((current_rate - year_ago_rate) / year_ago_rate) * 100
        
        print(f"📈 Current Rate: {current_rate:.4f} CNY per USD")
        print(f"📅 1 Year Ago: {year_ago_rate:.4f} CNY per USD")
        print(f"📊 Yearly Change: {yearly_change:+.2f}%")
        
        # Volatility analysis
        volatility = recent_data['Daily_Change'].std()
        print(f"📉 Daily Volatility: {volatility:.2f}%")
        
        # Trend analysis
        ma_20_current = recent_data['MA_20'].iloc[-1]
        ma_50_current = recent_data['MA_50'].iloc[-1]
        ma_200_current = recent_data['MA_200'].iloc[-1]
        
        print(f"\n📈 MOVING AVERAGES:")
        print(f"20-day MA: {ma_20_current:.4f}")
        print(f"50-day MA: {ma_50_current:.4f}")
        print(f"200-day MA: {ma_200_current:.4f}")
        
        # Trend direction
        if current_rate > ma_20_current > ma_50_current:
            trend = "Strong Uptrend"
        elif current_rate < ma_20_current < ma_50_current:
            trend = "Strong Downtrend"
        elif current_rate > ma_20_current:
            trend = "Short-term Uptrend"
        elif current_rate < ma_20_current:
            trend = "Short-term Downtrend"
        else:
            trend = "Sideways/Consolidation"
            
        print(f"🎯 Current Trend: {trend}")
        
        # Support and resistance levels
        high_52w = recent_data['High'].max()
        low_52w = recent_data['Low'].min()
        print(f"\n📊 52-WEEK RANGE:")
        print(f"High: {high_52w:.4f}")
        print(f"Low: {low_52w:.4f}")
        print(f"Range: {((high_52w - low_52w) / low_52w * 100):.2f}%")
        
        return {
            'current_rate': current_rate,
            'yearly_change': yearly_change,
            'volatility': volatility,
            'trend': trend,
            'ma_20': ma_20_current,
            'ma_50': ma_50_current,
            'ma_200': ma_200_current,
            'high_52w': high_52w,
            'low_52w': low_52w
        }

def main():
    """Main function to run the extended analysis"""
    print("🇨🇳 Extended CNY/USD Exchange Rate Analysis & Fed Impact Study")
    print("=" * 70)
    
    # Get API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ Alpha Vantage API key not found!")
        print("Please set the ALPHAVANTAGE_API_KEY environment variable")
        return
    
    # Initialize analyzer
    analyzer = ExtendedCNYUSDAnalyzer(api_key)
    
    # Fetch data
    data = analyzer.fetch_exchange_rate_data()
    if data is None:
        return
    
    # Run extended analysis
    analyzer.analyze_trends()
    analyzer.create_extended_predictions()
    analyzer.analyze_fed_rate_impact()
    analyzer.create_comprehensive_report()
    
    print("\n🎉 Extended analysis complete! Check the generated files:")
    print("- extended_cny_usd_report.md (comprehensive extended report)")

if __name__ == "__main__":
    main()
