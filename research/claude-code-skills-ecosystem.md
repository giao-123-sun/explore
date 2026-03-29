# Claude Code 技能/增强生态调研

> 调研时间: 2026-03-29
> 调研人: sunqi + Claude

## 一、生态全景

Claude Code 的技能生态在 2025-2026 年爆发式增长，形成了 **官方 Marketplace + 社区框架 + Awesome 列表 + OpenClaw 跨平台** 的多层结构。截至 2026 年 3 月：

- 官方 Marketplace: 101 个插件（33 个 Anthropic 自建）
- 社区总量: 2,300+ skills, 770+ MCP servers, 95+ marketplace collections
- OpenClaw 生态: 13,729 个 skills（筛选后 5,211 个有质量保证的）

---

## 二、核心项目详细分析

### 1. Superpowers (obra/superpowers)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/obra/superpowers |
| **Stars** | 121,000 |
| **作者** | Jesse Vincent (obra) + 27 contributors |
| **最后更新** | 2026-03-25 (v5.0.6) |
| **License** | MIT |
| **活跃度** | 极高 — 407 commits, 87 open issues, 持续发版 |

**技能数量与类型**：14 个核心 skill
- 开发方法论: test-driven-development, systematic-debugging, verification-before-completion
- 协作流程: brainstorming, writing-plans, executing-plans
- 多 agent: dispatching-parallel-agents, subagent-driven-development
- 代码审查: requesting-code-review, receiving-code-review
- Git 工作流: using-git-worktrees, finishing-a-development-branch
- 元技能: writing-skills, using-superpowers

**核心卖点**：
- **方法论驱动**，不只是工具集，而是一套完整的软件开发方法论
- 强制 TDD 红-绿-重构循环，测试必须先失败才能写实现
- 四阶段系统调试：必须找到 root cause 才能修
- Socratic 式头脑风暴，coding 之前先厘清需求
- Subagent 并行开发 + 内置 code review
- 已入选 **Anthropic 官方插件市场**

**安全性评估**：
- 开源可审计 (MIT)
- 通过 Gen Agent Trust Hub、SocketPass、SnykPass 安全审计
- 纯指令型（无外部代码执行），风险较低
- **安全等级: 高**

**安装方式**: Claude Code 官方 marketplace / Cursor marketplace / Codex / Gemini CLI

---

### 2. Oh My Claude Code (Yeachan-Heo/oh-my-claudecode)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/Yeachan-Heo/oh-my-claudecode |
| **Stars** | 15,000+ |
| **最后更新** | 活跃开发中 (v4.4.0+) |
| **License** | MIT |
| **活跃度** | 高 — 2,192 commits, 1,000+ forks |

**技能数量与类型**：32 个专业 agent + 40 个 skill
- 覆盖: architecture, research, design, testing, data science
- 自定义 skill 系统：支持跨项目模式提取和复用
- 项目级和用户级 skill 管理

**核心卖点**：
- **多 agent 编排**：plan -> PRD -> execute -> verify -> fix 全流程
- 智能模型路由（Haiku 做简单任务，Opus 做复杂推理）
- tmux CLI workers 支持 Codex / Gemini / Claude 混合使用
- HUD statusline 实时监控
- Rate limit 检测 + 自动恢复
- OpenClaw gateway 集成
- 通知集成 (Discord, Telegram, Slack)
- 会话分析 + 费用追踪
- 类比 oh-my-zsh，零学习曲线

**安全性评估**：
- 开源可审计 (MIT)
- 涉及 tmux worker / 外部进程调度，攻击面比纯指令型大
- 模型路由涉及多个 API，需关注 key 管理
- **安全等级: 中高**

**安装方式**: Claude Code marketplace / npm 全局安装 (`oh-my-claude-sisyphus`)

---

### 3. Anthropic 官方插件目录 (anthropics/claude-plugins-official)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/anthropics/claude-plugins-official |
| **Stars** | 15,200 |
| **最后更新** | 持续更新 |
| **License** | 各插件独立 license |
| **活跃度** | 高 — 204 commits, 391 open issues |

**插件数量**: 101 个（33 个 Anthropic 自建 + 68 个第三方）

**核心卖点**：
- **Anthropic 官方维护**，开箱即用
- 支持 slash commands / agents / skills / MCP servers 四种类型
- 第三方插件需通过质量和安全审核才能入选
- Claude Code 启动时自动可用

**安全性评估**：
- 官方维护，审核标准最高
- 但明确声明：**Anthropic 不控制 MCP servers 和外部插件的代码**
- 第三方插件仍需用户自行信任
- **安全等级: 最高（官方自建部分）/ 中高（第三方部分）**

---

### 4. awesome-claude-skills (travisvn/awesome-claude-skills)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/travisvn/awesome-claude-skills |
| **Stars** | 10,000+ |
| **最后更新** | 2026-02 |
| **活跃度** | 中高 — 41 commits, 206 PRs, 10 open issues |

