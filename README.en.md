<div align="center">

[中文](./README.md) · **English**

</div>

# mem-wrap-up

> A 7-step session wrap-up pipeline: memory health check → 5-phase audit → fileCount sync → doc-sync spot-check → compounding-experience sedimentation → 4-step verify → memory-layer sync + deep re-review.

[![license](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![CI](https://github.com/1273984347/mem-wrap-up/actions/workflows/validate.yml/badge.svg)](https://github.com/1273984347/mem-wrap-up/actions/workflows/validate.yml)
[![skills-ref](https://img.shields.io/badge/skills--ref-passing-2ea44f)](https://agentskills.io)
[![version](https://img.shields.io/badge/version-v1.1.0-1d76db)](https://github.com/1273984347/mem-wrap-up/releases/latest)

## What problem it solves

> When an AI says "synced, landed, updated," my first instinct is to grep. Not distrust — I've been burned too many times.

You've probably seen it too: a session ends and the AI just closes the window. Unverified conclusions, unsedimented experience, unwrapped context — all dumped on the next session's you. And the classic scene: the AI swears "version number updated, memory written," you open the file, and it's still the old value. The difference between wrapping up and not is "crawling out of a pit" vs "starting from zero."

This skill hardens wrap-up into a 7-step pipeline with two iron laws:

1. **Verification iron law**: grep spot-check actual file contents to verify the version number + task ID really landed — **never trust "it's done" claims** (a successful edit ≠ content changed; git-tracked ≠ committed).
2. **Knowledge governance**: a 6-surface state matrix audits consistency (code / runtime / docs / rules / memory / workspace) + a graduation criterion for compounding experience (when memory graduates to an authoritative doc).

## Core capabilities

- **7-step pipeline**: health check → 5-phase audit (frontmatter/dup/empty/big-file/broken-link) → fileCount sync → doc-sync spot-check + work-log (4-section schema) → sediment → 4-step verify → memory-layer spot-check + DRL reverse review
- **6-surface state matrix**: each surface marked `verified-current / pending / not-applicable` — never fabricate evidence
- **Memory write protocol**: Read-before-Edit → Grep-verify-after-Edit → Retry-on-fail (≤3)
- **Memory graduation criterion**: stable mechanism / recurring ≥3 times / must-know for the next maintainer → graduate to docs; one-off incidents stay in memory
- **Phased report template**: impact / changes / pending / leftovers, explicitly listing pending & out-of-scope

## Installation

A standard Agent Skill (`SKILL.md` + `references/`), installable by any Agent Skills client. Pick one:

**Option A: natural-language install (recommended)**

In Claude Code, Codex, or any Agent Skills client, just say:

```text
Install this skill: https://github.com/1273984347/mem-wrap-up
```

The agent clones it into your skills directory and registers it automatically. If your tool doesn't support that, copy it manually:

```bash
git clone https://github.com/1273984347/mem-wrap-up.git
cp -r mem-wrap-up <your-skills-dir>/mem-wrap-up
```

**Option B: Claude Code plugin marketplace (one command)**

```text
/plugin marketplace add 1273984347/mem-wrap-up
/plugin install mem-wrap-up@mem-wrap-up
```

**Option C: skills.sh CLI (the npm of agents)**

```bash
npm install -g @anthropic-ai/skills
npx skills add https://github.com/1273984347/mem-wrap-up
```

## Usage

Triggered on session wrap-up, user saying "wrap up / 收尾", a sedimented workflow to continue, or docs/code mismatch.

**How to trigger** (say any of these):

```
Wrap up
Help me wrap up
This session is ending — tidy it up
Docs and code are out of sync — sync them for me
```

## MCP integration (optional)

This skill and MCP are **complementary, not dependent**: MCP provides external system connections; the skill orchestrates wrap-up. MCP is an **optional enhancement** — without it, the skill falls back to built-in tools (Grep/Read/Test-Path).

**Typical integrations**:

| MCP type | Purpose | Enhancement |
|---|---|---|
| Service-status MCP | Query deployment / service health | Real evidence for the "runtime" surface of the 6-surface matrix |
| Notification MCP (e.g. IM / email) | Deliver the wrap-up report | Auto-delivery of the phased report template |
| Database / schema MCP | Verify schema vs doc consistency | Independent check for step 4a doc-sync spot-check |

**Steps**:
1. Enable the MCP server in your agent config;
2. Declare "optional MCP: xxx" in the SKILL.md `compatibility` field with a fallback rule;
3. In-skill instruction: "use the MCP if present, else built-in tools" — never break the wrap-up on a missing MCP.

## Version compatibility

| Check | Value |
|---|---|
| SKILL.md version | 1.1.0 |
| Agent Skills standard | Compatible ([agentskills.io](https://agentskills.io); frontmatter: name/description/license/metadata) |
| Frontmatter validation | `skills-ref validate` (CI, see [.github/workflows/validate.yml](.github/workflows/validate.yml)) |
| Runtime deps | No Python/Node scripts; needs file search (Grep/Read) + shell (Test-Path/Measure examples, adjust per platform) |
| MCP deps | None (optional) |
| Linked skills | [deep-review-loop](https://github.com/1273984347/deep-review-loop) (review) / [self-evolution](https://github.com/1273984347/self-evolution) (evolution) — works standalone |

**Client compatibility**:

| Client | Install method | Support |
|---|---|---|
| TRAE | Copy folder into skills dir, auto-registered | ✅ |
| Claude Code | `/plugin marketplace add` or copy folder | ✅ |
| Codex / Cursor / OpenCode etc. | Copy folder (Agent Skills standard clients) | ✅ |
| Others | Requires SKILL.md frontmatter + progressive disclosure | Depends |

## Environment

- Needs file search (Grep/Read) + shell (Test-Path/Measure examples; adjust per platform).
- All memory paths use `<memory_root>` / `<project-slug>` placeholders — replace per your environment.
- Step 7 links to [deep-review-loop](https://github.com/1273984347/deep-review-loop): if the standalone skill is installed, call it; otherwise execute the 5 rounds manually per protocol.

## Related repos

- [agent-session-loop](https://github.com/1273984347/agent-session-loop) — all-in-one review → wrap-up → evolution pipeline
- [deep-review-loop](https://github.com/1273984347/deep-review-loop) — review (linked in Step 7)
- [self-evolution](https://github.com/1273984347/self-evolution) — evolution (consumes sediment/audit/work-log)

## License

[Apache-2.0](LICENSE)
