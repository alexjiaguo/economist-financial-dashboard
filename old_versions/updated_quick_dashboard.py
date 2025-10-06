#!/usr/bin/env python3
"""
Updated Quick CNY/USD Dashboard - Enhanced version
"""

import requests
import os
from datetime import datetime
import time

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
        print(f"❌ Error fetching rate: {str(e)}")
    return 7.12  # Fallback

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def display_dashboard(api_key, cny_amount=100000):
    """Display the enhanced dashboard"""
    clear_screen()
    
    current_rate = fetch_cny_usd_rate(api_key)
    
    print("🇨🇳 CNY/USD Trading Dashboard - Enhanced")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Current status with color coding
    print("📊 CURRENT STATUS")
    print("-" * 30)
    print(f"CNY/USD Rate:     {current_rate:.4f}")
    
    # Trading recommendation with enhanced logic
    if current_rate <= 7.0:
        print("🟢 RECOMMENDATION: SELL (Excellent rate!)")
        confidence = 95
        emoji = "🚨"
        urgency = "IMMEDIATE ACTION"
    elif current_rate <= 7.1:
        print("🟢 RECOMMENDATION: SELL (Good rate)")
        confidence = 80
        emoji = "✅"
        urgency = "SOON"
    elif current_rate <= 7.2:
        print("🟡 RECOMMENDATION: HOLD (Wait for Fed cuts)")
        confidence = 60
        emoji = "⏳"
        urgency = "WAIT"
    else:
        print("🔴 RECOMMENDATION: SELL (Stop-loss)")
        confidence = 70
        emoji = "⚠️"
        urgency = "RISK MANAGEMENT"
    
    print(f"Confidence:       {confidence}%")
    print(f"Urgency:          {emoji} {urgency}")
    print()
    
    # Enhanced profit calculator
    print("💰 PROFIT CALCULATOR")
    print("-" * 30)
    print(f"CNY Amount:       {cny_amount:,.0f}")
    print()
    
    current_usd = cny_amount / current_rate
    scenarios = [
        ("Current Rate", current_rate, "Current"),
        ("Target Rate (7.0)", 7.0, "Excellent"),
        ("Good Rate (7.1)", 7.1, "Good"),
        ("Stop Loss (7.3)", 7.3, "Emergency")
    ]
    
    print("Scenario Analysis:")
    for scenario_name, rate, quality in scenarios:
        target_usd = cny_amount / rate
        profit = target_usd - current_usd
        profit_pct = (profit / current_usd) * 100
        
        # Color coding for profit
        if profit > 0:
            profit_str = f"+${profit:,.2f} (+{profit_pct:.2f}%)"
        else:
            profit_str = f"${profit:,.2f} ({profit_pct:.2f}%)"
        
        print(f"  {scenario_name:20} ${target_usd:,.2f} ({profit_str})")
    print()
    
    # Fed policy with countdown
    print("🏦 FEDERAL RESERVE POLICY")
    print("-" * 30)
    print("Current Rate:      4.25-4.50%")
    print("Next Meeting:      October 29, 2025")
    
    # Calculate days until next meeting
    next_meeting = datetime(2025, 10, 29)
    days_until = (next_meeting - datetime.now()).days
    print(f"Days Until:        {days_until} days")
    print("Cut Probability:   90%")
    print("Expected Change:   -25 bps")
    print("CNY Impact:        Positive (USD weakening)")
    print()
    
    # Enhanced key levels with current position
    print("📊 KEY LEVELS & CURRENT POSITION")
    print("-" * 30)
    levels = [
        (7.0, "🟢 SELL ZONE", "Excellent rate"),
        (7.1, "🟡 GOOD ZONE", "Good rate"),
        (7.2, "🟠 WAIT ZONE", "Wait for better"),
        (7.3, "🔴 STOP LOSS", "Emergency exit")
    ]
    
    for level, zone, description in levels:
        if current_rate <= level:
            position = "← YOU ARE HERE"
        else:
            position = ""
        print(f"{zone:15} ≤ {level:.1f} ({description}) {position}")
    print()
    
    # Market sentiment
    print("📈 MARKET SENTIMENT")
    print("-" * 30)
    print("Fed Funds Futures: Rate cuts expected (90%)")
    print("Bond Market:       Rate cuts expected")
    print("Equity Market:     Risk-on sentiment")
    print("Dollar Index:      Weakening trend")
    print("Overall:           BULLISH for CNY")
    print()
    
    # Enhanced alerts
    print("🔔 ALERTS & NOTIFICATIONS")
    print("-" * 30)
    if current_rate <= 7.0:
        print("🚨🚨🚨 EXCELLENT RATE ALERT! 🚨🚨🚨")
        print("   Consider selling immediately!")
        print("   This is the target rate you've been waiting for!")
    elif current_rate <= 7.1:
        print("🟢 GOOD RATE ALERT!")
        print("   Consider selling soon!")
        print("   Good opportunity to convert CNY to USD")
    elif current_rate >= 7.3:
        print("🔴 STOP-LOSS ALERT!")
        print("   Consider selling to limit losses!")
        print("   Rate has reached emergency exit level")
    else:
        print("🟡 WAITING FOR BETTER RATE")
        print("   Fed cuts expected to strengthen CNY")
        print("   Monitor closely for rate drops below 7.0")
    
    print()
    print("💡 NEXT STEPS:")
    if current_rate <= 7.0:
        print("   1. ✅ SELL CNY immediately")
        print("   2. ✅ You've reached your target rate")
        print("   3. ✅ Maximize your USD gains")
    elif current_rate <= 7.1:
        print("   1. 🟢 Consider selling soon")
        print("   2. 🟢 Good rate for conversion")
        print("   3. 🟢 Don't wait too long")
    else:
        print("   1. ⏳ Wait for rate to drop below 7.0")
        print("   2. ⏳ Monitor Fed meeting on October 29")
        print("   3. ⏳ Set alerts for rate changes")
    
    print()
    print("🔄 Dashboard refreshes automatically every 60 seconds")
    print("   Press Ctrl+C to stop monitoring")

def main():
    """Main function with continuous monitoring"""
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ Alpha Vantage API key not found!")
        print("Please set the ALPHAVANTAGE_API_KEY environment variable")
        return
    
    print("🚀 Starting Enhanced CNY/USD Dashboard...")
    print("💰 Monitoring 100,000 CNY (default)")
    print("⏱️  Auto-refresh every 60 seconds")
    print("Press Ctrl+C to stop")
    print()
    time.sleep(2)
    
    try:
        while True:
            display_dashboard(api_key)
            time.sleep(60)  # Refresh every 60 seconds
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped. Good luck with your trading!")
        print("🎯 Remember: The goal is to maximize USD gains!")

if __name__ == "__main__":
    main()
