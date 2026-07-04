"""Search result and statistics containers shared by all planners."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SearchStats:
    """Bookkeeping collected while searching (for comparative analysis)."""

    expanded: int = 0
    generated: int = 0
    evaluated: int = 0  # heuristic evaluations
    reopened: int = 0
    deadends: int = 0
    runtime: float = 0.0

    def as_dict(self) -> dict:
        return {
            "expanded": self.expanded,
            "generated": self.generated,
            "evaluated": self.evaluated,
            "reopened": self.reopened,
            "deadends": self.deadends,
            "runtime": self.runtime,
        }


@dataclass
class SearchResult:
    """The outcome of a search: a plan (list of operators) plus statistics."""

    solved: bool
    plan: Optional[list] = None  # list[Operator]
    cost: Optional[int] = None
    stats: SearchStats = field(default_factory=SearchStats)

    @property
    def plan_length(self) -> Optional[int]:
        return None if self.plan is None else len(self.plan)

    def plan_names(self) -> Optional[list]:
        return None if self.plan is None else [op.name for op in self.plan]
