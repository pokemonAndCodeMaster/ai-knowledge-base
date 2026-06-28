---
name: notebooklm-source-ingest
description: 无损导出 NotebookLM 笔记本全部 source 并摄入本仓库 Markdown 知识库。用于用户要求“拉取所有 source”“完整原文一点不能少”“保留 Markdown 格式”“从 WSL2 连接 Windows NotebookLM 登录态”“批量摄入、索引、双链和完整性校验”时；覆盖 MCP/CLI 失效、认证过期、内容 RPC 压扁 Markdown、usercontent 403 等降级路径。
---

# NotebookLM 完整来源摄入

把“能读到内容”和“无损拿到原文件”分开处理。用户要求完整 Markdown 时，以 NotebookLM 原始下载文件为事实源；内容 RPC 只用于检索或交叉检查。

## 必读边界

- 先读取仓库 `AGENTS.md`、`skills/ai-librarian/SKILL.md`、`schema.md`、`TAXONOMY.yaml`。
- 操作认证、WSL2 或 Windows Chrome 前读取 [WSL2 认证与故障降级](references/wsl2-auth-and-failures.md)。
- 不输出 Cookie、CSRF token 或浏览器会话内容。
- 提取浏览器 Cookie 前必须取得用户明确授权；调试端口只绑定 `127.0.0.1`，完成后关闭临时浏览器。
- 冻结 source 清单后再导出；没有“基线数 = 成功数 = 本地文件数”就不得声明完整。

## 工作流

### 1. 检索现有知识

运行：

```bash
python scripts/query_graph.py "<笔记本名> NotebookLM source 完整导出 Markdown 摄入"
```

读取命中的 NotebookLM 卡片、既有来源卡和目标业务 Hub，确定复用与更新范围。

### 2. 验证在线认证

依次判断：

1. `auth_status` 只能证明认证文件存在，不能证明会话在线有效。
2. 调用 `notebook_list`；若超时或为空，使用新客户端访问 NotebookLM 首页验证。
3. 首页若跳转 `accounts.google.com`，会话已过期。
4. WSL2 中不要假设 `DISPLAY=:0` 会在 Windows 桌面显示窗口；按 reference 从 WSL 调起 Windows Chrome。

认证恢复后重新初始化 MCP/客户端。长驻 MCP 进程可能缓存旧 Cookie，必要时重启 MCP 或 Codex 会话。

### 3. 精确定位笔记本并冻结基线

- 用规范化标题匹配：忽略大小写、空格、下划线和连字符。
- 记录 notebook ID、标题、source 总数、每个 source ID、标题、类型和原始下载 URL。
- 将 source 总数作为不可变基线；导出期间若数量变化，停止并重新冻结。

### 4. 选择导出通道

| 用户目标 | 使用通道 |
|---|---|
| 查询、总结、语义核对 | `source_get_content` / 内容 RPC |
| 完整 Markdown、保留 YAML/表格/代码块/换行 | 原始 `.md` 下载 URL |
| PDF/网页等无原始 Markdown | 保存原文件；另生成派生 Markdown，清楚标注转换而非原文 |

禁止把内容 RPC 的结果冒充原始 Markdown。其叶节点拼接会压扁 Frontmatter、列表、表格与空行。

### 5. 无损下载与清单

优先让已登录浏览器下载原始文件：

1. 创建隔离的临时下载目录。
2. 用 Chrome DevTools Protocol 设置 `Browser.setDownloadBehavior`。
3. 对每个原始 URL 创建临时 target，等待 `Browser.downloadWillBegin` 和 `Browser.downloadProgress`。
4. 仅在 `state=completed` 且 `receivedBytes == totalBytes == 本地文件字节数` 时记成功。
5. 把原始字节复制到 `raw/notebooklm_exports/<notebook_id>/`，不改写、不加 Frontmatter。
6. 生成 `_MANIFEST.md`，至少记录 index、source ID、文件名、字节数、字符数、行数、SHA-256。

运行完整性检查：

```bash
python skills/notebooklm-source-ingest/scripts/verify_export.py \
  raw/notebooklm_exports/<notebook_id> --expected-count <source总数>
```

重复 source 也要分别保存；用 SHA-256 识别重复，知识卡可合并但来源追踪不能丢。

### 6. Map-Reduce 摄入

按 `ai-librarian` 执行：

1. 长文先运行 `scripts/chunk_raw.py`。
2. 读完全部原文后输出《高保真摄入清单》，注明 source/章节位置。
3. 复用现有卡；新增卡使用合法中文 Frontmatter、合法 domain/type。
4. 参数、SQL、API 请求体、阈值和代码块保留原文快照。
5. 上游代码路径若不在当前仓库存在，不得写入有效 `related_code`；保存在“原始元数据快照”并注明来源范围。
6. NotebookLM 未提供原文但被引用的卡名，不得补写想象内容。创建 `[待人类补充]` 占位或缺失引用索引。
7. 焊接来源总卡 ↔ 正文卡 ↔ Hub/概念卡反链，更新 `index.md`、`log.md`。

### 7. 完成前验证

至少证明：

- NotebookLM 基线数 = Manifest 条目数 = 原始文件数。
- 每个 source ID 唯一且可映射到本地文件。
- 每个文件字节数与 SHA-256 和 Manifest 一致。
- 原始正文与原始 Frontmatter 已完整进入对应知识卡，或明确仅保存在 raw。
- 新卡 domain/type 合法，来源卡与正文卡双向链接。
- 本轮范围断链 0、孤岛 0。
- `compile_graph.py`、`check_staleness.py`、目标查询均执行成功。
- 交付目录不含 Cookie/token。

不要把全库既有断链或 stale 项冒充本轮失败；报告全局存量与本轮范围两个口径。

### 8. 安全收尾

- 关闭临时 Windows Chrome，确认 `127.0.0.1:9222` 不再监听。
- 保留认证文件只在用户授权范围内使用，权限设为 `0600`。
- 不自动删除原始导出、Manifest 或验证报告。

## 完成标准

只有在数量、字节、哈希、知识映射、双链和图谱验证全部有新鲜证据时，才可以说“完整摄入完成”。
