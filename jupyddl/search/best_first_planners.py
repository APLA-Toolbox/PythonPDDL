"""Best-first planners defined by their priority function over ``(g, h)``."""

from __future__ import annotations

from .base import Planner, best_first
from .result import SearchResult


class UniformCostSearch(Planner):
    """Dijkstra's algorithm: priority = g. Cost-optimal, uninformed."""

    name = "dijkstra"
    optimal = True

    def search(self, task, heuristic=None) -> SearchResult:
        return best_first(task, lambda g, h: g, heuristic=None)


class GreedyBestFirstSearch(Planner):
    """Greedy best-first: priority = h. Fast but not optimal."""

    name = "gbfs"
    requires_heuristic = True

    def search(self, task, heuristic=None) -> SearchResult:
        return best_first(task, lambda g, h: h, heuristic=heuristic)


class AStarSearch(Planner):
    """A*: priority = g + h. Cost-optimal with an admissible heuristic."""

    name = "astar"
    requires_heuristic = True
    optimal = True

    def search(self, task, heuristic=None) -> SearchResult:
        return best_first(task, lambda g, h: g + h, heuristic=heuristic)


class WeightedAStarSearch(Planner):
    """Weighted A*: priority = g + w * h. Bounded-suboptimal for w > 1."""

    name = "wastar"
    requires_heuristic = True

    def __init__(self, weight: float = 2.0):
        self.weight = weight

    def search(self, task, heuristic=None) -> SearchResult:
        w = self.weight
        return best_first(task, lambda g, h: g + w * h, heuristic=heuristic)
