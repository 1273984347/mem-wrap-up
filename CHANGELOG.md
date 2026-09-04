# Changelog

本文件记录 mem-wrap-up 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

## [1.1.3] - 2026-09-04

### Fixed
- publish-tessl.yml：TESSL_TOKEN 提升到 job 级 env——step 自身的 env 在它自己的 `if` 求值时尚未应用，原 step 级写法条件恒为 false，配置了 secret 也永远跳过（发布流水线死代码修复）
- GitHub Actions 全部 pin 到 commit SHA（actions/checkout v4/v6、setup-python v5、tesslio/setup-tessl v2），消除可变 tag 的供应链风险
- memory 目录树与 agent-session-loop / self-evolution 统一：补 knowledge/ 三层、experience-log / experience-quickref / skill-usage-checklist 三件套、retrospective（标注写入方），保留 session_memory_*.jsonl——消除三仓库目录树互相矛盾
- verdict 禁词自匹配误报：grep 命中先剔除禁词定义行本身再计数（meta-skill 场景 +「OK」子串误报 TOKEN/BROKEN 等），fragment-lint 新增锚点防漂移
- runtime-audit.py 端口探测标注启发式局限（docstring + JSON `caveat` 字段 + 文本输出）：连接成功 ≠ 本项目服务存活，不作为运行态 `verified` 的唯一依据
- 防 ping-pong 护栏：Step 7b 每次收尾至多执行一轮 DRL，收敛后不再回触重入本 skill

### Changed
- compatibility 字段如实声明：需要文件系统 + shell（PowerShell/POSIX）+ 文件搜索；无 shell 的纯 Web agent 不支持（原文 "Agent-agnostic" 超前）
- CI 加 windows-latest runner（skills-ref 两步在 Windows 跳过：上游 CLI 静默 exit 1）；lint/eval 步骤三平台覆盖
- .gitignore 补 `__pycache__/` 与 `.mimosa/`
- README（中/英）补 token 成本预期；运行依赖行同步 compatibility 修订

## [1.1.2] - 2026-08-31

### Fixed
- 路径预检 + Grep 空结果判别：占位符使用前强制 `test -e`，预检失败中断问用户（漏洞 7/9/15）
- 安全扫描局限标注：0 发现必须附「正则仅覆盖硬编码格式」注记（漏洞 16）
- Step 7 反向审查继承 DRL 出口 ACK 门禁（漏洞 6）

### Added
- LLM 行为 eval（evals/run_behavior_llm.py，发布前手动门禁）
- fragment-lint 交叉引用校验；version-lint 内容漂移软告警
- README badge 改动态 release badge；CI 加 macos-latest runner + skills-ref pin

## [1.1.1] - 2026-08-31

### Fixed
- Step 7b 补「未安装 deep-review-loop 时」的降级声明（精简审查 + 显式标注 `DRL downgraded`，不允许静默省略）
- Step 6 输出改为 P2 ≤ N_max（对齐 deep-review-loop 层 1 P2 残留规则，移除三零目标冲突）
- Step 4b work-log 路径矛盾修正（统一为 memory 路径约定）
- Step 7b R0 描述对齐 4 件套（expected hits 必现 + 项目阶段判定）
- bridge_note 术语补定义

### Added
- session_memory_*.jsonl 加入文件结构约定（步骤 1 / 步骤 5 引用定义）
- runtime-audit.py 分发路径说明（插件路径调用方式）
- scripts/fragment-lint.py 共享片段一致性 lint + CI 接入

### Changed
- 跨平台清理：NEEDS_CONTEXT 信号通用化（去掉 TRAE 平台绑定），compatibility 字段改为 subagent optional
- 新增「无子代理平台的降级模式」：并行 subagent → 串行/主代理分轮内审，独立审查 → 自我对抗（显式标注 `degraded (no-subagent)`），降级 ≠ 跳过
- 四源版本同步（SKILL.md / README / CHANGELOG / marketplace.json）

## [1.1.0] - 2026-08-10

### Added
- 运行态面脚本化：scripts/runtime-audit.py（纯 stdlib、只读、跨平台）
- evals 评估体系：4 个行为场景 fixtures + trigger-eval 12 条触发查询 + 双层 CI
- 英文 README + 中英导航 + 自然语言触发示例
- README 叙事升级（金句 + 痛点故事线）
- GitHub Release v1.1.0、Discussions、项目文档（CONTRIBUTING/CoC/SECURITY/CHANGELOG）

## [1.0.0] - 初始发布

### Added
- 7 步收尾流水线 + 6 面状态矩阵 + memory 写入协议 + 记忆毕业判据
