---
title: "WSL2 镜像网络与远程 Codex 分层验收规范"
domain: ["tooling", "agent_tool_use", "harness_engineering"]
type: "norm"
tags: ["WSL2", "Clash", "Mihomo", "TUN", "Codex", "Happy Coder", "sudo", "SSH", "验收"]
created: 2026-07-04
updated: 2026-07-04
sources: 10
status: active
related_code:
  - "scripts/happy-proxy"
  - "scripts/happy_proxy_preload.cjs"
affects_path:
  - "/mnt/c/Users/89268/.wslconfig"
  - "/etc/wsl.conf"
  - "/etc/resolv.conf"
  - "/home/yyh/.config/wsl-proxy.sh"
  - "/home/yyh/.codex/config.toml"
  - "/home/yyh/.happy/settings.json"
  - "/home/yyh/.ssh"
  - "scripts/happy-proxy"
  - "scripts/happy_proxy_preload.cjs"
trigger_keywords: ["WSL网络验收", "Clash mixed", "Happy per-project", "sudo apt Fake-IP", "Happy SSH push", "Codex网络分层"]
---

# WSL2 镜像网络与远程 Codex 分层验收规范

## 目的

本规范用于本机 Windows + Clash Verge Rev + WSL2 mirrored + VS Code Codex + Happy Coder 组合。任何“网络已修好”“Happy 可推送”的声明必须逐层验证，禁止用单个 `curl` 或手机在线状态代替端到端证据。

关联避坑：[[codex沙箱与wsl2宿主网络边界]]、[[happy_coder_wsl2消息无响应排障]]。

## 一、四层故障边界

| 层 | 证明命令 | 典型失败 | 处理方向 |
|---|---|---|---|
| Windows / Clash TUN | `curl --noproxy '*'`、Fake-IP 路由 | Fake-IP 可解析但 TLS 超时 | TUN stack、Windows 防火墙、路由 |
| 普通 WSL Shell | `env`、`sudo apt`、SSH | 普通 curl 成功但 sudo/SSH 失败 | 代理继承与 TUN 分开处理 |
| Codex Shell / MCP | `CODEX_SANDBOX_NETWORK_DISABLED`、MCP 进程环境 | Shell 禁网或 MCP 未继承代理 | Codex sandbox 与 MCP env 分开配置 |
| Happy Coder | Session 日志、sandbox 日志、Git dry-run | Socket 在线但内层 Codex禁网或读不到密钥 | Happy 外层 sandbox、依赖、凭据边界 |

## 二、Clash TUN 完成门槛

本机失败配置为 `enhanced-mode: fake-ip`、`stack: gvisor`。DNS 返回 `198.18.0.17` 属于预期 Fake-IP，但 HTTPS 直连超时；显式代理成功只能证明 `127.0.0.1:7890` 可用。

> 实测失败快照：`curl --noproxy '*' ...` → `Connection timed out after 15002 milliseconds`

将 Clash TUN stack 改为 `mixed` 后，TCP 改走系统栈，直连 TLS 恢复：

> 实测成功快照：`curl --noproxy '*' -I .../noble/InRelease` → `HTTP/2 200`

因此本机稳定基线为：TUN 开启、`stack=mixed`、`auto-route=true`。只要强制直连 HTTPS 未通过，就不得把问题归因于 sudo、Git 凭据或 Codex。

## 三、sudo 与 APT

`sudo` 不拥有独立网络；它与用户进程共用 WSL 网络，但默认 `env_reset` 会清除代理变量。TUN 故障时，普通 curl 因读取 `HTTPS_PROXY` 成功，`sudo apt` 却退回坏掉的 Fake-IP 直连。

临时绕过只用于恢复包管理：

```bash
sudo apt-get \
  -o Acquire::http::Proxy="http://127.0.0.1:7890" \
  -o Acquire::https::Proxy="http://127.0.0.1:7890" \
  update
```

最终验收必须回到 TUN 直连：

```bash
sudo apt-get \
  -o Acquire::http::Proxy="DIRECT" \
  -o Acquire::https::Proxy="DIRECT" \
  update
```

