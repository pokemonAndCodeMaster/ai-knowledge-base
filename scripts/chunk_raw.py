#!/usr/bin/env python3
"""
chunk_raw.py — AST 语义分块器

用于将数万字的长篇 Raw 资料按 Markdown 标题层级（H1/H2）进行语义切分，
避免 Agent 一次性处理长文时触发 "Lost in the Middle" 导致细节丢失。

零外部依赖，纯 Python 实现。

Usage:
    python scripts/chunk_raw.py raw/articles/some_long_doc.md
"""

import sys
import re
from pathlib import Path

def chunk_markdown(filepath: str, output_dir: str):
    path = Path(filepath)
    if not path.exists():
        print(f"错误: 找不到文件 {filepath}")
        sys.exit(1)

    content = path.read_text(encoding='utf-8')
    lines = content.split('\n')

    chunks = []
    current_chunk_lines = []
    in_code_block = False

    # 预先处理输出目录
    out_path = Path(output_dir) / path.stem
    out_path.mkdir(parents=True, exist_ok=True)

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        # 匹配 H1 和 H2 标题
        header_match = re.match(r'^(#{1,2})\s+(.*)', line)

        # 遇到不在代码块内的 H1/H2 时，切断形成新 Chunk
        if not in_code_block and header_match:
            if current_chunk_lines:
                chunks.append(current_chunk_lines)
                current_chunk_lines = []

        current_chunk_lines.append(line)

    # 收集最后一块
    if current_chunk_lines:
        chunks.append(current_chunk_lines)

    # 写入分块文件
    for i, chunk_lines in enumerate(chunks, 1):
        chunk_file = out_path / f"chunk_{i:03d}.md"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            # 注入上下文面包屑，防止 Agent 迷失
            f.write(f"> 📍 来源文件: {path.name} | 语义分块: {i}/{len(chunks)}\n\n")
            f.write("\n".join(chunk_lines))

    print(f"✅ 成功将 {path.name} 切分为 {len(chunks)} 个语义块。")
    print(f"📂 输出目录: {out_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/chunk_raw.py <raw_markdown_file>")
        sys.exit(1)
    
    target_file = sys.argv[1]
    
    # 默认输出到原文件所在目录的 .chunks 子目录中
    target_path = Path(target_file)
    default_out_dir = target_path.parent / ".chunks"
    
    out_d = sys.argv[2] if len(sys.argv) > 2 else default_out_dir
    chunk_markdown(target_file, out_d)
