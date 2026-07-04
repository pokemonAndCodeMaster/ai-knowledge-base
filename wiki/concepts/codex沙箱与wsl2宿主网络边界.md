---
title: Codex 命令沙箱与 WSL2 宿主网络边界
domain: ["tooling", "agent_tool_use", "harness_engineering"]
type: "pitfall"
tags: [Codex CLI, WSL2, mirrored networking, Clash, DNS, Git, Happy Coder, 沙箱]
created: 2026-07-04
updated: 2026-07-04
sources: 6
status: active
related_code:
  - "scripts/happy-proxy"
  - "scripts/happy_proxy_preload.cjs"
affects_path:
  - "/mnt/c/Users/89268/.wslconfig"
  - "/etc/wsl.conf"
  - "/etc/resolv.conf"
  - "/home/yyh/.config/wsl-proxy.sh"
  - "/home/yyh/.bashrc"
  - "/home/yyh/.codex/config.toml"
  - "/home/yyh/.happy/logs/"
  - "scripts/happy-proxy"
  - "scripts/happy_proxy_preload.cjs"
trigger_keywords: ["git push Could not resolve hostname github.com", "Codex EAI_AGAIN", "WSL2 mirrored 网络", "Clash TUN Codex", "Happy Code 网络不能中断", "Codex sandbox network"]
---

# Codex 命令沙箱与 WSL2 宿主网络边界

## 核心结论

Codex 发起的 Shell 命令可能运行在额外隔离层中。沙箱里的 DNS、loopback、netlink、Windows interop、文件系统权限和环境变量，不等同于启动 Codex/Happy Coder 的普通 WSL2 Shell。沙箱里 `git push` 报 DNS 错误，不能单独证明 Windows、Clash TUN 或 WSL2 mirrored networking 故障。

排障必须分别验证：

1. Windows + Clash 网络；
2. 普通 WSL2 Shell；
3. Happy Coder 的 Node/Socket.IO 链路；
4. Codex 命令沙箱。

不得用第 4 层的失败直接修改前 3 层，更不能在 Happy 会话在线时重启 WSL、Clash、daemon 或删除 `~/.happy`。

## 2026-07-04 本机配置快照

Windows 用户配置：

```ini
# /mnt/c/Users/89268/.wslconfig
[wsl2]
networkingMode=mirrored
autoProxy=false
dnsTunneling=true
firewall=true
```

WSL 内部配置：

```ini
# /etc/wsl.conf
[user]
default=yyh

[boot]
systemd=true

[network]
generateResolvConf = false
```

```text
# /etc/resolv.conf
nameserver 223.5.5.5
nameserver 114.114.114.114
nameserver 8.8.8.8
```

这里存在配置叠加：Windows 侧启用了 `dnsTunneling=true`，但 Linux 侧关闭自动生成 `resolv.conf` 并固定公共 DNS。静态文件绕开了 WSL 自动提供的 DNS 入口，因此不能仅凭 `.wslconfig` 宣称 DNS tunneling 已在 Linux 内实际生效。调整该处需要 `wsl --shutdown`，会中断当前 Happy/Codex 会话，本次不做在线修改。

## Shell 显式代理策略

`~/.bashrc` 加载 `/home/yyh/.config/wsl-proxy.sh`。脚本策略是：

1. mirrored 模式优先探测 `127.0.0.1:7890`；
2. 失败时尝试 NAT 默认网关；
3. 探测成功才导出大小写两套 HTTP(S)/ALL_PROXY；
4. 均失败则清空代理变量，避免留下不可用代理。

Clash TUN 与显式代理是两条不同路径。TUN 可透明接管普通流量；`HTTP_PROXY`/`HTTPS_PROXY` 只对主动读取变量的客户端有效。Node WebSocket 不保证自动使用这些变量。

## Happy Coder 当前链路

Happy Coder 1.1.9 的 Node Socket.IO 在本机曾出现：curl/TUN 可达，但 Node 原生 TLS 超时。当前使用：

- `scripts/happy_proxy_preload.cjs`：只对 `api.cluster-fluster.com` 注入 `HttpsProxyAgent`；
- `scripts/happy-proxy`：通过 `NODE_OPTIONS=--require=...` 启动原始 Happy；
- `~/.local/bin/happy-proxy`：指向仓库包装器。

