# 🦴 代码目录架构骨架 (Code Skeleton)

> 提取目标: `graphify/graphify/`
> 共包含 36 个代码文件

## 📄 graphify/graphify/__init__.py
> **模块说明**: graphify - extract · build · cluster · analyze · report.

### ⚡ 函数 (Functions)
- `def __getattr__(...):`

---

## 📄 graphify/graphify/__main__.py
> **模块说明**: graphify CLI - `graphify install` sets up the Claude Code skill.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import functools`
- `import json`
- `import os`
- `import platform`
- `import re`
- `import shutil`
- `import sys`
- `from pathlib import Path`

### ⚡ 函数 (Functions)
- `def _always_on(...):`
- `def __getattr__(...):`
- `def _default_graph_path(...):`
- `def _enforce_graph_size_cap_or_exit(...):`
- `def _check_skill_version(...):`
- `def _refresh_all_version_stamps(...):`
- `def _platform_skill_destination(...):`
- `def _packaged_skill_refs_dir(...):`
- `def _install_skill_references(...):`
- `def _copy_skill_file(...):`
- `def _remove_skill_file(...):`
- `def _project_scope_root(...):`
- `def _remove_claude_skill_registration(...):`
- `def _print_project_git_add_hint(...):`
- `def _skill_registration(...):`
- `def _replace_or_append_section(...):`
- `def _print_banner(...):`
- `def install(...):`
- `def _print_install_usage(...):`
- `def gemini_install(...):`
- `def _install_gemini_hook(...):`
- `def _uninstall_gemini_hook(...):`
- `def gemini_uninstall(...):`
- `def vscode_install(...):`
- `def vscode_uninstall(...):`
- `def _kiro_install(...):`
- `def _kiro_uninstall(...):`
- `def _antigravity_finalize(...):`
- `def _antigravity_install(...):`
- `def _antigravity_uninstall(...):`
- `def _cursor_install(...):`
- `def _cursor_uninstall(...):`
- `def _devin_rules_install(...):`
- `def _devin_rules_uninstall(...):`
- `def _strip_json_comments(...):`
- `def _load_json_like(...):`
- `def _kilo_config_path(...):`
- `def _kilo_config_write_path(...):`
- `def _install_kilo_plugin(...):`
- `def _uninstall_kilo_plugin(...):`
- `def _install_opencode_plugin(...):`
- `def _uninstall_opencode_plugin(...):`
- `def _resolve_graphify_exe(...):`
- `def _install_codex_hook(...):`
- `def _uninstall_codex_hook(...):`
- `def _agents_install(...):`
- `def _amp_legacy_cleanup(...):`
- `def _amp_install(...):`
- `def _amp_uninstall(...):`
- `def _project_install(...):`
- `def _project_uninstall(...):`
- `def _project_uninstall_all(...):`
- `def _agents_uninstall(...):`
- `def _kilo_uninstall_global(...):`
- `def _kilo_install(...):`
- `def _kilo_uninstall(...):`
- `def claude_install(...):`
- `def _install_claude_hook(...):`
- `def _uninstall_claude_hook(...):`
- `def uninstall_all(...):`
- `def claude_uninstall(...):`
- `def codebuddy_install(...):`
- `def _install_codebuddy_hook(...):`
- `def _uninstall_codebuddy_hook(...):`
- `def codebuddy_uninstall(...):`
- `def _clone_repo(...):`
- `def main(...):`

---

## 📄 graphify/graphify/affected.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `from collections import deque`
- `from dataclasses import dataclass`
- `from pathlib import Path`
- `from typing import Iterable`
- `import networkx`

### 🏗️ 类 (Classes)
- `class AffectedHit:`

### ⚡ 函数 (Functions)
- `def _node_label(...):`
- `def _format_location(...):`
- `def resolve_seed(...):`
- `def affected_nodes(...):`
- `def format_affected(...):`
- `def load_graph(...):`

---

## 📄 graphify/graphify/analyze.py
> **模块说明**: Graph analysis: god nodes (most connected), surprising connections (cross-community), suggested questions.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `from pathlib import Path`
- `import networkx`
- `from graphify.build import edge_data`
- `from graphify.detect import CODE_EXTENSIONS`
- `from graphify.detect import DOC_EXTENSIONS`
- `from graphify.detect import PAPER_EXTENSIONS`
- `from graphify.detect import IMAGE_EXTENSIONS`

### ⚡ 函数 (Functions)
- `def _cross_language(...):`
- `def _node_community_map(...):`
- `def _is_file_node(...):`
- `def _is_json_key_node(...):`
- `def god_nodes(...):`
- `def surprising_connections(...):`
- `def _is_concept_node(...):`
- `def _file_category(...):`
- `def _top_level_dir(...):`
- `def _surprise_score(...):`
- `def _cross_file_surprises(...):`
- `def _cross_community_surprises(...):`
- `def suggest_questions(...):`
- `def graph_diff(...):`
- `def find_import_cycles(...):`

---

## 📄 graphify/graphify/benchmark.py
> **模块说明**: Token-reduction benchmark - measures how much context graphify saves vs naive full-corpus approach.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import sys`
- `from pathlib import Path`
- `import networkx`
- `from networkx.readwrite import json_graph`
- `from graphify.build import edge_data`
- `from graphify.serve import _query_terms`

