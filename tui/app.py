"""
Explore TUI — sunqi + Claude 的技术探索可视化终端
在另一个终端运行: python tui/app.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from datetime import datetime

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Static,
    Markdown,
    Tree,
    TabbedContent,
    TabPane,
    Label,
    ListView,
    ListItem,
)
from textual.reactive import reactive
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.console import Group


ROOT = Path(__file__).resolve().parent.parent


def _load_md(name: str) -> str:
    """Load a markdown file from research/ dir, fallback to empty."""
    p = ROOT / "research" / name
    if p.exists():
        return p.read_text(encoding="utf-8")
    return f"*{name} not found*"


# ── Data ────────────────────────────────────────────────────────────────

ECOSYSTEM_STARS = [
    ("karpathy/autoresearch", 58865, "优化循环开山之作"),
    ("gpt-researcher", 26066, "深度调研报告"),
    ("microsoft/RD-Agent", 12088, "MLE-Bench 冠军"),
    ("AutoResearchClaw", 9197, "MetaClaw 自学习"),
    ("AI-Research-SKILLs", 5731, "87 个技能模块"),
    ("AgentLaboratory", 5444, "三阶段全流程"),
    ("AI-Researcher", 4976, "NeurIPS 2025"),
    ("AI-Scientist-v2", 3068, "首篇 AI 论文被接收"),
    ("autoresearch (udit)", 2589, "Claude Code Skill"),
    ("awesome-autoresearch", 867, "生态索引"),
    ("WecoAI/awesome", 435, "实践案例"),
    ("Awesome-Auto-Tools", 138, "工具选型"),
]

PARADIGM_EVOLUTION = """```
  autoresearch (Karpathy, 2026.03)
  ┌─────────────────────────────────────┐
  │ program.md + train.py               │
  │ 单指标 · 不可变 eval · 无限循环      │
  │ 领域: LLM 训练                      │
  └──────────────┬──────────────────────┘
                 │
       ┌─────────┴──────────┐
       ▼                    ▼
  autoresearch-anything    GOAL.md
  ┌──────────────────┐  ┌─────────────────────────┐
  │ npx 一行命令启动  │  │ 构造式指标 · 双分评分    │
  │ 问答式脚手架      │  │ Action Catalog          │
  │ 适合: 指标已知    │  │ 3 种 Operating Mode     │
  └──────────────────┘  │ 适合: 需要造尺子的项目   │
                        └─────────────────────────┘
```"""


FIVE_PATTERNS = """## 跨项目关键模式

### ① Fitness Function 是一切的基础
没有可度量的指标，就没有自动优化。
如果指标不存在，**先造指标**。

### ② Keep-or-Revert 是最安全的探索策略
每次尝试要么让事情变好，要么完全回滚。
git 是天然的 checkpoint 系统。

### ③ Iteration Log 是 Skill 进化的原材料
iterations.jsonl 记录每次 before/after + action + 结果。
这就是 Voyager skill library 的数据来源。

### ④ Dual Score 防止 Goodhart's Law
"当一个度量变成目标，它就不再是好的度量。"
双分评分：优化目标 + 验证度量工具本身。

### ⑤ Constraints 不是建议，是红线
没有约束的 agent 会创造性地"让数字变好"。
明确声明不可触碰的文件和不可绕过的验证。"""

GOAL_MD_DETAIL = """## GOAL.md — 五要素拆解

### 1. Fitness Function（适应度函数）
```bash
./scripts/score.sh    # → 47/100... 52... 61... 83
```

三种模式:
| 模式 | 含义 |
|------|------|
| **Locked** | Agent 不能碰评分代码 |
| **Split** | Agent 可改工具，不改定义 |
| **Open** | Agent 可改一切 |

### 2. Improvement Loop（改进循环）
```
repeat:
  1. 跑 fitness function
  2. 找最弱环节
  3. 选最高 impact 动作
  4. 执行变更
  5. 重新度量
  6. 变好? commit. 变差? revert.
```