2026-07-04 当前会话日志证据：

```text
/home/yyh/.happy/logs/2026-07-04-09-39-51-pid-478033.log
[09:39:54.447] Socket connected successfully
```

daemon 日志仍持续记录 `Connected to server` 与 keep-alive。完整根因和包装器说明见 [[happy_coder_wsl2消息无响应排障]]。

## Codex 沙箱的实测边界

当前 Happy Code 会话中的 Codex 命令环境为受管 `workspace-write`，网络标记为 restricted。2026-07-04 实测：

```text
git push origin master
ssh: Could not resolve hostname github.com: Temporary failure in name resolution
```

```text
fetch-codex-manual.mjs
getaddrinfo EAI_AGAIN developers.openai.com
```

同一环境还出现：

```text
ip address
Cannot open netlink socket: Operation not permitted
```

```text
powershell.exe ...
WSL ERROR: UtilBindVsockAnyPort:307: socket failed 1
```

此外，沙箱内 `/home` 为只读、看不到宿主 Happy 进程、无法访问宿主 `127.0.0.1:7890`。但沙箱外的 Happy 日志在同一时段持续追加并保持 Socket 在线。这组对照证明本次 Git DNS 失败发生在 Codex 命令隔离层，不能归因于 Git remote、SSH key、Clash TUN 或 mirrored networking。

## 2026-07-04 三层网络对照与 NotebookLM MCP 修复

新鲜对照进一步把“Codex 工具网络”拆成两类：

1. **Shell 工具沙箱**：当前 VS Code Codex 会话包含 `CODEX_SANDBOX_NETWORK_DISABLED=1`；沙箱内 `/proc/net/route` 为空、看不到宿主路由，也无法连接 `127.0.0.1:7890`。GitHub、NotebookLM、netlink 的失败都发生在这一层。
2. **MCP 子进程**：NotebookLM MCP 与其父 `codex app-server` 位于普通 WSL 的网络命名空间，不受 Shell 工具网络命名空间隔离；但进程启动时没有继承任何大小写形式的代理变量。
3. **普通 WSL 登录 Shell**：加载 `~/.config/wsl-proxy.sh` 后使用 `127.0.0.1:7890`。同一时刻访问 GitHub 返回 200，访问 NotebookLM 返回登录重定向；带认证的新 `NotebookLMClient` 在 2.3 秒内列出 19 个笔记本，并识别 `quality_check`（ID `6b4b949e-d423-4033-b16f-bd037ac03fa8`）。

因此有两个独立根因：

- Git/普通 Shell 命令无法联网，是 Codex Shell 沙箱禁网；修改 WSL、DNS 或 Clash 不能修复它。
- NotebookLM MCP 超时，是 stdio MCP 启动环境未继承登录 Shell 代理；认证和 RPC 本身已在宿主网络验证正常。

NotebookLM MCP 采用最小范围修复：只在 `~/.codex/config.toml` 的 `mcp_servers.notebooklm.env` 中注入 `HTTP_PROXY`、`HTTPS_PROXY` 及小写等价值，均指向 `http://127.0.0.1:7890`。配置变更只对新启动的 MCP 进程生效；已有 Codex 会话需要重启或重新加载 MCP。不要把代理变量全局硬编码到 MCP 实现源码。

## APT、sudo 与 Clash Fake-IP 半通状态

2026-07-04 新鲜对照显示，WSL 并非所有出站路径都正常：

- 经显式 `HTTPS_PROXY=http://127.0.0.1:7890` 请求清华 Ubuntu 镜像成功；
- `curl --noproxy '*'` 请求同一 HTTPS 文件 15 秒超时；
- DNS 返回 Clash Fake-IP `198.18.0.17`，说明 DNS 劫持生效，但 WSL 发往 Fake-IP 的直连 TLS 没有被 TUN 正确接管；
- `sudo apt` 默认清理普通用户的代理环境，APT 又没有持久化 `Acquire::*::Proxy`，因此它停在 `Connected to ... (198.18.0.17)`。

这是一种“显式代理可用、TUN 透明直连失效”的半通状态。APT 可先使用命令行 `Acquire::http::Proxy` / `Acquire::https::Proxy` 显式指向 `127.0.0.1:7890`；SSH、原生 Node TLS 等不自动读取 HTTP 代理的客户端仍需独立代理或修复 TUN。不要用普通 curl 经代理成功推断 TUN 已恢复。

