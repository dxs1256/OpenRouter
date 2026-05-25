# GitHub 仓库设置指南

## 方法一：使用脚本（推荐）

### 前提条件
1. 安装 GitHub CLI: https://github.com/cli/cli#installation
2. 登录 GitHub: `gh auth login`

### 执行步骤

```bash
# 1. 初始化 git 仓库
git init
git add .
git commit -m "Initial commit: OpenRouter model monitor"

# 2. 运行设置脚本
chmod +x setup-github-repo.sh
./setup-github-repo.sh

# 3. 推送到 GitHub
git push -u origin main
```

### 启用 GitHub Actions

1. 访问创建的仓库：https://github.com/你的用户名/openrouter-model-monitor
2. 点击 **Actions** 标签
3. 点击 **I understand my workflows, go ahead and enable them**

---

## 方法二：手动创建

### 1. 创建仓库

```bash
# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 创建远程仓库（在 GitHub 网站上操作）
# 访问：https://github.com/new
# 仓库名：openrouter-model-monitor
# 描述：监控 OpenRouter 免费模型
# 可见性：Public 或 Private
```

### 2. 关联远程仓库

```bash
# 替换为你的仓库地址
git remote add origin https://github.com/你的用户名/openrouter-model-monitor.git
git branch -M main
git push -u origin main
```

### 3. 配置 GitHub Actions

1. 在仓库页面点击 **Actions**
2. 点击 **set up a workflow yourself**
3. 复制 `.github/workflows/monitor.yml` 的内容
4. 点击 **Start commit** -> **Commit new file**

### 4. 启用工作流

- 如果是 Private 仓库，需要手动批准第一次运行
- 访问 **Actions** -> 选择工作流 -> **Enable workflow**

---

## 配置通知方式

### 1. GitHub Issue 通知（已配置）

工作流会自动创建 Issue 通知新模型

### 2. 邮件通知

GitHub会自动发送邮件到：
- 仓库所有者
- 被@提及的用户

设置：https://github.com/settings/notifications

### 3. Discord 通知

修改 `.github/workflows/monitor.yml`，添加：

```yaml
- name: Discord 通知
  if: success()
  uses: Ilshin02/discord-web-action@v1.0.0
  with:
    DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
    MESSAGE: '发现新模型！请查看 Issue'
```

在仓库设置中添加 Secret:
**Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**
- Name: `DISCORD_WEBHOOK`
- Value: 你的 Discord Webhook URL

### 4. 钉钉/飞书通知

类似 Discord，添加对应的 Webhook Secret

---

## 验证工作流

### 手动触发测试

```bash
# 在 GitHub 网站操作:
# Actions -> OpenRouter Model Monitor -> Run workflow -> Run workflow
```

### 查看运行日志

```bash
# GitHub 网站: Actions -> 点击最近的运行记录 -> 查看日志
```

### 查看缓存文件

```bash
# 在仓库中查看 openrouter_models_cache.json
# 或下载 artifact
```

---

## 自定义监控频率

编辑 `.github/workflows/monitor.yml`:

```yaml
on:
  schedule:
    # 每 30 分钟
    - cron: '*/30 * * * *'
    
    # 每 6 小时
    - cron: '0 */6 * * *'
    
    # 每天早上 9 点 (UTC)
    - cron: '0 9 * * *'
```

Cron 表达式参考：https://crontab.guru/

---

## 故障排查

### 工作流没有运行

1. 检查 Actions 是否已启用
2. 检查 cron 表达式是否正确（注意是 UTC 时间）
3. 手动触发测试

### 创建 Issue 失败

1. 确认使用 `GITHUB_TOKEN` 有权限创建 Issue
2. 查看工作流日志中的错误信息

### 没有找到新模型

1. 首次运行会保存基准模型列表
2. 之后只会有新模型出现时才通知
3. 可以删除缓存文件重置：Actions 中手动触发，修改脚本添加 `rm openrouter_models_cache.json`

---

## 安全提示

⚠️ **永远不要**在代码中硬编码 Token
⚠️ **永远不要**在聊天中分享 Token
⚠️ 使用 GitHub Secrets 存储敏感信息
⚠️ 定期轮换 Token

---

## 仓库地址模板

```
https://github.com/你的用户名/openrouter-model-monitor
```

---

## 下一步

1. ✅ 创建仓库
2. ✅ 推送代码
3. ✅ 启用 Actions
4. ✅ 等待第一次自动运行（或手动触发）
5. ✅ 配置额外通知（可选）