### ⚡ 函数 (Functions)
- `def _safe(...):`
- `def _hr(...):`
- `def _estimate_tokens(...):`
- `def _query_subgraph_tokens(...):`
- `def run_benchmark(...):`
- `def print_benchmark(...):`

---

## 📄 graphify/graphify/build.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import os`
- `import re`
- `import sys`
- `import unicodedata`
- `from pathlib import Path`
- `import networkx`
- `from validate import validate_extraction`

### ⚡ 函数 (Functions)
- `def _normalize_id(...):`
- `def _norm_source_file(...):`
- `def edge_data(...):`
- `def edge_datas(...):`
- `def build_from_json(...):`
- `def build(...):`
- `def _norm_label(...):`
- `def deduplicate_by_label(...):`
- `def build_merge(...):`
- `def prefix_graph_for_global(...):`
- `def prune_repo_from_graph(...):`

---

## 📄 graphify/graphify/cache.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import atexit`
- `import hashlib`
- `import json`
- `import os`
- `import tempfile`
- `from pathlib import Path`

### ⚡ 函数 (Functions)
- `def _body_content(...):`
- `def _stat_index_file(...):`
- `def _ensure_stat_index(...):`
- `def _flush_stat_index(...):`
- `def _normalize_path(...):`
- `def file_hash(...):`
- `def _relativize_source_files_in(...):`
- `def _absolutize_source_files_in(...):`
- `def cache_dir(...):`
- `def load_cached(...):`
- `def save_cached(...):`
- `def cached_files(...):`
- `def clear_cache(...):`
- `def check_semantic_cache(...):`
- `def save_semantic_cache(...):`

---

## 📄 graphify/graphify/callflow_html.py
> **模块说明**: callflow_html.py — Generate call-flow architecture HTML from graphify knowledge graph outputs.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import argparse`
- `import os`
- `import re`
- `import sys`
- `import hashlib`
- `from pathlib import Path`
- `from collections import Counter`
- `from collections import defaultdict`
- `from datetime import datetime`
- `from datetime import timezone`
- `from html import escape`

### 🏗️ 类 (Classes)
- `class CallflowOptions:`
- `    def __init__(...):`

### ⚡ 函数 (Functions)
- `def read_json(...):`
- `def first_present(...):`
- `def first_list(...):`
- `def to_float(...):`
- `def endpoint_id(...):`
- `def normalize_node(...):`
- `def normalize_edge(...):`
- `def _node_link_payload(...):`
- `def load_graph(...):`
- `def load_labels(...):`
- `def load_sections(...):`
- `def load_report(...):`
- `def safe_mermaid_text(...):`
- `def html_comment_text(...):`
- `def stable_ascii_id(...):`
- `def node_mermaid_id(...):`
- `def mermaid_section_id(...):`
- `def safe_file_path(...):`
- `def safe_filename(...):`
- `def infer_project_name(...):`
- `def resolve_graphify_paths(...):`
- `def is_zh(...):`
- `def pick_text(...):`
- `def detect_lang(...):`
- `def truncate_text(...):`
- `def humanize_label(...):`
- `def node_kind(...):`
- `def relation_label(...):`
- `def preferred_edges(...):`
- `def edge_score(...):`
- `def mermaid_init(...):`
- `def mermaid_class_defs(...):`
- `def build_community_index(...):`
- `def html_anchor_id(...):`
- `def normalize_communities(...):`
- `def normalize_sections(...):`
- `def label_for_community(...):`
- `def _community_text(...):`
- `def _keyword_score(...):`
- `def _rank_grouped_sections(...):`
- `def derive_sections_from_communities(...):`
- `def build_section_node_map(...):`
- `def node_in_section(...):`
- `def classify_edges(...):`
- `def should_include_edge(...):`
- `def node_degree_scores(...):`
- `def node_importance(...):`
- `def select_diagram_nodes(...):`
- `def node_label(...):`
- `def group_nodes_by_file(...):`
- `def section_edge_summary(...):`
- `def generate_overview_graph(...):`
- `def generate_section_flowchart(...):`
- `def generate_nav(...):`
- `def node_display_name(...):`
- `def format_node_refs(...):`
- `def generate_call_table_rows(...):`
- `def _suggest_tag(...):`
- `def _describe_node(...):`
- `def generate_header(...):`
- `def derive_flow_chain(...):`
- `def generate_overview_cards(...):`
- `def section_keywords(...):`
- `def generate_section_intro(...):`
- `def generate_section_cards(...):`
- `def _report_highlights(...):`
- `def write_callflow_html(...):`
- `def main(...):`

---

## 📄 graphify/graphify/cluster.py
> **模块说明**: Community detection on NetworkX graphs. Uses Leiden (graspologic) if available, falls back to Louvain (networkx). Splits oversized communities. Returns cohesion scores.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import contextlib`
- `import inspect`
- `import io`
- `import json`
- `import sys`
- `import networkx`

