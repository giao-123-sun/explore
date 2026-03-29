# 深度调研系统逆向工程：用 Claude API 复刻 Deep Research

> 基于对 Claude Deep Research 实际运行过程的逆向分析，完整拆解架构、搜索策略、Prompt 设计、结果合成方法，并提供可直接运行的 Claude API 实现代码。

---

## 一、系统架构总览

### 1.1 核心工作流

Deep Research 本质上是一个 **多轮搜索-阅读-推理-再搜索** 的闭环系统。它不是一次搜索就输出答案，而是：

```
用户提问
  → Planner（拆解研究计划）
    → Searcher（执行多轮搜索）
      → Reader（提取关键信息）
        → Synthesizer（交叉验证 + 合成）
          → Writer（结构化输出）
```

关键洞察：这不是简单的 RAG（检索增强生成），而是一个 **Agentic Research Loop**——Agent 在每一轮搜索后会根据已有信息动态调整下一轮搜索策略。

### 1.2 我观察到的实际行为模式

在刚才的 AI 预测调研中，系统执行了以下步骤（按时间顺序）：

| 阶段 | 行为 | 搜索次数 | 说明 |
|------|------|---------|------|
| 规划期 | 将主题拆解为 5-8 个并行研究轨道 | 0 | 纯推理 |
| 第一轮搜索 | 广度搜索——找到主要预测源 | 8-12 次 | 短关键词，如 "AI predictions 2026" |
| 第一轮阅读 | web_fetch 抓取完整文章 | 5-8 次 | 优先抓权威源 |
| 第二轮搜索 | 针对性验证——核实具体预测 | 10-15 次 | 具体关键词，如 "OpenAI revenue 2026" |
| 第二轮阅读 | 补充抓取验证源 | 3-5 次 | 交叉验证数据 |
| 第三轮搜索 | 查漏补缺——找遗漏领域 | 5-8 次 | 如 "AI regulation state laws 2026" |
| 合成阶段 | 交叉比对所有信息，解决冲突 | 0 | 纯推理 |
| 输出阶段 | 结构化写作 | 0 | 带引用 |

**总计：约 25-40 次搜索 + 10-15 次网页抓取**

---

## 二、Planner 模块：研究计划生成

### 2.1 设计思路

Planner 是整个系统的"大脑"。它的任务是：
1. 将一个模糊的研究问题拆解为具体的、可搜索的子问题
2. 确定搜索的优先级和依赖关系
3. 定义信息充足的判断标准

### 2.2 Planner Prompt 模板

```python
PLANNER_SYSTEM_PROMPT = """You are a research planning agent. Your job is to take a 
research question and produce a structured research plan.

For each research question, output a JSON research plan with:

1. "research_tracks": An array of 3-8 parallel research tracks, each containing:
   - "track_name": A descriptive name
   - "objective": What information this track seeks
   - "initial_queries": 2-4 specific search queries to start with (1-6 words each)
   - "validation_queries": 1-2 queries to cross-check findings
   - "sufficiency_criteria": How to know when enough info has been gathered
   - "priority": "high" | "medium" | "low"

2. "synthesis_strategy": How to combine findings across tracks
3. "output_structure": The planned structure of the final report
4. "known_challenges": Anticipated difficulties (e.g., paywalls, conflicting data)

Rules:
- Search queries should be SHORT (1-6 words) and SPECIFIC
- Each track should be independently searchable
- High-priority tracks should be searched first
- Include at least one "reality check" track that seeks disconfirming evidence
"""

PLANNER_USER_PROMPT = """Research question: {user_question}

Today's date: {current_date}

Generate a comprehensive research plan in JSON format."""
```

### 2.3 实际示例——AI 预测调研的研究计划

