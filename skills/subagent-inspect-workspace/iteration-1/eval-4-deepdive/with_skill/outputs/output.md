# Eval 4: 最大Agent深度审计

找到 agent-a7d9792fb5c466b6e（555KB，359行），任务：研究MCP图片处理机制。
主要执行步骤：MCP规范→源码404→Playwright MCP→npm包分析→二进制逆向(strings claude.exe)→被中断。

关键发现：通过strings反编译获取了ImageContent转换格式、32MB图片限制常量、hooks字段名。