### ⚡ 函数 (Functions)
- `def _suppress_output(...):`
- `def _partition(...):`
- `def cluster(...):`
- `def _split_community(...):`
- `def cohesion_score(...):`
- `def score_all(...):`
- `def remap_communities_to_previous(...):`

---

## 📄 graphify/graphify/dedup.py
> **模块说明**: Entity deduplication pipeline for graphify knowledge graphs.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import math`
- `import re`
- `import unicodedata`
- `from collections import defaultdict`
- `from datasketch import MinHash`
- `from datasketch import MinHashLSH`
- `from rapidfuzz.distance import JaroWinkler`

### 🏗️ 类 (Classes)
- `class _UF:`
- `    def __init__(...):`
- `    def find(...):`
- `    def union(...):`
- `    def components(...):`

### ⚡ 函数 (Functions)
- `def _norm(...):`
- `def _entropy(...):`
- `def _shingles(...):`
- `def _make_minhash(...):`
- `def _is_variant_pair(...):`
- `def _short_label_blocked(...):`
- `def _is_code(...):`
- `def deduplicate_entities(...):`
- `def _pick_winner(...):`
- `def _llm_tiebreak(...):`

---

## 📄 graphify/graphify/detect.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import fnmatch`
- `import json`
- `import os`
- `import re`
- `import shlex`
- `from enum import Enum`
- `from pathlib import Path`
- `from graphify.google_workspace import GOOGLE_WORKSPACE_EXTENSIONS`
- `from graphify.google_workspace import convert_google_workspace_file`
- `from graphify.google_workspace import google_workspace_enabled`

### 🏗️ 类 (Classes)
- `class FileType(str, Enum):`

### ⚡ 函数 (Functions)
- `def _file_within_size_cap(...):`
- `def _zip_within_caps(...):`
- `def _generic_keyword_hit(...):`
- `def _is_sensitive(...):`
- `def _looks_like_paper(...):`
- `def _split_env_s(...):`
- `def _env_command_args(...):`
- `def _shebang_interpreter(...):`
- `def _shebang_file_type(...):`
- `def classify_file(...):`
- `def extract_pdf_text(...):`
- `def docx_to_markdown(...):`
- `def xlsx_to_markdown(...):`
- `def xlsx_extract_structure(...):`
- `def convert_office_file(...):`
- `def count_words(...):`
- `def _is_noise_dir(...):`
- `def _parse_gitignore_line(...):`
- `def _find_vcs_root(...):`
- `def _load_graphifyignore(...):`
- `def _is_ignored(...):`
- `def _load_graphifyinclude(...):`
- `def _is_included(...):`
- `def _could_contain_included_path(...):`
- `def _auto_follow_symlinks(...):`
- `def detect(...):`
- `def _md5_file(...):`
- `def _to_relative_for_storage(...):`
- `def _to_absolute_from_storage(...):`
- `def load_manifest(...):`
- `def save_manifest(...):`
- `def detect_incremental(...):`

---

## 📄 graphify/graphify/diagnostics.py
> **模块说明**: Read-only diagnostics for MultiDiGraph readiness.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import re`
- `from collections import Counter`
- `from collections import defaultdict`
- `from copy import deepcopy`
- `from pathlib import Path`
- `from typing import Any`
- `import networkx`

### ⚡ 函数 (Functions)
- `def _safe_text(...):`
- `def _edge_list(...):`
- `def _node_ids(...):`
- `def _canonical_edge(...):`
- `def _exact_signature(...):`
- `def _count_extra(...):`
- `def _variant_group_count(...):`
- `def _tuple_arity_from_annotation(...):`
- `def scan_producer_suppression_sites(...):`
- `def diagnose_extraction(...):`
- `def _read_json_file(...):`
- `def diagnose_file(...):`
- `def format_diagnostic_json(...):`
- `def format_diagnostic_report(...):`

---

## 📄 graphify/graphify/export.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import hashlib`
- `import html`
- `import json`
- `import math`
- `import os`
- `import re`
- `import shutil`
- `from collections import Counter`
- `from datetime import date`
- `from pathlib import Path`
- `import networkx`
- `from networkx.readwrite import json_graph`
- `from graphify.security import sanitize_label`
- `from graphify.analyze import _node_community_map`
- `from graphify.build import edge_data`

### ⚡ 函数 (Functions)
- `def backup_if_protected(...):`
- `def _obsidian_tag(...):`
- `def _strip_diacritics(...):`
- `def _yaml_str(...):`
- `def _viz_node_limit(...):`
- `def _html_styles(...):`
- `def _hyperedge_script(...):`
- `def _html_script(...):`
- `def attach_hyperedges(...):`
- `def _git_head(...):`
- `def to_json(...):`
- `def prune_dangling_edges(...):`
- `def _cypher_escape(...):`
- `def _cypher_label(...):`
- `def to_cypher(...):`
- `def to_html(...):`
- `def _cap_filename(...):`
- `def to_obsidian(...):`
- `def to_canvas(...):`
- `def push_to_neo4j(...):`
- `def to_graphml(...):`
- `def to_svg(...):`

---