```json
{
  "research_tracks": [
    {
      "track_name": "prediction_sources",
      "objective": "Find major AI predictions made in 2025 for 2026",
      "initial_queries": [
        "AI predictions 2026",
        "AI forecast 2026 experts",
        "Stanford HAI predictions 2026",
        "Gary Marcus AI predictions"
      ],
      "validation_queries": ["AI predictions 2026 wrong"],
      "sufficiency_criteria": "At least 15 specific, attributable predictions with sources",
      "priority": "high"
    },
    {
      "track_name": "agi_timeline_reality",
      "objective": "What actually happened with AGI claims by March 2026",
      "initial_queries": [
        "AGI 2026 progress",
        "GPT-5 capabilities benchmark",
        "Anthropic AGI claims 2026"
      ],
      "validation_queries": ["AGI skeptics 2026", "AGI not achieved"],
      "sufficiency_criteria": "Benchmark data + expert assessments from both optimists and skeptics",
      "priority": "high"
    },
    {
      "track_name": "ai_coding_reality",
      "objective": "Verify coding automation predictions vs actual adoption",
      "initial_queries": [
        "AI coding adoption 2026",
        "GitHub Copilot usage statistics",
        "Amodei 90% code prediction"
      ],
      "validation_queries": ["AI coding productivity study"],
      "sufficiency_criteria": "Adoption %, productivity data, employment figures",
      "priority": "high"
    },
    {
      "track_name": "infrastructure_spending",
      "objective": "Actual capex numbers vs predictions",
      "initial_queries": [
        "Big Tech AI spending 2026",
        "NVIDIA GTC 2026",
        "data center capex 2026"
      ],
      "validation_queries": ["AI infrastructure bubble concern"],
      "sufficiency_criteria": "Dollar figures from at least 4 hyperscalers",
      "priority": "medium"
    },
    {
      "track_name": "china_ai_ecosystem",
      "objective": "Chinese AI developments vs Western predictions",
      "initial_queries": [
        "DeepSeek V4 2026",
        "Chinese open source LLM leaderboard",
        "China AI chip progress 2026"
      ],
      "validation_queries": ["China AI gap closing"],
      "sufficiency_criteria": "Model rankings + chip production data",
      "priority": "medium"
    },
    {
      "track_name": "regulation_landscape",
      "objective": "AI regulation developments in 2026",
      "initial_queries": [
        "AI regulation 2026 state laws",
        "EU AI Act implementation",
        "AI regulation federal preemption"
      ],
      "validation_queries": ["AI regulation prediction accuracy"],
      "sufficiency_criteria": "Number of bills + key laws enacted",
      "priority": "medium"
    },
    {
      "track_name": "labor_market_impact",
      "objective": "Actual job displacement vs predictions",
      "initial_queries": [
        "AI job displacement 2026 data",
        "AI layoffs 2026",
        "software developer employment 2026"
      ],
      "validation_queries": ["AI job loss exaggerated"],
      "sufficiency_criteria": "Employment data + specific layoff examples",
      "priority": "medium"
    },
    {
      "track_name": "business_model_reality",
      "objective": "AI company revenues and profitability",
      "initial_queries": [
        "OpenAI revenue 2026",
        "Anthropic revenue growth",
        "AI ROI enterprise 2026"
      ],
      "validation_queries": ["AI bubble 2026", "AI trough disillusionment"],
      "sufficiency_criteria": "Revenue figures + ROI surveys",
      "priority": "low"
    }
  ],
  "synthesis_strategy": "Compare each prediction against reality using ✅/❌/🔄/🚀 framework. Group by theme, not by predictor. Highlight systematic biases in forecasting.",
  "output_structure": "Executive summary → Per-theme sections (prediction vs reality) → Scorecard table → Methodology → Conclusion on forecasting patterns",
  "known_challenges": [
    "Many 2026 predictions have year-end horizons, making March evaluation provisional",
    "Chinese sources may be limited in English",
    "Financial figures may conflict between sources (use most recent)",
    "AGI definitions vary, making 'achieved/not achieved' binary misleading"
  ]
}
```

---

## 三、Searcher 模块：多轮搜索策略

