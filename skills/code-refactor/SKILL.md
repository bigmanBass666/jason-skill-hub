---
name: code-refactor
description: 专门用于 AI Agent 及复杂项目的代码优化与重构。当用户提到代码有 bug、架构混乱、屎山代码、模块不连贯、代码难以维护、想重构项目、需要 code review、遇到奇怪的错误但不知道根因、或者感觉代码越来越难改时，必须使用此 skill。关键词触发：「重构」「屎山」「bug 太多」「架构混乱」「模块耦合」「代码优化」「code review」「refactor」「技术债」「难以维护」「不知道哪里出问题」。即使用户只是说「这段代码越改越乱」也应触发此 skill。
---

# Code Refactor & Optimization Skill

专为 AI Agent 开发中的高复杂度代码库设计的重构方法论。核心原则：**先诊断，再手术；先止血，再重建。**

---

## Phase 0: 快速问诊（必做，<5分钟）

在开始任何分析前，先搞清楚以下几点：

```
1. 项目规模：文件数 / 代码行数大概多少？
2. 最痛的问题是什么？（Bug 频繁？改一处坏另一处？逻辑混乱？）
3. 有没有测试？（有测试 = 重构更安全）
4. 这次重构的目标是什么？（修 bug / 改架构 / 提性能 / 清理代码）
5. 当前最需要先解决的是哪个模块？
```

**不要跳过这步。** 没有问诊就开方子是最大的浪费。

---

## Phase 1: 全局扫描（Codebase Audit）

### 1.1 目录结构审查

```bash
# 快速了解项目结构
find . -type f -name "*.py" | head -50   # Python
find . -type f -name "*.ts" | head -50   # TypeScript
find . -type f -name "*.js" | head -50   # JavaScript

# 查看目录层级
tree -L 3 --gitignore 2>/dev/null || find . -maxdepth 3 -type d | sort
```

分析时关注：
- 有没有明显的「万能文件」（utils.py / helper.js 超过 500 行）
- 有没有循环依赖的迹象
- 命名是否一致（camelCase vs snake_case 混用等）

### 1.2 复杂度热点识别

```bash
# 找出最大的文件（通常是问题集中地）
wc -l **/*.py | sort -rn | head -20

# 找出函数/类过长的文件
grep -n "def \|class " file.py | head -50
```

**红旗信号（直接记录下来）：**
- 单文件 > 500 行
- 单函数 > 80 行  
- 嵌套超过 4 层
- 函数参数超过 6 个
- 同一个概念有多种命名（`agent` / `bot` / `assistant` 混用）

### 1.3 依赖关系图谱

```bash
# Python 项目
pip install pydeps --quiet && pydeps --max-bacon 3 src/

# 手动梳理（更可靠）：
grep -r "^import\|^from" --include="*.py" . | \
  awk -F: '{print $1, $2}' | sort | uniq
```

画出（或用文字描述）模块间的调用关系。**重点找：**
- A 依赖 B，B 又依赖 A（循环依赖）
- 一个模块被几乎所有其他模块依赖（脆弱核心）
- 本该分离的逻辑混在一起（业务逻辑 + IO + 状态管理混杂）

---

## Phase 2: AI Agent 专项诊断

AI Agent 项目有特殊的 bug 模式，以下是最常见的：

### 2.1 状态管理混乱
```
症状：变量在多个地方被修改，不知道当前状态从哪来
检查点：
  □ 有没有全局可变状态？（global 变量、类属性随处修改）
  □ Agent 的 memory / context 是否有明确的读写边界？
  □ 多轮对话的状态传递路径是否清晰？
```

### 2.2 错误处理黑洞
```
症状：报错了但不知道哪一步出的问题，或错误被静默吞掉
检查点：
  □ try/except 里有没有裸 except: pass？
  □ LLM API 调用有没有明确的错误类型处理？
  □ 工具调用（tool call）失败后有没有回退逻辑？
  □ 错误日志是否包含足够的上下文？
```

### 2.3 Prompt 与逻辑耦合
```
症状：改 prompt 影响业务逻辑，改业务逻辑需要改 prompt
检查点：
  □ Prompt 是否硬编码在业务函数里？
  □ 有没有统一的 prompt 管理层？
  □ System prompt 和 user prompt 职责是否清晰？
```

### 2.4 工具调用混乱（Tool/Function Calling）
```
症状：工具被错误调用、参数解析失败、工具结果处理不一致
检查点：
  □ 工具的输入/输出 schema 是否有验证？
  □ 工具调用结果是否有统一的格式化层？
  □ 工具的幂等性如何？（重试会不会有副作用）
```

### 2.5 上下文窗口泄漏
```
症状：随着对话轮次增加，响应变慢、变差、报 token 超限
检查点：
  □ 有没有 context 截断/压缩策略？
  □ 每次传入 LLM 的 messages 有没有上限？
  □ 有没有把不必要的内容（如完整工具结果）放进 context？
```

---

## Phase 3: Bug 根因分析框架

遇到具体 bug 时，用这个框架系统分析，**不要跳着猜**：

