from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from fcx import __version__
from fcx.gf0 import load_frame_yaml, validate_gf0_struct
from fcx.kernel import Budget, Kernel, KernelCtx
from fcx.profiles.specframe_k1 import PROFILE_VALIDATORS, infer_profile
from fcx.util import read_text, sha256_text, stable_json, write_text_deterministic
from fcx.validators.inline_markup_k1 import validate_inline_markup_k1
from fcx.validators.pub_tex_inline_v0 import validate_pub_tex_inline_v0
from fcx.validators.references import validate_references
from fcx.gates import gate_enforce_repo_law
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


def _k_validate_inline_markup(ctx: KernelCtx, args: Dict[str, Any]):
    v, w = validate_inline_markup_k1(ctx)
    receipts = {"kernel": sha256_text("validate_inline_markup@0.1.0")}
    return {}, v, w, receipts


def _k_validate_pub_tex(ctx: KernelCtx, args: Dict[str, Any]):
    v, w = validate_pub_tex_inline_v0(ctx)
    receipts = {"kernel": sha256_text("validate_pub_tex@0.1.0")}
    return {}, v, w, receipts


def _k_validate_references(ctx: KernelCtx, args: Dict[str, Any]):
    v, w = validate_references(ctx)
    receipts = {"kernel": sha256_text("validate_references@0.1.0")}
    return {}, v, w, receipts


def _k_gate_enforce_repo_law(ctx: KernelCtx, args: Dict[str, Any]):
    v, w = gate_enforce_repo_law(ctx)
    receipts = {"kernel": sha256_text("gate_enforce_repo_law@0.1.0")}
    return {}, v, w, receipts


KERNELS: Dict[str, Kernel] = {
    "validate_gf0": Kernel(kid="validate_gf0", version="0.1.0", run=_k_validate_gf0),
    "validate_frame": Kernel(kid="validate_frame", version="0.1.0", run=_k_validate_frame),
    "validate_inline_markup": Kernel(kid="validate_inline_markup", version="0.1.0", run=_k_validate_inline_markup),
    "validate_pub_tex": Kernel(kid="validate_pub_tex", version="0.1.0", run=_k_validate_pub_tex),
    "validate_references": Kernel(kid="validate_references", version="0.1.0", run=_k_validate_references),
    "gate_enforce_repo_law": Kernel(kid="gate_enforce_repo_law", version="0.1.0", run=_k_gate_enforce_repo_law),
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

    vim = sub.add_parser("validate-inline-markup")
    
    vpt = sub.add_parser("validate-pub-tex")
    
    vref = sub.add_parser("validate-references")

    glaw = sub.add_parser("gate-enforce-repo-law")

    args = ap.parse_args(list(argv) if argv is not None else None)

    ctx = KernelCtx(repo_root=args.repo_root, budget=Budget(max_meta_depth=args.max_meta_depth), gamma={})

    if args.cmd == "validate-gf0":
        rep = run_kernel(ctx, "validate_gf0", {"frame": args.frame})
    elif args.cmd == "validate-frame":
        rep = run_kernel(ctx, "validate_frame", {"frame": args.frame})
    elif args.cmd == "validate-inline-markup":
        rep = run_kernel(ctx, "validate_inline_markup", {})
    elif args.cmd == "validate-pub-tex":
        rep = run_kernel(ctx, "validate_pub_tex", {})
    elif args.cmd == "validate-references":
        rep = run_kernel(ctx, "validate_references", {})
    elif args.cmd == "gate-enforce-repo-law":
        rep = run_kernel(ctx, "gate_enforce_repo_law", {})
    else:
        raise RuntimeError("unreachable")

    payload = stable_json(rep.to_obj())

    if args.out:
        write_text_deterministic(Path(args.out), payload)
    else:
        print(payload, end="")

    return 0 if rep.ok else 1
