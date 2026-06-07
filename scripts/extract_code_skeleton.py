#!/usr/bin/env python3
"""
extract_code_skeleton.py — 源码骨架提取器

用于大批量代码库摄入时的预处理。
通过 AST 解析（针对 Python）或正则提取，掏空所有代码实现细节，
仅保留文件结构、Import 依赖关系、类定义与关键函数签名。

零外部依赖。

Usage:
    python scripts/extract_code_skeleton.py <文件或目录路径>
"""

import sys
import os
import ast
import re
from pathlib import Path

def extract_python_skeleton(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        tree = ast.parse(content)
    except Exception as e:
        return f"解析失败 ({filepath.name}): {e}"

    lines = [f"## 📄 {filepath}"]
    
    # 提取模块级 Docstring
    doc = ast.get_docstring(tree)
    if doc:
        lines.append(f"> **模块说明**: {doc.split(chr(10))[0]}")
        
    imports = []
    classes = []
    functions = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(f"from {module} import {alias.name}")
        elif isinstance(node, ast.ClassDef):
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
            base_str = f"({', '.join(bases)})" if bases else ""
            classes.append(f"class {node.name}{base_str}:")
            # 提取类方法
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    classes.append(f"    def {item.name}(...):")
        elif isinstance(node, ast.FunctionDef):
            functions.append(f"def {node.name}(...):")

    if imports:
        lines.append("\n### 📦 依赖 (Imports)")
        lines.extend([f"- `{imp}`" for imp in imports])
    
    if classes:
        lines.append("\n### 🏗️ 类 (Classes)")
        lines.extend([f"- `{cls}`" for cls in classes])
        
    if functions:
        lines.append("\n### ⚡ 函数 (Functions)")
        lines.extend([f"- `{func}`" for func in functions])

    return "\n".join(lines)

def extract_generic_skeleton(filepath):
    """处理非 Python 文件的通用正则 fallback"""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ""
        
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        # 简单匹配常见的类/函数/导出声明
        if re.match(r'^(import |export |class |def |function |func |type |interface )', line):
            lines.append(f"- `{line}`")
            
    if not lines:
        return f"## 📄 {filepath}\n> 无识别到的结构签名"
        
    return f"## 📄 {filepath}\n### 🔍 结构探测\n" + "\n".join(lines[:50]) # 最多显示50行防刷屏

def process_target(target_path, output_dir):
    path = Path(target_path)
    if not path.exists():
        print(f"错误: 找不到路径 {target_path}")
        sys.exit(1)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    out_file = out_path / "code_skeleton.md"

    files_to_process = []
    if path.is_file():
        files_to_process.append(path)
    else:
        for root, dirs, files in os.walk(path):
            # 过滤隐藏目录和缓存
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.go', '.java')):
                    files_to_process.append(Path(root) / file)

    if not files_to_process:
        print("未找到支持的代码文件。")
        sys.exit(0)

    output_content = ["# 🦴 代码目录架构骨架 (Code Skeleton)\n"]
    output_content.append(f"> 提取目标: `{target_path}`\n> 共包含 {len(files_to_process)} 个代码文件\n")

    for f in sorted(files_to_process):
        if f.suffix == '.py':
            res = extract_python_skeleton(f)
        else:
            res = extract_generic_skeleton(f)
        output_content.append(res)
        output_content.append("\n---\n")

    out_file.write_text("\n".join(output_content), encoding='utf-8')
    print(f"✅ 骨架提取完成！共掏空 {len(files_to_process)} 个代码文件的实现细节。")
    print(f"📉 Token 压缩：极致降低 Context 开销。")
    print(f"📂 输出路径: {out_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_code_skeleton.py <dir_or_file>")
        sys.exit(1)
    target = sys.argv[1]
    
    # 默认输出到 .chunks 目录
    default_out_dir = ".chunks"
    out_d = sys.argv[2] if len(sys.argv) > 2 else default_out_dir
    process_target(target, out_d)
