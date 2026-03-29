# AI Agent 浏览器会话共享工具调研

> 调研日期：2026-03-29
> 核心问题：如何让 AI agent 访问用户已登录的网站（共享 cookie/session）

## TL;DR

这个领域在 2025-2026 爆发了。核心方案分三类：

1. **连接真实浏览器**（推荐）— Chrome DevTools MCP、Playwriter、BrowserMCP、chrome-cdp-skill
2. **持久化 profile 复用**（主力）— Playwright MCP、agent-browser、browser-use
3. **Cookie 提取注入**（辅助）— sweet-cookie、storage-state 文件

**与 Claude Code 集成的最佳方案**：Chrome DevTools MCP（Google 官方）或 Playwright MCP（Microsoft 官方），都有一等 MCP 支持。

---

## 方案一：连接用户真实浏览器实例

### 1. Chrome DevTools MCP（Google 官方）

| 项目 | 信息 |
|------|------|
| URL | https://github.com/ChromeDevTools/chrome-devtools-mcp |
| Stars | 32.1k |
| 维护者 | Google ChromeDevTools 团队 |
| 许可证 | 未明确标注（Google 官方项目） |
| 活跃度 | 非常活跃，688 commits |

**工作原理**：
- 作为 MCP server 运行，通过 Chrome DevTools Protocol（CDP）连接到正在运行的 Chrome
- Chrome 146+ 支持 `autoConnect`：直接接管用户当前浏览器实例，包括所有 cookie、登录态、localStorage
- 也支持通过 `--user-data-dir` 创建独立调试 profile

**Claude Code 集成**：
```bash
# 方式1：连接已运行的 Chrome（需开启 autoConnect）
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --browserUrl=http://127.0.0.1:9222

# 方式2：自动启动 Chrome
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

**安全评估**：
- [x] 开源可审计（Google 官方维护）
- [x] 纯本地运行，cookie 不外传
- [ ] **无权限控制** — 连接后 agent 可访问所有 tab 的所有数据
- [x] 社区信任度极高（32k+ stars）
- **风险**：autoConnect 模式下 agent 能看到浏览器里的一切，包括银行、邮箱。cookie 管理目前还是 open issue (#408)

**安全建议**：
- 只在需要时开启 autoConnect，用完立即关
- 关掉敏感网站的 tab 再让 agent 操作
- 优先用 `--user-data-dir` 隔离 profile 方案

---

### 2. Playwriter

| 项目 | 信息 |
|------|------|
| URL | https://github.com/remorses/playwriter |
| Stars | 3.3k |
| 许可证 | MIT |
| 最新版 | v0.0.89 (2026-03-13) |
| 活跃度 | 活跃开发中 |

**工作原理**：
- Chrome 扩展 + 本地 WebSocket Server (localhost:19988) + MCP Client
- 扩展通过 `chrome.debugger` API 接入 CDP
- **用户必须点击扩展图标授权每个 tab**（显式同意模型）
- Agent 在用户真实浏览器里执行 Playwright 代码片段

**安全评估**：
- [x] 开源可审计
- [x] 纯本地运行（server 绑定 localhost）
- [x] **有权限控制** — tab 级别显式授权，只有点过图标的 tab 才能被操控
- [x] Origin 验证，只有合法扩展 ID 能连接
- [x] Chrome 会显示自动化提示横幅
- **中等信任度**（3.3k stars，但安全模型设计合理）

**安全建议**：
- 安全模型在同类工具中最好 — tab 级别授权 + 可视化提示
- 适合需要精细控制的场景

---

### 3. BrowserMCP

| 项目 | 信息 |
|------|------|
| URL | https://github.com/BrowserMCP/mcp |
| Stars | 6.2k |
| 许可证 | Apache 2.0 |
| 最近提交 | 2025-01-25 |
| 活跃度 | **开发停滞**（最后更新 2025年1月） |

**工作原理**：
- Chrome 扩展 + MCP Server 双组件
- 连接用户现有浏览器实例，保持所有登录态
- 基于 Microsoft Playwright MCP 改造，专门面向用户真实浏览器

**安全评估**：
- [x] 开源可审计
- [x] 纯本地运行
- [ ] 无细粒度权限控制
- **风险**：项目已停更超过 1 年，可能有未修复的安全问题

---

### 4. chrome-cdp-skill

| 项目 | 信息 |
|------|------|
| URL | https://github.com/pasky/chrome-cdp-skill |
| Stars | 2.7k |
| 许可证 | MIT |
| 最新版 | v1.0.2 (2026-03-13) |
| 活跃度 | 活跃 |

**工作原理**：
- 直接通过 WebSocket 连接 Chrome CDP，无中间框架
- 连接到用户已打开的 tab，保留登录态和页面上下文
- 后台 daemon 维持连接，20分钟不活动自动终止
- Chrome 会弹出一次权限确认弹窗

**安全评估**：
- [x] 开源可审计
- [x] 纯本地运行
- [x] Chrome 原生权限弹窗保护
- [x] 零依赖（纯 Node.js）
- **中等信任度**（2.7k stars）

**集成方式**：主要面向 pi agents（skills 系统），但可手动集成到其他 agent。

---

## 方案二：持久化 Profile / Session 复用

### 5. Playwright MCP（Microsoft 官方）

| 项目 | 信息 |
|------|------|
| URL | https://github.com/microsoft/playwright-mcp |
| Stars | 29.9k |
| 维护者 | Microsoft |
| 许可证 | 有 LICENSE 文件 |
| 活跃度 | 非常活跃 |

**工作原理**：
三种模式：
1. **持久 Profile 模式**（默认）— 在系统缓存目录存储登录信息，跨会话保持
2. **隔离模式** — 临时 context，关闭即丢失
3. **浏览器扩展模式** — 连接已有 tab，复用登录态（类似方案一）

**Session 共享方法**：
- `--user-data-dir`：指定 Chrome profile 目录，保留所有 cookie/localStorage
- `--storage-state`：加载包含 cookie + localStorage 的 JSON 文件
- 也可连接现有浏览器实例

**Claude Code 集成**：
```bash
# 基础配置
claude mcp add playwright -- npx @playwright/mcp@latest

