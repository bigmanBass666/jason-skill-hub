#!/usr/bin/env node
/**
 * scan.js - 扫描 skills 目录并生成 INDEX.md 和 _redirects
 *
 * 使用方法：node scripts/scan.js
 *
 * 配置：
 *   所有域名配置在 scripts/config.js 中
 *   可以通过环境变量覆盖默认配置：
 *   BASE_URL=https://custom.com/files node scripts/scan.js
 *   DOMAIN=https://example.com node scripts/scan.js
 *   INCLUDE_FILES=true node scripts/scan.js           # 输出引用文件列表（默认 false）
 *   FILE_EXTENSIONS=md,txt,py,js,html node scripts/scan.js  # 白名单模式：只包含指定扩展名
 */

const fs = require('fs');
const path = require('path');
const config = require('./config');

const SKILLS_DIR = path.join(__dirname, '..', 'skills');
const OUTPUT_INDEX = path.join(SKILLS_DIR, 'INDEX.md');
const OUTPUT_JSON = path.join(SKILLS_DIR, 'skills.json');
const OUTPUT_REDIRECTS = path.join(__dirname, '..', '_redirects');
const AGENTS_TEMPLATE = path.join(__dirname, '..', 'AGENTS.md.template');
const OUTPUT_AGENTS = path.join(__dirname, '..', 'AGENTS.md');

/**
 * 获取 skill 的完整 URL
 */
function getSkillUrl(skillPath) {
  return config.getSkillUrl(skillPath);
}

/**
 * 解析 YAML frontmatter
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};

  const yaml = match[1];
  const result = {};

  const lines = yaml.split(/\r?\n/);
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const key = line.slice(0, colonIndex).trim();
    let value = line.slice(colonIndex + 1).trim();

    if (value.startsWith('[') && value.endsWith(']')) {
      value = value.slice(1, -1).split(',').map(s => s.trim().replace(/['"]/g, ''));
      result[key] = value;
      continue;
    }

    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    result[key] = value;
  }

  return result;
}

/**
 * 递归获取目录下所有文件
 */
function getAllFiles(dirPath, basePath = '') {
  const files = [];

  if (!fs.existsSync(dirPath)) return files;

  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    const relativePath = path.join(basePath, entry.name);

    if (entry.isDirectory()) {
      files.push(...getAllFiles(fullPath, relativePath));
    } else {
      files.push(relativePath);
    }
  }

  return files;
}

/**
 * 检查 SKILL.md 中引用的文件是否存在
 */
function checkReferences(skillDir, skillName, content) {
  const refPatterns = [
    /`([^`]*\.(md|txt|py|js|sh|yaml|yml|json|html))`/g,
    /\[([^\]]*\.(md|txt|py|js|sh|yaml|yml|json|html))\]/g,
  ];

  const referencedFiles = new Set();
  for (const pattern of refPatterns) {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      let ref = match[1].trim();
      if (ref.startsWith('./')) ref = ref.slice(2);
      if (ref.startsWith('http://') || ref.startsWith('https://')) continue;
      if (ref.startsWith('../')) continue;
      referencedFiles.add(ref);
    }
  }

  const actualFiles = new Set();
  function collectFiles(dir, base) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relPath = base ? `${base}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        collectFiles(fullPath, relPath);
      } else {
        actualFiles.add(relPath);
      }
    }
  }
  collectFiles(skillDir, '');

  for (const ref of referencedFiles) {
    if (!actualFiles.has(ref)) {
      const lowerRef = ref.toLowerCase();
      const caseMatch = [...actualFiles].find(f => f.toLowerCase() === lowerRef);
      if (caseMatch) {
        console.warn(`⚠️  Warning: [${skillName}] Reference "${ref}" case mismatch — actual file is "${caseMatch}"`);
      } else {
        console.warn(`⚠️  Warning: [${skillName}] Referenced file "${ref}" not found`);
      }
    }
  }
}

const BINARY_EXTENSIONS = new Set([
  'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'webp', 'bmp', 'tiff',
  'ttf', 'otf', 'woff', 'woff2', 'eot',
  'pyc', 'pyo', 'exe', 'dll', 'so', 'o',
  'zip', 'tar', 'gz', 'rar', '7z',
  'mp3', 'mp4', 'avi', 'mov', 'wav', 'flac', 'ogg',
  'docx', 'xlsx', 'pptx', 'pdf',
  'db', 'sqlite',
]);

function isReferenceFile(normalized) {
  if (normalized === 'SKILL.md') return false;
  const ext = normalized.split('.').pop().toLowerCase();
  if (config.fileExtensions) {
    return config.fileExtensions.includes(ext);
  }
  return !BINARY_EXTENSIONS.has(ext);
}

/**
 * 扫描 skills 目录
 */
function scanSkills() {
  const skills = [];

  if (!fs.existsSync(SKILLS_DIR)) {
    console.error('Skills directory not found:', SKILLS_DIR);
    return skills;
  }

  const entries = fs.readdirSync(SKILLS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;

    const skillDir = path.join(SKILLS_DIR, entry.name);
    const skillMd = path.join(skillDir, 'SKILL.md');

    if (!fs.existsSync(skillMd)) continue;

    const content = fs.readFileSync(skillMd, 'utf-8');
    const frontmatter = parseFrontmatter(content);

    if (frontmatter.name && frontmatter.name !== entry.name) {
      console.warn(`⚠️  Warning: Directory "${entry.name}" has frontmatter name "${frontmatter.name}" — using directory name for URL`);
    }

    checkReferences(skillDir, entry.name, content);

    const allFiles = getAllFiles(skillDir);

    skills.push({
      name: frontmatter.name || entry.name,
      description: frontmatter.description || '',
      path: entry.name,
      files: allFiles
    });
  }

  return skills;
}

