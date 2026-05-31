const path = require('path');

const DEFAULT_GITHUB_BASE = 'https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master';

const URL_FORMATS = {
  'github-raw': {
    base: 'https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master',
    pattern: (path) => `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/${path}`
  },
  'jsdelivr': {
    base: 'https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master',
    pattern: (path) => `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/${path}`
  },
  'gcore': {
    base: 'https://gcore.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master',
    pattern: (path) => `https://gcore.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/${path}`
  }
};

function getBaseUrl() {
  if (process.env.BASE_URL) {
    return process.env.BASE_URL;
  }
  if (process.env.DOMAIN) {
    const owner = process.env.GITHUB_OWNER || 'bigmanBass666';
    const repo = process.env.GITHUB_REPO || 'jason-skill-hub';
    const branch = process.env.GITHUB_BRANCH || 'master';
    return `${process.env.DOMAIN}/${owner}/${repo}/${branch}`;
  }

  const urlFormat = process.env.URL_FORMAT || 'jsdelivr';
  return URL_FORMATS[urlFormat].base;
}

function getConfig() {
  const computedBaseUrl = getBaseUrl();
  const urlFormat = process.env.URL_FORMAT || 'jsdelivr';
  const formatConfig = URL_FORMATS[urlFormat] || URL_FORMATS['jsdelivr'];
  const projectRoot = path.join(__dirname, '..');

  return {
    baseUrl: computedBaseUrl,
    rawBaseUrl: computedBaseUrl,
    skillBaseUrl: `${computedBaseUrl}/skills`,
    urlFormat: urlFormat,

    getSkillUrl(skillName) {
      return formatConfig.pattern(`skills/${skillName}/SKILL.md`);
    },

    getFileUrl(skillName, filePath) {
      return formatConfig.pattern(`skills/${skillName}/${filePath}`);
    },

    syncSourceDir: process.env.SYNC_SOURCE_DIR || 'C:\\Users\\86150\\.agents\\skills',
    syncIntervalMs: parseInt(process.env.SYNC_INTERVAL_MS, 10) || 300000,
    syncTargetDir: process.env.SYNC_TARGET_DIR || path.join(__dirname, '..', 'skills'),
    projectRoot: projectRoot,

    includeFiles: process.env.INCLUDE_FILES === 'true',
    fileExtensions: process.env.FILE_EXTENSIONS
      ? process.env.FILE_EXTENSIONS.split(',').map(e => e.trim().toLowerCase())
      : null
  };
}

module.exports = getConfig();
