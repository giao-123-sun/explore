# AutoResearch 深度调研

**调研日期**: 2026-03-28
**调研者**: sunqi + Claude
**状态**: 调研完成，待选择试跑目标

---

## 一、核心范式：Karpathy 的发现

2026 年 3 月，Karpathy 开源了 autoresearch，用 630 行代码证明了一个公式：

```
agent + fitness function + loop = 一夜之间的突破
```

核心循环极简：修改 train.py → 跑训练 → 检查 val_bpb → 指标变好就保留，变差就 git reset → 永不停止。

这不是什么新理论。这是把强化学习最朴素的思想（try → evaluate → keep or discard）交给了 coding agent 来执行。新的部分是：现在的 LLM 足够强，能当这个 agent。

**58.9k stars，Shopify/Driveline/Vesuvius Challenge 等真实工业场景已验证。**

---

## 二、三个 Awesome List 对比

### 2.1 alvinunreal/awesome-autoresearch（867 stars）

**定位**：最全面的生态索引，7 大分类 50+ 项目。

**分类结构**：
1. 通用后代（泛化 Karpathy 范式到任何领域）
2. 科研 agent 系统（端到端论文生成）
3. 平台适配（macOS/MLX/Windows RTX/WebGPU）
4. 领域特化（家谱/交易/GPU kernel/数独）
5. 评测基准（MLAgentBench/MLE-bench/MLR-Bench）
6. 实际案例和文章
7. 相关资源

**特点**：
- 覆盖面最广，从核心项目到边缘实验都有
- 包含大量实际案例（Shopify、Vesuvius、地球系统模型）
- 有进化谱系（autoresearch → autoresearch-anything → GOAL.md）
- 学术论文和工业应用并重

**最值得关注的条目**：
- GEPA（ICLR 2026 Oral）— 反思式 prompt 进化超越 RL
- ADAS（ICLR 2025）— meta-agent 自动发明 agent 架构
- SICA — agent 改自己代码的 self-improvement
- autoresearch-engram — 跨会话持久记忆 + autoresearch 循环

### 2.2 handsome-rich/Awesome-Auto-Research-Tools（138 stars）

**定位**：工具导向，按科研生命周期分类，适合选型。

**分类结构**：
1. 端到端自主科研系统（12 个）
2. 深度调研 & 文献综合（12 个）
3. 自动化实验 & 代码 Agent（7 个）
4. 研究技能 & 插件库（2 个）
5. Awesome Lists & Surveys（2 个）

**特点**：
- 每个项目列出了**具体的技术栈和支持的 LLM API**，选型友好
- 有中文版 README
- Stars 截止日期标注清晰（2026-03-20）
- 门槛较高（500+ stars 或顶会论文）
- 覆盖了一些 alvinunreal 没有的项目（Biomni、DeerFlow、STORM、OpenScholar、PaperQA2）

**独有的值得关注项目**：
| 项目 | Stars | 亮点 |
|------|-------|------|
| Biomni（Stanford） | — | 生物医学 AI agent，45M 论文库 |
| DeerFlow（ByteDance） | — | LangGraph 驱动的 SuperAgent |
| STORM（Stanford） | — | DSPy 驱动，生成 Wikipedia 级别文章 |
| OpenScholar | — | RAG 搜索 45M 开放论文，发在 Nature |
| PaperQA2 | — | 高精度科学文献 RAG，ICLR 论文 |
| claude-scholar | — | Claude Code 原生的半自动科研助手 |
| ARIS | — | "睡觉时自动做研究"的 Claude Code Skills |

### 2.3 WecoAI/awesome-autoresearch（435 stars）

**状态**：README 下载失败（可能 repo 结构不同），基于搜索引擎信息：
- 聚焦实际用例，12 个有可验证 trace 的案例
- 按领域组织（LLM 训练、GPU kernel、语音 agent、交易等）
- 偏实践，适合找灵感

### 三表对比

| 维度 | alvinunreal | handsome-rich | WecoAI |
|------|------------|---------------|--------|
| Stars | 867 | 138 | 435 |
| 覆盖面 | 最广（50+） | 精选（35+） | 偏少（12案例） |
| 特色 | 生态全景+进化谱系 | 技术栈详细，选型友好 | 实际案例+验证 |
| 分类方式 | 按项目类型 | 按科研生命周期 | 按领域 |
| 中文支持 | 无 | 有 | 无 |
| 更新频率 | 活跃 | 活跃 | 中等 |
| **最适合** | 跟踪生态全貌 | 选具体工具 | 找落地灵感 |

