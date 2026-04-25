/**
 * config.js - 域名配置中心
 *
 * 所有 URL 域名相关配置集中管理
 *
 * 使用方法：
 *   const config = require('./config.js');
 *   console.log(config.baseUrl); // 输出当前配置的 baseUrl
 *
 * 环境变量覆盖：
 *   BASE_URL=https://custom.com/files node scripts/scan.js
 *   DOMAIN=https://example.com OWNER=user REPO=repo BRANCH=main node scripts/scan.js
 *
 * URL 格式选项：
 *   URL_FORMAT=github-raw  - GitHub Raw URL (默认)
 *   URL_FORMAT=jsdelivr    - jsDelivr CDN URL
 *   URL_FORMAT=gcore       - jsDelivr + gcore 国内加速
 */

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

  const urlFormat = process.env.URL_FORMAT || 'github-raw';
  return URL_FORMATS[urlFormat].base;
}

function getConfig() {
  const computedBaseUrl = getBaseUrl();
  const urlFormat = process.env.URL_FORMAT || 'github-raw';
  const formatConfig = URL_FORMATS[urlFormat] || URL_FORMATS['github-raw'];

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
    }
  };
}

module.exports = getConfig();
