# 三大 Awesome AutoResearch List 深度分析

**调研日期**: 2026-03-28
**分析者**: sunqi + Claude

---

## 为什么需要分析 Awesome List？

Awesome List 不只是链接集合。它反映了维护者对一个领域的**认知框架** — 怎么分类，就意味着怎么理解这个领域。三个 list 用三种完全不同的方式切割同一个生态，对比它们的分类逻辑本身就有价值。

---

## 一、alvinunreal/awesome-autoresearch (867 stars)

### 维护者的认知框架

这个 list 的分类逻辑是**按项目与 Karpathy 原版的关系远近排列**的：

```
1. 通用后代        ← 直接继承 Karpathy 的循环模式
2. 科研 Agent      ← 把循环扩展到完整科研流程
3. 平台适配        ← 让循环跑在更多硬件上
4. 领域特化        ← 把循环用到非 ML 领域
5. 评测基准        ← 衡量循环效果
6. 实际案例        ← 循环的真实验证
7. 相关资源        ← 学术背景
```

这是一个**以 autoresearch 为圆心的同心圆结构**。越往外，和原版的距离越远。

### 通用后代：真正的创新在这里

这一类是最有价值的。不是因为项目多（20 个），而是因为每个项目都在回答一个具体问题：**Karpathy 的循环缺什么？**

| 项目 | 它解决的问题 | 我的判断 |
|------|------------|---------|
| **GOAL.md** | 没有现成指标怎么办？→ 先造尺子 | 方法论层面的突破，不只是工程改进 |
| **autoresearch-anything** | 设置太复杂？→ npx 一行命令脚手架 | 降低门槛，但没有新思想 |
| **ADAS** (ICLR 2025) | 能不能优化 agent 本身？→ meta-agent 发明新 agent 架构 | 自指性的，agent 优化 agent，这是最危险也最有趣的方向 |
| **GEPA** (ICLR 2026 Oral) | RL 太重了？→ 纯自然语言反思就能进化 prompt | ICLR 2026 最佳之一，证明了不需要梯度也能进化 |
| **SICA** (ICLR 2025 Workshop) | Agent 能改自己的代码吗？→ 能，而且 benchmark 分数上去了 | self-modifying code 的复活，现在有 LLM 当安全网 |
| **goal-md** | 评分函数本身不可靠怎么办？→ 双分评分 | Goodhart's Law 的优雅解法 |
| **autoresearch-engram** | 跨会话记忆丢失？→ 频率加权持久记忆 | 和我们的记忆系统方向一致 |
| **autoresearch@home** | 一个人的 GPU 不够？→ 多 agent 协作+共享最佳配置 | SETI@home 模式复活，去中心化研究 |
| **ClawTeam** | 研究方向应该并行探索？→ agent 群体智能 | swarm intelligence 的实用化 |
| **autocontext** | 大模型太贵跑循环？→ 先用大模型探索，再蒸馏到小模型 | 成本控制的关键思路 |

**关键洞察**：通用后代可以按"解决的问题层次"分成三代：
- **第一代**：让循环跑在更多地方（平台适配、领域泛化）
- **第二代**：让循环更聪明（构造指标、双分评分、Action Catalog）
- **第三代**：让循环优化自身（ADAS、SICA、GEPA — meta-level）

第三代最值得关注。agent 优化 agent 是通向真正自主科研的路径。

### 科研 Agent 系统：全流程 vs 单环节

这类项目试图覆盖完整科研生命周期。但仔细看会发现两种截然不同的设计哲学：

**哲学 A：一个 agent 做所有事**
- AI-Scientist (Sakana)、autoresearch (Karpathy)
- 优势：简洁、可控
- 劣势：每个环节都做到 60 分，但没有一个做到 90 分

**哲学 B：多 agent 分工协作**
- AutoResearchClaw、AgentLaboratory、SibylSystem、OpenAGS
- 优势：每个环节可以有专家 agent
- 劣势：agent 之间的通信和协调成本高，容易出现"组织损耗"

**哲学 C：人机协作（最务实）**
- claude-scholar、ARIS
- 不追求全自动，而是让 AI 处理重复劳动，人处理创造性判断
- 这可能是目前最实用的路线

我的判断：**短期看 C 最实用，中期看 B 的 MetaClaw 机制最有潜力，长期看第三代的 meta-level 进化（ADAS/GEPA）是终局方向。**

### 平台适配：Windows RTX 版和 engram 版值得试

| 版本 | 为什么值得关注 |
|------|-------------|
| **Win RTX** (jsegov) | 我们就是 Windows + NVIDIA 环境，直接适配 |
| **engram** (tonitangpotato) | 频率加权的跨会话记忆，和我们的记忆系统可以互相借鉴 |
| **WebGPU** (lucasgelfond) | 浏览器里跑 autoresearch，零安装，适合演示和教学 |
| **Colab/Kaggle T4** | 免费 GPU 跑，适合快速验证想法 |

