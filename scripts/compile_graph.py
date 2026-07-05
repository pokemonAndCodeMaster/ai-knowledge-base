#!/usr/bin/env python3
"""
compile_graph.py — 知识库图索引编译器

解析 wiki/ 下所有 .md 文件的 frontmatter 和 [[双链]]，
构建邻接表，输出 .wiki_graph.json。

零外部依赖（不依赖 PyYAML），纯正则解析 frontmatter。

Usage:
    python scripts/compile_graph.py
    python scripts/compile_graph.py --project-root /path/to/project
"""

import os
import re
import sys
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ─── 正则常量 ──────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')


# ─── 纯正则 YAML Frontmatter 解析器 ───────────────────────────────
# 只处理我们 schema 中用到的类型：string, list, int, bool
# 不支持嵌套对象（我们的 frontmatter 不需要）

def _parse_yaml_value(raw: str) -> Any:
    """解析单个 YAML 值（string / int / bool / list）。"""
    raw = raw.strip()

    # 空值
    if not raw or raw in ('~', 'null', 'None'):
        return None

    # 行内列表: ["a", "b"] 或 [a, b]
    if raw.startswith('[') and raw.endswith(']'):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in re.split(r',\s*', inner):
            item = item.strip().strip('"').strip("'")
            if item:
                items.append(item)
        return items

    # 布尔
    if raw.lower() in ('true', 'yes'):
        return True
    if raw.lower() in ('false', 'no'):
        return False

    # 整数
    try:
        return int(raw)
    except ValueError:
        pass

    # 字符串（去掉引号）
    return raw.strip('"').strip("'")


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """从 markdown 内容中提取 YAML frontmatter 并解析为 dict。"""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}

    fm_text = match.group(1)
    result = {}
    current_key = None
    list_accumulator = None

    for line in fm_text.split('\n'):
        # 跳过注释和空行
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            # 如果正在积累多行列表，空行结束它
            if list_accumulator is not None and current_key:
                result[current_key] = list_accumulator
                list_accumulator = None
                current_key = None
            continue

        # 多行列表项: "  - value"
        if stripped.startswith('- ') and list_accumulator is not None:
            val = stripped[2:].strip().strip('"').strip("'")
            list_accumulator.append(val)
            continue

        # 键值对: "key: value"
        kv_match = re.match(r'^(\w[\w_]*)\s*:\s*(.*)', line)
        if kv_match:
            # 先保存之前的列表
            if list_accumulator is not None and current_key:
                result[current_key] = list_accumulator
                list_accumulator = None

            key = kv_match.group(1)
            val_raw = kv_match.group(2).strip()

            if not val_raw:
                # 可能是多行列表的开始
                current_key = key
                list_accumulator = []
            else:
                result[key] = _parse_yaml_value(val_raw)
                current_key = key
                list_accumulator = None
        elif list_accumulator is not None and stripped.startswith('- '):
            # 多行列表项（无缩进也算）
            val = stripped[2:].strip().strip('"').strip("'")
            list_accumulator.append(val)

    # 最后一个列表
    if list_accumulator is not None and current_key:
        result[current_key] = list_accumulator

    return result


# ─── Markdown 解析工具 ────────────────────────────────────────────

def extract_wikilinks(content: str) -> List[str]:
    """提取正文中的 [[wikilink]]，忽略无损原文快照区。"""
    body = FRONTMATTER_RE.sub('', content)
    body = re.sub(
        r'<!-- ORIGINAL_START -->.*?<!-- ORIGINAL_END -->',
        '',
        body,
        flags=re.DOTALL,
    )
    return list(set(WIKILINK_RE.findall(body)))


def extract_summary(content: str, max_len: int = 200) -> str:
    """提取首段摘要：frontmatter 之后、第一个 ## 之前的非空内容。"""
    body = FRONTMATTER_RE.sub('', content).strip()
    lines = body.split('\n')
    summary_lines = []
    for line in lines:
        if line.startswith('## '):
            break
        # 跳过主标题
        if line.startswith('# '):
            continue
        cleaned = line.strip()
        if cleaned:
            summary_lines.append(cleaned)
    summary = ' '.join(summary_lines)
    if len(summary) > max_len:
        summary = summary[:max_len - 3] + '...'
    return summary


def compute_file_hash(filepath: str) -> str:
    """计算文件 SHA256 哈希（截取前 16 位）。"""
    try:
        if os.path.isdir(filepath):
            return ''
        with open(filepath, 'rb') as f:
            return f'sha256:{hashlib.sha256(f.read()).hexdigest()[:16]}'
    except (FileNotFoundError, PermissionError):
        return ''


# ─── 核心编译逻辑 ─────────────────────────────────────────────────

def build_slug_to_path(wiki_dir: Path, project_root: Path) -> Dict[str, str]:
    """构建 slug（文件名无扩展名）→ 相对路径 的映射。"""
    mapping = {}
    for md_file in sorted(wiki_dir.rglob('*.md')):
        slug = md_file.stem
        rel_path = str(md_file.relative_to(project_root))
        # 如果 slug 重复，优先保留路径较短的（更"核心"的）
        if slug not in mapping or len(rel_path) < len(mapping[slug]):
            mapping[slug] = rel_path
    return mapping


