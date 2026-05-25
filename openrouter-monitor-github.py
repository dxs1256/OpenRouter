#!/usr/bin/env python3
"""
OpenRouter 免费模型监控 - GitHub Actions 版本
支持创建 Issue 通知新模型
"""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests

DATA_FILE = Path(__file__).parent / "openrouter_models_cache.json"
OPENROUTER_API = "https://openrouter.ai/api/v1/models"

# GitHub 配置（从环境变量读取）
GH_TOKEN = os.getenv("GH_TOKEN")
GH_REPO = os.getenv("GITHUB_REPOSITORY", "")
GH_API = f"https://api.github.com/repos/{GH_REPO}"


def fetch_free_models():
    """获取所有免费模型"""
    response = requests.get(OPENROUTER_API, timeout=30, headers={
        "Accept": "application/json"
    })
    response.raise_for_status()
    data = response.json()
    
    free_models = []
    for model in data.get("data", []):
        pricing = model.get("pricing", {})
        if pricing.get("prompt", "0") == "0" and pricing.get("completion", "0") == "0":
            free_models.append({
                "id": model.get("id"),
                "name": model.get("name"),
                "context_length": model.get("context_length"),
                "pricing": pricing,
            })
    
    return free_models


def create_github_issue(title, body):
    """创建 GitHub Issue 通知"""
    if not GH_TOKEN:
        print("[提示] 未设置 GH_TOKEN，跳过 Issue 创建")
        return
    
    headers = {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": title,
        "body": body,
        "labels": ["new-model", "openrouter"]
    }
    
    response = requests.post(
        f"{GH_API}/issues",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code == 201:
        issue_url = response.json().get("html_url")
        print(f"✓ Issue 已创建：{issue_url}")
        return issue_url
    else:
        print(f"创建 Issue 失败：{response.status_code} - {response.text}")


def check():
    """检查新模型"""
    current = fetch_free_models()
    print(f"\n发现 {len(current)} 个免费模型")
    
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"models": current}, f, ensure_ascii=False, indent=2)
        print("✓ 已保存初始模型列表")
        return
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        cached = json.load(f).get("models", [])
    
    cached_ids = {m["id"] for m in cached}
    current_ids = {m["id"] for m in current}
    new_ids = current_ids - cached_ids
    
    if new_ids:
        new_models = [m for m in current if m["id"] in new_ids]
        
        # 构建通知内容
        title = f"🎉 发现 {len(new_models)} 个新的免费模型"
        body = f"""
## 发现时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)

## 新模型列表

| 模型名称 | Model ID | 上下文长度 |
|---------|----------|-----------|
"""
        for model in new_models:
            body += f"| {model['name']} | `{model['id']}` | {model.get('context_length', 'N/A'):,} |\n"
        
        body += f"""
## 查看详情
访问 OpenRouter 查看所有免费模型：https://openrouter.ai/models?q=free

---
*此 Issue 由 OpenRouter Model Monitor 自动创建*
"""
        
        print(f"\n🎉 发现 {len(new_models)} 个新模型：")
        for model in new_models:
            print(f"  • {model['name']} ({model['id']})")
        
        # 创建 GitHub Issue
        create_github_issue(title, body)
        
        # 更新缓存
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"models": current}, f, ensure_ascii=False, indent=2)
    else:
        print("\n✓ 没有新模型")


if __name__ == "__main__":
    check()
