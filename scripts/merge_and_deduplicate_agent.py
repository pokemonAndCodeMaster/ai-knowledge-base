import os
import re
import urllib.parse

def clean_title(title):
    # 去除多余后缀和格式
    title = re.sub(r'\\ Anthropic', '', title)
    title = re.sub(r'\\ OpenAI', '', title)
    title = re.sub(r'\| Claude', '', title)
    title = re.sub(r'\| HumanLayer Blog', '', title)
    title = re.sub(r'\| Parallel Web Systems.*', '', title)
    title = re.sub(r'\| Code Wiki', '', title)
    title = re.sub(r'\.pdf$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\.md$', '', title, flags=re.IGNORECASE)
    # 转换为小写并去除非英文字符及空格
    title = title.lower().strip()
    title = re.sub(r'[^a-z0-9]', '', title)
    return title

def extract_github_repo(url):
    if not url:
        return None
    url = url.lower()
    # 可能是 https://codewiki.google/github.com/owner/repo
    # 或者是 https://github.com/owner/repo
    match = re.search(r'github\.com/([^/]+)/([^/#\?]+)', url)
    if match:
        owner = match.group(1)
        repo = match.group(2).replace(".git", "")
        return f"{owner}/{repo}"
    return None

def normalize_url(url):
    if not url:
        return ""
    # 去除末尾斜杠
    url = url.strip().rstrip('/')
    # 标准化 codewiki 链接为 github 链接
    if "codewiki.google/github.com" in url:
        url = url.replace("https://codewiki.google/github.com", "https://github.com")
        url = url.replace("http://codewiki.google/github.com", "https://github.com")
    return url

def load_openharness_inventory(filepath):
    # 解析 inventory_openharness.md (或者是直接解析 openharness_details.json 更准)
    # 我们直接读取 JSON 文件
    import json
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    sources_raw = data[0][1]
    sources = []
    
    # 辅助找 url
    from parse_sources import find_url, determine_type
    
    for item in sources_raw:
        try:
            ids = item[0]
            source_id = ids[0] if isinstance(ids, list) and len(ids) > 0 else ""
            title = item[1]
            meta = item[2]
            url = find_url(meta)
            
            normalized_url = normalize_url(url)
            github = extract_github_repo(normalized_url)
            
            sources.append({
                "id": source_id,
                "title": title,
                "url": normalized_url,
                "github": github,
                "type": determine_type(title, url if url else ""),
                "origin": "NotebookLM"
            })
        except Exception as e:
            print(f"Error parse: {e}")
            
    return sources

def load_harness_inventory_md(filepath):
    # 解析 harness_engineering_inventory.md
    # 提取格式: - [ ] [Title](URL)
    sources = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_category = "General"
    
    for line in lines:
        if line.startswith("###"):
            current_category = line.replace("###", "").strip()
            continue
            
        match = re.search(r'-\s*\[\s*\]\s*\[(.*?)\]\((.*?)\)', line)
        if match:
            title = match.group(1).strip()
            url = match.group(2).strip()
            
            normalized_url = normalize_url(url)
            github = extract_github_repo(normalized_url)
            
            # 判定类型
            from parse_sources import determine_type
            t = determine_type(title, normalized_url)
            
            sources.append({
                "id": "",
                "title": title,
                "url": normalized_url,
                "github": github,
                "type": t,
                "origin": "awesome-list",
                "category": current_category
            })
            
    return sources

def merge_and_deduplicate(notebook_sources, awesome_sources):
    merged = []
    
    # 建立索引以去重
    # 优先使用规范化的 URL，然后是 GitHub 仓库，最后是 clean title
    url_map = {}
    github_map = {}
    title_map = {}
    
    all_sources = notebook_sources + awesome_sources
    
    # 优先放入 NotebookLM 里的 Source，因为它们有 NotebookLM 的 ID，能直接关联
    # 排序：NotebookLM 在前
    all_sources.sort(key=lambda x: 0 if x["origin"] == "NotebookLM" else 1)
    
    for src in all_sources:
        url = src["url"]
        github = src["github"]
        ct = clean_title(src["title"])
        
        # 查找是否存在重复
        dup_found = None
        
        if url and url in url_map:
            dup_found = url_map[url]
        elif github and github in github_map:
            dup_found = github_map[github]
        elif ct in title_map:
            # 标题相似度或精确匹配
            dup_found = title_map[ct]
            
        if dup_found:
            # 合并属性
            # 如果原有的 ID 为空，但新的有，则填入 ID
            if not dup_found["id"] and src["id"]:
                dup_found["id"] = src["id"]
            # 合并 origin
            if src["origin"] not in dup_found["origin"]:
                dup_found["origin"] = f"{dup_found['origin']} + {src['origin']}"
            # 如果 url 没有，填入 url
            if not dup_found["url"] and src["url"]:
                dup_found["url"] = src["url"]
            # 如果 category 没有，填入 category
            if "category" in src and "category" not in dup_found:
                dup_found["category"] = src["category"]
        else:
            # 插入新元素
            url_map[url] = src
            if github:
                github_map[github] = src
            title_map[ct] = src
            merged.append(src)
            
    return merged

def generate_merged_inventory(merged_sources, output_path, raw_dir):
    from parse_sources import check_local_existence
    
    markdown_lines = []
    markdown_lines.append("# Merged Agent Engineering & Harness Research Inventory")
    markdown_lines.append("")
    markdown_lines.append("This inventory consolidates and deduplicates sources from the **OpenHarness NotebookLM** and the **awesome-agent-harness** list.")
    markdown_lines.append("")
    markdown_lines.append("| Title | Type | URL | Exists Locally? | Path | ID | Origin | Category |")
    markdown_lines.append("|---|---|---|---|---|---|---|---|")
    
    exists_count = 0
    total_count = len(merged_sources)
    
    for src in merged_sources:
        exists, path = check_local_existence(src["title"], src["url"], raw_dir)
        exists_str = "✅ Yes" if exists else "❌ No"
        if exists:
            exists_count += 1
            
        cat = src.get("category", "General")
        markdown_lines.append(
            f"| {src['title']} | {src['type']} | {src['url']} | {exists_str} | {path} | {src['id']} | {src['origin']} | {cat} |"
        )
        
    markdown_lines.append("")
    markdown_lines.append(f"**Merged Statistics**: {exists_count}/{total_count} files exist locally ({(exists_count/total_count)*100:.2f}%)")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown_lines))
        
    print(f"Merged Inventory generated. Total items: {total_count}, exists locally: {exists_count}.")

if __name__ == "__main__":
    raw_dir = "/home/yyh/project/ai-knowledge-base/raw"
    
    notebook_sources = load_openharness_inventory(os.path.join(raw_dir, "openharness_details.json"))
    awesome_sources = load_harness_inventory_md("/home/yyh/project/ai-knowledge-base/harness_engineering_inventory.md")
    
    print(f"Loaded {len(notebook_sources)} notebook sources.")
    print(f"Loaded {len(awesome_sources)} awesome-list sources.")
    
    merged = merge_and_deduplicate(notebook_sources, awesome_sources)
    
    generate_merged_inventory(
        merged,
        os.path.join(raw_dir, "inventory_merged_agent.md"),
        raw_dir
    )
