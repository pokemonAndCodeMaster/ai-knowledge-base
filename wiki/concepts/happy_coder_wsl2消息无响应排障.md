---
title: Happy Coder 在 WSL2 中消息无响应排障
domain: ["tooling", "agent_tool_use"]
type: "pitfall"
tags: [Happy Coder, Codex CLI, WSL2, Socket.IO, 代理, 排障]
created: 2026-07-03
updated: 2026-07-03
sources: 3
status: active
related_code: []
affects_path:
  - "/home/yyh/.happy/logs/"
  - "/home/yyh/.happy/settings.json"
  - "/home/yyh/.nvm/versions/node/v22.22.2/lib/node_modules/happy-coder/"
  - "scripts/happy_proxy_preload.cjs"
  - "scripts/happy-proxy"
trigger_keywords: ["Happy Coder 手机无响应", "happy codex", "Socket connection error timeout", "WSL2 Happy", "手机已连接但收不到消息"]
---

# Happy Coder 在 WSL2 中消息无响应排障

## 适用症状

手机端显示机器或会话已连接，但手机发送文字或语音后，WSL2 终端没有收到消息，Codex 也不开始执行。

## 已验证的本机故障边界

2026-06-21 的本机日志表明，Happy 能启动 Codex app-server，故障发生在 Happy CLI/守护进程连接中继服务阶段，而不是 Codex 初始化阶段。

> 引用自本机 `/home/yyh/.happy/logs/2026-06-21-13-56-43-pid-28201.log`：
> `[CodexAppServer] Connected and initialized`
>
> `[MessageQueue2] Waiting for messages...`
>
> `[API] Socket connection error: Error: timeout`

守护进程同时出现相同方向的超时：

> 引用自本机 `/home/yyh/.happy/logs/2026-06-21-13-50-51-pid-24809-daemon.log`：
> `[API MACHINE] Connection error: timeout`

已安装版本为 `happy-coder 1.1.9`、`codex-cli 0.141.0`。已安装 CLI 代码的默认服务端为：

> 引用自本机 Happy Coder 分发代码：
> `this.serverUrl = process.env.HAPPY_SERVER_URL || "https://api.cluster-fluster.com";`

因此，“手机显示连接”只证明手机能够读取云端已有机器/会话状态，不足以证明当前 WSL2 进程与中继的实时双向 Socket 通道正常。

## 最短定位顺序

### 1. 以新日志复现

在普通 WSL2 终端中执行：

```bash
happy doctor
happy codex
```

手机发送一条纯文字消息，然后在另一终端检查最新日志：

```bash
ls -lt ~/.happy/logs | head
tail -f ~/.happy/logs/最新日志文件
```

判断：

- 出现 `User message received`：中继下行已通，继续查 Codex turn/权限。
- 持续出现 `Socket connection error` 或 `Connection error: timeout`：继续查网络与代理。
- 没有新日志：当前手机操作的不是这个 WSL2 会话，或 `happy codex` 已退出。

### 2. 分开验证 HTTPS、直连与真实 WebSocket 路径

CLI 1.1.9 默认连接 `https://api.cluster-fluster.com`；若设置了 `HAPPY_SERVER_URL`，必须改用实际地址。

```bash
printf '%s\n' "${HAPPY_SERVER_URL:-https://api.cluster-fluster.com}"
curl -v --connect-timeout 10 "${HAPPY_SERVER_URL:-https://api.cluster-fluster.com}/"
curl --noproxy '*' -v --connect-timeout 10 "${HAPPY_SERVER_URL:-https://api.cluster-fluster.com}/"

curl --http1.1 -v --connect-timeout 10 \
  -H 'Connection: Upgrade' \
  -H 'Upgrade: websocket' \
  -H 'Sec-WebSocket-Version: 13' \
  -H 'Sec-WebSocket-Key: SGVsbG9Xb3JsZDEyMzQ1Ng==' \
  "${HAPPY_SERVER_URL:-https://api.cluster-fluster.com}/v1/updates/?EIO=4&transport=websocket"
```

判断：第一条验证当前环境（可能经代理）的 HTTPS；第二条强制绕过代理，验证 Happy WebSocket 所需的直连是否可用；第三条使用 Happy 1.1.9 的真实 Socket.IO 路径并请求 WebSocket 升级。DNS、TCP、TLS 任一阶段超时都属于 WSL2 出站链路问题。HTTP 首页可达不等于 WebSocket/Socket.IO 可用。

不要用通用 `/socket.io/?EIO=4&transport=polling` 判断 Happy 1.1.9：该版本明确配置 `path: "/v1/updates"` 且 `transports: ["websocket"]`，所以通用路径返回 404 是预期结果。

### 3. 核对 WSL2 代理

```bash
env | grep -i proxy
getent hosts api.cluster-fluster.com
```

常见根因是 `curl`、Axios 等 HTTP 客户端使用了 `HTTP_PROXY`/`HTTPS_PROXY`，但 Socket.IO 的 Node WebSocket 没有自动使用这些环境变量。此时 HTTP 探针经代理成功，Happy 仍直接建 TCP/WebSocket 并超时。Happy Coder 1.1.9 的已安装分发代码中没有发现 `https-proxy-agent`、`proxy-agent` 或等价的 WebSocket 代理注入。

用强制直连探针确认：

```bash
curl --noproxy '*' -v --connect-timeout 10 https://api.cluster-fluster.com/
```

如果经代理的 `curl` 成功而强制直连超时，优先启用 Clash/Mihomo 的 TUN 模式，让未显式支持代理的 Node WebSocket 也经过系统透明代理。另一种临时验证方式是用正确配置的 `proxychains4` 包裹 `happy codex`；确认有效后再选择持久方案。不要把中继域名加入 `NO_PROXY`，这会强制它直连，方向相反。

