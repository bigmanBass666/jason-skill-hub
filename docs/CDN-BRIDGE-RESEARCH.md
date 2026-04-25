# CDN 桥接服务深度调研报告

**调研日期：** 2026-04-25

**背景：** GitHub Raw URL 在多个 AI 平台（z.ai、通义千问、DeepSeek 等）被屏蔽或返回 403，需要寻找能够桥接 GitHub 仓库并返回原始文件内容的 CDN/代理服务。

---

## 完整对比表格

### 一、CDN 桥接服务（国际）

| 服务 | URL 格式 | 免费额度 | 国内速度 | AI 兼容性 | 302重定向 | 稳定性 |
|------|---------|---------|---------|----------|-----------|--------|
| **jsDelivr** | `cdn.jsdelivr.net/gh/{owner}/{repo}@{ref}/{path}` | 无限 | 🟡 一般（可用 gcore 节点优化） | ⭐⭐⭐⭐ 高 | ❌ 无，直接返回内容 | ⭐⭐⭐⭐⭐ 极高 |
| **Statically** | `cdn.statically.io/gh/{user}/{repo}/{tag}/{file}` | 无限 | 🟢 快 | ⭐⭐⭐⭐ 高 | ❌ 无 | ⭐⭐⭐⭐ 高 |
| **ghproxy.com** | `ghproxy.com/{完整URL}` | 有限制 | 🟢 快 | ⭐⭐⭐ 中 | ❌ 无 | ⭐⭐⭐ 中（第三方维护） |

### 二、国内 CDN 镜像服务

| 服务 | URL 格式 | 免费额度 | 国内速度 | AI 兼容性 | 302重定向 | 稳定性 |
|------|---------|---------|---------|----------|-----------|--------|
| **Gitee CDN** (新) | `raw.giteeusercontent.com/{owner}/{repo}/{branch}/{path}` | 有限制 | 🟢 极快 | ⭐⭐⭐ 中 | ❌ 无 | ⭐⭐⭐⭐ 新上线 |
| **Gitee Raw** (旧) | `gitee.com/{owner}/{repo}/raw/{branch}/{path}` | 有限制 | 🟢 极快 | ⭐⭐ 中 | ⚠️ 可能有 | ⚠️ 正在废弃 |
| **FastGit** | `raw.fastgit.org/...` → 已迁移到 `fgit.cf` | 有限制 | 🟢 快 | ⭐⭐ 中 | ❌ 无 | ⚠️ 已迁移 |

### 三、代理/Worker 方案

| 方案 | 实现难度 | 成本 | 国内速度 | AI 兼容性 | 稳定性 |
|------|---------|------|---------|----------|--------|
| **Cloudflare Workers** | 🟡 中 | $0（每天10万请求） | 🟢 快 | ⭐⭐⭐⭐⭐ 极高 | ⭐⭐⭐⭐⭐ 极高 |
| **Vercel Edge** | 🟡 中 | $0（每天10万请求） | 🟢 快 | ⭐⭐⭐⭐⭐ 极高 | ⭐⭐⭐⭐⭐ 高 |
| **自建 Nginx** | 🟢 低 | 服务器成本 | 🟢 快 | ⭐⭐⭐⭐⭐ 极高 | ⭐⭐⭐⭐ 依赖服务器 |

### 四、特殊服务

| 服务 | URL 格式 | 适用场景 | AI 兼容性 | 备注 |
|------|---------|---------|----------|------|
| **Netlify** | `{site}.netlify.app/{path}` | 已在用 | ⭐⭐⭐⭐⭐ 极高 | 直接返回原始文件 |
| **GitHub Pages** | `{user}.github.io/{repo}/{path}` | 不适合 | ⭐⭐⭐⭐⭐ 高 | 需构建/渲染流程 |

---

## Top 3 推荐方案

### 🥇 推荐 1：jsDelivr（最简单，立即可用）

**URL 格式：**
```
https://cdn.jsdelivr.net/gh/{owner}/{repo}@{ref}/{path}
```

**实际示例：**
```
# 原来的 GitHub Raw（被 AI 平台屏蔽）
https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md

# jsDelivr 替代方案
https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
```

**优点：**
- ✅ 完全免费，无限带宽
- ✅ 不返回 302 重定向，直接返回原始内容
- ✅ 全球 CDN 加速，多节点 failover
- ✅ 支持版本锁定（@sha）或分支（@master）
- ✅ AI 平台兼容性好（独立的 CDN 域名，不容易被屏蔽）
- ✅ 国内有加速节点（通过 gcore.jsdelivr.net）

