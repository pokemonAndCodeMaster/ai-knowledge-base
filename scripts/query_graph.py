#!/usr/bin/env python3
"""
query_graph.py — 知识库图检索查询器

基于 .wiki_graph.json 的编译产物，执行 "Seed → Expand → Classify" 三阶段检索。
给定任务描述，找出所有相关知识卡片并按类型分桶、按优先级排序。

零外部依赖，纯 Python 实现（无需 jieba，用子串匹配）。

Usage:
    python scripts/query_graph.py "设计一个多Agent协作系统"
    python scripts/query_graph.py "重构知识库检索" --domains "knowledge_mgmt,agent_engineering"
    python scripts/query_graph.py "修改SKILL.md" --paths "skills/"
    python scripts/query_graph.py "设计一个多Agent协作系统" --max-hops 3
    python scripts/query_graph.py "设计一个多Agent协作系统" --top-seeds 8
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set, Optional
from collections import defaultdict


# ─── Seed 发现算法（多维加权匹配） ─────────────────────────────────

def _tokenize_simple(text: str) -> Set[str]:
    """简单分词：按标点/空格切分 + 保留原始文本用于子串匹配。
    
    对中文：保留 2-4 字的滑动窗口 n-gram 作为候选 token。
    对英文：按空格/标点切分。
    """
    tokens = set()
    # 英文词（含数字）
    tokens.update(w.lower() for w in re.findall(r'[a-zA-Z_]\w{2,}', text))
    # 中文 n-gram（2-4 字）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
    for segment in chinese_chars:
        for n in range(2, min(5, len(segment) + 1)):
            for i in range(len(segment) - n + 1):
                tokens.add(segment[i:i + n])
    return tokens


def find_seeds(
    task: str,
    nodes: Dict[str, Dict],
    opts: Dict[str, Any],
    top_k: int = 5,
) -> List[Tuple[str, float, str]]:
    """多维 Seed 发现。返回 [(path, score, match_reason), ...]。"""
    task_lower = task.lower()
    task_tokens = _tokenize_simple(task)
    scores: Dict[str, Tuple[float, List[str]]] = {}

    for path, node in nodes.items():
        score = 0.0
        reasons = []

        # 1. trigger_keywords 子串命中（权重最高）
        for kw in node.get('trigger_keywords', []):
            if kw and kw.lower() in task_lower:
                score += 3.0
                reasons.append(f'keyword:{kw}')

        # 2. title 匹配
        title = node.get('title', '').lower()
        if title and (title in task_lower or task_lower in title):
            score += 2.5
            reasons.append('title_match')
        elif title:
            # title 中的关键词匹配
            title_tokens = _tokenize_simple(title)
            overlap = task_tokens & title_tokens
            if overlap:
                bonus = min(len(overlap) * 0.5, 2.0)
                score += bonus
                reasons.append(f'title_partial:{",".join(list(overlap)[:3])}')

        # 3. tags 子串命中
        for tag in node.get('tags', []):
            if tag and tag.lower() in task_lower:
                score += 1.0
                reasons.append(f'tag:{tag}')

        # 4. domain 过滤（如果指定了 --domains）
        if opts.get('domains'):
            req_domains = set(opts['domains'])
            node_domains = set(node.get('domain', []))
            if req_domains & node_domains:
                score += 1.5
                reasons.append(f'domain:{",".join(req_domains & node_domains)}')

        # 5. affects_path / related_code 路径匹配（如果指定了 --paths）
        if opts.get('paths'):
            for ap in node.get('affects_path', []):
                for p in opts['paths']:
                    if p in ap or ap in p:
                        score += 2.5
                        reasons.append(f'affects_path:{ap}')
            for rc in node.get('related_code', []):
                for p in opts['paths']:
                    if p in rc or rc in p:
                        score += 2.5
                        reasons.append(f'related_code:{rc}')

        # 6. summary 中的关键词匹配（较低权重）
        summary = node.get('summary', '').lower()
        if summary:
            summary_tokens = _tokenize_simple(summary)
            overlap = task_tokens & summary_tokens
            if len(overlap) >= 2:
                bonus = min(len(overlap) * 0.3, 1.5)
                score += bonus
                reasons.append(f'summary_match:{len(overlap)}tokens')

        if score > 0:
            scores[path] = (score, reasons)

    # 按分数降序排列，取 top-k
    ranked = sorted(scores.items(), key=lambda x: -x[1][0])[:top_k]
    return [(path, sc, '|'.join(reasons)) for path, (sc, reasons) in ranked]


# ─── 图扩展（BFS 2 跳） ──────────────────────────────────────────

def _resolve_slug_to_path(slug: str, nodes: Dict[str, Dict]) -> Optional[str]:
    """通过 slug 查找对应的 path。"""
    for path, node in nodes.items():
        if node.get('slug') == slug:
            return path
    return None


def expand_from_seeds(
    seed_paths: List[str],
    nodes: Dict[str, Dict],
    max_hops: int = 2,
) -> Dict[str, int]:
    """从种子节点出发，BFS 扩展 max_hops 跳。返回 {path: hop_count}。"""
    visited: Dict[str, int] = {}  # path → 最小跳数
    queue: List[Tuple[str, int]] = [(p, 0) for p in seed_paths]

    while queue:
        current, hops = queue.pop(0)
        if current in visited:
            continue
        visited[current] = hops

        if hops >= max_hops:
            continue

        node = nodes.get(current)
        if not node:
            continue

        # 沿 outlinks 扩展
        for slug in node.get('outlinks', []):
            neighbor = _resolve_slug_to_path(slug, nodes)
            if neighbor and neighbor not in visited:
                queue.append((neighbor, hops + 1))

        # 沿 inlinks 扩展（反向链接也走）
        for slug in node.get('inlinks', []):
            neighbor = _resolve_slug_to_path(slug, nodes)
            if neighbor and neighbor not in visited:
                queue.append((neighbor, hops + 1))

    return visited


# ─── 优先级分配 ──────────────────────────────────────────────────

def assign_priority(node: Dict, is_seed: bool, hop_count: int) -> str:
    """根据卡片类型、是否种子、跳数，分配读取优先级。"""
    node_type = node.get('type', '')

    # pitfall / norm 无条件全文读取（它们是硬约束）
    if node_type in ('pitfall', 'norm'):
        return 'full_read'
    # code_module 全文读取（含代码引用信息）
    if node_type == 'code_module':
        return 'full_read'
    # seed 直接命中的 concept/module_doc 全文读取
    if is_seed and node_type in ('concept', 'module_doc', 'synthesis'):
        return 'full_read'
    # 1 跳内的概念/综合 → 读摘要
    if hop_count <= 1 and node_type in ('concept', 'synthesis', 'module_doc'):
        return 'summary_only'
    # 其余 → 仅列标题
    return 'title_only'


# ─── 结果分类与组装 ───────────────────────────────────────────────

def classify_results(
    expanded: Dict[str, int],
    seed_paths: Set[str],
    seed_reasons: Dict[str, str],
    nodes: Dict[str, Dict],
) -> Dict[str, Any]:
    """将扩展结果按类型分桶，按优先级排序。"""
    classified = defaultdict(list)
    suggested_read_order = []

    for path, hop_count in expanded.items():
        node = nodes.get(path)
        if not node:
            continue

        is_seed = path in seed_paths
        priority = assign_priority(node, is_seed, hop_count)
        node_type = node.get('type', 'unknown')

        entry = {
            'path': path,
            'title': node.get('title', ''),
            'type': node_type,
            'summary': node.get('summary', ''),
            'hop_count': hop_count,
            'is_seed': is_seed,
            'priority': priority,
        }
        if is_seed:
            entry['seed_reason'] = seed_reasons.get(path, '')

        classified[node_type].append(entry)
        suggested_read_order.append(entry)

    # 排序：full_read 优先 → summary_only → title_only；同优先级按跳数排序
    priority_order = {'full_read': 0, 'summary_only': 1, 'title_only': 2}
    suggested_read_order.sort(
        key=lambda x: (priority_order.get(x['priority'], 9), x['hop_count'])
    )

    return {
        'classified': dict(classified),
        'suggested_read_order': suggested_read_order,
    }


# ─── CLI 入口 ─────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args or not args:
        print(__doc__)
        sys.exit(0)

    # 解析参数
    task = args[0]
    opts: Dict[str, Any] = {}

    if '--domains' in args:
        idx = args.index('--domains')
        opts['domains'] = [d.strip() for d in args[idx + 1].split(',')]

    if '--paths' in args:
        idx = args.index('--paths')
        opts['paths'] = [p.strip() for p in args[idx + 1].split(',')]

    max_hops = 2
    if '--max-hops' in args:
        idx = args.index('--max-hops')
        max_hops = int(args[idx + 1])

    top_seeds = 5
    if '--top-seeds' in args:
        idx = args.index('--top-seeds')
        top_seeds = int(args[idx + 1])

    # 定位图索引文件
    project_root = Path(__file__).resolve().parent.parent
    if '--project-root' in args:
        idx = args.index('--project-root')
        project_root = Path(args[idx + 1]).resolve()

    graph_path = project_root / '.wiki_graph.json'
    if not graph_path.exists():
        print(f'错误：图索引文件不存在：{graph_path}', file=sys.stderr)
        print(f'请先运行：python scripts/compile_graph.py', file=sys.stderr)
        sys.exit(1)

    # 加载图索引
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph = json.load(f)

    nodes = graph.get('nodes', {})
    compiled_at = graph.get('compiled_at', 'unknown')

    # 阶段 1: Seed 发现
    seeds = find_seeds(task, nodes, opts, top_k=top_seeds)
    seed_paths = set(p for p, _, _ in seeds)
    seed_reasons = {p: r for p, _, r in seeds}

    # 阶段 2: 图扩展
    expanded = expand_from_seeds(list(seed_paths), nodes, max_hops=max_hops)

    # 阶段 3: 分类与组装
    result = classify_results(expanded, seed_paths, seed_reasons, nodes)

    # 输出
    output = {
        'task': task,
        'graph_compiled_at': compiled_at,
        'total_graph_cards': len(nodes),
        'seeds': [
            {
                'path': p,
                'title': nodes[p]['title'] if p in nodes else p,
                'score': round(s, 2),
                'reason': r,
            }
            for p, s, r in seeds
        ],
        'total_retrieved': len(expanded),
        'classified': result['classified'],
        'suggested_read_order': result['suggested_read_order'],
        'read_stats': {
            'full_read': sum(1 for e in result['suggested_read_order'] if e['priority'] == 'full_read'),
            'summary_only': sum(1 for e in result['suggested_read_order'] if e['priority'] == 'summary_only'),
            'title_only': sum(1 for e in result['suggested_read_order'] if e['priority'] == 'title_only'),
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
