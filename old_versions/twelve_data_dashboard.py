#!/usr/bin/env python3
"""
Universal Trading Dashboard - Multi-Asset Trading Platform
Powered by Twelve Data API (800 free requests/day)
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

class TwelveDataDashboard:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.twelvedata.com"
        self.current_data = {}
        self.last_update = None
        
        # Asset categories
        self.currencies = {
            'USD/CNY': 'US Dollar to Chinese Yuan',
            'EUR/USD': 'Euro to US Dollar',
            'GBP/USD': 'British Pound to US Dollar',
            'USD/JPY': 'US Dollar to Japanese Yen',
            'AUD/USD': 'Australian Dollar to US Dollar',
            'USD/CAD': 'US Dollar to Canadian Dollar',
            'USD/CHF': 'US Dollar to Swiss Franc',
            'NZD/USD': 'New Zealand Dollar to US Dollar',
            'EUR/GBP': 'Euro to British Pound',
            'EUR/JPY': 'Euro to Japanese Yen',
            'GBP/JPY': 'British Pound to Japanese Yen',
            'CNY/USD': 'Chinese Yuan to US Dollar'
        }
        
        self.stocks = {
            'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp.', 'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.', 'TSLA': 'Tesla Inc.', 'META': 'Meta Platforms Inc.',
            'NVDA': 'NVIDIA Corp.', 'BRK.A': 'Berkshire Hathaway', 'JPM': 'JPMorgan Chase',
            'V': 'Visa Inc.', 'PG': 'Procter & Gamble', 'MA': 'Mastercard Inc.',
            'HD': 'Home Depot Inc.', 'DIS': 'Walt Disney Co.', 'PYPL': 'PayPal Holdings',
            'ADBE': 'Adobe Inc.', 'CRM': 'Salesforce Inc.', 'NFLX': 'Netflix Inc.',
            'INTC': 'Intel Corp.', 'AMD': 'AMD Inc.'
        }
        
        self.indices = {
            'SPX': 'S&P 500', 'NDX': 'NASDAQ 100', 'DJI': 'Dow Jones',
            'RUT': 'Russell 2000', 'VIX': 'Volatility Index', 'FTSE': 'FTSE 100',
            'DAX': 'DAX Index', 'N225': 'Nikkei 225', 'HSI': 'Hang Seng',
            'SSE': 'Shanghai Composite'
        }
        
        self.cryptocurrencies = {
            'BTC/USD': 'Bitcoin', 'ETH/USD': 'Ethereum', 'BNB/USD': 'Binance Coin',
            'ADA/USD': 'Cardano', 'SOL/USD': 'Solana', 'XRP/USD': 'Ripple',
            'DOT/USD': 'Polkadot', 'DOGE/USD': 'Dogecoin', 'AVAX/USD': 'Avalanche',
            'MATIC/USD': 'Polygon', 'LINK/USD': 'Chainlink', 'UNI/USD': 'Uniswap',
            'LTC/USD': 'Litecoin', 'BCH/USD': 'Bitcoin Cash', 'ATOM/USD': 'Cosmos'
        }
    
    def fetch_quote(self, symbol: str, asset_type: str = 'stock') -> tuple:
        """Fetch real-time quote from Twelve Data"""
        try:
            # Determine the interval based on asset type
            interval = '1min' if asset_type == 'crypto' else '1day'
            
            params = {
                'symbol': symbol,
                'apikey': self.api_key,
                'interval': interval
            }
            
            # Use quote endpoint for real-time data
            response = requests.get(f"{self.base_url}/quote", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"Twelve Data Response for {symbol}: {data}")
            
            if 'price' in data or 'close' in data:
                price = float(data.get('price') or data.get('close'))
                change_percent = float(data.get('percent_change', 0))
                return price, change_percent, None
            elif 'code' in data and data['code'] == 429:
                return None, None, "⚠️ API rate limit reached. Please wait a minute."
            elif 'code' in data and data['code'] == 401:
                return None, None, "⚠️ Invalid API key. Please check your Twelve Data API key."
            elif 'message' in data:
                return None, None, f"API Error: {data['message']}"
            elif 'status' in data and data['status'] == 'error':
                return None, None, f"Error: {data.get('message', 'Unknown error')}"
            else:
                return None, None, f"Unexpected response: {data}"
        except Exception as e:
            error_msg = f"Error fetching {symbol}: {str(e)}"
            print(error_msg)
            return None, None, error_msg
    
    def fetch_time_series(self, symbol: str, asset_type: str = 'stock') -> tuple:
        """Fetch time series data to calculate price change"""
        try:
            params = {
                'symbol': symbol,
                'apikey': self.api_key,
                'interval': '1day',
                'outputsize': 2  # Get last 2 days to calculate change
            }
            
            response = requests.get(f"{self.base_url}/time_series", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'values' in data and len(data['values']) >= 2:
                current_price = float(data['values'][0]['close'])
                prev_price = float(data['values'][1]['close'])
                change_percent = ((current_price - prev_price) / prev_price) * 100
                return current_price, change_percent, None
            elif 'code' in data and data['code'] == 429:
                return None, None, "⚠️ API rate limit reached. Please wait a minute."
            elif 'code' in data and data['code'] == 401:
                return None, None, "⚠️ Invalid API key. Please check your Twelve Data API key."
            else:
                # Fallback to quote endpoint
                return self.fetch_quote(symbol, asset_type)
        except Exception as e:
            # Fallback to quote endpoint
            return self.fetch_quote(symbol, asset_type)
    
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
    
    def get_market_data(self, asset_type: str, symbol: str):
        """Get comprehensive market data for any asset"""
        current_price = 0
        asset_name = ""
        price_change = 0
        error_message = None
        
        # Get asset name and fetch data based on type
        if asset_type == 'currency':
            asset_name = self.currencies.get(symbol, symbol)
            current_price, price_change, error_message = self.fetch_quote(symbol, 'forex')
        elif asset_type == 'stock':
            asset_name = self.stocks.get(symbol, symbol)
            current_price, price_change, error_message = self.fetch_time_series(symbol, 'stock')
        elif asset_type == 'crypto':
            asset_name = self.cryptocurrencies.get(symbol, symbol)
            current_price, price_change, error_message = self.fetch_quote(symbol, 'crypto')
        elif asset_type == 'index':
            asset_name = self.indices.get(symbol, symbol)
            current_price, price_change, error_message = self.fetch_time_series(symbol, 'index')
        
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
            'action': signals['action'],
            'confidence': signals['confidence'],
            'reasoning': signals['reasoning'],
            'risk_level': signals['risk_level'],
            'target_price': signals['target_price'],
            'stop_loss': signals['stop_loss']
        }

# Initialize dashboard
api_key = os.getenv('TWELVEDATA_API_KEY', 'demo')
dashboard = TwelveDataDashboard(api_key)

# Modern HTML Template (same as before, with updated title)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Trading Dashboard - Twelve Data</title>
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
        
        .header .api-info {
            margin-top: 10px;
            font-size: 0.9rem;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
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
            <div class="api-info">✨ Powered by Twelve Data • 800 free requests/day</div>
        </div>
        
        <div class="controls">
            <div class="control-row">
                <div class="control-group">
                    <label for="asset-type">Asset Type</label>
                    <select id="asset-type" onchange="updateSymbolOptions()">
                        <option value="currency">Currency Pair</option>
                        <option value="stock">Stock</option>
                        <option value="crypto">Cryptocurrency</option>
                        <option value="index">Index</option>
                    </select>
                </div>
                
                <div class="control-group" id="symbol-controls">
                    <label for="symbol">Symbol</label>
                    <select id="symbol">
                        <!-- Will be populated by JavaScript -->
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
        
        const symbolOptions = {
            'currency': [
                {value: 'USD/CNY', text: 'USD/CNY - US Dollar to Chinese Yuan'},
                {value: 'EUR/USD', text: 'EUR/USD - Euro to US Dollar'},
                {value: 'GBP/USD', text: 'GBP/USD - British Pound to US Dollar'},
                {value: 'USD/JPY', text: 'USD/JPY - US Dollar to Japanese Yen'},
                {value: 'AUD/USD', text: 'AUD/USD - Australian Dollar to US Dollar'},
                {value: 'USD/CAD', text: 'USD/CAD - US Dollar to Canadian Dollar'},
                {value: 'USD/CHF', text: 'USD/CHF - US Dollar to Swiss Franc'},
                {value: 'NZD/USD', text: 'NZD/USD - New Zealand Dollar to US Dollar'},
                {value: 'EUR/GBP', text: 'EUR/GBP - Euro to British Pound'},
                {value: 'EUR/JPY', text: 'EUR/JPY - Euro to Japanese Yen'},
                {value: 'GBP/JPY', text: 'GBP/JPY - British Pound to Japanese Yen'},
                {value: 'CNY/USD', text: 'CNY/USD - Chinese Yuan to US Dollar'}
            ],
            'stock': [
                {value: 'AAPL', text: 'AAPL - Apple Inc.'},
                {value: 'MSFT', text: 'MSFT - Microsoft Corp.'},
                {value: 'GOOGL', text: 'GOOGL - Alphabet Inc.'},
                {value: 'AMZN', text: 'AMZN - Amazon.com Inc.'},
                {value: 'TSLA', text: 'TSLA - Tesla Inc.'},
                {value: 'META', text: 'META - Meta Platforms Inc.'},
                {value: 'NVDA', text: 'NVDA - NVIDIA Corp.'},
                {value: 'JPM', text: 'JPM - JPMorgan Chase'},
                {value: 'V', text: 'V - Visa Inc.'},
                {value: 'PG', text: 'PG - Procter & Gamble'}
            ],
            'crypto': [
                {value: 'BTC/USD', text: 'BTC/USD - Bitcoin'},
                {value: 'ETH/USD', text: 'ETH/USD - Ethereum'},
                {value: 'BNB/USD', text: 'BNB/USD - Binance Coin'},
                {value: 'ADA/USD', text: 'ADA/USD - Cardano'},
                {value: 'SOL/USD', text: 'SOL/USD - Solana'},
                {value: 'XRP/USD', text: 'XRP/USD - Ripple'},
                {value: 'DOT/USD', text: 'DOT/USD - Polkadot'}
            ],
            'index': [
                {value: 'SPX', text: 'SPX - S&P 500'},
                {value: 'NDX', text: 'NDX - NASDAQ 100'},
                {value: 'DJI', text: 'DJI - Dow Jones'},
                {value: 'RUT', text: 'RUT - Russell 2000'},
                {value: 'VIX', text: 'VIX - Volatility Index'},
                {value: 'FTSE', text: 'FTSE - FTSE 100'},
                {value: 'DAX', text: 'DAX - DAX Index'}
            ]
        };
        
        function updateSymbolOptions() {
            const assetType = document.getElementById('asset-type').value;
            const symbolSelect = document.getElementById('symbol');
            symbolSelect.innerHTML = '';
            
            symbolOptions[assetType].forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.text;
                symbolSelect.appendChild(optionElement);
            });
        }
        
        function addAsset() {
            const assetType = document.getElementById('asset-type').value;
            const symbol = document.getElementById('symbol').value;
            const assetId = `${assetType}_${symbol.replace('/', '_')}`;
            
            if (assets.find(asset => asset.id === assetId)) {
                alert('This asset is already being monitored!');
                return;
            }
            
            const asset = {
                id: assetId,
                type: assetType,
                symbol: symbol
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
                symbol: asset.symbol
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
                    <div class="error">${data.error}</div>
                    <button class="btn" onclick="removeAsset('${assetId}')" style="margin-top: 15px; width: 100%;">Remove</button>
                `;
                return;
            }
            
            const price = data.current_price.toFixed(data.asset_type === 'currency' || data.asset_type === 'crypto' ? 4 : 2);
            const signalClass = `signal-${data.action.toLowerCase()}`;
            const riskClass = `risk-${data.risk_level.toLowerCase()}`;
            const changePercent = data.price_change || 0;
            const changeColor = changePercent >= 0 ? '#4caf50' : '#f44336';
            const changeSymbol = changePercent >= 0 ? '+' : '';
            
            card.innerHTML = `
                <div class="asset-header">
                    <div class="asset-name">${data.asset_name}</div>
                    <div class="asset-type type-${data.asset_type}">${data.asset_type}</div>
                </div>
                <div class="price">${price} <span style="font-size: 0.5em; color: ${changeColor}">${changeSymbol}${changePercent.toFixed(2)}%</span></div>
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
            updateInterval = setInterval(refreshData, 30000);
        }
        
        // Initialize
        updateSymbolOptions();
        startAutoRefresh();
        
        // Add USD/CNY by default
        window.addEventListener('load', () => {
            document.getElementById('asset-type').value = 'currency';
            updateSymbolOptions();
            document.getElementById('symbol').value = 'USD/CNY';
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
        symbol = request.args.get('symbol', 'USD/CNY')
        
        return jsonify(dashboard.get_market_data(asset_type, symbol))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('DASHBOARD_PORT', 8080))
    print("🚀 Starting Universal Trading Dashboard (Twelve Data)...")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("✨ Free tier: 800 requests/day")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=port, debug=False)

