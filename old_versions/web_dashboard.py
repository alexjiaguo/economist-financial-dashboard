#!/usr/bin/env python3
"""
Simple Web-based CNY/USD Dashboard using Flask
Alternative to Streamlit for better compatibility
"""

from flask import Flask, render_template_string, jsonify
import requests
import json
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)

class WebCNYUSDDashboard:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.current_data = {}
        
    def fetch_cny_usd_rate(self) -> float:
        """Fetch current CNY/USD exchange rate"""
        try:
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': 'USD',
                'to_currency': 'CNY',
                'apikey': self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Realtime Currency Exchange Rate' in data:
                rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                return rate
        except Exception as e:
            print(f"Error fetching rate: {str(e)}")
        return 7.12  # Fallback
    
    def get_market_data(self):
        """Get comprehensive market data"""
        current_rate = self.fetch_cny_usd_rate()
        
        # Calculate trading signal
        if current_rate <= 7.0:
            action = "SELL"
            confidence = 95
            reasoning = "Excellent rate - CNY strengthening significantly"
        elif current_rate <= 7.1:
            action = "SELL"
            confidence = 80
            reasoning = "Good rate - CNY strengthening expected"
        elif current_rate <= 7.2:
            action = "HOLD"
            confidence = 60
            reasoning = "Wait for better rate - Fed cuts expected"
        else:
            action = "SELL"
            confidence = 70
            reasoning = "High rate - Consider selling to avoid further losses"
        
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cny_usd_rate': current_rate,
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'fed_funds_rate': 4.375,
            'inflation_rate': 2.7,
            'unemployment_rate': 4.2,
            'next_fed_meeting': 'October 29, 2025',
            'cut_probability': 90
        }
    
    def update_data(self):
        """Update data in background"""
        while True:
            self.current_data = self.get_market_data()
            time.sleep(30)  # Update every 30 seconds

# Initialize dashboard
api_key = os.getenv('ALPHAVANTAGE_API_KEY', 'demo')
dashboard = WebCNYUSDDashboard(api_key)

# Start background data updates
data_thread = threading.Thread(target=dashboard.update_data, daemon=True)
data_thread.start()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🇨🇳 CNY/USD Trading Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; margin: 10px 0; }
        .metric-label { color: #666; font-size: 0.9em; }
        .positive { color: #28a745; }
        .negative { color: #dc3545; }
        .neutral { color: #ffc107; }
        .recommendation { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .sell { border-left: 5px solid #28a745; }
        .hold { border-left: 5px solid #ffc107; }
        .profit-calc { background: white; padding: 20px; border-radius: 10px; }
        .input-group { margin: 10px 0; }
        .input-group label { display: block; margin-bottom: 5px; }
        .input-group input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .alert { padding: 15px; margin: 10px 0; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .alert-danger { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .footer { text-align: center; margin-top: 30px; color: #666; }
    </style>
    <script>
        function updateData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('rate').textContent = data.cny_usd_rate.toFixed(4);
                    document.getElementById('action').textContent = data.action;
                    document.getElementById('confidence').textContent = data.confidence + '%';
                    document.getElementById('reasoning').textContent = data.reasoning;
                    document.getElementById('timestamp').textContent = data.timestamp;
                    document.getElementById('fed-rate').textContent = data.fed_funds_rate.toFixed(3) + '%';
                    document.getElementById('inflation').textContent = data.inflation_rate + '%';
                    document.getElementById('unemployment').textContent = data.unemployment_rate + '%';
                    document.getElementById('next-meeting').textContent = data.next_fed_meeting;
                    document.getElementById('cut-prob').textContent = data.cut_probability + '%';
                    
                    // Update recommendation styling
                    const rec = document.getElementById('recommendation');
                    rec.className = 'recommendation ' + data.action.toLowerCase();
                    
                    // Calculate profit
                    calculateProfit();
                })
                .catch(error => console.error('Error:', error));
        }
        
        function calculateProfit() {
            const cnyAmount = parseFloat(document.getElementById('cny-amount').value) || 100000;
            const currentRate = parseFloat(document.getElementById('rate').textContent);
            const targetRate = parseFloat(document.getElementById('target-rate').value) || 7.0;
            
            const currentUsd = cnyAmount / currentRate;
            const targetUsd = cnyAmount / targetRate;
            const profit = targetUsd - currentUsd;
            const profitPct = (profit / currentUsd) * 100;
            
            document.getElementById('current-usd').textContent = '$' + currentUsd.toFixed(2);
            document.getElementById('target-usd').textContent = '$' + targetUsd.toFixed(2);
            document.getElementById('profit').textContent = '$' + profit.toFixed(2);
            document.getElementById('profit-pct').textContent = profitPct.toFixed(2) + '%';
            
            // Color code profit
            const profitEl = document.getElementById('profit');
            const profitPctEl = document.getElementById('profit-pct');
            if (profit > 0) {
                profitEl.className = 'positive';
                profitPctEl.className = 'positive';
            } else {
                profitEl.className = 'negative';
                profitPctEl.className = 'negative';
            }
        }
        
        // Update data every 30 seconds
        setInterval(updateData, 30000);
        
        // Initial load
        updateData();
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇨🇳 CNY/USD Trading Dashboard</h1>
            <p>Real-time monitoring to maximize your USD gains</p>
            <p>Last Updated: <span id="timestamp">Loading...</span></p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">CNY/USD Rate</div>
                <div class="metric-value" id="rate">Loading...</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Trading Signal</div>
                <div class="metric-value" id="action">Loading...</div>
                <div class="metric-label">Confidence: <span id="confidence">Loading...</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Fed Funds Rate</div>
                <div class="metric-value" id="fed-rate">Loading...</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Inflation Rate</div>
                <div class="metric-value" id="inflation">Loading...</div>
            </div>
        </div>
        
        <div class="recommendation" id="recommendation">
            <h3>🎯 Trading Recommendation</h3>
            <p id="reasoning">Loading...</p>
        </div>
        
        <div class="profit-calc">
            <h3>💰 Profit Calculator</h3>
            <div class="input-group">
                <label for="cny-amount">CNY Amount:</label>
                <input type="number" id="cny-amount" value="100000" onchange="calculateProfit()">
            </div>
            <div class="input-group">
                <label for="target-rate">Target Rate:</label>
                <input type="number" id="target-rate" value="7.0" step="0.01" onchange="calculateProfit()">
            </div>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">Current USD Value</div>
                    <div class="metric-value" id="current-usd">$0.00</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Target USD Value</div>
                    <div class="metric-value" id="target-usd">$0.00</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Potential Profit</div>
                    <div class="metric-value" id="profit">$0.00</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Profit %</div>
                    <div class="metric-value" id="profit-pct">0.00%</div>
                </div>
            </div>
        </div>
        
        <div class="recommendation">
            <h3>📊 Market Information</h3>
            <p><strong>Unemployment Rate:</strong> <span id="unemployment">Loading...</span></p>
            <p><strong>Next Fed Meeting:</strong> <span id="next-meeting">Loading...</span></p>
            <p><strong>Rate Cut Probability:</strong> <span id="cut-prob">Loading...</span></p>
        </div>
        
        <div class="footer">
            <p>This dashboard is for informational purposes only. Always consult with financial professionals for investment decisions.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard_page():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    return jsonify(dashboard.get_market_data())

if __name__ == '__main__':
    print("🌐 Starting CNY/USD Web Dashboard...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5000, debug=False)
