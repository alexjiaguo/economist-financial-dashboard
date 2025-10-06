#!/usr/bin/env python3
"""
Tesla Stock Price Prediction Analysis Across Multiple Time Windows
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
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TeslaStockPredictor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.data = None
        self.symbol = "TSLA"
        
    def fetch_tesla_data(self, outputsize="full"):
        """Fetch historical Tesla stock data from Alpha Vantage"""
        print("🔄 Fetching Tesla (TSLA) stock data from Alpha Vantage...")
        
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.symbol,
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
            time_series = data.get('Time Series (Daily)', {})
            if not time_series:
                raise Exception("No time series data found")
                
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Rename columns (API returns numbered keys)
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype(float)
            
            # Calculate additional technical indicators
            df['Daily_Return'] = df['Close'].pct_change()
            df['Daily_Change'] = df['Daily_Return'] * 100
            df['Volatility'] = df['Daily_Return'].rolling(window=20).std() * np.sqrt(252) * 100
            df['MA_5'] = df['Close'].rolling(window=5).mean()
            df['MA_10'] = df['Close'].rolling(window=10).mean()
            df['MA_20'] = df['Close'].rolling(window=20).mean()
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['MA_200'] = df['Close'].rolling(window=200).mean()
            
            # RSI calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD calculation
            exp1 = df['Close'].ewm(span=12).mean()
            exp2 = df['Close'].ewm(span=26).mean()
            df['MACD'] = exp1 - exp2
            df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
            
            # Bollinger Bands
            df['BB_Middle'] = df['Close'].rolling(window=20).mean()
            bb_std = df['Close'].rolling(window=20).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle'] * 100
            
            self.data = df
            print(f"✅ Successfully fetched {len(df)} days of Tesla data")
            print(f"📅 Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching Tesla data: {str(e)}")
            return None
    
    def get_current_price(self):
        """Get current Tesla stock price"""
        print("🔄 Fetching current Tesla stock price...")
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': self.symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                current_price = float(quote['05. price'])
                change = float(quote['09. change'])
                change_percent = float(quote['10. change percent'].replace('%', ''))
                volume = int(quote['06. volume'])
                last_refreshed = quote['07. latest trading day']
                
                print(f"✅ Current Tesla Price: ${current_price:.2f}")
                print(f"📊 Change: ${change:+.2f} ({change_percent:+.2f}%)")
                print(f"📈 Volume: {volume:,} shares")
                print(f"🕐 Last Updated: {last_refreshed}")
                
                return {
                    'price': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'volume': volume,
                    'last_refreshed': last_refreshed
                }
            else:
                raise Exception("No quote data found")
                
        except Exception as e:
            print(f"❌ Error fetching current price: {str(e)}")
            return None
    
    def analyze_current_trends(self):
        """Analyze current Tesla stock trends and technical indicators"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return None
            
        print("\n📊 ANALYZING TESLA STOCK TRENDS")
        print("=" * 50)
        
        # Get current data
        current_data = self.data.tail(252)  # Last year
        current_price = current_data['Close'].iloc[-1]
        year_ago_price = current_data['Close'].iloc[0]
        yearly_return = ((current_price - year_ago_price) / year_ago_price) * 100
        
        print(f"📈 Current Price: ${current_price:.2f}")
        print(f"📅 1 Year Ago: ${year_ago_price:.2f}")
        print(f"📊 1-Year Return: {yearly_return:+.2f}%")
        
        # Volatility analysis
        volatility = current_data['Volatility'].iloc[-1]
        print(f"📉 Annualized Volatility: {volatility:.2f}%")
        
        # Moving averages
        ma_5 = current_data['MA_5'].iloc[-1]
        ma_10 = current_data['MA_10'].iloc[-1]
        ma_20 = current_data['MA_20'].iloc[-1]
        ma_50 = current_data['MA_50'].iloc[-1]
        ma_200 = current_data['MA_200'].iloc[-1]
        
        print(f"\n📈 MOVING AVERAGES:")
        print(f"5-day MA: ${ma_5:.2f}")
        print(f"10-day MA: ${ma_10:.2f}")
        print(f"20-day MA: ${ma_20:.2f}")
        print(f"50-day MA: ${ma_50:.2f}")
        print(f"200-day MA: ${ma_200:.2f}")
        
        # Technical indicators
        rsi = current_data['RSI'].iloc[-1]
        macd = current_data['MACD'].iloc[-1]
        macd_signal = current_data['MACD_Signal'].iloc[-1]
        
        print(f"\n🔍 TECHNICAL INDICATORS:")
        print(f"RSI (14): {rsi:.2f}")
        print(f"MACD: {macd:.4f}")
        print(f"MACD Signal: {macd_signal:.4f}")
        
        # Trend analysis
        if current_price > ma_20 > ma_50:
            trend = "Strong Uptrend"
        elif current_price < ma_20 < ma_50:
            trend = "Strong Downtrend"
        elif current_price > ma_20:
            trend = "Short-term Uptrend"
        elif current_price < ma_20:
            trend = "Short-term Downtrend"
        else:
            trend = "Sideways/Consolidation"
            
        print(f"🎯 Current Trend: {trend}")
        
        # Support and resistance
        high_52w = current_data['High'].max()
        low_52w = current_data['Low'].min()
        print(f"\n📊 52-WEEK RANGE:")
        print(f"High: ${high_52w:.2f}")
        print(f"Low: ${low_52w:.2f}")
        print(f"Range: {((high_52w - low_52w) / low_52w * 100):.2f}%")
        
        return {
            'current_price': current_price,
            'yearly_return': yearly_return,
            'volatility': volatility,
            'trend': trend,
            'ma_5': ma_5,
            'ma_10': ma_10,
            'ma_20': ma_20,
            'ma_50': ma_50,
            'ma_200': ma_200,
            'rsi': rsi,
            'macd': macd,
            'macd_signal': macd_signal,
            'high_52w': high_52w,
            'low_52w': low_52w
        }
    
    def create_predictions(self, time_windows=[7, 30, 90, 180, 365]):
        """Create predictions for different time windows"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return None
            
        print(f"\n🔮 CREATING TESLA PREDICTIONS FOR MULTIPLE TIME WINDOWS")
        print("=" * 60)
        
        # Use last 2 years of data for training
        training_data = self.data.tail(500).copy()
        training_data = training_data.dropna()
        
        # Prepare features
        feature_columns = ['Close', 'Volume', 'MA_5', 'MA_10', 'MA_20', 'MA_50', 'RSI', 'MACD', 'Volatility']
        X = training_data[feature_columns].values
        y = training_data['Close'].values
        
        predictions = {}
        
        for days in time_windows:
            print(f"\n📅 PREDICTING {days} DAYS AHEAD:")
            print("-" * 40)
            
            # Create time-based features for prediction
            X_time = np.arange(len(training_data)).reshape(-1, 1)
            
            # Linear regression
            lr_model = LinearRegression()
            lr_model.fit(X_time, y)
            lr_pred = lr_model.predict([[len(training_data) + days - 1]])[0]
            
            # Polynomial regression
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X_time)
            poly_model = LinearRegression()
            poly_model.fit(X_poly, y)
            poly_pred = poly_model.predict(poly_features.transform([[len(training_data) + days - 1]]))[0]
            
            # Random Forest (using technical indicators)
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X, y)
            rf_pred = rf_model.predict([X[-1]])[0]
            
            # Ensemble prediction (weighted average)
            ensemble_pred = (lr_pred * 0.3 + poly_pred * 0.3 + rf_pred * 0.4)
            
            # Calculate confidence intervals (simplified)
            current_price = y[-1]
            price_change = ensemble_pred - current_price
            price_change_pct = (price_change / current_price) * 100
            
            # Estimate confidence interval based on historical volatility
            volatility = training_data['Volatility'].iloc[-1] / 100
            confidence_interval = 1.96 * volatility * np.sqrt(days / 365) * current_price
            
            print(f"Current Price: ${current_price:.2f}")
            print(f"Linear Model: ${lr_pred:.2f} ({((lr_pred - current_price) / current_price * 100):+.2f}%)")
            print(f"Polynomial Model: ${poly_pred:.2f} ({((poly_pred - current_price) / current_price * 100):+.2f}%)")
            print(f"Random Forest: ${rf_pred:.2f} ({((rf_pred - current_price) / current_price * 100):+.2f}%)")
            print(f"Ensemble Prediction: ${ensemble_pred:.2f} ({price_change_pct:+.2f}%)")
            print(f"Confidence Interval: ±${confidence_interval:.2f}")
            
            predictions[days] = {
                'current_price': current_price,
                'linear_prediction': lr_pred,
                'polynomial_prediction': poly_pred,
                'random_forest_prediction': rf_pred,
                'ensemble_prediction': ensemble_pred,
                'price_change': price_change,
                'price_change_pct': price_change_pct,
                'confidence_interval': confidence_interval,
                'upper_bound': ensemble_pred + confidence_interval,
                'lower_bound': ensemble_pred - confidence_interval
            }
        
        return predictions
    
    def create_comprehensive_visualizations(self, predictions):
        """Create comprehensive visualizations for Tesla predictions"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return
            
        print("\n📊 CREATING COMPREHENSIVE TESLA VISUALIZATIONS")
        print("=" * 60)
        
        # Set up the plot
        fig = plt.figure(figsize=(20, 16))
        
        # Main price chart with predictions
        ax1 = plt.subplot(3, 2, 1)
        recent_data = self.data.tail(252)  # Last year
        
        ax1.plot(recent_data.index, recent_data['Close'], label='Tesla Price', linewidth=2, color='#E31937')
        ax1.plot(recent_data.index, recent_data['MA_20'], label='20-day MA', alpha=0.7, color='#FF6B35')
        ax1.plot(recent_data.index, recent_data['MA_50'], label='50-day MA', alpha=0.7, color='#F7931E')
        ax1.plot(recent_data.index, recent_data['MA_200'], label='200-day MA', alpha=0.7, color='#FFD23F')
        
        # Add prediction points
        current_date = recent_data.index[-1]
        for days, pred_data in predictions.items():
            future_date = current_date + timedelta(days=days)
            ax1.scatter(future_date, pred_data['ensemble_prediction'], 
                       s=100, alpha=0.8, label=f'{days}d: ${pred_data["ensemble_prediction"]:.0f}')
        
        ax1.set_title('Tesla Stock Price with Moving Averages & Predictions', fontweight='bold', fontsize=14)
        ax1.set_ylabel('Price ($)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Prediction comparison chart
        ax2 = plt.subplot(3, 2, 2)
        time_windows = list(predictions.keys())
        ensemble_preds = [predictions[days]['ensemble_prediction'] for days in time_windows]
        price_changes = [predictions[days]['price_change_pct'] for days in time_windows]
        
        bars = ax2.bar([f'{days}d' for days in time_windows], price_changes, 
                      color=['green' if x > 0 else 'red' for x in price_changes], alpha=0.7)
        ax2.set_title('Tesla Price Predictions by Time Window', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Expected Change (%)')
        ax2.set_xlabel('Time Window')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height > 0 else -0.5),
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=10)
        
        # RSI chart
        ax3 = plt.subplot(3, 2, 3)
        rsi_data = recent_data['RSI'].dropna()
        ax3.plot(rsi_data.index, rsi_data, color='#8E44AD', linewidth=2)
        ax3.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax3.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax3.axhline(y=50, color='gray', linestyle='-', alpha=0.5, label='Neutral (50)')
        ax3.fill_between(rsi_data.index, 30, 70, alpha=0.1, color='gray')
        ax3.set_title('RSI (Relative Strength Index)', fontweight='bold', fontsize=14)
        ax3.set_ylabel('RSI')
        ax3.set_ylim(0, 100)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # MACD chart
        ax4 = plt.subplot(3, 2, 4)
        macd_data = recent_data['MACD'].dropna()
        macd_signal_data = recent_data['MACD_Signal'].dropna()
        macd_hist_data = recent_data['MACD_Histogram'].dropna()
        
        ax4.plot(macd_data.index, macd_data, label='MACD', color='#3498DB', linewidth=2)
        ax4.plot(macd_signal_data.index, macd_signal_data, label='Signal', color='#E74C3C', linewidth=2)
        ax4.bar(macd_hist_data.index, macd_hist_data, label='Histogram', alpha=0.6, color='#95A5A6')
        ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax4.set_title('MACD (Moving Average Convergence Divergence)', fontweight='bold', fontsize=14)
        ax4.set_ylabel('MACD')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Volatility chart
        ax5 = plt.subplot(3, 2, 5)
        volatility_data = recent_data['Volatility'].dropna()
        ax5.plot(volatility_data.index, volatility_data, color='#E67E22', linewidth=2)
        ax5.fill_between(volatility_data.index, volatility_data, alpha=0.3, color='#E67E22')
        ax5.set_title('Annualized Volatility (20-day rolling)', fontweight='bold', fontsize=14)
        ax5.set_ylabel('Volatility (%)')
        ax5.grid(True, alpha=0.3)
        
        # Volume chart
        ax6 = plt.subplot(3, 2, 6)
        volume_data = recent_data['Volume'] / 1e6  # Convert to millions
        ax6.bar(recent_data.index, volume_data, alpha=0.7, color='#9B59B6')
        ax6.set_title('Trading Volume (Millions)', fontweight='bold', fontsize=14)
        ax6.set_ylabel('Volume (M)')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/boss/Documents/cursor/placeholder/tesla_stock_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Tesla visualization saved as 'tesla_stock_analysis.png'")
        plt.show()
    
    def generate_comprehensive_report(self, predictions, current_quote=None):
        """Generate comprehensive Tesla analysis report"""
        if self.data is None:
            print("❌ No data available. Please fetch data first.")
            return
            
        print("\n📋 GENERATING COMPREHENSIVE TESLA ANALYSIS REPORT")
        print("=" * 70)
        
        # Get current data
        trend_analysis = self.analyze_current_trends()
        
        # Handle current quote
        if current_quote is None:
            current_quote = self.get_current_price()
        
        # Generate report
        report = f"""
# Tesla (TSLA) Stock Price Prediction Analysis
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Current Market Status
- **Current Price**: ${trend_analysis['current_price']:.2f}
- **1-Year Return**: {trend_analysis['yearly_return']:+.2f}%
- **Annualized Volatility**: {trend_analysis['volatility']:.2f}%
- **Current Trend**: {trend_analysis['trend']}
- **52-Week High**: ${trend_analysis['high_52w']:.2f}
- **52-Week Low**: ${trend_analysis['low_52w']:.2f}

## 📈 Technical Analysis
- **RSI (14)**: {trend_analysis['rsi']:.2f}
- **MACD**: {trend_analysis['macd']:.4f}
- **MACD Signal**: {trend_analysis['macd_signal']:.4f}
- **5-day MA**: ${trend_analysis['ma_5']:.2f}
- **10-day MA**: ${trend_analysis['ma_10']:.2f}
- **20-day MA**: ${trend_analysis['ma_20']:.2f}
- **50-day MA**: ${trend_analysis['ma_50']:.2f}
- **200-day MA**: ${trend_analysis['ma_200']:.2f}

## 🔮 Multi-Time Window Predictions

"""
        
        # Add predictions for each time window
        for days, pred_data in predictions.items():
            time_label = f"{days} days" if days < 30 else f"{days//30} months" if days < 365 else f"{days//365} year"
            report += f"""
### {time_label.title()} ({days} days)
- **Current Price**: ${pred_data['current_price']:.2f}
- **Predicted Price**: ${pred_data['ensemble_prediction']:.2f}
- **Expected Change**: {pred_data['price_change_pct']:+.2f}%
- **Confidence Interval**: ±${pred_data['confidence_interval']:.2f}
- **Upper Bound**: ${pred_data['upper_bound']:.2f}
- **Lower Bound**: ${pred_data['lower_bound']:.2f}

"""
        
        # Add model breakdown
        report += f"""
## 🤖 Model Performance Breakdown

### Linear Regression Model
- Uses time-based trend analysis
- Good for identifying long-term trends
- Less sensitive to short-term volatility

### Polynomial Regression Model
- Captures non-linear price movements
- Better for cyclical patterns
- More responsive to recent changes

### Random Forest Model
- Uses technical indicators (RSI, MACD, Moving Averages)
- Captures complex market relationships
- Robust to outliers and noise

### Ensemble Prediction
- Weighted combination of all models
- Linear: 30%, Polynomial: 30%, Random Forest: 40%
- Provides balanced view of potential outcomes

## 🎯 Key Insights & Recommendations

"""
        
        # Add insights based on analysis
        current_price = trend_analysis['current_price']
        
        # Short-term insights (1 week)
        if 7 in predictions:
            short_term_change = predictions[7]['price_change_pct']
            if short_term_change > 2:
                report += "- **Short-term (1 week)**: Strong bullish momentum expected\n"
            elif short_term_change < -2:
                report += "- **Short-term (1 week)**: Bearish pressure anticipated\n"
            else:
                report += "- **Short-term (1 week)**: Sideways movement expected\n"
        
        # Medium-term insights (1-3 months)
        if 30 in predictions and 90 in predictions:
            med_term_30 = predictions[30]['price_change_pct']
            med_term_90 = predictions[90]['price_change_pct']
            if med_term_90 > med_term_30:
                report += "- **Medium-term (1-3 months)**: Accelerating upward trend expected\n"
            elif med_term_90 < med_term_30:
                report += "- **Medium-term (1-3 months)**: Momentum may be slowing\n"
            else:
                report += "- **Medium-term (1-3 months)**: Consistent trend expected\n"
        
        # Long-term insights (6-12 months)
        if 180 in predictions and 365 in predictions:
            long_term_180 = predictions[180]['price_change_pct']
            long_term_365 = predictions[365]['price_change_pct']
            if long_term_365 > 20:
                report += "- **Long-term (6-12 months)**: Strong bullish outlook\n"
            elif long_term_365 < -20:
                report += "- **Long-term (6-12 months)**: Bearish outlook\n"
            else:
                report += "- **Long-term (6-12 months)**: Moderate expectations\n"
        
        # Technical analysis insights
        if trend_analysis['rsi'] > 70:
            report += "- **RSI**: Overbought conditions - potential pullback risk\n"
        elif trend_analysis['rsi'] < 30:
            report += "- **RSI**: Oversold conditions - potential bounce opportunity\n"
        else:
            report += "- **RSI**: Neutral conditions - no extreme signals\n"
        
        if trend_analysis['macd'] > trend_analysis['macd_signal']:
            report += "- **MACD**: Bullish crossover - upward momentum\n"
        else:
            report += "- **MACD**: Bearish crossover - downward pressure\n"
        
        # Volatility insights
        if trend_analysis['volatility'] > 50:
            report += "- **Volatility**: High volatility - expect significant price swings\n"
        elif trend_analysis['volatility'] < 30:
            report += "- **Volatility**: Low volatility - relatively stable price action\n"
        else:
            report += "- **Volatility**: Moderate volatility - normal market conditions\n"
        
        report += f"""
## ⚠️ Risk Factors & Considerations

### Tesla-Specific Risks
- **EV Market Competition**: Increasing competition from traditional automakers
- **Regulatory Changes**: Government policies affecting EV adoption
- **Production Challenges**: Manufacturing and supply chain issues
- **CEO Influence**: Elon Musk's public statements and actions
- **Autonomous Driving**: Regulatory approval and technology development

### Market Risks
- **Interest Rate Changes**: Fed policy affecting growth stocks
- **Economic Conditions**: Recession or economic slowdown
- **Market Sentiment**: Risk-on vs risk-off market conditions
- **Sector Rotation**: Technology stock performance trends

### Technical Risks
- **High Volatility**: Tesla's stock is inherently volatile
- **Momentum Shifts**: Rapid changes in market sentiment
- **Support/Resistance**: Key price levels that may cause reversals

## 📚 Methodology & Data Sources

### Data Sources
- **Primary**: Alpha Vantage API (real-time and historical data)
- **Time Period**: Last 2 years of daily data
- **Update Frequency**: Real-time quotes, daily historical data

### Prediction Models
- **Linear Regression**: Time-based trend analysis
- **Polynomial Regression**: Non-linear pattern recognition
- **Random Forest**: Technical indicator-based predictions
- **Ensemble Method**: Weighted combination for balanced outlook

### Technical Indicators Used
- **Moving Averages**: 5, 10, 20, 50, 200-day periods
- **RSI**: 14-day Relative Strength Index
- **MACD**: 12, 26, 9-day Moving Average Convergence Divergence
- **Volatility**: 20-day rolling annualized volatility
- **Volume**: Trading volume analysis

### Confidence Intervals
- Based on historical volatility and time horizon
- 95% confidence level (±1.96 standard deviations)
- Accounts for increasing uncertainty over longer time periods

## 🎯 Investment Considerations

### For Short-term Traders (1-30 days)
- Monitor technical indicators closely
- Watch for momentum shifts
- Consider volatility for position sizing
- Set appropriate stop-losses

### For Medium-term Investors (1-6 months)
- Focus on fundamental developments
- Monitor EV market trends
- Consider Tesla's competitive position
- Watch for regulatory changes

### For Long-term Investors (6+ months)
- Evaluate Tesla's growth prospects
- Consider market expansion opportunities
- Monitor autonomous driving progress
- Assess competitive moat sustainability

---
*This analysis is for informational purposes only and should not be considered as financial advice. Tesla stock is highly volatile and speculative. Always consult with financial professionals and conduct your own research before making investment decisions.*
"""
        
        # Save report
        with open('/Users/boss/Documents/cursor/placeholder/tesla_stock_prediction_report.md', 'w') as f:
            f.write(report)
            
        print("✅ Tesla prediction report saved as 'tesla_stock_prediction_report.md'")
        print("\n" + "="*70)
        print(report)

def main():
    """Main function to run Tesla stock prediction analysis"""
    print("🚗 Tesla (TSLA) Stock Price Prediction Analysis")
    print("=" * 60)
    
    # Get API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ Alpha Vantage API key not found!")
        print("Please set the ALPHAVANTAGE_API_KEY environment variable")
        return
    
    # Initialize predictor
    predictor = TeslaStockPredictor(api_key)
    
    # Fetch data
    data = predictor.fetch_tesla_data()
    if data is None:
        return
    
    # Get current quote
    current_quote = predictor.get_current_price()
    
    # Create predictions for multiple time windows
    time_windows = [7, 30, 90, 180, 365]  # 1 week, 1 month, 3 months, 6 months, 1 year
    predictions = predictor.create_predictions(time_windows)
    
    # Create visualizations
    predictor.create_comprehensive_visualizations(predictions)
    
    # Generate comprehensive report
    predictor.generate_comprehensive_report(predictions, current_quote)
    
    print("\n🎉 Tesla analysis complete! Check the generated files:")
    print("- tesla_stock_analysis.png (comprehensive visualizations)")
    print("- tesla_stock_prediction_report.md (detailed analysis report)")

if __name__ == "__main__":
    main()
