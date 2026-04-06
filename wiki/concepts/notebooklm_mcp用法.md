---
title: NotebookLM MCP Server 实践用法手册
tags: [工具, NotebookLM, MCP, CLI, nlm]
created: 2026-04-06
updated: 2026-04-06
sources: 1
status: active
---

# NotebookLM MCP Server 实践用法手册

**关联节点**：[[统一学习与知识管理框架]] | [[ai知识库操作指南]] | [[复利知识库]]

---

## 🧭 一、概念定位

NotebookLM 提供两种调用方式：
- **浏览器 UI**：可视化操作，适合一次性探索。
- **MCP Server + nlm CLI**：程序化调用，可嵌入 AI 工作流自动化（即 ai-librarian Skill 的基础设施层）。

完整闭环：
```
你（人类总编辑）
  ↓ 发现好内容
NotebookLM（收集层，通过 MCP/UI 添加 Source）
  ↓ nlm source content → 导出原始文本
llm_wiki/raw/（原始区，不可变）
  ↓ 触发 ai-librarian Ingest
llm_wiki/wiki/（编译知识网络，AI维护）
```

---

## 📟 二、nlm CLI 核心命令速查

### 📒 笔记本管理
```bash
nlm notebook list                          # 列出所有笔记本
nlm notebook get <notebook_id>             # 查看详情（含所有 source 列表）
nlm notebook create --title "笔记本名称"   # 创建新笔记本
nlm notebook rename <notebook_id> --title "新名称"
```

### 📄 源文件（Sources）管理
```bash
nlm source list <notebook_id>             # 列出所有 Sources
nlm source add <notebook_id> --url "https://example.com"   # 添加网页
nlm source add <notebook_id> --file "./my_notes.pdf"       # 上传本地文件
nlm source get <source_id>                # 查看元数据
nlm source content <source_id>            # 🔑 导出原始纯文本（最常用）
nlm source content <source_id> > ./llm_wiki/raw/文件名.md  # 导出并保存
nlm source delete <source_id> --confirm   # 删除（不可逆）
```

### 🤖 Studio 生成内容
```bash
nlm studio audio <notebook_id>            # 生成播客
nlm studio report <notebook_id> --format "Briefing Doc"
nlm studio flashcards <notebook_id>
nlm studio status <notebook_id>           # 查看生成状态
nlm studio download <notebook_id> --type audio --output ./podcast.mp4
```

### 🔍 深度研究
```bash
nlm research start <notebook_id> --query "主题关键词" --mode deep
nlm research status <notebook_id>
nlm research import <notebook_id> --task-id <task_id>
```

### 🗣️ 查询笔记本
```bash
nlm notebook query <notebook_id> "你的问题"
```

---

## 🔄 三、批量搬运 Sources 到本地

### Python 脚本（推荐，自动跳过已下载）
```python
import json, subprocess, os

sources = [{"id": "...", "title": "..."}]  # 来自 nlm notebook get --json
out_dir = "./llm_wiki/raw"

for src in sources:
    path = f"{out_dir}/{src['title'].replace('/', '_')}.md"
    if os.path.exists(path): continue
    result = subprocess.run(
        ["nlm", "source", "content", src["id"]],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        with open(path, "w") as f:
            f.write(result.stdout)
```

### Bash 一行魔法（配合 jq）
```bash
nlm notebook get <notebook_id> --json \
  | jq -c '.sources[]' \
  | while read i; do
      id=$(echo $i | jq -r .id)
      title=$(echo $i | jq -r .title | tr ' /' '__')
      nlm source content $id > "./llm_wiki/raw/${title}.md"
    done
```

---

## ⚠️ 四、注意事项

| 问题 | 说明 |
|---|---|
| **频率限制** | 并发太多会被 NotebookLM 限速，批量下载推荐线性执行 |
| **内容完整性** | `source content` 获取的是索引后文本，图表可能丢失 |
| **认证失效** | 执行 `nlm login` 重新认证；`nlm login switch <profile>` 切换账号 |
| **raw/ 铁律** | 下载到 `raw/` 的文件只读，永远不要修改 |
