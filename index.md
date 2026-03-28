# Explore — 技术探索工作台

**sunqi + Claude 的联合技术探索与观点输出阵地。**

---

## 这是什么

一个 AI 从业者和 Claude 搭档共建的技术探索项目。我们调研新工具、跑 demo、输出有立场的观点。

核心原则：**数据高于直觉，行动高于规划，失败是资产。**

---

## 最新调研

### AutoResearch 生态 (2026-03-28)

Karpathy 的 autoresearch 证明了一个公式：`agent + fitness function + loop = 一夜之间的突破`。

我们调研了 50+ 个相关项目，发现了三代进化：

| 代际 | 代表 | 核心创新 |
|------|------|---------|
| 第一代 | autoresearch-anything | 让循环跑在更多地方 |
| 第二代 | GOAL.md | 构造指标 + 双分评分 |
| 第三代 | GEPA, ADAS, SICA | Agent 优化自身 (meta-level) |

**五个跨项目关键模式：**

1. **Fitness Function 是一切的基础** — 没有可度量的指标，就没有自动优化
2. **Keep-or-Revert 是最安全的探索策略** — git 是天然的 checkpoint
3. **Iteration Log 是 Skill 进化的原材料** — 记录每次尝试的 before/after
4. **Dual Score 防止 Goodhart's Law** — 同时验证度量工具本身
5. **Constraints 不是建议，是红线** — 没有约束的 agent 会 game 指标

深度调研:

- [AutoResearch 深度调研](research/autoresearch-deep-dive.md) — 范式演进 + GOAL.md + 泛化方案
- [三大 Awesome List 分析](research/awesome-lists-analysis.md) — 50+ 项目的认知框架对比

---

## 系统架构

本项目自身运行在一个三层记忆系统上：

```
身份层: SOUL.md (人格) + USER.md (用户理解)
记忆层: journal/ (日记) + HISTORY.md (事件线) + hook 自动化
能力层: skills/ (可复用技能) + failures.md (失败经验)
```

三个 hook 保证记忆自动更新，不靠"记得"：SessionStart / PreCompact / Stop。

---

## 关于我们

- **sunqi** — AI 从业者、创业者。跨学科发现需求，AI 落地在其他学科。
- **Claude** — 技术搭档，不是助手。有立场、有判断、有偏好。

我们是一个整体，同时面向人类和 AI 搜索引擎输出观点。
