#!/usr/bin/env python3
"""
Simple CNY/USD Trading Dashboard - Terminal Version
Real-time monitoring without web interface
"""

import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import json
import os
import sys

class SimpleCNYUSDDashboard:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        
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
            print(f"❌ Error fetching CNY/USD rate: {str(e)}")
        return 7.12  # Fallback rate
    
    def fetch_historical_data(self, days: int = 30) -> pd.DataFrame:
        """Fetch historical CNY/USD data"""
        try:
            params = {
                'function': 'FX_DAILY',
                'from_symbol': 'USD',
                'to_symbol': 'CNY',
                'outputsize': 'compact',
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            time_series = data.get('Time Series FX (Daily)', {})
            if time_series:
                df = pd.DataFrame.from_dict(time_series, orient='index')
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()
                
                # Convert to float
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df.tail(days)
        except Exception as e:
            print(f"❌ Error fetching historical data: {str(e)}")
        return pd.DataFrame()
    
    def calculate_trading_signal(self, current_rate: float) -> dict:
        """Calculate trading signal and recommendation"""
        signals = {
            'action': 'HOLD',
            'confidence': 0,
            'target_rate': 0,
            'stop_loss': 0,
            'reasoning': '',
            'risk_level': 'MEDIUM'
        }
        
        if current_rate <= 7.0:
            signals.update({
                'action': 'SELL',
                'confidence': 95,
                'target_rate': current_rate,
                'stop_loss': 7.1,
                'reasoning': 'Excellent rate - CNY strengthening significantly',
                'risk_level': 'LOW'
            })
        elif current_rate <= 7.1:
            signals.update({
                'action': 'SELL',
                'confidence': 80,
                'target_rate': current_rate,
                'stop_loss': 7.2,
                'reasoning': 'Good rate - CNY strengthening expected',
                'risk_level': 'LOW'
            })
        elif current_rate <= 7.2:
            signals.update({
                'action': 'HOLD',
                'confidence': 60,
                'target_rate': 7.0,
                'stop_loss': 7.3,
                'reasoning': 'Wait for better rate - Fed cuts expected',
                'risk_level': 'MEDIUM'
            })
        else:
            signals.update({
                'action': 'SELL',
                'confidence': 70,
                'target_rate': current_rate,
                'stop_loss': 7.4,
                'reasoning': 'High rate - Consider selling to avoid further losses',
                'risk_level': 'HIGH'
            })
        
        return signals
    
    def calculate_profit(self, cny_amount: float, current_rate: float, target_rate: float) -> dict:
        """Calculate potential profit"""
        current_usd = cny_amount / current_rate
        target_usd = cny_amount / target_rate
        profit = target_usd - current_usd
        profit_pct = (profit / current_usd) * 100
        
        return {
            'current_usd': current_usd,
            'target_usd': target_usd,
            'profit': profit,
            'profit_pct': profit_pct
        }
    
    def display_dashboard(self, cny_amount: float = 100000):
        """Display the dashboard in terminal"""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🇨🇳 CNY/USD Trading Dashboard - Real-Time Monitoring")
        print("=" * 60)
        print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Fetch current data
        current_rate = self.fetch_cny_usd_rate()
        historical_data = self.fetch_historical_data(7)  # Last 7 days
        
        # Calculate signals
        signals = self.calculate_trading_signal(current_rate)
        
        # Display key metrics
        print("📊 CURRENT MARKET STATUS")
        print("-" * 30)
        print(f"CNY/USD Rate:     {current_rate:.4f}")
        print(f"Trading Signal:   {signals['action']} ({signals['confidence']}% confidence)")
        print(f"Risk Level:       {signals['risk_level']}")
        print(f"Target Rate:      {signals['target_rate']:.4f}")
        print(f"Stop Loss:        {signals['stop_loss']:.4f}")
        print()
        
        # Display recommendation
        print("🎯 TRADING RECOMMENDATION")
        print("-" * 30)
        if signals['action'] == 'SELL':
            print(f"🟢 {signals['action']} - {signals['reasoning']}")
        elif signals['action'] == 'HOLD':
            print(f"🟡 {signals['action']} - {signals['reasoning']}")
        print()
        
        # Display profit calculator
        print("💰 PROFIT CALCULATOR")
        print("-" * 30)
        print(f"CNY Amount:       {cny_amount:,.0f}")
        
        # Calculate profits for different scenarios
        scenarios = [
            ("Current Rate", current_rate),
            ("Target Rate (7.0)", 7.0),
            ("Good Rate (7.1)", 7.1),
            ("Stop Loss (7.3)", 7.3)
        ]
        
        for scenario_name, rate in scenarios:
            profit_data = self.calculate_profit(cny_amount, current_rate, rate)
            print(f"{scenario_name:20} ${profit_data['target_usd']:,.2f} ({profit_data['profit_pct']:+.2f}%)")
        print()
        
        # Display recent history
        if not historical_data.empty:
            print("📈 RECENT HISTORY (Last 7 Days)")
            print("-" * 30)
            recent_rates = historical_data['4. close'].tail(7)
            for date, rate in recent_rates.items():
                change = ((rate - current_rate) / current_rate) * 100
                print(f"{date.strftime('%Y-%m-%d')}    {rate:.4f} ({change:+.2f}%)")
            print()
        
        # Display Fed policy info
        print("🏦 FEDERAL RESERVE POLICY")
        print("-" * 30)
        print("Current Rate:      4.25-4.50%")
        print("Next Meeting:      October 29, 2025")
        print("Cut Probability:   90%")
        print("Expected Change:   -25 bps")
        print("CNY Impact:        Positive (USD weakening)")
        print()
        
        # Display market sentiment
        print("📊 MARKET SENTIMENT")
        print("-" * 30)
        print("Fed Funds Futures: Rate cuts expected (90%)")
        print("Bond Market:       Rate cuts expected")
        print("Equity Market:     Risk-on sentiment")
        print("Dollar Index:      Weakening trend")
        print("Overall:           BULLISH for CNY")
        print()
        
        # Display alerts
        print("🔔 ALERTS & NOTIFICATIONS")
        print("-" * 30)
        if current_rate <= 7.0:
            print("🚨 ALERT: Excellent rate! Consider selling immediately!")
        elif current_rate <= 7.1:
            print("🟢 ALERT: Good rate! Consider selling soon!")
        elif current_rate >= 7.3:
            print("🔴 ALERT: Stop-loss triggered! Consider selling!")
        else:
            print("🟡 INFO: Waiting for better rate - Fed cuts expected")
        
        # Countdown to next Fed meeting
        next_meeting = datetime(2025, 10, 29)
        days_until = (next_meeting - datetime.now()).days
        print(f"📅 Next Fed Meeting: {days_until} days (October 29, 2025)")
        print()
        
        # Display key levels
        print("📊 KEY LEVELS TO WATCH")
        print("-" * 30)
        print("🟢 SELL ZONE:     ≤ 7.0 (Excellent rate)")
        print("🟡 GOOD ZONE:     ≤ 7.1 (Good rate)")
        print("🟠 WAIT ZONE:     7.1-7.2 (Wait for better)")
        print("🔴 STOP LOSS:     ≥ 7.3 (Emergency exit)")
        print()
        
        return current_rate, signals
    
    def run_monitoring(self, cny_amount: float = 100000, refresh_interval: int = 60):
        """Run continuous monitoring"""
        print("🚀 Starting CNY/USD monitoring...")
        print(f"💰 Monitoring {cny_amount:,.0f} CNY")
        print(f"⏱️  Refresh interval: {refresh_interval} seconds")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                current_rate, signals = self.display_dashboard(cny_amount)
                
                # Check for alerts
                if current_rate <= 7.0:
                    print("🚨🚨🚨 EXCELLENT RATE ALERT! 🚨🚨🚨")
                    print("Consider selling immediately!")
                elif current_rate <= 7.1:
                    print("🟢 Good rate alert - consider selling soon!")
                elif current_rate >= 7.3:
                    print("🔴 Stop-loss alert - consider selling!")
                
                print(f"\n⏳ Refreshing in {refresh_interval} seconds...")
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped. Good luck with your trading!")

def main():
    """Main function"""
    print("🇨🇳 CNY/USD Trading Dashboard - Terminal Version")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ Alpha Vantage API key not found!")
        print("Please set the ALPHAVANTAGE_API_KEY environment variable")
        return
    
    # Initialize dashboard
    dashboard = SimpleCNYUSDDashboard(api_key)
    
    # Get user preferences
    try:
        cny_amount = float(input("Enter your CNY amount (default 100000): ") or "100000")
        refresh_interval = int(input("Enter refresh interval in seconds (default 60): ") or "60")
    except ValueError:
        cny_amount = 100000
        refresh_interval = 60
    
    # Run monitoring
    dashboard.run_monitoring(cny_amount, refresh_interval)

if __name__ == "__main__":
    main()