## 📄 graphify/graphify/extract.py
> **模块说明**: Deterministic structural extraction from source code using tree-sitter. Outputs nodes+edges dicts.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import importlib`
- `import json`
- `import os`
- `import re`
- `import sys`
- `import unicodedata`
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from pathlib import Path`
- `from typing import Any`
- `from typing import Callable`
- `from cache import load_cached`
- `from cache import save_cached`
- `from mcp_ingest import extract_mcp_config`
- `from mcp_ingest import is_mcp_config_path`

### 🏗️ 类 (Classes)
- `class LanguageConfig:`
- `class _SymbolDeclarationFact:`
- `class _SymbolImportFact:`
- `class _SymbolAliasFact:`
- `class _SymbolExportFact:`
- `class _StarExportFact:`
- `class _SymbolUseFact:`
- `class _SymbolResolutionFacts:`

### ⚡ 函数 (Functions)
- `def _raise_recursion_limit(...):`
- `def _safe_extract(...):`
- `def _make_id(...):`
- `def _file_stem(...):`
- `def _file_node_id(...):`
- `def _source_location(...):`
- `def _semantic_reference_edge(...):`
- `def _resolve_js_import_path(...):`
- `def _strip_jsonc(...):`
- `def _read_tsconfig_aliases(...):`
- `def _load_tsconfig_aliases(...):`
- `def _find_workspace_root(...):`
- `def _workspace_globs(...):`
- `def _load_workspace_packages(...):`
- `def _package_entry_candidates(...):`
- `def _resolve_workspace_import(...):`
- `def _resolve_js_module_path(...):`
- `def _read_text(...):`
- `def _python_collect_type_refs(...):`
- `def _csharp_pre_scan_interfaces(...):`
- `def _csharp_classify_base(...):`
- `def _csharp_collect_type_refs(...):`
- `def _csharp_attribute_names(...):`
- `def _java_collect_type_refs(...):`
- `def _java_method_annotation_names(...):`
- `def _go_collect_type_refs(...):`
- `def _rust_collect_type_refs(...):`
- `def _php_name_text(...):`
- `def _php_collect_type_refs(...):`
- `def _php_method_return_type_node(...):`
- `def _kotlin_user_type_name(...):`
- `def _kotlin_collect_type_refs(...):`
- `def _kotlin_property_type_node(...):`
- `def _kotlin_function_return_type_node(...):`
- `def _swift_declaration_keyword(...):`
- `def _swift_pre_scan(...):`
- `def _swift_classify_base(...):`
- `def _swift_user_type_name(...):`
- `def _swift_collect_type_refs(...):`
- `def _swift_property_type_node(...):`
- `def _c_collect_type_refs(...):`
- `def _cpp_collect_type_refs(...):`
- `def _scala_collect_type_refs(...):`
- `def _python_collect_param_refs(...):`
- `def _resolve_name(...):`
- `def _find_body(...):`
- `def _import_python(...):`
- `def _resolve_js_import_target(...):`
- `def _import_js(...):`
- `def _dynamic_import_js(...):`
- `def _import_java(...):`
- `def _resolve_c_include_path(...):`
- `def _import_c(...):`
- `def _import_csharp(...):`
- `def _import_kotlin(...):`
- `def _import_scala(...):`
- `def _import_php(...):`
- `def _get_c_func_name(...):`
- `def _get_cpp_func_name(...):`
- `def _find_require_call(...):`
- `def _require_imports_js(...):`
- `def _js_extra_walk(...):`
- `def _csharp_extra_walk(...):`
- `def _swift_extra_walk(...):`
- `def _resolve_lua_import_target(...):`
- `def _import_lua(...):`
- `def _import_swift(...):`
- `def _read_csharp_type_name(...):`
- `def _extract_generic(...):`
- `def _is_autogenerated_python(...):`
- `def _extract_python_rationale(...):`
- `def extract_python(...):`
- `def extract_js(...):`
- `def extract_svelte(...):`
- `def extract_astro(...):`
- `def extract_java(...):`
- `def _is_spock_file(...):`
- `def _extract_spock_fallback(...):`
- `def extract_groovy(...):`
- `def extract_c(...):`
- `def extract_cpp(...):`
- `def extract_ruby(...):`
- `def extract_csharp(...):`
- `def extract_apex(...):`
- `def extract_kotlin(...):`
- `def extract_scala(...):`
- `def extract_php(...):`
- `def extract_blade(...):`
- `def extract_dart(...):`
- `def extract_verilog(...):`
- `def extract_sql(...):`
- `def extract_lua(...):`
- `def extract_swift(...):`
- `def extract_julia(...):`
- `def _cpp_preprocess(...):`
- `def extract_fortran(...):`
- `def extract_go(...):`
- `def extract_rust(...):`
- `def extract_zig(...):`
- `def extract_powershell(...):`
- `def _source_key(...):`
- `def _disambiguate_colliding_node_ids(...):`
- `def _node_label_key(...):`
- `def _is_type_like_definition(...):`
- `def _rewire_unique_stub_nodes(...):`
- `def _js_source_path(...):`
- `def _apply_symbol_resolution_facts(...):`
- `def _parse_js_tree(...):`
- `def _walk_js_tree(...):`
- `def _js_module_specifier(...):`
- `def _js_named_specifiers(...):`
- `def _js_export_clause(...):`
- `def _js_export_statement_is_star(...):`
- `def _js_lexical_aliases(...):`
- `def _js_exported_declaration_names(...):`
- `def _js_top_level_function_bodies(...):`
- `def _js_call_identifier(...):`
- `def _ts_heritage_clause_entries(...):`
- `def _ts_collect_type_refs(...):`
- `def _ts_walk_class_members(...):`
- `def _collect_js_symbol_resolution_facts(...):`
- `def _parse_python_tree(...):`
- `def _walk_python_tree(...):`
- `def _python_import_from_module(...):`
- `def _python_imported_names(...):`
- `def _resolve_python_module_path(...):`
- `def _python_top_level_function_bodies(...):`
- `def _python_call_identifier(...):`
- `def _collect_python_symbol_resolution_facts(...):`
- `def _augment_symbol_resolution_edges(...):`
- `def _augment_js_reexport_edges(...):`
- `def _resolve_cross_file_imports(...):`
- `def _merge_swift_extensions(...):`
- `def _resolve_cross_file_java_imports(...):`
- `def extract_objc(...):`
- `def extract_elixir(...):`
- `def extract_markdown(...):`
- `def _pascal_project_root(...):`
- `def _pascal_resolve_unit(...):`
- `def _pascal_resolve_class(...):`
- `def _pascal_strip_comments(...):`
- `def _pascal_split_sections(...):`
- `def _pascal_split_uses(...):`
- `def _pascal_split_bases(...):`
- `def _pascal_find_body(...):`
- `def _extract_pascal_regex(...):`
- `def extract_pascal(...):`
- `def extract_lazarus_form(...):`
- `def extract_delphi_form(...):`
- `def _project_xml_is_safe(...):`
- `def extract_lazarus_package(...):`
- `def _check_tree_sitter_version(...):`
- `def extract_bash(...):`
- `def extract_sln(...):`
- `def extract_slnx(...):`
- `def extract_csproj(...):`
- `def extract_razor(...):`
- `def extract_json(...):`
- `def extract_dm(...):`
- `def _read_dmi_description(...):`
- `def extract_dmi(...):`
- `def _split_dmm_tile(...):`
- `def _dmm_type_path(...):`
- `def extract_dmm(...):`
- `def extract_dmf(...):`
- `def extract_terraform(...):`
- `def _get_extractor(...):`
- `def _extract_single_file(...):`
- `def _extract_parallel(...):`
- `def _extract_sequential(...):`
- `def extract(...):`
- `def collect_files(...):`

