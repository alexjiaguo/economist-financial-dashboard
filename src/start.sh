#!/bin/bash
# Start the Economist Dashboard

echo "🚀 Starting Economist Financial Dashboard..."
echo ""

# Check if TWELVEDATA_API_KEY is set
if [ -z "$TWELVEDATA_API_KEY" ]; then
    echo "⚠️  Warning: TWELVEDATA_API_KEY not set"
    echo "Please set your API key:"
    echo "  export TWELVEDATA_API_KEY='your_key_here'"
    echo ""
    echo "Or create a .env file with:"
    echo "  TWELVEDATA_API_KEY=your_key_here"
    exit 1
fi

# Start the dashboard
cd "$(dirname "$0")"
python3 app.py

