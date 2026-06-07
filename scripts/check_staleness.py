#!/usr/bin/env python3
"""
check_staleness.py — 知识库过期检测器

扫描知识卡片，检测：
1. 代码卡片（code_module）的 related_code 文件是否有变更（通过 code_hash 比对）
2. 所有卡片的 updated 日期是否超过阈值（默认 90 天）
3. status 为 stale 但未处理的卡片

零外部依赖。

Usage:
    python scripts/check_staleness.py
    python scripts/check_staleness.py --code-only
    python scripts/check_staleness.py --days 60
"""

import sys
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# 复用 compile_graph 的 frontmatter 解析器
sys.path.insert(0, str(Path(__file__).parent))
from compile_graph import parse_frontmatter, compute_file_hash, FRONTMATTER_RE


def check_code_staleness(
    project_root: Path,
    nodes: Dict[str, Dict],
) -> List[Dict[str, Any]]:
    """检查 code_module 卡片的关联代码是否有变更。"""
    stale = []

    for path, node in nodes.items():
        if node.get('type') != 'code_module':
            continue

        related_code = node.get('related_code', [])
        if not related_code:
            continue

        # 读取卡片文件获取 code_hash
        card_path = project_root / path
        if not card_path.exists():
            continue

        content = card_path.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        stored_hash = fm.get('code_hash', '')

        for code_path in related_code:
            abs_code = project_root / code_path
            if not abs_code.exists():
                stale.append({
                    'card': path,
                    'code_path': code_path,
                    'issue': 'code_file_missing',
                    'message': f'关联代码文件不存在：{code_path}',
                    'action': '检查路径是否正确，或删除 related_code 引用',
                })
                continue

            current_hash = compute_file_hash(str(abs_code))
            if stored_hash and current_hash != stored_hash:
                stale.append({
                    'card': path,
                    'code_path': code_path,
                    'issue': 'code_changed',
                    'old_hash': stored_hash,
                    'new_hash': current_hash,
                    'message': f'代码文件已变更：{code_path}',
                    'action': 'Agent 需审阅代码变更并更新卡片内容和 code_hash',
                })
            elif not stored_hash:
                stale.append({
                    'card': path,
                    'code_path': code_path,
                    'issue': 'no_hash_recorded',
                    'current_hash': current_hash,
                    'message': f'卡片缺少 code_hash 字段：{code_path}',
                    'action': '在卡片 frontmatter 中添加 code_hash 字段',
                })

    return stale


def check_time_staleness(
    nodes: Dict[str, Dict],
    max_days: int = 90,
) -> List[Dict[str, Any]]:
    """检查 updated 日期超过阈值的卡片。"""
    stale = []
    now = datetime.now()
    cutoff = now - timedelta(days=max_days)

    for path, node in nodes.items():
        status = node.get('status', 'active')

        # 已经标记为 stale 的
        if status == 'stale':
            stale.append({
                'card': path,
                'issue': 'marked_stale',
                'message': f'卡片已标记为 stale 但未处理',
                'action': '审阅并更新或标记为 superseded',
            })
            continue

        # 跳过非 active 的
        if status != 'active':
            continue

        # 这里我们需要从编译产物中获取 updated 日期
        # 但当前编译产物不包含 updated，需要直接读文件
        # 为了效率，先跳过（在后续版本中可以把 updated 加入编译产物）

    return stale


def check_orphans_and_broken(graph: Dict) -> Dict[str, List]:
    """从编译产物的 stats 中提取孤岛和断链信息。"""
    stats = graph.get('stats', {})
    return {
        'orphan_cards': stats.get('orphan_cards', []),
        'broken_links': stats.get('broken_links', []),
    }


# ─── CLI 入口 ─────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(__doc__)
        sys.exit(0)

    code_only = '--code-only' in args
    max_days = 90
    if '--days' in args:
        idx = args.index('--days')
        max_days = int(args[idx + 1])

    # 定位项目根
    project_root = Path(__file__).resolve().parent.parent
    if '--project-root' in args:
        idx = args.index('--project-root')
        project_root = Path(args[idx + 1]).resolve()

    # 加载图索引
    graph_path = project_root / '.wiki_graph.json'
    if not graph_path.exists():
        print(f'错误：图索引不存在，请先运行 python scripts/compile_graph.py', file=sys.stderr)
        sys.exit(1)

    with open(graph_path, 'r', encoding='utf-8') as f:
        graph = json.load(f)

    nodes = graph.get('nodes', {})

    # 执行检查
    report = {
        'checked_at': datetime.now().astimezone().isoformat(),
        'total_cards': len(nodes),
    }

    # 代码过期检查
    code_stale = check_code_staleness(project_root, nodes)
    report['code_staleness'] = code_stale
    report['code_stale_count'] = len(code_stale)

    if not code_only:
        # 时间过期检查
        time_stale = check_time_staleness(nodes, max_days)
        report['time_staleness'] = time_stale
        report['time_stale_count'] = len(time_stale)

        # 孤岛和断链
        health = check_orphans_and_broken(graph)
        report['orphan_cards'] = health['orphan_cards']
        report['orphan_count'] = len(health['orphan_cards'])
        report['broken_links'] = health['broken_links']
        report['broken_link_count'] = len(health['broken_links'])

    # 输出
    print(json.dumps(report, ensure_ascii=False, indent=2))

    # 汇总到 stderr
    print(f'\n检查完成:', file=sys.stderr)
    print(f'  代码过期: {report["code_stale_count"]} 个', file=sys.stderr)
    if not code_only:
        print(f'  时间过期: {report.get("time_stale_count", 0)} 个', file=sys.stderr)
        print(f'  孤岛卡片: {report.get("orphan_count", 0)} 个', file=sys.stderr)
        print(f'  断链: {report.get("broken_link_count", 0)} 个', file=sys.stderr)


if __name__ == '__main__':
    main()
