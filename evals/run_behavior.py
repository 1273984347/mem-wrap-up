#!/usr/bin/env python3
"""Executable behavior evals for mem-wrap-up (deterministic mode, CI-safe)."""

from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = ROOT / "evals"

VERSION_RE = re.compile(r"v(\d+\.\d+\.\d+)")


def scene_checks(eval_id: int, ws: Path) -> list[tuple[str, bool]]:
    """Return [(description, holds)] assertions for this eval's fixture workspace."""
    checks: list[tuple[str, bool]] = []

    if eval_id == 1:
        # eval 1 (stale-docs)：CHANGELOG 头部为 v2.1.0（当前段），README 头部仍声明 v2.0.0（stale）。
        cl, rd = ws / "CHANGELOG.md", ws / "README.md"
        checks.append(("CHANGELOG.md 存在", cl.exists()))
        checks.append(("README.md 存在", rd.exists()))
        if cl.exists() and rd.exists():
            cl_text = cl.read_text(encoding="utf-8")
            rd_text = rd.read_text(encoding="utf-8")
            cl_ver = VERSION_RE.search(cl_text)
            rd_ver = VERSION_RE.search(rd_text)
            checks.append(("CHANGELOG 头部版本号可提取", cl_ver is not None))
            checks.append(("README 头部版本号可提取", rd_ver is not None))
            checks.append((
                "README 头部版本与 CHANGELOG 当前版本不一致（stale 缺陷存在）",
                cl_ver is not None and rd_ver is not None and rd_ver.group(1) != cl_ver.group(1),
            ))
            checks.append(("CHANGELOG 保留历史版本段（v2.0.0 历史记录应保留）", "v2.0.0" in cl_text))

    elif eval_id == 2:
        # eval 2 (memory-sync)：work-log.md 缺 4 段 schema 的 verification cost 段、
        # topics.md 缺 session_id 字段，且存在未闭合项（pending review）。
        base = ws / "memory" / "projects" / "demo" / "20260810"
        topics, wl = base / "topics.md", base / "work-log.md"
        checks.append(("topics.md 存在", topics.exists()))
        checks.append(("work-log.md 存在", wl.exists()))
        if topics.exists():
            t_text = topics.read_text(encoding="utf-8")
            checks.append(("topics.md 缺 session_id 字段（含缺失标记，Grep 可发现）", "缺 session_id" in t_text))
            checks.append(("topics.md 存在未闭合项（pending review 状态）", "pending" in t_text))
        if wl.exists():
            w_text = wl.read_text(encoding="utf-8")
            checks.append(("work-log.md 缺 verification cost 段（4 段 schema 缺口）", "verification cost" in w_text))
            checks.append(("work-log.md 的 session_id 未填写（假收敛）", "未填写" in w_text))
        checks.append(("retrospective.md 缺失（retro_link 指向但三件套不完整）", not (base / "retrospective.md").exists()))

    elif eval_id == 3:
        # eval 3 (sedimentation)：experience-log.md 存在可沉淀经验条目（含根因与毕业判据线索）。
        exp, pm = ws / "experience-log.md", ws / "project_memory.md"
        checks.append(("experience-log.md 存在", exp.exists()))
        checks.append(("project_memory.md 存在", pm.exists()))
        if exp.exists():
            e_text = exp.read_text(encoding="utf-8")
            checks.append((
                "experience-log.md 含 ≥1 条经验记录（2026-08-08 tRPC 迁移条目）",
                "2026-08-08" in e_text and "tRPC" in e_text,
            ))
            checks.append((
                "经验条目含结构化三段（踩坑/根因/下次怎么做）",
                all(s in e_text for s in ("踩坑", "根因", "下次怎么做")),
            ))
            checks.append(("经验含根因深度（5Why 线索：根因段存在）", "根因" in e_text))
            checks.append(("含毕业判据线索（同类出现 ≥3 次 → 应沉淀/毕业）", "3 次" in e_text))

    elif eval_id == 4:
        # eval 4 (closeout-report)：workspace.md 存在待收尾项（删除候选 / 待确认 / pending 遗留）。
        ws_md = ws / "workspace.md"
        checks.append(("workspace.md 存在", ws_md.exists()))
        if ws_md.exists():
            text = ws_md.read_text(encoding="utf-8")
            checks.append(("工作区存在会话残留（待收尾项）", "会话残留" in text))
            checks.append(("含删除候选清单（未确认前不删除）", "删除候选" in text))
            checks.append(("含待确认标记（删除候选待确认）", "待确认" in text))
            checks.append(("含 pending 遗留项（cache 层文档未更新）", "pending" in text))

    return checks


def main() -> None:
    data = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    failures = 0
    for ev in data["evals"]:
        ws = ROOT / ev["files"][0]
        if not ws.is_dir():
            print(f"FAIL: eval {ev['id']} fixture missing: {ws}"); failures += 1; continue
        checks = scene_checks(ev["id"], ws)
        failed = [(d, ok) for d, ok in checks if not ok]
        if failed:
            failures += 1
            for d, ok in failed:
                print(f"  FAIL: {d}")
        else:
            print(f"PASS: eval {ev['id']} ({ev['name']}) - {len(checks)} assertions hold")
    if failures:
        sys.exit(f"{failures} behavior eval(s) failed")
    print(f"mem-wrap-up: all behavior evals passed ({len(data['evals'])} evals)")


if __name__ == "__main__":
    main()