---

## 📄 graphify/graphify/global_graph.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import hashlib`
- `import sys`
- `from datetime import datetime`
- `from datetime import timezone`
- `from pathlib import Path`
- `import networkx`
- `from networkx.readwrite import json_graph`

### ⚡ 函数 (Functions)
- `def _load_manifest(...):`
- `def _save_manifest(...):`
- `def _load_global_graph(...):`
- `def _save_global_graph(...):`
- `def _file_hash(...):`
- `def global_add(...):`
- `def global_remove(...):`
- `def global_list(...):`
- `def global_path(...):`

---

## 📄 graphify/graphify/google_workspace.py
> **模块说明**: Optional Google Workspace shortcut export support.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import hashlib`
- `import json`
- `import os`
- `import re`
- `import shutil`
- `import subprocess`
- `import tempfile`
- `import urllib.parse`
- `from pathlib import Path`
- `from typing import Callable`
- `from typing import Any`

### ⚡ 函数 (Functions)
- `def google_workspace_enabled(...):`
- `def _safe_yaml_str(...):`
- `def _extract_file_id_from_url(...):`
- `def _extract_resource_key(...):`
- `def read_google_shortcut(...):`
- `def _run_gws_export(...):`
- `def _sidecar_path(...):`
- `def _with_frontmatter(...):`
- `def convert_google_workspace_file(...):`

---

## 📄 graphify/graphify/hooks.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import configparser`
- `import re`
- `import sys`
- `from pathlib import Path`

### ⚡ 函数 (Functions)
- `def _detached_launch(...):`
- `def _git_root(...):`
- `def _hooks_dir(...):`
- `def _install_hook(...):`
- `def _uninstall_hook(...):`
- `def _user_hooks_dir(...):`
- `def install(...):`
- `def uninstall(...):`
- `def status(...):`

---

## 📄 graphify/graphify/ingest.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import re`
- `import urllib.error`
- `import urllib.parse`
- `from datetime import datetime`
- `from datetime import timezone`
- `from pathlib import Path`
- `from graphify.security import safe_fetch`
- `from graphify.security import safe_fetch_text`
- `from graphify.security import validate_url`

### ⚡ 函数 (Functions)
- `def _yaml_str(...):`
- `def _safe_filename(...):`
- `def _detect_url_type(...):`
- `def _fetch_html(...):`
- `def _html_to_markdown(...):`
- `def _fetch_tweet(...):`
- `def _fetch_webpage(...):`
- `def _fetch_arxiv(...):`
- `def _download_binary(...):`
- `def ingest(...):`
- `def save_query_result(...):`

