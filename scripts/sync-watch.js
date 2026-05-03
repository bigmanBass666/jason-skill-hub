const chokidar = require('chokidar');
const { fullSync } = require('./sync-lib');
const config = require('./config');

const args = process.argv.slice(2);
const once = args.includes('--once');
const dryRun = args.includes('--dry-run');

function timestamp() {
  const now = new Date();
  const hh = String(now.getHours()).padStart(2, '0');
  const mm = String(now.getMinutes()).padStart(2, '0');
  const ss = String(now.getSeconds()).padStart(2, '0');
  return `[${hh}:${mm}:${ss}]`;
}

function log(msg) {
  console.log(`${timestamp()} ${msg}`);
}

async function runSync() {
  log('Sync started...');
  try {
    await fullSync({
      dryRun,
      projectRoot: config.projectRoot,
      sourceDir: config.syncSourceDir,
      targetDir: config.syncTargetDir
    });
    log('Sync complete.');
  } catch (err) {
    log(`Sync failed: ${err.message}`);
  }
}

if (once) {
  runSync().then(() => process.exit(0)).catch((err) => {
    log(`Sync error: ${err.message}`);
    process.exit(1);
  });
} else {
  let dirty = false;
  let lastSyncTime = 0;
  let cooldownTimer = null;
  const cooldownMs = config.syncIntervalMs || 300000;

  async function triggerSync() {
    dirty = false;
    lastSyncTime = Date.now();
    await runSync();
    if (dirty) {
      scheduleSync();
    }
  }

  function scheduleSync() {
    if (cooldownTimer) {
      return;
    }
    const elapsed = Date.now() - lastSyncTime;
    const remaining = cooldownMs - elapsed;
    if (remaining <= 0) {
      triggerSync();
    } else {
      log(`Cooldown active, waiting ${Math.ceil(remaining / 1000)}s before next sync...`);
      cooldownTimer = setTimeout(() => {
        cooldownTimer = null;
        if (dirty) {
          triggerSync();
        }
      }, remaining);
    }
  }

  function onChange(eventType, path) {
    log(`Change detected: ${eventType} - ${path}`);
    dirty = true;
    scheduleSync();
  }

  log(`Watch daemon started`);
  log(`  Source: ${config.syncSourceDir}`);
  log(`  Target: ${config.syncTargetDir}`);
  log(`  Cooldown interval: ${cooldownMs}ms`);

  const watcher = chokidar.watch(config.syncSourceDir, {
    ignoreInitial: true,
    awaitWriteFinish: {
      stabilityThreshold: 2000
    }
  });

  watcher.on('add', (path) => onChange('add', path));
  watcher.on('change', (path) => onChange('change', path));
  watcher.on('unlink', (path) => onChange('unlink', path));
  watcher.on('addDir', (path) => onChange('addDir', path));
  watcher.on('unlinkDir', (path) => onChange('unlinkDir', path));

  watcher.on('ready', () => {
    log('Watcher ready, performing initial sync...');
    triggerSync();
  });

  watcher.on('error', (err) => {
    log(`Watcher error: ${err.message}`);
  });

  function shutdown() {
    log('Shutting down...');
    if (cooldownTimer) {
      clearTimeout(cooldownTimer);
      cooldownTimer = null;
    }
    watcher.close().then(() => {
      log('Watcher closed.');
      process.exit(0);
    });
  }

  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}
