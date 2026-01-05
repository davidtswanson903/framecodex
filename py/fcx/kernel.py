from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from fcx.violations import Violation


@dataclass(frozen=True)
class Budget:
    seconds: Optional[int] = None
    max_meta_depth: int = 16


@dataclass(frozen=True)
class KernelCtx:
    repo_root: str
    budget: Budget
    gamma: Dict[str, str] = field(default_factory=dict)


KernelFn = Callable[[KernelCtx, Dict[str, Any]], Tuple[Dict[str, Any], List[Violation], List[Violation], Dict[str, str]]]


@dataclass(frozen=True)
class Kernel:
    kid: str
    version: str
    run: KernelFn
