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
const OUTPUT_INDEX = path.join(__dirname, '..', 'SKILLS_INDEX.md');
const OUTPUT_REDIRECTS = path.join(__dirname, '..', '_redirects');
const AGENTS_TEMPLATE = path.join(__dirname, '..', 'AGENTS.md.template');
const OUTPUT_AGENTS = path.join(__dirname, '..', 'AGENTS.md');
const SKILLIGNORE_PATH = path.join(__dirname, '..', '.skillignore');

/**
 * 解析 .skillignore 文本，返回模式列表
 * 每条模式是 { raw, isDir, regex }
 */
function parseIgnorePatterns(rawText) {
  const rawPatterns = rawText.split('\n')
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('#'));

  return rawPatterns.map(p => {
    const isDir = p.endsWith('/');
    const namePart = isDir ? p.slice(0, -1) : p;
    // 将 glob 转换为正则：转义特殊字符，* 匹配非分隔符
    const escaped = namePart.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '[^/]*').replace(/\?/g, '.');
    return { raw: p, isDir, regex: new RegExp('^' + escaped + '$', 'i') };
  });
}

/**
 * 加载根目录 .skillignore 文件
 */
function loadSkillIgnore() {
  if (!fs.existsSync(SKILLIGNORE_PATH)) return [];
  return parseIgnorePatterns(fs.readFileSync(SKILLIGNORE_PATH, 'utf-8'));
}

/**
 * 加载指定目录的 .skillignore 文件
 * 用于层级 ignore 机制：每个子目录都可以放自己的 .skillignore
 */
function loadLocalSkillIgnore(dirPath) {
  const ignorePath = path.join(dirPath, '.skillignore');
  if (!fs.existsSync(ignorePath)) return [];
  return parseIgnorePatterns(fs.readFileSync(ignorePath, 'utf-8'));
}

/**
 * 判断文件名是否匹配 .skillignore 中的某个模式
 * 不带 / 的模式匹配 basename（任意层级）
 */
function isIgnored(name, patterns) {
  return patterns.some(p => p.regex.test(name));
}

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
 * 递归获取目录下所有文件（跳过 .skillignore 匹配项）
 * 支持层级 .skillignore：每层目录的规则与父级规则合并
 */
function getAllFiles(dirPath, basePath = '', inheritedPatterns = []) {
  const files = [];

  if (!fs.existsSync(dirPath)) return files;

  // 加载本目录的 .skillignore 并合并到继承的规则中
  const localPatterns = loadLocalSkillIgnore(dirPath);
  const effectivePatterns = inheritedPatterns.concat(localPatterns);

  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    const relativePath = path.join(basePath, entry.name);

    // 检查是否被任一层的 .skillignore 排除
    if (isIgnored(entry.name, effectivePatterns)) continue;

    if (entry.isDirectory()) {
      files.push(...getAllFiles(fullPath, relativePath, effectivePatterns));
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
  const ignorePatterns = loadSkillIgnore();

  if (!fs.existsSync(SKILLS_DIR)) {
    console.error('Skills directory not found:', SKILLS_DIR);
    return skills;
  }

  const entries = fs.readdirSync(SKILLS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;

    // 跳过被 .skillignore 排除的顶级目录（根 .skillignore）
    if (isIgnored(entry.name, ignorePatterns)) continue;

    const skillDir = path.join(SKILLS_DIR, entry.name);

    // 检查 skill 目录内的 .skillignore（层级机制）
    // 如果 skill 目录中有 .skillignore，匹配该目录名则整个 skill 被忽略
    const localPatterns = loadLocalSkillIgnore(skillDir);
    if (isIgnored(entry.name, localPatterns)) continue;

    const skillMd = path.join(skillDir, 'SKILL.md');

    if (!fs.existsSync(skillMd)) continue;

    const content = fs.readFileSync(skillMd, 'utf-8');
    const frontmatter = parseFrontmatter(content);

    if (frontmatter.name && frontmatter.name !== entry.name) {
      console.warn(`⚠️  Warning: Directory "${entry.name}" has frontmatter name "${frontmatter.name}" — using directory name for URL`);
    }

    checkReferences(skillDir, entry.name, content);

    // 合并根 .skillignore + 本技能目录的 .skillignore，传给 getAllFiles
    const allIgnorePatterns = ignorePatterns.concat(localPatterns);
    const allFiles = getAllFiles(skillDir, '', allIgnorePatterns);

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
  const headerPath = path.join(__dirname, '..', 'INDEX_HEADER.md');
  let md = fs.existsSync(headerPath)
    ? fs.readFileSync(headerPath, 'utf-8')
    : `# Skill Catalog\n\n<!-- Auto-generated by scan.js -->\n\n## Skills\n\n`;

  for (const skill of skills) {
    md += `### ${skill.name}\n`;
    md += `- **Description**: ${skill.description}\n`;
    md += `- **Raw**: ${getSkillUrl(skill.path)}\n`;
    md += `- **Zip**: ${config.getZipUrl(skill.path)}\n`;

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