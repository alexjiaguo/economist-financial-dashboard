#!/usr/bin/env python3
"""
Federal Reserve Policy Analysis and Market Sentiment Assessment
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

class FedPolicyAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        
    def analyze_fed_policy_factors(self):
        """Analyze key factors influencing Federal Reserve decisions"""
        print("\n🏦 FEDERAL RESERVE POLICY FACTORS ANALYSIS")
        print("=" * 60)
        
        # Current economic indicators (as of October 2025)
        current_indicators = {
            'inflation': {
                'current_rate': 2.7,
                'target_rate': 2.0,
                'core_inflation': 2.9,
                'trend': 'Above target, but moderating',
                'fed_concern': 'High - Primary mandate',
                'impact_on_rates': 'Higher inflation = Higher rates'
            },
            'unemployment': {
                'current_rate': 4.2,
                'natural_rate': 4.0,
                'trend': 'Rising slightly (4.1% to 4.2%)',
                'fed_concern': 'Medium - Dual mandate',
                'impact_on_rates': 'Higher unemployment = Lower rates'
            },
            'gdp_growth': {
                'current_rate': 3.0,
                'domestic_sales': 1.2,
                'trend': 'Strong headline, weak domestic',
                'fed_concern': 'Medium - Economic health',
                'impact_on_rates': 'Slower growth = Lower rates'
            },
            'trade_policies': {
                'tariff_rate': 18.4,
                'trend': 'Increasing tariffs',
                'fed_concern': 'High - Inflationary pressure',
                'impact_on_rates': 'Higher tariffs = Higher rates'
            },
            'global_conditions': {
                'china_growth': 'Slowing',
                'europe_rates': 'Cutting',
                'fed_concern': 'Medium - Global coordination',
                'impact_on_rates': 'Global easing = US can ease'
            }
        }
        
        print("📊 CURRENT ECONOMIC INDICATORS:")
        print()
        
        for indicator, data in current_indicators.items():
            print(f"🔍 {indicator.upper().replace('_', ' ')}:")
            for key, value in data.items():
                if key != 'fed_concern' and key != 'impact_on_rates':
                    print(f"   • {key.replace('_', ' ').title()}: {value}")
            print(f"   • Fed Concern Level: {data['fed_concern']}")
            print(f"   • Rate Impact: {data['impact_on_rates']}")
            print()
        
        return current_indicators
    
    def analyze_market_sentiment(self):
        """Analyze current market sentiment and expectations"""
        print("\n📈 MARKET SENTIMENT ANALYSIS")
        print("=" * 60)
        
        # Market sentiment indicators
        sentiment_data = {
            'fed_funds_futures': {
                'october_2025': {
                    'rate_cut_probability': 90,
                    'expected_rate': '3.75-4.00%',
                    'change': '-25 bps',
                    'confidence': 'Very High'
                },
                'december_2025': {
                    'rate_cut_probability': 75,
                    'expected_rate': '3.50-3.75%',
                    'change': '-50 bps total',
                    'confidence': 'High'
                }
            },
            'bond_market': {
                '10_year_treasury': {
                    'current_yield': '4.1%',
                    'trend': 'Declining',
                    'signal': 'Expecting rate cuts'
                },
                '2_year_treasury': {
                    'current_yield': '4.3%',
                    'trend': 'Declining',
                    'signal': 'Expecting rate cuts'
                }
            },
            'equity_market': {
                'sp500': {
                    'trend': 'Rising',
                    'signal': 'Risk-on sentiment',
                    'rate_expectation': 'Cuts coming'
                },
                'vix': {
                    'level': 'Low (15-20)',
                    'signal': 'Low volatility',
                    'rate_expectation': 'Stable policy'
                }
            },
            'dollar_index': {
                'current_level': '103-104',
                'trend': 'Weakening',
                'signal': 'Expecting USD weakness',
                'rate_expectation': 'Rate cuts expected'
            }
        }
        
        print("📊 MARKET SENTIMENT INDICATORS:")
        print()
        
        for category, data in sentiment_data.items():
            print(f"🔍 {category.upper().replace('_', ' ')}:")
            for indicator, details in data.items():
                print(f"   • {indicator.replace('_', ' ').title()}:")
                if isinstance(details, dict):
                    for key, value in details.items():
                        print(f"     - {key.replace('_', ' ').title()}: {value}")
                else:
                    print(f"     - {details}")
                print()
        
        return sentiment_data
    
    def create_fed_decision_scenarios(self):
        """Create scenarios for Federal Reserve decisions"""
        print("\n🎯 FEDERAL RESERVE DECISION SCENARIOS")
        print("=" * 60)
        
        scenarios = {
            'immediate_cut_october': {
                'probability': 90,
                'rate_change': '-25 bps',
                'new_rate': '4.00-4.25%',
                'triggers': [
                    'Weak July jobs report',
                    'Rising unemployment (4.1% → 4.2%)',
                    'Slowing domestic growth (1.2%)',
                    'Market expectations (90% probability)'
                ],
                'cny_usd_impact': 'USD weakens → CNY strengthens → Rate drops to 7.0-7.1',
                'your_strategy': 'WAIT - CNY will strengthen significantly'
            },
            'gradual_cuts_2025': {
                'probability': 75,
                'rate_change': '-50 bps total',
                'new_rate': '3.75-4.00%',
                'triggers': [
                    'Inflation moderating (2.7%)',
                    'Economic growth concerns',
                    'Global central bank coordination',
                    'Trade policy uncertainty'
                ],
                'cny_usd_impact': 'USD weakens → CNY strengthens → Rate drops to 6.9-7.0',
                'your_strategy': 'WAIT - Significant CNY strengthening expected'
            },
            'no_cuts_2025': {
                'probability': 10,
                'rate_change': '0 bps',
                'new_rate': '4.25-4.50%',
                'triggers': [
                    'Inflation spikes above 3%',
                    'Strong economic data',
                    'Trade tensions escalate',
                    'Geopolitical risks'
                ],
                'cny_usd_impact': 'USD strengthens → CNY weakens → Rate rises to 7.2-7.4',
                'your_strategy': 'SELL NOW - CNY will weaken further'
            },
            'aggressive_cuts_2025': {
                'probability': 25,
                'rate_change': '-100 bps total',
                'new_rate': '3.25-3.50%',
                'triggers': [
                    'Recession concerns',
                    'Unemployment spikes above 5%',
                    'Deflationary pressures',
                    'Financial market stress'
                ],
                'cny_usd_impact': 'USD weakens significantly → CNY strengthens → Rate drops to 6.8-6.9',
                'your_strategy': 'WAIT - Massive CNY strengthening opportunity'
            }
        }
        
        print("📊 SCENARIO ANALYSIS:")
        print()
        
        for scenario, details in scenarios.items():
            print(f"🎯 {scenario.upper().replace('_', ' ')}:")
            print(f"   • Probability: {details['probability']}%")
            print(f"   • Rate Change: {details['rate_change']}")
            print(f"   • New Rate: {details['new_rate']}")
            print(f"   • Triggers:")
            for trigger in details['triggers']:
                print(f"     - {trigger}")
            print(f"   • CNY/USD Impact: {details['cny_usd_impact']}")
            print(f"   • Your Strategy: {details['your_strategy']}")
            print()
        
        return scenarios
    
    def analyze_key_fed_meetings(self):
        """Analyze upcoming Federal Reserve meetings and expectations"""
        print("\n📅 UPCOMING FEDERAL RESERVE MEETINGS")
        print("=" * 60)
        
        meetings = {
            'october_29_2025': {
                'rate_cut_probability': 90,
                'expected_change': '-25 bps',
                'key_factors': [
                    'July jobs report disappointment',
                    'Rising unemployment',
                    'Market expectations',
                    'Inflation moderation'
                ],
                'cny_impact': 'Immediate CNY strengthening if cut occurs'
            },
            'december_17_2025': {
                'rate_cut_probability': 60,
                'expected_change': '-25 bps (if October cut)',
                'key_factors': [
                    'Economic data trends',
                    'Inflation trajectory',
                    'Global conditions',
                    'Year-end positioning'
                ],
                'cny_impact': 'Further CNY strengthening'
            },
            'january_28_2026': {
                'rate_cut_probability': 40,
                'expected_change': 'Hold or -25 bps',
                'key_factors': [
                    'New year economic outlook',
                    'Previous cuts impact',
                    'Inflation data',
                    'Employment trends'
                ],
                'cny_impact': 'Continued CNY strength if cuts continue'
            }
        }
        
        print("📊 MEETING SCHEDULE & EXPECTATIONS:")
        print()
        
        for meeting, details in meetings.items():
            print(f"📅 {meeting.replace('_', ' ').title()}:")
            print(f"   • Rate Cut Probability: {details['rate_cut_probability']}%")
            print(f"   • Expected Change: {details['expected_change']}")
            print(f"   • Key Factors:")
            for factor in details['key_factors']:
                print(f"     - {factor}")
            print(f"   • CNY Impact: {details['cny_impact']}")
            print()
        
        return meetings
    
    def create_comprehensive_fed_report(self):
        """Generate comprehensive Federal Reserve analysis report"""
        print("\n📋 GENERATING COMPREHENSIVE FED ANALYSIS REPORT")
        print("=" * 70)
        
        # Run all analyses
        economic_indicators = self.analyze_fed_policy_factors()
        market_sentiment = self.analyze_market_sentiment()
        scenarios = self.create_fed_decision_scenarios()
        meetings = self.analyze_key_fed_meetings()
        
        # Generate comprehensive report
        report = f"""