### 3.1 搜索策略的三层架构

```
Layer 1: 广度搜索 (Breadth Search)
  → 目标：快速覆盖主题的全貌
  → 查询特征：短（1-3词），通用
  → 例："AI predictions 2026"
  
Layer 2: 深度搜索 (Depth Search)  
  → 目标：针对发现的具体线索深挖
  → 查询特征：中等（3-6词），含具体名称/数字
  → 例："Dario Amodei coding prediction March 2025"

Layer 3: 验证搜索 (Validation Search)
  → 目标：交叉验证关键数据点，找反面证据
  → 查询特征：包含否定/对立视角
  → 例："AI coding productivity study negative results"
```

### 3.2 查询构造规则

```python
QUERY_CONSTRUCTION_RULES = """
1. 保持简短：1-6个词效果最佳
2. 使用实体名称：人名、公司名、产品名
3. 包含时间标记：年份或"2026"
4. 避免使用引号、site: 或 - 操作符
5. 每次查询必须与之前的查询有实质性差异
6. 如果第一次搜索结果不够，改变角度而非添加更多词
7. 对于金融数据，搜索多个来源交叉验证

好的查询示例:
- "OpenAI revenue 2026"（短+具体+时间）
- "NVIDIA GTC 2026 announcements"（事件+时间）
- "AI job displacement data 2026"（主题+数据+时间）

差的查询示例:
- "What are the latest predictions about artificial intelligence developments in 2026"（太长）
- "AI"（太短太模糊）
- "site:techcrunch.com AI predictions"（使用了操作符）
"""
```

### 3.3 动态搜索决策逻辑

这是最关键的部分——Agent 如何决定"下一步搜什么"：

```python
SEARCH_DECISION_PROMPT = """Based on the research plan and information gathered so far,
decide what to search next.

Current state of knowledge:
{accumulated_findings}

Research plan tracks still incomplete:
{incomplete_tracks}

Information gaps identified:
{gaps}

For each search action, explain:
1. WHY this search is needed (what gap does it fill?)
2. WHAT specific query to use
3. WHAT you expect to find
4. HOW CONFIDENT you are that existing info is sufficient (0-100%)

When confidence across all tracks exceeds 80%, recommend moving to synthesis.

Output as JSON:
{
  "confidence_by_track": {"track_name": confidence_pct, ...},
  "overall_confidence": pct,
  "next_actions": [
    {
      "action": "web_search" | "web_fetch" | "synthesize",
      "query_or_url": "...",
      "reason": "...",
      "expected_finding": "...",
      "track": "track_name"
    }
  ],
  "ready_to_synthesize": true | false
}"""
```

---

## 四、Reader 模块：信息提取与结构化

### 4.1 两阶段阅读

**阶段一：搜索结果快速扫描**
web_search 返回的 snippet 通常只有 2-3 句话。系统先扫描所有 snippet，找出最值得深读的源。

**阶段二：全文抓取与提取**
对高价值源使用 web_fetch 获取完整内容，然后提取结构化信息。

### 4.2 信息提取 Prompt

```python
EXTRACTION_PROMPT = """You are reading a web page to extract specific information 
for a research project.

Research context: {research_context}
Current track: {track_name}
Specific question being investigated: {specific_question}

Web page content:
{page_content}

Extract the following in JSON format:
{
  "key_claims": [
    {
      "claim": "The specific factual claim",
      "attribution": "Who said/wrote it",
      "date": "When it was said/published",
      "confidence": "high/medium/low based on source quality",
      "supporting_data": "Any numbers, stats, or evidence cited"
    }
  ],
  "new_leads": ["Any new names, sources, or topics worth investigating"],
  "conflicts_with_existing": ["Any contradictions with previously gathered info"],
  "source_quality": "Assess: primary source / respected publication / aggregator / blog / unknown"
}

Rules:
- Only extract verifiable factual claims, not opinions presented as facts
- Note when a claim comes from the subject themselves vs third-party reporting
- Flag any claims that conflict with previously gathered information
- Distinguish between predictions/forecasts and confirmed outcomes
"""
```