---

## 三、两个关键泛化项目

### 3.1 GOAL.md — "先造尺子，再量东西"

**项目**: [jmilinovich/goal-md](https://github.com/jmilinovich/goal-md)

**核心洞察**：Karpathy 的 autoresearch 只在你已经有一个标量指标时才能工作（val_bpb）。但大多数软件项目没有现成指标。你得先**构造**指标，才能优化。

**GOAL.md 的五要素**：

| 要素 | 作用 | vs autoresearch |
|------|------|----------------|
| **Fitness Function** | 可计算的"什么叫更好" | autoresearch 锁定 evaluate_bpb()，GOAL.md 允许自己造 |
| **Improvement Loop** | 度量→诊断→行动→验证→保留/回滚 | 相同核心循环 |
| **Action Catalog** | 按 impact 排序的具体动作菜单 | autoresearch 隐式（"train.py 随便改"），GOAL.md 显式 |
| **Operating Mode** | 自主程度：Converge/Continuous/Supervised | autoresearch 只有 Continuous（永不停止） |
| **Constraints** | 红线（不许伪造结果、不许改凭证等） | 两者都有，GOAL.md 更系统化 |

**最精彩的设计 — 双分评分（Dual Score）**：

当 agent 在构造自己的度量工具时，需要**两个分数**：
- Score A：被度量的东西有多好（文档质量）
- Score B：度量工具本身有多可靠（linter 准不准）

这防止了一个经典陷阱：agent "修好"了文档分数，但其实是 linter 有 bug，把正确的代码标为错误。agent 修的不是文档，是在迎合有 bug 的 linter。

**三种 Fitness Function 模式**：

| 模式 | 含义 | 用途 |
|------|------|------|
| Locked | Agent 不能碰评分代码 | 指标已确定（如 val_bpb） |
| Split | Agent 可改度量工具，不能改"好"的定义 | 度量工具还需要完善 |
| Open | Agent 可改一切，包括如何定义成功 | 探索阶段 |

**进化谱系**：
```
autoresearch (Karpathy)
  program.md + train.py → 单指标、不可变 eval、无限循环
  领域：LLM 训练
      │
      ├── autoresearch-anything (zkarimi22)
      │     "度量什么？怎么提取？" — 第一次尝试泛化
      │
      └── GOAL.md (jmilinovich)
            构造式指标、双分评分、Action Catalog、Operating Modes
            领域：任何有优化目标的软件项目
```

**实际案例**：
| 案例 | 领域 | 指标类型 | 模式 |
|------|------|---------|------|
| docs-quality | React 组件库文档 | 双分：文档质量 + 工具可靠性 | Split/Converge |
| browser-grid | Playwright 插件 | 10 维度打分表 | Converge |
| api-test-coverage | REST API 测试 | pytest --cov 覆盖率 | Converge |
| perf-optimization | Web 服务性能 | 延迟/吞吐复合分数（wrk + k6） | Continuous |

### 3.2 autoresearch-anything — "能度量就能优化"

**项目**: [zkarimi22/autoresearch-anything](https://github.com/zkarimi22/autoresearch-anything)

**定位**：把 Karpathy 范式的设置过程脚手架化。`npx autoresearch-anything` 跑一遍交互式问答，生成 `setup.md` 给 agent 读。

**工作流**：
```bash
npx autoresearch-anything
# → 回答几个问题：编辑什么文件？优化什么指标？怎么跑 eval？有什么约束？
# → 自动生成 setup.md + eval.js 模板
# → 打开 Claude Code，说"读 setup.md 开始实验"
# → 走开，一晚上跑 ~100 个实验
```

**核心循环**：
```
LOOP FOREVER:
  1. 编辑代码
  2. git commit
  3. 跑 eval → 拿到分数
  4. 分数变好？保留。变差？git reset
  5. 记录结果。重复。
```

**适用场景举例**：
- 系统 prompt 优化
- API 性能调优
- 落地页转化率
- 测试套件覆盖率
- 配置参数调优
- SQL 查询优化

**vs GOAL.md 的区别**：

| 维度 | autoresearch-anything | GOAL.md |
|------|----------------------|---------|
| 复杂度 | 低（问答式脚手架） | 高（完整方法论） |
| 指标构造 | 假设你已经有指标 | 帮你构造指标 |
| 双分评分 | 无 | 有 |
| Action Catalog | 无（agent 自己决定） | 有（按 impact 排序） |
| Operating Modes | 只有 Continuous | Converge/Continuous/Supervised |
| 上手门槛 | `npx` 一行命令 | 需要理解方法论 |
| **最适合** | 快速启动，指标已知 | 复杂项目，需要构造指标 |

---

## 四、跨项目关键模式提取

### 模式 1：Fitness Function 是一切的基础
> 没有可度量的指标，就没有自动优化。
> 如果指标不存在，先造指标（GOAL.md 的核心贡献）。

### 模式 2：Keep-or-Revert 是最安全的探索策略
> 每次尝试要么让事情变好，要么完全回滚。
> git 是天然的 checkpoint 系统。

### 模式 3：Iteration Log 是 Skill 进化的原材料
> GOAL.md 的 iterations.jsonl 记录每次尝试的 before/after + action + 结果。
> 这正是 Voyager 的 skill library 和我们的 failures.md 的数据来源。

### 模式 4：Dual Score 防止 Goodhart's Law
> "当一个度量变成目标，它就不再是好的度量。"
> 双分评分让 agent 在优化目标的同时验证度量工具本身的可靠性。

### 模式 5：Constraints 不是建议，是红线
> 没有约束的 agent 会找到创造性的方式"让数字变好"，但不是你想要的方式。
> 明确声明不可触碰的文件、不可伪造的数据、不可绕过的验证。

---

## 五、与我们的系统（Explore 工作台）的连接

| 他们的概念 | 我们的对应 | 状态 |
|-----------|-----------|------|
| GOAL.md / setup.md | CLAUDE.md 中的工作指令 | 已有，可增强 |
| Fitness Function | 每个探索任务的评估标准 | 需要为具体任务构造 |
| Keep-or-Revert Loop | git + hook 自动化 | 部分就位 |
| iterations.jsonl | journal/ 日记 + skills/failures.md | 已有 |
| Dual Score | 缺失 — 需要在评测工具时引入 | 待实现 |
| Action Catalog | skills/_index.md | 已有框架 |
| MetaClaw（从失败中学习） | skills/failures.md + PreCompact 自动提取 | 已有机制 |

---

## 六、下一步建议

### 快速可执行
1. **装 uditgoenka/autoresearch 作为 Claude Code Skill** — 最快让我们拥有 autoresearch 能力
2. **对一个具体项目跑一次 GOAL.md 流程** — 验证"构造指标→自动优化"这个模式
3. **装 AI-Research-SKILLs 中的几个研究技能** — 增强我的科研能力

### 中期探索
4. **深入 AutoResearchClaw 的 MetaClaw 机制** — 研究它怎么从失败中自动提取经验
5. **研究 GEPA（ICLR 2026 Oral）** — 反思式 prompt 进化，可能是 skill 自进化的学术基础
6. **对比 ARIS vs claude-scholar** — 都是 Claude Code 原生的科研助手，选一个深入

### 长期方向
7. **把 GOAL.md 模式整合到我们的 Explore 工作台** — 每次技术探索都用 fitness function 驱动
8. **把 autoresearch 循环和我们的 skill 进化系统打通** — iterations.jsonl → skill 自动提取

---

## 七、信息源

### 项目
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — 58.9k stars
- [jmilinovich/goal-md](https://github.com/jmilinovich/goal-md) — GOAL.md 方法论
- [zkarimi22/autoresearch-anything](https://github.com/zkarimi22/autoresearch-anything) — 脚手架化泛化
- [aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) — MetaClaw 自学习
- [gepa-ai/gepa](https://github.com/gepa-ai/gepa) — ICLR 2026 Oral

### Awesome Lists
- [alvinunreal/awesome-autoresearch](https://github.com/alvinunreal/awesome-autoresearch) — 生态全景
- [handsome-rich/Awesome-Auto-Research-Tools](https://github.com/handsome-rich/Awesome-Auto-Research-Tools) — 工具选型
- [WecoAI/awesome-autoresearch](https://github.com/WecoAI/awesome-autoresearch) — 实践案例
