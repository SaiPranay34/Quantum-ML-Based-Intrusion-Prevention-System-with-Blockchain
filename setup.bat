@echo off
echo ============================================
echo  QUANTUM BLOCKCHAIN IDS - PROJECT SETUP
echo ============================================

echo [1/5] Creating folder structure...
mkdir blockchain 2>nul
mkdir blockchain\contract 2>nul
mkdir routes 2>nul
mkdir services 2>nul
mkdir utils 2>nul
mkdir datasets 2>nul
mkdir datasets\simulation 2>nul
mkdir datasets\upload 2>nul
mkdir templates 2>nul
mkdir templates\partials 2>nul
mkdir templates\components 2>nul
mkdir static 2>nul
mkdir static\uploads 2>nul

echo [2/5] Creating root files...
type nul > app.py
type nul > deploy.py
type nul > config.py
type nul > dataset.py
type nul > requirements.txt

echo [3/5] Creating blockchain files...
type nul > blockchain\blockchain.py
type nul > blockchain\contract\Intrusion.sol

echo [4/5] Creating routes, services, utils...
type nul > routes\auth.py
type nul > routes\monitor.py
type nul > routes\ledger.py
type nul > routes\upload.py
type nul > routes\reports.py
type nul > routes\settings.py
type nul > routes\__init__.py
type nul > services\ml_service.py
type nul > services\alert_service.py
type nul > services\ip_service.py
type nul > services\__init__.py
type nul > utils\database.py
type nul > utils\__init__.py

echo [5/5] Creating templates...
type nul > templates\index.html
type nul > templates\login.html
type nul > templates\signup.html
type nul > templates\dashboard.html
type nul > templates\partials\stats.html
type nul > templates\partials\performance.html
type nul > templates\partials\monitoring.html
type nul > templates\partials\upload.html
type nul > templates\partials\ledger.html
type nul > templates\partials\blocked_ips.html
type nul > templates\partials\reports.html
type nul > templates\partials\settings.html
type nul > templates\components\alert_popup.html
type nul > templates\components\navbar.html
type nul > templates\components\sidebar.html

echo.
echo ============================================
echo  Installing dependencies...
echo ============================================
pip install flask flask-cors pennylane torch numpy pandas scikit-learn joblib web3 pysha3 py-solc-x

echo.
echo ============================================
echo  SETUP COMPLETE
echo  Next steps:
echo    1. Run: python deploy.py
echo    2. Run: python app.py
echo ============================================
pause