**缺点：**
- ❌ 需要添加 `@{ref}` 版本标记
- ❌ 依赖第三方服务

**国内加速优化：**
jsDelivr 默认节点国内访问一般，可以使用 `gcore.jsdelivr.net` 节点：
```
https://gcore.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
```

---

### 🥈 推荐 2：Cloudflare Workers 代理（最稳定，长期方案）

如果你有自己的域名，可以搭建一个 Cloudflare Workers 代理，完全掌控访问。

**实现方式：**
```javascript
// Worker 代码
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  const githubRaw = `https://raw.githubusercontent.com${path}`;
  return fetch(githubRaw);
}
```

**URL 格式：**
```
https://workers.yourdomain.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md
```

**优点：**
- ✅ 完全自控，不依赖第三方
- ✅ 免费额度充足（每天10万请求）
- ✅ Cloudflare 全球加速，国内访问快
- ✅ AI 平台兼容性最高

**缺点：**
- ❌ 需要有自己的域名
- ❌ 需要部署 Worker 代码

---

### 🥉 推荐 3：Gitee CDN 镜像（国内最快）

如果国内访问速度是首要考虑，可以用 Gitee 做一个镜像。

**URL 格式：**
```
https://raw.giteeusercontent.com/{owner}/{repo}/{branch}/{path}
```

**实际示例：**
```
https://raw.giteeusercontent.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md
```

**优点：**
- ✅ 国内访问极快
- ✅ 独立 CDN 域名
- ✅ 免费额度

**缺点：**
- ❌ Gitee 的 raw 链接存在时效性问题
- ❌ 可能返回 302 重定向
- ❌ robots.txt 显示 raw 路径被 disallow
- ❌ Gitee 正在废弃旧路径

---

## 其他调研发现

### FastGit
- 原来域名 `hub.fastgit.org` 已迁移到 `hub.fgit.cf`
- Raw 访问：`https://raw.fgit.cf/{user}/{repo}/{branch}/{path}`

### Statically
- URL 格式：`https://cdn.statically.io/gh/{user}/{repo}/{tag}/{file}`
- 支持 GitHub、GitLab、Bitbucket
- 免费无限流量

### ghproxy.com
- URL 格式：`https://ghproxy.com/{完整GitHub URL}`
- 支持 GitHub Releases、Raw、Archive 等
- 第三方维护，稳定性一般

---

## 切换成本评估

| 方案 | 切换难度 | 需改多少文件 | 风险 |
|------|---------|-------------|------|
| **jsDelivr** | 🟢 极低 | 只改 INDEX.md 的 Path 前缀 | 低 |
| **Cloudflare Workers** | 🟡 中 | 需要改 scan.js + 部署 Worker | 中 |
| **Gitee 镜像** | 🟡 中 | INDEX.md + 同步脚本 | 中（Gitee 不稳定） |

**最小改动方案（jsDelivr）：**
只需要把 INDEX.md 里的 Path 从：
```
https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/awwwards-design/SKILL.md
```
改成：
```
https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/SKILL.md
```

---

## 风险提示

| 方案 | 潜在风险 |
|------|---------|
| **jsDelivr** | 第三方服务可能变动（但目前非常稳定）、版本标记需要更新 |
| **Gitee CDN** | 时效性问题、正在废弃旧路径、可能返回 302 |
| **Cloudflare Workers** | 需要域名和配置、有每日请求限制（但10万次足够） |
| **ghproxy.com** | 第三方维护可能不稳定、有限制政策 |

---

## 最终建议

### 立即可用（最小改动）：
用 **jsDelivr**，修改 INDEX.md 的 URL 格式，scan.js 添加输出 jsDelivr URL 的选项。

### 长期稳定（推荐）：
用 **Cloudflare Workers** 搭建自己的代理，完全自控，不依赖第三方。

### 国内最快（备选）：
用 **Gitee CDN**，但作为备选而非主力（因为不稳定）。

---

## 下一步行动

1. **立即测试 jsDelivr**：把 INDEX.md 里的 URL 改成 jsDelivr 格式，让 AI 在 z.ai 上测试能否正常访问

2. **如果 jsDelivr 可用**：修改 scan.js 支持输出 jsDelivr URL 格式

3. **如果 jsDelivr 被屏蔽**：尝试 Cloudflare Workers 方案

4. **备选方案**：Gitee CDN 镜像（作为降级方案）