---

## 📄 graphify/graphify/llm.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import base64`
- `import hashlib`
- `import json`
- `import os`
- `import re`
- `import sys`
- `import time`
- `from collections.abc import Callable`
- `from concurrent.futures import ThreadPoolExecutor`
- `from concurrent.futures import as_completed`
- `from dataclasses import dataclass`
- `from dataclasses import replace`
- `from pathlib import Path`

### 🏗️ 类 (Classes)
- `class _ImageRef:`
- `    def b64(...):`
- `    def bedrock_format(...):`

### ⚡ 函数 (Functions)
- `def _get_tokenizer(...):`
- `def _custom_providers_path(...):`
- `def provider_base_url_ok(...):`
- `def _load_custom_providers(...):`
- `def _resolve_max_tokens(...):`
- `def _resolve_api_timeout(...):`
- `def _extraction_system(...):`
- `def _file_to_text(...):`
- `def _neutralise_injection_sentinels(...):`
- `def _wrap_untrusted(...):`
- `def _read_files(...):`
- `def _is_vision_image(...):`
- `def _partition_semantic_files(...):`
- `def _build_image_refs(...):`
- `def _strip_pixels(...):`
- `def _backend_supports_vision(...):`
- `def _image_notes(...):`
- `def _with_image_notes(...):`
- `def _anthropic_content(...):`
- `def _openai_content(...):`
- `def _bedrock_content(...):`
- `def _parse_llm_json(...):`
- `def _response_is_hollow(...):`
- `def _backend_env_keys(...):`
- `def _get_backend_api_key(...):`
- `def _format_backend_env_keys(...):`
- `def _default_model_for_backend(...):`
- `def _backend_pkg_hint(...):`
- `def _call_openai_compat(...):`
- `def _call_claude(...):`
- `def _call_claude_cli(...):`
- `def _azure_client(...):`
- `def _call_azure(...):`
- `def _call_bedrock(...):`
- `def extract_files_direct(...):`
- `def _estimate_file_tokens(...):`
- `def _pack_chunks_by_tokens(...):`
- `def _looks_like_context_exceeded(...):`
- `def _extract_with_adaptive_retry(...):`
- `def extract_corpus_parallel(...):`
- `def _merge_into(...):`
- `def _call_llm(...):`
- `def estimate_cost(...):`
- `def _ollama_host_is_link_local_or_metadata(...):`
- `def _validate_ollama_base_url(...):`
- `def detect_backend(...):`
- `def _placeholder_community_labels(...):`
- `def _community_label_lines(...):`
- `def _parse_label_response(...):`
- `def label_communities(...):`
- `def generate_community_labels(...):`

---

## 📄 graphify/graphify/manifest.py

### 📦 依赖 (Imports)
- `from graphify.detect import save_manifest`
- `from graphify.detect import load_manifest`
- `from graphify.detect import detect_incremental`

---

## 📄 graphify/graphify/mcp_ingest.py
> **模块说明**: mcp_ingest.py — Extract MCP (Model Context Protocol) server configuration files.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import re`
- `import unicodedata`
- `from pathlib import Path`
- `from typing import Any`
- `from graphify.security import sanitize_label`

### ⚡ 函数 (Functions)
- `def is_mcp_config_path(...):`
- `def extract_mcp_config(...):`
- `def _emit_server(...):`
- `def _detect_package_from_args(...):`
- `def _strip_version(...):`
- `def _add_node(...):`
- `def _add_edge(...):`
- `def _make_id(...):`
- `def _file_stem(...):`

---

## 📄 graphify/graphify/multigraph_compat.py
> **模块说明**: Runtime compatibility probe for Graphify MultiDiGraph mode.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `from collections.abc import Callable`
- `from dataclasses import dataclass`
- `from functools import lru_cache`
- `import sys`
- `from typing import Any`
- `import networkx`
- `from networkx.readwrite import json_graph`

### 🏗️ 类 (Classes)
- `class CapabilityCheck:`
- `class MultigraphCapabilityResult:`
- `    def ok(...):`
- `    def failed(...):`
- `    def error_message(...):`

### ⚡ 函数 (Functions)
- `def _check(...):`
- `def _build_probe_graph(...):`
- `def _probe_keyed_parallel_edges(...):`
- `def _probe_node_link_round_trip(...):`
- `def _probe_duplicate_key_overwrite_semantics(...):`
- `def _probe_reserved_key_attr_rejected(...):`
- `def _probe_remove_edges_from_two_tuple_semantics(...):`
- `def _probe_to_undirected_preserves_multigraph_type(...):`
- `def probe_multigraph_capabilities(...):`
- `def require_multigraph_capabilities(...):`

---

## 📄 graphify/graphify/pg_introspect.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `from pathlib import Path`
- `from graphify.extract import extract_sql`

### ⚡ 函数 (Functions)
- `def _quote_ident(...):`
- `def introspect_postgres(...):`

---

## 📄 graphify/graphify/prs.py
> **模块说明**: graphify prs — graph-aware PR dashboard.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import os`
- `import re`
- `import subprocess`
- `import sys`
- `from collections import defaultdict`
- `from concurrent.futures import ThreadPoolExecutor`
- `from concurrent.futures import as_completed`
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from datetime import datetime`
- `from datetime import timezone`
- `from pathlib import Path`

### 🏗️ 类 (Classes)
- `class PRInfo:`
- `    def status(...):`
- `    def days_old(...):`
- `    def blast_radius(...):`

### ⚡ 函数 (Functions)
- `def _c(...):`
- `def green(...):`
- `def red(...):`
- `def yellow(...):`
- `def cyan(...):`
- `def bold(...):`
- `def dim(...):`
- `def magenta(...):`
- `def _pad(...):`
- `def _classify(...):`
- `def _status_color(...):`
- `def _ci_icon(...):`
- `def _gh(...):`
- `def _detect_default_branch(...):`
- `def _parse_ci(...):`
- `def fetch_prs(...):`
- `def fetch_pr_files(...):`
- `def _path_match(...):`
- `def compute_pr_impact(...):`
- `def format_prs_text(...):`
- `def fetch_worktrees(...):`
- `def _load_graph_json(...):`
- `def build_community_labels(...):`
- `def attach_graph_impact(...):`
- `def _truncate(...):`
- `def render_dashboard(...):`
- `def render_worktrees(...):`
- `def render_conflicts(...):`
- `def render_pr_detail(...):`
- `def _resolve_triage_backend(...):`
- `def triage_with_opus(...):`
- `def cmd_prs(...):`

---

## 📄 graphify/graphify/querylog.py
> **模块说明**: Query logging for graphify — append-only JSONL, fail-silent.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import os`
- `import re`
- `import time`
- `from datetime import datetime`
- `from datetime import timezone`
- `from pathlib import Path`
- `from typing import Any`