## 四、VS Code Codex 与 NotebookLM MCP

VS Code/CLI 在 `workspace-write` 下需显式开放网络：

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = true
```

新 thread 验收：`CODEX_SANDBOX_NETWORK_DISABLED` 不得为 `1`，GitHub HTTPS 与 `git ls-remote` 必须成功。

stdio MCP 是独立子进程，不保证继承登录 Shell。NotebookLM MCP 必须在 `mcp_servers.notebooklm.env` 中显式设置大小写 `HTTP_PROXY` / `HTTPS_PROXY`，并重启 MCP。认证文件存在不能替代 `notebook_list` 在线验证。

## 五、Happy 外层 sandbox

依赖必须全部存在：

```bash
command -v rg bwrap socat
```

`happy sandbox configure` 的第一项默认是 workspace；per-project 是第二项。终端方向键不可用时，直接把 `~/.happy/settings.json` 配置为：

```json
{
  "enabled": true,
  "sessionIsolation": "strict",
  "networkMode": "allowed",
  "allowLocalBinding": false
}
```

这是字段片段，不得覆盖同文件的 `machineId` 等其他内容。状态必须满足：

```text
Enabled: yes
Scope: per-project
Network mode: allowed
```

重启 session 后，日志必须同时出现：

> `Sandbox enabled`
>
> `Socket connected successfully`

出现 `Failed to initialize sandbox; continuing without` 时，Happy 会退回内层 Codex `workspace-write`，网络可能再次被禁；不得继续宣称外层 sandbox 已生效。

Session 生命周期使用：

```bash
happy daemon list
happy daemon stop-session <happySessionId>
```

`happy daemon stop` 不结束已有 session。Happy 1.1.9 的 `happy codex --help` 会误启动真实 session，不得用它查看帮助。

## 六、SSH 凭据授权

`networkMode=allowed` 只解决网络。默认 `denyReadPaths` 包含 `~/.ssh`，SSH push 会因无法读取密钥失败。

若明确接受远程 Agent 可读取个人 SSH 私钥，可从 `denyReadPaths` 移除 `~/.ssh`，但不得把它加入 `extraWritePaths`。更安全的长期方案是使用仅授权当前仓库写权限的 deploy key。

最终验收：

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 -T git@github.com
git ls-remote --exit-code origin HEAD
git push --dry-run origin master
```

GitHub 的 SSH 成功提示可能退出码为 1；以认证文案、`ls-remote` 和 dry-run 为准。

> 最终实测：`git ls-remote` 退出码 0；`git push --dry-run` 输出 `master -> master`；真实 `git push origin master` 退出码 0。

## 七、沙箱副作用检查

Happy 外层 sandbox 启动后，本机仓库根出现 `.bashrc`、`.gitconfig`、`.gitmodules`、`.vscode` 等只读空文件，并导致 Git 报 `.gitmodules: Permission denied`。这些属于运行时副作用候选，当前不得自动提交或删除。

每次启用或调整 sandbox 后必须执行：

```bash
git status --short
find . -maxdepth 1 -type f -size 0 -perm 0444 -print
```

发现新点文件时先记录来源与进程状态，待 session 结束后确认是否自动消失；未获用户授权不得清理。

## 八、完成检查表

- [ ] `curl --noproxy '*'` 的 HTTPS 返回成功。
- [ ] `sudo apt` 在 DIRECT 模式可更新。
- [ ] VS Code Codex Shell 没有禁网标记。
- [ ] NotebookLM `notebook_list` 返回在线列表。
- [ ] Happy 状态为 per-project + network allowed。
- [ ] Happy 日志有 `Sandbox enabled` 与 `Socket connected successfully`。
- [ ] SSH 认证、`ls-remote`、push dry-run 按授权范围通过。
- [ ] `git status` 中没有误提交 sandbox 产生的点文件。

## 关系

- ✅ 支持：[[codex沙箱与wsl2宿主网络边界]] 提供故障机理与权限映射。
- ✅ 支持：[[happy_coder_wsl2消息无响应排障]] 提供 Socket.IO 与 session 排障证据。
