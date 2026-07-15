const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const LOG_DIR = process.env.LOG_DIR || path.join(__dirname, '..', 'logs');
const LOG_RETENTION_DAYS = 30;

function timestamp() {
  const now = new Date();
  return now.toTimeString().slice(0, 8);
}

function getLogDate() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function logToFile(msg) {
  try {
    const logDir = path.resolve(LOG_DIR);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    const logFile = path.join(logDir, `sync-${getLogDate()}.log`);
    const entry = `[${new Date().toISOString()}] ${msg}\n`;
    fs.appendFileSync(logFile, entry, 'utf-8');
  } catch (e) {
    // 文件日志失败不阻塞主流程
  }
}

function cleanOldLogs() {
  try {
    const logDir = path.resolve(LOG_DIR);
    if (!fs.existsSync(logDir)) return;
    const maxAge = LOG_RETENTION_DAYS * 24 * 60 * 60 * 1000;
    const now = Date.now();
    const entries = fs.readdirSync(logDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith('.log')) continue;
      const fullPath = path.join(logDir, entry.name);
      const stat = fs.statSync(fullPath);
      if (now - stat.mtimeMs > maxAge) {
        fs.unlinkSync(fullPath);
      }
    }
  } catch (e) {
    // 清理失败不阻塞主流程
  }
}

function log(msg) {
  console.log(`[${timestamp()}] ${msg}`);
  logToFile(msg);
}

// 模块加载时执行一次旧日志清理
cleanOldLogs();

const IGNORED_DIRS = new Set(['.git', '__pycache__', 'node_modules', '.DS_Store', 'free-resource-hunter-workspace']);
const PRESERVED_FILES = new Set(['INDEX.md', 'INDEX_HEADER.md', 'skills.json']);

function walkDir(dir, preserveRootFiles) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (IGNORED_DIRS.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      const subResults = walkDir(fullPath, false);
      for (const r of subResults) {
        results.push(path.join(entry.name, r));
      }
    } else {
      if (preserveRootFiles && PRESERVED_FILES.has(entry.name)) continue;
      results.push(entry.name);
    }
  }
  return results;
}

function detectChanges(sourceDir, targetDir) {
  const sourceFiles = walkDir(sourceDir);
  const targetFiles = walkDir(targetDir, PRESERVED_FILES);

  const sourceSet = new Set(sourceFiles);
  const targetSet = new Set(targetFiles);

  const added = [];
  const modified = [];
  const deleted = [];

  for (const rel of sourceSet) {
    if (!targetSet.has(rel)) {
      added.push(rel);
    } else {
      const srcStat = fs.statSync(path.join(sourceDir, rel));
      const tgtStat = fs.statSync(path.join(targetDir, rel));
      if (srcStat.mtimeMs > tgtStat.mtimeMs || srcStat.size !== tgtStat.size) {
        modified.push(rel);
      }
    }
  }

  for (const rel of targetSet) {
    if (!sourceSet.has(rel)) {
      deleted.push(rel);
    }
  }

  log(`检测变更完成: +${added.length} 修改:${modified.length} 删除:${deleted.length}`);
  return { added, modified, deleted };
}

function mirrorSync(sourceDir, targetDir, changes, dryRun) {
  const { added, modified, deleted } = changes;
  let addedCount = 0;
  let modifiedCount = 0;
  let deletedCount = 0;

  for (const rel of added) {
    const srcPath = path.join(sourceDir, rel);
    const tgtPath = path.join(targetDir, rel);
    if (dryRun) {
      log(`[DRY-RUN] 将添加: ${rel}`);
    } else {
      fs.mkdirSync(path.dirname(tgtPath), { recursive: true });
      fs.copyFileSync(srcPath, tgtPath);
      log(`已添加: ${rel}`);
    }
    addedCount++;
  }

  for (const rel of modified) {
    const srcPath = path.join(sourceDir, rel);
    const tgtPath = path.join(targetDir, rel);
    if (dryRun) {
      log(`[DRY-RUN] 将修改: ${rel}`);
    } else {
      fs.mkdirSync(path.dirname(tgtPath), { recursive: true });
      fs.copyFileSync(srcPath, tgtPath);
      log(`已修改: ${rel}`);
    }
    modifiedCount++;
  }

  for (const rel of deleted) {
    const tgtPath = path.join(targetDir, rel);
    if (dryRun) {
      log(`[DRY-RUN] 将删除: ${rel}`);
    } else {
      fs.unlinkSync(tgtPath);
      log(`已删除: ${rel}`);
      let parent = path.dirname(tgtPath);
      while (parent !== targetDir) {
        try {
          const entries = fs.readdirSync(parent);
          if (entries.length === 0) {
            fs.rmdirSync(parent);
            log(`已清理空目录: ${path.relative(targetDir, parent)}`);
            parent = path.dirname(parent);
          } else {
            break;
          }
        } catch {
          break;
        }
      }
    }
    deletedCount++;
  }

  const summary = { added: addedCount, modified: modifiedCount, deleted: deletedCount };
  log(`同步完成: +${summary.added} 修改:${summary.modified} 删除:${summary.deleted}`);
  return summary;
}