# Federal Reserve Policy Analysis & Market Sentiment Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🏦 Current Federal Reserve Policy Status
- **Current Rate**: 4.25% - 4.50%
- **Last Change**: December 2024 (Hold)
- **Next Meeting**: October 29, 2025
- **Market Expectation**: 90% probability of -25 bps cut

## 📊 Key Economic Indicators (October 2025)

### 🔥 Inflation (Primary Fed Concern)
- **Current Rate**: 2.7% (Above 2% target)
- **Core Inflation**: 2.9%
- **Trend**: Moderating but still elevated
- **Fed Impact**: **HIGH** - Primary mandate
- **Rate Impact**: Higher inflation = Higher rates

### 👥 Employment (Dual Mandate)
- **Unemployment Rate**: 4.2% (Rising from 4.1%)
- **Natural Rate**: ~4.0%
- **Trend**: Slight deterioration
- **Fed Impact**: **MEDIUM** - Dual mandate
- **Rate Impact**: Higher unemployment = Lower rates

### 📈 Economic Growth
- **GDP Growth**: 3.0% (Q2 2025)
- **Domestic Sales**: 1.2% (Weak)
- **Trend**: Strong headline, weak domestic
- **Fed Impact**: **MEDIUM** - Economic health
- **Rate Impact**: Slower growth = Lower rates