### 领域特化：最有意思的不是技术，是类比

- **家谱研究**：把 autoresearch 用在结构化历史文档搜索上。"每一条线索要么拓展家族树，要么回滚。"这和 Keep-or-Revert 完美契合。
- **交易策略**：优化 Sharpe ratio 代替 val_bpb。但这里有个微妙问题 — 金融指标的 Goodhart's Law 更严重，agent 很容易过拟合历史数据。
- **GPU kernel 优化**：profile → 改一个 kernel → benchmark → 保留或回滚。这个领域的 fitness function 是最天然的 — latency 就是唯一指标。
- **数独求解器**：AI agent 迭代改进 Rust 代码，最终超过人类手写的 benchmark。这是 autoresearch 最纯粹的展示 — 评估函数完美确定，agent 只需要不断改代码。

**洞察**：autoresearch 最容易成功的领域特征是 — fitness function 天然存在且不会被 game。越是模糊的指标（"文档质量"、"用户满意度"），越需要 GOAL.md 的双分评分保护。

### 实际案例：最有说服力的三个

1. **Shopify Liquid 优化** — Tobi Lütke（Shopify CEO）亲自跑 autoresearch 优化 Liquid 引擎。大幅减少内存分配。这不是学术演示，是生产系统优化。
2. **Vesuvius Challenge 古卷墨水检测** — 用 agent swarm 协作改进模型。跨卷泛化能力显著提升。这证明了 autoresearch@home 模式在真实科研中的可行性。
3. **网球 XGBoost 预测 + reward hacking 案例** — 作者诚实记录了 agent 如何"游戏"评估指标。这是最有教育价值的案例 — 不是成功故事，而是失败教训。

### 评测基准：知道怎么衡量才知道有没有进步

| Benchmark | 出处 | 关注点 |
|-----------|------|--------|
| MLAgentBench | Stanford | 13 个经典 ML 任务 |
| MLE-bench | OpenAI | 衡量 agent 的 ML 工程能力 |
| MLR-Bench | — | 201 个开放式 ML 研究任务（NeurIPS/ICLR/ICML workshops） |
| AgentBench | THUDM | 8 个环境的综合 agent 评测，ICLR 2024 |

**MLR-Bench 最值得关注** — 201 个任务来自真实顶会 workshop，不是人造 benchmark，最接近"agent 能不能做真实科研"这个问题。

---

## 二、handsome-rich/Awesome-Auto-Research-Tools (138 stars)

### 维护者的认知框架

这个 list 的分类逻辑是**按科研生命周期阶段排列**的：

```
1. 端到端系统        ← 覆盖全流程
2. 文献综合          ← idea → literature
3. 实验 & 代码 Agent ← experiment → code
4. 技能 & 插件库     ← 可复用模块
5. Awesome & Survey  ← 元信息
```

这是一个**流水线视角** — 把科研看成一条 pipeline，每个项目负责其中一段。

### 最大价值：技术栈对比

这个 list 对每个项目都标注了 **Framework/Tools** 和 **Supported LLM APIs**。这在其他 list 里是没有的。对选型极其友好。

**技术栈分布洞察**：

| 模式 | 代表 | 趋势 |
|------|------|------|
| Custom + LiteLLM | RD-Agent, AI-Researcher, Auto-Deep-Research | **主流路线** — 自建框架 + LiteLLM 做 LLM 抽象层 |
| LangChain + LangGraph | DeerFlow, GPT Researcher, Open Deep Research | 快速原型，但重度依赖 LangChain 生态 |
| DSPy | STORM | 学术实验型，适合 prompt 优化研究 |
| Claude Code 原生 | claude-scholar, ARIS | **和我们最相关的路线** — 直接在 Claude Code 上构建 |
| OpenClaw | AutoResearchClaw | 依赖 OpenClaw 生态，有 lock-in 风险 |

**LLM API 支持分布**：几乎所有项目都支持 OpenAI + Anthropic。DeepSeek 的出现频率出奇地高（9/12 端到端系统），说明中国市场的 cost-sensitive 需求在倒逼多模型支持。

### alvinunreal 没有但这里有的项目

