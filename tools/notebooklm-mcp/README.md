# NotebookLM MCP Wrapper

本目录提供本项目使用的 NotebookLM MCP stdio server。

它复用本机已有的可审计实现：

- `/home/yyh/project/llm_base/notebooklm-mcp/build/api-client.js`
- `/home/yyh/project/llm_base/notebooklm-mcp/build/orchestrator.js`
- `/home/yyh/project/llm_base/notebooklm-mcp/node_modules/@modelcontextprotocol/sdk`

认证文件沿用 `~/.notebooklm-mcp/auth.json`。如认证过期，先运行：

```bash
node /home/yyh/project/llm_base/notebooklm-mcp/build/browser-auth.js
```

## Codex MCP 配置

```bash
codex mcp add notebooklm -- node /home/yyh/project/ai-knowledge-base/tools/notebooklm-mcp/server.mjs
```

配置后重启 Codex 会话，工具会作为 NotebookLM MCP server 暴露。

## 关键工具

- `notebook_list`：列出 NotebookLM 笔记本。
- `notebook_get`：获取笔记本原始结构。
- `source_list`：列出某笔记本的 sources。
- `source_get_content`：拉取单个 source 原文内容。
- `source_export_all`：批量导出 source 原文到 `raw/notebooklm_exports/<notebook_id>/`。
- `notebook_query`：基于笔记本 sources 对话。
- `generate_artifact`：生成音频、视频、quiz、slides、infographic、report、mind map。
- `studio_list`：列出生成产物。