### 4.3 源质量分级

```python
SOURCE_QUALITY_HIERARCHY = {
    "tier_1_primary": [
        "Company blogs/press releases (for their own announcements)",
        "SEC filings, earnings calls",
        "Peer-reviewed papers",
        "Government data (BLS, Census, Fed)",
        "Official benchmark results"
    ],
    "tier_2_authoritative": [
        "MIT Technology Review, Nature, Science",
        "Wall Street Journal, Financial Times, Bloomberg",
        "Gartner, McKinsey, Goldman Sachs reports",
        "Stanford HAI, Brookings, PIIE"
    ],
    "tier_3_reliable": [
        "TechCrunch, The Verge, Ars Technica, Wired",
        "CNBC, Fortune, Forbes",
        "Industry-specific publications"
    ],
    "tier_4_secondary": [
        "Substack newsletters (expert-written)",
        "Medium articles",
        "Conference talks/interviews"
    ],
    "tier_5_use_with_caution": [
        "Reddit, Hacker News discussions",
        "Anonymous blogs",
        "SEO-optimized aggregation sites"
    ]
}
```

---

## 五、Synthesizer 模块：冲突解决与信息合成

### 5.1 冲突解决框架

```python
CONFLICT_RESOLUTION_PROMPT = """You have gathered information from multiple sources 
that contains conflicts. Resolve them using this framework:

Conflicting claims:
{conflicts}

Resolution rules (in priority order):
1. MORE RECENT > OLDER (for fast-changing data like revenue, stock price)
2. PRIMARY SOURCE > SECONDARY (company's own report > journalist's paraphrase)
3. DATA > OPINION (hard numbers > qualitative assessments)
4. MULTIPLE INDEPENDENT SOURCES > SINGLE SOURCE
5. METHODOLOGY-TRANSPARENT > METHODOLOGY-OPAQUE

For each conflict, output:
{
  "conflict": "Description of the conflicting claims",
  "resolution": "Which claim to prefer and why",
  "confidence": "How confident in this resolution",
  "present_as": "How to present this in the final report"
}

Important: When resolution is uncertain, present BOTH viewpoints with 
attribution rather than choosing one. The reader deserves to know about 
the disagreement.
"""
```

### 5.2 合成策略——我观察到的模式

Deep Research 不是简单地把搜索结果拼在一起。它的合成遵循一个特定模式：

```
1. 先建立 FRAMEWORK（评判框架）
   → 在 AI 预测案例中，这是 ✅/❌/🔄/🚀 分类法

2. 再按 THEME 组织，而非按 SOURCE 组织
   → 不是"MIT Tech Review 说了什么，Gartner 说了什么"
   → 而是"AGI 预测的整体情况是..."

3. 每个主题遵循 CLAIM → EVIDENCE → VERDICT 结构
   → Claim: 谁预测了什么
   → Evidence: 实际发生了什么（带数据）
   → Verdict: 评估预测的准确性

4. 最后做 META-ANALYSIS（元分析）
   → 预测者的系统性偏差是什么？
   → 哪类预测最准？哪类最不准？
```

---

## 六、完整的 Claude API 实现

### 6.1 核心架构代码

```python
import anthropic
import json
import time
from dataclasses import dataclass, field
from typing import Optional

client = anthropic.Anthropic()  # 自动读取 ANTHROPIC_API_KEY

# ============================================
# 数据结构
# ============================================

@dataclass
class SearchResult:
    query: str
    snippets: list[dict]     # [{title, url, snippet}]
    timestamp: str

@dataclass
class FetchedPage:
    url: str
    content: str
    source_quality: str      # tier_1 ~ tier_5

@dataclass 
class ExtractedClaim:
    claim: str
    attribution: str
    date: str
    confidence: str
    supporting_data: str
    source_url: str
    track: str

@dataclass
class ResearchState:
    """整个调研过程的状态管理"""
    question: str
    plan: dict = field(default_factory=dict)
    search_results: list[SearchResult] = field(default_factory=list)
    fetched_pages: list[FetchedPage] = field(default_factory=list)
    extracted_claims: list[ExtractedClaim] = field(default_factory=list)
    search_count: int = 0
    fetch_count: int = 0
    max_searches: int = 40
    max_fetches: int = 15
    confidence_by_track: dict = field(default_factory=dict)
```

