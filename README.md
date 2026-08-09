<div align="center">

**中文** · [English](./README.en.md)

</div>

# mem-wrap-up

> 7 步 session 收尾流水线：memory 健康检查 → 5 phase 审计 → fileCount 同步 → 文档同步 spot-check → 复利经验沉淀 → 4 步 verify → memory 层同步 + 深度复检。

[![license](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

## 解决什么问题

> AI 说"已同步、已落地、已更新"的时候，我的第一反应是去 Grep 一下。不是不信任，是被骗太多次了。

你大概也遇到过：一个 session 结束，AI 直接关窗走人。结论没验证、经验没沉淀、上下文没交接——全甩给下一个 session 的你。还有那个经典场面：AI 信誓旦旦说"版本号已更新、memory 已写入"，你打开文件一看，还是旧值。收尾不收尾，差别就是"下一次从坑里爬出来"和"从零开始"。

本 skill 把收尾固化为 7 步流水线，核心两条铁律：

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

**方式 A：自然语言安装（推荐）**

在 Claude Code、Codex 等支持 Agent Skills 的工具里，直接说：

```text
帮我安装这个 skill：https://github.com/1273984347/mem-wrap-up
```

Agent 会自动 clone 到 skills 目录并注册，不用手动找路径。工具不支持时，手动复制：

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

**怎么触发**（说这些就会跑起来）：

```
收尾
帮我 wrap up 一下
这个 session 快结束了，整理一下
文档和代码对不上了，帮我同步
```

## MCP 接入（可选）

本 skill 与 MCP **互补而非依赖**：MCP 提供外部系统连接，本 skill 负责收尾编排。MCP 作为**可选增强**，无 MCP 时自动回退到内建工具（Grep/Read/Test-Path）。

**典型接入场景**：

| MCP 类型 | 用途 | 增强点 |
|---|---|---|
| 服务状态 MCP | 查询部署 / 服务健康 | 6 面状态矩阵「运行态」面的真实证据源 |
| 通知 MCP（如 IM / 邮件） | 收尾汇报推送 | 分阶段汇报模板的自动化投递 |
| 数据库 / Schema MCP | 校验 schema 与文档一致性 | 4a 文档同步 spot-check 的独立核对 |

**接入步骤**：
1. 在你的 agent 配置中启用对应 MCP server；
2. 在 SKILL.md 的 `compatibility` 字段声明「可选 MCP：xxx」，并注明 fallback 规则；
3. skill 内写「有 xxx MCP 则调用其验证，无则用内建工具」——绝不因 MCP 缺失而中断收尾流程。

## 版本兼容性

| 检查项 | 值 |
|---|---|
| SKILL.md 版本 | 1.1.0 |
| Agent Skills 标准 | 兼容（[agentskills.io](https://agentskills.io) 开放标准，frontmatter: name/description/license/metadata） |
| frontmatter 校验 | 通过 `skills-ref validate`（CI 自动检查，见 [.github/workflows/validate.yml](.github/workflows/validate.yml)） |
| 运行依赖 | 无 Python/Node 脚本；需文件搜索（Grep/Read）+ shell（Test-Path/Measure 示例，跨平台需相应调整） |
| MCP 依赖 | 无（可选接入） |
| 联动 skill | [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）/ [self-evolution](https://github.com/1273984347/self-evolution)（沉淀）——不装也能独立运行 |

**客户端兼容矩阵**：

| 客户端 | 安装方式 | 支持 |
|---|---|---|
| TRAE | 复制目录到 skills 目录，自动注册 | ✅ |
| Claude Code | `/plugin marketplace add` 或复制目录 | ✅ |
| Codex / Cursor / OpenCode 等 | 复制目录（Agent Skills 标准客户端） | ✅ |
| 其他 | 需支持 SKILL.md frontmatter + 渐进披露 | 视实现 |

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
