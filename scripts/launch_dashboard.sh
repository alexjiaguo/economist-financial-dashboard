#!/bin/bash

# CNY/USD Trading Dashboard Launcher
echo "🚀 Launching CNY/USD Trading Dashboard..."

# Check if API key is set
if [ -z "$ALPHAVANTAGE_API_KEY" ]; then
    echo "❌ Error: ALPHAVANTAGE_API_KEY environment variable not set"
    echo "Please set your Alpha Vantage API key:"
    echo "export ALPHAVANTAGE_API_KEY='your_api_key_here'"
    exit 1
fi

# Install requirements if needed
echo "📦 Installing dashboard requirements..."
pip3 install -r dashboard_requirements.txt

# Launch the dashboard
echo "🌐 Starting dashboard on http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run cny_usd_dashboard.py --server.port 8501 --server.address localhost