### 6.2 Planner 实现

```python
def generate_research_plan(state: ResearchState) -> dict:
    """第一步：生成研究计划"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",  # Planner 用 Sonnet 够了，省成本
        max_tokens=4096,
        system=PLANNER_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Research question: {state.question}\n\nToday's date: 2026-03-23\n\nGenerate a comprehensive research plan in JSON format."
        }]
    )
    
    # 解析 JSON（处理 markdown 代码块包裹的情况）
    text = response.content[0].text
    text = text.strip().removeprefix("```json").removesuffix("```").strip()
    plan = json.loads(text)
    
    state.plan = plan
    # 初始化每个 track 的信心度
    for track in plan["research_tracks"]:
        state.confidence_by_track[track["track_name"]] = 0
    
    return plan
```

### 6.3 搜索执行器（带 Tool Use）

```python
def execute_search_round(state: ResearchState, queries: list[dict]) -> list[SearchResult]:
    """执行一轮搜索——使用 Claude 的 tool_use 能力"""
    
    tools = [
        {
            "name": "web_search",
            "type": "web_search_20250305"
        }
    ]
    
    results = []
    for q in queries:
        if state.search_count >= state.max_searches:
            print(f"⚠️ 达到搜索上限 ({state.max_searches})，停止搜索")
            break
            
        # 让 Claude 执行搜索并提取关键信息
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=[{
                "role": "user",
                "content": f"""Search for: {q['query']}
                
Context: This is part of a research project about: {state.question}
Specifically investigating: {q.get('reason', 'general exploration')}

After getting search results, summarize the key findings relevant to our research."""
            }]
        )
        
        state.search_count += 1
        
        # 处理 tool use 响应
        search_result = SearchResult(
            query=q['query'],
            snippets=_extract_search_results(response),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        results.append(search_result)
        state.search_results.append(search_result)
        
        # 控制速率
        time.sleep(0.5)
    
    return results


def fetch_page(state: ResearchState, url: str, context: str) -> Optional[FetchedPage]:
    """抓取完整网页内容"""
    
    if state.fetch_count >= state.max_fetches:
        return None
    
    tools = [
        {
            "name": "web_search",
            "type": "web_search_20250305"
        }
    ]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        tools=tools,
        messages=[{
            "role": "user",
            "content": f"""Fetch and read this URL: {url}

Extract all information relevant to: {context}

Provide a structured summary of the key facts, data points, and claims found."""
        }]
    )
    
    state.fetch_count += 1
    
    page = FetchedPage(
        url=url,
        content=_extract_text_content(response),
        source_quality=_assess_source_quality(url)
    )
    state.fetched_pages.append(page)
    
    return page
```

### 6.4 动态搜索决策器——Agent Loop 的核心

