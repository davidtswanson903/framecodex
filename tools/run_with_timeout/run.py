#!/usr/bin/env python3
"""Run a command with a hard timeout and minimal, deterministic reporting.

This is intended to mitigate wedged or long-running gates in CI and locally.

Usage:
  tools/run_with_timeout/run.py --seconds 120 --out out/<gate>/log.txt -- <cmd> [args...]

Exit codes:
  - returns the child process exit code if it completes
  - returns 124 on timeout

Notes:
  - Writes combined stdout/stderr to the log file.
  - Also prints a short tail to stdout for quick visibility.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def tail_lines(s: str, n: int) -> str:
    lines = s.splitlines()
    if len(lines) <= n:
        return s
    return "\n".join(lines[-n:])


def main() -> None:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--seconds", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tail", type=int, default=80)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    if not args.cmd or args.cmd[0] != "--" or len(args.cmd) < 2:
        print("Expected: -- <cmd> [args...]", file=sys.stderr)
        sys.exit(2)

    cmd = args.cmd[1:]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure non-interactive defaults.
    env = dict(os.environ)
    env.setdefault("GIT_PAGER", "cat")
    env.setdefault("PAGER", "cat")
    env.setdefault("GIT_TERMINAL_PROMPT", "0")

    try:
        p = subprocess.run(
            cmd,
            cwd=os.getcwd(),
            env=env,
            capture_output=True,
            text=True,
            timeout=args.seconds,
            check=False,
        )
        combined = (p.stdout or "") + (p.stderr or "")
        out_path.write_text(combined, encoding="utf-8")
        if combined.strip():
            print(tail_lines(combined, args.tail))
        sys.exit(p.returncode)
    except subprocess.TimeoutExpired as e:
        combined = ""
        if e.stdout:
            combined += e.stdout
        if e.stderr:
            combined += e.stderr
        combined += f"\n[run_with_timeout] TIMEOUT after {args.seconds}s: {' '.join(cmd)}\n"
        out_path.write_text(combined, encoding="utf-8")
        if combined.strip():
            print(tail_lines(combined, args.tail))
        sys.exit(124)


if __name__ == "__main__":
    main()
