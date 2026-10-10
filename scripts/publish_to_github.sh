#!/bin/bash
set -e

# ==============================================================================
# StockLearning 一键初始化与 GitHub 发布脚本
# ==============================================================================

REPO_URL="$1"

if [ -z "$REPO_URL" ]; then
    echo "使用方法: ./scripts/publish_to_github.sh <YOUR_GITHUB_REPO_URL>"
    echo "示例: ./scripts/publish_to_github.sh https://github.com/hsthanb4/stocklearning.git"
    exit 1
fi

echo "🚀 [1/4] 初始化本地 Git 仓库..."
git init

echo "📦 [2/4] 提交主分支 (包含题目版、文档与 Web 平台)..."
git add .
git commit -m "feat: initial commit for stocklearning interactive curriculum" || true
git branch -M main

echo "🔗 [3/4] 关联远程仓库: $REPO_URL ..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

echo "📤 [4/4] 推送至 GitHub main 分支..."
git push -u origin main

echo "=============================================================================="
echo "🎉 发布成功！"
echo "👉 请前往 GitHub 仓库设置 (Settings -> Pages):"
echo "   - Source 选择: Deploy from a branch"
echo "   - Branch 选择: main, Folder 选择: /web"
echo "   完成后你的在线课程平台即可通过 GitHub Pages 免费公开发布！"
echo "=============================================================================="
