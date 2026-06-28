# WSL2 认证与故障降级

## 目录

- 安全原则
- WSL2 调起 Windows Chrome
- 在线认证判断
- 无损 Markdown 下载
- 故障矩阵

## 安全原则

- 浏览器 Cookie 属于敏感凭据。提取或持久化前，要求用户明确授权具体动作和目标路径。
- Chrome 调试端口必须是 `127.0.0.1:9222`；禁止绑定 `0.0.0.0`。
- 使用独立临时 profile，避免碰用户日常 Chrome profile。
- 日志只输出 Cookie 数量、更新时间和在线验证布尔值；不输出名称对应的值。
- 认证文件写到 `~/.notebooklm-mcp/auth.json`，权限 `0600`。
- 完成后通过 CDP `Browser.close` 关闭临时浏览器。

## WSL2 调起 Windows Chrome

先检测 Windows Chrome：

```bash
test -f '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'
```

在获得用户授权后，从 WSL 调用 Windows PowerShell：

```powershell
$profile = Join-Path $env:TEMP "notebooklm-codex-auth"
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  -ArgumentList @(
    "--remote-debugging-port=9222",
    "--remote-debugging-address=127.0.0.1",
    "--remote-allow-origins=http://127.0.0.1:9222",
    "--user-data-dir=$profile",
    "--no-first-run",
    "--no-default-browser-check",
    "https://notebooklm.google.com/"
  )
```

从 WSL 验证：

```bash
curl -fsS http://127.0.0.1:9222/json/version
curl -fsS http://127.0.0.1:9222/json/list
```

必须等待页面从 `accounts.google.com` 进入 `https://notebooklm.google.com/` 后再读取会话。

## 在线认证判断

`auth_status` 常见误区：它只检查文件存在、Cookie 数量和更新时间，不访问 NotebookLM。

可靠判断：

1. 使用 Cookie 请求 `https://notebooklm.google.com/`。
2. 页面不能重定向到 `accounts.google.com`。
3. 页面应包含当前请求上下文，如 `SNlM0e`（CSRF）和 `FdrFJe`（session）。
4. 再执行 notebook list/get。

如果认证刚刷新但 MCP 仍超时，通常是长驻进程缓存了旧 client；重启 MCP/会话或创建新 client。

## 无损 Markdown 下载

### 为什么内容 RPC 不够

`source_get_content` 的常见实现会寻找文本叶节点、排序后直接 `join("")`。它适合语义读取，却会丢掉 Markdown 的结构性空白、Frontmatter 分隔线、列表和表格布局。

### 为什么 WSL HTTP 直下会 403

`contribution.usercontent.google.com/download` 可能要求浏览器上下文。即便携带 Google Cookie，WSL 的 axios/curl 仍可能得到 403。

### 浏览器下载事件

使用已登录 Chrome：

1. `Browser.setDownloadBehavior(behavior="allow", eventsEnabled=true)`。
2. `Target.createTarget(url=<原始下载URL>)`。
3. 记录 `Browser.downloadWillBegin.suggestedFilename`。
4. 等待 `Browser.downloadProgress.state == "completed"`。
5. 校验 `receivedBytes == totalBytes == stat(file).size`。
6. 读取文件原始字节并计算 SHA-256，不经过文本重写。

## 故障矩阵

| 现象 | 原因 | 处理 |
|---|---|---|
| `auth_status ok`，但 notebook list 超时 | 认证文件存在但在线会话已过期 | 请求首页检查是否跳登录页；重新认证 |
| notebook list 返回空数组 | 私有 RPC 参数/解析器过时，或后端返回错误 envelope | 检查原始响应；刷新 `SNlM0e`、`FdrFJe` 和 build label |
| RPC 错误码 16 | 请求上下文或 RPC payload 不匹配 | 对照新客户端；列表参数可能从旧 `[null,2]` 变为 `[null,1,null,[2]]` |
| 登录窗口“已打开”但 Windows 看不到 | 启动的是 WSL Chromium，`DISPLAY` 不等于 Windows 桌面 | 用 `powershell.exe` 调起 Windows Chrome |
| Windows Chrome 调试端口不可达 | 绑定地址/WSL 网络转发不正确 | 只绑定 127.0.0.1；先测 `/json/version`，不要改成 0.0.0.0 |
| 内容 RPC 有文字但 Markdown 乱了 | 文本叶节点拼接压扁结构 | 改用原始 `.md` 浏览器下载 |
| 原始 URL 用 curl/axios 403 | 下载端点要求浏览器上下文 | 用已登录 Chrome 的下载事件 |
| 38 个 source 只有 36 个唯一 hash | NotebookLM 内有重复 source | raw 全保留；知识层按 hash 合并并记录多个 source ID |
| 编译仍显示全库断链 | 可能是历史存量，不一定来自本轮 | 按路径过滤本轮范围，分别报告全局和新增范围 |
| 上游 source 引用当前仓库不存在的代码 | 来源项目与当前仓库边界不同 | 原路径放元数据快照；有效 `related_code` 留空并注明范围 |
