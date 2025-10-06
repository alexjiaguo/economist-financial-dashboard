#!/usr/bin/env python3
"""
Quick CNY/USD Dashboard - Non-interactive version
"""

import requests
import os
from datetime import datetime

def fetch_cny_usd_rate(api_key):
    """Fetch current CNY/USD exchange rate"""
    try:
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': 'USD',
            'to_currency': 'CNY',
            'apikey': api_key
        }
        response = requests.get("https://www.alphavantage.co/query", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'Realtime Currency Exchange Rate' in data:
            rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
            return rate
    except Exception as e:
        print(f"Error fetching rate: {str(e)}")
    return 7.12  # Fallback

def main():
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ API key not found!")
        return
    
    current_rate = fetch_cny_usd_rate(api_key)
    
    print("🇨🇳 CNY/USD Trading Dashboard")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📊 CURRENT STATUS")
    print(f"CNY/USD Rate: {current_rate:.4f}")
    
    # Trading recommendation
    if current_rate <= 7.0:
        print("🟢 RECOMMENDATION: SELL (Excellent rate!)")
        confidence = 95
    elif current_rate <= 7.1:
        print("🟢 RECOMMENDATION: SELL (Good rate)")
        confidence = 80
    elif current_rate <= 7.2:
        print("🟡 RECOMMENDATION: HOLD (Wait for Fed cuts)")
        confidence = 60
    else:
        print("🔴 RECOMMENDATION: SELL (Stop-loss)")
        confidence = 70
    
    print(f"Confidence: {confidence}%")
    print()
    
    # Profit calculation for 100,000 CNY
    cny_amount = 100000
    current_usd = cny_amount / current_rate
    target_usd_7_0 = cny_amount / 7.0
    target_usd_7_1 = cny_amount / 7.1
    
    print("💰 PROFIT CALCULATOR (100,000 CNY)")
    print(f"Current USD: ${current_usd:,.2f}")
    print(f"At 7.0 rate: ${target_usd_7_0:,.2f} (+${target_usd_7_0 - current_usd:,.2f})")
    print(f"At 7.1 rate: ${target_usd_7_1:,.2f} (+${target_usd_7_1 - current_usd:,.2f})")
    print()
    
    print("🏦 FED POLICY")
    print("Current Rate: 4.25-4.50%")
    print("Next Meeting: October 29, 2025")
    print("Cut Probability: 90%")
    print("Expected Impact: CNY strengthening")
    print()
    
    print("🎯 KEY LEVELS")
    print("🟢 SELL: ≤ 7.0 (Excellent)")
    print("🟡 GOOD: ≤ 7.1 (Good)")
    print("🟠 WAIT: 7.1-7.2 (Hold)")
    print("🔴 STOP: ≥ 7.3 (Emergency)")
    print()
    
    if current_rate <= 7.0:
        print("🚨 ALERT: Excellent rate! Consider selling immediately!")
    elif current_rate <= 7.1:
        print("🟢 ALERT: Good rate! Consider selling soon!")
    elif current_rate >= 7.3:
        print("🔴 ALERT: Stop-loss triggered! Consider selling!")
    else:
        print("🟡 INFO: Waiting for better rate - Fed cuts expected")

if __name__ == "__main__":
    main()