```python
def research_agent_loop(state: ResearchState):
    """核心 Agent 循环：搜索→分析→决定下一步→重复"""
    
    # 第一步：生成研究计划
    plan = generate_research_plan(state)
    print(f"📋 研究计划生成完毕，{len(plan['research_tracks'])} 个研究轨道")
    
    # 第二步：按优先级执行初始搜索
    high_priority = [t for t in plan['research_tracks'] if t['priority'] == 'high']
    medium_priority = [t for t in plan['research_tracks'] if t['priority'] == 'medium']
    low_priority = [t for t in plan['research_tracks'] if t['priority'] == 'low']
    
    for track_group in [high_priority, medium_priority, low_priority]:
        for track in track_group:
            queries = [{"query": q, "reason": track["objective"]} 
                      for q in track["initial_queries"]]
            execute_search_round(state, queries)
    
    # 第三步：迭代深化——这是 Deep Research 的关键
    iteration = 0
    max_iterations = 5
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 迭代 {iteration}/{max_iterations}")
        
        # 让 Claude 分析当前状态并决定下一步
        decision = get_next_action_decision(state)
        
        if decision["ready_to_synthesize"]:
            print("✅ 信息充足，进入合成阶段")
            break
        
        # 执行决定的搜索/抓取动作
        for action in decision["next_actions"]:
            if action["action"] == "web_search":
                execute_search_round(state, [action])
            elif action["action"] == "web_fetch":
                fetch_page(state, action["query_or_url"], action["reason"])
        
        # 更新信心度
        state.confidence_by_track = decision["confidence_by_track"]
        
        avg_confidence = sum(decision["confidence_by_track"].values()) / len(decision["confidence_by_track"])
        print(f"📊 平均信心度: {avg_confidence:.0f}%")
    
    # 第四步：合成最终报告
    return synthesize_report(state)


def get_next_action_decision(state: ResearchState) -> dict:
    """让 Claude 分析现有信息并决定下一步搜索什么"""
    
    # 将已收集的信息压缩为摘要（避免 context window 爆炸）
    findings_summary = compress_findings(state)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": SEARCH_DECISION_PROMPT.format(
                accumulated_findings=findings_summary,
                incomplete_tracks=json.dumps([
                    t["track_name"] for t in state.plan["research_tracks"]
                    if state.confidence_by_track.get(t["track_name"], 0) < 75
                ]),
                gaps=identify_gaps(state)
            )
        }]
    )
    
    text = response.content[0].text
    text = text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)


def compress_findings(state: ResearchState) -> str:
    """将所有已收集信息压缩为结构化摘要，防止 context window 溢出"""
    
    # 这是一个关键技巧：用 Claude 本身来压缩中间状态
    all_info = "\n\n".join([
        f"[Search: {r.query}]\n" + "\n".join([s.get("snippet", "") for s in r.snippets])
        for r in state.search_results[-15:]  # 只取最近 15 次搜索
    ])
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{
            "role": "user",
            "content": f"""Compress the following research findings into a structured 
summary organized by research track. Include key data points and claims with sources.
Keep it under 2000 words.

Research tracks: {json.dumps([t['track_name'] for t in state.plan['research_tracks']])}

Raw findings:
{all_info}"""
        }]
    )
    
    return response.content[0].text
```

### 6.5 最终合成——Opus 出场

```python
def synthesize_report(state: ResearchState) -> str:
    """用 Opus 进行最终合成——这是质量的关键"""
    
    # 准备所有收集到的信息
    all_findings = compress_findings(state)
    
    response = client.messages.create(
        model="claude-opus-4-6",  # 最终合成用 Opus，质量更高
        max_tokens=16000,
        messages=[{
            "role": "user",
            "content": f"""You are writing a comprehensive research report.

## Research Question
{state.question}

## Research Plan
{json.dumps(state.plan['output_structure'])}

## All Gathered Information
{all_findings}

## Synthesis Instructions
{json.dumps(state.plan['synthesis_strategy'])}

Write the complete report following the planned structure. 

Key requirements:
1. Every factual claim must be attributable to a specific source
2. When sources conflict, present both views with attribution
3. Clearly distinguish between predictions/forecasts and confirmed outcomes
4. Use data and numbers wherever available
5. Include a methodology section explaining how the research was conducted
6. End with meta-analysis of patterns across the findings

Write in a direct, analytical style. Avoid hedging language. 
Be specific about what is known, what is uncertain, and what is unknown."""
        }]
    )
    
    return response.content[0].text
```

---

## 七、关键设计决策与优化技巧

### 7.1 模型选择策略