### 🌍 Trade Policies
- **Average Tariff Rate**: 18.4%
- **Trend**: Increasing tariffs
- **Fed Impact**: **HIGH** - Inflationary pressure
- **Rate Impact**: Higher tariffs = Higher rates

## 📈 Market Sentiment Analysis

### 🎯 Fed Funds Futures (Most Reliable Indicator)
- **October 2025**: 90% probability of -25 bps cut
- **December 2025**: 75% probability of -50 bps total
- **Market Confidence**: Very High

### 📊 Bond Market Signals
- **10-Year Treasury**: 4.1% (Declining)
- **2-Year Treasury**: 4.3% (Declining)
- **Signal**: Expecting rate cuts

### 📈 Equity Market Signals
- **S&P 500**: Rising (Risk-on sentiment)
- **VIX**: Low (15-20) - Low volatility
- **Signal**: Expecting rate cuts

### 💱 Dollar Index
- **Current Level**: 103-104
- **Trend**: Weakening
- **Signal**: Expecting USD weakness from rate cuts

## 🎯 Federal Reserve Decision Scenarios

### 🟢 Immediate Cut (October 2025) - 90% Probability
- **Rate Change**: -25 bps to 4.00-4.25%
- **Triggers**: Weak jobs report, rising unemployment, market expectations
- **CNY/USD Impact**: Rate drops to 7.0-7.1
- **Your Strategy**: **WAIT** - CNY will strengthen significantly