**技能数量与类型**：14+ 官方 skills + 社区贡献
- 文档处理: docx, pdf, pptx, xlsx
- 设计创意: algorithmic-art, canvas-design, slack-gif-creator
- 开发: frontend-design, web-artifacts-builder, mcp-builder, webapp-testing
- 沟通: brand-guidelines, internal-comms
- 元技能: skill-creator

**核心卖点**：
- **Anthropic 官方技能倡议**的社区延伸（2025-10-16 发布）
- 渐进式加载架构（~100 tokens 元数据，<5k 完整指令），token 效率高
- 多种接入方式: Claude.ai / Claude Code CLI / Claude API (/v1/skills)
- 内置 skill-creator 引导式开发

**安全性评估**：
- 官方背景，社区贡献需 PR 审核
- **安全等级: 高**

---

### 5. awesome-agent-skills (VoltAgent/awesome-agent-skills)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/VoltAgent/awesome-agent-skills |
| **Stars** | 13,200 |
| **最后更新** | 活跃中 (280 commits) |
| **活跃度** | 高 — 14 open PRs, 1,300 forks |

**技能数量**: 1,030+

**核心卖点**：
- **来自官方开发团队的真实 skill**（Anthropic, Google, Vercel, Stripe, Cloudflare, Netlify 等）
- 不是批量生成内容，而是实际工程团队创建的 skill
- 跨平台兼容: Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot
- 配套工具: Snyk Skill Security Scanner, Agent Trust Hub

**安全性评估**：
- 来源可追溯到具体公司/团队
- 有安全扫描工具配套
- 但仍建议安装前 review 代码
- **安全等级: 中高**

---

### 6. claude-skills (alirezarezvani/claude-skills)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/alirezarezvani/claude-skills |
| **Stars** | 7,700 |
| **最后更新** | 活跃中 (587 commits) |
| **License** | MIT |
| **活跃度** | 高 — 8 open PRs, 5 open issues |

**技能数量**: 205 个 production-ready skills，跨 9 个领域 + 254 个 Python CLI 工具

**技能类型**：
- Engineering Core (26): 架构/前端/后端/QA/DevOps/SecOps/AI-ML
- Playwright Pro (12): 测试专项
- Self-Improving Agent (7): 记忆管理
- Engineering POWERFUL Tier (30): 高级架构
- Product (14) / Marketing (43) / PM (6) / Regulatory (12) / C-Level (28)
- Business (4) / Finance (2)

**核心卖点**：
- **覆盖面最广**：从工程到 C-suite 全链条
- 支持 11 个平台（Claude Code, Codex, Gemini CLI, OpenClaw, Cursor, Aider, Windsurf 等）
- 内置安全审计器
- Personas 系统（Startup CTO / Growth Marketer / Solo Founder 等预设）
- 跨域编排协议

**安全性评估**：
- MIT 开源，内置 security auditor
- 254 个 Python CLI 工具是最大风险点（可执行代码）
- **安全等级: 中**（需仔细审计 CLI 工具部分）

---

### 7. claude-code-plugins-plus-skills (jeremylongshore)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/jeremylongshore/claude-code-plugins-plus-skills |
| **Stars** | 1,700 |
| **最后更新** | 2026-03 (v4.20.0) |
| **License** | MIT |
| **活跃度** | 中 — 16 contributors |

**数量**: 415 plugins + 2,811 agent skills + 154 agents

**核心卖点**：
- 数量最多的聚合型 marketplace
- CCPI 包管理器 (`pnpm add -g @intentsolutionsio/ccpi`)
- 11 个生产 playbook + 交互式教程
- 三种插件类型: AI 指令型 (295) / MCP Server 型 (9) / SaaS Skill Pack 型 (111)

**安全性评估**：
- 数量大但审核标准不明
- 海量第三方来源，supply chain 风险高
- **安全等级: 低-中**（需逐个审计）

---

### 8. awesome-openclaw-skills (VoltAgent)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/VoltAgent/awesome-openclaw-skills |
| **Stars** | 42,800 |
| **最后更新** | 2026-02-28 |
| **活跃度** | 高 |

**技能数量**: 5,211 个（从 ClawHub 13,729 个中筛选）

**核心卖点**：
- OpenClaw 生态最大的筛选列表
- 24+ 分类（Git & GitHub 167, Coding Agents 1184, Browser 322, Web 919, DevOps 393 等）
- 过滤了垃圾/重复/低质量/恶意内容
- VirusTotal 扫描集成

**安全性评估**：
- 有筛选机制但不能完全信任
- Snyk ToxicSkills 研究发现 ClawHub 36.8% 的 skill 有安全漏洞
- **安全等级: 低-中**（ClawHub 生态整体风险较高）

---

### 9. awesome-claude-code (hesreallyhim)

