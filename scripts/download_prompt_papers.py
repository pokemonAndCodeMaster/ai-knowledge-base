import os
import time
import urllib.request
import urllib.error

# 显式清空代理，防止 WSL 动态 IP 代理卡死导致超时
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['all_proxy'] = ''

PAPERS = {
    "CoT_2022": "2201.11903",
    "ToT_2023": "2305.10601",
    "GoT_2023": "2308.09687",
    "APO_2023": "2305.03495",
    "TextGrad_2024": "2406.07496",
    "SkillOpt_2026": "2605.03816",
    "SkillOS_2026": "2605.06614",
    "SLIM_2026": "2605.05318"
}

TARGET_DIR = "/home/yyh/project/ai-knowledge-base/raw/articles/prompt_optimization"

def download_pdf(name, arxiv_id):
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    path = os.path.join(TARGET_DIR, f"{name}_{arxiv_id}.pdf")
    
    if os.path.exists(path):
        print(f"✅ [已存在] {name} ({arxiv_id})")
        return True
        
    print(f"📥 正在下载 {name} ({arxiv_id}) from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                with open(path, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"🎉 [成功] {name} 已下载至 {path}")
            time.sleep(2)  # 礼貌延迟，避免被 Arxiv 封锁
            return True
        except urllib.error.URLError as e:
            print(f"⚠️ [重试 {attempt+1}/{max_retries}] 下载失败 {name}: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"❌ [错误] 发生未知异常 {name}: {e}")
            break
            
    print(f"❌ [失败] 无法下载 {name} ({arxiv_id})")
    return False

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    success_count = 0
    for name, arxiv_id in PAPERS.items():
        if download_pdf(name, arxiv_id):
            success_count += 1
            
    print(f"\n📊 下载完毕。成功: {success_count}/{len(PAPERS)}")

if __name__ == "__main__":
    main()
