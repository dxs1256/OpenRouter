# OpenRouter 免费模型监控脚本

监控 OpenRouter 平台上的免费模型，当有新模型上线时自动通知。

## 文件说明

- `openrouter-monitor-simple.py` - 快速检查版本（运行一次）
- `openrouter-model-monitor.py` - 持续监控版本（后台运行）
- `openrouter_models_cache.json` - 模型缓存文件（自动生成）
- `openrouter_notifications.log` - 通知日志（自动生成）

## 使用方法

### 方法一：快速检查（推荐）

运行一次，检查是否有新模型：

```bash
python3 openrouter-monitor-simple.py
```

### 方法二：持续监控

后台运行，定期检查（默认每小时检查一次）：

```bash
# 前台运行
python3 openrouter-model-monitor.py

# 后台运行（Linux/Mac）
nohup python3 openrouter-model-monitor.py &

# 后台运行（使用 screen）
screen -S openrouter-monitor
python3 openrouter-model-monitor.py
# 按 Ctrl+A, D .detach
```

### 修改检查间隔

编辑 `openrouter-model-monitor.py`，修改 `CHECK_INTERVAL` 变量：

```python
CHECK_INTERVAL = 1800  # 30 分钟
CHECK_INTERVAL = 7200  # 2 小时
CHECK_INTERVAL = 86400  # 24 小时
```

## 通知方式

脚本支持以下通知方式：

1. **控制台输出** - 实时显示新模型信息
2. **日志文件** - 记录所有通知到 `openrouter_notifications.log`
3. **桌面通知** - 自动调用系统通知（如果可用）

## 查看通知历史

```bash
cat openrouter_notifications.log
```

## 查看当前缓存的模型

```bash
python3 -c "import json; print(json.dumps(json.load(open('openrouter_models_cache.json'))['models'], indent=2, ensure_ascii=False))"
```

## 重置监控

删除缓存文件，重新记录模型列表：

```bash
rm openrouter_models_cache.json
python3 openrouter-monitor-simple.py
```

## 依赖

- Python 3.6+
- requests 库（自动安装）

## 当前免费模型列表

目前监控到 **28 个免费模型**，包括：

- Google: Gemma 4 系列
- NVIDIA: Nemotron 系列
- Meta: Llama 3.x 系列
- OpenAI: gpt-oss 系列
- Qwen: Qwen3 系列
- 以及更多...

## 注意事项

1. 首次运行会保存当前所有免费模型作为基准
2. 之后每次运行只会通知新出现或下架的模型
3. 缓存文件会记录模型 ID、名称和上下文长度等信息
4. 日志文件会记录所有通知，方便回顾

## 数据来源

API: https://openrouter.ai/api/v1/models
网页：https://openrouter.ai/models?q=free