### ⚡ 函数 (Functions)
- `def _log_path(...):`
- `def _log_responses(...):`
- `def nodes_from_result(...):`
- `def log_query(...):`

---

## 📄 graphify/graphify/report.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import re`
- `from datetime import date`
- `import networkx`

### ⚡ 函数 (Functions)
- `def _safe_community_name(...):`
- `def generate(...):`

---

## 📄 graphify/graphify/scip_ingest.py
> **模块说明**: scip_ingest.py — SCIP JSON ingestion (simplified subset).

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import hashlib`
- `import re`
- `from typing import Any`
- `from graphify.security import sanitize_metadata`

### ⚡ 函数 (Functions)
- `def ingest_scip_json(...):`
- `def _emit_symbol_node(...):`
- `def _emit_relationships(...):`
- `def _resolve_relationship_target(...):`
- `def _is_true(...):`
- `def _scip_relation_for(...):`
- `def _first_occurrence_line(...):`
- `def _coerce_str(...):`
- `def _make_scip_node_id(...):`
- `def _scip_kind_to_file_type(...):`
- `def _build_scip_metadata(...):`

---

## 📄 graphify/graphify/security.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import html`
- `import http.client`
- `import os`
- `import re`
- `import urllib.error`
- `import urllib.parse`
- `import urllib.request`
- `from collections.abc import Mapping`
- `from pathlib import Path`
- `from typing import Any`
- `import ipaddress`
- `import socket`

### 🏗️ 类 (Classes)
- `class _SSRFGuardedHTTPConnection:`
- `    def connect(...):`
- `class _SSRFGuardedHTTPSConnection:`
- `    def connect(...):`
- `class _SSRFGuardedHTTPHandler:`
- `    def http_open(...):`
- `class _SSRFGuardedHTTPSHandler:`
- `    def https_open(...):`
- `class _NoFileRedirectHandler:`
- `    def redirect_request(...):`

### ⚡ 函数 (Functions)
- `def _max_graph_file_bytes(...):`
- `def _ip_is_blocked(...):`
- `def validate_url(...):`
- `def _resolve_and_validate(...):`
- `def _build_opener(...):`
- `def safe_fetch(...):`
- `def safe_fetch_text(...):`
- `def validate_graph_path(...):`
- `def check_graph_file_size_cap(...):`
- `def sanitize_label(...):`
- `def _sanitize_metadata_string(...):`
- `def _sanitize_metadata_value(...):`
- `def sanitize_metadata(...):`

---

## 📄 graphify/graphify/semantic_cleanup.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import re`
- `from pathlib import Path`

### ⚡ 函数 (Functions)
- `def validate_semantic_fragment(...):`
- `def load_validated_semantic_fragment(...):`
- `def _validate_semantic_id(...):`
- `def sanitize_semantic_fragment(...):`
- `def _is_sentence_like_rationale_label(...):`
- `def _append_rationale_attr(...):`

---

## 📄 graphify/graphify/serve.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import json`
- `import math`
- `import re`
- `import sys`
- `from pathlib import Path`
- `import networkx`
- `from networkx.readwrite import json_graph`
- `from graphify.security import sanitize_label`
- `from graphify.security import check_graph_file_size_cap`
- `from graphify.build import edge_data`

