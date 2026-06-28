---
name: chaoxing-auto-answer
description: >
  超星学习通（i.chaoxing.com）自动化答题工具。当用户需要完成学习通上的作业、测验、考试时使用此技能。
  支持自动登录、进入课程、填写单选题/多选题/填空题/判断题并提交。自动识别预览页/考试页/作业页/已交卷页，
  按页面类型执行不同流程。必须配合 Playwright MCP 浏览器工具使用。
  触发场景：打开学习通、完成作业、做测验、超星答题、chaoxing 作业、学习通考试、学习通试卷。
compatibility:
  requires:
    - playwright MCP (browser_navigate, browser_click, browser_evaluate, browser_snapshot, browser_type, browser_fill_form)
    - 用户需先在浏览器中登录学习通或提供登录信息
---

# 超星学习通自动化答题 Skill

## 概述

本技能用于自动化完成超星学习通平台上的在线作业和考试。支持：
- **单选题、多选题、判断题** — 通过 `[role="radio"]` 点击选择
- **填空题、简答题、论述题** — 通过 UEditor iframe 内容写入
- **自动识别页面类型** — 预览页 / 考试页 / 作业页 / 已交卷页，走不同流程

---

## 核心流程

### 第一步：导航与页面类型识别

导航到目标页面后，**先识别页面类型**，再决定后续操作。

**URL 路由表：**

| URL 模式 | 页面类型 | 操作 |
|----------|---------|------|
| `/exam/preview` | 考试预览页 | 先点击"进入考试"，等待跳转到考试页 |
| `/exam/test/` | 考试答题页 | 直接答题 |
| `/exam/test/look` | 已交卷查看页 | 终止，提示已交卷 |
| `/mooc2/work/dowork` | 作业答题页 | 直接答题 |
| `/mooc2/work/list` | 作业列表页 | 先选择具体作业进入 |
| `passport2.chaoxing.com/login` | 登录页 | 等待用户手动登录 |

**页面类型判断代码：**
```javascript
const url = window.location.href;
if (url.includes('/exam/preview')) return 'exam_preview';
if (url.includes('/exam/test/look')) return 'exam_look';     // 已交卷
if (url.match(/\/exam\/test\//)) return 'exam_test';          // 考试中
if (url.includes('/mooc2/work/dowork')) return 'work';        // 作业
if (url.includes('/mooc2/work/list')) return 'work_list';     // 作业列表
if (url.includes('/login')) return 'login';
return 'unknown';
```

**考试预览页处理：** 预览页的选项点击不会实际保存，必须先触发"进入考试"。
- 页面上有隐藏的 `<a id="tabIntoexam2">进入考试</a>` 和对应的取消/确定按钮弹窗
- 需要调用 `document.getElementById('tabIntoexam2')?.click()` 触发进入
- 或者直接构造包含 `enc` 参数的考试 URL 导航到 `/exam/test/` 页

### 第二步：进入课程

**方法A - 通过课程列表：** 导航到课程列表页，查找目标课程名称，点击进入。

**方法B - 直接通过URL：**
```
https://mooc1.chaoxing.com/visit/stucoursemiddle?courseid={courseId}&clazzid={classId}&cpi={cpi}&ismooc2=1
```

### 第三步：找到作业/考试

**作业列表（work/list）：** 课程页面中的作业列表在 iframe 中，获取 iframe.src 后跳转到作业列表页。
```javascript
const iframe = document.querySelector('iframe');
const workListUrl = iframe.src;
```
在列表中通过文本匹配查找目标作业：
```javascript
document.querySelectorAll('li, [role="listitem"]').forEach(item => {
  const text = item.textContent || '';
  if (text.includes('作业名称') && text.includes('未交')) {
    item.querySelector('a')?.click();
  }
});
```

**考试（exam）：** 直接使用考试 URL 导航，无需经过课程页面。

### 第四步：页面侦察（填写前必做）

进入答题/考试页面后，**先用侦察脚本摸清结构**，然后再填写。这样做比逐步试探高效得多。

