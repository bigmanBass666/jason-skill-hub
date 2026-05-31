---
name: chaoxing-auto-answer
description: >
  超星学习通（i.chaoxing.com）自动化答题工具。当用户需要完成学习通上的作业、测验、考试时使用此技能。
  支持自动登录、进入课程、填写单选题/多选题/填空题/判断题并提交。
  触发场景：打开学习通、完成作业、做测验、超星答题、chaoxing 作业、学习通考试。
  必须配合 Playwright MCP 浏览器工具使用。
compatibility:
  requires:
    - playwright MCP (browser_navigate, browser_click, browser_evaluate, browser_snapshot, browser_type, browser_fill_form)
    - 用户需先在浏览器中登录学习通或提供登录信息
---

# 超星学习通自动化答题 Skill

## 概述

本技能用于自动化完成超星学习通平台上的各类在线作业和测验。支持：
- 单选题、多选题
- 判断题
- 填空题

## 核心流程

### 第一步：初始化与导航

```javascript
// 打开学习通主页
await page.goto('https://i.chaoxing.com');
```

**关键点：**
- 如果页面跳转到登录页，需要用户手动登录或扫码
- 登录成功后会重定向到个人空间页面
- 记录当前 URL 和 enc 参数用于后续请求

### 第二步：进入课程

**方法A - 通过课程列表：**
1. 导航到课程列表页
2. 查找目标课程名称
3. 点击进入课程详情

**方法B - 直接通过URL：**
```
https://mooc1.chaoxing.com/visit/stucoursemiddle?courseid={courseId}&clazzid={classId}&cpi={cpi}&ismooc2=1
```

### 第三步：找到作业列表

**获取 iframe URL：**
```javascript
// 课程页面中的作业列表在 iframe 中
const iframe = document.querySelector('iframe');
const workListUrl = iframe.src; // 类似 mooc2/work/list?...
```

**直接访问作业列表：**
```
https://mooc1.chaoxing.com/mooc2/work/list?courseId=...&classId=...&cpi=...&enc=...
```

### 第四步：点击进入具体作业

**通过文本匹配查找链接：**
```javascript
const listItems = document.querySelectorAll('li, [role="listitem"]');
for (let item of listItems) {
  const text = item.textContent || '';
  if (text.includes('第X章作业') && text.includes('未交')) {
    item.querySelector('a')?.click();
    break;
  }
}
```

**新标签页会打开，记录 URL：**
- 格式：`https://mooc1.chaoxing.com/mooc-ans/mooc2/work/dowork?workId=...&answerId=...&enc=...`

### 第五步：填写答案

#### 页面结构理解

学习通答题页面的 DOM 结构：

```
页面
├── 外层容器
│   ├── 单选题区域 [role="radio"]
│   │   └── 每个 option 有 role="radio" 属性
│   ├── 填空题区域 (iframe)
│   │   └── 每个 iframe 包含一个 contenteditable 区域
│   └── 判断题区域 [role="radio"]
│       └── "对" / "错" 选项
└── 提交按钮
```

#### 单选题/多选题操作

**正确方式 - 通过 ref 属性点击：**
```javascript
// 从 snapshot 中获取 ref 值，例如 e32, e47 等
document.querySelector('[ref="e32"]')?.click();
```

**或者通过索引点击（需要先确认索引）：**
```javascript
const radios = document.querySelectorAll('[role="radio"]');
radios[目标索引]?.click();
```

**验证是否选中成功：**
```javascript
// 检查 aria-checked 属性
const isChecked = radio.getAttribute('aria-checked') === 'true';
// 或者检查 class 是否包含选中状态
```

⚠️ **重要：click() 可能不会立即更新 aria-checked！**
- 需要等待一小段时间后再验证
- 如果未选中，尝试 dispatchEvent 方式

**可靠的点击方式：**
```javascript
function clickRadio(ref) {
  const el = document.querySelector('[ref="' + ref + '"]');
  if (!el) return false;
  
  // 方法1：直接 click
  el.click();
  
  // 方法2：如果没生效，用 dispatchEvent
  if (el.getAttribute('aria-checked') !== 'true') {
    el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  }
  
  // 方法3：聚焦后按回车
  el.focus();
  el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
  
  return true;
}
```

#### 填空题操作