### 当前配置根因与主修复路线

Windows 侧当前合并配置为 `tun.enable=true`、`stack=gvisor`、`auto-route=true`、`enhanced-mode=fake-ip`，Fake-IP 网段为 `198.18.0.1/16`。Windows Meta 网卡存在默认路由，但 WSL 对 Fake-IP 的直连 HTTPS 超时，属于 TUN 数据面半故障，不是 Fake-IP 地址本身异常。

主修复按以下顺序进行：

1. Clash Verge Rev 将 TUN stack 从 `gvisor` 改为 Mihomo 官方推荐的 `mixed`；保持 `auto-route=true`，先不启用 `strict-route`。
2. Windows 防火墙放行 Mihomo/Clash core；官方文档说明防火墙开启时 `mixed/system` 栈需要放行内核。
3. `.wslconfig` 保留 `networkingMode=mirrored`、`dnsTunneling=true`、`firewall=true`，把 `autoProxy` 改为 `true`。
4. `/etc/wsl.conf` 恢复 `generateResolvConf=true`（或移除关闭项），删除旧的手工 `/etc/resolv.conf` 后由 WSL 重建，使 DNS tunneling 真正生效。
5. 执行 `wsl --shutdown` 后重启发行版，分别验证显式代理、强制直连 HTTPS、`sudo apt update`、GitHub SSH 和 Happy Socket。

完成门槛不是“代理 curl 成功”，而是 `curl --noproxy '*'` 的 HTTPS、无需 APT 代理的 `sudo apt update`、以及 GitHub SSH 都成功。失败时优先回滚 WSL DNS 文件和 TUN stack；不直接改用全局 `danger-full-access` 掩盖网络故障。

## 安全操作顺序

## Happy Codex 启动权限模型

本机 `happy-coder 1.1.9` 有两层权限控制，不能混为一谈：

1. **Happy OS sandbox**：由 `happy sandbox configure/status/disable` 管理，配置保存在 `~/.happy/settings.json`；控制文件范围、网络和本地端口绑定。
2. **Codex sandbox + approval policy**：Happy 根据会话的 `permissionMode` 映射后，通过 app-server 协议传给 Codex。

本机 2026-07-04 的 `~/.happy/settings.json` 没有 `sandboxConfig`，因此当前会话没有 Happy 外层 sandbox；限制来自默认 permission mode 映射出的 Codex `workspace-write`。

### Happy permission mode 映射

以下是已安装 Happy 1.1.9 的 `resolveCodexExecutionPolicy()` 实际映射：

| `--permission-mode` | Codex approval policy | Codex sandbox | 含义 |
|---|---|---|---|
| `default` | `untrusted` | `workspace-write` | 工作区可写；非可信命令申请批准；网络仍受 sandbox 限制 |
| `read-only` | `never` | `read-only` | 只读且不申请放权，适合审阅 |
| `acceptEdits` | `on-request` | `workspace-write` | 可编辑工作区，由模型按需申请额外权限 |
| `safe-yolo` | `on-failure` | `workspace-write` | 工作区内自动执行，失败后才申请；不能解决 workspace sandbox 的网络隔离 |
| `yolo` | `on-failure` | `danger-full-access` | 完整宿主权限，能直接联网和访问工作区外文件，风险最高 |
| `bypassPermissions` | `on-failure` | `danger-full-access` | 兼容 Claude 模式，效果接近 `yolo` |
| `plan` | `untrusted` | `workspace-write` | 保守审批，但 Happy 代码仍映射为工作区可写，不应把名称理解为 OS 级只读 |

若启用了 Happy OS sandbox，Happy 会把内层 Codex 固定为 `approvalPolicy=never + danger-full-access`，因为真正的边界已由外层 Happy sandbox 接管。此时看见 Codex `danger-full-access` 不代表宿主裸奔，必须同时查看 Happy sandbox 状态。

### 推荐启动方式

长期远程开发推荐先在普通 WSL 终端交互配置一次：

```bash
happy sandbox configure
```

选择：

- file scope：`per-project`；
- network：`allowed`；
- localhost binding：只有需要启动开发服务器时才开启。

确认状态：

```bash
happy sandbox status
```

之后从仓库目录启动：

