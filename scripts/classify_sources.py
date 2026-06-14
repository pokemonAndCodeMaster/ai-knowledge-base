import os
import re

def parse_markdown_inventory(filepath):
    if not os.path.exists(filepath):
        return []
    
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith("|") and not any(h in line for h in ["Title", "---"]):
            parts = [p.strip() for p in line.split("|")][1:-1]
            if len(parts) >= 6:
                entries.append({
                    "title": parts[0],
                    "type": parts[1],
                    "url": parts[2],
                    "exists": parts[3],
                    "path": parts[4],
                    "id": parts[5]
                })
    return entries

def classify_agent_entry(title, url):
    t_lower = title.lower()
    u_lower = url.lower()
    
    if any(k in t_lower or k in u_lower for k in ["self-evolution", "self_evolution", "进化", "优化", "修正", "成长", "evol"]):
        return "agent_self_evolution"
    elif any(k in t_lower or k in u_lower for k in ["eval", "评价", "评测", "noise"]):
        return "agent_evaluation"
    elif any(k in t_lower or k in u_lower for k in ["tool", "mcp", "acp", "tooling", "interaction", "接口"]):
        return "agent_tool_use"
    elif any(k in t_lower or k in u_lower for k in ["rl", "强化学习", "反馈", "reward", "r1"]):
        return "agent_rl"
    elif any(k in t_lower or k in u_lower for k in ["prompt", "提示词", "指令"]):
        return "agent_prompt"
    elif any(k in t_lower or k in u_lower for k in ["memory", "状态", "context", "mem", "记忆"]):
        return "agent_memory"
    elif any(k in t_lower or k in u_lower for k in ["multi", "swarm", "coordination", "protocol", "agent-swarm", "swarms"]):
        return "agent_multi"
    elif any(k in t_lower or k in u_lower for k in ["harness", "cybernetics", "赛博"]):
        return "harness_engineering"
    else:
        return "agent_engineering"

def classify_multimodal_entry(title, url):
    t_lower = title.lower()
    u_lower = url.lower()
    
    if any(k in t_lower or k in u_lower for k in ["rope", "roformer", "位置编码", "positional"]):
        return "mllm_positional_encoding"
    elif any(k in t_lower or k in u_lower for k in ["clip", "siglip", "vision encoder", "vision-encoder", "对比", "contrastive"]):
        return "mllm_vision_encoder"
    elif any(k in t_lower or k in u_lower for k in ["resolution", "动态分辨率", "navit", "可变输入"]):
        return "mllm_dynamic_resolution"
    elif any(k in t_lower or k in u_lower for k in ["video", "视频"]):
        return "mllm_long_video"
    elif any(k in t_lower or k in u_lower for k in ["reasoning", "思维链", "thinking", "distillation", "思考", "反思", "thinking", "cot"]):
        return "mllm_reasoning"
    else:
        return "mllm_architecture"

def main():
    raw_dir = "/home/yyh/project/ai-knowledge-base/raw"
    
    agent_entries = parse_markdown_inventory(os.path.join(raw_dir, "inventory_merged_agent.md"))
    multimodal_entries = parse_markdown_inventory(os.path.join(raw_dir, "inventory_multimodal.md"))
    
    print(f"Loaded {len(agent_entries)} agent entries, {len(multimodal_entries)} multimodal entries.")
    
    classified_data = {}
    
    # 初始化统计字典
    stats = {}
    
    # 分类 Agent
    for entry in agent_entries:
        domain = classify_agent_entry(entry["title"], entry["url"])
        entry["domain"] = domain
        entry["category"] = "Agent Engineering"
        
        if domain not in classified_data:
            classified_data[domain] = []
        classified_data[domain].append(entry)
        stats[domain] = stats.get(domain, 0) + 1
        
    # 分类 Multimodal
    for entry in multimodal_entries:
        domain = classify_multimodal_entry(entry["title"], entry["url"])
        entry["domain"] = domain
        entry["category"] = "Multimodal LLM"
        
        if domain not in classified_data:
            classified_data[domain] = []
        classified_data[domain].append(entry)
        stats[domain] = stats.get(domain, 0) + 1
        
    # 输出到 raw/material_taxonomy.md
    output_path = os.path.join(raw_dir, "material_taxonomy.md")
    
    markdown_lines = []
    markdown_lines.append("# Knowledge Base Material Taxonomy Mapping")
    markdown_lines.append("")
    markdown_lines.append("This document tracks the classification mapping of all 229 ingested research materials to the extended repository domains.")
    markdown_lines.append("")
    
    # 写入统计
    markdown_lines.append("## Domain Statistics Summary")
    markdown_lines.append("")
    markdown_lines.append("| Domain | Total Count | Category | Description |")
    markdown_lines.append("|---|---|---|---|")
    
    # 描述字典
    domain_desc = {
        "agent_self_evolution": "Agent 自进化与 Skill 进化",
        "agent_evaluation": "Agent 评测与可信度评估",
        "agent_tool_use": "Agent 工具调用能力与交互控制",
        "agent_rl": "Agent 强化学习与反馈决策",
        "agent_prompt": "Agent 提示词工程与系统指令优化",
        "agent_memory": "Agent 记忆、状态与长期上下文管理",
        "agent_multi": "多智能体协同、对齐与通讯协议",
        "harness_engineering": "Harness 约束工程与赛博反馈",
        "agent_engineering": "通用 Agent 工程设计模式",
        "mllm_positional_encoding": "多模态位置编码（2D-RoPE 等）",
        "mllm_vision_encoder": "视觉编码与对比学习（CLIP 等）",
        "mllm_dynamic_resolution": "动态分辨率与可变输入大小",
        "mllm_long_video": "长视频时空建模与检索式理解",
        "mllm_reasoning": "多模态推理与反思",
        "mllm_architecture": "通用多模态架构设计"
    }
    
    for dom in sorted(stats.keys(), key=lambda x: stats[x], reverse=True):
        cat = "Agent" if "agent" in dom or dom == "harness_engineering" else "Multimodal"
        markdown_lines.append(f"| `{dom}` | {stats[dom]} | {cat} | {domain_desc.get(dom, '')} |")
        
    markdown_lines.append("")
    
    # 写入按 Domain 分组的资料列表
    markdown_lines.append("## Materials Classified by Domains")
    markdown_lines.append("")
    
    for dom in sorted(classified_data.keys()):
        markdown_lines.append(f"### {dom.upper()} ({domain_desc.get(dom, '')})")
        markdown_lines.append("")
        markdown_lines.append("| Title | Type | Exists Locally? | Path | ID |")
        markdown_lines.append("|---|---|---|---|---|")
        
        for entry in classified_data[dom]:
            markdown_lines.append(f"| {entry['title']} | {entry['type']} | {entry['exists']} | {entry['path']} | {entry['id']} |")
            
        markdown_lines.append("")
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown_lines))
        
    print(f"Material taxonomy file generated at {output_path}.")

if __name__ == "__main__":
    main()
