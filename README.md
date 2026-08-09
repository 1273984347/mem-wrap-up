# mem-wrap-up

> 7 步 session 收尾流水线：memory 健康检查 → 5 phase 审计 → fileCount 同步 → 文档同步 spot-check → 复利经验沉淀 → 4 步 verify → memory 层同步 + 深度复检。

## 解决什么问题

session 结束时不收尾 = 结论没验证、经验没沉淀、交接成本转嫁给下一个 session。本 skill 把收尾固化为 7 步流水线，重点是两件事：

1. **验证铁律**：Grep spot-check 文件内容，验证版本号 + 任务 ID 实际落地——**不信任「已落地」声明**（Edit 成功 ≠ 内容已修改，git tracked ≠ 内容已提交）。
2. **知识治理**：6 面状态矩阵审计一致性（代码/运行态/文档/规则/记忆/工作区）+ 复利经验毕业判据（何时从 memory 升级为权威文档）。

## 核心能力

- **7 步流水线**：健康检查 → 5 phase audit（frontmatter/dup/empty/big-file/broken-link）→ fileCount sync → 文档同步 spot-check + work-log（4 段 schema）→ sediment 沉淀 → 4-step verify → memory 层 spot-check + DRL 反向审查
- **6 面状态矩阵**：逐面标 `verified-current / pending / not-applicable`，不编造证据
- **memory 写入协议**：Read-before-Edit → Grep-verify-after-Edit → Retry-on-fail（≤3 次）
- **记忆毕业判据**：稳定机制 / 反复出现 ≥3 次 / 接手者必须知道 → 毕业到 docs；一次性事故留在 memory
- **分阶段汇报模板**：影响 / 改动 / 待确认 / 遗留，明确列出 pending 与 out-of-scope

## 安装

标准 Agent Skill（`SKILL.md` + `references/`），任何支持 Agent Skills 的客户端都能装。三种方式任选：

**方式 A：直接复制（通用）**

```bash
git clone https://github.com/1273984347/mem-wrap-up.git
cp -r mem-wrap-up <your-skills-dir>/mem-wrap-up
```

**方式 B：Claude Code 插件市场（一条命令）**

```text
/plugin marketplace add 1273984347/mem-wrap-up
/plugin install mem-wrap-up@mem-wrap-up
```

**方式 C：skills.sh CLI（Agent 界的 npm）**

```bash
npm install -g @anthropic-ai/skills
npx skills add https://github.com/1273984347/mem-wrap-up
```

## 使用

session 收尾、用户说「收尾 / wrap up」、工作流已沉淀需继续、或文档与代码不一致时触发。

## 环境适配

- 需要文件搜索（Grep/Read）+ shell（Test-Path/Measure 示例，跨平台需相应调整）。
- 所有 memory 路径使用 `<memory_root>` / `<project-slug>` 占位符，按你的环境替换。
- Step 7 联动 [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）：装了独立 skill 直接调用；未装则按协议手动执行 5 轮。

## 相关仓库

- [agent-session-loop](https://github.com/1273984347/agent-session-loop)（整合版：审查→收尾→沉淀流水线）
- [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查：Step 7 联动）
- [self-evolution](https://github.com/1273984347/self-evolution)（沉淀：sediment/audit/work-log 喂给复盘维度）

## 许可证

[Apache-2.0](LICENSE)
