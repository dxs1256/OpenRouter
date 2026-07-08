# OpenRouter 免费模型监控

监控 OpenRouter 平台上的免费模型，自动跟踪模型变化并通过 PushPlus 推送通知。

## 📊 当前免费模型列表

| # | 模型名称 | Model ID | 上下文长度 | 提供商 | 综合评分 |
| # | 模型名称 | Model ID | 上下文长度 | 提供商 | 推理评分 |
|---|---------|----------|-----------|--------|----------|
| 1 | Qwen: Qwen3 Coder 480B A35B (free) | `qwen/qwen3-coder:free` | 1,048,576 | Qwen | ⭐140 |
| 2 | Nous: Hermes 3 405B Instruct (free) | `nousresearch/hermes-3-llama-3.1-405b:free` | 131,072 | Nous | ⭐118 |
| 3 | OpenAI: gpt-oss-120b (free) | `openai/gpt-oss-120b:free` | 131,072 | OpenAI | ⭐113 |
| 4 | Google: Lyria 3 Pro Preview | `google/lyria-3-pro-preview` | 1,048,576 | Google | ⭐105 |
| 5 | Google: Lyria 3 Clip Preview | `google/lyria-3-clip-preview` | 1,048,576 | Google | ⭐105 |
| 6 | OpenAI: gpt-oss-20b (free) | `openai/gpt-oss-20b:free` | 131,072 | OpenAI | ⭐103 |
| 7 | Meta: Llama 3.3 70B Instruct (free) | `meta-llama/llama-3.3-70b-instruct:free` | 131,072 | Meta | ⭐103 |
| 8 | Google: Gemma 4 26B A4B  (free) | `google/gemma-4-26b-a4b-it:free` | 262,144 | Google | ⭐100 |
| 9 | Google: Gemma 4 31B (free) | `google/gemma-4-31b-it:free` | 262,144 | Google | ⭐100 |
| 10 | Qwen: Qwen3 Next 80B A3B Instruct (free) | `qwen/qwen3-next-80b-a3b-instruct:free` | 262,144 | Qwen | ⭐100 |
| 11 | NVIDIA: Nemotron 3 Ultra (free) | `nvidia/nemotron-3-ultra-550b-a55b:free` | 1,000,000 | NVIDIA | ⭐98 |
| 12 | NVIDIA: Nemotron 3 Super (free) | `nvidia/nemotron-3-super-120b-a12b:free` | 1,000,000 | NVIDIA | ⭐98 |
| 13 | Meta: Llama 3.2 3B Instruct (free) | `meta-llama/llama-3.2-3b-instruct:free` | 131,072 | Meta | ⭐96 |
| 14 | NVIDIA: Nemotron 3 Nano 30B A3B (free) | `nvidia/nemotron-3-nano-30b-a3b:free` | 256,000 | NVIDIA | ⭐93 |
| 15 | NVIDIA: Nemotron 3 Nano Omni (free) | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | 256,000 | NVIDIA | ⭐90 |
| 16 | NVIDIA: Nemotron Nano 12B 2 VL (free) | `nvidia/nemotron-nano-12b-v2-vl:free` | 128,000 | NVIDIA | ⭐90 |
| 17 | NVIDIA: Nemotron Nano 9B V2 (free) | `nvidia/nemotron-nano-9b-v2:free` | 128,000 | NVIDIA | ⭐90 |
| 18 | NVIDIA: Nemotron 3.5 Content Safety (free) | `nvidia/nemotron-3.5-content-safety:free` | 128,000 | NVIDIA | ⭐89 |
| 19 | LiquidAI: LFM2.5-1.2B-Thinking (free) | `liquid/lfm-2.5-1.2b-thinking:free` | 32,768 | LiquidAI | ⭐88 |
| 20 | Free Models Router | `openrouter/free` | 200,000 | OpenRouter | ⭐77 |
| 21 | LiquidAI: LFM2.5-1.2B-Instruct (free) | `liquid/lfm-2.5-1.2b-instruct:free` | 32,768 | LiquidAI | ⭐73 |
| 22 | Tencent: Hy3 (free) | `tencent/hy3:free` | 262,144 | Tencent | ⭐72 |
| 23 | Poolside: Laguna XS 2.1 (free) | `poolside/laguna-xs-2.1:free` | 262,144 | Poolside | ⭐72 |
| 24 | Cohere: North Mini Code (free) | `cohere/north-mini-code:free` | 256,000 | Cohere | ⭐72 |
| 25 | Poolside: Laguna XS.2 (free) | `poolside/laguna-xs.2:free` | 262,144 | Poolside | ⭐72 |
| 26 | Poolside: Laguna M.1 (free) | `poolside/laguna-m.1:free` | 262,144 | Poolside | ⭐72 |
| 27 | Venice: Uncensored (free) | `cognitivecomputations/dolphin-mistral-24b-venice-edition:free` | 32,768 | Venice | ⭐65 |

> 📌 **最后更新**: 2026-07-08 12:16:35 (北京时间)  
> 📊 **总计**: 27 个免费模型
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