def compile_graph(project_root: Path) -> Dict[str, Any]:
    """主编译函数：遍历 wiki/ → 构建图索引 → 返回 dict。"""
    wiki_dir = project_root / 'wiki'
    if not wiki_dir.exists():
        print(f'错误：wiki 目录不存在：{wiki_dir}', file=sys.stderr)
        sys.exit(1)

    slug_to_path = build_slug_to_path(wiki_dir, project_root)
    nodes: Dict[str, Dict[str, Any]] = {}
    all_outlink_slugs: Dict[str, List[str]] = {}  # rel_path → [slug]

    md_files = sorted(wiki_dir.rglob('*.md'))

    for md_file in md_files:
        rel_path = str(md_file.relative_to(project_root))
        try:
            content = md_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            print(f'警告：无法读取 {rel_path}（编码错误），跳过', file=sys.stderr)
            continue

        fm = parse_frontmatter(content)
        wikilinks = extract_wikilinks(content)
        summary = extract_summary(content)

        # 规范化 domain 为 list
        domain = fm.get('domain', [])
        if isinstance(domain, str):
            domain = [domain]

        # 规范化列表字段
        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        trigger_kw = fm.get('trigger_keywords', [])
        if isinstance(trigger_kw, str):
            trigger_kw = [trigger_kw]
        affects = fm.get('affects_path', [])
        if isinstance(affects, str):
            affects = [affects]
        related_code = fm.get('related_code', [])
        if isinstance(related_code, str):
            related_code = [related_code]

        node = {
            'title': fm.get('title', md_file.stem),
            'slug': md_file.stem,
            'domain': domain,
            'type': fm.get('type', ''),
            'tags': tags,
            'trigger_keywords': trigger_kw,
            'affects_path': affects,
            'related_code': related_code,
            'status': fm.get('status', 'active'),
            'summary': summary,
            'outlinks': wikilinks,
            'inlinks': [],  # 稍后回填
        }

        # 代码模块卡：计算关联文件哈希
        if fm.get('type') == 'code_module' and related_code:
            code_hashes = {}
            for cp in related_code:
                abs_cp = project_root / cp
                h = compute_file_hash(str(abs_cp))
                if h:
                    code_hashes[cp] = h
            node['code_hashes'] = code_hashes

        nodes[rel_path] = node
        all_outlink_slugs[rel_path] = wikilinks

    # ─── 回填反向链接（inlinks） ───
    for source_path, outlinks in all_outlink_slugs.items():
        source_slug = nodes[source_path]['slug']
        for target_slug in outlinks:
            target_path = slug_to_path.get(target_slug)
            if target_path and target_path in nodes:
                inlinks = nodes[target_path]['inlinks']
                if source_slug not in inlinks:
                    inlinks.append(source_slug)

    # ─── 统计信息 ───
    orphan_cards = [
        path for path, node in nodes.items()
        if not node['inlinks'] and node['type'] not in ('hub', 'schema')
    ]
    broken_links = []
    for path, outlinks in all_outlink_slugs.items():
        for slug in outlinks:
            if slug not in slug_to_path:
                broken_links.append({'from': path, 'target': slug})

    total_links = sum(len(links) for links in all_outlink_slugs.values())

    return {
        'version': 1,
        'compiled_at': datetime.now().astimezone().isoformat(),
        'stats': {
            'total_cards': len(nodes),
            'total_links': total_links,
            'orphan_count': len(orphan_cards),
            'orphan_cards': orphan_cards,
            'broken_link_count': len(broken_links),
            'broken_links': broken_links,
        },
        'nodes': nodes,
    }


# ─── CLI 入口 ─────────────────────────────────────────────────────

def main():
    # 解析参数
    project_root = Path(__file__).resolve().parent.parent
    args = sys.argv[1:]
    if '--project-root' in args:
        idx = args.index('--project-root')
        project_root = Path(args[idx + 1]).resolve()
    if '--help' in args or '-h' in args:
        print(__doc__)
        sys.exit(0)

    print(f'编译知识图谱索引...', file=sys.stderr)
    print(f'  项目根目录: {project_root}', file=sys.stderr)

    graph = compile_graph(project_root)

    # 输出到 .wiki_graph.json
    output_path = project_root / '.wiki_graph.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    stats = graph['stats']
    print(f'  ✅ 编译完成:', file=sys.stderr)
    print(f'     卡片数: {stats["total_cards"]}', file=sys.stderr)
    print(f'     链接数: {stats["total_links"]}', file=sys.stderr)
    print(f'     孤岛卡片: {stats["orphan_count"]}', file=sys.stderr)
    print(f'     断链: {stats["broken_link_count"]}', file=sys.stderr)
    print(f'  输出: {output_path}', file=sys.stderr)


if __name__ == '__main__':
    main()