```javascript
// 侦察脚本 — 一次性返回页面完整结构
const info = {
  pageType: /* 判断代码同上 */,
  // 统计所有 radio 选项
  radios: Array.from(document.querySelectorAll('[role="radio"]')).map((r, i) => ({
    index: i,
    text: r.textContent.replace(/\s+/g, ' ').trim().substring(0, 40),
    // 检查是否已有选中状态（学习通用 class 或 onclick 保存，不是 aria-checked）
    onclick: !!r.getAttribute('onclick'),
    hasRef: !!r.getAttribute('ref')
  })),
  // 统计 iframe 编辑器（用于填空题/简答题）
  editors: Array.from(document.querySelectorAll('iframe')).map((f, i) => {
    try { return { index: i, w: f.offsetWidth, h: f.offsetHeight, hasBody: !!f.contentDocument?.body }; }
    catch(e) { return { index: i, error: 'cross-origin' }; }
  }),
  // 可见按钮
  buttons: Array.from(document.querySelectorAll('a, button, [role="button"]'))
    .filter(el => el.offsetParent !== null)
    .map(el => el.textContent.trim().substring(0, 20)),
  // 答题卡状态（如果有）
  answeredCount: document.body.textContent.match(/(\d+)\s*\/\s*(\d+)\s*(?:已答|未答)/)?.[0] || 'not found'
};
```

侦察结果能告诉你：
- 全部 radio 选项的索引和文本映射 → 用于批量点击公式
- 单选/判断各多少题（每4个一组 = 单选，每2个一组 = 判断）
- 编辑器 iframe 的数量和位置 → 用于填空/简答
- 当前页面上的按钮 → 找到提交/保存按钮

### 第五步：填写答案

#### 5.1 选项点击 — 四级降级链

学习通的 radio 选项是自定义 div（`<div role="radio" onclick="saveSingleSelect(this, qid)">`），不是原生 `<input type="radio">`。**`ref` 属性是 Playwright snapshot 的虚拟标识，不是真实 DOM 属性**，不要依赖它定位。

推荐按以下四级策略依次尝试。越靠前越精确，越靠后越兜底：

```javascript
// 策略1（首选）：按索引点击
// 单选题每4个选项一组：index = (qNum-1)*4 + offset（A=0, B=1, C=2, D=3）
// 判断题每2个选项一组：index = 单选总数*4 + (qNum-31)*2 + (对=0, 错=1)
document.querySelectorAll('[role="radio"]')[index].click();

// 策略2：按文本点击（当索引不确定时）
const allRadios = document.querySelectorAll('[role="radio"]');
allRadios.forEach(r => {
  if (r.textContent.trim().startsWith('C') && r.textContent.includes('软件功能')) {
    r.click();
  }
});

// 策略3：dispatchEvent（click() 不生效时）
el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));

// 策略4（最后手段）：直接调用 onclick 函数
el.onclick.call(el, {currentTarget: el});
```

> **为什么需要降级链？** 学习通用 `saveSingleSelect` 函数处理点击，但不同版本的页面实现不同。有的直接用 `onclick`，有的用事件监听。降级链确保无论哪种实现都能触发选择。

#### 5.2 批量填写通用公式

**公式原理：** 所有 `[role="radio"]` 元素在 DOM 中按题目顺序线性排列。你不需要为每个选项单独写代码，算出索引即可：

```
单选题索引: (qNum - 1) × 4 + offset       # offset: A=0, B=1, C=2, D=3
判断题索引: judgeStart + (qNum - 31) × 2   # judgeStart = 单选题数 × 4
填空题iframes索引: qNum - firstFillQNum      # 按题目顺序对应
```

**一次性完成的完整脚本：**
```javascript
const allRadios = document.querySelectorAll('[role="radio"]');
const iframes = document.querySelectorAll('iframe');

// === 单选题 ===
const singleChoice = { 1:'C', 2:'A', /* ...30题 */ };
for (let q = 1; q <= 30; q++) {
  const idx = (q - 1) * 4 + (singleChoice[q].charCodeAt(0) - 65);
  allRadios[idx]?.click();
}

// === 判断题（单选题后面）===
const judgeStart = 30 * 4; // 30道单选后开始
const judge = { 31:'错', 32:'对', /* ...15题 */ };
for (let q = 31; q <= 45; q++) {
  const offset = judge[q] === '对' ? 0 : 1;
  allRadios[judgeStart + (q - 31) * 2 + offset]?.click();
}

// === 填空题/简答题（UEditor iframe）===
const fillAnswers = ['答案1', '答案2', /* ... */];
for (let i = 0; i < fillAnswers.length; i++) {
  if (iframes[i]?.contentDocument?.body) {
    iframes[i].contentDocument.body.innerHTML = '<p>' + fillAnswers[i] + '</p>';
  }
}
```

#### 5.3 UEditor 填写要点

