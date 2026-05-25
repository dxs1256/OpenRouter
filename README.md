# OpenRouter 免费模型监控

监控 OpenRouter 平台上的免费模型，自动跟踪模型变化并通过 PushPlus 推送通知。

## 📊 当前免费模型列表

| # | 模型名称 | Model ID | 上下文长度 | 提供商 |
|---|---------|----------|-----------|--------|
| 1 | Google: Gemma 4 26B A4B (free) | `google/gemma-4-26b-a4b-it:free` | 262,144 | Google |
| 2 | Google: Gemma 4 31B (free) | `google/gemma-4-31b-it:free` | 262,144 | Google |
| 3 | Meta: Llama 3.3 70B Instruct (free) | `meta-llama/llama-3.3-70b-instruct:free` | 131,072 | Meta |
| 4 | Meta: Llama 3.2 3B Instruct (free) | `meta-llama/llama-3.2-3b-instruct:free` | 131,072 | Meta |
| 5 | NVIDIA: Nemotron 3 Super (free) | `nvidia/nemotron-3-super-120b-a12b:free` | 1,000,000 | NVIDIA |
| 6 | Qwen: Qwen3 Coder 480B A35B (free) | `qwen/qwen3-coder:free` | 1,048,576 | Qwen |
| 7 | DeepSeek: DeepSeek V4 Flash (free) | `deepseek/deepseek-v4-flash:free` | 1,048,576 | DeepSeek |
| 8 | OpenAI: gpt-oss-120b (free) | `openai/gpt-oss-120b:free` | 131,072 | OpenAI |
| 9 | OpenAI: gpt-oss-20b (free) | `openai/gpt-oss-20b:free` | 131,072 | OpenAI |
| 10 | OpenRouter Owl Alpha | `openrouter/owl-alpha` | 1,048,756 | OpenRouter |

> 📌 **最后更新**: 2026-05-25 03:00:00 UTC  
> 📊 **总计**: 10 个免费模型

---

## 🔔 通知说明

- **新模型上线**: 推送新模型名称、ID、上下文长度
- **模型下架**: 推送下架模型名称
- **无变化**: 不发送推送，避免打扰

---

## 🚀 使用方式

### 配置 PushPlus Secret

1. 微信扫码关注"推送加"公众号
2. 发送消息"token"获取你的 Token
3. 在仓库设置中配置 Secret：
   - **Name**: `PUSHPLUS_TOKEN`
   - **Value**: 你的 PushPlus token

### 手动触发

访问 Actions 页面 → 选择 workflow → 点击 **Run workflow**

### 自动运行

每小时自动检查一次（UTC 时间整点）

---

## 📁 文件说明

```
.
├── .github/workflows/monitor.yml    # GitHub Actions 工作流
├── openrouter-monitor-pushplus.py   # 监控脚本
└── README.md                        # 说明文档（含模型列表）
```

---

## 📈 监控历史

查看 [Actions](https://github.com/dxs1256/OpenRouter/actions) 了解运行记录。

---

**最后更新**: 2026-05-25
