# Lexi - Quick Setup Script
# Run this script to set up the entire project
# Created by UOIONHHC

Write-Host ">> Lexi - Legal Document Templating System Setup" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([0-9]+)") {
        $minorVersion = [int]$Matches[1]
        if ($minorVersion -lt 10) {
            Write-Host "[X] Python 3.10+ required. Found: $pythonVersion" -ForegroundColor Red
            exit 1
        }
        Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "[X] Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[X] Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Yellow
Write-Host ("-" * 60) -ForegroundColor Gray

# Backend setup
Set-Location backend

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Gray
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# Create .env if not exists
if (Test-Path ".env") {
    Write-Host ".env file already exists" -ForegroundColor Gray
} else {
    Write-Host "Creating .env file from template..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "[!] IMPORTANT: Edit backend\.env and add your API keys:" -ForegroundColor Yellow
    Write-Host "   - GEMINI_API_KEY (required)" -ForegroundColor Yellow
    Write-Host "   - EXA_API_KEY (optional, for bonus features)" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Press Enter after you've added your API keys, or type 'skip' to continue without them"
    if ($continue -eq 'skip') {
        Write-Host "[!] Continuing without API keys - features will be limited" -ForegroundColor Yellow
    }
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Cyan
python -m app.db.init_db

Write-Host "[OK] Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Return to root
Set-Location ..

Write-Host "Setting up Frontend..." -ForegroundColor Yellow
Write-Host ("-" * 60) -ForegroundColor Gray

# Frontend setup
Set-Location frontend

# Create .env.local if not exists
if (Test-Path ".env.local") {
    Write-Host ".env.local already exists" -ForegroundColor Gray
} else {
    Write-Host "Creating .env.local..." -ForegroundColor Cyan
    Set-Content -Path ".env.local" -Value "NEXT_PUBLIC_API_URL=http://localhost:8000"
}

# Install dependencies
Write-Host "Installing Node.js dependencies (this may take a minute)..." -ForegroundColor Cyan
npm install --silent

Write-Host "[OK] Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Return to root
Set-Location ..

Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "[OK] Setup Complete!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start the backend:" -ForegroundColor Cyan
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   uvicorn app.main:app --reload --port 8000" -ForegroundColor White
Write-Host ""
Write-Host "2. In a NEW terminal, start the frontend:" -ForegroundColor Cyan
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Open your browser:" -ForegroundColor Cyan
Write-Host "   http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host ">> For detailed demo instructions, see DEMO_GUIDE.md" -ForegroundColor Yellow
Write-Host ""
Write-Host ">> Built by: UOIONHHC" -ForegroundColor Magenta
Write-Host ""