**填空题在 iframe 中，需要特殊处理：**
```javascript
const iframes = document.querySelectorAll('iframe');

// 找到填空题的 iframe（通常前几个是填空题）
if (iframes[i] && iframes[i].contentDocument) {
  iframes[i].contentDocument.body.innerHTML = '<p>答案内容</p>';
}
```

**注意：**
- iframe 的 src 可能是 `javascript:void(...)` 内联 iframe
- 使用 `contentDocument` 访问内部文档
- 答案格式通常用 `<p>答案</p>` 包裹

#### 判断题操作

与单选题相同方式，只是选项是"对"/"错"：
```javascript
// 对应的 ref 示例：
// Q13-对: e240
// Q13-错: e244
document.querySelector('[ref="e240"]')?.click(); // 选"对"
document.querySelector('[ref="e244"]')?.click(); // 选"错"
```

### 第六步：验证所有答案

**提交前的完整检查清单：**

```javascript
async function verifyAllAnswers() {
  const result = {
    singleChoice: { selected: [], total: 0 },
    fillInBlank: { filled: [], total: 0 },
    judge: { selected: [], total: 0 },
    allComplete: false
  };
  
  // 1. 检查所有 radio 按钮
  const radios = document.querySelectorAll('[role="radio"]');
  let selectedRadios = [];
  radios.forEach((radio, i) => {
    if (radio.getAttribute('aria-checked') === 'true') {
      selectedRadios.push({
        index: i,
        text: radio.textContent.replace(/\s+/g, ' ').trim().substring(0, 30)
      });
    }
  });
  result.singleChoice.selected = selectedRadios;
  result.singleChoice.total = radios.length / 4; // 每4个一组（ABCD）
  
  // 2. 检查填空题 iframe
  const iframes = document.querySelectorAll('iframe');
  let filledBlanks = [];
  for (let i = 0; i < Math.min(iframes.length, 10); i++) {
    try {
      const text = iframes[i].contentDocument?.body?.textContent?.trim();
      if (text && text.length > 0) {
        filledBlanks.push({ index: i, content: text.substring(0, 20) });
      }
    } catch(e) {}
  }
  result.fillInBlank.filled = filledBlanks;
  result.fillInBlank.total = filledBlanks.length; // 实际有内容的数量
  
  // 3. 判断完整性
  const expectedTotal = /* 从题目信息获取总题数 */;
  result.allComplete = 
    result.singleChoice.selected.length >= expectedSingleChoice &&
    result.fillInBlank.filled.length >= expectedFillInBlank &&
    result.judge.selected.length >= expectedJudge;
  
  return result;
}
```

### 第七步：提交作业

**定位并点击提交按钮：**
```javascript
// 提交按钮通常是 button 元素
const buttons = document.querySelectorAll('button');
for (let btn of buttons) {
  if (btn.textContent.includes('提交')) {
    btn.click();
    break;
  }
}
```

**处理确认弹窗：**
```javascript
// 学习通可能会弹出确认对话框
if (window.confirm) {
  // 自动确认
}
```

## 答案输入格式

用户可以通过以下方式提供答案：

### 格式1：JSON 结构化答案
```json
{
  "singleChoice": [
    {"q": 1, "answer": "C"},
    {"q": 2, "answer": "B"}
  ],
  "fillInBlank": [
    {"q": 9, "answers": ["子项目"]},
    {"q": 10, "answers": ["清单", "图表"]}
  ],
  "judge": [
    {"q": 13, "answer": "对"},
    {"q": 14, "answer": "错"}
  ]
}
```

### 格式2：简化的文本描述
```
单选题：
1. C
2. B
...

填空题：
9. 子项目
10. 清单、图表
...

判断题：
13. 对
14. 错
...
```

## 常见问题与解决方案

### 问题1：页面显示"作答状态异常"
**原因：** 作业已经提交过，无法重新作答
**解决：** 需要联系老师开启重新作答权限，或使用新的 answerId

### 问题2：点击选项后未选中
**原因：** 
- 页面使用了自定义事件处理
- 需要先聚焦父元素
- iframe 跨域限制