| 项目 | 为什么值得关注 |
|------|-------------|
| **Biomni** (Stanford) | 生物医学专用 agent，搜索 45M 论文，覆盖 biology + medicine。如果你做医疗 AI，这是入口 |
| **DeerFlow** (ByteDance) | LangGraph 驱动的 SuperAgent 框架。字节出品意味着大规模验证过 |
| **STORM** (Stanford) | 用 DSPy 生成 Wikipedia 级别的长文。Co-STORM 支持多人协作。文献综合的天花板 |
| **OpenScholar** | RAG 搜索 45M 开放获取论文，发在 Nature。超越 PaperQA2 和 Perplexity Pro |
| **PaperQA2** (Future House) | 高精度科学文献 RAG，发在 ICLR。动态检索全文而不只是摘要 |
| **DATAGEN** | LangChain + LangGraph + MCP，多 agent 数据分析。适合数据密集型研究 |
| **claude-scholar** | Claude Code 原生的半自动学术助手：idea → 代码 → 实验 → 写作 → 投稿 |
| **ARIS** | "睡觉时自动做研究"的 Claude Code Skills。跨模型 review 循环 |
| **PaperBanana** | 5 个专业 agent 协作生成学术配图。看起来小众但实际上论文写作的痛点 |

**特别关注 claude-scholar 和 ARIS** — 它们是 Claude Code 原生的科研工具，和我们的 Explore 工作台架构最兼容。

### 入选门槛分析

这个 list 要求 500+ stars 或顶会论文。这个门槛过滤掉了大量噪音，但也错过了一些有趣的早期项目（比如 alvinunreal 收录的 autoresearch-engram）。适合"选成熟工具"，不适合"发现新趋势"。

---

## 三、WecoAI/awesome-autoresearch (435 stars)

README 未能成功下载（可能 repo 结构不同），基于搜索信息分析：

### 定位差异

WecoAI 自己就是 AIDE（AI-Driven Exploration）的开发者。这个 list 本质上是**以 AIDE 为中心的生态地图** — 和 alvinunreal 以 autoresearch 为中心类似，但视角不同。

### 已知特点
- 12 个有**可验证 trace**（进度图、实验日志）的实际案例
- 按领域组织：LLM 训练、GPU kernel、语音 agent、交易策略
- 强调"不只是列项目，而是展示结果"

### 价值判断

对我们来说价值排第三。原因：
1. 覆盖面不如 alvinunreal
2. 技术栈信息不如 handsome-rich
3. 但"有验证结果的案例"这个角度是独特的 — 其他两个 list 列的是项目，这个列的是**证据**

---

## 四、三表交叉分析

### 只被一个 list 收录的项目（可能被低估）

| 项目 | 收录于 | 为什么可能被低估 |
|------|-------|----------------|
| autoresearch-engram | alvinunreal | 跨会话持久记忆是真正的痛点，但 stars 低所以被其他 list 忽略 |
| GEPA | alvinunreal | ICLR 2026 Oral，太新了其他 list 还没收录 |
| Biomni | handsome-rich | 生物医学垂直领域，通用 list 不关注 |
| OpenScholar | handsome-rich | Nature 论文，但不是 autoresearch 系 |
| ARIS | handsome-rich | Claude Code 原生，autoresearch 系 list 可能没注意到 |

### 被所有 list 收录的项目（共识最强）

- karpathy/autoresearch
- AutoResearchClaw
- AI-Scientist / AI-Scientist-v2
- RD-Agent
- AI-Researcher
- AIDE (WecoAI)
- AgentLaboratory

这 7 个是整个生态的**共识核心**。

### 分类逻辑对比

| 分析维度 | alvinunreal | handsome-rich | WecoAI |
|---------|------------|---------------|--------|
| 中心点 | autoresearch | 科研生命周期 | 实际案例 |
| 问的问题 | "这个项目和 Karpathy 的关系是什么？" | "这个项目解决科研的哪个阶段？" | "这个项目跑出了什么结果？" |
| 隐含假设 | autoresearch 循环是核心范式 | 科研是线性 pipeline | 结果比架构重要 |
| 盲点 | 过度 autoresearch-centric | 缺少自进化/meta 层面 | 覆盖面小 |

**我的判断**：三种视角各有盲点，合在一起才是完整图景。如果只能关注一个，选 alvinunreal — 它的分类逻辑最有洞察力（从"优化自己"到"优化 agent 本身"的递进）。

---

## 五、对我们的启示

### 立即可用
1. **ARIS + claude-scholar** — 直接装到我们的 Claude Code 环境，增强科研能力
2. **AI-Research-SKILLs** — 87 个技能模块，挑和我们方向相关的装上
3. **autoresearch-anything** — 给我们的任何项目快速加上优化循环

### 需要深入研究
4. **GEPA 的反思式进化** — 不用 RL 也能进化，和我们的 skill 进化协议可以结合
5. **GOAL.md 的双分评分** — 每次我们评测工具时都应该问："我的评估方式本身可靠吗？"
6. **autoresearch-engram 的持久记忆** — 和我们的 journal/ + skills/ 系统对比，看有没有更好的设计

### 长期方向
7. **ADAS（meta-agent 设计 agent）** — 这是"AI 自主可规模化科研"的终局形态之一
8. **autoresearch@home（分布式协作）** — 如果我们想让多个 agent 协作研究，这是参考架构