### 3. Action Catalog（动作目录）
| Action | Impact | How |
|--------|--------|-----|
| 修复坏掉的测试 | +5 pts | 诊断→修复→重跑 |
| 补缺失的配置页 | +3-5 pts | 从模板创建 |
| 修复双向链接 | +2-3 pts | 补缺失的一端 |

### 4. Operating Mode（运行模式）
| 模式 | 用途 |
|------|------|
| **Converge** | 达标即停 |
| **Continuous** | 永不停止（autoresearch 默认） |
| **Supervised** | 关键节点人工确认 |

### 5. Constraints（约束红线）
- 永远不伪造测试结果
- 永远不改凭证
- 每次改动前后必须度量
- 原子提交，回滚干净"""


# ── Widgets ─────────────────────────────────────────────────────────────


class StarsChart(Static):
    """Bar chart of project stars."""

    def render(self):
        table = Table(
            title="AutoResearch 生态 Stars 排行",
            title_style="bold cyan",
            show_lines=False,
            padding=(0, 1),
            expand=True,
        )
        table.add_column("项目", style="white", min_width=24)
        table.add_column("Stars", justify="right", style="yellow", min_width=8)
        table.add_column("", min_width=40)
        table.add_column("定位", style="dim", min_width=20)

        max_stars = ECOSYSTEM_STARS[0][1]
        for name, stars, desc in ECOSYSTEM_STARS:
            bar_len = int(stars / max_stars * 35)
            bar = "█" * bar_len + "░" * (35 - bar_len)
            color = (
                "bright_green"
                if stars > 10000
                else "green" if stars > 5000 else "yellow" if stars > 1000 else "dim"
            )
            table.add_row(name, f"{stars:,}", f"[{color}]{bar}[/]", desc)

        return table


class DocViewer(VerticalScroll):
    """Scrollable markdown document viewer."""

    doc_path: reactive[str] = reactive("")

    def compose(self) -> ComposeResult:
        yield Markdown("", id="doc-content")

    def watch_doc_path(self, path: str) -> None:
        if path and os.path.isfile(path):
            content = Path(path).read_text(encoding="utf-8")
            self.query_one("#doc-content", Markdown).update(content)
        elif path:
            self.query_one("#doc-content", Markdown).update(
                f"*File not found: {path}*"
            )


# ── Main App ────────────────────────────────────────────────────────────


class ExploreTUI(App):
    """Explore 工作台 TUI"""

    CSS = """
    Screen {
        background: $surface;
    }
    #sidebar {
        width: 32;
        dock: left;
        background: $panel;
        border-right: solid $primary;
        padding: 1;
    }
    #sidebar ListView {
        height: auto;
        margin-top: 1;
    }
    #sidebar ListItem {
        padding: 0 1;
    }
    #sidebar ListItem:hover {
        background: $primary 20%;
    }
    #sidebar .sidebar-title {
        text-style: bold;
        color: $text;
        padding: 0 1;
    }
    TabbedContent {
        height: 1fr;
    }
    TabPane {
        padding: 0;
    }
    TabPane > VerticalScroll, TabPane > Vertical {
        height: 1fr;
        padding: 1 2;
    }
    VerticalScroll {
        scrollbar-size: 1 1;
    }
    StarsChart {
        height: auto;
        margin: 1 0;
    }
    .section-header {
        text-style: bold;
        color: $accent;
        margin: 1 0 0 0;
    }
    DocViewer {
        height: 1fr;
    }
    #doc-list {
        height: auto;
        max-height: 16;
        margin: 0 0 1 0;
    }
    """

    TITLE = "Explore TUI — 技术探索可视化"
    SUB_TITLE = f"sunqi + Claude | {datetime.now().strftime('%Y-%m-%d')}"

    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("d", "toggle_dark", "主题"),
        Binding("1", "tab_overview", "总览"),
        Binding("2", "tab_paradigm", "范式"),
        Binding("3", "tab_awesome", "Awesome"),
        Binding("4", "tab_goalmd", "GOAL.md"),
        Binding("5", "tab_docs", "文档"),
        Binding("r", "refresh_docs", "刷新"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(id="tabs"):
            with TabPane("总览 [1]", id="tab-overview"):
                with VerticalScroll():
                    yield Static(
                        "[bold cyan]AutoResearch 生态全景[/]\n"
                        "调研日期: 2026-03-28 | 覆盖 50+ 项目 | 3 个 Awesome List\n",
                        classes="section-header",
                    )
                    yield StarsChart()
                    yield Markdown(FIVE_PATTERNS)

            with TabPane("范式演进 [2]", id="tab-paradigm"):
                with VerticalScroll():
                    yield Markdown(
                        "# 从 autoresearch 到 GOAL.md\n\n"
                        "Karpathy 证明了 `agent + fitness function + loop = 突破`。\n"
                        "但当没有现成指标时呢？\n\n"
                        + PARADIGM_EVOLUTION
                        + "\n\n---\n\n"
                        "## 对比\n\n"
                        "| | autoresearch | autoresearch-anything | GOAL.md |\n"
                        "|---|---|---|---|\n"
                        "| 复杂度 | 最低 | 低 | 中 |\n"
                        "| 指标来源 | 必须已有 | 假设已有 | 帮你构造 |\n"
                        "| 双分评分 | ✗ | ✗ | ✓ |\n"
                        "| Action Catalog | 隐式 | 无 | 显式 |\n"
                        "| Operating Modes | Continuous | Continuous | 3种 |\n"
                        "| 上手方式 | 读 program.md | `npx` | 读方法论 |\n"
                        "| **适合** | LLM 训练 | 快速启动 | 复杂项目 |\n"
                    )

            with TabPane("Awesome Lists [3]", id="tab-awesome"):
                with VerticalScroll():
                    yield Markdown(_load_md("awesome-lists-analysis.md"))

            with TabPane("GOAL.md [4]", id="tab-goalmd"):
                with VerticalScroll():
                    yield Markdown(GOAL_MD_DETAIL)

            with TabPane("文档 [5]", id="tab-docs"):
                with Vertical():
                    yield Label("选择文档:", classes="section-header")
                    yield ListView(
                        *self._build_doc_items(),
                        id="doc-list",
                    )
                    yield DocViewer(id="doc-viewer")

        yield Footer()

    def _build_doc_items(self) -> list[ListItem]:
        items = []
        doc_dirs = [ROOT / "research", ROOT / "tools"]
        for d in doc_dirs:
            if d.exists():
                for f in sorted(d.glob("*.md")):
                    label = f"[{'research' if 'research' in str(d) else 'tools'}] {f.stem}"
                    item = ListItem(Label(label))
                    item._doc_path = str(f)
                    items.append(item)
        # also add top-level docs
        for name in ["SOUL.md", "USER.md", "HISTORY.md", "CLAUDE.md"]:
            p = ROOT / name
            if p.exists():
                item = ListItem(Label(f"[system] {name}"))
                item._doc_path = str(p)
                items.append(item)
        # journal
        journal_dir = ROOT / "journal"
        if journal_dir.exists():
            for f in sorted(journal_dir.glob("*.md"), reverse=True):
                item = ListItem(Label(f"[journal] {f.stem}"))
                item._doc_path = str(f)
                items.append(item)
        return items

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, "_doc_path"):
            viewer = self.query_one("#doc-viewer", DocViewer)
            viewer.doc_path = item._doc_path

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def action_tab_overview(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-overview"

    def action_tab_paradigm(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-paradigm"

    def action_tab_awesome(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-awesome"

    def action_tab_goalmd(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-goalmd"

    def action_tab_docs(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-docs"

    def action_refresh_docs(self) -> None:
        """刷新文档列表 + 重新加载当前文档"""
        doc_list = self.query_one("#doc-list", ListView)
        doc_list.clear()
        for item in self._build_doc_items():
            doc_list.append(item)
        # 也刷新 Awesome tab（从文件重新加载）
        try:
            awesome_tab = self.query_one("#tab-awesome VerticalScroll Markdown", Markdown)
            awesome_tab.update(_load_md("awesome-lists-analysis.md"))
        except Exception:
            pass
        self.notify(f"已刷新，发现 {len(self._build_doc_items())} 个文档")


if __name__ == "__main__":
    app = ExploreTUI()
    app.run()
