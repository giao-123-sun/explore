# Day 2 调研：技能生态 + Error Learning + 浏览器会话共享

**调研日期**: 2026-03-29

---

## 一、Claude Code 技能生态

### 全景规模
- 官方 Marketplace：101 个插件
- 社区 Skills：2,300+
- OpenClaw 生态：13,700+（筛选后 5,200+，但 36.8% 有安全漏洞）

### 核心项目

| 项目 | Stars | 核心差异 | 安全等级 |
|------|-------|---------|---------|
| **Superpowers** (obra) | 121K | 方法论驱动：TDD + 系统调试 + code review，14 个核心 skill | 高（官方审计） |
| **Oh My Claude Code** | 15K | 32 agent 多 agent 编排，智能模型路由 | 中高 |
| **官方 Marketplace** | 15.2K | Anthropic 维护，101 个插件 | 最高 |
| **awesome-agent-skills** | 13.2K | 1,030+ skill，来自 Vercel/Stripe/Cloudflare 等 | 中高 |
| **awesome-openclaw-skills** | 42.8K | 5,211 个筛选 skill | 低-中（36.8% 有漏洞） |

### 安全是最大问题

Snyk 2026-02 ToxicSkills 研究：
- ClawHub **36.8% 的 skill 有安全漏洞**，76 个确认恶意
- 91% 恶意 skill 结合 prompt injection + 传统恶意软件
- 类似早期 npm/PyPI 的 supply chain 安全问题

**建议**：优先用 **Superpowers + 官方 Marketplace**（纯指令型、经审计）。对含可执行代码的社区 skill 保持警惕。

### Superpowers 详解

121K stars 不是浪得虚名。核心不是"一堆 skill 的集合"，而是一套**方法论**：
- TDD-first：先写测试再写代码
- 系统调试：不盲目修 bug，先理解系统
- Code Review：自动审查自己的代码
- 14 个 skill 覆盖开发全流程

### Oh My Claude Code 详解

亮点是**多 agent 编排**：
- 32 个预配置 agent
- 智能模型路由（简单任务用 Haiku，复杂任务用 Opus）
- 团队式协作（不同 agent 负责不同环节）

---

## 二、Error Learning Pattern

### 核心思路

> Agent 犯错时，把错误模式写入持久化文件；新任务开始前，先读这个文件，避免重蹈覆辙。

一句 prompt 触发完整循环：
**Reflect（分析出错原因）→ Abstract（提取通用模式）→ Generalize（生成可复用的决策框架）→ Write（写入持久文件）**

### 五种实现变体

| 变体 | 代表 | 核心差异 |
|------|------|---------|
| **CLAUDE.md 追加** | Glen Rhodes 的 lessons.md | 最简方案，犯错后追加 NEVER/ALWAYS 规则 |
| **自动技能提取** | Claudeception | UserPromptSubmit hook 自动评估+提取，有质量门控 |
| **置信度分级反射** | claude-reflect-system | HIGH/MEDIUM/LOW 三级信号分类，Stop hook 自动触发 |
| **摩擦分析** | claude-skill-self-improvement | 分析对话历史，找重复摩擦点 |
| **多通道记忆** | Addy Osmani | Git history + Progress log + Task state + AGENTS.md 四通道互补 |

### 与我们现有系统的对比

| 他们的机制 | 我们已有的对应 | 差距 |
|-----------|--------------|------|
| lessons.md / CLAUDE.md 追加 | skills/failures.md | 已有，格式可优化 |
| Claudeception 自动提取 | PreCompact hook 自动检查 | 已有，但缺少 UserPromptSubmit hook |
| 置信度分级 | 缺失 | 可以加：区分"严重错误"和"小改进" |
| 对话历史摩擦分析 | 缺失 | 需要类似 claude-log-cli 的分析工具 |
| 多通道记忆 | journal/ + skills/ + HISTORY.md + git | 已有雏形 |

**关键缺失**：我们有 PreCompact 和 Stop hook，但没有 **UserPromptSubmit hook** — 这是 Claudeception 的核心，每次用户提交 prompt 时注入"检查是否有可提取知识"的提醒。

---

## 三、GUI/Web Agent 上的 Error Learning

### 核心论文

| 论文 | 会议 | 核心创新 | 效果 |
|------|------|---------|------|
| **WebCoach** | 2025.11 | 跨会话记忆 + FAISS 向量检索 + 运行时经验注入 | 38B: 47.3% → 61.4% |
| **BacktrackAgent** | EMNLP 2025 | 实时错误检测 + 回溯机制 | +7.6% 成功率 |
| **SEAgent** | 2025.08 | 对抗失败模仿（主动惩罚错误模式）| 11.3% → 34.5% |
| **WebAgent-R1** | EMNLP 2025 | 端到端多轮 RL | 8B 模型超过 o3 |

### WebCoach：最接近"CLAUDE.md for web agents"

