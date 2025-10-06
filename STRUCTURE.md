# 📁 Project Structure Guide

## Overview

This document explains the organization of the Economist Financial Dashboard project.

---

## 🌳 Directory Tree

```
economist-financial-dashboard/
│
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 .gitignore                   # Git ignore rules
├── 📄 STRUCTURE.md                 # This file - project structure guide
│
├── 📂 src/                         # SOURCE CODE (Production)
│   ├── 🐍 app.py                   # Main Flask application (1,200+ lines)
│   ├── 📋 requirements.txt         # Python dependencies
│   ├── 📝 .env.example            # Environment variables template
│   └── 🚀 start.sh                # Quick start script
│
├── 📂 docs/                        # DOCUMENTATION
│   ├── 📘 SETUP.md                # Installation & setup guide
│   ├── 📗 ECONOMIST_DASHBOARD_GUIDE.md  # Complete user manual
│   ├── 📙 FEATURES_QUICK_REFERENCE.md   # Feature lookup table
│   ├── 📕 REAL_DATA_UPDATE.md     # Real data implementation
│   ├── 📔 NEW_FEATURES_SUMMARY.md # All features explained
│   ├── 📓 QUICK_START.md          # 5-minute setup
│   ├── 📖 DASHBOARD_UPDATE_SUMMARY.md  # Change history
│   ├── 📚 GITHUB_SETUP.md         # GitHub deployment guide
│   ├── 📜 PROJECT_SUMMARY.md      # Project overview
│   ├── 🎉 SUCCESS.md              # Post-setup guide
│   ├── 🔧 TWELVE_DATA_SETUP.md    # API setup instructions
│   └── 📋 ...                     # Additional documentation
│
├── 📂 scripts/                     # HELPER SCRIPTS
│   ├── 🚀 push_to_github.sh       # GitHub deployment automation
│   └── 🔧 ...                     # Other utility scripts
│
└── 📂 old_versions/                # ARCHIVE (Historical code)
    ├── cny_usd_analysis.py        # Early CNY/USD analysis
    ├── cny_usd_dashboard.py       # First dashboard attempt
    ├── tesla_stock_prediction.py  # Stock prediction experiments
    ├── simple_dashboard.py        # Simple dashboard iterations
    ├── web_dashboard.py           # Web dashboard prototypes
    ├── twelve_data_dashboard.py   # Twelve Data integration tests
    └── ...                        # Other archived files
```

---

## 📂 Folder Breakdown

### `/src` - Source Code (Production)

**Purpose**: Contains the live, production-ready application code.

#### Key Files:
- **`app.py`** (Main Application)
  - 1,200+ lines of Python code
  - Flask web server
  - API integration with Twelve Data
  - Forecasting algorithms
  - Economic indicators logic
  - HTML/CSS/JavaScript rendering
  
- **`requirements.txt`** (Dependencies)
  ```
  flask>=2.3.0
  requests>=2.31.0
  twelvedata>=1.2.0
  numpy>=1.24.0
  scikit-learn>=1.3.0
  ```

- **`.env.example`** (Environment Template)
  ```bash
  TWELVEDATA_API_KEY=your_api_key_here
  ```

- **`start.sh`** (Quick Launcher)
  - Checks for API key
  - Starts Flask server
  - Opens dashboard on port 8080

**Usage**:
```bash
cd src
export TWELVEDATA_API_KEY='your_key'
python3 app.py
```

---

### `/docs` - Documentation

**Purpose**: Comprehensive guides and documentation for users and developers.

#### Documentation Categories:

**Setup & Installation**:
- `SETUP.md` - Full installation guide with troubleshooting
- `QUICK_START.md` - 5-minute setup for quick deployment
- `GITHUB_SETUP.md` - How to deploy on GitHub
- `TWELVE_DATA_SETUP.md` - API key setup instructions

**User Guides**:
- `ECONOMIST_DASHBOARD_GUIDE.md` - Complete feature walkthrough
- `FEATURES_QUICK_REFERENCE.md` - Quick lookup table
- `SUCCESS.md` - Post-setup tips and next steps

**Technical Documentation**:
- `REAL_DATA_UPDATE.md` - How real data is fetched and processed
- `NEW_FEATURES_SUMMARY.md` - All features with technical details
- `DASHBOARD_UPDATE_SUMMARY.md` - Change history and updates

**Project Info**:
- `PROJECT_SUMMARY.md` - Comprehensive project overview
- `STRUCTURE.md` - This file!

---

### `/scripts` - Helper Scripts

**Purpose**: Automation scripts for deployment, testing, and maintenance.

#### Available Scripts:
- **`push_to_github.sh`** - Automates GitHub deployment
- Other utility scripts for setup and maintenance

**Usage**:
```bash
cd scripts
./push_to_github.sh
```

---

### `/old_versions` - Archive

**Purpose**: Historical versions of the project for reference.

**Contains**:
- Early prototypes
- Experimental features
- Previous API integrations (Alpha Vantage)
- Different dashboard designs
- Analysis scripts
- Test files

**Note**: These files are kept for reference but are not part of the production code.

---

## 🎯 Key File Locations

### Need to...?

**Start the dashboard**:
```bash
cd src
./start.sh
```

**Read setup instructions**:
```bash
cat docs/SETUP.md
```

**Check all features**:
```bash
cat docs/FEATURES_QUICK_REFERENCE.md
```

