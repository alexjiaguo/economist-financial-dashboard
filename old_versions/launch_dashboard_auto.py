#!/usr/bin/env python3
"""
Auto-launch CNY/USD Dashboard - Finds available port automatically
"""

import socket
import subprocess
import sys
import os
import time

def find_free_port(start_port=8080, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def launch_dashboard():
    """Launch the dashboard on an available port"""
    print("🚀 CNY/USD Dashboard Auto-Launcher")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("❌ Error: ALPHAVANTAGE_API_KEY not found!")
        print("Please set your API key:")
        print("export ALPHAVANTAGE_API_KEY='your_api_key_here'")
        return False
    
    # Find free port
    print("🔍 Finding available port...")
    port = find_free_port()
    if not port:
        print("❌ Error: No available ports found!")
        return False
    
    print(f"✅ Found free port: {port}")
    
    # Set environment variable for the port
    os.environ['DASHBOARD_PORT'] = str(port)
    
    # Launch dashboard
    print(f"🌐 Starting dashboard on http://localhost:{port}")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Use the improved web dashboard
        subprocess.run([
            sys.executable, 'improved_web_dashboard.py'
        ], env={**os.environ, 'DASHBOARD_PORT': str(port)})
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Good luck with your trading!")
        return True
    except Exception as e:
        print(f"❌ Error launching dashboard: {str(e)}")
        return False

if __name__ == "__main__":
    launch_dashboard()
