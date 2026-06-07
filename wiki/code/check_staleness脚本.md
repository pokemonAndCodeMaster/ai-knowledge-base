---
title: "check_staleness脚本"
domain: ["knowledge_mgmt", "meta"]
type: "code_module"
tags: [过期检测, code_hash, 断链, 孤岛]
created: 2026-06-07
updated: 2026-06-07
sources: 0
status: active
related_code:
  - "scripts/check_staleness.py"
code_hash: "sha256:dfff7005e1455787"
affects_path: []
trigger_keywords:
  - check_staleness
  - 过期检测
  - 代码变更检测
  - code_hash
  - 卡片过期
  - 断链检测
---

# check_staleness脚本

## 职责（一句话）

扫描知识卡片，检测代码文件变更（hash 比对）、已标记 stale 的未处理卡片、孤岛和断链。

## 运行方式

```bash
# 全量检查（代码过期 + 时间过期 + 孤岛/断链）
python3 scripts/check_staleness.py

# 仅检查代码相关卡片
python3 scripts/check_staleness.py --code-only

# 自定义时间阈值（默认 90 天）
python3 scripts/check_staleness.py --days 60
```

## 关键函数与流程

```
main()
  ├─ 加载 .wiki_graph.json
  ├─ check_code_staleness()
  │    └─ 遍历 type=code_module 的节点
  │         └─ 计算 related_code 文件的 SHA256
  │              ├─ 与 frontmatter.code_hash 比对
  │              ├─ 文件不存在 → code_file_missing
  │              ├─ hash 不一致 → code_changed（需更新卡片）
  │              └─ 缺少 hash → no_hash_recorded（需补填）
  ├─ check_time_staleness()
  │    └─ 检查 status=stale 但未处理的卡片
  └─ check_orphans_and_broken()
       └─ 直接读 .wiki_graph.json 的 stats 字段（编译时已算好）
```

## 输出格式

```json
{
  "checked_at": "...",
  "total_cards": 55,
  "code_stale_count": 1,
  "code_staleness": [
    {
      "card": "wiki/code/xxx.md",
      "code_path": "scripts/xxx.py",
      "issue": "code_changed",
      "old_hash": "sha256:abc...",
      "new_hash": "sha256:def...",
      "action": "Agent 需审阅代码变更并更新卡片内容和 code_hash"
    }
  ],
  "orphan_count": 14,
  "broken_link_count": 71
}
```

## issue 类型说明

| issue | 含义 | 处理方式 |
|-------|------|---------|
| `code_changed` | 代码文件 hash 与卡片记录不一致 | 审阅 git diff → 更新卡片 → 刷新 hash |
| `code_file_missing` | related_code 指向的文件不存在 | 检查路径拼写 or 删除引用 |
| `no_hash_recorded` | code_module 卡片没有 code_hash 字段 | 补填 hash（见规范卡片） |
| `marked_stale` | status=stale 但未处理 | 审阅并更新或标记 superseded |

## 与其他脚本的关系

- 依赖 [[compile_graph脚本]] 的产物 `.wiki_graph.json`
- 导入 `compile_graph.py` 中的 `parse_frontmatter()` 和 `compute_file_hash()` 工具函数
- 在 `[health]` 工作流中与 `compile_graph.py` 配合使用（见 [[知识图谱编译与检索操作规范]]）