**Deploy to GitHub**:
```bash
cd scripts
./push_to_github.sh
```

**Edit the main code**:
```bash
vim src/app.py
```

**Update dependencies**:
```bash
vim src/requirements.txt
pip install -r src/requirements.txt
```

---

## 📊 File Statistics

### Production Code (`/src`)
- **Files**: 4
- **Lines of Code**: ~1,200 (app.py)
- **Size**: ~55 KB (app.py)

### Documentation (`/docs`)
- **Files**: 15+
- **Total Words**: ~20,000+
- **Covers**: Setup, usage, features, troubleshooting

### Archive (`/old_versions`)
- **Files**: 15+
- **Purpose**: Historical reference
- **Not used**: In production

---

## 🚀 Development Workflow

### 1. Clone Repository
```bash
git clone https://github.com/alexjiaguo/economist-financial-dashboard.git
cd economist-financial-dashboard
```

### 2. Read Documentation
```bash
# Quick start
cat docs/QUICK_START.md

# Or full setup
cat docs/SETUP.md
```

### 3. Install Dependencies
```bash
cd src
pip install -r requirements.txt
```

### 4. Configure API Key
```bash
export TWELVEDATA_API_KEY='your_key_here'
```

### 5. Run Application
```bash
python3 app.py
# Or
./start.sh
```

### 6. Access Dashboard
```
http://localhost:8080
```

---

## 🔧 Customization

### Adding New Assets

**Location**: `src/app.py`

**Find**:
```python
self.assets = {
    'currencies': { ... },
    'stocks': { ... },
    # Add your category here
}
```

### Modifying Design

**Location**: `src/app.py` (look for CSS section)

**Find**:
```python
<style>
    /* Economist theme colors */
    :root {
        --economist-red: #e3120b;
        /* Modify colors here */
    }
</style>
```

### Changing Refresh Frequency

**Location**: `src/app.py`

**Find**:
```javascript
setInterval(() => {
    loadAsset();
}, 3600000); // 1 hour = 3600000 ms
```

---

## 📦 Dependencies

### Python Packages (see `src/requirements.txt`)
- **Flask** (2.3.0+): Web framework
- **Requests** (2.31.0+): HTTP client
- **twelvedata** (1.2.0+): API client
- **NumPy** (1.24.0+): Numerical computing
- **scikit-learn** (1.3.0+): Machine learning

### Frontend Libraries (CDN)
- **Chart.js** (3.9.1): Interactive charts
- **Google Fonts**: Typography (Merriweather, Open Sans)

---

## 🌐 URLs

### Repository
- **GitHub**: https://github.com/alexjiaguo/economist-financial-dashboard
- **Clone**: `git clone https://github.com/alexjiaguo/economist-financial-dashboard.git`

### Dashboard
- **Local**: http://localhost:8080
- **API Endpoint**: http://localhost:8080/api/asset

### External Services
- **Twelve Data**: https://twelvedata.com/
- **API Docs**: https://twelvedata.com/docs

---

## 📝 Important Notes

### What to Edit
✅ **Edit**: `/src/app.py` - Main application
✅ **Edit**: `/src/requirements.txt` - Dependencies
✅ **Edit**: `/docs/*.md` - Documentation
✅ **Edit**: `README.md` - Main readme

### What NOT to Edit
❌ **Don't Edit**: `/old_versions/*` - Archived files
❌ **Don't Commit**: `.env` - Contains API keys
❌ **Don't Push**: `__pycache__/` - Python cache

### Gitignore Protects
- `.env` - Your API key
- `__pycache__/` - Python bytecode
- `.DS_Store` - macOS files
- `*.pyc` - Compiled Python

---

## 🎓 Learning Path

### New Users
1. Read `README.md` (this file)
2. Follow `docs/QUICK_START.md`
3. Explore dashboard at http://localhost:8080
4. Read `docs/FEATURES_QUICK_REFERENCE.md`

### Developers
1. Read `docs/SETUP.md`
2. Study `src/app.py`
3. Read `docs/REAL_DATA_UPDATE.md`
4. Check `docs/NEW_FEATURES_SUMMARY.md`

### Contributors
1. Fork repository
2. Create feature branch
3. Read `docs/PROJECT_SUMMARY.md`
4. Submit pull request

---

## 🏆 Best Practices

### Code Organization
✅ Keep production code in `/src`
✅ Document all changes
✅ Test before committing
✅ Use meaningful commit messages

### File Management
✅ Archive old code in `/old_versions`
✅ Update documentation when adding features
✅ Keep README.md current
✅ Don't commit sensitive data

### Git Workflow
```bash
git add src/app.py
git commit -m "Add new feature: XYZ"
git push origin main
```

---

## 🔍 Quick Reference

### Find Something?

**Main application**: `src/app.py`
**Setup guide**: `docs/SETUP.md`
**All features**: `docs/FEATURES_QUICK_REFERENCE.md`
**API setup**: `docs/TWELVE_DATA_SETUP.md`
**Troubleshooting**: `docs/SETUP.md` (bottom section)

---

## 📞 Support

### Issues?
- Check `docs/SETUP.md` troubleshooting section
- Review `docs/ECONOMIST_DASHBOARD_GUIDE.md`
- Create GitHub issue

### Questions?
- Read documentation in `/docs`
- Check `README.md`
- Open GitHub discussion

---

**Happy Coding!** 🚀📊

*Last Updated: October 6, 2025*