若强制直连解析到 Clash Fake-IP（如 `198.18.0.0/15`）并成功，且真实 `/v1/updates` 返回 `101 Switching Protocols`，则 TUN、WSL2 出站、TLS、Cloudflare 和 WebSocket Upgrade 均已通过。此时不应继续调整 TUN；应使用 Happy 自带的 `socket.io-client` 做最小连接测试，把故障继续二分为“Node Socket.IO 传输兼容”与“Happy 凭证/会话认证”。

```bash
node <<'NODE'
const { io } = require('/home/yyh/.nvm/versions/node/v22.22.2/lib/node_modules/happy-coder/node_modules/socket.io-client');
const socket = io('wss://api.cluster-fluster.com', {
  path: '/v1/updates',
  transports: ['websocket'],
  reconnection: false,
  timeout: 15000,
  auth: {
    token: 'invalid-diagnostic-token',
    clientType: 'session-scoped',
    sessionId: 'invalid-diagnostic-session',
    happyClient: 'diagnostic'
  }
});
socket.on('connect', () => { console.log('UNEXPECTED_CONNECTED'); socket.close(); process.exit(0); });
socket.on('connect_error', (error) => {
  console.error('CONNECT_ERROR:', error.message);
  console.error('TYPE:', error.type || 'n/a');
  process.exit(0);
});
setTimeout(() => { console.error('CLIENT_TIMEOUT'); process.exit(2); }, 20000);
NODE
```

- 快速返回 `Unauthorized`、`Authentication` 或其他明确服务端错误：同一 Node 传输正常，转查真实 Happy 凭证与会话注册，可执行 `happy auth login --force` 重新配对。
- 返回 Socket.IO `timeout` 或最终 `CLIENT_TIMEOUT`：故障位于 Node Socket.IO 传输层，而非 Happy 凭证；再对比 Node 版本或用 `proxychains4` 验证，不要先删除 `~/.happy`。

## 本机最终根因与已验证修复

2026-07-03 在 WSL2 mirrored networking、Clash TUN、Node.js 22.22.2 环境中完成分层对照：

- `curl --noproxy '*'` 解析到 Clash Fake-IP `198.18.1.166`，HTTPS 成功。
- `curl` 对 `/v1/updates` 的 WebSocket Upgrade 返回 `101 Switching Protocols`。
- Node 原生 `tls.connect` 对同一主机超时。
- Happy 自带 `socket.io-client` 不注入代理时返回 `timeout`。
- 为 Socket.IO 显式传入 `HttpsProxyAgent(http://127.0.0.1:7890)` 后，立即收到预期的 `Invalid authentication token`，证明代理后的 Node Socket.IO 链路正常。

最终采用非侵入包装器，不修改全局 npm 包与 `~/.happy` 凭证：

- `scripts/happy_proxy_preload.cjs`：仅对 `api.cluster-fluster.com` 的 `https.request` 强制注入 Happy 依赖树自带的 `HttpsProxyAgent`，避免影响 Codex 的其他 HTTPS 请求。
- `scripts/happy-proxy`：设置 `HAPPY_CODER_ROOT` 与 `NODE_OPTIONS=--require=...` 后执行原版 `happy`。
- `~/.local/bin/happy-proxy`：指向仓库包装器的符号链接。

包装器必须先对 `${BASH_SOURCE[0]}` 执行 `readlink -f`，再计算 `SCRIPT_DIR`。否则从符号链接入口启动时会错误查找 `~/.local/bin/happy_proxy_preload.cjs`。

使用方式：

```bash
happy-proxy codex
```

真实凭证验证日志：

> 引用自 `/home/yyh/.happy/logs/2026-07-03-22-19-25-pid-460027.log`：
> `Socket connected successfully`

> 引用自 `/home/yyh/.happy/logs/2026-07-03-22-19-26-pid-460059-daemon.log`：
> `[API MACHINE] Connected to server`
>
> `[API MACHINE] Keep-alive started (20s interval)`
>
> `[API MACHINE] Daemon state updated successfully`

上游 Happy 或 Node/Clash 修复后，应先用原始 `happy codex` 复测；原始命令不再 timeout 时可删除该 workaround。

### 4. 网络通了再处理状态

网络探针通过但仍无消息时：

1. 执行 `happy doctor`，清理命令以该版本实际输出为准。
2. 完全退出旧的 `happy`/daemon 进程，再启动一个新的 `happy codex` 会话。
3. 确认手机进入的是刚启动的新会话，而非历史会话。
4. 最后才考虑重新配对、升级 Happy Coder，并保留升级前后的日志对比。

不要先删除 `~/.happy/access.key`、`sessions.json` 或整个 `~/.happy`；这会破坏配对证据，但无法修复 Socket 超时。

## 诊断环境边界

2026-07-03 的 Codex 诊断沙箱把 `/home` 以只读方式挂载，因此在该沙箱内执行 `happy` 会额外产生：

> `Error: EROFS: read-only file system, open '/home/yyh/.happy/logs/...'`

这只说明诊断沙箱无法写 Happy 日志，不能证明用户的普通 WSL2 终端也存在只读文件系统故障。复现必须在普通 WSL2 交互终端完成。

## 关系

- Happy 的双向消息依赖“手机应用 ↔ 中继服务 ↔ WSL2 中的 Happy CLI”，任一侧显示在线都不能代替端到端验证。
- 官方架构说明：<https://happy.engineering/docs/how-it-works/>
- 官方网络排障入口：<https://happy.engineering/docs/faq/>
