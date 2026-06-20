import fs from 'fs';
import path from 'path';

const rawDir = '/home/yyh/project/ai-knowledge-base/raw';
const destDir = '/home/yyh/project/ai-knowledge-base/wiki/quality_portal';

if (!fs.existsSync(destDir)) {
  fs.mkdirSync(destDir, { recursive: true });
}

const files = fs.readdirSync(rawDir).filter(f => f.endsWith('.md'));

console.log(`Found ${files.length} markdown files in raw dir.`);

const processedFiles = [];

for (const file of files) {
  const filePath = path.join(rawDir, file);
  const content = fs.readFileSync(filePath, 'utf8');
  
  let newTitle = file.replace('.md', '');
  
  // Try to extract title from `title: "..."`
  const titleMatch = content.match(/title:\s*"([^"]+)"/);
  if (titleMatch) {
    newTitle = titleMatch[1];
  } else if (file === '前端架构评估与建议.md') {
    newTitle = '前端架构评估与建议';
  } else {
    // Look for first heading or non-empty line
    const lines = content.split('\n');
    for (const line of lines) {
      if (line.trim() && !line.includes('---')) {
        let potentialTitle = line.replace(/^[#\s]+/, '').trim();
        if (potentialTitle.length > 3 && potentialTitle.length < 50) {
          newTitle = potentialTitle;
          break;
        }
      }
    }
  }

  const safeTitle = newTitle.replace(/[\/\\?%*:|"<>]/g, '_').trim();
  const destFile = path.join(destDir, `${safeTitle}.md`);
  
  fs.copyFileSync(filePath, destFile);
  console.log(`Moved: ${file} -> wiki/quality_portal/${safeTitle}.md`);
  
  processedFiles.push({
    title: safeTitle,
    path: `wiki/quality_portal/${safeTitle}.md`
  });
}

// Now update index.md to include a new section
const indexPath = '/home/yyh/project/ai-knowledge-base/index.md';
let indexContent = fs.readFileSync(indexPath, 'utf8');

if (!indexContent.includes('## 🏢 Quality Check Pipeline (Business Portal)')) {
  let newSection = `\n## 🏢 Quality Check Pipeline (Business Portal)\n\n| 文件 | 摘要 |\n|---|---|\n`;
  
  for (const info of processedFiles) {
    newSection += `| [${info.title}](${info.path}) | 自动驾驶端到端训练数据的数据质量一站式网页相关文档 |\n`;
  }
  
  indexContent += newSection;
  fs.writeFileSync(indexPath, indexContent);
  console.log('Updated index.md with new Quality Portal section.');
} else {
  console.log('Quality Portal section already exists in index.md.');
}