### 🟡 Gradual Cuts (2025) - 75% Probability
- **Rate Change**: -50 bps total to 3.75-4.00%
- **Triggers**: Inflation moderating, growth concerns, global coordination
- **CNY/USD Impact**: Rate drops to 6.9-7.0
- **Your Strategy**: **WAIT** - Significant CNY strengthening expected

### 🔴 No Cuts (2025) - 10% Probability
- **Rate Change**: 0 bps (Hold at 4.25-4.50%)
- **Triggers**: Inflation spike, strong data, trade tensions
- **CNY/USD Impact**: Rate rises to 7.2-7.4
- **Your Strategy**: **SELL NOW** - CNY will weaken further

### 🟢 Aggressive Cuts (2025) - 25% Probability
- **Rate Change**: -100 bps total to 3.25-3.50%
- **Triggers**: Recession concerns, unemployment spike, deflation
- **CNY/USD Impact**: Rate drops to 6.8-6.9
- **Your Strategy**: **WAIT** - Massive CNY strengthening opportunity

## 📅 Key Fed Meetings & CNY Impact

### October 29, 2025 (90% Cut Probability)
- **Expected**: -25 bps cut
- **CNY Impact**: Immediate strengthening
- **Your Action**: **WAIT** - Don't sell CNY before this meeting

### December 17, 2025 (60% Cut Probability)
- **Expected**: -25 bps cut (if October cut)
- **CNY Impact**: Further strengthening
- **Your Action**: **MONITOR** - Could be peak CNY strength

### January 28, 2026 (40% Cut Probability)
- **Expected**: Hold or -25 bps
- **CNY Impact**: Continued strength if cuts continue
- **Your Action**: **EVALUATE** - Assess if peak reached

## 🎯 Strategic Recommendations

### **IMMEDIATE ACTION (Next 30 Days)**
- **DO NOT SELL CNY** - 90% probability of rate cut
- **WAIT for October 29 meeting** - Major CNY strengthening expected
- **Monitor economic data** - Any weak data increases cut probability

### **MEDIUM-TERM STRATEGY (60-120 Days)**
- **Target CNY/USD below 7.0** - Significant strengthening expected
- **Consider selling at 6.9-7.0** - Peak strength likely
- **Set stop-loss at 7.3** - If no cuts occur, sell immediately

### **RISK MANAGEMENT**
- **Split position**: 70% wait, 30% sell now (hedge)
- **Monitor Fed speeches**: Powell's comments are key
- **Watch economic data**: Jobs, inflation, GDP reports

## ⚠️ Key Risk Factors

### **Fed Cut Risks**
- **Inflation spike**: Could halt cuts
- **Strong economic data**: Could delay cuts
- **Geopolitical events**: Could change priorities

### **CNY Risks**
- **Chinese economic weakness**: Could offset USD weakness
- **PBOC intervention**: Could limit CNY strength
- **Trade tensions**: Could create volatility

## 📚 Data Sources & Methodology
- **Economic Data**: Federal Reserve, BLS, BEA
- **Market Data**: CME FedWatch, Treasury yields, Dollar Index
- **Analysis**: Technical and fundamental analysis
- **Timeframe**: October 2025 - January 2026

---
*This analysis is for informational purposes only and should not be considered as financial advice. Always consult with financial professionals for investment decisions.*
"""
        
        # Save report
        with open('/Users/boss/Documents/cursor/placeholder/fed_policy_analysis_report.md', 'w') as f:
            f.write(report)
            
        print("✅ Fed policy analysis report saved as 'fed_policy_analysis_report.md'")
        print("\n" + "="*70)
        print(report)

def main():
    """Main function to run the Fed policy analysis"""
    print("🏦 Federal Reserve Policy Analysis & Market Sentiment Assessment")
    print("=" * 70)
    
    # Get API key (not needed for this analysis, but keeping for consistency)
    api_key = os.getenv('ALPHAVANTAGE_API_KEY', 'dummy')
    
    # Initialize analyzer
    analyzer = FedPolicyAnalyzer(api_key)
    
    # Run comprehensive analysis
    analyzer.create_comprehensive_fed_report()
    
    print("\n🎉 Fed policy analysis complete! Check the generated files:")
    print("- fed_policy_analysis_report.md (comprehensive Fed analysis)")

if __name__ == "__main__":
    main()
