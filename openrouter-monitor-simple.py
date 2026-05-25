#!/usr/bin/env python3
"""
OpenRouter 免费模型监控 - 快速检查版本
运行一次，检查是否有新模型
"""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("正在安装 requests 库...")
    os.system("pip3 install --break-system-packages requests")
    import requests

DATA_FILE = Path(__file__).parent / "openrouter_models_cache.json"
OPENROUTER_API = "https://openrouter.ai/api/v1/models"


def fetch_free_models():
    """获取所有免费模型"""
    print("正在获取模型列表...")
    response = requests.get(OPENROUTER_API, timeout=30)
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
        print(f"\n🎉 发现 {len(new_ids)} 个新模型：")
        for model in [m for m in current if m["id"] in new_ids]:
            print(f"  • {model['name']} ({model['id']})")
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"models": current}, f, ensure_ascii=False, indent=2)
    else:
        print("\n✓ 没有新模型")


if __name__ == "__main__":
    check()
