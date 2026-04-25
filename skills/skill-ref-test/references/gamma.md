# Gamma Configuration

[VERIFICATION:GAMMA_MARKER]

## 配置概述

Gamma 配置项定义了数字炼金系统的全局配置参数。

## 配置结构

```yaml
gamma:
  system:
    name: DigitalAlchemist
    version: 2.0.0
    mode: production

  rendering:
    engine: webgl
    quality: high
    fps_target: 60

  effects:
    particles:
      enabled: true
      count: 1500
      interactive: true
    blur:
      enabled: true
      intensity: 0.5
```

## 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| GAMMA_ENV | production | 运行环境 |
| GAMMA_DEBUG | false | 调试模式 |
| GAMMA_CACHE | true | 启用缓存 |

## 初始化

```javascript
import { gammaConfig } from './gamma';

gammaConfig.init({
  system: { name: 'MyAlchemist' },
  rendering: { quality: 'ultra' }
});
```

---

**验证标记**: [VERIFICATION:GAMMA_MARKER]
