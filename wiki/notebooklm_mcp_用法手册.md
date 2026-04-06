# NotebookLM MCP Server 实践用法手册

**知识卡片类型**：工具实践 / 操作指南
**关联节点**：[[统一知识系统主干指南]] | [[AI 知识库操作指南]] | [[自动化摄入（Ingest）]]

---

## 🧭 一、概念定位

NotebookLM 提供了两种调用方式：
- **浏览器 UI**：可视化操作，适合一次性探索。
- **MCP Server + nlm CLI**：程序化调用，可嵌入进 AI 工作流自动化流程（如 ai-librarian Skill）。

本卡片重点记录的是 **MCP Server + `nlm` CLI 的实战用法**，它是让 AI 助手（如 Antigravity）能够帮你自动管理 NotebookLM 的关键基础设施。

---

## 📟 二、nlm CLI 核心命令速查表

### 📒 笔记本管理
```bash
# 列出所有笔记本
nlm notebook list

# 查看某个笔记本的详情（含所有 source 列表）
nlm notebook get <notebook_id>

# 创建新笔记本
nlm notebook create --title "笔记本名称"

# 重命名笔记本
nlm notebook rename <notebook_id> --title "新名称"
```

### 📄 源文件（Sources）管理

```bash
# 列出笔记本的所有 Sources
nlm source list <notebook_id>

# 添加一个网页/YouTube URL 作为 Source
nlm source add <notebook_id> --url "https://example.com"

# 上传本地文件作为 Source（支持 PDF、txt、md、音频）
nlm source add <notebook_id> --file "./my_notes.pdf"

# 获取某个 Source 的元数据详情
nlm source get <source_id>

# 🔑 关键：导出 Source 的原始纯文本（无 AI 摘要污染）
nlm source content <source_id>

# 导出并保存到本地（这是最常用的"搬运"用法）
nlm source content <source_id> > ./llm_wiki/raw/文件名.md

# 删除一个 Source（不可逆，需要加 --confirm）
nlm source delete <source_id> --confirm
```

### 🤖 AI 生成内容（Studio）

```bash
# 生成音频播客（Audio Overview）
nlm studio audio <notebook_id>

# 生成报告
nlm studio report <notebook_id> --format "Briefing Doc"

# 生成闪卡
nlm studio flashcards <notebook_id>

# 查看已生成内容的状态和下载地址
nlm studio status <notebook_id>

# 下载某个生成产物到本地
nlm studio download <notebook_id> --type audio --output ./podcast.mp4
```

### 🔍 深度研究（Research）

```bash
# 启动一个深度网络研究任务（约 5 分钟，~40 条新来源）
nlm research start <notebook_id> --query "Zettelkasten + AI 知识管理" --mode deep

# 查看研究任务进度（会阻塞直到完成或超时）
nlm research status <notebook_id>

# 将研究成果自动导入为 Sources
nlm research import <notebook_id> --task-id <task_id>
```

### 🗣️ 对话查询（Query）

```bash
# 向笔记本 AI 提问（基于已有 Sources 的语义检索）
nlm notebook query <notebook_id> "费曼学习法和主动召回的区别是什么？"
```

---

## 🔄 三、实战：批量搬运 NotebookLM Sources 到本地

这是将 NotebookLM 内容"物理化迁移"到本地 `llm_wiki/raw/` 目录的标准流程：

### 方法 A：Python 脚本（推荐，自动跳过已下载）
```python
import json, subprocess, os

sources = [{"id": "...", "title": "..."}, ...]  # 来自 nlm notebook get
out_dir = "./llm_wiki/raw"

for src in sources:
    path = f"{out_dir}/{src['title'].replace('/', '_')}.md"
    if os.path.exists(path):
        continue  # 跳过已下载
    result = subprocess.run(
        ["nlm", "source", "content", src["id"]], 
        capture_output=True, text=True
    )
    if result.returncode == 0:
        with open(path, "w") as f:
            f.write(result.stdout)
        print(f"[OK] {src['title']}")
```

### 方法 B：Bash 一行魔法（配合 jq）
```bash
# 获取 notebook 详情并批量导出所有 Sources 到本地目录
nlm notebook get <notebook_id> --json \
  | jq -c '.sources[]' \
  | while read i; do
      id=$(echo $i | jq -r .id)
      title=$(echo $i | jq -r .title | tr ' /' '__')
      echo "Downloading $title..."
      nlm source content $id > "./llm_wiki/raw/${title}.md"
    done
```

---

## ⚠️ 四、重要注意事项

| 问题 | 说明 |
|---|---|
| **频率限制** | 并发请求太多会被 NotebookLM 限速，批量下载推荐线性执行（不并发）|
| **内容完整性** | `source content` 获取的是索引后的文本，部分格式（如图表）可能丢失 |
| **认证 Token** | 如遇鉴权失败，执行 `nlm login` 重新认证；使用 `nlm login switch <profile>` 切换账号 |
| **原件不可变** | 下载到 `raw/` 的文件只读，永远不要在 `raw/` 中修改，是 wiki 架构的铁律 |

---

## 🧩 五、与 AI 知识库工作流的整合要点

MCP Server 是 ai-librarian Skill 的**基础设施层**。完整的闭环是：

```
你 (人类总编辑)
  ↓ 发现好内容（网页、PDF、推文等）
  ↓
NotebookLM (收集层，通过 MCP/UI 添加 Source)
  ↓ nlm source content → 导出原始文本
  ↓
llm_wiki/raw/ (原始区，不可变)
  ↓ 触发 ai-librarian Ingest 操作
  ↓
llm_wiki/wiki/ (编译知识网络，AI 维护)
```

**参见**：[[AI 知识库操作指南（ai-librarian Prompt 触发手册）]]
