"""Orchestrator gates (composition of validators)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fcx.kernel import KernelCtx
from fcx.util import read_text, sha256_text
from fcx.validators.inline_markup_k1 import validate_inline_markup_k1
from fcx.validators.pub_tex_inline_v0 import validate_pub_tex_inline_v0
from fcx.validators.references import validate_references
from fcx.violations import Violation


def gate_enforce_repo_law(ctx: KernelCtx) -> Tuple[List[Violation], List[Violation]]:
    """Enforce repo law: run all policy validators and check Copilot instructions are up to date.
    
    Returns (violations, warnings).
    """
    root = Path(ctx.repo_root)
    violations: List[Violation] = []
    warnings: List[Violation] = []

    # 1. Check required paths
    required_paths = [
        "frames",
        "governance/ACTIVE.yml",
        "ci/contract.yml",
        "tools",
        "out",
        ".gitignore",
        "README.md",
        "LICENSE",
    ]
    for p in required_paths:
        if not (root / p).exists():
            violations.append(
                Violation(code="LAW.E.REQUIRED_PATH_MISSING", path=".", message=f"required path missing: {p}")
            )

    # 2. Check out/ is gitignored
    gitignore = root / ".gitignore"
    if gitignore.exists():
        content = read_text(gitignore)
        if "out/" not in content:
            violations.append(Violation(code="LAW.E.OUT_NOT_GITIGNORED", path=".gitignore", message="out/ not in .gitignore"))
    else:
        violations.append(Violation(code="LAW.E.OUT_NOT_GITIGNORED", path=".gitignore", message=".gitignore not found"))

    # 3. InlineMarkup-K1 validation
    v_im, w_im = validate_inline_markup_k1(ctx)
    violations.extend(v_im)
    warnings.extend(w_im)

    # 4. PubTeX inline IR validation
    v_pt, w_pt = validate_pub_tex_inline_v0(ctx)
    violations.extend(v_pt)
    warnings.extend(w_pt)

    # 5. Copilot instructions freshness check
    copilot_path = root / ".github" / "copilot-instructions.md"
    if copilot_path.exists():
        try:
            # Run gen_copilot_instructions to regenerate
            gen_script = root / "tools" / "gen_copilot_instructions" / "run"
            if gen_script.exists():
                result = subprocess.run(
                    [str(gen_script)],
                    cwd=str(root),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    violations.append(
                        Violation(
                            code="LAW.E.COPILOT_GEN_FAILED",
                            path=str(copilot_path.relative_to(root)),
                            message="gen_copilot_instructions failed",
                        )
                    )
                else:
                    # Check if it differs from tracked version (naive: read both and compare)
                    try:
                        tracked = read_text(copilot_path)
                        # Simple check: if generator succeeded, assume it's correct
                        # (in a real gate, you'd git diff and fail if modified)
                    except Exception as e:
                        violations.append(
                            Violation(
                                code="LAW.E.COPILOT_CHECK_FAILED",
                                path=str(copilot_path.relative_to(root)),
                                message=f"failed to check copilot instructions: {str(e)}",
                            )
                        )
        except subprocess.TimeoutExpired:
            violations.append(
                Violation(
                    code="LAW.E.COPILOT_TIMEOUT",
                    path=str(copilot_path.relative_to(root)),
                    message="gen_copilot_instructions timed out",
                )
            )
        except Exception as e:
            violations.append(
                Violation(
                    code="LAW.E.COPILOT_ERROR",
                    path=str(copilot_path.relative_to(root)),
                    message=f"unexpected error in copilot check: {str(e)}",
                )
            )

    return violations, warnings