**解决方案：**
```javascript
// 尝试多种点击方式
async function reliableClick(element) {
  // 方式1
  element.click();
  await new Promise(r => setTimeout(r, 100));
  
  // 方式2
  element.dispatchEvent(new MouseEvent('click', {bubbles: true}));
  await new Promise(r => setTimeout(r, 100));
  
  // 方式3：模拟真实用户行为
  element.focus();
  await new Promise(r => setTimeout(r, 50));
  element.dispatchEvent(new KeyboardEvent('keydown', {key: ' ', bubbles: true}));
  await new Promise(r => setTimeout(r, 50));
  element.dispatchEvent(new KeyboardEvent('keyup', {key: ' ', bubbles: true}));
}
```

### 问题3：找不到提交按钮
**原因：** 提交按钮可能在动态加载的内容中
**解决：** 等待页面完全加载后再查找，或使用 `browser_snapshot` 获取最新 DOM

### 问题4：跨域 iframe 无法访问
**现象：** `SecurityError: Blocked a frame from accessing`
**说明：** 这是正常的安全限制
**解决：** 对于内联 iframe（src 为 javascript:），通常可以直接访问；对于跨域外部 iframe，可能需要使用其他方式

### 问题5：作业时间即将截止
**建议：** 
- 优先确保单选题和判断题正确（占大部分分数）
- 填空题相对简单，快速填写即可
- 先保存草稿，再仔细核对

## 最佳实践

### 1. 操作顺序
1. 先导航到作业页面
2. 获取页面快照（snapshot）分析结构
3. 按题目类型批量填写
4. 每填写一题就验证
5. 全部完成后统一检查
6. 最后提交

### 2. 错误恢复
- 如果页面异常，重新导航到作业 URL
- 保留 enc 参数，这是身份验证的关键
- 如果答案丢失，快速重新填写（不要从头分析）

### 3. 性能优化
- 使用 `browser_evaluate` 批量操作，减少往返次数
- 将多个点击操作合并到一个 evaluate 调用中
- 避免频繁调用 snapshot（会产生大文件）

## 完整示例代码

### 示例：完成一份作业
```javascript
// ====== 配置 ======
const WORK_URL = 'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/dowork?...';

// ====== 步骤1：导航到作业页 ======
await page.goto(WORK_URL);
await page.waitForLoadState('networkidle');

// ====== 步骤2：获取页面结构 ======
// 使用 browser_snapshot 获取完整的 DOM 结构
// 分析出每个选项的 ref 或索引

// ====== 步骤3：填写单选题 ======
await page.evaluate(() => {
  // 单选题答案映射（根据实际题目）
  const answers = {
    1: 'e32',  // Q1 选 C
    2: 'e47',  // Q2 选 B
    3: 'e74',  // Q3 选 D
    // ... 更多
  };
  
  Object.values(answers).forEach(ref => {
    document.querySelector('[ref="' + ref + '"]')?.click();
  });
});

// ====== 步骤4：填写填空题 ======
await page.evaluate(() => {
  const iframes = document.querySelectorAll('iframe');
  const blankAnswers = ['子项目', '清单', '图表', '工作包'];
  iframes.forEach((iframe, i) => {
    if (iframe.contentDocument && blankAnswers[i]) {
      iframe.contentDocument.body.innerHTML = '<p>' + blankAnswers[i] + '</p>';
    }
  });
});

// ====== 步骤5：填写判断题 ======
await page.evaluate(() => {
  const judgeAnswers = ['e240', 'e255', 'e262']; // 对/错 的 ref
  judgeAnswers.forEach(ref => {
    document.querySelector('[ref="' + ref + '"]')?.click();
  });
});

// ====== 步骤6：验证 ======
const checkResult = await page.evaluate(() => {
  const radios = document.querySelectorAll('[role="radio"]');
  let count = 0;
  radios.forEach(r => { if (r.getAttribute('aria-checked') === 'true') count++; });
  return count;
});
console.log(`已选择 ${checkResult} 个选项`);

// ====== 步骤7：提交 ======
await page.evaluate(() => {
  document.querySelector('button')?.click(); // 提交按钮
});
```

## 注意事项

1. **不要自动提交**：除非用户明确要求，否则只填写不提交
2. **保留原始答案**：方便用户核对和修改
3. **处理异常情况**：网络超时、页面刷新等
4. **尊重平台规则**：避免过于明显的自动化特征
5. **及时反馈进度**：让用户知道当前状态
