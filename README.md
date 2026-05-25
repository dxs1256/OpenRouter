# OpenRouter 免费模型监控

监控 OpenRouter 平台上的免费模型，自动跟踪模型变化并通过 PushPlus 推送通知。

## 📊 当前免费模型列表

| # | 模型名称 | Model ID | 上下文长度 | 提供商 | 综合评分 |
| # | 模型名称 | Model ID | 上下文长度 | 提供商 | 综合评分 |
|---|---------|----------|-----------|--------|----------|
| 1 | Google: Lyria 3 Pro Preview | `google/lyria-3-pro-preview` | 1,048,576 | Google | ⭐1,992,294 |
| 2 | Google: Lyria 3 Clip Preview | `google/lyria-3-clip-preview` | 1,048,576 | Google | ⭐1,992,294 |
| 3 | NVIDIA: Nemotron 3 Super (free) | `nvidia/nemotron-3-super-120b-a12b:free` | 1,000,000 | NVIDIA | ⭐1,700,000 |
| 4 | Qwen: Qwen3 Coder 480B A35B (free) | `qwen/qwen3-coder:free` | 1,048,576 | Qwen | ⭐1,677,721 |
| 5 | DeepSeek: DeepSeek V4 Flash (free) | `deepseek/deepseek-v4-flash:free` | 1,048,576 | DeepSeek | ⭐1,635,778 |
| 6 | Google: Gemma 4 26B A4B  (free) | `google/gemma-4-26b-a4b-it:free` | 262,144 | Google | ⭐498,073 |
| 7 | Google: Gemma 4 31B (free) | `google/gemma-4-31b-it:free` | 262,144 | Google | ⭐498,073 |
| 8 | NVIDIA: Nemotron 3 Nano Omni (free) | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | 256,000 | NVIDIA | ⭐435,200 |
| 9 | NVIDIA: Nemotron 3 Nano 30B A3B (free) | `nvidia/nemotron-3-nano-30b-a3b:free` | 256,000 | NVIDIA | ⭐435,200 |
| 10 | Qwen: Qwen3 Next 80B A3B Instruct (free) | `qwen/qwen3-next-80b-a3b-instruct:free` | 262,144 | Qwen | ⭐419,430 |
| 11 | MiniMax: MiniMax M2.5 (free) | `minimax/minimax-m2.5:free` | 204,800 | MiniMax | ⭐286,720 |
| 12 | Arcee AI: Trinity Large Thinking (free) | `arcee-ai/trinity-large-thinking:free` | 262,144 | Arcee AI | ⭐262,144 |
| 13 | OpenAI: gpt-oss-120b (free) | `openai/gpt-oss-120b:free` | 131,072 | OpenAI | ⭐262,144 |
| 14 | OpenAI: gpt-oss-20b (free) | `openai/gpt-oss-20b:free` | 131,072 | OpenAI | ⭐262,144 |
| 15 | Meta: Llama 3.3 70B Instruct (free) | `meta-llama/llama-3.3-70b-instruct:free` | 131,072 | Meta | ⭐235,929 |
| 16 | Meta: Llama 3.2 3B Instruct (free) | `meta-llama/llama-3.2-3b-instruct:free` | 131,072 | Meta | ⭐235,929 |
| 17 | NVIDIA: Nemotron Nano 12B 2 VL (free) | `nvidia/nemotron-nano-12b-v2-vl:free` | 128,000 | NVIDIA | ⭐217,600 |
| 18 | NVIDIA: Nemotron Nano 9B V2 (free) | `nvidia/nemotron-nano-9b-v2:free` | 128,000 | NVIDIA | ⭐217,600 |
| 19 | Nous: Hermes 3 405B Instruct (free) | `nousresearch/hermes-3-llama-3.1-405b:free` | 131,072 | Nous | ⭐196,608 |
| 20 | Z.ai: GLM 4.5 Air (free) | `z-ai/glm-4.5-air:free` | 131,072 | Z.ai | ⭐170,393 |
| 21 | Baidu Qianfan: CoBuddy (free) | `baidu/cobuddy:free` | 131,072 | Baidu | ⭐157,286 |
| 22 | Poolside: Laguna XS.2 (free) | `poolside/laguna-xs.2:free` | 131,072 | Poolside | ⭐144,179 |
| 23 | Poolside: Laguna M.1 (free) | `poolside/laguna-m.1:free` | 131,072 | Poolside | ⭐144,179 |
| 24 | LiquidAI: LFM2.5-1.2B-Thinking (free) | `liquid/lfm-2.5-1.2b-thinking:free` | 32,768 | LiquidAI | ⭐29,491 |
| 25 | LiquidAI: LFM2.5-1.2B-Instruct (free) | `liquid/lfm-2.5-1.2b-instruct:free` | 32,768 | LiquidAI | ⭐29,491 |
| 26 | Venice: Uncensored (free) | `cognitivecomputations/dolphin-mistral-24b-venice-edition:free` | 32,768 | Venice | ⭐26,214 |

> 📌 **最后更新**: 2026-05-25 11:42:11 (北京时间)  
> 📊 **总计**: 26 个免费模型
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