```
Step 1: 复现
  → 能稳定复现吗？触发条件是什么？
  → 最小复现用例是什么？

Step 2: 定位
  → 加日志，找到 bug 出现在哪个函数/哪一行
  → 是数据问题（输入不符合预期）还是逻辑问题（处理过程出错）？

Step 3: 溯源
  → 这个错误的数据/状态从哪里来？
  → 往上追溯直到找到第一个「脏数据产生点」

Step 4: 理解影响范围
  → 这个 bug 影响哪些其他模块？
  → 修复这里会不会破坏别处？

Step 5: 修复 + 防护
  → 修复 bug 本身
  → 加类型检查 / 断言 / 日志防止同类 bug 再出现
```

**黄金原则：永远不要在不理解根因的情况下 patch 代码。**

---

## Phase 4: 重构优先级矩阵

根据诊断结果，用这个矩阵决定先改什么：

```
高影响 + 低风险  → 立即重构（Quick Win）
高影响 + 高风险  → 计划重构（需要测试覆盖）
低影响 + 低风险  → 有空再说
低影响 + 高风险  → 暂时别动
```

**影响评估**：这块代码的 bug 频率、被依赖程度、开发摩擦
**风险评估**：是否有测试、改动范围大小、理解程度

---

## Phase 5: 重构执行策略

### 5.1 原则
- **小步前进**：每次重构一个明确的问题，不要大爆炸式重写
- **保持可运行**：每次改动后代码必须能跑起来
- **一次一件事**：不要同时改架构 + 修 bug + 加功能

### 5.2 典型重构动作清单

**提取函数（Extract Function）**
```python
# Before: 100 行函数里混着所有逻辑
# After: 每个函数只做一件事，<30 行

def process_agent_response(response):
    # 只做解析
    parsed = parse_response(response)
    # 只做验证  
    validated = validate_response(parsed)
    # 只做转换
    return format_output(validated)
```

**统一错误处理**
```python
# 建立统一的错误处理层
class AgentError(Exception):
    def __init__(self, message, context=None, recoverable=True):
        self.context = context
        self.recoverable = recoverable
        super().__init__(message)

# 所有 LLM 调用走统一入口
def call_llm_with_retry(messages, **kwargs):
    try:
        ...
    except RateLimitError as e:
        raise AgentError("Rate limit hit", context={"messages_count": len(messages)})
```

**状态集中管理**
```python
# Before: 状态散落各处
# After: 单一数据源
@dataclass
class AgentState:
    conversation_history: list
    current_tool_calls: list
    memory: dict
    metadata: dict
    
    def to_context(self, max_tokens=4000):
        # 统一的 context 截断逻辑
        ...
```

**Prompt 分离**
```python
# Before: prompt 写在业务逻辑里
# After: 独立的 prompt 层
# prompts/system.py
SYSTEM_PROMPT = """..."""

# prompts/templates.py  
def build_tool_result_prompt(tool_name, result, error=None):
    ...
```

### 5.3 重构检查清单

每次重构完成后验证：
```
□ 功能和之前一致（手动测试 or 自动测试）
□ 错误处理没有退化
□ 没有引入新的全局状态
□ 函数命名准确表达意图
□ 删掉了死代码和注释掉的代码
□ 更新了相关注释/文档
```

---

## Phase 6: 架构改善模式

### 6.1 AI Agent 推荐架构分层

```
┌─────────────────────────────────┐
│         Interface Layer          │  ← 接收输入，返回输出，不含逻辑
├─────────────────────────────────┤
│          Agent Core              │  ← 编排逻辑、决策、循环控制
├─────────────────────────────────┤
│          Tool Layer              │  ← 工具定义、调用、结果处理
├─────────────────────────────────┤
│        LLM Gateway               │  ← 所有 LLM 调用的统一入口
├─────────────────────────────────┤
│       State / Memory             │  ← 状态读写，context 管理
├─────────────────────────────────┤
│       External Services          │  ← API、数据库、文件系统
└─────────────────────────────────┘
```

**每层只依赖下层，禁止跨层调用。**

### 6.2 模块边界判断
好的模块边界满足：
- 内部高内聚：同一模块的代码因为同一个原因变化
- 外部低耦合：修改一个模块不需要改动其他模块
- 接口稳定：模块暴露的接口比实现稳定得多

### 6.3 何时应该重写而不是重构

重写的信号（慎重）：
- 架构根本性错误，无法增量修复
- 代码理解成本高于重写成本
- 需求已经和原始设计完全不符

**重写前必须**：明确新架构、有测试验证新实现、分阶段迁移。

---

## 输出模板

完成分析后，按以下格式输出：

```markdown
## 诊断报告

### 🔴 紧急问题（立即处理）
- [问题描述] → [建议修复方案]

### 🟡 重要问题（本周处理）  
- [问题描述] → [建议修复方案]

### 🟢 优化建议（有空处理）
- [问题描述] → [建议修复方案]

### 重构路线图
1. 第一步：[具体操作] - 预计影响：[文件/函数]
2. 第二步：...

### 架构改善建议
[当前架构问题 + 目标架构描述]
```

---

## 附加参考

- 如有具体代码，直接粘贴进来进行 inline review
- 如需深入某个具体问题，参见 `references/` 目录下的专项指南（待扩展）
- 优先解决高频 bug 路径，而不是追求完美架构