### 🏗️ 类 (Classes)
- `class _MCPASGIApp:`
- `    def __init__(...):`
- `class _ApiKeyMiddleware:`
- `    def __init__(...):`

### ⚡ 函数 (Functions)
- `def _load_graph(...):`
- `def _communities_from_graph(...):`
- `def _strip_diacritics(...):`
- `def _search_tokens(...):`
- `def _has_chinese(...):`
- `def _segment_chinese(...):`
- `def _is_searchable(...):`
- `def _query_terms(...):`
- `def _compute_idf(...):`
- `def _score_nodes(...):`
- `def _pick_seeds(...):`
- `def _normalize_context_filters(...):`
- `def _infer_context_filters(...):`
- `def _resolve_context_filters(...):`
- `def _filter_graph_by_context(...):`
- `def _bfs(...):`
- `def _dfs(...):`
- `def _subgraph_to_text(...):`
- `def _query_graph_text(...):`
- `def _find_node(...):`
- `def _filter_blank_stdin(...):`
- `def _build_server(...):`
- `def serve(...):`
- `def _build_http_app(...):`
- `def serve_http(...):`
- `def _main(...):`

---

## 📄 graphify/graphify/symbol_resolution.py
> **模块说明**: Deterministic symbol indexing and conservative cross-file resolution helpers.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import ast`
- `import re`
- `import unicodedata`
- `from dataclasses import dataclass`
- `from pathlib import Path`
- `from collections.abc import Sequence`
- `from typing import Any`
- `from graphify.security import sanitize_metadata`

### 🏗️ 类 (Classes)
- `class ImportedSymbol:`

### ⚡ 函数 (Functions)
- `def normalise_callable_label(...):`
- `def node_is_resolvable_symbol(...):`
- `def build_label_index(...):`
- `def existing_edge_pairs(...):`
- `def iter_raw_calls(...):`
- `def _module_stem(...):`
- `def parse_python_import_aliases(...):`
- `def _node_source_stem(...):`
- `def build_python_symbol_index(...):`
- `def find_unique_python_symbol(...):`
- `def resolve_python_import_guided_calls(...):`
- `def resolve_cross_file_raw_calls(...):`
- `def _bash_make_id(...):`
- `def _bash_file_stem(...):`
- `def _file_node_id_for_path(...):`
- `def resolve_bash_source_edges(...):`

---

## 📄 graphify/graphify/transcribe.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import os`
- `from pathlib import Path`

### ⚡ 函数 (Functions)
- `def _model_name(...):`
- `def _get_whisper(...):`
- `def _get_yt_dlp(...):`
- `def is_url(...):`
- `def download_audio(...):`
- `def build_whisper_prompt(...):`
- `def transcribe(...):`
- `def transcribe_all(...):`

---

## 📄 graphify/graphify/tree_html.py
> **模块说明**: tree_html — emit a D3 v7 collapsible-tree HTML view of a graph.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import html`
- `import json`
- `from collections import defaultdict`
- `from pathlib import Path`
- `from typing import Any`
- `from typing import Dict`
- `from typing import List`
- `from typing import Optional`

### ⚡ 函数 (Functions)
- `def _common_root(...):`
- `def _make_truncation_leaf(...):`
- `def build_tree(...):`
- `def emit_html(...):`
- `def write_tree_html(...):`

---

## 📄 graphify/graphify/validate.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`

### ⚡ 函数 (Functions)
- `def validate_extraction(...):`
- `def assert_valid(...):`

---

## 📄 graphify/graphify/watch.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import contextlib`
- `import json`
- `import os`
- `import re`
- `import sys`
- `import time`
- `from pathlib import Path`
- `from graphify.detect import CODE_EXTENSIONS`
- `from graphify.detect import DOC_EXTENSIONS`
- `from graphify.detect import PAPER_EXTENSIONS`
- `from graphify.detect import IMAGE_EXTENSIONS`
- `from graphify.detect import _load_graphifyignore`
- `from graphify.detect import _is_ignored`

### ⚡ 函数 (Functions)
- `def _queue_pending(...):`
- `def _drain_pending(...):`
- `def _merge_changed_paths(...):`
- `def _rebuild_lock(...):`
- `def _apply_resource_limits(...):`
- `def _git_head(...):`
- `def _report_root_label(...):`
- `def _relativize_source_files(...):`
- `def _node_community_map(...):`
- `def _canonical_graph_for_compare(...):`
- `def _canonical_topology_for_compare(...):`
- `def _topology_from_graph(...):`
- `def _check_shrink(...):`
- `def _report_for_compare(...):`
- `def _json_text(...):`
- `def _rebuild_code(...):`
- `def check_update(...):`
- `def _notify_only(...):`
- `def _has_non_code(...):`
- `def watch(...):`

---

## 📄 graphify/graphify/wiki.py

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `from collections import Counter`
- `from pathlib import Path`
- `import networkx`
- `from graphify.build import edge_data`

### ⚡ 函数 (Functions)
- `def _safe_filename(...):`
- `def _cross_community_links(...):`
- `def _community_article(...):`
- `def _god_node_article(...):`
- `def _index_md(...):`
- `def to_wiki(...):`

---
