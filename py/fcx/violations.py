from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Violation:
    code: str
    path: str
    node_id: Optional[str] = None
    edge_id: Optional[str] = None
    message: str = ""


@dataclass
class Report:
    tool: Dict[str, str]
    ok: bool
    violations: List[Violation] = field(default_factory=list)
    warnings: List[Violation] = field(default_factory=list)
    receipts: Dict[str, str] = field(default_factory=dict)

    def to_obj(self) -> Dict[str, Any]:
        return {
            "tool": self.tool,
            "ok": self.ok,
            "violations": [asdict(v) for v in self.violations],
            "warnings": [asdict(v) for v in self.warnings],
            "receipts": dict(sorted(self.receipts.items(), key=lambda kv: kv[0])),
        }
