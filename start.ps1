# start.ps1
# 方便的启动脚本（双击即可运行）
# 使用前请确保已经运行过 .\setup.ps1 并配置好 .env 中的 DeepSeek Key

Write-Host "正在启动 AI Resume Assistant..." -ForegroundColor Cyan

# 激活虚拟环境
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "❌ 未找到虚拟环境，请先运行 .\setup.ps1" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 启动 Streamlit
streamlit run app.py

# 如果 Streamlit 退出，保持窗口打开方便看错误信息
Read-Host "应用已退出，按回车键关闭窗口"