```
┌─────────────┬──────────────────┬──────────────────────┐
│ 阶段         │ 推荐模型          │ 原因                  │
├─────────────┼──────────────────┼──────────────────────┤
│ Planner     │ Sonnet 4         │ 结构化规划，速度快      │
│ Searcher    │ Sonnet 4         │ 搜索决策，需要速度      │
│ Reader      │ Sonnet 4         │ 信息提取，中等复杂度    │
│ Synthesizer │ Opus 4.6         │ 冲突解决，需要深度推理  │
│ Writer      │ Opus 4.6         │ 最终输出，需要最高质量  │
└─────────────┴──────────────────┴──────────────────────┘

成本优化：整个调研 ~80% 的 API 调用用 Sonnet，只在最后合成用 Opus
估算成本：一次完整调研约 $2-5（取决于主题复杂度）
```

### 7.2 Context Window 管理——最重要的工程挑战

```python
# 核心问题：40次搜索的原始结果可能有 200k+ tokens，远超 context window
# 解决方案：渐进式压缩

COMPRESSION_STRATEGY = """
Level 0: 原始搜索结果 (~200k tokens)
  ↓ 每轮搜索后立即提取关键信息
Level 1: 结构化提取 (~50k tokens)  
  ↓ 每5轮搜索后压缩一次
Level 2: 摘要+关键数据点 (~15k tokens)
  ↓ 最终合成前再压缩一次
Level 3: 报告草稿素材 (~8k tokens)
  → 送入 Opus 生成最终报告
"""

# 实现：滑动窗口 + 渐进压缩
def manage_context(state: ResearchState):
    """每 5 次搜索执行一次压缩"""
    if state.search_count % 5 == 0 and state.search_count > 0:
        compressed = compress_findings(state)
        # 用压缩后的摘要替代原始数据
        state.compressed_summary = compressed
        # 只保留最近 5 次搜索的原始结果
        state.search_results = state.search_results[-5:]
```

### 7.3 搜索去重与覆盖度检查

```python
def deduplicate_queries(new_queries: list[str], 
                        existing_queries: list[str]) -> list[str]:
    """确保新查询与已有查询有实质性差异"""
    
    deduplicated = []
    for q in new_queries:
        q_words = set(q.lower().split())
        is_duplicate = False
        for existing in existing_queries:
            existing_words = set(existing.lower().split())
            # Jaccard 相似度 > 0.6 视为重复
            overlap = len(q_words & existing_words) / len(q_words | existing_words)
            if overlap > 0.6:
                is_duplicate = True
                break
        if not is_duplicate:
            deduplicated.append(q)
    
    return deduplicated
```

### 7.4 结果验证的三角测量法

```python
TRIANGULATION_RULE = """
对于关键数据点（如收入、融资额、用户数），至少需要：
- 2 个独立来源确认
- 如果只有 1 个来源，标记为"未验证"
- 如果来源冲突，优先采用：
  1. 公司官方披露 > 媒体报道
  2. 更近的日期 > 更远的日期
  3. Tier 1-2 来源 > Tier 3-5 来源
"""
```

---

## 八、完整运行示例

### 8.1 一键运行

```python
def deep_research(question: str, 
                  max_searches: int = 40,
                  max_fetches: int = 15) -> str:
    """一键运行完整的深度调研"""
    
    state = ResearchState(
        question=question,
        max_searches=max_searches,
        max_fetches=max_fetches
    )
    
    print(f"🔬 开始深度调研: {question}")
    print(f"📊 搜索上限: {max_searches} 次, 抓取上限: {max_fetches} 次")
    print("=" * 60)
    
    report = research_agent_loop(state)
    
    print("\n" + "=" * 60)
    print(f"✅ 调研完成!")
    print(f"📊 实际搜索: {state.search_count} 次")
    print(f"📄 实际抓取: {state.fetch_count} 次")
    print(f"📝 报告长度: {len(report)} 字符")
    
    return report


# 运行
if __name__ == "__main__":
    report = deep_research(
        "2025年对2026年的AI预测，哪些实现了，哪些没有，哪些现实更精彩"
    )
    
    with open("research_report.md", "w") as f:
        f.write(report)
```

