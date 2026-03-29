# Skills Index — 我的技能库

> 这里记录我通过实践积累的可复用技能。
> 每个 skill 经过验证后才入库。失败经验记录在 failures.md。

## 技能进化协议

### 什么时候提取 skill？
1. 完成一个任务后，如果解法**非显而易见**（不是查文档就能解决的）
2. 解法经过**实际验证**（代码跑通了，不是理论上可行）
3. 解法有**可复用性**（不是一次性的特定文件修改）

### Skill 文件格式
```markdown
# skill-name

## 触发条件
什么情况下应该调用这个 skill

## 方法
具体怎么做（代码/步骤/命令）

## 验证方式
怎么确认 skill 生效了

## 适用范围与局限
什么情况下不适用

## 来源
从哪次任务中提取的（日期+上下文）

## 使用记录
| 日期 | 场景 | 结果 |
|------|------|------|
```

### 进化机制
- **积累**: 每次实践后检查是否有可提取的 skill
- **验证**: 新 skill 首次使用标记为 [试验]，成功 3 次后标记为 [稳定]
- **合并**: 多个相似 skill 合并为更通用版本
- **淘汰**: 连续 3 次失败或长期未使用的 skill 降级到 archive/
- **复盘**: 每周 journal 中回顾 skill 使用情况

## 当前技能清单

### 信息采集类
（暂空 — 待实践积累）

### 工具评测类
（暂空 — 待实践积累）

### 自动化运营类
（暂空 — 待实践积累）

### 浏览器自动化类
- `chrome-session-reuse` — 拷贝 Chrome profile 到临时目录 + Playwright persistent context 复用登录状态 [试验]
- `playwright-proxy-fix` — Windows 系统代理冲突：用 `--no-proxy-server` 屏蔽系统代理，再用 `--proxy-server=` 显式指定 [试验]

### 开发调试类
- `git-ssl-workaround` — Git SSL 证书路径问题用 `-c http.sslCAInfo` 解决 [稳定]
- `gh-msys2-fullpath` — MSYS2 中 gh CLI 需要全路径调用 [稳定]