```bash
cd /home/yyh/project/ai-knowledge-base
happy-proxy codex
```

这套组合让 Happy 外层 sandbox 限制到当前项目，同时允许 GitHub 网络；Happy 会让内层 Codex 自由执行，但不能越过外层文件边界。

临时、一次性需要完整 WSL 权限时可用：

```bash
happy-proxy codex --permission-mode yolo
```

这会把 Codex 映射为 `danger-full-access`。远程手机误操作、恶意仓库指令和依赖脚本都可访问 SSH 凭证、其他项目与系统文件，不建议作为默认启动命令。

`--no-sandbox` 只关闭 Happy 外层 sandbox；若会话仍是 `default`，Codex 仍会使用 `workspace-write`，因此它单独不能解决当前 GitHub socket 被禁止的问题。

### 与原生 Codex CLI 参数的区别

直接运行 `codex` 时，本机 0.141.0 支持：

```text
--sandbox read-only|workspace-write|danger-full-access
--ask-for-approval untrusted|on-failure|on-request|never
--dangerously-bypass-approvals-and-sandbox
--add-dir <DIR>
--config <key=value>
```

但 `happy codex` 使用 app-server 协议和自己的 permission mode 映射，不应假设所有原生 Codex CLI 参数都会原样透传。Happy 侧应优先使用 `--permission-mode`、`happy sandbox ...` 与 `--no-sandbox`。

## VS Code Codex 与 Happy Codex 的联网启用步骤

### VS Code Codex：保留工作区沙箱并开启网络（推荐）

CLI 与 IDE 共用 Codex 配置。在 `~/.codex/config.toml`（全局）或可信仓库的 `.codex/config.toml`（项目级）加入：

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = true
```

保存后新建 Codex thread；必要时执行 **Developer: Reload Window**。旧 thread 不保证热加载 sandbox policy。用新 thread 验证 `CODEX_SANDBOX_NETWORK_DISABLED`、GitHub HTTPS 和 NotebookLM；项目配置只有在仓库被信任时加载。

VS Code 界面的一次性全权限方式是把输入框下方权限选择器切到 **Agent (Full Access)**。它会解除网络和文件沙箱，风险显著高于上述配置；仅用于完全信任的仓库与短时任务，完成后切回 Agent/Auto。

### Happy Codex：外层项目沙箱允许网络（推荐）

Happy 1.1.9 当前尚未配置外层 sandbox。先在普通 WSL 终端运行：

```bash
happy sandbox configure
```

交互选择：file scope 为 `per-project`，network 为 `allowed`；只有确实要启动本地服务时才允许 localhost binding。随后检查：

```bash
happy sandbox status
```

Happy 1.1.9 的真实首屏问题是 `How should file access be scoped?`，默认高亮 `workspace - Full workspace root directory`；必须按下方向键选择第二项 `per-project - Only current project directory`。选择后配置落盘为 `sessionIsolation: "strict"`，不会再显示 `Workspace root`。当前本机仍是 `Scope: workspace`、`Workspace root: ~/Workspace`，说明此前保存的是默认第一项，不是 per-project。

结束旧 Happy Codex session，新开会话：

```bash
happy daemon list
happy daemon stop-session <happySessionId>

