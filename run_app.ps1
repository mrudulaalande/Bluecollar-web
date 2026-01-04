# 🚀 Unified Startup Script for Blue Collar Hub
# This script runs both the Backend and Frontend together.

$env:PYTHONPATH = "."
$PORT = 8080

Write-Host "`n🚀 Starting Blue Collar Hub - Fit For All..." -ForegroundColor Cyan
Write-Host "-------------------------------------------"

# 1. Initialize Database
Write-Host "📦 Initializing Database..." -ForegroundColor Yellow
python -m backend.init_db

# 2. Choose Mode
$choice = Read-Host "`nSelect Mode: [1] Standard (8000/8501) [2] Cloud Test (8080 - Single URL)"
if ($choice -eq "2") {
    Write-Host "`n🧪 Running in Cloud Test Mode (Port 8080)..." -ForegroundColor Magenta
    Write-Host "Note: In this mode, we simulate Cloud Run by running BOTH in one process."
    ./start.sh
} else {
    Write-Host "`n🔌 Starting Backend API on http://localhost:8000..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='.'; uvicorn backend.main:app --host 0.0.0.0 --port 8000"

    Write-Host "🎨 Starting Frontend UI on http://localhost:8501..." -ForegroundColor Green
    python -m streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
}
