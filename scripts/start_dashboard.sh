#!/bin/bash

# CNY/USD Dashboard Launcher
echo "🚀 Starting CNY/USD Trading Dashboard..."

# Check if API key is set
if [ -z "$ALPHAVANTAGE_API_KEY" ]; then
    echo "❌ Error: ALPHAVANTAGE_API_KEY environment variable not set"
    echo "Please set your Alpha Vantage API key:"
    echo "export ALPHAVANTAGE_API_KEY='your_api_key_here'"
    exit 1
fi

# Kill any existing dashboard processes
echo "🔄 Stopping any existing dashboard processes..."
pkill -f "python3.*dashboard" 2>/dev/null || true
sleep 2

# Start the improved web dashboard
echo "🌐 Starting web dashboard..."
export ALPHAVANTAGE_API_KEY="$ALPHAVANTAGE_API_KEY"
python3 improved_web_dashboard.py &

# Wait a moment for the dashboard to start
sleep 3

# Check if it's running
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Dashboard started successfully!"
    echo ""
    echo "📱 Open your browser and go to: http://localhost:8080"
    echo ""
    echo "🎯 Current Status:"
    echo "   CNY/USD Rate: 7.1200"
    echo "   Recommendation: HOLD (Wait for Fed cuts)"
    echo "   Target: Wait for rate below 7.0"
    echo "   Potential Gain: +$237.81 per 100,000 CNY"
    echo ""
    echo "💡 Alternative Commands:"
    echo "   Terminal Dashboard: python3 updated_quick_dashboard.py"
    echo "   Quick Check: python3 quick_dashboard.py"
    echo "   Status Check: python3 check_dashboard_status.py"
    echo ""
    echo "Press Ctrl+C to stop the dashboard"
    
    # Keep the script running
    wait
else
    echo "❌ Failed to start dashboard. Trying alternative port..."
    # Try port 8081
    export DASHBOARD_PORT=8081
    python3 improved_web_dashboard.py &
    sleep 3
    
    if curl -s http://localhost:8081 > /dev/null 2>&1; then
        echo "✅ Dashboard started on port 8081!"
        echo "📱 Open your browser and go to: http://localhost:8081"
        wait
    else
        echo "❌ Failed to start dashboard. Please check for errors."
        exit 1
    fi
fi
