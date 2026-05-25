# PushPlus 通知配置指南

## 关于 PushPlus

PushPlus（推送加）是一个免费的推送通知服务，支持：
- 微信公众号推送
- 短信推送
- 邮件推送
- 钉钉/企业微信/飞书
- Webhook

官网：https://www.pushplus.plus/

---

## 配置步骤

### 1. 注册 PushPlus

1. 访问 https://www.pushplus.plus/
2. 使用微信扫码关注公众号
3. 获取 Token

### 2. 获取 Token

1. 关注微信公众号"推送加"
2. 发送消息"token"获取您的个人 Token
3. 或访问后台查看：https://www.pushplus.plus/doc/

### 3. 配置 GitHub Secret

```bash
# 方法一：使用 GitHub CLI
gh secret set PUSHPLUS_TOKEN --body "你的 token"

# 方法二：GitHub 网站操作
# 1. 访问仓库 Settings
# 2. Secrets and variables -> Actions
# 3. New repository secret
#    Name: PUSHPLUS_TOKEN
#    Value: 你的 token
```

### 4. （可选）配置群组推送

如果需要推送给多人群组：

```bash
# 使用 GitHub CLI
gh secret set PUSHPLUS_TOPIC --body "你的群组编码"

# 或在 GitHub 网站配置
# Name: PUSHPLUS_TOPIC
# Value: 群组编码
```

---

## 使用其他推送渠道

### 钉钉机器人

1. 创建钉钉机器人
2. 获取 Webhook URL
3. 使用钉钉通知版本：`openrouter-monitor-dingtalk.py`

### 企业微信

1. 创建企业微信应用
2. 配置 Webhook
3. 使用企业微信版本

### 飞书

1. 创建飞书机器人
2. 获取 Webhook URL
3. 使用飞书通知版本

---

## 测试推送

### 手动触发测试

1. 在 GitHub 仓库点击 **Actions**
2. 选择 **OpenRouter Model Monitor**
3. 点击 **Run workflow**
4. 查看运行结果

### 验证推送

```bash
# 本地测试（需要设置环境变量）
export PUSHPLUS_TOKEN="你的 token"
python openrouter-monitor-pushplus.py
```

---

## 推送频率说明

- **首次运行**：发送"监控已启动"通知，包含当前模型总数
- **后续运行**：只有发现新模型时才推送
- **无新模型**：不发送通知，避免骚扰

---

## 注意事项

1. **Token 安全**
   - 永远不要在代码中硬编码 Token
   - 使用 GitHub Secrets 存储
   - 定期轮换 Token

2. **推送频率**
   - PushPlus 对免费用户有频率限制
   - 建议设置合理的监控间隔（如每小时一次）
   - 避免设置 cron 为每分钟运行

3. **消息格式**
   - 支持 HTML 和纯文本两种格式
   - HTML 格式显示效果更好
   - 自动在末尾添加时间戳

---

## 常见问题

### Q: 没有收到推送？

**检查：**
1. Secret 是否正确配置
2. GitHub Actions 是否启用了
3. 查看 Actions 运行日志
4. 确认 PushPlus Token 有效

### Q: 推送失败？

**查看日志：**
- Actions -> 最近的运行 -> 查看详细日志
- 常见的错误：Token 无效、网络超时

### Q: 如何修改推送频率？

编辑工作流文件：

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # 每 2 小时一次
```

---

## 下一步

1. ✅ 注册 PushPlus 并获取 Token
2. ✅ 在 GitHub 配置 Secret: `PUSHPLUS_TOKEN`
3. ✅ 推送代码：`git push`
4. ✅ 手动触发一次测试
5. ✅ 等待自动运行

---

## 相关链接

- PushPlus 官网：https://www.pushplus.plus/
- PushPlus 文档：https://www.pushplus.plus/doc/
- GitHub Secrets: https://docs.github.com/en/actions/security-guides/encrypted-secrets
