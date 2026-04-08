import re

unindexed = {
  "wiki/concepts/computational_vs_inferential.md": "计算型与推理型 Harness",
  "wiki/concepts/steering_loop.md": "Steering Loop (控制回路)",
  "wiki/concepts/ashby_law.md": "Ashby's Law (必要多样性定律)",
  "wiki/concepts/feedforward_and_feedback.md": "前馈与反馈控制 (Feedforward and Feedback)",
  "wiki/sources/almirant.md": "Almirant (项目级 Agent 协调面板)",
  "wiki/sources/paperclip.md": "Paperclip (零人类公司编排系统)",
  "wiki/sources/martin_fowler_harness.md": "Martin Fowler：Harness",
  "wiki/entities/thoughtworks.md": "Thoughtworks",
  "wiki/entities/martin_fowler.md": "Martin Fowler",
  "wiki/synthesis/2026_AI智能体工程全景图.md": "2026 AI 智能体工程全景图"
}

index = open('index.md', encoding='utf-8').read()

def insert_into_section(content, section_header, items):
    if not items: return content
    pattern = re.compile(rf'(## {section_header}.*?)(?=\n## |\Z)', re.DOTALL)
    match = pattern.search(content)
    if match:
        section = match.group(1)
        addition = "\n".join([f"| [{title}]({path}) | 自动归档摄入 |" for path, title in items]) + "\n"
        new_section = section.rstrip() + "\n" + addition
        return content.replace(section, new_section + "\n")
    return content

synthesis_items = [(k, v) for k, v in unindexed.items() if 'synthesis/' in k]
concept_items = [(k, v) for k, v in unindexed.items() if 'concepts/' in k]
entity_items = [(k, v) for k, v in unindexed.items() if 'entities/' in k]
source_items = [(k, v) for k, v in unindexed.items() if 'sources/' in k]

index = insert_into_section(index, r'📌 综合分析.*', synthesis_items)
index = insert_into_section(index, r'🤖 AI 与智能体类', concept_items)
index = insert_into_section(index, r'🏷️ 实体.*', entity_items)
index = insert_into_section(index, r'📄 来源摘要.*', source_items)

open('index.md', 'w', encoding='utf-8').write(index)

from datetime import datetime
date_str = datetime.now().strftime("%Y-%m-%d")

log_entry = f"""
## [{date_str}] ingest | AI Librarain 自动整理与更新
- 动作：体检知识库 (Lint)，并将游离文件登记到 `index.md`。
- 详情：成功摄入并注册了 `2026_AI智能体工程全景图.md` 等 10 份新文件。
- 触发者：用户要求执行 lint、ingest 及 Git 提交。
"""
open('log.md', 'a', encoding='utf-8').write(log_entry)
