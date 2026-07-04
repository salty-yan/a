@echo off
chcp 65001 >nul
echo ============================================================
echo   TarotInsight - 推送至 GitHub 并自动构建 Windows exe
echo ============================================================
echo.
echo 步骤预览:
echo   1. 在浏览器打开 https://github.com/new 创建新仓库
echo   2. 仓库名建议填: TarotInsight
echo   3. 不要勾选 "Add a README file"
echo   4. 创建后复制仓库地址（如 https://github.com/你的用户名/TarotInsight.git）
echo   5. 回到本窗口，粘贴仓库地址
echo.
set /p REPO_URL="请输入 GitHub 仓库地址: "

echo.
echo [1/2] 添加远程仓库...
git remote add origin %REPO_URL%
if %errorlevel% neq 0 (
    echo 远程仓库已存在，尝试更新...
    git remote set-url origin %REPO_URL%
)

echo.
echo [2/2] 推送代码（首次推送用 main 分支）...
git branch -M main
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo [错误] 推送失败，可能原因:
    echo   - 仓库地址不正确
    echo   - 未登录 GitHub（请确保已配置 SSH Key 或 Personal Access Token）
    echo   - 网络连接问题
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   推送成功！GitHub Actions 将自动开始构建 Windows exe
echo.
echo   查看构建进度:
echo     浏览器打开 %REPO_URL%/actions
echo.
echo   约 5-10 分钟后，在 Actions 页面的最新运行记录中
echo   点击 "TarotInsight-Windows-exe" 即可下载 exe 压缩包
echo ============================================================
pause