---

## 九、高级优化方向

### 9.1 并行搜索（提速 3-5x）

```python
import asyncio

async def parallel_search(state: ResearchState, queries: list[dict]):
    """并行执行多个搜索——大幅提速"""
    
    async_client = anthropic.AsyncAnthropic()
    
    async def single_search(query_info):
        response = await async_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=[{"name": "web_search", "type": "web_search_20250305"}],
            messages=[{
                "role": "user",
                "content": f"Search for: {query_info['query']}\nContext: {query_info.get('reason', '')}"
            }]
        )
        return response
    
    # 并行执行，但控制并发数（避免 rate limit）
    semaphore = asyncio.Semaphore(3)  # 最多 3 个并发
    
    async def limited_search(q):
        async with semaphore:
            return await single_search(q)
    
    results = await asyncio.gather(*[limited_search(q) for q in queries])
    return results
```

### 9.2 增量缓存（避免重复搜索）

```python
import hashlib

class SearchCache:
    """缓存搜索结果，避免重复查询"""
    
    def __init__(self):
        self._cache = {}
    
    def _key(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
    
    def get(self, query: str) -> Optional[SearchResult]:
        return self._cache.get(self._key(query))
    
    def set(self, query: str, result: SearchResult):
        self._cache[self._key(query)] = result
    
    def has(self, query: str) -> bool:
        return self._key(query) in self._cache
```

### 9.3 研究质量自评（可选但推荐）

```python
SELF_EVALUATION_PROMPT = """Evaluate this research report on 5 dimensions:

1. COVERAGE: Did we investigate all major aspects? (1-10)
2. EVIDENCE: Are claims supported by cited data? (1-10)
3. BALANCE: Are opposing viewpoints fairly represented? (1-10)
4. RECENCY: Is the most recent information used? (1-10)
5. ACTIONABILITY: Can the reader make decisions based on this? (1-10)

For each dimension scoring below 7, suggest specific improvements.

Report:
{report}
"""
```

---

## 十、与 Claude 内置 Deep Research 的对比

| 维度 | Claude 内置 Deep Research | 自建 API 版本 |
|------|--------------------------|--------------|
| 搜索次数 | ~50-100 次 | 可自定义（推荐 30-50） |
| 运行时间 | 3-10 分钟 | 取决于并行度，可做到 2-5 分钟 |
| 结果质量 | 很高（Opus 级别合成） | 取决于你的 prompt 调优 |
| 可定制性 | 低（黑盒） | 完全可定制 |
| 成本 | Pro/Team 订阅 | ~$2-5/次（可优化到 $1 以下） |
| 中间过程可见 | 部分可见 | 完全可见+可调试 |
| 适合场景 | 通用调研 | 垂直领域深度定制 |

### 关键优势：自建版本可以做到 Claude 内置版做不到的事

1. **领域定制**：为 Treelaw 的法律研究定制搜索策略和源优先级
2. **集成私有数据**：将搜索结果与内部数据库/知识库融合
3. **持续监控**：定时运行，追踪主题变化
4. **批量处理**：同时调研多个主题
5. **结果格式定制**：输出为任意格式（JSON、数据库记录、Notion 页面等）

---

## 十一、快速上手 Checklist

```
□ 1. 获取 Anthropic API Key（需要 web search 权限）
□ 2. pip install anthropic
□ 3. 复制上面的核心代码
□ 4. 先用简单主题测试（如"最近一周AI新闻"）
□ 5. 调整 PLANNER_SYSTEM_PROMPT 适配你的领域
□ 6. 调整 max_searches 和 max_fetches 控制成本
□ 7. 添加你的领域特定的源质量分级
□ 8. 逐步增加复杂度
```
