import os
import re
from pathlib import Path

wiki_dir = Path('wiki')
index_file = Path('index.md')
log_file = Path('log.md')

index_content = index_file.read_text(encoding='utf-8')
all_md_files = list(wiki_dir.glob('**/*.md'))

unindexed_files = []
for f in all_md_files:
    if f.name == 'index.md' or f.name == 'log.md':
        continue
    rel_path = f.as_posix()
    # Check if rel_path is in index.md (URL encoded or not)
    # Simple check: just the filename
    if f.name not in index_content:
        unindexed_files.append(f)

# Find broken links
broken_links = []
link_pattern = re.compile(r'\[\[(.*?)\]\]')
all_defined_names = {f.stem for f in all_md_files}

for f in all_md_files:
    content = f.read_text(encoding='utf-8')
    links = link_pattern.findall(content)
    for link in links:
        link_name = link.split('|')[0].strip()
        # handle paths like sources/mit_notebooklm_48h
        link_name = link_name.split('/')[-1]
        if link_name not in all_defined_names and link_name + '.md' not in all_defined_names:
             broken_links.append((f.as_posix(), link_name))

print("Unindexed files:", [f.as_posix() for f in unindexed_files])
print("Broken links:", broken_links)

# Update Index
concepts = []
synthesis = []
entities = []
sources = []

for f in unindexed_files:
    content = f.read_text(encoding='utf-8')
    title_match = re.search(r'^title:\s*(.*)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else f.stem
    
    entry = f"| [{title}]({f.as_posix()}) | 新摄入内容 |\n"
    if 'concepts/' in f.parts:
        concepts.append(entry)
    elif 'synthesis/' in f.parts:
        synthesis.append(entry)
    elif 'entities/' in f.parts:
        entities.append(entry)
    elif 'sources/' in f.parts:
        sources.append(entry)

# It's safer to just print and let the agent decide how to insert or we can append at the end of the sections.
