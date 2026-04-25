# Alpha Component Definition

[VERIFICATION:ALPHA_MARKER]

## 组件概述

Alpha 组件是数字炼金系统的核心组件之一，负责将原始代码转换为可视化元素。

## 属性

| 属性名 | 类型 | 描述 |
|--------|------|------|
| name | string | 组件名称 |
| transform | function | 代码转换函数 |
| output | enum | 输出类型：canvas/svg/webgl |

## 使用示例

```javascript
import { Alpha } from './alpha';

const alpha = new Alpha({
  name: 'CodeAlchemist',
  transform: (code) => parseCode(code),
  output: 'webgl'
});

alpha.process('const x = 1;');
```

## 核心方法

### process(code: string): TransformationResult

将代码字符串转换为可视化元素。

### validate(input: unknown): boolean

验证输入是否符合 Alpha 组件规范。

---

**验证标记**: [VERIFICATION:ALPHA_MARKER]