填空题和简答题使用 UEditor 富文本编辑器（内联 iframe）。填写时注意：

- **内联 iframe（可直接访问）：** `src` 为 `javascript:void(function(){...})` 或 `javascript:false`。直接用 `contentDocument.body.innerHTML = '<p>答案</p>'`
- **跨域 iframe（无法访问）：** `SecurityError`。改用 Playwright 的 `browser_type` 在编辑器区域打字
- **初始化检测：** 如果 `body.innerHTML` 写入后未显示，先触发编辑器初始化：`ue.ready(() => ue.setContent('答案'))`（需在页面原有 UEditor 全局对象上调用）
- **分卷作答：** 考试可能按分卷划分，各分卷的 iframe 在不同容器中。填写前确认当前显示的是哪个分卷

#### 5.4 多选题操作

多选题的选项仍是 `[role="radio"]`，但允许多选。**每个选项独立点击，不需要互斥逻辑。** 按答案逐个点击即可。

### 第六步：状态验证

**不要依赖 `aria-checked` 判断是否选中。** 学习通的 radio 是自定义 div，选中后可能不更新 `aria-checked`。

多维验证方法（按可靠性从高到低）：

```javascript
// 方法1：通过答题卡计数（最可靠）
const answerCard = document.querySelector('.answerCard, [class*="answer-card"]');
const answered = answerCard?.textContent.match(/(\d+)\s*\/\s*(\d+)/);
if (answered) console.log(`已答 ${answered[1]}/${answered[2]}`);

// 方法2：检查 onclick 函数是否已被触发（请求完成标志）
// 如果 saveSingleSelect 发起了 AJAX 请求，等待网络静默
await new Promise(r => setTimeout(r, 1000));

// 方法3：检查 class 变化（部分版本会添加 selected/on 类）
const selectedDivs = document.querySelectorAll('.clearfix.answerBg');
let count = 0;
selectedDivs.forEach(d => {
  if (d.style.background || d.classList.contains('on') || d.querySelector('.num_option[style*="background"]')) {
    count++;
  }
});

// 方法4：截图检查（最后手段）
```

### 第七步：提交

**定位提交按钮：**
```javascript
// 考试页的按钮通常是可见的链接
document.querySelectorAll('a, button').forEach(el => {
  const text = el.textContent.trim();
  if (text.includes('交卷') || text.includes('提交')) {
    // 确认弹窗会自动处理
    if (el.offsetParent !== null) el.click();
  }
});
```

**弹窗处理清单（按出现的频率排序）：**

| 弹窗文本 | 处理方式 |
|----------|---------|
| "进入考试" / "取消" | 点击"进入考试"（id: tabIntoexam2） |
| "确认交卷？" / "确定" / "取消" | 点击"确定"（class: confirm） |
| "作答时间已用完" / "确定" | 点击"确定" |
| "当前考试需按分卷顺序作答" / "确定" | 点击"确定"，进入下一个分卷 |
| "继续考试" / "退出考试" | 点击"继续考试" |
| "交卷成功" | 已完成 |
| "知道了" | 点击"知道了"（常见提示） |

**交卷后验证：** 确认页面是否有"交卷成功"文本。如果跳转到 `/exam/test/look` 页面，读取提交时间、考试用时等确认信息。

---

## 答案输入格式

### 格式1：JSON 结构化答案
```json
{
  "singleChoice": [{"q": 1, "answer": "C"}, {"q": 2, "answer": "B"}],
  "fillInBlank": [{"q": 9, "answers": ["子项目"]}],
  "judge": [{"q": 13, "answer": "对"}, {"q": 14, "answer": "错"}]
}
```

### 格式2：简化的文本描述
```
单选题：1. C  2. B  ...
填空题：9. 子项目  ...
判断题：13. 对  14. 错  ...
```

---

## 常见问题与解决方案

### 1. 点击选项后无反应
**原因：** 学习通使用自定义 div 模拟 radio，不同版本的点击处理不同。
**解决：** 按降级链依次尝试（索引点击 → 文本匹配 → dispatchEvent → 直接调 onclick）。如果都不行，检查页面是否有 `<input type="radio">` 隐藏元素，直接设置 `input.checked = true` 并触发 change 事件。

### 2. 答题卡显示已答数与预期不符
**原因：** 
- 预览页的点击不会更新答题卡状态
- 点击后服务器保存有延迟
**解决：** 确认当前页面不是 `/exam/preview`；点击后等待 1-2 秒再验证。

