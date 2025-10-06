#!/usr/bin/env python3
"""
Chinese Yuan (CNY) to USD Exchange Rate Analysis and Prediction
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

class CNYUSDAnalyzer:
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
    
    def create_predictions(self, days_ahead=30):
        """Create simple predictions using linear and polynomial regression"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return None
            
        print(f"\n🔮 CREATING PREDICTIONS ({days_ahead} days ahead)")
        print("=" * 50)
        
        # Use last 2 years of data for prediction
        prediction_data = self.data.tail(500).copy()
        prediction_data = prediction_data.dropna()
        
        # Prepare features (time-based)
        X = np.arange(len(prediction_data)).reshape(-1, 1)
        y = prediction_data['Close'].values
        
        # Linear regression
        lr_model = LinearRegression()
        lr_model.fit(X, y)
        lr_predictions = lr_model.predict(X)
        lr_future = lr_model.predict(np.arange(len(prediction_data), len(prediction_data) + days_ahead).reshape(-1, 1))
        
        # Polynomial regression (degree 2)
        poly_features = PolynomialFeatures(degree=2)
        X_poly = poly_features.fit_transform(X)
        poly_model = LinearRegression()
        poly_model.fit(X_poly, y)
        poly_predictions = poly_model.predict(X_poly)
        poly_future = poly_model.predict(poly_features.transform(np.arange(len(prediction_data), len(prediction_data) + days_ahead).reshape(-1, 1)))
        
        # Calculate model performance
        lr_r2 = r2_score(y, lr_predictions)
        poly_r2 = r2_score(y, poly_predictions)
        
        print(f"📊 MODEL PERFORMANCE:")
        print(f"Linear Regression R²: {lr_r2:.4f}")
        print(f"Polynomial Regression R²: {poly_r2:.4f}")
        
        # Future predictions
        current_rate = y[-1]
        lr_final_pred = lr_future[-1]
        poly_final_pred = poly_future[-1]
        
        lr_change = ((lr_final_pred - current_rate) / current_rate) * 100
        poly_change = ((poly_final_pred - current_rate) / current_rate) * 100
        
        print(f"\n🎯 PREDICTIONS ({days_ahead} days ahead):")
        print(f"Current Rate: {current_rate:.4f}")
        print(f"Linear Model: {lr_final_pred:.4f} ({lr_change:+.2f}%)")
        print(f"Polynomial Model: {poly_final_pred:.4f} ({poly_change:+.2f}%)")
        
        # Average prediction
        avg_pred = (lr_final_pred + poly_final_pred) / 2
        avg_change = ((avg_pred - current_rate) / current_rate) * 100
        print(f"Average Prediction: {avg_pred:.4f} ({avg_change:+.2f}%)")
        
        return {
            'current_rate': current_rate,
            'linear_prediction': lr_final_pred,
            'polynomial_prediction': poly_final_pred,
            'average_prediction': avg_pred,
            'linear_change_pct': lr_change,
            'polynomial_change_pct': poly_change,
            'average_change_pct': avg_change,
            'linear_r2': lr_r2,
            'polynomial_r2': poly_r2
        }
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return
            
        print("\n📊 CREATING VISUALIZATIONS")
        print("=" * 50)
        
        # Set up the plot
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('CNY/USD Exchange Rate Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Price chart with moving averages
        ax1 = axes[0, 0]
        recent_data = self.data.tail(252)  # Last year
        
        ax1.plot(recent_data.index, recent_data['Close'], label='CNY/USD Rate', linewidth=2, color='#2E86AB')
        ax1.plot(recent_data.index, recent_data['MA_20'], label='20-day MA', alpha=0.7, color='#A23B72')
        ax1.plot(recent_data.index, recent_data['MA_50'], label='50-day MA', alpha=0.7, color='#F18F01')
        ax1.plot(recent_data.index, recent_data['MA_200'], label='200-day MA', alpha=0.7, color='#C73E1D')
        
        ax1.set_title('CNY/USD Exchange Rate with Moving Averages', fontweight='bold')
        ax1.set_ylabel('CNY per USD')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Daily changes
        ax2 = axes[0, 1]
        daily_changes = recent_data['Daily_Change'].dropna()
        ax2.hist(daily_changes, bins=50, alpha=0.7, color='#2E86AB', edgecolor='black')
        ax2.axvline(daily_changes.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {daily_changes.mean():.2f}%')
        ax2.axvline(daily_changes.median(), color='orange', linestyle='--', linewidth=2, label=f'Median: {daily_changes.median():.2f}%')
        
        ax2.set_title('Distribution of Daily Changes', fontweight='bold')
        ax2.set_xlabel('Daily Change (%)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Volatility over time
        ax3 = axes[1, 0]
        volatility_data = recent_data['Volatility'].dropna()
        ax3.plot(volatility_data.index, volatility_data, color='#A23B72', linewidth=2)
        ax3.fill_between(volatility_data.index, volatility_data, alpha=0.3, color='#A23B72')
        
        ax3.set_title('20-Day Rolling Volatility', fontweight='bold')
        ax3.set_ylabel('Volatility (%)')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Monthly performance
        ax4 = axes[1, 1]
        monthly_data = recent_data.resample('M').agg({
            'Close': 'last',
            'High': 'max',
            'Low': 'min'
        })
        
        monthly_returns = monthly_data['Close'].pct_change() * 100
        colors = ['green' if x > 0 else 'red' for x in monthly_returns]
        
        bars = ax4.bar(range(len(monthly_returns)), monthly_returns, color=colors, alpha=0.7)
        ax4.set_title('Monthly Returns', fontweight='bold')
        ax4.set_ylabel('Monthly Return (%)')
        ax4.set_xlabel('Month')
        ax4.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + (0.1 if height > 0 else -0.3),
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('/Users/boss/Documents/cursor/placeholder/cny_usd_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Visualization saved as 'cny_usd_analysis.png'")
        plt.show()
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return
            
        print("\n📋 GENERATING COMPREHENSIVE REPORT")
        print("=" * 60)
        
        # Get current rate
        current_rate, last_updated = self.get_current_rate()
        
        # Analyze trends
        trend_analysis = self.analyze_trends()
        
        # Create predictions
        predictions = self.create_predictions()
        
        # Handle case where current rate fetch failed
        if current_rate is None:
            current_rate = trend_analysis['current_rate']
            last_updated = "From historical data"
        
        # Generate report
        report = f"""
# CNY/USD Exchange Rate Analysis Report
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

## 🔮 30-Day Predictions
- **Current Rate**: {predictions['current_rate']:.4f}
- **Linear Model**: {predictions['linear_prediction']:.4f} ({predictions['linear_change_pct']:+.2f}%)
- **Polynomial Model**: {predictions['polynomial_prediction']:.4f} ({predictions['polynomial_change_pct']:+.2f}%)
- **Average Prediction**: {predictions['average_prediction']:.4f} ({predictions['average_change_pct']:+.2f}%)

## 📊 Model Performance
- **Linear Regression R²**: {predictions['linear_r2']:.4f}
- **Polynomial Regression R²**: {predictions['polynomial_r2']:.4f}

## 🎯 Key Insights
"""
        
        # Add insights based on analysis
        if trend_analysis['yearly_change'] > 0:
            report += "- CNY has weakened against USD over the past year\n"
        else:
            report += "- CNY has strengthened against USD over the past year\n"
            
        if trend_analysis['volatility'] > 1.0:
            report += "- High volatility indicates significant market uncertainty\n"
        else:
            report += "- Moderate volatility suggests relatively stable conditions\n"
            
        if predictions['average_change_pct'] > 0:
            report += "- Models predict CNY weakening against USD in the next 30 days\n"
        else:
            report += "- Models predict CNY strengthening against USD in the next 30 days\n"
            
        report += f"""
## ⚠️ Risk Factors
- Exchange rate predictions are inherently uncertain
- Economic policies, trade relations, and global events can significantly impact rates
- Past performance does not guarantee future results
- Consider consulting with financial professionals for investment decisions

## 📚 Methodology
- Data source: Alpha Vantage API
- Analysis period: Last 2 years of daily data
- Prediction models: Linear and Polynomial Regression
- Moving averages: 20, 50, and 200-day periods
- Volatility calculation: 20-day rolling standard deviation

---
*This analysis is for informational purposes only and should not be considered as financial advice.*
"""
        
        # Save report
        with open('/Users/boss/Documents/cursor/placeholder/cny_usd_report.md', 'w') as f:
            f.write(report)
            
        print("✅ Report saved as 'cny_usd_report.md'")
        print("\n" + "="*60)
        print(report)

def main():
    """Main function to run the analysis"""
    print("🇨🇳 CNY/USD Exchange Rate Analysis & Prediction")
    print("=" * 60)
    
    # Get API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ Alpha Vantage API key not found!")
        print("Please set the ALPHAVANTAGE_API_KEY environment variable")
        return
    
    # Initialize analyzer
    analyzer = CNYUSDAnalyzer(api_key)
    
    # Fetch data
    data = analyzer.fetch_exchange_rate_data()
    if data is None:
        return
    
    # Run analysis
    analyzer.analyze_trends()
    analyzer.create_predictions()
    analyzer.create_visualizations()
    analyzer.generate_report()
    
    print("\n🎉 Analysis complete! Check the generated files:")
    print("- cny_usd_analysis.png (visualizations)")
    print("- cny_usd_report.md (comprehensive report)")

if __name__ == "__main__":
    main()
