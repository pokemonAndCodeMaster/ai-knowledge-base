---
title: "NotebookLM 来源无损导出与摄入规范"
domain: ["tooling", "knowledge_mgmt"]
type: "norm"
tags: [NotebookLM, WSL2, Markdown, 无损导出, 完整性校验, 知识摄入]
created: 2026-06-28
updated: 2026-06-28
sources: 3
status: active
related_code: []
affects_path:
  - "skills/notebooklm-source-ingest/**"
  - "tools/notebooklm-mcp/**"
  - "raw/notebooklm_exports/**"
trigger_keywords: [NotebookLM完整导出, 所有source, 原始Markdown, WSL2登录, Cookie过期, source_export_all, 内容不能少]
---

# NotebookLM 来源无损导出与摄入规范

本规范约束 NotebookLM source 从在线笔记本进入本仓库知识图谱的完整链路。执行入口：`skills/notebooklm-source-ingest/SKILL.md`。

## 一、完整性的硬门槛

只有同时满足以下等式才可声明完整：

```text
NotebookLM source 基线数
= Manifest 条目数
= 原始文件数
= 成功下载数
```

每个文件还必须满足：

```text
浏览器 receivedBytes = totalBytes = 本地字节数
本地 SHA-256 = Manifest SHA-256
```

验证命令：

```bash
python skills/notebooklm-source-ingest/scripts/verify_export.py \
  raw/notebooklm_exports/<notebook_id> --expected-count <source总数>
```

> 引用自实战验证：`quality_check_pipeline` 基线 38，原始 Markdown 38，失败 0；1354 项完整性断言全部通过。详见 [[notebooklm_quality_check_pipeline]]。

## 二、禁止把内容 RPC 当原始 Markdown

`source_get_content` 和同类内容 RPC 用于查询、摘要与语义核对。其常见实现会排序文本叶节点后直接拼接，可能破坏：

- YAML Frontmatter 分隔线；
- 标题与空行；
- 列表、表格和代码块布局；
- 原始文件字节。

用户要求“完整原文”“一点不能少”“还原 Markdown”时，必须下载 NotebookLM 提供的原始 `.md`；若 source 不是 Markdown，保留原文件并把转换件明确标成派生产物。

## 三、WSL2 认证安全

1. `auth_status` 只证明认证文件存在，不证明在线会话有效。
2. 首页跳转 `accounts.google.com` 即视为认证过期。
3. WSL2 中使用 `powershell.exe` 调起 Windows Chrome，不依赖 WSL `DISPLAY`。
4. Cookie 提取前必须取得用户明确授权。
5. Chrome 调试端口只绑定 `127.0.0.1:9222`，禁止 `0.0.0.0`。
6. 不输出 Cookie/token；认证文件权限设为 `0600`；完成后关闭临时浏览器。

## 四、下载与摄入

1. 先冻结 notebook ID、38/其他 source 数量、source ID 与原始 URL。
2. 用已登录浏览器下载原始文件；WSL curl/axios 对 `usercontent` 返回 403 时不得退回到压扁文本。
3. raw 层分别保留重复 source；知识层按 SHA-256 合并，但记录全部 source ID。
4. 按 [[知识库高保真摄入管线]] 执行分块、Map Checklist、Reduce 写卡和对账。
5. 上游代码路径不存在于本仓库时，保留在原始元数据快照，禁止写入有效 `related_code`。
6. 只被引用但未提供正文的卡名使用 `[待人类补充]`，不得合理化补写。
7. 更新来源卡、Hub、`index.md`、`log.md` 并重编译图谱。

## 五、结果报告口径

分别报告：

- 本轮 source/文件/哈希/正文卡数量；
- 本轮范围断链与孤岛；
- 全库历史断链、孤岛和 stale 项。

禁止用全库历史问题掩盖本轮失败，也禁止把本轮刻意创建的缺失引用占位卡说成已获取原文。

## 关联

- [[notebooklm_mcp用法]]
- [[notebooklm_quality_check_pipeline]]
- [[知识库高保真摄入管线]]
- [[知识图谱编译与检索操作规范]]
