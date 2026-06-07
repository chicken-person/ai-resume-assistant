# check_install.ps1
# 部署前检查脚本 - 确保一切就绪后再运行
# 使用方法：.\check_install.ps1

Write-Host "🔍 AI Resume Assistant - 部署前检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$allGood = $true

# 1. 检查 Python
Write-Host "`n[1/6] 检查 Python 版本..." -ForegroundColor Yellow
try {
    $pythonVer = python --version 2>&1
    if ($pythonVer -match "Python 3\.(1[0-9]|[0-9])") {
        Write-Host "✅ Python: $pythonVer" -ForegroundColor Green
    } else {
        Write-Host "❌ Python 版本过低: $pythonVer (需要 3.10+)" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "❌ 未找到 python 命令。请安装 Python 3.10+ 并添加到 PATH" -ForegroundColor Red
    $allGood = $false
}

# 2. 检查虚拟环境
Write-Host "`n[2/6] 检查虚拟环境..." -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ 虚拟环境存在" -ForegroundColor Green
} else {
    Write-Host "❌ 虚拟环境不存在！请先运行: .\setup.ps1" -ForegroundColor Red
    $allGood = $false
}

# 3. 检查是否在虚拟环境中
Write-Host "`n[3/6] 检查是否激活虚拟环境..." -ForegroundColor Yellow
$venvPython = $env:VIRTUAL_ENV
if ($venvPython) {
    Write-Host "✅ 虚拟环境已激活: $venvPython" -ForegroundColor Green
} else {
    Write-Host "⚠️ 虚拟环境未激活！建议先执行:" -ForegroundColor Yellow
    Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "   然后重新运行此检查脚本" -ForegroundColor Yellow
    $allGood = $false
}

# 4. 检查关键依赖
Write-Host "`n[4/6] 检查依赖包..." -ForegroundColor Yellow
$required = @("streamlit", "pypdf", "langchain", "langchain-openai", "chromadb")
$missing = @()

foreach ($pkg in $required) {
    $found = pip show $pkg 2>$null
    if ($found) {
        Write-Host "✅ $pkg 已安装" -ForegroundColor Green
    } else {
        Write-Host "❌ $pkg 未安装" -ForegroundColor Red
        $missing += $pkg
        $allGood = $false
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`n请执行: pip install -r requirements.txt" -ForegroundColor Yellow
}

# 5. 检查 .env 和 DeepSeek Key
Write-Host "`n[5/6] 检查 .env 配置..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DEEPSEEK_API_KEY=sk-") {
        Write-Host "✅ .env 存在且包含 DeepSeek Key" -ForegroundColor Green
    } else {
        Write-Host "❌ .env 存在，但 DEEPSEEK_API_KEY 未正确设置" -ForegroundColor Red
        Write-Host "   请编辑 .env 文件，填入你的 sk- 开头的 Key" -ForegroundColor Yellow
        $allGood = $false
    }
} else {
    Write-Host "❌ .env 文件不存在！" -ForegroundColor Red
    Write-Host "   请复制 .env.example 为 .env 并填入 Key" -ForegroundColor Yellow
    $allGood = $false
}

# 6. 尝试导入核心模块（最终验证）
Write-Host "`n[6/6] 验证核心模块导入..." -ForegroundColor Yellow
try {
    python -c "from resume_parser import process_resume; from rag_engine import index_resume; print('✅ 核心模块导入成功')" 2>&1
    Write-Host "✅ 所有核心模块可正常导入" -ForegroundColor Green
} catch {
    Write-Host "❌ 模块导入失败: $_" -ForegroundColor Red
    Write-Host "   请确认已激活虚拟环境并安装了依赖" -ForegroundColor Yellow
    $allGood = $false
}

Write-Host "`n========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "🎉 所有检查通过！你现在可以运行：" -ForegroundColor Green
    Write-Host "   streamlit run app.py" -ForegroundColor Green
    Write-Host ""
    Write-Host "浏览器会自动打开 http://localhost:8501" -ForegroundColor Green
} else {
    Write-Host "⚠️ 存在问题，请根据上方提示修复后再试。" -ForegroundColor Red
    Write-Host "   修复后重新运行: .\check_install.ps1" -ForegroundColor Yellow
}
Write-Host ""