# Failures Log — 失败经验库

> 知道什么不行，比知道什么行更稀缺。
> 每次有意义的失败都记录在这里。无聊的 typo 不算。

## 格式

```markdown
### [日期] 简短描述
- **尝试做什么**:
- **实际发生了什么**:
- **根因**:
- **教训**:
- **避免方式**:
```

## 记录

### [2026-03-29] Playwright + Chrome 系统代理冲突
- **尝试做什么**: 用 Playwright 复用 Chrome User Data 访问网页
- **实际发生了什么**: 三次超时/连接失败。`ERR_PROXY_CONNECTION_FAILED` 出现在即使不指定 proxy 参数的情况下
- **根因**: Windows 系统代理设置（端口 15796）被 Chrome 自动继承，即使 Playwright 的 proxy 参数指定了不同端口（7890），Chrome 仍优先走系统代理。两个代理配置互相冲突
- **教训**: Chrome 继承系统代理，Playwright 的 `proxy` 参数不一定能覆盖。必须用 `--no-proxy-server` 先屏蔽系统代理，再通过 `--proxy-server=` 或 Playwright proxy 参数显式指定
- **避免方式**: 国内站用 `--no-proxy-server` 直连；国外站用 `--proxy-server=http://127.0.0.1:15796`。永远不要假设代理端口，先确认实际端口

### [2026-03-29] Chrome 默认 User Data 不允许远程调试
- **尝试做什么**: `launch_persistent_context(user_data_dir=Chrome默认路径)`
- **实际发生了什么**: `DevTools remote debugging requires a non-default data directory`
- **根因**: Chrome 禁止在默认 User Data 目录上启用远程调试（Playwright 需要）
- **教训**: 必须拷贝 profile 到临时目录再用
- **避免方式**: 用 `tempfile.mkdtemp()` 创建副本，只拷贝关键文件（Cookies/Login Data/Preferences/Local State），跳过 GB 级缓存
