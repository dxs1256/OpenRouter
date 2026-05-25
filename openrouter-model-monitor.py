#!/usr/bin/env python3
"""
OpenRouter 免费模型监控脚本
监控 https://openrouter.ai/models?q=free 中的免费模型
当有新模型上线时发送通知
"""

import json
import time
import hashlib
import os
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("正在安装 requests 库...")
    os.system("pip3 install --break-system-packages requests")
    import requests

# 配置
DATA_FILE = Path(__file__).parent / "openrouter_models_cache.json"
NOTIFICATION_FILE = Path(__file__).parent / "openrouter_notifications.log"
CHECK_INTERVAL = 3600  # 检查间隔（秒），默认 1 小时
OPENROUTER_API = "https://openrouter.ai/api/v1/models"


def fetch_free_models():
    """从 OpenRouter API 获取所有免费模型"""
    try:
        response = requests.get(OPENROUTER_API, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 过滤免费模型（pricing 为 0 的模型）
        free_models = []
        for model in data.get("data", []):
            pricing = model.get("pricing", {})
            # 检查 prompt 和 completion 是否都免费
            if pricing.get("prompt", "0") == "0" and pricing.get("completion", "0") == "0":
                free_models.append({
                    "id": model.get("id"),
                    "name": model.get("name"),
                    "context_length": model.get("context_length"),
                    "pricing": pricing,
                    "description": model.get("description", ""),
                    "top_provider": model.get("top_provider", {}),
                })
        
        return free_models
    except Exception as e:
        print(f"[错误] 获取模型列表失败：{e}")
        return None


def load_cached_models():
    """加载缓存的模型列表"""
    if not DATA_FILE.exists():
        return None
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("models", [])
    except Exception as e:
        print(f"[警告] 加载缓存失败：{e}")
        return None


def save_models_cache(models):
    """保存模型列表到缓存"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "models": models
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[错误] 保存缓存失败：{e}")


def log_notification(message):
    """记录通知到日志文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(NOTIFICATION_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"[错误] 写入日志失败：{e}")
    
    print(log_entry.strip())


def send_notification(title, message):
    """发送通知（支持多种通知方式）"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. 控制台输出
    print("\n" + "=" * 60)
    print(f"🔔 [{timestamp}] {title}")
    print("=" * 60)
    print(message)
    print("=" * 60 + "\n")
    
    # 2. 记录到日志
    full_message = f"{title}\n{message}"
    log_notification(full_message)
    
    # 3. 桌面通知（如果可用）
    try:
        if os.name == "posix":  # Linux/Mac
            os.system(f'notify-send "OpenRouter 模型监控" "{title}"')
        elif os.name == "nt":  # Windows
            os.system(f'msg * "{title}"')
    except Exception:
        pass  # 桌面通知不可用时忽略


def check_new_models():
    """检查是否有新模型"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查免费模型...")
    
    # 获取当前模型列表
    current_models = fetch_free_models()
    if current_models is None:
        print("[错误] 无法获取模型列表，跳过本次检查")
        return
    
    print(f"当前发现 {len(current_models)} 个免费模型")
    
    # 加载缓存
    cached_models = load_cached_models()
    
    if cached_models is None:
        # 首次运行，保存缓存
        print("[信息] 首次运行，保存初始模型列表")
        save_models_cache(current_models)
        send_notification(
            "监控已启动",
            f"已记录 {len(current_models)} 个免费模型\n后续发现新模型时将通知您"
        )
        return
    
    # 比较模型 ID
    cached_ids = {model["id"] for model in cached_models}
    current_ids = {model["id"] for model in current_models}
    
    # 找出新模型
    new_model_ids = current_ids - cached_ids
    
    if new_model_ids:
        # 发现新模型
        new_models = [m for m in current_models if m["id"] in new_model_ids]
        
        notification_msg = "发现以下新的免费模型：\n\n"
        for model in new_models:
            notification_msg += f"🆕 {model['name']}\n"
            notification_msg += f"   ID: {model['id']}\n"
            notification_msg += f"   上下文长度：{model.get('context_length', 'N/A')}\n"
            if model.get('description'):
                desc = model['description'][:100] + "..." if len(model.get('description', '')) > 100 else model['description']
                notification_msg += f"   描述：{desc}\n"
            notification_msg += "\n"
        
        notification_msg += f"\n总计：{len(new_models)} 个新模型"
        
        send_notification("发现新免费模型！", notification_msg)
        
        # 更新缓存
        save_models_cache(current_models)
    else:
        print("[信息] 没有新模型")
    
    # 检查是否有模型下架
    removed_ids = cached_ids - current_ids
    if removed_ids:
        removed_models = [m for m in cached_models if m["id"] in removed_ids]
        notification_msg = "以下免费模型已下架：\n\n"
        for model in removed_models:
            notification_msg += f"❌ {model.get('name', model['id'])}\n"
            notification_msg += f"   ID: {model['id']}\n\n"
        
        send_notification("模型下架通知", notification_msg)
        save_models_cache(current_models)


def main():
    """主函数"""
    print("OpenRouter 免费模型监控脚本")
    print("=" * 40)
    print(f"监控地址：{OPENROUTER_API}")
    print(f"检查间隔：{CHECK_INTERVAL} 秒 ({CHECK_INTERVAL / 3600} 小时)")
    print(f"缓存文件：{DATA_FILE}")
    print(f"日志文件：{NOTIFICATION_FILE}")
    print("=" * 40)
    
    # 首次检查
    check_new_models()
    
    # 持续监控
    print(f"\n开始持续监控，按 Ctrl+C 停止...")
    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            check_new_models()
    except KeyboardInterrupt:
        print("\n[信息] 监控已停止")


if __name__ == "__main__":
    main()
