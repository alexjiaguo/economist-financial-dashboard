#!/usr/bin/env python3
"""
Check Dashboard Status - Verify all dashboards are working
"""

import requests
import subprocess
import sys
import os
from datetime import datetime

def check_web_dashboard(port=8080):
    """Check if web dashboard is running"""
    try:
        response = requests.get(f'http://localhost:{port}', timeout=5)
        if response.status_code == 200:
            return True, f"✅ Web Dashboard running on http://localhost:{port}"
        else:
            return False, f"❌ Web Dashboard returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"❌ Web Dashboard not accessible: {str(e)}"

def check_api_data(port=8080):
    """Check if API data endpoint is working"""
    try:
        response = requests.get(f'http://localhost:{port}/api/data', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'cny_usd_rate' in data:
                return True, f"✅ API working - Current rate: {data['cny_usd_rate']:.4f}"
            else:
                return False, "❌ API response missing rate data"
        else:
            return False, f"❌ API returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"❌ API not accessible: {str(e)}"

def check_terminal_dashboard():
    """Check if terminal dashboard can run"""
    try:
        result = subprocess.run([
            sys.executable, '-c', 
            'import sys; sys.path.append("."); from updated_quick_dashboard import display_dashboard; import os; display_dashboard(os.getenv("ALPHAVANTAGE_API_KEY"))'
        ], capture_output=True, text=True, timeout=10, env=os.environ)
        
        if result.returncode == 0 and "CNY/USD Rate:" in result.stdout:
            return True, "✅ Terminal Dashboard working"
        else:
            return False, f"❌ Terminal Dashboard error: {result.stderr}"
    except Exception as e:
        return False, f"❌ Terminal Dashboard failed: {str(e)}"

def main():
    """Check all dashboard components"""
    print("🔍 CNY/USD Dashboard Status Check")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check API key
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if api_key:
        print("✅ API Key: Set")
    else:
        print("❌ API Key: Not set")
        return
    
    print()
    
    # Check web dashboard
    web_status, web_msg = check_web_dashboard()
    print(web_msg)
    
    # Check API data
    api_status, api_msg = check_api_data()
    print(api_msg)
    
    # Check terminal dashboard
    term_status, term_msg = check_terminal_dashboard()
    print(term_msg)
    
    print()
    
    # Summary
    if web_status and api_status and term_status:
        print("🎉 ALL DASHBOARDS WORKING PERFECTLY!")
        print()
        print("📱 Web Dashboard: http://localhost:8080")
        print("💻 Terminal Dashboard: python3 updated_quick_dashboard.py")
        print("⚡ Quick Check: python3 quick_dashboard.py")
        print()
        print("🎯 Ready to monitor CNY/USD for maximum USD gains!")
    else:
        print("⚠️  Some components need attention")
        print("Check the error messages above and try restarting")

if __name__ == "__main__":
    main()
