import os
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import time

def get_arxiv_title(arxiv_id):
    """
    通过 Arxiv API 获取论文的英文标题
    """
    # 尝试使用镜像加速
    url = f"http://cn.arxiv.org/api/query?id_list={arxiv_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        # XML namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', ns)
        if entry is not None:
            title_node = entry.find('atom:title', ns)
            if title_node is not None:
                title = title_node.text.strip().replace('\n', ' ')
                title = re.sub(r'\s+', ' ', title)
                return title
    except Exception as e:
        print(f"Error fetching title for {arxiv_id}: {e}")
    return None

def clean_filename(filename):
    # 保留字母、数字、点、横杠、下划线和空格
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.replace(" ", "_")
    return filename

def download_file(url, output_path):
    # 替换为 cn.arxiv.org 镜像加速
    if "arxiv.org/pdf" in url:
        url = url.replace("arxiv.org/pdf", "cn.arxiv.org/pdf")
        if not url.endswith(".pdf"):
            url = url + ".pdf"
            
    print(f"Downloading {url} to {output_path}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        # 创建父目录
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"✅ Successfully downloaded to {output_path}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error downloading {url}: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"❌ URL Error downloading {url}: {e.reason}")
    except Exception as e:
        print(f"❌ General Error downloading {url}: {e}")
    return False

def parse_inventory(filepath):
    # 解析 markdown 表格
    if not os.path.exists(filepath):
        return []
        
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if line.startswith("|") and idx > 1: # 排除前两行表头
            parts = [p.strip() for p in line.split("|")][1:-1]
            if len(parts) >= 6 and parts[0] != "Title":
                entries.append({
                    "line_idx": idx,
                    "title": parts[0],
                    "type": parts[1],
                    "url": parts[2],
                    "exists": parts[3],
                    "path": parts[4],
                    "id": parts[5],
                    "raw_line": line
                })
    return entries, lines

def run_download_workflow(inventory_file, raw_dir):
    entries, lines = parse_inventory(inventory_file)
    print(f"Parsed {len(entries)} entries from {inventory_file}")
    
    modified = False
    
    for entry in entries:
        # 只处理 PDF 并且本地不存在，且有 URL 的条目
        if entry["type"].lower() == "pdf" and "❌" in entry["exists"] and entry["url"]:
            url = entry["url"]
            title = entry["title"]
            
            # 检测是否是 Arxiv 链接
            arxiv_match = re.search(r'arxiv\.org/pdf/([0-9]+\.[0-9]+)', url)
            if arxiv_match:
                arxiv_id = arxiv_match.group(1)
                print(f"Found Arxiv ID: {arxiv_id} for {title}")
                # 尝试获取 Arxiv 真实标题
                paper_title = get_arxiv_title(arxiv_id)
                if not paper_title:
                    paper_title = title if not title.startswith("http") else f"Arxiv_{arxiv_id}"
            else:
                # 非 arxiv
                paper_title = title
                if paper_title.startswith("http"):
                    # 从 url 提取
                    paper_title = url.split("/")[-1].replace(".pdf", "")
            
            # 安全文件名与目录名
            paper_title_clean = clean_filename(paper_title)
            # 如果标题太长，截断它
            if len(paper_title_clean) > 80:
                paper_title_clean = paper_title_clean[:80]
                
            dir_name = os.path.join(raw_dir, "articles", paper_title_clean)
            pdf_path = os.path.join(dir_name, f"{paper_title_clean}.pdf")
            
            # 执行下载
            success = download_file(url, pdf_path)
            if success:
                # 更新这一行的 markdown
                # 表格列：| Title | Type | URL | Exists Locally? | Path | ID | ... |
                # 重新构造这一行
                parts = [p.strip() for p in entry["raw_line"].split("|")]
                parts[4] = "✅ Yes" # Exists Locally
                parts[5] = f"raw/articles/{paper_title_clean}" # Path
                
                new_line = "| " + " | ".join(parts[1:-1]) + " |\n"
                lines[entry["line_idx"]] = new_line
                modified = True
                
                # 稍微 sleep 防止被封
                time.sleep(2)
            else:
                print(f"Skipping update for {title} due to download failure.")
                
    if modified:
        with open(inventory_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Updated inventory: {inventory_file}")

if __name__ == "__main__":
    raw_dir = "/home/yyh/project/ai-knowledge-base/raw"
    
    print("=== Downloading Multimodal Papers ===")
    run_download_workflow(os.path.join(raw_dir, "inventory_multimodal.md"), raw_dir)
    
    print("=== Downloading Agent Papers ===")
    run_download_workflow(os.path.join(raw_dir, "inventory_merged_agent.md"), raw_dir)
