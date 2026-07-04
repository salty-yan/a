@echo off
chcp 65001 >nul
echo ============================================
echo   TarotInsight Windows 打包脚本
echo ============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [2/3] 开始打包（约 3-8 分钟）...
python build_exe.py
if %errorlevel% neq 0 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [3/3] 打包完成！
echo exe 文件位于: dist\TarotInsight\TarotInsight.exe
echo.
echo 提示：请将 dist\TarotInsight\ 整个文件夹复制到其他电脑使用，
echo      因为该文件夹包含了 exe 运行所需的卡牌图片等资源文件。
pause