### 3. 跨域 iframe 无法写入
**原因：** iframe 的 src 指向外部域名（非内联编辑器）。
**解决：** 这是浏览器安全策略，无法绕过。改用 `browser_type` 在编辑器区域输入文本，或提示用户手动填写。

### 4. 页面显示"作答状态异常"
**原因：** 作业/考试已提交过，无法重新作答。
**解决：** 需要老师开启重新作答权限，或使用新的 answerId/enc。

### 5. 找不到提交按钮
**原因：** 提交按钮可能动态加载，或当前是预览页没有提交功能。
**解决：** 用侦察脚本先确认页面类型；等待页面完全加载后再查找。

### 6. 分卷作答
考试可能分多个分卷，每个分卷独立计时。填写完当前分卷后点击"确定"进入下一分卷。注意确认答案在分卷切换时是否保存。

---

## 最佳实践

1. **操作顺序：** 侦察 → 批量填写单选/判断 → 批量填写填空/简答 → 验证 → 提交（不要逐题操作）
2. **批量处理：** 使用索引公式一次性填写所有单选和判断，不要逐个点击。用 `browser_evaluate` 执行完整脚本，减少往返
3. **截图确认：** 填写完成后截一张图让用户确认，再提交
4. **不自动提交：** 除非用户明确要求，否则只填写不提交
5. **enc 参数是关键：** URL 中的 enc 参数是身份令牌，丢失后需要重新登录

---

## 完整示例代码

### 考试模式（含预览页处理 + 批量填写）

```javascript
// ====== 导航到考试页 ======
// 用户提供的可能是 /exam/preview URL，自动处理
let url = 'https://mooc1.chaoxing.com/exam-ans/mooc2/exam/preview?...';
await page.goto(url);

// ====== 检测并处理预览页 ======
const isPreview = await page.evaluate(() => window.location.href.includes('/exam/preview'));
if (isPreview) {
  // 触发"进入考试"弹窗并确认
  await page.evaluate(() => document.getElementById('tabIntoexam2')?.click());
  await page.waitForTimeout(500);
  // 等待页面跳转到 /exam/test/
  await page.waitForURL('**/exam/test/**', { timeout: 10000 });
}

// ====== 侦察结构 ======
const radios = await page.evaluate(() => 
  Array.from(document.querySelectorAll('[role="radio"]')).map(r => ({
    index: Array.from(document.querySelectorAll('[role="radio"]')).indexOf(r),
    text: r.textContent.replace(/\s+/g, ' ').trim()
  }))
);
console.log(`发现 ${radios.length} 个选项`);

// ====== 批量填写 ======
await page.evaluate(() => {
  const allRadios = document.querySelectorAll('[role="radio"]');
  // 单选题答案
  const single = {1:'C',2:'A',3:'C',4:'A',5:'A',6:'B',7:'B',8:'B',9:'D',10:'D'};
  for (let q = 1; q <= 10; q++) {
    const idx = (q-1)*4 + (single[q].charCodeAt(0)-65);
    if (allRadios[idx]) allRadios[idx].click();
  }
  // 判断题
  const judge = {31:'错',32:'对'};
  const jStart = 30*4;
  for (let q = 31; q <= 32; q++) {
    const idx = jStart + (q-31)*2 + (judge[q]==='对'?0:1);
    if (allRadios[idx]) allRadios[idx].click();
  }
});

// ====== 验证 ======
const verified = await page.evaluate(() => {
  // 检查答题卡中已答计数
  const match = document.body.textContent.match(/(\d+)\s*\/\s*(\d+)\s*(?:已答)/);
  return match ? `已答 ${match[1]}/${match[2]}` : '答题卡计数未找到';
});
console.log(verified);

// ====== 提交 ======
// 仅在用户确认后执行
document.querySelector('.completeBtn, a:has-text("交卷")')?.click();
await page.waitForTimeout(500);
document.querySelector('.confirm, .jb_btn_92.confirm')?.click();
```

## ⚠️ 重要注意事项

1. **不要自动提交** — 除非用户明确要求。填写完成后让用户确认
2. **保留 enc 参数** — 它是身份令牌，丢失后需要重新登录
3. **考试 vs 作业** — 考试的 URL 路径是 `/exam/`，作业是 `/mooc2/work/`，流程有差异
4. **分卷考试** — 可能需要手动确认分卷切换
5. **及时反馈进度** — 每个步骤完成后告诉用户当前状态和已答数量
