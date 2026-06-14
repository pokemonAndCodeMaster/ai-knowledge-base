import json
import os
import re

def find_url(meta_list):
    """
    递归或遍历元数据列表，找出含有 'http' 开头的链接
    """
    if not isinstance(meta_list, list):
        return None
    for item in meta_list:
        if isinstance(item, list):
            # 判断是否是 [ "http..." ] 形式
            for sub in item:
                if isinstance(sub, str) and (sub.startswith('http://') or sub.startswith('https://')):
                    return sub
            # 递归查找
            res = find_url(item)
            if res:
                return res
        elif isinstance(item, str) and (item.startswith('http://') or item.startswith('https://')):
            return item
    return None

def parse_notebook_details(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return []
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    notebook_name = data[0][0]
    sources_raw = data[0][1]
    
    parsed_sources = []
    for item in sources_raw:
        # item 格式为 [ [ [id], title, meta_list ], ... ]
        try:
            ids = item[0]
            source_id = ids[0] if isinstance(ids, list) and len(ids) > 0 else ""
            title = item[1]
            meta = item[2]
            
            url = find_url(meta)
            parsed_sources.append({
                "id": source_id,
                "title": title,
                "url": url if url else ""
            })
        except Exception as e:
            print(f"Error parsing item: {item}, error: {e}")
            
    return parsed_sources

def determine_type(title, url):
    title_lower = title.lower()
    url_lower = url.lower()
    
    if "arxiv.org/pdf" in url_lower or url_lower.endswith(".pdf") or title_lower.endswith(".pdf"):
        return "PDF"
    elif "github.com" in url_lower or "code wiki" in title_lower:
        return "GitHub"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "Video"
    else:
        return "Markdown"

def check_local_existence(title, url, raw_dir):
    # 检查本地是否已经有匹配的文件
    # raw_dir 通常是 /home/yyh/project/ai-knowledge-base/raw
    title_clean = title.replace("/", "_").replace(" ", "_")
    
    # 1. 检查 articles 目录下是否有同名文件
    articles_dir = os.path.join(raw_dir, "articles")
    
    # 支持有些文章被解压为目录了
    possible_names = [
        title,
        title_clean,
        title.replace(".pdf", ""),
        title_clean.replace(".pdf", ""),
        title.replace(".md", ""),
        title_clean.replace(".md", "")
    ]
    
    for name in possible_names:
        # 检查是否直接在 raw/ 下
        if os.path.exists(os.path.join(raw_dir, name + ".md")):
            return True, os.path.join("raw", name + ".md")
        # 检查是否在 raw/articles/ 下
        if os.path.exists(os.path.join(articles_dir, name)):
            # 可能是目录
            return True, os.path.join("raw/articles", name)
        if os.path.exists(os.path.join(articles_dir, name + ".md")):
            return True, os.path.join("raw/articles", name + ".md")
            
    # 2. 如果是开源项目，检查项目根目录下是否有对应的目录
    if "github.com" in url:
        match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
        if match:
            repo_name = match.group(2).replace(".git", "")
            # 检查项目根目录是否有这个文件夹
            project_root = os.path.dirname(raw_dir)
            repo_path = os.path.join(project_root, repo_name)
            if os.path.exists(repo_path):
                return True, repo_name
                
    # 3. 检查 raw/projects/ 是否有对应的 readme
    projects_dir = os.path.join(raw_dir, "projects")
    if os.path.exists(projects_dir):
        for f in os.listdir(projects_dir):
            f_lower = f.lower()
            for name in possible_names:
                if name.lower() in f_lower:
                    return True, os.path.join("raw/projects", f)
                    
    return False, ""

def generate_inventory(details_path, output_path, raw_dir):
    sources = parse_notebook_details(details_path)
    print(f"Loaded {len(sources)} sources from {details_path}")
    
    markdown_lines = []
    markdown_lines.append(f"# NotebookLM Inventory: {os.path.basename(details_path)}")
    markdown_lines.append("")
    markdown_lines.append("| Title | Type | URL | Exists Locally? | Path | ID |")
    markdown_lines.append("|---|---|---|---|---|---|")
    
    exists_count = 0
    total_count = len(sources)
    
    for src in sources:
        t = determine_type(src["title"], src["url"])
        exists, path = check_local_existence(src["title"], src["url"], raw_dir)
        if exists:
            exists_count += 1
            exists_str = "✅ Yes"
        else:
            exists_str = "❌ No"
            
        markdown_lines.append(f"| {src['title']} | {t} | {src['url']} | {exists_str} | {path} | {src['id']} |")
        
    markdown_lines.append("")
    markdown_lines.append(f"**Total Statistics**: {exists_count}/{total_count} files exist locally ({(exists_count/total_count)*100:.2f}%)")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown_lines))
        
    print(f"Saved inventory to {output_path}. Stat: {exists_count}/{total_count} exists.")

if __name__ == "__main__":
    raw_dir = "/home/yyh/project/ai-knowledge-base/raw"
    
    generate_inventory(
        os.path.join(raw_dir, "openharness_details.json"),
        os.path.join(raw_dir, "inventory_openharness.md"),
        raw_dir
    )
    
    generate_inventory(
        os.path.join(raw_dir, "multimodal_details.json"),
        os.path.join(raw_dir, "inventory_multimodal.md"),
        raw_dir
    )