function getNodePath() {
  try {
    return process.execPath;
  } catch {
    return 'node';
  }
}

function runBuild(projectRoot) {
  const nodeExe = getNodePath();
  log(`执行构建: ${nodeExe} scripts/scan.js`);
  execSync(`"${nodeExe}" scripts/scan.js`, { cwd: projectRoot, stdio: 'inherit' });
  log('构建完成');
}

const GIT_SAFE = '-c safe.directory=*';

function gitRun(projectRoot, cmd, opts) {
  return execSync(`git ${GIT_SAFE} ${cmd}`, { cwd: projectRoot, stdio: 'inherit', ...opts });
}

function gitRunQuiet(projectRoot, cmd) {
  try {
    return execSync(`git ${GIT_SAFE} ${cmd}`, { cwd: projectRoot }).toString().trim();
  } catch {
    return '';
  }
}

function gitCommitAndPush(projectRoot, targetDir) {
  const relDir = path.relative(projectRoot, targetDir).replace(/\\/g, '/');
  const skillsStatus = gitRunQuiet(projectRoot, `status --porcelain -- "${relDir}"`);
  if (!skillsStatus) {
    log('无变更，跳过提交');
    return false;
  }

  const now = new Date();
  const dateStr = now.toISOString().replace('T', ' ').slice(0, 19);

  log(`执行 git add "${relDir}"`);
  gitRun(projectRoot, `add "${relDir}"`);

  log(`执行 git commit -m "sync: auto-sync skills from source [${dateStr}]"`);
  try {
    gitRun(projectRoot, `commit -m "sync: auto-sync skills from source [${dateStr}]"`);
  } catch (e) {
    log('commit 失败，重新 add 后重试');
    gitRun(projectRoot, `add "${relDir}"`);
    try {
      gitRun(projectRoot, `commit -m "sync: auto-sync skills from source [${dateStr}]"`);
    } catch (e2) {
      log('commit 仍然失败，跳过本次同步');
      return false;
    }
  }

  log('执行 git push');
  try {
    gitRun(projectRoot, 'push');
  } catch (e) {
    log('push 被拒绝，远端有新提交');
    const allStatus = gitRunQuiet(projectRoot, 'status --porcelain');
    let hasStash = false;
    if (allStatus) {
      log('暂存非 skills 变更以便 rebase');
      try {
        gitRun(projectRoot, 'stash --include-untracked');
        hasStash = true;
      } catch (se) {
        log('stash 失败，尝试直接 rebase');
      }
    }
    try {
      gitRun(projectRoot, 'pull --rebase');
      gitRun(projectRoot, 'push');
    } catch (re) {
      log('rebase 后 push 仍然失败，放弃本次推送，下次重试');
    }
    if (hasStash) {
      try {
        log('恢复暂存的变更');
        gitRun(projectRoot, 'stash pop');
      } catch (spe) {
        log('stash pop 失败，变更保留在 stash 中');
      }
    }
  }

  log('提交并推送完成');
  return true;
}

async function fullSync({ dryRun, projectRoot, targetDir }) {
  log('=== 开始同步流程 ===');

  if (!dryRun) {
    log('步骤 1/2: 执行构建（scan.js → INDEX + skills.json + _redirects）');
    runBuild(projectRoot);

    log('步骤 2/2: 提交并推送');
    gitCommitAndPush(projectRoot, targetDir);
  } else {
    log('[DRY-RUN] 跳过构建和提交');
  }

  log('=== 同步流程结束 ===');
}

module.exports = {
  runBuild,
  gitCommitAndPush,
  fullSync,
};