from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from fcx import __version__
from fcx.gf0 import load_frame_yaml, validate_gf0_struct
from fcx.kernel import Budget, Kernel, KernelCtx
from fcx.profiles.specframe_k1 import PROFILE_VALIDATORS, infer_profile
from fcx.util import read_text, sha256_text, stable_json, write_text_deterministic
from fcx.violations import Report, Violation


def _k_validate_gf0(ctx: KernelCtx, args: Dict[str, Any]):
    frame = Path(args["frame"])
    raw = load_frame_yaml(frame)
    violations = validate_gf0_struct(raw, frame_path=str(frame), budget=ctx.budget, meta_depth=0)
    receipts = {
        "input.frame_sha256": sha256_text(read_text(frame)),
        "kernel": sha256_text("validate_gf0@0.1.0"),
    }
    out = {
        "graph_id": raw.get("graph_id") if isinstance(raw, dict) else "",
        "version": raw.get("version") if isinstance(raw, dict) else "",
    }
    return out, violations, [], receipts


def _k_validate_frame(ctx: KernelCtx, args: Dict[str, Any]):
    frame = Path(args["frame"])
    raw = load_frame_yaml(frame)

    v = validate_gf0_struct(raw, frame_path=str(frame), budget=ctx.budget, meta_depth=0)
    if v:
        return {"phase": "gf0"}, v, [], {"input.frame_sha256": sha256_text(read_text(frame))}

    profile = infer_profile(raw)
    pv = PROFILE_VALIDATORS.get(profile)
    if pv is not None:
        v.extend(pv.validate(ctx, raw, str(frame)))

    receipts = {
        "input.frame_sha256": sha256_text(read_text(frame)),
        "kernel": sha256_text("validate_frame@0.1.0"),
        "profile": profile,
    }
    out = {
        "graph_id": raw.get("graph_id") if isinstance(raw, dict) else "",
        "version": raw.get("version") if isinstance(raw, dict) else "",
        "profile": profile,
    }
    return out, v, [], receipts


KERNELS: Dict[str, Kernel] = {
    "validate_gf0": Kernel(kid="validate_gf0", version="0.1.0", run=_k_validate_gf0),
    "validate_frame": Kernel(kid="validate_frame", version="0.1.0", run=_k_validate_frame),
}


def run_kernel(ctx: KernelCtx, kernel_id: str, args: Dict[str, Any]) -> Report:
    if kernel_id not in KERNELS:
        r = Report(tool={"id": "fcx", "kernel": kernel_id, "version": __version__}, ok=False)
        r.violations.append(
            Violation(code="FCX.E.UNKNOWN_KERNEL", path=str(args.get("frame", "")), message=f"unknown kernel: {kernel_id}")
        )
        return r

    k = KERNELS[kernel_id]
    out, v, w, receipts = k.run(ctx, args)
    ok = len(v) == 0

    rep = Report(tool={"id": "fcx", "kernel": k.kid, "version": k.version}, ok=ok, violations=v, warnings=w, receipts=receipts)
    rep.receipts["output.sha256"] = sha256_text(stable_json(out))
    return rep


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="fcx", description="framecodex tool-of-tools (kernelized)")
    ap.add_argument("--repo-root", default=str(Path(".").resolve()))
    ap.add_argument("--out", default="", help="Write report.json to this path (optional)")
    ap.add_argument("--max-meta-depth", type=int, default=16)

    sub = ap.add_subparsers(dest="cmd", required=True)

    vgf0 = sub.add_parser("validate-gf0")
    vgf0.add_argument("--frame", required=True)

    vfr = sub.add_parser("validate-frame")
    vfr.add_argument("--frame", required=True)

    args = ap.parse_args(list(argv) if argv is not None else None)

    ctx = KernelCtx(repo_root=args.repo_root, budget=Budget(max_meta_depth=args.max_meta_depth), gamma={})

    if args.cmd == "validate-gf0":
        rep = run_kernel(ctx, "validate_gf0", {"frame": args.frame})
    elif args.cmd == "validate-frame":
        rep = run_kernel(ctx, "validate_frame", {"frame": args.frame})
    else:
        raise RuntimeError("unreachable")

    payload = stable_json(rep.to_obj())

    if args.out:
        write_text_deterministic(Path(args.out), payload)
    else:
        print(payload, end="")

    return 0 if rep.ok else 1