# 使用自定义 profile（保持登录态）
claude mcp add playwright -- npx @playwright/mcp@latest --user-data-dir="$HOME/.playwright-profile"

# 使用 storage-state 文件注入 cookie
claude mcp add playwright -- npx @playwright/mcp@latest --storage-state=./auth.json
```

**安全评估**：
- [x] 开源可审计（Microsoft 官方维护）
- [x] 纯本地运行
- [x] **有限权限控制** — `--allowed-hosts` 白名单 + DNS rebinding 防护
- [x] 社区信任度极高（30k stars）
- **支持浏览器**：Chrome, Firefox, WebKit, Edge
- **注意**：origin blocklist/allowlist 官方说明"不作为安全边界"

---

### 6. agent-browser（Vercel Labs）

| 项目 | 信息 |
|------|------|
| URL | https://github.com/vercel-labs/agent-browser |
| Stars | 25.6k |
| 语言 | Rust |
| 许可证 | 未明确标注 |
| 活跃度 | 非常活跃（492 commits） |

**工作原理**：
- Rust 编写的高性能 CLI
- `--profile` 参数：指定 profile 目录，登录一次后跨会话复用
- `--session-name`：自动保存/恢复 cookie 和 localStorage 到 `~/.agent-browser/sessions/`
- 支持 AES-256-GCM 加密 session 数据（设置 `AGENT_BROWSER_ENCRYPTION_KEY`）

**安全评估**：
- [x] 开源可审计
- [x] 纯本地运行
- [x] **session 数据可加密**（AES-256-GCM，同类工具中唯一）
- [x] 社区信任度高（25.6k stars, Vercel 背书）
- **注意**：session 文件默认明文存储，必须设置加密密钥 + .gitignore

---

### 7. browser-use

| 项目 | 信息 |
|------|------|
| URL | https://github.com/browser-use/browser-use |
| Stars | 84.9k |
| 许可证 | MIT |
| 活跃度 | 极高活跃度（最热门的 AI browser agent 项目） |

**工作原理**：
- Python 库，底层基于 Playwright
- 可复用真实 Chrome profile（带已保存的登录信息）
- 支持 profile 同步到远程浏览器
- Cloud 版本提供持久化文件系统和会话记忆

**安全评估**：
- [x] 开源可审计
- [x] 本地模式纯本地运行
- [x] 社区信任度极高（85k stars，生态最大）
- [ ] Cloud 模式会将浏览器运行在远程 — **cookie 会到云端**
- **注意**：Cloud 模式下 session 数据在 Browserbase 服务器上，有信任风险

---

## 方案三：Cookie 提取/注入工具

### 8. sweet-cookie

| 项目 | 信息 |
|------|------|
| URL | https://github.com/steipete/sweet-cookie |
| Stars | 143 |
| 许可证 | 未明确标注 |
| 最新版 | v0.2.0 (2026-03-08) |
| 活跃度 | 小规模活跃 |

**工作原理**：
- TypeScript 库，直接读取浏览器本地 cookie 数据库文件
- 使用 OS 凭证存储解密加密的 cookie（macOS security、Windows DPAPI、Linux keyring）
- 附带 Chrome MV3 扩展用于导出 cookie
- 零网络传输，完全本地操作

**支持浏览器**：Chrome/Chromium、Edge、Firefox、Safari (macOS)

**安全评估**：
- [x] 开源可审计
- [x] 完全本地运行，零网络操作
- [ ] **Stars < 200，未经大规模社区验证** ⚠️
- **适用场景**：提取特定网站 cookie 给 agent 用于 HTTP 请求，不控制浏览器

---

## 云端方案（了解即可，安全风险更高）

### 9. Browserbase

| 项目 | 信息 |
|------|------|
| URL | https://browserbase.com |
| MCP Server | https://github.com/browserbase/mcp-server-browserbase (~824 stars) |
| 许可证 | MCP Server: Apache 2.0；平台本身闭源 |

- 云端浏览器即服务，B 轮融资 $40M
- Contexts API 跨 session 持久化 cookie
- **Cookie 数据在云端** — 必须信任 Browserbase 的安全措施
- 适合企业级大规模部署，不适合个人敏感场景

### 10. Steel Browser

| 项目 | 信息 |
|------|------|
| URL | https://github.com/steel-dev/steel-browser |
| Stars | 6.7k |
| 许可证 | Apache 2.0 |

- 开源浏览器 sandbox，可自部署
- 跨请求保持 cookie/localStorage
- 支持 Docker 自部署 — **自部署时 cookie 不外泄**
- 支持 Puppeteer/Playwright/Selenium 连接

---

## 综合对比

| 工具 | Stars | 方案类型 | Cookie 安全 | 权限控制 | Claude Code 集成 | 推荐度 |
|------|-------|---------|------------|---------|-----------------|--------|
| Chrome DevTools MCP | 32.1k | 连接真实浏览器 | 本地 | 无 | MCP 原生 | ★★★★★ |
| Playwright MCP | 29.9k | Profile 复用 | 本地 | 有（host白名单） | MCP 原生 | ★★★★★ |
| agent-browser | 25.6k | Profile 复用 | 本地+可加密 | 无 | CLI/Skill | ★★★★ |
| browser-use | 84.9k | Profile 复用 | 本地/云端 | 无 | 需适配 | ★★★★ |
| Playwriter | 3.3k | 连接真实浏览器 | 本地 | 有（tab级） | MCP 原生 | ★★★★ |
| BrowserMCP | 6.2k | 连接真实浏览器 | 本地 | 无 | MCP 原生 | ★★★ |
| chrome-cdp-skill | 2.7k | 连接真实浏览器 | 本地 | Chrome弹窗 | 需适配 | ★★★ |
| sweet-cookie | 143 | Cookie 提取 | 本地 | N/A | 需编码 | ★★ |
| Steel | 6.7k | 自部署沙箱 | 自部署安全 | 无 | 需适配 | ★★★ |
| Browserbase | ~824(MCP) | 云端 | ⚠️ 云端 | 有 | MCP | ★★ |

---

## 安全红线总结

### 必须警惕的风险

1. **autoConnect/远程调试端口** — 开放 9222 端口意味着本机任何程序都能访问你的浏览器。用完必须关。
2. **Cloud 方案的 cookie 外泄** — Browserbase、browser-use Cloud 模式都会让你的 session 到第三方服务器。除非有企业合规保障，个人敏感账号不要用。
3. **MCP 生态的供应链风险** — CVE-2025-6514（mcp-remote 命令注入）已证明 MCP 生态存在真实攻击面。只用大厂维护的 MCP server。
4. **Session 文件明文存储** — agent-browser 等工具的 session 文件默认明文。必须加密 + .gitignore。
5. **无细粒度网站限制** — 大多数工具连接后就是全部权限，没有"只允许访问 twitter.com"这种控制。Playwright MCP 的 `--allowed-hosts` 是目前最接近的方案。

### 安全使用原则

1. **只用开源可审计的工具**（上面列的都是开源的）
2. **只用本地方案**，除非有明确理由用云端
3. **用独立 profile**，不要让 agent 碰你的主浏览器 profile
4. **用完关端口**，调试端口不要长期开着
5. **Stars < 500 的工具要逐行审计代码**再用

---

## 我的推荐：Claude Code 最佳实践路径

### 场景1：需要访问已登录的网站（最常见）

**首选：Playwright MCP + user-data-dir**

```bash
# 1. 创建专用调试 profile
mkdir -p ~/.claude-browser-profile

# 2. 用这个 profile 打开 Chrome，手动登录需要的网站
google-chrome --user-data-dir="$HOME/.claude-browser-profile"

# 3. 关闭 Chrome，然后配置 Claude Code
claude mcp add playwright -- npx @playwright/mcp@latest \
  --user-data-dir="$HOME/.claude-browser-profile"
```

优点：Microsoft 官方维护，30k stars，支持多浏览器，有 host 白名单。

### 场景2：需要与当前打开的页面交互

**首选：Chrome DevTools MCP + autoConnect**

```bash
# 1. Chrome 地址栏打开 chrome://inspect/#remote-debugging 启用 autoConnect
# 2. 配置 Claude Code
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

优点：Google 官方维护，32k stars，能看到和操作你正在看的页面。
注意：用完立即关闭 autoConnect。

### 场景3：需要精细控制哪些 tab 可以被访问

**首选：Playwriter**

```bash
# 安装 Chrome 扩展 + 配置 MCP
claude mcp add playwriter -- npx playwriter@latest
```

优点：tab 级别授权，安全模型最好。只有你主动点了扩展图标的 tab 才会被 agent 控制。
