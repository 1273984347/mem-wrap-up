#!/usr/bin/env python3
"""Read-only runtime audit for the mem-wrap-up 6-surface matrix "runtime" face.

Probes what the user actually gets (not just what the code says):

  1. Listening ports extracted from project config
     (package.json, .env, docker-compose.yml, README port hints)
  2. Health endpoints on listening ports (/health, /ready, /api/health)
  3. Deploy markers (deploy notes, .deployed, REVISION, container refs)
  4. Build staleness (dist/ vs src/ last-modified comparison)

Design rules:
  - Pure read-only: never writes, never deletes, never executes project scripts.
  - Pure Python stdlib: cross-platform (Windows / macOS / Linux).
  - Each probe reports one of: verified / stale / not-found / not-applicable,
    matching the 6-surface matrix status vocabulary.

Caveat: the port probe is a heuristic. A listening socket on a config-derived
port proves that *something* answers locally, not that *this project's* service
is the process behind it (another local service may occupy the port). Treat
port/health results as heuristic evidence, never as sole proof of "verified".

Usage:
  python scripts/runtime-audit.py [--project-dir PATH] [--port PORT] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
from datetime import datetime
from pathlib import Path

HEALTH_PATHS = ("/health", "/ready", "/api/health", "/healthz")
MARKER_FILES = (
    "deploy.md",
    "DEPLOY.md",
    ".deployed",
    "REVISION",
    "release-state.json",
    "container.manifest",
)
BUILD_DIRS = ("dist", "build", "out")
SOURCE_DIRS = ("src", "app", "lib")

CAVEAT = (
    "port probe is heuristic: a listening socket on a config-derived port "
    "does not prove this project's service is the one answering"
)


def find_config_ports(project: Path) -> list[int]:
    """Extract candidate ports from common project config files."""
    ports: set[int] = set()

    env_file = project / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"\s*PORT\s*=\s*(\d{1,5})", line)
            if m:
                ports.add(int(m.group(1)))

    pkg = project / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            for field in ("start", "dev", "serve"):
                script = (data.get("scripts") or {}).get(field, "")
                for m in re.finditer(r"(?:--port|-p)\s+(\d{1,5})|PORT=(\d{1,5})", script):
                    ports.add(int(m.group(1) or m.group(2)))
        except (json.JSONDecodeError, OSError):
            pass

    compose = project / "docker-compose.yml"
    if compose.exists():
        text = compose.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'"?\d{1,5}:\d{1,5}"?', text):
            left = m.group(0).strip('"').split(":")[0]
            if left.isdigit():
                ports.add(int(left))

    readme = project / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"localhost:(\d{1,5})|127\.0\.0\.1:(\d{1,5})", text):
            ports.add(int(m.group(1) or m.group(2)))

    return sorted(ports)


def probe_port(port: int, host: str = "127.0.0.1", timeout: float = 0.8) -> bool:
    """Return True if something is listening on host:port."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def probe_health(port: int, timeout: float = 2.0) -> tuple[str, int]:
    """Probe common health endpoints on a listening port.

    Returns (verified_path, http_status) or ("", 0) if none responded.
    """
    for path in HEALTH_PATHS:
        try:
            req = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: localhost:{port}\r\n"
                "Connection: close\r\n\r\n"
            )
            with socket.create_connection(("127.0.0.1", port), timeout=timeout) as sock:
                sock.sendall(req.encode("ascii"))
                resp = sock.recv(256).decode("ascii", errors="ignore")
            status = resp.split(" ", 2)[1] if " " in resp else "0"
            if resp.startswith("HTTP/"):
                return path, int(status) if status.isdigit() else 0
        except OSError:
            continue
    return "", 0


def find_deploy_markers(project: Path) -> list[Path]:
    """Find deployment marker files at project root (one level deep)."""
    found: list[Path] = []
    for name in MARKER_FILES:
        candidate = project / name
        if candidate.exists():
            found.append(candidate)
    return found


def build_staleness(project: Path) -> tuple[float | None, float | None]:
    """Return (latest_build_mtime, latest_source_mtime) or None where absent."""
    build_latest: float | None = None
    for d in BUILD_DIRS:
        build_dir = project / d
        if build_dir.is_dir():
            for p in build_dir.rglob("*"):
                if p.is_file():
                    build_latest = max(build_latest or 0, p.stat().st_mtime)

    source_latest: float | None = None
    for d in SOURCE_DIRS:
        src_dir = project / d
        if src_dir.is_dir():
            for p in src_dir.rglob("*"):
                if p.is_file():
                    source_latest = max(source_latest or 0, p.stat().st_mtime)

    return build_latest, source_latest


def fmt_time(ts: float | None) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M") if ts else "-"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", default=".", help="project root to audit")
    parser.add_argument("--port", type=int, help="explicit port override")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        print(f"error: not a directory: {project}", file=sys.stderr)
        return 1

    report: dict[str, object] = {"project": str(project), "caveat": CAVEAT}

    # 1) Listening ports
    ports = [args.port] if args.port else find_config_ports(project)
    report["config_ports"] = ports
    listening = [p for p in ports if probe_port(p)]
    report["listening_ports"] = listening
    report["port_status"] = (
        "verified" if listening
        else ("not-applicable" if not ports else "not-found")
    )

    # 2) Health endpoints
    health: list[dict[str, object]] = []
    for port in listening:
        path, status = probe_health(port)
        if path:
            health.append({"port": port, "path": path, "status": status})
    report["health_endpoints"] = health
    report["health_status"] = "verified" if health else "not-found"

    # 3) Deploy markers
    markers = [str(p.relative_to(project)) for p in find_deploy_markers(project)]
    report["deploy_markers"] = markers
    report["deploy_status"] = "verified" if markers else "not-found"

    # 4) Build staleness
    build_ts, src_ts = build_staleness(project)
    report["build_latest"] = fmt_time(build_ts)
    report["source_latest"] = fmt_time(src_ts)
    if build_ts is None and src_ts is None:
        report["build_status"] = "not-applicable"
    elif build_ts is None:
        report["build_status"] = "stale"  # sources exist but no build output
    elif src_ts is None or build_ts >= src_ts:
        report["build_status"] = "verified"
    else:
        report["build_status"] = "stale"  # sources newer than build output

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"runtime audit: {report['project']}")
        print(f"  caveat            : {CAVEAT}")
        print(f"  config ports      : {ports}  -> listening: {listening}  [{report['port_status']}]")
        for h in health:
            print(f"  health            : :{h['port']}{h['path']} -> {h['status']}")
        if not health and listening:
            print("  health            : no /health-like endpoint responded  [not-found]")
        print(f"  deploy markers    : {markers or 'none'}  [{report['deploy_status']}]")
        print(f"  build vs source   : build={report['build_latest']}  source={report['source_latest']}  [{report['build_status']}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