架构三件套：
1. **WebCondenser** — 压缩导航日志为标准化摘要
2. **External Memory Store** — FAISS 向量数据库，存储轨迹，10ms 检索
3. **Coach Module** — 8B LLM 做运行时介入决策

关键发现：
- **自己的轨迹比别人的好用**：自积累 > GPT-4o 生成的种子数据
- **32B+ 模型才能有效利用记忆**：7B 模型加了记忆反而退步
- **复杂任务收益大**：简单按钮点击没帮助

### Test-time Prompt Learning vs 轨迹蒸馏/RL

| 维度 | Test-time Prompt Learning | 轨迹蒸馏/SFT | RL Fine-tuning |
|------|--------------------------|-------------|----------------|
| 需要训练 | 不需要 | 需要 | 需要 |
| 反馈延迟 | 即时 | 收集+训练 | 大量轨迹+训练 |
| 模型无关 | 高 | 低 | 低 |
| 上限 | 受限 context window | 受限数据质量 | 最高但最贵 |
| 可解释 | 人类可读 | 不可读 | 不可读 |

**sunqi 的判断很准**：现在模型能力足够强（32B+），test-time prompt learning 变得实用了。WebCoach 证明了 38B 开源模型 + 运行时记忆 ≈ GPT-4o 裸跑。

---

## 四、浏览器会话共享工具

### 推荐方案

| 场景 | 工具 | Stars | 安全等级 |
|------|------|-------|---------|
| **日常使用** | Playwright MCP + 独立 user-data-dir | 29.9K | 高（Microsoft 官方） |
| **操控当前页面** | Chrome DevTools MCP + autoConnect | 32.1K | 高（Google 官方） |
| **精细控制** | Playwriter（tab 级授权） | 3.3K | 最高 |
| **最方便** | Playwright 复用 Chrome profile | — | 中（需关 Chrome） |

### 直接读 Chrome Cookie 的现实

Chrome 127+（2024.07）加了 **app-bound encryption**，rookiepy/browser_cookie3 已经**无法解密** cookie。

**实际可行路径**：

```python
# 方案 A：Playwright 复用 Chrome profile（需先关 Chrome）
browser = p.chromium.launch_persistent_context(
    user_data_dir=r"C:\Users\sunqi\AppData\Local\Google\Chrome\User Data",
    channel="chrome",
    headless=False
)
# 打开的页面自动继承所有已登录状态
```

```python
# 方案 B：CDP 连接运行中的 Chrome
# 先用这个命令启动 Chrome：
# chrome.exe --remote-debugging-port=9222
browser = p.chromium.connect_over_cdp("http://localhost:9222")
# 接管当前浏览器的所有 tab 和 cookie
```

### 安全红线

1. **Cloud 方案（Browserbase、browser-use Cloud）cookie 会到第三方服务器** — 个人账号不要用
2. **远程调试端口开放期间本机任何程序都能访问** — 用完必须关
3. **MCP 供应链风险真实存在** — CVE-2025-6514 已证明，只用大厂维护的 server
4. **用独立 profile，不要让 agent 碰主浏览器 profile**

---

## 五、三个话题的交叉点

三个方向不是孤立的，它们汇聚成一个完整的能力栈：

```
┌─────────────────────────────────────────┐
│  Claude Code + Superpowers/OhMy Skills  │  ← 基础能力增强
├─────────────────────────────────────────┤
│  Error Learning (failures.md + hooks)   │  ← 从错误中自动进化
├─────────────────────────────────────────┤
│  浏览器会话共享 (Playwright + Chrome)    │  ← 访问真实世界
├─────────────────────────────────────────┤
│  GUI Agent + WebCoach 式记忆            │  ← 在网页上自主操作并学习
└─────────────────────────────────────────┘
```

**最终形态**：一个能访问你所有网站、从操作错误中自动学习、技能不断进化的 agent。这就是自动化运营的技术基础。

---

## 信息源

### 技能生态
- [Superpowers](https://github.com/obra/superpowers) — 121K stars
- [Oh My Claude Code](https://github.com/Yeachan-Heo/oh-my-claudecode) — 15K stars
- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)

### Error Learning
- [Claudeception](https://github.com/blader/Claudeception)
- [claude-reflect-system](https://github.com/haddock-development/claude-reflect-system)
- [Self-Improving Coding Agents (Addy Osmani)](https://addyosmani.com/blog/self-improving-agents/)
- [WebCoach](https://arxiv.org/abs/2511.12997)
- [BacktrackAgent (EMNLP 2025)](https://arxiv.org/abs/2505.20660)
- [SEAgent](https://github.com/SunzeY/SEAgent)

### 浏览器会话
- [Chrome DevTools MCP](https://github.com/anthropics/mcp-servers) — 32.1K stars
- [Playwright MCP](https://github.com/anthropics/mcp-servers) — 29.9K stars
- [Playwriter](https://github.com/nicholasgriffintn/playwriter) — 3.3K stars
