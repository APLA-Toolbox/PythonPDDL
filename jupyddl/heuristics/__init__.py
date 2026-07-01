"""Heuristics and a name-based registry."""

from __future__ import annotations

from functools import partial

from .base import Heuristic
from .critical_path import CriticalPathHeuristic
from .delete_relaxation import FFHeuristic, HAddHeuristic, HMaxHeuristic
from .lmcut import LMCutHeuristic
from .simple import BlindHeuristic, GoalCountHeuristic

# name -> callable(task) -> Heuristic
HEURISTICS = {
    "blind": BlindHeuristic,
    "goalcount": GoalCountHeuristic,
    "hmax": HMaxHeuristic,
    "hadd": HAddHeuristic,
    "hff": FFHeuristic,
    "lmcut": LMCutHeuristic,
    "h1": partial(CriticalPathHeuristic, m=1),
    "h2": partial(CriticalPathHeuristic, m=2),
    "hm": CriticalPathHeuristic,
}


def make_heuristic(name: str, task) -> Heuristic:
    """Instantiate a heuristic by name (see :data:`HEURISTICS`)."""
    try:
        factory = HEURISTICS[name]
    except KeyError:
        raise ValueError(
            f"Unknown heuristic '{name}'. Available: {sorted(HEURISTICS)}"
        ) from None
    return factory(task)


__all__ = [
    "Heuristic",
    "BlindHeuristic",
    "GoalCountHeuristic",
    "HMaxHeuristic",
    "HAddHeuristic",
    "FFHeuristic",
    "LMCutHeuristic",
    "CriticalPathHeuristic",
    "HEURISTICS",
    "make_heuristic",
]