cd /home/yyh/project/ai-knowledge-base
happy-proxy codex
```

`happy daemon stop` 只停止 daemon，文案明确说明既有 sessions 仍存活，因此不能用它代替 `stop-session`。前台手工启动的 session 可在对应终端按 `Ctrl+C`。Happy 1.1.9 的 `happy codex --help` 会意外实际启动一个 session，不要用它查看帮助；若误启动，使用 `happy daemon list` 找到对应 ID 后执行 `stop-session`。

启用 Happy 外层 sandbox 后，Happy 会让内层 Codex 使用 `danger-full-access`，但权限仍被外层 per-project/network policy 约束。这与裸 `yolo` 不同。

必须验证外层 sandbox **确实初始化成功**。若缺少 `bubblewrap` 或 `socat`，Happy 1.1.9 会记录 `Failed to initialize sandbox; continuing without`，随后把手机默认权限重新映射为内层 Codex `workspace-write`。Happy 的显式 thread policy 会使 Git 再次进入禁网沙箱，即使 `~/.codex/config.toml` 已设置 `sandbox_workspace_write.network_access = true`。因此“Happy status 显示 network allowed”不是完成证据；日志必须出现 `Sandbox enabled` 且不再出现初始化失败。

默认配置还包含 `denyReadPaths: ["~/.ssh", "~/.aws", "~/.gnupg"]`。因此 network allowed 只证明可以访问 GitHub，不代表 SSH `git push` 能读取私钥。安全默认是让 Happy 负责修改和提交、用户在普通终端 push；若明确要求 Agent push，必须另外授权凭据通道，并接受远程 Agent 可使用对应凭据的风险。

### Happy 中启用 Git SSH

快捷方案是从 `sandboxConfig.denyReadPaths` 移除 `~/.ssh`，但不要把 `~/.ssh` 加入 `extraWritePaths`。这样 Agent 能读取全部 SSH 私钥和已有 `known_hosts`，却不能改写 SSH 目录；适合用户明确接受该信任边界的场景。配置只对新 session 生效。

更安全的长期方案是为单个 GitHub 仓库创建具有写权限的 deploy key，把私钥放到不属于 `~/.ssh` deny 区的专用凭据目录，并用仓库级 `core.sshCommand` 指定该密钥。即使密钥泄露，权限也只覆盖一个仓库；优于向远程 Agent 暴露个人主 SSH key。

短时应急可用：

```bash
happy-proxy codex --permission-mode yolo
```

此方式没有项目级外层边界，可读取 SSH 凭据和其他项目；不作为默认启动方式。`safe-yolo` 仍映射为 `workspace-write`，不能解除网络隔离；单独使用 `--no-sandbox` 也不能解除内层 Codex 的默认 sandbox。

## 为什么 VS Code Codex 控制 WSL 时限制不同

VS Code Remote WSL 插件宿主直接运行在该 WSL 实例内，并从 VS Code/Codex 插件自己的信任、审批和 sandbox 配置启动命令。它不经过 Happy 1.1.9 的 app-server permission mode 映射，也没有 Happy OS sandbox 这一层。

因此两边即使使用同一套 `~/.codex/config.toml` 和同一个仓库，最终策略仍可能不同：

- VS Code 界面可能允许用户即时批准联网或宿主命令；
- Happy 远程会话的 `default` 固定映射为 `untrusted + workspace-write`；
- VS Code 进程通常继承普通 WSL 的 DNS、loopback、Windows interop 和代理环境；
- Happy/Codex sandbox 会主动隔离这些能力。

判断实际权限应看每个会话启动时的最终策略和新鲜探针，不能用“VS Code 中可推送”推断 Happy 中也可推送。

### 当前 Happy 会话在线时

只允许无中断操作：读取配置与日志、运行沙箱探针、编辑仓库文件。禁止：

- `wsl --shutdown`；
- 重启 Clash/TUN；
- 重启或 kill Happy daemon；
- 删除 `~/.happy` 状态；
- 在线替换 `/etc/resolv.conf`；
- 为绕过限制使用全局 `danger-full-access`。

### 推送仓库

首选在普通 WSL2 终端执行并验证：

```bash
getent hosts github.com
ssh -T -o ConnectTimeout=10 git@github.com
git push origin master
```

若普通终端成功而 Codex 失败，网络无需修复；这是沙箱策略差异。若希望 Codex 自行推送，应在新会话启动前显式选择允许网络且最小授权的策略，并保留人工审批。当前受管会话无法在仓库内或运行中提升网络权限。

### 宿主 DNS 的后续清理

仅在可以中断 WSL 会话的维护窗口处理 `.wslconfig` 与 `/etc/wsl.conf` 的 DNS 策略冲突。变更前后分别在普通 WSL 终端验证 GitHub、Happy 中继和 Windows interop；验证失败立即回滚。不要把这项清理当成本次沙箱 Git 推送的修复前置条件。

## 关系

- ✅ 支持：[[happy_coder_wsl2消息无响应排障]] 记录 Happy Socket.IO 的独立代理问题与定向修复。
- ✅ 支持：[[WSL2镜像网络与远程Codex分层验收规范]] 将本卡结论固化为逐层验收清单。
- ✅ 支持：Codex CLI 0.141.0 本地帮助列出 `read-only`、`workspace-write`、`danger-full-access` 沙箱模式及 approval policy；当前会话的受管策略优先于仓库配置。