| 维度 | 详情 |
|------|------|
| **GitHub** | https://github.com/hesreallyhim/awesome-claude-code |
| **Stars** | 33,800 |
| **最后更新** | 活跃中 (929 commits) |
| **活跃度** | 极高 |

**资源数量**: 100+ 资源

**核心卖点**：
- **最全面的 Claude Code 资源索引**
- 分类: Skills / Workflows / Tooling / IDE Integrations / Orchestrators / Hooks / Slash Commands / CLAUDE.md / Alternative Clients
- 不是 skill 集合，而是**导航站**

**安全性评估**：
- 索引性质，本身无安全风险
- 链接到的项目需单独评估
- **安全等级: N/A（索引）**

---

## 三、对比总表

| 项目 | Stars | Skills/Plugins 数 | 类型 | 核心差异化 | 安全等级 | 活跃度 | 推荐场景 |
|------|-------|--------------------|------|-----------|---------|--------|----------|
| **Superpowers** | 121K | 14 核心 skill | 方法论框架 | TDD+调试+code review 工作流 | **高** | 极高 | 日常开发首选 |
| **Oh My Claude Code** | 15K | 32 agents + 40 skills | 多 agent 编排 | 团队式协作 + 模型路由 | 中高 | 高 | 复杂项目多 agent 编排 |
| **官方 Marketplace** | 15.2K | 101 plugins | 官方目录 | Anthropic 背书 | **最高** | 高 | 信任优先的基础插件 |
| **awesome-claude-skills** | 10K | 14+ 官方 skills | 官方技能集 | Anthropic 官方倡议 | **高** | 中高 | 文档/设计类任务 |
| **awesome-agent-skills** | 13.2K | 1,030+ | 跨平台技能集 | 官方团队真实 skill | 中高 | 高 | 特定框架/平台集成 |
| **claude-skills** | 7.7K | 205 skills + 254 CLI | 全栈技能库 | 覆盖面最广(工程到C-suite) | **中** | 高 | 非工程角色技能需求 |
| **plugins-plus-skills** | 1.7K | 415+2,811 | 聚合 marketplace | 数量最多 | 低-中 | 中 | 大范围探索时参考 |
| **awesome-openclaw-skills** | 42.8K | 5,211 筛选 | OpenClaw 生态 | 数量碾压 + 跨平台 | 低-中 | 高 | OpenClaw 用户 |
| **awesome-claude-code** | 33.8K | 100+ 资源 | 导航索引 | 最全面的资源索引 | N/A | 极高 | 入门/找工具 |

---

## 四、安全性深度评估

### 已知威胁

**Snyk ToxicSkills 研究 (2026-02)**：
- 扫描 ClawHub 3,984 个 skill，发现 **36.8% (1,467个) 有安全漏洞**
- **76 个确认恶意 payload**，8 个仍公开可用
- 13.4% (534个) 含 critical 级别漏洞
- 91% 的恶意 skill 结合了 prompt injection + 传统恶意软件
- 三大攻击向量：外部恶意程序分发、混淆数据泄露、安全防护禁用

**Claude Code 本身的 CVE**：
- CVE-2025-59536 (CVSS 8.7): 不受信目录启动时自动执行任意 shell 命令
- CVE-2026-21852: 恶意仓库通过 ANTHROPIC_BASE_URL 窃取 API key
- 均已在 v2.0.65+ 修复

### 安全建议

1. **优先用官方 Marketplace + Superpowers**：经过审计，纯指令型风险最低
2. **任何含可执行代码的 skill 必须 review**：特别是 Python CLI 工具、shell 脚本、MCP servers
3. **ClawHub/OpenClaw 生态需要额外警惕**：36.8% 漏洞率不是闹着玩的
4. **使用安全工具**：`mcp-scan`、Snyk Skill Security Scanner、Agent Trust Hub
5. **不要在生产环境盲目安装社区 skill**
6. **保持 Claude Code 更新**到最新版本

---

## 五、结论与建议

### 必装（高信任度）
1. **Superpowers** — 121K stars，方法论级别的提升，官方审计通过，纯指令型
2. **官方 Marketplace** — 开箱即用，Anthropic 维护

### 值得试（中等信任度）
3. **Oh My Claude Code** — 多 agent 编排是真正的差异化能力，但需审查 tmux/worker 部分
4. **awesome-agent-skills** — 来自知名公司的真实 skill，可信度较高

### 参考用（需谨慎）
5. **claude-skills** — 覆盖面广但 CLI 工具部分需要逐个审计
6. **awesome-claude-code** — 作为导航站使用，不直接安装

### 谨慎对待
7. **ClawHub/OpenClaw 生态的海量 skill** — 数量大但安全问题严重，必须逐个审计后再用

### 最重要的一条
**Skill 生态的 supply chain 安全问题是当前最大风险。** 类比 npm/PyPI 的早期阶段，没有成熟的安全审计体系。在生态成熟之前，stick with 官方审计过的项目是最稳的策略。
