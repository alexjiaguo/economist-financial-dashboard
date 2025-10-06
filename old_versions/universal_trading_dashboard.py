#!/usr/bin/env python3
"""
Universal Trading Dashboard - Multi-Asset Trading Platform
Supports currencies, stocks, indices, and cryptocurrencies
"""

from flask import Flask, render_template_string, jsonify, request
import requests
import json
import os
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)

class UniversalTradingDashboard:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.current_data = {}
        self.last_update = None
        
        # Asset categories
        self.currencies = {
            'USD': 'US Dollar', 'EUR': 'Euro', 'GBP': 'British Pound', 'JPY': 'Japanese Yen',
            'CNY': 'Chinese Yuan', 'CAD': 'Canadian Dollar', 'AUD': 'Australian Dollar',
            'CHF': 'Swiss Franc', 'NZD': 'New Zealand Dollar', 'SEK': 'Swedish Krona',
            'NOK': 'Norwegian Krone', 'DKK': 'Danish Krone', 'PLN': 'Polish Zloty',
            'CZK': 'Czech Koruna', 'HUF': 'Hungarian Forint', 'RUB': 'Russian Ruble',
            'BRL': 'Brazilian Real', 'MXN': 'Mexican Peso', 'INR': 'Indian Rupee',
            'KRW': 'South Korean Won', 'SGD': 'Singapore Dollar', 'HKD': 'Hong Kong Dollar',
            'TRY': 'Turkish Lira', 'ZAR': 'South African Rand', 'THB': 'Thai Baht'
        }
        
        self.stocks = {
            'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp.', 'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.', 'TSLA': 'Tesla Inc.', 'META': 'Meta Platforms Inc.',
            'NVDA': 'NVIDIA Corp.', 'BRK.A': 'Berkshire Hathaway', 'UNH': 'UnitedHealth Group',
            'JNJ': 'Johnson & Johnson', 'V': 'Visa Inc.', 'PG': 'Procter & Gamble',
            'JPM': 'JPMorgan Chase', 'MA': 'Mastercard Inc.', 'HD': 'Home Depot Inc.',
            'DIS': 'Walt Disney Co.', 'PYPL': 'PayPal Holdings', 'ADBE': 'Adobe Inc.',
            'CRM': 'Salesforce Inc.', 'NFLX': 'Netflix Inc.'
        }
        
        self.indices = {
            'SPY': 'S&P 500', 'QQQ': 'NASDAQ 100', 'IWM': 'Russell 2000',
            'DIA': 'Dow Jones', 'VTI': 'Total Stock Market', 'VEA': 'Developed Markets',
            'VWO': 'Emerging Markets', 'BND': 'Total Bond Market', 'GLD': 'Gold',
            'SLV': 'Silver', 'USO': 'Oil', 'UNG': 'Natural Gas'
        }
        
        self.cryptocurrencies = {
            'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance Coin',
            'ADA': 'Cardano', 'SOL': 'Solana', 'XRP': 'Ripple',
            'DOT': 'Polkadot', 'DOGE': 'Dogecoin', 'AVAX': 'Avalanche',
            'MATIC': 'Polygon', 'LINK': 'Chainlink', 'UNI': 'Uniswap',
            'LTC': 'Litecoin', 'BCH': 'Bitcoin Cash', 'ATOM': 'Cosmos'
        }
    
    def fetch_currency_rate(self, from_currency: str, to_currency: str) -> tuple:
        """Fetch currency exchange rate - returns (rate, error_message)"""
        try:
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': from_currency,
                'to_currency': to_currency,
                'apikey': self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"Currency API Response for {from_currency}/{to_currency}: {data}")
            
            if 'Realtime Currency Exchange Rate' in data:
                rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                return rate, None
            elif 'Error Message' in data:
                return None, data['Error Message']
            elif 'Note' in data:
                return None, "⚠️ API rate limit reached (5 requests/minute). Please wait."
            elif 'Information' in data:
                # Daily rate limit reached
                return None, "⚠️ Daily API limit reached (25 requests/day). Using demo mode."
            else:
                return None, f"Unexpected API response: {list(data.keys())}"
        except Exception as e:
            error_msg = f"Error fetching {from_currency}/{to_currency}: {str(e)}"
            print(error_msg)
            return None, error_msg
    
    def fetch_stock_price(self, symbol: str) -> tuple:
        """Fetch stock price - returns (price, change_percent, error_message)"""
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"Stock API Response for {symbol}: {data}")
            
            if 'Global Quote' in data and data['Global Quote']:
                price = float(data['Global Quote']['05. price'])
                change_percent = float(data['Global Quote']['10. change percent'].rstrip('%'))
                return price, change_percent, None
            elif 'Error Message' in data:
                return None, None, data['Error Message']
            elif 'Note' in data:
                return None, None, "⚠️ API rate limit reached (5 requests/minute). Please wait."
            elif 'Information' in data:
                return None, None, "⚠️ Daily API limit reached (25 requests/day). Using demo mode."
            else:
                return None, None, f"Unexpected API response: {list(data.keys())}"
        except Exception as e:
            error_msg = f"Error fetching {symbol}: {str(e)}"
            print(error_msg)
            return None, None, error_msg
    
    def fetch_crypto_price(self, symbol: str) -> tuple:
        """Fetch cryptocurrency price - returns (price, change_percent, error_message)"""
        try:
            params = {
                'function': 'DIGITAL_CURRENCY_DAILY',
                'symbol': symbol,
                'market': 'USD',
                'apikey': self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"Crypto API Response for {symbol}: {list(data.keys())}")
            
            if 'Time Series (Digital Currency Daily)' in data:
                dates = sorted(data['Time Series (Digital Currency Daily)'].keys(), reverse=True)
                if len(dates) >= 2:
                    latest_date = dates[0]
                    prev_date = dates[1]
                    current_price = float(data['Time Series (Digital Currency Daily)'][latest_date]['4a. close (USD)'])
                    prev_price = float(data['Time Series (Digital Currency Daily)'][prev_date]['4a. close (USD)'])
                    change_percent = ((current_price - prev_price) / prev_price) * 100
                    return current_price, change_percent, None
            elif 'Error Message' in data:
                return None, None, data['Error Message']
            elif 'Note' in data:
                return None, None, "⚠️ API rate limit reached (5 requests/minute). Please wait."
            elif 'Information' in data:
                return None, None, "⚠️ Daily API limit reached (25 requests/day). Using demo mode."
            else:
                return None, None, f"Unexpected API response: {list(data.keys())}"
        except Exception as e:
            error_msg = f"Error fetching {symbol}: {str(e)}"
            print(error_msg)
            return None, None, error_msg
    
    def calculate_trading_signal(self, current_price: float, price_change_percent: float, asset_type: str, symbol: str) -> dict:
        """Calculate trading signal based on real price movement"""
        signals = {
            'action': 'HOLD',
            'confidence': 50,
            'target_price': current_price,
            'stop_loss': current_price * 0.95,
            'reasoning': 'Neutral market conditions',
            'risk_level': 'MEDIUM',
            'change_percent': price_change_percent
        }
        
        # Real signal generation based on actual price changes
        if price_change_percent > 3.0:
            signals.update({
                'action': 'BUY',
                'confidence': 80,
                'reasoning': f'Strong upward momentum (+{price_change_percent:.2f}%)',
                'risk_level': 'LOW',
                'target_price': current_price * 1.05
            })
        elif price_change_percent < -3.0:
            signals.update({
                'action': 'SELL',
                'confidence': 75,
                'reasoning': f'Downward pressure ({price_change_percent:.2f}%)',
                'risk_level': 'HIGH',
                'stop_loss': current_price * 0.97
            })
        elif price_change_percent > 1.0:
            signals.update({
                'action': 'BUY',
                'confidence': 65,
                'reasoning': f'Positive trend (+{price_change_percent:.2f}%)',
                'risk_level': 'MEDIUM',
                'target_price': current_price * 1.03
            })
        elif price_change_percent < -1.0:
            signals.update({
                'action': 'SELL',
                'confidence': 60,
                'reasoning': f'Negative trend ({price_change_percent:.2f}%)',
                'risk_level': 'MEDIUM',
                'stop_loss': current_price * 0.98
            })
        else:
            signals.update({
                'reasoning': f'Stable price movement ({price_change_percent:+.2f}%)',
                'target_price': current_price * 1.02
            })
        
        return signals
    
    def get_market_data(self, asset_type: str, symbol: str, from_currency: str = None, to_currency: str = None):
        """Get comprehensive market data for any asset"""
        current_price = 0
        asset_name = ""
        price_change = 0
        error_message = None
        
        if asset_type == 'currency':
            if from_currency and to_currency:
                current_price, error_message = self.fetch_currency_rate(from_currency, to_currency)
                asset_name = f"{from_currency}/{to_currency}"
                # For currencies, calculate daily change using historical data
                price_change = 0  # Simplified - would need time series data
        elif asset_type == 'stock':
            current_price, price_change, error_message = self.fetch_stock_price(symbol)
            asset_name = self.stocks.get(symbol, symbol)
        elif asset_type == 'crypto':
            current_price, price_change, error_message = self.fetch_crypto_price(symbol)
            asset_name = self.cryptocurrencies.get(symbol, symbol)
        elif asset_type == 'index':
            current_price, price_change, error_message = self.fetch_stock_price(symbol)
            asset_name = self.indices.get(symbol, symbol)
        
        # Handle errors
        if error_message:
            return {
                'error': error_message,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'asset_type': asset_type,
                'symbol': symbol,
                'asset_name': asset_name
            }
        
        if current_price is None:
            return {
                'error': 'Failed to fetch price data',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'asset_type': asset_type,
                'symbol': symbol,
                'asset_name': asset_name
            }
        
        signals = self.calculate_trading_signal(current_price, price_change, asset_type, symbol)
        
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'asset_type': asset_type,
            'symbol': symbol,
            'asset_name': asset_name,
            'current_price': current_price,
            'price_change': price_change,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'action': signals['action'],
            'confidence': signals['confidence'],
            'reasoning': signals['reasoning'],
            'risk_level': signals['risk_level'],
            'target_price': signals['target_price'],
            'stop_loss': signals['stop_loss']
        }
    
    def update_data(self):
        """Update data in background"""
        while True:
            try:
                # Update popular pairs
                popular_pairs = [
                    ('currency', 'USD', 'CNY', 'USD'),
                    ('currency', 'EUR', 'USD', 'EUR'),
                    ('stock', 'AAPL', None, None),
                    ('stock', 'TSLA', None, None),
                    ('crypto', 'BTC', None, None),
                    ('crypto', 'ETH', None, None)
                ]
                
                for asset_type, symbol, from_curr, to_curr in popular_pairs:
                    key = f"{asset_type}_{symbol}_{from_curr}_{to_curr}"
                    self.current_data[key] = self.get_market_data(asset_type, symbol, from_curr, to_curr)
                
                self.last_update = datetime.now()
                print(f"Data updated at {self.last_update.strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"Error updating data: {str(e)}")
            time.sleep(30)  # Update every 30 seconds

# Initialize dashboard
api_key = os.getenv('ALPHAVANTAGE_API_KEY', 'demo')
dashboard = UniversalTradingDashboard(api_key)

# Start background data updates
data_thread = threading.Thread(target=dashboard.update_data, daemon=True)
data_thread.start()

# Modern HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Trading Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .controls {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .control-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
        }
        
        .control-group label {
            font-weight: 600;
            margin-bottom: 8px;
            color: #555;
        }
        
        .control-group select,
        .control-group input {
            padding: 12px 16px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: white;
        }
        
        .control-group select:focus,
        .control-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .asset-card {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .asset-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }
        
        .asset-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .asset-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #333;
        }
        
        .asset-type {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .type-currency { background: #e3f2fd; color: #1976d2; }
        .type-stock { background: #f3e5f5; color: #7b1fa2; }
        .type-crypto { background: #fff3e0; color: #f57c00; }
        .type-index { background: #e8f5e8; color: #388e3c; }
        
        .price {
            font-size: 2.5rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }
        
        .signal {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }
        
        .signal-buy { background: #e8f5e8; color: #2e7d32; }
        .signal-sell { background: #ffebee; color: #c62828; }
        .signal-hold { background: #fff3e0; color: #ef6c00; }
        
        .confidence {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 10px;
        }
        
        .reasoning {
            font-size: 0.9rem;
            color: #555;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        
        .risk-level {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
        }
        
        .risk-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }
        
        .risk-low { background: #4caf50; }
        .risk-medium { background: #ff9800; }
        .risk-high { background: #f44336; }
        
        .status-bar {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            padding: 12px 24px;
            border-radius: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.9rem;
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4caf50;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #c62828;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .control-row { grid-template-columns: 1fr; }
            .dashboard-grid { grid-template-columns: 1fr; }
            .container { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Universal Trading Dashboard</h1>
            <p>Trade currencies, stocks, indices, and cryptocurrencies with confidence</p>
        </div>
        
        <div class="controls">
            <div class="control-row">
                <div class="control-group">
                    <label for="asset-type">Asset Type</label>
                    <select id="asset-type" onchange="updateControls()">
                        <option value="currency">Currency Pair</option>
                        <option value="stock">Stock</option>
                        <option value="crypto">Cryptocurrency</option>
                        <option value="index">Index</option>
                    </select>
                </div>
                
                <div class="control-group" id="currency-controls">
                    <label for="from-currency">From Currency</label>
                    <select id="from-currency">
                        <option value="USD">USD - US Dollar</option>
                        <option value="EUR">EUR - Euro</option>
                        <option value="GBP">GBP - British Pound</option>
                        <option value="JPY">JPY - Japanese Yen</option>
                        <option value="CNY">CNY - Chinese Yuan</option>
                        <option value="CAD">CAD - Canadian Dollar</option>
                        <option value="AUD">AUD - Australian Dollar</option>
                        <option value="CHF">CHF - Swiss Franc</option>
                    </select>
                </div>
                
                <div class="control-group" id="to-currency-controls">
                    <label for="to-currency">To Currency</label>
                    <select id="to-currency">
                        <option value="CNY">CNY - Chinese Yuan</option>
                        <option value="USD">USD - US Dollar</option>
                        <option value="EUR">EUR - Euro</option>
                        <option value="GBP">GBP - British Pound</option>
                        <option value="JPY">JPY - Japanese Yen</option>
                        <option value="CAD">CAD - Canadian Dollar</option>
                        <option value="AUD">AUD - Australian Dollar</option>
                        <option value="CHF">CHF - Swiss Franc</option>
                    </select>
                </div>
                
                <div class="control-group" id="symbol-controls" style="display: none;">
                    <label for="symbol">Symbol</label>
                    <select id="symbol">
                        <option value="AAPL">AAPL - Apple Inc.</option>
                        <option value="MSFT">MSFT - Microsoft Corp.</option>
                        <option value="GOOGL">GOOGL - Alphabet Inc.</option>
                        <option value="AMZN">AMZN - Amazon.com Inc.</option>
                        <option value="TSLA">TSLA - Tesla Inc.</option>
                        <option value="META">META - Meta Platforms Inc.</option>
                        <option value="NVDA">NVDA - NVIDIA Corp.</option>
                    </select>
                </div>
            </div>
            
            <div class="control-row">
                <button class="btn" onclick="addAsset()">Add Asset</button>
                <button class="btn" onclick="clearAssets()">Clear All</button>
                <button class="btn" onclick="refreshData()">Refresh Data</button>
            </div>
        </div>
        
        <div class="dashboard-grid" id="dashboard-grid">
            <!-- Assets will be added here dynamically -->
        </div>
    </div>
    
    <div class="status-bar">
        <div class="status-indicator"></div>
        <span>Last Updated: <span id="last-update">Loading...</span></span>
        <span>•</span>
        <span>Auto-refresh: 30s</span>
    </div>
    
    <script>
        let assets = [];
        let updateInterval;
        
        function updateControls() {
            const assetType = document.getElementById('asset-type').value;
            const currencyControls = document.getElementById('currency-controls');
            const toCurrencyControls = document.getElementById('to-currency-controls');
            const symbolControls = document.getElementById('symbol-controls');
            
            if (assetType === 'currency') {
                currencyControls.style.display = 'block';
                toCurrencyControls.style.display = 'block';
                symbolControls.style.display = 'none';
            } else {
                currencyControls.style.display = 'none';
                toCurrencyControls.style.display = 'none';
                symbolControls.style.display = 'block';
                updateSymbolOptions(assetType);
            }
        }
        
        function updateSymbolOptions(assetType) {
            const symbolSelect = document.getElementById('symbol');
            symbolSelect.innerHTML = '';
            
            const options = {
                'stock': [
                    {value: 'AAPL', text: 'AAPL - Apple Inc.'},
                    {value: 'MSFT', text: 'MSFT - Microsoft Corp.'},
                    {value: 'GOOGL', text: 'GOOGL - Alphabet Inc.'},
                    {value: 'AMZN', text: 'AMZN - Amazon.com Inc.'},
                    {value: 'TSLA', text: 'TSLA - Tesla Inc.'},
                    {value: 'META', text: 'META - Meta Platforms Inc.'},
                    {value: 'NVDA', text: 'NVDA - NVIDIA Corp.'}
                ],
                'crypto': [
                    {value: 'BTC', text: 'BTC - Bitcoin'},
                    {value: 'ETH', text: 'ETH - Ethereum'},
                    {value: 'BNB', text: 'BNB - Binance Coin'},
                    {value: 'ADA', text: 'ADA - Cardano'},
                    {value: 'SOL', text: 'SOL - Solana'},
                    {value: 'XRP', text: 'XRP - Ripple'},
                    {value: 'DOT', text: 'DOT - Polkadot'}
                ],
                'index': [
                    {value: 'SPY', text: 'SPY - S&P 500'},
                    {value: 'QQQ', text: 'QQQ - NASDAQ 100'},
                    {value: 'IWM', text: 'IWM - Russell 2000'},
                    {value: 'DIA', text: 'DIA - Dow Jones'},
                    {value: 'VTI', text: 'VTI - Total Stock Market'},
                    {value: 'GLD', text: 'GLD - Gold'},
                    {value: 'SLV', text: 'SLV - Silver'}
                ]
            };
            
            options[assetType].forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.text;
                symbolSelect.appendChild(optionElement);
            });
        }
        
        function addAsset() {
            const assetType = document.getElementById('asset-type').value;
            let symbol, fromCurrency, toCurrency;
            
            if (assetType === 'currency') {
                fromCurrency = document.getElementById('from-currency').value;
                toCurrency = document.getElementById('to-currency').value;
                symbol = `${fromCurrency}/${toCurrency}`;
            } else {
                symbol = document.getElementById('symbol').value;
                fromCurrency = null;
                toCurrency = null;
            }
            
            const assetId = `${assetType}_${symbol}_${fromCurrency}_${toCurrency}`;
            
            // Check if asset already exists
            if (assets.find(asset => asset.id === assetId)) {
                alert('This asset is already being monitored!');
                return;
            }
            
            const asset = {
                id: assetId,
                type: assetType,
                symbol: symbol,
                fromCurrency: fromCurrency,
                toCurrency: toCurrency
            };
            
            assets.push(asset);
            renderAssets();
            fetchAssetData(asset);
        }
        
        function removeAsset(assetId) {
            assets = assets.filter(asset => asset.id !== assetId);
            renderAssets();
        }
        
        function clearAssets() {
            assets = [];
            renderAssets();
        }
        
        function renderAssets() {
            const grid = document.getElementById('dashboard-grid');
            grid.innerHTML = '';
            
            assets.forEach(asset => {
                const card = document.createElement('div');
                card.className = 'asset-card loading';
                card.id = `card-${asset.id}`;
                card.innerHTML = `
                    <div class="asset-header">
                        <div class="asset-name">${asset.symbol}</div>
                        <div class="asset-type type-${asset.type}">${asset.type}</div>
                    </div>
                    <div class="price">Loading...</div>
                    <div class="signal signal-hold">HOLD</div>
                    <div class="confidence">Confidence: 0%</div>
                    <div class="reasoning">Loading market data...</div>
                    <div class="risk-level">
                        <div class="risk-indicator risk-medium"></div>
                        <span>Risk: MEDIUM</span>
                    </div>
                    <button class="btn" onclick="removeAsset('${asset.id}')" style="margin-top: 15px; width: 100%;">Remove</button>
                `;
                grid.appendChild(card);
            });
        }
        
        function fetchAssetData(asset) {
            const params = new URLSearchParams({
                asset_type: asset.type,
                symbol: asset.symbol,
                from_currency: asset.fromCurrency || '',
                to_currency: asset.toCurrency || ''
            });
            
            fetch(`/api/data?${params}`)
                .then(response => response.json())
                .then(data => {
                    updateAssetCard(asset.id, data);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    updateAssetCard(asset.id, {error: 'Failed to fetch data'});
                });
        }
        
        function updateAssetCard(assetId, data) {
            const card = document.getElementById(`card-${assetId}`);
            if (!card) return;
            
            card.classList.remove('loading');
            
            if (data.error) {
                card.innerHTML = `
                    <div class="error">Error: ${data.error}</div>
                    <button class="btn" onclick="removeAsset('${assetId}')" style="margin-top: 15px; width: 100%;">Remove</button>
                `;
                return;
            }
            
            const price = data.current_price.toFixed(data.asset_type === 'currency' ? 4 : 2);
            const signalClass = `signal-${data.action.toLowerCase()}`;
            const riskClass = `risk-${data.risk_level.toLowerCase()}`;
            const changePercent = data.price_change || 0;
            const changeClass = changePercent >= 0 ? 'positive' : 'negative';
            const changeSymbol = changePercent >= 0 ? '+' : '';
            
            card.innerHTML = `
                <div class="asset-header">
                    <div class="asset-name">${data.asset_name}</div>
                    <div class="asset-type type-${data.asset_type}">${data.asset_type}</div>
                </div>
                <div class="price">${price} <span style="font-size: 0.5em; color: ${changePercent >= 0 ? '#4caf50' : '#f44336'}">${changeSymbol}${changePercent.toFixed(2)}%</span></div>
                <div class="signal ${signalClass}">${data.action}</div>
                <div class="confidence">Confidence: ${data.confidence}%</div>
                <div class="reasoning">${data.reasoning}</div>
                <div class="risk-level">
                    <div class="risk-indicator ${riskClass}"></div>
                    <span>Risk: ${data.risk_level}</span>
                </div>
                <button class="btn" onclick="removeAsset('${assetId}')" style="margin-top: 15px; width: 100%;">Remove</button>
            `;
        }
        
        function refreshData() {
            assets.forEach(asset => {
                fetchAssetData(asset);
            });
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        }
        
        function startAutoRefresh() {
            updateInterval = setInterval(refreshData, 30000); // 30 seconds
        }
        
        function stopAutoRefresh() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        }
        
        // Initialize
        updateControls();
        startAutoRefresh();
        
        // Add some popular assets by default
        window.addEventListener('load', () => {
            // Add USD/CNY by default
            document.getElementById('asset-type').value = 'currency';
            document.getElementById('from-currency').value = 'USD';
            document.getElementById('to-currency').value = 'CNY';
            updateControls();
            addAsset();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard_page():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    try:
        asset_type = request.args.get('asset_type', 'currency')
        symbol = request.args.get('symbol', 'USD')
        from_currency = request.args.get('from_currency', 'USD')
        to_currency = request.args.get('to_currency', 'CNY')
        
        return jsonify(dashboard.get_market_data(asset_type, symbol, from_currency, to_currency))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('DASHBOARD_PORT', 8080))
    print("🚀 Starting Universal Trading Dashboard...")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=port, debug=False)
