#!/bin/bash
# GitHub 仓库创建和工作流配置脚本
# 使用前请确保已安装 gh CLI 工具

set -e

# 配置变量
REPO_NAME="openrouter-model-monitor"
REPO_DESC="监控 OpenRouter 免费模型并在发现新模型时通知"
REPO_VISIBILITY="public"  # 或 private

echo "=== GitHub 仓库创建和配置脚本 ==="
echo "仓库名：$REPO_NAME"
echo "描述：$REPO_DESC"
echo "可见性：$REPO_VISIBILITY"
echo ""

# 检查 gh 是否已安装
if ! command -v gh &> /dev/null; then
    echo "错误：gh CLI 未安装"
    echo "请先安装：https://github.com/cli/cli#installation"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "请先登录 GitHub：gh auth login"
    exit 1
fi

echo "✓ gh CLI 已安装并登录"
echo ""

# 创建仓库
echo "正在创建仓库..."
gh repo create "$REPO_NAME" \
    --description "$REPO_DESC" \
    --visibility "$REPO_VISIBILITY" \
    --source=. \
    --push \
    --remote=origin

echo "✓ 仓库创建成功"
echo ""

# 创建 GitHub Actions 工作流目录
mkdir -p .github/workflows

# 创建监控工作流
cat > .github/workflows/monitor.yml << 'EOF'
name: OpenRouter Model Monitor

on:
  schedule:
    # 每小时运行一次（UTC 时间）
    - cron: '0 * * * *'
  workflow_dispatch:
    # 允许手动触发

jobs:
  check-models:
    runs-on: ubuntu-latest
    
    steps:
    - name: 检出代码
      uses: actions/checkout@v4
    
    - name: 设置 Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install requests
    
    - name: 检查新模型
      run: python openrouter-monitor-simple.py
    
    - name: 上传缓存文件
      uses: actions/upload-artifact@v4
      with:
        name: model-cache
        path: openrouter_models_cache.json
        retention-days: 30

    - name: 发送通知
      if: failure()
      run: |
        echo "检测到新模型，请查看输出日志"
EOF

echo "✓ 工作流配置已创建"
echo ""

# 复制监控脚本
cp openrouter-monitor-simple.py .

echo "=== 配置完成 ==="
echo ""
echo "下一步操作："
echo "1. 推送到 GitHub: git push -u origin main"
echo "2. 在 GitHub 上启用 Actions: 访问仓库 -> Actions -> 启用工作流"
echo "3. 配置通知（可选）："
echo "   - 邮件通知：在 GitHub 设置中配置"
echo "   - Discord/Slack：添加对应的 Action step"
echo ""
echo "仓库地址：https://github.com/$(gh api user | jq -r '.login')/$REPO_NAME"
