#!/bin/bash
# TarotInsight - 推送到 GitHub 脚本
# 使用方法: bash push_to_github.sh https://github.com/你的用户名/TarotInsight.git

REPO_URL="$1"

if [ -z "$REPO_URL" ]; then
    echo "============================================================"
    echo "  TarotInsight - 推送至 GitHub"
    echo "============================================================"
    echo ""
    echo "  用法: bash push_to_github.sh <你的GitHub仓库地址>"
    echo ""
    echo "  示例: bash push_to_github.sh https://github.com/zhangsan/TarotInsight.git"
    echo ""
    echo "  如果还没有仓库，请先在浏览器打开: https://github.com/new"
    echo "  - 仓库名填: TarotInsight"
    echo "  - 不要勾选任何初始化选项"
    echo "  - 点击 Create repository"
    echo "  - 复制仓库地址后重新运行本脚本"
    echo ""
    exit 1
fi

echo "[1/2] 添加远程仓库 origin -> $REPO_URL"
git remote add origin "$REPO_URL" 2>/dev/null || {
    echo "  远程仓库已存在，更新地址..."
    git remote set-url origin "$REPO_URL"
}

echo "[2/2] 推送代码到 GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  ✅ 推送成功！"
    echo ""
    echo "  GitHub Actions 将自动开始构建 Windows exe"
    echo "  约 5-10 分钟后，打开以下链接下载:"
    echo ""
    stripped=$(echo "$REPO_URL" | sed 's/\.git$//')
    echo "  $stripped/actions"
    echo ""
    echo "  在最新运行记录中点击 TarotInsight-Windows-exe 下载"
    echo "============================================================"
else
    echo ""
    echo "❌ 推送失败，请检查:"
    echo "  1. 仓库地址是否正确"
    echo "  2. 是否已在 GitHub 登录 (运行: gh auth login)"
    echo "  3. 网络连接是否正常"
    exit 1
fi
