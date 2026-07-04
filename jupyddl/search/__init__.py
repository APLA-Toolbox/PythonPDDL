"""Search algorithms and a name-based planner registry."""

from .base import Planner, best_first
from .best_first_planners import (
    AStarSearch,
    GreedyBestFirstSearch,
    UniformCostSearch,
    WeightedAStarSearch,
)
from .enforced_hill_climbing import EnforcedHillClimbing
from .ida_star import IDAStarSearch
from .node import SearchNode, extract_plan
from .result import SearchResult, SearchStats
from .uninformed import (
    BreadthFirstSearch,
    DepthFirstSearch,
    IterativeDeepeningSearch,
)

# name -> zero-argument factory returning a fresh Planner instance.
PLANNERS = {
    "bfs": BreadthFirstSearch,
    "dfs": DepthFirstSearch,
    "iddfs": IterativeDeepeningSearch,
    "dijkstra": UniformCostSearch,
    "gbfs": GreedyBestFirstSearch,
    "astar": AStarSearch,
    "wastar": WeightedAStarSearch,
    "idastar": IDAStarSearch,
    "ehc": EnforcedHillClimbing,
}


def make_planner(name: str, **kwargs) -> Planner:
    """Instantiate a planner by name (see :data:`PLANNERS`)."""
    try:
        factory = PLANNERS[name]
    except KeyError:
        raise ValueError(
            f"Unknown planner '{name}'. Available: {sorted(PLANNERS)}"
        ) from None
    return factory(**kwargs)


__all__ = [
    "Planner",
    "best_first",
    "AStarSearch",
    "GreedyBestFirstSearch",
    "UniformCostSearch",
    "WeightedAStarSearch",
    "EnforcedHillClimbing",
    "IDAStarSearch",
    "BreadthFirstSearch",
    "DepthFirstSearch",
    "IterativeDeepeningSearch",
    "SearchNode",
    "SearchResult",
    "SearchStats",
    "extract_plan",
    "PLANNERS",
    "make_planner",
]
