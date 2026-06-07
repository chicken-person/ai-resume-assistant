# setup.ps1
# One-click local setup for AI Resume Assistant (Windows PowerShell)
# Run this after cloning the repo:
#   .\setup.ps1

Write-Host "🚀 Setting up AI Resume Assistant..." -ForegroundColor Cyan

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.10+ from https://python.org" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "✅ Found $pythonVersion"

# Create virtual environment if not exists
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate venv
. .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies (this may take a minute)..."
pip install --upgrade pip | Out-Null
pip install -r requirements.txt

# Create .env from example if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from .env.example..."
    Copy-Item .env.example .env
    Write-Host "⚠️  IMPORTANT: Edit .env and add your DEEPSEEK_API_KEY" -ForegroundColor Yellow
    Write-Host "   Get a free key at: https://platform.deepseek.com/api_keys" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Cyan
Write-Host "1. 编辑 .env 文件，填入你的 DeepSeek API Key（必须！）"
Write-Host "   Get free key: https://platform.deepseek.com/api_keys"
Write-Host ""
Write-Host "2. 启动应用："
Write-Host "   streamlit run app.py"
Write-Host ""
Write-Host "提示：以后每次打开新终端都要先激活环境：" -ForegroundColor Yellow
Write-Host "   .\.venv\Scripts\Activate.ps1"
Write-Host "   streamlit run app.py"
Write-Host ""