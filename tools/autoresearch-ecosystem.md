# AutoResearch 生态评测

**调研日期**: 2026-03-28
**状态**: 调研完成，待选择具体项目试跑

## 两大范式

### Karpathy 范式（优化循环）
改代码 → 跑实验 → 评估指标 → 保留/回滚。简洁、单 GPU、单文件。
- 代表：karpathy/autoresearch (58.9k stars)
- 泛化版：uditgoenka/autoresearch (2.6k stars, Claude Code Skill)

### 端到端科研
文献搜索 → 假设生成 → 实验设计 → 运行 → 论文撰写 → 自审。
- 代表：AutoResearchClaw (9.2k), AI-Researcher (5.0k), AI-Scientist-v2 (3.1k)

## 核心项目

| 项目 | Stars | 活跃度 | 核心特点 |
|------|-------|--------|---------|
| karpathy/autoresearch | 58.9k | 极活跃 | program.md 定义研究，单 GPU 优化循环 |
| AutoResearchClaw | 9.2k | 极活跃 | MetaClaw 自学习，23 阶段 pipeline，全流程 |
| microsoft/RD-Agent | 12.1k | 极活跃 | MLE-Bench 冠军，Docker+WebUI，工业级 |
| gpt-researcher | 26.1k | 活跃 | 深度调研报告，超 Perplexity/OpenAI |
| AI-Research-SKILLs | 5.7k | 活跃 | 87 个技能模块，即插即用 |
| HKUDS/AI-Researcher | 5.0k | 低 | NeurIPS 2025 Spotlight |
| SakanaAI/AI-Scientist-v2 | 3.1k | 低 | 首篇 AI 生成被接收论文 |

## 关键发现

1. MetaClaw（AutoResearchClaw）= 我们 skill 自进化的科研版，值得深入研究
2. program.md（karpathy）= 用 markdown 定义完整研究 program 的范式
3. RD-Agent 工程质量最高但门槛也最高（Docker 部署）
4. AI-Research-SKILLs 的 87 个技能可直接装配到我们的 Claude Code

## 推荐试跑顺序

1. karpathy/autoresearch — 理解范式基础
2. uditgoenka/autoresearch — 直接作为 Claude Code Skill 安装
3. AutoResearchClaw — 深入研究 MetaClaw 机制
4. AI-Research-SKILLs — 挑几个技能装上试试
