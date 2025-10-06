#!/usr/bin/env python3
"""
Economist-Style Trading Dashboard
Sophisticated financial analysis with economic indicators
Powered by Twelve Data API
"""

from flask import Flask, render_template_string, jsonify, request
import requests
import os
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)

class EconomistDashboard:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.twelvedata.com"
        
        # Asset categories with full names
        self.assets = {
            'currencies': {
                'USD/CNY': {'name': 'US Dollar / Chinese Yuan', 'desc': 'Major Asian currency pair'},
                'EUR/USD': {'name': 'Euro / US Dollar', 'desc': 'World\'s most traded pair'},
                'GBP/USD': {'name': 'British Pound / US Dollar', 'desc': 'Cable'},
                'USD/JPY': {'name': 'US Dollar / Japanese Yen', 'desc': 'Major Asian currency'},
                'AUD/USD': {'name': 'Australian Dollar / US Dollar', 'desc': 'Commodity currency'},
                'USD/CAD': {'name': 'US Dollar / Canadian Dollar', 'desc': 'Loonie'},
                'USD/CHF': {'name': 'US Dollar / Swiss Franc', 'desc': 'Safe haven currency'},
                'NZD/USD': {'name': 'New Zealand Dollar / US Dollar', 'desc': 'Kiwi'},
            },
            'stocks': {
                'AAPL': {'name': 'Apple Inc.', 'desc': 'Technology - Consumer Electronics'},
                'MSFT': {'name': 'Microsoft Corporation', 'desc': 'Technology - Software'},
                'GOOGL': {'name': 'Alphabet Inc.', 'desc': 'Technology - Internet Services'},
                'AMZN': {'name': 'Amazon.com Inc.', 'desc': 'Consumer - E-commerce'},
                'TSLA': {'name': 'Tesla Inc.', 'desc': 'Automotive - Electric Vehicles'},
                'META': {'name': 'Meta Platforms Inc.', 'desc': 'Technology - Social Media'},
                'NVDA': {'name': 'NVIDIA Corporation', 'desc': 'Technology - Semiconductors'},
                'JPM': {'name': 'JPMorgan Chase & Co.', 'desc': 'Financial Services - Banking'},
                'V': {'name': 'Visa Inc.', 'desc': 'Financial Services - Payments'},
                'JNJ': {'name': 'Johnson & Johnson', 'desc': 'Healthcare - Pharmaceuticals'},
            },
            'crypto': {
                'BTC/USD': {'name': 'Bitcoin', 'desc': 'Leading cryptocurrency'},
                'ETH/USD': {'name': 'Ethereum', 'desc': 'Smart contract platform'},
                'BNB/USD': {'name': 'Binance Coin', 'desc': 'Exchange token'},
                'ADA/USD': {'name': 'Cardano', 'desc': 'Proof-of-stake blockchain'},
                'SOL/USD': {'name': 'Solana', 'desc': 'High-performance blockchain'},
                'XRP/USD': {'name': 'Ripple', 'desc': 'Payment settlement system'},
            },
            'indices': {
                'DIA': {'name': 'Dow Jones Industrial Average', 'desc': '30 large US companies'},
                'QQQ': {'name': 'NASDAQ-100', 'desc': 'Technology-heavy index'},
                'IWM': {'name': 'Russell 2000', 'desc': 'Small-cap stocks'},
                'VTI': {'name': 'Total Stock Market', 'desc': 'Entire US stock market'},
            },
            'metals': {
                'XAU/USD': {'name': 'Gold', 'desc': 'Safe haven precious metal'},
                'XAG/USD': {'name': 'Silver', 'desc': 'Industrial precious metal'},
                'XPT/USD': {'name': 'Platinum', 'desc': 'Automotive catalyst metal'},
                'XPD/USD': {'name': 'Palladium', 'desc': 'Electronic components metal'},
                'GLD': {'name': 'Gold ETF (SPDR)', 'desc': 'Gold-backed exchange traded fund'},
                'SLV': {'name': 'Silver ETF (iShares)', 'desc': 'Silver-backed exchange traded fund'},
            }
        }
    
    def fetch_asset_data(self, symbol: str, asset_type: str) -> dict:
        """Fetch comprehensive asset data"""
        try:
            params = {
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/quote", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'code' in data:
                return {'error': data.get('message', 'API Error')}
            
            if 'price' in data or 'close' in data:
                current_price = float(data.get('price') or data.get('close'))
                change_percent = float(data.get('percent_change', 0))
                prev_close = float(data.get('previous_close', current_price))
                change = float(data.get('change', 0))
                
                # Calculate technical levels
                high_52w = float(data.get('fifty_two_week', {}).get('high', current_price * 1.2))
                low_52w = float(data.get('fifty_two_week', {}).get('low', current_price * 0.8))
                
                return {
                    'current_price': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'previous_close': prev_close,
                    'high_52w': high_52w,
                    'low_52w': low_52w,
                    'market_open': data.get('is_market_open', True),
                    'datetime': data.get('datetime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                }
            
            return {'error': 'No price data available'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def fetch_historical_data(self, symbol: str, days: int = 60) -> dict:
        """Fetch real historical price data from Twelve Data API"""
        try:
            params = {
                'symbol': symbol,
                'interval': '1day',
                'outputsize': days,
                'apikey': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/time_series", params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            print(f"Time Series API response keys for {symbol}: {list(data.keys())}")
            
            # Check for API errors
            if 'code' in data:
                print(f"API error for {symbol}: {data.get('message', 'Unknown error')}")
                return None
            
            if 'status' in data and data['status'] == 'error':
                print(f"API status error for {symbol}: {data.get('message', 'Unknown error')}")
                return None
            
            if 'values' not in data:
                print(f"No 'values' in response for {symbol}")
                return None
            
            # Extract historical data
            values = data['values']
            print(f"Fetched {len(values)} historical data points for {symbol}")
            
            if len(values) < 5:
                print(f"Too few data points for {symbol}: {len(values)}")
                return None
            
            historical_prices = []
            dates = []
            
            # Reverse to get chronological order (oldest first)
            for item in reversed(values):
                dates.append(item['datetime'][:10])  # YYYY-MM-DD
                historical_prices.append(float(item['close']))
            
            print(f"Processed {len(historical_prices)} prices for {symbol}, range: {min(historical_prices):.2f} - {max(historical_prices):.2f}")
            
            return {
                'dates': dates,
                'prices': historical_prices
            }
            
        except Exception as e:
            print(f"Exception fetching historical data for {symbol}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_forecast(self, historical_prices: list, days: int = 30) -> dict:
        """Generate future price forecast based on historical data using simple moving average and trend"""
        if not historical_prices or len(historical_prices) < 10:
            return {'dates': [], 'prices': []}
        
        # Use more data points for better trend estimation
        recent_window = min(30, len(historical_prices))
        recent_prices = historical_prices[-recent_window:]
        
        # Calculate linear trend (simple linear regression)
        n = len(recent_prices)
        x = list(range(n))
        y = recent_prices
        
        # Calculate slope and intercept
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator != 0:
            slope = numerator / denominator
            intercept = y_mean - slope * x_mean
        else:
            slope = 0
            intercept = recent_prices[-1]
        
        # Calculate volatility (standard deviation of daily returns)
        returns = [(recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1] 
                   for i in range(1, len(recent_prices))]
        mean_return = sum(returns) / len(returns) if returns else 0
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns) if returns else 0.0001
        std_dev = variance ** 0.5
        
        # Generate forecast with mean reversion and uncertainty bands
        forecast_prices = []
        forecast_dates = []
        
        for i in range(1, days + 1):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            
            # Linear trend projection
            trend_price = slope * (n + i - 1) + intercept
            
            # Add mean reversion (prices tend to revert to long-term average)
            long_term_avg = sum(historical_prices) / len(historical_prices)
            reversion_factor = 0.02  # 2% pull toward mean per day
            mean_reversion = (long_term_avg - trend_price) * reversion_factor * i / days
            
            # Combine trend with mean reversion
            base_price = trend_price + mean_reversion
            
            # Add realistic random walk component (decreasing confidence over time)
            # Uncertainty grows with sqrt(time) as in random walk theory
            uncertainty_factor = (i ** 0.5) * std_dev * random.gauss(0, 1) * 0.5
            
            # Final forecast price
            forecast_price = base_price * (1 + uncertainty_factor)
            
            # Ensure price stays reasonable (within 30% of current price for 30-day forecast)
            current_price = historical_prices[-1]
            max_change = 0.30  # 30% max change
            forecast_price = max(current_price * (1 - max_change), 
                                min(current_price * (1 + max_change), forecast_price))
            
            forecast_prices.append(round(forecast_price, 2))
            forecast_dates.append(date)
        
        return {
            'dates': forecast_dates,
            'prices': forecast_prices
        }
    
    def get_economic_indicators(self, asset_type: str, symbol: str) -> dict:
        """Get relevant economic indicators for the asset"""
        # Mock economic indicators - in production, fetch from economic APIs
        indicators = {
            'global': {
                'fed_rate': {
                    'value': 4.375, 'change': -0.25, 'trend': 'down', 
                    'desc': 'Federal Reserve Interest Rate',
                    'tooltip': 'The interest rate at which banks lend to each other overnight. Higher rates strengthen USD and reduce asset valuations. Rate cuts typically boost stocks and weaken USD.'
                },
                'us_inflation': {
                    'value': 3.2, 'change': -0.3, 'trend': 'down', 
                    'desc': 'US CPI Inflation Rate (%)',
                    'tooltip': 'Consumer Price Index measures price changes. High inflation erodes currency value and may trigger Fed rate hikes. Target is 2%. Rising inflation is negative for bonds and USD purchasing power.'
                },
                'us_unemployment': {
                    'value': 3.8, 'change': 0.1, 'trend': 'up', 
                    'desc': 'US Unemployment Rate (%)',
                    'tooltip': 'Percentage of workforce without jobs. Low unemployment (below 4%) indicates strong economy but may lead to wage inflation. Rising unemployment weakens USD and signals economic slowdown.'
                },
                'us_gdp': {
                    'value': 2.4, 'change': 0.3, 'trend': 'up', 
                    'desc': 'US GDP Growth (%)',
                    'tooltip': 'Gross Domestic Product measures economic output. Strong GDP (above 2.5%) supports USD and stocks. Negative GDP indicates recession. China\'s GDP significantly impacts CNY and commodity currencies.'
                },
            },
            'currency_specific': {
                'USD/CNY': {
                    'china_gdp': {
                        'value': 5.2, 'change': -0.3, 'trend': 'down', 
                        'desc': 'China GDP Growth (%)',
                        'tooltip': 'China economic growth rate. Target is 5%. Strong growth supports CNY. Slowing growth weakens CNY and may trigger stimulus measures. Directly impacts USD/CNY exchange rate and commodity demand.'
                    },
                    'china_pmi': {
                        'value': 49.2, 'change': -0.8, 'trend': 'down', 
                        'desc': 'China Manufacturing PMI',
                        'tooltip': 'Manufacturing activity index. Above 50 = expansion, below 50 = contraction. Low PMI weakens CNY and signals economic slowdown. Critical for USD/CNY as China is manufacturing hub.'
                    },
                    'trade_balance': {
                        'value': 78.2, 'change': 5.3, 'trend': 'up', 
                        'desc': 'China Trade Surplus ($B)',
                        'tooltip': 'Exports minus imports. Large surplus strengthens CNY as foreign buyers need CNY to pay Chinese exporters. Rising surplus supports CNY appreciation. Trade war impacts this significantly.'
                    },
                },
                'EUR/USD': {
                    'ecb_rate': {
                        'value': 4.0, 'change': 0.0, 'trend': 'stable', 
                        'desc': 'ECB Interest Rate (%)',
                        'tooltip': 'European Central Bank policy rate. Higher rates strengthen EUR vs USD. ECB following Fed policy with lag. Rate differential between Fed and ECB drives EUR/USD movements.'
                    },
                    'eu_inflation': {
                        'value': 2.9, 'change': -0.4, 'trend': 'down', 
                        'desc': 'Eurozone Inflation (%)',
                        'tooltip': 'Eurozone price increases. Target is 2%. High inflation may force ECB to raise rates, strengthening EUR. Energy prices heavily impact EU inflation due to import dependence.'
                    },
                    'eu_pmi': {
                        'value': 47.1, 'change': -0.9, 'trend': 'down', 
                        'desc': 'Eurozone Manufacturing PMI',
                        'tooltip': 'Manufacturing activity across EU. Below 50 indicates contraction, weakening EUR. Germany\'s industrial sector dominates this indicator. Weak PMI may trigger ECB stimulus.'
                    },
                }
            },
            'market_sentiment': {
                'vix': {
                    'value': 15.2, 'change': -2.1, 'trend': 'down', 
                    'desc': 'VIX Volatility Index',
                    'tooltip': 'Fear gauge for stock market. VIX below 15 = calm, 15-20 = normal, 20-30 = elevated anxiety, above 30 = panic. High VIX is negative for stocks and risk assets, but can support safe havens like gold and JPY.'
                },
                'consumer_confidence': {
                    'value': 102.3, 'change': 3.5, 'trend': 'up', 
                    'desc': 'US Consumer Confidence',
                    'tooltip': 'Measures consumer optimism. Above 100 indicates confidence in economy. High confidence drives spending, supporting USD and stocks. Falling confidence signals economic weakness and potential recession.'
                },
                'dollar_index': {
                    'value': 104.5, 'change': 0.3, 'trend': 'up', 'desc': 'US Dollar Index (DXY)',
                    'tooltip': 'Measures USD strength vs basket of currencies (EUR, JPY, GBP, CAD, SEK, CHF). Rising DXY strengthens USD pairs and pressures commodities/gold. Strong dollar is negative for US exporters and emerging markets.'
                },
                'bond_yield_2y': {
                    'value': 4.25, 'change': 0.08, 'trend': 'up', 
                    'desc': '2-Year Treasury Yield (%)',
                    'tooltip': 'Short-term interest rate reflecting Fed policy expectations. Sensitive to Fed rate changes. Rising yields strengthen USD and compete with stocks. Inverted yield curve (2Y > 10Y) signals recession.'
                },
                'bond_yield_10y': {
                    'value': 4.65, 'change': 0.12, 'trend': 'up', 
                    'desc': '10-Year Treasury Yield (%)',
                    'tooltip': 'Long-term interest rate benchmark for mortgages and loans. Rising yields strengthen USD but pressure stocks and real estate. High yields attract foreign capital, supporting USD. Inverted curve (below 2Y) = recession warning.'
                },
            }
        }
        
        result = {
            'global': indicators['global'],
            'sentiment': indicators['market_sentiment']
        }
        
        # Add asset-specific indicators
        if asset_type == 'currency' and symbol in indicators['currency_specific']:
            result['specific'] = indicators['currency_specific'][symbol]
        
        return result
    
    def calculate_analysis(self, price_data: dict, asset_type: str) -> dict:
        """Calculate trading analysis and predictions"""
        if 'error' in price_data:
            return {}
        
        current_price = price_data['current_price']
        change_percent = price_data['change_percent']
        high_52w = price_data['high_52w']
        low_52w = price_data['low_52w']
        
        # Calculate position in 52-week range
        range_position = ((current_price - low_52w) / (high_52w - low_52w)) * 100 if (high_52w - low_52w) > 0 else 50
        
        # Determine signal
        if change_percent > 2.0:
            signal = 'STRONG BUY'
            confidence = 80
            reasoning = f'Significant upward momentum (+{change_percent:.1f}%)'
        elif change_percent > 0.5:
            signal = 'BUY'
            confidence = 65
            reasoning = f'Positive trend (+{change_percent:.1f}%)'
        elif change_percent < -2.0:
            signal = 'STRONG SELL'
            confidence = 80
            reasoning = f'Significant downward pressure ({change_percent:.1f}%)'
        elif change_percent < -0.5:
            signal = 'SELL'
            confidence = 65
            reasoning = f'Negative trend ({change_percent:.1f}%)'
        else:
            signal = 'HOLD'
            confidence = 50
            reasoning = f'Stable price action ({change_percent:+.1f}%)'
        
        # Calculate support and resistance
        support = current_price * 0.98
        resistance = current_price * 1.02
        
        # Predictions
        predictions = {
            '7_day': current_price * (1 + (change_percent / 100) * 0.5),
            '30_day': current_price * (1 + (change_percent / 100) * 1.5),
            '90_day': current_price * (1 + (change_percent / 100) * 3.0),
        }
        
        return {
            'signal': signal,
            'confidence': confidence,
            'reasoning': reasoning,
            'range_position': range_position,
            'support': support,
            'resistance': resistance,
            'predictions': predictions
        }

dashboard = EconomistDashboard(os.getenv('TWELVEDATA_API_KEY', 'demo'))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Markets Dashboard | The Economist Style</title>
    <link href="https://fonts.googleapis.com/css2?family=Econ+Sans:wght@400;500;700&family=Milo+Serif:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        :root {
            --economist-red: #e3120b;
            --economist-blue: #006ba6;
            --economist-dark: #1a1a1a;
            --economist-light: #f4f4f4;
            --economist-gray: #666666;
            --economist-border: #d6d6d6;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Econ Sans', Arial, sans-serif;
            background: white;
            color: var(--economist-dark);
            line-height: 1.6;
        }
        
        .header {
            background: var(--economist-red);
            color: white;
            padding: 20px 40px;
            border-bottom: 4px solid var(--economist-dark);
        }
        
        .header h1 {
            font-family: 'Milo Serif', Georgia, serif;
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .header .subtitle {
            font-size: 1rem;
            margin-top: 5px;
            opacity: 0.95;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 40px;
        }
        
        .asset-selector {
            background: var(--economist-light);
            border: 2px solid var(--economist-border);
            padding: 25px;
            margin-bottom: 30px;
        }
        
        .selector-title {
            font-family: 'Milo Serif', Georgia, serif;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--economist-dark);
        }
        
        .selector-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .selector-group {
            display: flex;
            flex-direction: column;
        }
        
        .selector-group label {
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--economist-gray);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .selector-group select {
            padding: 12px;
            border: 2px solid var(--economist-border);
            background: white;
            font-size: 1rem;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .selector-group select:hover {
            border-color: var(--economist-blue);
        }
        
        .selector-group select:focus {
            outline: none;
            border-color: var(--economist-red);
            box-shadow: 0 0 0 3px rgba(227, 18, 11, 0.1);
        }
        
        .refresh-button {
            padding: 12px 24px;
            background: var(--economist-blue);
            color: white;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }
        
        .refresh-button:hover {
            background: var(--economist-red);
        }
        
        .refresh-button:active {
            transform: translateY(1px);
        }
        
        .refresh-button:disabled {
            background: var(--economist-gray);
            cursor: not-allowed;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .section {
            background: white;
            border: 2px solid var(--economist-border);
            padding: 25px;
        }
        
        .section-title {
            font-family: 'Milo Serif', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--economist-dark);
            border-bottom: 3px solid var(--economist-red);
            padding-bottom: 10px;
        }
        
        .price-display {
            text-align: center;
            padding: 30px;
            background: var(--economist-light);
            border: 2px solid var(--economist-border);
            margin-bottom: 25px;
        }
        
        .asset-name {
            font-size: 1.1rem;
            color: var(--economist-gray);
            margin-bottom: 10px;
        }
        
        .price {
            font-family: 'Milo Serif', Georgia, serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: var(--economist-dark);
            margin-bottom: 10px;
        }
        
        .price-change {
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        .positive { color: #2e7d32; }
        .negative { color: #c62828; }
        .neutral { color: var(--economist-gray); }
        
        .signal-box {
            padding: 20px;
            background: white;
            border-left: 5px solid var(--economist-blue);
            margin-bottom: 25px;
        }
        
        .signal-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--economist-gray);
            margin-bottom: 5px;
        }
        
        .signal-value {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .signal-reasoning {
            font-size: 0.95rem;
            color: var(--economist-gray);
            line-height: 1.5;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .metric {
            padding: 15px;
            background: var(--economist-light);
            border-left: 3px solid var(--economist-border);
        }
        
        .metric-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--economist-gray);
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--economist-dark);
        }
        
        .predictions {
            padding: 20px;
            background: var(--economist-light);
            border: 2px solid var(--economist-border);
        }
        
        .prediction-item {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid var(--economist-border);
        }
        
        .prediction-item:last-child {
            border-bottom: none;
        }
        
        .prediction-label {
            font-weight: 600;
            color: var(--economist-gray);
        }
        
        .prediction-value {
            font-weight: 700;
            color: var(--economist-dark);
        }
        
        .indicators-section {
            margin-top: 30px;
        }
        
        .indicator-category {
            margin-bottom: 25px;
        }
        
        .category-title {
            font-weight: 700;
            font-size: 1.1rem;
            color: var(--economist-dark);
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--economist-border);
        }
        
        .indicator {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 15px;
            padding: 12px 0;
            border-bottom: 1px solid var(--economist-light);
        }
        
        .indicator-name {
            color: var(--economist-gray);
            font-size: 0.9rem;
        }
        
        .indicator-value {
            font-weight: 700;
            text-align: right;
        }
        
        .indicator-trend {
            text-align: right;
            font-size: 0.85rem;
        }
        
        .trend-up { color: #2e7d32; }
        .trend-down { color: #c62828; }
        .trend-stable { color: var(--economist-gray); }
        
        .chart-container {
            background: white;
            padding: 25px;
            border: 2px solid var(--economist-border);
            margin-bottom: 30px;
            position: relative;
            height: 400px;
        }
        
        .chart-canvas {
            max-height: 350px;
        }
        
        .tooltip-icon {
            display: inline-block;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--economist-blue);
            color: white;
            text-align: center;
            line-height: 16px;
            font-size: 11px;
            font-weight: bold;
            cursor: help;
            margin-left: 5px;
            position: relative;
        }
        
        .tooltip-icon:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }
        
        .tooltip-text {
            visibility: hidden;
            width: 300px;
            background-color: var(--economist-dark);
            color: white;
            text-align: left;
            border-radius: 6px;
            padding: 12px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.85rem;
            line-height: 1.4;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        .tooltip-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: var(--economist-dark) transparent transparent transparent;
        }
        
        .footer {
            margin-top: 30px;
            padding: 20px;
            text-align: center;
            font-size: 0.85rem;
            color: var(--economist-gray);
            border-top: 2px solid var(--economist-border);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--economist-gray);
        }
        
        @media (max-width: 968px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Financial Markets Dashboard</h1>
        <div class="subtitle">Real-time market data and economic indicators</div>
    </div>
    
    <div class="container">
        <div class="asset-selector">
            <div class="selector-title">Select Asset</div>
            <div class="selector-grid">
                <div class="selector-group">
                    <label>Asset Type</label>
                    <select id="asset-type" onchange="updateAssetList()">
                        <option value="currencies">Foreign Exchange</option>
                        <option value="stocks">Equities</option>
                        <option value="crypto">Cryptocurrencies</option>
                        <option value="indices">Market Indices</option>
                        <option value="metals">Precious Metals</option>
                    </select>
                </div>
                
                <div class="selector-group">
                    <label>Select Asset</label>
                    <select id="asset-symbol" onchange="loadAsset()">
                        <!-- Will be populated by JavaScript -->
                    </select>
                </div>
                
                <div class="selector-group">
                    <label>&nbsp;</label>
                    <button class="refresh-button" onclick="manualRefresh()" id="refresh-btn">
                        Refresh Now
                    </button>
                </div>
            </div>
        </div>
        
        <div id="content">
            <div class="loading">
                <h2>Select an asset to begin analysis</h2>
                <p>Choose from currencies, stocks, cryptocurrencies, or indices above</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        Data provided by Twelve Data • Updated in real-time • For informational purposes only
    </div>
    
    <script>
        const assets = JSON.parse('""" + json.dumps({
            'currencies': list(dashboard.assets['currencies'].items()),
            'stocks': list(dashboard.assets['stocks'].items()),
            'crypto': list(dashboard.assets['crypto'].items()),
            'indices': list(dashboard.assets['indices'].items()),
            'metals': list(dashboard.assets['metals'].items())
        }).replace("'", "\\'") + """');
        
        let priceChart = null;
        
        function updateAssetList() {
            const assetType = document.getElementById('asset-type').value;
            const assetSelect = document.getElementById('asset-symbol');
            assetSelect.innerHTML = '';
            
            assets[assetType].forEach(([symbol, info]) => {
                const option = document.createElement('option');
                option.value = symbol;
                option.textContent = `${symbol} - ${info.name}`;
                assetSelect.appendChild(option);
            });
            
            loadAsset();
        }
        
        function loadAsset() {
            const assetType = document.getElementById('asset-type').value;
            const symbol = document.getElementById('asset-symbol').value;
            
            if (!symbol) return;
            
            document.getElementById('content').innerHTML = '<div class="loading"><h2>Loading data...</h2></div>';
            
            fetch(`/api/asset?type=${assetType}&symbol=${encodeURIComponent(symbol)}`)
                .then(response => response.json())
                .then(data => {
                    renderAsset(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('content').innerHTML = `<div class="loading"><h2>Error loading data</h2><p>${error.message}</p></div>`;
                });
        }
        
        function createChart(chartData, currentPrice, symbol) {
            const ctx = document.getElementById('priceChart');
            if (!ctx) return;
            
            // Destroy existing chart
            if (priceChart) {
                priceChart.destroy();
            }
            
            const allDates = [...chartData.historical.dates, ...chartData.forecast.dates];
            const historicalPrices = [...chartData.historical.prices];
            const forecastPrices = Array(chartData.historical.prices.length).fill(null).concat(chartData.forecast.prices);
            
            priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: allDates,
                    datasets: [{
                        label: 'Historical Price',
                        data: historicalPrices.concat(Array(chartData.forecast.prices.length).fill(null)),
                        borderColor: '#006ba6',
                        backgroundColor: 'rgba(0, 107, 166, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.1,
                        pointRadius: 0,
                        pointHoverRadius: 4
                    }, {
                        label: 'Forecast',
                        data: forecastPrices,
                        borderColor: '#e3120b',
                        backgroundColor: 'rgba(227, 18, 11, 0.05)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: true,
                        tension: 0.1,
                        pointRadius: 0,
                        pointHoverRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                font: { family: 'Econ Sans, Arial', size: 12 },
                                color: '#1a1a1a',
                                usePointStyle: true,
                                padding: 15
                            }
                        },
                        title: {
                            display: true,
                            text: `${symbol} - 60 Day History + 30 Day Forecast`,
                            font: { family: 'Milo Serif, Georgia', size: 16, weight: 'bold' },
                            color: '#1a1a1a',
                            padding: { bottom: 20 }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(26, 26, 26, 0.9)',
                            titleFont: { family: 'Econ Sans, Arial', size: 13 },
                            bodyFont: { family: 'Econ Sans, Arial', size: 12 },
                            padding: 12,
                            cornerRadius: 4
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: { display: false },
                            ticks: {
                                maxRotation: 45,
                                minRotation: 45,
                                font: { family: 'Econ Sans, Arial', size: 10 },
                                color: '#666',
                                autoSkip: true,
                                maxTicksLimit: 12
                            }
                        },
                        y: {
                            display: true,
                            grid: { color: '#f0f0f0', drawBorder: false },
                            ticks: {
                                font: { family: 'Econ Sans, Arial', size: 11 },
                                color: '#666',
                                callback: function(value) {
                                    return value.toFixed(2);
                                }
                            }
                        }
                    },
                    interaction: {
                        mode: 'nearest',
                        axis: 'x',
                        intersect: false
                    }
                }
            });
        }
        
        function renderAsset(data) {
            if (data.error) {
                document.getElementById('content').innerHTML = `<div class="loading"><h2>Error</h2><p>${data.error}</p></div>`;
                return;
            }
            
            const changeClass = data.price.change_percent > 0 ? 'positive' : data.price.change_percent < 0 ? 'negative' : 'neutral';
            const changeSymbol = data.price.change_percent > 0 ? '+' : '';
            
            let html = `
                <div class="chart-container">
                    <canvas id="priceChart" class="chart-canvas"></canvas>
                </div>
            `;
            
            html += `
                <div class="main-content">
                    <div class="section">
                        <div class="price-display">
                            <div class="asset-name">${data.name}</div>
                            <div class="price">${data.price.current_price.toFixed(2)}</div>
                            <div class="price-change ${changeClass}">
                                ${changeSymbol}${data.price.change.toFixed(2)} (${changeSymbol}${data.price.change_percent.toFixed(2)}%)
                            </div>
                        </div>
                        
                        ${data.analysis.signal ? `
                        <div class="signal-box">
                            <div class="signal-label">Trading Signal</div>
                            <div class="signal-value">${data.analysis.signal}</div>
                            <div class="signal-reasoning">${data.analysis.reasoning}</div>
                            <div style="margin-top: 10px; font-size: 0.9rem; color: var(--economist-gray);">
                                Confidence: ${data.analysis.confidence}%
                            </div>
                        </div>
                        ` : ''}
                        
                        <div class="section-title">Technical Levels</div>
                        <div class="metrics-grid">
                            <div class="metric">
                                <div class="metric-label">Support Level</div>
                                <div class="metric-value">${data.analysis.support ? data.analysis.support.toFixed(2) : 'N/A'}</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Resistance Level</div>
                                <div class="metric-value">${data.analysis.resistance ? data.analysis.resistance.toFixed(2) : 'N/A'}</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">52-Week High</div>
                                <div class="metric-value">${data.price.high_52w.toFixed(2)}</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">52-Week Low</div>
                                <div class="metric-value">${data.price.low_52w.toFixed(2)}</div>
                            </div>
                        </div>
                        
                        ${data.analysis.predictions ? `
                        <div class="section-title">Price Predictions</div>
                        <div class="predictions">
                            <div class="prediction-item">
                                <span class="prediction-label">7-Day Forecast</span>
                                <span class="prediction-value">${data.analysis.predictions['7_day'].toFixed(2)}</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">30-Day Forecast</span>
                                <span class="prediction-value">${data.analysis.predictions['30_day'].toFixed(2)}</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">90-Day Forecast</span>
                                <span class="prediction-value">${data.analysis.predictions['90_day'].toFixed(2)}</span>
                            </div>
                        </div>
                        ` : ''}
                    </div>
                    
                    <div class="section">
                        <div class="section-title">Economic Indicators</div>
                        
                        <div class="indicator-category">
                            <div class="category-title">Global Economy</div>
            `;
            
            // Add global indicators
            if (data.indicators.global) {
                for (const [key, indicator] of Object.entries(data.indicators.global)) {
                    const trendClass = indicator.trend === 'up' ? 'trend-up' : indicator.trend === 'down' ? 'trend-down' : 'trend-stable';
                    const trendSymbol = indicator.trend === 'up' ? '↑' : indicator.trend === 'down' ? '↓' : '→';
                    const tooltip = indicator.tooltip ? `
                        <span class="tooltip-icon">?
                            <span class="tooltip-text">${indicator.tooltip}</span>
                        </span>
                    ` : '';
                    html += `
                        <div class="indicator">
                            <div class="indicator-name">${indicator.desc}${tooltip}</div>
                            <div class="indicator-value">${indicator.value}${key.includes('rate') || key.includes('inflation') || key.includes('unemployment') || key.includes('gdp') || key.includes('yield') ? '%' : ''}</div>
                            <div class="indicator-trend ${trendClass}">${trendSymbol} ${indicator.change > 0 ? '+' : ''}${indicator.change}</div>
                        </div>
                    `;
                }
            }
            
            html += '</div>';
            
            // Add market sentiment
            if (data.indicators.sentiment) {
                html += '<div class="indicator-category"><div class="category-title">Market Sentiment</div>';
                for (const [key, indicator] of Object.entries(data.indicators.sentiment)) {
                    const trendClass = indicator.trend === 'up' ? 'trend-up' : indicator.trend === 'down' ? 'trend-down' : 'trend-stable';
                    const trendSymbol = indicator.trend === 'up' ? '↑' : indicator.trend === 'down' ? '↓' : '→';
                    const tooltip = indicator.tooltip ? `
                        <span class="tooltip-icon">?
                            <span class="tooltip-text">${indicator.tooltip}</span>
                        </span>
                    ` : '';
                    html += `
                        <div class="indicator">
                            <div class="indicator-name">${indicator.desc}${tooltip}</div>
                            <div class="indicator-value">${indicator.value}${key.includes('yield') ? '%' : ''}</div>
                            <div class="indicator-trend ${trendClass}">${trendSymbol} ${indicator.change > 0 ? '+' : ''}${indicator.change}</div>
                        </div>
                    `;
                }
                html += '</div>';
            }
            
            // Add asset-specific indicators
            if (data.indicators.specific) {
                html += '<div class="indicator-category"><div class="category-title">Asset-Specific Indicators</div>';
                for (const [key, indicator] of Object.entries(data.indicators.specific)) {
                    const trendClass = indicator.trend === 'up' ? 'trend-up' : indicator.trend === 'down' ? 'trend-down' : 'trend-stable';
                    const trendSymbol = indicator.trend === 'up' ? '↑' : indicator.trend === 'down' ? '↓' : '→';
                    const tooltip = indicator.tooltip ? `
                        <span class="tooltip-icon">?
                            <span class="tooltip-text">${indicator.tooltip}</span>
                        </span>
                    ` : '';
                    html += `
                        <div class="indicator">
                            <div class="indicator-name">${indicator.desc}${tooltip}</div>
                            <div class="indicator-value">${indicator.value}</div>
                            <div class="indicator-trend ${trendClass}">${trendSymbol} ${indicator.change > 0 ? '+' : ''}${indicator.change}</div>
                        </div>
                    `;
                }
                html += '</div>';
            }
            
            html += '</div></div></div>';
            
            document.getElementById('content').innerHTML = html;
            
            // Create chart after DOM is updated
            if (data.chart) {
                setTimeout(() => createChart(data.chart, data.price.current_price, data.symbol), 100);
            }
        }
        
        // Initialize
        updateAssetList();
        
        // Auto-refresh hourly (3600000 milliseconds = 1 hour)
        let autoRefreshInterval = null;
        
        function startAutoRefresh() {
            // Clear any existing interval
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
            }
            
            // Set up hourly refresh
            autoRefreshInterval = setInterval(() => {
                const assetType = document.getElementById('asset-type').value;
                const symbol = document.getElementById('asset-symbol').value;
                if (symbol) {
                    console.log('Auto-refreshing data (hourly update)...');
                    loadAsset();
                }
            }, 3600000); // 1 hour = 3600000 milliseconds
        }
        
        // Start auto-refresh when page loads
        startAutoRefresh();
        
        // Add visual indicator for last update time
        function updateTimestamp() {
            const now = new Date();
            const timeString = now.toLocaleString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                month: 'short',
                day: 'numeric'
            });
            
            // Update footer with last refresh time
            document.querySelector('.footer').innerHTML = `
                Data provided by Twelve Data • Last updated: ${timeString} • Next refresh: ${new Date(now.getTime() + 3600000).toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'})} • For informational purposes only
            `;
        }
        
        // Update timestamp when loading asset
        const originalLoadAsset = loadAsset;
        loadAsset = function() {
            originalLoadAsset();
            updateTimestamp();
        };
        
        // Manual refresh function with cooldown
        let lastRefresh = Date.now();
        function manualRefresh() {
            const now = Date.now();
            const timeSinceLastRefresh = now - lastRefresh;
            const cooldownPeriod = 60000; // 1 minute cooldown
            
            if (timeSinceLastRefresh < cooldownPeriod) {
                const remainingTime = Math.ceil((cooldownPeriod - timeSinceLastRefresh) / 1000);
                alert(`Please wait ${remainingTime} seconds before refreshing again.`);
                return;
            }
            
            const btn = document.getElementById('refresh-btn');
            btn.disabled = true;
            btn.textContent = 'Refreshing...';
            
            loadAsset();
            lastRefresh = now;
            
            setTimeout(() => {
                btn.disabled = false;
                btn.textContent = 'Refresh Now';
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard_page():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/asset')
def api_asset():
    try:
        asset_type = request.args.get('type', 'currencies')
        symbol = request.args.get('symbol', '')
        
        if not symbol:
            return jsonify({'error': 'No symbol provided'}), 400
        
        # Get asset info
        asset_info = dashboard.assets.get(asset_type, {}).get(symbol, {})
        
        # Fetch price data
        price_data = dashboard.fetch_asset_data(symbol, asset_type)
        
        if 'error' in price_data:
            return jsonify({'error': price_data['error']})
        
        # Get economic indicators
        indicators = dashboard.get_economic_indicators(asset_type, symbol)
        
        # Calculate analysis
        analysis = dashboard.calculate_analysis(price_data, asset_type)
        
        # Fetch real historical data
        historical_data = dashboard.fetch_historical_data(symbol, days=60)
        
        if historical_data:
            # Generate forecast based on real historical data
            forecast_data = dashboard.generate_forecast(historical_data['prices'], days=30)
            chart_data = {
                'historical': historical_data,
                'forecast': forecast_data
            }
        else:
            # Fallback: Use a simple placeholder if API fails
            print(f"Using fallback chart data for {symbol}")
            today = datetime.now()
            chart_data = {
                'historical': {
                    'dates': [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(60, -1, -1)],
                    'prices': [price_data['current_price']] * 61
                },
                'forecast': {
                    'dates': [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 31)],
                    'prices': [price_data['current_price']] * 30
                }
            }
        
        return jsonify({
            'symbol': symbol,
            'name': asset_info.get('name', symbol),
            'description': asset_info.get('desc', ''),
            'type': asset_type,
            'price': price_data,
            'analysis': analysis,
            'indicators': indicators,
            'chart': chart_data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('DASHBOARD_PORT', 8080))
    print("📊 Starting Economist-Style Financial Dashboard...")
    print(f"🌐 Open your browser and go to: http://localhost:{port}")
    print("✨ Powered by Twelve Data")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=port, debug=False)

