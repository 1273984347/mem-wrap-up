# Changelog

本文件记录 mem-wrap-up 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

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

## [1.1.1] - 2026-08-31

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
