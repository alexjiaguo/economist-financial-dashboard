#!/usr/bin/env python3
"""
Real-Time CNY/USD Trading Dashboard
Monitor exchange rates, Fed policy, and economic indicators to maximize USD gains
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
import threading
import queue

# Configure Streamlit page
st.set_page_config(
    page_title="CNY/USD Trading Dashboard",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class MarketData:
    """Data structure for market information"""
    timestamp: datetime
    cny_usd_rate: float
    usd_index: float
    fed_funds_rate: float
    inflation_rate: float
    unemployment_rate: float
    gdp_growth: float
    treasury_10y: float
    treasury_2y: float
    vix: float
    sp500: float

class CNYUSDDashboard:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.data_queue = queue.Queue()
        self.running = False
        
    def fetch_cny_usd_rate(self) -> Optional[float]:
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
            st.error(f"Error fetching CNY/USD rate: {str(e)}")
        return None
    
    def fetch_historical_data(self, symbol: str, function: str, days: int = 30) -> Optional[pd.DataFrame]:
        """Fetch historical data for various indicators"""
        try:
            params = {
                'function': function,
                'symbol': symbol,
                'outputsize': 'compact',
                'apikey': self.api_key
            }
            
            if function == 'FX_DAILY':
                params.update({
                    'from_symbol': 'USD',
                    'to_symbol': 'CNY'
                })
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract time series data
            time_series_key = None
            for key in data.keys():
                if 'Time Series' in key:
                    time_series_key = key
                    break
            
            if time_series_key and data[time_series_key]:
                df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()
                
                # Convert to float
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df.tail(days)
        except Exception as e:
            st.error(f"Error fetching {symbol} data: {str(e)}")
        return None
    
    def get_market_data(self) -> MarketData:
        """Get comprehensive market data"""
        # Fetch current CNY/USD rate
        cny_usd_rate = self.fetch_cny_usd_rate()
        
        # Mock data for other indicators (in real implementation, you'd fetch from APIs)
        # For demo purposes, using realistic values
        current_time = datetime.now()
        
        return MarketData(
            timestamp=current_time,
            cny_usd_rate=cny_usd_rate or 7.12,
            usd_index=103.5,
            fed_funds_rate=4.375,  # Current Fed rate
            inflation_rate=2.7,
            unemployment_rate=4.2,
            gdp_growth=3.0,
            treasury_10y=4.1,
            treasury_2y=4.3,
            vix=18.5,
            sp500=5450.0
        )
    
    def calculate_trading_signals(self, current_rate: float) -> Dict:
        """Calculate trading signals and recommendations"""
        signals = {
            'action': 'HOLD',
            'confidence': 0,
            'target_rate': 0,
            'stop_loss': 0,
            'reasoning': '',
            'risk_level': 'MEDIUM'
        }
        
        # Trading logic based on our analysis
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
    
    def create_exchange_rate_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create exchange rate chart with trading signals"""
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['4. close'],
            mode='lines',
            name='CNY/USD Rate',
            line=dict(color='#2E86AB', width=2)
        ))
        
        # Add moving averages
        if len(df) >= 20:
            df['MA20'] = df['4. close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['MA20'],
                mode='lines',
                name='20-Day MA',
                line=dict(color='#A23B72', width=1, dash='dash')
            ))
        
        # Add target levels
        fig.add_hline(y=7.0, line_dash="dot", line_color="green", 
                     annotation_text="Target: 7.0 (SELL)", annotation_position="top right")
        fig.add_hline(y=7.1, line_dash="dot", line_color="orange", 
                     annotation_text="Good: 7.1 (SELL)", annotation_position="top right")
        fig.add_hline(y=7.3, line_dash="dot", line_color="red", 
                     annotation_text="Stop Loss: 7.3 (SELL)", annotation_position="top right")
        
        fig.update_layout(
            title="CNY/USD Exchange Rate with Trading Signals",
            xaxis_title="Date",
            yaxis_title="CNY per USD",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_fed_policy_chart(self) -> go.Figure:
        """Create Fed policy expectations chart"""
        # Fed meeting dates and probabilities
        meetings = pd.DataFrame({
            'Date': ['2025-10-29', '2025-12-17', '2026-01-28'],
            'Cut_Probability': [90, 60, 40],
            'Expected_Rate': [4.125, 3.875, 3.625]
        })
        meetings['Date'] = pd.to_datetime(meetings['Date'])
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Fed Rate Cut Probability', 'Expected Fed Funds Rate'),
            vertical_spacing=0.1
        )
        
        # Probability chart
        fig.add_trace(
            go.Bar(x=meetings['Date'], y=meetings['Cut_Probability'], 
                   name='Cut Probability (%)', marker_color='lightblue'),
            row=1, col=1
        )
        
        # Rate chart
        fig.add_trace(
            go.Scatter(x=meetings['Date'], y=meetings['Expected_Rate'], 
                      mode='lines+markers', name='Expected Rate (%)', 
                      line=dict(color='red', width=2)),
            row=2, col=1
        )
        
        fig.update_layout(height=500, showlegend=True)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Probability (%)", row=1, col=1)
        fig.update_yaxes(title_text="Rate (%)", row=2, col=1)
        
        return fig
    
    def create_economic_indicators_chart(self, market_data: MarketData) -> go.Figure:
        """Create economic indicators radar chart"""
        categories = ['Inflation', 'Unemployment', 'GDP Growth', 'Treasury 10Y', 'VIX']
        values = [
            market_data.inflation_rate,
            market_data.unemployment_rate,
            market_data.gdp_growth,
            market_data.treasury_10y,
            market_data.vix
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current Values',
            line_color='blue'
        ))
        
        # Add target/optimal values
        target_values = [2.0, 4.0, 2.5, 3.5, 15]
        fig.add_trace(go.Scatterpolar(
            r=target_values,
            theta=categories,
            fill='toself',
            name='Target/Optimal',
            line_color='green'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True,
            title="Economic Indicators vs Targets"
        )
        
        return fig
    
    def create_profit_calculator(self) -> None:
        """Create profit calculator widget"""
        st.subheader("💰 Profit Calculator")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cny_amount = st.number_input("CNY Amount", min_value=1000, value=100000, step=1000)
        
        with col2:
            current_rate = st.number_input("Current Rate", min_value=6.0, max_value=8.0, value=7.12, step=0.01)
        
        with col3:
            target_rate = st.number_input("Target Rate", min_value=6.0, max_value=8.0, value=7.0, step=0.01)
        
        # Calculate profits
        current_usd = cny_amount / current_rate
        target_usd = cny_amount / target_rate
        profit = target_usd - current_usd
        profit_pct = (profit / current_usd) * 100
        
        st.metric("Current USD Value", f"${current_usd:,.2f}")
        st.metric("Target USD Value", f"${target_usd:,.2f}")
        st.metric("Potential Profit", f"${profit:,.2f} ({profit_pct:+.2f}%)")
    
    def run_dashboard(self):
        """Main dashboard function"""
        st.title("🇨🇳 CNY/USD Trading Dashboard")
        st.markdown("**Real-time monitoring to maximize your USD gains**")
        
        # Sidebar for settings
        with st.sidebar:
            st.header("⚙️ Dashboard Settings")
            refresh_interval = st.selectbox("Refresh Interval", [30, 60, 120, 300], index=1)
            auto_refresh = st.checkbox("Auto Refresh", value=True)
            
            st.header("📊 Your Position")
            cny_amount = st.number_input("CNY Amount", min_value=1000, value=100000, step=1000)
            target_rate = st.number_input("Target Rate", min_value=6.0, max_value=8.0, value=7.0, step=0.01)
            
            st.header("🔔 Alerts")
            enable_alerts = st.checkbox("Enable Alerts", value=True)
            alert_rate = st.number_input("Alert Rate", min_value=6.0, max_value=8.0, value=7.0, step=0.01)
        
        # Main dashboard content
        if st.button("🔄 Refresh Data") or auto_refresh:
            # Get market data
            market_data = self.get_market_data()
            
            # Calculate trading signals
            signals = self.calculate_trading_signals(market_data.cny_usd_rate)
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "CNY/USD Rate",
                    f"{market_data.cny_usd_rate:.4f}",
                    delta=f"{((market_data.cny_usd_rate - 7.12) / 7.12 * 100):+.2f}%"
                )
            
            with col2:
                st.metric(
                    "Trading Signal",
                    signals['action'],
                    delta=f"{signals['confidence']}% confidence"
                )
            
            with col3:
                st.metric(
                    "Fed Funds Rate",
                    f"{market_data.fed_funds_rate:.3f}%",
                    delta="Expected: 4.125%"
                )
            
            with col4:
                st.metric(
                    "USD Index",
                    f"{market_data.usd_index:.1f}",
                    delta="-0.5 (Weakening)"
                )
            
            # Trading recommendation
            st.subheader("🎯 Trading Recommendation")
            
            if signals['action'] == 'SELL':
                st.success(f"**{signals['action']}** - {signals['reasoning']}")
                st.info(f"Confidence: {signals['confidence']}% | Risk Level: {signals['risk_level']}")
            elif signals['action'] == 'HOLD':
                st.warning(f"**{signals['action']}** - {signals['reasoning']}")
                st.info(f"Confidence: {signals['confidence']}% | Risk Level: {signals['risk_level']}")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Exchange rate chart
                df = self.fetch_historical_data('USDCNY', 'FX_DAILY', 60)
                if df is not None:
                    fig = self.create_exchange_rate_chart(df)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Fed policy chart
                fig = self.create_fed_policy_chart()
                st.plotly_chart(fig, use_container_width=True)
            
            # Economic indicators
            st.subheader("📊 Economic Indicators")
            col1, col2 = st.columns(2)
            
            with col1:
                fig = self.create_economic_indicators_chart(market_data)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Profit calculator
                self.create_profit_calculator()
            
            # Market sentiment
            st.subheader("📈 Market Sentiment")
            
            sentiment_data = {
                'Indicator': ['Fed Funds Futures', 'Bond Market', 'Equity Market', 'Dollar Index'],
                'Signal': ['Rate Cuts Expected', 'Rate Cuts Expected', 'Risk-On', 'USD Weakening'],
                'Strength': ['Very Strong', 'Strong', 'Moderate', 'Strong'],
                'CNY Impact': ['Positive', 'Positive', 'Positive', 'Positive']
            }
            
            df_sentiment = pd.DataFrame(sentiment_data)
            st.dataframe(df_sentiment, use_container_width=True)
            
            # Alerts section
            if enable_alerts:
                st.subheader("🔔 Alerts & Notifications")
                
                if market_data.cny_usd_rate <= alert_rate:
                    st.success(f"🚨 ALERT: CNY/USD rate ({market_data.cny_usd_rate:.4f}) is at or below your target ({alert_rate:.4f})!")
                    st.balloons()
                
                # Next Fed meeting countdown
                next_meeting = datetime(2025, 10, 29)
                days_until = (next_meeting - datetime.now()).days
                st.info(f"📅 Next Fed Meeting: {days_until} days (October 29, 2025)")
                st.info(f"🎯 Cut Probability: 90%")
            
            # Auto-refresh
            if auto_refresh:
                time.sleep(refresh_interval)
                st.rerun()

def main():
    """Main function to run the dashboard"""
    # Get API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        st.error("❌ Alpha Vantage API key not found!")
        st.info("Please set the ALPHAVANTAGE_API_KEY environment variable")
        return
    
    # Initialize dashboard
    dashboard = CNYUSDDashboard(api_key)
    
    # Run dashboard
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
