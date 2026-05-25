#!/usr/bin/env python3
"""
OpenRouter 免费模型监控脚本
- 监控免费模型变化
- 更新 README.md 模型列表
- PushPlus 推送变化通知
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    os.system("pip3 install --break-system-packages requests")
    import requests

# 配置
DATA_FILE = Path(__file__).parent / "openrouter_models_cache.json"
README_FILE = Path(__file__).parent / "README.md"
OPENROUTER_API = "https://openrouter.ai/api/v1/models"

# PushPlus 配置
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "")
PUSHPLUS_TOPIC = os.getenv("PUSHPLUS_TOPIC", "")


def fetch_free_models():
    """获取所有免费模型（按上下文长度排序）"""
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
                "context_length": model.get("context_length", 0),
            })
    
    # 按上下文长度从大到小排序
    free_models.sort(key=lambda x: x.get("context_length", 0), reverse=True)
    
    return free_models


def generate_model_table(models):
    """生成 Markdown 模型表格"""
    table = "| # | 模型名称 | Model ID | 上下文长度 |\n"
    table += "|---|---------|----------|-----------|\n"
    
    for i, model in enumerate(models, 1):
        name = model.get("name", "Unknown")
        model_id = model.get("id", "unknown")
        context = model.get("context_length", 0)
        context_str = f"{context:,}" if context else "N/A"
        
        table += f"| {i} | {name} | `{model_id}` | {context_str} |\n"
    
    return table


def get_model_provider(model_id):
    """从 model_id 提取提供商"""
    provider = model_id.split("/")[0]
    provider_map = {
        "google": "Google",
        "meta-llama": "Meta",
        "nvidia": "NVIDIA",
        "qwen": "Qwen",
        "deepseek": "DeepSeek",
        "openai": "OpenAI",
        "openrouter": "OpenRouter",
        "baidu": "Baidu",
        "poolside": "Poolside",
        "minimax": "MiniMax",
        "liquid": "LiquidAI",
        "z-ai": "Z.ai",
        "cognitivecomputations": "Venice",
        "nousresearch": "Nous",
        "arcee-ai": "Arcee AI",
    }
    return provider_map.get(provider, provider.capitalize())


def generate_full_table(models):
    """生成完整模型表格（按上下文长度排序）"""
    table = "| # | 模型名称 | Model ID | 上下文长度 | 提供商 |\n"
    table += "|---|---------|----------|-----------|--------|\n"
    
    for i, model in enumerate(models, 1):
        name = model.get("name", "Unknown")
        model_id = model.get("id", "unknown")
        context = model.get("context_length", 0)
        context_str = f"{context:,}" if context else "N/A"
        provider = get_model_provider(model_id)
        
        table += f"| {i} | {name} | `{model_id}` | {context_str} | {provider} |\n"
    
    return table


def update_readme(models):
    """更新 README.md 中的模型列表"""
    if not README_FILE.exists():
        return False
    
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 生成新表格
        new_table = generate_full_table(models)
        
        # 北京时间 (UTC+8)
        from datetime import timezone, timedelta
        bj_tz = timezone(timedelta(hours=8))
        bj_time = datetime.now(bj_tz).strftime("%Y-%m-%d %H:%M:%S")
        update_info = f"> 📌 **最后更新**: {bj_time} (北京时间)  \n> 📊 **总计**: {len(models)} 个免费模型"
        
        # 查找并替换表格部分
        pattern = r"(\|\s*#\s*\|\s*模型名称.*?\| 综合评分 \|)(.*?)(>\s*📌\s*\*\*最后更新\*\*:.*?📊.*?个免费模型)"
        replacement = f"| # | 模型名称 | Model ID | 上下文长度 | 提供商 | 综合评分 |\n{new_table}\n{update_info}"
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content == content:
            print("[提示] README 格式不匹配，尝试简单替换...")
            if "| # | 模型名称" in content:
                start = content.find("| # | 模型名称")
                end = content.find("> 📊 **总计**:", start)
                if end > start:
                    end = content.find("\n", end) + 1
                    new_content = content[:start] + new_table + "\n\n" + update_info + content[end:]
        
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"✓ README.md 已更新 (北京时间 {bj_time})")
        return True
    except Exception as e:
        print(f"[错误] 更新 README 失败：{e}")
        return False


def send_pushplus(title, content):
    """发送 PushPlus 通知"""
    if not PUSHPLUS_TOKEN:
        print(f"[提示] 未配置 PUSHPLUS_TOKEN，只在日志显示变化")
        print(f"\n{title}\n")
        return None
    
    content_html = f"""
<h3>{title}</h3>
<p><strong>检测时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
{content}
<hr>
<p style="font-size:12px;color:#999;">此消息由 OpenRouter Model Monitor 自动推送</p>
"""
    
    url = "https://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content_html,
        "template": "html",
        "channel": "wechat"
    }
    
    if PUSHPLUS_TOPIC:
        data["topic"] = PUSHPLUS_TOPIC
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get("code") == 200:
            print("✓ PushPlus 推送成功")
            return True
        else:
            print(f"✗ PushPlus 失败：{result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ PushPlus 请求错误：{e}")
        return False


def check():
    """检查模型变化"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查...")
    
    current = fetch_free_models()
    if not current:
        print("[错误] 获取模型列表失败")
        return
    
    print(f"当前 {len(current)} 个免费模型")
    
    # 加载缓存
    cached = []
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            cached = json.load(f).get("models", [])
    
    cached_ids = {m["id"] for m in cached}
    current_ids = {m["id"] for m in current}
    
    new_ids = current_ids - cached_ids
    removed_ids = cached_ids - current_ids
    
    # 有变化才推送通知
    if new_ids or removed_ids:
        # 构建通知内容
        notify_msg = ""
        
        if new_ids:
            new_models = [m for m in current if m["id"] in new_ids]
            notify_msg += "<h4>✅ 新增模型:</h4><ul>"
            for model in new_models:
                context = model.get("context_length", 0)
                notify_msg += f"<li><strong>{model['name']}</strong><br><small>ID: {model['id']} | 上下文：{context:,}</small></li>"
            notify_msg += "</ul>"
        
        if removed_ids:
            removed_models = [m for m in cached if m["id"] in removed_ids]
            notify_msg += "<h4>❌ 下架模型:</h4><ul>"
            for model in removed_models:
                notify_msg += f"<li>{model.get('name', model['id'])}<br><small>ID: {model['id']}</small></li>"
            notify_msg += "</ul>"
        
        # 发送推送
        title = f"🎯 OpenRouter 模型变化 ({len(new_ids)} 新增/{len(removed_ids)} 下架)"
        send_pushplus(title, notify_msg)
    elif cached:
        print("✓ 无变化，不推送")
    
    # 每次运行都更新缓存和 README
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"models": current, "updated_at": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    
    update_readme(current)
    
    print(f"✓ 检查完成（README 已更新）")


if __name__ == "__main__":
    check()
