# 🚀 Setup Instructions

## Quick Setup (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/economist-dashboard.git
cd economist-dashboard
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get API Key
1. Go to [Twelve Data](https://twelvedata.com/)
2. Sign up for free account
3. Copy your API key (800 requests/day free tier)

### 4. Set Environment Variable
```bash
export TWELVEDATA_API_KEY="your_api_key_here"
```

Or create a `.env` file:
```bash
cp env.example .env
# Edit .env and add your API key
```

### 5. Run Dashboard
```bash
python3 economist_dashboard.py
```

### 6. Open Browser
```
http://localhost:8080
```

---

## Detailed Setup

### Prerequisites
- **Python 3.9 or higher**
- **pip** (Python package manager)
- **Internet connection** (for API calls)

### Check Python Version
```bash
python3 --version
```

Should show 3.9.0 or higher.

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### API Key Setup

#### Method 1: Environment Variable (Temporary)
```bash
export TWELVEDATA_API_KEY="your_key"
python3 economist_dashboard.py
```

#### Method 2: .env File (Permanent)
```bash
echo 'TWELVEDATA_API_KEY=your_key_here' > .env
python3 economist_dashboard.py
```

#### Method 3: Shell Profile (Persistent)
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export TWELVEDATA_API_KEY="your_key"
```

---

## Troubleshooting

### Port 8080 Already in Use
```bash
# Check what's using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use different port
export DASHBOARD_PORT=8081
python3 economist_dashboard.py
```

### Module Not Found Error
```bash
# Install missing module
pip install flask requests

# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

### API Key Not Working
1. Check you copied the full key
2. No extra spaces or quotes
3. Key is activated on Twelve Data dashboard
4. Free tier limit not exceeded (800/day)

### Chart Not Loading
1. Check browser console (F12)
2. Verify internet connection
3. Check API rate limit
4. Try different asset

---

## Configuration

### Change Port
```bash
export DASHBOARD_PORT=8081
python3 economist_dashboard.py
```

### Change Refresh Interval
Edit `economist_dashboard.py` line 1089:
```javascript
// Change 3600000 (1 hour) to desired milliseconds
setInterval(() => loadAsset(), 3600000);
```

### Change Forecast Period
Edit `economist_dashboard.py` line 1225:
```python
# Change days=30 to desired number
forecast_data = dashboard.generate_forecast(historical_data['prices'], days=30)
```

---

## Production Deployment

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 economist_dashboard:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY economist_dashboard.py .
ENV TWELVEDATA_API_KEY=""
EXPOSE 8080
CMD ["python3", "economist_dashboard.py"]
```

```bash
docker build -t economist-dashboard .
docker run -e TWELVEDATA_API_KEY="your_key" -p 8080:8080 economist-dashboard
```

### Using systemd (Linux)
Create `/etc/systemd/system/economist-dashboard.service`:
```ini
[Unit]
Description=Economist Dashboard
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/economist-dashboard
Environment="TWELVEDATA_API_KEY=your_key"
ExecStart=/usr/bin/python3 economist_dashboard.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable economist-dashboard
sudo systemctl start economist-dashboard
```

---

## Updating

### Pull Latest Changes
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Check Version
```bash
git log -1 --oneline
```

---

## Uninstall

### Remove Application
```bash
cd ..
rm -rf economist-dashboard
```

### Remove Virtual Environment
```bash
deactivate  # If active
rm -rf venv
```

---

## Getting Help

### Check Logs
The dashboard prints debug information to console. Look for:
- `Time Series API response keys`
- `Fetched X historical data points`
- `API error` messages

### Common Issues
1. **"Address already in use"**: Port 8080 occupied, use different port
2. **"Module not found"**: Run `pip install -r requirements.txt`
3. **"API error"**: Check API key and rate limits
4. **"No data"**: Try different asset or check API status

### Report Bug
1. Check [existing issues](https://github.com/yourusername/economist-dashboard/issues)
2. Create new issue with:
   - Python version
   - Error message
   - Steps to reproduce

---

## Success Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key obtained from Twelve Data
- [ ] Environment variable set
- [ ] Dashboard running on port 8080
- [ ] Browser showing dashboard
- [ ] Can select assets
- [ ] Charts displaying
- [ ] Tooltips working

**If all checked, you're ready to use the dashboard!** 🎉