/**
 * 生成 INDEX.md 内容
 */
function generateIndex(skills) {
  const headerPath = path.join(SKILLS_DIR, 'INDEX_HEADER.md');
  let md = fs.existsSync(headerPath)
    ? fs.readFileSync(headerPath, 'utf-8')
    : `# Skill Catalog\n\n<!-- Auto-generated by scan.js -->\n\n## Skills\n\n`;

  for (const skill of skills) {
    md += `### ${skill.name}\n`;
    md += `- **Description**: ${skill.description}\n`;
    md += `- **Raw**: ${getSkillUrl(skill.path)}\n`;

    const referenceFiles = skill.files.filter(f => {
      return isReferenceFile(f.replace(/\\/g, '/'));
    });

    if (referenceFiles.length > 0) {
      if (config.includeFiles) {
        md += `- **Files** (${referenceFiles.length}):\n`;
        for (const file of referenceFiles) {
          const normalized = file.replace(/\\/g, '/');
          const cdnUrl = config.getFileUrl(skill.path, normalized);
          md += `  - ${normalized} → ${cdnUrl}\n`;
        }
      } else {
        const topDirs = new Set();
        const extCount = {};
        for (const f of referenceFiles) {
          const normalized = f.replace(/\\/g, '/');
          const parts = normalized.split('/');
          if (parts.length > 1) topDirs.add(parts[0] + '/');
          const ext = normalized.split('.').pop().toLowerCase();
          extCount[ext] = (extCount[ext] || 0) + 1;
        }
        const dirStr = topDirs.size > 0 ? ` Directories: ${[...topDirs].sort().join(', ')}.` : '';
        const extStr = Object.entries(extCount)
          .sort((a, b) => b[1] - a[1])
          .map(([ext, count]) => `.${ext}(${count})`)
          .join(', ');
        const baseUrl = getSkillUrl(skill.path).replace('SKILL.md', '');
        md += `- **Has ${referenceFiles.length} file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: \`${baseUrl}\`${dirStr} File types: ${extStr}.\n`;
      }
    }

    md += `\n`;
  }

  return md;
}

/**
 * 生成 skills.json 结构化索引
 */
function generateSkillsJson(skills) {
  const data = skills.map(skill => {
    const base = {
      name: skill.name,
      description: skill.description,
      url: getSkillUrl(skill.path),
    };

    if (config.includeFiles) {
      const referenceFiles = skill.files.filter(f => {
        return isReferenceFile(f.replace(/\\/g, '/'));
      });
      base.references = referenceFiles.map(f => {
        const normalized = f.replace(/\\/g, '/');
        return {
          path: normalized,
          url: config.getFileUrl(skill.path, normalized)
        };
      });
    }

    return base;
  });

  return JSON.stringify(data, null, 2);
}

/**
 * 生成 _redirects 内容
 */
function generateRedirects(skills) {
  let redirects = `# Auto-generated by scan.js - DO NOT EDIT MANUALLY\n`;
  redirects += `# Skill 目录重定向到 SKILL.md\n\n`;
  redirects += `/ /INDEX.md 200\n\n`;

  for (const skill of skills) {
    redirects += `/${skill.path} /${skill.path}/SKILL.md 200\n`;
    redirects += `/${skill.path}/ /${skill.path}/SKILL.md 200\n`;
  }

  return redirects;
}

/**
 * 生成 AGENTS.md 内容
 */
function generateAgents() {
  if (!fs.existsSync(AGENTS_TEMPLATE)) {
    console.log('AGENTS.md.template not found, skipping AGENTS.md generation');
    return;
  }

  let template = fs.readFileSync(AGENTS_TEMPLATE, 'utf-8');
  template = template.replace(/\{\{BASE_URL\}\}/g, config.baseUrl);
  fs.writeFileSync(OUTPUT_AGENTS, template);
  console.log('Generated AGENTS.md');
}

/**
 * 主函数
 */
function main() {
  console.log('Scanning skills directory...');
  console.log(`Using base URL: ${config.baseUrl}`);

  const skills = scanSkills();

  if (skills.length === 0) {
    console.log('No skills found. Create at least one skill with SKILL.md');
    fs.writeFileSync(OUTPUT_INDEX, '# Skill Catalog\n\n_No skills found. Add a skill by creating a directory with SKILL.md._\n');
    return;
  }

  const indexContent = generateIndex(skills);
  fs.writeFileSync(OUTPUT_INDEX, indexContent);
  console.log('Generated INDEX.md');

  const jsonContent = generateSkillsJson(skills);
  fs.writeFileSync(OUTPUT_JSON, jsonContent);
  console.log('Generated skills.json');

  const redirectsContent = generateRedirects(skills);
  fs.writeFileSync(path.join(__dirname, '..', '_redirects'), redirectsContent);
  console.log('Generated _redirects');

  generateAgents();

  console.log(`Found ${skills.length} skill(s): ${skills.map(s => s.name).join(', ')}`);

  const totalReferences = skills.reduce((sum, s) => {
    return sum + s.files.filter(f => isReferenceFile(f.replace(/\\/g, '/'))).length;
  }, 0);

  const indexLines = fs.readFileSync(OUTPUT_INDEX, 'utf-8').split('\n').length;

  console.log(`\n📊 Statistics:`);
  console.log(`   Skills: ${skills.length}`);
  console.log(`   Reference files: ${totalReferences}`);
  console.log(`   INDEX.md: ${indexLines} lines`);
}

main();
